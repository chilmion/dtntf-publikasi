(function(){function __go(){

(function () {
  var akar = null
          || document.querySelector('.kt-stat:not([data-kt-siap])');
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
  var NAMA_KAT_PENDEK = { 'Jurnal Internasional': 'Jurnal Internasional', 'Prosiding Internasional': 'Prosiding Internasional',
    'Book Chapter / Book Series': 'Book Chapter', 'Jurnal Nasional': 'Jurnal Nasional', 'Buku': 'Buku', 'Paten & HKI': 'Paten & HKI',
    'Penelitian': 'Penelitian', 'Pengabdian kepada Masyarakat': 'Pengabdian' };
  var ringkas = null, entri = [], kat = '', thn = '', kata = '', tampil = 30;

  ambil(BASE + '/agregat/ringkas.json').then(function (d) {
    ringkas = d;
    return Promise.all((d.per_tahun || []).map(function (t) {
      return fetch(BASE + '/agregat/' + t.berkas + '.json', { cache: 'no-cache' })
        .then(function (r) { return r.ok ? r.json() : { entri: [] }; })
        .then(function (x) { return x.entri || []; }).catch(function () { return []; });
    }));
  }).then(function (lists) {
    entri = [].concat.apply([], lists);
    entri.sort(function (a, b) { return (b.tahun || 0) - (a.tahun || 0) || (b.sitasi || 0) - (a.sitasi || 0); });
    render();
  }).catch(function (e) {
    akar.innerHTML = '<div class="kt-galat">Statistik belum tersedia. (' + esc(e.message) + ')</div>';
  });

  var linkDosen = function (x) {
    return POLA ? '<a href="' + esc(POLA.replace('{slug}', encodeURIComponent(x.slug))) + '">' + esc(x.nama) + '</a>' : esc(x.nama);
  };
  function stat(label, kelas, span, angka, teks, sedang) {
    return '<div class="kt-tile ' + kelas + ' ' + span + '"><span class="kt-kicker" style="margin:0">' + label + '</span><div>' +
      '<div class="kt-angka' + (sedang ? ' sedang' : '') + '">' + angka + '</div>' + (teks ? '<div class="kt-label">' + teks + '</div>' : '') + '</div></div>';
  }

  function render() {
    var d = ringkas, dosen = d.dosen || [], s = d.statistik || {}, terdata = dosen.filter(function (x) { return x.ada_data; });
    var jumlah = function (k) { return terdata.reduce(function (a, x) { return a + (x[k] || 0); }, 0); };
    var artikel = s.artikel_scopus != null ? s.artikel_scopus : jumlah('artikel_scopus');
    var sitS = s.sitasi_scopus != null ? s.sitasi_scopus : jumlah('sitasi_scopus');
    var sitG = s.sitasi_scholar != null ? s.sitasi_scholar : jumlah('sitasi_scholar');
    var hMaks = s.hindex_scopus_maks != null ? s.hindex_scopus_maks : Math.max.apply(null, [0].concat(terdata.map(function (x) { return x.hindex_scopus || 0; })));
    var kuartil = s.kuartil || [];
    var top = terdata.filter(function (x) { return x.skor_sinta; }).sort(function (a, b) { return b.skor_sinta - a.skor_sinta; }).slice(0, 5);
    var katTot = d.per_kategori || [], katMaks = katTot.reduce(function (a, k) { return Math.max(a, k.jumlah); }, 0) || 1;

    var h = [];
    h.push('<span class="kt-kicker">Departemen Teknik Nuklir dan Teknik Fisika</span><h1 class="kt-h1">Statistik Publikasi</h1>' +
      '<p style="margin:0 0 28px;font-size:18px">Rekam jejak riset dosen DTNTF, diperbarui otomatis dari SINTA' + (d.diperbarui ? ' · ' + esc(d.diperbarui) : '') + '.' +
      (terdata.length < dosen.length ? ' Saat ini baru ' + terdata.length + ' dari ' + dosen.length + ' dosen yang datanya terhitung.' : '') + '</p>');

    var g = [];
    g.push(stat('Dosen', 'lime pola', 's3', num(dosen.length), 'dosen tetap DTNTF'));
    g.push(stat('Artikel Scopus', 'navy pola', 's5 r2', num(artikel), 'artikel terindeks Scopus' + (terdata.length ? ' dari ' + terdata.length + ' profil dosen' : '')));
    g.push(stat('Sitasi Scopus', 'putih', 's4', num(sitS), 'dijumlahkan dari profil dosen', true));
    g.push(stat('h-index tertinggi', 'sky', 's3', num(hMaks), 'h-index Scopus', true));
    g.push(stat('Sitasi Google Scholar', 'lime pola', 's4', num(sitG), 'dijumlahkan dari profil dosen', true));
    if (kuartil.length && donat(kuartil)) g.push('<div class="kt-tile putih s5"><h3 class="kt-h3">Kuartil artikel Scopus</h3>' + donat(kuartil) + '</div>');
    if (top.length) g.push('<div class="kt-tile navy pola ' + (kuartil.length ? 's7' : 's12') + '"><h3 class="kt-h3">Skor SINTA tertinggi</h3><ol class="kt-top">' +
      top.map(function (x, i) { return '<li><span class="no">' + (i + 1) + '</span><span>' + linkDosen(x) + '</span><b>' + num(x.skor_sinta) + '</b></li>'; }).join('') + '</ol></div>');
    if (katTot.length) g.push('<div class="kt-tile abu s12"><h3 class="kt-h3">Luaran tercatat per kategori</h3><div>' +
      katTot.map(function (k) { return '<div class="kt-bar-k"><span>' + esc(NAMA_KAT_PENDEK[k.nama] || k.nama) + '</span><span class="jalur"><span class="isi" style="width:' +
        Math.max(2, k.jumlah / katMaks * 100).toFixed(1) + '%"></span></span><b>' + num(k.jumlah) + '</b></div>'; }).join('') + '</div></div>');
    h.push('<div class="kt-grid">' + g.join('') + '</div>');

    var cnt = {}; entri.forEach(function (e) { cnt[e.kategori] = (cnt[e.kategori] || 0) + 1; });
    var tahun = []; entri.forEach(function (e) { if (e.tahun && tahun.indexOf(e.tahun) < 0) tahun.push(e.tahun); }); tahun.sort(function (a, b) { return b - a; });
    h.push('<div class="kt-blok"><h2 class="kt-h2">Daftar luaran</h2><div class="kt-filter"><div class="kt-chips">' +
      '<button class="kt-chip aktif" type="button" data-k="">Semua (' + entri.length + ')</button>' +
      katTot.filter(function (k) { return cnt[k.nama]; }).map(function (k) { return '<button class="kt-chip" type="button" data-k="' + esc(k.nama) + '">' +
        esc(NAMA_KAT_PENDEK[k.nama] || k.nama) + ' (' + cnt[k.nama] + ')</button>'; }).join('') + '</div>' +
      '<div class="baris"><input class="kt-cari" type="search" placeholder="Cari judul, jurnal, atau nama dosen…" aria-label="Cari luaran">' +
      '<select class="kt-pilih" aria-label="Tahun"><option value="">Semua tahun</option>' + tahun.map(function (y) { return '<option value="' + y + '">' + y + '</option>'; }).join('') + '</select></div></div>' +
      '<div class="kt-tile putih s12" style="min-height:0;margin-top:12px"><div class="kt-hitung"></div><div class="kt-daftar"></div></div></div>');
    akar.innerHTML = h.join('');

    akar.querySelector('.kt-chips').addEventListener('click', function (ev) {
      var b = ev.target.closest ? ev.target.closest('.kt-chip') : null; if (!b) return;
      kat = b.getAttribute('data-k'); tampil = 30;
      [].forEach.call(akar.querySelectorAll('.kt-chip'), function (c) { c.classList.toggle('aktif', c === b); }); daftar();
    });
    akar.querySelector('.kt-pilih').addEventListener('change', function () { thn = this.value; tampil = 30; daftar(); });
    var tunda; akar.querySelector('.kt-cari').addEventListener('input', function () {
      var v = this.value; clearTimeout(tunda); tunda = setTimeout(function () { kata = v.toLowerCase().trim(); tampil = 30; daftar(); }, 180);
    });
    daftar();
  }

  function lencana(p) {
    if (p.kuartil) return p.kuartil;
    if (p.akreditasi && !/unknown/i.test(p.akreditasi)) return p.akreditasi;
    return p.jenis_paten || p.dana || (p.isbn ? 'ISBN ' + p.isbn : '') || '';
  }

  function daftar() {
    var hasil = entri.filter(function (e) {
      if (kat && e.kategori !== kat) return false;
      if (thn && String(e.tahun) !== thn) return false;
      if (!kata) return true;
      return ((e.judul || '') + ' ' + (e.venue || '') + ' ' + (e.dosen || []).map(function (x) { return x.nama; }).join(' ')).toLowerCase().indexOf(kata) > -1;
    });
    akar.querySelector('.kt-hitung').textContent = hasil.length + ' luaran' + (kat || thn || kata ? ' cocok' : ' tercatat');
    var el = akar.querySelector('.kt-daftar');
    el.innerHTML = hasil.length ? hasil.slice(0, tampil).map(function (e) {
      var lb = lencana(e);
      return '<div class="kt-ent"><p class="kt-ent-judul">' + (e.url ? '<a href="' + esc(e.url) + '" target="_blank" rel="noopener">' + esc(e.judul) + '</a>' : esc(e.judul)) + '</p>' +
        '<p class="kt-ent-dosen">' + (e.dosen || []).map(linkDosen).join(', ') + '</p><div class="kt-meta">' +
        (e.venue ? '<span>' + esc(e.venue) + '</span>' : '') + (e.tahun ? '<span class="kt-tag">' + e.tahun + '</span>' : '') +
        '<span class="kt-tag" style="background:#E8EEF4;color:#073C64">' + esc(NAMA_KAT_PENDEK[e.kategori] || e.kategori) + '</span>' +
        (lb ? '<span class="kt-tag">' + esc(lb) + '</span>' : '') + (e.sitasi ? '<span>' + num(e.sitasi) + ' sitasi</span>' : '') + '</div></div>';
    }).join('') + (hasil.length > tampil ? '<button class="kt-lagi" type="button">Tampilkan lebih banyak (' + (hasil.length - tampil) + ' lagi)</button>' : '')
      : '<p style="padding:24px 0;text-align:center">Tidak ada luaran yang cocok.</p>';
    var l = el.querySelector('.kt-lagi'); if (l) l.addEventListener('click', function () { tampil += 30; daftar(); });
  }

})();

}
if(document.readyState==='loading'){document.addEventListener('DOMContentLoaded',__go)}else{__go()}})();
