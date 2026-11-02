#!/usr/bin/env python3
"""
Buat 38 templat Elementor profil dosen (satu berkas per dosen) di elementor/profil/<slug>.json.

Isi tiap berkas: foto, nama, gelar, tautan, tombol SINTA (dari dosen.csv + manual/dosen-info.csv)
sebagai widget Elementor BIASA (bisa diedit), ditambah satu widget HTML `katur-profil-cv.html`
(sudah diisi data-slug dosen itu) yang menyusun profil mengikuti CV: data diri, pendidikan,
sertifikat, pekerjaan, organisasi, penghargaan, kerjasama & penelitian, HKI, jurnal, prosiding, buku.
Tanpa Skor SINTA. Bagian kosong = lorem ipsum (kelas .kt-lorem) sampai data diisi.

Selain 38 berkas di elementor/profil/, dibuat elementor/profil-38.zip (berkas JSON di akar ZIP,
tanpa folder) untuk impor massal.

    python3 scripts/buat_profil_dosen.py [URL-data-GitHub-Pages]
"""

import csv
import json
import pathlib
import sys
import zipfile

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import buat_elementor as be  # noqa: E402

ROOT = be.ROOT
OUT = ROOT / "elementor" / "profil"
NAVY, LIME, DARK, ABU, GARIS = "#073C64", "#C8E86D", "#1A2C43", "#F5F5F5", "#E3E3E3"


def sudut(n=10):
    return {"unit": "px", "top": str(n), "right": str(n), "bottom": str(n), "left": str(n), "isLinked": True}


def ruang(n=24):
    return {"unit": "px", "top": str(n), "right": str(n), "bottom": str(n), "left": str(n), "isLinked": True}


def teks(html, warna="#636363", ukuran=16, glob="text"):
    return be.widget("text-editor", editor=html, text_color=warna,
                     typography_typography="custom", typography_font_family="Barlow",
                     typography_font_weight="400", typography_font_size=be.ukuran_(ukuran),
                     typography_line_height={"unit": "em", "size": 1.5, "sizes": []},
                     **({"__globals__": {"text_color": f"globals/colors?id={glob}"}} if glob else {}))


def kicker(teks_, warna=NAVY):
    return be.widget("heading", title=teks_, header_size="span", title_color=warna,
                     typography_typography="custom", typography_font_family="Barlow",
                     typography_font_weight="600", typography_font_size=be.ukuran_(12),
                     typography_text_transform="uppercase",
                     typography_letter_spacing={"unit": "px", "size": 0.8, "sizes": []})


def judul(teks_, tag="h1"):
    return be.widget("heading", title=teks_, header_size=tag, title_color="#161616",
                     typography_typography="custom", typography_font_family="Plus Jakarta Sans",
                     typography_font_weight="400", typography_font_size=be.ukuran_(56),
                     typography_font_size_tablet=be.ukuran_(40), typography_font_size_mobile=be.ukuran_(28),
                     typography_line_height={"unit": "em", "size": 1.2, "sizes": []},
                     typography_letter_spacing={"unit": "px", "size": -3.4, "sizes": []},
                     __globals__={"title_color": "globals/colors?id=primary"})


def subjudul(teks_, warna="#161616"):
    return be.widget("heading", title=teks_, header_size="h3", title_color=warna,
                     typography_typography="custom", typography_font_family="Plus Jakarta Sans",
                     typography_font_weight="400", typography_font_size=be.ukuran_(24),
                     typography_font_size_mobile=be.ukuran_(18),
                     typography_line_height={"unit": "em", "size": 1.2, "sizes": []},
                     typography_letter_spacing={"unit": "px", "size": -1.3, "sizes": []})


def tile(anak, bg, lebar=None, garis=False):
    s = dict(content_width="full", background_background="classic", background_color=bg,
             border_radius=sudut(10), padding=ruang(24), flex_direction="column", flex_gap=be.gap(8))
    if garis:
        s.update(border_border="solid", border_width={"unit": "px", "top": "1", "right": "1", "bottom": "1",
                                                      "left": "1", "isLinked": True}, border_color=GARIS)
    if lebar:
        s.update(width=be.ukuran(lebar, "%"), width_mobile=be.ukuran(100, "%"))
    return be.container(anak, **s)


def kelompok_dari(bidang):
    b = (bidang or "").lower()
    return "Teknik Nuklir" if b.startswith("rekayasa nuklir") else "Teknik Fisika" if b.startswith("rekayasa fisika") else "Dosen"


