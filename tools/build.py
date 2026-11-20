#!/usr/bin/env python3
"""Rebuild the home page list, thumbnails, share images, SEO tags, sitemap and feed.
Run from the repo root after adding or editing a post: python3 tools/build.py"""
import html, json, os, re, io, hashlib
from datetime import datetime, timezone, timedelta
from xml.sax.saxutils import escape as xml_esc
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = 'consciousness.ink'
SITE_URL = 'https://%s' % SITE
SERIES = 'Meditations on Synthetic Consciousness'
SERIES_SUB = 'and Hybrid Mind Uploading'
SITE_TITLE = SERIES + ' ' + SERIES_SUB
AUTHOR = 'Daniel Burger'
AUTHOR_X = 'https://x.com/danburonline'
INKHAVEN_URL = 'https://inkhaven.blog'
INKHAVEN_LINK = ('<a class="inkhaven" href="%s" target="_blank" rel="noopener">Inkhaven</a>'
                 % INKHAVEN_URL)
PT = timezone(timedelta(hours=-8))
OG_W, OG_H = 1200, 630
OG_SITE = '  <meta property="og:site_name" content="%s">\n' % SITE
def min_css(css):
    """Small, safe minifier: comments and whitespace only (selectors are left alone)."""
    css = re.sub(r'/\*.*?\*/', '', css, flags=re.S)
    css = re.sub(r'\s+', ' ', css)
    css = re.sub(r'\s*([{};])\s*', r'\1', css)
    return css.replace(';}', '}').strip()

# styles.css is the source; it is inlined into every page so the first paint
# does not wait for a second request. Re-run the build after editing it.
CSS_INLINE = min_css(open(os.path.join(ROOT, 'styles.css'), encoding='utf-8').read())
THEME_HEAD = '''  <meta name="color-scheme" content="light dark">
  <script>(function(){var r=document.documentElement;window.__inkTheme=function(t){var x=t==='light'||t==='dark',m=document.querySelectorAll('meta[name="theme-color"]'),c=document.querySelector('meta[name="color-scheme"]');if(x){r.setAttribute('data-theme',t);r.style.colorScheme=t}else{r.removeAttribute('data-theme');r.style.removeProperty('color-scheme')}for(var i=0;i<m.length;i++){m[i].content=x?(t==='dark'?'#15130f':'#f6f1e8'):(i===0?'#f6f1e8':'#15130f');if(x)m[i].removeAttribute('media');else m[i].setAttribute('media','(prefers-color-scheme: '+(i===0?'light':'dark')+')')}if(c)c.content=x?t:'light dark'};var t='auto';try{t=localStorage.getItem('theme')||'auto'}catch(e){}window.__inkTheme(t)})()</script>
  <style>%s</style>''' % CSS_INLINE
FEED_LINK = '  <link rel="alternate" type="application/rss+xml" title="%s" href="%s/feed.xml">' % (
    html.escape(SITE_TITLE), SITE_URL)
# Crimson Pro is close to the site's Iowan/Palatino stack and supports weight axes.
CRIMSON = '/usr/share/fonts/truetype/sand-box/google/Crimson Pro/CrimsonPro-VariableFont_wght.ttf'
SERIF_FALLBACK = '/usr/share/fonts/truetype/sand-box/custom/Source Serif Pro/SourceSerifPro-Regular.ttf'
FONT_PATH = CRIMSON if os.path.exists(CRIMSON) else SERIF_FALLBACK

def is_post_path(path):
    return bool(re.search(r'[/\\]\d+-[^/\\]+[/\\]index\.html$', path))

def ensure_chrome(path):
    """Add og:site_name, and strip the old wordmark, so older templates
    stay consistent after a build. Post pages get their chrome from
    rewrite_post_chrome instead (no masthead, no series-in-h1)."""
    s = open(path, encoding='utf-8').read()
    changed = False
    if 'property="og:site_name"' not in s and "property='og:site_name'" not in s:
        if re.search(r'<meta property="og:url"[^>]*>\n', s):
            s = re.sub(r'(<meta property="og:url"[^>]*>\n)', r'\1' + OG_SITE, s, count=1)
        else:
            s = s.replace('</head>', OG_SITE + '</head>', 1)
        changed = True
    if 'class="masthead"' in s:
        s = re.sub(r'\s*<p class="masthead">.*?</p>', '', s, count=1, flags=re.S)
        changed = True
    if changed:
        open(path, 'w', encoding='utf-8').write(s)

SOCIAL_ICON_RE = re.compile(
    r'<a\b(?=[^>]*\bclass="[^"]*\bicon\b[^"]*")[^>]*href="https://(?:www\.)?(?:x\.com|twitter\.com|github\.com|substack\.com)[^"]*"[^>]*>',
    re.I)

def ensure_social_newtab(path):
    """Give X / GitHub / Substack icon links target=_blank rel=noopener.
    Glossary and other same-origin links stay in this tab."""
    s = open(path, encoding='utf-8').read()
    def add_blank(m):
        tag = m.group(0)
        if re.search(r'\btarget=', tag):
            if 'noopener' not in tag and 'rel=' not in tag:
                tag = re.sub(r'\btarget="[^"]*"', 'target="_blank" rel="noopener"', tag, count=1)
            return tag
        if tag.endswith('/>'):
            return tag[:-2] + ' target="_blank" rel="noopener"/>'
        return tag[:-1] + ' target="_blank" rel="noopener">'
    s2, n = SOCIAL_ICON_RE.subn(add_blank, s)
    if n:
        open(path, 'w', encoding='utf-8').write(s2)

NUM_WRAP_RE = re.compile(r'(<span class="num-wrap">.*?</span>)', re.S)
DEFAULT_NUM_WRAP = (
    '<span class="num-wrap"><button class="num-menu" type="button" '
    'aria-haspopup="menu" aria-expanded="false" title="All meditations">'
    '%s/30<svg aria-hidden="true" viewBox="0 0 12 12" width="11" height="11">'
    '<path d="M2.5 4.5 6 8l3.5-3.5" fill="none" stroke="currentColor" '
    'stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>'
    '</svg></button></span>'
)

def words_label(n):
    return '{:,} words'.format(n)

def slim_nav_html(end_inner=''):
    """Slim sticky site nav: back chevron + series title, optional right slot
    (4/30 menu on posts; empty on glossary/404/offline so theme.js can add
    the icon-only toggle)."""
    end = ('\n        %s\n      ' % end_inner) if end_inner else ''
    return (
        '    <nav class="post-nav" aria-label="Site">\n'
        '      <a class="post-nav-brand" href="/" title="%s" aria-label="%s">'
        '<svg class="brand-back" aria-hidden="true" viewBox="0 0 12 12" width="11" height="11">'
        '<path d="M7.5 2.5 4 6l3.5 3.5" fill="none" stroke="currentColor" '
        'stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>'
        '<span class="brand-full">%s</span>'
        '<span class="brand-short">Meditations</span></a>\n'
        '      <div class="post-nav-end">%s</div>\n'
        '    </nav>\n' % (html.escape(SERIES),
                           html.escape('Back to home: ' + SERIES),
                           html.escape(SERIES), end)
    )

def rewrite_post_chrome(path, num, short, iso, date_text, words):
    """Idempotent: turn a post's top chrome into the slim nav + title + byline."""
    s = open(path, encoding='utf-8').read()
    m = NUM_WRAP_RE.search(s)
    num_wrap = m.group(1) if m else (DEFAULT_NUM_WRAP % num)
    s = re.sub(r'\s*<p class="masthead">.*?</p>', '', s, count=1, flags=re.S)
    s = re.sub(r'\s*<p class="back">.*?</p>', '', s, count=1, flags=re.S)
    s = re.sub(r'\s*<nav class="post-nav"[^>]*>.*?</nav>', '', s, count=1, flags=re.S)
    s = re.sub(r'\s*<header class="post-header">.*?</header>', '', s, count=1, flags=re.S)
    s = re.sub(
        r'\s*<h1>(?:<span class="num-wrap">.*?</span>\s*)?'
        r'(?:<span class="series">.*?</span>:\s*)?.*?</h1>\s*'
        r'<time class="post-date"[^>]*>.*?</time>',
        '', s, count=1, flags=re.S)
    nav = slim_nav_html(num_wrap)
    header = (
        '      <header class="post-header">\n'
        # empty .tcopy slot: titlecopy.js fills it; reserving its width here
        # keeps the title from rewrapping when the script runs
        '        <h1>%s <span class="tcopy"></span></h1>\n'
        '        <p class="post-byline"><a class="author-link post-author" href="%s" target="_blank" rel="author me noopener">%s</a>'
        '<span class="post-meta-sep" aria-hidden="true">·</span>'
        '<time class="post-date" datetime="%s">%s</time>'
        '<span class="post-meta-sep" aria-hidden="true">·</span>'
        '<span class="post-words">%s</span></p>\n'
        '      </header>\n' % (html.escape(short), AUTHOR_X, html.escape(AUTHOR), iso, html.escape(date_text), words_label(words))
    )
    s2, n = re.subn(r'(<div class="wrap">\n)', r'\1' + nav, s, count=1)
    if n != 1:
        raise SystemExit('could not insert post-nav in %s' % path)
    s = s2
    s2, n = re.subn(r'(<article>\s*)', r'\1' + header, s, count=1)
    if n != 1:
        raise SystemExit('could not insert post-header in %s' % path)
    open(path, 'w', encoding='utf-8').write(s2)

