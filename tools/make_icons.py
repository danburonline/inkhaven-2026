#!/usr/bin/env python3
"""Render favicon and PWA icons from the Source Serif semibold "c" mark.

The letter is drawn from the font outlines (vector), rasterised at 8× the
target size and downsampled with area averaging, so edges stay sharp at every
size. Layout matches the original mark: glyph height 0.428 of the canvas,
top at 0.267, on the light page colour. The maskable icon is the same mark
centred at height 0.34, which sits inside the 80% safe zone.

Also writes a path-based favicon.svg (so the tab icon does not depend on a
system font) and a multi-size favicon.ico (16, 32, 48).

Run from the repo root if the design or this script changes:
    python3 tools/make_icons.py
Then run the site build so icon ?v= hashes update:
    python3 tools/build.py
"""
import os
import re
from PIL import Image, ImageDraw, ImageFont
from fontTools.misc.transform import Transform
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SERIF_SB = '/usr/share/fonts/truetype/sand-box/custom/Source Serif Pro/SourceSerifPro-Semibold.ttf'
BG, FG = '#f6f1e8', '#1c1916'
DARK_BG, DARK_FG = '#15130f', '#e8e1d5'
# Fractions of the canvas, measured from the original apple-touch-icon.
GLYPH_H, TOP = 0.428, 0.267
# Maskable: centred, inside the 80% safe zone (10% padding on each side).
MASKABLE_H = 0.34
SCALE = 8  # supersample factor; BOX downsample = area average, no ringing
VIEWBOX = 64  # favicon.svg coordinate space (rx=10 matches the previous SVG)


def _round_path(d, nd=2):
    def repl(m):
        s = f'{float(m.group()):.{nd}f}'.rstrip('0').rstrip('.')
        return '0' if s == '-0' else s
    return re.sub(r'-?\d+\.?\d*', repl, d)


def write_svg(path):
    """Outlined lowercase c, same placement as the PNGs, with a rounded rect
    and a dark-mode palette — the previous favicon.svg design, but as a path
    so it stays crisp and identical on every system."""
    font = TTFont(SERIF_SB)
    gs = font.getGlyphSet()
    glyph = gs['c']
    bounds = BoundsPen(gs)
    glyph.draw(bounds)
    xmin, ymin, xmax, ymax = bounds.bounds
    ink_w, ink_h = xmax - xmin, ymax - ymin
    sc = (GLYPH_H * VIEWBOX) / ink_h
    x0 = (VIEWBOX - ink_w * sc) / 2 - xmin * sc
    y_top = TOP * VIEWBOX
    pen = SVGPathPen(gs)
    glyph.draw(TransformPen(pen, Transform(sc, 0, 0, -sc, x0, y_top + ymax * sc)))
    d = _round_path(pen.getCommands())
    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d">'
        '<style>rect{fill:%s}path{fill:%s}'
        '@media (prefers-color-scheme:dark){rect{fill:%s}path{fill:%s}}</style>'
        '<rect width="%d" height="%d" rx="10"/>'
        '<path d="%s"/></svg>\n' % (
            VIEWBOX, VIEWBOX, BG, FG, DARK_BG, DARK_FG, VIEWBOX, VIEWBOX, d)
    )
    open(path, 'w', encoding='utf-8').write(svg)


def icon(size, glyph_h, top=None):
    """Rasterise the mark at 8× size from the font outlines, then downsample."""
    S = size * SCALE
    probe = ImageFont.truetype(SERIF_SB, 1000)
    b = probe.getbbox('c')
    font = ImageFont.truetype(SERIF_SB, round(1000 * glyph_h * S / (b[3] - b[1])))
    b = font.getbbox('c')
    w, h = b[2] - b[0], b[3] - b[1]
    im = Image.new('RGB', (S, S), BG)
    y = (S - h) / 2 if top is None else top * S
    ImageDraw.Draw(im).text(((S - w) / 2 - b[0], y - b[1]), 'c', font=font, fill=FG)
    return im.resize((size, size), Image.Resampling.BOX)


def save_png(im, name):
    path = os.path.join(ROOT, name)
    im.save(path, optimize=True, compress_level=9)
    print(name, im.size[0])


if __name__ == '__main__':
    if not os.path.isfile(SERIF_SB):
        raise SystemExit('missing font: %s' % SERIF_SB)

    write_svg(os.path.join(ROOT, 'favicon.svg'))
    print('favicon.svg')

    # Standard mark (same placement as the original apple-touch-icon).
    for size, name in (
        (32, 'favicon-32.png'),
        (180, 'apple-touch-icon.png'),
        (192, 'icon-192.png'),
        (512, 'icon-512.png'),
    ):
        save_png(icon(size, GLYPH_H, TOP), name)

    save_png(icon(512, MASKABLE_H, None), 'icon-maskable-512.png')

    # Pillow keeps only sizes that fit in the first image, so the largest
    # frame has to be saved first; the 16 and 32 frames are attached as-is.
    ico_sizes = (16, 32, 48)
    frames = [icon(s, GLYPH_H, TOP) for s in ico_sizes]
    frames[-1].save(
        os.path.join(ROOT, 'favicon.ico'), format='ICO',
        append_images=frames[:-1], sizes=[(s, s) for s in ico_sizes])
    print('favicon.ico', 'x'.join(str(s) for s in ico_sizes))
