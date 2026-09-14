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

## Memverifikasi parser (penting untuk run pertama)

Tab Scopus sudah diuji terhadap HTML asli. Tab **iprs, services, books, dan
researches** belum — strukturnya kemungkinan besar sama (`.ar-list-item`),
tapi belum terverifikasi. Jalankan diagnostik ini dulu:

```bash
python3 scripts/build.py --periksa 6010146
```

Untuk tiap tab, ia melaporkan berapa blok ada di HTML versus berapa yang
terbaca parser, plus satu contoh entri. Kalau ada baris
`!! ada blok di HTML tapi parser tidak membacanya`, simpan halaman itu
(Save Page As) dan kirim — parser tinggal disesuaikan.

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
