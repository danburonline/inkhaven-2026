/* Full-screen image viewer for article images */
(function () {
  var imgs = document.querySelectorAll('article img:not(.pv-img)');
  if (!imgs.length) return;
  var box, big, scrollY = 0, lastFocus = null, viaKey = false;

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
  function build() {
    box = document.createElement('div');
    box.className = 'lb';
    box.setAttribute('role', 'dialog');
    box.setAttribute('aria-modal', 'true');
    box.innerHTML = '<button class="lb-close" type="button" aria-label="Close">&times;</button><img class="lb-img" alt="">';
    big = box.querySelector('.lb-img');
    box.addEventListener('click', function (e) { if (e.target !== big) close(); });
    box.querySelector('.lb-close').addEventListener('click', close);
    box.addEventListener('touchmove', function (e) { e.preventDefault(); }, { passive: false });
    document.body.appendChild(box);
  }
  function open(img, key) {
    if (!box) build();
    viaKey = !!key;
    lastFocus = img;
    big.src = img.currentSrc || img.src;
    big.alt = img.alt || '';
    lock();
    box.classList.add('on');
    box.querySelector('.lb-close').focus({ preventScroll: true });
  }
  function close() {
    if (!box || !box.classList.contains('on')) return;
    box.classList.remove('on');
    unlock();
    if (viaKey && lastFocus) lastFocus.focus({ preventScroll: true });
    else if (document.activeElement) document.activeElement.blur();
  }
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') close(); });
  imgs.forEach(function (img) {
    img.classList.add('zoomable');
    img.setAttribute('tabindex', '0');
    img.setAttribute('role', 'button');
    img.addEventListener('click', function (e) { e.preventDefault(); open(img, false); });
    img.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); open(img, true); } });
  });
})();
