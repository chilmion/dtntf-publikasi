#!/usr/bin/env python3
"""Gambar prodi Teknik Nuklir dibuat ulang sebagai SVG (tajam, tema DTNTF), stdlib saja.
Sumber: gambar raster lama di data/prodi/ (nilai grafik dibaca/diperkirakan dari gambar).
Keluaran: data/prodi/svg/*.svg. Dipakai sebagai widget HTML (SVG inline, font mengikuti halaman)."""
import math, os
from xml.sax.saxutils import escape as E

OUT = os.path.join(os.path.dirname(__file__), '..', 'data', 'prodi', 'svg')
NAVY, DARK, BLUE, LIME, LINE = '#073C64', '#1A2C43', '#003D79', '#C8E86D', '#E3E3E3'
FONT = 'font-family:inherit'


def svg(w, h, body, titel):
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" role="img" aria-label="%s" '
            'style="width:100%%;max-width:%dpx;height:auto;display:block;%s;color:%s">'
            '<title>%s</title>%s</svg>\n') % (w, h, E(titel), w, FONT, DARK, E(titel), body)


def txt(x, y, s, size=13, weight=500, fill=DARK, anchor='middle', extra=''):
    return '<text x="%s" y="%s" font-size="%s" font-weight="%s" fill="%s" text-anchor="%s" %s>%s</text>' % (
        x, y, size, weight, fill, anchor, extra, E(str(s)))


def box(x, y, w, h, lines, fill, stroke, color=DARK, size=12.5, weight=600, r=8):
    s = '<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="%s" stroke="%s" stroke-width="1.2"/>' % (x, y, w, h, r, fill, stroke)
    n = len(lines)
    y0 = y + h / 2 - (n - 1) * 8 + 4.5
    for i, l in enumerate(lines):
        s += txt(x + w / 2, y0 + i * 16, l, size, weight, color)
    return s


def path(pts, color=DARK, arrow=True, w=1.5):
    d = 'M' + ' L'.join('%s %s' % p for p in pts)
    return '<path d="%s" fill="none" stroke="%s" stroke-width="%s" stroke-linejoin="round"%s/>' % (
        d, color, w, ' marker-end="url(#ah%s)"' % color[1:] if arrow else '')


def defs(*cols):
    s = '<defs>'
    for c in cols:
        s += ('<marker id="ah%s" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
              '<path d="M0 0 L10 5 L0 10 z" fill="%s"/></marker>') % (c[1:], c)
    return s + '</defs>'


def peminatan_ten():
    W, H = 760, 480
    b = defs(DARK, '#C0392B')
    b += txt(0, 28, 'Peminatan Teknologi Energi Nuklir', 22, 800, NAVY, 'start')
    for x, t in ((210, 'MK Prasyarat'), (410, 'Semester 5'), (675, 'Semester 6')):
        b += box(x - 65, 56, 130, 44, [t], NAVY, NAVY, '#fff', 13, 700)
    b += '<rect x="16" y="318" width="270" height="130" rx="10" fill="none" stroke="#7A8794" stroke-width="1.3" stroke-dasharray="5 4"/>'
    pre, sem, sl = NAVY, '#E8F0F8', '#5B7083'
    b += path([(270, 152), (340, 152)])
    b += path([(296, 152), (296, 118), (590, 118), (590, 156), (610, 156)])
    b += path([(296, 152), (296, 214), (340, 214)])
    b += path([(312, 152), (312, 346), (340, 346)], '#C0392B')
    b += path([(270, 210), (282, 210), (282, 188), (570, 188), (570, 170), (610, 170)])
    b += path([(270, 270), (340, 270)])
    b += path([(114, 345), (132, 345), (132, 405), (150, 405)])
    b += path([(114, 405), (150, 405)])
    b += path([(270, 405), (340, 405)])
    b += path([(325, 405), (325, 214)], arrow=False)
    b += path([(480, 214), (545, 214), (545, 144), (610, 144)])
    for y, l in ((130, ['Fisika Reaktor Nuklir']), (188, ['Pengantar Teknik', 'Nuklir dan 3S Nuklir']), (248, ['Teknik Proses'])):
        b += box(150, y, 120, 44, l, pre, pre, '#fff', 11.5)
    for y, l in ((130, ['Analisis Reaktor Nuklir']), (192, ['Rekayasa Pembangkit', 'Daya Nuklir']), (248, ['Siklus Bahan Bakar', 'Nuklir']),
                 (324, ['Praktikum Fisika', 'Reaktor Nuklir']), (383, ['Termal Hidraulika', 'Reaktor Nuklir'])):
        b += box(340, y, 140, 44, l, sem, NAVY, NAVY, 12)
    b += box(610, 126, 140, 62, ['Analisis Keselamatan', 'Nuklir / Keselamatan', 'Instalasi Nuklir'], sem, NAVY, NAVY, 12)
    b += box(30, 324, 84, 44, ['Termodinamika'], sl, sl, '#fff', 11.5)
    b += box(30, 383, 84, 44, ['Mekanika Fluida'], sl, sl, '#fff', 11.5)
    b += box(150, 383, 120, 44, ['Perpindahan', 'Kalor dan Massa'], sl, sl, '#fff', 11.5)
    return svg(W, H, b, 'Alur mata kuliah peminatan Teknologi Energi Nuklir')


