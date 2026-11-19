#!/usr/bin/env python3
"""
Halaman prodi untuk tf.ugm.ac.id yang menyaring HTML widget: versi NATIVE dari buat_prodi.py.
Tanpa <style>/<svg>/<script>; SVG -> PNG (data/prodi/png-tf/, dibuat dengan Chrome headless), kartu dokumen bergaya inline.
URL gambar di tf diambil dari data/prodi/png-tf/urls.json (nama -> URL media tf; diisi setelah unggah).
    python3 scripts/buat_native_prodi.py   ->  elementor/native/prodi-<nama>.json
"""
import json, pathlib, re, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import buat_prodi as bpr  # noqa: E402
import buat_elementor as be  # noqa: E402
import buat_profil_dosen as bp  # noqa: E402

ROOT = be.ROOT
PNG = ROOT / "data" / "prodi" / "png-tf"
URLS = json.loads((PNG / "urls.json").read_text()) if (PNG / "urls.json").exists() else {}


def url_png(nama):
    nama = nama.removesuffix(".svg")
    return URLS.get(nama, f"https://raw.githubusercontent.com/chilmion/dtntf-publikasi/main/data/prodi/png-tf/{nama}.png")


def dok_kartu(judul, ket, sampul, tag, url=""):
    cover = ("flex:0 0 104px;aspect-ratio:3/4;border-radius:8px;background:linear-gradient(165deg,#073C64 0%,#1A2C43 100%);"
             "color:#fff;padding:11px 10px;display:flex;flex-direction:column;justify-content:space-between;border-bottom:5px solid #C8E86D;box-sizing:border-box")
    t = "display:block;color:#fff;word-spacing:0;"
    btn = ("display:inline-block;padding:10px 18px;border-radius:999px;background:#073C64;color:#fff;font-size:14px;"
           "font-weight:600;text-decoration:none;line-height:1")
    a = f'<a style="{btn}" href="{url}">' if url else f'<a style="{btn};opacity:.55" title="Dokumen segera tersedia">'
    return (f'<div style="display:flex;gap:18px;align-items:center;padding:18px;border:1px solid #E3E3E3;border-radius:16px;background:#fff">'
            f'<div style="{cover}"><small style="{t}font-size:7px;line-height:1.3;font-weight:600;opacity:.85">DEPARTEMEN TEKNIK NUKLIR DAN TEKNIK FISIKA · UGM</small>'
            f'<b style="{t}font-size:13px;line-height:1.2;font-weight:800">{bpr.inline(sampul).replace(";", "<br>")}</b>'
            f'<i style="{t}font-style:normal;font-size:7px;font-weight:700;color:#C8E86D">{bpr.inline(tag)}</i></div>'
            f'<div style="min-width:0"><h4 style="margin:0 0 4px;font-size:17px;line-height:1.3;font-weight:700;color:#073C64;word-spacing:0;letter-spacing:0">{bpr.inline(judul)}</h4>'
            f'<p style="margin:0 0 14px;font-size:14px;line-height:1.5;color:#5B6670">{bpr.inline(ket)}</p>{a}↓ Unduh dokumen</a></div></div>')


def dok_grid(daftar):
    return ('<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,440px),1fr));gap:20px;margin:20px 0 8px">'
            + "".join(dok_kartu(*d) for d in daftar) + "</div>")


bpr.dok_grid = dok_grid


class _P(pathlib.PurePosixPath):
    pass


_orig_html_blok = bpr.html_blok


def html_blok(md):
    def sub(m):
        return f"![{m.group(1)}]({url_png(m.group(2))})"
    md = re.sub(r"!\[(.*?)\]\(svg:(.+?)\)", lambda m: f"![{m.group(1)}](TFPNG:{m.group(2)})", md)
    out = _orig_html_blok(md)
    # gambar TFPNG: diubah _orig menjadi <img src=".../prodi/TFPNG:nama">
    return re.sub(r'src="[^"]*?TFPNG:([^"]+)"', lambda m: f'src="{url_png(m.group(1))}"', out)


bpr.html_blok = html_blok
_orig_hero = bpr.hero


def hero(judul, lead, hm):
    hm = dict(hm)
    if hm.get("gambar", "").endswith(".svg"):
        hm["gambar"] = "TFPNG:" + hm["gambar"][:-4]
    w = _orig_hero(judul, lead, hm)
    s = json.dumps(w, ensure_ascii=False)
    s = re.sub(r'https?://[^"]*?/prodi/TFPNG:([^"]+)', lambda m: url_png(m.group(1)), s)
    return json.loads(s)


bpr.hero = hero


