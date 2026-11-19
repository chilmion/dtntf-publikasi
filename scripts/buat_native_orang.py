#!/usr/bin/env python3
"""
Pengurus Departemen + Tenaga Kependidikan untuk tf.ugm.ac.id, desain v1 terbaru (kartu baris: foto 4:5 di kiri, label jabatan
biru tebal, nama navy tebal, gelar/email kecil; bagian ber-latar putih/abu), 100% widget native.
    python3 scripts/buat_native_orang.py -> elementor/native/pengurus.json, tendik.json
"""
import csv, json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import buat_elementor as be  # noqa: E402
import buat_profil_dosen as bp  # noqa: E402
import native_tipografi as nt  # noqa: E402

ROOT = be.ROOT
TF = "https://tf.ugm.ac.id/wp-content/uploads/sites/7/2026/11/"
TIER = {"koor": (150, 20, 14.5, 5), "tek": (124, 19, 14.5, 2), "staf": (104, 17, 14, 2), "peng": (110, 19, 13, 3), "pimp": (165, 24, 13, 2)}


def kartu(foto, alt, label, nama, gelar, email, tier, cols, navy=False, pas=False):
    w, nm, rl, lines = TIER[tier]
    if pas:   # pengurus: ukuran mengikuti v1 (teks kecil, nama tebal) agar muat dalam tinggi foto
        w, nm, rl = {2: (102, 19, 12.5), 3: (123, 18, 12.5), 4: (88, 16, 12)}[cols] if tier == "peng" else (164, 24, 13)
    h = round(w * 1.25)
    gambar = be.widget("image", image={"url": foto, "id": "", "alt": alt}, image_size="full", width=be.ukuran(100, "%"),
                       height=be.ukuran(h, "px"), image_border_radius=bp.sudut(12), _title="Foto " + nama,
                       _element_width="initial", _element_custom_width=be.ukuran(w, "px"), **{"object-fit": "cover", "object-position": "center 12%"})
    c_lab, c_nama, c_gel = ("#C8E86D", "#FFFFFF", "#D6E2EC") if navy else ("#003D79", "#073C64", "#636363")
    anak = [be.widget("text-editor", editor=f"<p>{label}</p>", text_color=c_lab, typography_typography="custom",
                      typography_font_family="Barlow", typography_font_weight="700", typography_font_size=be.ukuran_(rl),
                      typography_line_height={"unit": "em", "size": 1.4, "sizes": []}, _title="Jabatan"),
            be.widget("heading", title=nama, header_size="h3", title_color=c_nama, _title="Nama", **({"_nm": nm} if pas else {}))]
    if gelar:
        anak.append(bp.teks(f"<p>{gelar}</p>", c_gel, 13 if pas else 14, None))
    if email:
        atas = be.container(anak, content_width="full", flex_direction="column", flex_gap=be.gap(6), padding=bp.ruang(0), _title="Jabatan dan nama")
        mail = bp.teks(f'<p><a href="mailto:{email}" style="color:{c_gel}">{email}</a></p>', c_gel, 12 if pas else 13, None)
        anak = [atas, mail]
    kanan = be.container(anak, content_width="full", flex_direction="column", flex_gap=be.gap(6), padding=bp.ruang(0), flex_size="grow",
                         flex_justify_content="space-between", min_height=be.ukuran(h, "px"), min_height_mobile=be.ukuran(0, "px"), _title="Teks kartu")
    pct = {2: 48.5, 3: 31.5, 4: 23.5}[cols]
    return be.container([gambar, kanan], content_width="full", flex_direction="row", flex_align_items="stretch" if pas else "flex-start",
                        flex_gap=be.gap(18 if tier != "staf" else 14), width=be.ukuran(pct, "%"), width_tablet=be.ukuran(48.5, "%"),
                        width_mobile=be.ukuran(100, "%"), flex_direction_mobile="row", background_background="classic", background_color="#073C64" if navy else "#FFFFFF",
                        border_border="solid", border_width={"unit": "px", "top": "1", "right": "1", "bottom": "1", "left": "1", "isLinked": True},
                        border_color="#073C64" if navy else bp.GARIS, border_radius=bp.sudut(16), padding=bp.ruang(14), _title="Kartu: " + nama)


