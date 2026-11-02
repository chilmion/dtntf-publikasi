#!/usr/bin/env python3
"""
Buat halaman uji lokal (uji-*.html) dari widget/ — untuk pratinjau tanpa WordPress.
Jalankan server di folder repo, lalu buka alamatnya:

    python3 scripts/buat_uji.py
    python3 -m http.server 8000        # http://localhost:8000/uji-daftar-dosen.html

Halaman: daftar dosen, 3 profil contoh (lengkap, minim, tanpa foto), induk KBK, 4 halaman KBK.
Kerangka Elementor (foto, nama, kartu) ditiru dengan HTML biasa; widget aslinya dipakai apa adanya.
"""

import csv
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
PLACEHOLDER = "https://NAMA-AKUN.github.io/dtntf-profil/data"
HEAD = ("<!doctype html><meta charset=utf-8><meta name=viewport content='width=device-width,initial-scale=1'>"
        "<title>{judul}</title><link href='https://fonts.googleapis.com/css2?family=Barlow:wght@400;500;600&"
        "family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap' rel=stylesheet>"
        "<style>body{{margin:0;font-family:'Barlow',system-ui;background:#fff}}.uji{{max-width:1180px;margin:0 auto;padding:60px 20px 80px}}"
        ".uji .kt-pagehead{{font:600 12px Barlow;letter-spacing:.8px;text-transform:uppercase;color:#073C64}}"
        ".uji h1{{font:400 56px/1.2 'Plus Jakarta Sans';letter-spacing:-3.4px;color:#161616;margin:6px 0 10px}}"
        ".uji .remah{{font-size:14px;color:#636363;margin:0 0 24px}}"
        ".uji .profil{{display:flex;gap:32px;align-items:flex-start}}.uji .kiri{{flex:0 0 28%}}.uji .kiri img,.uji .kiri .nofoto{{width:100%;border-radius:10px;display:block}}"
        ".uji .nofoto{{aspect-ratio:4/5;background:#E8EEF4;color:#073C64;display:flex;align-items:center;justify-content:center;font:600 14px Barlow}}"
        ".uji .tautan{{background:#073C64;color:#fff;border-radius:10px;padding:24px;margin-top:16px;font-size:16px}}"
        ".uji .kanan{{flex:1;min-width:0}}"
        ".uji .grid-dosen{{display:flex;flex-wrap:wrap;gap:16px;align-items:stretch}}"
        ".uji .kartu{{width:calc(30% + 4px);flex-grow:1;max-width:calc(33.3% - 11px);display:flex;flex-direction:column;border:1px solid #E3E3E3;border-radius:10px;overflow:hidden}}"
        ".uji .kartu img{{width:100%;height:360px;object-fit:cover;object-position:top center;display:block}}"
        ".uji .kartu .isi{{padding:20px;display:flex;flex-direction:column;gap:6px;flex:1;min-height:200px;justify-content:space-between}}"
        ".uji .kartu h3{{font:400 22px/1.2 'Plus Jakarta Sans';letter-spacing:-1.3px;margin:0;color:#161616}}"
        ".uji .kartu a{{font:600 15px Barlow;color:#073C64;text-decoration:none}}"
        "@media(max-width:1024px){{.uji .kartu{{max-width:48%}}.uji h1{{font-size:40px}}}}"
        "@media(max-width:767px){{.uji{{padding:32px 16px 48px}}.uji h1{{font-size:28px;letter-spacing:-1.8px}}.uji .profil{{flex-direction:column}}.uji .kiri{{flex:none;width:100%}}.uji .kartu{{max-width:100%;width:100%}}.uji .kartu img{{height:300px}}}}"
        "</style><body><div class='uji'>")


def widget(nama, **attr):
    h = (ROOT / "widget" / nama).read_text(encoding="utf-8").replace(PLACEHOLDER, "./data")
    for k, v in attr.items():
        h = h.replace(f'{k}=""', f'{k}="{v}"', 1) if f'{k}=""' in h else h
    return h


