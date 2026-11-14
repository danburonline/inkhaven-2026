#!/usr/bin/env python3
"""Rebuild the home page list, thumbnails, share images, SEO tags, sitemap and feed.
Run from the repo root after adding or editing a post: python3 tools/build.py"""
import html, json, os, re
from datetime import datetime, timezone, timedelta
from xml.sax.saxutils import escape as xml_esc
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = 'consciousness.ink'
SITE_URL = 'https://%s' % SITE
SITE_TITLE = 'Meditations on Synthetic Consciousness and Hybrid Mind Uploading'
AUTHOR = 'Daniel Burger'
AUTHOR_X = 'https://x.com/danburonline'
PT = timezone(timedelta(hours=-8))
OG_W, OG_H = 1200, 630
OG_SITE = '  <meta property="og:site_name" content="%s">\n' % SITE
MASTHEAD = '    <p class="masthead"><a href="/">%s</a></p>\n' % SITE
THEME_HEAD = '''  <meta name="color-scheme" content="light dark">
  <script>(function(){try{var t=localStorage.getItem('theme');if(t==='light'||t==='dark')document.documentElement.setAttribute('data-theme',t)}catch(e){}})()</script>
  <link rel="stylesheet" href="/styles.css">'''
FEED_LINK = '  <link rel="alternate" type="application/rss+xml" title="%s" href="%s/feed.xml">' % (
    html.escape(SITE_TITLE), SITE_URL)
SERIF = '/usr/share/fonts/truetype/sand-box/custom/Source Serif Pro/SourceSerifPro-Regular.ttf'
SERIF_SB = '/usr/share/fonts/truetype/sand-box/custom/Source Serif Pro/SourceSerifPro-Semibold.ttf'

def ensure_chrome(path):
    """Add the wordmark and og:site_name so new posts copied from an older
    template still get them after a build."""
    s = open(path, encoding='utf-8').read()
    changed = False
    if 'property="og:site_name"' not in s and "property='og:site_name'" not in s:
        if re.search(r'<meta property="og:url"[^>]*>\n', s):
            s = re.sub(r'(<meta property="og:url"[^>]*>\n)', r'\1' + OG_SITE, s, count=1)
        else:
            s = s.replace('</head>', OG_SITE + '</head>', 1)
        changed = True
    if 'class="masthead"' not in s:
        s = re.sub(r'(<div class="wrap">\n)', r'\1' + MASTHEAD, s, count=1)
        changed = True
    if changed:
        open(path, 'w', encoding='utf-8').write(s)

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
    for sel in ['h1', 'time', '.x-callout', '.tweet-embed', 'script', 'figcaption', '.num-menu-pop']:
        for el in body.select(sel):
            el.decompose()
    for p in body.find_all('p'):
        t = p.get_text(' ', strip=True)
        if t:
            return t
    return body.get_text(' ', strip=True)