def peminatan_fm():
    W, H = 780, 700
    b = defs(DARK)
    b += txt(0, 28, 'Peminatan Fisika Medis', 22, 800, NAVY, 'start')
    for x, t in ((100, 'MK Prasyarat'), (395, 'Semester 5'), (690, 'Semester 6')):
        b += box(x - 75, 56, 150, 52, [t], NAVY, NAVY, '#fff', 13, 700)
    sem, st = '#E8F0F8', NAVY
    b += path([(175, 186), (278, 186)], arrow=False)
    b += path([(278, 186), (322, 186)])
    b += path([(278, 186), (278, 271), (322, 271)])
    b += path([(175, 271), (248, 271), (248, 355), (322, 355)])
    b += path([(248, 271), (248, 229), (580, 229), (580, 186), (618, 186)])
    b += path([(175, 355), (215, 355), (215, 440), (322, 440)])
    b += path([(470, 186), (618, 186)])
    b += path([(494, 186), (494, 612), (470, 612)])
    b += path([(395, 580), (395, 560)])
    b += box(25, 158, 150, 56, ['Biologi Dasar'], '#E08A1E', '#E08A1E', '#fff', 12.5)
    b += box(25, 243, 150, 56, ['Deteksi dan', 'Pengukuran Radiasi'], '#B3261E', '#B3261E', '#fff', 12.5)
    b += box(25, 327, 150, 56, ['Fisika Kesehatan dan', 'Proteksi Radiasi'], '#E9DDF2', '#9A7BB5', DARK, 12.5)
    for y, l in ((158, ['Anatomi dan Fisiologi']), (243, ['Radiobiologi']), (327, ['Fisika Radiologi', 'dan Dosimetri']),
                 (412, ['Fisika Kedokteran', 'Nuklir']), (496, ['Praktikum Fisika Medis']), (580, ['Fisika Radiologi', 'Diagnostik dan', 'Intervensional'])):
        b += box(322, y, 148, 62 if y < 580 else 64, l, sem, st, NAVY, 12.5)
    b += box(618, 158, 148, 56, ['Fisika Radioterapi'], sem, st, NAVY, 12.5)
    return svg(W, H, b, 'Alur mata kuliah peminatan Fisika Medis')


def bar_chart(title, cats, vals, ymax, step, xlabel, W=720, H=420, color=NAVY):
    L, R, T, B = 58, 16, 40, 96
    pw, ph = W - L - R, H - T - B
    b = txt(0, 22, title, 17, 800, NAVY, 'start')
    for v in range(0, ymax + 1, step):
        y = T + ph - ph * v / ymax
        b += '<line x1="%d" x2="%d" y1="%.1f" y2="%.1f" stroke="%s"/>' % (L, W - R, y, y, LINE)
        b += txt(L - 8, y + 4, v, 12, 500, '#5B6670', 'end')
    b += '<text transform="translate(16 %d) rotate(-90)" font-size="12.5" font-weight="600" fill="%s" text-anchor="middle">Jumlah mahasiswa</text>' % (T + ph / 2, DARK)
    n = len(cats); bw = pw / n
    for i, (c, v) in enumerate(zip(cats, vals)):
        x = L + i * bw + bw * 0.2; h = ph * v / ymax; y = T + ph - h
        if v:
            b += '<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="2" fill="%s"/>' % (x, y, bw * 0.6, h, color)
            b += txt(x + bw * 0.3, y - 5, v, 11, 700, NAVY)
        cx = L + i * bw + bw / 2
        b += '<text transform="translate(%.1f %d) rotate(-45)" font-size="12" font-weight="500" fill="%s" text-anchor="end">%s</text>' % (cx + 4, T + ph + 16, DARK, E(c))
    b += '<line x1="%d" x2="%d" y1="%d" y2="%d" stroke="%s" stroke-width="1.5"/>' % (L, W - R, T + ph, T + ph, DARK)
    b += txt(L + pw / 2, H - 6, xlabel, 12.5, 600)
    return svg(W, H, b, title)


