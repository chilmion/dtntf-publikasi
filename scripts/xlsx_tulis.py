#!/usr/bin/env python3
"""
Penulis .xlsx sederhana (stdlib: zipfile + XML) untuk templat/berkas isian di manual/.

    from xlsx_tulis import tulis_xlsx
    tulis_xlsx(path, [{"nama": "Pendidikan", "kepala": ["dosen", "tahun", "keterangan"],
                       "lebar": [30, 12, 70], "baris": [[...], ...], "dropdown": {"A": "Daftar dosen"}}, ...])

Baris pertama tiap lembar = nama kolom (tebal, dibekukan). Lembar bernama "Petunjuk"
ditulis tanpa kepala: tiap elemen `baris` = [teks] atau [teks, True] untuk huruf tebal.
`dropdown` = {kolom: nama lembar daftar} → validasi daftar (peringatan, bukan larangan).
"""

import pathlib
import sys
import zipfile
from xml.sax.saxutils import escape

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from buat_templat import kol, sel, sheet  # noqa: E402

TIPE = "application/vnd.openxmlformats-officedocument.spreadsheetml"
REL = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"


def _lembar(ls, ukuran_daftar):
    if ls["nama"] == "Petunjuk":
        baris = [[sel(f"A{n}", b[0], 1 if len(b) > 1 and b[1] else 0)] for n, b in enumerate(ls["baris"], 1)]
        return sheet(baris, lebar=[150])
    baris = [[sel(f"{kol(i)}1", k, 1) for i, k in enumerate(ls["kepala"])]]
    for n, r in enumerate(ls["baris"], 2):
        baris.append([sel(f"{kol(i)}{n}", v) for i, v in enumerate(r) if v not in (None, "")])
    ekstra = ""
    dd = ls.get("dropdown") or {}
    if dd:
        item = []
        for huruf, daftar in dd.items():
            item.append('<dataValidation type="list" errorStyle="warning" allowBlank="1" showErrorMessage="1" '
                        'errorTitle="Dosen" error="Nama tidak ada di daftar dosen." '
                        f'sqref="{huruf}2:{huruf}{ls.get("maks", 500)}"><formula1>\'{daftar}\'!$A$2:$A${ukuran_daftar[daftar] + 1}'
                        '</formula1></dataValidation>')
        ekstra = f'<dataValidations count="{len(item)}">{"".join(item)}</dataValidations>'
    return sheet(baris, lebar=ls["lebar"], beku=True, ekstra=ekstra)


def tulis_xlsx(path, lembar):
    path = pathlib.Path(path)
    ukuran_daftar = {l["nama"]: len(l["baris"]) for l in lembar}
    n = len(lembar)
    parts = {
        "[Content_Types].xml": '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
            '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
            '<Default Extension="xml" ContentType="application/xml"/>'
            f'<Override PartName="/xl/workbook.xml" ContentType="{TIPE}.sheet.main+xml"/>'
            + "".join(f'<Override PartName="/xl/worksheets/sheet{i}.xml" ContentType="{TIPE}.worksheet+xml"/>' for i in range(1, n + 1))
            + f'<Override PartName="/xl/styles.xml" ContentType="{TIPE}.styles+xml"/></Types>',
        "_rels/.rels": '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            f'<Relationship Id="rId1" Type="{REL}/officeDocument" Target="xl/workbook.xml"/></Relationships>',
        "xl/workbook.xml": '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            f'<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="{REL}"><sheets>'
            + "".join(f'<sheet name="{escape(l["nama"])}" sheetId="{i}" r:id="rId{i}"/>' for i, l in enumerate(lembar, 1))
            + '</sheets></workbook>',
        "xl/_rels/workbook.xml.rels": '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            + "".join(f'<Relationship Id="rId{i}" Type="{REL}/worksheet" Target="worksheets/sheet{i}.xml"/>' for i in range(1, n + 1))
            + f'<Relationship Id="rId{n + 1}" Type="{REL}/styles" Target="styles.xml"/></Relationships>',
        "xl/styles.xml": '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
            '<fonts count="2"><font><sz val="11"/><name val="Calibri"/></font>'
            '<font><b/><sz val="11"/><name val="Calibri"/></font></fonts>'
            '<fills count="2"><fill><patternFill patternType="none"/></fill>'
            '<fill><patternFill patternType="gray125"/></fill></fills>'
            '<borders count="1"><border><left/><right/><top/><bottom/><diagonal/></border></borders>'
            '<cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>'
            '<cellXfs count="2"><xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/>'
            '<xf numFmtId="0" fontId="1" fillId="0" borderId="0" xfId="0" applyFont="1"/></cellXfs>'
            '<cellStyles count="1"><cellStyle name="Normal" xfId="0" builtinId="0"/></cellStyles></styleSheet>',
    }
    for i, l in enumerate(lembar, 1):
        parts[f"xl/worksheets/sheet{i}.xml"] = _lembar(l, ukuran_daftar)
    path.parent.mkdir(exist_ok=True)
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for nama, isi in parts.items():
            z.writestr(nama, isi)
