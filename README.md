# Inkhaven 2026

Thirty days of writing for Inkhaven, **11 November to 10 December 2026**.

**Site:** [https://consciousness.ink](https://consciousness.ink/)

The site is plain static HTML. Every push to `main` deploys to Vercel.

## Published posts

- [2/30 Meditations on Synthetic Consciousness: What Could Be Hybrid about Mind Uploading?](https://consciousness.ink/2-hybrid-mind-uploading/) · [X](https://x.com/danburonline/status/2121507855979393536)
- [1/30 Meditations on Synthetic Consciousness: Causa Finalis](https://consciousness.ink/1-causa-finalis/) · [X](https://x.com/danburonline/status/2121143118062031238)
- [0/30 Meditations on Synthetic Consciousness: The Start](https://consciousness.ink/0-the-start/) · [X](https://x.com/danburonline/status/2120735544422629421)

## Adding a post

1. Create a new folder such as `1-synthetic-consciousness/` with an `index.html`. The easiest starting point is to copy `0-the-start/index.html` and replace the title, date, canonical/og URLs (`og:url`, `og:image`, `og:site_name`), and article body. Keep the `consciousness.ink` wordmark at the top.
2. Run `python3 tools/build.py` from the repo root. This rebuilds the home list, thumbnails and `posts.json`, and adds the wordmark and `og:site_name` if they are missing.
3. Add the post to the list above, with both the site URL and the X post URL.
4. Commit and push to `main`. Vercel will publish the new page at a path matching the folder name, for example `https://consciousness.ink/1-synthetic-consciousness/`.
