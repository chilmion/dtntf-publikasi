// Halaman prodi TN (revisi dosen D1+D2, 19 Nov 2026): kartu dokumen bergambar sampul + tombol Unduh.
// Tautan SENGAJA KOSONG (belum ada berkas final dari jurusan). Nanti isi href tiap tombol: edit widget HTML -> ganti <a class="pd-btn"> menjadi <a class="pd-btn" href="URL"> (hapus aria-disabled).
// Dipakai di EDITOR Elementor halaman prodi (v1 id 688; tf.ugm.ac.id id 688): await deployProdiDokumen()
// Sisip: (1) setelah paragraf terakhir bagian "Kurikulum" (sebelum judul "Bidang Peminatan"), (2) setelah paragraf terakhir "Laporan Kinerja Akademik" (sebelum judul "Mitra dan Kerja Sama").
window.deployProdiDokumen = async function () {
  const CSS = '<style>.pd-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(310px,1fr));gap:20px;margin:28px 0 8px;max-width:1120px}' +
    '.pd-card{display:flex;gap:18px;align-items:center;padding:18px;border:1px solid #E3E3E3;border-radius:16px;background:#fff}' +
    '.pd-cover{flex:0 0 104px;aspect-ratio:3/4;border-radius:8px;background:linear-gradient(165deg,#073C64 0%,#1A2C43 100%);color:#fff;padding:11px 10px;display:flex;flex-direction:column;justify-content:space-between;position:relative;overflow:hidden;box-shadow:0 6px 16px rgba(7,60,100,.22)}' +
    '.pd-cover::after{content:"";position:absolute;left:0;right:0;bottom:0;height:5px;background:#C8E86D}' +
    '.pd-cover small{font-size:7px;line-height:1.3;font-weight:600;letter-spacing:.02em;opacity:.85;display:block}' +
    '.pd-cover b{font-size:13px;line-height:1.2;font-weight:800;display:block}' +
    '.pd-cover i{font-style:normal;font-size:7px;font-weight:700;color:#C8E86D}' +
    '.pd-body{min-width:0}.pd-body h4{margin:0 0 4px;font-size:17px;line-height:1.3;font-weight:700;color:#073C64!important;word-spacing:0!important;letter-spacing:0!important;font-family:"Plus Jakarta Sans",sans-serif!important}' +
    '.pd-body p{margin:0 0 14px;font-size:14px;line-height:1.5;color:#5B6670}' +
    '.pd-btn{display:inline-flex;align-items:center;gap:8px;padding:10px 18px;border-radius:999px;background:#073C64;color:#fff!important;font-size:14px;font-weight:600;text-decoration:none!important;line-height:1;word-spacing:0!important}' +
    '.pd-btn:hover{background:#C8E86D;color:#073C64!important}.pd-cover b,.pd-cover small,.pd-cover i{word-spacing:0!important;color:inherit}.pd-cover i{color:#C8E86D}.pd-btn svg{width:16px;height:16px}</style>';
  const IC = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3v12m0 0l-4-4m4 4l4-4M4 20h16"/></svg>';
  const kartu = (judul, ket, sampul, tag) => '<div class="pd-card"><div class="pd-cover"><small>DEPARTEMEN TEKNIK NUKLIR DAN TEKNIK FISIKA · UGM</small><b>' + sampul + '</b><i>' + tag + '</i></div>' +
    '<div class="pd-body"><h4>' + judul + '</h4><p>' + ket + '</p><a class="pd-btn" role="button" aria-disabled="true" title="Dokumen segera tersedia">' + IC + 'Unduh dokumen</a></div></div>';
  const KUR = CSS + '<div class="pd-grid" style="max-width:560px">' + kartu('Dokumen Kurikulum 2026', 'Struktur mata kuliah, capaian pembelajaran, dan peta kurikulum Program Sarjana Teknik Nuklir.', 'Kurikulum<br>2026', 'S1 TEKNIK NUKLIR · PDF') + '</div>';
  const LK = CSS + '<div class="pd-grid">' + [['2024/2025', 'TA 2024/2025'], ['2023/2024', 'TA 2023/2024'], ['2022/2023', 'TA 2022/2023'], ['2021/2022', 'TA 2021/2022']]
    .map(a => kartu('Laporan Kinerja Akademik ' + a[1], 'Laporan kinerja Program Sarjana Teknik Nuklir tahun akademik ' + a[0] + '.', 'Laporan<br>Kinerja<br>' + a[0], 'S1 TEKNIK NUKLIR · PDF')).join('') + '</div>';
  const walk = (c, f) => { f(c); const ch = c.children; if (ch) (ch.models || ch).forEach(x => walk(x, f)); };
  let P = null; walk(elementor.getPreviewContainer(), c => { if (!P && c.model && c.model.get('elType') === 'container' && (c.children.models || c.children).some(x => x.model.get('widgetType') === 'heading' && x.settings.get('title') === 'Kurikulum')) P = c; });
  if (!P) throw new Error('kontainer tidak ketemu');
  const kids = () => (P.children.models || P.children);
  const at = judul => kids().findIndex(x => x.model.get('widgetType') === 'heading' && (x.settings.get('title') || '').trim().startsWith(judul));
  const ins = (idx, html, t) => $e.run('document/elements/create', {container: P, model: {elType: 'widget', widgetType: 'html', settings: {html, _title: t}}, options: {at: idx}});
  // sisip yang kedua dulu (indeks tidak bergeser)
  const iM = at('Mitra dan Kerja Sama'); if (iM < 0) throw new Error('heading Mitra tidak ada'); ins(iM, LK, 'Dokumen Laporan Kinerja');
  const iB = at('Bidang Peminatan'); if (iB < 0) throw new Error('heading Bidang Peminatan tidak ada'); ins(iB, KUR, 'Dokumen Kurikulum');
  await $e.run('document/save/default', {force: true});
  return 'ok';
};