ABBREV = re.compile(r'\b(i\.e|e\.g|vs|Mr|Mrs|Ms|Dr|Prof)\.', re.I)

def excerpt(text, limit=170):
    """Faithful ~150-170 character summary from the opening, no invented claims."""
    text = re.sub(r'\[[^\]]*\]', '', text)
    text = re.sub(r'\([^)]{40,}\)', '', text)
    text = text.replace('*', '')
    text = re.sub(r'\s+', ' ', text).replace(' ,', ',').replace(' .', '.').strip()
    marks = []
    def hold(m):
        marks.append(m.group(0))
        return '‹%d›' % (len(marks) - 1)
    def restore(s):
        return re.sub(r'‹(\d+)›', lambda m: marks[int(m.group(1))], s)
    tmp = ABBREV.sub(hold, text)
    if len(text) <= limit:
        return text
    acc, chosen = '', ''
    for part in re.findall(r'.+?(?:[.?!](?=\s|$)|$)', tmp):
        cand = (acc + part).strip()
        out = restore(cand)
        if len(out) <= limit and part.strip():
            chosen, acc = out, cand + ' '
        else:
            break
    if chosen and len(chosen) >= 70:
        rest = text[len(chosen):].lstrip()
        if rest:
            m = re.match(r'(.+?)(, (?:and|or)\b)', rest)
            if m:
                extra = m.group(1).strip()
                cand = (chosen + ' ' + extra).strip()
                if not cand.endswith(('.', '?', '!')):
                    cand += '.'
                if len(cand) <= limit:
                    chosen = cand
        return close_excerpt(chosen, text, limit)
    window = tmp[:limit + 1]
    for punct in '.!?)':
        i = window.rfind(punct)
        if i >= 110:
            return close_excerpt(restore(window[:i + 1]).strip(), text, limit)
    i = window.rfind(' ')
    return close_excerpt(restore(window[:i]).rstrip(' ,;:'), text, limit, ellipsis=True)

def close_excerpt(chosen, text, limit, ellipsis=False):
    chosen = re.sub(r' +', ' ', chosen).strip()
    # If we stopped just before a closing parenthesis or period in the source,
    # keep it so the summary does not hang open.
    if chosen in text:
        rest = text[text.find(chosen) + len(chosen):]
        take = ''
        for ch in rest:
            if ch in ').' and len(chosen) + len(take) + 1 <= limit + 2:
                take += ch
            else:
                break
        chosen = (chosen + take).strip()
    chosen = re.sub(r' +', ' ', chosen).strip()
    if ellipsis and not chosen.endswith(('.', '?', '!', '…', ')')):
        chosen += '…'
    return chosen

def first_para(art):
    body = BeautifulSoup(str(art), 'html.parser').find('article')
    for sel in ['h1', 'time', '.post-nav', '.post-header', '.post-byline', '.essence', '.x-callout', '.tweet-embed', 'script', 'figcaption', '.num-menu-pop']:
        for el in body.select(sel):
            el.decompose()
    for p in body.find_all('p'):
        t = p.get_text(' ', strip=True)
        if t:
            return t
    return body.get_text(' ', strip=True)

# Dark typographic share cards, 1200x630, drawn at 2x then downsampled.
# Palette matches the site's dark theme. No pills, boxes, bars or gradients.
OG_BG, OG_TEXT, OG_MUTED = '#15130f', '#e8e1d5', '#a69d90'
OG_SCALE = 2
OG_BYLINE = AUTHOR + ' · Inkhaven 2026'

def wrap_text(draw, text, font, max_width):
    words = text.split()
    lines, cur = [], ''
    for w in words:
        trial = w if not cur else cur + ' ' + w
        if draw.textlength(trial, font=font) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def wrap_balanced(draw, text, font, max_width):
    """Greedy wrap, then rebalance so the last line is not a single leftover word."""
    words = text.split()
    n = len(words)
    if n <= 1:
        return words or ['']
    widths = [draw.textlength(w, font=font) for w in words]
    space = draw.textlength(' ', font=font)
    def lw(i, j):
        return sum(widths[i:j]) + space * max(0, j - i - 1)
    if lw(0, n) <= max_width:
        return [' '.join(words)]
    best = None
    for mid in range(1, n):
        w1, w2 = lw(0, mid), lw(mid, n)
        if w1 <= max_width and w2 <= max_width:
            cost = abs(w1 - w2) + (max_width if n - mid == 1 else 0)
            if best is None or cost < best[0]:
                best = (cost, [' '.join(words[:mid]), ' '.join(words[mid:])])
    if best:
        return best[1]
    best = None
    for a in range(1, n - 1):
        for b in range(a + 1, n):
            ws = [lw(0, a), lw(a, b), lw(b, n)]
            if all(w <= max_width for w in ws):
                cost = max(ws) - min(ws) + (max_width * 0.5 if n - b == 1 else 0)
                if best is None or cost < best[0]:
                    best = (cost, [' '.join(words[:a]), ' '.join(words[a:b]), ' '.join(words[b:])])
    if best:
        return best[1]
    return wrap_text(draw, text, font, max_width)

def og_font(size, weight=400):
    f = ImageFont.truetype(FONT_PATH, size * OG_SCALE)
    if hasattr(f, 'set_variation_by_axes'):
        try:
            f.set_variation_by_axes([weight])
        except Exception:
            pass
    return f

def og_fh(f):
    a, d = f.getmetrics()
    return a + d

def og_underline(dr, x, y, text, font, size):
    w = dr.textlength(text, font=font)
    thick = max(2 * OG_SCALE, round(0.055 * size * OG_SCALE))
    offset = round(0.18 * size * OG_SCALE)
    uy = y + font.getmetrics()[0] + offset
    dr.rectangle([x, uy, x + w, uy + thick], fill=OG_MUTED)

def fit_title(draw, text, max_width, min_size=44, max_size=80, max_lines=3):
    for size in range(max_size, min_size - 1, -1):
        f = og_font(size, 650)
        lines = wrap_balanced(draw, text, f, max_width)
        if len(lines) <= max_lines:
            return f, size, lines
    f = og_font(min_size, 650)
    return f, min_size, wrap_balanced(draw, text, f, max_width)

def _og_canvas():
    sw, sh = OG_W * OG_SCALE, OG_H * OG_SCALE
    im = Image.new('RGB', (sw, sh), OG_BG)
    return im, ImageDraw.Draw(im), sw, sh

def _og_down(im):
    return im.resize((OG_W, OG_H), Image.LANCZOS)

def compose_home_og():
    im, dr, sw, sh = _og_canvas()
    word, by = og_font(32, 400), og_font(26, 400)
    size, max_w = 56, (OG_W - 160) * OG_SCALE
    while size >= 36 and dr.textlength(SERIES, font=og_font(size, 650)) > max_w:
        size -= 1
    title = og_font(size, 650)
    gap1, gap_t, gap2 = 48 * OG_SCALE, 12 * OG_SCALE, 44 * OG_SCALE
    block = og_fh(word) + gap1 + og_fh(title) + gap_t + og_fh(title) + gap2 + og_fh(by)
    y = (sh - block) // 2
    def cx(text, font):
        return (sw - dr.textlength(text, font=font)) // 2
    dr.text((cx(SITE, word), y), SITE, font=word, fill=OG_MUTED)
    y += og_fh(word) + gap1
    x = cx(SERIES, title)
    dr.text((x, y), SERIES, font=title, fill=OG_TEXT)
    og_underline(dr, x, y, SERIES, title, size)
    y += og_fh(title) + gap_t
    dr.text((cx(SERIES_SUB, title), y), SERIES_SUB, font=title, fill=OG_TEXT)
    y += og_fh(title) + gap2
    dr.text((cx(OG_BYLINE, by), y), OG_BYLINE, font=by, fill=OG_MUTED)
    return _og_down(im)

def compose_post_og(num, short, date):
    im, dr, sw, sh = _og_canvas()
    mx = 96 * OG_SCALE
    word, kicker = og_font(30, 400), og_font(32, 400)
    series_f, date_f = og_font(28, 400), og_font(26, 400)
    tf, size, lines = fit_title(dr, short, sw - 2 * mx)
    lead = int(round(size * 1.12 * OG_SCALE))
    title_h = lead * (len(lines) - 1) + og_fh(tf) if lines else 0
    gap_k, gap_s, gap_d = 10 * OG_SCALE, 28 * OG_SCALE, 32 * OG_SCALE
    block = (og_fh(word) + 52 * OG_SCALE + og_fh(kicker) + gap_k + title_h
             + gap_s + og_fh(series_f) + gap_d + og_fh(date_f))
    y = (sh - block) // 2
    dr.text((mx, y), SITE, font=word, fill=OG_MUTED)
    y += og_fh(word) + 52 * OG_SCALE
    dr.text((mx, y), '%s/30' % num, font=kicker, fill=OG_MUTED)
    y += og_fh(kicker) + gap_k
    for i, line in enumerate(lines):
        dr.text((mx, y), line, font=tf, fill=OG_TEXT)
        y += lead if i < len(lines) - 1 else og_fh(tf)
    y += gap_s
    dr.text((mx, y), SERIES, font=series_f, fill=OG_MUTED)
    y += og_fh(series_f) + gap_d
    dr.text((mx, y), date, font=date_f, fill=OG_MUTED)
    return _og_down(im)

