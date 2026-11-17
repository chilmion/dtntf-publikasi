# Rapikan halaman dalam v2 (17 Nov 2026)

Sesi terpisah dari Home v2 (Home, header Theme Builder 16571 dan menu 326 ditangani sesi lain). Dikerjakan dengan `docs/deploy-ugm/rancang.js` (pustaka pembangun) lewat tab wp-admin Browser kampus.

## Pola halaman dalam (satu standar)
- **Banner** navy gradasi (#073C64 -> #1A2C43) dengan breadcrumb 14px, H1 putih 48/40/32 dan garis aksen lime 64x4. Tinggi mengikuti isi (bukan 53vh seperti v1).
- **Seksi** lebar penuh, isi 1180px, jarak vertikal 64/48/40 (desktop/tablet/mobile), latar bergantian putih dan #F5F5F5.
- **Tipografi** (manual per widget, tanpa kit global): H1 48/40/32, H2 36/30/28, H3 22/22/20 (Plus Jakarta Sans; letter-spacing -0.025/-0.02/-0.01em), isi 17/16/16 dan keterangan 15/15/14 (Barlow).
- **Kartu** putih radius 16, border 1px #E3E3E3, tanpa bayangan; tombol pil (utama lime, kedua outline navy).
- **Pola dua kolom** (28/72) untuk isi bertahap (Sejarah, Visi dan Misi); grid 3-4 kolom untuk kartu/orang; tablet 2 kolom, mobile 1 (orang 2).

## Perintah
```js
// di tab wp-admin tf.ugm.ac.id
const rq = await (await fetch('https://raw.githubusercontent.com/chilmion/dtntf-publikasi/<cabang>/docs/deploy-ugm/rancang.js')).text(); (0,eval)(rq);
const {Banner, Sec, Head, Grid, Card, H, Pg, B, Im, C, crumb, norm, simpan} = R;
await R.simpan(ID, [Banner('Judul', crumb('Judul','Grup')), Sec([Head('Judul bagian','Pengantar')])], settingsHalaman);
```
- `R.norm(els)` menormalkan heading/teks/tombol/gambar widget yang sudah ada (dipakai di Pengurus, Dosen, Publikasi).
- Catatan: custom_css Elementor mengubah `>` menjadi `&gt;`; pakai selector tanpa child combinator. Nonce bisa hilang saat server 502: ulangi setelah 6 detik.

## Cadangan
JSON Elementor setiap halaman sebelum diubah disimpan di IndexedDB tab wp-admin Browser kampus: database `dtntf_bk`, store `docs`, kunci `bk_<id>` (isi `{when,id,title,elements,settings}`). Untuk memulihkan: `await R.simpan(id, doc.elements, doc.settings)`.

## Halaman yang dibangun ulang (isi asli dipertahankan)
Sejarah (garis waktu 5 periode), Visi dan Misi (4 entitas), Struktur Organisasi (judul "Contact Us" yang salah diganti, bagan + kartu program studi), Akreditasi (6 kartu sertifikat; satu berkas belum ada), Panduan Akademik, Tenaga Kependidikan (grid foto), Laboratorium, Fasilitas Umum, Kalender Akademik, Layanan Akademik (isi baru: tautan layanan nyata), Mitra, Mitra Pengabdian (halaman baru `mitra-pengabdian`, id 17246), Galeri, Kemahasiswaan dan Alumni, Kontak (info + formulir + peta), Prestasi.
Diberi banner dan/atau normalisasi: Pengurus Departemen, Dosen Tetap, Publikasi, Publikasi dan Riset, Pengabdian, KBK (indeks).
Tidak diubah: Prodi TN/TF, IUP, Magister (sudah memakai rancangan v2/lorem), halaman KBK per kelompok.

## Keputusan yang perlu user
- Kategori daftar berita: Mitra = `kerjasama` (id 14), Mitra Pengabdian = `pengabdian-masyarakat` (106), Kemahasiswaan = `prestasi` (19) + `alumni` (6), Prestasi = 19.
- Penerima email formulir Kontak masih bawaan situs.