def bagian(judul, kartu_list, bg, tengah=False):
    grid = be.container(kartu_list, content_width="full", flex_direction="row", flex_wrap="wrap", flex_gap=be.gap(16),
                        flex_justify_content="center", flex_align_items="stretch", padding=bp.ruang(0), _title="Kartu " + judul)
    h2 = be.widget("heading", title=judul, header_size="h2", title_color="#161616", _title="Judul bagian", **({"align": "center"} if tengah else {}))
    return be.container([h2, grid], content_width="full", flex_direction="column", flex_gap=be.gap(24), background_background="classic",
                        background_color=bg, border_radius=bp.sudut(10), padding=bp.ruang(40), padding_mobile=bp.ruang(20), _title="Bagian " + judul)


def banner(judul, induk="Tentang Kami"):
    remah = bp.teks(f'<p><a href="/" style="color:#C8E86D">Beranda</a> / {induk} / {judul}</p>', "#FFFFFF", 14, None)
    h = be.widget("heading", title=judul, header_size="h1", title_color="#FFFFFF", typography_typography="custom",
                  typography_font_family="Plus Jakarta Sans", typography_font_weight="400", typography_font_size=be.ukuran_(48),
                  typography_font_size_mobile=be.ukuran_(32), typography_line_height={"unit": "em", "size": 1.15, "sizes": []},
                  typography_letter_spacing={"unit": "em", "size": -0.02, "sizes": []}, _title="Judul halaman")
    bar = be.container([], content_width="full", width=be.ukuran(64, "px"), height=be.ukuran(4, "px"), background_background="classic",
                       background_color="#C8E86D", padding=bp.ruang(0), _title="Garis lime")
    return be.container([remah, h, bar], content_width="full", flex_direction="column", flex_gap=be.gap(12), background_background="gradient",
                        background_color="#073C64", background_color_b="#1A2C43", background_gradient_angle={"unit": "deg", "size": 135, "sizes": []},
                        border_radius=bp.sudut(10), padding=bp.ruang(40), padding_mobile=bp.ruang(24), _title="Banner halaman")


def halaman(anak, judul):
    top = be.halaman_katur([banner(judul)] + anak)
    top["settings"]["_title"] = judul
    top["settings"]["flex_gap"] = be.gap(24)
    nt.terapkan(top)
    # banner memakai ukuran sendiri (setelah normalisasi)
    def pas(e):
        st = e.get("settings", {})
        if e.get("widgetType") == "heading" and "_nm" in st:
            n = st.pop("_nm")
            st.update(typography_font_weight="700", typography_font_size=be.ukuran_(n), typography_font_size_tablet=be.ukuran_(n),
                      typography_font_size_mobile=be.ukuran_(min(n, 18)), typography_line_height={"unit": "em", "size": 1.2, "sizes": []},
                      typography_letter_spacing={"unit": "em", "size": -0.01, "sizes": []})
        for a in e.get("elements", []):
            pas(a)
    pas(top)
    b = top["elements"][0]["elements"][1]["settings"]
    b.update(typography_font_size=be.ukuran_(48), typography_font_size_tablet=be.ukuran_(40), typography_font_size_mobile=be.ukuran_(32))
    return {"version": "0.4", "title": judul, "type": "container", "content": [top], "page_settings": []}


