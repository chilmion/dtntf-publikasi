# Deploy ke web jurusan (tf.ugm.ac.id) — catatan kerja

Status per 10 Nov 2026. Tujuan: pasang desain v1.katur.online sebagai halaman v2 di tf.ugm.ac.id, lalu tukar menu/beranda setelah disetujui user.
Snapshot v1 lengkap ada di repo privat `chilmion/dtntf-wp-snapshot` (WXR, halaman, templat, screenshot).

## Aturan (WAJIB)
- Chrome yang dipakai: Claude in Chrome di komputer Windows jurusan, sudah login admin tf.ugm.ac.id (user yang login; jangan menyentuh sandi/captcha/2FA).
- DILARANG tanpa ACC eksplisit user di chat: menerbitkan halaman (status publish), mengubah menu/header/footer/kit/plugin, mengganti halaman depan, menimpa halaman yang sudah ada, membersihkan cache global.
- Halaman baru dibuat sebagai `draft` atau `private`. Home v2 (id 16487, slug `new`) SUDAH diterbitkan atas izin user. Pilot Andang (id 16511) `private`.
- Jangan timpa slug yang sudah dipakai UGM. Bentrok: kbk, kbk-instrumentasi, kbk-multifisika, kbk-proses-nuklir, kbk-energi-nuklir-dan-energi-terbarukan, pengurus-departemen, publikasi, kalender-akademik, kontak, laboratorium, sejarah, tenaga-kependidikan, visi-dan-misi → pakai akhiran `-v2` (keputusan akhir ada pada user).
- Tidak bentrok: 38 slug dosen, daftar-dosen-departemen-teknik-nuklir-dan-teknik-fisika-ft-ugm, kbk-enet, pengabdian, prodi, prodi-s1-teknik-fisika.
- Server UGM kadang menampilkan "Bad Gateway" sesaat setelah menyimpan; tunggu 10 detik lalu muat ulang.

## Temuan teknis penting
1. Server UGM membuang tag `<script>`, `<style>`, komentar HTML dari widget HTML Elementor, juga dari Elementor Pro Custom Code. Jangan memasang widget apa adanya.
2. Yang lolos: Custom CSS Elementor Pro (pengaturan halaman/widget) dan kotak **Custom JS Essential Addons** (`eael_custom_js` di pengaturan halaman), TETAPI JS di sana di-escape HTML: dilarang memakai karakter `& < > "`. Solusi: kotak itu hanya berisi satu baris pemuat (lihat `scripts/buat_aset_ugm.py`, fungsi `pemuat`) yang memuat `data/ugm/<widget>.css` dan `.js` dari GitHub Pages. Aset dibuat dengan `python3 scripts/buat_aset_ugm.py` (CSS memuat dasar warna/font v1 + @import Google Fonts; token `--e-global-*` diganti nilai literal).
3. Tambahkan `?v=YYYYMMDDn` pada URL aset di pemuat saat aset diubah (cache GitHub Pages 10 menit).
4. Kit global UGM beda dengan v1: warna/tipografi `__globals__` di templat HARUS diselesaikan menjadi nilai literal. Warna: primary #161616, secondary #414142, text #636363, accent #E3E3E3, Brand Main #073C64, Darker #1A2C43, Lighter #003D79, Subtle/lime #C8E86D, border #CAC0BE, bg #F5F5F5, putih #FFFFFF. Heading tanpa warna harus diberi #161616 (kalau tidak, tema UGM memberi biru muda #6EC1E4). Font: Plus Jakarta Sans (judul), Barlow (teks), Mulish (kit body).
5. Mencocokkan gaya persis: ukur gaya v1 dengan Playwright di Mac (v1.katur.online diblokir dari jaringan kampus), lalu terapkan per elemen berdasarkan teks (lihat riwayat Home v2). Hasil Home v2: 93 elemen, semua font/warna sesuai palet.
6. Widget Gum (`gum_posts_list`) tidak ada di UGM; diganti widget ElementsKit blog posts atau HTML sendiri (tanpa script).
7. Gambar: unggah ke Media UGM lewat REST `POST /wp-json/wp/v2/media` (sumber: GitHub Pages `data/…`, CORS terbuka), lalu ganti URL dan `id` di data Elementor.
8. Halaman Elementor dibuat: REST `POST /wp-json/wp/v2/pages` (draft) → buka editor `post.php?post=ID&action=elementor` → `elementor_ajax` action `save_builder` (nonce dari `elementorCommon.ajax.requestConstants._nonce`), settings: `template: elementor_header_footer`, `eael_custom_js: <pemuat>`, `custom_css: ''`. Muat ulang halaman dua kali setelah simpan (CSS dibangun di permintaan kedua).
9. Template halaman `elementor_header_footer` menyembunyikan judul/penulis bawaan tema UGM.
10. Menu: UGM memakai menu tema (Beranda, Profil, Program Studi, Riset & PPM, Akademik, Kemahasiswaan, Umum). Menu v2 belum dibuat. Opsi: templat Header Elementor Pro (Theme Builder) dengan kondisi hanya untuk halaman v2 + menu v2 terpisah; butuh ACC user.

