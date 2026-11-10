(function(){function __go(){

(function () {
  var akar = null
          || document.querySelector('.kt-kartu:not([data-kt-siap])');
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
  if (!SLUG) { akar.innerHTML = '<div class="kt-galat">Isi data-slug dengan slug dosen.</div>'; return; }
  Promise.all([ambil(BASE + '/' + encodeURIComponent(SLUG) + '.json'),
               ambil(BASE + '/agregat/ringkas.json').catch(function () { return null; })])
    .then(function (r) { render(r[0], r[1]); })
    .catch(function (e) { akar.innerHTML = '<div class="kt-galat">Data dosen belum tersedia. (' + esc(e.message) + ')</div>'; });

  function render(d, ringkas) {
    var i = ((ringkas && ringkas.dosen) || []).filter(function (x) { return x.slug === d.slug; })[0] || {};
    var t = d.tautan || {}, baris = [];
    var email = d.email || i.email;
    if (email) baris.push('<p class="kt-k-baris"><small>Email</small><a href="mailto:' + esc(email) + '">' + esc(email) + '</a></p>');
    if (i.homepage) baris.push('<p class="kt-k-baris"><small>Laman pribadi</small><a href="' + esc(i.homepage) + '" target="_blank" rel="noopener">' + esc(i.homepage.replace(/^https?:\/\//, '')) + '</a></p>');
    if (d.sinta_id) baris.push('<p class="kt-k-baris"><small>ID SINTA</small>' + esc(d.sinta_id) + '</p>');
    var btn = [];
    if (t.sinta) btn.push('<a class="kt-btn" href="' + esc(t.sinta) + '" target="_blank" rel="noopener">SINTA ↗</a>');
    if (t.scholar) btn.push('<a class="kt-btn" href="' + esc(t.scholar) + '" target="_blank" rel="noopener">Google Scholar ↗</a>');
    if (t.scopus) btn.push('<a class="kt-btn" href="' + esc(t.scopus) + '" target="_blank" rel="noopener">Scopus ↗</a>');
    var foto = i.foto_url || d.foto_url;
    akar.innerHTML = '<div class="kt-k-wrap"><div class="kt-k-foto"><span class="kt-k-ini">' + esc(inisial(d.nama)) + '</span>' +
      (foto ? '<img src="' + esc(foto) + '" alt="' + esc(d.nama) + '">' : '') + '</div>' +
      '<div class="kt-tile navy pola" style="margin-top:16px;min-height:0"><div><span class="kt-kicker" style="opacity:.7">Kontak</span>' +
      (baris.join('') || '<p class="kt-k-baris">Belum ada data kontak.</p>') + '</div>' +
      (btn.length ? '<div class="kt-k-btn">' + btn.join('') + '</div>' : '') + '</div></div>';
    var im = akar.querySelector('img');
    if (im) im.addEventListener('error', function () { im.style.display = 'none'; });
  }

})();

}
if(document.readyState==='loading'){document.addEventListener('DOMContentLoaded',__go)}else{__go()}})();
