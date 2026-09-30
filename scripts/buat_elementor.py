#!/usr/bin/env python3
"""
Buat templat Elementor (.json) dari widget/*.html — siap diimpor:
Elementor → Templates → Saved Templates → Import Templates.

  elementor/profil-dosen.json   kerangka halaman profil (foto, nama, bio) + widget publikasi
  elementor/departemen.json     kerangka halaman departemen + widget departemen

Gaya v1.katur.online (font/warna/ukuran diambil dari kit Elementor situs itu):
  elementor/katur-daftar-dosen.json   halaman daftar dosen (kartu, saring prodi + cari)
  elementor/katur-profil-dosen.json   halaman profil dosen (kartu kiri, info, bio manual, data GitHub)
  elementor/katur-statistik.json      halaman statistik: bento + daftar luaran yang bisa disaring

Struktur memakai Container (Flexbox) Elementor, bukan Section lama.
    python3 scripts/buat_elementor.py [URL-data-GitHub-Pages]
Stdlib saja.
"""

import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "elementor"
PLACEHOLDER_BASE = "https://NAMA-AKUN.github.io/dtntf-profil/data"
BASE = sys.argv[1] if len(sys.argv) > 1 else "https://chilmion.github.io/dtntf-publikasi/data"

NAVY, DARK, LILAC = "#073C64", "#1A2C43", "#F7F7FB"
_n = [0]


def eid():
    _n[0] += 1
    return f"{0xd7f00000 + _n[0] * 7919:08x}"[-8:]


def ukuran(n, unit="px"):
    return {"unit": unit, "size": n, "sizes": []}


def gap(n):
    return {"column": str(n), "row": str(n), "isLinked": True, "unit": "px", "size": n}


def container(anak, **s):
    return {"id": eid(), "elType": "container", "settings": s, "elements": anak, "isInner": False}


def widget(tipe, **s):
    return {"id": eid(), "elType": "widget", "widgetType": tipe, "settings": s, "elements": []}


def html_widget(nama_file):
    h = (ROOT / "widget" / nama_file).read_text(encoding="utf-8").replace(PLACEHOLDER_BASE, BASE)
    return widget("html", html=h)


def profil():
    kiri = container(
        [widget("image", image={"url": "https://placehold.co/400x500/E8EEF4/073C64?text=Foto+Dosen", "id": ""},
                image_size="full", width=ukuran(100, "%"),
                image_border_radius={"unit": "px", "top": "12", "right": "12", "bottom": "12",
                                     "left": "12", "isLinked": True})],
        content_width="full", width=ukuran(28, "%"), width_tablet=ukuran(40, "%"),
        width_mobile=ukuran(100, "%"), flex_direction="column")
    kanan = container(
        [widget("heading", title="Prof. Dr. Nama Dosen, S.T., M.Sc.", header_size="h1",
                title_color=DARK, typography_typography="custom",
                typography_font_family="Plus Jakarta Sans", typography_font_weight="700",
                typography_font_size=ukuran(2.1, "rem")),
         widget("heading", title="Jabatan fungsional · Program Studi Teknik Fisika", header_size="h3",
                title_color=NAVY, typography_typography="custom",
                typography_font_family="Plus Jakarta Sans", typography_font_weight="500",
                typography_font_size=ukuran(1, "rem")),
         widget("text-editor", editor="<p>Tulis biografi singkat dosen di sini: bidang keahlian, "
                "riwayat pendidikan, dan minat riset. Bagian ini kamu desain sendiri; hanya widget "
                "publikasi di bawahnya yang terisi otomatis.</p><p>Email: nama@ugm.ac.id</p>",
                text_color="#4a5264")],
        content_width="full", width=ukuran(72, "%"), width_tablet=ukuran(60, "%"),
        width_mobile=ukuran(100, "%"), flex_direction="column", flex_gap=gap(10))
    baris = container([kiri, kanan], content_width="full", flex_direction="row",
                      flex_direction_mobile="column", flex_gap=gap(36),
                      flex_align_items="flex-start")
    baris["isInner"] = True
    isi = container([html_widget("publikasi.html")], content_width="full")
    isi["isInner"] = True
    return container([baris, isi], content_width="boxed", boxed_width=ukuran(1080),
                     flex_direction="column", flex_gap=gap(44),
                     padding={"unit": "px", "top": "56", "right": "20", "bottom": "64",
                              "left": "20", "isLinked": False})


