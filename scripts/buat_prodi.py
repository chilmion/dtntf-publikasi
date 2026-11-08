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


def main():
    for nama, judul in (("teknik-nuklir", "DTNTF Katur – Prodi Sarjana Teknik Nuklir (/prodi/)"),
                        ("teknik-fisika", "DTNTF Katur – Prodi S1 Teknik Fisika (/prodi-s1-teknik-fisika/)")):
        be._n[0] = 0
        md = (ROOT / "manual" / "prodi" / f"{nama}.md").read_text(encoding="utf-8")
        h, _ = halaman(md, judul)
        doc = {"version": "0.4", "title": judul, "type": "container", "content": [h], "page_settings": []}
        (ROOT / "elementor" / f"prodi-{nama}.json").write_text(json.dumps(doc, ensure_ascii=False), encoding="utf-8")
        print(f"Tertulis elementor/prodi-{nama}.json")


if __name__ == "__main__":
    main()
