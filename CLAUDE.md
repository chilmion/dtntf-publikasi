# CLAUDE.md — Publikasi DTNTF UGM

Sistem auto-update publikasi untuk situs Departemen Teknik Nuklir dan Teknik Fisika (DTNTF) UGM.
WordPress + Elementor, TIDAK boleh menambah plugin WP. Semua tampilan = widget HTML Elementor.

## Arsitektur
scraper Python (stdlib saja) -> JSON per dosen -> GitHub Pages -> widget HTML fetch JSON dari browser.

- `dosen.csv` — 38 dosen (slug, nama, gelar, jabatan, email, sinta_id, scopus_id, scholar_id, foto_url). `jabatan` sengaja kosong (diisi manual).
- `scripts/build.py` — scrape SINTA (6 tab: scopus, garuda, books, iprs, services, researches), tulis `data/<slug>.json`, lalu panggil `agregat.py`.
- `scripts/agregat.py` — gabung semua dosen jadi `data/agregat/ringkas.json` + `<tahun>.json`; paper multi-penulis digabung (kunci: EID Scopus -> DOI -> judul ternormalisasi, judul <25 karakter tidak digabung).
- `widget/publikasi.html` — profil dosen (`.dtntf-pub`), atribut `data-base`, `data-slug`, `data-tampil="skor,grafik,metrik,publikasi"`. Bagian foto/nama/bio dibuat manual di Elementor, hanya bagian statistik + daftar ini yang otomatis.
- `widget/departemen.html` — halaman departemen (`.dtntf-dep`), atribut `data-base`, `data-profil` (sudah sederhana: tanpa filter/pencarian).
- `.github/workflows/update.yml` — TIDAK scrape (IP GitHub diblokir SINTA; keputusan user 30 Sep 2026: scrape hanya lokal). Hanya `manual.py` (data manual + agregat) → commit `data/` → deploy Pages; dipicu push ke `dosen.csv`/`scripts/**`/`widget/**`/`manual/dosen-info.csv` atau manual. Scrape: `scripts/perbarui_lokal.py` (klik `Perbarui Data SINTA.command`), yang juga memicu `manual.yml` untuk menerbitkan.
- `scripts/manual.py` — gabung `manual/luaran.xlsx` (satu berkas Excel jurusan; templat `manual/templat-luaran.xlsx`, dibuat `scripts/buat_templat.py`) ke `data/<slug>.json` (entri bertanda `manual:true`, idempoten), lalu agregat. Dipanggil di `update.yml` setelah build dan di `manual.yml` (cepat, dipicu push `manual/luaran.xlsx`).
- `scripts/unggah_manual.py` — mini app lokal (127.0.0.1:8787) untuk unggah xlsx via GitHub API dengan PAT tersimpan di `~/.dtntf-publikasi-token`. JANGAN pernah menaruh token di browser/halaman publik.
- `scripts/buat_elementor.py` — buat `elementor/*.json` (templat Container siap impor) dari `widget/*.html`; jalankan ulang tiap widget berubah.
- `widget/katur-*.html` — widget bergaya v1.katur.online (daftar dosen, statistik bento + daftar filter, profil: kartu/info/data). Token warna/tipografi diambil dari kit Elementor katur (`--e-global-*`, fallback literal). Templat: `elementor/katur-*.json` (dibuat `scripts/buat_elementor.py`). `manual/dosen-info.csv` = pendidikan/bidang ilmu/riset/homepage per dosen (dari halaman Dosen Tetap lama); `agregat.py` menurunkan `kelompok` (Teknik Nuklir/Fisika) dan memasukkan semua dosen di dosen.csv ke `ringkas.json`.
- `jalankan.sh` — cadangan: cron di mesin lokal ber-IP Indonesia.
- `uji-*.html` — halaman uji lokal (`python3 -m http.server`).

