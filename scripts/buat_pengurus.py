#!/usr/bin/env python3
"""
Buat elementor/katur-pengurus-departemen.json — halaman Pengurus Departemen (slug /pengurus-departemen/)
dengan sistem desain terbaru (kartu seperti daftar dosen: foto, nama, jabatan, email, tautan profil).

Isi dari manual/pengurus.csv (kelompok, jabatan, slug, nama_lengkap, email) + foto_url di dosen.csv
(foto resmi terbaru). Kartu = container Elementor yang BISA DIEDIT (Image + Heading + teks + tombol).
Periode di judul: konstanta PERIODE.

    python3 scripts/buat_pengurus.py [URL-data-GitHub-Pages]
"""

import csv
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import buat_elementor as be  # noqa: E402
import buat_profil_dosen as bp  # noqa: E402

ROOT = be.ROOT
PERIODE = "2026–2031"
KELAS = "kt-kartu-pengurus"


def kartu(p, foto):
    nama = p["nama_lengkap"]
    gambar = be.widget("image", image={"url": foto or "https://placehold.co/400x500/E8EEF4/073C64?text=Foto", "id": "", "alt": nama},
                       image_size="full", width=be.ukuran(100, "%"),
                       height=be.ukuran(460), height_tablet=be.ukuran(420), height_mobile=be.ukuran(400),
                       **{"object-fit": "contain", "object-position": "top center"},
                       _background_background="classic", _background_color="#F5F5F5",
                       image_border_radius={"unit": "px", "top": "0", "right": "0", "bottom": "0", "left": "0", "isLinked": True})
    jabatan = bp.kicker(p["jabatan"])
    judul = be.widget("heading", title=nama, header_size="h3", title_color="#161616",
                      typography_typography="custom", typography_font_family="Plus Jakarta Sans",
                      typography_font_weight="400", typography_font_size=be.ukuran_(20),
                      typography_line_height={"unit": "em", "size": 1.25, "sizes": []},
                      typography_letter_spacing={"unit": "px", "size": -1.1, "sizes": []},
                      __globals__={"title_color": "globals/colors?id=primary"})
    email = bp.teks(f'<p style="margin:0;font-size:15px"><a href="mailto:{bp.esc(p["email"])}" style="color:{bp.NAVY}">{bp.esc(p["email"])}</a></p>')
    tombol = be.widget("button", text="Profil dosen →",
                       link={"url": f"/{p['slug']}/", "is_external": "", "nofollow": "", "custom_attributes": ""},
                       background_color="rgba(0,0,0,0)", button_text_color=bp.NAVY, border_radius=bp.sudut(0),
                       typography_typography="custom", typography_font_family="Barlow",
                       typography_font_weight="600", typography_font_size=be.ukuran_(15), typography_text_transform="none",
                       button_padding={"unit": "px", "top": "0", "right": "0", "bottom": "0", "left": "0", "isLinked": True})
    isi = be.container([jabatan, judul, email, tombol], content_width="full", flex_direction="column", flex_gap=be.gap(8),
                       padding=bp.ruang(20), flex_justify_content="space-between", flex_grow=1,
                       min_height=be.ukuran(200), min_height_mobile=be.ukuran(0))
    isi["isInner"] = True
    k = be.container([gambar, isi], content_width="full", flex_direction="column", flex_gap=be.gap(0),
                     background_background="classic", background_color="#FFFFFF", border_radius=bp.sudut(10),
                     border_border="solid", border_width={"unit": "px", "top": "1", "right": "1", "bottom": "1", "left": "1", "isLinked": True},
                     border_color=bp.GARIS, overflow="hidden", css_classes=KELAS,
                     width=be.ukuran(30, "%"), width_tablet=be.ukuran(48, "%"), width_mobile=be.ukuran(100, "%"),
                     _title=f"{p['jabatan']} – {nama}")
    k["isInner"] = True
    return k


def main():
    be.BASE = sys.argv[1] if len(sys.argv) > 1 else be.BASE
    be._n[0] = 0
    foto = {r["slug"]: (r.get("foto_url") or "").strip() for r in csv.DictReader(open(ROOT / "dosen.csv", newline="", encoding="utf-8"))}
    baris = list(csv.DictReader(open(ROOT / "manual" / "pengurus.csv", newline="", encoding="utf-8")))
    anak = [bp.kicker(f"Departemen Teknik Nuklir dan Teknik Fisika · Periode {PERIODE}"), bp.judul("Pengurus Departemen"),
            bp.teks("<p>Ketua dan sekretaris departemen, ketua program studi, kepala laboratorium, dan ketua kelompok bidang keahlian (KBK).</p>", "#636363", 18)]
    for kel in dict.fromkeys(r["kelompok"] for r in baris):
        grid = be.container([kartu(r, foto.get(r["slug"])) for r in baris if r["kelompok"] == kel], content_width="full",
                            flex_direction="row", flex_wrap="wrap", flex_gap=be.gap(16), flex_align_items="stretch", _title=f"Kartu {kel}")
        grid["isInner"] = True
        anak += [be.judul_katur(kel, "h2", 40, -1.7), grid]
    doc = {"version": "0.4", "title": "DTNTF Katur – Pengurus Departemen (/pengurus-departemen/)", "type": "container",
           "content": [be.halaman_katur(anak)], "page_settings": []}
    (ROOT / "elementor" / "katur-pengurus-departemen.json").write_text(json.dumps(doc, ensure_ascii=False), encoding="utf-8")
    print(f"Tertulis elementor/katur-pengurus-departemen.json ({len(baris)} kartu)")


if __name__ == "__main__":
    main()
