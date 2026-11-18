// Jarak antar kata: kit Elementor (v1: kit 217 / UGM: kit tema) memberi word-spacing 6px pada h1-h3 sehingga "Prof. Dr. Ir. Faridah" terlihat renggang.
// Perbaikan per widget: typography_word_spacing = 0 pada semua heading, teks, dan tombol. Jalankan di tab EDITOR halaman (setelah editor siap), SETELAH tiap deploy:
//   await kernFix()
window.kernFix = async function () {
  const Z = {unit: 'px', size: 0, sizes: []}; let n = 0;
  const walk = a => a.forEach(e => {
    if (e.elType === 'widget' && ['heading', 'text-editor', 'button'].includes(e.widgetType)) {
      const s = {typography_typography: 'custom', typography_word_spacing: Z};
      if (!e.settings.typography_font_size && e.widgetType !== 'button') delete s.typography_typography; // jangan paksa tipografi kustom bila belum ada
      $e.run('document/elements/settings', {container: elementor.getContainer(e.id), settings: Object.assign({typography_word_spacing: Z}, e.settings.typography_typography === 'custom' ? {} : {typography_typography: 'custom'})}); n++;
    }
    if (e.elements) walk(e.elements);
  });
  walk(elementor.config.initial_document.elements);
  await $e.run('document/save/default');
  return n;
};
