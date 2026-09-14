#!/usr/bin/env python3
"""
Gabungkan seluruh data/<slug>.json menjadi data agregat departemen.

Paper yang ditulis beberapa dosen DTNTF digabung jadi satu entri, dengan
semua nama dosen yang terlibat dicatat. Kunci penggabungan: DOI/URL kalau ada,
kalau tidak judul yang dinormalisasi.

Output:
    data/agregat/ringkas.json   → statistik + hitungan per tahun & kategori
    data/agregat/<tahun>.json   → entri publikasi tahun itu

Dipecah per tahun supaya halaman tidak perlu mengunduh ribuan entri sekaligus.

Dijalankan otomatis di akhir build.py; bisa juga sendiri:
    python3 scripts/agregat.py
"""

import json
import pathlib
import re
import sys
import time
import unicodedata

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
OUT = DATA / "agregat"

URUT_KATEGORI = ["Jurnal Internasional", "Prosiding Internasional",
                 "Book Chapter / Book Series", "Jurnal Nasional", "Buku",
                 "Paten & HKI", "Penelitian", "Pengabdian kepada Masyarakat", "Lainnya"]


def normal(judul):
    """Judul dinormalisasi untuk pencocokan: tanpa aksen, tanda baca, dan spasi ganda."""
    s = unicodedata.normalize("NFKD", judul or "").encode("ascii", "ignore").decode()
    s = re.sub(r"[^a-z0-9 ]", " ", s.lower())
    return re.sub(r"\s+", " ", s).strip()


def kunci(a):
    """DOI atau ID Scopus lebih dapat dipercaya daripada judul."""
    u = a.get("url") or ""
    m = re.search(r"eid=(2-s2\.0-\d+)", u)
    if m:
        return "scopus:" + m.group(1)
    m = re.search(r"10\.\d{4,9}/[^\s\"&?]+", u)
    if m:
        return "doi:" + m.group(0).lower().rstrip(".")
    n = normal(a.get("judul"))
    # Judul sangat pendek terlalu berisiko digabung keliru — biarkan terpisah.
    return ("judul:" + n) if len(n) > 25 else ("unik:" + n + "|" + str(a.get("tahun")))


def main():
    berkas = sorted(f for f in DATA.glob("*.json") if f.name != "index.json")
    if not berkas:
        print("Belum ada data dosen. Jalankan scripts/build.py dulu.", file=sys.stderr)
        return 1

    gabung, dosen_ringkas = {}, []

    for f in berkas:
        try:
            d = json.loads(f.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"  ! lewati {f.name}: {e}", file=sys.stderr)
            continue

        nama = d.get("nama") or d.get("nama_sinta") or d["slug"]
        dosen_ringkas.append({
            "slug": d["slug"], "nama": nama, "gelar": d.get("gelar"),
            "sinta_id": d.get("sinta_id"),
            "skor_sinta": (d.get("skor") or {}).get("overall"),
            "publikasi": len(d.get("publikasi") or []),
            "sitasi_scopus": (d.get("ringkas") or {}).get("sitasi_scopus"),
            "hindex_scopus": (d.get("ringkas") or {}).get("hindex_scopus"),
        })

        for a in d.get("publikasi") or []:
            k = kunci(a)
            e = gabung.get(k)
            if e is None:
                gabung[k] = {
                    "judul": a.get("judul"),
                    "tahun": a.get("tahun"),
                    "kategori": a.get("kategori") or "Lainnya",
                    "venue": a.get("venue"),
                    "kuartil": a.get("kuartil"),
                    "akreditasi": a.get("akreditasi"),
                    "jenis_paten": a.get("jenis_paten"),
                    "dana": a.get("dana"),
                    "isbn": a.get("isbn"),
                    "url": a.get("url"),
                    "sitasi": a.get("sitasi") or 0,
                    "kreator": a.get("kreator"),
                    "dosen": [{"slug": d["slug"], "nama": nama}],
                }
            else:
                if not any(x["slug"] == d["slug"] for x in e["dosen"]):
                    e["dosen"].append({"slug": d["slug"], "nama": nama})
                # ambil nilai terlengkap dari entri mana pun
                e["sitasi"] = max(e["sitasi"], a.get("sitasi") or 0)
                for kol in ("venue", "kuartil", "url", "tahun", "kreator",
                            "akreditasi", "jenis_paten", "dana", "isbn"):
                    if not e.get(kol) and a.get(kol):
                        e[kol] = a[kol]

    entri = list(gabung.values())
    for e in entri:
        e["dosen"].sort(key=lambda x: x["nama"])

    # ---- pecah per tahun ----
    OUT.mkdir(parents=True, exist_ok=True)
    for lama in OUT.glob("*.json"):
        lama.unlink()

    per_tahun = {}
    for e in entri:
        per_tahun.setdefault(e["tahun"] or 0, []).append(e)

    ringkas_tahun = []
    for th, daftar in sorted(per_tahun.items(), reverse=True):
        daftar.sort(key=lambda x: (URUT_KATEGORI.index(x["kategori"])
                                   if x["kategori"] in URUT_KATEGORI else 99,
                                   -(x["sitasi"] or 0), x["judul"] or ""))
        nama_file = str(th) if th else "tanpa-tahun"
        (OUT / f"{nama_file}.json").write_text(
            json.dumps({"tahun": th or None, "entri": daftar}, ensure_ascii=False, indent=1),
            encoding="utf-8")

        per_kat = {}
        for e in daftar:
            per_kat[e["kategori"]] = per_kat.get(e["kategori"], 0) + 1
        ringkas_tahun.append({
            "tahun": th or None, "berkas": nama_file,
            "jumlah": len(daftar),
            "sitasi": sum(e["sitasi"] or 0 for e in daftar),
            "per_kategori": per_kat,
        })

    total_kat = {}
    for e in entri:
        total_kat[e["kategori"]] = total_kat.get(e["kategori"], 0) + 1

    ilmiah = {"Jurnal Internasional", "Prosiding Internasional",
              "Book Chapter / Book Series", "Jurnal Nasional", "Buku"}
    kuartil = {}
    for e in entri:
        if e["kuartil"]:
            kuartil[e["kuartil"]] = kuartil.get(e["kuartil"], 0) + 1

    dosen_ringkas.sort(key=lambda x: (x["nama"] or "").lower())
    (OUT / "ringkas.json").write_text(json.dumps({
        "diperbarui": time.strftime("%Y-%m-%d"),
        "jumlah_dosen": len(dosen_ringkas),
        "total": {
            "semua": len(entri),
            "publikasi_ilmiah": sum(1 for e in entri if e["kategori"] in ilmiah),
            "sitasi": sum(e["sitasi"] or 0 for e in entri),
            "paten": total_kat.get("Paten & HKI", 0),
            "ppm": total_kat.get("Pengabdian kepada Masyarakat", 0),
            "penelitian": total_kat.get("Penelitian", 0),
        },
        "per_kategori": [{"nama": k, "jumlah": total_kat[k]}
                         for k in URUT_KATEGORI if k in total_kat],
        "kuartil": [{"nama": k, "jumlah": v} for k, v in sorted(kuartil.items())],
        "per_tahun": ringkas_tahun,
        "dosen": dosen_ringkas,
    }, ensure_ascii=False, indent=1), encoding="utf-8")

    ganda = sum(1 for e in entri if len(e["dosen"]) > 1)
    print(f"Agregat: {len(entri)} entri unik dari {len(dosen_ringkas)} dosen "
          f"({ganda} ditulis >1 dosen DTNTF), {len(per_tahun)} tahun")
    return 0


if __name__ == "__main__":
    sys.exit(main())
