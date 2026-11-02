#!/usr/bin/env python3
"""
Gabungkan data CV dosen (manual/profil-cv.xlsx) ke data/<slug>.json sebagai kunci "cv".

Berkas Excel: satu berkas untuk seluruh dosen, tiap bagian CV = satu lembar
(Identitas, Pendidikan, Sertifikat, Pekerjaan, Organisasi, Penghargaan, Kerjasama).
Templat kosong + petunjuk: manual/templat-profil-cv.xlsx (dibuat scripts/buat_templat_cv.py).

Bagian yang kosong tetap ditulis kosong; widget profil menampilkan teks lorem ipsum
(kelas .kt-lorem) sebagai penanda sampai datanya diisi.

PRIVASI: sengaja tidak ada kolom alamat rumah, HP pribadi, tanggal lahir, jenis kelamin, NIP/NIDN.

Dijalankan dari scripts/manual.py (idempoten), atau langsung:
    python3 scripts/profil_cv.py
"""

import csv
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
MANUAL = ROOT / "manual"
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

BERKAS = MANUAL / "profil-cv.xlsx"
INSTITUSI = "Departemen Teknik Nuklir dan Teknik Fisika, Fakultas Teknik, Universitas Gadjah Mada"
TELEPON_DEPARTEMEN = "(+62) (274) 580882"          # telepon institusi (departemen), bukan pribadi
RIWAYAT = {"Pendidikan": "pendidikan", "Sertifikat": "sertifikat", "Pekerjaan": "pekerjaan",
           "Organisasi": "organisasi", "Penghargaan": "penghargaan"}


def baca():
    """→ ({slug: cv}, [masalah]). Tanpa berkas → ({}, [])."""
    import manual  # lazy: manual.py memanggil modul ini dari main()
    if not BERKAS.exists():
        return {}, []
    peta, masalah, cv = manual.peta_dosen(), [], {}

    def dosen(r, lembar):
        s = peta.get(manual.agregat.normal(r.get("dosen", "")))
        if not s:
            masalah.append(f"{lembar} baris {r['_baris']}: dosen '{r.get('dosen', '')}' tidak dikenal")
        return s

    def wadah(s):
        return cv.setdefault(s, {"identitas": {}, **{k: [] for k in RIWAYAT.values()}, "kerjasama": []})

    for r in manual.baca_berkas(BERKAS, "Identitas"):
        s = dosen(r, "Identitas")
        if s:
            wadah(s)["identitas"] = {k: r.get(k, "") for k in
                                     ("nama_lengkap", "jabatan_fungsional", "bidang_kepakaran", "institusi", "telepon_institusi") if r.get(k)}
    for lembar, kunci in RIWAYAT.items():
        for r in manual.baca_berkas(BERKAS, lembar):
            s = dosen(r, lembar)
            if s and r.get("keterangan"):
                wadah(s)[kunci].append({"tahun": r.get("tahun", ""), "keterangan": r["keterangan"]})
    for r in manual.baca_berkas(BERKAS, "Kerjasama"):
        s = dosen(r, "Kerjasama")
        if s and r.get("riset_proyek"):
            wadah(s)["kerjasama"].append({"riset": r["riset_proyek"], "tahun": r.get("tahun", ""),
                                          "keterangan": r.get("keterangan", "")})
    return cv, masalah


def pasang():
    cv, masalah = baca()
    info = {}
    with open(MANUAL / "dosen-info.csv", newline="", encoding="utf-8") as f:
        info = {x["slug"]: x for x in csv.DictReader(f)}
    jml = 0
    for f in sorted(DATA.glob("*.json")):
        if f.name == "index.json":
            continue
        d = json.loads(f.read_text(encoding="utf-8"))
        c = cv.get(d["slug"]) or {"identitas": {}, **{k: [] for k in RIWAYAT.values()}, "kerjasama": []}
        i, x = c["identitas"], info.get(d["slug"], {})
        # nilai bawaan dari data yang sudah ada (bukan karangan): halaman Dosen Tetap lama + departemen
        i.setdefault("institusi", INSTITUSI)
        i.setdefault("telepon_institusi", TELEPON_DEPARTEMEN)
        if x.get("bidang_ilmu"):
            i.setdefault("bidang_kepakaran", x["bidang_ilmu"])
        if d.get("jabatan"):
            i.setdefault("jabatan_fungsional", d["jabatan"])
        if not c["pendidikan"] and x.get("pendidikan"):
            c["pendidikan"] = [{"tahun": "", "keterangan": x["pendidikan"]}]
        # keanggotaan/penghargaan/jabatan dari halaman Dosen Tetap lama (kolom "lainnya"), bila lembar kosong
        for it in (x.get("lainnya") or "").split(" | "):
            it = it.strip()
            kunci = ("organisasi" if it.lower().startswith("anggota") else
                     "penghargaan" if it.lower().startswith(("award", "penghargaan")) else
                     "pekerjaan" if it.lower().startswith("direktur") else None)
            if kunci and not c.get("_isi_" + kunci) and not cv.get(d["slug"], {}).get(kunci):
                c.setdefault("_lama_" + kunci, []).append(
                    {"tahun": "", "keterangan": it.split(":", 1)[1].strip(" .") if ":" in it and kunci != "pekerjaan" else it.strip(" .")})
        for kunci in ("organisasi", "penghargaan", "pekerjaan"):
            c[kunci] = c[kunci] or c.pop("_lama_" + kunci, [])
            c.pop("_lama_" + kunci, None)
        if d.get("cv") != c:
            d["cv"] = c
            f.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
        jml += 1
    print(f"Profil CV: {len(cv)} dosen punya data di {BERKAS.name if BERKAS.exists() else '(tanpa berkas)'}; "
          f"kunci cv dipasang ke {jml} berkas data/")
    for m in masalah:
        print("  ! " + m)


if __name__ == "__main__":
    pasang()
