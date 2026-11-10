(function(){function __go(){

(function () {
  var akar = null
          || document.querySelector('.kt-dinfo:not([data-kt-siap])');
  if (!akar || akar.dataset.ktSiap) return;
  akar.dataset.ktSiap = '1';
  var BASE = (akar.getAttribute('data-base') || '').replace(/\/$/, '');

  var esc = function (s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  };
  var num = function (n) { return (n == null) ? '–' : Number(n).toLocaleString('id-ID'); };
  var inisial = function (n) {
    var k = String(n || '').split(/\s+/).filter(function (w) { return /^[A-Za-z]/.test(w) && w.indexOf('.') < 0; });
    return (k.slice(0, 2).map(function (w) { return w[0]; }).join('') || '?').toUpperCase();
  };
  var ambil = function (u) {
    return fetch(u, { cache: 'no-cache' }).then(function (r) {
      if (!r.ok) throw new Error('HTTP ' + r.status); return r.json();
    });
  };
  // slug: atribut data-slug → ?d=slug di alamat halaman → widget lain di halaman yang punya data-slug
  var cariSlug = function (el) {
    var s = (el.getAttribute('data-slug') || '').trim();
    if (s) return s;
    try { s = new URLSearchParams(location.search).get('d') || ''; } catch (e) { s = ''; }
    if (s) return s;
    var lain = document.querySelectorAll('.dtntf-kt[data-slug]');
    for (var i = 0; i < lain.length; i++) { var v = (lain[i].getAttribute('data-slug') || '').trim(); if (v) return v; }
    return '';
  };
  var WARNA_Q = { 'Q1': '#073C64', 'Q2': '#3B7EA8', 'Q3': '#C8E86D', 'Q4': '#A9C9DD', 'No-Q': '#E3E3E3' };
  var NAMA_Q = { 'No-Q': 'Tanpa kuartil' };

  function donat(data, satuan) {
    var total = data.reduce(function (a, x) { return a + x.jumlah; }, 0);
    if (!total) return '';
    var kum = 0;
    var arc = data.map(function (x) {
      var p = x.jumlah / total * 100, w = WARNA_Q[x.nama] || '#8fb0c9';
      var c = '<circle cx="60" cy="60" r="44" fill="none" stroke="' + w + '" stroke-width="18" pathLength="100" ' +
        'stroke-dasharray="' + p.toFixed(3) + ' ' + (100 - p).toFixed(3) + '" stroke-dashoffset="' + (-kum).toFixed(3) +
        '" transform="rotate(-90 60 60)"><title>' + esc(NAMA_Q[x.nama] || x.nama) + ' · ' + x.jumlah + '</title></circle>';
      kum += p; return c;
    }).join('');
    var leg = data.map(function (x) {
      return '<div><i class="kt-dot" style="background:' + (WARNA_Q[x.nama] || '#8fb0c9') + ';' +
        (x.nama === 'No-Q' ? 'box-shadow:inset 0 0 0 1px #cfcfcf' : '') + '"></i>' +
        esc(NAMA_Q[x.nama] || x.nama) + '<b>' + num(x.jumlah) + '</b></div>';
    }).join('');
    return '<div class="kt-baris-g"><svg viewBox="0 0 120 120" width="150" height="150" role="img" aria-label="Sebaran kuartil">' + arc +
      '<text x="60" y="63" text-anchor="middle" style="font:400 22px var(--kt-f-judul);fill:var(--kt-ink)">' + num(total) + '</text>' +
      '<text x="60" y="76" text-anchor="middle" style="font:500 7px var(--kt-f-teks);fill:#858c9c">' + esc(satuan || 'artikel') + '</text></svg>' +
      '<div class="kt-legenda">' + leg + '</div></div>';
  }

  var SLUG = (akar.getAttribute('data-slug') || '').trim();
  // satu unduhan ringkas.json dipakai bersama oleh semua kartu di halaman
  var kunci = '__dtntfRingkas:' + BASE;
  window[kunci] = window[kunci] || ambil(BASE + '/agregat/ringkas.json');
  window[kunci].then(function (d) {
    var x = (d.dosen || []).filter(function (y) { return y.slug === SLUG; })[0];
    if (!x) { akar.innerHTML = ''; return; }
    var kel = x.kelompok || '';
    akar.innerHTML = (kel ? '<span class="kt-kicker">' + esc(kel) + '</span>' : '') +
      (x.gelar ? '<p class="kt-di-gelar">' + esc(x.gelar) + '</p>' : '') +
      (x.bidang_ilmu ? '<p class="kt-di-bidang">' + esc(x.bidang_ilmu) + '</p>' : '') +
      (x.ada_data && x.sitasi_scopus != null
        ? '<div class="kt-di-stat"><span><b>' + num(x.sitasi_scopus) + '</b>Sitasi Scopus</span></div>' : '');
  }).catch(function () { akar.innerHTML = ''; });

})();

}
if(document.readyState==='loading'){document.addEventListener('DOMContentLoaded',__go)}else{__go()}})();

;(function(){var M={"/kbk/": "/kbk-v2/", "/kbk-proses-nuklir/": "/kbk-proses-nuklir-v2/", "/kbk-multifisika/": "/kbk-multifisika-v2/", "/kbk-instrumentasi/": "/kbk-instrumentasi-v2/", "/pengurus-departemen/": "/pengurus-departemen-v2/", "/ferdiansjah/": "/ferdiansjah-v2/", "/nopriadi/": "/nopriadi-v2/"};var t=0;function fix(){document.querySelectorAll('.dtntf-kt a[href]').forEach(function(a){var h=a.getAttribute('href')||'';var p=h.replace(/^https?:\/\/tf\.ugm\.ac\.id/,'');if(M[p])a.setAttribute('href',M[p])})}function plan(){clearTimeout(t);t=setTimeout(fix,200)}new MutationObserver(plan).observe(document.documentElement,{childList:true,subtree:true});plan()})();
