#!/usr/bin/env python3
"""Mitra untuk tf (native, desain v1): dua halaman bertemplat sama (Mitra Penelitian, Mitra Pengabdian). Logo = gambar berwarna (revisi 19 Nov).
Bagian: Mitra kerja sama (grid logo), Sorotan kerja sama (bento), Kabar kerja sama. Data: data/mitra/mitra.json, artikel.json.
Gambar tf: data/mitra/urls-tf.json (nama berkas -> URL media tf; diisi setelah unggah)."""
import json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import buat_elementor as be  # noqa: E402
import buat_profil_dosen as bp  # noqa: E402
import buat_native_orang as bo  # noqa: E402

ROOT = be.ROOT
B = "https://tf.ugm.ac.id/wp-content/uploads/sites/7/2026/11/"
D = json.loads((ROOT / "data" / "mitra" / "mitra.json").read_text(encoding="utf-8"))
A = json.loads((ROOT / "data" / "mitra" / "artikel.json").read_text(encoding="utf-8"))["artikel"]
BORDER = {"unit": "px", "top": "1", "right": "1", "bottom": "1", "left": "1", "isLinked": True}
BULAN = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]


def url(p):
    nama = p.split("/")[-1]
    return B + "dtntf-mitra-" + nama.rsplit(".", 1)[0] + "." + nama.rsplit(".", 1)[1]


def tgl(s):
    y, m, d = s.split("-")
    return f"{int(d)} {BULAN[int(m) - 1]} {y}"


def logo(l):
    if l.get("gambar"):
        isi = be.widget("image", image={"url": url(l["gambar"]), "id": "", "alt": l["nama"]}, image_size="full", width=be.ukuran(100, "%"), height=be.ukuran(72, "px"),
                        _title="Logo " + l["nama"], **{"object-fit": "contain"})
    else:
        isi = be.widget("heading", title=l["nama"], header_size="div", title_color="#073C64", typography_typography="custom", typography_font_family="Plus Jakarta Sans",
                        typography_font_weight="600", typography_font_size=be.ukuran_(15), align="center", _title="Nama " + l["nama"])
    return be.container([isi], content_width="full", flex_justify_content="center", flex_align_items="center", min_height=be.ukuran(110, "px"), background_background="classic",
                        background_color="#FFFFFF", border_border="solid", border_width=BORDER, border_color=bp.GARIS, border_radius=bp.sudut(14), padding=bp.ruang(16),
                        width=be.ukuran(18.4, "%"), width_tablet=be.ukuran(31.5, "%"), width_mobile=be.ukuran(48, "%"), _title="Mitra " + l["nama"])


def sorot(s, w):
    foto = bool(s.get("gambar"))
    warna = s.get("warna")
    bg = {"navy": "#073C64", "lime": "#C8E86D", "putih": "#FFFFFF"}.get(warna, "#073C64")
    gelap = foto or warna == "navy"
    ink = "#FFFFFF" if gelap else "#1A2C43"
    judul = be.widget("heading", title=s["judul"], header_size="h3", title_color=ink, typography_typography="custom", typography_font_family="Plus Jakarta Sans",
                      typography_font_weight="600", typography_font_size=be.ukuran_(26 if s.get("ukuran") == "besar" else 22), _title="Judul",
                      **({"link": {"url": s["url"], "is_external": "on", "nofollow": "", "custom_attributes": ""}} if s.get("url") else {}))
    teks = bp.teks(f"<p>{s['ket']}</p>", ink, 15, None)
    teks["settings"]["text_color"] = ink
    anak = [judul, teks]
    if s.get("logo"):
        anak.insert(0, be.widget("image", image={"url": url(s["logo"]), "id": "", "alt": s["judul"]}, image_size="full", width=be.ukuran(100, "%"), height=be.ukuran(48, "px"),
                                 _title="Logo", **{"object-fit": "contain", "object-position": "left center"}))
    set_ = dict(content_width="full", flex_direction="column", flex_justify_content="flex-end", flex_gap=be.gap(8), padding=bp.ruang(24), border_radius=bp.sudut(20),
                min_height=be.ukuran(300 if s.get("ukuran") == "besar" else 240, "px"), width=be.ukuran(w, "%"), width_tablet=be.ukuran(100, "%"), width_mobile=be.ukuran(100, "%"),
                overflow="hidden", _title="Sorotan " + s["judul"])
    if foto:
        set_.update(background_background="classic", background_image={"url": url(s["gambar"]), "id": "", "size": "", "source": "library"}, background_position="center center",
                    background_size="cover", background_overlay_background="gradient", background_overlay_color="rgba(7,60,100,0.12)", background_overlay_color_b="rgba(7,60,100,0.94)",
                    background_overlay_gradient_angle={"unit": "deg", "size": 180, "sizes": []}, background_overlay_color_stop={"unit": "%", "size": 10, "sizes": []})
    else:
        set_.update(background_background="classic", background_color=bg, **({"border_border": "solid", "border_width": BORDER, "border_color": bp.GARIS} if warna == "putih" else {}))
    return be.container(anak, **set_)