def pengurus():
    foto = {r["slug"]: (r.get("foto_url") or "").strip() for r in csv.DictReader(open(ROOT / "dosen.csv", newline="", encoding="utf-8"))}
    baris = list(csv.DictReader(open(ROOT / "manual" / "pengurus.csv", newline="", encoding="utf-8")))

    def pilih(f):
        return [r for r in baris if f(r["jabatan"])]
    urut = lambda rs, kunci: sorted(rs, key=lambda r: next((i for i, k in enumerate(kunci) if k in r["jabatan"]), 99))  # noqa: E731
    grup = [("Pimpinan Departemen", pilih(lambda j: j in ("Ketua Departemen", "Sekretaris Departemen")), 2, "pimp", True, "#FFFFFF"),
            ("Ketua Program Studi", urut(pilih(lambda j: j.startswith("Ketua Program Studi")), ["Nuklir", "Fisika", "Magister"]), 3, "peng", False, "#F5F5F5"),
            ("Sekretaris Program Studi", urut(pilih(lambda j: j.startswith("Sekretaris Program Studi")), ["Nuklir", "Fisika"]), 2, "peng", False, "#FFFFFF"),
            ("Kepala Laboratorium", urut(pilih(lambda j: j.startswith("Kepala Laboratorium")), ["Sensor", "Energi Terbarukan", "Komputasi", "Proses", "Teknologi Energi Nuklir"]), 3, "peng", False, "#F5F5F5"),
            ("Koordinator Kelompok Bidang Keahlian (KBK)", pilih(lambda j: j.startswith("Koordinator KBK")), 4, "peng", False, "#FFFFFF")]
    out = []
    for judul, rs, cols, tier, navy, bg in grup:
        ks = []
        for r in rs:
            nama = r["nama_lengkap"]
            main, _, gel = nama.partition(", ")
            ks.append(kartu(foto.get(r["slug"]) or "https://placehold.co/400x500/E8EEF4/073C64?text=Foto", nama, r["jabatan"], main, gel, r["email"], tier, cols, navy, True))
        out.append(bagian(judul, ks, bg, True))
    return halaman(out, "Pengurus Departemen")


def tendik():
    koor = [("Sukiyat", "Koordinator Urusan Akademik, Kemahasiswaan dan Alumni", "Sukiyat-408x510-1.jpg"),
            ("Andi Sudarmanto, S.Sos.", "Koordinator Urusan Administrasi Umum, SDM, Penelitian dan Pengabdian pada Masyarakat, dan Kerjasama", "Andi-Sudarmanto-S.Sos_-408x510-1.jpg"),
            ("Johan Purwanto, S.Sos.", "Koordinator Urusan Aset, Sarana Prasarana, SHE, dan IT", "Johan-Purwanto-S.Sos_-408x510-1.jpg")]
    tek = [("Ardina Mei Devinta Suryana, S.S.T.", "Lab. Teknologi Energi Nuklir", "WhatsApp-Image-2026-10-08-at-15.36.52-394x510-1.jpg"),
           ("Winarno", "Lab. Sensor dan Sistem Telekontrol", "Winarno-408x510-1.jpg"),
           ("Budiyono", "Lab. Energi Terbarukan<br>Lab. Teknologi Proses dan Kimia Nuklir", "Budiyono-408x510-1.jpg"),
           ("Roma Setiawan, S.Pd.", "Lab. Komputasi Multifisika", "Roma-Setiawan-S.Pd_-408x510-1.jpg")]
    staf = [("Sukini, S.Kom.", "Pengelola Layanan Akademik", "Perempuan-DTNTF-408x510-1.jpg"), ("Triyanto", "Pengelola Layanan Akademik", "Triyanto-408x510-1.jpg"),
            ("Riny Wasita, A.Md.", "Pengelola Layanan Akademik", "1-408x510-1.jpg"), ("Safrudin", "Pengelola Keuangan", "Safrudin-408x510-1.jpg"),
            ("Parjiyo", "Pengelola Sarana dan Prasarana", "Parjiyo-408x510-1.jpg"), ("Widarto", "Pengelola Kepegawaian", "Widarto.jpg"),
            ("Arbiyhuno Lalintyo", "Pengelola Administrasi Umum", "Arbiyhuno-Lalintyo.jpg"), ("Slamet Haryadi", "Pengelola Penelitian", "Slamet-Haryadi.jpg"),
            ("Sabar", "Pramu Bakti", "Sabar-408x510-1.jpg")]   # revisi 19 Nov: Sabar terakhir

    def ks(lst, tier, cols):
        r = []
        for n, j, f in lst:
            main, _, gel = n.partition(", ")
            r.append(kartu(TF + f, n, j, main, gel, "", tier, cols))
        return r
    return halaman([bagian("Koordinator", ks(koor, "koor", 3), "#FFFFFF"), bagian("Teknisi dan Laboran", ks(tek, "tek", 2), "#F5F5F5"),
                    bagian("Staf", ks(staf, "staf", 3), "#FFFFFF")], "Tenaga Kependidikan")



