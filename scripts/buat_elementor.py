#!/usr/bin/env python3
"""
Buat templat Elementor (.json) dari widget/*.html — siap diimpor:
Elementor → Templates → Saved Templates → Import Templates.

  elementor/profil-dosen.json   kerangka halaman profil (foto, nama, bio) + widget publikasi
  elementor/departemen.json     kerangka halaman departemen + widget departemen

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


def tulis(nama, judul, isi):
    doc = {"version": "0.4", "title": judul, "type": "container", "content": [isi],
           "page_settings": []}
    (OUT / nama).write_text(json.dumps(doc, ensure_ascii=False), encoding="utf-8")
    print(f"Tertulis elementor/{nama}  (data-base = {BASE})")


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    tulis("profil-dosen.json", "DTNTF – Profil Dosen + Publikasi", profil())
    tulis("departemen.json", "DTNTF – Halaman Publikasi Departemen", departemen())