def kabar(x):
    return be.container([be.widget("image", image={"url": url(x["gambar"]), "id": "", "alt": x["judul"]}, image_size="full", width=be.ukuran(100, "%"), height=be.ukuran(190, "px"),
                                   image_border_radius=bp.sudut(12), _title="Foto", **{"object-fit": "cover"}),
                         bp.teks(f"<p>{tgl(x['tanggal'])}</p>", "#636363", 14, None),
                         be.widget("heading", title=x["judul"], header_size="h3", title_color="#161616", _title="Judul"),
                         be.widget("button", text="Baca selengkapnya", link={"url": x["url"], "is_external": "on", "nofollow": "", "custom_attributes": ""}, align="left",
                                   background_color="rgba(0,0,0,0)", button_text_color="#073C64", border_border="solid", border_width=BORDER, border_color="#073C64",
                                   border_radius=bp.sudut(999), typography_typography="custom", typography_font_family="Barlow", typography_font_weight="600",
                                   typography_font_size=be.ukuran_(14), text_padding={"unit": "px", "top": "9", "right": "18", "bottom": "9", "left": "18", "isLinked": False})],
                        content_width="full", flex_direction="column", flex_gap=be.gap(10), flex_justify_content="space-between", background_background="classic", background_color="#FFFFFF",
                        border_border="solid", border_width=BORDER, border_color=bp.GARIS, border_radius=bp.sudut(16), padding=bp.ruang(14), width=be.ukuran(31.5, "%"),
                        width_tablet=be.ukuran(48.5, "%"), width_mobile=be.ukuran(100, "%"), _title="Kabar " + x["judul"][:40])


def baris(ks, justify="flex-start", judul="Baris"):
    return be.container(ks, content_width="full", flex_direction="row", flex_wrap="wrap", flex_gap=be.gap(20), flex_align_items="stretch", flex_justify_content=justify,
                        padding=bp.ruang(0), _title=judul)


def blok(judul, sub, isi, bg):
    return be.container([be.widget("heading", title=judul, header_size="h2", title_color="#161616", _title="Judul bagian"), bp.teks(f"<p>{sub}</p>", "#636363", 17, None)] + isi,
                        content_width="full", flex_direction="column", flex_gap=be.gap(16), background_background="classic", background_color=bg, border_radius=bp.sudut(10),
                        padding=bp.ruang(40), padding_mobile=bp.ruang(20), _title="Bagian " + judul)


def halaman(judul, induk):
    so = D["sorotan"]
    pola = [(so[0], 62), (so[1], 36), (so[2], 31.4), (so[3], 31.4), (so[4], 31.4), (so[5], 31.4), (so[6], 31.4), (so[7], 31.4)]
    sorot_rows = [baris([sorot(s, w) for s, w in pola[:2]], judul="Sorotan 1"), baris([sorot(s, w) for s, w in pola[2:5]], judul="Sorotan 2"),
                  baris([sorot(s, w) for s, w in pola[5:]], judul="Sorotan 3")]
    n = len(A)
    kabar_rows = [baris([kabar(x) for x in A[i:i + 3]], "center", "Kabar") for i in range(0, n, 3)]
    anak = [blok("Mitra kerja sama", "Industri, lembaga pemerintah, dan perguruan tinggi yang bekerja sama dengan DTNTF dalam pendidikan, penelitian, dan pengabdian.",
                 [baris([logo(l) for l in D["logo"]], "center", "Logo mitra")], "#FFFFFF"),
            blok("Sorotan kerja sama", "Kerja sama yang sedang berjalan dan hasil yang sudah terlihat.", sorot_rows, "#F5F5F5"),
            blok("Kabar kerja sama", "Kegiatan terbaru bersama mitra.", kabar_rows, "#FFFFFF")]
    return bo.halaman(anak, judul, induk)


def gambar():
    s = set()
    for l in D["logo"]:
        if l.get("gambar"): s.add(l["gambar"])
    for x in D["sorotan"]:
        for k in ("gambar", "logo"):
            if x.get(k): s.add(x[k])
    for x in A: s.add(x["gambar"])
    return sorted(s)


def main():
    if "--gambar" in sys.argv:
        print("\n".join(gambar())); return
    for nama, judul, induk in (("mitra-penelitian", "Mitra Penelitian", "Penelitian"), ("mitra-pengabdian", "Mitra Pengabdian", "Pengabdian")):
        s = json.dumps(halaman(judul, induk), ensure_ascii=False)
        assert "<style" not in s and '"widgetType": "html"' not in s
        (ROOT / "elementor" / "native" / f"{nama}.json").write_text(s, encoding="utf-8")
        print("ok", nama, len(s))


if __name__ == "__main__":
    main()
