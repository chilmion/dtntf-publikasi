#!/usr/bin/env python3
"""Pratinjau HTML mandiri halaman prodi v2 (hero + bento + akordeon), gambar ditanam base64.
    python3 scripts/buat_uji_prodi.py teknik-nuklir  → uji-prodi-teknik-nuklir.html"""
import base64, mimetypes, pathlib, re, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import buat_prodi as bpr  # noqa: E402

ROOT = bpr.ROOT
NAVY, LIME, DARK, ABU, GARIS = "#073C64", "#C8E86D", "#1A2C43", "#F5F5F5", "#E3E3E3"
CSS = f"""
*{{box-sizing:border-box}}body{{margin:0;background:#fff;font:17px/1.5 Barlow,sans-serif;color:#636363}}
.bn{{background:{NAVY};color:#fff;padding:56px 20px;text-align:center;font:400 44px 'Plus Jakarta Sans',sans-serif;letter-spacing:-2px}}
.bn small{{display:block;font:600 12px Barlow;letter-spacing:.8px;opacity:.6;margin-bottom:8px}}
.w{{max-width:1180px;margin:0 auto;padding:60px 20px 80px;display:flex;flex-direction:column;gap:24px}}
h2,h3,h4{{font-family:'Plus Jakarta Sans',sans-serif;font-weight:400;color:#161616;margin:0}}
.kick{{font:600 12px Barlow;letter-spacing:.8px;text-transform:uppercase;color:{NAVY}}}
.hero{{background:{NAVY};border-radius:10px;padding:48px;display:flex;gap:40px;align-items:center}}
.hero .k{{flex:55%;display:flex;flex-direction:column;gap:16px}}.hero .g{{flex:45%}}.hero img{{width:100%;border-radius:10px;display:block}}
.hero h2{{color:#fff;font-size:52px;letter-spacing:-3px;line-height:1.2}}.hero .kick{{color:{LIME}}}.hero p{{color:rgba(255,255,255,.88);font-size:18px;margin:0}}
.bento{{display:flex;flex-wrap:wrap;gap:16px}}.t{{flex:1 1 24%;min-width:220px;border-radius:10px;padding:24px;display:flex;flex-direction:column;gap:6px}}
.t .n{{font:400 64px/1.1 'Plus Jakarta Sans';letter-spacing:-4px}}.t p{{margin:0}}
.lime{{background:{LIME};color:{DARK}}}.lime .kick{{color:{DARK}}}.navy{{background:{NAVY};color:rgba(255,255,255,.86)}}.navy .kick,.navy .n{{color:#fff}}
.putih{{border:1px solid {GARIS};color:#636363}}.putih .n{{color:#161616}}.abu{{background:{ABU}}}.abu .n{{color:#161616}}
.dua{{columns:2;column-gap:40px}}.dua p{{margin:0 0 12px}}
.visi{{background:{LIME};border-radius:10px;padding:24px;display:flex;flex-direction:column;gap:8px;color:{DARK}}}.visi .kick{{color:{DARK}}}.visi h3{{font-size:28px;letter-spacing:-1.3px;color:{DARK}}}
details{{background:#fff;border:1px solid {GARIS};border-radius:10px;padding:8px}}
summary{{list-style:none;cursor:pointer;display:flex;justify-content:space-between;align-items:center;padding:14px 16px;font:400 26px 'Plus Jakarta Sans';letter-spacing:-1.3px;color:#161616}}
summary::-webkit-details-marker{{display:none}}summary::after{{content:"+";color:{NAVY};font-size:22px}}details[open] summary{{color:{NAVY}}}details[open] summary::after{{content:"−"}}
.c{{padding:4px 16px 16px}}
@media(max-width:800px){{.hero{{flex-direction:column;padding:24px}}.hero h2{{font-size:30px}}.dua{{columns:1}}.t .n{{font-size:44px}}}}
"""


def render(nama):
    md = (ROOT / "manual" / "prodi" / f"{nama}.md").read_text(encoding="utf-8")
    meta, bagian = bpr.bagi(md)
    (j0, i0), *lain = bagian
    paras = [p.strip() for p in i0.split("\n\n") if p.strip()]
    h = meta["hero"]
    o = [f'<div class="hero"><div class="k"><span class="kick">{h.get("kicker","")}</span><h2>{h.get("judul", j0)}</h2><p>{bpr.inline(paras[0])}</p></div>'
         + (f'<div class="g"><img src="{bpr.be.BASE}/prodi/{h["gambar"]}"></div>' if h.get("gambar") else "") + "</div>"]
    if meta["kartu"]:
        o.append('<div class="bento">' + "".join(
            f'<div class="t {g}"><span class="kick">{l}</span><div class="n">{n}</div><p>{bpr.inline(k)}</p></div>' for g, l, n, k in meta["kartu"]) + "</div>")
    if len(paras) > 1:
        o.append('<div class="dua">' + bpr.html_blok("\n\n".join(paras[1:])) + "</div>")
    for j, isi in lain:
        if j.lower().startswith("mitra"):
            continue
        if j.lower().startswith("visi"):
            q = "".join(f"<h3>{bpr.inline(b[2:])}</h3>" if b.startswith("> ") else bpr.html_blok(b) for b in isi.split("\n\n") if b.strip())
            o.append(f'<div class="visi"><span class="kick">{j}</span>{q}</div>')
        else:
            o.append(f"<details><summary>{j}</summary><div class='c'>{bpr.html_blok(isi)}</div></details>")
    html = (f"<!doctype html><meta charset=utf-8><meta name=viewport content='width=device-width,initial-scale=1'><title>Pratinjau prodi {nama}</title>"
            "<link href='https://fonts.googleapis.com/css2?family=Barlow:wght@400;600&family=Plus+Jakarta+Sans:wght@400&display=swap' rel=stylesheet>"
            f"<style>{CSS}</style><div class=bn><small>PRATINJAU — banner ini dari tema</small>Program Studi Sarjana {nama.replace('-', ' ').title()}</div><div class=w>{''.join(o)}</div>")

    def tanam(m):
        f = ROOT / "manual" / "prodi-gambar" / m.group(1)
        if not f.exists():
            return m.group(0)
        return f"src=\"data:{mimetypes.guess_type(f.name)[0]};base64,{base64.b64encode(f.read_bytes()).decode()}\""
    return re.sub(r'src="[^"]*/prodi/([^"]+)"', tanam, html)


if __name__ == "__main__":
    n = sys.argv[1] if len(sys.argv) > 1 else "teknik-nuklir"
    (ROOT / f"uji-prodi-{n}.html").write_text(render(n), encoding="utf-8")
    print(f"Tertulis uji-prodi-{n}.html")
