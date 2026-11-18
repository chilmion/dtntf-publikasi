// Dosen Tetap (revisi dosen 18 Nov 2026), versi 2 setelah masukan: layout kartu tetap, TAPI
//  (1) ruang vertikal dirapatkan (kontainer teks tanpa tinggi minimum 400px), (2) tombol menjadi ikon panah bulat saja (buka profil SINTA penuh),
//  (3) foto diseragamkan: file hasil crop wajah 4:5 (data/ugm/foto-dosen/<slug>.jpg, diunggah ke media situs; peta slug->{id,url} di localStorage '__fotoDosen').
// Urutan di tab wp-admin biasa: unggah foto (lihat fotoDosenUnggah di bawah), lalu di tab EDITOR halaman daftar dosen:  await dosenTetap()  lalu  await kernFix().
window.fotoDosenUnggah = async function (sha, slugs) {
  let M = JSON.parse(localStorage.getItem('__fotoDosen') || '{}');
  for (const s of slugs) { if (M[s]) continue;
    const b = await (await fetch('https://raw.githubusercontent.com/chilmion/dtntf-publikasi/' + sha + '/data/ugm/foto-dosen/' + s + '.jpg')).blob();
    const j = await (await fetch('/wp-json/wp/v2/media', {method: 'POST', headers: {'X-WP-Nonce': wpApiSettings.nonce, 'Content-Disposition': 'attachment; filename="dosen-' + s + '.jpg"', 'Content-Type': 'image/jpeg'}, body: b})).json();
    if (!j.id) throw new Error('unggah gagal ' + s); M[s] = {id: j.id, url: j.source_url.replace(location.origin, '')}; localStorage.setItem('__fotoDosen', JSON.stringify(M)); }
  return Object.keys(M).length;
};
window.dosenTetap = async function () {
  const SINTA = {"agus-arif": "6017225", "agus-budhie-wijatna": "6012781", "ahmad-agus-setiawan": "6644034", "alexander-agung": "44275", "andang-widi-harto": "6644036", "andhika-yudha-prawira": "6776502", "anung-muharini": "6586868", "ari-bimo-prakoso": "6776532", "awang-n-i-wardana": "5985252", "dwi-joko-suroso": "6759738", "ester-wijayanti": "6043678", "fadli-kasim": "6644053", "faridah": "6010146", "ferdiansjah": "6644056", "fitrotun-aliyah": "6043555", "gandha-satria-adi": "6693661", "gea-oswah-fatah-parikesit": "44178", "haryono-budi-santosa": "6644057", "kusnanto": "6644073", "kutut-suryopratomo": "6031021", "lucyana-dwi-larasati": "6745153", "m-arif-efendi": "6807580", "m-kholid-ridwan": "6017034", "nazrul-effendy": "5996476", "nopriadi": "6016990", "nunung-prabaningrum": "6043524", "nur-abdillah-siddiq": "6727271", "rachmawan-budiarto": "5985995", "sentagi-sesotya-utami": "6014179", "sihana": "6022828", "sita-gandes-pinasti": "6777296", "sunarno": "6011022", "susetyo-hario-putero": "6131321", "thomas-oka-pratama": "6806864", "widya-rosita": "6016573", "yakub-fahim-luckyarno": "6693667", "yanuar-ady-setiawan": "6693680", "yudi-utomo-imardjoko": "6644106"};
  const BYID = Object.fromEntries(Object.entries(SINTA).map(([s, i]) => [i, s]));
  const M = JSON.parse(localStorage.getItem('__fotoDosen') || '{}');
  const px = v => ({unit: 'px', size: v, sizes: []});
  const P4 = v => ({unit: 'px', top: String(v), right: String(v), bottom: String(v), left: String(v), isLinked: true});
  let n = 0, tanpaFoto = [];
  const C = id => elementor.getContainer(id), set = (id, s) => $e.run('document/elements/settings', {container: C(id), settings: s});
  const walk = a => a.forEach(e => {
    const cls = (e.settings && e.settings.css_classes) || '';
    if (e.elType === 'container' && /kt-kartu-dosen/.test(cls)) {
      const kids = e.elements || [], img = kids.find(k => k.widgetType === 'image'), inner = kids.find(k => k.elType === 'container');
      const html = inner && inner.elements.find(k => k.widgetType === 'html'), btn = inner && inner.elements.find(k => k.widgetType === 'button');
      set(e.id, {width: {unit: '%', size: 32.2, sizes: []}, width_tablet: {unit: '%', size: 48.5, sizes: []}, width_mobile: {unit: '%', size: 100, sizes: []}});
      let slug = ''; if (btn) { const u = (btn.settings.link || {}).url || ''; const last = u.replace(/\/$/, '').split('/').pop(); slug = BYID[last] || (SINTA[last] ? last : ''); }
      if (img) { const s = {custom_css: 'selector img{display:block;width:100%;height:auto;aspect-ratio:4/5;object-fit:cover;object-position:center 12%}'}; if (M[slug]) s.image = {url: M[slug].url, id: M[slug].id, size: '', source: 'library'}; else tanpaFoto.push(slug); set(img.id, s); }
      if (inner) set(inner.id, {min_height: px(0), flex_justify_content: 'flex-start', padding: {unit: 'px', top: '16', right: '20', bottom: '20', left: '20', isLinked: false}, flex_gap: {column: '6', row: '6', isLinked: true, unit: 'px', size: 6}});
      if (html) { let h = String(html.settings.html); const s = h.indexOf('(x.ada_data && x.sitasi_scopus != null'); if (s >= 0) { const en = h.indexOf(": '')", s) + ": '')".length; h = h.slice(0, s) + "''" + h.slice(en); set(html.id, {html: h}); } }
      if (btn && slug) set(btn.id, {text: '', selected_icon: {value: 'fas fa-arrow-right', library: 'fa-solid'}, icon_align: 'left', align: 'left', _element_width: 'auto', _margin: {unit: 'px', top: '10', right: '0', bottom: '0', left: '0', isLinked: false},
        link: {url: 'https://sinta.kemdiktisaintek.go.id/authors/profile/' + SINTA[slug], is_external: 'on', nofollow: '', custom_attributes: 'aria-label|Lihat profil lengkap ' + slug + ' di SINTA,title|Lihat profil lengkap di SINTA'},
        button_text_color: '#073C64', background_color: '#C8E86D', border_radius: P4(999), text_padding: P4(13), border_border: '', typography_typography: 'custom', typography_font_size: px(16),
        custom_css: 'selector .elementor-button{width:44px;height:44px;padding:0;display:inline-flex;align-items:center;justify-content:center;transition:transform .25s,background .25s}selector .elementor-button-icon{margin:0}selector .elementor-button:hover{background:#073C64;color:#fff;transform:translateX(3px)}selector .elementor-button-icon svg,selector .elementor-button-icon i{fill:currentColor}'});
      n++;
    }
    if (e.elType === 'container' && (e.elements || []).some(k => /kt-kartu-dosen/.test((k.settings && k.settings.css_classes) || ''))) set(e.id, {padding: P4(0), flex_gap: {column: '16', row: '16', isLinked: true, unit: 'px', size: 16}}); // grid kartu sejajar kolom cari
    if (e.elements) walk(e.elements);
  });
  walk(elementor.config.initial_document.elements);
  await $e.run('document/save/default');
  return 'kartu=' + n + ' tanpa-foto=' + tanpaFoto.join(',');
};
