(function(){function __go(){

(function () {
  var akar = null
          || document.querySelector('.kt-daftar:not([data-kt-siap])');
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

  var POLA = akar.getAttribute('data-profil') || '';
  var semua = [], kelompok = '', kata = '';

  ambil(BASE + '/agregat/ringkas.json').then(function (d) {
    semua = (d.dosen || []).slice().sort(function (a, b) {
      return (a.nama || '').toLowerCase() < (b.nama || '').toLowerCase() ? -1 : 1;
    });
    kerangka(); gambar();
  }).catch(function (e) {
    akar.innerHTML = '<div class="kt-galat">Daftar dosen belum tersedia. (' + esc(e.message) + ')</div>';
  });

  function kelompokDari(x) { return x.kelompok || (/nuklir/i.test(x.prodi || '') ? 'Teknik Nuklir' : /fisika/i.test(x.prodi || '') ? 'Teknik Fisika' : 'Lainnya'); }

  function kerangka() {
    var ada = {};
    semua.forEach(function (x) { var k = kelompokDari(x); ada[k] = (ada[k] || 0) + 1; });
    var urut = ['Teknik Nuklir', 'Teknik Fisika', 'Lainnya'].filter(function (k) { return ada[k]; });
    akar.innerHTML =
      '<span class="kt-kicker">Departemen Teknik Nuklir dan Teknik Fisika</span>' +
      '<h1 class="kt-h1">Dosen Tetap</h1>' +
      '<p style="margin:0 0 24px;font-size:18px">' + semua.length + ' dosen dengan keahlian dari rekayasa nuklir hingga rekayasa fisika.</p>' +
      '<div class="kt-toolbar"><input class="kt-cari" type="search" placeholder="Cari nama atau bidang riset…" aria-label="Cari dosen">' +
      '<div class="kt-chips"><button class="kt-chip aktif" type="button" data-k="">Semua (' + semua.length + ')</button>' +
      urut.map(function (k) { return '<button class="kt-chip" type="button" data-k="' + esc(k) + '">' + esc(k) + ' (' + ada[k] + ')</button>'; }).join('') +
      '</div></div><div class="kt-dk-grid"></div>';
    akar.querySelector('.kt-cari').addEventListener('input', function () { kata = this.value.toLowerCase().trim(); gambar(); });
    akar.querySelector('.kt-chips').addEventListener('click', function (e) {
      var b = e.target.closest ? e.target.closest('.kt-chip') : null;
      if (!b) return;
      kelompok = b.getAttribute('data-k');
      [].forEach.call(akar.querySelectorAll('.kt-chip'), function (c) { c.classList.toggle('aktif', c === b); });
      gambar();
    });
  }

  function gambar() {
    var daftar = semua.filter(function (x) {
      if (kelompok && kelompokDari(x) !== kelompok) return false;
      if (!kata) return true;
      return ((x.nama || '') + ' ' + (x.gelar || '') + ' ' + (x.bidang_ilmu || '') + ' ' + (x.bidang_riset || '')).toLowerCase().indexOf(kata) > -1;
    });
    var g = akar.querySelector('.kt-dk-grid');
    g.innerHTML = daftar.length ? daftar.map(kartu).join('') : '<p class="kt-kosong" style="grid-column:1/-1">Tidak ada dosen yang cocok.</p>';
    [].forEach.call(g.querySelectorAll('img'), function (im) {
      im.addEventListener('error', function () { im.style.display = 'none'; });
    });
  }

  function kartu(x, i) {
    var href = POLA ? POLA.replace('{slug}', encodeURIComponent(x.slug)) : '#';
    var stat = x.ada_data && (x.skor_sinta != null || x.sitasi_scopus != null)
      ? '<div class="kt-dk-stat"><span><b>' + num(x.skor_sinta) + '</b>Skor SINTA</span><span><b>' + num(x.sitasi_scopus) + '</b>Sitasi Scopus</span></div>' : '';
    return '<a class="kt-dk" href="' + esc(href) + '">' +
      '<div class="kt-dk-foto t' + (i % 3) + '"><span class="kt-dk-ini">' + esc(inisial(x.nama)) + '</span>' +
      (x.foto_url ? '<img loading="lazy" src="' + esc(x.foto_url) + '" alt="' + esc(x.nama) + '">' : '') + '</div>' +
      '<div class="kt-dk-isi"><span class="kt-kicker">' + esc(kelompokDari(x) === 'Lainnya' ? 'Dosen' : kelompokDari(x)) + '</span>' +
      '<h3 class="kt-h3">' + esc(x.nama) + '</h3>' +
      (x.gelar ? '<p class="kt-gelar">' + esc(x.gelar) + '</p>' : '') +
      (x.bidang_ilmu ? '<p class="kt-bidang">' + esc(x.bidang_ilmu) + '</p>' : '') + stat + '</div></a>';
  }

})();

}
if(document.readyState==='loading'){document.addEventListener('DOMContentLoaded',__go)}else{__go()}})();

;(function(){var M={"/kbk/": "/kbk-v2/", "/kbk-proses-nuklir/": "/kbk-proses-nuklir-v2/", "/kbk-multifisika/": "/kbk-multifisika-v2/", "/kbk-instrumentasi/": "/kbk-instrumentasi-v2/", "/pengurus-departemen/": "/pengurus-departemen-v2/", "/ferdiansjah/": "/ferdiansjah-v2/", "/nopriadi/": "/nopriadi-v2/"};var t=0;function fix(){document.querySelectorAll('.dtntf-kt a[href]').forEach(function(a){var h=a.getAttribute('href')||'';var p=h.replace(/^https?:\/\/tf\.ugm\.ac\.id/,'');if(M[p])a.setAttribute('href',M[p])})}function plan(){clearTimeout(t);t=setTimeout(fix,200)}new MutationObserver(plan).observe(document.documentElement,{childList:true,subtree:true});plan()})();
