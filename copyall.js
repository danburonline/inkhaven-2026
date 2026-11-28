/* Home intro: "clicking here" copies meditations.txt (every published
   meditation as plain text, written by tools/build.py) to the clipboard. */
(function () {
  var link = document.querySelector('a.copy-all');
  if (!link) return;
  var status = document.querySelector('.copy-all-status');
  var src = link.getAttribute('href') || '/meditations.txt';
  var idle = link.textContent;
  var idleLabel = link.getAttribute('aria-label') || idle;
  var timer = 0, busy = false;

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
    link.textContent = state === 'idle' ? idle : text;
    link.classList.toggle('done', state === 'done');
    link.classList.toggle('fail', state === 'fail');
    if (status) status.textContent = state === 'idle' ? '' : text;
    if (state === 'idle') link.setAttribute('aria-label', idleLabel);
    else link.setAttribute('aria-label', text);
    if (state !== 'idle') timer = setTimeout(function () { show('idle', idle); }, 2500);
  }
  link.addEventListener('click', function (e) {
    if (e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
    e.preventDefault();
    if (busy) return;
    busy = true; link.setAttribute('aria-busy', 'true');
    var done = function () { busy = false; link.removeAttribute('aria-busy'); };
    copy().then(function () { show('done', 'Copied'); done(); },
                function () { show('fail', 'Could not copy'); done(); });
  });
})();
