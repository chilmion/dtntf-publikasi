#!/usr/bin/env python3
"""
Buat templat Elementor isi halaman program studi (judul/banner halaman sudah dari tema):

  elementor/prodi-teknik-nuklir.json   → halaman "Program Studi Sarjana Teknik Nuklir" (/prodi/)
  elementor/prodi-teknik-fisika.json   → halaman "Prodi S1 Teknik Fisika" (/prodi-s1-teknik-fisika/)

Isi dari manual/prodi/*.md (Markdown sederhana, bisa diedit lalu skrip dijalankan ulang):
  ## Judul bagian · ### Subjudul · paragraf · `- ` poin · `> ` kutipan (visi, kartu lime)
  `| a | b |` tabel · `**Label**` label tebal · `[[lorem]]` = lorem ipsum penanda (.kt-lorem) bagi data yang belum ada

Widget Elementor biasa (Heading + Text Editor) sehingga bisa diedit di Elementor.

    python3 scripts/buat_prodi.py
"""

import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import buat_elementor as be  # noqa: E402
import buat_profil_dosen as bp  # noqa: E402

ROOT = be.ROOT
LOREM = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
GAYA_LOREM = "font-style:italic;color:#7a5d00;background:#FFF6D6;border:1px dashed #D9B84A;border-radius:6px;padding:10px 14px;margin:0"


def inline(s):
    s = bp.esc(s.replace("\u00a0", " "))   # PPT/Word sering memakai spasi tak-putus → teks tidak membungkus
    return re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)


def tabel_html(baris):
    sel = lambda b: [c.strip() for c in b.strip().strip("|").split("|")]  # noqa: E731
    kepala, isi = sel(baris[0]), [sel(b) for b in baris[2:]]
    th = "".join(f'<th style="text-align:left;padding:10px 12px;border-bottom:2px solid {bp.NAVY};color:{bp.NAVY}">{inline(c)}</th>' for c in kepala)
    tr = "".join("<tr>" + "".join(f'<td style="padding:10px 12px;border-bottom:1px solid {bp.GARIS}">{inline(c)}</td>' for c in r) + "</tr>" for r in isi)
    return f'<table style="width:100%;border-collapse:collapse;font-size:16px"><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table>'


def blok(md):
    """Markdown → daftar widget Elementor."""
    out, para, bul, tab = [], [], [], []

    def tutup():
        nonlocal para, bul, tab
        if para:
            out.append(bp.teks("<p>" + inline(" ".join(para)) + "</p>", "#636363", 17))
        if bul:
            out.append(bp.teks("<ul style='margin:0;padding-left:22px'>" + "".join(f"<li style='margin:4px 0'>{inline(b)}</li>" for b in bul) + "</ul>", "#636363", 17))
        if tab:
            out.append(bp.teks(tabel_html(tab), "#161616", 16))
        para, bul, tab = [], [], []

    for baris in md.split("\n"):
        b = baris.rstrip()
        if not b.strip():
            tutup(); continue
        if b.startswith("### "):
            tutup(); out.append(be.judul_katur(b[4:], "h3", 26, -1.2)); continue
        if b.startswith("## "):
            tutup(); out.append(be.judul_katur(b[3:], "h2", 40, -1.7)); continue
        if b.startswith("> "):
            tutup()
            out.append(bp.tile([bp.subjudul(b[2:], bp.DARK)], bp.LIME))
            continue
        m = re.fullmatch(r"!\[(.*?)\]\((.+?)\)", b.strip())
        if m:   # gambar: berkas di manual/prodi-gambar/ (disalin ke data/prodi/ oleh manual.py)
            tutup()
            out.append(be.widget("image", image={"url": f"{be.BASE}/prodi/{m.group(2)}", "id": "", "alt": m.group(1)},
                                 image_size="full", width=be.ukuran(100, "%"), image_border_radius=bp.sudut(10)))
            continue
        if b.strip() == "[[lorem]]":
            tutup(); out.append(bp.teks(f'<p class="kt-lorem" data-lorem="1" style="{GAYA_LOREM}">{LOREM}</p>', "#7a5d00", 16, None)); continue
        if b.startswith("- "):
            if para:
                tutup()
            bul.append(b[2:]); continue
        if b.startswith("|"):
            tab.append(b); continue
        if bul:
            tutup()
        para.append(b.strip())
    tutup()
    return out


def halaman(md, judul):
    anak = blok(md)
    isi = be.container(anak, content_width="full", flex_direction="column", flex_gap=be.gap(16))
    isi["isInner"] = True
    return be.halaman_katur([isi]), judul


# ---------------------------------------------------------------- rancangan v2: hero + kartu bento + akordeon
HERO_BG = "#073C64"


def kapital(s):
    return s


