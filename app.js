// Mobile nav toggle + simple lightbox for gallery images.
(function () {
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.querySelector('.site-nav');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }

  // Lightbox: only for real (loaded) images, not pending placeholders.
  var lb = document.createElement('div');
  lb.className = 'lb';
  lb.innerHTML = '<button class="lb-close" aria-label="Close">&times;</button><img alt="">';
  document.body.appendChild(lb);
  var lbImg = lb.querySelector('img');
  var closeBtn = lb.querySelector('.lb-close');

  function open(src, alt) {
    lbImg.src = src; lbImg.alt = alt || '';
    lb.classList.add('open');
    document.body.style.overflow = 'hidden';
  }
  function close() {
    lb.classList.remove('open'); lbImg.src = '';
    document.body.style.overflow = '';
  }
  document.addEventListener('click', function (e) {
    var fig = e.target.closest ? e.target.closest('.work') : null;
    if (fig && !fig.classList.contains('pending')) {
      var img = fig.querySelector('.frame img');
      if (img && img.src) open(img.src, img.alt);
    }
  });
  closeBtn.addEventListener('click', close);
  lb.addEventListener('click', function (e) { if (e.target === lb) close(); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') close(); });

  // Generative art: load the interactive iframe only when the viewer hits Play.
  document.querySelectorAll('.gen-stage[data-src]').forEach(function (stage) {
    var btn = stage.querySelector('.gen-play');
    if (!btn) return;
    btn.addEventListener('click', function () {
      if (stage.classList.contains('playing')) return;
      var f = document.createElement('iframe');
      f.src = stage.getAttribute('data-src');
      f.title = stage.getAttribute('data-title') || 'Interactive artwork';
      f.setAttribute('allow', 'fullscreen; accelerometer; gyroscope');
      f.setAttribute('allowfullscreen', '');
      f.setAttribute('sandbox', 'allow-scripts allow-same-origin allow-pointer-lock allow-fullscreen');
      stage.appendChild(f);
      stage.classList.add('playing');
    });
  });
})();
