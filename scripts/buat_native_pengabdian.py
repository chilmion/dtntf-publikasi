#!/usr/bin/env python3
"""Pengabdian untuk tf (native, desain v1): statistik bento, grafik 'Kegiatan per tahun' (PNG berangka, 2016-2026, label per 5 tahun), kegiatan bersama mitra.
Grafik: scripts/buat_grafik_pengabdian.py -> data/ugm/pengabdian-per-tahun.png (diunggah ke media tf: dtntf-pengabdian-per-tahun-scaled.png).
Data statis dari agregat SINTA saat build (daftar kegiatan terfilter v1 tidak ada: butuh skrip)."""
import json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import buat_elementor as be  # noqa: E402
import buat_profil_dosen as bp  # noqa: E402
import buat_native_orang as bo  # noqa: E402
import buat_native_kbk as bk  # noqa: E402
import buat_native_mitra as bm  # noqa: E402

ROOT = be.ROOT
KAT = "Pengabdian kepada Masyarakat"
R = json.loads((ROOT / "data/agregat/ringkas.json").read_text(encoding="utf-8"))
SERI = {t["tahun"]: t["per_kategori"].get(KAT, 0) for t in R["per_tahun"] if 2016 <= t["tahun"] <= 2026}
DOS = set()
for y in SERI:
    for e in json.loads((ROOT / f"data/agregat/{y}.json").read_text(encoding="utf-8")).get("entri", []):
        if e.get("kategori") == KAT:
            DOS.update(d["slug"] for d in e.get("dosen", []))
TOTAL = sum(SERI.values()); PUNCAK = max(SERI, key=SERI.get)


def main():
    stat = bm.baris([bk.tile_angka("lime", TOTAL, "Kegiatan 2016–2026"), bk.tile_angka("putih", len(DOS), "Dosen terlibat"),
                     bk.tile_angka("abu", SERI[PUNCAK], f"Tahun puncak ({PUNCAK})"), bk.tile_angka("navy", SERI[2026], "Kegiatan tahun 2026")], judul="Statistik")
    grafik = be.widget("image", image={"url": bm.B + "dtntf-pengabdian-per-tahun-scaled.png", "id": "", "alt": "Grafik kegiatan pengabdian kepada masyarakat per tahun, 2016 sampai 2026: " +
                                       ", ".join(f"{y} {n}" for y, n in sorted(SERI.items()))}, image_size="full", width=be.ukuran(100, "%"), _title="Grafik kegiatan per tahun")
    sec_g = bm.blok("Kegiatan per tahun", "Jumlah kegiatan pengabdian kepada masyarakat DTNTF per tahun, 2016–2026 (sumber: SINTA).", [grafik], "#FFFFFF")
    kabar = [bm.baris([bm.kabar(x) for x in bm.A[i:i + 3]], "center", "Kabar") for i in range(0, len(bm.A), 3)]
    sec_k = bm.blok("Kegiatan bersama mitra", "Pengabdian dan kerja sama DTNTF bersama industri, lembaga, dan masyarakat.", kabar, "#F5F5F5")
    d = bo.halaman([stat, sec_g, sec_k], "Pengabdian", "Pengabdian")
    s = json.dumps(d, ensure_ascii=False)
    assert "<style" not in s and '"widgetType": "html"' not in s
    (ROOT / "elementor" / "native" / "pengabdian.json").write_text(s, encoding="utf-8")
    print("ok pengabdian", len(s), "total", TOTAL, "dosen", len(DOS))


if __name__ == "__main__":
    main()
