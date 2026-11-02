#!/usr/bin/env python3
"""
Buat templat Excel kosong untuk data yang diisi manual:
  manual/templat-profil-cv.xlsx   riwayat CV tiap dosen (halaman profil) → dibaca scripts/profil_cv.py
  manual/templat-kbk.xlsx         data lima halaman KBK                  → dibaca scripts/kbk.py

Cara pakai: salin templat jadi manual/profil-cv.xlsx / manual/kbk.xlsx, isi, lalu unggah
(lewat mini app `scripts/unggah_manual.py` atau GitHub → Add file → Upload files).

    python3 scripts/buat_templat_cv.py

Modul ini juga menyediakan lembar_cv(isi) dan lembar_kbk(isi) agar berkas terisi bisa dibuat
dengan kolom yang sama persis.
"""

import csv
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from xlsx_tulis import tulis_xlsx  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
MANUAL = ROOT / "manual"

PETUNJUK_CV = [
    ("PROFIL CV DOSEN — petunjuk pengisian", True),
    ("Satu berkas untuk seluruh dosen. Satu baris = satu butir (satu pendidikan, satu penghargaan, dst).", False),
    ("Kolom 'dosen': pilih nama dari dropdown (sama dengan dosen.csv). Jangan ganti nama lembar atau nama kolom.", False),
    ("", False),
    ("Lembar Identitas — satu baris per dosen. Kolom boleh kosong:", True),
    ("  nama_lengkap (dengan gelar, mis. Prof. Dr. Ir. Nama, M.T.; kosong = nama + gelar dari dosen.csv),", False),
    ("  jabatan_fungsional (mis. Guru Besar, Lektor Kepala), bidang_kepakaran, institusi, telepon_institusi.", False),
    ("  Kosong = institusi & telepon memakai nilai departemen; jabatan_fungsional kosong = tampil lorem ipsum.", False),
    ("Lembar Pendidikan, Sertifikat, Pekerjaan, Organisasi, Penghargaan — kolom: dosen, tahun, keterangan.", True),
    ("  tahun boleh rentang ('2001 - 2006'), 'sekarang', atau kosong. Urutan baris = urutan tampil (terbaru dulu).", False),
    ("  Pendidikan kosong → dipakai teks pendidikan dari halaman Dosen Tetap lama (manual/dosen-info.csv).", False),
    ("Lembar Kerjasama — Pengalaman Kerjasama dan Penelitian: dosen, riset_proyek, tahun, keterangan.", True),
    ("  Ditampilkan bersama Penelitian & Pengabdian dari SINTA (otomatis).", False),
    ("", False),
    ("Yang TIDAK dari berkas ini (otomatis dari SINTA / berkas luaran.xlsx): Kekayaan Intelektual, Publikasi Jurnal,", False),
    ("Prosiding Seminar, Buku.", False),
    ("", False),
    ("PRIVASI: JANGAN menambah kolom alamat rumah, nomor HP pribadi, tanggal lahir, jenis kelamin, NIP, atau NIDN.", True),
    ("Bagian yang belum terisi tampil sebagai teks lorem ipsum (penanda) di halaman; hilang sendiri setelah diisi.", False),
]

