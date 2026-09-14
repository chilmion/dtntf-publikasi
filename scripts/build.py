#!/usr/bin/env python3
"""
Scraper profil dosen DTNTF — sumber tunggal: SINTA (kemdiktisaintek).

SINTA sudah mengagregasi Scopus, Garuda, dan Google Scholar dalam satu profil,
jadi tidak perlu menyentuh situs Scopus (yang melarang scraping) sama sekali.

Yang diambil per dosen:
  - identitas, afiliasi, program studi, subject
  - skor SINTA overall & 3 tahun
  - tabel metrik: artikel, sitasi, cited document, h-index, i10, g-index
    untuk Scopus dan Google Scholar
  - daftar publikasi Scopus (judul, jurnal, kuartil, urutan penulis, tahun, sitasi)
  - daftar publikasi Garuda

Hanya pustaka standar Python — tidak perlu pip install apa pun.

Pakai:
    python3 scripts/build.py                    # semua dosen di dosen.csv
    python3 scripts/build.py faridah,widya-rosita   # sebagian saja
    python3 scripts/build.py --periksa 6010146      # diagnostik semua tab
    python3 scripts/build.py --halaman 6010146      # diagnostik paginasi
"""

import csv
import html as html_mod
import os
import json
import pathlib
import random
import re
import sys
import time
import http.cookiejar
import urllib.error
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
SINTA = "https://sinta.kemdiktisaintek.go.id"

# Opsional: kalau diisi, daftar Scopus diambil lengkap lewat API Elsevier
# alih-alih 10 entri dari SINTA. Simpan sebagai secret SCOPUS_API_KEY.
SCOPUS_KEY = os.environ.get("SCOPUS_API_KEY", "").strip()

# Jeda antar request. Jangan diturunkan — ini yang membuat scraper tidak
# dianggap serangan dan tidak membuat IP diblokir.
JEDA = (2.5, 5.0)
MAKS_HALAMAN = 25        # pengaman; 1 halaman = 20 artikel

# Tab profil SINTA yang ditarik: (parameter ?view=, label sumber, kategori)
VIEWS = [
    ("scopus",      "scopus",     "Scopus"),
    ("garuda",      "garuda",     "Garuda"),
    ("books",       "buku",       "Buku"),
    ("iprs",        "paten",      "Paten & HKI"),
    ("services",    "ppm",        "Pengabdian"),
    ("researches",  "penelitian", "Penelitian"),
]

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")

# SINTA tampaknya menyimpan posisi halaman di sesi, bukan murni di URL:
# permintaan tanpa cookie selalu mendapat halaman pertama. Satu opener
# dipakai bersama agar cookie sesi terbawa antar permintaan, persis seperti
# browser biasa.
BISKUIT = http.cookiejar.CookieJar()
OPENER = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(BISKUIT))


# ---------------------------------------------------------------- pengambilan

def ambil(url, tries=3, lapor=False):
    """GET satu halaman.

    Mengembalikan teks HTML, atau None kalau gagal. Dengan lapor=True,
    alasan kegagalan dicetak — ini yang membuat log bisa menjelaskan sendiri
    kenapa sebuah tab berhenti lebih awal.
    """
    sebab = "tidak diketahui"
    for attempt in range(tries):
        try:
            req = urllib.request.Request(url, headers={
                "User-Agent": UA,
                "Accept": "text/html,application/xhtml+xml",
                "Accept-Language": "id-ID,id;q=0.9,en;q=0.8",
                "Referer": SINTA + "/",
            })
            with OPENER.open(req, timeout=45) as r:
                isi = r.read().decode("utf-8", "replace")
                if lapor:
                    print(f"        HTTP {r.status} · {len(isi)//1024} KB · "
                          f"{isi.count('ar-list-item')} blok")
                return isi
        except urllib.error.HTTPError as e:
            sebab = f"HTTP {e.code}"
            if e.code in (403, 429):
                tunggu = 30 * (attempt + 1)
                print(f"      ! diblokir sementara ({e.code}); tunggu {tunggu}s", file=sys.stderr)
                time.sleep(tunggu)
            elif e.code == 404:
                if lapor:
                    print("        HTTP 404 — halaman tidak ada")
                return None
            else:
                time.sleep(5)
        except Exception as e:
            sebab = str(e)[:80]
            time.sleep(5)
    if lapor:
        print(f"        gagal setelah {tries} percobaan: {sebab}")
    return None