def compose_glossary_og():
    im, dr, sw, sh = _og_canvas()
    word, hero = og_font(32, 400), og_font(72, 650)
    size, max_w = 36, (OG_W - 160) * OG_SCALE
    while size >= 28 and dr.textlength(SERIES, font=og_font(size, 650)) > max_w:
        size -= 1
    title, by = og_font(size, 650), og_font(26, 400)
    gap0, gap1, gap_t, gap2 = 40 * OG_SCALE, 36 * OG_SCALE, 10 * OG_SCALE, 44 * OG_SCALE
    block = (og_fh(word) + gap0 + og_fh(hero) + gap1 + og_fh(title)
             + gap_t + og_fh(title) + gap2 + og_fh(by))
    y = (sh - block) // 2
    def cx(text, font):
        return (sw - dr.textlength(text, font=font)) // 2
    dr.text((cx(SITE, word), y), SITE, font=word, fill=OG_MUTED)
    y += og_fh(word) + gap0
    dr.text((cx('Glossary', hero), y), 'Glossary', font=hero, fill=OG_TEXT)
    y += og_fh(hero) + gap1
    x = cx(SERIES, title)
    dr.text((x, y), SERIES, font=title, fill=OG_TEXT)
    og_underline(dr, x, y, SERIES, title, size)
    y += og_fh(title) + gap_t
    dr.text((cx(SERIES_SUB, title), y), SERIES_SUB, font=title, fill=OG_TEXT)
    y += og_fh(title) + gap2
    dr.text((cx(OG_BYLINE, by), y), OG_BYLINE, font=by, fill=OG_MUTED)
    return _og_down(im)

def write_og(im, directory):
    """Save a content-hashed og-<hash>.jpg and remove stale share images."""
    os.makedirs(directory, exist_ok=True)
    buf = io.BytesIO()
    im.save(buf, 'JPEG', quality=92, optimize=True, progressive=True, subsampling=0)
    data = buf.getvalue()
    name = 'og-%s.jpg' % hashlib.sha1(data).hexdigest()[:10]
    path = os.path.join(directory, name)
    if not os.path.exists(path):
        open(path, 'wb').write(data)
    for f in os.listdir(directory):
        if f != name and (f == 'og.jpg' or re.match(r'^og-[0-9a-f]+\.jpg$', f)):
            os.remove(os.path.join(directory, f))
    return name

def set_head(path, lines):
    s = open(path, encoding='utf-8').read()
    head = '<head>\n' + '\n'.join(lines) + '\n</head>'
    s2, n = re.subn(r'<head>.*?</head>', head, s, count=1, flags=re.S)
    if n != 1:
        raise SystemExit('could not replace head in %s' % path)
    open(path, 'w', encoding='utf-8').write(s2)

def rfc822(iso):
    d = datetime.strptime(iso, '%Y-%m-%d').replace(tzinfo=PT)
    return d.strftime('%a, %d %b %Y %H:%M:%S %z')

def ld(obj):
    return '  <script type="application/ld+json">%s</script>' % json.dumps(obj, ensure_ascii=False, separators=(',', ':'))

# ---------------------------------------------------------------------------
# Identity, topics and discoverability
# ---------------------------------------------------------------------------
import hashlib, subprocess, sys
sys.path.insert(0, os.path.join(ROOT, 'tools'))
from glossary import TERMS, MENTIONS

PERSON_ID = SITE_URL + '/#daniel-burger'
WEBSITE_ID = SITE_URL + '/#website'
BLOG_ID = SITE_URL + '/#blog'
GLOSSARY_URL = SITE_URL + '/glossary/'
TERMSET_ID = GLOSSARY_URL + '#terms'
# Verified profile URLs only (see README "Identity links"). No bio facts.
SAME_AS = [
    'https://danielburger.online/',
    'https://x.com/danburonline',
    'https://www.linkedin.com/in/danburonline/',
    'https://github.com/danburonline',
    'https://substack.com/@danburonline',
]
PERSON = {
    '@type': 'Person',
    '@id': PERSON_ID,
    'name': AUTHOR,
    'url': 'https://danielburger.online/',
    'sameAs': SAME_AS,
    'knowsAbout': [{'@id': GLOSSARY_URL + '#' + t['slug']} for t in TERMS],
}
REL_ME = '\n'.join('  <link rel="me" href="%s">' % u for u in SAME_AS)
def file_v(name):
    return hashlib.sha1(open(os.path.join(ROOT, name), 'rb').read()).hexdigest()[:10]

# Icon URLs carry a content hash so browsers, the service worker and Vercel's
# week-long image cache pick up a new file as soon as the mark is regenerated.
ICON_FILES = ('favicon.svg', 'favicon.ico', 'favicon-32.png', 'apple-touch-icon.png',
              'icon-192.png', 'icon-512.png', 'icon-maskable-512.png')
ICON_V = {n: file_v(n) for n in ICON_FILES}

def icon_src(name):
    return '/%s?v=%s' % (name, ICON_V[name])

ICONS = '''  <link rel="icon" href="%s" type="image/svg+xml">
  <link rel="icon" href="%s" type="image/png" sizes="32x32">
  <link rel="icon" href="%s" sizes="16x16 32x32 48x48">
  <link rel="apple-touch-icon" href="%s" sizes="180x180">
  <link rel="manifest" href="/manifest.webmanifest">
  <meta name="theme-color" content="#f6f1e8" media="(prefers-color-scheme: light)">
  <meta name="theme-color" content="#15130f" media="(prefers-color-scheme: dark)">''' % (
    icon_src('favicon.svg'), icon_src('favicon-32.png'),
    icon_src('favicon.ico'), icon_src('apple-touch-icon.png'))
SERIES_KEYWORDS = ['synthetic consciousness', 'hybrid mind uploading', 'mind uploading',
                   'gradual brain replacement', 'Daniel Burger']
HOME_TITLE = SITE_TITLE
TOPICS_RE = re.compile(r'\n?\s*<!-- topics:start -->.*?<!-- topics:end -->', re.S)
META = json.load(open(os.path.join(ROOT, 'tools', 'meta.json'), encoding='utf-8'))
HOME_DESC = META.get('home', {}).get('description') or (
    'Daniel Burger\'s 30 meditations on synthetic consciousness and hybrid mind uploading, '
    'from gradual brain replacement to the process world-line.')
MOD_PATH = os.path.join(ROOT, 'tools', 'modified.json')
MODIFIED = json.load(open(MOD_PATH, encoding='utf-8')) if os.path.exists(MOD_PATH) else {}
TODAY = datetime.now(PT).strftime('%Y-%m-%d')

def term_ref(t, full=False):
    node = {'@type': 'DefinedTerm', '@id': GLOSSARY_URL + '#' + t['slug'], 'name': t['name'],
            'url': GLOSSARY_URL + '#' + t['slug'], 'inDefinedTermSet': {'@id': TERMSET_ID}}
    if t.get('also'):
        node['alternateName'] = t['also']
    if t.get('sameAs'):
        node['sameAs'] = t['sameAs']
    if full:
        node['description'] = t['text']
        node['termCode'] = t['slug']
    return node

def plain_name(t):
    return re.sub(r'\s*\([A-Z]+\)$', '', t['name'])

def body_text(art):
    body = BeautifulSoup(str(art), 'html.parser').find('article')
    for sel in ['h1', 'time', '.post-nav', '.post-header', '.post-byline', '.essence', '.x-callout', '.tweet-embed', 'script', 'figcaption', '.num-menu-pop']:
        for el in body.select(sel):
            el.decompose()
    return re.sub(r'\s+', ' ', body.get_text(' ')).strip()

def article_hash(text):
    return hashlib.sha1(text.encode('utf-8')).hexdigest()

def ensure_extras(path, topics):
    """Glossary link in the footer and the Topics line after the article."""
    s = open(path, encoding='utf-8').read()
    s = TOPICS_RE.sub('', s)
    if topics:
        links = ', '.join('<a href="/glossary/#%s">%s</a>' % (t['slug'], html.escape(plain_name(t).lower()))
                          for t in topics)
        block = ('\n    <!-- topics:start -->\n    <p class="topics">Topics: %s</p>\n    <!-- topics:end -->' % links)
        s = s.replace('</article>', '</article>' + block, 1)
    if '<main>' not in s:
        s = s.replace('<article>', '<main>\n    <article>', 1)
        end = '<!-- topics:end -->' if topics else '</article>'
        s = s.replace(end, end + '\n    </main>', 1)
    if 'href="/glossary/"' not in s:
        s = re.sub(r'(<footer class="site">\s*<a href="/">[^<]*</a>)', r'\1<a href="/glossary/">Glossary</a>', s, count=1)
    open(path, 'w', encoding='utf-8').write(s)