# ---------------------------------------------------------------- akordeon NATIVE (nested-accordion; isi = container + widget native)
def _h(tek, ukur, warna, bobot="700", tag="h4", font="Plus Jakarta Sans", spasi=0):
    return be.widget("heading", title=tek, header_size=tag, title_color=warna, typography_typography="custom",
                     typography_font_family=font, typography_font_weight=bobot, typography_font_size=be.ukuran_(ukur),
                     typography_letter_spacing={"unit": "px", "size": spasi, "sizes": []})


def kartu_dok(judul, ket, sampul, tag, url=""):
    link = {"url": url, "is_external": "", "nofollow": "", "custom_attributes": ""}
    cover = be.container([_h("DEPARTEMEN TEKNIK NUKLIR DAN TEKNIK FISIKA · UGM", 8, "#FFFFFF", "600", "span", "Barlow"),
                          _h(sampul.replace(";", " "), 15, "#FFFFFF", "800", "span"),
                          _h(tag, 8, "#C8E86D", "700", "span", "Barlow")],
                         content_width="full", flex_direction="column", justify_content="space-between", width=be.ukuran(112, "px"),
                         width_mobile=be.ukuran(100, "%"), background_background="classic", background_color="#073C64",
                         border_radius=bp.sudut(8), padding=bp.ruang(12), flex_gap=be.gap(10), _title="Sampul dokumen")
    tombol = be.widget("button", text="Unduh dokumen", link=link, align="left", background_color="#073C64", button_text_color="#FFFFFF",
                       border_radius=bp.sudut(999), typography_typography="custom", typography_font_family="Barlow",
                       typography_font_weight="600", typography_font_size=be.ukuran_(14),
                       text_padding={"unit": "px", "top": "10", "right": "18", "bottom": "10", "left": "18", "isLinked": False})
    isi = be.container([_h(judul, 17, "#073C64"), bp.teks(f"<p>{bpr.inline(ket)}</p>", "#5B6670", 14, None), tombol],
                       content_width="full", flex_direction="column", flex_gap=be.gap(8), flex_size="grow", _title="Isi kartu dokumen")
    return be.container([cover, isi], content_width="full", flex_direction="row", flex_direction_mobile="column",
                        flex_gap=be.gap(18), flex_align_items="center", width=be.ukuran(100, "%"),
                        background_background="classic", background_color="#FFFFFF", border_border="solid",
                        border_width={"unit": "px", "top": "1", "right": "1", "bottom": "1", "left": "1", "isLinked": True},
                        border_color=bp.GARIS, border_radius=bp.sudut(16), padding=bp.ruang(18), _title="Kartu dokumen: " + judul)


def widget_blok(md):
    """Markdown -> daftar widget/container native (tanpa HTML kustom)."""
    out, para, bul, tab, dok = [], [], [], [], []

    def tutup():
        nonlocal para, bul, tab
        if para:
            out.append(bp.teks("<p>" + bpr.inline(" ".join(para)) + "</p>", "#636363", 17, None))
        if bul:
            out.append(bp.teks("<ul>" + "".join(f"<li>{bpr.inline(b)}</li>" for b in bul) + "</ul>", "#636363", 17, None))
        if tab:
            out.append(bp.teks(bpr.tabel_html(tab), "#161616", 16, None))
        para, bul, tab = [], [], []

    def tutup_dok():
        if dok:
            out.append(be.container([kartu_dok(*d) for d in dok], content_width="full", flex_direction="row", flex_wrap="wrap",
                                    flex_gap=be.gap(20), flex_direction_mobile="column", _title="Dokumen"))
            dok.clear()

    for baris in md.split("\n"):
        b = baris.rstrip()
        if not b.strip():
            tutup(); continue
        md_ = re.fullmatch(r"\[\[dokumen (.+?)\]\]", b.strip())
        if not md_:
            tutup_dok()
        if md_:
            tutup(); dok.append([x.strip() for x in md_.group(1).split("|")]); continue
        if b.startswith("### "):
            tutup(); out.append(_h(b[4:], 22, "#161616", "400", "h4", spasi=-1)); continue
        if b.startswith("> "):
            tutup(); out.append(bp.tile([bp.subjudul(b[2:], bp.DARK)], bp.LIME)); continue
        m = re.fullmatch(r"!\[(.*?)\]\((.+?)\)", b.strip())
        if m:
            tutup(); nm = m.group(2)
            u = url_png(nm[4:]) if nm.startswith("svg:") else URLS.get(nm.rsplit(".", 1)[0], f"{be.BASE}/prodi/{nm}")
            out.append(be.widget("image", image={"url": u, "id": "", "alt": m.group(1)}, image_size="full",
                                 width=be.ukuran(100, "%"), image_border_radius=bp.sudut(10), _title="Gambar: " + m.group(1)[:40]))
            continue
        if b.strip() == "[[lorem]]":
            tutup(); out.append(bp.teks(f'<p style="{bpr.GAYA_LOREM}">{bpr.LOREM}</p>', "#7a5d00", 16, None)); continue
        if b.startswith("- "):
            if para:
                tutup()
            bul.append(b[2:]); continue
        if b.startswith("|"):
            tab.append(b); continue
        if bul:
            tutup()
        para.append(b.strip())
    tutup(); tutup_dok()
    return out


