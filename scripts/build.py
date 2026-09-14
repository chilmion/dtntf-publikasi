#!/usr/bin/env python3
"""
Scraper profil dosen DTNTF — sumber tunggal: SINTA (kemdiktisaintek).

SINTA sudah mengagregasi Scopus, Garuda, dan Google Scholar dalam satu profil,
jadi tidak perlu menyentuh situs Scopus (yang melarang scraping) sama sekali.

Yang diambil per dosen:
  - identitas, afiliasi, program studi, subject
  - skor SINTA overall & 3 tahun
  - tabel metrik: artikel, sitasi, cited document, h-index, i10, g-index
    untuk Scopus dan Google Scholar
  - daftar publikasi Scopus (judul, jurnal, kuartil, urutan penulis, tahun, sitasi)
  - daftar publikasi Garuda

Hanya pustaka standar Python — tidak perlu pip install apa pun.

Pakai:
    python3 scripts/build.py                    # semua dosen di dosen.csv
    python3 scripts/build.py faridah,widya-rosita   # sebagian saja
    python3 scripts/build.py --periksa 6010146      # diagnostik satu profil
"""

import csv
import html as html_mod
import os
import json
import pathlib
import random
import re
import sys
import time
import urllib.error
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
SINTA = "https://sinta.kemdiktisaintek.go.id"

# Jeda antar request. Jangan diturunkan — ini yang membuat scraper tidak
# dianggap serangan dan tidak membuat IP diblokir.
JEDA = (2.5, 5.0)
MAKS_HALAMAN = 25        # pengaman; 1 halaman = 20 artikel

# Tab profil SINTA yang ditarik: (parameter ?view=, label sumber, kategori)
VIEWS = [
    ("scopus",      "scopus",     "Scopus"),
    ("garuda",      "garuda",     "Garuda"),
    ("books",       "buku",       "Buku"),
    ("iprs",        "paten",      "Paten & HKI"),
    ("services",    "ppm",        "Pengabdian"),
    ("researches",  "penelitian", "Penelitian"),
]

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")


# ---------------------------------------------------------------- pengambilan

def ambil(url, tries=3):
    """GET satu halaman. Mengembalikan teks HTML atau None."""
    for attempt in range(tries):
        try:
            req = urllib.request.Request(url, headers={
                "User-Agent": UA,
                "Accept": "text/html,application/xhtml+xml",
                "Accept-Language": "id-ID,id;q=0.9,en;q=0.8",
            })
            with urllib.request.urlopen(req, timeout=45) as r:
                return r.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            if e.code in (403, 429):
                tunggu = 30 * (attempt + 1)
                print(f"      ! diblokir sementara ({e.code}); tunggu {tunggu}s", file=sys.stderr)
                time.sleep(tunggu)
            elif e.code == 404:
                return None
            else:
                time.sleep(5)
        except Exception as e:
            print(f"      ! {e}", file=sys.stderr)
            time.sleep(5)
    return None


def santai():
    time.sleep(random.uniform(*JEDA))


# ---------------------------------------------------------------- parsing

def bersih(s):
    """Buang tag, rapikan entitas dan spasi."""
    s = re.sub(r"<[^>]+>", " ", s or "")
    return re.sub(r"\s+", " ", html_mod.unescape(s)).strip()


def angka(s):
    s = (s or "").strip().replace(".", "").replace(",", ".")
    try:
        return float(s) if "." in s else int(s)
    except ValueError:
        return None


