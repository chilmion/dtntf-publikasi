// Halaman prodi rancangan v2 (hero + kartu bento + akordeon) + revisi 19 Nov 2026: SVG tajam, kartu dokumen (tautan kosong), gambar tidak melebihi ukuran asli.
// Dibuat dari manual/prodi/*.md oleh scripts/buat_prodi.py -> elementor/prodi-<nama>.json.
// Jalankan di EDITOR Elementor halaman yang dituju (buka .../wp-admin/post.php?post=<id>&action=elementor), lalu: await deployProdiV2('teknik-nuklir', '<sha>')
//   nama: teknik-nuklir (/prodi/ id 688) | teknik-fisika (/prodi-s1-teknik-fisika/ id 1763) | iup-teknik-nuklir (/iup-teknik-nuklir/) | magister-teknik-fisika (/program-studi-magister-teknik-fisika/)
// Mengganti SELURUH isi halaman. Di tf.ugm.ac.id IUP & Magister sudah ada (rancangan lama, salinan TN) -> cukup buka editornya dan jalankan ini.
// v1: IUP = id 2345, Magister = id 2346 (dibuat 19 Nov untuk uji).
window.deployProdiV2 = async function (nama, sha) {
  const T = await (await fetch('https://raw.githubusercontent.com/chilmion/dtntf-publikasi/' + sha + '/elementor/prodi-' + nama + '.json')).json();
  const top = elementor.getPreviewContainer(); const kids = [...(top.children.models || top.children)];
  kids.forEach(c => $e.run('document/elements/delete', {container: c}));
  T.content.forEach((el, i) => $e.run('document/elements/create', {container: top, model: el, options: {at: i}}));
  await $e.run('document/save/default', {force: true});
  return 'ok ' + kids.length + ' -> ' + T.content.length;
};
