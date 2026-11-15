/* X embeds: widgets.js renders the card at most 550px wide, so it is scaled up
   to the full text column width. The card stays invisible behind the skeleton
   until it has loaded and has its final size, then fades in, so it never shows
   at a smaller width or in a different position. */
(function () {
  var BASE = 550;
  function rendered(wrap) { return wrap.querySelector('.twitter-tweet-rendered'); }
  function frame(el) { return el.tagName === 'IFRAME' ? el : el.querySelector('iframe'); }
  // only write when a value changes, so the MutationObserver doesn't loop
  function set(o, k, v) { if (o.style[k] !== v) o.style[k] = v; }
  function cls(o, c, on) { if (o.classList.contains(c) !== on) o.classList.toggle(c, on); }
  function fit(wrap) {
    var el = rendered(wrap);
    if (!el) return;
    var w = wrap.clientWidth;
    if (w <= BASE + 4) { cls(wrap, 'fit', false); set(el, 'transform', ''); set(wrap, 'height', ''); return; }
    cls(wrap, 'fit', true);
    var k = w / BASE;
    set(el, 'transform', 'scale(' + k + ')');
    var h = el.offsetHeight;
    set(wrap, 'height', h ? Math.ceil(h * k) + 'px' : '');
  }
  // X shows its iframe (visibility) once the card has loaded and been measured
  function loaded(el) {
    var f = frame(el);
    return !!f && f.offsetHeight > 40 && getComputedStyle(f).visibility !== 'hidden' && getComputedStyle(el).visibility !== 'hidden';
  }
  // expected card height (at 550px or less) from data-h="w1:h1,w2:h2,..."
  function expected(wrap) {
    var pts = (wrap.getAttribute('data-h') || '').split(',').map(function (x) { return x.split(':').map(Number); })
      .filter(function (x) { return x[0] && x[1]; }).sort(function (a, b) { return a[0] - b[0]; });
    if (!pts.length) return 0;
    var w = Math.min(wrap.clientWidth, BASE);
    if (w <= pts[0][0]) return pts[0][1];
    for (var i = 1; i < pts.length; i++) {
      var a = pts[i - 1], b = pts[i];
      if (w <= b[0]) return a[1] + (b[1] - a[1]) * (w - a[0]) / (b[0] - a[0]);
    }
    return pts[pts.length - 1][1];
  }
  function skeleton(wrap) {
    if (wrap.querySelector('.tw-skel') || wrap.querySelector('blockquote.twitter-tweet')) return;
    var s = document.createElement('div');
    s.className = 'tw-skel';
    s.setAttribute('aria-hidden', 'true');
    wrap.appendChild(s);
  }
  function reveal(wrap) {
    if (wrap.classList.contains('ready')) return;
    fit(wrap);
    wrap.classList.add('ready');
    wrap.classList.remove('loading');
    wrap.style.minHeight = '';
    setTimeout(function () {
      if (!wrap.classList.contains('ready')) return;
      var s = wrap.querySelector('.tw-skel'); if (s) s.remove();
    }, 300);
  }
  function check(wrap) {
    var el = rendered(wrap);
    if (!el) { cls(wrap, 'ready', false); return; }
    if (!wrap.classList.contains('ready')) skeleton(wrap);
    fit(wrap);
    // reveal only once the card height has held still (media such as video
    // posters can grow the card just after X first shows it)
    if (!wrap.classList.contains('ready') && loaded(el)) {
      var h = frame(el).offsetHeight;
      if (wrap._h !== h) {
        wrap._h = h; clearTimeout(wrap._still);
        // a card far shorter than expected is usually still loading its
        // media, so it gets longer to settle
        var wait = h < 0.8 * expected(wrap) ? 1500 : 250;
        wrap._still = setTimeout(function () { if (rendered(wrap) === el && loaded(el) && frame(el).offsetHeight === wrap._h) reveal(wrap); else check(wrap); }, wait);
      }
    }
    if (wrap._el !== el) {
      wrap._el = el;
      // never leave a rendered card hidden, even if X changes its markup
      clearTimeout(wrap._safety);
      wrap._safety = setTimeout(function () { if (rendered(wrap) === el) reveal(wrap); }, 5000);
      if (wrap._ro) wrap._ro.disconnect();
      if (window.ResizeObserver) {
        wrap._ro = new ResizeObserver(function () { check(wrap); });
        wrap._ro.observe(wrap); wrap._ro.observe(el);
        var f = frame(el); if (f) wrap._ro.observe(f);
      }
    }
  }
  document.querySelectorAll('.tweet-embed').forEach(function (wrap) {
    // MutationObserver callbacks run before the next paint, so the card is
    // hidden and scaled before it can ever be drawn at 550px
    new MutationObserver(function () { check(wrap); })
      .observe(wrap, { childList: true, subtree: true, attributes: true, attributeFilter: ['style', 'class', 'height'] });
    check(wrap);
  });
  window.addEventListener('resize', function () { document.querySelectorAll('.tweet-embed').forEach(fit); });
})();