def santai():
    time.sleep(random.uniform(*JEDA))


# ---------------------------------------------------------------- parsing

def bersih(s):
    """Buang tag, rapikan entitas dan spasi."""
    s = re.sub(r"<[^>]+>", " ", s or "")
    return re.sub(r"\s+", " ", html_mod.unescape(s)).strip()


def angka(s):
    s = (s or "").strip().replace(".", "").replace(",", ".")
    try:
        return float(s) if "." in s else int(s)
    except ValueError:
        return None


def parse_profil(h):
    """Metrik dan identitas dari halaman profil SINTA."""
    d = {}

    m = re.search(r'<h3>\s*<a[^>]*>(.*?)</a>', h, re.S)
    d["nama_sinta"] = bersih(m.group(1)) if m else None

    m = re.search(r'href="[^"]*/affiliations/profile/\d+"[^>]*>(.*?)</a>', h, re.S)
    d["afiliasi"] = bersih(m.group(1)) if m else None

    m = re.search(r'href="[^"]*/departments/profile/[^"]*"[^>]*>(.*?)</a>', h, re.S)
    d["prodi"] = bersih(m.group(1)) if m else None

    m = re.search(r'<img\s+src="([^"]+)"[^>]*alt="avatar"', h)
    d["foto"] = html_mod.unescape(m.group(1)) if m else None

    # SINTA memuat foto dari Google Scholar, dan URL-nya membawa user id.
    m = re.search(r'scholar\.google[^"\']*?[?&](?:amp;)?user=([A-Za-z0-9_-]{8,})', h)
    d["scholar_id"] = m.group(1) if m else None

    m = re.search(r'<ul class="subject-list">(.*?)</ul>', h, re.S)
    d["subjects"] = ([bersih(x) for x in re.findall(r'<li>(.*?)</li>', m.group(1), re.S)]
                     if m else [])

    # skor: pasangan <div class="pr-num">…</div><div class="pr-txt">…</div>
    skor = {}
    for num, txt in re.findall(
            r'<div class="pr-num">(.*?)</div>\s*<div class="pr-txt">(.*?)</div>', h, re.S):
        skor[bersih(txt)] = angka(bersih(num))
    d["skor"] = {
        "overall": skor.get("SINTA Score Overall"),
        "tiga_tahun": skor.get("SINTA Score 3Yr"),
        "afiliasi": skor.get("Affil Score"),
        "afiliasi_tiga_tahun": skor.get("Affil Score 3Yr"),
    }

    # tabel metrik Scopus / GScholar / WOS
    metrik = {"scopus": {}, "scholar": {}, "wos": {}}
    m = re.search(r'<table[^>]*stat-table[^>]*>(.*?)</table>', h, re.S)
    if m:
        kunci = {"Article": "artikel", "Citation": "sitasi",
                 "Cited Document": "dokumen_disitasi", "H-Index": "hindex",
                 "i10-Index": "i10index", "G-Index": "gindex"}
        for baris in re.findall(r'<tr>(.*?)</tr>', m.group(1), re.S):
            sel = re.findall(r'<t[dh][^>]*>(.*?)</t[dh]>', baris, re.S)
            if len(sel) < 3:
                continue
            label = kunci.get(bersih(sel[0]))
            if not label:
                continue
            metrik["scopus"][label] = angka(bersih(sel[1]))
            metrik["scholar"][label] = angka(bersih(sel[2]))
            if len(sel) > 3:
                metrik["wos"][label] = angka(bersih(sel[3]))
    if not metrik["wos"]:
        metrik.pop("wos")
    d["metrik"] = metrik
    return d


# Slot ".ar-quartile" dipakai ulang SINTA untuk hal berbeda di tiap tab:
# kuartil di Scopus, akreditasi di Garuda, ISBN di Buku, jenis di Paten,
# dan nilai dana di PPM/Penelitian. Peta ini menaruhnya di field yang benar.
LABEL_FIELD = {
    "scopus": "kuartil",
    "garuda": "akreditasi",
    "buku": "isbn",
    "paten": "jenis_paten",
    "ppm": "dana",
    "penelitian": "dana",
}


def rapikan_venue(v):
    """Garuda menempelkan nomor halaman ke nama jurnal: '…Februari779-792'."""
    if not v:
        return v
    return re.sub(r"(?<=[^\d\s])(\d+\s*[-–]\s*\d+)\s*$", r" \1", v).strip()


