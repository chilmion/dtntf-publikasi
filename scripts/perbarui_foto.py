#!/usr/bin/env python3
"""
Perbarui kolom foto_url di dosen.csv dari halaman resmi https://tf.ugm.ac.id/dosen-tetap/.

Tiap kartu di halaman itu = foto + nama (h3) + ID SINTA. Pencocokan: nama dulu
(huruf kecil, tanpa gelar/tanda baca; ID SINTA di halaman resmi pernah dobel untuk dua dosen), lalu ID SINTA. Dosen yang tidak cocok dibiarkan
dan dilaporkan.

    python3 scripts/perbarui_foto.py            # tulis dosen.csv
    python3 scripts/perbarui_foto.py --uji      # hanya laporan
"""

import csv
import html
import pathlib
import re
import sys
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
URL = "https://tf.ugm.ac.id/dosen-tetap/"
# Foto yang tidak boleh diambil dari halaman resmi (slug → URL foto yang benar); kosong = semua ikut halaman resmi
PENGECUALIAN = {}


def ambil(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (DTNTF publikasi)"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read().decode("utf-8", "replace")


def norm(s):
    s = re.sub(r"\(.*?\)", " ", html.unescape(s).lower())
    return re.sub(r"[^a-z]+", " ", s).strip()


def kartu(h):
    """-> daftar (foto, nama, sinta_id) per <section> kartu dosen."""
    hasil = []
    for sec in re.split(r"<section ", h)[1:]:
        m = re.search(r'<img[^>]+src="([^"]*wp-content/uploads[^"]+)"', sec)
        n = re.search(r"<h3[^>]*>(.*?)</h3>", sec, re.S)
        if not (m and n):
            continue
        sid = re.search(r"profile/(\d+)|[?&]id=(\d+)", sec)
        hasil.append((m.group(1), re.sub(r"<.*?>", "", n.group(1)).strip(),
                      (sid.group(1) or sid.group(2)) if sid else ""))
    return hasil


def main():
    uji = "--uji" in sys.argv
    kk = kartu(ambil(URL))
    print(f"{len(kk)} kartu terbaca di halaman resmi")
    per_id = {s: f for f, n, s in kk if s}
    per_nama = {norm(n): f for f, n, s in kk}
    path = ROOT / "dosen.csv"
    with open(path, newline="", encoding="utf-8") as f:
        rd = csv.DictReader(f)
        kolom, baris = rd.fieldnames, list(rd)
    ubah, tdk = 0, []
    for r in baris:
        foto = PENGECUALIAN.get(r["slug"]) or per_nama.get(norm(r["nama"])) or per_id.get((r.get("sinta_id") or "").strip())
        if not foto:
            tdk.append(r["nama"])
            continue
        if foto != r["foto_url"]:
            ubah += 1
            r["foto_url"] = foto
    print(f"diperbarui: {ubah} · tidak cocok: {len(tdk)} {tdk}")
    if not uji:
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=kolom)
            w.writeheader()
            w.writerows(baris)


if __name__ == "__main__":
    main()
