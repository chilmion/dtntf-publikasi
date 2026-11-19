# Antrian revisi tf.ugm.ac.id — per grup menu (untuk dicek user per grup)

Aturan kerja: tiap grup dikerjakan penuh (revisi Google Docs 19 Nov + desain terbaru v1 + skala tipografi Home tf), lalu user mengecek beberapa halaman sekaligus, baru lanjut ke grup berikutnya. Semua halaman = widget Elementor native (tanpa HTML/style/svg/script). Tipografi: H1 64/48/36, H2 36/30/28, H3 22/22/20, isi 17/16/16 Barlow; judul Plus Jakarta Sans (`scripts/native_tipografi.py`).

## 0. Global (sudah / berjalan)
- [x] Menu: KBK "Kelompok Bidang Keahlian (KBK)" 2 kolom, Publikasi dan Riset + Mitra 3 kolom (header CSS, catatan 43). Header sudah OK.
- [x] Home: tetap versi sekarang.
- [x] Footer v1 hanya di halaman new 16487 — menunggu cek user

## 1. Tentang Kami (dikerjakan pertama)
- [x] Sejarah 16872: dibangun ulang dari v1 (peta jalan timeline tanpa foto + periode berkartu foto) — menunggu cek user
- [x] Visi dan Misi 16875: native dari v1 — menunggu cek user
- [x] Struktur Organisasi 16890: native dari v1, bagan PNG — menunggu cek user
- [x] Pengurus Departemen: ACC user 19 Nov (desain v1, judul center, Alexander<->Kholid) — id 16793
- [x] Dosen Tetap: tombol sejajar, tanpa judul bagian (id 16763); foto seragam AI menyusul
- [ ] Detail dosen (38 profil): angka bagian center + lebih besar
- [x] Tenaga Kependidikan: ACC user (id 16884)
- [x] Fasilitas Umum 16901: bento v1 native + 3 penggantian teks + urutan baru — menunggu cek user

## 2. Pendidikan
- [x] Gaya seragam Kalender, Panduan, Akreditasi — kartu dokumen/sertifikat (id 16887, 16913, 16893) — menunggu cek user
- [x] Panduan Akademik: kartu TN 2 tombol + kartu TF + Magister (tautan PDF IUP/TF/Magister kosong)
- [x] Akreditasi per prodi, center (judul LAM/IABEE yang tertukar sudah dibenarkan)
- [x] Prodi S1 TN, S1 TF, IUP, Magister: Laporan Akademik 1 kolom, kartu dokumen dirapikan (sampul ringkas), tipografi skala Home — LIVE ulang 19 Nov (SHA de76ab0)
- [ ] Kartu "Panduan Akademik" dan "Laporan Kinerja" per prodi (tautan kosong)

## 3. Penelitian
- [x] KBK x4 LIVE ulang dengan tipografi skala Home (SHA de76ab0); KBK Instrumentasi tanpa Anggota
- [ ] Halaman induk KBK /kbk/ (2 kolom, judul center)
- [ ] Publikasi dan Riset
- [x] Mitra Penelitian 16907 dan Mitra Pengabdian 17246: templat sama, logo berwarna (7 logo belum ada berkasnya: BAPETEN, PLN, SUCOFINDO, BPBD, PT PAL, ThorCon, IAEA) — menunggu cek user

## 4. Pengabdian
- [x] Pengabdian 16798: grafik PNG berangka 2016–2026 per 5 tahun — menunggu cek user

## 5. Kemahasiswaan & Alumni
- [x] Kemahasiswaan 16910: dua section, hero video YouTube DTNTF + grid artikel — menunggu cek user

## 6. Layanan
- [x] Layanan Akademik 16896: kartu SOP — menunggu cek user
- [x] Laboratorium 16881: tombol di semua lab, baris bawah center — menunggu cek user

## 7. Terakhir
- [ ] Logo mitra (cari di internet); video hero placeholder (cek kanal YouTube DTNTF)

## Rencana checkpoint (limit sesi hampir habis; urutan kerja berikutnya)
- **Checkpoint 1 (sudah bisa dicek user)**: Pendidikan > 4 prodi (TN, TF, IUP, Magister) dan Penelitian > 4 KBK, plus menu KBK/Mitra. Cek: kartu dokumen ringkas, tipografi, Laporan 1 kolom, galeri/anggota KBK.
- **Checkpoint 2 (Tentang Kami, ~60–90 mnt)**: Pengurus + Tenaga Kependidikan sinkron desain v1 (bangun ulang native dari v1), Dosen Tetap (tombol), Sejarah (timeline tanpa foto), Fasilitas, Visi Misi, Struktur.
- **Checkpoint 3 (Pendidikan sisa, ~45 mnt)**: gaya seragam Kalender/Panduan/Akreditasi, Panduan 2 tombol + kartu TF/Magister, Akreditasi per prodi.
- **Checkpoint 4**: Mitra x2 + Pengabdian (+ KBK induk), Kemahasiswaan (hero video placeholder), Layanan (SOP) + Laboratorium, footer v1, logo mitra terakhir.
Catatan: deploy tiap halaman ~1–2 mnt (simpan lambat); tiap checkpoint ditutup dengan daftar id halaman + tautan publik untuk dicek.
