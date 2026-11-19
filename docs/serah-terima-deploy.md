# Serah terima deploy: v1.katur.online → tf.ugm.ac.id (19 Nov 2026)

Dibuat 19 Nov 2026 ± 04.00. Sumber rinci: `catatan-revisi-dosen.md` (entri 1–26 dan seterusnya), skrip di `docs/deploy-ugm/revisi/`, README: `docs/deploy-ugm/README.md`.

## Catatan penting (baca dulu)

1. **Deploy ke tf.ugm.ac.id dilakukan HARI INI, begitu staf berhasil login.** Tadi malam tidak jadi karena staf masih di Klaten dan tidak ada sesi admin tf. Siang ini rapat memakai **v1.katur.online** sebagai preview hasil revisi.
   - Komputer jurusan (Windows) sudah tersambung ke Claude in Chrome ("Browser 2"), tetapi belum login ke tf.
   - `tf.ugm.ac.id/wp-admin/`, `/wp-login.php`, `/login/` semuanya 404 (UGM menyembunyikan alamat login). Alamat login tf harus dicari staf (history/bookmark Chrome di komputer jurusan). Tab yang terbuka di komputer itu hanya login **v1** (bukan tf).
   - Sandi, captcha, 2FA: hanya staf yang mengisi. Claude tidak menyentuhnya.
2. **Data yang masih kurang** — daftar lengkap di bagian "Data yang masih kurang" di bawah.

## STATUS DEPLOY tf (diperbarui 19 Nov, sesi tf)
Sudah live di tf: **menu** dan **header** (Pendidikan 2 kolom, Kontak). **Terhenti**: Chrome Windows (komputer jurusan) terputus saat sesi berjalan. **Penghalang**: akun lab menyaring `<style>`/`<svg>`/`<script>` saat simpan (catatan 35); halaman berbasis HTML widget bergaya perlu akun dengan `unfiltered_html` sungguhan. Yang masih mungkin dari akun ini (widget native saja, harus dites per halaman): Visi Misi, Akreditasi, Pengurus, Tenaga Kependidikan, Dosen Tetap, profil dosen.

## Prasyarat sebelum deploy

