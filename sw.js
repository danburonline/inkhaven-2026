/* Service worker for consciousness.ink
   - Pages (navigations): network first, so new posts and edits show up at once;
     the last good copy is used offline, then the offline page.
   - Same-origin static files (scripts, images, icons, JSON): stale-while-revalidate.
   - Everything else (other origins such as X embeds, non-GET, video ranges,
     feeds and text files) is not touched and goes straight to the network.
   VERSION and PRECACHE are filled in by tools/build.py. */
const VERSION = 'e000a38ee2';
const PRECACHE = ["/offline/", "/manifest.webmanifest", "/favicon.svg", "/theme.js?v=ee08ac4ef8", "/nav.js?v=8027db20fc", "/preview.js?v=4da7c2a5b2", "/lightbox.js?v=fb94a747e9", "/embed-fit.js?v=f9df00aeb9"];
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
  if (ASSET_RE.test(url.pathname)) event.respondWith(asset(event));
});
