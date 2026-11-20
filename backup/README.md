# Backup JSON halaman Elementor

- `v1-2026-11-20/` — data Elementor (elements + settings) 74 halaman/templat di v1.katur.online, diambil 20 Nov 2026 setelah sinkron revisi QC. Satu berkas per halaman: `<id>-<slug>.json`. Id 853 = header, 1991 = footer.
- Sumber halaman tf.ugm.ac.id yang dibangun native: `elementor/native/*.json` (dibuat `scripts/buat_native_*.py`).
- Backup langsung dari tf (Home, header 16571, Galeri, dll.) belum ada; lihat catatan 63.

## tf-2026-11-20 (situs live tf.ugm.ac.id)
118 berkas `<id>-<slug>.json` (halaman + templat Elementor termasuk header 16571), diambil 20 Nov 2026 dari editor Elementor lewat Chrome kampus. Isi: `{id,title,type,settings,elements}`. Pulihkan dengan memasukkan `elements` kembali ke editor halaman terkait.
