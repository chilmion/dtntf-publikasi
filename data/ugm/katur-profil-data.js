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

  var TAMPIL = (akar.getAttribute('data-tampil') || 'skor,grafik,metrik,publikasi').split(',').map(function (s) { return s.trim(); });
  var mau = function (n) { return TAMPIL.indexOf(n) > -1; };
  var SLUG = cariSlug(akar);
  if (!SLUG) { akar.innerHTML = '<div class="kt-galat">Isi data-slug (atau letakkan widget "kartu" di halaman ini).</div>'; return; }
  var NAMA_KAT = { scopus: 'Terindeks Scopus', garuda: 'Jurnal nasional (Garuda)', ilmiah: 'Publikasi ilmiah lainnya', buku: 'Buku',
                   paten: 'Paten &amp; HKI', penelitian: 'Penelitian', ppm: 'Pengabdian kepada masyarakat' };
  var URUT = ['scopus', 'garuda', 'ilmiah', 'buku', 'paten', 'penelitian', 'ppm'];
  var NAMA_OUT = { 'Articles': 'Artikel jurnal', 'Conference': 'Prosiding', 'Others': 'Lainnya' };

  ambil(BASE + '/' + encodeURIComponent(SLUG) + '.json').then(render).catch(function (e) {
    akar.innerHTML = '<div class="kt-galat">Data publikasi belum tersedia. (' + esc(e.message) + ')</div>';
  });

  function tile(kelas, span, angka, label, sedang) {
    return '<div class="kt-tile ' + kelas + ' ' + span + '"><span class="kt-kicker" style="margin:0">' + label + '</span>' +
      '<div class="kt-angka' + (sedang ? ' sedang' : '') + '">' + angka + '</div></div>';
  }

  function radar(data) {
    var n = data.length; if (n < 3) return '';
    var maks = Math.max.apply(null, data.map(function (x) { return x.jumlah; })) || 1, cx = 150, cy = 112, R = 74;
    var pt = function (i, f) { var a = -Math.PI / 2 + i * 2 * Math.PI / n; return [cx + Math.cos(a) * R * f, cy + Math.sin(a) * R * f]; };
    var cincin = [1 / 3, 2 / 3, 1].map(function (f) {
      return '<polygon points="' + data.map(function (_, i) { return pt(i, f).join(','); }).join(' ') + '" fill="none" stroke="#d9d9d9"/>';
    }).join('');
    var sumbu = data.map(function (_, i) { var p = pt(i, 1); return '<line x1="' + cx + '" y1="' + cy + '" x2="' + p[0].toFixed(1) + '" y2="' + p[1].toFixed(1) + '" stroke="#d9d9d9"/>'; }).join('');
    var area = '<polygon points="' + data.map(function (x, i) { return pt(i, Math.max(x.jumlah / maks, .02)).map(function (v) { return v.toFixed(1); }).join(','); }).join(' ') +
      '" fill="rgba(7,60,100,.25)" stroke="#073C64" stroke-width="1.8"/>';
    var teks = data.map(function (x, i) {
      var p = pt(i, 1.17), an = p[0] < cx - 6 ? 'end' : (p[0] > cx + 6 ? 'start' : 'middle');
      var y = p[1] + (p[1] < cy - 6 ? -4 : (p[1] > cy + 6 ? 13 : 4));
      return '<text x="' + p[0].toFixed(1) + '" y="' + y.toFixed(1) + '" text-anchor="' + an + '" style="font:500 12px var(--kt-f-teks);fill:#414142">' +
        esc(NAMA_OUT[x.nama] || x.nama) + ' · <tspan style="font-weight:700;fill:#073C64">' + num(x.jumlah) + '</tspan></text>';
    }).join('');
    return '<svg viewBox="0 0 300 235" style="max-width:340px;margin:0 auto;display:block" role="img" aria-label="Luaran riset">' + cincin + sumbu + area + teks + '</svg>';
  }

  function tahunan(data) {
    var n = data.length, maks = Math.max.apply(null, data.map(function (x) { return x.jumlah; })) || 1;
    var l = 100 / n, pad = Math.min(l * .2, 1.2);
    var bar = data.map(function (x, i) {
      var h = x.jumlah / maks * 84;
      return '<rect x="' + (i * l + pad).toFixed(2) + '" y="' + (92 - h).toFixed(2) + '" width="' + Math.max(l - pad * 2, .4).toFixed(2) +
        '" height="' + Math.max(h, .6).toFixed(2) + '" rx=".8" fill="#C8E86D"><title>' + x.tahun + ' · ' + x.jumlah + ' artikel</title></rect>';
    }).join('');
    return '<svg viewBox="0 0 100 100" preserveAspectRatio="none" style="width:100%;height:130px" role="img" aria-label="Artikel per tahun">' +
      '<line x1="0" y1="92" x2="100" y2="92" stroke="rgba(255,255,255,.3)" vector-effect="non-scaling-stroke"/>' + bar + '</svg>' +
      '<div style="display:flex;justify-content:space-between;font-size:13px;color:rgba(255,255,255,.7);margin-top:6px"><span>' + data[0].tahun +
      '</span><span>tertinggi ' + maks + ' per tahun</span><span>' + data[n - 1].tahun + '</span></div>';
  }

  function lencana(p) {
    if (p.kuartil) return p.kuartil;
    if (p.akreditasi && !/unknown/i.test(p.akreditasi)) return p.akreditasi;
    return p.jenis_paten || p.dana || (p.isbn ? 'ISBN ' + p.isbn : '') || '';
  }

  function render(d) {
    var m = d.metrik || {}, sk = d.skor || {}, g = d.grafik || {}, sc = m.scopus || {}, gs = m.scholar || {}, t = d.tautan || {}, h = [];

    if (mau('skor') || mau('metrik')) {
      var ub = [];
      if (sk.overall != null) ub.push(tile('navy pola', 's4', num(sk.overall), 'Skor SINTA keseluruhan'));
      if (sk.tiga_tahun != null) ub.push(tile('lime pola', 's4', num(sk.tiga_tahun), 'Skor SINTA 3 tahun terakhir'));
      if (sc.hindex != null) ub.push(tile('putih', 's4', num(sc.hindex), 'h-index Scopus'));
      var u2 = [];
      if (sc.artikel != null) u2.push(tile('navy pola', 's3', num(sc.artikel), 'Artikel Scopus', true));
      if (sc.sitasi != null) u2.push(tile('abu', 's3', num(sc.sitasi), 'Sitasi Scopus', true));
      if (gs.sitasi != null) u2.push(tile('lime pola', 's3', num(gs.sitasi), 'Sitasi Google Scholar', true));
      if (gs.hindex != null) u2.push(tile('putih', 's3', num(gs.hindex), 'h-index Scholar', true));
      if (ub.length || u2.length) h.push('<div class="kt-grid">' + ub.join('') + u2.join('') + '</div>');
    }

    if (mau('grafik')) {
      var gt = [];
      if ((g.kuartil || []).length && donat(g.kuartil)) gt.push('<div class="kt-tile putih s6"><h3 class="kt-h3">Kuartil artikel Scopus</h3>' + donat(g.kuartil) + '</div>');
      if ((g.output || []).length && radar(g.output)) gt.push('<div class="kt-tile abu s6"><h3 class="kt-h3">Luaran riset</h3>' + radar(g.output) + '</div>');
      if ((g.per_tahun || []).length > 1) gt.push('<div class="kt-tile navy pola s12"><h3 class="kt-h3">Artikel Scopus per tahun</h3>' + tahunan(g.per_tahun) + '</div>');
      if (gt.length) h.push('<div class="kt-grid" style="margin-top:16px">' + gt.join('') + '</div>');
    }

    if (mau('metrik') && (sc.artikel != null || gs.artikel != null)) {
      var BARIS = [['artikel', 'Artikel'], ['sitasi', 'Sitasi'], ['dokumen_disitasi', 'Dokumen disitasi'], ['hindex', 'h-index'], ['i10index', 'i10-index'], ['gindex', 'g-index']];
      var wos = m.wos || {};
      h.push('<div class="kt-grid" style="margin-top:16px"><div class="kt-tile putih s12"><h3 class="kt-h3">Metrik sitasi</h3><table class="kt-tabel"><thead><tr><th></th><th>Scopus</th><th>Google Scholar</th>' +
        (wos.artikel != null ? '<th>WOS</th>' : '') + '</tr></thead><tbody>' + BARIS.map(function (b) {
          return '<tr><td>' + b[1] + '</td><td>' + num(sc[b[0]]) + '</td><td>' + num(gs[b[0]]) + '</td>' + (wos.artikel != null ? '<td>' + num(wos[b[0]]) + '</td>' : '') + '</tr>';
        }).join('') + '</tbody></table></div></div>');
    }

    var pub = d.publikasi || [];
    if (mau('publikasi') && pub.length) {
      var lengkap = !!(d.batas_daftar && d.batas_daftar.lengkap), per = {};
      pub.forEach(function (p) { (per[p.sumber] = per[p.sumber] || []).push(p); });
      var isi = URUT.filter(function (k) { return per[k] && per[k].length; }).map(function (k) {
        var l = per[k].slice().sort(function (a, b) { return (b.tahun || 0) - (a.tahun || 0) || (b.sitasi || 0) - (a.sitasi || 0); });
        return '<div class="kt-tile putih s12" style="min-height:0;margin-top:16px"><div class="kt-kat-kepala"><h3 class="kt-h3">' + (NAMA_KAT[k] || k) + '</h3>' +
          '<span class="kt-kicker" style="margin:0">' + l.length + (lengkap ? ' luaran' : ' terbaru') + '</span></div><div>' +
          l.map(function (p) {
            var lb = lencana(p);
            return '<div class="kt-pub"><p class="kt-pub-judul">' + (p.url ? '<a href="' + esc(p.url) + '" target="_blank" rel="noopener">' + esc(p.judul) + '</a>' : esc(p.judul)) + '</p>' +
              '<div class="kt-meta">' + (p.venue ? '<span>' + esc(p.venue) + '</span>' : '') + (p.tahun ? '<span class="kt-tag">' + p.tahun + '</span>' : '') +
              (lb ? '<span class="kt-tag" style="background:#E8EEF4;color:#073C64">' + esc(lb) + '</span>' : '') +
              (p.sitasi ? '<span>' + num(p.sitasi) + ' sitasi</span>' : '') + '</div></div>';
          }).join('') + '</div></div>';
      }).join('');
      h.push('<div class="kt-blok"><h2 class="kt-h2">' + (lengkap ? 'Daftar luaran' : 'Luaran terbaru') + '</h2>' + isi +
        (lengkap ? '' : '<p class="kt-catatan">Statistik di atas mencakup seluruh karier. Daftar ini memuat ' + ((d.batas_daftar || {}).per_kategori || 10) +
          ' luaran terbaru per kategori, batas tampilan SINTA bagi pengunjung umum' + (t.sinta ? ' — daftar lengkap ada di <a href="' + esc(t.sinta) + '" target="_blank" rel="noopener">profil SINTA</a>' : '') + '.</p>') + '</div>');
    }

    h.push('<div class="kt-kaki"><span>Diperbarui otomatis dari SINTA · ' + esc((d.diperbarui || '').slice(0, 10)) + '</span></div>');
    akar.innerHTML = h.join('');
  }

})();

}
if(document.readyState==='loading'){document.addEventListener('DOMContentLoaded',__go)}else{__go()}})();

;(function(){var M={"/kbk/": "/kbk-v2/", "/kbk-proses-nuklir/": "/kbk-proses-nuklir-v2/", "/kbk-multifisika/": "/kbk-multifisika-v2/", "/kbk-instrumentasi/": "/kbk-instrumentasi-v2/", "/pengurus-departemen/": "/pengurus-departemen-v2/", "/ferdiansjah/": "/ferdiansjah-v2/", "/nopriadi/": "/nopriadi-v2/"};var t=0;function fix(){document.querySelectorAll('.dtntf-kt a[href]').forEach(function(a){var h=a.getAttribute('href')||'';var p=h.replace(/^https?:\/\/tf\.ugm\.ac\.id/,'');if(M[p])a.setAttribute('href',M[p])})}function plan(){clearTimeout(t);t=setTimeout(fix,200)}new MutationObserver(plan).observe(document.documentElement,{childList:true,subtree:true});plan()})();
