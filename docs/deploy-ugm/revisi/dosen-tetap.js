// Dosen Tetap (revisi dosen 18 Nov 2026): tautan langsung ke SINTA, tanpa jumlah sitasi, foto proporsional (kartu horizontal).
// Jalankan di tab EDITOR halaman daftar dosen (v1: id 1195) setelah editor siap:  await dosenTetap()   lalu  await kernFix()  (kern.js)
// Perubahan per kartu `.kt-kartu-dosen`: kartu mendatar (foto 112x140 kiri, teks kanan, lebar 32%), baris statistik sitasi dihapus dari widget info,
// tombol "selengkapnya" menjadi "Profil SINTA" yang membuka profil SINTA penuh (https://sinta.kemdiktisaintek.go.id/authors/profile/<id>) di tab baru.
window.dosenTetap = async function () {
  const SINTA = {"agus-arif": "6017225", "agus-budhie-wijatna": "6012781", "ahmad-agus-setiawan": "6644034", "alexander-agung": "44275", "andang-widi-harto": "6644036", "andhika-yudha-prawira": "6776502", "anung-muharini": "6586868", "ari-bimo-prakoso": "6776532", "awang-n-i-wardana": "5985252", "dwi-joko-suroso": "6759738", "ester-wijayanti": "6043678", "fadli-kasim": "6644053", "faridah": "6010146", "ferdiansjah": "6644056", "fitrotun-aliyah": "6043555", "gandha-satria-adi": "6693661", "gea-oswah-fatah-parikesit": "44178", "haryono-budi-santosa": "6644057", "kusnanto": "6644073", "kutut-suryopratomo": "6031021", "lucyana-dwi-larasati": "6745153", "m-arif-efendi": "6807580", "m-kholid-ridwan": "6017034", "nazrul-effendy": "5996476", "nopriadi": "6016990", "nunung-prabaningrum": "6043524", "nur-abdillah-siddiq": "6727271", "rachmawan-budiarto": "5985995", "sentagi-sesotya-utami": "6014179", "sihana": "6022828", "sita-gandes-pinasti": "6777296", "sunarno": "6011022", "susetyo-hario-putero": "6131321", "thomas-oka-pratama": "6806864", "widya-rosita": "6016573", "yakub-fahim-luckyarno": "6693667", "yanuar-ady-setiawan": "6693680", "yudi-utomo-imardjoko": "6644106"};
  const px = v => ({unit: 'px', size: v, sizes: []});
  const P4 = v => ({unit: 'px', top: String(v), right: String(v), bottom: String(v), left: String(v), isLinked: true});
  let n = 0, miss = [];
  const C = id => elementor.getContainer(id), set = (id, s) => $e.run('document/elements/settings', {container: C(id), settings: s});
  const walk = a => a.forEach(e => {
    const cls = (e.settings && e.settings.css_classes) || '';
    if (e.elType === 'container' && /kt-kartu-dosen/.test(cls)) {
      const kids = e.elements || [], img = kids.find(k => k.widgetType === 'image'), inner = kids.find(k => k.elType === 'container');
      const html = inner && inner.elements.find(k => k.widgetType === 'html'), btn = inner && inner.elements.find(k => k.widgetType === 'button');
      const slug = btn && ((btn.settings.link || {}).url || '').replace(/\/$/, '').split('/').pop();
      set(e.id, {flex_direction: 'row', flex_align_items: 'flex-start', flex_gap: {column: '16', row: '16', isLinked: true, unit: 'px', size: 16}, padding: P4(16), width: {unit: '%', size: 32, sizes: []}, width_tablet: {unit: '%', size: 48, sizes: []}, width_mobile: {unit: '%', size: 100, sizes: []}});
      if (img) set(img.id, {_element_width: 'initial', _element_custom_width: px(112), _flex_size: 'none', width: {unit: '%', size: 100, sizes: []}, _background_color: '', custom_css: 'selector{flex:0 0 112px}selector img{display:block;width:112px;height:140px;object-fit:cover;object-position:center 12%;border-radius:10px}'});
      if (inner) set(inner.id, {_flex_size: 'grow', min_height: px(0), flex_justify_content: 'flex-start', padding: P4(0), flex_gap: {column: '8', row: '8', isLinked: true, unit: 'px', size: 8}, custom_css: 'selector{min-width:0;flex:1 1 0%}'});
      if (html) { let h = String(html.settings.html); const s = h.indexOf('(x.ada_data && x.sitasi_scopus != null'); if (s >= 0) { const en = h.indexOf(": '')", s) + ": '')".length; h = h.slice(0, s) + "''" + h.slice(en); set(html.id, {html: h}); } }
      if (btn) { const id = SINTA[slug]; if (id) set(btn.id, {align: 'left', text: 'Profil SINTA \u2192', link: {url: 'https://sinta.kemdiktisaintek.go.id/authors/profile/' + id, is_external: 'on', nofollow: '', custom_attributes: ''}}); else miss.push(slug); }
      n++;
    }
    if (e.elType === 'container' && (e.elements || []).some(k => /kt-kartu-dosen/.test((k.settings && k.settings.css_classes) || ''))) set(e.id, {padding: P4(0)}); // grid kartu: tanpa padding bawaan
    if (e.elements) walk(e.elements);
  });
  walk(elementor.config.initial_document.elements);
  await $e.run('document/save/default');
  return 'kartu=' + n + ' tanpa-sinta=' + miss.join(',');
};