def common_head(title, desc, canonical):
    return [
        '  <meta charset="utf-8">',
        '  <meta name="viewport" content="width=device-width, initial-scale=1">',
        '  <title>%s</title>' % html.escape(title),
        '  <meta name="description" content="%s">' % html.escape(desc),
        '  <meta name="author" content="%s">' % AUTHOR,
        '  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">',
        '  <link rel="canonical" href="%s">' % canonical,
        FEED_LINK,
        '  <link rel="alternate" type="text/plain" title="llms.txt" href="%s/llms.txt">' % SITE_URL,
        REL_ME,
        ICONS,
    ]

def absolutize(fragment):
    fragment = re.sub(r'(src|href|poster)="/(?!/)', r'\1="%s/' % SITE_URL, fragment)
    return fragment

# ---------------------------------------------------------------------------
# Responsive images: every local article image gets AVIF and WebP variants at
# several widths in <post>/img/ (file names carry a content hash, so they can be
# cached forever). The first image above the text is the LCP candidate: it is
# loaded eagerly with fetchpriority=high and preloaded from <head>.
IMG_WIDTHS = [480, 720, 960, 1280, 1920]
IMG_SIZES = '(min-width: 760px) 640px, calc(100vw - 40px)'
PIC_RE = re.compile(r'<picture data-r>(?:\s*<source[^>]*>)*\s*(<img[^>]*>)\s*</picture>', re.S)
GEN_ATTRS = ('srcset', 'sizes', 'loading', 'decoding', 'fetchpriority', 'data-full')

def strip_attrs(tag, names):
    for n in names:
        tag = re.sub(r'\s%s="[^"]*"' % re.escape(n), '', tag)
    return tag

def add_attrs(tag, attrs):
    extra = ''.join(' %s="%s"' % (k, v) for k, v in attrs)
    return re.sub(r'\s*/?>$', extra + '>', tag)

def responsive_images(path, slug):
    s = open(path, encoding='utf-8').read()
    s = PIC_RE.sub(r'\1', s)
    a0, a1 = s.find('<article'), s.find('</article>')
    if a0 < 0 or a1 < 0:
        return None
    art = s[a0:a1]
    outdir = os.path.join(ROOT, slug, 'img')
    keep, state = set(), {'preload': None, 'first': True}

    def one(m):
        tag = m.group(0)
        sm = re.search(r'\ssrc="([^"]+)"', tag)
        if not sm:
            return tag
        src = sm.group(1)
        if (not src.startswith('/%s/' % slug) or '/img/' in src
                or not src.lower().endswith(('.jpg', '.jpeg', '.png'))):
            return tag
        fpath = os.path.join(ROOT, src.lstrip('/'))
        raw = open(fpath, 'rb').read()
        hh = hashlib.sha1(raw + repr(IMG_WIDTHS).encode()).hexdigest()[:8]
        im = Image.open(fpath)
        im = im.convert('RGBA' if im.mode in ('RGBA', 'LA', 'P') else 'RGB')
        stem = os.path.splitext(os.path.basename(src))[0]
        widths = sorted({w for w in IMG_WIDTHS if w < im.width} | {min(im.width, IMG_WIDTHS[-1])})
        os.makedirs(outdir, exist_ok=True)
        sets = {'avif': [], 'webp': []}
        for w in widths:
            resized = None
            for fmt in ('avif', 'webp'):
                name = '%s-%s-%d.%s' % (stem, hh, w, fmt)
                keep.add(name)
                out = os.path.join(outdir, name)
                if not os.path.exists(out):
                    if resized is None:
                        resized = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
                    if fmt == 'avif':
                        resized.save(out, 'AVIF', quality=60)
                    else:
                        resized.save(out, 'WEBP', quality=82, method=6)
                sets[fmt].append('/%s/img/%s %dw' % (slug, name, w))
        before = re.sub(r'<p>\s*$', '', art[:m.start()])
        hero = state['first'] and '<p>' not in before
        state['first'] = False
        img = strip_attrs(tag, GEN_ATTRS)
        if not re.search(r'\swidth="', img):
            img = add_attrs(img, [('width', im.width), ('height', im.height)])
        attrs = [('data-full', sets['webp'][-1].rsplit(' ', 1)[0])]
        attrs += [('fetchpriority', 'high')] if hero else [('loading', 'lazy'), ('decoding', 'async')]
        img = add_attrs(img, attrs)
        if hero:
            state['preload'] = ('  <link rel="preload" as="image" type="image/avif" imagesrcset="%s" imagesizes="%s" fetchpriority="high">'
                                % (', '.join(sets['avif']), IMG_SIZES))
        return ('<picture data-r><source type="image/avif" srcset="%s" sizes="%s">'
                '<source type="image/webp" srcset="%s" sizes="%s">%s</picture>'
                % (', '.join(sets['avif']), IMG_SIZES, ', '.join(sets['webp']), IMG_SIZES, img))

    art = re.sub(r'<img\b[^>]*>', one, art)
    s = s[:a0] + art + s[a1:]
    open(path, 'w', encoding='utf-8').write(s)
    if os.path.isdir(outdir):
        for f in os.listdir(outdir):
            if f not in keep:
                os.remove(os.path.join(outdir, f))
        if not os.listdir(outdir):
            os.rmdir(outdir)
    return state['preload']

# Section outline (tools/outline.json): the posts are continuous prose, so the
# build gives the paragraph where each section starts a stable id and renders a
# <nav class="toc" aria-label="Sections"> before the article. outline.js makes it
# a sticky sidebar on wide screens and a bottom sheet on narrow ones.
OUTLINE_PATH = os.path.join(ROOT, 'tools', 'outline.json')
OUTLINE = {k: v for k, v in json.load(open(OUTLINE_PATH, encoding='utf-8')).items() if not k.startswith('_')}
TOC_RE = re.compile(r'\s*<nav class="toc"[^>]*>.*?</nav>', re.S)
SEC_ID_RE = re.compile(r'<p id="sec-[^"]*"')
P_RE = re.compile(r'<p(\s[^>]*)?>(.*?)</p>', re.S)

def sec_id(label):
    return 'sec-' + (re.sub(r'[^a-z0-9]+', '-', label.lower()).strip('-') or 'part')

def norm_text(fragment):
    t = html.unescape(re.sub(r'<[^>]+>', ' ', fragment))
    return re.sub(r'\s+', ' ', t).strip()

SEC_AT_RE = re.compile(r'<span class="sec-at" id="sec-[^"]*"></span>')

def text_positions(fragment):
    """(non-space text, html offset of each of its characters) for an HTML fragment."""
    chars, offs, i = [], [], 0
    while i < len(fragment):
        c = fragment[i]
        if c == '<':
            i = fragment.index('>', i) + 1
            continue
        if c == '&':
            m = re.match(r'&(#x[0-9a-fA-F]+|#[0-9]+|[a-zA-Z]+);', fragment[i:])
            if m:
                for ch in html.unescape(m.group(0)):
                    if not ch.isspace():
                        chars.append(ch); offs.append(i)
                i += len(m.group(0))
                continue
        if not c.isspace():
            chars.append(c); offs.append(i)
        i += 1
    return ''.join(chars), offs

# Essence card (tools/essence.json): a short summary under the chart that also
# carries the "Originally posted on X" line as its footer. Idempotent: an existing
# card is unwrapped back to the plain banner first, so removing a key reverts it.
ESSENCE_PATH = os.path.join(ROOT, 'tools', 'essence.json')
ESSENCE = {k: v for k, v in json.load(open(ESSENCE_PATH, encoding='utf-8')).items() if not k.startswith('_')} if os.path.exists(ESSENCE_PATH) else {}
ESSENCE_RE = re.compile(r'<aside class="essence"[^>]*>.*?(<a class="x-callout".*?</a>)</aside>', re.S)
XC_RE = re.compile(r'<a class="x-callout".*?</a>', re.S)

def apply_essence(path, slug):
    s = open(path, encoding='utf-8').read()
    orig = s
    s = ESSENCE_RE.sub(lambda m: m.group(1), s)
    text = ESSENCE.get(slug)
    if text:
        words = len(text.split())
        if words >= 50:
            raise SystemExit('essence for %s has %d words; keep it under 50' % (slug, words))
        m = XC_RE.search(s)
        if not m:
            print('WARNING: essence for %s: no x-callout to attach to' % slug)
        else:
            card = ('<aside class="essence" id="sec-essence" aria-labelledby="essence-label">'
                    '<p class="essence-label" id="essence-label">TL;DR</p>'
                    '<p class="essence-text">%s</p>%s</aside>'
                    % (html.escape(text, quote=False), m.group(0)))
            s = s[:m.start()] + card + s[m.end():]
    if s != orig:
        open(path, 'w', encoding='utf-8').write(s)