def html_blok(md):
    """Markdown sederhana → HTML ber-gaya inline (untuk isi akordeon / kartu; atribut style lolos dari server UGM)."""
    out, para, bul, tab = [], [], [], []
    H = "font-family:'Plus Jakarta Sans',sans-serif;font-weight:400;color:#161616;"

    def tutup():
        nonlocal para, bul, tab
        if para:
            out.append("<p style='margin:0 0 12px'>" + inline(" ".join(para)) + "</p>")
        if bul:
            out.append("<ul style='margin:0 0 14px;padding-left:22px'>" + "".join(f"<li style='margin:4px 0'>{inline(b)}</li>" for b in bul) + "</ul>")
        if tab:
            out.append("<div style='overflow-x:auto;margin:8px 0 16px'>" + tabel_html(tab) + "</div>")
        para, bul, tab = [], [], []

    for baris in md.split("\n"):
        b = baris.rstrip()
        if not b.strip():
            tutup(); continue
        if b.startswith("### "):
            tutup(); out.append(f"<h4 style=\"{H}font-size:22px;letter-spacing:-1px;margin:22px 0 8px\">{inline(b[4:])}</h4>"); continue
        if b.startswith("> "):
            tutup(); out.append(f"<div style=\"background:{bp.LIME};color:{bp.DARK};border-radius:10px;padding:16px 20px;margin:0 0 12px;font-family:'Plus Jakarta Sans',sans-serif;font-size:20px;letter-spacing:-.8px\">{inline(b[2:])}</div>"); continue
        m = re.fullmatch(r"!\[(.*?)\]\((.+?)\)", b.strip())
        if m:
            tutup(); out.append(f"<img src=\"{be.BASE}/prodi/{m.group(2)}\" alt=\"{bp.esc(m.group(1))}\" style=\"width:100%;height:auto;border-radius:10px;margin:8px 0 16px;display:block\">"); continue
        if b.strip() == "[[lorem]]":
            tutup(); out.append(f'<p class="kt-lorem" data-lorem="1" style="{GAYA_LOREM}">{LOREM}</p>'); continue
        if b.startswith("- "):
            if para:
                tutup()
            bul.append(b[2:]); continue
        if b.startswith("|"):
            tab.append(b); continue
        if bul:
            tutup()
        para.append(b.strip())
    tutup()
    return "".join(out)


def bagi(md):
    """→ (meta, bagian[(judul, isi)]); meta dari baris @hero k=v / @kartu a|b|c."""
    meta = {"hero": {}, "kartu": []}
    sisa, bagian = [], []
    for b in md.split("\n"):
        m = re.match(r"@hero (\w+)=(.*)", b)
        if m:
            meta["hero"][m.group(1)] = m.group(2).strip(); continue
        if b.startswith("@kartu "):
            meta["kartu"].append([x.strip() for x in b[7:].split("|")]); continue
        sisa.append(b)
    for b in "\n".join(sisa).split("\n## "):
        b = b.strip()
        if not b:
            continue
        j, _, isi = b.removeprefix("## ").partition("\n")
        bagian.append((j.strip(), isi.strip()))
    return meta, bagian


def label_kecil(s, warna):
    return bp.kicker(s, warna)


def angka(s, warna):
    besar = 64 if len(s) <= 5 else 44 if len(s) <= 8 else 36   # skala agar teks panjang ("General Engineering", "144–150") tidak meluber
    w = be.judul_katur(s, "div", besar, -4 if besar == 64 else -2)
    w["settings"]["title_color"] = warna
    w["settings"].pop("__globals__", None)
    w["settings"]["typography_font_size_mobile"] = be.ukuran_(44)
    return w


def kartu_bento(k):
    gaya, label, nilai, ket = k
    bg = {"lime": bp.LIME, "navy": bp.NAVY, "putih": "#FFFFFF", "abu": bp.ABU}[gaya]
    ink, isi = ("#FFFFFF", "rgba(255,255,255,.86)") if gaya == "navy" else (bp.DARK if gaya == "lime" else "#161616", bp.DARK if gaya == "lime" else "#636363")
    t = bp.tile([label_kecil(label, "#FFFFFF" if gaya == "navy" else bp.NAVY if gaya != "lime" else bp.DARK), angka(nilai, ink), bp.teks(f"<p>{inline(ket)}</p>", isi, 16, None)],
                bg, 23, garis=(gaya == "putih"))
    t["settings"]["width_tablet"] = be.ukuran(48.5, "%")
    t["settings"]["flex_gap"] = be.gap(6)
    return t