def topik_ten():
    c = ['MIR', 'HTR', 'FBR', 'FLR', 'ADS', 'MSR', 'LWR', 'FUS', 'FEND', 'BEND', 'ARI', 'ARA', 'NS', 'EnvRad', 'DET', 'RadW', 'RadSaf', 'NMat', 'AI-NET']
    v = [21, 3, 1, 10, 1, 5, 8, 2, 3, 15, 6, 11, 7, 22, 3, 11, 11, 3, 0]
    return bar_chart('Topik tugas akhir: Teknologi Energi Nuklir (2021–2024)', c, v, 30, 5, 'Topik Teknologi Energi Nuklir')


def topik_fm():
    c = ['BNCT', 'CIRT', 'PT', 'NPMT', 'FNT', 'Shielding', 'TPS', 'NMed', 'AI-MP', 'Accel']
    v = [20, 5, 15, 8, 1, 15, 14, 10, 5, 2]
    return bar_chart('Topik tugas akhir: Fisika Medis (2021–2023)', c, v, 30, 5, 'Topik Fisika Medis', 720, 420)


def karier():
    data = [('Industri nuklir', 2, '#073C64'), ('Fisikawan medis', 5, '#3F7CB0'), ('Industri alat medis', 5, '#6FA3CF'),
            ('Institusi pemerintah', 8, '#9BC1E3'), ('Industri manufaktur', 25, '#C8E86D'), ('Industri energi', 5, '#A5C94A'),
            ('Industri jasa/konsultan', 23, '#1A2C43'), ('IT', 16, '#5B7083'), ('Pendidikan', 9, '#8FA2B3'),
            ('Lanjut studi', 1, '#D8DEE4'), ('Penelitian nuklir', 1, '#B7C0C9')]
    W, H = 720, 400; cx, cy, r = 190, 205, 160
    b = txt(0, 22, 'Sebaran karier alumni', 17, 800, NAVY, 'start')
    a = -math.pi / 2
    for name, p, col in data:
        a2 = a + 2 * math.pi * p / 100
        x1, y1, x2, y2 = cx + r * math.cos(a), cy + r * math.sin(a), cx + r * math.cos(a2), cy + r * math.sin(a2)
        b += '<path d="M%d %d L%.1f %.1f A%d %d 0 %d 1 %.1f %.1f Z" fill="%s" stroke="#fff" stroke-width="2"/>' % (
            cx, cy, x1, y1, r, r, 1 if p > 50 else 0, x2, y2, col)
        a = a2
    ly = 70
    for name, p, col in sorted(data, key=lambda d: -d[1]):
        b += '<rect x="400" y="%d" width="16" height="16" rx="3" fill="%s"/>' % (ly - 13, col)
        b += txt(426, ly, name, 14, 500, DARK, 'start')
        b += txt(690, ly, '%d%%' % p, 14, 800, NAVY, 'end')
        ly += 27
    return svg(W, H, b, 'Sebaran karier alumni Teknik Nuklir')