def parse_artikel(h, sumber):
    """Semua .ar-list-item pada satu halaman, disesuaikan dengan tab asalnya."""
    hasil = []
    for blok in re.findall(r'<div class="ar-list-item[^"]*">(.*?)(?=<div class="ar-list-item|\Z)',
                           h, re.S):
        m = re.search(r'<div class="ar-title">\s*<a[^>]*href="([^"]*)"[^>]*>(.*?)</a>', blok, re.S)
        if not m:
            m2 = re.search(r'<div class="ar-title">(.*?)</div>', blok, re.S)
            if not m2:
                continue
            url, judul = None, bersih(m2.group(1))
        else:
            url, judul = html_mod.unescape(m.group(1)), bersih(m.group(2))
        if not judul:
            continue

        # SINTA memakai href="#!" untuk entri tanpa tautan keluar.
        if url and not url.lower().startswith("http"):
            url = None

        def cari(pola):
            x = re.search(pola, blok, re.S)
            return bersih(x.group(1)) if x else None

        label = cari(r'class="ar-quartile"[^>]*>(.*?)</a>')
        tahun = cari(r'class="ar-year"[^>]*>(.*?)</a>')
        mentah_cited = cari(r'class="ar-cited"[^>]*>(.*?)</a>')

        # Hanya hitung sebagai sitasi kalau benar-benar bertuliskan "cited".
        # Di tab paten slot ini berisi nomor paten, di Garuda berisi nomor lain.
        sitasi, info = 0, None
        if mentah_cited:
            c = re.search(r"([\d.,]+)\s*cited", mentah_cited, re.I)
            if c:
                sitasi = angka(re.sub(r"\D", "", c.group(1))) or 0
            else:
                info = mentah_cited

        a = {
            "judul": judul,
            "url": url,
            "sumber": sumber,
            "venue": rapikan_venue(cari(r'class="ar-pub"[^>]*>(.*?)</a>')),
            "tahun": angka(re.sub(r"\D", "", tahun or "")),
            "sitasi": sitasi,
            "urutan_penulis": cari(r'>\s*Author Order\s*:\s*(.*?)</a>'),
            "kreator": cari(r'>\s*Creator\s*:\s*(.*?)</a>'),
            "kuartil": None,
            "jenis_venue": None,
            "info": info,
        }

        if label:
            if sumber == "scopus":
                # bentuknya "Q2 as Journal"
                a["kuartil"] = re.sub(r"\s*as\s+.*$", "", label).strip() or None
                if " as " in label:
                    a["jenis_venue"] = label.split(" as ", 1)[1].strip()
            else:
                nilai = re.sub(r"^\s*(Accred|ISBN)\s*:\s*", "", label).strip()
                a[LABEL_FIELD.get(sumber, "info")] = nilai or None

        hasil.append(a)
    return hasil


def ambil_semua_artikel(sinta_id, view, sumber, harapan=None):
    """Kumpulkan seluruh entri satu tab.

    SINTA memuat 10 entri per halaman dan tidak menampilkan tautan paginasi
    di HTML-nya, jadi jumlah halaman harus ditebak dengan mencoba ?page=N.

    Tiap halaman dicatat ke log (status HTTP, ukuran, jumlah blok, jumlah
    judul baru) supaya kalau sebuah tab berhenti lebih awal, log langsung
    menunjukkan penyebabnya tanpa perlu menebak.
    """
    semua, terlihat = [], set()
    kosong_beruntun = gagal_beruntun = 0
    print(f"      [{sumber}] mulai" + (f", SINTA menyebut {harapan} entri" if harapan else ""))

    # Buka tab tanpa nomor halaman dulu agar cookie sesi terbentuk, sama
    # seperti orang yang mengklik tab itu di browser sebelum pindah halaman.
    ambil(f"{SINTA}/authors/profile/{sinta_id}/?view={view}")
    santai()

    for hal in range(1, MAKS_HALAMAN + 1):
        print(f"      · hal {hal}")
        h = ambil(f"{SINTA}/authors/profile/{sinta_id}/?view={view}&page={hal}", lapor=True)
        if not h:
            # coba susunan parameter alternatif sebelum menganggap gagal
            print("        coba bentuk URL alternatif")
            h = ambil(f"{SINTA}/authors/profile/{sinta_id}?page={hal}&view={view}", lapor=True)
        if not h:
            gagal_beruntun += 1
            if gagal_beruntun >= 2:
                print(f"        berhenti: 2 halaman gagal berturut-turut")
                break
            santai()
            continue
        gagal_beruntun = 0

        batch = parse_artikel(h, sumber)
        if not batch:
            print("        0 entri terbaca — kemungkinan halaman terakhir")
            break

        baru_ini = [a for a in batch if a["judul"] not in terlihat]
        for a in baru_ini:
            terlihat.add(a["judul"])
        semua.extend(baru_ini)
        print(f"        {len(batch)} entri, {len(baru_ini)} baru, total {len(semua)}")

        if baru_ini:
            kosong_beruntun = 0
        else:
            kosong_beruntun += 1
            if kosong_beruntun >= 3:
                print("        berhenti: 3 halaman tanpa judul baru")
                break

        if harapan and len(semua) >= harapan:
            print(f"        berhenti: sudah mencapai {harapan} sesuai metrik SINTA")
            break

        santai()

    if harapan and len(semua) < harapan:
        print(f"      ! {sumber}: terkumpul {len(semua)}, menurut SINTA ada {harapan}",
              file=sys.stderr)
    return semua


