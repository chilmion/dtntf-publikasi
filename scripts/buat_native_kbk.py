#!/usr/bin/env python3
"""
Halaman KBK untuk tf.ugm.ac.id, 100% widget native Elementor (tanpa HTML/style/svg/script), dirender STATIS dari data/kbk/kbk.json.
URL gambar tf dibaca dari data/kbk/urls-tf.json (path 'kbk/x.jpg' -> URL media tf; diisi setelah unggah).
    python3 scripts/buat_native_kbk.py  ->  elementor/native/kbk-<kode>.json  (+ daftar gambar: --gambar)
"""
import json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import buat_elementor as be  # noqa: E402
import buat_profil_dosen as bp  # noqa: E402

ROOT = be.ROOT
U = ROOT / "data" / "kbk" / "urls-tf.json"
URLS = json.loads(U.read_text()) if U.exists() else {}
LOREM = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
LOREM_S = "Lorem ipsum dolor sit amet"
GAYA_L = "font-style:italic;color:#7a5d00;background:#FFF6D6;border:1px dashed #D9B84A;border-radius:6px;padding:10px 14px;margin:0"
esc = bp.esc


def img(path):
    return URLS.get(path, f"https://raw.githubusercontent.com/chilmion/dtntf-publikasi/main/data/{path}")


def gambar(path, alt, lebar=100, tinggi=None, judul=None, **kw):
    s = dict(image={"url": img(path), "id": "", "alt": alt}, image_size="full", width=be.ukuran(100, "%"),
             image_border_radius=bp.sudut(10), _title=judul or ("Gambar: " + alt[:40]))
    if tinggi:
        s.update(height=be.ukuran(tinggi, "px"), height_mobile=be.ukuran(min(tinggi, 240), "px"))
        s["object-fit"] = "cover"
    if lebar < 100:
        s.update(_element_width="initial", _element_custom_width=be.ukuran(lebar, "%"), _element_custom_width_mobile=be.ukuran(100, "%"))
    s.update(kw)
    return be.widget("image", **s)


def lorem(pendek=False):
    return bp.teks(f'<p style="{GAYA_L}">{LOREM_S if pendek else LOREM}</p>', "#7a5d00", 16, None)


def h(tek, ukur, warna="#161616", tag="h3", bobot="400", spasi=-1.3, font="Plus Jakarta Sans"):
    w = be.widget("heading", title=tek, header_size=tag, title_color=warna, typography_typography="custom",
                  typography_font_family=font, typography_font_weight=bobot, typography_font_size=be.ukuran_(ukur),
                  typography_font_size_mobile=be.ukuran_(min(ukur, max(18, ukur * 0.6))),
                  typography_line_height={"unit": "em", "size": 1.2, "sizes": []},
                  typography_letter_spacing={"unit": "px", "size": spasi, "sizes": []})
    return w


def kol(anak, lebar=None, judul=None, **kw):
    s = dict(content_width="full", flex_direction="column", flex_gap=be.gap(10), padding=bp.ruang(0), _title=judul or "Kolom")
    if lebar:
        s.update(width=be.ukuran(lebar, "%"), width_mobile=be.ukuran(100, "%"))
    s.update(kw)
    return be.container(anak, **s)


def baris(anak, judul="Baris", gap=16, **kw):
    s = dict(content_width="full", flex_direction="row", flex_wrap="wrap", flex_gap=be.gap(gap), flex_direction_mobile="column", padding=bp.ruang(0), _title=judul)
    s.update(kw)
    return be.container(anak, **s)


def tombol(teks, url, bg="#073C64", fg="#FFFFFF"):
    return be.widget("button", text=teks, link={"url": url, "is_external": "", "nofollow": "", "custom_attributes": ""}, align="left",
                     background_color=bg, button_text_color=fg, border_radius=bp.sudut(999), typography_typography="custom",
                     typography_font_family="Barlow", typography_font_weight="600", typography_font_size=be.ukuran_(14),
                     text_padding={"unit": "px", "top": "10", "right": "18", "bottom": "10", "left": "18", "isLinked": False})


def tile_angka(kelas, angka, label):
    bg = {"lime": bp.LIME, "putih": "#FFFFFF", "abu": bp.ABU, "navy": bp.NAVY}[kelas]
    ink = "#FFFFFF" if kelas == "navy" else bp.DARK
    a = h(f"{angka:,}".replace(",", ".") if angka else "–", 56, ink, "div", "400", -3.4)
    t = bp.tile([bp.kicker(label, "#FFFFFF" if kelas == "navy" else bp.NAVY), a], bg, 23.5, garis=(kelas == "putih"))
    t["settings"]["width_tablet"] = be.ukuran(48.5, "%")
    t["settings"]["_title"] = "Statistik: " + label
    return t


