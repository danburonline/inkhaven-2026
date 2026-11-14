# Inkhaven 2026

Thirty days of writing for Inkhaven, **11 November to 10 December 2026**.

**Site:** [https://consciousness.ink](https://consciousness.ink/)

The site is plain static HTML. Every push to `main` deploys to Vercel. There is also an [RSS feed](https://consciousness.ink/feed.xml).

## Published posts

- [2/30 Meditations on Synthetic Consciousness: What Could Be Hybrid about Mind Uploading?](https://consciousness.ink/2-hybrid-mind-uploading/) · [X](https://x.com/danburonline/status/2121507855979393536)
- [1/30 Meditations on Synthetic Consciousness: Causa Finalis](https://consciousness.ink/1-causa-finalis/) · [X](https://x.com/danburonline/status/2121143118062031238)
- [0/30 Meditations on Synthetic Consciousness: The Start](https://consciousness.ink/0-the-start/) · [X](https://x.com/danburonline/status/2120735544422629421)

## Adding a post

1. Create a new folder such as `1-synthetic-consciousness/` with an `index.html`. The easiest starting point is to copy `0-the-start/index.html` and replace the heading, date and article body. Keep the `consciousness.ink` wordmark at the top.
2. Run `python3 tools/build.py` from the repo root. This rebuilds the home list, thumbnails, 1200×630 share images, sitemap, `robots.txt`, RSS feed (full text), `llms.txt`, `llms-full.txt`, the glossary page, the 404 page and SEO tags (title, description, keywords, Open Graph, Twitter and JSON-LD), adds the wordmark if it is missing, and adds a Topics line under the post for every glossary term the post actually uses.
   - Optional: give the post a hand-written description in `tools/meta.json`; otherwise the opening of the post is used.
   - `tools/modified.json` records when each post's text last changed (used for `dateModified` and the sitemap).
3. Add the post to the list above, with both the site URL and the X post URL.
4. Commit and push to `main`. Vercel will publish the new page at a path matching the folder name, for example `https://consciousness.ink/1-synthetic-consciousness/`.

## Search and AI discoverability

- **Glossary:** terms live in `tools/glossary.py` (definition, spellings, the regex that detects the term in a post, and Wikipedia/Wikidata links where a matching article exists). Edit definitions there, then run the build. The page is at [/glossary/](https://consciousness.ink/glossary/).
- **Structured data:** every page carries JSON-LD with one `Person` (`https://consciousness.ink/#daniel-burger`), the `WebSite`, the `Blog`, each `BlogPosting` and the `DefinedTerm`s it is about.
- **Identity links:** only stable profile URLs, no bio facts: `https://danielburger.online/`, `https://x.com/danburonline`, `https://github.com/danburonline` (also as `rel="me"` links).
- **For AI tools:** [`/llms.txt`](https://consciousness.ink/llms.txt) and [`/llms-full.txt`](https://consciousness.ink/llms-full.txt). `robots.txt` explicitly allows search and AI crawlers.
- **IndexNow:** the key file is the 32-character `.txt` file in the repo root. After publishing, ping it with:

  ```
  python3 tools/indexnow.py
  ```
