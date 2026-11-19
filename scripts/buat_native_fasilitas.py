#!/usr/bin/env python3
"""Fasilitas Umum untuk tf (desain v1 native): kartu bento = container berlatar foto + overlay + judul/teks native.
Revisi 19 Nov: Kamar Mandi -> Aksesibilitas Difabel; Katalog Ruang -> Ruang kelas & auditorium fakultas teknik; Rumah Kayu -> Konseling Psikolog; urutan baru."""
import json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import buat_elementor as be  # noqa: E402
import buat_profil_dosen as bp  # noqa: E402
import buat_native_orang as bo  # noqa: E402

ROOT = be.ROOT
B = "https://tf.ugm.ac.id/wp-content/uploads/sites/7/2026/11/"
FTU = "https://ft.ugm.ac.id/"
A = [("Perpustakaan / Ruang Referensi", "Perpustakaan yang lengkap, representatif, dan nyaman untuk mendukung penelaahan literatur dan penelitian.", "Perpustakaan-20220105_083727-1-scaled-1.jpg", "", 62, 340),
     ("Co-working Space", "Ruang bersama yang nyaman untuk bekerja, belajar, dan berdiskusi bagi tamu, mahasiswa, dan dosen.", "DSC_5917-scaled-1.jpg", "", 36, 340),
     ("Pelayanan Akademik", "Pelayanan yang ramah, cepat, dan responsif untuk kegiatan pendidikan, penelitian, dan pengabdian masyarakat.", "photo_2025-11-23_19-02-11-1.jpg", "", 36, 300),
     ("Aksesibilitas Difabel", "Fasilitas yang bersih, nyaman, dan representatif untuk berbagai kalangan, termasuk penyandang difabel.", "Wastafel_DSCN6929-scaled-1.jpg", "", 62, 300)]
FT = [[("Ruang kelas & auditorium fakultas teknik", "Katalog ruang dan auditorium Fakultas Teknik.", "fasilitas-ft-katalog.jpg", FTU + "katalog-ruang/", 58, 300),
       ("Laboratorium", "Laboratorium di lingkungan Fakultas Teknik UGM.", "fasilitas-ft-lab.jpg", FTU + "fasilitas-laboratorium/", 40, 300)],
      [("Perpustakaan", "Perpustakaan dan fasilitasnya di Fakultas Teknik.", "fasilitas-ft-perpustakaan.jpg", FTU + "perpustakaan-dan-fasilitasnya/", 31.4, 260),
       ("Unit Layanan Terpadu", "Layanan terpadu Fakultas Teknik.", "fasilitas-ft-ult.jpg", FTU + "unit-layanan-terpadu/", 31.4, 260),
       ("Konseling Psikolog", "Rumah Kayu CLT Nusantara, Fakultas Teknik UGM.", "fasilitas-ft-rumahkayu.jpg", FTU + "rumah-clt-nusantara/", 31.4, 260)],
      [("Co-working space", "Ruang kerja bersama di Fakultas Teknik.", "fasilitas-ft-cws.jpg", FTU + "co-working-space-di-ft-ugm/", 31.4, 260),
       ("Fasilitas Difabel", "Fasilitas ramah difabel di kampus Fakultas Teknik.", "fasilitas-ft-difabel.jpg", FTU + "fasilitas-difabel/", 31.4, 260),
       ("Teknologi Informasi", "Layanan teknologi informasi Fakultas Teknik.", "fasilitas-ft-ti.jpg", FTU + "teknologi-informasi/", 31.4, 260)]]
UG = [("Perpustakaan UGM", "Layanan perpustakaan Universitas Gadjah Mada.", "fasilitas-ugm-perpustakaan.jpg", "https://lib.ugm.ac.id/", 58, 280),
      ("Fasilitas Kemahasiswaan UGM", "Fasilitas kemahasiswaan di UGM (Ditmawa).", "fasilitas-ugm-kemahasiswaan.jpg", "https://ditmawa.ugm.ac.id/fasilitas-kemahasiswaan/", 40, 280)]


