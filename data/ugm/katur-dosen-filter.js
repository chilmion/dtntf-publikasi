(function(){function __go(){

(function () {
  var akar = null
          || document.querySelector('.kt-dfilter:not([data-kt-siap])');
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

  var SEL = akar.getAttribute('data-kartu') || '.kt-kartu-dosen';
  var GRUP = [['', 'Semua'], ['kt-kel-nuklir', 'Teknik Nuklir'], ['kt-kel-fisika', 'Teknik Fisika'], ['kt-kel-lain', 'Lainnya']];
  var kelas = '', kata = '', terakhir = -1;

  // Kartu berada DI BAWAH widget ini, jadi belum ada saat skrip pertama jalan:
  // baca ulang setelah halaman selesai dimuat (dan setiap kali menyaring).
  var ambilKartu = function () { return [].slice.call(document.querySelectorAll(SEL)); };
  var jml = function (ks, k) { return k ? ks.filter(function (c) { return c.classList.contains(k); }).length : ks.length; };

  function bangun() {
    var ks = ambilKartu();
    if (ks.length === terakhir) return;
    terakhir = ks.length;
    akar.innerHTML = '<div class="kt-toolbar"><input class="kt-cari" type="search" placeholder="Cari nama atau bidang riset…" aria-label="Cari dosen" value="' + esc(kata) + '">' +
      '<div class="kt-chips">' + GRUP.filter(function (g) { return !g[0] || jml(ks, g[0]); }).map(function (g) {
        return '<button class="kt-chip' + (g[0] === kelas ? ' aktif' : '') + '" type="button" data-k="' + g[0] + '">' + g[1] + ' (' + jml(ks, g[0]) + ')</button>';
      }).join('') + '</div></div><p class="kt-kosong-d">Tidak ada dosen yang cocok.</p>';
    akar.querySelector('.kt-cari').addEventListener('input', function () { kata = this.value.toLowerCase().trim(); terapkan(); });
    akar.querySelector('.kt-chips').addEventListener('click', function (e) {
      var b = e.target.closest ? e.target.closest('.kt-chip') : null; if (!b) return;
      kelas = b.getAttribute('data-k');
      [].forEach.call(akar.querySelectorAll('.kt-chip'), function (c) { c.classList.toggle('aktif', c === b); });
      terapkan();
    });
  }

  function terapkan() {
    var n = 0;
    ambilKartu().forEach(function (c) {
      var ok = (!kelas || c.classList.contains(kelas)) && (!kata || (c.textContent || '').toLowerCase().indexOf(kata) > -1);
      c.style.display = ok ? '' : 'none';
      if (ok) n++;
    });
    var k = akar.querySelector('.kt-kosong-d'); if (k) k.style.display = n ? 'none' : 'block';
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', bangun); else bangun();
  window.addEventListener('load', bangun);
  setTimeout(bangun, 1200);   // cadangan untuk pratinjau editor Elementor

})();

}
if(document.readyState==='loading'){document.addEventListener('DOMContentLoaded',__go)}else{__go()}})();
