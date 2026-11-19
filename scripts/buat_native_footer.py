#!/usr/bin/env python3
"""Footer v1 untuk halaman 'new' (Home v2, id 16487) di tf, native: lambang + alamat, Peta & Arah, Terhubung Bersama Kami (ikon sosial + peta), Terakreditasi Oleh,
kolom Pendidikan / Layanan / Tautan Eksternal, bilah lime hak cipta. Hanya ditambahkan di halaman new (bukan template footer global)."""
import json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import buat_elementor as be  # noqa: E402
import buat_profil_dosen as bp  # noqa: E402

ROOT = be.ROOT
B = "https://tf.ugm.ac.id/wp-content/uploads/sites/7/2026/11/"
NAVY, LIME = "#073C64", "#C8E86D"


def tautan(items):
    h = "".join(f'<p style="margin:0 0 8px"><a href="{u}" style="color:#FFFFFF">{t}</a></p>' for t, u in items)
    return be.widget("text-editor", editor=h, text_color="#FFFFFF", typography_typography="custom", typography_font_family="Barlow", typography_font_size=be.ukuran_(15), _title="Tautan")


def judul(t, ukuran=22):
    return be.widget("heading", title=t, header_size="h3", title_color="#FFFFFF", typography_typography="custom", typography_font_family="Plus Jakarta Sans",
                     typography_font_weight="400", typography_font_size=be.ukuran_(ukuran), _title=t)


def kol(anak, lebar, judul_="Kolom"):
    return be.container(anak, content_width="full", flex_direction="column", flex_gap=be.gap(10), padding=bp.ruang(0), width=be.ukuran(lebar, "%"), width_tablet=be.ukuran(48, "%"),
                        width_mobile=be.ukuran(100, "%"), _title=judul_)


