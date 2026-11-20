/* Copy control on a post title: link icon copies the article URL, the chevron
   opens Copy link / Copy title / Copy text (plain text, links written out). */
(function () {
  var h1 = document.querySelector('.post-header h1');
  var article = h1 && h1.closest('article');
  if (!h1 || !article) return;

  var canon = document.querySelector('link[rel="canonical"]');
  var slug = location.pathname.replace(/^\/+|\/+$/g, '').split('/')[0];
  var url = canon && canon.href ? canon.href : 'https://consciousness.ink/' + slug + '/';
  var titleText = h1.textContent.replace(/\s+/g, ' ').trim();

  var ICON_LINK = '<svg aria-hidden="true" viewBox="0 0 16 16" width="15" height="15"><g fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M6.6 9.4a2.9 2.9 0 0 0 4.1 0l2.3-2.3a2.9 2.9 0 0 0-4.1-4.1l-.9.9"/><path d="M9.4 6.6a2.9 2.9 0 0 0-4.1 0L3 8.9a2.9 2.9 0 0 0 4.1 4.1l.9-.9"/></g></svg>';
  var ICON_CHECK = '<svg aria-hidden="true" viewBox="0 0 16 16" width="15" height="15"><path d="M3.2 8.4 6.5 11.6 12.8 4.6" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>';
  var ICON_CHEV = '<svg aria-hidden="true" viewBox="0 0 12 12" width="10" height="10"><path d="M2.5 4.5 6 8l3.5-3.5" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>';

  // ---- plain-text extraction ---------------------------------------------
  var SKIP = 'header.post-header, .essence-label, .x-callout, .tweet-embed, .twitter-tweet, iframe, picture, img, video, audio, figure, svg, script, style, noscript, button, nav, footer, .toc, .sec-at, .tcopy, .hl-pop, .pv-card, [aria-hidden="true"], [hidden]';
  var BLOCK = /^(P|H[1-6]|LI|BLOCKQUOTE|PRE|DIV|ASIDE|SECTION|UL|OL|TABLE|TR|FIGCAPTION|DL|DT|DD)$/;
  function bare(u) { return u.replace(/^https?:\/\//, '').replace(/^www\./, '').replace(/\/$/, ''); }
  function linkText(a) {
    var href = a.href, t = a.textContent.replace(/\s+/g, ' ').trim();
    if (!href || /^javascript:/i.test(href)) return t;
    // a.ref are bracketed stand-ins like [Nov 2026] for a raw link in the original post
    if (a.classList.contains('ref') || !t || bare(t) === bare(href)) return href;
    return t + ' (' + href + ')';
  }
  function inline(node) {
    var out = '';
    node.childNodes.forEach(function (c) {
      if (c.nodeType === 3) out += c.nodeValue;
      else if (c.nodeType !== 1 || c.matches(SKIP)) return;
      else if (c.tagName === 'BR') out += '\n';
      else if (c.tagName === 'A') out += linkText(c);
      else out += inline(c);
    });
    return out;
  }
  function clean(s) { return s.split('\n').map(function (l) { return l.replace(/[ \t\u00a0]+/g, ' ').trim(); }).join('\n').replace(/\n{2,}/g, '\n').trim(); }
  function blocks(node, out) {
    node.childNodes.forEach(function (c) {
      if (c.nodeType === 3) { var t = clean(c.nodeValue); if (t) out.push({ t: t }); return; }
      if (c.nodeType !== 1 || c.matches(SKIP)) return;
      var tag = c.tagName;
      if (tag === 'UL' || tag === 'OL') {
        var items = [], i = 0;
        [].forEach.call(c.children, function (li) {
          if (li.tagName !== 'LI' || li.matches(SKIP)) return;
          var t = clean(inline(li));
          if (t) items.push((tag === 'OL' ? (++i) + '. ' : '- ') + t.replace(/\n/g, '\n  '));
        });
        if (items.length) out.push({ t: items.join('\n') });
        return;
      }
      var hasBlockChild = [].some.call(c.children, function (k) { return BLOCK.test(k.tagName) && !k.matches(SKIP); });
      if (BLOCK.test(tag) && !hasBlockChild) {
        var t = clean(inline(c));
        if (t) out.push({ t: tag === 'BLOCKQUOTE' ? t.replace(/^/gm, '> ') : t });
      } else blocks(c, out);
    });
    return out;
  }
  function plainText() {
    var body = blocks(article, []).map(function (b) { return b.t; });
    return [titleText].concat(body).join('\n\n') + '\n';
  }
  window.__inkPlainText = plainText;

  // ---- clipboard ------------------------------------------------------------
  function fallbackCopy(text) {
    var ta = document.createElement('textarea');
    ta.value = text;
    ta.setAttribute('readonly', '');
    ta.style.cssText = 'position:fixed;top:0;left:0;width:1px;height:1px;opacity:0;';
    document.body.appendChild(ta);
    ta.select();
    var ok = false;
    try { ok = document.execCommand('copy'); } catch (e) {}
    document.body.removeChild(ta);
    return ok;
  }
  function copy(text, cb) {
    if (navigator.clipboard && navigator.clipboard.writeText && window.isSecureContext) {
      navigator.clipboard.writeText(text).then(function () { cb(true); }, function () { cb(fallbackCopy(text)); });
    } else cb(fallbackCopy(text));
  }

  // ---- UI -------------------------------------------------------------------
  // build.py puts an empty <span class="tcopy"> in the h1 so its width is
  // reserved before this runs; create it only if a page lacks it.
  var box = h1.querySelector('.tcopy');
  if (!box) {
    box = document.createElement('span');
    box.className = 'tcopy';
    h1.appendChild(document.createTextNode(' '));
    h1.appendChild(box);
  }
  box.innerHTML =
    '<button type="button" class="tcopy-main" aria-label="Copy link" title="Copy link">' + ICON_LINK + '</button>' +
    '<button type="button" class="tcopy-more" aria-label="More copy options" title="More copy options" aria-haspopup="menu" aria-expanded="false">' + ICON_CHEV + '</button>' +
    '<span class="tcopy-menu" role="menu" aria-label="Copy">' +
      '<button type="button" role="menuitem" tabindex="-1" data-c="link">Copy link</button>' +
      '<button type="button" role="menuitem" tabindex="-1" data-c="title">Copy title</button>' +
      '<button type="button" role="menuitem" tabindex="-1" data-c="text">Copy text</button>' +
    '</span>' +
    '<span class="tcopy-live" aria-live="polite"></span>';

  var main = box.querySelector('.tcopy-main'), more = box.querySelector('.tcopy-more'),
      menu = box.querySelector('.tcopy-menu'), live = box.querySelector('.tcopy-live'),
      items = [].slice.call(menu.querySelectorAll('[role="menuitem"]')), timer = 0;

  function feedback(ok, what) {
    clearTimeout(timer);
    main.innerHTML = ok ? ICON_CHECK : ICON_LINK;
    box.classList.toggle('done', ok);
    live.textContent = ok ? what + ' copied' : 'Copy failed';
    timer = setTimeout(function () { main.innerHTML = ICON_LINK; box.classList.remove('done'); live.textContent = ''; }, 1500);
  }
  function run(kind) {
    var text = kind === 'title' ? titleText : kind === 'text' ? plainText() : url;
    copy(text, function (ok) { feedback(ok, kind === 'title' ? 'Title' : kind === 'text' ? 'Text' : 'Link'); });
  }
  function isOpen() { return box.classList.contains('menu-open'); }
  function openMenu(focusFirst) {
    box.classList.add('menu-open', 'shown');
    more.setAttribute('aria-expanded', 'true');
    menu.style.left = ''; menu.style.right = '';
    // keep it inside the text column (ancestors clip horizontal overflow)
    var r = menu.getBoundingClientRect(),
        edge = Math.min(document.documentElement.clientWidth - 8, h1.getBoundingClientRect().right);
    if (r.right > edge) { menu.style.left = 'auto'; menu.style.right = '0'; }
    if (focusFirst) items[0].focus();
  }
  function closeMenu(focusBack) {
    if (!isOpen()) return;
    box.classList.remove('menu-open');
    more.setAttribute('aria-expanded', 'false');
    if (focusBack) more.focus();
  }

  main.addEventListener('click', function (e) { e.stopPropagation(); closeMenu(); run('link'); });
  more.addEventListener('click', function (e) { e.stopPropagation(); isOpen() ? closeMenu() : openMenu(e.detail === 0); });
  items.forEach(function (b) {
    b.addEventListener('click', function (e) { e.stopPropagation(); run(b.getAttribute('data-c')); closeMenu(true); });
  });
  menu.addEventListener('keydown', function (e) {
    var i = items.indexOf(document.activeElement);
    if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
      e.preventDefault();
      i = e.key === 'ArrowDown' ? (i + 1) % items.length : (i - 1 + items.length) % items.length;
      items[i].focus();
    } else if (e.key === 'Home') { e.preventDefault(); items[0].focus(); }
    else if (e.key === 'End') { e.preventDefault(); items[items.length - 1].focus(); }
    else if (e.key === 'Tab') closeMenu();
  });
  more.addEventListener('keydown', function (e) {
    if (e.key === 'ArrowDown') { e.preventDefault(); openMenu(true); }
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && isOpen()) { e.preventDefault(); closeMenu(true); }
  });

  // Touch: tap the title to reveal; it stays until a tap elsewhere.
  h1.addEventListener('click', function (e) {
    if (box.contains(e.target)) return;
    if (window.getSelection && String(window.getSelection())) return;
    box.classList.add('shown');
  });
  document.addEventListener('click', function (e) {
    if (h1.contains(e.target)) return;
    closeMenu();
    box.classList.remove('shown');
  });
  box.addEventListener('focusout', function () {
    setTimeout(function () { if (!box.contains(document.activeElement)) closeMenu(); }, 0);
  });
})();
