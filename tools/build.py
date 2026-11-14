#!/usr/bin/env python3
"""Rebuild the home page list, thumbnails and the post menu data.
Run from the repo root after adding or editing a post: python3 tools/build.py"""
import json, os, re, html
from bs4 import BeautifulSoup
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
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
    og = soup.find('meta', property='og:image')['content']
    img = os.path.join(ROOT, d, og.rsplit('/', 1)[1])
    # word count of the body text only
    body = BeautifulSoup(str(art), 'html.parser').find('article')
    for sel in ['h1', 'time', '.x-callout', '.tweet-embed', 'script', 'figcaption', '.num-menu-pop']:
        for el in body.select(sel):
            el.decompose()
    words = len(re.findall(r"[\w'’-]+", body.get_text(' ')))
    os.makedirs(os.path.join(ROOT, 'thumbs'), exist_ok=True)
    im = Image.open(img).convert('RGB')
    W, H = 360, 240
    s = max(W / im.width, H / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    l, tp = (im.width - W) // 2, (im.height - H) // 2
    im.crop((l, tp, l + W, tp + H)).save(os.path.join(ROOT, 'thumbs', d + '.jpg'), quality=82, optimize=True)
    num = int(m.group(1))
    short = title.split(':', 1)[1].strip() if ':' in title else title
    posts.append(dict(n=num, slug=d, title=title, short=short, date=t.get_text(strip=True),
                      iso=t['datetime'], words=words, thumb='/thumbs/%s.jpg' % d))
posts.sort(key=lambda x: -x['n'])

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

data = [{k: q[k] for k in ('n', 'slug', 'short', 'date', 'words')} for q in posts]
open(os.path.join(ROOT, 'posts.json'), 'w').write(json.dumps(data, indent=1, ensure_ascii=False))
print(json.dumps(data, ensure_ascii=False))
