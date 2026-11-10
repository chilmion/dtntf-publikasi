// Tempel ke javascript_tool pada tab wp-admin tf.ugm.ac.id (halaman admin biasa, bukan editor), lalu panggil:
//   await deployHalaman({slug:'andang-widi-harto', judul:'Andang Widi Harto', tpl:'profil/andang-widi-harto', status:'private'})
// tpl = jalur templat di elementor/ (tanpa .json); peta aset otomatis dari data/ugm/peta.json.
// Hasil: {id, status, aset}. Halaman dibuat 'private' (atau 'draft'); JANGAN 'publish' tanpa ACC user.
window.deployHalaman = async function ({slug, judul, tpl, status = 'private', template = 'elementor_header_footer', gambar = {}}) {
  const BASE = 'https://chilmion.github.io/dtntf-publikasi/data';
  const RAW = 'https://raw.githubusercontent.com/chilmion/dtntf-publikasi/main/elementor/';
  const nonce = (window.wpApiSettings || {}).nonce;
  if (!nonce) throw new Error('Buka halaman wp-admin biasa dulu');
  const H = {'X-WP-Nonce': nonce, 'Content-Type': 'application/json'};
  // 1. cari / buat halaman (tidak menimpa slug yang sudah ada milik orang lain)
  const ada = await (await fetch('/wp-json/wp/v2/pages?slug=' + slug + '&status=any&_fields=id,status,author', {credentials: 'include', headers: H})).json();
  let id;
  if (ada.length) { id = ada[0].id; }
  else {
    const r = await fetch('/wp-json/wp/v2/pages', {method: 'POST', credentials: 'include', headers: H, body: JSON.stringify({title: judul, slug, status: 'draft'})});
    const j = await r.json(); if (!j.id) throw new Error('gagal membuat halaman: ' + JSON.stringify(j).slice(0, 150)); id = j.id;
  }
  // 2. nonce Elementor dari halaman editor (GET ini juga mengaktifkan mode Elementor untuk halaman baru)
  const html = await (await fetch('/wp-admin/post.php?post=' + id + '&action=elementor', {credentials: 'include'})).text();
  const en = (html.match(/"_nonce":"([a-f0-9]{10})"/) || [])[1];
  if (!en) throw new Error('nonce Elementor tidak ketemu');
  // 3. templat, peta aset, ubah isi
  const T = await (await fetch(RAW + tpl + '.json', {cache: 'no-store'})).json();
  const peta = await (await fetch(BASE + '/ugm/peta.json', {cache: 'no-store'})).json();
  const aset = peta[tpl] || [];
  const els = JSON.parse(JSON.stringify(T.content));
  const C = {primary: '#161616', secondary: '#414142', text: '#636363', accent: '#E3E3E3', '870ef80': '#073C64', bf890a9: '#1A2C43', b70a650: '#003D79', '15e26ab': '#C8E86D', f184fe1: '#CAC0BE', '1e38924': '#F5F5F5', '5bd60dc': '#FFFFFF'};
  const walk = o => {
    if (Array.isArray(o)) { o.forEach(walk); return; }
    if (!o || typeof o !== 'object') return;
    const st = o.settings;
    if (st && st.__globals__) for (const [k, v] of Object.entries(st.__globals__)) {   // kit v1 -> nilai literal
      const m = /globals\/colors\?id=(.+)/.exec(v || ''); if (m && C[m[1]]) { st[k] = C[m[1]]; delete st.__globals__[k]; }
    }
    if (o.widgetType === 'html' && st && st.html) st.html = st.html.replace(/<!--[\s\S]*?-->/g, '').replace(/<style[^>]*>[\s\S]*?<\/style>/gi, '').replace(/<script[^>]*>[\s\S]*?<\/script>/gi, '').trim();
    if (o.widgetType === 'heading' && st && !st.title_color) st.title_color = '#161616';   // tema UGM memberi biru muda
    if (st) for (const [k, v] of Object.entries(st)) if (v && typeof v === 'object' && typeof v.url === 'string' && gambar[v.url]) { v.id = gambar[v.url].id; v.url = gambar[v.url].url; }
    (o.elements || []).forEach(walk);
  };
  walk(els);
  // 4. pemuat Custom JS (tanpa & < > ")  -- ?v= untuk menembus cache GitHub Pages
  const v = new Date().toISOString().slice(0, 10).replace(/-/g, '');
  const loader = aset.map(n => "(function(){var d=document;var l=d.createElement('link');l.rel='stylesheet';l.href='" + BASE + '/ugm/' + n + ".css?v=" + v + "';d.head.appendChild(l);var s=d.createElement('script');s.src='" + BASE + '/ugm/' + n + ".js?v=" + v + "';d.head.appendChild(s)})();").join('');
  const body = new URLSearchParams({action: 'elementor_ajax', _nonce: en, editor_post_id: String(id), actions: JSON.stringify({a: {action: 'save_builder', data: {status, elements: els, settings: {template, custom_css: '', eael_custom_js: loader}}}})});
  const r = await fetch('/wp-admin/admin-ajax.php', {method: 'POST', credentials: 'include', body});
  const txt = await r.text();
  return {id, http: r.status, aset, ok: r.ok && !/"success":false/.test(txt), cuplikan: txt.slice(0, 120)};
};
'deployHalaman siap'
