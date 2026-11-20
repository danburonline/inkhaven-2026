/* Post menu (click the N/30 in a post title) and the home page filter. */
(function () {
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }

  // Home page filter
  var input = document.querySelector('.filter');
  if (input) {
    var items = [].slice.call(document.querySelectorAll('.post-list li'));
    var none = document.querySelector('.no-match');
    input.addEventListener('input', function () {
      var q = input.value.trim().toLowerCase(), shown = 0;
      items.forEach(function (li) {
        var hit = !q || q.split(/\s+/).every(function (w) { return li.getAttribute('data-search').indexOf(w) !== -1; });
        li.hidden = !hit; if (hit) shown++;
      });
      if (none) none.hidden = shown !== 0;
    });
    var sort = document.querySelector('.sort'), list = document.querySelector('.post-list');
    if (sort && list) sort.addEventListener('change', function () {
      var k = sort.value, key = k === 'new' || k === 'old' ? 'data-n' : 'data-words', dir = k === 'old' || k === 'short' ? 1 : -1;
      items.slice().sort(function (a, b) { return dir * (+a.getAttribute(key) - +b.getAttribute(key)); })
        .forEach(function (li) { list.appendChild(li); });
    });
  }

  // Post title menu
  var btn = document.querySelector('.num-menu');
  if (!btn) return;
  var wrap = btn.parentNode, pop = null, dim = null;
  var here = location.pathname.replace(/\/+$/, '').split('/').pop();
  function ensureDim() {
    if (dim) return dim;
    dim = document.createElement('div');
    dim.className = 'num-menu-dim';
    dim.setAttribute('aria-hidden', 'true');
    document.body.appendChild(dim);
    dim.addEventListener('click', function () { close(); });
    return dim;
  }
  var coarse = window.matchMedia('(hover: none), (pointer: coarse)');
  var input2 = null, none2 = null;
  function build(posts) {
    pop = document.createElement('div');
    pop.className = 'num-menu-pop';
    pop.setAttribute('role', 'menu');
    pop.innerHTML = '<div class="nm-head" id="nm-head">All meditations</div>' +
      '<input class="nm-filter" type="search" placeholder="Filter by title, number or date" aria-label="Filter meditations" autocomplete="off" spellcheck="false">' +
      posts.map(function (p) {
      var cur = p.slug === here;
      var search = (p.n + '/30 ' + p.short + ' ' + p.date).toLowerCase();
      return '<a role="menuitem" href="/' + p.slug + '/" data-search="' + esc(search) + '"' + (cur ? ' class="current" aria-current="page"' : '') + '>' +
        '<span class="nm-n">' + p.n + '/30</span><span class="nm-t">' + esc(p.short) + '</span>' +
        '<span class="nm-d">' + esc(p.date.replace(/ \d{4}$/, '')) + ' &middot; ' + p.words.toLocaleString('en') + ' words' +
        (cur ? '<span class="nm-now"> &middot; Reading</span>' : '') + '</span></a>';
    }).join('') + '<p class="nm-none" hidden>No matches</p>' +
      '<a class="nm-all" role="menuitem" href="/">View all on the home page</a>';
    wrap.appendChild(pop);
    input2 = pop.querySelector('.nm-filter');
    none2 = pop.querySelector('.nm-none');
    input2.addEventListener('input', filter);
    input2.addEventListener('keydown', function (e) {
      if (e.key === 'Enter') {
        e.preventDefault();
        var first = visible()[0];
        if (first && !first.classList.contains('nm-all')) location.href = first.href;
      } else if (e.key === 'Escape' && input2.value) {
        e.preventDefault(); e.stopPropagation();
        input2.value = ''; filter();
      }
    });
  }
  function filter() {
    var q = input2.value.trim().toLowerCase(), shown = 0;
    [].forEach.call(pop.querySelectorAll('a[data-search]'), function (a) {
      var hit = !q || q.split(/\s+/).every(function (w) { return a.getAttribute('data-search').indexOf(w) !== -1; });
      a.hidden = !hit; if (hit) shown++;
    });
    none2.hidden = shown !== 0;
  }
  function visible() { return [].slice.call(pop.querySelectorAll('a')).filter(function (a) { return !a.hidden; }); }
  function open() {
    if (!pop) return;
    ensureDim();
    dim.classList.add('on');
    wrap.classList.add('open'); btn.setAttribute('aria-expanded', 'true');
    // desktop: focus the filter; touch: don't pop the keyboard, focus the current post
    if (!coarse.matches && input2) { input2.focus({ preventScroll: true }); return; }
    var c = pop.querySelector('.current') || pop.querySelector('a'); if (c) c.focus({ preventScroll: true });
  }
  function close(focus) {
    wrap.classList.remove('open');
    if (dim) dim.classList.remove('on');
    btn.setAttribute('aria-expanded', 'false');
    if (input2 && input2.value) { input2.value = ''; filter(); }
    if (focus) btn.focus();
  }
  btn.addEventListener('click', function (e) { e.stopPropagation(); wrap.classList.contains('open') ? close() : open(); });
  document.addEventListener('click', function (e) { if (pop && !pop.contains(e.target)) close(); });
  document.addEventListener('keydown', function (e) {
    if (!wrap.classList.contains('open')) return;
    if (e.key === 'Escape') { close(true); return; }
    if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
      e.preventDefault();
      var links = [input2].concat(visible()), i = links.indexOf(document.activeElement);
      if (i === -1) i = 0;
      i = e.key === 'ArrowDown' ? (i + 1) % links.length : (i - 1 + links.length) % links.length;
      links[i].focus();
    }
  });
  fetch('/posts.json?v=a4fac6c87a').then(function (r) { if (!r.ok) throw r; return r.json(); }).then(build).catch(function () {});
})();