def akordeon_native(bagian):
    """bagian = [(judul, isi_md)] -> satu widget nested-accordion; tiap item = container berisi widget native."""
    items, anak = [], []
    for j, isi in bagian:
        iid = be.eid()[:7]
        items.append({"item_title": j, "_id": iid, "element_css_id": ""})
        anak.append(be.container(widget_blok(isi), content_width="full", flex_direction="column", flex_gap=be.gap(14),
                                 padding=bp.ruang(16), _title=j))
    w = be.widget("nested-accordion", items=items, title_tag="h3", default_state="all_collapsed", max_items_expended="one",
                  accordion_item_title_icon={"value": "fas fa-plus", "library": "fa-solid"},
                  accordion_item_title_icon_active={"value": "fas fa-minus", "library": "fa-solid"},
                  accordion_item_title_icon_position="end", title_typography_typography="custom",
                  title_typography_font_family="Plus Jakarta Sans", title_typography_font_weight="400",
                  title_typography_font_size=be.ukuran_(26), title_typography_letter_spacing={"unit": "px", "size": -1.3, "sizes": []},
                  normal_title_color="#161616", hover_title_color="#073C64", active_title_color="#073C64",
                  _title="Akordeon")
    w["elements"] = anak
    return be.container([w], content_width="full", background_background="classic", background_color="#FFFFFF",
                        border_border="solid", border_width={"unit": "px", "top": "1", "right": "1", "bottom": "1", "left": "1", "isLinked": True},
                        border_color=bp.GARIS, border_radius=bp.sudut(10), padding=bp.ruang(8), _title="Bagian akordeon")


_orig_v2 = bpr.halaman_v2


def halaman_v2(md):
    meta, bagian = bpr.bagi(md)
    (j0, i0), *lain = bagian
    paras = [p.strip() for p in i0.split("\n\n") if p.strip()]
    anak = [bpr.hero(meta["hero"].get("judul", j0), paras[0], meta["hero"])]
    anak[0]["settings"]["_title"] = "Hero"
    if meta["kartu"]:
        anak.append(be.container([bpr.kartu_bento(k) for k in meta["kartu"]], content_width="full", flex_direction="row", flex_wrap="wrap",
                                 flex_gap=be.gap(16), flex_direction_mobile="column", _title="Kartu ringkas"))
    if len(paras) > 1:
        t = bp.teks("".join("<p>" + bpr.inline(p) + "</p>" for p in paras[1:]), "#636363", 17)
        t["settings"]["text_columns"] = "2"; t["settings"]["text_columns_mobile"] = "1"
        t["settings"]["column_gap"] = {"unit": "px", "size": 40, "sizes": []}
        anak.append(t)
    akor = []
    for j, isi in lain:
        if j.lower().startswith("mitra"):
            continue
        if j.lower().startswith("visi"):
            anak.append(bpr.kartu_visi(j, isi))
        else:
            akor.append((j, isi))
    if akor:
        anak.append(akordeon_native(akor))
    h = be.halaman_katur(anak)
    h["settings"]["_title"] = "Halaman prodi"
    return h


bpr.halaman_v2 = halaman_v2


if __name__ == "__main__":
    for nama, judul in (("teknik-nuklir", "Prodi Sarjana Teknik Nuklir"), ("teknik-fisika", "Prodi S1 Teknik Fisika"),
                        ("iup-teknik-nuklir", "IUP Teknik Nuklir"), ("magister-teknik-fisika", "Magister Teknik Fisika")):
        be._n[0] = 0
        md = (ROOT / "manual" / "prodi" / f"{nama}.md").read_text(encoding="utf-8")
        h = bpr.halaman_v2(md) if "@hero" in md else bpr.halaman(md, judul)[0]
        s = json.dumps({"version": "0.4", "title": judul, "type": "container", "content": [h], "page_settings": []}, ensure_ascii=False)
        s = re.sub(r"https://chilmion\.github\.io/dtntf-publikasi/data/prodi/([A-Za-z0-9_.-]+)", lambda m: URLS.get(m.group(1).rsplit(".", 1)[0], m.group(0)), s)
        s = s.replace("[[lorem]]", bpr.LOREM)
        assert "<style" not in s and "<svg" not in s and "<script" not in s and '"widgetType": "html"' not in s, nama
        (ROOT / "elementor" / "native" / f"prodi-{nama}.json").write_text(s, encoding="utf-8")
        print("ok", nama, len(s))
