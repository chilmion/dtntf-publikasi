// Pustaka pembangun halaman v2 DTNTF (Elementor JSON) — tempel/eval di tab wp-admin tf.ugm.ac.id.
// Satu sumber untuk ukuran/jarak/warna supaya semua halaman dalam seragam.
//   const R = window.R;  R.Banner(...), R.Sec([...]), R.H(...), R.Pg(...), R.Card(...), R.Grid(...), await R.simpan(id, els, settings)
// Catatan: custom_css Elementor mengubah '>' menjadi '&gt;' — jangan memakai child combinator di custom_css.
(function () {
  const T = {navy: '#073C64', dark: '#1A2C43', blue: '#003D79', lime: '#C8E86D', bg: '#F5F5F5', ink: '#161616', body: '#333333', muted: '#636363', line: '#E3E3E3', white: '#FFFFFF'};
  const rid = () => ('0000000' + Math.floor(Math.random() * 0xfffffff).toString(16)).slice(-7);
  const S = n => ({unit: 'px', size: n, sizes: []});
  const P4 = (t, r, b, l) => ({unit: 'px', top: String(t), right: String(r), bottom: String(b), left: String(l), isLinked: false});
  // [desktop, tablet, mobile, line-height, letter-spacing px (desktop), family, weight]
  const TY = {
    h1: [48, 40, 32, 1.12, -1.2, 'Plus Jakarta Sans', 400],
    h2: [36, 30, 28, 1.15, -0.72, 'Plus Jakarta Sans', 400],
    h3: [22, 22, 20, 1.3, -0.22, 'Plus Jakarta Sans', 500],
    p: [17, 16, 16, 1.6, 0, 'Barlow', 400],
    s: [15, 15, 14, 1.5, 0, 'Barlow', 400]
  };
  const ty = (k, over) => {
    const [d, t, m, lh, ls, ff, fw] = TY[k];
    return Object.assign({typography_typography: 'custom', typography_font_family: ff, typography_font_size: S(d), typography_font_size_tablet: S(t), typography_font_size_mobile: S(m), typography_font_weight: String(fw), typography_line_height: {unit: 'em', size: lh, sizes: []}, typography_letter_spacing: S(ls)}, over || {});
  };
  const wd = (type, settings) => ({id: rid(), elType: 'widget', widgetType: type, settings, elements: []});
  const clean = o => JSON.parse(JSON.stringify(o));

  function H(text, lv, o) {
    o = o || {}; lv = lv || 'h2';
    const k = lv === 'h1' ? 'h1' : lv === 'h2' ? 'h2' : 'h3';
    return wd('heading', Object.assign({title: text, header_size: lv, align: o.align || 'left', title_color: o.color || (o.dark ? T.white : T.ink)}, ty(k, o.ty)));
  }
  function Pg(html, o) {
    o = o || {};
    const s = Object.assign({editor: html, text_color: o.color || (o.dark ? 'rgba(255,255,255,0.9)' : T.body), align: o.align || 'left'}, ty(o.small ? 's' : 'p'));
    if (o.max) { s._element_width = 'initial'; s._element_custom_width = {unit: 'px', size: o.max, sizes: []}; }
    if (o.css) s.custom_css = o.css;
    return wd('text-editor', s);
  }
  function B(text, url, o) {
    o = o || {}; const pri = !o.outline;
    return wd('button', {text, link: {url: url || '#', is_external: o.ext ? 'on' : '', nofollow: '', custom_attributes: ''}, align: o.align || 'left', background_color: pri ? T.lime : 'rgba(0,0,0,0)', button_text_color: pri ? T.navy : (o.dark ? T.white : T.navy), border_border: pri ? '' : 'solid', border_width: {unit: 'px', top: '2', right: '2', bottom: '2', left: '2', isLinked: true}, border_color: o.dark ? T.white : T.navy, border_radius: {unit: 'px', top: '999', right: '999', bottom: '999', left: '999', isLinked: true}, text_padding: P4(14, 28, 14, 28), typography_typography: 'custom', typography_font_family: 'Barlow', typography_font_size: S(16), typography_font_weight: '600'});
  }
  function Im(url, id, o) {
    o = o || {};
    return wd('image', {image: {url, id: id || '', size: '', alt: o.alt || '', source: 'library'}, image_size: 'full', align: 'center', width: {unit: '%', size: 100, sizes: []},
      custom_css: 'selector img{width:100%;height:' + (o.h || 'auto') + ';object-fit:cover;aspect-ratio:' + (o.ratio || 'auto') + ';border-radius:' + (o.radius === undefined ? 12 : o.radius) + 'px;display:block}'});
  }
  // container: o = {dir, gap, pad:[t,r,b,l], padT/padM (tablet/mobile), bg, w (% lebar anak), wT, wM, align, justify, wrap, radius, border, boxed (px), full, css, minH}
  function C(children, o) {
    o = o || {};
    const g = o.gap === undefined ? 16 : o.gap;
    const s = {content_width: o.boxed ? 'boxed' : 'full', flex_direction: o.dir || 'column', flex_gap: {unit: 'px', column: String(g), row: String(g), isLinked: true, size: g}};
    if (o.boxed) s.boxed_width = S(o.boxed);
    if (o.pad) s.padding = P4.apply(null, o.pad);
    if (o.padT) s.padding_tablet = P4.apply(null, o.padT);
    if (o.padM) s.padding_mobile = P4.apply(null, o.padM);
    if (o.bg) { s.background_background = 'classic'; s.background_color = o.bg; }
    if (o.grad) { s.background_background = 'gradient'; s.background_color = o.grad[0]; s.background_color_b = o.grad[1]; s.background_gradient_angle = {unit: 'deg', size: o.grad[2] || 135, sizes: []}; }
    if (o.w) s.width = {unit: '%', size: o.w, sizes: []};
    if (o.wT) s.width_tablet = {unit: '%', size: o.wT, sizes: []};
    if (o.wM) s.width_mobile = {unit: '%', size: o.wM, sizes: []};
    if (o.px) s.width = {unit: 'px', size: o.px, sizes: []};
    if (o.align) s.flex_align_items = o.align;
    if (o.justify) s.flex_justify_content = o.justify;
    if (o.wrap) s.flex_wrap = 'wrap';
    if (o.dirT) s.flex_direction_tablet = o.dirT;
    if (o.dirM) s.flex_direction_mobile = o.dirM;
    if (o.radius !== undefined) s.border_radius = {unit: 'px', top: String(o.radius), right: String(o.radius), bottom: String(o.radius), left: String(o.radius), isLinked: true};
    if (o.border) { s.border_border = 'solid'; s.border_width = {unit: 'px', top: '1', right: '1', bottom: '1', left: '1', isLinked: true}; s.border_color = o.border === true ? T.line : o.border; }
    if (o.minH) s.min_height = S(o.minH);
    if (o.css) s.custom_css = o.css;
    return {id: rid(), elType: 'container', settings: s, elements: children.filter(Boolean)};
  }
  // seksi lebar penuh: latar + jarak vertikal 64/48/40, isi 1180px
  function Sec(children, o) {
    o = o || {};
    const pt = o.pt === undefined ? 64 : o.pt, pb = o.pb === undefined ? 64 : o.pb;
    return C(children, Object.assign({boxed: 1180, gap: o.gap === undefined ? 32 : o.gap, pad: [pt, 24, pb, 24], padT: [Math.round(pt * .8), 24, Math.round(pb * .8), 24], padM: [Math.round(pt * .65), 20, Math.round(pb * .65), 20]}, o.c || {}, o.bg ? {bg: o.bg} : {}, o.grad ? {grad: o.grad} : {}, o.css ? {css: o.css} : {}));
  }
  // judul bagian: H2 + pengantar opsional
  function Head(title, intro, o) {
    o = o || {};
    return C([H(title, 'h2', {dark: o.dark, align: o.align}), intro ? Pg(intro, {dark: o.dark, max: 720, align: o.align}) : null], {gap: 12, align: o.align === 'center' ? 'center' : undefined});
  }
  const accent = () => C([], {px: 64, minH: 4, bg: T.lime, radius: 2, gap: 0});
  // banner halaman dalam: crumbs = [[label, url?], ...]
  function Banner(title, crumbs) {
    const cr = (crumbs || []).map(c => c[1] ? '<a href="' + c[1] + '">' + c[0] + '</a>' : c[0]).join(' &nbsp;/&nbsp; ');
    return Sec([
      crumbs ? Pg(cr, {small: true, color: 'rgba(255,255,255,0.8)', css: 'selector a{color:#fff;text-decoration:underline;text-underline-offset:3px}selector a:hover{color:#C8E86D}'}) : null,
      H(title, 'h1', {dark: true}),
      accent()
    ], {pt: 56, pb: 56, gap: 14, grad: [T.navy, T.dark, 135]});
  }
  function Card(children, o) {
    o = o || {};
    return C(children, Object.assign({bg: T.white, radius: 16, border: true, pad: [28, 28, 28, 28], padM: [22, 20, 22, 20], gap: 12}, o));
  }
  // grid kartu: cols desktop (tablet 2, mobile 1), lebar anak dihitung dari jarak
  function Grid(items, o) {
    o = o || {}; const cols = o.cols || 3, gap = o.gap === undefined ? 24 : o.gap;
    const pct = n => Math.floor((100 - ((n - 1) * gap / 11.8)) / n * 100) / 100;
    items.forEach(it => { it.settings.width = {unit: '%', size: pct(cols), sizes: []}; it.settings.width_tablet = {unit: '%', size: pct(2), sizes: []}; it.settings.width_mobile = {unit: '%', size: 100, sizes: []}; });
    return C(items, {dir: 'row', wrap: true, gap, align: o.align || 'stretch'});
  }

  // normalisasi gaya widget yang sudah ada (heading/teks/tombol/gambar/kartu) mengikuti skala standar
  function norm(els, o) {
    o = o || {};
    const DARK = ['#073C64', '#1A2C43', '#003D79'];
    const stripTy = s => { Object.keys(s).forEach(k => { if (/^typography_|^title_typography|^text_typography/.test(k)) delete s[k]; }); if (s.__globals__) { Object.keys(s.__globals__).forEach(k => { if (/typography|color/i.test(k)) delete s.__globals__[k]; }); } };
    const walk = (arr, ctx) => (arr || []).forEach(n => {
      const s = n.settings || (n.settings = {});
      if (n.elType === 'container') {
        const bg = (s.background_color || '').toUpperCase();
        const dark = ctx.dark || DARK.includes(bg) || s.background_background === 'gradient';
        const card = bg === '#FFFFFF' && ctx.depth > 0;
        if (card) { s.border_radius = {unit: 'px', top: '16', right: '16', bottom: '16', left: '16', isLinked: true}; s.border_border = 'solid'; s.border_width = {unit: 'px', top: '1', right: '1', bottom: '1', left: '1', isLinked: true}; s.border_color = T.line; }
        walk(n.elements, {dark, card: ctx.card || card, depth: ctx.depth + 1});
        return;
      }
      if (n.widgetType === 'heading') {
        const sz = (s.header_size || 'h2').toLowerCase(); stripTy(s);
        const lvl = sz === 'h1' ? 'h1' : sz === 'h2' ? 'h2' : (sz === 'h3' || sz === 'h4') ? 'h3' : 'role';
        if (lvl === 'role') Object.assign(s, ty('s', {typography_font_weight: '600', typography_font_family: 'Barlow'}), {title_color: ctx.dark ? 'rgba(255,255,255,0.85)' : T.navy});
        else Object.assign(s, ty(lvl), {title_color: ctx.dark ? T.white : T.ink});
      } else if (n.widgetType === 'text-editor') {
        stripTy(s); Object.assign(s, ty(ctx.card ? 's' : 'p'), {text_color: ctx.dark ? 'rgba(255,255,255,0.9)' : (ctx.card ? T.muted : T.body)});
      } else if (n.widgetType === 'button') {
        stripTy(s); Object.assign(s, {typography_typography: 'custom', typography_font_family: 'Barlow', typography_font_size: S(15), typography_font_weight: '600'});
      } else if (n.widgetType === 'image') {
        s.image_border_radius = {unit: 'px', top: '12', right: '12', bottom: '12', left: '12', isLinked: true};
      }
      walk(n.elements, ctx);
    });
    walk(els, {dark: false, card: false, depth: 0});
    return els;
  }
  const crumb = (title, grup, grupUrl) => [['Beranda', '/new/'], grup ? [grup, grupUrl || ''] : null, [title]].filter(Boolean);

  // simpan dokumen Elementor halaman (status dipertahankan 'publish' kecuali opsi)
  async function simpan(id, elements, settings, status) {
    const html = await (await fetch('/wp-admin/post.php?post=' + id + '&action=elementor', {credentials: 'include'})).text();
    const en = (html.match(/"ajax":\{"url":"[^"]+","nonce":"([a-f0-9]{10})"/) || [])[1];
    if (!en) throw new Error('nonce Elementor tidak ketemu');
    const st = Object.assign({}, settings || {}); delete st.post_title; delete st.post_status;
    const body = new URLSearchParams({action: 'elementor_ajax', _nonce: en, editor_post_id: String(id), actions: JSON.stringify({a: {action: 'save_builder', data: {status: status || 'publish', elements: clean(elements), settings: Object.assign({template: 'elementor_header_footer'}, st)}}})});
    const r = await fetch('/wp-admin/admin-ajax.php', {method: 'POST', credentials: 'include', body});
    const tx = await r.text();
    if (!(r.ok && !/"success":false/.test(tx))) throw new Error('simpan: ' + tx.slice(0, 120));
    return 'ok ' + id;
  }
  window.R = {T, TY, rid, S, P4, ty, wd, H, Pg, B, Im, C, Sec, Head, accent, Banner, Card, Grid, crumb, simpan, clean, norm};
  return 'R siap';
})();