def kategori(a):
    """Kelompok yang dipakai di halaman departemen."""
    if a["sumber"] == "scopus":
        jv = (a.get("jenis_venue") or "").lower()
        if "conference" in jv or "proceeding" in jv:
            return "Prosiding Internasional"
        if "book" in jv:
            return "Book Chapter / Book Series"
        return "Jurnal Internasional"
    return {"garuda": "Jurnal Nasional", "buku": "Buku",
            "paten": "Paten & HKI", "ppm": "Pengabdian kepada Masyarakat",
            "penelitian": "Penelitian"}.get(a["sumber"], "Lainnya")


URUT_KATEGORI = ["Jurnal Internasional", "Prosiding Internasional",
                 "Book Chapter / Book Series", "Jurnal Nasional", "Buku",
                 "Paten & HKI", "Penelitian", "Pengabdian kepada Masyarakat", "Lainnya"]


# ---------------------------------------------------------------- perakitan

def hitung_hindex(sitasi):
    s = sorted(sitasi, reverse=True)
    h = 0
    for i, c in enumerate(s, 1):
        if c >= i:
            h = i
        else:
            break
    return h


def rakit(row, profil, artikel):
    sinta_id = row["sinta_id"].strip()
    m = profil.get("metrik", {})
    sc, gs = m.get("scopus", {}), m.get("scholar", {})

    ilmiah = [a for a in artikel if a["sumber"] in ("scopus", "garuda", "buku")]
    per_tahun = {}
    for a in ilmiah:
        if a["tahun"]:
            e = per_tahun.setdefault(a["tahun"], {"tahun": a["tahun"], "publikasi": 0, "sitasi": 0})
            e["publikasi"] += 1
            e["sitasi"] += a["sitasi"] or 0

    kuartil = {}
    for a in artikel:
        if a["sumber"] == "scopus" and a["kuartil"]:
            kuartil[a["kuartil"]] = kuartil.get(a["kuartil"], 0) + 1

    venue = {}
    for a in ilmiah:
        if a["venue"]:
            venue[a["venue"]] = venue.get(a["venue"], 0) + 1

    per_sumber = {}
    for a in artikel:
        per_sumber[a["sumber"]] = per_sumber.get(a["sumber"], 0) + 1
    n_scopus = per_sumber.get("scopus", 0)
    n_garuda = per_sumber.get("garuda", 0)

    return {
        "slug": row["slug"].strip(),
        "sinta_id": sinta_id,
        "nama": row.get("nama", "").strip() or profil.get("nama_sinta"),
        "nama_sinta": profil.get("nama_sinta"),
        "gelar": row.get("gelar", "").strip() or None,
        "jabatan": row.get("jabatan", "").strip() or None,
        "email": row.get("email", "").strip() or None,
        "prodi": profil.get("prodi"),
        "afiliasi": profil.get("afiliasi"),
        "foto_url": row.get("foto_url", "").strip() or profil.get("foto"),
        "diperbarui": time.strftime("%Y-%m-%dT%H:%M:%S+07:00"),
        # SINTA hanya menampilkan 10 entri per tab untuk pengunjung tanpa login
        # (tombol "View more" mengarah ke halaman login). Ditandai di sini supaya
        # widget bisa menyampaikannya apa adanya ke pembaca.
        "batas_daftar": {"sumber": "sinta", "per_kategori": 10,
                         "lengkap": bool(SCOPUS_KEY)},
        "tautan": {
            "sinta": f"{SINTA}/authors/profile/{sinta_id}",
            "scopus": (f"https://www.scopus.com/authid/detail.uri?authorId={row['scopus_id'].strip()}"
                       if row.get("scopus_id", "").strip() else None),
            "garuda": f"{SINTA}/authors/profile/{sinta_id}/?view=garuda",
            "scholar": (lambda sid: f"https://scholar.google.com/citations?user={sid}" if sid else None)(
                row.get("scholar_id", "").strip() or profil.get("scholar_id")),
        },
        "skor": profil.get("skor", {}),
        "metrik": m,
        "ringkas": {
            "publikasi_scopus": sc.get("artikel") if sc.get("artikel") is not None else n_scopus,
            "publikasi_garuda": n_garuda,
            "sitasi_scopus": sc.get("sitasi"),
            "sitasi_scholar": gs.get("sitasi"),
            "hindex_scopus": sc.get("hindex"),
            "hindex_scholar": gs.get("hindex"),
            "hindex_terdaftar": hitung_hindex([a["sitasi"] or 0 for a in artikel]),
            "paten": per_sumber.get("paten", 0),
            "ppm": per_sumber.get("ppm", 0),
            "buku": per_sumber.get("buku", 0),
            "penelitian": per_sumber.get("penelitian", 0),
        },
        "per_sumber": per_sumber,
        "subjects": profil.get("subjects", []),
        "per_tahun": sorted(per_tahun.values(), key=lambda x: x["tahun"]),
        "kuartil": [{"nama": k, "jumlah": v}
                    for k, v in sorted(kuartil.items(), key=lambda kv: kv[0])],
        "venue_teratas": [{"nama": k, "jumlah": v}
                          for k, v in sorted(venue.items(), key=lambda kv: -kv[1])[:10]],
        "publikasi": sorted([dict(a, kategori=kategori(a)) for a in artikel],
                            key=lambda a: (-(a["tahun"] or 0), -(a["sitasi"] or 0))),
    }