def apply_outline(path, slug):
    """Idempotent: section anchors (an id on the paragraph, or an empty
    <span class="sec-at"> before a sentence inside it) plus the Sections nav."""
    s = open(path, encoding='utf-8').read()
    orig = s
    s = TOC_RE.sub('', s, count=1)
    s = SEC_ID_RE.sub('<p', s)
    s = SEC_AT_RE.sub('', s)
    entries = OUTLINE.get(slug)
    if not entries:
        print('WARNING: no outline for %s; add it to tools/outline.json' % slug)
    else:
        a0 = s.index('<article>')
        a1 = s.index('</article>', a0)
        art = s[a0:a1]
        items, used, ids = [], set(), set()
        paras = list(P_RE.finditer(art))
        for e in entries:
            want = re.sub(r'\s+', '', html.unescape(e['starts']))
            hit = next((m for m in paras if re.sub(r'\s+', '', norm_text(m.group(2))).startswith(want)), None)
            if not hit:
                print('WARNING: outline for %s: no paragraph starts with %r' % (slug, want))
                continue
            sid = e.get('id') or sec_id(e['label'])
            if not re.fullmatch(r'sec-[a-z0-9-]+', sid):
                raise SystemExit('invalid outline id for %s: %s' % (slug, sid))
            if sid in ids:
                raise SystemExit('duplicate outline id for %s: %s' % (slug, sid))
            ids.add(sid)
            if e.get('at'):
                txt, offs = text_positions(hit.group(2))
                at = re.sub(r'\s+', '', html.unescape(e['at']))
                k = txt.find(at)
                if k < 0:
                    print('WARNING: outline for %s: %r not found in the paragraph starting %r' % (slug, e['at'], e['starts']))
                    continue
                items.append((sid, e['label'], hit.start(2) + offs[k], 'span'))
            else:
                if hit.start() in used:
                    raise SystemExit('two outline entries start the same paragraph in %s' % slug)
                used.add(hit.start())
                items.append((sid, e['label'], hit.start(), 'p'))
        for sid, _, pos, kind in sorted(items, key=lambda x: -x[2]):
            if kind == 'p':
                art = art[:pos] + '<p id="%s"' % sid + art[pos + 2:]
            else:
                art = art[:pos] + '<span class="sec-at" id="%s"></span>' % sid + art[pos:]
        s = s[:a0] + art + s[a1:]
        # The TL;DR card stays on the page but is not a section in the outline.
        items.sort(key=lambda x: x[2])
        nav = ('    <nav class="toc" id="toc" aria-label="Sections">\n'
               '      <p class="toc-head" aria-hidden="true">Sections</p>\n      <ol>\n'
               + ''.join('        <li><a href="#%s">%s</a></li>\n' % (sid, html.escape(lab, quote=False)) for sid, lab, _, _ in items)
               + '      </ol>\n    </nav>\n')
        s2, n = re.subn(r'(<main>\n)', lambda m: m.group(1) + nav, s, count=1)
        if n != 1:
            raise SystemExit('could not insert outline in %s' % path)
        s = s2
    if s != orig:
        open(path, 'w', encoding='utf-8').write(s)

posts = []
for d in sorted(os.listdir(ROOT)):
    m = re.match(r'^(\d+)-', d)
    p = os.path.join(ROOT, d, 'index.html')
    if not m or not os.path.exists(p):
        continue
    preload = responsive_images(p, d)
    apply_essence(p, d)
    apply_outline(p, d)
    soup = BeautifulSoup(open(p, encoding='utf-8').read(), 'html.parser')
    art = soup.find('article')
    h1 = art.find('h1')
    raw = re.sub(r'\s+', ' ', h1.get_text(' ', strip=True)).replace(' /', '/').replace(' :', ':').strip()
    t = art.find('time')
    num = int(m.group(1))
    # New chrome: h1 is only the post title. Old chrome: "N/30 Series: Title".
    if art.find(class_='post-header') or ':' not in raw:
        short = raw
    else:
        short = raw.split(':', 1)[1].strip()
    # Keep the historical full title so JSON-LD, llms.txt and search stay stable.
    title = '%s/30 %s: %s' % (num, SERIES, short)
    page_title = '%s/30 %s · Meditations on Synthetic Consciousness' % (num, short)
    meta = META.get(d, {})
    desc = meta.get('description') or excerpt(first_para(art))
    img_el = art.find('img')
    video = art.find('video')
    if img_el and img_el.get('src'):
        src_file = img_el['src'].rsplit('/', 1)[-1]
        alt = img_el.get('alt') or short
    elif video and video.get('poster'):
        src_file = video['poster'].rsplit('/', 1)[-1]
        alt = 'Video poster for %s/30 %s' % (num, short)
    else:
        ogm = soup.find('meta', property='og:image')
        src_file = ogm['content'].rsplit('/', 1)[-1]
        alt = short
    src_path = os.path.join(ROOT, d, src_file)
    os.makedirs(os.path.join(ROOT, 'thumbs'), exist_ok=True)
    im = Image.open(src_path).convert('RGB')
    W, H = 360, 240
    s = max(W / im.width, H / im.height)
    thumb = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    l, tp = (thumb.width - W) // 2, (thumb.height - H) // 2
    thumb.crop((l, tp, l + W, tp + H)).save(
        os.path.join(ROOT, 'thumbs', d + '.jpg'), quality=82, optimize=True)
    og_name = write_og(compose_post_og(num, short, t.get_text(strip=True)), os.path.join(ROOT, d))
    text = body_text(art)
    words = len(re.findall(r"[\w'’-]+", text))
    # dateModified: the day the article text last changed (tracked in tools/modified.json)
    h = article_hash(text)
    rec = MODIFIED.get(d)
    if not rec or rec.get('hash') != h:
        rec = {'hash': h, 'date': max(TODAY, t['datetime']) if rec else t['datetime']}
        MODIFIED[d] = rec
    modified = max(rec['date'], t['datetime'])
    topics = [x for x in TERMS if re.search(x['pattern'], text, re.I)]
    mentions = [x for x in MENTIONS if re.search(x['pattern'], text, re.I)]
    xc = art.find('a', class_='x-callout')
    url = '%s/%s/' % (SITE_URL, d)
    og_url = '%s/%s/%s' % (SITE_URL, d, og_name)
    og_alt = '%s/30 %s' % (num, short)
    video_src = None
    if video and video.get('src'):
        video_src = SITE_URL + video['src']
    # full article HTML for the feed and plain text for llms-full.txt
    clean = BeautifulSoup(str(art), 'html.parser').find('article')
    for sel in ['h1', 'time', '.post-nav', '.post-header', '.post-byline', '.essence', '.x-callout', 'script', '.num-menu-pop']:
        for el in clean.select(sel):
            el.decompose()
    for el in clean.select('p[id^="sec-"]'):
        del el['id']
    for el in clean.select('span.sec-at'):
        el.decompose()
    for pic in clean.select('picture'):
        im_el = pic.find('img')
        for k in GEN_ATTRS:
            im_el.attrs.pop(k, None)
        pic.replace_with(im_el)
    rewrite_post_chrome(p, num, short, t['datetime'], t.get_text(strip=True), words)
    posts.append(dict(preload=preload,
        n=num, slug=d, title=title, short=short, page_title=page_title,
        date=t.get_text(strip=True), iso=t['datetime'], modified=modified, words=words,
        thumb='/thumbs/%s.jpg?v=%s' % (d, hashlib.sha1(open(os.path.join(ROOT, 'thumbs', d + '.jpg'), 'rb').read()).hexdigest()[:8]), desc=desc, alt=alt, og_alt=og_alt, url=url, og=og_url,
        video=video_src, vw=video.get('width') if video else None,
        vh=video.get('height') if video else None, topics=topics, mentions=mentions,
        x=xc['href'] if xc else None, html=absolutize(clean.decode_contents().strip()),
        text=text, path=p))

posts.sort(key=lambda x: -x['n'])
json.dump(MODIFIED, open(MOD_PATH, 'w', encoding='utf-8'), indent=1, sort_keys=True)
last_mod = max(q['modified'] for q in posts)