def seksi(judul, isi, nama=None):
    return kol([h(judul, 40, tag="h2", spasi=-1.7)] + isi, judul=nama or ("Bagian: " + judul), flex_gap=be.gap(20))


def link_orang(o):
    return f'<a href="{esc(o["url"])}">{esc(o["nama"])}</a>' if o.get("url") else esc(o["nama"])


def hero(k):
    ketua = k.get("ketua")
    kt = f"Ketua / koordinator: <a href=\"{esc(ketua['url'])}\" style=\"color:#C8E86D\">{esc(ketua['nama'])}{', ' + esc(ketua['gelar']) if ketua.get('gelar') else ''}</a>" if ketua else "Ketua / koordinator: " + LOREM_S
    t = h(k["nama"], 56, "#FFFFFF", "h1", "400", -3.4)
    teks = kol([bp.kicker("Kelompok Bidang Keahlian · Departemen Teknik Nuklir dan Teknik Fisika", bp.LIME), t,
                bp.teks(f"<p>{kt}</p>", "#FFFFFF", 16, None), bp.kicker("Sekilas", bp.LIME),
                bp.teks(f"<p>{esc(k['sekilas'])}</p>" if k.get("sekilas") else f"<p>{LOREM}</p>", "rgba(255,255,255,.9)", 18, None)],
               lebar=55, judul="Teks hero", flex_gap=be.gap(14), justify_content="center")
    anak = [teks]
    if k.get("gambar"):
        anak.append(kol([gambar(k["gambar"], k["nama"], 100, 420, "Gambar hero")], lebar=45, judul="Gambar hero"))
    return be.container(anak, content_width="full", flex_direction="row", flex_direction_mobile="column", flex_gap=be.gap(36),
                        flex_align_items="center", background_background="classic", background_color=bp.NAVY, border_radius=bp.sudut(10),
                        padding=bp.ruang(40), padding_mobile=bp.ruang(24), _title="Hero")


def galeri(g):
    g = g[:8]
    cap = lambda x: x.get("judul") or "Dokumentasi riset"  # noqa: E731
    besar = gambar(g[0]["gambar"], cap(g[0]), 100, 440, "Foto besar")
    kecil = [gambar(x["gambar"], cap(x), 48.5, 214) for x in g[1:5]]
    kanan = baris(kecil, "Foto kecil", 12)
    atas = baris([kol([besar], 49, "Foto besar"), kol([kanan], 49, "Foto kecil", flex_gap=be.gap(12))], "Galeri atas", 16)
    anak = [atas]
    sisa = g[5:]
    if sisa:
        w = 100 / len(sisa) - 2.5
        anak.append(baris([gambar(x["gambar"], cap(x), w, 220) for x in sisa], "Galeri bawah", 16))
    return seksi("Galeri riset", anak)


def kompetensi(k):
    bdg = k.get("bidang") or []
    tiles = []
    for c in k.get("kompetensi") or []:
        isi = [h(f"{c['no']:02d}", 40, bp.NAVY, "div", "400", -2), h(c["judul"], 24, tag="h3"),
               bp.teks(f"<p>{esc(c['deskripsi'])}</p>" if c.get("deskripsi") else f"<p style=\"{GAYA_L}\">{LOREM}</p>", "#636363", 16, None)]
        daftar = [b for b in bdg if b.get("subkbk") == c["judul"]]
        if daftar:
            li = "".join(f"<li><strong>{esc(b['bidang'])}</strong>{' <em>(' + esc(b['en']) + ')</em>' if b.get('en') else ''}<br>"
                         f"{', '.join(link_orang(d) for d in b.get('dosen', []))}</li>" for b in daftar)
            isi.append(bp.teks(f"<ul>{li}</ul>", "#636363", 15, None))
        t = bp.tile(isi, "#FFFFFF", 32, garis=True)
        t["settings"]["_title"] = f"Kompetensi {c['no']}: {c['judul']}"
        t["settings"]["width_tablet"] = be.ukuran(48.5, "%")
        tiles.append(t)
    if not tiles:
        tiles = [bp.tile([h(f"{n:02d}", 40, bp.NAVY, "div"), lorem(True), lorem()], "#FFFFFF", 32, garis=True) for n in (1, 2, 3)]
    return seksi("Kompetensi & keahlian", [baris(tiles, "Kartu kompetensi")])


