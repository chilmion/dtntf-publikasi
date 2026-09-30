# Publikasi DTNTF — auto-update dari SINTA

Dua halaman WordPress/Elementor yang mengisi dirinya sendiri dari SINTA,
tanpa plugin apa pun.

**1. Halaman departemen** (`/publikasi/`) — `widget/departemen.html`
Statistik departemen (jumlah dosen, sitasi Scopus, h-index tertinggi), tabel
dosen, lalu daftar luaran terbaru per tahun yang dikelompokkan per jenis
(Jurnal Internasional, Prosiding, Jurnal Nasional, Buku, Paten & HKI,
Penelitian, Pengabdian). Sengaja sederhana: tanpa pencarian dan filter.

**2. Halaman profil dosen** — `widget/publikasi.html`
Skor SINTA, metrik sitasi (Scopus, Google Scholar, WOS), dan daftar luaran
terbaru satu dosen, dikunci lewat `data-slug`.
Bagian foto/nama/bio di atasnya kamu desain sendiri di Elementor.

```
┌──────────────────────────────────┐
│  Profil dosen — desain manual    │  ← Elementor
│  foto · nama · gelar · bio       │
├──────────────────────────────────┤
│  widget/publikasi.html           │  ← auto-update
│  skor · metrik · daftar luaran   │
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
data/agregat/ringkas.json  daftar dosen + statistik, indeks tahun
data/agregat/2026.json     entri tahun itu (sudah digabung)
data/agregat/2025.json     …dst
manual/luaran.xlsx         input manual dari jurusan (opsional)
```

Dipecah per tahun supaya tiap berkas tetap kecil. Widget departemen mengunduh
`ringkas.json` lalu semua berkas tahun sekaligus.

## Warna & font

Mengikuti Brand Guideline DTNTF 2026, jadi tidak perlu kirim HTML tema:

| Token | Nilai | Dipakai untuk |
|---|---|---|
| UGM Navy | `#073C64` | angka statistik, kartu skor, batang metrik, tautan, badge kuartil |
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
   (*Actions* = mesin gratis GitHub yang menjalankan script otomatis;
   *Pages* = layanan GitHub yang menyajikan berkas repo sebagai situs.)
4. Tab **Actions → Perbarui data publikasi → Run workflow**. Isian `dosen`
   sudah default `faridah,widya-rosita` — inilah beta-nya.
5. Cek hasil: `https://<akun>.github.io/<repo>/data/faridah.json`
6. **Halaman profil dosen** — widget **HTML** di bawah blok profil, tempel
   `widget/publikasi.html`, lalu ubah:

```html
data-base="https://<akun>.github.io/<repo>/data"
data-slug="faridah"
data-tampil="skor,grafik,metrik,publikasi"
```

`data-tampil` menentukan bagian mana yang muncul, dipisah koma:

- `skor` — kartu skor SINTA;
- `grafik` — ringkasan riset dari SINTA: donat kuartil artikel, radar luaran riset, artikel per tahun (butuh data grafik, lihat di bawah);
- `metrik` — bar artikel, sitasi, h-index, dst. untuk Scopus/GScholar/WOS;
- `publikasi` — daftar luaran terbaru per kategori.

Hapus salah satu kalau tidak mau ditampilkan, misalnya
`data-tampil="publikasi"` untuk daftar saja.

**Data grafik.** SINTA menggambar grafik Summary lewat JavaScript, dan `scripts/grafik.py` mengambil datanya dari skrip di halaman profil. Format aslinya belum terverifikasi; kalau tidak ditemukan, `build.py` menulis `diagnostik-grafik.txt` (potongan skrip mentah) dan blok grafik disembunyikan otomatis sampai polanya dicocokkan.

7. **Halaman departemen** (`/publikasi/`) — widget **HTML**, tempel
   `widget/departemen.html`, lalu ubah:

