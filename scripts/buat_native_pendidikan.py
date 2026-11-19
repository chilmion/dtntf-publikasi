#!/usr/bin/env python3
"""Panduan Akademik (16913) dan Kalender Akademik (16887) untuk tf, native, gaya seragam (kartu dokumen seperti halaman prodi).
Revisi 19 Nov: kartu Kurikulum S1 TN = dua tombol (Reguler, IUP); di sampingnya kartu S1 Teknik Fisika dan Magister (satu tombol Unduh PDF); Laporan Kinerja 1 kolom terbaru di atas."""
import json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import buat_elementor as be  # noqa: E402
import buat_profil_dosen as bp  # noqa: E402
import buat_native_orang as bo  # noqa: E402
import buat_native_prodi as bnp  # noqa: E402

ROOT = be.ROOT
U = "https://tf.ugm.ac.id/wp-content/uploads/sites/7/2026/11/"
BORDER = {"unit": "px", "top": "1", "right": "1", "bottom": "1", "left": "1", "isLinked": True}


def tombol(teks, url=""):
    return be.widget("button", text=teks, link={"url": url, "is_external": "", "nofollow": "", "custom_attributes": ""}, align="left", background_color="#073C64",
                     button_text_color="#FFFFFF", border_radius=bp.sudut(999), typography_typography="custom", typography_font_family="Barlow", typography_font_weight="600",
                     typography_font_size=be.ukuran_(14), text_padding={"unit": "px", "top": "10", "right": "18", "bottom": "10", "left": "18", "isLinked": False}, _title=teks)


def kartu_kur(judul, ket, tombols):
    return be.container([be.widget("heading", title=judul, header_size="h3", title_color="#073C64", _title="Judul"), bp.teks(f"<p>{ket}</p>", "#636363", 15, None),
                         be.container(tombols, content_width="full", flex_direction="row", flex_wrap="wrap", flex_gap=be.gap(10), padding=bp.ruang(0), _title="Tombol")],
                        content_width="full", flex_direction="column", flex_gap=be.gap(12), background_background="classic", background_color="#FFFFFF", border_border="solid",
                        border_width=BORDER, border_color=bp.GARIS, border_radius=bp.sudut(16), padding=bp.ruang(24), width=be.ukuran(31.5, "%"), width_tablet=be.ukuran(48.5, "%"),
                        width_mobile=be.ukuran(100, "%"), _title="Kartu " + judul)


def panduan():
    kur = bo.bagian("Panduan Kurikulum", [
        kartu_kur("Kurikulum S1 Teknik Nuklir", "Dokumen kurikulum Program Studi S1 Teknik Nuklir (Kurikulum TN 2021 V.2.0, rangkuman).",
                  [tombol("Unduh PDF Reguler", U + "Kurikulum-TN-2021-V.2.0-Rangkuman-Final.pdf"), tombol("Unduh PDF IUP")]),
        kartu_kur("Kurikulum S1 Teknik Fisika", "Dokumen kurikulum Program Studi S1 Teknik Fisika.", [tombol("Unduh PDF")]),
        kartu_kur("Kurikulum Magister Teknik Fisika", "Dokumen kurikulum Program Studi Magister Teknik Fisika.", [tombol("Unduh PDF")])], "#FFFFFF", True)
    lap = [("2024/2025", "Laporan-Kinerja-Prodi-STN-TA2024-2025-Final.pdf"), ("2023/2024", "Laporan-Kinerja-Akademik-Prodi-STN-TA2023-2024-Final.pdf"),
           ("2022/2023", "Laporan-Kinerja-Prodi-STN-2022-2023-10-04-Final.pdf"), ("2021/2022", "Laporan-Kinerja-Prodi-STN-2021-2022-09-19-Final.pdf")]
    kartu = [bnp.kartu_dok(f"Laporan Kinerja Akademik TA {t}", f"Laporan kinerja Program Sarjana Teknik Nuklir tahun akademik {t}.", f"Laporan;Kinerja;{t}", "S1 TEKNIK NUKLIR · PDF", U + f)
             for t, f in lap]
    lk = bo.bagian("Laporan Kinerja Akademik", [be.container(kartu, content_width="full", flex_direction="column", flex_gap=be.gap(16), padding=bp.ruang(0), _title="Daftar laporan")],
                   "#F5F5F5", True)
    return bo.halaman([kur, lk], "Panduan Akademik")


def kalender():
    k = bnp.kartu_dok("Kalender Akademik TA 2026/2027", "Jadwal kegiatan akademik semester gasal dan genap.", "Kalender;Akademik;2026/2027", "DEPARTEMEN · PDF",
                      U + "266-2026_KEPTOR_KALENDER_AKADEMIK.pdf")
    return bo.halaman([bo.bagian("Kalender Akademik TA 2026/2027", [k], "#FFFFFF", True)], "Kalender Akademik")


def main():
    for nama, d in (("panduan", panduan()), ("kalender", kalender())):
        s = json.dumps(d, ensure_ascii=False)
        assert "<style" not in s and '"widgetType": "html"' not in s
        (ROOT / "elementor" / "native" / f"{nama}.json").write_text(s, encoding="utf-8")
        print("ok", nama, len(s))


if __name__ == "__main__":
    main()
