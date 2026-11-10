#!/usr/bin/env python3
"""
Pecah widget/*.html menjadi aset terpisah untuk web UGM (server UGM membuang <style>/<script> dari widget HTML):

  data/ugm/<nama>.css   dari <style>
  data/ugm/<nama>.js    dari <script> (menunggu DOM siap; tanpa document.currentScript)

Halaman WordPress hanya berisi markup widget + satu baris pemuat di kotak "Custom JS" Essential Addons
(JS itu tidak boleh memuat & < > "), lihat pemuat() di bawah. Aset disajikan GitHub Pages dan ikut ter-update otomatis.

    python3 scripts/buat_aset_ugm.py
"""
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "ugm"
BASE = "https://chilmion.github.io/dtntf-publikasi/data/ugm"


def pecah(nama):
    t = (ROOT / "widget" / f"{nama}.html").read_text(encoding="utf-8")
    css = "\n".join(re.findall(r"<style[^>]*>(.*?)</style>", t, re.S))
    # token kit Elementor (--e-global-*) berbeda di tiap situs: pakai nilai cadangan v1 langsung
    css = re.sub(r"var\(--e-global-[\w-]+\s*,\s*([^()]+?)\)", r"\1", css)
    js = "\n;\n".join(re.findall(r"<script[^>]*>(.*?)</script>", t, re.S))
    js = re.sub(r"document\.currentScript\.parentNode\.querySelector\(([^)]*)\)", "null", js)
    js = "(function(){function __go(){\n" + js + "\n}\nif(document.readyState==='loading'){document.addEventListener('DOMContentLoaded',__go)}else{__go()}})();\n"
    return css, js


def pemuat(nama):
    """Satu baris JS aman untuk kotak Custom JS (tanpa karakter & < > ")."""
    return ("(function(){var d=document;var l=d.createElement('link');l.rel='stylesheet';l.href='%s/%s.css';d.head.appendChild(l);"
            "var s=d.createElement('script');s.src='%s/%s.js';d.head.appendChild(s)})();" % (BASE, nama, BASE, nama))


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for p in sorted((ROOT / "widget").glob("katur-*.html")):
        nama = p.stem
        css, js = pecah(nama)
        (OUT / f"{nama}.css").write_text(css, encoding="utf-8")
        (OUT / f"{nama}.js").write_text(js, encoding="utf-8")
        print(f"data/ugm/{nama}.css ({len(css)}) .js ({len(js)})")
        assert not re.search(r"[&<>\"]", pemuat(nama))


if __name__ == "__main__":
    main()