def kartu(n, d, img, url, w, h):
    big = h >= 300
    judul = be.widget("heading", title=n, header_size="h3", title_color="#FFFFFF", typography_typography="custom", typography_font_family="Plus Jakarta Sans",
                      typography_font_weight="600", typography_font_size=be.ukuran_(28 if big else 22), typography_font_size_mobile=be.ukuran_(22),
                      typography_line_height={"unit": "em", "size": 1.2, "sizes": []}, _title="Judul",
                      **({"link": {"url": url, "is_external": "on", "nofollow": "", "custom_attributes": ""}} if url else {}))
    teks = bp.teks(f"<p>{d}</p>", "#FFFFFF", 16 if big else 15, None)
    teks["settings"]["text_color"] = "#FFFFFF"
    return be.container([judul, teks], content_width="full", flex_direction="column", flex_justify_content="flex-end", flex_gap=be.gap(6), padding=bp.ruang(24),
                        padding_mobile=bp.ruang(18), border_radius=bp.sudut(20), min_height=be.ukuran(h, "px"), min_height_mobile=be.ukuran(220, "px"),
                        width=be.ukuran(w, "%"), width_tablet=be.ukuran(100, "%"), width_mobile=be.ukuran(100, "%"), overflow="hidden",
                        background_background="classic", background_image={"url": B + img if not img.startswith("http") else img, "id": "", "size": "", "source": "library"},
                        background_position="center center", background_size="cover", background_repeat="no-repeat",
                        background_overlay_background="gradient", background_overlay_color="rgba(7,60,100,0.06)", background_overlay_color_b="rgba(7,60,100,0.82)",
                        background_overlay_gradient_angle={"unit": "deg", "size": 180, "sizes": []}, background_overlay_color_stop={"unit": "%", "size": 35, "sizes": []},
                        _title="Kartu " + n)


def baris(rows):
    return be.container([kartu(*r) for r in rows], content_width="full", flex_direction="row", flex_wrap="wrap", flex_gap=be.gap(20), flex_align_items="stretch",
                        padding=bp.ruang(0), _title="Baris kartu")


def bagian(judul, sub, rows, bg):
    h2 = be.widget("heading", title=judul, header_size="h2", title_color="#161616", _title="Judul bagian")
    return be.container([h2, bp.teks(f"<p>{sub}</p>", "#636363", 17, None), be.container([baris(r) for r in rows], content_width="full", flex_direction="column", flex_gap=be.gap(20),
                                                                                        padding=bp.ruang(0), _title="Kartu")],
                        content_width="full", flex_direction="column", flex_gap=be.gap(14), background_background="classic", background_color=bg,
                        border_radius=bp.sudut(10), padding=bp.ruang(40), padding_mobile=bp.ruang(20), _title="Bagian " + judul)


def main():
    out = [bagian("Fasilitas departemen", "Fasilitas yang melayani tamu, mahasiswa, dan dosen Departemen Teknik Nuklir dan Teknik Fisika.", [A[:2], A[2:]], "#FFFFFF"),
           bagian("Fasilitas Fakultas Teknik", "Fasilitas bersama di tingkat fakultas. Klik judul kartu untuk membuka halaman di situs Fakultas Teknik.", FT, "#F5F5F5"),
           bagian("Fasilitas UGM", "Layanan dan fasilitas di tingkat universitas.", [UG], "#FFFFFF")]
    d = bo.halaman(out, "Fasilitas Umum")
    s = json.dumps(d, ensure_ascii=False)
    assert "<style" not in s and '"widgetType": "html"' not in s
    (ROOT / "elementor" / "native" / "fasilitas.json").write_text(s, encoding="utf-8")
    print("ok fasilitas", len(s))


if __name__ == "__main__":
    main()
