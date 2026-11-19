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

- Slug dosen yang dipakai Media UGM (halaman lampiran) sehingga WordPress menambah -2: `ferdiansjah` dan `nopriadi`. Profil dipasang sebagai `ferdiansjah-v2` (id 16634) dan `nopriadi-v2` (id 16692). Pada daftar dosen, tautan kartu diganti lewat parameter `ganti` ('"/ferdiansjah/"' -> '"/ferdiansjah-v2/"').
- Server UGM memberi 502/500 bila halaman diminta cepat berturut-turut: beri jeda >= 4 detik antar permintaan, coba ulang bila 5xx.
- Status 10 Nov malam: 38 profil dosen sudah ada (private; Andang publish). Sisa: daftar dosen, KBK, pengurus, pengabdian, prodi, 6 halaman v2, 9 halaman menu.

## Status 11 Nov 2026 (dini hari)
- 68 halaman buatan akun 742 sudah TERBIT (tanpa masuk menu): 38 profil dosen, daftar dosen, kbk-v2 + 4 KBK, pengurus-departemen-v2, pengabdian, 18 halaman snapshot v1 (sejarah-v2, visi-dan-misi-v2, kontak-v2, laboratorium-v2, tenaga-kependidikan-v3 [v2 dipakai halaman UGM id 14292], kalender-akademik-v2, struktur-organisasi, akreditasi, layanan-akademik, publikasi-dan-riset, fasilitas-umum, galeri, mitra, kemahasiswaan, panduan-akademik-prodi-s1-teknik-nuklir, publikasi-v2, prodi, prodi-s1-teknik-fisika), iup-teknik-nuklir dan program-studi-magister-teknik-fisika (lorem), kategori-prestasi (contoh arsip kategori), Home v2 (new).
- Halaman snapshot dipasang dengan aturan (globals->literal, heading #161616), BELUM diukur per elemen terhadap v1 seperti Home v2; cek font/warna saat QC. Widget html di kalender-akademik-v2 dan publikasi-dan-riset kehilangan script/style (kemungkinan rusak). MetForm di kontak-v2: plugin MetForm di UGM terpasang tapi NONAKTIF.
- Fungsi: docs/deploy-ugm/deploy-halaman.js (widget kita) dan docs/deploy-ugm/deploy-v2.js (halaman snapshot dari data/staging-v2; dibuat oleh dtntf-wp-snapshot/scripts/siapkan_halaman_v2.py). Gambar halaman snapshot sudah diunggah (peta nama->id di localStorage '__peta2' tab Chrome; bila hilang, unggah ulang dari data/staging-v2/img).
- Menu v2 sengaja TIDAK diubah (user: perlu redesain). Item kategori artikel akan ditautkan ke arsip kategori yang didesain ulang (contoh: kategori-prestasi).
- Berkas sementara di repo publik yang harus dihapus setelah QC: data/staging-home/, data/staging-v2/.

## Revisi QC 16 Nov 2026
- Sumber: dua Google Docs QC tim internal + masukan dosen (spasi, ukuran font, kontras). Skala: H1 56/44/32, H2 40/34/28, isi 17/16, kartu judul 22/18.
- Skrip: docs/deploy-ugm/revisi-qc.js (skalaFont2, tataPage). deployV2 perlu patch lokal: opsi `ubah` (fungsi yang mengubah els sebelum disimpan), `sumber` (URL JSON templat, mis. elementor/*.json) dan `js` (isi Custom JS).
- Aset: perbaikan widget berulang (info kartu dosen) dan warna b/heading (inherit) di scripts/buat_aset_ugm.py (PR #36).
- Header v2 (id 16571): logo 22% + menu 76% satu baris. Menu v2 diedit tim (Program Studi -> Pendidikan), jangan ditimpa.
- Tenaga Kependidikan yang benar = tenaga-kependidikan-v3 (v2 = halaman UGM id 14292).
- Keputusan tertunda: form Kontak (opsi Elementor Pro Form, butuh email penerima), isi Layanan Akademik.

## ID di web UGM
Home v2 = 16487 (publish, slug new). Andang Widi Harto = 16511 (private). Media Home v2: 23 gambar. Dosen & KBK & prodi: belum dipasang.

## Sumber templat (repo ini)
`elementor/profil/<slug>.json` (38), `elementor/katur-daftar-dosen.json`, `elementor/kbk/*.json`, `elementor/katur-kbk-induk.json`, `elementor/katur-pengurus-departemen.json`, `elementor/katur-pengabdian.json`, `elementor/prodi-teknik-nuklir.json`, `elementor/prodi-teknik-fisika.json`. Widget: `widget/katur-*.html`. Data JSON & gambar: GitHub Pages `https://chilmion.github.io/dtntf-publikasi/data`.

## Berkas sementara di repo publik (hapus setelah selesai)
`data/staging-home/*` (gambar + home.json untuk Home v2).

## Skala tipografi Home v2 (17 Nov 2026, revisi 2; acuan halaman lain)
Diatur manual per widget (bukan kit global). Desktop / tablet / mobile:
- H1 hero 64 / 48 / 36 (line-height 1.1)
- H2 judul bagian 36 / 30 / 28 (1.15) — termasuk "Hiliriset" (dulu H1 34)
- H3 judul kartu 22 / 22 / 20 (1.3) — dulu H2 24 / H4 32
- Isi 17 / 16 / 16 (1.6); tanggal/keterangan 15 / 15 / 14; strip atas >= 13
- Menu header 17px, tanpa kotak saat hover/aktif (hanya warna #003D79)
Catatan teknis: editor Elementor Home v2 kadang gagal memuat pratinjau (SecurityError lintas-origin). Simpan lewat `elementorCommon.ajax.addRequest('save_builder', ...)` dengan `elementor.config.initial_document.elements` yang sudah diubah.
- Jarak huruf (letter-spacing): H1 -0.025em, H2 -0.02em, H3 -0.01em, isi 0, tombol +0.02em. Bobot: H1/H2 400, H3 500. Judul Plus Jakarta Sans; isi/tombol/daftar Barlow. Blog posts (Berita Terbaru) masih beda; dirapikan di revisi 6.

## Home v2: revisi 3-6 (17 Nov 2026)
- Hero: tombol utama lime (Mulai Perjalananmu) + tombol kedua outline (Lihat Program Studi, tautan #program); 16px, tinggi 52px, dalam wadah baris (gap 14px; kolom di mobile).
- Program (id elemen `program`): 3 kartu tanpa tombol, seluruh kartu tautan ke /prodi/, /prodi-s1-teknik-fisika/, /program-studi-magister-teknik-fisika/ (stretched link lewat CSS). Statistik dari manual/prodi/*.md; data Magister bertanda [Contoh] (belum ada sumber).
- Acara: kategori WP "Acara" (id 328) + 4 artikel contoh (id 17181, 17183, 17185, 17187; foto Unsplash, sumber di deskripsi media). Widget ekit-blog-posts `h3r0ac4`, mode "Category Post" (`is_manual_selection` kosong; nilai "recent" mengabaikan kategori).
- Berita: widget `4f348d1f`, kategori Berita (id 8), 3 kartu; gambar 200px, tinggi kartu sama (equal_height).
- Hapus artikel contoh Acara bila sudah ada acara sungguhan (judul diawali "[Contoh]").
- Acara Home v2 (rev. 17 Nov): foto kiri (`h3r0im1`) + daftar kanan (`h3r0ls1`, kelas `dt-acara-daftar`). Blok tanggal besar dibuat skrip kecil di `eael_custom_js` halaman (membaca baris pertama isi artikel: "Sabtu, 6 Desember 2026, 09.00 WIB, Tempat"). Aturan skrip: tanpa karakter `& < > "` DAN tanpa backslash (backslash hilang saat keluar; pakai [0-9] dan spasi, bukan \d \s). Simpan dua kali agar skrip keluar. Panah tombol digambar CSS murni (data:URI di custom CSS dibuang server). Format isi artikel Acara wajib: baris pertama tanggal + jam + tempat.

## Home v2: poin 7 (17 Nov 2026)
- Judul bagian (Program, Acara, Berita, Fasilitas, MOOC) rata tengah; padding vertikal bagian 3/4/6/7 = 80 (tablet 64, mobile 48).
- Widget video Elementor bawaan ("Choose your video") di kartu Profil Alumni diganti teks; kartu MOOC: gambar 150px landscape (object-fit cover), judul "[Contoh] ..." rata kiri.
- PERINGATAN simpan via save_builder: selalu muat ulang editor sebelum tiap simpan (initial_document basi menimpa perubahan sebelumnya). Server UGM sering 502; beri jeda 40 dtk.
- Angka kartu fasilitas (5+ Mitra Kerjasama, 5+ KBK, 5+ Profesor dan Doktor) masih data contoh dari v1; ganti data nyata.


## Home v2: revisi 8 (17 Nov 2026)
- Tautan tombol: Mulai Perjalananmu -> /sejarah-v2/; Profil Alumni -> /kemahasiswaan/; Rekayasa -> /visi-dan-misi-v2/; Mitra -> /mitra/; KBK -> /kbk/; Fasilitas/Laboratorium ke halamannya. Kartu MOOC belum bertautan.
- Bagian "Masa depanmu dimulai dengan pilihan yang tepat" mengikuti v1.katur.online: lebar kotak 1280px, tinggi baris 400/440px, kartu angka (Mitra, KBK) dengan ikon panah bertautan (`white-space:nowrap` pada judul agar tidak terbungkus).
- Latar kartu: Fasilitas = slideshow foto (media 16839, 16841, 16838; 4,5 dtk, fade); Laboratorium = slideshow foto lab (16811, 16814, 16812, 16813, 16810); Profil Alumni = latar video (`background_video_link`, saat ini video demo Elementor sebagai placeholder; ganti bila ada video nyata). Isi di atas video perlu `z-index` lewat custom CSS.
- Keunggulan Akademik: logo IABEE (media 17384), BAN-PT (17385), LAM Teknik (17400) di kotak putih (gambar diperkecil 280px).
- Header (template 16571, widget menu `ca1b78c`): panel submenu ElementsKit dulu terpisah ~6px dari menu sehingga menutup saat kursor lewat. Perbaikan: `top:calc(100% - 12px)` plus jembatan `.elementskit-dropdown::before` setinggi 24px (penanda `/*PONTON*/`). Strip atas selebar baris logo (boxed 1300) agar sejajar kiri dengan logo.
- Belum diverifikasi di mobile 390px. Data contoh: angka 5+, statistik Magister, kartu MOOC, artikel "[Contoh]" Acara.