def periksa_halaman(sinta_id, view="scopus"):
    """Bandingkan isi halaman 1, 2, dan 3 satu tab.

    Menjawab pertanyaan: apakah ?page=2 benar-benar memberi entri berbeda,
    atau SINTA mengabaikannya dan mengirim ulang halaman pertama?
    """
    print(f"Membandingkan halaman 1-3 tab '{view}' untuk SINTA {sinta_id}\n")
    kumpulan = []
    for hal in (1, 2, 3):
        h = ambil(f"{SINTA}/authors/profile/{sinta_id}/?view={view}&page={hal}")
        if not h:
            print(f"  halaman {hal}: tidak terbaca"); kumpulan.append(set()); continue
        a = parse_artikel(h, view)
        judul = {x["judul"] for x in a}
        kumpulan.append(judul)
        print(f"  halaman {hal}: {len(a)} entri")
        for x in a[:3]:
            print(f"     · {(x['judul'] or '')[:64]}")
        santai()

    if kumpulan[0] and kumpulan[1]:
        sama = len(kumpulan[0] & kumpulan[1])
        print(f"\n  halaman 1 ∩ halaman 2 : {sama} judul sama dari {len(kumpulan[0])}")
        if sama == len(kumpulan[0]):
            print("  → ?page= DIABAIKAN SINTA. Paginasi butuh cara lain.")
        elif sama:
            print("  → halaman tumpang tindih sebagian; urutan daftar tidak stabil.")
        else:
            print("  → paginasi bekerja normal.")
    semua = set().union(*kumpulan) if kumpulan else set()
    print(f"  total judul unik dari 3 halaman: {len(semua)}")
    return 0


