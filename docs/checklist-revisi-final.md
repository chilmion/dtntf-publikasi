# Checklist revisi final jurusan (Google Docs "Revisi Terbaru DTNTF 19 November") — sudah diklarifikasi user

Status di tf.ugm.ac.id. ✅ live · ⬜ belum. Semua halaman tf = widget Elementor native (tanpa widget HTML).

| # | Halaman | Revisi (sesudah klarifikasi) | tf |
|---|---------|------------------------------|----|
| 1 | Sejarah | Bagian "Peta jalan" jadi timeline TANPA foto (foto sudah ada di bagian bawahnya) | ⬜ |
| 2 | Pengurus | Alexander Agung <-> Kholid Ridwan; baris bawah grid rata tengah | ✅ (cek ulang baris lab) |
| 3 | Dosen Tetap | "Profil lengkap →": hapus panah, jadikan tombol yang jelas | ⬜ |
| 4 | Detail dosen | Angka bagian (1,2,3) dibuat center dan lebih besar, sejajar judul | ⬜ |
| 5 | Tenaga Kependidikan | Sabar di urutan terakhir | ✅ |
| 6 | Laboratorium | Tombol "Selengkapnya" di SEMUA lab; baris bawah (2 kartu) rata tengah | ⬜ (halaman /laboratorium-v2/) |
| 7 | Fasilitas Umum | "Kamar Mandi / Toilet" -> "Aksesibilitas Difabel"; "Katalog Ruang" -> "Ruang kelas & auditorium fakultas teknik"; "Rumah Kayu" -> "Konseling Psikolog"; urutan: Ruang kelas & auditorium, Laboratorium / Perpustakaan, Unit Layanan Terpadu, Konseling Psikolog / Co-working space, Fasilitas Difabel, Teknologi Informasi (gambar kartu tetap; cek dengan screenshot) | ⬜ |
| 8 | Panduan Akademik | Kartu TN: satu kartu, DUA tombol (Unduh PDF Reguler, Unduh PDF IUP); di sampingnya kartu Teknik Fisika dan Magister Teknik Fisika (struktur sama, satu tombol Unduh PDF) | ⬜ |
| 9 | Akreditasi | Dikelompokkan per prodi: S1 Teknik Nuklir, S1 Teknik Fisika, Magister Teknik Fisika; grid rata tengah, jumlah kartu mengikuti jumlah dokumen | ⬜ |
| 10 | Prodi S1 TN | Laporan Akademik 1 kolom menurun, terbaru di atas | ✅ |
| 11 | Prodi S1 TF | Laporan Akademik seperti TN (4 tahun, 1 kolom) | ✅ |
| 12 | IUP TN, Magister TF | Templat seperti TN/TF, data kosong | ✅ |
| 13 | KBK Instrumentasi | Hapus section Anggota | ✅ |
| 14 | Menu KBK (mega-menu) | Judul "Kelompok Bidang Keahlian (KBK)", rata tengah, 2 kolom; urutan ENET, Proses Nuklir / Multifisika, Instrumentasi | ⬜ (header 16571, lihat risiko) |
| 15 | Menu Penelitian | "Mitra" digeser ke kanan sehingga ada 3 kolom | ⬜ (header) |
| 16 | Mitra | Dua submenu/halaman: Mitra di Penelitian dan Mitra di Pengabdian; template dan isi disamakan dulu; logo berwarna | ⬜ |
| 17 | Pengabdian | Grafik Kegiatan per tahun: angka di tiap batang; tahun 2016–2026, label per 5 tahun | ⬜ (grafik = PNG) |
| 18 | Kemahasiswaan & Alumni | Dua section: "Prestasi dan Mahasiswa" (di paling atas) dan "Prestasi dan Kabar Alumni"; tiap section: hero video (tampilan seperti hero Home) lalu grid artikel | ⬜ |
| 19 | Layanan Akademik | Ganti judul 6 kartu: Kalender Akademik -> SOP Tugas Akhir, Panduan Akademik -> SOP Kerja Praktek, 4 lainnya judul "SOP" dikosongkan agar bisa diedit; deskripsi disesuaikan | ⬜ |

## Risiko dan pertanyaan terbuka
- #14/#15 (menu): mega-menu digambar CSS di header 16571, dan header TIDAK boleh disimpan ulang (catatan 34: merusak CSS). Perlu cara lain (mis. ubah item menu lewat REST `menu-items` dan CSS lewat Customizer) atau keputusan user.
- #18: sumber video hero dan artikel "Prestasi dan Mahasiswa" belum ada (video: YouTube/berkas?).
- #16: logo berwarna: 7 logo (BAPETEN, PLN, PT PAL, ThorCon, IAEA, SUCOFINDO, BPBD) belum punya berkas; yang ada saja yang diberi warna aslinya.
- #8: tautan PDF (Reguler, IUP, TF, Magister) belum ada; tombol dibuat dengan tautan kosong.
