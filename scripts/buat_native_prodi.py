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

if __name__ == "__main__":
    for nama, judul in (("teknik-nuklir", "Prodi Sarjana Teknik Nuklir"), ("teknik-fisika", "Prodi S1 Teknik Fisika"),
                        ("iup-teknik-nuklir", "IUP Teknik Nuklir"), ("magister-teknik-fisika", "Magister Teknik Fisika")):
        be._n[0] = 0
        md = (ROOT / "manual" / "prodi" / f"{nama}.md").read_text(encoding="utf-8")
        h = bpr.halaman_v2(md) if "@hero" in md else bpr.halaman(md, judul)[0]
        s = json.dumps({"version": "0.4", "title": judul, "type": "container", "content": [h], "page_settings": []}, ensure_ascii=False)
        s = re.sub(r"https://chilmion\.github\.io/dtntf-publikasi/data/prodi/([A-Za-z0-9_.-]+)", lambda m: URLS.get(m.group(1).rsplit(".", 1)[0], m.group(0)), s)
        assert "<style" not in s and "<svg" not in s and "<script" not in s, nama
        (ROOT / "elementor" / "native" / f"prodi-{nama}.json").write_text(s, encoding="utf-8")
        print("ok", nama, len(s))
