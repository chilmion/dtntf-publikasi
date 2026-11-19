// Mitra (E3) dan Pengabdian (E2) — dijalankan di EDITOR Elementor halaman tujuan.
//   Mitra (v1 id 1750; tf: id halaman /mitra/): await deployMitraPengabdian('mitra', '<sha>')      -> pertahankan banner (container pertama), ganti sisanya
//   Pengabdian (v1 id 1917; tf: id /pengabdian/):  await deployMitraPengabdian('pengabdian', '<sha>') -> ganti seluruh isi
// Data-base: di v1 dipakai raw.githubusercontent per SHA (Pages hanya dari main). Di tf setelah PR digabung, pakai data-base asli (jangan ganti) -> argumen ganti=false.
window.deployMitraPengabdian = async function (jenis, sha, gantiBase = true) {
  let tx = await (await fetch('https://raw.githubusercontent.com/chilmion/dtntf-publikasi/' + sha + '/elementor/katur-' + jenis + '.json')).text();
  if (gantiBase) tx = tx.split('https://chilmion.github.io/dtntf-publikasi/data').join('https://raw.githubusercontent.com/chilmion/dtntf-publikasi/' + sha + '/data');
  const T = JSON.parse(tx), top = elementor.getPreviewContainer(), kids = [...(top.children.models || top.children)];
  const mulai = jenis === 'mitra' ? 1 : 0;
  kids.slice(mulai).forEach(c => $e.run('document/elements/delete', {container: c}));
  T.content.forEach((el, i) => $e.run('document/elements/create', {container: top, model: el, options: {at: mulai + i}}));
  await $e.run('document/save/default', {force: true});
  return 'ok';
};
