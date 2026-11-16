// Revisi QC 16 Nov 2026 (skala font, spasi, kontras) untuk halaman v2 di web UGM.
// Dipakai sebagai opsi `ubah` pada deployV2 (docs/deploy-ugm/deploy-v2.js; versi repo perlu patch: lihat README "opsi ubah/sumber/js").
//   deployV2('sejarah-v2', {ubah: els => { skalaFont2(els); tataPage('sejarah-v2', els); }})
// Skala: H1 hero 80 -> 56/44/32 (desktop/tablet/mobile), H2 56 -> 40/34/28, judul 38-52 -> 34/28/24;
//        text-editor minimal 17 (mobile 16), warna #636363; globals warna/tipografi yang tak terselesaikan dibuang.
const px = v => ({unit: 'px', size: v, sizes: []});
const setF = (st, d, t, m) => { st.typography_typography = 'custom'; st.typography_font_size = px(d); st.typography_font_size_tablet = px(t); st.typography_font_size_mobile = px(m); };
window.skalaFont2 = function (els) {
  const DEF = {title_color: '#161616', text_color: '#636363', button_text_color: '#161616', number_color: '#161616'};
  const w = o => {
    if (Array.isArray(o)) { o.forEach(w); return; }
    if (!o || typeof o !== 'object') return;
    const st = o.settings, t = o.widgetType;
    if (st && st.__globals__) for (const [k, v] of Object.entries(st.__globals__)) if (/globals\/(colors|typography)/.test(v || '')) { delete st.__globals__[k]; if (/colors/.test(v) && !st[k] && DEF[k]) st[k] = DEF[k]; }
    if (st && t === 'heading') { if (!st.title_color) st.title_color = '#161616'; const s = (st.typography_font_size || {}).size; if (s >= 72) setF(st, 56, 44, 32); else if (s >= 52) setF(st, 40, 34, 28); else if (s >= 38) setF(st, 34, 28, 24); }
    if (st && t === 'text-editor') {
      const s = (st.typography_font_size || {}).size;
      if (!s || s < 17) { st.typography_typography = 'custom'; st.typography_font_size = px(17); if (!st.typography_font_family) st.typography_font_family = 'Barlow'; }
      if (!st.text_color) st.text_color = '#636363';
      if (['#7A7A7A', '#999999', '#888888', '#8A8A8A', '#9A9A9A'].includes(String(st.text_color).toUpperCase())) st.text_color = '#4A4A4A';
      const m = (st.typography_font_size_mobile || {}).size; if (!m || m < 16) st.typography_font_size_mobile = px(16);
    }
    (o.elements || []).forEach(w);
  };
  w(els);
};
// kartu berita ElementsKit (3 kolom) rata tinggi: gambar 16:10, tombol di dasar
const CSS_EQ = '.post-items{display:grid!important;grid-template-columns:repeat(3,1fr);gap:24px;margin:0!important}.post-item{width:auto!important;max-width:none!important;flex:none!important;padding:0!important;margin:0!important;display:flex}.elementskit-post-image-card{display:flex;flex-direction:column;width:100%;height:100%}.elementskit-entry-header img{width:100%;aspect-ratio:16/10;object-fit:cover;display:block}.elementskit-post-body{flex:1;display:flex;flex-direction:column}.elementskit-post-body .btn-wraper,.elementskit-post-body .post-footer{margin-top:auto}@media(max-width:1024px){.post-items{grid-template-columns:repeat(2,1fr)}}@media(max-width:767px){.post-items{grid-template-columns:1fr}}';
const cssSelector = css => css.split('}').filter(Boolean).map(r => { if (r.startsWith('@media')) { const i = r.indexOf('{'); return r.slice(0, i + 1) + 'selector ' + r.slice(i + 1) + '}'; } return 'selector ' + r + '}'; }).join('');
window.tataPage = function (slug, els) {
  const w = o => {
    if (Array.isArray(o)) { o.forEach(w); return; }
    if (!o || typeof o !== 'object') return;
    const st = o.settings || {};
    if (o.widgetType === 'elementskit-blog-posts' && st.ekit_blog_posts_column !== 'ekit-col-12') st.custom_css = cssSelector(CSS_EQ);
    if (slug === 'akreditasi' && o.widgetType === 'heading' && (st.typography_font_size || {}).size === 32) { st.typography_font_size = px(22); st.typography_font_size_tablet = px(20); st.typography_font_size_mobile = px(18); st.align = 'center'; st.title_color = '#333333'; }
    if (slug === 'sejarah-v2' && o.elType === 'container') {
      if (['row', 'row-reverse'].includes(st.flex_direction) && (o.elements || []).length >= 2 && (o.elements || []).some(x => x.widgetType === 'text-editor' || x.widgetType === 'heading') && (st.padding || {}).top !== '32') { st.flex_direction_mobile = 'column'; st.flex_gap_mobile = {column: '6', row: '6', isLinked: true, unit: 'px', size: 6}; }
      const p = st.padding; if (p && p.top === '40' && p.right === '50') st.padding_mobile = {unit: 'px', top: '24', right: '16', bottom: '24', left: '16', isLinked: false};
    }
    (o.elements || []).forEach(w);
  };
  w(els);
};
'revisi-qc siap'
