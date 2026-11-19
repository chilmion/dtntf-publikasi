#!/usr/bin/env python3
"""Struktur Organisasi untuk tf (desain v1 native): banner, bagan = gambar PNG (data/ugm/struktur-bagan.png, dari SVG v1; diunggah ke media tf
sebagai dtntf-struktur-bagan.png), kartu program studi bento (foto latar, judul tertaut)."""
import json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import buat_elementor as be  # noqa: E402
import buat_profil_dosen as bp  # noqa: E402
import buat_native_orang as bo  # noqa: E402
import buat_native_fasilitas as bf  # noqa: E402

ROOT = be.ROOT
B = "https://tf.ugm.ac.id/wp-content/uploads/sites/7/2026/11/"
PR = [("S1 Teknik Nuklir", "Program sarjana teknologi nuklir.", "sejarah-1630142895.jpg", "/prodi/", 62, 360),
      ("S1 Teknik Fisika", "Program sarjana fisika terapan.", "sejarah-1781330189.jpg", "/prodi-s1-teknik-fisika/", 36, 360),
      ("IUP Teknik Nuklir", "Program sarjana internasional.", "sejarah-1745571479.jpg", "/iup-teknik-nuklir/", 36, 300),
      ("Magister Teknik Fisika", "Program magister.", "sejarah-1759328381.jpg", "/program-studi-magister-teknik-fisika/", 62, 300)]


def main():
    bagan = be.widget("image", image={"url": B + "dtntf-struktur-bagan-scaled.png", "id": "", "alt": "Bagan struktur organisasi Departemen Teknik Nuklir dan Teknik Fisika: Ketua Departemen, Sekretaris, Kantor Urusan Administrasi, program studi, KBK, dan laboratorium"},
                      image_size="full", width=be.ukuran(100, "%"), _title="Bagan organisasi")
    kar = be.container([bagan], content_width="full", flex_direction="column", background_background="classic", background_color="#FFFFFF", border_border="solid",
                       border_width={"unit": "px", "top": "1", "right": "1", "bottom": "1", "left": "1", "isLinked": True}, border_color=bp.GARIS,
                       border_radius=bp.sudut(16), padding=bp.ruang(24), padding_mobile=bp.ruang(12), _title="Kartu bagan")
    s1 = be.container([be.widget("heading", title="Bagan organisasi", header_size="h2", title_color="#161616", _title="Judul"),
                       bp.teks("<p>Susunan organisasi Departemen Teknik Nuklir dan Teknik Fisika, Fakultas Teknik UGM.</p>", "#636363", 17, None), kar],
                      content_width="full", flex_direction="column", flex_gap=be.gap(14), padding=bp.ruang(0), _title="Bagan")
    cards = []
    for n, d, img, u, w, h in PR:
        c = bf.kartu(n, d, img, "", w, h)
        c["elements"][0]["settings"]["link"] = {"url": u, "is_external": "", "nofollow": "", "custom_attributes": ""}
        cards.append(c)
    s2 = be.container([be.widget("heading", title="Program studi di bawah departemen", header_size="h2", title_color="#161616", _title="Judul"),
                       be.container([bf.baris([]) if False else be.container(cards[:2], content_width="full", flex_direction="row", flex_wrap="wrap", flex_gap=be.gap(20), padding=bp.ruang(0), _title="Baris 1"),
                                     be.container(cards[2:], content_width="full", flex_direction="row", flex_wrap="wrap", flex_gap=be.gap(20), padding=bp.ruang(0), _title="Baris 2")],
                                    content_width="full", flex_direction="column", flex_gap=be.gap(20), padding=bp.ruang(0), _title="Kartu prodi")],
                      content_width="full", flex_direction="column", flex_gap=be.gap(14), background_background="classic", background_color="#F5F5F5", border_radius=bp.sudut(10),
                      padding=bp.ruang(40), padding_mobile=bp.ruang(20), _title="Program studi")
    d = bo.halaman([s1, s2], "Struktur Organisasi")
    s = json.dumps(d, ensure_ascii=False)
    assert "<style" not in s and '"widgetType": "html"' not in s
    (ROOT / "elementor" / "native" / "struktur.json").write_text(s, encoding="utf-8")
    print("ok struktur", len(s))


if __name__ == "__main__":
    main()
