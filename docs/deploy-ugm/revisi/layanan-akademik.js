// Layanan Akademik (v1 id 1818, 19 Nov 2026): salinan halaman tf.ugm.ac.id/layanan-akademik/ (banner tema + H2 + lead + 6 kartu 3x2).
// Pakai di tab wp-admin v1: tempel berkas ini lalu `await deployLayananAkademik(1818)` (kernFix/nolPadding sudah termasuk; tombol tanpa huruf kapital).
// Di tf halaman ini SUDAH ADA (jangan ditimpa). Tautan internal v1: /kalender-akademik/, /panduan-akademik-prodi-s1-teknik-nuklir/, /prodi/, /kontak/.
window.deployLayananAkademik = async function (halamanId) {
  if (!window.R) { const t = await (await fetch('https://raw.githubusercontent.com/chilmion/dtntf-publikasi/main/docs/deploy-ugm/rancang.js', {cache: 'no-store'})).text(); (0, eval)(t); }
  const {Banner, Sec, H, Pg, B, C, Card, Grid, simpan, T} = R;
  const K = [
    ['Kalender akademik', 'Jadwal kegiatan akademik semester gasal dan genap.', 'Lihat kalender', '/kalender-akademik/', false],
    ['Panduan akademik', 'Panduan kurikulum dan laporan kinerja akademik Program Studi S1 Teknik Nuklir.', 'Buka panduan', '/panduan-akademik-prodi-s1-teknik-nuklir/', false],
    ['SIMASTER', 'Sistem informasi akademik UGM untuk KRS, nilai, dan jadwal kuliah.', 'Buka SIMASTER', 'https://simaster.ugm.ac.id/', true],
    ['Program studi', 'Informasi program sarjana dan magister di departemen.', 'Lihat program studi', '/prodi/', false],
    ['SMS FT', 'Layanan pengaduan dan informasi Fakultas Teknik untuk departemen.', 'Buka SMS FT', 'https://sms.ft.ugm.ac.id/dtntf', true],
    ['Kontak', 'Tanya jawab dan bantuan layanan akademik langsung ke departemen.', 'Hubungi kami', '/kontak/', false]];
  const kartu = k => Card([
    H(k[0], 'h3'),
    Pg(k[1], {color: T.muted}),
    B(k[2], k[3], {outline: true, ext: k[4]})], {gap: 12});
  const els = [
    Banner('Layanan Akademik', [['Beranda', '/'], ['Pendidikan'], ['Layanan Akademik']]),
    Sec([C([H('Layanan untuk mahasiswa', 'h2'), Pg('Akses cepat ke layanan akademik departemen dan universitas.', {color: T.body})], {gap: 12, pad: [0, 0, 0, 0]}),
      Grid(K.map(kartu), {cols: 3, gap: 24})], {pt: 56, pb: 72, gap: 28, bg: T.white})];
  // kit Elementor: word-spacing 6px di judul dan huruf kapital tiap kata di tombol -> nolkan langsung (tanpa kernFix)
  const fix = a => a.forEach(e => { if (e.elType === 'widget') { Object.assign(e.settings, {typography_typography: 'custom', typography_word_spacing: {unit: 'px', size: 0, sizes: []}}); if (e.widgetType === 'button') e.settings.typography_text_transform = 'none'; } fix(e.elements || []); }); fix(els);
  const zero = (a, d) => a.forEach(e => { if (e.elType === 'container' && d > 0 && !e.settings.padding) e.settings.padding = {unit: 'px', top: '0', right: '0', bottom: '0', left: '0', isLinked: true}; zero(e.elements || [], d + 1); }); zero(els, 0);
  return await simpan(halamanId, els, {});
};
