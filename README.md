# Publikasi DTNTF — auto-update dari SINTA

Dua halaman WordPress/Elementor yang mengisi dirinya sendiri dari SINTA,
tanpa plugin apa pun.

**1. Halaman departemen** (`/publikasi/`) — `widget/departemen.html`
Seluruh luaran 38 dosen: highlight & grafik tren di atas, lalu daftar per
tahun dikelompokkan per jenis (Jurnal Internasional, Prosiding, Jurnal
Nasional, Buku, Paten & HKI, Penelitian, Pengabdian), gaya sitasi seperti
halaman lama. Ada filter jenis/tahun/dosen dan pencarian.

**2. Halaman profil dosen** — `widget/publikasi.html`
Statistik, tren, dan daftar paper satu dosen, dikunci lewat `data-slug`.
Bagian foto/nama/bio di atasnya kamu desain sendiri di Elementor.

```
┌──────────────────────────────────┐
│  Profil dosen — desain manual    │  ← Elementor
│  foto · nama · gelar · bio       │
├──────────────────────────────────┤
│  widget/publikasi.html           │  ← auto-update
│  statistik · tren · daftar paper │
└──────────────────────────────────┘
```

## Sumber data

Hanya SINTA (`sinta.kemdiktisaintek.go.id`) — profil SINTA sudah
mengagregasi semuanya. Enam tab ditarik per dosen:

| Tab SINTA | Jadi kategori |
|---|---|
| `?view=scopus` | Jurnal Internasional / Prosiding Internasional / Book Chapter (dari label kuartil) |
| `?view=garuda` | Jurnal Nasional |
| `?view=books` | Buku |
| `?view=iprs` | Paten & HKI |
| `?view=services` | Pengabdian kepada Masyarakat |
| `?view=researches` | Penelitian |

Ditambah metrik **Scopus** dan **Google Scholar** dari tabel sidebar. Situs
Scopus tidak disentuh — ToS-nya melarang scraping.

## Penggabungan paper multi-penulis

Satu paper yang ditulis 2–3 dosen DTNTF muncul di profil masing-masing, tapi
di halaman departemen digabung jadi **satu entri** dengan semua nama dosen
disebut, supaya total departemen akurat. Kunci penggabungan: ID Scopus (EID)
atau DOI dari URL; kalau tidak ada, judul yang dinormalisasi. Judul pendek
(<25 karakter) sengaja tidak digabung untuk menghindari salah gabung.

## Struktur data

```
data/<slug>.json           satu dosen: metrik + seluruh luarannya
data/agregat/ringkas.json  statistik departemen, hitungan per tahun & kategori
data/agregat/2026.json     entri tahun itu (sudah digabung)
data/agregat/2025.json     …dst
```

Dipecah per tahun supaya halaman departemen tidak perlu mengunduh ribuan
entri sekaligus — saat dibuka hanya 3 tahun terbaru yang diambil, sisanya
menyusul saat tombol ditekan atau filter dipakai.

## Warna & font

Mengikuti Brand Guideline DTNTF 2026, jadi tidak perlu kirim HTML tema:

| Token | Nilai | Dipakai untuk |
|---|---|---|
| UGM Navy | `#073C64` | angka statistik, batang grafik, tautan, badge kuartil |
| Dark Navy | `#1A2C43` | judul bagian |
| Cinder | `#0B0B16` | teks utama |
| White Lilac | `#F7F7FB` | latar kartu |
| Mute Lime | `#C8E86D` | garis aksen di bawah judul, badge Garuda |

Font memakai **Plus Jakarta Sans**; kalau tema sudah memuatnya, widget ikut
otomatis. Semua token ada di blok `:root` widget — kalau nanti perlu digeser,
ubah di satu tempat saja, bagian `--dp-…` paling atas.

Semua CSS dikurung dalam `.dtntf-pub` sehingga tidak bocor ke elemen Elementor
lain.

## Memasang

1. Buat repo GitHub, unggah isi folder ini.
2. **Settings → Pages → Source: GitHub Actions.**
3. **Settings → Actions → General → Workflow permissions:** pilih
   *Read and write permissions* (agar workflow bisa commit hasil scrape).
4. Tab **Actions → Perbarui data publikasi → Run workflow**. Isian `dosen`
   sudah default `faridah,widya-rosita` — inilah beta-nya.
5. Cek hasil: `https://<akun>.github.io/<repo>/data/faridah.json`
6. **Halaman profil dosen** — widget **HTML** di bawah blok profil, tempel
   `widget/publikasi.html`, lalu ubah:

```html
data-base="https://<akun>.github.io/<repo>/data"
data-slug="faridah"
data-tampil="statistik,tren,publikasi"
```

`data-tampil` menentukan bagian mana yang muncul — hapus `statistik` kalau
angkanya sudah kamu taruh sendiri di blok profil, atau hapus `tren` kalau mau
daftar papernya saja.

7. **Halaman departemen** (`/publikasi/`) — widget **HTML**, tempel
   `widget/departemen.html`, lalu ubah:

```html
data-base="https://<akun>.github.io/<repo>/data"
data-awal="3"
data-profil="/dosen/{slug}/"
```

`data-profil` membuat nama dosen di tiap entri jadi tautan ke halaman
profilnya. Kosongkan kalau halaman profil belum ada.

## Setelah beta lolos

Ubah dua hal di `.github/workflows/update.yml`:

- default `faridah,widya-rosita` → kosongkan (`''`) agar semua 38 dosen ikut;
- jadwalnya sudah Senin 03:00 WIB, sesuaikan bila perlu.