def main():
    lambang = be.widget("image", image={"url": B + "dtntf-footer-lambang-ugm-putih.png", "id": "", "alt": "Lambang Universitas Gadjah Mada"}, image_size="full",
                        width=be.ukuran(88, "px"), align="left", _title="Lambang UGM")
    alamat = be.widget("text-editor", editor="<p style=\"margin:0\"><strong>Departemen Teknik Nuklir &amp; Teknik Fisika<br>Fakultas Teknik, Universitas Gadjah Mada</strong><br>Jl. Grafika 2, Yogyakarta 55281, Indonesia<br>"
                       "Phone/Fax: +62-274-580882<br>Email: <a href=\"mailto:dtntf.ft@ugm.ac.id\" style=\"color:#FFFFFF\">dtntf.ft@ugm.ac.id</a></p>",
                       text_color="#FFFFFF", typography_typography="custom", typography_font_family="Barlow", typography_font_size=be.ukuran_(15), _title="Alamat")
    peta_link = tautan([("Peta &amp; Arah", "https://maps.app.goo.gl/NPn45c4r3v4Mxj257")])
    sosial = be.widget("social-icons", social_icon_list=[
        {"_id": be.eid()[:7], "social_icon": {"value": "fab fa-instagram", "library": "fa-brands"}, "link": {"url": "https://www.instagram.com/dtntf_ugm/", "is_external": "on", "nofollow": "", "custom_attributes": ""}},
        {"_id": be.eid()[:7], "social_icon": {"value": "fab fa-youtube", "library": "fa-brands"}, "link": {"url": "https://www.youtube.com/channel/UCO-95rJvaOPC_ujUxn5BK7w", "is_external": "on", "nofollow": "", "custom_attributes": ""}},
        {"_id": be.eid()[:7], "social_icon": {"value": "fab fa-facebook", "library": "fa-brands"}, "link": {"url": "https://www.facebook.com/dtntf.ft.ugm/", "is_external": "on", "nofollow": "", "custom_attributes": ""}},
        {"_id": be.eid()[:7], "social_icon": {"value": "fab fa-x-twitter", "library": "fa-brands"}, "link": {"url": "https://x.com/dtntf_ugm", "is_external": "on", "nofollow": "", "custom_attributes": ""}}],
        shape="rounded", align="left", icon_color="custom", icon_primary_color="#FFFFFF", icon_secondary_color="#073C64",
        icon_size={"unit": "px", "size": 14, "sizes": []}, icon_padding={"unit": "em", "size": 0.7, "sizes": []}, _title="Ikon sosial")
    # iframe Google Maps DIBLOKIR kebijakan keamanan tf (frame-src hanya self + YouTube) -> gambar peta statis (OpenStreetMap) bertaut ke Google Maps
    peta = be.widget("image", image={"url": B + "dtntf-footer-peta.png", "id": "", "alt": "Peta lokasi Departemen Teknik Nuklir dan Teknik Fisika UGM (Jl. Grafika 2, Yogyakarta)"},
                     image_size="full", width=be.ukuran(100, "%"), image_border_radius=bp.sudut(10), link_to="custom",
                     link={"url": "https://maps.app.goo.gl/NPn45c4r3v4Mxj257", "is_external": "on", "nofollow": "", "custom_attributes": ""}, _title="Peta kecil")
    akreditasi = be.container([be.widget("image", image={"url": B + "dtntf-footer-iabee.png", "id": "", "alt": "IABEE"}, image_size="full", width=be.ukuran(100, "%"), _element_width="initial",
                                         _element_custom_width=be.ukuran(56, "px"), _title="IABEE"),
                               be.widget("image", image={"url": B + "dtntf-footer-ban-pt.png", "id": "", "alt": "BAN-PT"}, image_size="full", width=be.ukuran(100, "%"), _element_width="initial",
                                         _element_custom_width=be.ukuran(56, "px"), _title="BAN-PT")],
                              content_width="full", flex_direction="row", flex_gap=be.gap(10), padding=bp.ruang(0), _title="Logo akreditasi")
    kiri = kol([lambang, alamat, peta_link, judul("Terhubung Bersama Kami", 20), sosial, peta,
                bp.teks("<p><strong>Terakreditasi Oleh :</strong></p>", "#FFFFFF", 14, None), akreditasi], 36, "Alamat dan sosial")
    pend = kol([judul("Pendidikan"), tautan([("S1 - Teknik Fisika", "/prodi-s1-teknik-fisika/"), ("S1 - Teknik Nuklir", "/prodi/"), ("IUP Teknik Nuklir", "/iup-teknik-nuklir/"),
                                           ("S2 - Teknik Fisika", "/program-studi-magister-teknik-fisika/")])], 16, "Pendidikan")
    lay = kol([judul("Layanan"), tautan([("Simaster", "https://simaster.ugm.ac.id/"), ("SMS FT", "https://sms.ft.ugm.ac.id/dtntf"), ("Layanan Akademik", "/layanan-akademik/"),
                                       ("Layanan Alumni", "https://ft.ugm.ac.id/layanan-untuk-alumni/")])], 16, "Layanan")
    eks = kol([judul("Tautan Eksternal"), tautan([("Astechnova", "https://astechnova.ugm.ac.id/"), ("Fakultas Teknik", "http://ft.ugm.ac.id/"), ("Universitas Gadjah Mada", "https://ugm.ac.id/"),
                                                 ("Beasiswa UGM", "https://ditmawa.ugm.ac.id/category/info-beasiswa/"), ("UGM Career", "https://alumni.ugm.ac.id/ugmcareer/"),
                                                 ("eLearning (eLOK) UGM", "https://elok.ugm.ac.id/"), ("eJournals", "http://ezproxy.ugm.ac.id/menu")])], 22, "Tautan eksternal")
    isi = be.container([kiri, pend, lay, eks], content_width="boxed", boxed_width=be.ukuran(1280), flex_direction="row", flex_wrap="wrap", flex_gap=be.gap(32), flex_align_items="flex-start",
                       padding={"unit": "px", "top": "64", "right": "24", "bottom": "56", "left": "24", "isLinked": False}, _title="Isi footer")
    bar = be.container([bp.teks("<p><strong>© 2026 DTNTF - UNIVERSITAS GADJAH MADA</strong></p>", NAVY, 13, None),
                        bp.teks('<p style="text-align:right"><strong><a href="https://tf.ugm.ac.id/privacy_policy" style="color:#073C64">KEBIJAKAN PRIVASI/PRIVACY POLICY</a></strong></p>', NAVY, 13, None)],
                       content_width="boxed", boxed_width=be.ukuran(1280), flex_direction="row", flex_justify_content="space-between", flex_wrap="wrap", padding=bp.ruang(14), _title="Hak cipta")
    bar_bg = be.container([bar], content_width="full", background_background="classic", background_color=LIME, padding=bp.ruang(0), _title="Bilah hak cipta")
    foot = be.container([isi, bar_bg], content_width="full", flex_direction="column", flex_gap=be.gap(0), background_background="classic", background_color=NAVY,
                        padding=bp.ruang(0), _title="Footer DTNTF (halaman new)")
    s = json.dumps({"version": "0.4", "title": "Footer", "type": "container", "content": [foot], "page_settings": []}, ensure_ascii=False)
    assert "<style" not in s and '"widgetType": "html"' not in s
    (ROOT / "elementor" / "native" / "footer.json").write_text(s, encoding="utf-8")
    print("ok footer", len(s))


if __name__ == "__main__":
    main()
