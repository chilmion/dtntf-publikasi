(function(){function __go(){

(function () {
  var akar = null
          || document.querySelector('.kt-data:not([data-kt-siap])');
  if (!akar || akar.dataset.ktSiap) return;
  akar.dataset.ktSiap = '1';
  var BASE = (akar.getAttribute('data-base') || '').replace(/\/$/, '');
  var esc = function (s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  };
  var num = function (n) { return (n == null) ? '–' : Number(n).toLocaleString('id-ID'); };
  var ambil = function (u) {
    return fetch(u, { cache: 'no-cache' }).then(function (r) {
      if (!r.ok) throw new Error('HTTP ' + r.status); return r.json();
    });
  };
  // PENANDA: teks lorem ipsum = datanya belum diisi (kelas .kt-lorem, atribut data-lorem)
  var LOREM = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.';
  var LOREM_PENDEK = 'Lorem ipsum dolor sit amet';
  var lorem = function (pendek) { return '<span class="kt-lorem" data-lorem="1">' + (pendek ? LOREM_PENDEK : LOREM) + '</span>'; };
  var loremP = function () { return '<p class="kt-lorem" data-lorem="1">' + LOREM + '</p>'; };

  var KODE = (akar.getAttribute('data-kbk') || '').trim().toLowerCase();
  if (!KODE) { akar.innerHTML = '<div class="kt-galat">Isi data-kbk (kode KBK, mis. enet).</div>'; return; }
  ambil(BASE + '/kbk/kbk.json').then(function (d) {
    var k = (d.kbk || []).filter(function (x) { return x.kode === KODE; })[0];
    if (!k) throw new Error('KBK "' + KODE + '" tidak ada di kbk.json');
    render(k);
  }).catch(function (e) { akar.innerHTML = '<div class="kt-galat">Data KBK belum tersedia. (' + esc(e.message) + ')</div>'; });

  function orang(o) { return o ? '<a href="' + esc(o.url) + '">' + esc(o.nama) + (o.gelar ? ', ' + esc(o.gelar) : '') + '</a>' : lorem(true); }
  function sec(judul, isi, no) {
    return '<section class="kt-sec"><div class="kt-sec-kepala">' + (no ? '<span class="kt-no">' + no + '</span>' : '') + '<h2 class="kt-h2">' + judul + '</h2></div>' + isi + '</section>';
  }
  function stat(kelas, angka, label) {
    return '<div class="kt-tile ' + kelas + ' s3"><span class="kt-kicker" style="margin:0">' + label + '</span><div class="kt-angka sedang">' + (angka ? num(angka) : '–') + '</div></div>';
  }
  function kartu(a, ketua) {
    var peran = a.peran || (ketua && ketua.slug === a.slug ? 'Ketua' : '');
    return '<a class="kt-kartu" href="' + esc(a.url) + '"><div class="kt-kartu-foto">' +
      (a.foto_url ? '<img src="' + esc(a.foto_url) + '" alt="' + esc(a.nama) + '" loading="lazy">' : '') +
      (peran ? '<span class="kt-lencana">' + esc(peran) + '</span>' : '') + '</div>' +
      '<div class="kt-kartu-isi"><h3>' + esc(a.nama) + '</h3>' + (a.gelar ? '<span style="font-size:14px">' + esc(a.gelar) + '</span>' : '') +
      '<p>' + (a.keahlian ? esc(a.keahlian) : lorem(true)) + '</p><span class="kt-lanjut">Selengkapnya →</span></div></a>';
  }
  function kartuLorem() {
    return '<div class="kt-kartu"><div class="kt-kartu-foto"></div><div class="kt-kartu-isi"><h3>' + lorem(true) + '</h3><p>' + lorem(true) + '</p></div></div>';
  }
  function tema(t) {
    var riset = (t.riset || []).slice(0, 5), pub = (t.publikasi || []).slice(0, 5);
    var li = function (x) { return '<li>' + esc(x) + '</li>'; };
    var lp = function (p) {
      var doi = p.doi && /^10\./.test(p.doi) ? ' <a href="https://doi.org/' + esc(p.doi) + '" target="_blank" rel="noopener">DOI ↗</a>' : '';
      return '<li>' + esc(p.sitasi) + doi + '</li>';
    };
    return '<div class="kt-tile putih kt-tema" style="min-height:0;display:block"><div class="kt-tema-kepala"><h3 class="kt-h3">' + (t.no ? '<span class="kt-no" style="margin-right:10px;vertical-align:middle">' + t.no + '</span>' : '') +
      (t.judul ? esc(t.judul) : lorem(true)) + '</h3>' + (t.jumlah_publikasi ? '<span class="kt-tag">' + num(t.jumlah_publikasi) + ' publikasi</span>' : '') + '</div>' +
      (t.deskripsi ? '<p style="margin:0">' + esc(t.deskripsi) + '</p>' : loremP()) +
      '<div class="kt-tema-isi"><div><span class="kt-kicker" style="margin:0">Riset terkait</span><ul>' + (riset.length ? riset.map(li).join('') : '<li>' + lorem() + '</li>') + '</ul></div>' +
      '<div><span class="kt-kicker" style="margin:0">Publikasi terpilih</span><ul>' + (pub.length ? pub.map(lp).join('') : '<li>' + lorem() + '</li>') + '</ul></div></div></div>';
  }

  function render(k) {
    var st = k.statistik || {}, h = [];
    // a. hero: teks di kiri, visual KBK di kanan
    var gbr = k.gambar ? '<div class="kt-hero-gambar"><img src="' + esc(BASE + '/' + k.gambar) + '" alt="' + esc(k.nama || 'KBK') + '"></div>'
                       : '<div class="kt-hero-gambar kt-lorem" data-lorem="1"><span>Gambar KBK</span></div>';
    h.push('<div class="kt-tile navy pola kt-hero" style="display:grid"><div class="kt-hero-teks"><span class="kt-kicker">Kelompok Bidang Keahlian · Departemen Teknik Nuklir dan Teknik Fisika</span>' +
      '<h1 class="kt-h1">' + (k.nama ? esc(k.nama) : lorem(true)) + '</h1>' +
      '<p class="kt-ketua">Ketua / koordinator: ' + orang(k.ketua) + '</p>' +
      '<span class="kt-kicker" style="margin-top:8px">Sekilas</span>' + (k.sekilas ? '<p>' + esc(k.sekilas) + '</p>' : loremP()) + '</div>' + gbr + '</div>');
    // b. statistik bento
    h.push('<div class="kt-grid" style="margin-top:16px">' + stat('lime pola', st.dosen, 'Dosen anggota') + stat('putih', st.kompetensi, 'Bidang kompetensi') +
      stat('abu', st.tema, 'Tema penelitian') + stat('navy pola', st.publikasi, 'Publikasi terpilih') + '</div>');
    // c. kompetensi
    var kp = (k.kompetensi || []).map(function (c) {
      return '<div class="kt-tile putih"><div class="kt-angka">' + c.no + '</div><h3>' + esc(c.judul) + '</h3><p>' + (c.deskripsi ? esc(c.deskripsi) : lorem()) + '</p></div>';
    }).join('') || [1, 2, 3].map(function (n) { return '<div class="kt-tile putih"><div class="kt-angka">' + n + '</div><h3>' + lorem(true) + '</h3><p>' + lorem() + '</p></div>'; }).join('');
    h.push(sec('Kompetensi &amp; keahlian', '<div class="kt-komp">' + kp + '</div>'));
    // d. anggota
    var ag = (k.anggota || []).map(function (a) { return kartu(a, k.ketua); }).join('') || kartuLorem() + kartuLorem() + kartuLorem();
    h.push(sec('Anggota', '<div class="kt-anggota">' + ag + '</div>'));
    // e. tema penelitian
    var tm = (k.tema || []).length ? k.tema.map(tema).join('') : tema({ no: 1 }) + tema({ no: 2 });
    h.push(sec('Tema penelitian', tm));
    akar.innerHTML = h.join('');
  }

})();

}
if(document.readyState==='loading'){document.addEventListener('DOMContentLoaded',__go)}else{__go()}})();

;(function(){var M={"/kbk/": "/kbk-v2/", "/kbk-proses-nuklir/": "/kbk-proses-nuklir-v2/", "/kbk-multifisika/": "/kbk-multifisika-v2/", "/kbk-instrumentasi/": "/kbk-instrumentasi-v2/", "/pengurus-departemen/": "/pengurus-departemen-v2/", "/ferdiansjah/": "/ferdiansjah-v2/", "/nopriadi/": "/nopriadi-v2/"};var t=0;function fix(){document.querySelectorAll('.dtntf-kt a[href]').forEach(function(a){var h=a.getAttribute('href')||'';var p=h.replace(/^https?:\/\/tf\.ugm\.ac\.id/,'');if(M[p])a.setAttribute('href',M[p])})}function plan(){clearTimeout(t);t=setTimeout(fix,200)}new MutationObserver(plan).observe(document.documentElement,{childList:true,subtree:true});plan()})();
