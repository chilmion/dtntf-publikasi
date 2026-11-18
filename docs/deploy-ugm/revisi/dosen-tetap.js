// Dosen Tetap (revisi dosen 18 Nov 2026), VERSI RINGKAS sesuai permintaan: layout kartu TIDAK diubah (kartu tegak, foto tetap lebar penuh).
// Hanya: (1) tombol "selengkapnya" -> "Profil SINTA" yang membuka profil SINTA penuh, (2) baris jumlah sitasi dihapus, (3) foto dicrop proporsional 4:5 (fokus wajah).
// Jalankan di tab EDITOR halaman daftar dosen (v1: id 1195):  await dosenTetap()   lalu  await kernFix()  (kern.js)
window.dosenTetap = async function () {
  const SINTA = {"agus-arif": "6017225", "agus-budhie-wijatna": "6012781", "ahmad-agus-setiawan": "6644034", "alexander-agung": "44275", "andang-widi-harto": "6644036", "andhika-yudha-prawira": "6776502", "anung-muharini": "6586868", "ari-bimo-prakoso": "6776532", "awang-n-i-wardana": "5985252", "dwi-joko-suroso": "6759738", "ester-wijayanti": "6043678", "fadli-kasim": "6644053", "faridah": "6010146", "ferdiansjah": "6644056", "fitrotun-aliyah": "6043555", "gandha-satria-adi": "6693661", "gea-oswah-fatah-parikesit": "44178", "haryono-budi-santosa": "6644057", "kusnanto": "6644073", "kutut-suryopratomo": "6031021", "lucyana-dwi-larasati": "6745153", "m-arif-efendi": "6807580", "m-kholid-ridwan": "6017034", "nazrul-effendy": "5996476", "nopriadi": "6016990", "nunung-prabaningrum": "6043524", "nur-abdillah-siddiq": "6727271", "rachmawan-budiarto": "5985995", "sentagi-sesotya-utami": "6014179", "sihana": "6022828", "sita-gandes-pinasti": "6777296", "sunarno": "6011022", "susetyo-hario-putero": "6131321", "thomas-oka-pratama": "6806864", "widya-rosita": "6016573", "yakub-fahim-luckyarno": "6693667", "yanuar-ady-setiawan": "6693680", "yudi-utomo-imardjoko": "6644106"};
  let n = 0;
  const C = id => elementor.getContainer(id), set = (id, s) => $e.run('document/elements/settings', {container: C(id), settings: s});
  const walk = a => a.forEach(e => {
    const cls = (e.settings && e.settings.css_classes) || '';
    if (e.elType === 'container' && /kt-kartu-dosen/.test(cls)) {
      const kids = e.elements || [], img = kids.find(k => k.widgetType === 'image'), inner = kids.find(k => k.elType === 'container');
      const html = inner && inner.elements.find(k => k.widgetType === 'html'), btn = inner && inner.elements.find(k => k.widgetType === 'button');
      if (img) set(img.id, {custom_css: 'selector img{display:block;width:100%;height:auto;aspect-ratio:4/5;object-fit:cover;object-position:center 12%}'});
      if (html) { let h = String(html.settings.html); const s = h.indexOf('(x.ada_data && x.sitasi_scopus != null'); if (s >= 0) { const en = h.indexOf(": '')", s) + ": '')".length; h = h.slice(0, s) + "''" + h.slice(en); set(html.id, {html: h}); } }
      if (btn) { const u = (btn.settings.link || {}).url || ''; const slug = u.replace(/\/$/, '').split('/').pop(); const id = SINTA[slug] || (/^[0-9]+$/.test(slug) ? slug : ''); if (id) set(btn.id, {text: 'Profil SINTA \u2192', link: {url: 'https://sinta.kemdiktisaintek.go.id/authors/profile/' + id, is_external: 'on', nofollow: '', custom_attributes: ''}}); }
      n++;
    }
    if (e.elements) walk(e.elements);
  });
  walk(elementor.config.initial_document.elements);
  await $e.run('document/save/default');
  return 'kartu=' + n;
};