def dosen():
    """Dosen Tetap (v1): satu grid tanpa judul bagian; kartu = foto, kelompok, nama, gelar, bidang (tumbuh), tombol di dasar kartu (sejajar)."""
    rows = sorted(csv.DictReader(open(ROOT / "dosen.csv", newline="", encoding="utf-8")), key=lambda r: r["nama"].strip().lower())
    info = {x["slug"]: x for x in csv.DictReader(open(ROOT / "manual" / "dosen-info.csv", newline="", encoding="utf-8"))}
    ks = []
    for r in rows:
        i = info.get(r["slug"].strip())
        kel = bp.kelompok_info(i) or "Teknik Fisika"
        nama, gelar = r["nama"].strip(), (r.get("gelar") or "").strip()
        foto = be.widget("image", image={"url": (r.get("foto_url") or "").strip() or "https://placehold.co/400x500/E8EEF4/073C64?text=Foto", "id": "", "alt": nama},
                         image_size="full", width=be.ukuran(100, "%"), height=be.ukuran(330, "px"), height_mobile=be.ukuran(300, "px"),
                         image_border_radius=bp.sudut(10), _title="Foto " + nama, **{"object-fit": "cover", "object-position": "top center"})
        teks = [bp.kicker(kel.upper(), bp.NAVY), be.widget("heading", title=nama, header_size="h3", title_color="#161616", _title="Nama")]
        if gelar:
            teks.append(bp.teks(f"<p>{bp.esc(gelar)}</p>", "#7a7a7a", 14, None))
        if (i or {}).get("bidang_ilmu"):
            teks.append(bp.teks(f"<p>{bp.esc(i['bidang_ilmu'])}</p>", "#003D79", 14, None))
        blok = be.container(teks, content_width="full", flex_direction="column", flex_gap=be.gap(8), padding=bp.ruang(0), flex_size="grow", _title="Teks kartu")
        tombol = be.widget("button", text="Profil lengkap", link={"url": f"/{r['slug'].strip()}/", "is_external": "", "nofollow": "", "custom_attributes": ""},
                           align="left", background_color="rgba(0,0,0,0)", button_text_color="#073C64", border_border="solid",
                           border_width={"unit": "px", "top": "1", "right": "1", "bottom": "1", "left": "1", "isLinked": True},
                           border_color="#073C64", border_radius=bp.sudut(999), typography_typography="custom", typography_font_family="Barlow",
                           typography_font_weight="600", typography_font_size=be.ukuran_(14),
                           text_padding={"unit": "px", "top": "9", "right": "18", "bottom": "9", "left": "18", "isLinked": False})
        ks.append(be.container([foto, blok, tombol], content_width="full", flex_direction="column", flex_gap=be.gap(10), background_background="classic",
                               background_color="#FFFFFF", border_border="solid",
                               border_width={"unit": "px", "top": "1", "right": "1", "bottom": "1", "left": "1", "isLinked": True},
                               border_color=bp.GARIS, border_radius=bp.sudut(16), padding=bp.ruang(14), width=be.ukuran(23.5, "%"),
                               width_tablet=be.ukuran(48.5, "%"), width_mobile=be.ukuran(100, "%"), _title="Kartu " + nama))
    grid = be.container(ks, content_width="full", flex_direction="row", flex_wrap="wrap", flex_gap=be.gap(16), flex_align_items="stretch",
                        flex_justify_content="flex-start", padding=bp.ruang(0), _title="Daftar dosen")
    return halaman([grid], "Dosen Tetap")


if __name__ == "__main__":
    for nama, d in (("pengurus", pengurus()), ("tendik", tendik()), ("dosen-tetap", dosen())):
        s = json.dumps(d, ensure_ascii=False)
        assert "<style" not in s and '"widgetType": "html"' not in s
        (ROOT / "elementor" / "native" / f"{nama}.json").write_text(s, encoding="utf-8")
        print("ok", nama, len(s))
