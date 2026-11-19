#!/usr/bin/env python3
"""Akreditasi untuk tf (native): dikelompokkan per prodi (S1 TN, S1 TF, Magister), grid rata tengah, jumlah kartu mengikuti jumlah dokumen.
Gambar sertifikat = media tf yang sudah ada (akreditasi-1..5). Kartu tanpa berkas = teks 'Berkas sertifikat akan ditambahkan'."""
import json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import buat_elementor as be  # noqa: E402
import buat_profil_dosen as bp  # noqa: E402
import buat_native_orang as bo  # noqa: E402

ROOT = be.ROOT
B = "https://tf.ugm.ac.id/wp-content/uploads/sites/7/2026/11/"
G = [("S1 Teknik Nuklir", [("Akreditasi LAM Teknik Program Studi S1 Teknik Nuklir", "akreditasi-1.jpeg"), ("Akreditasi IABEE Program Studi S1 Teknik Nuklir", "akreditasi-2.png")]),
     ("S1 Teknik Fisika", [("Akreditasi LAM Teknik Program Studi S1 Teknik Fisika", "akreditasi-3.png"), ("Akreditasi IABEE Program Studi S1 Teknik Fisika", "akreditasi-4.jpeg")]),
     ("Magister Teknik Fisika", [("Akreditasi LAM Teknik Program Magister, Program Studi Teknik Fisika", "akreditasi-5.png")])]
# Catatan: judul asli di halaman tf tidak cocok dengan gambar; pemetaan ini hasil membaca isi tiap sertifikat (19 Nov).


def kartu(judul, img):
    if img:
        isi = be.widget("image", image={"url": B + img, "id": "", "alt": judul}, image_size="full", width=be.ukuran(100, "%"), height=be.ukuran(220, "px"),
                        image_border_radius=bp.sudut(10), _title="Sertifikat", **{"object-fit": "contain"})
    else:
        isi = be.container([bp.teks("<p>Berkas sertifikat akan ditambahkan.</p>", "#636363", 15, None)], content_width="full", flex_justify_content="center",
                           flex_align_items="center", min_height=be.ukuran(220, "px"), background_background="classic", background_color="#F5F5F5", border_radius=bp.sudut(10),
                           padding=bp.ruang(16), _title="Berkas belum ada")
    return be.container([isi, be.widget("heading", title=judul, header_size="h3", title_color="#161616", _title="Judul")], content_width="full", flex_direction="column",
                        flex_gap=be.gap(12), background_background="classic", background_color="#FFFFFF", border_border="solid",
                        border_width={"unit": "px", "top": "1", "right": "1", "bottom": "1", "left": "1", "isLinked": True}, border_color=bp.GARIS,
                        border_radius=bp.sudut(16), padding=bp.ruang(14), width=be.ukuran(31.5, "%"), width_tablet=be.ukuran(48.5, "%"), width_mobile=be.ukuran(100, "%"),
                        _title="Kartu " + judul)


def main():
    out = []
    for i, (prodi, ks) in enumerate(G):
        out.append(bo.bagian(prodi, [kartu(*k) for k in ks], "#F5F5F5" if i % 2 else "#FFFFFF", True))
    intro = bp.teks("<p>Akreditasi program studi dari LAM Teknik dan IABEE.</p>", "#636363", 17, None)
    d = bo.halaman([intro] + out, "Akreditasi")
    s = json.dumps(d, ensure_ascii=False)
    assert "<style" not in s and '"widgetType": "html"' not in s
    (ROOT / "elementor" / "native" / "akreditasi.json").write_text(s, encoding="utf-8")
    print("ok akreditasi", len(s))


if __name__ == "__main__":
    main()
