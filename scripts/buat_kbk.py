#!/usr/bin/env python3
"""
Buat templat Elementor lima halaman KBK (Kelompok Bidang Keahlian):

  elementor/katur-kbk-induk.json        halaman induk: kartu semua KBK        (widget/katur-kbk-induk.html)
  elementor/kbk/<kode>.json             satu halaman per KBK, mis. enet.json  (widget/katur-kbk.html, data-kbk=<kode>)

Daftar KBK (kode, nama, alamat halaman) dibaca dari lembar "KBK" di manual/kbk.xlsx. Alamat bawaan:
/kbk/ (induk), /kbk-enet/, /kbk-proses-nuklir/, /kbk-multifisika/, /kbk-instrumentasi/ — atur di
kolom "halaman" lalu jalankan ulang skrip ini (dan scripts/kbk.py) bila diganti.

    python3 scripts/buat_kbk.py [URL-data-GitHub-Pages]
"""

import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import buat_elementor as be  # noqa: E402
import buat_profil_dosen as bp  # noqa: E402
import manual  # noqa: E402

ROOT = be.ROOT
OUT = ROOT / "elementor" / "kbk"


def halaman(widget_html, kicker_teks, judul_teks, remah_teks):
    remah = bp.teks(f'<p style="font-size:14px;margin:0">{remah_teks}</p>')
    anak = [remah]
    if kicker_teks:
        anak += [bp.kicker(kicker_teks), bp.judul(judul_teks)]
    isi = be.container([be.widget("html", html=widget_html)], content_width="full")
    isi["isInner"] = True
    return be.halaman_katur(anak + [isi])


def tulis(path, judul, isi):
    doc = {"version": "0.4", "title": judul, "type": "container", "content": [isi], "page_settings": []}
    path.write_text(json.dumps(doc, ensure_ascii=False), encoding="utf-8")


def main():
    base = sys.argv[1] if len(sys.argv) > 1 else be.BASE
    be.BASE = base
    induk = (ROOT / "widget" / "katur-kbk-induk.html").read_text(encoding="utf-8").replace(be.PLACEHOLDER_BASE, base)
    satu = (ROOT / "widget" / "katur-kbk.html").read_text(encoding="utf-8").replace(be.PLACEHOLDER_BASE, base)
    daftar = [r for r in manual.baca_berkas(ROOT / "manual" / "kbk.xlsx", "KBK") if r.get("kode")]
    OUT.mkdir(parents=True, exist_ok=True)
    be._n[0] = 0
    tulis(ROOT / "elementor" / "katur-kbk-induk.json", "DTNTF Katur – KBK (induk, /kbk/)",
          halaman(induk, "Departemen Teknik Nuklir dan Teknik Fisika", "Kelompok Bidang Keahlian", "Beranda &rsaquo; KBK"))
    for r in daftar:
        kode = r["kode"].strip().lower()
        alamat = (r.get("halaman") or f"kbk-{kode}").strip("/ ")
        be._n[0] = 0
        tulis(OUT / f"{kode}.json", f"DTNTF Katur – KBK {r.get('nama', kode)} (/{alamat}/)",
              halaman(satu.replace('data-kbk="enet"', f'data-kbk="{kode}"'), "", "",
                      f"Beranda &rsaquo; <a href='/kbk/'>KBK</a> &rsaquo; {r.get('nama', kode)}"))
    print(f"Tertulis elementor/katur-kbk-induk.json + {len(daftar)} berkas di elementor/kbk/  (data-base = {base})")


if __name__ == "__main__":
    main()
