#!/usr/bin/env python3
"""Grafik 'Kegiatan per tahun' (pengabdian) 2016-2026 -> data/ugm/pengabdian-per-tahun.png (Chrome headless, font Plus Jakarta Sans).
Angka di atas tiap batang, label tahun per 5 tahun (2016, 2021, 2026). Data: data/agregat/ringkas.json (kategori 'Pengabdian kepada Masyarakat')."""
import json, pathlib, subprocess, tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
KAT = "Pengabdian kepada Masyarakat"
r = json.loads((ROOT / "data/agregat/ringkas.json").read_text(encoding="utf-8"))
seri = {t["tahun"]: t["per_kategori"].get(KAT, 0) for t in r["per_tahun"] if 2016 <= t["tahun"] <= 2026}
yrs = list(range(2016, 2027)); v = [seri.get(y, 0) for y in yrs]
W, H, PL, PR, PT, PB = 1100, 360, 40, 40, 60, 60
bw = (W - PL - PR) / len(yrs); mx = max(v)
bars = ""
for i, (y, n) in enumerate(zip(yrs, v)):
    h = (H - PT - PB) * n / mx; x = PL + i * bw + bw * .18; w = bw * .64; yy = H - PB - h
    bars += f'<rect x="{x:.1f}" y="{yy:.1f}" width="{w:.1f}" height="{h:.1f}" rx="6" fill="#C8E86D"/>'
    bars += f'<text x="{x + w / 2:.1f}" y="{yy - 10:.1f}" text-anchor="middle" fill="#fff" font-size="22" font-weight="700">{n}</text>'
    if (y - 2016) % 5 == 0:
        bars += f'<text x="{x + w / 2:.1f}" y="{H - PB + 32}" text-anchor="middle" fill="rgba(255,255,255,.85)" font-size="20" font-weight="600">{y}</text>'
svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}"><rect width="{W}" height="{H}" rx="20" fill="#073C64"/><line x1="{PL}" y1="{H - PB}" x2="{W - PR}" y2="{H - PB}" stroke="rgba(255,255,255,.35)" stroke-width="2"/>{bars}</svg>'
tmp = pathlib.Path(tempfile.mkdtemp()); (tmp / "g.html").write_text(f"<!doctype html><body style=\"margin:0;font-family:'Plus Jakarta Sans',sans-serif;background:#fff\">{svg}</body>", encoding="utf-8")
out = ROOT / "data/ugm/pengabdian-per-tahun.png"
subprocess.run(["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=3",
                f"--window-size={W},{H}", f"--screenshot={out}", f"file://{tmp / 'g.html'}"], capture_output=True, timeout=90)
print(out, dict(zip(yrs, v)), "total", sum(v))
