// Struktur Organisasi (revisi dosen 18 Nov 2026: resolusi). Bagan digambar ulang sebagai SVG vektor (tajam di semua ukuran), warna tema.
// Diuji di v1 (halaman 1620). tf.ugm.ac.id: tab wp-admin biasa -> await deployStruktur(16890) ; lalu di editor halaman: nolPadding() (sejarah.js)
window.deployStruktur = async function (halamanId) {
  if (!window.R) { const t = await (await fetch('https://raw.githubusercontent.com/chilmion/dtntf-publikasi/main/docs/deploy-ugm/rancang.js', {cache: 'no-store'})).text(); (0, eval)(t); }
  const {Banner, Sec, Head, Grid, Card, H, Pg, B, C, crumb, wd, simpan, T} = R;
  const NAVY = '#073C64', LINE = '#3F5F7A';
  const tx = (x, y, lines, col, fs, wt) => '<text x="' + x + '" y="' + (y - (lines.length - 1) * (fs * 0.6)) + '" text-anchor="middle" fill="' + col + '" font-size="' + fs + '" font-weight="' + (wt || 700) + '">' + lines.map((l, i) => '<tspan x="' + x + '" dy="' + (i ? fs * 1.25 : 0) + '">' + l + '</tspan>').join('') + '</text>';
  const bx = (x, y, w, h, fill, stroke, lines, col, fs) => '<rect x="' + x + '" y="' + y + '" width="' + w + '" height="' + h + '" rx="8" fill="' + fill + '" ' + (stroke ? 'stroke="' + stroke + '" stroke-width="2.5"' : '') + '/>' + tx(x + w / 2, y + h / 2 + fs * 0.35, lines, col, fs || 13);
  const ln = (d, dash, arrow) => '<path d="' + d + '" fill="none" stroke="' + (dash ? '#1A2C43' : LINE) + '" stroke-width="' + (dash ? 1.8 : 3) + '" ' + (dash ? 'stroke-dasharray="5 4" ' : '') + 'stroke-linejoin="round"' + (arrow ? ' marker-end="url(#a)"' : '') + (arrow == 2 ? ' marker-start="url(#a)"' : '') + '/>';
  let s = '';
  s += ln('M530,64 V355'); s += ln('M530,125 H360'); s += ln('M530,195 H580'); s += ln('M530,90 H965 V130');
  s += ln('M255,145 V273'); s += ln('M255,196 H230'); s += ln('M255,273 H230'); s += ln('M255,214 H290');
  s += ln('M160,355 H830'); s += ln('M160,355 V380'); s += ln('M400,355 V380'); s += ln('M640,355 V380'); s += ln('M830,355 V380');
  s += ln('M85,430 V530'); s += ln('M325,430 V530'); s += ln('M565,430 V470'); s += ln('M805,430 V698');
  [[85, 470], [85, 530], [325, 470], [325, 530], [565, 470]].forEach(a => { s += ln('M' + a[0] + ',' + a[1] + ' H' + (a[0] + 25)); });
  [470, 530, 590, 650, 710].forEach(y => { s += ln('M805,' + y + ' H830'); });
  s += ln('M620,42 H1085 V190 H1060', true, 1);
  s += ln('M870,215 H800 V335 H160', true); s += ln('M160,335 V376', true, 1); s += ln('M400,335 V376', true, 1); s += ln('M640,335 V376', true, 1);
  s += ln('M965,262 C965,322 930,322 930,376', true, 2);
  s += bx(440, 20, 180, 44, NAVY, null, ['Ketua Departemen'], '#fff', 14);
  s += bx(150, 105, 210, 40, '#fff', NAVY, ['Kantor Urusan Administrasi'], '#161616', 13);
  s += bx(40, 170, 190, 52, '#1B7F3B', null, ['Kour Aset, Sarana Prasarana,', 'SHE dan IT'], '#fff', 12.5);
  s += bx(40, 236, 190, 74, '#1B6E94', null, ['Kour Administrasi Umum, SDM,', 'Penelitian, Pengabdian pada', 'Masyarakat, dan Kerjasama'], '#fff', 12.5);
  s += bx(290, 190, 210, 48, '#8E1B3A', null, ['Kour Akademik,', 'Kemahasiswaan dan Alumni'], '#fff', 12.5);
  s += bx(580, 172, 170, 44, '#1A6B6B', null, ['Sekretaris Departemen'], '#fff', 13);
  s += '<rect x="870" y="130" width="190" height="132" rx="8" fill="#fff" stroke="#5B3FA8" stroke-width="2"/><rect x="870" y="130" width="190" height="24" rx="8" fill="#5B3FA8"/><rect x="870" y="142" width="190" height="12" fill="#5B3FA8"/>' + tx(965, 147, ['KBK'], '#fff', 12.5);
  [['KBK 1', 888, 166], ['KBK 2', 944, 166], ['KBK 3', 1000, 166], ['KBK ...', 916, 214]].forEach(k => { s += '<rect x="' + k[1] + '" y="' + k[2] + '" width="48" height="36" rx="4" fill="#fff" stroke="#1A2C43" stroke-width="1.5"/>' + tx(k[1] + 24, k[2] + 22, [k[0]], '#161616', 11, 600); });
  s += bx(60, 380, 200, 50, '#fff', NAVY, ['Program Studi Sarjana', 'Teknik Nuklir'], '#161616', 13);
  s += bx(300, 380, 200, 50, '#fff', NAVY, ['Program Studi Sarjana', 'Teknik Fisika'], '#161616', 13);
  s += bx(540, 380, 200, 50, '#fff', NAVY, ['Program Studi Magister', 'Teknik Fisika'], '#161616', 13);
  s += bx(780, 380, 200, 50, '#fff', NAVY, ['Laboratorium'], '#161616', 14);
  [[110, 450, 'Ketua Program Studi'], [110, 510, 'Sekretaris Program Studi'], [350, 450, 'Ketua Program Studi'], [350, 510, 'Sekretaris Program Studi'], [590, 450, 'Ketua Program Studi']].forEach(a => { s += bx(a[0], a[1], 180, 40, '#8E1B3A', null, [a[2]], '#fff', 12.5); });
  [['Kepala Laboratorium Sensor', 'dan Sistem Telekontrol'], ['Kepala Laboratorium Energi', 'Terbarukan'], ['Kepala Laboratorium', 'Teknologi Energi Nuklir'], ['Kepala Laboratorium Teknologi', 'Proses dan Kimia Nuklir'], ['Kepala Laboratorium', 'Komputasi Multifisika']].forEach((l, i) => { s += bx(830, 446 + i * 60, 250, 48, '#6B5B95', null, l, '#fff', 12.5); });
  s += tx(850, 30, ['Penelitian, Pengabdian pada Masyarakat, Kerjasama, SDM Dosen'], '#1A2C43', 11.5, 600);
  s += tx(300, 327, ['Akademik dan Jaminan Mutu'], '#1A2C43', 11.5, 600);
  s += tx(1000, 312, ['Penelitian'], '#1A2C43', 11.5, 600);
  const svg = '<div class="dt-bagan"><svg viewBox="0 0 1100 770" role="img" aria-label="Bagan struktur organisasi Departemen Teknik Nuklir dan Teknik Fisika" font-family="Plus Jakarta Sans, Barlow, sans-serif"><defs><marker id="a" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#1A2C43"/></marker></defs>' + s + '</svg></div><style>.dt-bagan{overflow-x:auto;-webkit-overflow-scrolling:touch}.dt-bagan svg{display:block;width:100%;min-width:760px;height:auto}</style>';
  // Kartu program studi bergaya bento (foto latar + gradasi, ukuran 62/36 bergantian). Foto = Unsplash (ilustrasi), diunggah sekali ke pustaka situs.
  const FOTO = {tn: '1630142895963-6996ae6b3a5b', tf: '1781330189305-d92d518dc28d', iup: '1766297247924-6638d54e7c89', mtf: '1759328381007-64559a862aa6'};
  const U = JSON.parse(localStorage.getItem('__prodiFoto') || '{}');
  for (const [k, id] of Object.entries(FOTO)) {
    if (U[k]) continue;
    const bl = await (await fetch('https://images.unsplash.com/photo-' + id + '?w=1200&fm=jpg&q=78&fit=max')).blob();
    const j = await (await fetch('/wp-json/wp/v2/media', {method: 'POST', headers: {'X-WP-Nonce': wpApiSettings.nonce, 'Content-Disposition': 'attachment; filename="prodi-' + k + '.jpg"', 'Content-Type': 'image/jpeg'}, body: bl})).json();
    if (!j.id) throw new Error('unggah foto gagal ' + k); U[k] = {id: j.id, url: j.source_url}; localStorage.setItem('__prodiFoto', JSON.stringify(U));
  }
  const Z = [0, 0, 0, 0];
  const PR = [
    {n: 'S1 Teknik Nuklir', d: 'Program sarjana teknologi nuklir.', u: '/prodi/', f: U.tn, w: 62, h: 360},
    {n: 'S1 Teknik Fisika', d: 'Program sarjana fisika terapan.', u: '/prodi-s1-teknik-fisika/', f: U.tf, w: 36, h: 360},
    {n: 'IUP Teknik Nuklir', d: 'Program sarjana internasional.', u: '/iup-teknik-nuklir/', f: U.iup, w: 36, h: 300},
    {n: 'Magister Teknik Fisika', d: 'Program magister.', u: '/program-studi-magister-teknik-fisika/', f: U.mtf, w: 62, h: 300}];
  const arrow = '<span class="dt-arr"><svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="#073C64" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg></span><style>.dt-arr{display:flex;align-items:center;justify-content:center;width:46px;height:46px;border-radius:50%;background:#C8E86D;transition:transform .3s}</style>';
  const card = p => {
    const h = H(p.n, 'h3', {dark: true}); h.settings.link = {url: p.u, is_external: '', nofollow: '', custom_attributes: ''};
    Object.assign(h.settings, {typography_font_size: {unit: 'px', size: 30, sizes: []}, typography_font_size_mobile: {unit: 'px', size: 26, sizes: []}, typography_font_weight: '600'});
    const d = Pg(p.d, {dark: true, css: 'selector,selector p{font-size:17px;margin:0;color:rgba(255,255,255,.92)}'});
    const a = wd('html', {html: arrow, custom_css: 'selector{position:absolute;top:24px;right:24px;z-index:6}'});
    const c = C([a, h, d], {dir: 'column', justify: 'flex-end', gap: 8, pad: [28, 28, 28, 28], padM: [22, 20, 22, 20], radius: 20, minH: p.h, w: p.w, wT: 100, wM: 100, css: 'selector{position:relative;overflow:hidden;transition:transform .35s ease,box-shadow .35s ease}selector:hover{transform:translateY(-4px);box-shadow:0 18px 38px rgba(7,60,100,.28)}selector:hover .dt-arr{transform:translateX(4px)}selector .elementor-heading-title a{color:#fff}selector .elementor-heading-title a::after{content:"";position:absolute;inset:0;z-index:5}'});
    Object.assign(c.settings, {background_background: 'classic', background_image: {url: p.f.url, id: p.f.id, size: '', source: 'library'}, background_position: 'center center', background_size: 'cover', background_overlay_background: 'gradient', background_overlay_color: 'rgba(7,60,100,0.10)', background_overlay_color_b: 'rgba(7,25,50,0.86)', background_overlay_gradient_angle: {unit: 'deg', size: 180, sizes: []}, background_overlay_color_stop: {unit: '%', size: 25, sizes: []}, background_overlay_opacity: {unit: 'px', size: 1, sizes: []}});
    return c;
  };
  const row = (a, b) => C([card(a), card(b)], {dir: 'row', dirT: 'column', gap: 20, pad: Z, wrap: true, align: 'stretch'});
  const els = [Banner('Struktur Organisasi', crumb('Struktur Organisasi', 'Tentang Kami')),
    Sec([Head('Bagan organisasi', 'Susunan organisasi Departemen Teknik Nuklir dan Teknik Fisika, Fakultas Teknik UGM.'), Card([wd('html', {html: svg})], {pad: [24, 24, 24, 24], padM: [16, 12, 16, 12]})], {pb: 40}),
    Sec([Head('Program studi di bawah departemen'), C([row(PR[0], PR[1]), row(PR[2], PR[3])], {dir: 'column', gap: 20, pad: Z})], {bg: T.bg, pt: 56, pb: 56})];
  const zero = (a, d) => a.forEach(e => { if (e.elType === 'container' && d > 0 && !e.settings.padding) e.settings.padding = {unit: 'px', top: '0', right: '0', bottom: '0', left: '0', isLinked: true}; zero(e.elements || [], d + 1); }); zero(els, 0);
  return await simpan(halamanId, els, {});
};
