/* Service worker for consciousness.ink
   - Pages (navigations): network first, so new posts and edits show up at once;
     the last good copy is used offline, then the offline page.
   - Data files (/previews.json, /posts.json): network first, cache as offline
     fallback, so new link previews and posts are never hidden by an old copy.
   - Same-origin static files (scripts, images, icons): stale-while-revalidate.
   - Everything else (other origins such as X embeds, non-GET, video ranges,
     feeds and text files) is not touched and goes straight to the network.
   VERSION and PRECACHE are filled in by tools/build.py. */
const VERSION = 'ce9c0c90f8';
const PRECACHE = ["/offline/", "/manifest.webmanifest", "/favicon.svg?v=bd556e1b70", "/theme.js?v=96807dd5d4", "/nav.js?v=1240c94384", "/preview.js?v=b76e1c5909", "/lightbox.js?v=d9b0f1adcc", "/embed-fit.js?v=d979f65494", "/highlight.js?v=2c738ccc8e", "/outline.js?v=0471b63513", "/titlecopy.js?v=d8c4a61497"];
const PREFIX = 'ci-';
const STATIC = PREFIX + 'static-' + VERSION;
const PAGES = PREFIX + 'pages-' + VERSION;
const ASSETS = PREFIX + 'assets-' + VERSION;
const MAX_ASSETS = 120;
const MAX_PAGES = 60;
const ASSET_RE = /\.(?:js|css|png|jpe?g|webp|avif|gif|svg|ico|json|webmanifest)$/i;

self.addEventListener('install', (event) => {
  event.waitUntil(caches.open(STATIC).then((c) => c.addAll(PRECACHE)).then(() => self.skipWaiting()));
});

self.addEventListener('activate', (event) => {
  event.waitUntil((async () => {
    const keep = [STATIC, PAGES, ASSETS];
    for (const key of await caches.keys()) {
      if (key.startsWith(PREFIX) && !keep.includes(key)) await caches.delete(key);
    }
    if (self.registration.navigationPreload) await self.registration.navigationPreload.enable();
    await self.clients.claim();
  })());
});

async function trim(name, max) {
  const cache = await caches.open(name);
  const keys = await cache.keys();
  for (let i = 0; i < keys.length - max; i++) await cache.delete(keys[i]);
}

// Only plain, successful, same-origin responses are stored. Redirects (old
// host, missing trailing slash) are passed through to the browser untouched.
function storable(res) {
  return res && res.ok && res.status === 200 && res.type === 'basic' && !res.redirected;
}

async function page(event) {
  const req = event.request;
  try {
    const res = (await event.preloadResponse) || (await fetch(req));
    if (storable(res)) {
      const copy = res.clone();
      event.waitUntil(caches.open(PAGES).then((c) => c.put(req, copy)).then(() => trim(PAGES, MAX_PAGES)));
    }
    return res;
  } catch (err) {
    const url = new URL(req.url);
    const hit = (await caches.match(req, { ignoreSearch: true }))
      || (!url.pathname.endsWith('/') && (await caches.match(url.pathname + '/')))
      || (await caches.match('/offline/'));
    return hit || Response.error();
  }
}

async function asset(event) {
  const req = event.request;
  const hit = await caches.match(req);
  const net = fetch(req).then((res) => {
    if (storable(res)) {
      const copy = res.clone();
      event.waitUntil(caches.open(ASSETS).then((c) => c.put(req, copy)).then(() => trim(ASSETS, MAX_ASSETS)));
    }
    return res;
  });
  if (hit) {
    event.waitUntil(net.catch(() => {}));
    return hit;
  }
  return net.catch(() => Response.error());
}

async function data(event) {
  const req = event.request;
  try {
    const res = await fetch(req);
    if (storable(res)) {
      const copy = res.clone();
      event.waitUntil(caches.open(ASSETS).then((c) => c.put(req, copy)).then(() => trim(ASSETS, MAX_ASSETS)));
    }
    return res;
  } catch (err) {
    return (await caches.match(req, { ignoreSearch: true })) || Response.error();
  }
}

self.addEventListener('fetch', (event) => {
  const req = event.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);
  if (url.origin !== self.location.origin) return;
  if (req.headers.has('range') || url.pathname === '/sw.js') return;
  if (req.mode === 'navigate') {
    event.respondWith(page(event));
    return;
  }
  if (url.pathname === '/previews.json' || url.pathname === '/posts.json') {
    event.respondWith(data(event));
    return;
  }
  if (ASSET_RE.test(url.pathname)) event.respondWith(asset(event));
});
