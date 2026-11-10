// Halaman v1 siap-deploy (data/staging-v2/<slug>.json dari snapshot) -> web UGM. Tempel/eval di tab wp-admin biasa.
//   await deployV2('sejarah-v2', {publish:true})          // opsi: slug, judul, template, ganti:{a:b}, publish:false
// Prasyarat: gambar sudah diunggah dan petanya ada di localStorage '__peta2' ({namaBerkas:{id,url}}).
window.deployV2 = async function (slugUgm, opsi = {}) {
  const BASE = 'https://chilmion.github.io/dtntf-publikasi/data/staging-v2';
  const H = {'X-WP-Nonce': wpApiSettings.nonce, 'Content-Type': 'application/json'};
  const D = await (await fetch(BASE + '/' + slugUgm + '.json', {cache: 'no-store'})).json();
  const G = await (await fetch(BASE + '/gambar.json', {cache: 'no-store'})).json();
  const M = JSON.parse(localStorage.getItem('__peta2') || '{}');
  const slug = opsi.slug || D.slug;
  let s = JSON.stringify(D.elements), tukar = 0;
  for (const [u, n] of Object.entries(G)) if (M[n] && s.includes(u)) { s = s.split(u).join(M[n].url); tukar++; }
  for (const [a, b] of Object.entries(opsi.ganti || {})) s = s.split(a).join(b);
  const sisaV1 = (s.match(/v1\.katur/g) || []).length;
  const els = JSON.parse(s);
  const byUrl = {}; Object.values(M).forEach(v => byUrl[v.url] = v.id);
  const setId = v => { if (v && typeof v === 'object' && typeof v.url === 'string' && byUrl[v.url] !== undefined && ('id' in v)) v.id = byUrl[v.url]; };
  const walk = o => {
    if (Array.isArray(o)) { o.forEach(walk); return; }
    if (!o || typeof o !== 'object') return;
    const st = o.settings;
    if (o.widgetType === 'html' && st && st.html) st.html = st.html.replace(/<!--[\s\S]*?-->/g, '').replace(/<style[^>]*>[\s\S]*?<\/style>/gi, '').replace(/<script[^>]*>[\s\S]*?<\/script>/gi, '').trim();
    if (st) for (const v of Object.values(st)) { setId(v); if (Array.isArray(v)) v.forEach(it => { if (it && typeof it === 'object') Object.values(it).forEach(setId); }); }
    (o.elements || []).forEach(walk);
  };
  walk(els);
  const ex = await (await fetch('/wp-json/wp/v2/pages?slug=' + slug + '&status=any&_fields=id,status,author', {credentials: 'include', headers: H})).json();
  let id;
  if (ex.length) { if (ex[0].author !== 742) throw new Error('slug dipakai halaman lain: ' + slug + ' id ' + ex[0].id); id = ex[0].id; }
  else {
    const r = await fetch('/wp-json/wp/v2/pages', {method: 'POST', credentials: 'include', headers: H, body: JSON.stringify({title: opsi.judul || D.judul, slug, status: 'draft'})});
    const j = await r.json(); if (!j.id) throw new Error('buat: ' + JSON.stringify(j).slice(0, 120)); id = j.id;
  }
  const html = await (await fetch('/wp-admin/post.php?post=' + id + '&action=elementor', {credentials: 'include'})).text();
  const en = (html.match(/"ajax":\{"url":"[^"]+","nonce":"([a-f0-9]{10})"/) || [])[1];
  if (!en) throw new Error('nonce Elementor tidak ketemu');
  const body = new URLSearchParams({action: 'elementor_ajax', _nonce: en, editor_post_id: String(id), actions: JSON.stringify({a: {action: 'save_builder', data: {status: 'draft', elements: els, settings: {template: opsi.template || 'elementor_header_footer'}}}})});
  const r2 = await fetch('/wp-admin/admin-ajax.php', {method: 'POST', credentials: 'include', body});
  const tx = await r2.text();
  if (!(r2.ok && !/"success":false/.test(tx))) throw new Error('simpan: ' + tx.slice(0, 100));
  let st = 'draft';
  if (opsi.publish !== false) { const p = await fetch('/wp-json/wp/v2/pages/' + id, {method: 'POST', credentials: 'include', headers: H, body: JSON.stringify({status: 'publish'})}); st = (await p.json()).status; }
  return {slug, id, status: st, gambar: tukar, sisaV1};
};
'deployV2 siap'
