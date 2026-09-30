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
- `.github/workflows/update.yml` — workflow_dispatch (input `dosen`, default `faridah,widya-rosita`), cron Senin 03:00 WIB, push ke `dosen.csv`/`scripts/**`/`widget/**`; commit `data/` lalu deploy Pages.
- `scripts/manual.py` — gabung `manual/luaran.xlsx` (satu berkas Excel jurusan; templat `manual/templat-luaran.xlsx`, dibuat `scripts/buat_templat.py`) ke `data/<slug>.json` (entri bertanda `manual:true`, idempoten), lalu agregat. Dipanggil di `update.yml` setelah build dan di `manual.yml` (cepat, dipicu push `manual/luaran.xlsx`).
- `scripts/unggah_manual.py` — mini app lokal (127.0.0.1:8787) untuk unggah xlsx via GitHub API dengan PAT tersimpan di `~/.dtntf-publikasi-token`. JANGAN pernah menaruh token di browser/halaman publik.
- `scripts/buat_elementor.py` — buat `elementor/*.json` (templat Container siap impor) dari `widget/*.html`; jalankan ulang tiap widget berubah.
- `jalankan.sh` — cadangan: cron di mesin lokal ber-IP Indonesia.
- `uji-*.html` — halaman uji lokal (`python3 -m http.server`).

## Fakta penting tentang SINTA (jangan lupa)
- Pengunjung tanpa login HANYA melihat 10 entri terbaru per tab. "View more" -> /logins. `?page=N` tidak membantu. JANGAN otomatisasi login.
- Tabel metrik `.stat-table` (Article, Citation, Cited Doc, H-Index, i10, G-Index untuk Scopus/GScholar/WOS) dan kartu skor `.pr-num`/`.pr-txt` lengkap dan akurat seumur karier.
- Donat kuartil, radar riset, dan artikel/tahun digambar echarts via JS. `scripts/grafik.py` mencoba mengambilnya dari skrip inline (pola pie/radar/line umum) → `grafik` di JSON dosen; widget `data-tampil=grafik`. FORMAT ASLI BELUM TERVERIFIKASI: bila kosong, `build.py` menulis `diagnostik-grafik.txt` — minta user mengirim berkas itu lalu cocokkan pola di grafik.py.
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
4. Jalankan beta Actions untuk Faridah (SINTA 6010146) & Widya Rosita (6016573); data widya-rosita.json saat ini hanya salinan uji. Bila 403/429 dari IP GitHub -> pindah ke `jalankan.sh` di mesin lokal.
5. Setelah beta lolos: kosongkan default `dosen` di workflow agar 38 dosen ikut.
6. (Opsional) cari sumber data donat kuartil/radar SINTA.
7. (Opsional) isi `jabatan` di `dosen.csv`.