def periksa(sinta_id):
    """Cek satu per satu tab SINTA dan laporkan apa yang terbaca.

    Dipakai untuk memastikan parser cocok, terutama tab iprs/services/
    books/researches yang strukturnya belum diverifikasi.
    """
    print(f"Memeriksa profil SINTA {sinta_id}\n")
    h = ambil(f"{SINTA}/authors/profile/{sinta_id}")
    if not h:
        print("  profil tidak bisa diambil — cek koneksi atau ID"); return 1
    pr = parse_profil(h)
    print(f"  nama    : {pr['nama_sinta']}")
    print(f"  prodi   : {pr['prodi']}")
    print(f"  subject : {', '.join(pr['subjects']) or '(kosong)'}")
    print(f"  skor    : {pr['skor']}")
    for src, m in (pr.get("metrik") or {}).items():
        print(f"  metrik {src:8s}: {m}")
    santai()

    for view, sumber, label in VIEWS:
        h = ambil(f"{SINTA}/authors/profile/{sinta_id}/?view={view}&page=1")
        if not h:
            print(f"\n  [{label}] halaman tidak terbaca"); continue
        a = parse_artikel(h, sumber)
        n_item = h.count('class="ar-list-item')
        print(f"\n  [{label}] ?view={view} → {n_item} blok di HTML, {len(a)} terbaca parser")
        if a:
            c = a[0]
            print(f"    contoh : {(c['judul'] or '')[:70]}")
            print(f"    tahun={c['tahun']} venue={c['venue']} kuartil={c['kuartil']} "
                  f"sitasi={c['sitasi']} kategori={kategori(c)}")
            kosong = [k for k in ("judul", "tahun") if not c.get(k)]
            if kosong:
                print(f"    !! field kosong: {', '.join(kosong)} — parser perlu disesuaikan")
        elif n_item:
            print("    !! ada blok di HTML tapi parser tidak membacanya — kirim HTML ini")
        else:
            print("    (tab ini memang kosong untuk dosen tsb, atau butuh login)")
        santai()
    print("\nSelesai memeriksa.")
    return 0


# ------------------------------------------------------- Scopus API (opsional)

def get_json_scopus(url):
    req = urllib.request.Request(url, headers={
        "X-ELS-APIKey": SCOPUS_KEY, "Accept": "application/json", "User-Agent": UA})
    try:
        with OPENER.open(req, timeout=45) as r:
            return json.loads(r.read().decode())
    except Exception as e:
        print(f"      ! Scopus API: {e}", file=sys.stderr)
        return None


def scopus_publikasi(scopus_id, maks=200):
    """Daftar lengkap artikel dari Scopus Search API.

    Ini jalur sah untuk melewati batas 10 entri SINTA: Scopus mendisambiguasi
    penulis lewat Author ID, bukan nama, jadi hasilnya bersih dan lengkap.
    Butuh SCOPUS_API_KEY (minta ke perpustakaan/DSSDI UGM) dan kolom scopus_id
    terisi di dosen.csv. Tanpa itu fungsi ini dilewati dan sistem memakai
    10 entri dari SINTA seperti biasa.
    """
    if not SCOPUS_KEY or not scopus_id:
        return []

    hasil, mulai = [], 0
    while mulai < maks:
        q = urllib.parse.urlencode({
            "query": f"AU-ID({scopus_id})",
            "count": 25, "start": mulai,
            "field": ("dc:title,prism:publicationName,prism:coverDate,prism:doi,"
                      "citedby-count,subtypeDescription,eid"),
        })
        d = get_json_scopus(f"https://api.elsevier.com/content/search/scopus?{q}")
        if not d:
            break
        hasilnya = d.get("search-results") or {}
        entri = hasilnya.get("entry") or []
        if not entri or "error" in entri[0]:
            break
        for e in entri:
            tahun = (e.get("prism:coverDate") or "")[:4]
            jenis = (e.get("subtypeDescription") or "").lower()
            hasil.append({
                "judul": e.get("dc:title"),
                "url": (f"https://doi.org/{e['prism:doi']}" if e.get("prism:doi")
                        else (f"https://www.scopus.com/record/display.uri?eid={e['eid']}"
                              if e.get("eid") else None)),
                "sumber": "scopus",
                "venue": e.get("prism:publicationName"),
                "tahun": angka(tahun) if tahun.isdigit() else None,
                "sitasi": angka(e.get("citedby-count")) or 0,
                "urutan_penulis": None, "kreator": None,
                "kuartil": None,
                "jenis_venue": ("Conference Proceeding" if "conference" in jenis
                                else "Book" if "book" in jenis else "Journal"),
                "info": None,
            })
        total = int(hasilnya.get("opensearch:totalResults") or 0)
        mulai += 25
        if mulai >= total:
            break
        time.sleep(0.5)

    print(f"      [scopus-api] {len(hasil)} artikel")
    return hasil