for q in posts:
    kw = [plain_name(x).lower() for x in q['topics']] + [k for k in SERIES_KEYWORDS
                                                         if k.lower() not in [plain_name(x).lower() for x in q['topics']]]
    q['keywords'] = kw
    posting = {
        '@type': 'BlogPosting',
        '@id': q['url'] + '#post',
        'headline': q['title'][:110],
        'name': q['title'],
        'description': q['desc'],
        'url': q['url'],
        'datePublished': q['iso'],
        'dateModified': q['modified'],
        'wordCount': q['words'],
        'inLanguage': 'en',
        'author': {'@id': PERSON_ID},
        'publisher': {'@id': PERSON_ID},
        'image': {'@type': 'ImageObject', 'url': q['og'], 'width': OG_W, 'height': OG_H},
        'mainEntityOfPage': {'@id': q['url']},
        'isPartOf': {'@id': BLOG_ID},
        'position': q['n'],
        'keywords': ', '.join(kw),
        'about': [{'@id': GLOSSARY_URL + '#' + x['slug']} for x in q['topics']],
    }
    if q['mentions']:
        posting['mentions'] = [{'@type': 'Thing', 'name': x['name'], 'sameAs': x['sameAs']} for x in q['mentions']]
    if q['x']:
        posting['discussionUrl'] = q['x']
    if q['video']:
        posting['video'] = {'@type': 'VideoObject', 'name': q['title'], 'contentUrl': q['video'],
                            'thumbnailUrl': q['og'], 'uploadDate': q['iso'], 'description': q['desc']}
    graph = {'@context': 'https://schema.org', '@graph': [
        posting,
        {'@type': 'WebPage', '@id': q['url'], 'url': q['url'], 'name': q['page_title'],
         'isPartOf': {'@id': WEBSITE_ID}, 'inLanguage': 'en',
         'primaryImageOfPage': {'@type': 'ImageObject', 'url': q['og']},
         'breadcrumb': {'@type': 'BreadcrumbList', 'itemListElement': [
             {'@type': 'ListItem', 'position': 1, 'name': SITE, 'item': SITE_URL + '/'},
             {'@type': 'ListItem', 'position': 2, 'name': q['title'], 'item': q['url']}]}},
        {'@type': ['Blog', 'CreativeWorkSeries'], '@id': BLOG_ID, 'name': SITE_TITLE, 'url': SITE_URL + '/'},
        PERSON,
    ] + [term_ref(x) for x in q['topics']]}
    lines = common_head(q['page_title'], q['desc'], q['url'])
    if q['preload']:
        lines.insert(3, q['preload'])
    lines += [
        '  <meta name="keywords" content="%s">' % html.escape(', '.join(kw)),
        '  <meta property="og:type" content="article">',
        '  <meta property="og:title" content="%s">' % html.escape(q['page_title']),
        '  <meta property="og:description" content="%s">' % html.escape(q['desc']),
        '  <meta property="og:url" content="%s">' % q['url'],
        '  <meta property="og:site_name" content="%s">' % SITE,
        '  <meta property="og:locale" content="en_GB">',
        '  <meta property="og:image" content="%s">' % q['og'],
        '  <meta property="og:image:width" content="%s">' % OG_W,
        '  <meta property="og:image:height" content="%s">' % OG_H,
        '  <meta property="og:image:alt" content="%s">' % html.escape(q['og_alt']),
    ]
    if q['video']:
        lines += [
            '  <meta property="og:video" content="%s">' % q['video'],
            '  <meta property="og:video:type" content="video/mp4">',
            '  <meta property="og:video:width" content="%s">' % (q['vw'] or '1280'),
            '  <meta property="og:video:height" content="%s">' % (q['vh'] or '720'),
        ]
    lines += [
        '  <meta property="article:published_time" content="%s">' % q['iso'],
        '  <meta property="article:modified_time" content="%s">' % q['modified'],
        '  <meta property="article:author" content="%s">' % 'https://danielburger.online/',
        '  <meta property="article:section" content="%s">' % html.escape(SITE_TITLE),
    ] + ['  <meta property="article:tag" content="%s">' % html.escape(k) for k in kw] + [
        '  <meta name="twitter:card" content="summary_large_image">',
        '  <meta name="twitter:site" content="@danburonline">',
        '  <meta name="twitter:creator" content="@danburonline">',
        '  <meta name="twitter:title" content="%s">' % html.escape(q['page_title']),
        '  <meta name="twitter:description" content="%s">' % html.escape(q['desc']),
        '  <meta name="twitter:image" content="%s">' % q['og'],
        '  <meta name="twitter:image:alt" content="%s">' % html.escape(q['og_alt']),
        ld(graph),
        THEME_HEAD,
    ]
    set_head(q['path'], lines)
    ensure_extras(q['path'], q['topics'])

# ---------------------------------------------------------------------------
# Home
items = []
for q in posts:
    items.append(f'''        <li data-n="{q['n']}" data-words="{q['words']}" data-search="{html.escape((q['title'] + ' ' + q['date']).lower())}">
          <div class="thumb"><img src="{q['thumb']}" width="180" height="120" alt="" loading="lazy"></div>
          <div class="post-info">
            <a class="title" href="/{q['slug']}/">{q['n']}/30 {html.escape(q['short'])}</a>
            <span class="meta"><time datetime="{q['iso']}">{q['date']}</time><span class="dot" aria-hidden="true">&middot;</span>{q['words']:,} words</span>
          </div>
        </li>''')
total = sum(q['words'] for q in posts)
block = ('<!-- posts:start -->\n'
         f'      <div class="list-tools"><input class="filter" type="search" placeholder="Filter meditations" aria-label="Filter meditations"><select class="sort" aria-label="Sort meditations"><option value="new">Newest first</option><option value="old">Oldest first</option><option value="long">Longest first</option><option value="short">Shortest first</option></select><span class="list-count" data-total="{len(posts)}">{len(posts)} of 30 published &middot; {total:,} words so far</span></div>\n'
         '      <ul class="post-list">\n' + '\n'.join(items) + '\n      </ul>\n'
         '      <p class="no-match" hidden>No meditations match that.</p>\n'
         '      <!-- posts:end -->')
ip = os.path.join(ROOT, 'index.html')
s = open(ip, encoding='utf-8').read()
s = re.sub(r'<!-- posts:start -->.*?<!-- posts:end -->', lambda _: block, s, flags=re.S)
if 'href="/glossary/"' not in s:
    s = s.replace('<a href="https://github.com/danburonline/inkhaven-2026">GitHub</a>',
                  '<a href="https://github.com/danburonline/inkhaven-2026">GitHub</a><a href="/glossary/">Glossary</a>', 1)
open(ip, 'w', encoding='utf-8').write(s)

home_desc = HOME_DESC
home_og_name = write_og(compose_home_og(), ROOT)
home_og_url = SITE_URL + '/' + home_og_name
about_terms = [{'@id': GLOSSARY_URL + '#' + x['slug']} for x in TERMS]
home_ld = {
    '@context': 'https://schema.org',
    '@graph': [
        {
            '@type': 'WebSite', '@id': WEBSITE_ID, 'name': SITE, 'alternateName': SITE_TITLE,
            'url': SITE_URL + '/', 'description': home_desc, 'inLanguage': 'en',
            'author': {'@id': PERSON_ID}, 'publisher': {'@id': PERSON_ID},
        },
        {
            '@type': ['Blog', 'CreativeWorkSeries'], '@id': BLOG_ID, 'name': SITE_TITLE, 'url': SITE_URL + '/',
            'description': home_desc, 'inLanguage': 'en', 'isPartOf': {'@id': WEBSITE_ID},
            'author': {'@id': PERSON_ID}, 'publisher': {'@id': PERSON_ID},
            'image': home_og_url, 'dateModified': last_mod,
            'keywords': ', '.join(plain_name(x).lower() for x in TERMS),
            'about': about_terms,
            'blogPost': [{'@type': 'BlogPosting', '@id': q['url'] + '#post', 'headline': q['title'][:110],
                          'url': q['url'], 'datePublished': q['iso'], 'author': {'@id': PERSON_ID}}
                         for q in posts],
        },
        {'@type': 'WebPage', '@id': SITE_URL + '/', 'url': SITE_URL + '/', 'name': HOME_TITLE,
         'isPartOf': {'@id': WEBSITE_ID}, 'about': {'@id': BLOG_ID}, 'inLanguage': 'en'},
        PERSON,
        {'@type': 'DefinedTermSet', '@id': TERMSET_ID, 'name': 'Glossary', 'url': GLOSSARY_URL},
    ] + [term_ref(x) for x in TERMS],
}
set_head(ip, common_head(HOME_TITLE, home_desc, SITE_URL + '/') + [
    '  <meta name="keywords" content="%s">' % html.escape(', '.join(plain_name(x).lower() for x in TERMS) + ', Daniel Burger'),
    '  <meta property="og:type" content="website">',
    '  <meta property="og:title" content="%s">' % html.escape(HOME_TITLE),
    '  <meta property="og:description" content="%s">' % html.escape(home_desc),
    '  <meta property="og:url" content="%s/">' % SITE_URL,
    '  <meta property="og:site_name" content="%s">' % SITE,
    '  <meta property="og:locale" content="en_GB">',
    '  <meta property="og:image" content="%s">' % home_og_url,
    '  <meta property="og:image:width" content="%s">' % OG_W,
    '  <meta property="og:image:height" content="%s">' % OG_H,
    '  <meta property="og:image:alt" content="%s">' % html.escape(SITE_TITLE),
    '  <meta name="twitter:card" content="summary_large_image">',
    '  <meta name="twitter:site" content="@danburonline">',
    '  <meta name="twitter:creator" content="@danburonline">',
    '  <meta name="twitter:title" content="%s">' % html.escape(HOME_TITLE),
    '  <meta name="twitter:description" content="%s">' % html.escape(home_desc),
    '  <meta name="twitter:image" content="%s">' % home_og_url,
    '  <meta name="twitter:image:alt" content="%s">' % html.escape(SITE_TITLE),
    ld(home_ld),
    THEME_HEAD,
])

for q in posts:
    ensure_chrome(q['path'])
ensure_chrome(ip)
# Home header icons live in a nav, not a paragraph, so the page has a landmark.
hs = open(ip, encoding='utf-8').read()
hs2, n = re.subn(
    r'<p class="site-links">',
    '<nav class="site-links" aria-label="Site">',
    hs, count=1)
if n:
    hs2, n2 = re.subn(
        r'</p>(\s*</header>)',
        r'</nav>\1',
        hs2, count=1)
    if n2:
        hs = hs2
        open(ip, 'w', encoding='utf-8').write(hs)

# Link the home intro's Inkhaven mention to the official residency site.
def _link_intro_inkhaven(m):
    block = m.group(0)
    if 'inkhaven.blog' in block or 'class="inkhaven"' in block:
        return block
    if 'Inkhaven' not in block:
        return block
    return block.replace('Inkhaven', INKHAVEN_LINK, 1)
