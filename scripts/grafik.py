#!/usr/bin/env python3
"""
Ambil data grafik "Summary" SINTA (Article Quartile, Research Output, dan
publikasi per tahun) dari skrip inline di halaman profil.

SINTA menggambar grafik itu dengan echarts lewat JavaScript, jadi datanya ada
di dalam <script>, bukan di elemen HTML. Modul ini mencari konfigurasi echarts
(pie / radar / line / bar) dan menerjemahkannya. Format persisnya belum pernah
dilihat langsung (sesi cloud tidak bisa membuka SINTA), maka:

  * ekstrak()  mencoba beberapa pola umum dan hanya mengembalikan yang lolos
               pemeriksaan kewajaran; kalau tidak ada yang cocok → {}.
  * diagnosa() menulis potongan skrip mentah ke berkas teks supaya polanya bisa
               dicocokkan dengan format asli.

Pakai sendiri:
    python3 scripts/grafik.py 6010146     # ambil profil, cetak hasil, tulis diagnostik-grafik.txt
"""

import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
_sudah_diagnosa = [False]


# ------------------------------------------------------- penerjemah literal JS
def _seimbang(t, i):
    """Indeks penutup untuk [ atau { di posisi i (menghormati string), atau -1."""
    buka, tutup = t[i], {"[": "]", "{": "}"}[t[i]]
    dalam, kutip, esc = 0, None, False
    for j in range(i, len(t)):
        c = t[j]
        if kutip:
            if esc: esc = False
            elif c == "\\": esc = True
            elif c == kutip: kutip = None
            continue
        if c in "'\"`":
            kutip = c
        elif c == buka:
            dalam += 1
        elif c == tutup:
            dalam -= 1
            if dalam == 0:
                return j
    return -1


def _buang_panggilan(s):
    """Ganti `function(...) {...}` dan `new X.Y(...)` (mis. LinearGradient) dengan null —
    keduanya ada di konfigurasi echarts SINTA dan bukan data."""
    for pola, tutup in ((r"\bfunction\s*\([^)]*\)\s*\{", "}"), (r"\bnew\s+[\w.$]+\s*\(", ")")):
        while True:
            m = re.search(pola, s)
            if not m:
                break
            i = m.end() - 1                       # posisi { atau (
            dalam, kutip, esc, j = 0, None, False, -1
            for k in range(i, len(s)):
                c = s[k]
                if kutip:
                    if esc: esc = False
                    elif c == "\\": esc = True
                    elif c == kutip: kutip = None
                    continue
                if c in "'\"`": kutip = c
                elif c == s[i]: dalam += 1
                elif c == tutup:
                    dalam -= 1
                    if dalam == 0:
                        j = k
                        break
            if j < 0:
                break
            s = s[:m.start()] + "null" + s[j + 1:]
    return s


def _js(s):
    """Literal JS sederhana → objek Python; None kalau tidak bisa."""
    s = _buang_panggilan(s)
    s = re.sub(r"/\*.*?\*/", "", s, flags=re.S)
    s = re.sub(r"(?m)^\s*//.*$", "", s)
    s = re.sub(r"'((?:[^'\\]|\\.)*)'", lambda m: json.dumps(m.group(1).replace("\\'", "'")), s)
    s = re.sub(r"([{,]\s*)([A-Za-z_$][\w$]*)\s*:", r'\1"\2":', s)
    s = re.sub(r",\s*([\]}])", r"\1", s)
    s = re.sub(r"\bundefined\b", "null", s)
    try:
        return json.loads(s)
    except Exception:
        return None


def _literal_setelah(t, pola, mulai=0):
    """Literal [..] atau {..} yang mengikuti `pola` (regex yang diakhiri ':' / '=')."""
    for m in re.finditer(pola, t[mulai:]):
        i = mulai + m.end()
        while i < len(t) and t[i] in " \t\r\n":
            i += 1
        if i < len(t) and t[i] in "[{":
            j = _seimbang(t, i)
            if j > 0:
                v = _js(t[i:j + 1])
                if v is not None:
                    yield m.start() + mulai, v


