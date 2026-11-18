# Revisi dosen jurusan (18 Nov 2026) — dibahas per halaman

## Cara kerja (keputusan user, 18 Nov 2026 malam)
- Presentasi 19 Nov siang. Web jurusan (tf.ugm.ac.id) logout dan tidak ada orang di kampus -> revisi dikerjakan dulu di **v1.katur.online** (Chrome Mac sudah login) agar bisa dilihat.
- Per halaman: samakan dengan versi terbaru web jurusan, terapkan revisi dosen kalau ada, lalu bahas bersama.
- Besok pagi staf lab login di komputer jurusan (Chrome Windows tersambung ke Claude), lalu semua yang disetujui di v1 diterapkan ke tf.ugm.ac.id.
- **Beranda (Home): hanya revisi navigasi** (header, footer, isi menu). Isi tengah Home tidak diubah.

## Status penerapan
- v1.katur.online: A dan B SELESAI (A = DONE). tf.ugm.ac.id: BELUM (menunggu login).
- Catatan teknis v1: header id 853 (widget menu `ca1b78c`), footer id 1991, Home id 265, menu WP id 15 (`menu-dtntf`, diubah lewat REST `wp/v2/menu-items` dengan nonce dari halaman admin). Tampilan header v1 disalin dari CSS publik tf.ugm.ac.id/post-16571.css; susunan: logo baris atas, menu baris bawah.
- Di tf.ugm.ac.id, menu header = menu WP (nav-menus.php diarahkan 404 untuk akun lab; ubah lewat REST atau editor header 16571).


Status: [ ] belum, [~] sedang, [x] selesai. "?" = perlu keputusan/bahan dari jurusan.

## A. Menu & navigasi (header) — A DONE (v1)
- [x] A1. Akreditasi + Panduan Akademik pindah dari Tentang Kami ke Pendidikan
- [x] A2. Pendidikan 2 kolom: K1 Kalender Akademik, Panduan Akademik, Akreditasi; K2 Sarjana Teknik Nuklir, Sarjana Teknik Fisika, MTF
- [x] A3. Layanan Akademik pindah ke menu Layanan
- [x] A4. Urutan Penelitian: KBK, Publikasi dan Riset, Mitra
- [x] A5. Kontak jadi menu sendiri di samping Layanan -> DONE di v1: menu top-level "Kontak" setelah Layanan (halaman Kontak lama id 879)

## B. Home (bawah: footer) — DONE (v1)
- [x] B1. Footer: Terhubung Bersama Kami (IG dtntf_ugm, YouTube UCO-95rJvaOPC_ujUxn5BK7w, FB dtntf.ft.ugm, X dtntf_ugm) + peta Google kecil di sampingnya (embed -7.7662333,110.3728); Layanan: Kontak diganti Layanan Akademik

## C. Tentang Kami
- [x] C1 (v1 selesai, tf.ugm belum). Sejarah: timeline peta jalan dalam satu gambar; periode "2022–Sekarang: Ekspansi Global dan Nasional" (melebarkan kerja sama dengan perusahaan dan universitas); font tahun lebih besar, teks lebih tebal
- [x] C2 (v1 selesai, tf.ugm belum). Visi Misi: ukuran dan kontras font, visibilitas
- [x] C3 (v1 selesai, tf.ugm belum). Struktur organisasi: resolusi gambar (? berkas asli resolusi tinggi)
- [x] C4 (v1 selesai, tf.ugm belum). Sertifikat akreditasi: 5 slot (? berkas sertifikat)
- [ ] C5. Pengurus Departemen: foto lebih kecil dan close up, tata letak mengacu web lama + contoh web FT; jumlah Kadep/Sekdep 2, Kaprodi 3, Sekprodi 2, Kalab 3 (baris "Kalab 2" ?), KBK 4 (? foto baru atau potong ulang)
- [ ] C6. Dosen Tetap: tautan langsung ke SINTA (lengkap), hapus jumlah sitasi di depan, foto lebih proporsional
- [ ] C7. Tenaga Kependidikan: grup Koordinator / Teknisi Laboran / Staf, grid tanpa yang tertinggal
- [ ] C8. Fasilitas umum: Ruang Tunggu jadi Co-working Space; tautan ke fasilitas FT dan UGM

