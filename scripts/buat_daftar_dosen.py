#!/usr/bin/env python3
"""
Buat elementor/katur-daftar-dosen.json — halaman daftar dosen dengan kartu yang BISA DIEDIT.

Tiap dosen = satu container Elementor berisi:
  Image (foto, bawaan dari foto_url di dosen.csv)  → bisa diganti
  Heading (nama)                                    → bisa diedit
  widget HTML (kelompok, gelar, bidang ilmu, skor & sitasi SINTA dari GitHub)
  Tautan teks "selengkapnya →" (isi tautan profil detail sendiri; bawaan /<slug>/)
Di atasnya: Heading + teks pengantar + widget HTML cari/filter.

    python3 scripts/buat_daftar_dosen.py [URL-data-GitHub-Pages]
"""

import csv
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import buat_elementor as be  # noqa: E402
import buat_profil_dosen as bp  # noqa: E402  (helper gaya: tile, kicker, teks, dsb.)

ROOT = be.ROOT
KELAS_KEL = {"Teknik Nuklir": "kt-kel-nuklir", "Teknik Fisika": "kt-kel-fisika"}


def kelompok(bidang):
    return bp.kelompok_dari(bidang)


def kartu(r, info, info_html):
    slug, nama = r["slug"].strip(), r["nama"].strip()
    kel = kelompok((info or {}).get("bidang_ilmu"))
    kelas = f"kt-kartu-dosen {KELAS_KEL.get(kel, 'kt-kel-lain')}"

    foto = be.widget("image", image={"url": r["foto_url"].strip(), "id": "", "alt": nama},
                     image_size="full", width=be.ukuran(100, "%"),
                     height=be.ukuran(360), height_tablet=be.ukuran(320), height_mobile=be.ukuran(300),
                     **{"object-fit": "cover", "object-position": "top center"},
                     image_border_radius={"unit": "px", "top": "0", "right": "0", "bottom": "0", "left": "0", "isLinked": True})
    judul = be.widget("heading", title=nama, header_size="h3", title_color="#161616",
                      typography_typography="custom", typography_font_family="Plus Jakarta Sans",
                      typography_font_weight="400", typography_font_size=be.ukuran_(22),
                      typography_line_height={"unit": "em", "size": 1.2, "sizes": []},
                      typography_letter_spacing={"unit": "px", "size": -1.3, "sizes": []},
                      __globals__={"title_color": "globals/colors?id=primary"})
    data = be.widget("html", html=info_html.replace('data-slug=""', f'data-slug="{slug}"'))
    tombol = be.widget("button", text="selengkapnya →",
                       link={"url": f"/{slug}/", "is_external": "", "nofollow": "", "custom_attributes": ""},
                       background_color="rgba(0,0,0,0)", button_text_color=bp.NAVY, border_radius=bp.sudut(0),
                       typography_typography="custom", typography_font_family="Barlow",
                       typography_font_weight="600", typography_font_size=be.ukuran_(15),
                       typography_text_transform="none",
                       button_padding={"unit": "px", "top": "0", "right": "0", "bottom": "0", "left": "0", "isLinked": True})
    isi = be.container([judul, data, tombol], content_width="full", flex_direction="column",
                       flex_gap=be.gap(6), padding=bp.ruang(20), flex_justify_content="space-between", flex_grow=1,
                       min_height=be.ukuran(400), min_height_tablet=be.ukuran(360), min_height_mobile=be.ukuran(0))
    isi["isInner"] = True
    k = be.container([foto, isi], content_width="full", flex_direction="column", flex_gap=be.gap(0),
                     background_background="classic", background_color="#FFFFFF", border_radius=bp.sudut(10),
                     border_border="solid", border_width={"unit": "px", "top": "1", "right": "1", "bottom": "1", "left": "1", "isLinked": True},
                     border_color=bp.GARIS, overflow="hidden", css_classes=kelas,
                     width=be.ukuran(30, "%"), width_tablet=be.ukuran(48, "%"), width_mobile=be.ukuran(100, "%"),
                     _title=f"Kartu {nama}")
    k["isInner"] = True
    return k


def main():
    base = sys.argv[1] if len(sys.argv) > 1 else be.BASE
    be.BASE = base
    filter_html = (ROOT / "widget" / "katur-dosen-filter.html").read_text(encoding="utf-8")
    info_html = (ROOT / "widget" / "katur-dosen-info.html").read_text(encoding="utf-8").replace(be.PLACEHOLDER_BASE, base)
    with open(ROOT / "dosen.csv", newline="", encoding="utf-8") as f:
        dosen = sorted(csv.DictReader(f), key=lambda r: r["nama"].strip().lower())
    with open(ROOT / "manual" / "dosen-info.csv", newline="", encoding="utf-8") as f:
        info = {x["slug"]: x for x in csv.DictReader(f)}

    kicker = bp.kicker("Departemen Teknik Nuklir dan Teknik Fisika")
    judul = bp.judul("Dosen Tetap")
    pengantar = bp.teks(f"<p>{len(dosen)} dosen dengan keahlian dari rekayasa nuklir hingga rekayasa fisika.</p>", "#636363", 18)
    bilah = be.widget("html", html=filter_html)
    grid = be.container([kartu(r, info.get(r["slug"]), info_html) for r in dosen], content_width="full",
                        flex_direction="row", flex_wrap="wrap", flex_gap=be.gap(16), flex_align_items="stretch",
                        _title="Daftar kartu dosen")
    grid["isInner"] = True
    halaman = be.halaman_katur([kicker, judul, pengantar, bilah, grid])
    doc = {"version": "0.4", "title": "DTNTF Katur – Daftar Dosen (bisa diedit)", "type": "container",
           "content": [halaman], "page_settings": []}
    (ROOT / "elementor" / "katur-daftar-dosen.json").write_text(json.dumps(doc, ensure_ascii=False), encoding="utf-8")
    print(f"Tertulis elementor/katur-daftar-dosen.json ({len(dosen)} kartu; data-base = {base})")


if __name__ == "__main__":
    main()
