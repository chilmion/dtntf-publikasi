// Akreditasi (revisi dosen 18 Nov 2026: 5 slot sertifikat). Diuji di v1 (halaman 727).
// tf.ugm.ac.id: tab wp-admin biasa -> await deployAkreditasi(16893). Syarat: 5 berkas sertifikat sudah ada di pustaka media (slug mengandung "akreditasi-1".."akreditasi-5"; urutan: 1 LAM TN, 2 IABEE TN, 3 LAM TF, 4 IABEE TF, 5 LAM Magister).
// Di jurusan ada kotak ke-6 "Berkas sertifikat akan ditambahkan" -> dibuang (jadi 5 slot).
window.deployAkreditasi = async function (halamanId) {
  if (!window.R) { const t = await (await fetch('https://raw.githubusercontent.com/chilmion/dtntf-publikasi/main/docs/deploy-ugm/rancang.js', {cache: 'no-store'})).text(); (0, eval)(t); }
  const {Banner, Sec, Head, Card, H, Pg, C, crumb, simpan, Im} = R; const Z = [0, 0, 0, 0];
  const med = await (await fetch('/wp-json/wp/v2/media?per_page=30&search=akreditasi&_fields=id,source_url,slug', {headers: {'X-WP-Nonce': wpApiSettings.nonce}})).json();
  const M = {}; med.forEach(m => { const k = (m.slug.match(/akreditasi-(\d)/) || [])[1]; if (k && !M[k]) M[k] = {id: m.id, url: m.source_url}; });
  if (Object.keys(M).length < 5) throw new Error('berkas sertifikat kurang: ' + Object.keys(M).join(','));
  const G = [
    {n: 'S1 Teknik Nuklir', items: [['LAM Teknik', M[1], 'Akreditasi LAM Teknik Program Studi S1 Teknik Nuklir'], ['IABEE', M[2], 'Akreditasi IABEE Program Studi S1 Teknik Nuklir']]},
    {n: 'S1 Teknik Fisika', items: [['LAM Teknik', M[3], 'Akreditasi LAM Teknik Program Studi S1 Teknik Fisika'], ['IABEE', M[4], 'Akreditasi IABEE Program Studi S1 Teknik Fisika']]},
    {n: 'Magister Teknik Fisika', items: [['LAM Teknik', M[5], 'Akreditasi LAM Teknik Program Magister, Program Studi Teknik Fisika']]}];
  const cert = (lem, m, alt) => { const im = Im(m.url, m.id, {alt, ratio: '1.41/1', radius: 10}); im.settings.link_to = 'custom'; im.settings.link = {url: m.url, is_external: 'on', nofollow: '', custom_attributes: ''}; im.settings.custom_css += 'selector img{object-fit:contain;background:#F5F5F5;border:1px solid #E3E3E3;transition:transform .3s}selector a:hover img{transform:scale(1.02)}';
    return Card([im, H(lem, 'h3'), Pg(alt, {small: true, color: '#4A4A4A'})], {gap: 12, pad: [16, 16, 20, 16], padM: [14, 14, 18, 14]}); };
  const col = g => C([H(g.n, 'h2'), ...g.items.map(i => cert(i[0], i[1], i[2]))], {gap: 18, pad: Z, w: 31.4, wT: 48, wM: 100, align: 'stretch'});
  const els = [Banner('Akreditasi', crumb('Akreditasi', 'Tentang Kami')),
    Sec([Head('Sertifikat akreditasi', 'Akreditasi program studi dari LAM Teknik dan IABEE. Klik sertifikat untuk melihat berkas lengkap.'), C(G.map(col), {dir: 'row', gap: 24, pad: Z, wrap: true, align: 'flex-start'})], {pt: 56, pb: 72})];
  const px = v => ({unit: 'px', size: v, sizes: []});
  const fix = a => a.forEach(e => { if (e.widgetType === 'heading' && e.settings.header_size === 'h2' && G.some(g => g.n === e.settings.title)) Object.assign(e.settings, {typography_typography: 'custom', typography_font_family: 'Plus Jakarta Sans', typography_font_weight: '700', typography_font_size: px(30), typography_font_size_tablet: px(28), typography_font_size_mobile: px(26), title_color: '#073C64'}); fix(e.elements || []); }); fix(els);
  const zero = (a, d) => a.forEach(e => { if (e.elType === 'container' && d > 0 && !e.settings.padding) e.settings.padding = {unit: 'px', top: '0', right: '0', bottom: '0', left: '0', isLinked: true}; zero(e.elements || [], d + 1); }); zero(els, 0);
  return await simpan(halamanId, els, {});
};