def departemen():
    judul = widget("heading", title="Publikasi & Pengabdian Departemen", header_size="h1",
                   title_color=DARK, typography_typography="custom",
                   typography_font_family="Plus Jakarta Sans", typography_font_weight="700",
                   typography_font_size=ukuran(2.1, "rem"))
    pengantar = widget("text-editor", editor="<p>Luaran dosen Departemen Teknik Nuklir dan Teknik "
                       "Fisika UGM. Data diperbarui otomatis dari SINTA.</p>", text_color="#4a5264")
    isi = container([html_widget("departemen.html")], content_width="full")
    isi["isInner"] = True
    return container([judul, pengantar, isi], content_width="boxed", boxed_width=ukuran(1140),
                     flex_direction="column", flex_gap=gap(24),
                     padding={"unit": "px", "top": "56", "right": "20", "bottom": "64",
                              "left": "20", "isLinked": False})


# ---------------------------------------------------------------- gaya katur
def katur_html(nama_file):
    return html_widget(nama_file)


def judul_katur(teks, tag="h1", ukuran=56, spasi=-3.4):
    """Heading native: Plus Jakarta Sans 400, tracking negatif (tipografi global situs katur)."""
    return widget("heading", title=teks, header_size=tag, title_color="#161616",
                  typography_typography="custom", typography_font_family="Plus Jakarta Sans",
                  typography_font_weight="400", typography_font_size=ukuran_(ukuran),
                  typography_line_height={"unit": "em", "size": 1.2, "sizes": []},
                  typography_letter_spacing={"unit": "px", "size": spasi, "sizes": []},
                  __globals__={"title_color": "globals/colors?id=primary"})


def ukuran_(n):
    return {"unit": "px", "size": n, "sizes": []}


def teks_katur(html):
    return widget("text-editor", editor=html, text_color="#636363",
                  typography_typography="custom", typography_font_family="Barlow",
                  typography_font_weight="400", typography_font_size=ukuran_(16),
                  __globals__={"text_color": "globals/colors?id=text"})


def halaman_katur(anak):
    return container(anak, content_width="boxed", boxed_width=ukuran(1180),
                     flex_direction="column", flex_gap=gap(24),
                     padding={"unit": "px", "top": "60", "right": "20", "bottom": "80",
                              "left": "20", "isLinked": False},
                     padding_mobile={"unit": "px", "top": "32", "right": "16", "bottom": "48",
                                     "left": "16", "isLinked": False})


def katur_daftar():
    isi = container([katur_html("katur-daftar-dosen.html")], content_width="full")
    isi["isInner"] = True
    return halaman_katur([isi])


def katur_statistik():
    isi = container([katur_html("katur-statistik.html")], content_width="full")
    isi["isInner"] = True
    return halaman_katur([isi])


def katur_profil():
    remah = teks_katur('<p style="font-size:14px;margin:0">Beranda &rsaquo; Dosen Tetap &rsaquo; Nama Dosen</p>')
    kiri = container([katur_html("katur-profil-kartu.html")], content_width="full",
                     width=ukuran(28, "%"), width_tablet=ukuran(34, "%"), width_mobile=ukuran(100, "%"),
                     flex_direction="column")
    tentang = [judul_katur("Tentang", "h2", 40, -1.7),
               teks_katur("<p>Tulis profil singkat dosen di sini: riwayat, minat, dan capaian. Bagian ini kamu "
                          "desain sendiri di Elementor; nama, foto, kontak, pendidikan, dan data publikasi "
                          "di sekitarnya terisi otomatis dari GitHub.</p>")]
    kanan = container([katur_html("katur-profil-info.html")] + tentang + [katur_html("katur-profil-data.html")],
                      content_width="full", width=ukuran(72, "%"), width_tablet=ukuran(66, "%"),
                      width_mobile=ukuran(100, "%"), flex_direction="column", flex_gap=gap(40))
    baris = container([kiri, kanan], content_width="full", flex_direction="row",
                      flex_direction_tablet="row", flex_direction_mobile="column",
                      flex_gap=gap(32), flex_align_items="flex-start")
    baris["isInner"] = True
    return halaman_katur([remah, baris])


def tulis(nama, judul, isi):
    doc = {"version": "0.4", "title": judul, "type": "container", "content": [isi],
           "page_settings": []}
    (OUT / nama).write_text(json.dumps(doc, ensure_ascii=False), encoding="utf-8")
    print(f"Tertulis elementor/{nama}  (data-base = {BASE})")


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    tulis("profil-dosen.json", "DTNTF – Profil Dosen + Publikasi", profil())
    tulis("departemen.json", "DTNTF – Halaman Publikasi Departemen", departemen())
    tulis("katur-daftar-dosen.json", "DTNTF Katur – Daftar Dosen", katur_daftar())
    tulis("katur-profil-dosen.json", "DTNTF Katur – Profil Dosen", katur_profil())
    tulis("katur-statistik.json", "DTNTF Katur – Statistik Publikasi", katur_statistik())
