/* Hover / tap previews for inline reference links (a.ref), data from /previews.json */
(function () {
  var links = document.querySelectorAll('a.ref');
  if (!links.length) return;
  var data = null, card = null, cur = null, hideT = null, showT = null;
  var touch = window.matchMedia('(hover: none), (pointer: coarse)').matches;
  var lastTouch = 0;
  document.addEventListener('touchstart', function () { lastTouch = Date.now(); touch = true; }, { passive: true, capture: true });
  document.addEventListener('pointerdown', function (e) { if (e.pointerType === 'touch' || e.pointerType === 'pen') { lastTouch = Date.now(); touch = true; } }, true);
  function isTouch() { return touch || Date.now() - lastTouch < 1000; }
  fetch('/previews.json').then(function (r) { return r.json(); }).then(function (j) { data = j; });

  function esc(s) { var d = document.createElement('div'); d.textContent = s || ''; return d.innerHTML; }
  function fmtDate(s) {
    var d = new Date(s); if (isNaN(d)) return '';
    return d.toLocaleDateString('en-GB', { day: 'numeric', month: 'short', year: 'numeric' });
  }
  function build(a, e) {
    var h = '';
    if (e.image) h += '<img class="pv-img" src="' + e.image + '" alt="" loading="lazy">';
    h += '<div class="pv-body">';
    if (e.type === 'x') {
      h += '<div class="pv-meta"><strong>' + esc(e.author) + '</strong> <span>' + esc(e.handle) + ' · ' + fmtDate(e.date) + '</span></div>';
    } else {
      h += '<div class="pv-meta"><span>' + esc(e.site) + '</span></div><div class="pv-title">' + esc(e.title) + '</div>';
      if (e.byline) h += '<div class="pv-meta"><span>' + esc(e.byline) + '</span></div>';
    }
    h += '<div class="pv-text">' + esc(e.text).replace(/\n+/g, '<br>') + '</div>';
    if (e.quote) h += '<div class="pv-quote"><strong>' + esc(e.quote.author) + '</strong> ' + esc(e.quote.text) + '</div>';
    if (isTouch()) h += '<a class="pv-open" href="' + a.href + '" target="_blank" rel="noopener">Open ' + (e.type === 'x' ? 'post on X' : esc(e.site)) + ' ↗</a>';
    h += '</div>';
    return h;
  }
  function place(a) {
    var r = a.getBoundingClientRect(), w = Math.min(360, window.innerWidth - 24);
    card.style.width = w + 'px';
    var left = Math.max(12, Math.min(r.left + r.width / 2 - w / 2, window.innerWidth - w - 12));
    card.style.left = left + window.scrollX + 'px';
    var ch = card.offsetHeight, below = window.innerHeight - r.bottom;
    var top = (below > ch + 16 || below > r.top) ? r.bottom + 8 : r.top - ch - 8;
    card.style.top = top + window.scrollY + 'px';
  }
  function show(a) {
    if (!data || !data[a.getAttribute('href')]) return false;
    clearTimeout(hideT);
    if (!card) {
      card = document.createElement('div'); card.className = 'pv-card'; document.body.appendChild(card);
      card.addEventListener('pointerenter', function (e) { if (e.pointerType === 'mouse') clearTimeout(hideT); });
      card.addEventListener('pointerleave', function (e) { if (e.pointerType === 'mouse') hide(); });
      card.addEventListener('click', function (e) {
        if (!isTouch() || !cur) return;
        if (e.target.closest('a')) return;
        window.open(cur.href, '_blank', 'noopener');
      });
    }
    if (cur !== a || card._touch !== isTouch()) {
      card._touch = isTouch();
      card.innerHTML = build(a, data[a.getAttribute('href')]);
      var img = card.querySelector('img'); if (img) img.onload = function () { if (cur === a) place(a); };
    }
    cur = a; card.classList.add('on'); place(a);
    return true;
  }
  function hide() { hideT = setTimeout(function () { if (card) card.classList.remove('on'); cur = null; }, 150); }

  links.forEach(function (a) {
    a.addEventListener('click', function (ev) {
      if (!isTouch()) return;
      if (cur === a && card && card.classList.contains('on')) return; /* second tap follows the link */
      if (show(a)) ev.preventDefault();
    });
    a.addEventListener('pointerenter', function (e) {
      if (e.pointerType !== 'mouse') return;
      clearTimeout(showT); showT = setTimeout(function () { show(a); }, 250);
    });
    a.addEventListener('pointerleave', function (e) {
      if (e.pointerType !== 'mouse') return;
      clearTimeout(showT); hide();
    });
    a.addEventListener('focus', function () { if (!isTouch()) show(a); });
    a.addEventListener('blur', function () { if (!isTouch()) hide(); });
  });
  document.addEventListener('click', function (ev) {
    if (card && cur && !card.contains(ev.target) && ev.target !== cur) { card.classList.remove('on'); cur = null; }
  });
  window.addEventListener('scroll', function () { if (cur && !isTouch()) { card.classList.remove('on'); cur = null; } }, { passive: true });
})();
