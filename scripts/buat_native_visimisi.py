#!/usr/bin/env python3
"""Visi dan Misi untuk tf (desain v1 native). Data: data/visimisi-v1.json (dari docs/deploy-ugm/revisi/visi-misi.js)."""
import json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import buat_elementor as be  # noqa: E402
import buat_profil_dosen as bp  # noqa: E402
import buat_native_orang as bo  # noqa: E402

ROOT = be.ROOT
E = json.loads((ROOT / "data" / "visimisi-v1.json").read_text(encoding="utf-8"))
BORDER = {"unit": "px", "top": "1", "right": "1", "bottom": "1", "left": "1", "isLinked": True}


def label(t, gelap):
    return be.widget("heading", title=t, header_size="div", title_color="#C8E86D" if gelap else "#073C64", typography_typography="custom",
                     typography_font_family="Plus Jakarta Sans", typography_font_weight="800", typography_font_size=be.ukuran_(32), typography_font_size_mobile=be.ukuran_(26),
                     typography_line_height={"unit": "em", "size": 1.15, "sizes": []}, typography_letter_spacing={"unit": "em", "size": -0.02, "sizes": []}, _title=t)


def besar(t, gelap):
    return be.widget("heading", title=t, header_size="div", title_color="#FFFFFF" if gelap else "#073C64", typography_typography="custom",
                     typography_font_family="Plus Jakarta Sans", typography_font_weight="500", typography_font_size=be.ukuran_(28), typography_font_size_mobile=be.ukuran_(20),
                     typography_line_height={"unit": "em", "size": 1.4, "sizes": []}, typography_letter_spacing={"unit": "em", "size": -0.01, "sizes": []}, _title="Teks visi")


def bagian(i, e):
    dep = i == 0
    kiri = be.container([bp.teks(f"<p><strong>{e['k']}</strong></p>", "#636363", 16, None),
                         be.widget("heading", title=e["n"], header_size="h2", title_color="#073C64", _title="Nama")],
                        content_width="full", flex_direction="column", flex_gap=be.gap(8), padding=bp.ruang(0), width=be.ukuran(28, "%"), width_tablet=be.ukuran(100, "%"),
                        width_mobile=be.ukuran(100, "%"), _title="Judul")
    visi = be.container([label("Visi", dep), besar(e["vis"], dep)], content_width="full", flex_direction="column", flex_gap=be.gap(14), padding=bp.ruang(32),
                        padding_mobile=bp.ruang(22), border_radius=bp.sudut(16), background_background="classic", background_color="#073C64" if dep else "#FFFFFF",
                        **({} if dep else {"border_border": "solid", "border_width": BORDER, "border_color": bp.GARIS}), _title="Visi")
    ol = "<ol>" + "".join(f"<li style='margin-bottom:14px'>{m}</li>" for m in e["mis"]) + "</ol>"
    misi = be.container([label("Misi", False), bp.teks(ol, "#161616", 19, None)], content_width="full", flex_direction="column", flex_gap=be.gap(14),
                        padding={"unit": "px", "top": "0", "right": "32", "bottom": "0", "left": "32", "isLinked": False}, _title="Misi")
    kanan = be.container([visi, misi], content_width="full", flex_direction="column", flex_gap=be.gap(28), padding=bp.ruang(0), width=be.ukuran(67, "%"),
                         width_tablet=be.ukuran(100, "%"), width_mobile=be.ukuran(100, "%"), _title="Visi dan misi")
    return be.container([kiri, kanan], content_width="full", flex_direction="row", flex_wrap="wrap", flex_gap=be.gap(40), flex_align_items="flex-start",
                        background_background="classic", background_color="#F5F5F5" if i % 2 else "#FFFFFF", border_radius=bp.sudut(10),
                        padding=bp.ruang(40), padding_mobile=bp.ruang(20), _title="Bagian " + e["n"])


def main():
    d = bo.halaman([bagian(i, e) for i, e in enumerate(E)], "Visi dan Misi")
    s = json.dumps(d, ensure_ascii=False)
    assert "<style" not in s and '"widgetType": "html"' not in s
    (ROOT / "elementor" / "native" / "visimisi.json").write_text(s, encoding="utf-8")
    print("ok visimisi", len(s))


if __name__ == "__main__":
    main()
