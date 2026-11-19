"""
Normalisasi tipografi halaman native tf mengikuti skala Home v2 (docs/deploy-ugm/README.md, 'Skala tipografi Home v2'):
H1 64/48/36 lh1.1 ls-0.025em w400 · H2 36/30/28 lh1.15 ls-0.02em w400 · H3 22/22/20 lh1.3 ls-0.01em w500 · H4 20 ·
isi 17/16/16 lh1.6 (Barlow; teks kecil <=15 dibiarkan) · tombol Barlow ls+0.02em. Judul = Plus Jakarta Sans.
Heading 'div'/'span' (angka besar, kicker) tidak diubah.
"""


def _u(n, unit="px"):
    return {"unit": unit, "size": n, "sizes": []}


SKALA = {"h1": (64, 48, 36, 1.1, -0.025, "400"), "h2": (36, 30, 28, 1.15, -0.02, "400"),
         "h3": (22, 22, 20, 1.3, -0.01, "500"), "h4": (20, 20, 18, 1.3, -0.01, "500")}


def terapkan(el):
    s = el.get("settings", {})
    w = el.get("widgetType")
    if w == "heading" and s.get("header_size") in SKALA:
        d, t, m, lh, ls, bobot = SKALA[s["header_size"]]
        s.update(typography_typography="custom", typography_font_family="Plus Jakarta Sans", typography_font_weight=bobot,
                 typography_font_size=_u(d), typography_font_size_tablet=_u(t), typography_font_size_mobile=_u(m),
                 typography_line_height=_u(lh, "em"), typography_letter_spacing=_u(ls, "em"), typography_word_spacing=_u(0))
    elif w == "text-editor":
        ukur = (s.get("typography_font_size") or {}).get("size", 17)
        if ukur >= 16:
            s.update(typography_typography="custom", typography_font_family="Barlow", typography_font_size=_u(17),
                     typography_font_size_tablet=_u(16), typography_font_size_mobile=_u(16), typography_line_height=_u(1.6, "em"))
    elif w == "button":
        s.update(typography_font_family="Barlow", typography_letter_spacing=_u(0.02, "em"))
    for a in el.get("elements", []):
        terapkan(a)
    return el