def parse_profil(h):
    """Metrik dan identitas dari halaman profil SINTA."""
    d = {}

    m = re.search(r'<h3>\s*<a[^>]*>(.*?)</a>', h, re.S)
    d["nama_sinta"] = bersih(m.group(1)) if m else None

    m = re.search(r'href="[^"]*/affiliations/profile/\d+"[^>]*>(.*?)</a>', h, re.S)
    d["afiliasi"] = bersih(m.group(1)) if m else None

    m = re.search(r'href="[^"]*/departments/profile/[^"]*"[^>]*>(.*?)</a>', h, re.S)
    d["prodi"] = bersih(m.group(1)) if m else None

    m = re.search(r'<img\s+src="([^"]+)"[^>]*alt="avatar"', h)
    d["foto"] = html_mod.unescape(m.group(1)) if m else None

    m = re.search(r'<ul class="subject-list">(.*?)</ul>', h, re.S)
    d["subjects"] = ([bersih(x) for x in re.findall(r'<li>(.*?)</li>', m.group(1), re.S)]
                     if m else [])

    # skor: pasangan <div class="pr-num">…</div><div class="pr-txt">…</div>
    skor = {}
    for num, txt in re.findall(
            r'<div class="pr-num">(.*?)</div>\s*<div class="pr-txt">(.*?)</div>', h, re.S):
        skor[bersih(txt)] = angka(bersih(num))
    d["skor"] = {
        "overall": skor.get("SINTA Score Overall"),
        "tiga_tahun": skor.get("SINTA Score 3Yr"),
        "afiliasi": skor.get("Affil Score"),
        "afiliasi_tiga_tahun": skor.get("Affil Score 3Yr"),
    }

    # tabel metrik Scopus / GScholar / WOS
    metrik = {"scopus": {}, "scholar": {}, "wos": {}}
    m = re.search(r'<table[^>]*stat-table[^>]*>(.*?)</table>', h, re.S)
    if m:
        kunci = {"Article": "artikel", "Citation": "sitasi",
                 "Cited Document": "dokumen_disitasi", "H-Index": "hindex",
                 "i10-Index": "i10index", "G-Index": "gindex"}
        for baris in re.findall(r'<tr>(.*?)</tr>', m.group(1), re.S):
            sel = re.findall(r'<t[dh][^>]*>(.*?)</t[dh]>', baris, re.S)
            if len(sel) < 3:
                continue
            label = kunci.get(bersih(sel[0]))
            if not label:
                continue
            metrik["scopus"][label] = angka(bersih(sel[1]))
            metrik["scholar"][label] = angka(bersih(sel[2]))
            if len(sel) > 3:
                metrik["wos"][label] = angka(bersih(sel[3]))
    if not metrik["wos"]:
        metrik.pop("wos")
    d["metrik"] = metrik
    return d


def parse_artikel(h, sumber):
    """Semua .ar-list-item pada satu halaman."""
    hasil = []
    for blok in re.findall(r'<div class="ar-list-item[^"]*">(.*?)(?=<div class="ar-list-item|\Z)',
                           h, re.S):
        m = re.search(r'<div class="ar-title">\s*<a[^>]*href="([^"]*)"[^>]*>(.*?)</a>', blok, re.S)
        if not m:
            m2 = re.search(r'<div class="ar-title">(.*?)</div>', blok, re.S)
            if not m2:
                continue
            url, judul = None, bersih(m2.group(1))
        else:
            url, judul = html_mod.unescape(m.group(1)), bersih(m.group(2))
        if not judul:
            continue

        def cari(pola):
            x = re.search(pola, blok, re.S)
            return bersih(x.group(1)) if x else None

        kuartil = cari(r'class="ar-quartile"[^>]*>(.*?)</a>')
        tahun = cari(r'class="ar-year"[^>]*>(.*?)</a>')
        sitasi = cari(r'class="ar-cited"[^>]*>(.*?)</a>')
        urutan = cari(r'>\s*Author Order\s*:\s*(.*?)</a>')
        kreator = cari(r'>\s*Creator\s*:\s*(.*?)</a>')

        hasil.append({
            "judul": judul,
            "url": url,
            "sumber": sumber,
            "venue": cari(r'class="ar-pub"[^>]*>(.*?)</a>'),
            "kuartil": (re.sub(r"\s*as\s+.*$", "", kuartil).strip() if kuartil else None),
            "jenis_venue": (kuartil.split(" as ", 1)[1].strip()
                            if kuartil and " as " in kuartil else None),
            "tahun": angka(re.sub(r"\D", "", tahun or "")),
            "sitasi": angka(re.sub(r"\D", "", sitasi or "")) or 0,
            "urutan_penulis": urutan,
            "kreator": kreator,
        })
    return hasil


