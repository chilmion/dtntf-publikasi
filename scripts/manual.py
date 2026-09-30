#!/usr/bin/env python3
"""
Gabungkan luaran yang diisi MANUAL (dari jurusan) ke data/<slug>.json.

Sumber: manual/luaran.xlsx (dipakai kalau ada) atau manual/luaran.csv.
Kolom: lihat manual/templat-luaran.xlsx dan README.

Aman dijalankan berulang: entri manual lama (bertanda "manual": true) dibuang
dulu, lalu dipasang ulang dari berkas. Entri yang judulnya sudah ada dari SINTA
untuk dosen yang sama dilewati (data SINTA yang dipakai).

Dijalankan setelah scripts/build.py; di akhir, agregat departemen dibangun ulang.
    python3 scripts/manual.py
Stdlib saja — .xlsx dibaca langsung lewat zipfile + XML.
"""

import csv
import io
import json
import pathlib
import re
import sys
import zipfile
import xml.etree.ElementTree as ET

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
MANUAL = ROOT / "manual"
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import agregat  # noqa: E402

KOLOM = ["dosen", "jenis", "judul", "tahun", "penerbit_jurnal", "tautan",
         "kuartil", "akreditasi", "jenis_paten", "dana", "isbn", "sitasi"]

# jenis (huruf kecil) → (kategori resmi, kunci sumber untuk widget profil)
JENIS = {
    "jurnal internasional": ("Jurnal Internasional", "ilmiah"),
    "prosiding internasional": ("Prosiding Internasional", "ilmiah"),
    "book chapter": ("Book Chapter / Book Series", "ilmiah"),
    "book chapter / book series": ("Book Chapter / Book Series", "ilmiah"),
    "jurnal nasional": ("Jurnal Nasional", "ilmiah"),
    "buku": ("Buku", "buku"),
    "paten": ("Paten & HKI", "paten"),
    "hki": ("Paten & HKI", "paten"),
    "paten & hki": ("Paten & HKI", "paten"),
    "penelitian": ("Penelitian", "penelitian"),
    "pengabdian": ("Pengabdian kepada Masyarakat", "ppm"),
    "ppm": ("Pengabdian kepada Masyarakat", "ppm"),
    "pengabdian kepada masyarakat": ("Pengabdian kepada Masyarakat", "ppm"),
}

NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
      "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships"}


# ---------------------------------------------------------------- pembaca
def _kolom_ke_indeks(ref):
    huruf = re.match(r"[A-Z]+", ref).group(0)
    n = 0
    for c in huruf:
        n = n * 26 + ord(c) - 64
    return n - 1


def baca_xlsx(path):
    """Baris-baris sheet pertama ('Luaran') sebagai list of list string."""
    with zipfile.ZipFile(path) as z:
        bersama = []
        if "xl/sharedStrings.xml" in z.namelist():
            for si in ET.fromstring(z.read("xl/sharedStrings.xml")).findall("m:si", NS):
                bersama.append("".join(t.text or "" for t in si.iter("{%s}t" % NS["m"])))
        wb = ET.fromstring(z.read("xl/workbook.xml"))
        rel = ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
        target = {r.get("Id"): r.get("Target") for r in rel}
        sheets = wb.find("m:sheets", NS).findall("m:sheet", NS)
        pilih = next((s for s in sheets if s.get("name", "").lower() == "luaran"), sheets[0])
        t = target[pilih.get("{%s}id" % NS["r"])].lstrip("/")
        if not t.startswith("xl/"):
            t = "xl/" + t
        baris = []
        for row in ET.fromstring(z.read(t)).iter("{%s}row" % NS["m"]):
            sel = []
            for c in row.findall("m:c", NS):
                i = _kolom_ke_indeks(c.get("r"))
                while len(sel) <= i:
                    sel.append("")
                tipe = c.get("t")
                if tipe == "inlineStr":
                    nilai = "".join(x.text or "" for x in c.iter("{%s}t" % NS["m"]))
                else:
                    v = c.find("m:v", NS)
                    nilai = v.text if v is not None and v.text is not None else ""
                    if tipe == "s" and nilai != "":
                        nilai = bersama[int(nilai)]
                    elif nilai.endswith(".0"):      # 2024 tersimpan sebagai "2024.0"
                        nilai = nilai[:-2]
                sel[i] = nilai
            baris.append(sel)
        return baris


def baca_csv(path):
    mentah = path.read_bytes()
    try:
        teks = mentah.decode("utf-8-sig")
    except UnicodeDecodeError:
        teks = mentah.decode("cp1252")
    try:  # Excel Indonesia sering memakai titik-koma
        dialek = csv.Sniffer().sniff(teks[:4000], delimiters=",;\t")
    except csv.Error:
        dialek = csv.excel
    return list(csv.reader(io.StringIO(teks), dialek))


