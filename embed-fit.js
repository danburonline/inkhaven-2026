/* Scale X embeds (capped at 550px by X) up to the full text column width */
(function () {
  var BASE = 550;
  function fit(wrap) {
    var el = wrap.querySelector('.twitter-tweet-rendered');
    if (!el) return;
    var w = wrap.clientWidth;
    if (w <= BASE + 4) { wrap.classList.remove('fit'); el.style.transform = ''; wrap.style.height = ''; return; }
    wrap.classList.add('fit');
    var k = w / BASE;
    el.style.transform = 'scale(' + k + ')';
    wrap.style.height = Math.ceil(el.offsetHeight * k) + 'px';
  }
  function watch(wrap) {
    var el = wrap.querySelector('.twitter-tweet-rendered');
    if (wrap._fit === el) { fit(wrap); return; } wrap._fit = el;
    if (window.ResizeObserver) {
      var ro = new ResizeObserver(function () { fit(wrap); });
      ro.observe(wrap); if (el) ro.observe(el);
      var f = el && el.querySelector('iframe'); if (f) ro.observe(f);
    }
    fit(wrap);
  }
  function scan() {
    document.querySelectorAll('.tweet-embed').forEach(function (w) {
      if (w.querySelector('.twitter-tweet-rendered')) watch(w);
    });
  }
  window.addEventListener('resize', function () { document.querySelectorAll('.tweet-embed').forEach(fit); });
  var tries = 0, t = setInterval(function () {
    scan();
    if (window.twttr && twttr.events && !scan.bound) { scan.bound = true; twttr.events.bind('rendered', function () { scan(); setTimeout(scan, 300); }); }
    if (++tries > 40) clearInterval(t);
  }, 500);
})();
