#!/usr/bin/env python3
"""Lima halaman Laboratorium untuk tf (native, sederhana; isi dasar dari kartu daftar lab + pengurus.csv + tendik). Bagian tanpa data = placeholder agar diisi jurusan.
    python3 scripts/buat_native_lab.py -> elementor/native/lab-<kode>.json"""
import csv, json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import buat_elementor as be  # noqa: E402
import buat_profil_dosen as bp  # noqa: E402
import buat_native_orang as bo  # noqa: E402

ROOT = be.ROOT
U = "https://tf.ugm.ac.id/wp-content/uploads/sites/7/2026/11/"
GAYA_L = "font-style:italic;color:#7a5d00;background:#FFF6D6;border:1px dashed #D9B84A;border-radius:6px;padding:10px 14px;margin:0"
LAB = [
    dict(kode="eter", slug="lab-energi-terbarukan", nama="Lab Energi Terbarukan (ETER)", kepala="Kepala Laboratorium Energi Terbarukan", foto="Lab-ETR-1.jpg",
         teks="Merupakan wadah untuk melakukan praktikum dan eksperimen penelitian dasar maupun terapan seputar Energi Baru dan Terbarukan (Air, Surya, Bayu) berserta efisiensi dan konservasi energi untuk mewujudkan green and sustainable life.",
         teknisi=[("Budiyono", "Lab. Energi Terbarukan", "Budiyono-408x510-1.jpg")]),
    dict(kode="sstk", slug="lab-sensor-dan-sistem-telekontrol", nama="Lab Sensor dan Sistem Telekontrol (SSTK)", kepala="Kepala Laboratorium Sensor dan Sistem Telekontrol", foto="Lab-Sensor-1.jpg",
         teks="Merupakan wadah untuk melakukan praktikum, eksperimen penelitian dan technopreneurship seputar sensor dan perangkat kendali jarak jauh untuk aplikasi instrumentasi industri dan mitigasi kebencanaan.",
         teknisi=[("Winarno", "Lab. Sensor dan Sistem Telekontrol", "Winarno-408x510-1.jpg")]),
    dict(kode="ten", slug="lab-teknologi-energi-nuklir", nama="Lab Teknologi Energi Nuklir (TEN)", kepala="Kepala Laboratorium Teknologi Energi Nuklir", foto="Lab-TEN.jpg",
         teks="Merupakan wadah untuk melakukan praktikum dan eksperimen seputar deteksi dan pengukuran radiasi serta analisis kandungan unsur dalam suatu material menggunakan Analisis Aktivasi Neutron (AAN).",
         teknisi=[("Ardina Mei Devinta Suryana, S.S.T.", "Lab. Teknologi Energi Nuklir", "WhatsApp-Image-2026-10-08-at-15.36.52-394x510-1.jpg")]),
    dict(kode="tpkn", slug="lab-teknologi-proses-dan-kimia-nuklir", nama="Lab Teknologi Proses dan Kimia Nuklir (TPKN)", kepala="Kepala Laboratorium Teknologi Proses dan Kimia Nuklir", foto="Lab-TPKN.jpg",
         teks="Merupakan wadah untuk melakukan praktikum dan eksperimen penelitian seputar proses kimia secara umum dan kimia nuklir seperti pengelolaan limbah radioaktif dan penerapan zat radioaktif di berbagai bidang (termasuk radiotracer).",
         teknisi=[("Budiyono", "Lab. Teknologi Proses dan Kimia Nuklir", "Budiyono-408x510-1.jpg")]),
    dict(kode="kmf", slug="lab-komputasi-multifisika", nama="Lab Komputasi Multifisika (KMF)", kepala="Kepala Laboratorium Komputasi Multifisika", foto="Lab-KMF-1.jpeg",
         teks="Merupakan wadah untuk melakukan Praktikum Dasar Informatika (PDI), Praktikum Pemrograman Komputer (PPK) dan penelitian-penelitian lainnya yang berhubungan dengan simulasi sistem fisik, simulasi energi bangunan (IESEV) dan kecerdasan buatan.",
         teknisi=[("Roma Setiawan, S.Pd.", "Lab. Komputasi Multifisika", "Roma-Setiawan-S.Pd_-408x510-1.jpg")]),
]


def lorem(t):
    return bp.teks(f'<p style="{GAYA_L}">{t}</p>', "#7a5d00", 16, None)


