#!/usr/bin/env python3
"""
Buat elementor/katur-pengabdian.json — halaman Pengabdian kepada Masyarakat (slug /pengabdian/),
rekap seperti halaman publikasi tetapi hanya kategori Pengabdian: bento + daftar kegiatan yang bisa
disaring (tahun, dosen, kata kunci). Data: kategori "Pengabdian kepada Masyarakat" dari SINTA
(data/agregat). Widget: widget/katur-pengabdian.html.

    python3 scripts/buat_pengabdian.py [URL-data-GitHub-Pages]
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
    h = (ROOT / "widget" / "katur-pengabdian.html").read_text(encoding="utf-8").replace(be.PLACEHOLDER_BASE, be.BASE)
    isi = be.container([be.widget("html", html=h)], content_width="full")
    isi["isInner"] = True
    doc = {"version": "0.4", "title": "DTNTF Katur – Pengabdian (/pengabdian/)", "type": "container",
           "content": [be.halaman_katur([isi])], "page_settings": []}
    (ROOT / "elementor" / "katur-pengabdian.json").write_text(json.dumps(doc, ensure_ascii=False), encoding="utf-8")
    print(f"Tertulis elementor/katur-pengabdian.json  (data-base = {be.BASE})")


if __name__ == "__main__":
    main()