## D. Halaman prodi (TN id 688, TF id 1763, MTF)
- [ ] D1. Tautan dokumen kurikulum di bawah bagian kurikulum (? berkas)
- [ ] D2. Laporan Kinerja: unggahan dokumen (? berkas)
- [ ] D3. Ukuran/resolusi gambar disesuaikan

## E. Penelitian
- [ ] E1. KBK: galeri riset paling menonjol; peta jalan; Kompetensi dan Keahlian; dosen dikelompokkan per bidang (nama tertaut ke profil); "Riset Terkait" jadi "Pendanaan"; tampil hanya judul, deskripsi, foto, read more
- [ ] E2. Pengabdian: galeri diganti konten Mitra
- [ ] E3. Mitra: logo + konten kerja sama yang ditonjolkan (BPBD, PLN, BRIN, ...) (? logo dan teks)

## F. Profil dosen (CV) & data SINTA
- [ ] F1. Hapus: jabatan fungsional, institusi, telepon institusi, riwayat pekerjaan, penghargaan, tulisan "DATA SINTA"
- [ ] F2. "Pengalaman kerja sama dan penelitian" jadi "Pengalaman kerja sama"
- [ ] F3. Rupiah di penelitian dan PPM dari SINTA tidak ditampilkan (termasuk halaman Pengabdian, ?)

## Catatan konflik dengan keputusan lama (konfirmasi)
- Akreditasi dulu di Tentang Kami; sekarang ke Pendidikan.
- CV: Penghargaan dan Riwayat pekerjaan sebelumnya ada; sekarang dihapus (data di profil-cv.xlsx tetap boleh disimpan).
- Urutan menu Penelitian berubah.

## Urutan pembahasan yang diusulkan
1. A (menu) -> 2. F (CV/SINTA, cepat dan berdampak ke 38 profil) -> 3. C5-C7 (pengurus, dosen, tendik) -> 4. C1-C4, C8 -> 5. E (KBK, Mitra, Pengabdian) -> 6. D -> 7. B

## Peta halaman web jurusan (dari menu publik tf.ugm.ac.id/new/)
Beranda /new/; Sejarah /sejarah-v2/; Visi dan Misi /visi-dan-misi-v2/; Struktur /struktur-organisasi/; Akreditasi /akreditasi/; Panduan Akademik /panduan-akademik-prodi-s1-teknik-nuklir/; Pengurus /pengurus-departemen-v2/; Dosen Tetap /daftar-dosen-departemen-teknik-nuklir-dan-teknik-fisika-ft-ugm/; Tenaga Kependidikan /tenaga-kependidikan-v3/; Laboratorium /laboratorium-v2/; Fasilitas Umum /fasilitas-umum/; Kalender /kalender-akademik-v2/; Prodi TF /prodi-s1-teknik-fisika/; Prodi TN /prodi/; IUP /iup-teknik-nuklir/; Magister /program-studi-magister-teknik-fisika/; Layanan Akademik /layanan-akademik/; Publikasi dan Riset /publikasi-dan-riset/; KBK /kbk-v2/ + /kbk-enet/ /kbk-proses-nuklir-v2/ /kbk-multifisika-v2/ /kbk-instrumentasi-v2/; Mitra /mitra/; Galeri /galeri/; Mitra Pengabdian /mitra-pengabdian/; Pengabdian /pengabdian/; Kemahasiswaan /kemahasiswaan/; Kontak /kontak-v2/.
Catatan: menu tf.ugm.ac.id masih lama (belum ada revisi A: Akreditasi di Tentang Kami, Kontak di bawah Layanan).

## Hasil perbandingan v1 vs web jurusan (18 Nov malam)
- Halaman dalam jurusan dibangun ulang dengan `docs/deploy-ugm/rancang.js` (Banner, Sec, Card, Grid; skala 48/36/22/17). v1 masih tampilan lama. Cara menyamakan di v1: muat rancang.js di tab wp-admin v1 lalu `R.simpan(<id halaman v1>, elemen)`.
- Halaman yang TIDAK ada di v1: IUP Teknik Nuklir, Magister TF, Layanan Akademik (di jurusan ada).
- Id halaman v1: sejarah 779, visi-dan-misi 325, struktur 1620, akreditasi 727, panduan 538, pengurus 368, dosen tetap 1195, tenaga kependidikan 1632, laboratorium 514, fasilitas umum 1693, kalender 1707, prodi TF 1763, prodi TN 688, KBK 1920 (+1921, 1924, 1925, 1928), mitra 1750, galeri 1733, pengabdian 1917, kemahasiswaan 1721.
- Sejarah v1 dibangun ulang (peta jalan HTML satu blok + 6 periode + periode 2022-Sekarang "Ekspansi Global dan Nasional"; typo asli diperbaiki: Kerjsama, penekakan, 20 16, 1999/200). Detail 2022-Sekarang perlu dilengkapi jurusan.

