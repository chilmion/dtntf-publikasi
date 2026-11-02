#!/usr/bin/env python3
"""
Bangun data/kbk/kbk.json dari manual/kbk.xlsx — data lima halaman KBK
(Kelompok Bidang Keahlian: halaman induk + satu halaman per KBK).

Lembar di kbk.xlsx (baris pertama = nama kolom; petunjuk ada di lembar "Petunjuk"):
  KBK          kode, nama, singkatan, halaman, ketua, ringkasan, sekilas
  Kompetensi   kbk, judul, deskripsi              (nomor = urutan baris)
  Anggota      kbk, dosen, keahlian, peran        (peran: Ketua / Koordinator / kosong)
  Tema         kbk, judul, deskripsi, jumlah_publikasi
  Riset        kbk, tema (nomor), riset           (riset terkait, maks 5 ditampilkan)
  Publikasi    kbk, tema (nomor), sitasi, doi     (publikasi terpilih, maks 5 ditampilkan)

Satu dosen boleh ada di beberapa KBK. KBK ini BERBEDA dari kolom "kelompok"
(Teknik Nuklir/Teknik Fisika) di agregat. Isian yang kosong = widget menampilkan
lorem ipsum (kelas .kt-lorem). Statistik dihitung dari isi (dosen, kompetensi, tema,
publikasi).

    python3 scripts/kbk.py
"""

import csv
import json
import pathlib
import sys
import time

ROOT = pathlib.Path(__file__).resolve().parent.parent
MANUAL = ROOT / "manual"
OUT = ROOT / "data" / "kbk" / "kbk.json"
BERKAS = MANUAL / "kbk.xlsx"
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))


def _int(x, bawaan=0):
    try:
        return int(str(x).strip())
    except ValueError:
        return bawaan


def bangun():
    import manual
    if not BERKAS.exists():
        print("Tidak ada manual/kbk.xlsx — data/kbk/kbk.json dilewati.")
        return
    baca = lambda l: manual.baca_berkas(BERKAS, l)  # noqa: E731
    peta, masalah = manual.peta_dosen(), []
    with open(ROOT / "dosen.csv", newline="", encoding="utf-8") as f:
        dosen = {r["slug"].strip(): r for r in csv.DictReader(f)}

    def orang(nama, ket):
        s = peta.get(manual.agregat.normal(nama or ""))
        if not s:
            masalah.append(f"{ket}: dosen '{nama}' tidak dikenal (cek ejaan, pilih dari dropdown)")
            return None
        r = dosen[s]
        return {"slug": s, "nama": r["nama"].strip(), "gelar": (r.get("gelar") or "").strip(),
                "foto_url": (r.get("foto_url") or "").strip(), "url": f"/{s}/"}

    with open(MANUAL / "dosen-info.csv", newline="", encoding="utf-8") as f:
        info = {r["slug"]: r for r in csv.DictReader(f)}
    hasil = []
    for k in baca("KBK"):
        kode = k.get("kode", "").strip().lower()
        if not kode:
            continue
        mine = lambda lembar: [r for r in baca(lembar) if r.get("kbk", "").strip().lower() == kode]  # noqa: E731
        anggota = []
        for r in mine("Anggota"):
            o = orang(r.get("dosen"), f"Anggota {kode} baris {r['_baris']}")
            if o:
                # keahlian kosong → bidang ilmu dari halaman Dosen Tetap lama (data nyata, bukan karangan)
                keahlian = r.get("keahlian") or info.get(o["slug"], {}).get("bidang_ilmu", "")
                anggota.append({**o, "keahlian": keahlian, "peran": r.get("peran", "")})
        ketua = orang(k["ketua"], f"KBK {kode} ketua") if k.get("ketua") else None
        tema = [{"no": i, "judul": r.get("judul", ""), "deskripsi": r.get("deskripsi", ""),
                 "jumlah_publikasi": _int(r.get("jumlah_publikasi")), "riset": [], "publikasi": []}
                for i, r in enumerate(mine("Tema"), 1)]
        for r in mine("Riset"):
            if 1 <= _int(r.get("tema")) <= len(tema) and r.get("riset"):
                tema[_int(r["tema"]) - 1]["riset"].append(r["riset"])
        for r in mine("Publikasi"):
            if 1 <= _int(r.get("tema")) <= len(tema) and r.get("sitasi"):
                tema[_int(r["tema"]) - 1]["publikasi"].append({"sitasi": r["sitasi"], "doi": r.get("doi", "")})
        komp = [{"no": i, "judul": r.get("judul", ""), "deskripsi": r.get("deskripsi", "")}
                for i, r in enumerate(mine("Kompetensi"), 1)]
        jml_pub = sum(t["jumlah_publikasi"] or len(t["publikasi"]) for t in tema)
        halaman = (k.get("halaman") or f"kbk-{kode}").strip("/ ")
        hasil.append({"kode": kode, "nama": k.get("nama", ""), "singkatan": k.get("singkatan", ""),
                      "halaman": halaman, "url": f"/{halaman}/", "ketua": ketua,
                      "ringkasan": k.get("ringkasan", ""), "sekilas": k.get("sekilas", ""),
                      "kompetensi": komp, "anggota": anggota, "tema": tema,
                      "statistik": {"dosen": len(anggota), "kompetensi": len(komp), "tema": len(tema),
                                    "publikasi": jml_pub}})
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({"diperbarui": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "kbk": hasil},
                              ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"KBK: {len(hasil)} KBK ditulis ke {OUT.relative_to(ROOT)}")
    for m in masalah:
        print("  ! " + m)


if __name__ == "__main__":
    bangun()
