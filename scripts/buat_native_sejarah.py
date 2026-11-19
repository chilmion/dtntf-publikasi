#!/usr/bin/env python3
"""Sejarah untuk tf (desain v1, native): banner, pengantar, 'Peta jalan' = timeline TANPA foto (revisi 19 Nov), 6 periode berkartu foto.
Data: data/sejarah-v1.json (dari docs/deploy-ugm/revisi/sejarah.js). Foto: media tf sejarah-<id10>.jpg (diunggah deploySejarah)."""
import json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import buat_elementor as be  # noqa: E402
import buat_profil_dosen as bp  # noqa: E402
import buat_native_orang as bo  # noqa: E402
import native_tipografi as nt  # noqa: E402

ROOT = be.ROOT
P = json.loads((ROOT / "manual" / "halaman" / "sejarah-v1.json").read_text(encoding="utf-8"))
FOTO = "https://tf.ugm.ac.id/wp-content/uploads/sites/7/2026/11/sejarah-%s.jpg"
BORDER = {"unit": "px", "top": "1", "right": "1", "bottom": "1", "left": "1", "isLinked": True}


def h(tek, ukur, warna="#073C64", tag="div", bobot="800", spasi=-0.02, **kw):
    return be.widget("heading", title=tek, header_size=tag, title_color=warna, typography_typography="custom", typography_font_family="Plus Jakarta Sans",
                     typography_font_weight=bobot, typography_font_size=be.ukuran_(ukur), typography_font_size_mobile=be.ukuran_(min(ukur, 26)),
                     typography_line_height={"unit": "em", "size": 1.1, "sizes": []}, typography_letter_spacing={"unit": "em", "size": spasi, "sizes": []}, **kw)


def simpul(p):
    t = be.container([h(p["y"], 24), bp.teks(f"<p><strong>{p['n']}</strong></p>", "#073C64", 14, None), bp.teks(f"<p>{p['t']}</p>", "#636363", 14, None)],
                     content_width="full", flex_direction="column", flex_gap=be.gap(6), width=be.ukuran(23.5, "%"), width_tablet=be.ukuran(48.5, "%"),
                     width_mobile=be.ukuran(100, "%"), border_border="solid", border_width={"unit": "px", "top": "4", "right": "0", "bottom": "0", "left": "0", "isLinked": False},
                     border_color="#073C64", padding={"unit": "px", "top": "16", "right": "0", "bottom": "0", "left": "0", "isLinked": False}, _title="Titik " + p["y"])
    return t


def baris(label, ps):
    g = be.container([simpul(p) for p in ps], content_width="full", flex_direction="row", flex_wrap="wrap", flex_gap=be.gap(20), padding=bp.ruang(0), _title="Titik waktu")
    return be.container([h(label, 22, tag="div"), g], content_width="full", flex_direction="column", flex_gap=be.gap(14), padding=bp.ruang(0), _title="Peta jalan " + label)


def kartu(it):
    y, judul, teks, foto = it
    return be.container([be.widget("image", image={"url": FOTO % foto[:10], "id": "", "alt": judul}, image_size="full", width=be.ukuran(100, "%"),
                                   height=be.ukuran(200, "px"), image_border_radius=bp.sudut(12), _title="Foto " + judul, **{"object-fit": "cover"}),
                         h(y, 28), be.widget("heading", title=judul, header_size="h3", title_color="#161616", _title="Judul"),
                         bp.teks(f"<p>{teks}</p>", "#4A4A4A", 15, None)],
                        content_width="full", flex_direction="column", flex_gap=be.gap(10), background_background="classic", background_color="#FFFFFF",
                        border_border="solid", border_width=BORDER, border_color=bp.GARIS, border_radius=bp.sudut(16), padding=bp.ruang(14),
                        width=be.ukuran(32, "%"), width_tablet=be.ukuran(48.5, "%"), width_mobile=be.ukuran(100, "%"), _title="Kartu " + judul)


def periode(i, p):
    kop = be.container([h(p["y"], 44), be.widget("heading", title=p["n"], header_size="h2", title_color="#161616", _title="Nama periode")],
                       content_width="full", flex_direction="column", flex_gap=be.gap(6), padding=bp.ruang(0), _title="Judul periode")
    g = be.container([kartu(it) for it in p["items"]], content_width="full", flex_direction="row", flex_wrap="wrap", flex_gap=be.gap(20),
                     flex_justify_content="flex-start", padding=bp.ruang(0), _title="Kartu periode")
    return be.container([kop, g], content_width="full", flex_direction="column", flex_gap=be.gap(24), background_background="classic",
                        background_color="#F5F5F5" if i % 2 else "#FFFFFF", border_radius=bp.sudut(10), padding=bp.ruang(40), padding_mobile=bp.ruang(20),
                        _title="Periode " + p["y"], _element_id=f"periode-{i + 1}")


def main():
    intro = be.container([be.widget("heading", title="Sejarah Departemen Teknik Nuklir dan Teknik Fisika (DTNTF)", header_size="h2", title_color="#161616", _title="Judul"),
                          bp.teks("<p>Perjalanan jurusan dari kerja sama UGM dan BATAN pada 1974 hingga pengembangan program sarjana, magister, dan kerja sama global saat ini.</p>", "#636363", 17, None)],
                         content_width="full", flex_direction="column", flex_gap=be.gap(10), padding=bp.ruang(0), _title="Pengantar")
    peta = be.container([be.widget("heading", title="Peta jalan", header_size="h2", title_color="#161616", _title="Judul peta jalan"),
                         baris("1974 – 2016", P[:4]), baris("2016 – Sekarang", P[4:])], content_width="full", flex_direction="column", flex_gap=be.gap(28),
                        padding=bp.ruang(0), _title="Peta jalan")
    d = bo.halaman([intro, peta] + [periode(i, p) for i, p in enumerate(P)], "Sejarah")
    s = json.dumps(d, ensure_ascii=False)
    assert "<style" not in s and '"widgetType": "html"' not in s
    (ROOT / "elementor" / "native" / "sejarah.json").write_text(s, encoding="utf-8")
    print("ok sejarah", len(s))


if __name__ == "__main__":
    main()
