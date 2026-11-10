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

  ambil(BASE + '/kbk/kbk.json').then(function (d) { render(d.kbk || []); })
    .catch(function (e) { akar.innerHTML = '<div class="kt-galat">Data KBK belum tersedia. (' + esc(e.message) + ')</div>'; });
  // 4 varian bergilir: gambar penuh (lebar 7) · lime + gambar (5) · navy + gambar (5) · gambar penuh (7)
  var VARIAN = [['img', 'w7'], ['lime', 'w5'], ['navy', 'w5'], ['img', 'w7']];
  function render(daftar) {
    akar.innerHTML = '<div class="kt-daftar-kbk">' + daftar.map(function (k, i) {
      var v = VARIAN[i % VARIAN.length], gbr = k.gambar ? esc(BASE + '/' + k.gambar) : '';
      var k_ = k.ketua ? '<a href="' + esc(k.ketua.url) + '">' + esc(k.ketua.nama) + '</a>' : lorem(true);
      var teks = '<div class="kb-teks"><span class="kt-kicker" style="margin:0">KBK' + (k.singkatan ? ' · ' + esc(k.singkatan) : '') + '</span>' +
        '<h2 class="kb-nama">' + (k.nama ? esc(k.nama) : lorem(true)) + '</h2>' +
        '<p class="kb-ring">' + (k.ringkasan ? esc(k.ringkasan) : lorem()) + '</p>' +
        '<p class="kb-ketua">Ketua / koordinator: ' + k_ + '</p></div>';
      var bawah = '<div class="kb-bawah"><div class="kb-kv"><span><b>' + ((k.statistik || {}).dosen ? num(k.statistik.dosen) : '–') + '</b>dosen anggota</span>' +
        '<span><b>' + ((k.statistik || {}).tema ? num(k.statistik.tema) : '–') + '</b>tema penelitian</span></div>' +
        '<a class="kt-btn" href="' + esc(k.url) + '">Lihat KBK →</a></div>';
      if (v[0] === 'img') {
        return '<div class="kb img ' + v[1] + '">' + (gbr ? '<img class="kb-fon" src="' + gbr + '" alt="" loading="lazy">' : '') + teks + bawah + '</div>';
      }
      return '<div class="kb ' + v[0] + ' ' + v[1] + '">' + teks + (gbr ? '<div class="kb-gbr"><img src="' + gbr + '" alt="' + esc(k.nama || '') + '" loading="lazy"></div>' : '') + bawah + '</div>';
    }).join('') + '</div>';
  }
})();

}
if(document.readyState==='loading'){document.addEventListener('DOMContentLoaded',__go)}else{__go()}})();