hs = open(ip, encoding='utf-8').read()
hs2, n = re.subn(r'<p class="intro">.*?</p>', _link_intro_inkhaven, hs, count=1, flags=re.S)
if n and hs2 != hs:
    open(ip, 'w', encoding='utf-8').write(hs2)


# ---------------------------------------------------------------------------
# Glossary page
by_slug = {q['slug']: q for q in posts}
gl_desc = ('Working definitions of synthetic consciousness, hybrid mind uploading, gradual brain replacement '
           'and related terms, as used in Daniel Burger\'s meditations.')
gl_title = 'Glossary · Meditations on Synthetic Consciousness'
sections = []
for x in TERMS:
    used = [by_slug[sl] for sl in x['sources'] if sl in by_slug]
    used += [q for q in sorted(posts, key=lambda q: q['n']) if x in q['topics'] and q not in used]
    used = sorted(used, key=lambda q: q['n'])
    also = ''
    if x.get('also'):
        also = '\n        <p class="term-also">Also: %s</p>' % ', '.join(html.escape(a) for a in x['also'])
    src = ''
    if used:
        src = '\n        <p class="term-src">Discussed in %s</p>' % ', '.join(
            '<a href="/%s/">%s/30 %s</a>' % (q['slug'], q['n'], html.escape(q['short'])) for q in used)
    sections.append(f'''      <section class="term" id="{x['slug']}">
        <h2>{html.escape(x['name'])}</h2>
        <p>{html.escape(x['text'])}</p>{also}{src}
      </section>''')
gl_body = f'''<body>
  <div class="wrap glossary">
{slim_nav_html()}
    <main>
      <h1>Glossary</h1>
      <p class="intro">Terms as they are used in <a href="/">{html.escape(SITE_TITLE)}</a> by {AUTHOR}. These are working definitions and will change as the series does.</p>
{chr(10).join(sections)}
    </main>
    <footer class="site">
      <a href="/">&larr; All posts</a><a href="https://x.com/danburonline">@danburonline</a>
    </footer>
  </div>
  <script src="/theme.js"></script>
</body>
</html>
'''
gl_ld = {'@context': 'https://schema.org', '@graph': [
    {'@type': ['DefinedTermSet', 'WebPage'], '@id': TERMSET_ID, 'url': GLOSSARY_URL, 'name': 'Glossary',
     'description': gl_desc, 'inLanguage': 'en', 'isPartOf': {'@id': WEBSITE_ID},
     'author': {'@id': PERSON_ID}, 'dateModified': last_mod,
     'hasDefinedTerm': [{'@id': GLOSSARY_URL + '#' + x['slug']} for x in TERMS]},
    PERSON,
] + [term_ref(x, full=True) for x in TERMS]}
gdir = os.path.join(ROOT, 'glossary')
os.makedirs(gdir, exist_ok=True)
gl_og_name = write_og(compose_glossary_og(), gdir)
gl_og_url = SITE_URL + '/glossary/' + gl_og_name
gl_og_alt = 'Glossary · ' + SERIES
gl_head = common_head(gl_title, gl_desc, GLOSSARY_URL) + [
    '  <meta name="keywords" content="%s">' % html.escape(', '.join(plain_name(x).lower() for x in TERMS)),
    '  <meta property="og:type" content="website">',
    '  <meta property="og:title" content="%s">' % html.escape(gl_title),
    '  <meta property="og:description" content="%s">' % html.escape(gl_desc),
    '  <meta property="og:url" content="%s">' % GLOSSARY_URL,
    '  <meta property="og:site_name" content="%s">' % SITE,
    '  <meta property="og:locale" content="en_GB">',
    '  <meta property="og:image" content="%s">' % gl_og_url,
    '  <meta property="og:image:width" content="%s">' % OG_W,
    '  <meta property="og:image:height" content="%s">' % OG_H,
    '  <meta property="og:image:alt" content="%s">' % html.escape(gl_og_alt),
    '  <meta name="twitter:card" content="summary_large_image">',
    '  <meta name="twitter:site" content="@danburonline">',
    '  <meta name="twitter:creator" content="@danburonline">',
    '  <meta name="twitter:title" content="%s">' % html.escape(gl_title),
    '  <meta name="twitter:description" content="%s">' % html.escape(gl_desc),
    '  <meta name="twitter:image" content="%s">' % gl_og_url,
    '  <meta name="twitter:image:alt" content="%s">' % html.escape(gl_og_alt),
    ld(gl_ld),
    THEME_HEAD,
]
open(os.path.join(gdir, 'index.html'), 'w', encoding='utf-8').write(
    '<!DOCTYPE html>\n<html lang="en">\n<head>\n' + '\n'.join(gl_head) + '\n</head>\n' + gl_body)

# 404 page
nf_head = [
    '  <meta charset="utf-8">',
    '  <meta name="viewport" content="width=device-width, initial-scale=1">',
    '  <title>Page not found · Meditations on Synthetic Consciousness</title>',
    '  <meta name="robots" content="noindex">',
    ICONS,
    THEME_HEAD,
]
open(os.path.join(ROOT, '404.html'), 'w', encoding='utf-8').write(
    '<!DOCTYPE html>\n<html lang="en">\n<head>\n' + '\n'.join(nf_head) + '\n</head>\n' + f'''<body>
  <div class="wrap">
{slim_nav_html()}
    <main>
      <h1>Page not found</h1>
      <p>There is nothing at this address. The meditations are listed on the <a href="/">home page</a>, and the terms they use are in the <a href="/glossary/">glossary</a>.</p>
    </main>
  </div>
  <script src="/theme.js"></script>
</body>
</html>
''')

# ---------------------------------------------------------------------------
# sitemap, robots, feed, llms.txt
smap = ['<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
smap.append('  <url><loc>%s/</loc><lastmod>%s</lastmod><changefreq>daily</changefreq></url>' % (SITE_URL, last_mod))
smap.append('  <url><loc>%s</loc><lastmod>%s</lastmod></url>' % (GLOSSARY_URL, last_mod))
for q in posts:
    smap.append('  <url><loc>%s</loc><lastmod>%s</lastmod></url>' % (xml_esc(q['url']), q['modified']))
smap.append('</urlset>\n')
open(os.path.join(ROOT, 'sitemap.xml'), 'w', encoding='utf-8').write('\n'.join(smap))

BOTS = ['Googlebot', 'Google-Extended', 'Bingbot', 'Applebot', 'Applebot-Extended', 'DuckDuckBot',
        'GPTBot', 'OAI-SearchBot', 'ChatGPT-User', 'ClaudeBot', 'Claude-SearchBot', 'Claude-User',
        'anthropic-ai', 'PerplexityBot', 'Perplexity-User', 'CCBot', 'Google-CloudVertexBot',
        'Meta-ExternalAgent', 'Amazonbot', 'YandexBot', 'cohere-ai', 'MistralAI-User', 'xAI-Bot']
robots = ['# Search engines and AI systems are welcome to read and cite this site.',
          '# Summary for language models: %s/llms.txt' % SITE_URL, '']
for b in BOTS:
    robots += ['User-agent: %s' % b, 'Allow: /', '']
robots += ['User-agent: *', 'Allow: /', '', 'Sitemap: %s/sitemap.xml' % SITE_URL, '']
open(os.path.join(ROOT, 'robots.txt'), 'w', encoding='utf-8').write('\n'.join(robots))

feed = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:content="http://purl.org/rss/1.0/modules/content/">',
    '  <channel>',
    '    <title>%s</title>' % xml_esc(SITE_TITLE),
    '    <link>%s/</link>' % SITE_URL,
    '    <description>%s</description>' % xml_esc(home_desc),
    '    <language>en</language>',
    '    <lastBuildDate>%s</lastBuildDate>' % rfc822(last_mod),
    '    <atom:link href="%s/feed.xml" rel="self" type="application/rss+xml"/>' % SITE_URL,
]
for q in posts:
    feed += [
        '    <item>',
        '      <title>%s</title>' % xml_esc(q['page_title']),
        '      <link>%s</link>' % xml_esc(q['url']),
        '      <guid isPermaLink="true">%s</guid>' % xml_esc(q['url']),
        '      <pubDate>%s</pubDate>' % rfc822(q['iso']),
        '      <dc:creator>%s</dc:creator>' % xml_esc(AUTHOR),
    ] + ['      <category>%s</category>' % xml_esc(k) for k in q['keywords'][:len(q['topics'])]] + [
        '      <description>%s</description>' % xml_esc(q['desc']),
        '      <content:encoded><![CDATA[%s]]></content:encoded>' % q['html'].replace(']]>', ']]&gt;'),
        '    </item>',
    ]
feed += ['  </channel>', '</rss>', '']
open(os.path.join(ROOT, 'feed.xml'), 'w', encoding='utf-8').write('\n'.join(feed))

