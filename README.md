# Inkhaven 2026

Thirty days of writing for Inkhaven, **11 November to 10 December 2026**.

**Site:** [https://consciousness.ink](https://consciousness.ink/)

The site is plain static HTML. Every push to `main` deploys to Vercel. There is also an [RSS feed](https://consciousness.ink/feed.xml).

## Published posts

- [7/30 Meditations on Synthetic Consciousness: Augmented Cognition Needs a Baseline First](https://consciousness.ink/7-augmented-cognition/) · [X](https://x.com/danburonline/status/2123299553327849974)
- [8/30 Meditations on Synthetic Consciousness: Who Says Individuality Will Stay Forever?](https://consciousness.ink/8-collective-mind/) · [X](https://x.com/danburonline/status/2123682201342759353)
- [9/30 Meditations on Synthetic Consciousness: Weak and Strong Multiple Realisability](https://consciousness.ink/9-multiple-realisability/) · [X](https://x.com/danburonline/status/2124042530153222418)
- [10/30 Meditations on Synthetic Consciousness: I Care Deeply about the Continuity of the Human Brain](https://consciousness.ink/10-continuer-migration/) · [X](https://x.com/danburonline/status/2124388849220775977)
- [11/30 Meditations on Synthetic Consciousness: Does My NCC Look Big in This Substrate?](https://consciousness.ink/11-morphological-independence/) · [X](https://x.com/danburonline/status/2124748091480039921)
- [12/30 Meditations on Synthetic Consciousness: Distributed, yet Unified](https://consciousness.ink/12-distributed-unification/) · [X](https://x.com/danburonline/status/2125438683243573702)
- [13/30 Meditations on Synthetic Consciousness: Are You Just Your Brain?](https://consciousness.ink/13-brain-centredness/) · [X](https://x.com/danburonline/status/2125472977949192375)
- [14/30 Meditations on Synthetic Consciousness: My Electrode Is a Functionalist](https://consciousness.ink/14-methodological-physicalism/) · [X](https://x.com/danburonline/status/2125826626118422701)
- [15/30 Meditations on Synthetic Consciousness: No Bird Ever Broke the Sound Barrier](https://consciousness.ink/15-non-organicism/) · [X](https://x.com/danburonline/status/2126204047166513391)
- [6/30 Meditations on Synthetic Consciousness: Computational Vs. Physical Substrate Independence](https://consciousness.ink/6-substrate-independence/) · [X](https://x.com/danburonline/status/2122956433914478644)
- [5/30 Meditations on Synthetic Consciousness: Transcending Biology, but not Physics](https://consciousness.ink/5-transcending-biology/) · [X](https://x.com/danburonline/status/2122573865079709758)
- [4/30 Meditations on Synthetic Consciousness: Measurements, Models and Theories](https://consciousness.ink/4-measurements-models-theories/) · [X](https://x.com/danburonline/status/2122235784644477415)
- [3/30 Meditations on Synthetic Consciousness: Solving Death](https://consciousness.ink/3-solving-death/) · [X](https://x.com/danburonline/status/2121890643983151389)
- [2/30 Meditations on Synthetic Consciousness: What Could Be Hybrid about Mind Uploading?](https://consciousness.ink/2-hybrid-mind-uploading/) · [X](https://x.com/danburonline/status/2121507855979393536)
- [1/30 Meditations on Synthetic Consciousness: Causa Finalis](https://consciousness.ink/1-causa-finalis/) · [X](https://x.com/danburonline/status/2121143118062031238)
- [0/30 Meditations on Synthetic Consciousness: The Start](https://consciousness.ink/0-the-start/) · [X](https://x.com/danburonline/status/2120735544422629421)

## Adding a post

1. Create a new folder such as `1-synthetic-consciousness/` with an `index.html`. The easiest starting point is to copy `0-the-start/index.html` and replace the heading, date and article body. Keep the `consciousness.ink` wordmark at the top.
2. Run `python3 tools/build.py` from the repo root (needs Python with Pillow and BeautifulSoup). This rebuilds the home list, thumbnails, 1200×630 share images, sitemap, `robots.txt`, RSS feed (full text), `llms.txt`, `llms-full.txt`, the glossary page, the 404 page and SEO tags (title, description, keywords, Open Graph, Twitter and JSON-LD), adds the wordmark if it is missing, and adds a Topics line under the post for every glossary term the post actually uses.
   - It also makes responsive AVIF and WebP copies of every image in the post (see "Performance" below), wraps the post in `<main>`, and versions the script URLs.
   - Optional: give the post a hand-written description in `tools/meta.json`; otherwise the opening of the post is used.
   - `tools/modified.json` records when each post's text last changed (used for `dateModified` and the sitemap).
   - Before building, add the post's section outline to `tools/outline.json` (see "Section outline" below). The build prints a warning for any post without one.
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

## Performance

Lighthouse target: 100 in Performance, Accessibility, Best Practices and SEO, on mobile and desktop.

- **Images:** for every local image in a post, the build writes AVIF and WebP copies at 480, 720, 960, 1280 and 1920 px wide into `<post>/img/` (file names carry a content hash) and wraps the `<img>` in a `<picture>` with `srcset` and `sizes`. The original JPG/PNG stays as the fallback and as the source for thumbnails. Share images are typographic 1200×630 title cards (dark palette, hashed filenames such as `og-<hash>.jpg`) generated at build time for the home page, each post and the glossary. The first image above the text is loaded with `fetchpriority="high"` and preloaded from `<head>`; later images use `loading="lazy"`. The lightbox opens the largest WebP (`data-full`) and supports zoom (wheel or ctrl+wheel around the cursor, click or double-tap to toggle 2.5x, pinch, drag to pan, +/-/0 keys; 1x to 5x, pan clamped to the edges); on the first zoom it swaps in the original JPG/PNG so charts stay sharp. Put new images in the post folder and reference them with a plain `<img src="/<post>/<file>.jpg" width=".." height=".." alt="..">`; the build does the rest.
- **CSS:** `styles.css` is the source, but the build inlines a minified copy into every page so the first paint needs no extra request. After editing `styles.css`, run the build.
- **Scripts:** pages load `/theme.js?v=<hash>` and so on; the hash changes when the file does, so `vercel.json` can cache them for a year.
- **Caching (`vercel.json`):** `<post>/img/*`, hashed share images (`og-<hash>.jpg`), versioned scripts and versioned icons (`?v=<hash>`) are cached for a year (`immutable`); other images, icons and video for a week; `previews.json`/`posts.json` for an hour; HTML and `sw.js` are always revalidated.
- **Links to highlights:** `highlight.js` (on every post; the build adds the script tag if a post lacks it) shows a "Copy link to highlight" button when text in the post is selected. The link is the page URL plus `#hl=<anchors>` and a standard `:~:text=<anchors>` fragment; on load the script marks the passage (`mark.hl`, also across paragraphs) and scrolls it into view. If the text has changed since, the page just loads normally.
- **Section outline:** the posts have no headings, so `tools/outline.json` holds a short outline per post, keyed by folder name: 3 to 7 sections, each with a `label` (2 to 6 words that summarise that stretch in the post's own terms, no added claims) `id` (a unique `sec-...` anchor, keep it unchanged once published), and `starts` (the first few words of the paragraph where the section begins). For every new post, add its entry before building. The build gives those paragraphs stable ids from the outline, renders `<nav class="toc" aria-label="Sections">` before the article (the text itself is unchanged), adds `/outline.js` and warns if an entry is missing or a `starts` text no longer matches. On screens 1220 px and wider the outline sits in the left margin and marks the section being read; on narrower screens a small pill at the bottom (hidden while scrolling down or selecting text) opens it as a bottom sheet. Clicking a section scrolls there and sets `#sec-...` in the URL.
- **X embeds:** `theme.js` only loads X's `widgets.js` when an embed comes within about two screens of the viewport. Until then the skeleton (sized from `data-h`) holds the space, so nothing jumps.

## Offline and installable (PWA)

- `manifest.webmanifest` (generated by the build) with `icon-192.png`, `icon-512.png` and a maskable `icon-maskable-512.png` (the mark sits in the 80% safe zone). `tools/make_icons.py` draws every icon from the Source Serif semibold "c" outlines: it writes a path-based `favicon.svg`, a 32×32 PNG fallback, a 16/32/48 `favicon.ico`, an 180×180 `apple-touch-icon.png`, and the manifest PNGs, each rasterised at 8× and downsampled. Pages and the manifest reference them with `?v=<hash>`. Rerun the script, then the site build, if the design changes.
- `sw.js` is registered quietly by `theme.js` (no install prompts or banners). Pages are network first, so new posts and edits appear immediately, and the last copy is used offline. Same-origin scripts, images, icons and JSON are stale-while-revalidate. Other origins (X embeds), non-GET requests, video range requests, feeds and text files are never touched, and redirects are passed straight through and never cached.
- Pages you have not opened yet show `/offline/` when there is no connection.
- The build fills in the service worker's `VERSION` and `PRECACHE` list; old caches are deleted when a new version activates.