```html
data-base="https://<akun>.github.io/<repo>/data"
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

## Input manual (luaran yang tidak ada di SINTA)

Jurusan mengisi **satu berkas Excel** untuk seluruh dosen; isinya ditambahkan
ke data SINTA.

1. Pakai templat `manual/templat-luaran.xlsx`. Isi sheet **Luaran**, satu baris
   satu luaran. Wajib: `dosen`, `jenis`, `judul`, `tahun`; kolom lain opsional.
   Nama dosen dipilih dari dropdown (beberapa dosen: pisahkan dengan `;`).
   Sheet *Petunjuk* menjelaskan tiap kolom. Jangan ganti nama sheet/kolom.
2. Unggah sebagai `manual/luaran.xlsx` — lewat mini app di bawah (tanpa login
   GitHub) atau lewat GitHub: *Add file → Upload files* di folder `manual/`.
3. Workflow **Perbarui data manual** jalan otomatis (±1–2 menit, tanpa scrape
   SINTA) dan menerbitkan ulang. Workflow mingguan juga memasangnya lagi.

Luaran yang judulnya sudah ada di SINTA untuk dosen yang sama dilewati. Baris
yang salah (jenis/tahun tidak valid, dosen tak dikenal) dilewati dan
dilaporkan di log.

### Mini app unggah (tanpa login GitHub)

```
python3 scripts/unggah_manual.py
```

Buka halaman lokal `http://127.0.0.1:8787` (hanya dari komputermu). Pilih
berkas → **Periksa** → **Unggah & perbarui**. Perlu sekali saja membuat token:

1. GitHub → foto profil → *Settings → Developer settings → Personal access
   tokens → Fine-grained tokens → Generate new token*.
2. *Repository access:* Only select repositories → `dtntf-publikasi`.
3. *Permissions:* **Contents = Read and write**, **Actions = Read and write**.
4. Salin token, tempel di halaman mini app. Tersimpan di
   `~/.dtntf-publikasi-token` (bukan di repo). Kalau bocor, hapus token itu di
   GitHub. Token punya masa berlaku; buat baru bila habis.

Butuh Python 3 (Mac: jalankan `python3` di Terminal, macOS akan menawarkan
pemasangan bila belum ada) dan folder repo ini (Code → Download ZIP).

## Batas 10 entri dari SINTA

SINTA hanya menampilkan **10 entri terbaru per kategori** bagi pengunjung tanpa
login — tombol "View more" di halaman profil mengarah ke `/logins`. Tidak ada
parameter URL yang bisa menembusnya; `?page=2` diabaikan.

Karena itu tampilan dibagi dua dengan jujur:

- **Statistik lengkap** (kartu skor, tabel metrik) datang dari tabel SINTA
  sendiri dan akurat seumur karier.
- **Daftar luaran** hanya 10 terbaru per kategori. Widget memberi catatan
  singkat tentang hal ini.

Angka yang dihitung dari daftar itu (tren per tahun, sebaran kuartil, jurnal
tersering) bias ke tahun terbaru, jadi **tidak ditampilkan**.

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

`scripts/build.py` masih mencoba `?page=2`, `?page=3`, … dan berhenti setelah 3
halaman berturut-turut tanpa judul baru. Untuk pengunjung tanpa login SINTA
mengabaikan parameter itu, jadi hasilnya tetap 10 entri per tab. Log memuat
peringatan `terkumpul X, menurut SINTA ada Y` bila jumlahnya kurang; itu wajar
selama batas 10 entri berlaku.

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
`http://localhost:8000/uji-publikasi.html` (profil, data `data/faridah.json`)
atau `http://localhost:8000/uji-departemen.html` (data `data/agregat/`).
`uji-faridah.html` dan `uji-widya-rosita.html` adalah widget profil untuk
masing-masing dosen.

Kalau hanya data agregat yang perlu dibangun ulang (tanpa scraping):
`python3 scripts/agregat.py`
