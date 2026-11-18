// Fasilitas Umum (revisi dosen 18 Nov 2026): Ruang Tunggu -> Co-working Space; tautan ke fasilitas FT dan UGM; semua dalam kartu bento bergambar.
// Gambar tautan FT/UGM diambil dari web FT UGM (ft.ugm.ac.id) dan Ditmawa UGM, disimpan di data/ugm/fasilitas/*.jpg lalu diunggah ke media situs.
// v1: tab wp-admin biasa -> await deployFasilitas(1693, '<sha>')   ;  tf.ugm.ac.id: halaman fasilitas-umum (cari id lewat slug). Setelah itu: paksa simpan dari editor (CSS) + kernFix tidak perlu (word-spacing sudah diset).
window.deployFasilitas = async function (halamanId, sha) {
  if (!window.R) { const t = await (await fetch('https://raw.githubusercontent.com/chilmion/dtntf-publikasi/main/docs/deploy-ugm/rancang.js', {cache: 'no-store'})).text(); (0, eval)(t); }
  const {Banner, Sec, H, Pg, C, crumb, wd, simpan, T} = R; const Z = [0, 0, 0, 0];
  const H0 = {headers: {'X-WP-Nonce': wpApiSettings.nonce}};
  // 1. unggah gambar baru (sekali)
  const KEYS = ['ft-lab', 'ft-perpustakaan', 'ft-cws', 'ft-ult', 'ft-difabel', 'ft-katalog', 'ft-ti', 'ft-rumahkayu', 'ugm-perpustakaan', 'ugm-kemahasiswaan'];
  let M = JSON.parse(localStorage.getItem('__fasFoto') || '{}');
  for (const k of KEYS) { if (M[k]) continue;
    const b = await (await fetch('https://raw.githubusercontent.com/chilmion/dtntf-publikasi/' + sha + '/data/ugm/fasilitas/' + k + '.jpg')).blob();
    const j = await (await fetch('/wp-json/wp/v2/media', {method: 'POST', headers: {'X-WP-Nonce': wpApiSettings.nonce, 'Content-Disposition': 'attachment; filename="fasilitas-' + k + '.jpg"', 'Content-Type': 'image/jpeg'}, body: b})).json();
    if (!j.id) throw new Error('unggah gagal ' + k); M[k] = {id: j.id, url: j.source_url.replace(location.origin, '')}; localStorage.setItem('__fasFoto', JSON.stringify(M)); }
  // 2. foto fasilitas departemen yang sudah ada di pustaka media
  const cari = async q => { const r = await (await fetch('/wp-json/wp/v2/media?per_page=10&search=' + encodeURIComponent(q) + '&_fields=id,source_url,slug', H0)).json(); if (!r.length) throw new Error('foto tidak ada: ' + q); return {id: r[0].id, url: r[0].source_url.replace(location.origin, '')}; };
  const O = {perpus: await cari('Perpustakaan-20220105'), akademik: await cari('DSC_5917'), cws: await cari('photo_2025-11-23'), toilet: await cari('Wastafel')};
  const px = v => ({unit: 'px', size: v, sizes: []}); const WS = {unit: 'px', size: 0, sizes: []};
  const FTU = 'https://ft.ugm.ac.id/';
  const A = [  // fasilitas departemen (tanpa tautan)
    {n: 'Perpustakaan / Ruang Referensi', d: 'Perpustakaan yang lengkap, representatif, dan nyaman untuk mendukung penelaahan literatur dan penelitian.', img: O.perpus, w: 62, h: 340},
    {n: 'Co-working Space', d: 'Ruang bersama yang nyaman untuk bekerja, belajar, dan berdiskusi bagi tamu, mahasiswa, dan dosen.', img: O.cws, w: 36, h: 340},
    {n: 'Pelayanan Akademik', d: 'Pelayanan yang ramah, cepat, dan responsif untuk kegiatan pendidikan, penelitian, dan pengabdian masyarakat.', img: O.akademik, w: 36, h: 300},
    {n: 'Kamar Mandi / Toilet', d: 'Kamar mandi yang bersih, nyaman, dan representatif untuk berbagai kalangan.', img: O.toilet, w: 62, h: 300}];
  const FT = [
    {n: 'Fasilitas Laboratorium', d: 'Laboratorium di lingkungan Fakultas Teknik UGM.', u: FTU + 'fasilitas-laboratorium/', img: M['ft-lab'], w: 58, h: 300},
    {n: 'Perpustakaan', d: 'Perpustakaan dan fasilitasnya di Fakultas Teknik.', u: FTU + 'perpustakaan-dan-fasilitasnya/', img: M['ft-perpustakaan'], w: 40, h: 300},
    {n: 'Co-Working Space', d: 'Ruang kerja bersama di Fakultas Teknik.', u: FTU + 'co-working-space-di-ft-ugm/', img: M['ft-cws'], w: 31.4, h: 260},
    {n: 'Unit Layanan Terpadu', d: 'Layanan terpadu Fakultas Teknik.', u: FTU + 'unit-layanan-terpadu/', img: M['ft-ult'], w: 31.4, h: 260},
    {n: 'Fasilitas Difabel', d: 'Fasilitas ramah difabel di kampus Fakultas Teknik.', u: FTU + 'fasilitas-difabel/', img: M['ft-difabel'], w: 31.4, h: 260},
    {n: 'Katalog Ruang', d: 'Katalog ruang dan auditorium Fakultas Teknik.', u: FTU + 'katalog-ruang/', img: M['ft-katalog'], w: 31.4, h: 260},
    {n: 'Teknologi Informasi', d: 'Layanan teknologi informasi Fakultas Teknik.', u: FTU + 'teknologi-informasi/', img: M['ft-ti'], w: 31.4, h: 260},
    {n: 'Rumah Kayu', d: 'Rumah Kayu CLT Nusantara, Fakultas Teknik UGM.', u: FTU + 'rumah-clt-nusantara/', img: M['ft-rumahkayu'], w: 31.4, h: 260}];
  const UG = [
    {n: 'Perpustakaan UGM', d: 'Layanan perpustakaan Universitas Gadjah Mada.', u: 'https://lib.ugm.ac.id/', img: M['ugm-perpustakaan'], w: 58, h: 280},
    {n: 'Fasilitas Kemahasiswaan UGM', d: 'Fasilitas kemahasiswaan di UGM (Ditmawa).', u: 'https://ditmawa.ugm.ac.id/fasilitas-kemahasiswaan/', img: M['ugm-kemahasiswaan'], w: 40, h: 280}];
  const arrow = '<span class="dt-arr"><svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="#073C64" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7 17L17 7M9 7h8v8"/></svg></span><style>.dt-arr{display:flex;align-items:center;justify-content:center;width:40px;height:40px;border-radius:50%;background:#C8E86D;transition:transform .3s}</style>';
  const card = p => {
    const big = p.h >= 300, h = H(p.n, 'h3', {dark: true});
    if (p.u) h.settings.link = {url: p.u, is_external: 'on', nofollow: '', custom_attributes: ''};
    Object.assign(h.settings, {typography_typography: 'custom', typography_font_family: 'Plus Jakarta Sans', typography_font_weight: '600', typography_font_size: px(big ? 28 : 22), typography_font_size_mobile: px(22), typography_line_height: {unit: 'em', size: 1.2, sizes: []}, typography_word_spacing: WS, title_color: '#FFFFFF'});
    const d = Pg(p.d, {dark: true, css: 'selector,selector p{font-size:' + (big ? 16 : 15) + 'px;line-height:1.45;margin:0;color:rgba(255,255,255,.92)}'}); Object.assign(d.settings, {typography_typography: 'custom', typography_font_family: 'Barlow', typography_font_size: px(big ? 16 : 15), typography_word_spacing: WS, text_color: 'rgba(255,255,255,.92)'});
    const kids = [h, d]; if (p.u) kids.unshift(wd('html', {html: arrow, custom_css: 'selector{position:absolute;top:18px;right:18px;z-index:6}'}));
    const c = C(kids, {dir: 'column', justify: 'flex-end', gap: 6, pad: [24, 24, 24, 24], padM: [20, 18, 20, 18], radius: 20, minH: p.h, w: p.w, wT: 100, wM: 100, css: 'selector{position:relative;overflow:hidden;transition:transform .35s ease,box-shadow .35s ease}selector:hover{transform:translateY(-4px);box-shadow:0 18px 38px rgba(7,60,100,.28)}selector .elementor-heading-title a{color:#fff}selector .elementor-heading-title a::after{content:"";position:absolute;inset:0;z-index:5}'});
    Object.assign(c.settings, {background_background: 'classic', background_image: {url: p.img.url, id: p.img.id, size: '', source: 'library'}, background_position: 'center center', background_size: 'cover', background_overlay_background: 'gradient', background_overlay_color: 'rgba(7,60,100,0.06)', background_overlay_color_b: 'rgba(7,25,50,0.88)', background_overlay_gradient_angle: {unit: 'deg', size: 180, sizes: []}, background_overlay_color_stop: {unit: '%', size: 30, sizes: []}, background_overlay_opacity: {unit: 'px', size: 1, sizes: []}});
    return c;
  };
  const row = list => C(list.map(card), {dir: 'row', dirT: 'column', gap: 20, pad: Z, wrap: true, align: 'stretch'});
  const head = (txt, sub) => { const h = H(txt, 'h2'); Object.assign(h.settings, {typography_typography: 'custom', typography_font_family: 'Plus Jakarta Sans', typography_font_weight: '700', typography_font_size: px(30), typography_font_size_tablet: px(28), typography_font_size_mobile: px(24), typography_word_spacing: WS, title_color: '#073C64'}); return sub ? C([h, Pg(sub, {css: 'selector,selector p{font-size:17px;color:#4A4A4A;margin:0}'})], {gap: 6, pad: Z}) : h; };
  const sec = (title, sub, rows, bg) => Sec([head(title, sub), C(rows, {dir: 'column', gap: 20, pad: Z})], {bg, pt: 56, pb: 56});
  const els = [Banner('Fasilitas Umum', crumb('Fasilitas Umum', 'Tentang Kami')),
    sec('Fasilitas departemen', 'Fasilitas yang melayani tamu, mahasiswa, dan dosen Departemen Teknik Nuklir dan Teknik Fisika.', [row(A.slice(0, 2)), row(A.slice(2, 4))], T.white),
    sec('Fasilitas Fakultas Teknik', 'Fasilitas bersama di tingkat fakultas. Klik kartu untuk membuka halaman di situs Fakultas Teknik.', [row(FT.slice(0, 2)), row(FT.slice(2, 5)), row(FT.slice(5, 8))], T.bg),
    sec('Fasilitas UGM', 'Layanan dan fasilitas di tingkat universitas.', [row(UG)], T.white)];
  const zero = (a, d) => a.forEach(e => { if (e.elType === 'container' && d > 0 && !e.settings.padding) e.settings.padding = {unit: 'px', top: '0', right: '0', bottom: '0', left: '0', isLinked: true}; zero(e.elements || [], d + 1); }); zero(els, 0);
  return await simpan(halamanId, els, {});
};