## Log perubahan di v1 (untuk deploy ke tf.ugm.ac.id, 19 Nov pagi)
Prasyarat: staf lab login di komputer jurusan (Chrome Windows). Header tf.ugm = template 16571, menu WP tf.ugm memakai REST menu-items (nav-menus.php di-404).
1. **Menu** (v1 menu 15): Akreditasi pindah ke Pendidikan (+ item baru "Panduan Akademik" -> halaman Panduan, "Layanan Akademik" -> /layanan-akademik/ di Layanan); urutan Pendidikan: Kalender, Panduan, Akreditasi, S1 TN, S1 TF, MTF, IUP; Penelitian: KBK, Publikasi dan Riset, Mitra; Kontak jadi top-level setelah Layanan. Di tf.ugm: ulang lewat REST (id item beda) lalu cek menu header.
2. **Header**: v1 id 853 sudah disamakan dengan tf.ugm (logo SVG, logo baris atas + menu baris bawah, CSS persis dari tf.ugm). Di tf.ugm tambahkan saja: kolom `li.menu-item-<id Pendidikan>` 2 kolom (CSS `/*PENDIDIKAN2*/` di widget menu `ca1b78c`: `column-count:2` + `li:nth-child(4){break-before:column}`) dan karena ada 8 menu (Kontak) pastikan muat di 1300px.
3. **Footer** (v1 id 1991): sosmed 4 tautan (IG, YouTube, FB, X; TikTok dihapus), peta Google kecil di sampingnya, Layanan: Kontak -> Layanan Akademik. Footer tf.ugm bukan template v1: terapkan elemennya manual di template footer tf.ugm (atau pasang HTML widget).
4. **Sejarah**: `docs/deploy-ugm/revisi/sejarah.js` -> `deploySejarah(16872)` di tab wp-admin tf.ugm, lalu `nolPadding()` di tab editor halaman itu. Foto Unsplash (ilustrasi), isi 2022-Sekarang satu kalimat.
5. Aturan umum halaman rancang.js: setelah `R.simpan`, kontainer bersarang tanpa padding perlu dinolkan (`nolPadding`), kalau tidak teks bergeser 30px dan garis aksen banner jadi kotak hijau.
6. **Visi dan Misi**: `docs/deploy-ugm/revisi/visi-misi.js` -> `deployVisiMisi(16875)`; lalu di editor jalankan `nolPadding()` (dari sejarah.js) untuk garis aksen banner. Visi jadi blok besar 28px (Departemen = panel navy), Misi daftar bernomor 19px.
7. **Struktur Organisasi**: `docs/deploy-ugm/revisi/struktur.js` -> `deployStruktur(16890)`. Bagan digambar ulang sebagai SVG vektor (isi sama dengan gambar lama 1024x723); kartu prodi menaut ke /prodi/, /prodi-s1-teknik-fisika/, /iup-teknik-nuklir/, /program-studi-magister-teknik-fisika/ (dua terakhir belum ada di v1).
8. **Struktur: kartu Program Studi** gaya bento (foto latar + gradasi navy, ukuran 62%/36% bergantian, panah lime, kartu seluruhnya bertaut). Sudah masuk struktur.js. Foto Unsplash (ilustrasi; IUP = dua peneliti di lab).
9. **Akreditasi**: `docs/deploy-ugm/revisi/akreditasi.js` -> `deployAkreditasi(16893)`. 5 slot (kotak ke-6 kosong di jurusan dibuang), dikelompokkan 3 kolom: S1 TN (LAM, IABEE), S1 TF (LAM, IABEE), Magister (LAM); klik = berkas penuh. Lalu nolPadding() di editor halaman.
