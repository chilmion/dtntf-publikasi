#!/usr/bin/env python3
"""Galeri riset KBK (bento): potong gambar dokumentasi/gambar contoh -> manual/kbk-ekstra/galeri-<kode>-N.jpg
dan tulis kunci "galeri" ke manual/kbk-ekstra/<kode>.json. Gambar `contoh: true` = penanda sementara (ganti dengan foto riset asli
dengan menimpa berkasnya, lalu hapus "contoh"). Memakai sips (macOS)."""
import json, pathlib, subprocess, tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
EK = ROOT / "manual" / "kbk-ekstra"


def sips(*a):
    subprocess.run(["sips", *a], check=True, capture_output=True)


def potong(src, y, x, h, w, nama, lebar=1000):
    """Potong persegi (y,x,h,w). sips hanya andal dengan offset vertikal: potong baris, putar 90, potong lagi, putar balik."""
    d = pathlib.Path(tempfile.mkdtemp())
    lebar_asli = int(subprocess.run(["sips", "-g", "pixelWidth", str(src)], capture_output=True, text=True).stdout.split()[-1])
    sips("-s", "format", "jpeg", "--cropOffset", str(y), "0", "-c", str(h - 2), str(lebar_asli - 2), str(src), "--out", str(d / "1.jpg"))
    h = h - 2
    sips("-r", "90", str(d / "1.jpg"), "--out", str(d / "2.jpg"))
    w = w - 2
    x = max(1, min(x, lebar_asli - 2 - w - 4))   # sips tidak memotong bila tepi potongan tepat di tepi gambar
    sips("--cropOffset", str(x), "0", "-c", str(w), str(h - 2), str(d / "2.jpg"), "--out", str(d / "3.jpg"))
    sips("-r", "270", str(d / "3.jpg"), "--out", str(d / "4.jpg"))
    sips("-s", "formatOptions", "80", "-Z", str(lebar), str(d / "4.jpg"), "--out", str(EK / nama))


def tulis(kode, galeri):
    f = EK / f"{kode}.json"
    d = json.loads(f.read_text(encoding="utf-8")) if f.exists() else {}
    d["galeri"] = galeri
    f.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")


# Instrumentasi: kolase dokumentasi (2262x1304, 3x3 foto) dipotong per foto; skala dari tampilan 1000px = 2.262
k = 1800 / 1000    # kolase sudah diperkecil ke 1800px lebar; koordinat di bawah dari tampilan 1000px
col = ROOT / "manual" / "kbk-ekstra" / "instrumentasi-dokumentasi.jpg"
ins = [("rapat koordinasi tim", 8, 334, 188, 329), ("pengujian panel kontrol", 8, 664, 188, 336), ("model 3D gedung", 192, 0, 181, 333),
       ("smart switch di ruang lab", 192, 664, 181, 336), ("pengujian sensor di ruang akustik", 192, 336, 181, 326),
       ("peta sebaran intensitas cahaya", 377, 0, 199, 333), ("pemasangan perangkat ukur", 377, 336, 199, 326), ("prototipe perangkat sensor", 377, 664, 199, 336)]
g = []
for i, (j, y, x, h, w) in enumerate(ins, 1):
    n = f"galeri-instrumentasi-{i}.jpg"
    potong(col, round(y * k), round(x * k), round(h * k), round(w * k), n)
    g.append({"gambar": "kbk/" + n, "judul": j[0].upper() + j[1:]})
tulis("instrumentasi", g)

# KBK lain: gambar contoh seadanya (hero KBK + foto fasilitas FT) — tandai "contoh"
FAS = ROOT / "data" / "ugm" / "fasilitas"
H = ROOT / "data" / "kbk"
def contoh(kode, daftar):
    g = []
    for i, (src, y, x, h, w, j) in enumerate(daftar, 1):
        n = f"galeri-{kode}-{i}.jpg"
        potong(src, y, x, h, w, n)
        g.append({"gambar": "kbk/" + n, "judul": j, "contoh": True})
    tulis(kode, g)
contoh("enet", [(H / "enet.jpg", 0, 0, 933, 933, "Dokumentasi riset"), (FAS / "ft-lab.jpg", 0, 0, 800, 1200, "Laboratorium"), (H / "enet.jpg", 480, 0, 900, 900, "Kegiatan penelitian"),
                (FAS / "ft-ti.jpg", 0, 0, 563, 1200, "Pengujian"), (FAS / "ft-perpustakaan.jpg", 0, 0, 800, 1200, "Diskusi riset")])
contoh("proses-nuklir", [(H / "proses-nuklir.jpg", 0, 0, 1227, 1400, "Dokumentasi riset"), (FAS / "ft-lab.jpg", 0, 0, 800, 1200, "Laboratorium"),
                         (H / "proses-nuklir.jpg", 0, 350, 800, 1000, "Kegiatan penelitian"), (FAS / "ft-ti.jpg", 0, 0, 563, 1200, "Pengujian"), (FAS / "ft-perpustakaan.jpg", 0, 0, 800, 1200, "Diskusi riset")])
contoh("multifisika", [(FAS / "ft-lab.jpg", 0, 0, 800, 1200, "Dokumentasi riset"), (FAS / "ft-ti.jpg", 0, 0, 563, 1200, "Pengujian"), (FAS / "ft-katalog.jpg", 0, 0, 800, 1200, "Ruang penelitian"),
                        (FAS / "ft-ult.jpg", 0, 0, 800, 1200, "Kegiatan penelitian"), (FAS / "ft-cws.jpg", 0, 0, 800, 1200, "Diskusi riset")])
print("galeri ditulis")
