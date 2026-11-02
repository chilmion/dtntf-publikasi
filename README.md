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
   *Read and write permissions* (agar workflow bisa menyimpan hasil agregat).
   (*Actions* = mesin gratis GitHub yang menjalankan script otomatis;
   *Pages* = layanan GitHub yang menyajikan berkas repo sebagai situs.)
4. Ambil data SINTA **dari komputermu** (bukan dari GitHub): klik
   `Perbarui Data SINTA.command` (uji 2 dosen dulu, lalu ketik `semua`). GitHub
   tidak scrape sama sekali — server GitHub diblokir SINTA.
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
data-profil="/{slug}/"
```

`data-profil` membuat nama dosen di tiap entri jadi tautan ke halaman
profilnya. Kosongkan kalau halaman profil belum ada.

## Siapa mengerjakan apa

| Tugas | Di mana |
|---|---|
| Scrape SINTA (dan cookie login) | **Komputermu** (`Perbarui Data SINTA.command`, atau `jalankan.sh` + cron) |
| Pasang data manual, bangun agregat, terbitkan situs | **GitHub Actions** — otomatis saat `widget/`, `scripts/`, `dosen.csv`, `manual/dosen-info.csv` berubah, atau saat `manual/luaran.xlsx` diunggah |

Workflow mingguan yang dulu mencoba scrape dari GitHub sudah dihapus karena pasti
gagal (HTTP 403). Kalau mau jadwal rutin, pakai cron di komputer lokal dengan
`jalankan.sh`.

## Templat Elementor bergaya v1.katur.online

Tiga templat siap impor (Templates → Saved Templates → Import Templates), memakai Container:

| Berkas | Isi |
|---|---|
| `elementor/katur-daftar-dosen.json` | Daftar dosen: kartu foto, saring Teknik Nuklir/Teknik Fisika, cari nama/bidang riset. Tautan ke profil lewat `data-profil="/{slug}/"`. |
| `elementor/katur-daftar-dosen.json` (bisa diedit) | Daftar dosen dengan **kartu yang bisa diedit**: tiap dosen = satu container berisi Image (foto), Heading (nama), widget HTML (kelompok, gelar, bidang ilmu, sitasi Scopus dari GitHub), dan tombol "Selengkapnya →" (isi tautan profil sendiri; bawaan `/<slug>/`). Ada bilah cari + filter. Dibuat `scripts/buat_daftar_dosen.py`. Versi serba-otomatis (satu widget) ada di `katur-daftar-dosen-otomatis.json`. |
| `elementor/katur-profil-dosen.json` | Profil dosen generik: kartu kiri (foto, kontak, tautan) + widget `katur-profil-cv.html` (susunan CV, lihat bagian *Profil dosen susunan CV*). Cukup isi `data-slug` **sekali** di widget kartu; widget CV mengikutinya. Satu halaman untuk semua dosen juga bisa: kosongkan `data-slug`, buka `/halaman/?d=faridah`. |
| `elementor/katur-statistik.json` | Statistik departemen bergaya bento (angka dari metrik SINTA), lalu daftar luaran yang bisa disaring per kategori/tahun/kata kunci. |

**38 templat profil siap impor (satu per dosen):** `elementor/profil/<slug>.json`, dibuat `python3 scripts/buat_profil_dosen.py`. Foto, nama, gelar, tautan, dan tombol SINTA berupa widget Elementor biasa (bisa diedit); selebihnya satu widget HTML `katur-profil-cv.html` yang sudah diisi `data-slug` dosen itu. Untuk impor massal ada `elementor/profil-38.zip` (JSON di akar ZIP, tanpa folder).

Foto dosen diambil dari halaman resmi <https://tf.ugm.ac.id/dosen-tetap/>: `python3 scripts/perbarui_foto.py` mencocokkan per ID SINTA/nama dan memperbarui kolom `foto_url` di `dosen.csv`, lalu jalankan ulang `buat_profil_dosen.py` dan `buat_daftar_dosen.py`.

## Profil dosen susunan CV

Widget `widget/katur-profil-cv.html` menyusun halaman profil mengikuti contoh CV, **tanpa Skor SINTA**:

1. Data diri (nama lengkap + gelar, jabatan fungsional, bidang kepakaran, institusi, email, telepon institusi)
2. Riwayat pendidikan · 3. Sertifikat kompetensi · 4. Riwayat pekerjaan · 5. Organisasi profesi · 6. Penghargaan
7. Pengalaman kerjasama dan penelitian (tabel No, Riset/Proyek, Tahun, Keterangan)
8. Kekayaan intelektual (HKI/paten) · 9. Publikasi (jurnal) · 10. Prosiding seminar · 11. Buku

Di bawahnya blok **Data SINTA** seperti sebelumnya, hanya tanpa Skor SINTA: Penelitian, Pengabdian, kartu h-index/artikel/sitasi Scopus & Google Scholar, grafik (kuartil, luaran riset, artikel per tahun), dan tabel metrik Scopus/Scholar/WOS (`data-tampil="statistik,grafik,metrik"`).

Bagian 1–7 diisi dari **`manual/profil-cv.xlsx`** (satu berkas Excel untuk semua dosen; templat kosong
`manual/templat-profil-cv.xlsx`, dibuat `python3 scripts/buat_templat_cv.py`). Satu lembar per bagian
(Identitas, Pendidikan, Sertifikat, Pekerjaan, Organisasi, Penghargaan, Kerjasama); kolom `dosen` dipilih dari
dropdown. Bagian 7 juga memuat Penelitian & Pengabdian dari SINTA. Bagian 8–11 otomatis dari SINTA
(dan `manual/luaran.xlsx`). `scripts/profil_cv.py` (dipanggil `scripts/manual.py`) menaruh hasilnya di
`data/<slug>.json` sebagai kunci `cv`. Nilai bawaan dari data yang sudah ada: pendidikan, bidang ilmu,
keanggotaan, dan penghargaan dari `manual/dosen-info.csv`; institusi dan telepon = departemen.

**Lorem ipsum = penanda data kosong.** Bagian yang belum ada datanya tidak disembunyikan; isinya teks
lorem ipsum berkelas `.kt-lorem` (kuning, bergaris putus-putus, atribut `data-lorem`). Setelah datanya diisi
dan `manual.py` dijalankan (otomatis lewat GitHub Actions saat berkas diunggah), teks itu diganti data asli.
Cari yang tersisa dengan mencari `kt-lorem` di inspektur browser.

**Privasi.** Tidak ada kolom alamat rumah, HP pribadi, tanggal lahir, jenis kelamin, NIP/NIDN. Jangan menambahnya.
Folder `referensi-lokal/` (contoh CV dan PPT) ada di `.gitignore` dan tidak boleh di-commit.

Cara memperbarui: isi `manual/profil-cv.xlsx` → di GitHub buka folder `manual/` → *Add file → Upload files*
(timpa berkas lama) → workflow *Perbarui data manual* jalan otomatis (±2 menit).

## Halaman KBK (Kelompok Bidang Keahlian)

Lima halaman: induk `/kbk/` (kartu semua KBK) + satu halaman per KBK: `/kbk-enet/`, `/kbk-proses-nuklir/`,
`/kbk-multifisika/`, `/kbk-instrumentasi/`. KBK **berbeda** dari kolom `kelompok` (Teknik Nuklir/Teknik Fisika);
satu dosen boleh ada di beberapa KBK.

| Berkas | Isi |
|---|---|
| `manual/kbk.xlsx` | Data semua KBK: lembar KBK, Kompetensi, Anggota, Tema, Riset, Publikasi (petunjuk di lembar *Petunjuk*; templat kosong `manual/templat-kbk.xlsx`) |
| `scripts/kbk.py` | `manual/kbk.xlsx` → `data/kbk/kbk.json` (statistik dihitung otomatis; dipanggil `manual.py`) |
| `widget/katur-kbk.html` | Satu halaman KBK (`data-kbk="enet"`): hero, statistik bento, kompetensi, anggota (kartu bergaya daftar dosen, menaut ke `/<slug>/`), tema penelitian |
| `widget/katur-kbk-induk.html` | Halaman induk |
| `elementor/katur-kbk-induk.json`, `elementor/kbk/<kode>.json` | Templat siap impor, dibuat `python3 scripts/buat_kbk.py` |

Bagian yang datanya belum ada (mis. seluruh isi Multifisika dan Instrumentasi) tampil sebagai lorem ipsum
(`.kt-lorem`) sampai lembar Excelnya diisi. Alamat halaman diatur di kolom `halaman` lembar KBK.

Gambar hero tiap KBK: `manual/kbk-gambar/<kode>.jpg` (enet, proses-nuklir, multifisika, instrumentasi); timpa berkas dengan gambar lebih tajam bila ada, `kbk.py` menyalinnya ke `data/kbk/`.

## Halaman Pengabdian

`widget/katur-pengabdian.html` + `elementor/katur-pengabdian.json` (dibuat `python3 scripts/buat_pengabdian.py`), alamat `/pengabdian/`
untuk menu *Riset & PPM → Pengabdian*. Seperti rekap publikasi tetapi hanya kategori *Pengabdian kepada Masyarakat* dari SINTA:
statistik bento, grafik kegiatan per tahun, dosen paling aktif, dan daftar kegiatan yang bisa disaring (tahun, dosen, kata kunci).

## Halaman Pengurus Departemen

`elementor/katur-pengurus-departemen.json` (`python3 scripts/buat_pengurus.py`), alamat `/pengurus-departemen/`. Kartu bergaya daftar
dosen (container Elementor yang bisa diedit: foto, jabatan, nama lengkap, email, tombol profil) dalam tiga kelompok: departemen &
program studi, kepala laboratorium, ketua KBK. Isi dari `manual/pengurus.csv` (kolom kelompok, jabatan, slug, nama_lengkap, email);
foto dari `dosen.csv` (foto resmi terbaru). Ubah periode di konstanta `PERIODE` skrip. Email lab Teknologi Energi Nuklir disalin dari
halaman lama (`sekdep-tntf.ft@ugm.ac.id`); cek apakah memang itu.

## Pratinjau lokal

```bash
python3 scripts/manual.py        # pasang data CV & KBK ke data/ (hanya untuk uji; hasil resmi dibuat GitHub Actions)
python3 scripts/buat_uji.py      # buat uji-daftar-dosen, uji-profil-*, uji-kbk-*
python3 -m http.server 8000      # buka http://localhost:8000/uji-daftar-dosen.html
```

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