def main():
    if len(sys.argv) > 2 and sys.argv[1] == "--periksa":
        return periksa(sys.argv[2].strip())
    if len(sys.argv) > 2 and sys.argv[1] == "--halaman":
        return periksa_halaman(sys.argv[2].strip(),
                               sys.argv[3].strip() if len(sys.argv) > 3 else "scopus")

    DATA.mkdir(exist_ok=True)
    with open(ROOT / "dosen.csv", newline="", encoding="utf-8") as f:
        rows = [r for r in csv.DictReader(f) if (r.get("sinta_id") or "").strip()]

    # Argumen: daftar slug atau ID SINTA dipisah koma, mis.
    #   python3 scripts/build.py faridah,widya-rosita
    # Bisa juga lewat env BETA_DOSEN (dipakai GitHub Actions).
    pilih = (sys.argv[1] if len(sys.argv) > 1 else os.environ.get("BETA_DOSEN", "")).strip()
    if pilih.startswith("-"):
        pilih = ""
    if pilih:
        ingin = {x.strip().lower() for x in pilih.split(",") if x.strip()}
        rows = [r for r in rows
                if r["slug"].strip().lower() in ingin or r["sinta_id"].strip() in ingin]
        if not rows:
            print(f"Tidak ada dosen cocok dengan: {pilih}", file=sys.stderr)
            return

    index, gagal = [], []
    for i, row in enumerate(rows, 1):
        sid, slug = row["sinta_id"].strip(), row["slug"].strip()
        print(f"[{i}/{len(rows)}] {slug} (SINTA {sid})")

        h = ambil(f"{SINTA}/authors/profile/{sid}")
        if not h or "ar-list-item" not in h and "stat-table" not in h:
            print("      ! profil tidak terbaca, dilewati")
            gagal.append(slug)
            continue
        profil = parse_profil(h)
        santai()

        # SINTA menyebut jumlah artikel Scopus di tabel metrik — pakai sebagai
        # patokan supaya paginasi tahu kapan benar-benar sudah lengkap.
        harapan = {"scopus": ((profil.get("metrik") or {}).get("scopus") or {}).get("artikel")}

        # Kalau API key Scopus tersedia, daftar Scopus diambil dari sana
        # (lengkap & terdisambiguasi) dan tab Scopus SINTA dilewati.
        lengkap_scopus = scopus_publikasi(row.get("scopus_id", "").strip())

        artikel = list(lengkap_scopus)
        for view, sumber, _label in VIEWS:
            if sumber == "scopus" and lengkap_scopus:
                continue
            artikel += ambil_semua_artikel(sid, view, sumber, harapan.get(sumber))
            santai()

        rek = rakit(row, profil, artikel)
        (DATA / f"{slug}.json").write_text(
            json.dumps(rek, ensure_ascii=False, indent=1), encoding="utf-8")

        index.append({
            "slug": slug, "sinta_id": sid,
            "nama": rek["nama"], "gelar": rek["gelar"], "jabatan": rek["jabatan"],
            "foto_url": rek["foto_url"], "prodi": rek["prodi"],
            "skor_sinta": (rek["skor"] or {}).get("overall"),
            "publikasi": len(rek["publikasi"]),
            "sitasi_scopus": rek["ringkas"]["sitasi_scopus"],
            "sitasi_scholar": rek["ringkas"]["sitasi_scholar"],
            "hindex_scopus": rek["ringkas"]["hindex_scopus"],
        })
        print(f"      ✓ {len(rek['publikasi'])} publikasi")
        santai()

    # Gabung dengan index lama supaya build sebagian tidak menghapus dosen lain.
    lama = {}
    f_index = DATA / "index.json"
    if f_index.exists():
        try:
            for e in json.loads(f_index.read_text())["dosen"]:
                lama[e["slug"]] = e
        except Exception:
            pass
    for e in index:
        lama[e["slug"]] = e
    index = list(lama.values())

    index.sort(key=lambda x: (x["nama"] or "").lower())
    (DATA / "index.json").write_text(json.dumps(
        {"diperbarui": time.strftime("%Y-%m-%d"), "dosen": index},
        ensure_ascii=False, indent=1), encoding="utf-8")

    print(f"\nSelesai: {len(index)} berhasil, {len(gagal)} gagal"
          + (f" → {', '.join(gagal)}" if gagal else ""))

    # Bangun ulang agregat departemen dari seluruh JSON yang ada.
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
    import agregat
    agregat.main()


if __name__ == "__main__":
    sys.exit(main() or 0)
