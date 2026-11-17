/* Links to a highlighted passage.
   Select text in a post and a small "Copy link to highlight" button appears.
   The link is the page URL plus #hl=<anchors>, followed by the standard
   :~:text=<anchors> directive (browsers with native support scroll before any
   script runs and strip it from location.hash). On load, this script finds the
   passage itself, wraps it in <mark class="hl"> (across paragraphs if needed)
   and scrolls it to the middle of the screen. If the passage is not found
   (the post changed), the page simply loads as usual.
   Anchor format follows text fragments: [prefix-,]start[,end][,-suffix]. */
(function () {
  var article = document.querySelector('main article') || document.querySelector('article');
  if (!article || !window.getSelection) return;

  var BLOCK = /^(P|LI|UL|OL|H[1-6]|BLOCKQUOTE|FIGURE|FIGCAPTION|DIV|HEADER|FOOTER|SECTION|PRE|TABLE|TR|TD|TH|DL|DT|DD|HR|BR|PICTURE|IMG|VIDEO)$/;
  var SKIP = /^(SCRIPT|STYLE|NOSCRIPT|TEMPLATE|SVG|BUTTON|IFRAME)$/;
  var WORD = /[\p{L}\p{N}]/u;
  var SPACE = /[\s\u00a0\u200b]/;

  /* Normalised text of the article: whitespace collapsed to one space, block
     boundaries as "\n". For every character we keep the text node and offset
     it came from (or null for a synthetic boundary). */
  function model() {
    var out = [], mN = [], mO = [], tn = [], tk = [];
    function boundary() {
      var n = out.length;
      if (!n) return;
      if (out[n - 1] === ' ') out[n - 1] = '\n';
      else if (out[n - 1] !== '\n') { out.push('\n'); mN.push(null); mO.push(0); }
    }
    function walk(el) {
      for (var c = el.firstChild; c; c = c.nextSibling) {
        if (c.nodeType === 3) {
          var s = c.data, first = -1;
          for (var i = 0; i < s.length; i++) {
            var ch = s.charAt(i), n = out.length;
            if (SPACE.test(ch)) {
              if (!n || out[n - 1] === ' ' || out[n - 1] === '\n') continue;
              ch = ' ';
            }
            if (first < 0) first = out.length;
            out.push(ch); mN.push(c); mO.push(i);
          }
          tn.push(c); tk.push([first, first < 0 ? -1 : out.length - 1]);
        } else if (c.nodeType === 1) {
          var tag = c.tagName.toUpperCase();
          if (SKIP.test(tag) || c.classList.contains('tweet-embed') || c.classList.contains('x-callout') || c.classList.contains('hl-pop')) { if (BLOCK.test(tag) || tag === 'DIV') boundary(); continue; }
          var b = BLOCK.test(tag);
          if (b) boundary();
          walk(c);
          if (b) boundary();
        }
      }
    }
    walk(article);
    return { text: out.join(''), mN: mN, mO: mO, tn: tn, tk: tk };
  }

  function isWord(ch) { return !!ch && WORD.test(ch); }

  // index of the first model character at or after a DOM point
  function startIndex(m, c, o) {
    var i = c.nodeType === 3 ? m.tn.indexOf(c) : -1;
    if (i >= 0 && m.tk[i][0] >= 0) {
      for (var k = m.tk[i][0]; k <= m.tk[i][1]; k++) if (m.mN[k] === c && m.mO[k] >= o) return k;
      return m.tk[i][1] + 1;
    }
    var p = document.createRange();
    p.setStart(c, o);
    for (var j = 0; j < m.tn.length; j++) {
      if (m.tk[j][0] < 0) continue;
      if (p.comparePoint(m.tn[j], 0) >= 0) return m.tk[j][0];
    }
    return m.text.length;
  }
  // exclusive index just after the last model character before a DOM point
  function endIndex(m, c, o) {
    var i = c.nodeType === 3 ? m.tn.indexOf(c) : -1;
    if (i >= 0 && m.tk[i][0] >= 0) {
      for (var k = m.tk[i][1]; k >= m.tk[i][0]; k--) if (m.mN[k] === c && m.mO[k] < o) return k + 1;
      return m.tk[i][0];
    }
    var p = document.createRange();
    p.setStart(c, o);
    for (var j = m.tn.length - 1; j >= 0; j--) {
      if (m.tk[j][0] < 0) continue;
      if (p.comparePoint(m.tn[j], 0) < 0) return m.tk[j][1] + 1;
    }
    return 0;
  }

  function enc(s) { return encodeURIComponent(s).replace(/-/g, '%2D'); }
  function words(s) { return s.split(' ').filter(Boolean); }

  // selection -> anchor string, or null
  function anchorFor(range) {
    if (!range || range.collapsed || !range.intersectsNode(article)) return null;
    var m = model(), t = m.text;
    var s = startIndex(m, range.startContainer, range.startOffset);
    var e = endIndex(m, range.endContainer, range.endOffset);
    while (s < e && SPACE.test(t.charAt(s))) s++;
    while (e > s && SPACE.test(t.charAt(e - 1))) e--;
    if (e <= s) return null;
    while (s > 0 && isWord(t.charAt(s - 1)) && isWord(t.charAt(s))) s--;
    while (e < t.length && isWord(t.charAt(e)) && isWord(t.charAt(e - 1))) e++;
    var sel = t.slice(s, e);
    if (!/[\p{L}\p{N}]/u.test(sel)) return null;
    var parts = [];
    var before = t.slice(Math.max(0, s - 80), s);
    before = before.slice(before.lastIndexOf('\n') + 1);
    var pw = words(before);
    if (pw.length) parts.push(enc(pw.slice(-3).join(' ')) + '-');
    var sw = words(sel);
    if (sel.indexOf('\n') < 0 && sw.length <= 10) {
      parts.push(enc(sel));
    } else {
      var firstLine = sel.split('\n')[0], lastLine = sel.split('\n').pop();
      var a = words(firstLine), z = words(lastLine);
      parts.push(enc(a.slice(0, 5).join(' ')));
      parts.push(enc(z.slice(-5).join(' ')));
    }
    var after = t.slice(e, e + 80);
    var nl = after.indexOf('\n');
    if (nl >= 0) after = after.slice(0, nl);
    var aw = words(after);
    if (aw.length) parts.push('-' + enc(aw.slice(0, 3).join(' ')));
    return parts.join(',');
  }

  function parse(v) {
    var parts = v.split(','), o = {};
    try {
      if (parts.length > 1 && /-$/.test(parts[0])) o.prefix = decodeURIComponent(parts.shift().slice(0, -1));
      if (parts.length > 1 && /^-/.test(parts[parts.length - 1])) o.suffix = decodeURIComponent(parts.pop().slice(1));
      if (!parts.length || parts.length > 2) return null;
      o.start = decodeURIComponent(parts[0]);
      if (parts[1]) o.end = decodeURIComponent(parts[1]);
    } catch (err) { return null; }
    return o.start ? o : null;
  }

  function squash(s) { return s.replace(/\s+/g, ' ').trim(); }
  function locate(t, a) {
    var best = null, from = 0, pre = a.prefix && squash(a.prefix), suf = a.suffix && squash(a.suffix);
    for (var guard = 0; guard < 500; guard++) {
      var i = t.indexOf(a.start, from);
      if (i < 0) break;
      from = i + 1;
      if (isWord(t.charAt(i - 1)) && isWord(a.start.charAt(0))) continue;
      var e;
      if (a.end) {
        var j = t.indexOf(a.end, i + a.start.length);
        if (j < 0) break;
        e = j + a.end.length;
      } else e = i + a.start.length;
      if (isWord(t.charAt(e)) && isWord(t.charAt(e - 1))) continue;
      var score = 0;
      if (!pre || squash(t.slice(Math.max(0, i - pre.length - 4), i)).slice(-pre.length) === pre) score++;
      if (!suf || squash(t.slice(e, e + suf.length + 4)).slice(0, suf.length) === suf) score++;
      if (!best || score > best.score) best = { s: i, e: e, score: score };
      if (score === 2) break;
    }
    return best;
  }

  function wrap(m, s, e) {
    var segs = [], last = null;
    for (var k = s; k < e; k++) {
      var n = m.mN[k];
      if (!n) continue;
      if (last && last.n === n) last.b = m.mO[k] + 1;
      else { last = { n: n, a: m.mO[k], b: m.mO[k] + 1 }; segs.push(last); }
    }
    var marks = [];
    segs.forEach(function (g) {
      var node = g.n;
      if (!/\S/.test(node.data.slice(g.a, g.b))) return;
      var mid = g.a > 0 ? node.splitText(g.a) : node;
      if (g.b - g.a < mid.data.length) mid.splitText(g.b - g.a);
      var mk = document.createElement('mark');
      mk.className = 'hl';
      mid.parentNode.insertBefore(mk, mid);
      mk.appendChild(mid);
      marks.push(mk);
    });
    return marks;
  }

  function clear() {
    var ms = article.querySelectorAll('mark.hl');
    for (var i = 0; i < ms.length; i++) {
      var mk = ms[i], p = mk.parentNode;
      while (mk.firstChild) p.insertBefore(mk.firstChild, mk);
      p.removeChild(mk);
      p.normalize();
    }
  }

  function hashValue() {
    var h = location.hash || '';
    var x = h.indexOf(':~:');
    if (x >= 0) h = h.slice(0, x);
    var mt = /^#hl=([^&]+)/.exec(h);
    return mt ? mt[1] : '';
  }

  var userMoved = false;
  function center(marks) {
    if (userMoved || !marks.length) return;
    var r1 = marks[0].getBoundingClientRect(), r2 = marks[marks.length - 1].getBoundingClientRect();
    var top = r1.top + window.pageYOffset, h = r2.bottom - r1.top, vh = window.innerHeight;
    var y = h < vh * 0.7 ? top - (vh - h) / 2 : top - vh * 0.18;
    window.scrollTo(0, Math.max(0, y));
  }

  function apply() {
    var v = hashValue();
    clear();
    if (!v) return;
    var a = parse(v);
    if (!a) return;
    var m = model();
    var hit = locate(m.text, a);
    if (!hit) return;
    var marks = wrap(m, hit.s, hit.e);
    if (!marks.length) return;
    userMoved = false;
    center(marks);
    var again = function () { center(marks); };
    window.addEventListener('load', function () { again(); setTimeout(again, 700); }, { once: true });
    if (document.readyState === 'complete') setTimeout(again, 300);
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(again);
    setTimeout(again, 1600);
  }
  ['wheel', 'touchmove', 'keydown', 'mousedown'].forEach(function (ev) {
    window.addEventListener(ev, function () { userMoved = true; }, { passive: true, capture: true });
  });

  /* ------------------------------------------------------------- popup */
  var pop = null, live = null, link = '', shownY = 0, pressing = false, dragging = false, resetT = 0, selT = 0;
  var coarse = window.matchMedia('(hover: none), (pointer: coarse)');
  var LABEL = 'Copy link to highlight', DONE = 'Link copied';

  function build() {
    pop = document.createElement('button');
    pop.type = 'button';
    pop.className = 'hl-pop';
    pop.setAttribute('aria-label', LABEL);
    pop.innerHTML = '<svg aria-hidden="true" viewBox="0 0 16 16" width="13" height="13"><path d="M6.6 9.4a3 3 0 0 0 4.2 0l2.1-2.1a3 3 0 0 0-4.2-4.2l-.9.9M9.4 6.6a3 3 0 0 0-4.2 0L3.1 8.7a3 3 0 0 0 4.2 4.2l.9-.9" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg><span>' + LABEL + '</span>';
    live = document.createElement('span');
    live.className = 'hl-live';
    live.setAttribute('role', 'status');
    live.setAttribute('aria-live', 'polite');
    pop.addEventListener('pointerdown', function (e) { pressing = true; if (e.pointerType === 'mouse') e.preventDefault(); });
    pop.addEventListener('mousedown', function (e) { e.preventDefault(); });
    pop.addEventListener('click', function (e) { e.preventDefault(); pressing = false; copy(); });
    document.body.appendChild(pop);
    document.body.appendChild(live);
  }

  function hide() {
    if (!pop || !pop.classList.contains('on')) return;
    pop.classList.remove('on');
    clearTimeout(resetT);
  }

  function setLabel(t) { pop.lastChild.textContent = t; pop.setAttribute('aria-label', t); }

  function place(range) {
    var rects = range.getClientRects(), first = null, lastR = null;
    for (var i = 0; i < rects.length; i++) {
      if (rects[i].width < 1 || rects[i].height < 1) continue;
      if (!first) first = rects[i];
      lastR = rects[i];
    }
    var box = range.getBoundingClientRect();
    if (!first) first = lastR = box;
    var pw = pop.offsetWidth, ph = pop.offsetHeight, vw = document.documentElement.clientWidth, gap = 10;
    var below = coarse.matches, x, y;
    if (!below) {
      y = first.top - ph - gap;
      if (y < 8) below = true;
      x = (rects.length > 1 ? (box.left + box.right) / 2 : (first.left + first.right) / 2) - pw / 2;
    }
    if (below) {
      // phones: under the selection, clear of the native selection menu and handles
      y = lastR.bottom + gap + (coarse.matches ? 14 : 0);
      x = (lastR.left + lastR.right) / 2 - pw / 2;
      if (y + ph > window.innerHeight - 8 && first.top - ph - gap > 8) y = first.top - ph - gap - (coarse.matches ? 48 : 0);
    }
    x = Math.max(8, Math.min(x, vw - pw - 8));
    pop.style.left = Math.round(x + window.pageXOffset) + 'px';
    pop.style.top = Math.round(y + window.pageYOffset) + 'px';
  }

  function check() {
    var sel = window.getSelection();
    if (!sel || !sel.rangeCount || sel.isCollapsed) { if (!pressing) hide(); return; }
    var range = sel.getRangeAt(0);
    var anc = range.commonAncestorContainer;
    if (anc.nodeType !== 1) anc = anc.parentNode;
    if (!article.contains(anc) && !anc.contains(article)) { hide(); return; }
    var a = anchorFor(range);
    if (!a) { hide(); return; }
    link = location.origin + location.pathname + '#hl=' + a + ':~:text=' + a;
    if (!pop) build();
    clearTimeout(resetT);
    setLabel(LABEL);
    pop.classList.remove('done');
    place(range);
    shownY = window.pageYOffset;
    // reflow so the fade-in runs when shown for the first time
    void pop.offsetWidth;
    pop.classList.add('on');
  }

  function done() {
    setLabel(DONE);
    pop.classList.add('done');
    live.textContent = DONE;
    clearTimeout(resetT);
    resetT = setTimeout(function () { hide(); live.textContent = ''; }, 1400);
  }
  function fallbackCopy(text) {
    var ta = document.createElement('textarea');
    ta.value = text;
    ta.setAttribute('readonly', '');
    ta.style.cssText = 'position:fixed;top:0;left:0;opacity:0;pointer-events:none';
    var sel = window.getSelection(), saved = sel.rangeCount ? sel.getRangeAt(0).cloneRange() : null;
    document.body.appendChild(ta);
    ta.select();
    var ok = false;
    try { ok = document.execCommand('copy'); } catch (err) {}
    document.body.removeChild(ta);
    if (saved) { sel.removeAllRanges(); sel.addRange(saved); }
    return ok;
  }
  function copy() {
    if (!link) return;
    var text = link;
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(done, function () { if (fallbackCopy(text)) done(); });
    } else if (fallbackCopy(text)) done();
  }

  document.addEventListener('mousedown', function (e) {
    if (pop && pop.contains(e.target)) return;
    if (e.button === 0) dragging = true;
    hide();
  }, true);
  document.addEventListener('mouseup', function () {
    if (!dragging) return;
    dragging = false;
    clearTimeout(selT);
    selT = setTimeout(check, 10);
  }, true);
  document.addEventListener('selectionchange', function () {
    if (pressing) return;
    var sel = window.getSelection();
    if (!sel || sel.isCollapsed) { clearTimeout(selT); hide(); return; }
    if (dragging) return;
    clearTimeout(selT);
    selT = setTimeout(check, coarse.matches ? 350 : 220);
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') hide();
  });
  document.addEventListener('pointerup', function () { if (pressing) setTimeout(function () { pressing = false; }, 450); }, true);
  document.addEventListener('pointercancel', function () { pressing = false; }, true);
  window.addEventListener('scroll', function () {
    if (pop && pop.classList.contains('on') && Math.abs(window.pageYOffset - shownY) > 40) hide();
  }, { passive: true });
  window.addEventListener('resize', hide);

  window.addEventListener('hashchange', apply);
  apply();
})();