def baca_berkas(path):
    """Baca .xlsx / .csv → list of dict (kunci = nama kolom huruf kecil, plus _baris)."""
    path = pathlib.Path(path)
    semua = baca_xlsx(path) if path.suffix.lower() == ".xlsx" else baca_csv(path)
    if not semua:
        return []
    kepala = [re.sub(r"\s+", "_", (h or "").strip().lower()) for h in semua[0]]
    hasil = []
    for no, sel in enumerate(semua[1:], start=2):
        rec = {k: (sel[i].strip() if i < len(sel) and sel[i] is not None else "")
               for i, k in enumerate(kepala) if k}
        if any(rec.values()):
            rec["_baris"] = no
            hasil.append(rec)
    return hasil


def baca_baris():
    for nama in ("luaran.xlsx", "luaran.csv"):
        p = MANUAL / nama
        if p.exists():
            print(f"Membaca {p.relative_to(ROOT)}")
            return baca_berkas(p)
    return None


# ---------------------------------------------------------------- gabung
def peta_dosen():
    """nama/slug dinormalisasi → slug"""
    p = {}
    with open(ROOT / "dosen.csv", newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            slug = r["slug"].strip()
            p[agregat.normal(slug.replace("-", " "))] = slug
            p[agregat.normal(r.get("nama") or "")] = slug
    return p


def validasi(baris):
    """→ (per_dosen {slug: [entri]}, masalah [str], jumlah_baris_valid)"""
    peta, masalah, per_dosen, valid = peta_dosen(), [], {}, 0
    for r in baris:
        no = r["_baris"]
        jenis = JENIS.get(re.sub(r"\s+", " ", r.get("jenis", "").lower()).strip())
        if not r.get("judul"):
            masalah.append(f"baris {no}: judul kosong"); continue
        if not jenis:
            masalah.append(f"baris {no}: jenis '{r.get('jenis','')}' tidak dikenal"); continue
        try:
            tahun = int(float(r.get("tahun", "")))
            assert 1950 <= tahun <= 2100
        except Exception:
            masalah.append(f"baris {no}: tahun '{r.get('tahun','')}' tidak valid"); continue
        try:
            sitasi = int(float(r["sitasi"])) if r.get("sitasi") else 0
        except ValueError:
            sitasi = 0

        slugs = []
        for nama in re.split(r"[;\n]", r.get("dosen", "")):
            if not nama.strip():
                continue
            s = peta.get(agregat.normal(nama.replace("-", " ")))
            if s: slugs.append(s)
            else: masalah.append(f"baris {no}: dosen '{nama.strip()}' tidak ada di dosen.csv")
        if not slugs:
            masalah.append(f"baris {no}: tidak ada dosen yang cocok"); continue

        kategori, sumber = jenis
        entri = {
            "judul": r["judul"], "url": r.get("tautan") or None, "sumber": sumber,
            "venue": r.get("penerbit_jurnal") or None, "tahun": tahun, "sitasi": sitasi,
            "urutan_penulis": None, "kreator": None,
            "kuartil": (r.get("kuartil") or None), "jenis_venue": None, "info": None,
            "akreditasi": r.get("akreditasi") or None,
            "jenis_paten": r.get("jenis_paten") or None,
            "dana": r.get("dana") or None, "isbn": r.get("isbn") or None,
            "kategori": kategori, "manual": True,
        }
        valid += 1
        for s in slugs:
            per_dosen.setdefault(s, []).append(entri)
    return per_dosen, masalah, valid


def main():
    baris = baca_baris()
    if baris is None:
        # tanpa berkas, entri manual lama tetap dibersihkan
        print("Tidak ada manual/luaran.xlsx atau manual/luaran.csv.")
        baris = []

    per_dosen, masalah, _ = validasi(baris)

    # tulis ke tiap data/<slug>.json (bersihkan entri manual lama dulu)
    ditambah = dilewati = 0
    for f in sorted(DATA.glob("*.json")):
        if f.name == "index.json":
            continue
        d = json.loads(f.read_text(encoding="utf-8"))
        asli = [a for a in d.get("publikasi") or [] if not a.get("manual")]
        ada = {agregat.normal(a.get("judul")) for a in asli}
        baru = []
        for e in per_dosen.get(d["slug"], []):
            if agregat.normal(e["judul"]) in ada:
                dilewati += 1
                print(f"  = {d['slug']}: '{e['judul'][:50]}' sudah ada dari SINTA, dilewati")
            else:
                baru.append(dict(e)); ditambah += 1
        if len(baru) or len(asli) != len(d.get("publikasi") or []):
            d["publikasi"] = asli + baru
            f.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")

    tanpa_data = [s for s in per_dosen if not (DATA / f"{s}.json").exists()]
    for s in tanpa_data:
        masalah.append(f"dosen '{s}' belum punya data/{s}.json (belum pernah di-scrape); entrinya belum dipasang")

    print(f"Manual: {ditambah} entri dipasang, {dilewati} dilewati (sudah ada dari SINTA)")
    for m in masalah:
        print("  ! " + m)
    agregat.main()
    return 0


if __name__ == "__main__":
    sys.exit(main())