def anggota(k):
    kt = (k.get("ketua") or {}).get("slug")
    cards = []
    for a in k.get("anggota") or []:
        peran = a.get("peran") or ("Ketua" if a.get("slug") == kt else "")
        isi = []
        if a.get("foto_url"):
            isi.append(be.widget("image", image={"url": a["foto_url"], "id": "", "alt": a["nama"]}, image_size="full", width=be.ukuran(100, "%"),
                                 height=be.ukuran(280, "px"), image_border_radius=bp.sudut(10), _title="Foto " + a["nama"], **{"object-fit": "cover"}))
        if peran:
            isi.append(bp.kicker(peran, bp.NAVY))
        isi += [h(a["nama"], 20, tag="h4", spasi=-.6), ]
        if a.get("gelar"):
            isi.append(bp.teks(f"<p>{esc(a['gelar'])}</p>", "#636363", 14, None))
        isi.append(bp.teks(f"<p>{esc(a['keahlian'])}</p>" if a.get("keahlian") else f"<p style=\"{GAYA_L}\">{LOREM_S}</p>", "#636363", 15, None))
        isi.append(tombol("Selengkapnya →", a["url"]))
        c = bp.tile(isi, "#FFFFFF", 23.5, garis=True)
        c["settings"]["_title"] = "Anggota: " + a["nama"]
        c["settings"]["width_tablet"] = be.ukuran(48.5, "%")
        cards.append(c)
    if not cards:
        cards = [bp.tile([lorem(True), lorem(True)], "#FFFFFF", 23.5, garis=True) for _ in range(3)]
    return seksi("Anggota", [baris(cards, "Kartu anggota")])


def peta(k):
    pj = k.get("peta_jalan") or {}
    if not pj.get("gambar"):
        return None
    anak = [gambar(pj["gambar"], pj.get("alt") or pj.get("judul") or "Peta jalan penelitian", 100, None, "Peta jalan")]
    lain = pj.get("lainnya") or []
    if lain:
        anak.append(baris([kol([gambar(x["gambar"], x["judul"], 100), bp.teks(f"<p>{esc(x['judul'])}</p>", "#636363", 14, None)], 31.5, x["judul"]) for x in lain],
                          "Peta jalan lainnya"))
    return seksi("Peta jalan penelitian", anak)