## Fakta penting tentang SINTA (jangan lupa)
- Pengunjung tanpa login HANYA melihat 10 entri terbaru per tab. "View more" -> /logins. `?page=N` tidak membantu. JANGAN otomatisasi login DENGAN KATA SANDI. Keputusan user (30 Sep 2026): boleh pakai COOKIE sesi yang user salin sendiri dari browser (`~/.dtntf-sinta-cookie` atau env `SINTA_COOKIE`; tidak pernah masuk repo/log). `build.py` memverifikasi cookie (?page=2 harus memuat entri baru) dan mengisi `batas_daftar.lengkap`; data lama dipertahankan bila hasil <50% dari sebelumnya.
- Tabel metrik `.stat-table` (Article, Citation, Cited Doc, H-Index, i10, G-Index untuk Scopus/GScholar/WOS) dan kartu skor `.pr-num`/`.pr-txt` lengkap dan akurat seumur karier.
- Donat kuartil, radar riset, dan artikel/tahun digambar echarts via JS. `scripts/grafik.py` mencoba mengambilnya dari skrip inline (pola pie/radar/line umum) → `grafik` di JSON dosen; widget `data-tampil=grafik`. Format asli TERVERIFIKASI (30 Sep 2026): pie `quartile-pie`, radar `research-radar`, line `scopus-chart-articles`; konfigurasi memuat `new echarts.graphic.LinearGradient(...)` dan `function(){}` yang dibuang `_buang_panggilan`. Bila ada yang kosong, `build.py` menulis `diagnostik-grafik.txt`.
- Slot `.ar-quartile` dipakai ulang tiap tab: Scopus "Q2 as Journal"; Garuda "Accred : Sinta 3"; Buku "ISBN : ..."; Paten jenis; PPM/Penelitian "Rp. ...". `.ar-cited` = sitasi hanya di Scopus. Lihat `LABEL_FIELD` di build.py.
- Tab Garuda mencocokkan berdasarkan NAMA -> dosen bernama tunggal kemasukan paper orang lain. Keputusan user: tetap dipakai, widget beri label "via indeks Garuda".
- Statistik turunan dari daftar 10 entri itu bias (tren tahunan, sebaran kuartil, venue) -> jangan ditampilkan selama `batas_daftar.lengkap` false.

## Konsep tampilan terbaru (keputusan user)
Tampilkan statistik LENGKAP dari SINTA (kartu skor + bar metrik), lalu daftar sederhana luaran terbaru per sumber. TANPA pencarian/filter/tombol muat-lebih. Widget profil sudah begini; widget departemen BELUM (masih ada filter & pencarian).

## Merek (Brand Guideline DTNTF 2026)
UGM Navy #073C64, Dark Navy #1A2C43, Cinder #0B0B16, White Lilac #F7F7FB, Mute Lime #C8E86D. Font Plus Jakarta Sans. Semua CSS di-scope ke `.dtntf-pub` / `.dtntf-dep`, token di blok `:root` (`--dp-...`).

## Aturan kerja
- Python stdlib saja; tidak ada dependensi baru. Widget = satu file HTML mandiri (CSS+JS inline), tanpa library eksternal.
- Scraping sopan: jeda 2.5–5 dtk, retry/backoff untuk 403/429. Scopus situs tidak boleh di-scrape.
- Scopus API: kode sudah ada tapi tidur (`SCOPUS_API_KEY` secret + kolom `scopus_id`). Ditunda sampai user bicara dengan admin IT UGM.
- Kalau scrape gagal, JSON lama tidak boleh ditimpa.
- Jangan commit `data/` dengan tangan bila Actions yang menghasilkannya, kecuali untuk data uji.
- Sesi cloud memakai IP luar negeri: tidak bisa menguji SINTA live. Uji dengan data di `data/` dan `uji-*.html`, atau minta user menjalankan workflow Actions.
- Bahasa: Indonesia, singkat. User pemula GitHub — beri langkah konkret, jelaskan istilah.
- Buat branch + PR; jangan langsung ke main.

## Status & TODO
1. Render & cek `widget/publikasi.html` (belum pernah dilihat hasil renderingnya) — pakai playwright/chromium, screenshot `uji-publikasi.html`.
2. Sederhanakan `widget/departemen.html` sejalan dengan konsep baru (statistik departemen + daftar per tahun sederhana; hapus filter/pencarian).
3. Perbarui README (`data-tampil` sekarang `skor,metrik,publikasi`, bukan `statistik,tren,publikasi`) dan panduan setup untuk pemula.
4. (SELESAI) Scrape dipindah ke lokal. Tinggal user menjalankan `semua` untuk 38 dosen dan mengimpor templat Elementor.
5. (SELESAI) Workflow GitHub tidak lagi scrape.
6. (Opsional) cari sumber data donat kuartil/radar SINTA.
7. (Opsional) isi `jabatan` di `dosen.csv`.
