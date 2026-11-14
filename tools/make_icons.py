#!/usr/bin/env python3
"""Render the PWA icons from the favicon design: a Source Serif semibold "c" on the
light page colour, matching apple-touch-icon.png. Run once if the design changes:
python3 tools/make_icons.py"""
import os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SERIF_SB = '/usr/share/fonts/truetype/sand-box/custom/Source Serif Pro/SourceSerifPro-Semibold.ttf'
BG, FG = '#f6f1e8', '#1c1916'

def icon(size, glyph_h, top=None):
    """glyph_h and top are fractions of the icon size (apple-touch-icon: 0.428 and 0.267)."""
    scale = 4  # supersample for smooth edges
    S = size * scale
    probe = ImageFont.truetype(SERIF_SB, 1000)
    b = probe.getbbox('c')
    font = ImageFont.truetype(SERIF_SB, round(1000 * glyph_h * S / (b[3] - b[1])))
    b = font.getbbox('c')
    w, h = b[2] - b[0], b[3] - b[1]
    im = Image.new('RGB', (S, S), BG)
    y = (S - h) / 2 if top is None else top * S
    ImageDraw.Draw(im).text(((S - w) / 2 - b[0], y - b[1]), 'c', font=font, fill=FG)
    return im.resize((size, size), Image.LANCZOS)

if __name__ == '__main__':
    for size, gh, top, name in [(192, 0.428, 0.267, 'icon-192.png'), (512, 0.428, 0.267, 'icon-512.png'),
                                (512, 0.34, None, 'icon-maskable-512.png')]:
        icon(size, gh, top).save(os.path.join(ROOT, name), optimize=True)
        print(name)