def lulusan():
    yrs = list(range(1977, 2026))
    ne = {}; mp = {}; mi = {}; ac = {}
    simple = [16, 21, 16, 19, 46, 49, 49, 50, 44, 40, 41, 37, 23, 23, 23, 23, 26, 20, 32]
    for i, v in enumerate(simple): ne[1977 + i] = v
    for y, (a, b_, c) in {1996: (28, 0, 10), 1997: (22, 0, 13), 1998: (36, 12, 12), 1999: (37, 15, 11), 2000: (20, 17, 16), 2001: (20, 10, 4),
                          2002: (15, 4, 7), 2003: (25, 0, 6), 2004: (27, 1, 2), 2005: (19, 3, 2), 2006: (35, 0, 0), 2007: (38, 0, 0), 2008: (24, 0, 0),
                          2009: (31, 13, 0), 2010: (21, 11, 0), 2011: (33, 13, 0), 2012: (22, 10, 0), 2013: (24, 8, 0), 2014: (43, 8, 0), 2015: (32, 16, 0),
                          2016: (29, 7, 0), 2017: (20, 23, 0), 2018: (33, 26, 0), 2019: (23, 21, 0), 2020: (33, 16, 0), 2021: (11, 3, 0)}.items():
        ne[y], mp[y], mi[y] = a, b_, c
    ac.update({2019: 9, 2020: 15, 2021: 29, 2022: 49, 2023: 55, 2024: 54, 2025: 51})
    W, H = 900, 440; L, R, T, B = 52, 12, 70, 70; pw, ph = W - L - R, H - T - B; ymax = 70
    b = txt(0, 22, 'Mahasiswa dan lulusan Teknik Nuklir per angkatan masuk', 17, 800, NAVY, 'start')
    b += txt(0, 46, 'Total lulusan 1619 (G-MP 237)  ·  Mahasiswa aktif 261', 13.5, 600, DARK, 'start')
    b += txt(W, 22, 'Desember 2025', 12, 500, '#5B6670', 'end')
    for v in range(0, ymax + 1, 10):
        y = T + ph - ph * v / ymax
        b += '<line x1="%d" x2="%d" y1="%.1f" y2="%.1f" stroke="%s"/>' % (L, W - R, y, y, LINE) + txt(L - 8, y + 4, v, 11.5, 500, '#5B6670', 'end')
    b += '<text transform="translate(14 %d) rotate(-90)" font-size="12" font-weight="600" fill="%s" text-anchor="middle">Jumlah mahasiswa-lulusan</text>' % (T + ph / 2, DARK)
    n = len(yrs); bw = pw / n
    cols = (('G-NE', NAVY, ne), ('G-MP', '#2E9E6B', mp), ('G-MI', '#B5651D', mi), ('Aktif', LIME, ac))
    for i, y in enumerate(yrs):
        x = L + i * bw + bw * 0.18; w = bw * 0.64; base = T + ph
        for nm, col, d in cols:
            v = d.get(y, 0)
            if v:
                h = ph * v / ymax; base -= h
                b += '<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s"%s/>' % (x, base, w, h, col, ' stroke="#9DBE3E" stroke-width="0.8"' if nm == 'Aktif' else '')
        if i % 2 == 0 or y == 2025:
            b += '<text transform="translate(%.1f %d) rotate(-60)" font-size="10.5" fill="%s" text-anchor="end">%d</text>' % (x + w / 2 + 3, T + ph + 14, DARK, y)
    b += '<line x1="%d" x2="%d" y1="%d" y2="%d" stroke="%s" stroke-width="1.5"/>' % (L, W - R, T + ph, T + ph, DARK)
    b += txt(L + pw / 2, H - 4, 'Tahun masuk', 12.5, 600)
    lx = 600
    for nm, col, _ in cols:
        b += '<rect x="%d" y="38" width="13" height="13" rx="2" fill="%s"/>' % (lx, col) + txt(lx + 19, 49, nm, 12.5, 600, DARK, 'start'); lx += 70
    return svg(W, H, b, 'Grafik jumlah mahasiswa dan lulusan Teknik Nuklir per angkatan masuk')


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    for n, f in (('tn-peminatan-ten', peminatan_ten), ('tn-peminatan-fisika-medis', peminatan_fm), ('tn-topik-ta-ten', topik_ten),
                 ('tn-topik-ta-fisika-medis', topik_fm), ('tn-karier-alumni', karier), ('tn-lulusan-per-angkatan', lulusan)):
        open(os.path.join(OUT, n + '.svg'), 'w', encoding='utf-8').write(f())
        print('ok', n)
