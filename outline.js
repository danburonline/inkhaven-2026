/* Section outline. The build renders <nav class="toc"> from tools/outline.json
   and gives each section's first paragraph an id. On wide screens the nav sits
   in the left margin and marks the section being read; on narrow screens a
   small pill at the bottom shows the current section and opens the list as a
   bottom sheet. Clicking a section scrolls there and sets #sec-... in the URL
   (replaceState, so no extra history entries; #hl= links still land as usual). */
(function () {
  var nav = document.getElementById('toc');
  if (!nav) return;
  var links = [].slice.call(nav.querySelectorAll('a[href^="#"]'));
  var secs = links.map(function (a) { return document.getElementById(a.getAttribute('href').slice(1)); });
  if (!links.length || secs.indexOf(null) >= 0) return;
  var wide = window.matchMedia('(min-width: 1220px)');
  var still = window.matchMedia('(prefers-reduced-motion: reduce)');
  var cur = -1, pill = null, pillText = null, dim = null, isOpen = false, lastFocus = null;

  function headH() {
    var pn = document.querySelector('.post-nav');
    return pn ? pn.getBoundingClientRect().height : 0;
  }
  function update() {
    var line = headH() + window.innerHeight * 0.25, k = -1;
    for (var i = 0; i < secs.length; i++) if (secs[i].getBoundingClientRect().top <= line) k = i;
    if (k === cur) return;
    cur = k;
    links.forEach(function (a, i) {
      if (i === k) a.setAttribute('aria-current', 'location'); else a.removeAttribute('aria-current');
    });
    if (pillText) {
      pillText.textContent = k >= 0 ? links[k].textContent : 'Sections';
      pill.setAttribute('aria-label', k >= 0 ? 'Sections: ' + links[k].textContent : 'Sections');
    }
  }
  var raf = 0;
  function soon() { if (!raf) raf = requestAnimationFrame(function () { raf = 0; update(); }); }
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(soon, { rootMargin: '-10% 0px -60% 0px' });
    secs.forEach(function (s) { io.observe(s); });
  }

  function go(i) {
    var el = secs[i];
    var y = el.getBoundingClientRect().top + window.pageYOffset - headH() - 16;
    window.scrollTo({ top: Math.max(0, y), behavior: still.matches ? 'auto' : 'smooth' });
    try { history.replaceState(history.state, '', '#' + el.id); } catch (err) {}
    cur = -1;
    setTimeout(update, still.matches ? 0 : 600);
  }
  links.forEach(function (a, i) {
    a.addEventListener('click', function (e) {
      if (e.metaKey || e.ctrlKey || e.shiftKey || e.altKey || e.button) return;
      e.preventDefault();
      if (isOpen) close(false);
      go(i);
      try { secs[i].setAttribute('tabindex', '-1'); secs[i].focus({ preventScroll: true }); } catch (err) {}
    });
  });

  /* ------------------------------------------------ narrow: pill + sheet */
  function buildNarrow() {
    if (pill) return;
    pill = document.createElement('button');
    pill.type = 'button';
    pill.className = 'toc-pill';
    pill.setAttribute('aria-controls', 'toc');
    pill.setAttribute('aria-expanded', 'false');
    pill.setAttribute('aria-haspopup', 'dialog');
    pill.innerHTML = '<svg aria-hidden="true" viewBox="0 0 16 16" width="16" height="16"><g fill="currentColor"><circle cx="2.5" cy="4" r="1.25"/><circle cx="2.5" cy="8" r="1.25"/><circle cx="2.5" cy="12" r="1.25"/></g><path d="M6 4h8M6 8h8M6 12h5.5" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg><span class="toc-pill-t"></span>';
    pillText = pill.lastChild;
    pillText.textContent = 'Sections';
    pill.setAttribute('aria-label', 'Sections');
    pill.addEventListener('click', function () { isOpen ? close(true) : open(); });
    dim = document.createElement('div');
    dim.className = 'toc-dim';
    dim.addEventListener('click', function () { close(true); });
    var grip = document.createElement('div');
    grip.className = 'toc-grip';
    grip.setAttribute('aria-hidden', 'true');
    nav.insertBefore(grip, nav.firstChild);
    var closeBtn = document.createElement('button');
    closeBtn.type = 'button';
    closeBtn.className = 'toc-close';
    closeBtn.setAttribute('aria-label', 'Close sections');
    closeBtn.textContent = 'Close';
    closeBtn.addEventListener('click', function () { close(true); });
    nav.insertBefore(closeBtn, nav.firstChild);
    document.body.appendChild(dim);
    document.body.appendChild(pill);
    cur = -1;
    soon();
  }
  function open() {
    if (isOpen || wide.matches) return;
    isOpen = true;
    lastFocus = document.activeElement;
    nav.setAttribute('role', 'dialog');
    nav.setAttribute('aria-modal', 'true');
    nav.classList.add('open');
    dim.classList.add('on');
    pill.setAttribute('aria-expanded', 'true');
    document.documentElement.classList.add('toc-lock');
    var a = links[cur >= 0 ? cur : 0];
    a.focus({ preventScroll: true });
    var r = a.getBoundingClientRect(), n = nav.getBoundingClientRect();
    if (r.bottom > n.bottom || r.top < n.top) nav.scrollTop += r.top - n.top - n.height / 2;
  }
  function close(focus) {
    if (!isOpen) return;
    isOpen = false;
    nav.classList.remove('open');
    nav.removeAttribute('role');
    nav.removeAttribute('aria-modal');
    nav.style.transform = '';
    dim.classList.remove('on');
    pill.setAttribute('aria-expanded', 'false');
    document.documentElement.classList.remove('toc-lock');
    if (focus) (pill || lastFocus).focus({ preventScroll: true });
  }
  document.addEventListener('keydown', function (e) {
    if (!isOpen) return;
    if (e.key === 'Escape') { e.preventDefault(); close(true); return; }
    if (e.key === 'Tab') {
      var focusable = [].slice.call(nav.querySelectorAll('button, a[href]'));
      var i = focusable.indexOf(document.activeElement);
      if (e.shiftKey && i <= 0) { e.preventDefault(); focusable[focusable.length - 1].focus(); }
      else if (!e.shiftKey && i === focusable.length - 1) { e.preventDefault(); focusable[0].focus(); }
    }
    if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
      e.preventDefault();
      var j = links.indexOf(document.activeElement);
      j = e.key === 'ArrowDown' ? (j + 1) % links.length : (j - 1 + links.length) % links.length;
      links[j].focus();
    }
  });
  // swipe the sheet down to close it
  var y0 = null, dy = 0;
  nav.addEventListener('touchstart', function (e) {
    if (!isOpen || e.touches.length !== 1) return;
    y0 = nav.scrollTop <= 0 ? e.touches[0].clientY : null; dy = 0;
  }, { passive: true });
  nav.addEventListener('touchmove', function (e) {
    if (y0 === null) return;
    dy = e.touches[0].clientY - y0;
    if (dy > 0) nav.style.transform = 'translateY(' + dy + 'px)';
  }, { passive: true });
  nav.addEventListener('touchend', function () {
    if (y0 === null) return;
    y0 = null;
    nav.style.transform = '';
    if (dy > 60) close(true);
  });

  nav.addEventListener('touchcancel', function () { y0 = null; nav.style.transform = ''; });

  // the pill hides while scrolling down, near the top, and while text is
  // selected (so it never meets the highlight popup or the selection menu)
  var lastY = window.pageYOffset, selecting = false;
  function pillState() {
    if (!pill) return;
    var y = window.pageYOffset, show = pill.classList.contains('on');
    var first = secs[0].getBoundingClientRect().top + y;
    if (y > lastY + 4) show = false;
    else if (y < lastY - 4) show = true;
    if (y + window.innerHeight >= document.documentElement.scrollHeight - 8) show = true;
    if (y < window.innerHeight * 0.5 || y + window.innerHeight * 0.6 < first) show = false;
    if (selecting) show = false;
    if (isOpen) show = true;
    if (Math.abs(y - lastY) > 4 || show !== pill.classList.contains('on')) lastY = y;
    pill.classList.toggle('on', show);
  }
  window.addEventListener('scroll', function () { soon(); pillState(); }, { passive: true });
  document.addEventListener('selectionchange', function () {
    var s = window.getSelection();
    var was = selecting;
    selecting = !!(s && !s.isCollapsed);
    if (was !== selecting) pillState();
  });

  function mode() {
    if (wide.matches) { close(false); if (pill) pill.classList.remove('on'); }
    else buildNarrow();
  }
  if (wide.addEventListener) wide.addEventListener('change', mode); else wide.addListener(mode);
  window.addEventListener('resize', soon);
  mode();
  soon();
})();
