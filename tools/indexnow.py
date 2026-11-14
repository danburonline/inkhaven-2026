#!/usr/bin/env python3
"""Tell IndexNow (Bing, Yandex, Seznam, Naver...) about every URL in sitemap.xml.
Run after a deploy: python3 tools/indexnow.py"""
import glob, json, os, re, urllib.request
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
key = [os.path.basename(p)[:-4] for p in glob.glob(os.path.join(ROOT, '*.txt'))
       if re.fullmatch(r'[0-9a-f]{32}\.txt', os.path.basename(p))][0]
urls = re.findall(r'<loc>([^<]+)</loc>', open(os.path.join(ROOT, 'sitemap.xml')).read())
urls += ['https://consciousness.ink/llms.txt', 'https://consciousness.ink/llms-full.txt', 'https://consciousness.ink/feed.xml']
body = json.dumps({'host': 'consciousness.ink', 'key': key,
                   'keyLocation': 'https://consciousness.ink/%s.txt' % key, 'urlList': urls}).encode()
for ep in ['https://api.indexnow.org/indexnow', 'https://www.bing.com/indexnow', 'https://yandex.com/indexnow']:
    req = urllib.request.Request(ep, data=body, headers={'Content-Type': 'application/json; charset=utf-8'})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            print(ep, r.status)
    except urllib.error.HTTPError as e:
        print(ep, e.code, e.read()[:200])