def esc(s):
    return (s or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def profil(r, i, base, data_html):
    nama, slug, sid = r["nama"].strip(), r["slug"].strip(), (r.get("sinta_id") or "").strip()
    gelar = (r.get("gelar") or "").strip()
    kel = kelompok_dari(i.get("bidang_ilmu"))

    # ---- kolom kiri: foto + tautan (data diri, riwayat, dst. ada di widget HTML di kanan)
    url_foto = (r.get("foto_url") or "").strip() or "https://placehold.co/400x500/E8EEF4/073C64?text=Foto"
    foto = be.widget("image", image={"url": url_foto, "id": "", "alt": nama}, image_size="full",
                     width=be.ukuran(100, "%"), image_border_radius=sudut(10))
    baris = []
    tautan = []
    for pasang in (i.get("tautan") or "").split(" ;; "):
        if "::" in pasang:
            lb, u = pasang.split("::", 1)
            tautan.append(f'<a href="{esc(u)}" target="_blank" rel="noopener" style="color:#fff">{esc(lb)} ↗</a>')
    if tautan:
        baris.append('<strong style="color:#fff">Tautan</strong><br>' + "<br>".join(tautan))
    kontak = [kicker("Tautan", "#FFFFFF")]
    if baris:
        kontak.append(teks("<p>" + "</p><p>".join(baris) + "</p>", "#FFFFFF", 16, None))
    if sid:
        kontak.append(be.widget("button", text="Profil SINTA ↗",
                                link={"url": f"https://sinta.kemdiktisaintek.go.id/authors/profile/{sid}",
                                      "is_external": "on", "nofollow": "", "custom_attributes": ""},
                                background_color=LIME, button_text_color=DARK, border_radius=sudut(99),
                                typography_typography="custom", typography_font_family="Barlow",
                                typography_font_weight="600", typography_font_size=be.ukuran_(14)))
    kiri = be.container([foto] + ([tile(kontak, NAVY)] if (baris or sid) else []), content_width="full", width=be.ukuran(28, "%"),
                        width_tablet=be.ukuran(34, "%"), width_mobile=be.ukuran(100, "%"),
                        flex_direction="column", flex_gap=be.gap(16))

    # ---- kolom kanan: nama + widget CV
    kanan_isi = [kicker(kel), judul(nama)]
    if gelar:
        kanan_isi.append(teks(f"<p>{esc(gelar)}</p>", "#414142", 18, "secondary"))
    kanan_isi.append(be.widget("html", html=data_html.replace('data-slug=""', f'data-slug="{slug}"')))
    kanan = be.container(kanan_isi, content_width="full", width=be.ukuran(72, "%"), width_tablet=be.ukuran(66, "%"),
                         width_mobile=be.ukuran(100, "%"), flex_direction="column", flex_gap=be.gap(16))

    baris_utama = be.container([kiri, kanan], content_width="full", flex_direction="row",
                               flex_direction_tablet="row", flex_direction_mobile="column",
                               flex_gap=be.gap(32), flex_align_items="flex-start")
    baris_utama["isInner"] = True
    remah = teks(f'<p style="font-size:14px;margin:0">Beranda &rsaquo; Dosen Tetap &rsaquo; {esc(nama)}</p>')
    return be.halaman_katur([remah, baris_utama])


def main():
    base = sys.argv[1] if len(sys.argv) > 1 else be.BASE
    be.BASE = base
    data_html = (ROOT / "widget" / "katur-profil-cv.html").read_text(encoding="utf-8").replace(be.PLACEHOLDER_BASE, base)
    with open(ROOT / "dosen.csv", newline="", encoding="utf-8") as f:
        dosen = list(csv.DictReader(f))
    with open(ROOT / "manual" / "dosen-info.csv", newline="", encoding="utf-8") as f:
        info = {x["slug"]: x for x in csv.DictReader(f)}
    OUT.mkdir(parents=True, exist_ok=True)
    for r in dosen:
        be._n[0] = 0
        doc = {"version": "0.4", "title": f"DTNTF – Profil {r['nama'].strip()}", "type": "container",
               "content": [profil(r, info.get(r["slug"], {}), base, data_html)], "page_settings": []}
        (OUT / f"{r['slug']}.json").write_text(json.dumps(doc, ensure_ascii=False), encoding="utf-8")
    zip_path = ROOT / "elementor" / "profil-38.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        for r in dosen:
            z.write(OUT / f"{r['slug']}.json", arcname=f"{r['slug']}.json")   # datar: JSON di akar ZIP
    print(f"Tertulis {len(dosen)} berkas di elementor/profil/ + {zip_path.name}  (data-base = {base})")


if __name__ == "__main__":
    main()
