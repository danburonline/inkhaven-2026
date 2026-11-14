/* Theme toggle: Auto (follows system) -> Light -> Dark. Also themes X embeds
   and loads widgets.js itself so embeds render in the right theme. */
(function () {
  var root = document.documentElement;
  var mq = window.matchMedia ? matchMedia('(prefers-color-scheme: dark)') : null;
  var ORDER = ['auto', 'light', 'dark'];
  var LABEL = { auto: 'Auto', light: 'Light', dark: 'Dark' };
  var ICON = {
    auto: '<svg width="14" height="14" viewBox="0 0 16 16" aria-hidden="true"><circle cx="8" cy="8" r="6.25" fill="none" stroke="currentColor" stroke-width="1.5"/><path d="M8 1.75a6.25 6.25 0 0 1 0 12.5z" fill="currentColor"/></svg>',
    light: '<svg width="14" height="14" viewBox="0 0 16 16" aria-hidden="true"><circle cx="8" cy="8" r="3" fill="currentColor"/><g stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><path d="M8 1v1.6M8 13.4V15M1 8h1.6M13.4 8H15M3.05 3.05l1.13 1.13M11.82 11.82l1.13 1.13M3.05 12.95l1.13-1.13M11.82 4.18l1.13-1.13"/></g></svg>',
    dark: '<svg width="14" height="14" viewBox="0 0 16 16" aria-hidden="true"><path d="M13.5 10.2A6 6 0 0 1 5.8 2.5a6 6 0 1 0 7.7 7.7z" fill="currentColor"/></svg>'
  };
  function getMode() { try { var m = localStorage.getItem('theme'); return m === 'light' || m === 'dark' ? m : 'auto'; } catch (e) { return 'auto'; } }
  function effective(mode) { return mode === 'auto' ? (mq && mq.matches ? 'dark' : 'light') : mode; }

  // X embeds: keep pristine copies so they can be re-rendered on theme change
  var embeds = [];
  document.querySelectorAll('.tweet-embed').forEach(function (wrap) {
    var bq = wrap.querySelector('blockquote.twitter-tweet');
    if (bq) { embeds.push({ wrap: wrap, html: bq.outerHTML }); reserve(wrap); wrap.classList.add('loading'); }
  });
  // Reserve roughly the final embed height so the page doesn't jump.
  // data-h="w1:h1,w2:h2,..." are measured card heights at given widths.
  function estimate(wrap) {
    var pts = (wrap.getAttribute('data-h') || '').split(',').map(function (x) { return x.split(':').map(Number); })
      .filter(function (x) { return x[0] && x[1]; }).sort(function (a, b) { return a[0] - b[0]; });
    if (!pts.length) return 0;
    var w = wrap.clientWidth, base = pts[pts.length - 1];
    if (w >= base[0]) return base[1] * (w > 550 ? w / 550 : 1) + 20;
    for (var i = pts.length - 1; i > 0; i--) {
      var a = pts[i - 1], b = pts[i];
      if (w >= a[0]) return a[1] + (b[1] - a[1]) * (w - a[0]) / (b[0] - a[0]) + 20;
    }
    return pts[0][1] + 20;
  }
  function reserve(wrap) { var h = estimate(wrap); if (h) wrap.style.minHeight = Math.round(h) + 'px'; }
  function settle() {
    embeds.forEach(function (e) {
      if (e.wrap.querySelector('.twitter-tweet-rendered iframe')) {
        e.wrap.classList.remove('loading');
        // let the iframe size itself before dropping the reservation
        setTimeout(function () { if (!e.wrap.classList.contains('loading')) e.wrap.style.minHeight = ''; }, 600);
      }
    });
  }
  var bindTries = 0;
  (function bind() {
    if (window.twttr && twttr.events && twttr.events.bind) { twttr.events.bind('rendered', settle); return; }
    if (++bindTries < 80) setTimeout(bind, 250);
  })();
  var embedTheme = null;
  function themeEmbeds(t) {
    if (t === embedTheme) return;
    var first = embedTheme === null; embedTheme = t;
    embeds.forEach(function (e) {
      if (!first) { e.wrap.innerHTML = e.html; e.wrap.classList.remove('fit'); e.wrap.style.height = ''; e.wrap.classList.add('loading'); reserve(e.wrap); }
      var bq = e.wrap.querySelector('blockquote.twitter-tweet');
      if (bq) bq.setAttribute('data-theme', t);
      if (!first && window.twttr && twttr.widgets) twttr.widgets.load(e.wrap);
    });
  }

  var btn;
  function apply(mode) {
    if (mode === 'auto') root.removeAttribute('data-theme'); else root.setAttribute('data-theme', mode);
    var t = effective(mode);
    themeEmbeds(t);
    if (btn) {
      btn.innerHTML = ICON[mode] + '<span>' + LABEL[mode] + '</span>';
      btn.setAttribute('aria-label', 'Theme: ' + LABEL[mode] + (mode === 'auto' ? ' (' + t + ')' : '') + '. Click to change.');
      btn.title = mode === 'auto' ? 'Following system (' + t + ')' : LABEL[mode] + ' theme';
    }
  }

  btn = document.createElement('button');
  btn.type = 'button';
  btn.className = 'theme-toggle';
  var host = document.querySelector('.site-links') || document.querySelector('.back');
  if (host) host.appendChild(btn);
  btn.addEventListener('click', function () {
    var next = ORDER[(ORDER.indexOf(getMode()) + 1) % ORDER.length];
    try { if (next === 'auto') localStorage.removeItem('theme'); else localStorage.setItem('theme', next); } catch (e) {}
    apply(next);
  });
  if (mq) {
    var onSys = function () { if (getMode() === 'auto') apply('auto'); };
    if (mq.addEventListener) mq.addEventListener('change', onSys); else if (mq.addListener) mq.addListener(onSys);
  }
  apply(getMode());

  // Load widgets.js with retries: X's script and embed backend fail now and
  // then (slow mobile networks, timeouts), which leaves the bare fallback link.
  function pending() {
    return embeds.filter(function (e) { return !e.wrap.querySelector('.twitter-tweet-rendered'); });
  }
  var scriptTries = 0, renderTries = 0;
  function loadScript() {
    var s = document.createElement('script');
    s.async = true; s.charset = 'utf-8';
    s.src = 'https://platform.twitter.com/widgets.js' + (scriptTries ? '?r=' + scriptTries : '');
    s.onerror = function () {
      s.remove();
      if (++scriptTries < 4) setTimeout(loadScript, 1500 * scriptTries);
      else embeds.forEach(function (e) { e.wrap.classList.remove('loading'); e.wrap.classList.add('failed'); e.wrap.style.minHeight = ''; });
    };
    document.body.appendChild(s);
  }
  function check() {
    var p = pending();
    if (!p.length) return;
    if (renderTries >= 4) { p.forEach(function (e) { e.wrap.classList.remove('loading'); e.wrap.classList.add('failed'); e.wrap.style.minHeight = ''; }); return; }
    if (window.twttr && twttr.widgets) {
      renderTries++;
      p.forEach(function (e) {
        // reset a half-rendered or failed embed to its original markup, then retry
        if (!e.wrap.querySelector('blockquote.twitter-tweet') || e.wrap.querySelector('iframe')) {
          e.wrap.innerHTML = e.html;
          var bq = e.wrap.querySelector('blockquote.twitter-tweet');
          if (bq) bq.setAttribute('data-theme', embedTheme);
        }
        twttr.widgets.load(e.wrap);
      });
    }
    setTimeout(check, 4000);
  }
  if (embeds.length) { loadScript(); setTimeout(check, 6000); }
})();