def ambil_semua_artikel(sinta_id, view, sumber):
    """Loop halaman sampai habis atau berulang."""
    semua, terlihat = [], set()
    for hal in range(1, MAKS_HALAMAN + 1):
        url = f"{SINTA}/authors/profile/{sinta_id}/?view={view}&page={hal}"
        h = ambil(url)
        if not h:
            break
        batch = parse_artikel(h, sumber)
        if not batch:
            break
        baru = [a for a in batch if a["judul"] not in terlihat]
        if not baru:
            break                       # halaman mengulang isi yang sama
        for a in baru:
            terlihat.add(a["judul"])
        semua.extend(baru)
        print(f"      {sumber} hal.{hal}: +{len(baru)}")
        santai()
    return semua


def kategori(a):
    """Kelompok yang dipakai di halaman departemen."""
    if a["sumber"] == "scopus":
        jv = (a.get("jenis_venue") or "").lower()
        if "conference" in jv or "proceeding" in jv:
            return "Prosiding Internasional"
        if "book" in jv:
            return "Book Chapter / Book Series"
        return "Jurnal Internasional"
    return {"garuda": "Jurnal Nasional", "buku": "Buku",
            "paten": "Paten & HKI", "ppm": "Pengabdian kepada Masyarakat",
            "penelitian": "Penelitian"}.get(a["sumber"], "Lainnya")


URUT_KATEGORI = ["Jurnal Internasional", "Prosiding Internasional",
                 "Book Chapter / Book Series", "Jurnal Nasional", "Buku",
                 "Paten & HKI", "Penelitian", "Pengabdian kepada Masyarakat", "Lainnya"]


# ---------------------------------------------------------------- perakitan

def hitung_hindex(sitasi):
    s = sorted(sitasi, reverse=True)
    h = 0
    for i, c in enumerate(s, 1):
        if c >= i:
            h = i
        else:
            break
    return h


