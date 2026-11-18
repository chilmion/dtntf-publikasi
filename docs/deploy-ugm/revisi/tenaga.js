// Tenaga Kependidikan (revisi dosen 18 Nov 2026): kelompok Koordinator, Teknisi/Laboran, Staf; grid tanpa kartu yatim (3 / 4 / 3x3).
// Diuji di v1 (halaman 1632). tf.ugm.ac.id: tab wp-admin biasa -> await deployTenaga(16884, 'tf')   (v1: await deployTenaga(1632, 'v1'))
window.deployTenaga = async function (halamanId, situs) {
  if (!window.R) { const t = await (await fetch('https://raw.githubusercontent.com/chilmion/dtntf-publikasi/main/docs/deploy-ugm/rancang.js', {cache: 'no-store'})).text(); (0, eval)(t); }
  const {Banner, Sec, H, Pg, C, crumb, wd, simpan, T} = R; const Z = [0, 0, 0, 0];
  const B = situs === 'tf' ? 'https://tf.ugm.ac.id/wp-content/uploads/sites/7/2026/11/' : '/wp-content/uploads/2026/10/';
  const F = situs === 'tf'
    ? {ardina: 'WhatsApp-Image-2026-10-08-at-15.36.52-394x510-1.jpg', winarno: 'Winarno-408x510-1.jpg', budiyono: 'Budiyono-408x510-1.jpg', roma: 'Roma-Setiawan-S.Pd_-408x510-1.jpg', sukiyat: 'Sukiyat-408x510-1.jpg', andi: 'Andi-Sudarmanto-S.Sos_-408x510-1.jpg', johan: 'Johan-Purwanto-S.Sos_-408x510-1.jpg', sukini: 'Perempuan-DTNTF-408x510-1.jpg', triyanto: 'Triyanto-408x510-1.jpg', riny: '1-408x510-1.jpg', sabar: 'Sabar-408x510-1.jpg', safrudin: 'Safrudin-408x510-1.jpg', parjiyo: 'Parjiyo-408x510-1.jpg', widarto: 'Widarto.jpg', arbiyhuno: 'Arbiyhuno-Lalintyo.jpg', slamet: 'Slamet-Haryadi.jpg'}
    : {ardina: 'WhatsApp-Image-2026-10-08-at-15.36.52-394x510-1.jpg', winarno: 'Winarno-408x510-1.jpg', budiyono: 'Budiyono-408x510-1.jpg', roma: 'Roma-Setiawan-S.Pd_-408x510-1.jpg', sukiyat: 'Sukiyat-408x510-1.jpg', andi: 'Andi-Sudarmanto-S.Sos_-408x510-1.jpg', johan: 'Johan-Purwanto-S.Sos_-408x510-1.jpg', sukini: 'Perempuan-DTNTF-408x510-1.jpg', triyanto: 'Triyanto-408x510-1.jpg', riny: '1-408x510-1.jpg', sabar: 'Sabar-408x510-1.jpg', safrudin: 'Safrudin-408x510-1.jpg', parjiyo: 'Parjiyo-408x510-1.jpg', widarto: 'Widarto-819x1024.jpg', arbiyhuno: 'Arbiyhuno-Lalintyo-819x1024.jpg', slamet: 'Slamet-Haryadi-819x1024.jpg'};
  const D = {
    koor: [['Sukiyat', 'Koordinator Urusan Akademik, Kemahasiswaan dan Alumni', 'sukiyat'], ['Andi Sudarmanto, S.Sos.', 'Koordinator Urusan Administrasi Umum, SDM, Penelitian dan Pengabdian pada Masyarakat, dan Kerjasama', 'andi'], ['Johan Purwanto, S.Sos.', 'Koordinator Urusan Aset, Sarana Prasarana, SHE, dan IT', 'johan']],
    tek: [['Ardina Mei Devinta Suryana, S.S.T.', 'Lab. Teknologi Energi Nuklir', 'ardina'], ['Winanro', 'Lab. Sensor dan Sistem Telekontrol', 'winarno'], ['Budiyono', 'Lab. Energi Terbarukan; Lab. Teknologi Proses dan Kimia Nuklir', 'budiyono'], ['Roma Setiawan, S.Pd.', 'Lab. Komputasi Multifisika', 'roma']],
    staf: [['Sukini, S.Kom.', 'Pengelola Layanan Akademik', 'sukini'], ['Triyanto', 'Pengelola Layanan Akademik', 'triyanto'], ['Riny Wasita, A.Md.', 'Pengelola Layanan Akademik', 'riny'], ['Sabar', 'Pramu Bakti', 'sabar'], ['Safrudin', 'Pengelola Keuangan', 'safrudin'], ['Parjiyo', 'Pengelola Sarana dan Prasarana', 'parjiyo'], ['Widarto', 'Pengelola Kepegawaian', 'widarto'], ['Arbiyhuno Lalintyo', 'Pengelola Administrasi Umum', 'arbiyhuno'], ['Slamet Haryadi', 'Pengelola Penelitian', 'slamet']]
  };
  D.tek[1][0] = 'Winarno';
  const TIER = {koor: {w: 150, name: 20, role: 14.5, min: 52}, tek: {w: 124, name: 18.5, role: 14, min: 96}, staf: {w: 104, name: 17, role: 13.5, min: 46}};  // min = tinggi blok nama (agar label jabatan sejajar antar kolom)
  const px = v => ({unit: 'px', size: v, sizes: []}); const WS = {unit: 'px', size: 0, sizes: []};
  const person = (p, k) => {
    const t = TIER[k];
    const img = wd('html', {html: '<img src="' + B + F[p[2]] + '" alt="' + p[0].replace(/"/g, '') + '" loading="lazy" style="display:block;width:100%;height:auto;aspect-ratio:4/5;object-fit:cover;object-position:center 12%;border-radius:12px;background:#E9EEF3;box-shadow:0 1px 2px rgba(7,60,100,.12)">'});
    const cut = p[0].indexOf(','), main = cut > 0 ? p[0].slice(0, cut) : p[0], gelar = cut > 0 ? p[0].slice(cut + 1).trim() : '';
    const name = H(main + (gelar ? '<br><span class="dt-g">' + gelar + '</span>' : ''), 'h3'); Object.assign(name.settings, {typography_typography: 'custom', typography_font_family: 'Plus Jakarta Sans', typography_font_weight: '700', typography_font_size: px(t.name), typography_font_size_mobile: px(Math.min(t.name, 18)), typography_line_height: {unit: 'em', size: 1.25, sizes: []}, typography_word_spacing: WS, title_color: '#073C64', custom_css: 'selector .elementor-widget-container{min-height:' + t.min + 'px}selector .elementor-heading-title{overflow-wrap:anywhere}selector .dt-g{display:block;margin-top:4px;font-family:Barlow,sans-serif;font-size:' + (t.name <= 18 ? 13.5 : 15) + 'px;font-weight:500;line-height:1.4;letter-spacing:0;color:#5A6B7A}'});
    const role = Pg(p[1], {css: 'selector,selector p{font-family:Barlow,sans-serif;font-size:' + t.role + 'px;font-weight:600;line-height:1.4;margin:0;color:#4A4A4A}'}); role.settings.typography_word_spacing = WS; role.settings.typography_typography = 'custom';
    const left = C([img], {pad: Z, gap: 0, px: t.w}); left.settings._flex_size = 'none'; left.settings._flex_align_self = 'flex-start';
    const right = C([name, role], {pad: Z, gap: 6, justify: 'flex-start'}); right.settings._flex_size = 'grow'; right.settings.custom_css = 'selector{min-width:0;flex:1 1 0%}';
    return C([left, right], {dir: 'row', align: 'flex-start', gap: 16, pad: [14, 14, 14, 14], radius: 16, bg: '#FFFFFF', border: T.line});
  };
  const row = (list, k, cols, gap) => { const pct = Math.floor(((100 - ((cols - 1) * gap / 11.8)) / cols - 0.8) * 100) / 100; const items = list.map(p => { const c = person(p, k); c.settings.width = {unit: '%', size: pct, sizes: []}; c.settings.width_tablet = {unit: '%', size: 48.5, sizes: []}; c.settings.width_mobile = {unit: '%', size: 100, sizes: []}; return c; }); return C(items, {dir: 'row', wrap: true, gap, pad: Z, justify: 'flex-start', align: 'stretch'}); };
  const head = txt => { const h = H(txt, 'h2'); Object.assign(h.settings, {typography_typography: 'custom', typography_font_family: 'Plus Jakarta Sans', typography_font_weight: '700', typography_font_size: px(30), typography_font_size_tablet: px(28), typography_font_size_mobile: px(24), typography_word_spacing: WS, title_color: '#073C64'}); return h; };
  const sec = (title, rows, bg) => Sec([head(title), ...rows], {bg, pt: 48, pb: 48});
  const els = [Banner('Tenaga Kependidikan', crumb('Tenaga Kependidikan', 'Tentang Kami')),
    sec('Koordinator', [row(D.koor, 'koor', 3, 20)], T.white),
    sec('Teknisi dan Laboran', [row(D.tek, 'tek', 4, 20)], T.bg),
    sec('Staf', [row(D.staf.slice(0, 3), 'staf', 3, 20), row(D.staf.slice(3, 6), 'staf', 3, 20), row(D.staf.slice(6, 9), 'staf', 3, 20)], T.white)];
  const zero = (a, d) => a.forEach(e => { if (e.elType === 'container' && d > 0 && !e.settings.padding) e.settings.padding = {unit: 'px', top: '0', right: '0', bottom: '0', left: '0', isLinked: true}; zero(e.elements || [], d + 1); }); zero(els, 0);
  return await simpan(halamanId, els, {});
};
