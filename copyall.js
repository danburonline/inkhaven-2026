/* "Copy all text" on the home page: copies meditations.txt (every published
   meditation as plain text, written by tools/build.py) to the clipboard. */
(function () {
  var btn = document.querySelector('.copy-all');
  if (!btn) return;
  var label = btn.querySelector('.copy-all-label');
  var status = document.querySelector('.copy-all-status');
  var src = btn.getAttribute('data-src') || '/meditations.txt';
  var idle = label.textContent, timer = 0, busy = false;
  var ICON_COPY = btn.querySelector('svg').outerHTML;
  var ICON_CHECK = '<svg aria-hidden="true" viewBox="0 0 16 16" width="14" height="14"><path d="M3.2 8.4 6.5 11.6 12.8 4.6" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>';
  btn.hidden = false;

  function fetchText() {
    return fetch(src, { cache: 'no-cache' }).then(function (r) {
      if (!r.ok) throw new Error('HTTP ' + r.status);
      return r.text();
    });
  }
  function legacyCopy(text) {
    var ta = document.createElement('textarea');
    ta.value = text; ta.setAttribute('readonly', ''); ta.setAttribute('aria-hidden', 'true');
    ta.style.cssText = 'position:fixed;top:0;left:0;opacity:0;pointer-events:none';
    document.body.appendChild(ta); ta.select();
    var ok = false;
    try { ok = document.execCommand('copy'); } catch (e) {}
    document.body.removeChild(ta);
    if (!ok) throw new Error('copy failed');
  }
  function copy() {
    var cb = navigator.clipboard;
    // the text is handed over as a promise, so the copy still counts as part
    // of the click (Safari needs that) while the file downloads
    if (cb && cb.write && window.ClipboardItem) {
      var p = fetchText();
      return cb.write([new ClipboardItem({ 'text/plain': p.then(function (t) { return new Blob([t], { type: 'text/plain' }); }) })]);
    }
    return fetchText().then(function (t) {
      if (cb && cb.writeText) return cb.writeText(t).catch(function () { legacyCopy(t); });
      legacyCopy(t);
    });
  }
  function show(state, text) {
    clearTimeout(timer);
    label.textContent = text;
    btn.classList.toggle('done', state === 'done');
    btn.classList.toggle('fail', state === 'fail');
    var svg = btn.querySelector('svg');
    svg.outerHTML = state === 'done' ? ICON_CHECK : ICON_COPY;
    status.textContent = state === 'idle' ? '' : text;
    if (state !== 'idle') timer = setTimeout(function () { show('idle', idle); }, 2500);
  }
  btn.addEventListener('click', function () {
    if (busy) return;
    busy = true; btn.setAttribute('aria-busy', 'true');
    var done = function () { busy = false; btn.removeAttribute('aria-busy'); };
    copy().then(function () { show('done', 'Copied'); done(); },
                function () { show('fail', 'Could not copy'); done(); });
  });
})();