def cover_og(src, dest):
    im = Image.open(src).convert('RGB')
    s = max(OG_W / im.width, OG_H / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    l, t = (im.width - OG_W) // 2, (im.height - OG_H) // 2
    im.crop((l, t, l + OG_W, t + OG_H)).save(
        dest, 'JPEG', quality=88, optimize=True, progressive=True)

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

def make_home_og(dest):
    im = Image.new('RGB', (OG_W, OG_H), '#f6f1e8')
    dr = ImageDraw.Draw(im)
    word = ImageFont.truetype(SERIF, 54)
    sub = ImageFont.truetype(SERIF, 28)
    by = ImageFont.truetype(SERIF, 22)
    max_w = 920
    title_lines = wrap_text(dr, SITE_TITLE, sub, max_w)
    gap1, gap2 = 28, 22
    h_word = word.getbbox(SITE)[3] - word.getbbox(SITE)[1]
    h_sub = sum(sub.getbbox(line)[3] - sub.getbbox(line)[1] + 8 for line in title_lines)
    h_by = by.getbbox(AUTHOR)[3] - by.getbbox(AUTHOR)[1]
    block = h_word + gap1 + h_sub + gap2 + h_by
    y = (OG_H - block) // 2
    x = (OG_W - dr.textlength(SITE, font=word)) / 2
    dr.text((x, y), SITE, font=word, fill='#1c1916')
    y += h_word + gap1
    for line in title_lines:
        x = (OG_W - dr.textlength(line, font=sub)) / 2
        dr.text((x, y), line, font=sub, fill='#5e574e')
        y += sub.getbbox(line)[3] - sub.getbbox(line)[1] + 8
    y += gap2 - 8
    x = (OG_W - dr.textlength(AUTHOR, font=by)) / 2
    dr.text((x, y), AUTHOR, font=by, fill='#5e574e')
    os.makedirs(os.path.dirname(dest) or '.', exist_ok=True)
    im.save(dest, 'JPEG', quality=90, optimize=True, progressive=True)

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

posts = []
for d in sorted(os.listdir(ROOT)):
    m = re.match(r'^(\d+)-', d)
    p = os.path.join(ROOT, d, 'index.html')
    if not m or not os.path.exists(p):
        continue
    soup = BeautifulSoup(open(p, encoding='utf-8').read(), 'html.parser')
    art = soup.find('article')
    h1 = art.find('h1')
    title = h1.get_text(' ', strip=True)
    title = re.sub(r'\s+', ' ', title).replace(' /', '/').strip()
    t = art.find('time')
    num = int(m.group(1))
    short = title.split(':', 1)[1].strip() if ':' in title else title
    page_title = '%s/30 %s · Meditations on Synthetic Consciousness' % (num, short)
    desc = excerpt(first_para(art))
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
    og_file = os.path.join(ROOT, d, 'og.jpg')
    cover_og(src_path, og_file)
    body = BeautifulSoup(str(art), 'html.parser').find('article')
    for sel in ['h1', 'time', '.x-callout', '.tweet-embed', 'script', 'figcaption', '.num-menu-pop']:
        for el in body.select(sel):
            el.decompose()
    words = len(re.findall(r"[\w'’-]+", body.get_text(' ')))
    url = '%s/%s/' % (SITE_URL, d)
    og_url = '%s/%s/og.jpg' % (SITE_URL, d)
    video_src = None
    if video and video.get('src'):
        video_src = SITE_URL + video['src']
        vw = video.get('width') or '1280'
        vh = video.get('height') or '720'
    posts.append(dict(
        n=num, slug=d, title=title, short=short, page_title=page_title,
        date=t.get_text(strip=True), iso=t['datetime'], words=words,
        thumb='/thumbs/%s.jpg' % d, desc=desc, alt=alt, url=url, og=og_url,
        video=video_src, vw=video.get('width') if video else None,
        vh=video.get('height') if video else None,
        path=p))

posts.sort(key=lambda x: -x['n'])

for q in posts:
    graph = {
        '@context': 'https://schema.org',
        '@type': 'BlogPosting',
        'headline': q['page_title'],
        'name': q['title'],
        'description': q['desc'],
        'datePublished': q['iso'],
        'author': {'@type': 'Person', 'name': AUTHOR, 'url': AUTHOR_X},
        'image': {'@type': 'ImageObject', 'url': q['og'], 'width': OG_W, 'height': OG_H},
        'url': q['url'],
        'mainEntityOfPage': {'@type': 'WebPage', '@id': q['url']},
        'isPartOf': {'@type': 'Blog', 'name': SITE_TITLE, 'url': SITE_URL + '/'},
        'publisher': {'@type': 'Person', 'name': AUTHOR, 'url': AUTHOR_X},
    }
    lines = [
        '  <meta charset="utf-8">',
        '  <meta name="viewport" content="width=device-width, initial-scale=1">',
        '  <title>%s</title>' % html.escape(q['page_title']),
        '  <meta name="description" content="%s">' % html.escape(q['desc']),
        '  <meta name="author" content="%s">' % AUTHOR,
        '  <link rel="canonical" href="%s">' % q['url'],
        FEED_LINK,
        '  <meta property="og:type" content="article">',
        '  <meta property="og:title" content="%s">' % html.escape(q['page_title']),
        '  <meta property="og:description" content="%s">' % html.escape(q['desc']),
        '  <meta property="og:url" content="%s">' % q['url'],
        '  <meta property="og:site_name" content="%s">' % SITE,
        '  <meta property="og:image" content="%s">' % q['og'],
        '  <meta property="og:image:width" content="%s">' % OG_W,
        '  <meta property="og:image:height" content="%s">' % OG_H,
        '  <meta property="og:image:alt" content="%s">' % html.escape(q['alt']),
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
        '  <meta property="article:author" content="%s">' % AUTHOR,
        '  <meta name="twitter:card" content="summary_large_image">',
        '  <meta name="twitter:creator" content="@danburonline">',
        '  <meta name="twitter:title" content="%s">' % html.escape(q['page_title']),
        '  <meta name="twitter:description" content="%s">' % html.escape(q['desc']),
        '  <meta name="twitter:image" content="%s">' % q['og'],
        ld(graph),
        THEME_HEAD,
    ]
    set_head(q['path'], lines)

items = []
for q in posts:
    items.append(f'''        <li data-n="{q['n']}" data-words="{q['words']}" data-search="{html.escape((q['title'] + ' ' + q['date']).lower())}">
          <a class="thumb" href="/{q['slug']}/" tabindex="-1" aria-hidden="true"><img src="{q['thumb']}" width="180" height="120" alt="" loading="lazy"></a>
          <div class="post-info">
            <a class="title" href="/{q['slug']}/">{html.escape(q['title'])}</a>
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
open(ip, 'w', encoding='utf-8').write(s)

soup = BeautifulSoup(open(ip, encoding='utf-8').read(), 'html.parser')
about = soup.select_one('.about')
intro = soup.select_one('.intro')
home_src = ' '.join(t.get_text(' ', strip=True) for t in [about, intro] if t)
home_desc = excerpt(home_src, 155)
home_og = os.path.join(ROOT, 'og.jpg')
make_home_og(home_og)
home_og_url = SITE_URL + '/og.jpg'
home_ld = {
    '@context': 'https://schema.org',
    '@graph': [
        {
            '@type': 'WebSite',
            'name': SITE,
            'url': SITE_URL + '/',
            'description': home_desc,
            'inLanguage': 'en',
            'publisher': {'@type': 'Person', 'name': AUTHOR, 'url': AUTHOR_X},
        },
        {
            '@type': 'Blog',
            'name': SITE_TITLE,
            'url': SITE_URL + '/',
            'description': home_desc,
            'author': {'@type': 'Person', 'name': AUTHOR, 'url': AUTHOR_X},
        },
    ],
}
home_title = SITE_TITLE + ' · ' + AUTHOR
set_head(ip, [
    '  <meta charset="utf-8">',
    '  <meta name="viewport" content="width=device-width, initial-scale=1">',
    '  <title>%s</title>' % html.escape(home_title),
    '  <meta name="description" content="%s">' % html.escape(home_desc),
    '  <meta name="author" content="%s">' % AUTHOR,
    '  <link rel="canonical" href="%s/">' % SITE_URL,
    FEED_LINK,
    '  <meta property="og:type" content="website">',
    '  <meta property="og:title" content="%s">' % html.escape(home_title),
    '  <meta property="og:description" content="%s">' % html.escape(home_desc),
    '  <meta property="og:url" content="%s/">' % SITE_URL,
    '  <meta property="og:site_name" content="%s">' % SITE,
    '  <meta property="og:image" content="%s">' % home_og_url,
    '  <meta property="og:image:width" content="%s">' % OG_W,
    '  <meta property="og:image:height" content="%s">' % OG_H,
    '  <meta property="og:image:alt" content="%s">' % html.escape(SITE_TITLE),
    '  <meta name="twitter:card" content="summary_large_image">',
    '  <meta name="twitter:creator" content="@danburonline">',
    '  <meta name="twitter:title" content="%s">' % html.escape(home_title),
    '  <meta name="twitter:description" content="%s">' % html.escape(home_desc),
    '  <meta name="twitter:image" content="%s">' % home_og_url,
    ld(home_ld),
    THEME_HEAD,
])

for q in posts:
    ensure_chrome(q['path'])
ensure_chrome(ip)

# sitemap, robots, feed
urls = [SITE_URL + '/'] + [q['url'] for q in posts]
smap = ['<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
smap.append('  <url><loc>%s/</loc><changefreq>daily</changefreq></url>' % SITE_URL)
for q in posts:
    smap.append('  <url><loc>%s</loc><lastmod>%s</lastmod></url>' % (xml_esc(q['url']), q['iso']))
smap.append('</urlset>\n')
open(os.path.join(ROOT, 'sitemap.xml'), 'w', encoding='utf-8').write('\n'.join(smap))
open(os.path.join(ROOT, 'robots.txt'), 'w', encoding='utf-8').write(
    'User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n' % SITE_URL)

feed = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:dc="http://purl.org/dc/elements/1.1/">',
    '  <channel>',
    '    <title>%s</title>' % xml_esc(SITE_TITLE),
    '    <link>%s/</link>' % SITE_URL,
    '    <description>%s</description>' % xml_esc(home_desc),
    '    <language>en</language>',
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
        '      <description>%s</description>' % xml_esc(q['desc']),
        '    </item>',
    ]
feed += ['  </channel>', '</rss>', '']
open(os.path.join(ROOT, 'feed.xml'), 'w', encoding='utf-8').write('\n'.join(feed))

data = [{k: q[k] for k in ('n', 'slug', 'short', 'date', 'words')} for q in posts]
open(os.path.join(ROOT, 'posts.json'), 'w').write(json.dumps(data, indent=1, ensure_ascii=False))
print(json.dumps([{**{k: q[k] for k in ('n', 'slug', 'page_title', 'desc')}, 'og_bytes': os.path.getsize(os.path.join(ROOT, q['slug'], 'og.jpg'))} for q in posts] + [{'home_desc': home_desc, 'home_og_bytes': os.path.getsize(home_og)}], ensure_ascii=False, indent=2))