PETUNJUK_KBK = [
    ("DATA HALAMAN KBK — petunjuk pengisian", True),
    ("Lembar KBK: satu baris per KBK. kode (huruf kecil, mis. enet), halaman (alamat: kbk-enet → /kbk-enet/),", False),
    ("  ketua (nama dosen persis seperti di dosen.csv), ringkasan (SATU kalimat untuk kartu di halaman induk),", False),
    ("  sekilas (satu paragraf untuk bagian hero).", False),
    ("Lembar Kompetensi: kbk (kode), judul, deskripsi — nomor mengikuti urutan baris.", False),
    ("Lembar Anggota: kbk (kode), dosen (dropdown), keahlian (bidang keahlian singkat), peran (Ketua / Koordinator / kosong).", False),
    ("  Satu dosen boleh muncul di beberapa KBK (satu baris per KBK).", False),
    ("Lembar Tema: kbk (kode), judul, deskripsi (2-3 kalimat), jumlah_publikasi (angka total publikasi tema itu).", False),
    ("Lembar Riset: kbk (kode), tema (nomor urut tema di KBK itu), riset (satu riset terkait per baris; maks 5 tampil).", False),
    ("Lembar Publikasi: kbk (kode), tema (nomor), sitasi (teks sitasi lengkap), doi (opsional); maks 5 tampil per tema.", False),
    ("", False),
    ("Sel/lembar yang dibiarkan kosong → halaman menampilkan lorem ipsum sebagai penanda. Statistik dihitung otomatis.", False),
    ("KBK ini BERBEDA dari kelompok Teknik Nuklir/Teknik Fisika.", True),
]


def nama_dosen():
    with open(ROOT / "dosen.csv", newline="", encoding="utf-8") as f:
        return sorted({r["nama"].strip() for r in csv.DictReader(f) if r["nama"].strip()}, key=str.lower)


def _daftar():
    return {"nama": "Daftar dosen", "kepala": ["nama"], "lebar": [36], "baris": [[n] for n in nama_dosen()]}


def lembar_cv(isi=None):
    isi = isi or {}
    L = lambda nama, kepala, lebar, dd="A": {  # noqa: E731
        "nama": nama, "kepala": kepala, "lebar": lebar, "baris": isi.get(nama, []), "dropdown": {dd: "Daftar dosen"}}
    riwayat = lambda n: L(n, ["dosen", "tahun", "keterangan"], [30, 16, 90])  # noqa: E731
    return [{"nama": "Petunjuk", "baris": [list(p) for p in PETUNJUK_CV]},
            L("Identitas", ["dosen", "nama_lengkap", "jabatan_fungsional", "bidang_kepakaran", "institusi", "telepon_institusi"],
              [30, 50, 26, 50, 50, 24]),
            riwayat("Pendidikan"), riwayat("Sertifikat"), riwayat("Pekerjaan"), riwayat("Organisasi"),
            riwayat("Penghargaan"),
            L("Kerjasama", ["dosen", "riset_proyek", "tahun", "keterangan"], [30, 90, 14, 50]),
            _daftar()]


def lembar_kbk(isi=None):
    isi = isi or {}
    L = lambda nama, kepala, lebar, dd=None: {  # noqa: E731
        "nama": nama, "kepala": kepala, "lebar": lebar, "baris": isi.get(nama, []),
        **({"dropdown": {dd: "Daftar dosen"}} if dd else {})}
    return [{"nama": "Petunjuk", "baris": [list(p) for p in PETUNJUK_KBK]},
            L("KBK", ["kode", "nama", "singkatan", "halaman", "ketua", "ringkasan", "sekilas"],
              [12, 40, 14, 22, 36, 70, 90], dd="E"),
            L("Kompetensi", ["kbk", "judul", "deskripsi"], [10, 44, 100]),
            L("Anggota", ["kbk", "dosen", "keahlian", "peran"], [10, 34, 70, 14], dd="B"),
            L("Tema", ["kbk", "judul", "deskripsi", "jumlah_publikasi"], [10, 50, 100, 18]),
            L("Riset", ["kbk", "tema", "riset"], [10, 8, 110]),
            L("Publikasi", ["kbk", "tema", "sitasi", "doi"], [10, 8, 110, 34]),
            _daftar()]


def main():
    tulis_xlsx(MANUAL / "templat-profil-cv.xlsx", lembar_cv())
    tulis_xlsx(MANUAL / "templat-kbk.xlsx", lembar_kbk())
    print("Tertulis manual/templat-profil-cv.xlsx dan manual/templat-kbk.xlsx")


if __name__ == "__main__":
    main()