def rakit(row, profil, artikel):
    sinta_id = row["sinta_id"].strip()
    m = profil.get("metrik", {})
    sc, gs = m.get("scopus", {}), m.get("scholar", {})

    ilmiah = [a for a in artikel if a["sumber"] in ("scopus", "garuda", "buku")]
    per_tahun = {}
    for a in ilmiah:
        if a["tahun"]:
            e = per_tahun.setdefault(a["tahun"], {"tahun": a["tahun"], "publikasi": 0, "sitasi": 0})
            e["publikasi"] += 1
            e["sitasi"] += a["sitasi"] or 0

    kuartil = {}
    for a in artikel:
        if a["sumber"] == "scopus" and a["kuartil"]:
            kuartil[a["kuartil"]] = kuartil.get(a["kuartil"], 0) + 1

    venue = {}
    for a in ilmiah:
        if a["venue"]:
            venue[a["venue"]] = venue.get(a["venue"], 0) + 1

    per_sumber = {}
    for a in artikel:
        per_sumber[a["sumber"]] = per_sumber.get(a["sumber"], 0) + 1
    n_scopus = per_sumber.get("scopus", 0)
    n_garuda = per_sumber.get("garuda", 0)

    return {
        "slug": row["slug"].strip(),
        "sinta_id": sinta_id,
        "nama": row.get("nama", "").strip() or profil.get("nama_sinta"),
        "nama_sinta": profil.get("nama_sinta"),
        "gelar": row.get("gelar", "").strip() or None,
        "jabatan": row.get("jabatan", "").strip() or None,
        "email": row.get("email", "").strip() or None,
        "prodi": profil.get("prodi"),
        "afiliasi": profil.get("afiliasi"),
        "foto_url": row.get("foto_url", "").strip() or profil.get("foto"),
        "diperbarui": time.strftime("%Y-%m-%dT%H:%M:%S+07:00"),
        "tautan": {
            "sinta": f"{SINTA}/authors/profile/{sinta_id}",
            "scopus": (f"https://www.scopus.com/authid/detail.uri?authorId={row['scopus_id'].strip()}"
                       if row.get("scopus_id", "").strip() else None),
            "garuda": f"{SINTA}/authors/profile/{sinta_id}/?view=garuda",
            "scholar": (f"https://scholar.google.com/citations?user={row['scholar_id'].strip()}"
                        if row.get("scholar_id", "").strip() else None),
        },
        "skor": profil.get("skor", {}),
        "metrik": m,
        "ringkas": {
            "publikasi_scopus": sc.get("artikel") if sc.get("artikel") is not None else n_scopus,
            "publikasi_garuda": n_garuda,
            "sitasi_scopus": sc.get("sitasi"),
            "sitasi_scholar": gs.get("sitasi"),
            "hindex_scopus": sc.get("hindex"),
            "hindex_scholar": gs.get("hindex"),
            "hindex_terdaftar": hitung_hindex([a["sitasi"] or 0 for a in artikel]),
            "paten": per_sumber.get("paten", 0),
            "ppm": per_sumber.get("ppm", 0),
            "buku": per_sumber.get("buku", 0),
            "penelitian": per_sumber.get("penelitian", 0),
        },
        "per_sumber": per_sumber,
        "subjects": profil.get("subjects", []),
        "per_tahun": sorted(per_tahun.values(), key=lambda x: x["tahun"]),
        "kuartil": [{"nama": k, "jumlah": v}
                    for k, v in sorted(kuartil.items(), key=lambda kv: kv[0])],
        "venue_teratas": [{"nama": k, "jumlah": v}
                          for k, v in sorted(venue.items(), key=lambda kv: -kv[1])[:10]],
        "publikasi": sorted([dict(a, kategori=kategori(a)) for a in artikel],
                            key=lambda a: (-(a["tahun"] or 0), -(a["sitasi"] or 0))),
    }


def periksa(sinta_id):
    """Cek satu per satu tab SINTA dan laporkan apa yang terbaca.

    Dipakai untuk memastikan parser cocok, terutama tab iprs/services/
    books/researches yang strukturnya belum diverifikasi.
    """
    print(f"Memeriksa profil SINTA {sinta_id}\n")
    h = ambil(f"{SINTA}/authors/profile/{sinta_id}")
    if not h:
        print("  profil tidak bisa diambil — cek koneksi atau ID"); return 1
    pr = parse_profil(h)
    print(f"  nama    : {pr['nama_sinta']}")
    print(f"  prodi   : {pr['prodi']}")
    print(f"  subject : {', '.join(pr['subjects']) or '(kosong)'}")
    print(f"  skor    : {pr['skor']}")
    for src, m in (pr.get("metrik") or {}).items():
        print(f"  metrik {src:8s}: {m}")
    santai()

    for view, sumber, label in VIEWS:
        h = ambil(f"{SINTA}/authors/profile/{sinta_id}/?view={view}&page=1")
        if not h:
            print(f"\n  [{label}] halaman tidak terbaca"); continue
        a = parse_artikel(h, sumber)
        n_item = h.count('class="ar-list-item')
        print(f"\n  [{label}] ?view={view} → {n_item} blok di HTML, {len(a)} terbaca parser")
        if a:
            c = a[0]
            print(f"    contoh : {(c['judul'] or '')[:70]}")
            print(f"    tahun={c['tahun']} venue={c['venue']} kuartil={c['kuartil']} "
                  f"sitasi={c['sitasi']} kategori={kategori(c)}")
            kosong = [k for k in ("judul", "tahun") if not c.get(k)]
            if kosong:
                print(f"    !! field kosong: {', '.join(kosong)} — parser perlu disesuaikan")
        elif n_item:
            print("    !! ada blok di HTML tapi parser tidak membacanya — kirim HTML ini")
        else:
            print("    (tab ini memang kosong untuk dosen tsb, atau butuh login)")
        santai()
    print("\nSelesai memeriksa.")
    return 0


