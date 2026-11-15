/* Full-screen image viewer for article images, with zoom and pan */
(function () {
  var imgs = document.querySelectorAll('article img:not(.pv-img)');
  if (!imgs.length) return;
  var MIN = 1, MAX = 5, STEP = 2.5;
  var box, big, closeBtn, scrollY = 0, lastFocus = null, viaKey = false;
  var cur = null, hiSrc = '', hiDone = false, natW = 0, natH = 0;
  var s = 1, tx = 0, ty = 0, baseW = 0, baseH = 0;
  var ptrs = {}, nptr = 0, gest = null, tap = null, lastTap = null, lastToggle = 0, closeTimer = 0, animTimer = 0;
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)');

  function lock() {
    scrollY = window.scrollY || window.pageYOffset;
    var b = document.body;
    b.style.position = 'fixed';
    b.style.top = -scrollY + 'px';
    b.style.left = '0';
    b.style.right = '0';
    b.style.width = '100%';
    b.style.overflow = 'hidden';
    document.documentElement.style.overflow = 'hidden';
  }
  function unlock() {
    var b = document.body;
    b.style.position = b.style.top = b.style.left = b.style.right = b.style.width = b.style.overflow = '';
    document.documentElement.style.overflow = '';
    window.scrollTo(0, scrollY);
  }
  function isOpen() { return box && box.classList.contains('on'); }
  function clampS(v) { return Math.min(MAX, Math.max(MIN, v)); }

  /* Fit the image into the viewer at 1x, from the original's dimensions */
  function fit() {
    var cs = getComputedStyle(box);
    var aw = box.clientWidth - parseFloat(cs.paddingLeft) - parseFloat(cs.paddingRight);
    var ah = box.clientHeight - parseFloat(cs.paddingTop) - parseFloat(cs.paddingBottom);
    var w = natW || big.naturalWidth, h = natH || big.naturalHeight;
    if (!w || !h) { big.style.width = big.style.height = ''; return; }
    var k = Math.min(1, aw / w, ah / h);
    baseW = w * k; baseH = h * k;
    big.style.width = baseW + 'px';
    big.style.height = baseH + 'px';
  }
  /* Untransformed centre of the image in viewport coordinates */
  function centre() {
    var r = box.getBoundingClientRect();
    return { x: r.left + big.offsetLeft + big.offsetWidth / 2, y: r.top + big.offsetTop + big.offsetHeight / 2 };
  }
  function clampT(c) {
    c = c || centre();
    var vw = box.clientWidth, vh = box.clientHeight;
    var W = (baseW || big.offsetWidth) * s, H = (baseH || big.offsetHeight) * s;
    if (s <= 1) { tx = ty = 0; return; }
    if (W <= vw) tx = 0; else tx = Math.min(W / 2 - c.x, Math.max(vw - c.x - W / 2, tx));
    if (H <= vh) ty = 0; else ty = Math.min(H / 2 - c.y, Math.max(vh - c.y - H / 2, ty));
  }
  function apply(anim) {
    clearTimeout(animTimer);
    if (anim && !(reduce && reduce.matches)) {
      big.classList.add('lb-anim');
      animTimer = setTimeout(function () { big.classList.remove('lb-anim'); }, 260);
    } else big.classList.remove('lb-anim');
    big.style.transform = s === 1 ? '' : 'translate(' + tx + 'px,' + ty + 'px) scale(' + s + ')';
    box.classList.toggle('zoomed', s > 1);
    if (s > 1) loadHi();
  }
  function zoomAt(ns, px, py, anim) {
    var c = centre();
    ns = clampS(ns);
    if (px == null) { px = c.x + tx; py = c.y + ty; }
    var k = ns / s;
    tx = px - c.x - k * (px - c.x - tx);
    ty = py - c.y - k * (py - c.y - ty);
    s = ns;
    if (s <= 1.001) { s = 1; tx = ty = 0; }
    clampT(c);
    apply(anim);
  }
  function reset(anim) { s = 1; tx = ty = 0; apply(anim); }
  function toggleAt(x, y) {
    lastToggle = Date.now();
    if (s > 1) reset(true); else zoomAt(STEP, x, y, true);
  }
  /* Swap in the original file (or largest candidate) once zoomed, so charts stay sharp */
  function loadHi() {
    if (hiDone || !hiSrc) return;
    hiDone = true;
    var want = cur, pre = new Image();
    pre.onload = function () {
      var go = function () { if (cur === want && isOpen()) big.src = hiSrc; };
      if (pre.decode) pre.decode().then(go, go); else go();
    };
    pre.src = hiSrc;
  }
  function onImage(x, y) {
    var r = big.getBoundingClientRect();
    return x >= r.left && x <= r.right && y >= r.top && y <= r.bottom;
  }
  function dist(a, b) { return Math.hypot(a.x - b.x, a.y - b.y); }
  function two() { var k = Object.keys(ptrs); return [ptrs[k[0]], ptrs[k[1]]]; }

  function startPan(p) { gest = { type: 'pan', x: p.x, y: p.y, tx: tx, ty: ty }; }
  function startPinch() {
    var p = two(), c = centre();
    var mx = (p[0].x + p[1].x) / 2, my = (p[0].y + p[1].y) / 2;
    gest = { type: 'pinch', d: dist(p[0], p[1]) || 1, s: s, qx: (mx - c.x - tx) / s, qy: (my - c.y - ty) / s, c: c };
  }

  function down(e) {
    if (e.target.closest && e.target.closest('.lb-close')) return;
    if (e.pointerType === 'mouse' && e.button !== 0) return;
    e.preventDefault();
    try { box.setPointerCapture(e.pointerId); } catch (_) {}
    ptrs[e.pointerId] = { x: e.clientX, y: e.clientY };
    nptr = Object.keys(ptrs).length;
    big.classList.remove('lb-anim');
    if (nptr === 1) {
      tap = { x: e.clientX, y: e.clientY, t: Date.now(), moved: false, type: e.pointerType };
      if (s > 1) startPan(ptrs[e.pointerId]); else gest = null;
    } else if (nptr === 2) {
      if (tap) tap.moved = true;
      clearTimeout(closeTimer);
      startPinch();
    }
  }
  function move(e) {
    if (!ptrs[e.pointerId]) return;
    e.preventDefault();
    ptrs[e.pointerId] = { x: e.clientX, y: e.clientY };
    if (tap && !tap.moved && Math.hypot(e.clientX - tap.x, e.clientY - tap.y) > (tap.type === 'mouse' ? 4 : 10)) tap.moved = true;
    if (!gest) return;
    if (gest.type === 'pinch' && nptr >= 2) {
      var p = two(), c = gest.c;
      var mx = (p[0].x + p[1].x) / 2, my = (p[0].y + p[1].y) / 2;
      s = clampS(gest.s * dist(p[0], p[1]) / gest.d);
      tx = mx - c.x - s * gest.qx;
      ty = my - c.y - s * gest.qy;
      if (s <= 1.001) { s = 1; tx = ty = 0; }
      clampT(c);
      apply(false);
    } else if (gest.type === 'pan' && s > 1) {
      tx = gest.tx + e.clientX - gest.x;
      ty = gest.ty + e.clientY - gest.y;
      clampT();
      apply(false);
      if (tap && tap.moved) box.classList.add('dragging');
    }
  }
  function up(e) {
    if (!ptrs[e.pointerId]) return;
    delete ptrs[e.pointerId];
    nptr = Object.keys(ptrs).length;
    box.classList.remove('dragging');
    if (nptr === 1) {
      var k = Object.keys(ptrs)[0];
      if (s > 1) startPan(ptrs[k]); else gest = null;
      return;
    }
    if (nptr > 1) return;
    gest = null;
    var t = tap; tap = null;
    if (!t || t.moved || e.type === 'pointercancel' || Date.now() - t.t > 500) return;
    var x = e.clientX, y = e.clientY, now = Date.now();
    if (t.type === 'mouse') {
      if (now - lastToggle < 350) return; // second click of a double-click
      if (s > 1 || onImage(x, y)) toggleAt(x, y); else close();
      return;
    }
    if (lastTap && now - lastTap.t < 320 && Math.hypot(x - lastTap.x, y - lastTap.y) < 40) {
      clearTimeout(closeTimer);
      lastTap = null;
      toggleAt(x, y);
      return;
    }
    lastTap = { x: x, y: y, t: now };
    if (s === 1 && !onImage(x, y)) {
      clearTimeout(closeTimer);
      closeTimer = setTimeout(function () { if (s === 1) close(); }, 320);
    }
  }
  function wheel(e) {
    if (!isOpen()) return;
    e.preventDefault();
    var dy = e.deltaY * (e.deltaMode === 1 ? 16 : e.deltaMode === 2 ? 400 : 1);
    dy = Math.max(-100, Math.min(100, dy));
    zoomAt(s * Math.exp(-dy * (e.ctrlKey ? 0.01 : 0.003)), e.clientX, e.clientY, false);
  }

  function build() {
    box = document.createElement('div');
    box.className = 'lb';
    box.setAttribute('role', 'dialog');
    box.setAttribute('aria-modal', 'true');
    box.setAttribute('aria-label', 'Image viewer');
    box.setAttribute('aria-describedby', 'lb-help');
    box.innerHTML = '<button class="lb-close" type="button" aria-label="Close">&times;</button>' +
      '<img class="lb-img" alt="" draggable="false">' +
      '<span id="lb-help" class="lb-help">Plus and minus zoom, 0 resets, arrow keys pan, Escape closes.</span>';
    big = box.querySelector('.lb-img');
    closeBtn = box.querySelector('.lb-close');
    closeBtn.addEventListener('click', close);
    box.addEventListener('pointerdown', down);
    box.addEventListener('pointermove', move);
    box.addEventListener('pointerup', up);
    box.addEventListener('pointercancel', up);
    box.addEventListener('wheel', wheel, { passive: false });
    box.addEventListener('touchmove', function (e) { e.preventDefault(); }, { passive: false });
    box.addEventListener('gesturestart', function (e) { e.preventDefault(); });
    box.addEventListener('gesturechange', function (e) { e.preventDefault(); });
    box.addEventListener('dblclick', function (e) { e.preventDefault(); });
    box.addEventListener('dragstart', function (e) { e.preventDefault(); });
    window.addEventListener('resize', function () { if (isOpen()) { fit(); clampT(); apply(false); } });
    document.body.appendChild(box);
  }
  function open(img, key) {
    if (!box) build();
    viaKey = !!key;
    lastFocus = cur = img;
    ptrs = {}; nptr = 0; gest = tap = lastTap = null;
    natW = parseFloat(img.getAttribute('width')) || img.naturalWidth;
    natH = parseFloat(img.getAttribute('height')) || img.naturalHeight;
    var src = img.getAttribute('src');
    hiSrc = src ? new URL(src, location.href).href : (img.currentSrc || img.src);
    hiDone = false;
    big.src = img.getAttribute('data-full') || img.currentSrc || img.src;
    if (big.src === hiSrc) hiDone = true;
    big.alt = img.alt || '';
    s = 1; tx = ty = 0; apply(false);
    lock();
    box.classList.add('on');
    fit();
    closeBtn.focus({ preventScroll: true });
  }
  function close() {
    if (!isOpen()) return;
    clearTimeout(closeTimer);
    box.classList.remove('on', 'dragging');
    unlock();
    if (viaKey && lastFocus) lastFocus.focus({ preventScroll: true });
    else if (document.activeElement) document.activeElement.blur();
  }
  document.addEventListener('keydown', function (e) {
    if (!isOpen()) return;
    var k = e.key;
    if (k === 'Escape') { close(); return; }
    if (k === 'Tab') { e.preventDefault(); closeBtn.focus({ preventScroll: true }); return; }
    if (e.ctrlKey || e.metaKey || e.altKey) return;
    if (k === '+' || k === '=') { e.preventDefault(); zoomAt(s * 1.5, null, null, true); }
    else if (k === '-' || k === '_') { e.preventDefault(); zoomAt(s / 1.5, null, null, true); }
    else if (k === '0') { e.preventDefault(); reset(true); }
    else if (s > 1 && /^Arrow/.test(k)) {
      e.preventDefault();
      var d = 80;
      if (k === 'ArrowLeft') tx += d; else if (k === 'ArrowRight') tx -= d;
      else if (k === 'ArrowUp') ty += d; else ty -= d;
      clampT(); apply(true);
    }
  });
  imgs.forEach(function (img) {
    img.classList.add('zoomable');
    img.setAttribute('tabindex', '0');
    img.setAttribute('role', 'button');
    img.addEventListener('click', function (e) { e.preventDefault(); open(img, false); });
    img.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); open(img, true); } });
  });
})();
