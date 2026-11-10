(function(){function __go(){

(function () {
  var akar = null
          || document.querySelector('.kt-info:not([data-kt-siap])');
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

  var SLUG = cariSlug(akar);
  if (!SLUG) { akar.innerHTML = '<div class="kt-galat">Isi data-slug (atau letakkan widget "kartu" di halaman ini).</div>'; return; }
  Promise.all([ambil(BASE + '/' + encodeURIComponent(SLUG) + '.json'),
               ambil(BASE + '/agregat/ringkas.json').catch(function () { return null; })])
    .then(function (r) { render(r[0], r[1]); })
    .catch(function (e) { akar.innerHTML = '<div class="kt-galat">Data dosen belum tersedia. (' + esc(e.message) + ')</div>'; });

  function render(d, ringkas) {
    var i = ((ringkas && ringkas.dosen) || []).filter(function (x) { return x.slug === d.slug; })[0] || {};
    var kel = i.kelompok || (d.prodi ? d.prodi.replace(/^S\d\s*-\s*/i, '') : '');
    var tiles = [];
    if (i.pendidikan) tiles.push('<div class="kt-tile putih s12"><span class="kt-kicker">Pendidikan</span><p>' + esc(i.pendidikan) + '</p></div>');
    if (i.bidang_ilmu) tiles.push('<div class="kt-tile lime pola s5"><span class="kt-kicker">Bidang ilmu</span><h3 class="kt-h3" style="margin:0">' + esc(i.bidang_ilmu) + '</h3></div>');
    if (i.bidang_riset) tiles.push('<div class="kt-tile navy pola ' + (i.bidang_ilmu ? 's7' : 's12') + '"><span class="kt-kicker">Bidang riset</span><p style="color:#fff">' + esc(i.bidang_riset) + '</p></div>');
    if ((i.lainnya || []).length) tiles.push('<div class="kt-tile abu s12"><span class="kt-kicker">Keanggotaan &amp; penghargaan</span>' +
      i.lainnya.map(function (x) { return '<p>' + esc(x) + '</p>'; }).join('') + '</div>');
    akar.innerHTML = '<span class="kt-kicker">' + esc([kel, d.jabatan || i.jabatan].filter(Boolean).join(' · ') || 'Dosen DTNTF') + '</span>' +
      '<h1 class="kt-h1">' + esc(d.nama) + '</h1>' +
      (d.gelar ? '<p style="margin:0;font-size:18px">' + esc(d.gelar) + '</p>' : '') +
      ((d.subjects || []).length ? '<div class="kt-i-tag">' + d.subjects.map(function (s) { return '<span class="kt-tag">' + esc(s) + '</span>'; }).join('') + '</div>' : '') +
      (tiles.length ? '<div class="kt-grid kt-i-grid" style="margin-top:28px">' + tiles.join('') + '</div>' : '');
  }

})();

}
if(document.readyState==='loading'){document.addEventListener('DOMContentLoaded',__go)}else{__go()}})();