def halaman(L):
    peng = {r["jabatan"]: r for r in csv.DictReader(open(ROOT / "manual" / "pengurus.csv", newline="", encoding="utf-8"))}
    foto = {r["slug"]: (r.get("foto_url") or "").strip() for r in csv.DictReader(open(ROOT / "dosen.csv", newline="", encoding="utf-8"))}
    k = peng[L["kepala"]]
    main, _, gel = k["nama_lengkap"].partition(", ")
    hero = be.container([be.widget("image", image={"url": U + L["foto"], "id": "", "alt": L["nama"]}, image_size="full", width=be.ukuran(100, "%"), height=be.ukuran(340, "px"),
                                   image_border_radius=bp.sudut(16), _title="Foto laboratorium", **{"object-fit": "cover"}),
                         ],
                        content_width="full", flex_direction="column", padding=bp.ruang(0), width=be.ukuran(46, "%"), width_tablet=be.ukuran(100, "%"), width_mobile=be.ukuran(100, "%"), _title="Foto")
    teks = be.container([bp.kicker("Laboratorium · Departemen Teknik Nuklir dan Teknik Fisika", bp.NAVY),
                         be.widget("heading", title=L["nama"], header_size="h2", title_color="#073C64", _title="Nama laboratorium"),
                         bp.teks(f"<p>{L['teks']}</p>", "#161616", 17, None),
                         be.widget("button", text="← Semua laboratorium", link={"url": "/laboratorium-v2/", "is_external": "", "nofollow": "", "custom_attributes": ""}, align="left",
                                   background_color="rgba(0,0,0,0)", button_text_color="#073C64", border_border="solid",
                                   border_width={"unit": "px", "top": "1", "right": "1", "bottom": "1", "left": "1", "isLinked": True}, border_color="#073C64", border_radius=bp.sudut(999),
                                   typography_typography="custom", typography_font_family="Barlow", typography_font_weight="600", typography_font_size=be.ukuran_(14))],
                        content_width="full", flex_direction="column", flex_gap=be.gap(14), padding=bp.ruang(0), flex_justify_content="center", width=be.ukuran(50, "%"),
                        width_tablet=be.ukuran(100, "%"), width_mobile=be.ukuran(100, "%"), _title="Tentang laboratorium")
    sec1 = be.container([hero, teks], content_width="full", flex_direction="row", flex_wrap="wrap", flex_gap=be.gap(32), flex_align_items="center", background_background="classic",
                        background_color="#FFFFFF", border_radius=bp.sudut(10), padding=bp.ruang(40), padding_mobile=bp.ruang(20), _title="Tentang")
    kep = bo.kartu(foto.get(k["slug"]) or "https://placehold.co/400x500/E8EEF4/073C64?text=Foto", main, "Kepala Laboratorium", main, gel, k["email"], "peng", 3, False, True)
    tek = [bo.kartu(U + f, n, "Teknisi / Laboran", n.split(", ")[0], n.partition(", ")[2], "", "peng", 3, False, True) for n, j, f in L["teknisi"]]
    sec2 = bo.bagian("Pengelola laboratorium", [kep] + tek, "#F5F5F5", True)
    sec3 = bo.bagian("Kegiatan dan fasilitas", [be.container([lorem("Daftar praktikum, penelitian, dan peralatan laboratorium akan ditambahkan oleh jurusan.")], content_width="full",
                                                          padding=bp.ruang(0), width=be.ukuran(100, "%"), _title="Placeholder")], "#FFFFFF", False)
    sec4 = bo.bagian("Kontak", [be.container([bp.teks(f'<p>Email: <a href="mailto:{k["email"]}">{k["email"]}</a></p>', "#161616", 17, None)], content_width="full", padding=bp.ruang(0),
                                             width=be.ukuran(100, "%"), _title="Email")], "#F5F5F5", False)
    return bo.halaman([sec1, sec2, sec3, sec4], L["nama"], "Laboratorium")


def main():
    for L in LAB:
        be._n[0] = 0
        s = json.dumps(halaman(L), ensure_ascii=False)
        assert "<style" not in s and '"widgetType": "html"' not in s
        (ROOT / "elementor" / "native" / f"lab-{L['kode']}.json").write_text(s, encoding="utf-8")
        print("ok", L["kode"], len(s))


if __name__ == "__main__":
    main()
