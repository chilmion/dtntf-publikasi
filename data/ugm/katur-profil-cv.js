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

  var TAMPIL = (akar.getAttribute('data-tampil') || 'statistik,grafik,metrik').split(',').map(function (s) { return s.trim(); });
  var mau = function (n) { return TAMPIL.indexOf(n) > -1; };
  var cariSlug = function (el) {
    var s = (el.getAttribute('data-slug') || '').trim();
    if (s) return s;
    try { s = new URLSearchParams(location.search).get('d') || ''; } catch (e) { s = ''; }
    if (s) return s;
    var lain = document.querySelectorAll('.dtntf-kt[data-slug]');
    for (var i = 0; i < lain.length; i++) { var v = (lain[i].getAttribute('data-slug') || '').trim(); if (v) return v; }
    return '';
  };
  var SLUG = cariSlug(akar);
  if (!SLUG) { akar.innerHTML = '<div class="kt-galat">Isi data-slug dosen pada widget ini.</div>'; return; }
  ambil(BASE + '/' + encodeURIComponent(SLUG) + '.json').then(render).catch(function (e) {
    akar.innerHTML = '<div class="kt-galat">Data profil belum tersedia. (' + esc(e.message) + ')</div>';
  });

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

  var NAMA_OUT = { 'Articles': 'Artikel jurnal', 'Conference': 'Prosiding', 'Others': 'Lainnya' };
  var BATAS = 10;
  var tahunUrut = function (a, b) { return (b.tahun || 0) - (a.tahun || 0) || (b.sitasi || 0) - (a.sitasi || 0); };
  var thn = function (t) { return (String(t || '').match(/\d{4}/g) || ['0']).slice(-1)[0] * 1; };

  // daftar panjang: BATAS pertama tampil, sisanya di <details> (tanpa JS tambahan)
  function lipat(item, fungsi, bungkus) {
    var tampil = item.slice(0, BATAS), sisa = item.slice(BATAS);
    var h = bungkus(tampil.map(fungsi).join(''), true);
    if (sisa.length) h += '<details class="kt-lipat"><summary>Tampilkan ' + sisa.length + ' lainnya</summary>' + bungkus(sisa.map(fungsi).join(''), false) + '</details>';
    return h;
  }
  function bagian(no, judul, isi) {
    return '<section class="kt-sec"><div class="kt-sec-kepala">' + (no !== '' ? '<span class="kt-no">' + no + '</span>' : '') + '<h2 class="kt-h2">' + judul + '</h2></div>' +
      '<div class="kt-tile putih" style="min-height:0;display:block">' + isi + '</div></section>';
  }
  function riwayat(item) {
    if (!item || !item.length) return loremP();
    return item.map(function (x) {
      return '<div class="kt-riw"><span class="kt-riw-th">' + esc(x.tahun || '') + '</span><span>' + esc(x.keterangan) + '</span></div>';
    }).join('');
  }
  function lencana(p) {
    if (p.kuartil) return p.kuartil;
    if (p.akreditasi && !/unknown/i.test(p.akreditasi)) return p.akreditasi;
    return p.jenis_paten || p.dana || (p.isbn ? 'ISBN ' + p.isbn : '') || '';
  }
  function luaran(p) {
    var lb = lencana(p);
    return '<div class="kt-pub"><p class="kt-pub-judul">' + (p.url ? '<a href="' + esc(p.url) + '" target="_blank" rel="noopener">' + esc(p.judul) + '</a>' : esc(p.judul)) + '</p>' +
      '<div class="kt-meta">' + (p.venue ? '<span>' + esc(p.venue) + '</span>' : '') + (p.tahun ? '<span class="kt-tag">' + p.tahun + '</span>' : '') +
      (lb ? '<span class="kt-tag" style="background:#E8EEF4;color:#073C64">' + esc(lb) + '</span>' : '') +
      (p.sumber === 'garuda' ? '<span class="kt-tag" style="background:#E8EEF4;color:#073C64">via indeks Garuda</span>' : '') +
      (p.sitasi ? '<span>' + num(p.sitasi) + ' sitasi</span>' : '') + '</div></div>';
  }
  function daftarLuaran(item) {
    if (!item.length) return loremP();
    return lipat(item.slice().sort(tahunUrut), luaran, function (h) { return '<div>' + h + '</div>'; });
  }

  function render(d) {
    var cv = d.cv || {}, id = cv.identitas || {}, pub = d.publikasi || [], t = d.tautan || {}, m = d.metrik || {};
    var h = [];

    // 1. Data diri
    var kv = function (lb, isi, lebar) { return '<div' + (lebar ? ' class="s-penuh"' : '') + '><span class="kt-kicker">' + lb + '</span><b>' + isi + '</b></div>'; };
    h.push(bagian(1, 'Data diri', '<div class="kt-pasang">' +
      kv('Nama lengkap', esc(id.nama_lengkap || ((d.nama || '') + (d.gelar ? ', ' + d.gelar : ''))), true) +
      kv('Jabatan fungsional', id.jabatan_fungsional ? esc(id.jabatan_fungsional) : lorem(true)) +
      kv('Bidang kepakaran', id.bidang_kepakaran ? esc(id.bidang_kepakaran) : lorem(true)) +
      kv('Institusi', id.institusi ? esc(id.institusi) : lorem(true), true) +
      kv('Email', d.email ? '<a href="mailto:' + esc(d.email) + '">' + esc(d.email) + '</a>' : lorem(true)) +
      kv('Telepon institusi', id.telepon_institusi ? esc(id.telepon_institusi) : lorem(true)) + '</div>'));

    // 2-6. riwayat
    h.push(bagian(2, 'Riwayat pendidikan', riwayat(cv.pendidikan)));
    h.push(bagian(3, 'Sertifikat kompetensi', riwayat(cv.sertifikat)));
    h.push(bagian(4, 'Riwayat pekerjaan', riwayat(cv.pekerjaan)));
    h.push(bagian(5, 'Organisasi profesi', riwayat(cv.organisasi)));
    h.push(bagian(6, 'Penghargaan', riwayat(cv.penghargaan)));

    // 7. Pengalaman kerjasama dan penelitian: baris dari manual/profil-cv.xlsx (Penelitian & Pengabdian SINTA ada di bagian terpisah di bawah)
    var baris = (cv.kerjasama || []).map(function (x) { return { riset: x.riset, tahun: x.tahun, ket: x.keterangan }; });
    var no = 0;
    var barisKj = function (x) {
      no++;
      return '<tr><td>' + no + '</td><td>' + (x.url ? '<a href="' + esc(x.url) + '" target="_blank" rel="noopener">' + esc(x.riset) + '</a>' : esc(x.riset)) +
        '</td><td>' + esc(x.tahun) + '</td><td>' + esc(x.ket) + '</td></tr>';
    };
    var tabel = function (isi, pertama) {
      return '<div class="kt-lintas"><table class="kt-tabel kt-kj">' + (pertama ? '<thead><tr><th>No</th><th>Riset / Proyek</th><th>Tahun</th><th>Keterangan</th></tr></thead>' : '') +
        '<tbody>' + isi + '</tbody></table></div>';
    };
    h.push(bagian(7, 'Pengalaman kerjasama dan penelitian', baris.length
      ? lipat(baris, barisKj, tabel)
      : '<div class="kt-lintas"><table class="kt-tabel kt-kj"><thead><tr><th>No</th><th>Riset / Proyek</th><th>Tahun</th><th>Keterangan</th></tr></thead><tbody>' +
        '<tr class="kt-lorem" data-lorem="1"><td>1</td><td>' + LOREM_PENDEK + '</td><td>0000</td><td>' + LOREM_PENDEK + '</td></tr></tbody></table></div>'));

    // 8-11. luaran dari SINTA / luaran.xlsx
    var kat = function (re) { return pub.filter(function (p) { return re.test(p.kategori || '') || re.test(p.sumber || ''); }); };
    h.push(bagian(8, 'Kekayaan intelektual (HKI / paten)', daftarLuaran(pub.filter(function (p) { return p.sumber === 'paten' || /paten/i.test(p.kategori || ''); }))));
    var jurnalIntl = pub.filter(function (p) { return p.kategori === 'Jurnal Internasional'; });
    var jurnalNas = pub.filter(function (p) { return p.kategori === 'Jurnal Nasional'; });
    var j = '';
    if (jurnalIntl.length) j += '<p class="kt-sub" style="margin-top:0">Jurnal internasional · ' + jurnalIntl.length + '</p>' + daftarLuaran(jurnalIntl);
    if (jurnalNas.length) j += '<p class="kt-sub">Jurnal nasional · ' + jurnalNas.length + '</p>' + daftarLuaran(jurnalNas);
    h.push(bagian(9, 'Publikasi (jurnal)', j || loremP()));
    h.push(bagian(10, 'Prosiding seminar', daftarLuaran(pub.filter(function (p) { return p.kategori === 'Prosiding Internasional'; }))));
    h.push(bagian(11, 'Buku', daftarLuaran(pub.filter(function (p) { return p.sumber === 'buku' || /^Book/.test(p.kategori || ''); }))));

    // Data SINTA tambahan (di luar urutan CV; tanpa Skor SINTA): penelitian, pengabdian, statistik, grafik, metrik
    h.push('<h2 class="kt-h2 kt-blok" style="margin-top:56px">Data SINTA</h2>');
    h.push(bagian('', 'Penelitian', daftarLuaran(pub.filter(function (p) { return p.sumber === 'penelitian'; }))));
    h.push(bagian('', 'Pengabdian kepada masyarakat', daftarLuaran(pub.filter(function (p) { return p.sumber === 'ppm'; }))));
    var sc = m.scopus || {}, gs = m.scholar || {}, g = d.grafik || {};
    if (mau('statistik')) {
      var u2 = [];
      if (sc.hindex != null) u2.push(tile('navy pola', 's3', num(sc.hindex), 'h-index Scopus', true));
      if (sc.artikel != null) u2.push(tile('putih', 's3', num(sc.artikel), 'Artikel Scopus', true));
      if (sc.sitasi != null) u2.push(tile('abu', 's3', num(sc.sitasi), 'Sitasi Scopus', true));
      if (gs.sitasi != null) u2.push(tile('lime pola', 's3', num(gs.sitasi), 'Sitasi Google Scholar', true));
      if (u2.length) h.push('<div class="kt-grid" style="margin-top:32px">' + u2.join('') + '</div>');
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

    var lengkap = !!(d.batas_daftar && d.batas_daftar.lengkap);
    h.push('<div class="kt-kaki"><span>' + (lengkap ? '' : 'Publikasi, HKI, prosiding, dan buku dari SINTA memuat ' + ((d.batas_daftar || {}).per_kategori || 10) +
      ' luaran terbaru per kategori' + (t.sinta ? ' — daftar lengkap di <a href="' + esc(t.sinta) + '" target="_blank" rel="noopener">profil SINTA</a>' : '') + '. ') +
      'Diperbarui otomatis · ' + esc((d.diperbarui || '').slice(0, 10)) + '</span></div>');
    akar.innerHTML = h.join('');
  }

})();

}
if(document.readyState==='loading'){document.addEventListener('DOMContentLoaded',__go)}else{__go()}})();