def tema(t, i):
    paras = t.get("deskripsi_lengkap") or ([t["deskripsi"]] if t.get("deskripsi") else [])
    pub = t.get("publikasi") or []
    jum = t.get("jumlah_publikasi") or len(pub)
    kepala = [h(f"{t['no']:02d}  {t['judul']}" if t.get("judul") else f"{i:02d}  {LOREM_S}", 28, tag="h3", spasi=-1.3)]
    if jum:
        kepala.append(bp.kicker(f"{jum} publikasi", bp.NAVY))
    kiri = list(kepala)
    tim = t.get("tim") or []
    if tim:
        kiri.append(bp.teks("<p><strong>Tim:</strong> " + ", ".join(link_orang(d) for d in tim) + "</p>", "#636363", 15, None))
    kiri.append(bp.teks(f"<p>{esc(paras[0])}</p>" if paras else f"<p style=\"{GAYA_L}\">{LOREM}</p>", "#636363", 17, None))
    atas = [kol(kiri, 62 if t.get("gambar") else 100, "Ringkasan tema")]
    if t.get("gambar"):
        atas.append(kol([gambar(t["gambar"], t.get("judul") or "Dokumentasi penelitian", 100, 300)], 38, "Foto tema"))
    isi = [baris(atas, "Atas tema", 24, flex_wrap="nowrap")]
    detail = [bp.teks(f"<p>{esc(p)}</p>", "#636363", 16, None) for p in paras[1:]]
    dana = t.get("pendanaan") or []
    ld = ([f"<li><strong>{esc(d['judul'])}</strong><br>{esc(d['periode'])} · {esc(d['sumber'])}</li>" for d in dana]
          or [f"<li>{esc(x)}</li>" for x in (t.get("riset") or [])])
    def daftar(judul, li):
        detail.append(bp.kicker(judul, bp.NAVY))
        detail.append(bp.teks("<ul>" + "".join(li) + "</ul>" if li else f"<p style=\"{GAYA_L}\">{LOREM_S}</p>", "#636363", 15, None))
    daftar("Pendanaan", ld)
    pat = t.get("paten") or []
    if pat:
        daftar("Paten", [f"<li><strong>{esc(x['judul'])}</strong><br>{esc(x.get('jenis', ''))} {esc(x.get('nomor', ''))}{' · ' + esc(x['tahun']) if x.get('tahun') else ''}</li>" for x in pat])
    def lp(p):
        doi = f' <a href="https://doi.org/{esc(p["doi"])}" target="_blank" rel="noopener">DOI ↗</a>' if p.get("doi") and p["doi"].startswith("10.") else ""
        return f"<li>{esc(p['sitasi'])}{doi}</li>"
    daftar("Publikasi terpilih", [lp(p) for p in pub])
    iid = be.eid()[:7]
    w = be.widget("nested-accordion", items=[{"item_title": "Baca selengkapnya", "_id": iid, "element_css_id": ""}], title_tag="h4",
                  default_state="all_collapsed", max_items_expended="one",
                  accordion_item_title_icon={"value": "fas fa-plus", "library": "fa-solid"},
                  accordion_item_title_icon_active={"value": "fas fa-minus", "library": "fa-solid"}, accordion_item_title_icon_position="end",
                  title_typography_typography="custom", title_typography_font_family="Barlow", title_typography_font_weight="600",
                  title_typography_font_size=be.ukuran_(16), normal_title_color=bp.NAVY, hover_title_color=bp.NAVY, active_title_color=bp.NAVY,
                  _title="Baca selengkapnya")
    w["elements"] = [kol(detail, judul="Rincian tema", padding=bp.ruang(12))]
    isi.append(w)
    c = bp.tile(isi, "#FFFFFF", None, garis=True)
    c["settings"]["_title"] = f"Tema {t.get('no', i)}: {t.get('judul', 'contoh')}"
    c["settings"]["flex_gap"] = be.gap(16)
    c["settings"]["padding"] = bp.ruang(28)
    return c


def halaman(k):
    st = k.get("statistik") or {}
    anak = [bp.teks(f'<p><a href="/">Beranda</a> › <a href="/kbk/">KBK</a> › {esc(k["nama"])}</p>', "#636363", 14, None), hero(k),
            baris([tile_angka("lime", st.get("dosen"), "Dosen anggota"), tile_angka("putih", st.get("kompetensi"), "Bidang kompetensi"),
                   tile_angka("abu", st.get("tema"), "Tema penelitian"), tile_angka("navy", st.get("publikasi"), "Publikasi terpilih")], "Statistik")]
    if len(k.get("galeri") or []) >= 3:
        anak.append(galeri(k["galeri"]))
    anak.append(kompetensi(k))
    if k["kode"] != "instrumentasi":   # revisi 19 Nov: section Anggota KBK Instrumentasi dihapus
        anak.append(anggota(k))
    p = peta(k)
    if p:
        anak.append(p)
    tm = [tema(t, i) for i, t in enumerate(k.get("tema") or [], 1)] or [tema({"no": 1}, 1), tema({"no": 2}, 2)]
    anak.append(seksi("Tema penelitian", tm))
    top = be.halaman_katur(anak)
    top["settings"]["_title"] = "KBK " + k["nama"]
    top["settings"]["flex_gap"] = be.gap(48)
    return top


def main():
    d = json.loads((ROOT / "data" / "kbk" / "kbk.json").read_text())
    if "--gambar" in sys.argv:
        s = set()
        for k in d["kbk"]:
            s.add(k["gambar"]); s.update(g["gambar"] for g in k["galeri"]); s.add(k["peta_jalan"]["gambar"])
            s.update(x["gambar"] for x in k["peta_jalan"].get("lainnya", [])); s.update(t["gambar"] for t in k["tema"] if t.get("gambar"))
        print("\n".join(sorted(x for x in s if x))); return
    for k in d["kbk"]:
        be._n[0] = 0
        s = json.dumps({"version": "0.4", "title": "KBK " + k["nama"], "type": "container", "content": [halaman(k)], "page_settings": []}, ensure_ascii=False)
        assert "<style" not in s and "<svg" not in s and "<script" not in s and '"widgetType": "html"' not in s
        (ROOT / "elementor" / "native" / f"kbk-{k['kode']}.json").write_text(s, encoding="utf-8")
        print("ok", k["kode"], len(s))


if __name__ == "__main__":
    main()