def _angka(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


# --------------------------------------------------------------- ekstraksi
def _skrip(html):
    return [s for s in re.findall(r"<script\b[^>]*>(.*?)</script>", html, re.S | re.I)
            if re.search(r"echarts|series|indicator", s)]


def _kuartil_valid(pasangan):
    nama = [n for n, _ in pasangan]
    return len(nama) >= 2 and sum(bool(re.match(r"(?i)^(q[1-4]|no[- ]?q)", n.strip())) for n in nama) >= 2


def _bersihkan_nama(n):
    return re.sub(r"\s*[:：]\s*\d+\s*$", "", str(n)).strip()


def ekstrak(html):
    """→ {'kuartil': [{nama,jumlah}], 'output': [...], 'per_tahun': [{tahun,jumlah}]} (yang ditemukan saja)"""
    hasil = {}
    for t in _skrip(html):
        # -- pie / donat: kuartil
        for pos, seri in _literal_setelah(t, r"\bseries\s*[:=]"):
            for s in (seri if isinstance(seri, list) else [seri]):
                if not isinstance(s, dict):
                    continue
                tipe = s.get("type")
                data = s.get("data")
                if tipe == "pie" and isinstance(data, list):
                    ps = [(_bersihkan_nama(d.get("name")), _angka(d.get("value")))
                          for d in data if isinstance(d, dict)]
                    ps = [(n, v) for n, v in ps if n and v is not None]
                    if _kuartil_valid(ps) and "kuartil" not in hasil:
                        hasil["kuartil"] = [{"nama": n, "jumlah": int(v)} for n, v in ps]
                elif tipe == "radar" and isinstance(data, list) and data:
                    # nama sumbu dari `indicator` terdekat sebelum series
                    ind = None
                    for _, v in _literal_setelah(t, r"\bindicator\s*[:=]"):
                        ind = v
                    nilai = data[0].get("value") if isinstance(data[0], dict) else data[0]
                    if isinstance(ind, list) and isinstance(nilai, list) and len(ind) == len(nilai):
                        ps = [(str(i.get("name", "")).strip(), _angka(v)) for i, v in zip(ind, nilai)
                              if isinstance(i, dict)]
                        if ps and all(n and v is not None for n, v in ps) and "output" not in hasil:
                            hasil["output"] = [{"nama": n, "jumlah": int(v)} for n, v in ps]
                elif tipe in ("line", "bar") and isinstance(data, list):
                    x = None
                    for p, v in _literal_setelah(t, r"\bxAxis\s*[:=]"):
                        if p < pos:
                            x = v
                    xs = (x.get("data") if isinstance(x, dict) else
                          x[0].get("data") if isinstance(x, list) and x and isinstance(x[0], dict) else None)
                    ys = [d.get("value") if isinstance(d, dict) else d for d in data]
                    if isinstance(xs, list) and len(xs) == len(ys) and \
                            all(re.fullmatch(r"(19|20)\d\d", str(a)) for a in xs) and "per_tahun" not in hasil:
                        pasang = [(int(a), _angka(b)) for a, b in zip(xs, ys)]
                        if all(b is not None for _, b in pasang):
                            hasil["per_tahun"] = [{"tahun": a, "jumlah": int(b)} for a, b in pasang]
    return hasil


# -------------------------------------------------------------- diagnostik
def diagnosa(html, sinta_id=""):
    """Teks laporan: potongan skrip terkait grafik + URL yang mencurigakan."""
    baris = [f"# Diagnostik grafik SINTA {sinta_id}", f"# ukuran halaman: {len(html)//1024} KB",
             f"# hasil ekstrak: {json.dumps(ekstrak(html), ensure_ascii=False)}", ""]
    urls = set(re.findall(r"""["'](/[^"'\s]*(?:ajax|json|chart|graph|api|summary)[^"'\s]*)["']""", html, re.I))
    baris.append("# URL kandidat sumber data (AJAX): " + (", ".join(sorted(urls)) or "-"))
    ada = _skrip(html)
    baris.append(f"# skrip inline dengan echarts/series/indicator: {len(ada)}\n")
    for n, s in enumerate(ada, 1):
        baris.append(f"===== SKRIP {n} ({len(s)} karakter; dipotong 12000) =====")
        baris.append(s[:12000])
        baris.append("")
    if not ada:
        baris.append("# Tidak ada skrip inline dengan echarts. Cari kata 'echarts' / 'Article Quartile' di")
        baris.append("# View Source, atau lihat tab Network (filter Fetch/XHR) saat halaman dimuat.")
        for m in re.finditer(r"<script[^>]+src=[\"']([^\"']+)", html):
            baris.append("# script src: " + m.group(1))
    return "\n".join(baris)


def simpan_diagnosa(html, sinta_id="", sekali=True):
    if sekali and _sudah_diagnosa[0]:
        return None
    _sudah_diagnosa[0] = True
    p = ROOT / "diagnostik-grafik.txt"
    p.write_text(diagnosa(html, sinta_id), encoding="utf-8")
    return p


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
    import build
    h = build.ambil(f"{build.SINTA}/authors/profile/{sys.argv[1].strip()}", lapor=True)
    if not h:
        sys.exit("Halaman tidak terbaca.")
    print(json.dumps(ekstrak(h), ensure_ascii=False, indent=1))
    print("Laporan mentah ditulis ke", simpan_diagnosa(h, sys.argv[1], sekali=False))
