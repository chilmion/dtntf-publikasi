(function(){function __go(){

(function () {
  var akar = null
          || document.querySelector('.kt-pgb:not([data-kt-siap])');
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
  var POLA = akar.getAttribute('data-profil') || '';
  var KAT = 'Pengabdian kepada Masyarakat';
  var entri = [], thn = '', dsn = '', kata = '', tampil = 30, diperbarui = '';

  ambil(BASE + '/agregat/ringkas.json').then(function (d) {
    diperbarui = d.diperbarui || '';
    return Promise.all((d.per_tahun || []).filter(function (t) { return (t.per_kategori || {})[KAT]; }).map(function (t) {
      return fetch(BASE + '/agregat/' + t.berkas + '.json', { cache: 'no-cache' })
        .then(function (r) { return r.ok ? r.json() : { entri: [] }; })
        .then(function (x) { return (x.entri || []).filter(function (e) { return e.kategori === KAT; }); }).catch(function () { return []; });
    }));
  }).then(function (lists) {
    entri = [].concat.apply([], lists);
    entri.sort(function (a, b) { return (b.tahun || 0) - (a.tahun || 0); });
    render();
  }).catch(function (e) {
    akar.innerHTML = '<div class="kt-galat">Data pengabdian belum tersedia. (' + esc(e.message) + ')</div>';
  });

  var linkDosen = function (x) {
    return POLA ? '<a href="' + esc(POLA.replace('{slug}', encodeURIComponent(x.slug))) + '">' + esc(x.nama) + '</a>' : esc(x.nama);
  };
  function stat(label, kelas, span, angka, teks, sedang) {
    return '<div class="kt-tile ' + kelas + ' ' + span + '"><span class="kt-kicker" style="margin:0">' + label + '</span><div>' +
      '<div class="kt-angka' + (sedang ? ' sedang' : '') + '">' + angka + '</div>' + (teks ? '<div class="kt-label">' + teks + '</div>' : '') + '</div></div>';
  }
  function tahunan(data) {
    var n = data.length, maks = Math.max.apply(null, data.map(function (x) { return x.jumlah; })) || 1, l = 100 / n, pad = Math.min(l * .2, 1.2);
    var bar = data.map(function (x, i) {
      var h = x.jumlah / maks * 84;
      return '<rect x="' + (i * l + pad).toFixed(2) + '" y="' + (92 - h).toFixed(2) + '" width="' + Math.max(l - pad * 2, .4).toFixed(2) +
        '" height="' + Math.max(h, .6).toFixed(2) + '" rx=".8" fill="#C8E86D"><title>' + x.tahun + ' · ' + x.jumlah + ' kegiatan</title></rect>';
    }).join('');
    return '<svg viewBox="0 0 100 100" preserveAspectRatio="none" style="width:100%;height:130px" role="img" aria-label="Kegiatan pengabdian per tahun">' +
      '<line x1="0" y1="92" x2="100" y2="92" stroke="rgba(255,255,255,.3)" vector-effect="non-scaling-stroke"/>' + bar + '</svg>' +
      '<div style="display:flex;justify-content:space-between;font-size:13px;color:rgba(255,255,255,.7);margin-top:6px"><span>' + data[0].tahun +
      '</span><span>tertinggi ' + maks + ' per tahun</span><span>' + data[n - 1].tahun + '</span></div>';
  }

  function render() {
    var per = {}, dosen = {};
    entri.forEach(function (e) {
      if (e.tahun) per[e.tahun] = (per[e.tahun] || 0) + 1;
      (e.dosen || []).forEach(function (x) { var o = dosen[x.slug] = dosen[x.slug] || { slug: x.slug, nama: x.nama, n: 0 }; o.n++; });
    });
    var tahunUrut = Object.keys(per).map(Number).sort(function (a, b) { return a - b; });
    var seri = tahunUrut.map(function (y) { return { tahun: y, jumlah: per[y] }; });
    var terakhir = tahunUrut.length ? tahunUrut[tahunUrut.length - 1] : null;
    var dosenArr = Object.keys(dosen).map(function (k) { return dosen[k]; }).sort(function (a, b) { return b.n - a.n || a.nama.localeCompare(b.nama); });
    var h = [];
    h.push('<span class="kt-kicker">Departemen Teknik Nuklir dan Teknik Fisika</span><h1 class="kt-h1">Pengabdian kepada Masyarakat</h1>' +
      '<p style="margin:0 0 28px;font-size:18px">Kegiatan pengabdian dosen DTNTF, diperbarui otomatis dari SINTA' + (diperbarui ? ' · ' + esc(diperbarui.slice(0, 10)) : '') + '.</p>');
    var g = [];
    g.push(stat('Kegiatan pengabdian', 'navy pola', 's5 r2', num(entri.length), 'kegiatan tercatat di SINTA'));
    g.push(stat('Dosen terlibat', 'lime pola', 's3', num(dosenArr.length), 'dosen DTNTF'));
    g.push(stat('Tahun ' + (terakhir || ''), 'putih', 's4', num(terakhir ? per[terakhir] : 0), 'kegiatan di tahun terbaru', true));
    g.push(stat('Rentang tahun', 'sky', 's3', tahunUrut.length ? tahunUrut[0] + '–' + terakhir : '–', '', true));
    if (seri.length > 1) g.push('<div class="kt-tile navy pola s12"><h3 class="kt-h3">Kegiatan per tahun</h3>' + tahunan(seri) + '</div>');
    h.push('<div class="kt-grid">' + g.join('') + '</div>');

    h.push('<div class="kt-blok"><h2 class="kt-h2">Daftar kegiatan</h2><div class="kt-filter">' +
      '<div class="baris"><input class="kt-cari" type="search" placeholder="Cari judul, skema, atau nama dosen…" aria-label="Cari kegiatan">' +
      '<select class="kt-pilih kt-fth" aria-label="Tahun"><option value="">Semua tahun</option>' + tahunUrut.slice().reverse().map(function (y) { return '<option value="' + y + '">' + y + ' (' + per[y] + ')</option>'; }).join('') + '</select>' +
      '<select class="kt-pilih kt-fds" aria-label="Dosen"><option value="">Semua dosen</option>' + dosenArr.slice().sort(function (a, b) { return a.nama.localeCompare(b.nama); }).map(function (x) { return '<option value="' + esc(x.slug) + '">' + esc(x.nama) + ' (' + x.n + ')</option>'; }).join('') + '</select></div></div>' +
      '<div class="kt-tile putih s12" style="min-height:0;margin-top:12px"><div class="kt-hitung"></div><div class="kt-daftar"></div></div></div>');
    akar.innerHTML = h.join('');
    akar.querySelector('.kt-fth').addEventListener('change', function () { thn = this.value; tampil = 30; daftar(); });
    akar.querySelector('.kt-fds').addEventListener('change', function () { dsn = this.value; tampil = 30; daftar(); });
    var tunda; akar.querySelector('.kt-cari').addEventListener('input', function () {
      var v = this.value; clearTimeout(tunda); tunda = setTimeout(function () { kata = v.toLowerCase().trim(); tampil = 30; daftar(); }, 180);
    });
    daftar();
  }

  function daftar() {
    var hasil = entri.filter(function (e) {
      if (thn && String(e.tahun) !== thn) return false;
      if (dsn && !(e.dosen || []).some(function (x) { return x.slug === dsn; })) return false;
      if (!kata) return true;
      return ((e.judul || '') + ' ' + (e.venue || '') + ' ' + (e.dosen || []).map(function (x) { return x.nama; }).join(' ')).toLowerCase().indexOf(kata) > -1;
    });
    akar.querySelector('.kt-hitung').textContent = hasil.length + ' kegiatan' + (thn || dsn || kata ? ' cocok' : ' tercatat');
    var el = akar.querySelector('.kt-daftar');
    el.innerHTML = hasil.length ? hasil.slice(0, tampil).map(function (e) {
      return '<div class="kt-ent"><p class="kt-ent-judul">' + (e.url ? '<a href="' + esc(e.url) + '" target="_blank" rel="noopener">' + esc(e.judul) + '</a>' : esc(e.judul)) + '</p>' +
        '<p class="kt-ent-dosen">' + (e.dosen || []).map(linkDosen).join(', ') + '</p><div class="kt-meta">' +
        (e.venue ? '<span>' + esc(e.venue) + '</span>' : '') + (e.tahun ? '<span class="kt-tag">' + e.tahun + '</span>' : '') +
        (e.dana ? '<span class="kt-tag" style="background:#E8EEF4;color:#073C64">' + esc(e.dana) + '</span>' : '') + '</div></div>';
    }).join('') + (hasil.length > tampil ? '<button class="kt-lagi" type="button">Tampilkan lebih banyak (' + (hasil.length - tampil) + ' lagi)</button>' : '')
      : '<p style="padding:24px 0;text-align:center">Tidak ada kegiatan yang cocok.</p>';
    var l = el.querySelector('.kt-lagi'); if (l) l.addEventListener('click', function () { tampil += 30; daftar(); });
  }

})();

}
if(document.readyState==='loading'){document.addEventListener('DOMContentLoaded',__go)}else{__go()}})();