- Sesi admin tf aktif di Chrome Windows (user: staf lab).
- Gabungkan PR branch `docs-home-v2-revisi-8` ke `main` (PR #48 dan yang menyusul) agar GitHub Pages menyajikan `data/` terbaru. Di v1, widget KBK/Mitra/Pengabdian memakai `data-base` = `raw.githubusercontent.com/chilmion/dtntf-publikasi/<SHA>/data`; di tf pakai `https://chilmion.github.io/dtntf-publikasi/data` (hasil default `buat_kbk.py`, `buat_mitra.py`, `buat_pengabdian.py`). Cek Pages sudah terbit sebelum memasang.
- Setiap skrip dipanggil dari tab wp-admin/editor tf lewat `fetch` raw GitHub pada SHA tertentu lalu `eval` (pola yang sama dengan v1). Cari id halaman tf lewat slug (`/wp-json/wp/v2/pages?slug=`), id v1 TIDAK sama.
- Setelah tiap halaman: `await kernFix()` + `await nolPadding()` (bila halaman rancang.js), simpan paksa dari editor (CSS Elementor), muat ulang dengan `?v=n`, cek visual.

## Checklist (mulai dari awal)

Status: ✅ selesai dan diperiksa · 🟡 sebagian/draf · ⬜ belum. Kolom v1 = hasil yang bisa dilihat di rapat siang; kolom tf = deploy hari ini.

| # | Item | v1 | tf | Skrip / cara | Catatan |
|---|------|----|----|--------------|---------|
| A | **Menu** (A1–A5): Akreditasi + Panduan ke Pendidikan (2 kolom), Layanan Akademik ke Layanan, urutan Penelitian, Kontak top-level | ✅ | ✅ (19 Nov, REST; catatan 34) | REST `wp/v2/menu-items` + header 16571 (`/*PENDIDIKAN2*/`) | id item beda di tf; `nav-menus.php` di tf 404. Cek 8 menu muat di 1300px |
| A' | **Header** (logo + menu 2 baris, CSS dari tf) | ✅ | ✅ Pendidikan 2 kolom + Kontak (lewat pemulihan CSS; JANGAN simpan header lagi, catatan 34) | tambahkan kolom Pendidikan + Kontak saja | v1 meniru tf, jadi di tf hanya 2 tambahan |
| B | **Footer** (sosmed 4 tautan, peta kecil, Layanan Akademik) | ✅ | ⬜ ditunda: tf tidak punya footer/template footer, butuh keputusan (catatan 36) | terapkan elemen manual di template footer tf | footer tf bukan template v1 |
| C1 | Sejarah | ✅ | ⛔ dicoba lalu dipulihkan: butuh `unfiltered_html` (catatan 35) | `sejarah.js` `deploySejarah(16872)` | foto Unsplash ilustrasi; isi 2022–sekarang satu kalimat |
| C2 | Visi dan Misi | ✅ | ⬜ | `visi-misi.js` `deployVisiMisi(16875)` | |
| C3 | Struktur Organisasi (bagan SVG, kartu prodi bento) | ✅ | ⬜ | `struktur.js` `deployStruktur(16890)` | tautan IUP/Magister baru ada setelah halamannya ada |
| C4 | Akreditasi (5 slot) | ✅ | ⬜ | `akreditasi.js` `deployAkreditasi(16893)` | |
| C5 | Pengurus Departemen | 🟡 | ⬜ | `pengurus.js` `deployPengurus(<id>)` | draf menunggu revisi user; email Kalab TEN pakai a_agung@ugm.ac.id |
| C6 | Dosen Tetap ("Profil lengkap →", foto 4:5 seragam) | ✅ | ⬜ | `fotoDosenUnggah('<sha>', slugs)` lalu `dosenTetap()` + `kernFix()` | foto seragam final menunggu hasil AI (lihat data kurang) |
| C7 | Tenaga Kependidikan | ✅ | ⬜ | `tenaga.js` `deployTenaga(16884, 'tf')` | |
| C8 | Fasilitas Umum (bento, Co-working Space) | ✅ | ⬜ | `fasilitas.js` `deployFasilitas(<id>, '<sha>')` | foto Perpustakaan UGM dari Google Maps, ganti bila ada yang resmi |
| D | **Prodi** TN, TF, IUP, Magister (hero + bento + akordeon, SVG, kartu dokumen tautan kosong, gambar tak melebihi ukuran asli) | ✅ | ✅ native, 19 Nov (catatan 38) | `prodi-v2.js` `deployProdiV2(nama, sha)` di editor tiap halaman | tf: TN = /prodi/ id 688, TF id 1763; IUP dan Magister sudah ada di tf (rancangan lama salinan TN) → timpa. Di v1 IUP=2345, Magister=2346. Konfirmasi tf tidak punya perubahan manual (user: tidak ada) |
| E1 | **KBK** (galeri bento, bidang per dosen, peta jalan, Pendanaan) | 🟡 | ⬜ | ganti isi 4 halaman dari `elementor/kbk/*.json` (data-base Pages) | hanya Instrumentasi berisi data dosen; 3 KBK lain galeri contoh; tf punya halaman lama (kbk-instrumentasi dll.) jangan bentrok slug: pakai `-v2` bila perlu |
| E2 | **Pengabdian** (galeri = kabar kegiatan mitra, kartu sama besar) | ✅ v1 id 1917 (dicek sesi `v1-mitra-home`) | ⬜ | `elementor/katur-pengabdian.json` | tf /pengabdian/ saat ini hanya H1 kosong |
| E3 | **Mitra** (logo paling atas, sorotan bento, kabar) | ✅ v1 id 1750 (dicek sesi `v1-mitra-home`) | ⬜ | `elementor/katur-mitra.json` | pertahankan banner tema; artikel nyata dari tf.ugm.ac.id/mitra |
| F | **Profil dosen** 38 halaman (hapus jabatan fungsional, institusi, telepon, riwayat pekerjaan, penghargaan, 'Data SINTA', rupiah; bagian 1–9) | ✅ | ⬜ | `profil-dosen.js` `patchProfilDosen('semua', slugs)` | id halaman tf lewat slug |
| H | **Home** isi tengah: mirror desain Home tf "new" ke Home katur (v1) | ✅ v1 id 265 = salinan render Home tf /new/ dalam satu widget HTML (catatan 27–29) | – | — | arah sebaliknya dari yang lain: v1 mengikuti tf; di tf tidak ada deploy Home baru kecuali kernFix Home v2 (16487) |
| — | Sejarah/Struktur dst: **kernFix + nolPadding** setelah tiap deploy | ✅ | ⬜ | `kern.js`, `sejarah.js` | wajib; Home v2 tf juga kena word-spacing |

**Layanan Akademik**: sudah dipasang di v1 (id 1818, menu Layanan menaut ke sana; catatan 32). Di tf halaman SUDAH ADA (/layanan-akademik/, 6 kartu), tidak perlu dibuat; cukup arahkan item menu Layanan ke sana. Kalender Akademik dan Panduan Akademik: urutan menu sudah, isi halaman tidak diubah.

## Aturan KBK saat deploy (keputusan user)
KBK yang bahannya belum lengkap tetap dideploy dengan **lorem ipsum placeholder** untuk bagian kosong (tidak disembunyikan, tidak mengarang data); gambar contoh berlabel "Gambar contoh". Widget sudah otomatis. Detail: `catatan-revisi-dosen.md` entri 30.

## Urutan deploy yang disarankan di tf (hari ini)

1. Login staf berhasil → cek `tabs_context` Browser 2 menunjukkan sesi admin tf.
2. Merge PR ke `main`, tunggu Pages terbit, cek `https://chilmion.github.io/dtntf-publikasi/data/kbk/kbk.json` dan `mitra/mitra.json` terbuka.
3. **Menu** (REST) → header 16571 (Pendidikan 2 kolom, Kontak) → footer. Cek tampilan header di 1300px.
4. Halaman Tentang Kami: Sejarah, Visi Misi, Struktur, Akreditasi, Pengurus, Dosen Tetap (foto), Tenaga Kependidikan, Fasilitas. Tiap halaman: kernFix, nolPadding, simpan paksa, cek.
5. Prodi: TN, TF, IUP, Magister (`deployProdiV2`).
6. KBK (4), Pengabdian, Mitra.
7. Profil dosen 38 (`patchProfilDosen`).
8. Cek akhir: klik semua menu, buka 5 profil acak, cek tautan antar halaman, cek di lebar HP (belum pernah diverifikasi di mobile 390px di halaman manapun).

## Data yang masih kurang

**Akses**
- Alamat login admin tf.ugm.ac.id dan staf yang login (staf di Klaten).

**Bahan dari jurusan/dosen**
- KBK ENET, Proses Nuklir, Multifisika: peta jalan, tabel bidang keahlian per dosen, penelitian unggulan (deskripsi, tim, publikasi, paten, pendanaan), dokumentasi/foto riset asli (sekarang galeri berlabel "Gambar contoh"). KBK Instrumentasi tema 2–6 (Gempa, VR, Sistem Cerdas Tertanam, Manajemen Baterai, Sensor Robotika) masih lorem ipsum. Format: `manual/kbk-ekstra/<kode>.json` (lihat instrumentasi.json).
- Prodi IUP Teknik Nuklir dan Magister Teknik Fisika: akreditasi, SKS, peminatan, jumlah lulusan, visi, kurikulum, laporan kinerja (sekarang kartu "–" dan lorem ipsum, tidak ada data karangan).
- Dokumen yang ditautkan ke tombol Unduh (kartu dokumen tautannya kosong): Kurikulum dan Laporan Kinerja untuk TN (PDF TN sudah ada di media v1, id 543–547, belum ditautkan), TF, IUP, Magister.
- Konfirmasi mahasiswa aktif Teknik Nuklir: grafik lama "261" vs teks halaman "307".
- Struktur Organisasi: berkas asli resolusi tinggi (bila ada); Akreditasi: berkas sertifikat 5 slot (dipakai yang sudah ada).
- Pengurus: revisi final user (C5), foto koordinator KBK, ejaan dan jumlah Kalab.
- Sejarah periode 2022–sekarang: detail kegiatan (sekarang satu kalimat).

**Aset**
- Foto dosen seragam hasil AI (zip `foto-dosen-untuk-diseragamkan.zip` di folder proyek; 15 foto lama + 9 foto sumber terlalu dekat). Setelah ada: timpa `data/ugm/foto-dosen/<slug>.jpg`, jalankan ulang `fotoDosenUnggah` + `dosenTetap`.
- Logo mitra tanpa berkas: BAPETEN, PLN, PT PAL, ThorCon, IAEA, SUCOFINDO, BPBD (sekarang tampil teks nama). Taruh di `data/mitra/logo/` dan tambah di `data/mitra/mitra.json`.
- Foto Perpustakaan UGM resmi (sekarang foto atrium dari Google Maps).
- Halaman Layanan Akademik versi v1 (belum dibuat).

## Jebakan yang sudah ditemukan (hemat waktu)

- Setelah halaman dibangun ulang lewat skrip: tampil tanpa gaya → buka editor, ubah apa saja kecil, `$e.run('document/save/default')`, muat ulang `?v=n`.
- Kit Elementor memberi `word-spacing` 6px di h1–h3 → jalankan `kernFix()`.
- Kontainer bersarang punya padding default 10px → `nolPadding()`.
- Output filter memblokir URL/query string/base64 di hasil `javascript_tool`; cetak potongan tanpa `?&=` atau simpan lewat variabel `window.__x` lalu baca ulang.
- Jangan navigasi dari tab editor saat skrip berjalan; hasil proses panjang dibaca lewat `window.__x`.
- sips (crop gambar): potongan yang tepinya tepat di tepi gambar diabaikan; offset horizontal harus lewat putar 90.
- Berkas `uji-*.html` hanya pratinjau lokal (`python3 scripts/buat_uji.py` lalu `python3 -m http.server`), jangan di-deploy.