chron = sorted(posts, key=lambda q: q['n'])
llms = [
    '# %s' % SITE_TITLE, '',
    '> %s is the home of "%s", a series of thirty daily essays by %s (11 November to 10 December 2026). '
    'They work through the ideas of synthetic consciousness (the vision) and hybrid mind uploading (the mission), '
    'one concept per day, as meditations in Descartes\' sense: first-person working through, not settled claims.' % (SITE, SITE_TITLE, AUTHOR), '',
    'Author: %s. Profiles: %s.' % (AUTHOR, ', '.join(SAME_AS)), '',
    'When citing, please attribute the concepts below as used here to %s and link the relevant page. '
    'Hybrid mind uploading (HMU) is distinct from classical mind uploading (CMU): HMU keeps one process '
    'world-line going through a hybrid biological and engineered state with gradual replacement, while CMU '
    'scans, stores and simulates a brain, and the series does not treat the resulting copy as survival.' % AUTHOR, '',
    '## Key concepts', '',
]
for x in TERMS:
    llms.append('- [%s](%s#%s): %s' % (x['name'], GLOSSARY_URL, x['slug'], x['short']))
llms += ['', '## Meditations', '']
for q in chron:
    llms.append('- [%s](%s): %s' % (q['title'], q['url'], q['desc']))
llms += ['', '## Optional', '',
         '- [Glossary](%s): working definitions of every term above' % GLOSSARY_URL,
         '- [Full text of all meditations](%s/llms-full.txt)' % SITE_URL,
         '- [RSS feed with full content](%s/feed.xml)' % SITE_URL,
         '- [Source on GitHub](https://github.com/danburonline/inkhaven-2026)', '']
open(os.path.join(ROOT, 'llms.txt'), 'w', encoding='utf-8').write('\n'.join(llms))

full = ['# %s' % SITE_TITLE, '', 'By %s. %s' % (AUTHOR, SITE_URL + '/'), '', '## Glossary', '']
for x in TERMS:
    full += ['### %s' % x['name'], '', x['text'], '', 'Source: %s#%s' % (GLOSSARY_URL, x['slug']), '']
for q in chron:
    full += ['---', '', '## %s' % q['title'], '',
             'URL: %s' % q['url'], 'Author: %s' % AUTHOR, 'Published: %s' % q['iso'],
             'Topics: %s' % ', '.join(plain_name(x).lower() for x in q['topics']), '']
    soup_t = BeautifulSoup(q['html'], 'html.parser')
    for el in soup_t.select('.tweet-embed, figcaption'):
        el.decompose()
    for blk in soup_t.find_all(['p', 'li', 'h2', 'h3', 'blockquote']):
        tx = re.sub(r'\s+', ' ', blk.get_text(' ', strip=True)).strip()
        if tx and not blk.find_parent(['p', 'li', 'blockquote']):
            full += [tx, '']
open(os.path.join(ROOT, 'llms-full.txt'), 'w', encoding='utf-8').write('\n'.join(full))

# ---------------------------------------------------------------------------
# PWA: offline page, web app manifest, service worker, versioned script URLs
off_dir = os.path.join(ROOT, 'offline')
os.makedirs(off_dir, exist_ok=True)
off_head = [
    '  <meta charset="utf-8">',
    '  <meta name="viewport" content="width=device-width, initial-scale=1">',
    '  <title>Offline · Meditations on Synthetic Consciousness</title>',
    '  <meta name="robots" content="noindex">',
    ICONS,
    THEME_HEAD,
]
open(os.path.join(off_dir, 'index.html'), 'w', encoding='utf-8').write(
    '<!DOCTYPE html>\n<html lang="en">\n<head>\n' + '\n'.join(off_head) + '\n</head>\n' + f"""<body>
  <div class="wrap">
{slim_nav_html()}
    <main>
      <h1>You are offline</h1>
      <p>This page has not been saved for reading without a connection yet. Meditations you have opened before are still available, as are the <a href="/">home page</a> and the <a href="/glossary/">glossary</a> if you have visited them.</p>
    </main>
  </div>
  <script src="/theme.js"></script>
</body>
</html>
""")

manifest = {
    'id': '/',
    'name': SITE_TITLE,
    'short_name': SITE,
    'description': HOME_DESC,
    'lang': 'en',
    'dir': 'ltr',
    'start_url': '/',
    'scope': '/',
    'display': 'standalone',
    'background_color': '#f6f1e8',
    'theme_color': '#f6f1e8',
    'categories': ['books', 'education'],
    'icons': [
        {'src': icon_src('icon-192.png'), 'sizes': '192x192', 'type': 'image/png', 'purpose': 'any'},
        {'src': icon_src('icon-512.png'), 'sizes': '512x512', 'type': 'image/png', 'purpose': 'any'},
        {'src': icon_src('icon-maskable-512.png'), 'sizes': '512x512', 'type': 'image/png', 'purpose': 'maskable'},
        {'src': icon_src('favicon.svg'), 'sizes': 'any', 'type': 'image/svg+xml', 'purpose': 'any'},
    ],
}
open(os.path.join(ROOT, 'manifest.webmanifest'), 'w', encoding='utf-8').write(
    json.dumps(manifest, indent=1, ensure_ascii=False) + '\n')

data = [{k: q[k] for k in ('n', 'slug', 'short', 'date', 'words')} for q in posts]
open(os.path.join(ROOT, 'posts.json'), 'w').write(json.dumps(data, indent=1, ensure_ascii=False))

# preview.js and nav.js fetch /previews.json and /posts.json with ?v=<content
# hash>, so a changed file always gets a new URL and no browser or service
# worker cache can serve a copy without the newest entries.
for js, jf in (('preview.js', 'previews.json'), ('nav.js', 'posts.json')):
    jv = hashlib.sha1(open(os.path.join(ROOT, jf), 'rb').read()).hexdigest()[:10]
    jp = os.path.join(ROOT, js)
    t = open(jp, encoding='utf-8').read()
    t2 = re.sub(r"'/%s(?:\?v=[0-9a-f]+)?'" % re.escape(jf), "'/%s?v=%s'" % (jf, jv), t)
    if t2 != t:
        open(jp, 'w', encoding='utf-8').write(t2)

# Scripts are referenced as /name.js?v=<content hash>, so vercel.json can cache
# them for a year and a changed file always gets a new URL.
ASSETS = ['theme.js', 'nav.js', 'preview.js', 'lightbox.js', 'embed-fit.js', 'highlight.js', 'outline.js', 'titlecopy.js']
ASSET_V = {a: hashlib.sha1(open(os.path.join(ROOT, a), 'rb').read()).hexdigest()[:10] for a in ASSETS}
ASSET_RE = re.compile(r'(src|href)="/(%s)(?:\?v=[0-9a-f]+)?"' % '|'.join(re.escape(a) for a in ASSETS))
html_files = [ip, os.path.join(gdir, 'index.html'), os.path.join(ROOT, '404.html'),
              os.path.join(off_dir, 'index.html')] + [q['path'] for q in posts]
HIGHLIGHT_TAG = '  <script defer src="/highlight.js"></script>\n'
OUTLINE_TAG = '  <script defer src="/outline.js"></script>\n'
TITLECOPY_TAG = '  <script defer src="/titlecopy.js"></script>\n'
for f in html_files:
    t = open(f, encoding='utf-8').read()
    # every post gets highlight.js (copy link to highlight, #hl= landing)
    if is_post_path(f) and '/highlight.js' not in t:
        t = t.replace('</body>', HIGHLIGHT_TAG + '</body>', 1)
        open(f, 'w', encoding='utf-8').write(t)
    # posts with an outline get outline.js (sidebar / bottom sheet)
    if is_post_path(f) and 'class="toc"' in t and '/outline.js' not in t:
        t = t.replace('</body>', OUTLINE_TAG + '</body>', 1)
        open(f, 'w', encoding='utf-8').write(t)
    # every post gets titlecopy.js (copy link / title / plain text from the h1)
    if is_post_path(f) and '/titlecopy.js' not in t:
        t = t.replace('</body>', TITLECOPY_TAG + '</body>', 1)
        open(f, 'w', encoding='utf-8').write(t)
    t2 = ASSET_RE.sub(lambda m: '%s="/%s?v=%s"' % (m.group(1), m.group(2), ASSET_V[m.group(2)]), t)
    if t2 != t:
        open(f, 'w', encoding='utf-8').write(t2)
    ensure_social_newtab(f)

# Service worker: precache the offline page and the shared scripts; the cache
# version changes whenever any of them (or sw.js itself) changes.
sw_path = os.path.join(ROOT, 'sw.js')
sw = open(sw_path, encoding='utf-8').read()
precache = ['/offline/', '/manifest.webmanifest', icon_src('favicon.svg')] + ['/%s?v=%s' % (a, ASSET_V[a]) for a in ASSETS]
sw = re.sub(r"const PRECACHE = \[.*?\];", lambda _: 'const PRECACHE = %s;' % json.dumps(precache), sw, count=1, flags=re.S)
sw_body = re.sub(r"const VERSION = '[^']*';", "const VERSION = '';", sw, count=1)
ver = hashlib.sha1((sw_body + open(os.path.join(off_dir, 'index.html'), encoding='utf-8').read()
                    + json.dumps(manifest)).encode('utf-8')).hexdigest()[:10]
sw = re.sub(r"const VERSION = '[^']*';", "const VERSION = '%s';" % ver, sw, count=1)
open(sw_path, 'w', encoding='utf-8').write(sw)

print(json.dumps([{**{k: q[k] for k in ('n', 'slug', 'page_title', 'desc', 'modified')},
                   'topics': [x['slug'] for x in q['topics']]} for q in posts]
                 + [{'home_desc': home_desc, 'len': len(home_desc)}], ensure_ascii=False, indent=2))
