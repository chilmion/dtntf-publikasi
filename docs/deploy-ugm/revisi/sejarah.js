// Sejarah (revisi dosen 18 Nov 2026): peta jalan 2 baris + foto di tiap titik + kartu bergambar.
// Dibuat dan diuji di v1.katur.online (halaman id 779). Untuk tf.ugm.ac.id: jalankan di tab wp-admin biasa (bukan editor):
//   await deploySejarah(16872)      // 16872 = id halaman "sejarah-v2" di tf.ugm.ac.id
// Lalu buka editor halaman itu dan jalankan: await nolPadding()
// (kontainer bersarang tanpa padding bawaan Elementor 10px bikin teks bergeser 30px dan garis aksen jadi kotak).
// Foto = Unsplash (ilustrasi); ganti dengan foto arsip jurusan bila ada.
window.deploySejarah = async function (halamanId) {
  if (!window.R) { const t = await (await fetch('https://raw.githubusercontent.com/chilmion/dtntf-publikasi/main/docs/deploy-ugm/rancang.js', {cache: 'no-store'})).text(); (0, eval)(t); }
  const {Banner, Sec, Head, Grid, Card, H, Pg, C, crumb, wd, simpan, T, Im} = R;
  const FOTO = ['1778867127717-8e55e8e9dea4','1589982334462-f1cead0e1519','1745571479662-54a2ad1c747f','1781330168090-a2b6721eb435','1759328381007-64559a862aa6','1761195689615-9469b65dac01','1591200834528-4050ce99fe78','1623075838713-24d8993464d2','1630142895963-6996ae6b3a5b','1581091226033-d5c48150dbaa','1772376920820-4fb715c21e79','1623075840956-c95a6b0ea89e','1581092459682-ccfffd6ddc37','1630142896875-d71a6ee6db03','1781330189305-d92d518dc28d','1781330175070-6ec7e25f57aa','1648201158624-7141d2bb44e9','1581092160607-ee22621dd758','1622103339597-1e7d9918b4e1','1627488043116-f66f15a31bfe'];
  const U = JSON.parse(localStorage.getItem('__sejarahFoto') || '{}');
  for (const id of FOTO) {
    if (U[id]) continue;
    const b = await (await fetch('https://images.unsplash.com/photo-' + id + '?w=1000&fm=jpg&q=78&fit=max')).blob();
    const j = await (await fetch('/wp-json/wp/v2/media', {method: 'POST', headers: {'X-WP-Nonce': wpApiSettings.nonce, 'Content-Disposition': 'attachment; filename="sejarah-' + id.slice(0, 10) + '.jpg"', 'Content-Type': 'image/jpeg'}, body: b})).json();
    if (!j.id) throw new Error('unggah gagal ' + id);
    U[id] = {id: j.id, url: j.source_url}; localStorage.setItem('__sejarahFoto', JSON.stringify(U));
  }
  const g = k => U[k];
  const P = [
    {y: '1974–1978', n: 'Periode Awal Berdiri', t: 'Kerja sama UGM dan BATAN', rm: '1778867127717-8e55e8e9dea4', items: [
      ['1974', 'Kerjasama UGM - BATAN', 'UGM dan Badan Tenaga Atom Nasional (BATAN) menjalin Kerjasama Induk pada tanggal 5 Desember 1974 yang kemudian diperpanjang pada 22 Februari 1978.', '1591200834528-4050ce99fe78'],
      ['1978', 'Pembukaan Jurusan Teknik Nuklir', 'Soetojo Tjokrodihardjo selaku Dekan Fakultas Teknik UGM bersama Prof. A. Baiquni, M.Sc., Ph.D selaku Direktur Jenderal BATAN secara resmi membuka Jurusan Teknik Nuklir.', '1623075838713-24d8993464d2'],
      ['1981', 'Program S-1 Teknik Nuklir', 'Fakultas Teknik UGM memutuskan untuk menyelenggarakan Program Pendidikan S-1 Teknik Nuklir melalui proyek PERINTIS I.', '1630142895963-6996ae6b3a5b']]},
    {y: '1981–1993', n: 'Periode Pertumbuhan', t: 'Kurikulum dan gedung baru', rm: '1589982334462-f1cead0e1519', items: [
      ['1983', 'Pergantian Kurikulum', 'Kurikulum 1981 berjalan sekitar 2 tahun hingga 1983. Setelah itu diterapkan Kurikulum 1983 yang ditetapkan oleh Konsorium Ilmu Pengetahuan dan Teknologi.', '1581091226033-d5c48150dbaa'],
      ['1988', 'Program Kerjasama dengan Kraftwerk Union - Siemens', 'Kerjasama yang dimaksud adalah dalam bentuk hibah alat lab dan pembiayaan studi lanjut dan riset.', '1772376920820-4fb715c21e79'],
      ['1993', 'Pemindahan Gedung', 'Pada tahun 1993, semua kegiatan dipindahkan dari Sekip ke gedung baru yang terletak di Jalan Grafika 2. Mulai saat itu, laboratorium dilengkapi dengan mendirikan Lab. Radiokimia dan Lab. Kimia Terapan, Lab. Komputasi, dan Lab. Elektronika Nuklir.', '1623075840956-c95a6b0ea89e']]},
    {y: '1995–1998', n: 'Periode Pertumbuhan', t: 'Alih jalur dan kurikulum baru', rm: '1745571479662-54a2ad1c747f', items: [
      ['1996', 'Perubahan Kurikulum', 'Setelah diterapkan selama 12 tahun sejak 1983, kurikulum diperbarui dan diterapkan mulai Tahun Akademik 1996/1997. Diharapkan kurikulum baru tersebut dapat menyesuaikan perkembangan teknologi nuklir pada skala nasional dan internasional.', '1581092459682-ccfffd6ddc37'],
      ['1995', 'Alih jalur Pendidikan Ahli Teknik Nuklir (PATN)', 'Jurusan Teknik Nuklir Fakultas Teknik UGM menyelenggarakan pendidikan program alih jalur D3 Pendidikan Ahli Teknik Nuklir (PATN - S1 Teknik Nuklir) dengan penekanan minat Teknik Akselerator Nuklir. Program ini merupakan peningkatan program kerjasama dengan BATAN.', '1630142896875-d71a6ee6db03'],
      ['1997', 'Program Alih Jalur D3 Elektro Medik - S1 TN', 'Jurusan Teknik Nuklir bekerjasama dengan Departemen Kesehatan RI melaksanakan program alih jalur D3 Teknik Elektro Medik - S1 Teknik Nuklir dengan penekanan minat Instrumentasi Medik.', '1745571479662-54a2ad1c747f']]},
    {y: '1998–2016', n: 'Periode Pengembangan', t: 'Lahirnya Teknik Fisika', rm: '1781330168090-a2b6721eb435', items: [
      ['1998', 'Lahirnya Teknik Fisika', 'Memasuki tahun akademik 1998/1999, Jurusan Teknik Nuklir memiliki 2 (dua) program studi, yakni Program Studi Teknik Nuklir dan Program Studi Fisika Teknik. Sementara itu nama Jurusan telah diproses untuk diubah menjadi Jurusan Teknik Fisika, dan mulai diberlakukan sejak tanggal 25 Juni 2001.', '1781330189305-d92d518dc28d'],
      ['1999/2000', 'Penyelenggaraan S2 Magister Rekayasa Keselamatan Industri', 'Jurusan Teknik Fisika Fakultas Teknik UGM mulai menyelenggarakan program pendidikan Magister Rekayasa Keselamatan Industri (MRKI). Dalam tahun akademik yang sama, dilakukan perubahan kurikulum yang mendasar dengan beban mahasiswa dari 154 SKS menjadi 144 SKS dalam 8 (delapan) semester.', '1781330175070-6ec7e25f57aa'],
      ['2013–2016', 'Peningkatan Kerjasama', 'Pada tahun 2014, Program Studi Teknik Nuklir resmi termasuk dalam International Nuclear Security Education Network (INSEN) yang digagas oleh International Atomic Energy Agency (IAEA). Selain itu, diselenggarakan Konferensi Internasional ASTECHNOVA yang meningkatkan kerjasama dengan NAMCSSTC.', '1648201158624-7141d2bb44e9']]},
    {y: '2016–2021', n: 'Periode Pengembangan', t: 'Departemen dan akreditasi', rm: '1759328381007-64559a862aa6', items: [
      ['2016', 'Perubahan Nama dari Jurusan Menjadi Departemen', 'Pada tahun 2016, UGM melakukan perubahan struktur organisasi dan tata kelola fakultas berdasar Peraturan Rektor No. 809/P/SK/HT/2015. Seiring dengan perubahan tersebut, nama Jurusan Teknik Fisika berubah menjadi Departemen Teknik Nuklir dan Teknik Fisika.', '1622103339597-1e7d9918b4e1'],
      ['2016', 'Dibukanya S2 Teknik Fisika', 'Surat Keputusan Rektor Universitas Gadjah Mada No. 515/UN1.P.1/SK/HUKOR/2016 tertanggal 15 Februari 2016 tentang ijin operasional Program Studi Magister Teknik Fisika di Universitas Gadjah Mada.', '1581092160607-ee22621dd758'],
      ['2021', 'Akreditasi IABEE Berstatus Penuh', 'Pada 2021, DTNTF mendapatkan visitasi dari IABEE dan berdasarkan hasil evaluasi, status Prodi Teknik Nuklir dan Teknik Fisika terakreditasi IABEE secara penuh.', '1627488043116-f66f15a31bfe']]},
    {y: '2022–Sekarang', n: 'Ekspansi Global dan Nasional', t: 'Kerja sama yang makin luas', rm: '1761195689615-9469b65dac01', items: [
      ['2022–Sekarang', 'Ekspansi Global dan Nasional', 'Melebarkan kerja sama dengan perusahaan dan universitas di tingkat nasional maupun global.', '1761195689615-9469b65dac01']]}
  ];
  const node = (p, i) => '<a class="dt-rm-n" href="#periode-' + (i + 1) + '"><span class="dt-rm-img" style="background-image:url(' + g(p.rm).url + ')"></span><span class="dt-rm-dot"></span><span class="dt-rm-y">' + p.y + '</span><span class="dt-rm-p">' + p.n + '</span><span class="dt-rm-t">' + p.t + '</span></a>';
  const row = (label, ps, off, n) => '<div class="dt-rm-row"><div class="dt-rm-lab">' + label + '</div><div class="dt-rm-g" style="--n:' + n + '">' + ps.map((p, k) => node(p, off + k)).join('') + '</div></div>';
  const CSS = '<style>.dt-rm{display:flex;flex-direction:column;gap:44px}.dt-rm-lab{font-family:"Plus Jakarta Sans",sans-serif;font-weight:800;font-size:22px;letter-spacing:-.02em;color:#073C64;margin-bottom:16px}.dt-rm-g{display:grid;grid-template-columns:repeat(var(--n),1fr);gap:20px}.dt-rm-n{position:relative;display:flex;flex-direction:column;gap:6px;text-decoration:none;color:#161616}.dt-rm-img{display:block;height:130px;border-radius:12px;background-size:cover;background-position:center;margin-bottom:22px}.dt-rm-dot{position:relative;z-index:2;width:20px;height:20px;border-radius:50%;background:#fff;border:5px solid #073C64;margin-bottom:8px}.dt-rm-n::before{content:"";position:absolute;left:10px;top:152px;height:4px;width:calc(100% + 20px);background:#073C64;border-radius:2px}.dt-rm-g .dt-rm-n:last-child::before{opacity:0}.dt-rm-row:last-child .dt-rm-n:nth-child(2)::before{opacity:0}.dt-rm-row:last-child .dt-rm-n:nth-child(2) .dt-rm-dot{border-color:#C8E86D;background:#073C64}.dt-rm-y{font-family:"Plus Jakarta Sans",sans-serif;font-weight:800;font-size:26px;line-height:1.1;letter-spacing:-.02em;color:#073C64}.dt-rm-p{font-family:Barlow,sans-serif;font-weight:700;font-size:16px}.dt-rm-t{font-family:Barlow,sans-serif;font-size:15px;line-height:1.4;color:#636363}.dt-rm-n:hover .dt-rm-y{color:#003D79}@media(max-width:1024px){.dt-rm-g{grid-template-columns:repeat(2,1fr)}.dt-rm-n::before{display:none}}@media(max-width:600px){.dt-rm-g{grid-template-columns:1fr}.dt-rm-y{font-size:22px}}</style>';
  const rm = '<div class="dt-rm">' + row('1974 – 2016', P.slice(0, 4), 0, 4) + row('2016 – Sekarang', P.slice(4), 4, 4) + '</div>' + CSS;
  const yr = s => Pg('<strong>' + s + '</strong>', {css: 'selector,selector p,selector strong{font-family:"Plus Jakarta Sans",sans-serif;font-size:30px;font-weight:800;line-height:1.1;letter-spacing:-.02em;color:#073C64;margin:0}'});
  const sec = P.map((p, i) => Sec([
    C([Pg('<strong>' + p.y + '</strong>', {css: 'selector,selector p,selector strong{font-family:"Plus Jakarta Sans",sans-serif;font-size:44px;font-weight:800;line-height:1.05;letter-spacing:-.025em;color:#073C64;margin:0}'}), H(p.n, 'h2')], {gap: 6}),
    Grid(p.items.map(it => { const m = g(it[3]); return Card([Im(m.url, m.id, {alt: it[1], ratio: '16/10', radius: 12}), yr(it[0]), H(it[1], 'h3'), Pg(it[2], {small: true, color: '#4A4A4A'})], {gap: 12}); }), {cols: 3, gap: 20})
  ], {bg: i % 2 ? T.bg : T.white, pt: 48, pb: 48}));
  sec.forEach((s, i) => { s.settings._element_id = 'periode-' + (i + 1); });
  const els = [Banner('Sejarah', crumb('Sejarah', 'Tentang Kami')),
    Sec([Head('Sejarah Departemen Teknik Nuklir dan Teknik Fisika (DTNTF)', 'Perjalanan jurusan dari kerja sama UGM dan BATAN pada 1974 hingga pengembangan program sarjana, magister, dan kerja sama global saat ini.')], {pb: 24}),
    Sec([H('Peta jalan', 'h2'), wd('html', {html: rm})], {pt: 16, pb: 48}), ...sec];
  return await simpan(halamanId, els, {});
};
// Jalankan di tab EDITOR halaman (setelah editor siap, elementor.getContainer berfungsi).
window.nolPadding = async function () {
  const Z = {unit: 'px', top: '0', right: '0', bottom: '0', left: '0', isLinked: true}; let n = 0;
  const walk = (a, d) => a.forEach(e => { if (e.elType === 'container' && d > 0 && !(e.settings && e.settings.padding)) { $e.run('document/elements/settings', {container: elementor.getContainer(e.id), settings: {padding: Z}}); n++; } if (e.elements) walk(e.elements, d + 1); });
  walk(elementor.config.initial_document.elements, 0); await $e.run('document/save/default'); return n;
};