def main():
    if len(sys.argv) > 2 and sys.argv[1] == "--periksa":
        return periksa(sys.argv[2].strip())

    DATA.mkdir(exist_ok=True)
    with open(ROOT / "dosen.csv", newline="", encoding="utf-8") as f:
        rows = [r for r in csv.DictReader(f) if (r.get("sinta_id") or "").strip()]

    # Argumen: daftar slug atau ID SINTA dipisah koma, mis.
    #   python3 scripts/build.py faridah,widya-rosita
    # Bisa juga lewat env BETA_DOSEN (dipakai GitHub Actions).
    pilih = (sys.argv[1] if len(sys.argv) > 1 else os.environ.get("BETA_DOSEN", "")).strip()
    if pilih.startswith("-"):
        pilih = ""
    if pilih:
        ingin = {x.strip().lower() for x in pilih.split(",") if x.strip()}
        rows = [r for r in rows
                if r["slug"].strip().lower() in ingin or r["sinta_id"].strip() in ingin]
        if not rows:
            print(f"Tidak ada dosen cocok dengan: {pilih}", file=sys.stderr)
            return

    index, gagal = [], []
    for i, row in enumerate(rows, 1):
        sid, slug = row["sinta_id"].strip(), row["slug"].strip()
        print(f"[{i}/{len(rows)}] {slug} (SINTA {sid})")

        h = ambil(f"{SINTA}/authors/profile/{sid}")
        if not h or "ar-list-item" not in h and "stat-table" not in h:
            print("      ! profil tidak terbaca, dilewati")
            gagal.append(slug)
            continue
        profil = parse_profil(h)
        santai()

        artikel = []
        for view, sumber, _label in VIEWS:
            artikel += ambil_semua_artikel(sid, view, sumber)
            santai()

        rek = rakit(row, profil, artikel)
        (DATA / f"{slug}.json").write_text(
            json.dumps(rek, ensure_ascii=False, indent=1), encoding="utf-8")

        index.append({
            "slug": slug, "sinta_id": sid,
            "nama": rek["nama"], "gelar": rek["gelar"], "jabatan": rek["jabatan"],
            "foto_url": rek["foto_url"], "prodi": rek["prodi"],
            "skor_sinta": (rek["skor"] or {}).get("overall"),
            "publikasi": len(rek["publikasi"]),
            "sitasi_scopus": rek["ringkas"]["sitasi_scopus"],
            "sitasi_scholar": rek["ringkas"]["sitasi_scholar"],
            "hindex_scopus": rek["ringkas"]["hindex_scopus"],
        })
        print(f"      ✓ {len(rek['publikasi'])} publikasi")
        santai()

    # Gabung dengan index lama supaya build sebagian tidak menghapus dosen lain.
    lama = {}
    f_index = DATA / "index.json"
    if f_index.exists():
        try:
            for e in json.loads(f_index.read_text())["dosen"]:
                lama[e["slug"]] = e
        except Exception:
            pass
    for e in index:
        lama[e["slug"]] = e
    index = list(lama.values())

    index.sort(key=lambda x: (x["nama"] or "").lower())
    (DATA / "index.json").write_text(json.dumps(
        {"diperbarui": time.strftime("%Y-%m-%d"), "dosen": index},
        ensure_ascii=False, indent=1), encoding="utf-8")

    print(f"\nSelesai: {len(index)} berhasil, {len(gagal)} gagal"
          + (f" → {', '.join(gagal)}" if gagal else ""))

    # Bangun ulang agregat departemen dari seluruh JSON yang ada.
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
    import agregat
    agregat.main()


if __name__ == "__main__":
    sys.exit(main() or 0)
