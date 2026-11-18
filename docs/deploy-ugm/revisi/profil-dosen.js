// Profil dosen (revisi dosen 18 Nov 2026): hapus jabatan fungsional, institusi, telepon institusi, riwayat pekerjaan, penghargaan,
// tulisan "DATA SINTA" dan nominal rupiah (dana) pada penelitian/PPM; "Pengalaman kerjasama dan penelitian" -> "Pengalaman kerjasama"; bagian dinomori ulang 1-9.
// Sama dengan perubahan di widget/katur-profil-cv.html. Menambal widget yang SUDAH terpasang di 38 halaman profil lewat Elementor (tanpa membuka editor).
// Jalankan di tab wp-admin biasa:   await patchProfilDosen(['<id halaman>', ...])   atau   await patchProfilDosen('semua')  (slug dari dosen.csv)
window.PROFIL_GANTI = [["      kv('Jabatan fungsional', id.jabatan_fungsional ? esc(id.jabatan_fungsional) : lorem(true)) +\n", ""], ["      kv('Institusi', id.institusi ? esc(id.institusi) : lorem(true), true) +\n", ""], ["kv('Telepon institusi', id.telepon_institusi ? esc(id.telepon_institusi) : lorem(true)) + '</div>'));", "'</div>'));"], ["    h.push(bagian(4, 'Riwayat pekerjaan', riwayat(cv.pekerjaan)));\n", ""], ["    h.push(bagian(6, 'Penghargaan', riwayat(cv.penghargaan)));\n", ""], ["bagian(5, 'Organisasi profesi'", "bagian(4, 'Organisasi profesi'"], ["bagian(7, 'Pengalaman kerjasama dan penelitian'", "bagian(5, 'Pengalaman kerjasama'"], ["bagian(8, 'Kekayaan intelektual", "bagian(6, 'Kekayaan intelektual"], ["bagian(9, 'Publikasi (jurnal)'", "bagian(7, 'Publikasi (jurnal)'"], ["bagian(10, 'Prosiding seminar'", "bagian(8, 'Prosiding seminar'"], ["bagian(11, 'Buku'", "bagian(9, 'Buku'"], ["h.push('<h2 class=\"kt-h2 kt-blok\" style=\"margin-top:56px\">Data SINTA</h2>');", "h.push('<div class=\"kt-blok\" style=\"margin-top:56px\"></div>');"], ["return p.jenis_paten || p.dana || (p.isbn", "return p.jenis_paten || (p.isbn"]];
window.patchProfilDosen = async function (ids, slugs) {
  if (!window.R) { const t = await (await fetch('https://raw.githubusercontent.com/chilmion/dtntf-publikasi/main/docs/deploy-ugm/rancang.js', {cache: 'no-store'})).text(); (0, eval)(t); }
  const H = {headers: {'X-WP-Nonce': wpApiSettings.nonce}};
  if (ids === 'semua') { ids = []; for (const sl of slugs) { const r = await (await fetch('/wp-json/wp/v2/pages?slug=' + sl + '&status=any&_fields=id', H)).json(); if (r[0]) ids.push(r[0].id); else ids.push('?' + sl); } }
  const log = [];
  for (const id of ids) {
    if (String(id).startsWith('?')) { log.push(id + ' tidak ada'); continue; }
    const html = await (await fetch('/wp-admin/post.php?post=' + id + '&action=elementor', {credentials: 'include'})).text();
    const i = html.indexOf('"initial_document":'); if (i < 0) { log.push(id + ' tanpa dokumen'); continue; }
    let s = html.indexOf('{', i), d = 0, inStr = false, esc = false, e = s;
    for (; e < html.length; e++) { const c = html[e]; if (inStr) { if (esc) esc = false; else if (c === '\\') esc = true; else if (c === '"') inStr = false; } else if (c === '"') inStr = true; else if (c === '{') d++; else if (c === '}') { d--; if (d === 0) break; } }
    const doc = JSON.parse(html.slice(s, e + 1)); let n = 0;
    const walk = a => a.forEach(el => { if (el.widgetType === 'html' && String(el.settings.html || '').includes('kt-bagian') || (el.widgetType === 'html' && String(el.settings.html || '').includes('Riwayat pendidikan'))) { let h = String(el.settings.html); let ch = 0; for (const [a1, b1] of window.PROFIL_GANTI) { if (h.includes(a1)) { h = h.split(a1).join(b1); ch++; } } if (ch) { el.settings.html = h; n += ch; } } if (el.elements) walk(el.elements); });
    walk(doc.elements || []);
    if (!n) { log.push(id + ' sudah/tidak ada perubahan'); continue; }
    log.push(id + ' ' + await R.simpan(id, doc.elements, (doc.settings && doc.settings.settings) || {}) + ' (' + n + ' ganti)');
  }
  return log.join('\n');
};
