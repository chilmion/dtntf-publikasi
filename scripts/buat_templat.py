#!/usr/bin/env python3
"""
Buat manual/templat-luaran.xlsx — templat Excel untuk diisi jurusan.

Sheet: Petunjuk (aturan + contoh), Luaran (yang diisi & dibaca script),
Daftar dosen (isi dropdown kolom dosen). Stdlib saja.
    python3 scripts/buat_templat.py
"""

import csv
import pathlib
import zipfile
from xml.sax.saxutils import escape

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "manual" / "templat-luaran.xlsx"

JENIS = ["Jurnal Internasional", "Prosiding Internasional", "Book Chapter",
         "Jurnal Nasional", "Buku", "Paten & HKI", "Penelitian", "Pengabdian"]
KEPALA = [("dosen", 30), ("jenis", 24), ("judul", 60), ("tahun", 8),
          ("penerbit_jurnal", 36), ("tautan", 34), ("kuartil", 9),
          ("akreditasi", 12), ("jenis_paten", 16), ("dana", 16),
          ("isbn", 18), ("sitasi", 8)]
BARIS_MAKS = 500

PETUNJUK = [
    ("PETUNJUK PENGISIAN — sheet 'Luaran'", 1),
    ("Isi satu baris per luaran di sheet 'Luaran'. Jangan ubah nama kolom di baris 1 dan jangan ubah nama sheet.", 0),
    ("", 0),
    ("Wajib: dosen, jenis, judul, tahun. Kolom lain boleh kosong.", 0),
    ("dosen  — nama dosen persis seperti di sheet 'Daftar dosen' (pilih dari dropdown). Kalau ditulis beberapa dosen DTNTF, pisahkan dengan titik-koma: Faridah; Widya Rosita", 0),
    ("jenis  — pilih dari dropdown: Jurnal Internasional, Prosiding Internasional, Book Chapter, Jurnal Nasional, Buku, Paten & HKI, Penelitian, Pengabdian", 0),
    ("judul  — judul lengkap luaran", 0),
    ("tahun  — 4 angka, mis. 2024", 0),
    ("penerbit_jurnal — nama jurnal / prosiding / penerbit / skema (untuk penelitian & pengabdian)", 0),
    ("tautan — alamat web (DOI, jurnal, dsb.) kalau ada; judul akan bisa diklik", 0),
    ("kuartil — Q1 / Q2 / Q3 / Q4 (hanya jurnal bereputasi Scopus)", 0),
    ("akreditasi — mis. Sinta 2 (jurnal nasional)", 0),
    ("jenis_paten — mis. Paten, Paten Sederhana, Hak Cipta (hanya Paten & HKI)", 0),
    ("dana — mis. Rp. 25.000.000 (Penelitian / Pengabdian)", 0),
    ("isbn — hanya untuk Buku", 0),
    ("sitasi — jumlah sitasi (angka), boleh kosong", 0),
    ("", 0),
    ("Contoh baris:", 1),
    ("Faridah | Jurnal Nasional | Rancang Bangun Sistem Monitoring ... | 2024 | Jurnal Teknofisika | https://doi.org/10.xxxx | | Sinta 3", 0),
    ("", 0),
    ("Catatan: luaran yang judulnya sudah ada di SINTA untuk dosen yang sama akan dilewati otomatis (tidak dobel).", 0),
    ("Simpan sebagai .xlsx lalu kirim ke pengelola web. Jangan hapus baris contoh di sheet ini; sheet 'Luaran' harus tetap kosong dari contoh.", 0),
]


def kol(i):
    s = ""
    i += 1
    while i:
        i, r = divmod(i - 1, 26)
        s = chr(65 + r) + s
    return s


def sel(ref, teks, gaya=0):
    return (f'<c r="{ref}" t="inlineStr" s="{gaya}"><is><t xml:space="preserve">'
            f'{escape(str(teks))}</t></is></c>')


