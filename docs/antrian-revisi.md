# Antrian revisi tf.ugm.ac.id — per grup menu (untuk dicek user per grup)

Aturan kerja: tiap grup dikerjakan penuh (revisi Google Docs 19 Nov + desain terbaru v1 + skala tipografi Home tf), lalu user mengecek beberapa halaman sekaligus, baru lanjut ke grup berikutnya. Semua halaman = widget Elementor native (tanpa HTML/style/svg/script). Tipografi: H1 64/48/36, H2 36/30/28, H3 22/22/20, isi 17/16/16 Barlow; judul Plus Jakarta Sans (`scripts/native_tipografi.py`).

## 0. Global (sudah / berjalan)
- [x] Menu: KBK "Kelompok Bidang Keahlian (KBK)" 2 kolom, Publikasi dan Riset + Mitra 3 kolom (header CSS, catatan 43). Header sudah OK.
- [x] Home: tetap versi sekarang.
- [ ] Footer: pakai footer terbaru v1 (perlu template footer baru di tf; kondisi tampil di halaman buatan akun lab).

## 1. Tentang Kami (dikerjakan pertama)
- [x] Sejarah: halaman tf (16872) sudah timeline teks tanpa foto (69 container, 0 gambar); tidak perlu diubah — cek visual user
- [ ] Visi dan Misi: selaraskan tipografi/gaya v1
- [ ] Struktur Organisasi: selaras v1 (bagan jadi gambar PNG)
- [x] Pengurus Departemen: ACC user 19 Nov (desain v1, judul center, Alexander<->Kholid) — id 16793
- [x] Dosen Tetap: tombol sejajar, tanpa judul bagian (id 16763); foto seragam AI menyusul
- [ ] Detail dosen (38 profil): angka bagian center + lebih besar
- [x] Tenaga Kependidikan: ACC user (id 16884)
- [~] Fasilitas Umum 16901: 2 teks diganti (Aksesibilitas Difabel, Co-working Space) di desain lama tf; bento v1 8 kartu + urutan baru belum (perlu generator native)

## 2. Pendidikan
- [ ] Gaya seragam di Kalender Akademik, Panduan Akademik, Akreditasi (acuan: halaman Panduan Akademik tf)
- [ ] Panduan Akademik: kartu TN 2 tombol (Reguler, IUP) + kartu TF + Magister
- [ ] Akreditasi: kelompok per prodi (S1 TN, S1 TF, Magister), center
- [x] Prodi S1 TN, S1 TF, IUP, Magister: Laporan Akademik 1 kolom, kartu dokumen dirapikan (sampul ringkas), tipografi skala Home — LIVE ulang 19 Nov (SHA de76ab0)
- [ ] Kartu "Panduan Akademik" dan "Laporan Kinerja" per prodi (tautan kosong)

## 3. Penelitian
- [x] KBK x4 LIVE ulang dengan tipografi skala Home (SHA de76ab0); KBK Instrumentasi tanpa Anggota
- [ ] Halaman induk KBK /kbk/ (2 kolom, judul center)
- [ ] Publikasi dan Riset
- [ ] Mitra Penelitian (halaman baru) dan Mitra Pengabdian (halaman baru): templat sama, logo berwarna (logo dicari terakhir)

## 4. Pengabdian
- [ ] Pengabdian: angka di grafik, 2016–2026 per 5 tahun (grafik PNG)

## 5. Kemahasiswaan & Alumni
- [ ] "Prestasi dan Mahasiswa" + "Prestasi dan Kabar Alumni": masing-masing hero video (placeholder YouTube DTNTF) + grid artikel

## 6. Layanan
- [ ] Layanan Akademik: 6 kartu "SOP …" (judul kosong kecuali SOP Tugas Akhir, SOP Kerja Praktek)
- [ ] Laboratorium: tombol Selengkapnya di semua lab, baris bawah center

## 7. Terakhir
- [ ] Logo mitra (cari di internet); video hero placeholder (cek kanal YouTube DTNTF)

## Rencana checkpoint (limit sesi hampir habis; urutan kerja berikutnya)
- **Checkpoint 1 (sudah bisa dicek user)**: Pendidikan > 4 prodi (TN, TF, IUP, Magister) dan Penelitian > 4 KBK, plus menu KBK/Mitra. Cek: kartu dokumen ringkas, tipografi, Laporan 1 kolom, galeri/anggota KBK.
- **Checkpoint 2 (Tentang Kami, ~60–90 mnt)**: Pengurus + Tenaga Kependidikan sinkron desain v1 (bangun ulang native dari v1), Dosen Tetap (tombol), Sejarah (timeline tanpa foto), Fasilitas, Visi Misi, Struktur.
- **Checkpoint 3 (Pendidikan sisa, ~45 mnt)**: gaya seragam Kalender/Panduan/Akreditasi, Panduan 2 tombol + kartu TF/Magister, Akreditasi per prodi.
- **Checkpoint 4**: Mitra x2 + Pengabdian (+ KBK induk), Kemahasiswaan (hero video placeholder), Layanan (SOP) + Laboratorium, footer v1, logo mitra terakhir.
Catatan: deploy tiap halaman ~1–2 mnt (simpan lambat); tiap checkpoint ditutup dengan daftar id halaman + tautan publik untuk dicek.