**Perhatian saat naik ke 38 dosen:** GitHub Actions jalan dari IP luar negeri,
dan 38 dosen berarti ratusan request ke SINTA per sync. Risiko diblokir jauh
lebih besar daripada saat beta 2 dosen. Kalau mulai muncul HTTP 403/429 di log
Actions, pindahkan eksekusi ke mesin lokal ber-IP Indonesia dengan
`jalankan.sh` + cron — script-nya sama persis, tidak perlu diubah.

## Batas 10 entri dari SINTA

SINTA hanya menampilkan **10 entri terbaru per kategori** bagi pengunjung tanpa
login — tombol "View more" di halaman profil mengarah ke `/logins`. Tidak ada
parameter URL yang bisa menembusnya; `?page=2` diabaikan.

Konsekuensinya penting untuk kejujuran tampilan: **semua angka yang dihitung
dari daftar itu jadi bias ke tahun terbaru.** Karena yang terambil selalu yang
terbaru, tahun berjalan selalu terlihat melonjak, dan sebaran kuartil hanya
mencerminkan 10 artikel, bukan 38.

Karena itu, selama `batas_daftar.lengkap` bernilai `false`, widget profil
**menyembunyikan** grafik tren tahunan, sebaran kuartil, dan daftar jurnal
tersering. Yang tetap tampil adalah kartu statistik — angkanya datang dari
tabel metrik SINTA sendiri, bukan dari daftar, jadi tetap akurat dan lengkap.

Ketiga blok itu muncul kembali otomatis begitu `SCOPUS_API_KEY` diisi, karena
daftarnya jadi lengkap.

## Jalur lengkap: API Scopus

Isi secret `SCOPUS_API_KEY` (minta ke perpustakaan/DSSDI UGM) dan kolom
`scopus_id` di `dosen.csv`. Kalau keduanya ada, daftar Scopus diambil lewat
Scopus Search API — lengkap, terdisambiguasi per Author ID, tanpa scraping —
dan tab Scopus SINTA dilewati. Tanpa key, fungsinya dilewati diam-diam dan
sistem berjalan seperti biasa.

## Catatan kualitas data Garuda

Tab Garuda di SINTA mencocokkan berdasarkan **nama**, bukan ID penulis. Untuk
dosen bernama tunggal atau umum, entri milik orang lain ikut masuk. Ini bawaan
SINTA, bukan bug scraper — data yang sama tampil di profil SINTA publiknya.
Widget menandai tiap entri Garuda dengan label "via indeks Garuda" supaya
pembaca tahu itu hasil pencocokan otomatis.

## Catatan paginasi

SINTA memuat **10 entri per halaman** dan tidak menampilkan tautan paginasi
sama sekali di HTML-nya, jadi jumlah halaman harus ditebak dengan mencoba
`?page=2`, `?page=3`, dan seterusnya.

Masalahnya, urutan daftar SINTA tampaknya tidak stabil antar permintaan —
halaman 2 kadang berisi judul yang sama dengan halaman 1. Karena itu
`ambil_semua_artikel()`:

- tidak berhenti pada halaman pertama yang tidak membawa judul baru;
  baru menyerah setelah **3 halaman berturut-turut** tanpa judul baru;
- berhenti lebih awal kalau jumlah terkumpul sudah mencapai angka yang SINTA
  sebut sendiri di tabel metrik (khusus Scopus);
- mencoba susunan parameter alternatif (`?page=N&view=X`) kalau bentuk utama
  gagal;
- menulis peringatan `terkumpul X, menurut SINTA ada Y` kalau hasilnya kurang.

**Perhatikan peringatan itu di log.** Kalau muncul terus, paginasi SINTA
butuh pendekatan lain.

Tiap halaman dicatat ke log dengan format:

```
      [scopus] mulai, SINTA menyebut 37 entri
      · hal 1
        HTTP 200 · 38 KB · 10 blok
        10 entri, 10 baru, total 10
      · hal 2
        HTTP 200 · 37 KB · 10 blok
        10 entri, 10 baru, total 20
```

Kalau sebuah tab berhenti lebih awal, baris terakhirnya menyebut alasannya —
`HTTP 404`, `gagal setelah 3 percobaan`, `0 entri terbaca`,
`3 halaman tanpa judul baru`, atau `2 halaman gagal berturut-turut`. Tidak
perlu menebak lagi.

## Diagnostik

```bash
python3 scripts/build.py --periksa 6010146    # semua tab: berapa terbaca
python3 scripts/build.py --halaman 6010146    # apakah ?page= benar bekerja
```

`--halaman` mengambil halaman 1, 2, dan 3 satu tab lalu membandingkan
judulnya — ini yang memastikan apakah `?page=` dihormati SINTA, diabaikan,
atau daftarnya sekadar tidak stabil.

## Kalau ada yang salah

- **Semua angka kosong** → SINTA mengubah struktur HTML-nya. Yang perlu
  disesuaikan: `parse_profil()` dan `parse_artikel()` di `scripts/build.py`.
  Selector yang dipakai: `.stat-table`, `.pr-num`/`.pr-txt`, `.ar-list-item`,
  `.ar-title`, `.ar-quartile`, `.ar-year`, `.ar-cited`, `.subject-list`.
- **Scraping gagal** → JSON lama tidak ditimpa, halaman tetap menampilkan data
  terakhir yang berhasil.
- **ID SINTA salah** → dilaporkan di akhir log (`N berhasil, M gagal`).

Uji lokal: jalankan `python3 -m http.server` di folder ini, lalu buka
`uji-departemen.html`, `uji-faridah.html`, atau `uji-widya-rosita.html`.

Kalau hanya data agregat yang perlu dibangun ulang (tanpa scraping):
`python3 scripts/agregat.py`
