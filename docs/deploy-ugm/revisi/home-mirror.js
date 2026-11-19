// Mirror isi Home tf.ugm.ac.id/new/ (Home v2, id 16487) ke Home v1 (id 265) — 19 Nov 2026, untuk preview rapat.
// Cara: salinan HTML hasil render halaman tf + <link> CSS Elementor-nya ditaruh di SATU widget HTML di v1 (bukan elemen Elementor terpisah, jadi
// tidak bisa disunting per elemen; tampilan = tf). 12 bagian lama Home v1 TIDAK dihapus: disembunyikan (hide_desktop/tablet/mobile), bisa ditampilkan lagi.
// Langkah 1 — di tab tf.ugm.ac.id/new/ (jalankan lalu langsung buka editor v1 di TAB YANG SAMA; window.name ikut terbawa):
//   const pg=document.querySelector('[data-elementor-type="wp-page"]'); const skip=/post-16571|post-10822|header-footer-elementor|nav-menu|widget-search|widget-social|brands\.css|fontawesome|solid\.css|eicons|elementor-icons|inc\/widgets-css|assets\/css\/frontend\.min\.css/i;
//   const css=[...new Set([...document.querySelectorAll('link[rel=stylesheet]')].map(l=>l.href).filter(h=>/elementor|swiper|ekit|elementskit|animations|assets\/css\/(button|common|blog-posts)/i.test(h)&&!skip.test(h)))];
//   const c=pg.cloneNode(true); c.querySelectorAll('script').forEach(s=>s.remove()); window.name=JSON.stringify({css,html:c.outerHTML}); location='https://v1.katur.online/wp-admin/post.php?post=265&action=elementor';
// Langkah 2 — di editor v1 (setelah termuat): await pasangMirrorHome()
window.pasangMirrorHome = async function () {
  const p = JSON.parse(window.name);
  const skip = /mega-menu|opensans|roboto|general\.min|solid\.min|ekiticons|widget-blockquote/i;
  const links = p.css.filter(h => !skip.test(h)).map(h => '<link rel="stylesheet" href="' + h + '">').join('');
  const d = document.createElement('div'); d.innerHTML = p.html;
  // iframe video latar YouTube hasil JS tf diganti penampung kosong: Elementor v1 membuat ulang pemutarnya sendiri (iframe salinan tidak pernah tampil)
  d.querySelectorAll('iframe.elementor-background-video-embed').forEach(f => { const ph = document.createElement('div'); ph.className = 'elementor-background-video-embed'; f.replaceWith(ph); });
  const html = links + d.innerHTML, top = elementor.getPreviewContainer();
  const lama = [...(top.children.models || top.children)].filter(c => c.id !== 'tfmirror1');
  lama.forEach(c => $e.run('document/elements/settings', {container: c, settings: {hide_desktop: 'hidden-desktop', hide_tablet: 'hidden-tablet', hide_mobile: 'hidden-mobile'}}));
  const ada = elementor.getContainer('tfmirror2');
  if (ada) $e.run('document/elements/settings', {container: ada, settings: {html}});
  else $e.run('document/elements/create', {container: top, options: {at: 0}, model: {id: 'tfmirror1', elType: 'container', settings: {content_width: 'full', padding: {unit: 'px', top: '0', right: '0', bottom: '0', left: '0', isLinked: true}, _title: 'Mirror Home tf /new/'},
    elements: [{id: 'tfmirror2', elType: 'widget', widgetType: 'html', settings: {html, _title: 'HTML hasil render Home tf'}, elements: []}]}});
  await $e.run('document/save/default', {force: true});
  return 'ok ' + html.length;
};