## Pembaruan 10 Nov 2026 (malam)
- Header v2: templat Theme Builder id 16571 "Header Home v2 (DTNTF)", TERBIT; kondisi Singular > Laman by author > akun lab-komputasidtntf.ft (user id 742). Header v2 + Menu v2 hanya tampil di halaman buatan akun ini. Beranda & halaman UGM lain tidak terpengaruh. Nonaktifkan: draf-kan templat itu.
- Menu v2: menu WP id 326, slug menu-v2, 39 item, belum dipasang ke lokasi menu. Tautan ke halaman yang belum ada akan 404.
- FATAL, JANGAN DIULANG: jangan membuat templat lewat POST ke edit.php?action=elementor_new_post (membuat POS berita biasa; sempat terbit di daftar berita). Templat Theme Builder hanya lewat tombol resmi di UI. Dialog kondisi tampil: set select lewat JS (value + dispatch input & change); untuk author tambahkan Option value=742 ke select ke-4.
- Setelah mengubah/menghapus pos, bersihkan cache halaman terkait (tombol Delete Cache di bilah admin) dan simpan ulang halaman v2 yang memuat daftar berita.
- Urutan deploy per halaman (WAJIB): deployHalaman -> REST status 'private' -> deployHalaman lagi. Simpanan pertama saja membuat Custom JS Essential Addons tidak keluar (widget tetap "Memuat profil…").
- Muat ulang halaman dua kali setelah simpan (CSS dibangun di permintaan kedua).
- Peta aset per templat: data/ugm/peta.json (dibuat scripts/buat_aset_ugm.py).
- Sudah ada di UGM: Home v2 16487 (publish), Andang 16511 (publish), Agus Arif 16574 (private, berfungsi). Profil lain dijalankan lewat loop di tab Chrome jurusan (sesi lokal); cek daftar halaman author 742 untuk status terbaru.

## ID di web UGM
Home v2 = 16487 (publish, slug new). Andang Widi Harto = 16511 (private). Media Home v2: 23 gambar. Dosen & KBK & prodi: belum dipasang.

## Sumber templat (repo ini)
`elementor/profil/<slug>.json` (38), `elementor/katur-daftar-dosen.json`, `elementor/kbk/*.json`, `elementor/katur-kbk-induk.json`, `elementor/katur-pengurus-departemen.json`, `elementor/katur-pengabdian.json`, `elementor/prodi-teknik-nuklir.json`, `elementor/prodi-teknik-fisika.json`. Widget: `widget/katur-*.html`. Data JSON & gambar: GitHub Pages `https://chilmion.github.io/dtntf-publikasi/data`.

## Berkas sementara di repo publik (hapus setelah selesai)
`data/staging-home/*` (gambar + home.json untuk Home v2).