def sheet(baris, lebar=None, ekstra="", beku=False):
    cols = ("<cols>" + "".join(
        f'<col min="{i+1}" max="{i+1}" width="{w}" customWidth="1"/>'
        for i, w in enumerate(lebar)) + "</cols>") if lebar else ""
    pane = ('<sheetViews><sheetView workbookViewId="0"><pane ySplit="1" topLeftCell="A2" '
            'activePane="bottomLeft" state="frozen"/></sheetView></sheetViews>') if beku else ""
    data = "".join(f'<row r="{n}">{"".join(cs)}</row>' for n, cs in enumerate(baris, 1))
    return ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
            f'{pane}{cols}<sheetData>{data}</sheetData>{ekstra}</worksheet>')


def main():
    with open(ROOT / "dosen.csv", newline="", encoding="utf-8") as f:
        nama = sorted({r["nama"].strip() for r in csv.DictReader(f) if r["nama"].strip()},
                      key=str.lower)

    petunjuk = sheet([[sel(f"A{n}", t, 1 if tebal else 0)] for n, (t, tebal) in
                      enumerate(PETUNJUK, 1)], lebar=[150])
    luaran = sheet([[sel(f"{kol(i)}1", k, 1) for i, (k, _) in enumerate(KEPALA)]],
                   lebar=[w for _, w in KEPALA], beku=True, ekstra=(
        '<dataValidations count="2">'
        f'<dataValidation type="list" allowBlank="1" showErrorMessage="1" sqref="B2:B{BARIS_MAKS}">'
        f'<formula1>"{escape(",".join(JENIS))}"</formula1></dataValidation>'
        f'<dataValidation type="list" errorStyle="warning" allowBlank="1" showErrorMessage="1" '
        f'errorTitle="Dosen" error="Nama tidak ada di daftar. Untuk beberapa dosen, pisahkan dengan titik-koma." '
        f'sqref="A2:A{BARIS_MAKS}"><formula1>\'Daftar dosen\'!$A$2:$A${len(nama)+1}</formula1>'
        '</dataValidation></dataValidations>'))
    daftar = sheet([[sel("A1", "nama", 1)]] + [[sel(f"A{n}", x)] for n, x in enumerate(nama, 2)],
                   lebar=[36])

    parts = {
        "[Content_Types].xml": '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
            '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
            '<Default Extension="xml" ContentType="application/xml"/>'
            '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>'
            + "".join(f'<Override PartName="/xl/worksheets/sheet{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>' for i in (1, 2, 3))
            + '<Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/></Types>',
        "_rels/.rels": '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/></Relationships>',
        "xl/workbook.xml": '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
            'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><sheets>'
            '<sheet name="Petunjuk" sheetId="1" r:id="rId1"/>'
            '<sheet name="Luaran" sheetId="2" r:id="rId2"/>'
            '<sheet name="Daftar dosen" sheetId="3" r:id="rId3"/></sheets></workbook>',
        "xl/_rels/workbook.xml.rels": '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            + "".join(f'<Relationship Id="rId{i}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet{i}.xml"/>' for i in (1, 2, 3))
            + '<Relationship Id="rId4" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/></Relationships>',
        "xl/styles.xml": '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
            '<fonts count="2"><font><sz val="11"/><name val="Calibri"/></font>'
            '<font><b/><sz val="11"/><name val="Calibri"/></font></fonts>'
            '<fills count="2"><fill><patternFill patternType="none"/></fill>'
            '<fill><patternFill patternType="gray125"/></fill></fills>'
            '<borders count="1"><border><left/><right/><top/><bottom/><diagonal/></border></borders>'
            '<cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>'
            '<cellXfs count="2"><xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/>'
            '<xf numFmtId="0" fontId="1" fillId="0" borderId="0" xfId="0" applyFont="1"/></cellXfs></styleSheet>',
        "xl/worksheets/sheet1.xml": petunjuk,
        "xl/worksheets/sheet2.xml": luaran,
        "xl/worksheets/sheet3.xml": daftar,
    }
    OUT.parent.mkdir(exist_ok=True)
    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
        for n, isi in parts.items():
            z.writestr(n, isi)
    print(f"Tertulis {OUT.relative_to(ROOT)} ({len(nama)} dosen di dropdown)")


if __name__ == "__main__":
    main()
