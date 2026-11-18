#!/usr/bin/env python3
"""
Buat elementor/katur-mitra.json (isi halaman Mitra: logo, sorotan bento, kabar kerja sama) dan uji-mitra.html (pratinjau lokal).
Data: data/mitra/mitra.json + data/mitra/artikel.json (artikel dari halaman Mitra tf.ugm.ac.id).
Widget: widget/katur-mitra.html.   python3 scripts/buat_mitra.py [URL-data-GitHub-Pages]
"""
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import buat_elementor as be  # noqa: E402

ROOT = be.ROOT


def main():
    be.BASE = sys.argv[1] if len(sys.argv) > 1 else be.BASE
    be._n[0] = 0
    mentah = (ROOT / "widget" / "katur-mitra.html").read_text(encoding="utf-8")
    h = mentah.replace(be.PLACEHOLDER_BASE, be.BASE)
    isi = be.container([be.widget("html", html=h)], content_width="full")
    isi["isInner"] = True
    doc = {"version": "0.4", "title": "DTNTF Katur – Mitra (/mitra/)", "type": "container",
           "content": [be.halaman_katur([isi])], "page_settings": []}
    (ROOT / "elementor" / "katur-mitra.json").write_text(json.dumps(doc, ensure_ascii=False), encoding="utf-8")
    uji = ("<!doctype html><meta charset=utf-8><meta name=viewport content='width=device-width,initial-scale=1'><title>Uji – Mitra</title>"
           "<link href='https://fonts.googleapis.com/css2?family=Barlow:wght@400;500;600&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap' rel=stylesheet>"
           "<body style='margin:0;font-family:Barlow'><div style='max-width:1180px;margin:0 auto;padding:60px 20px 80px'>" + mentah.replace(be.PLACEHOLDER_BASE, "./data") + "</div>")
    (ROOT / "uji-mitra.html").write_text(uji, encoding="utf-8")
    print(f"Tertulis elementor/katur-mitra.json dan uji-mitra.html (data-base = {be.BASE})")


if __name__ == "__main__":
    main()