def hero(judul, lead, hero_meta):
    kiri = [bp.kicker(hero_meta.get("kicker", ""), bp.LIME),
            be.judul_katur(judul, "h2", 52, -3)]
    kiri[1]["settings"]["title_color"] = "#FFFFFF"
    kiri[1]["settings"].pop("__globals__", None)
    kiri[1]["settings"]["typography_font_size_mobile"] = be.ukuran_(30)
    kiri.append(bp.teks(f"<p>{inline(lead)}</p>", "rgba(255,255,255,.88)", 18, None))
    k = be.container(kiri, content_width="full", flex_direction="column", flex_gap=be.gap(16), justify_content="center",
                     width=be.ukuran(55, "%"), width_mobile=be.ukuran(100, "%"))
    gambar = hero_meta.get("gambar")
    anak = [k]
    if gambar:
        img = be.widget("image", image={"url": f"{be.BASE}/prodi/{gambar}", "id": "", "alt": judul}, image_size="full",
                        width=be.ukuran(100, "%"), image_border_radius=bp.sudut(10))
        anak.append(be.container([img], content_width="full", width=be.ukuran(45, "%"), width_mobile=be.ukuran(100, "%")))
    return be.container(anak, content_width="full", flex_direction="row", flex_direction_mobile="column", flex_gap=be.gap(40),
                        flex_align_items="center", background_background="classic", background_color=HERO_BG,
                        border_radius=bp.sudut(10), padding=bp.ruang(48),
                        padding_mobile=bp.ruang(24))


def akordeon(judul, isi_md):
    tab = {"_id": be.eid()[:7], "tab_title": judul, "tab_content": html_blok(isi_md)}
    a = be.widget("toggle", tabs=[tab], selected_icon={"value": "fas fa-plus", "library": "fa-solid"},
                  selected_active_icon={"value": "fas fa-minus", "library": "fa-solid"}, icon_align="right",
                  title_html_tag="h3", border_width=be.ukuran(0), title_color="#161616", tab_active_color=bp.NAVY,
                  icon_color=bp.NAVY, icon_active_color=bp.NAVY, content_color="#636363",
                  title_typography_typography="custom", title_typography_font_family="Plus Jakarta Sans",
                  title_typography_font_weight="400", title_typography_font_size=be.ukuran_(26),
                  title_typography_letter_spacing={"unit": "px", "size": -1.3, "sizes": []},
                  tab_typography_typography="custom", content_typography_typography="custom",
                  content_typography_font_family="Barlow", content_typography_font_size=be.ukuran_(17))
    return be.container([a], content_width="full", background_background="classic", background_color="#FFFFFF",
                        border_border="solid", border_width={"unit": "px", "top": "1", "right": "1", "bottom": "1", "left": "1", "isLinked": True},
                        border_color=bp.GARIS, border_radius=bp.sudut(10), padding=bp.ruang(8))


def kartu_visi(judul, isi_md):
    isi = [bp.kicker(judul, bp.DARK)]
    for b in isi_md.split("\n\n"):
        b = b.strip()
        if b.startswith("> "):
            w = bp.subjudul(b[2:], bp.DARK)
            w["settings"]["typography_font_size"] = be.ukuran_(28)
            isi.append(w)
        elif b:
            isi.append(bp.teks(html_blok(b), bp.DARK, 17, None))
    return bp.tile(isi, bp.LIME)


def halaman_v2(md):
    meta, bagian = bagi(md)
    (j0, i0), *lain = bagian
    paras = [p.strip() for p in i0.split("\n\n") if p.strip()]
    anak = [hero(meta["hero"].get("judul", j0), paras[0], meta["hero"])]
    if meta["kartu"]:
        anak.append(be.container([kartu_bento(k) for k in meta["kartu"]], content_width="full", flex_direction="row",
                                 flex_wrap="wrap", flex_gap=be.gap(16), flex_direction_mobile="column"))
    if len(paras) > 1:
        t = bp.teks(html_blok("\n\n".join(paras[1:])), "#636363", 17)
        t["settings"]["text_columns"] = "2"
        t["settings"]["text_columns_mobile"] = "1"
        t["settings"]["column_gap"] = {"unit": "px", "size": 40, "sizes": []}
        anak.append(t)
    for j, isi in lain:
        if j.lower().startswith("mitra"):
            continue    # slideshow logo mitra sudah ada di templat tema
        anak.append(kartu_visi(j, isi) if j.lower().startswith("visi") else akordeon(j, isi))
    return be.halaman_katur(anak)


def main():
    for nama, judul in (("teknik-nuklir", "DTNTF Katur – Prodi Sarjana Teknik Nuklir (/prodi/)"),
                        ("teknik-fisika", "DTNTF Katur – Prodi S1 Teknik Fisika (/prodi-s1-teknik-fisika/)")):
        be._n[0] = 0
        md = (ROOT / "manual" / "prodi" / f"{nama}.md").read_text(encoding="utf-8")
        h = halaman_v2(md) if "@hero" in md else halaman(md, judul)[0]
        doc = {"version": "0.4", "title": judul, "type": "container", "content": [h], "page_settings": []}
        (ROOT / "elementor" / f"prodi-{nama}.json").write_text(json.dumps(doc, ensure_ascii=False), encoding="utf-8")
        print(f"Tertulis elementor/prodi-{nama}.json")


if __name__ == "__main__":
    main()