def tulis(nama, judul, isi):
    (ROOT / nama).write_text(HEAD.format(judul=judul) + isi + "</div>", encoding="utf-8")
    print("Tertulis", nama)


def esc(s):
    return (s or "").replace("&", "&amp;").replace("<", "&lt;")


def main():
    dosen = list(csv.DictReader(open(ROOT / "dosen.csv", newline="", encoding="utf-8")))
    per_slug = {r["slug"]: r for r in dosen}
    # --- daftar dosen
    kartu = []
    for r in sorted(dosen, key=lambda r: r["nama"].lower()):
        info = widget("katur-dosen-info.html").replace('data-slug=""', f'data-slug="{r["slug"]}"')
        kartu.append(f'<div class="kartu kt-kartu-dosen"><img src="{esc(r["foto_url"])}" alt="{esc(r["nama"])}" loading="lazy">'
                     f'<div class="isi"><h3>{esc(r["nama"])}</h3>{info}<a href="/{r["slug"]}/">selengkapnya →</a></div></div>')
    tulis("uji-daftar-dosen.html", "Uji – Daftar dosen",
          '<div class="kt-pagehead">Departemen Teknik Nuklir dan Teknik Fisika</div><h1>Dosen Tetap</h1>'
          + widget("katur-dosen-filter.html") + '<div class="grid-dosen">' + "".join(kartu) + "</div>")

    # --- profil: lengkap / minim / tanpa foto
    def profil(slug, berkas, ket, tanpa_foto=False):
        r = per_slug[slug]
        foto = "" if tanpa_foto or not r["foto_url"] else r["foto_url"]
        kiri = (f'<img src="{esc(foto)}" alt="">' if foto else '<div class="nofoto">(tanpa foto)</div>')
        isi = (f'<p class="remah">Beranda › Dosen Tetap › {esc(r["nama"])} &nbsp;·&nbsp; <i>{ket}</i></p><div class="profil"><div class="kiri">{kiri}'
               '<div class="tautan"><b>Tautan</b><br>Profil SINTA ↗</div></div><div class="kanan">'
               f'<div class="kt-pagehead">Kelompok</div><h1>{esc(r["nama"])}</h1><p style="font-size:18px;color:#414142;margin:0 0 24px">{esc(r["gelar"])}</p>'
               + widget("katur-profil-cv.html").replace('data-slug=""', f'data-slug="{slug}"') + "</div></div>")
        tulis(berkas, f"Uji – Profil {r['nama']} ({ket})", isi)

    def jml(s):
        try:
            return len(json.loads((ROOT / "data" / f"{s}.json").read_text(encoding="utf-8")).get("publikasi") or [])
        except OSError:
            return 10 ** 9
    minim = min((r["slug"] for r in dosen), key=jml)
    profil("andang-widi-harto", "uji-profil-lengkap.html", "data lengkap")
    profil(minim, "uji-profil-minim.html", "data minim, banyak lorem ipsum")
    profil("faridah", "uji-profil-tanpa-foto.html", "tanpa foto", tanpa_foto=True)

    # --- KBK
    d = json.loads((ROOT / "data" / "kbk" / "kbk.json").read_text(encoding="utf-8"))
    tulis("uji-kbk-induk.html", "Uji – Induk KBK",
          '<p class="remah">Beranda › KBK</p><div class="kt-pagehead">Departemen Teknik Nuklir dan Teknik Fisika</div><h1>Kelompok Bidang Keahlian</h1>'
          + widget("katur-kbk-induk.html"))
    for k in d["kbk"]:
        tulis(f"uji-kbk-{k['kode']}.html", f"Uji – KBK {k['nama']}",
              f'<p class="remah">Beranda › KBK › {esc(k["nama"])}</p>' + widget("katur-kbk.html").replace('data-kbk="enet"', f'data-kbk="{k["kode"]}"'))


if __name__ == "__main__":
    main()
