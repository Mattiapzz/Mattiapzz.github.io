/* reveal.js — photo ⇄ artwork reveal.
   Markup: <div class="reveal soft" data-reveal="pointer"> img + .art + .seam
   Modes:  pointer | scroll | drag
   Drag, keyboard and reduced-motion handling are automatic. */
(function () {
  var reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;

  function set(el, p) {
    p = Math.max(0, Math.min(100, p));
    el.style.setProperty('--r', p + '%');
    el.setAttribute('aria-valuenow', Math.round(p));
  }

  document.querySelectorAll('[data-reveal]').forEach(function (el) {
    var mode = el.dataset.reveal || 'pointer', dragging = false;

    function fromEvent(e) {
      var r = el.getBoundingClientRect();
      var x = (e.touches ? e.touches[0].clientX : e.clientX) - r.left;
      set(el, x / r.width * 100);
    }

    if (mode === 'pointer' && matchMedia('(hover: hover)').matches) {
      el.addEventListener('mousemove', fromEvent);
      el.addEventListener('mouseleave', function () { set(el, 50); });
    } else if (mode === 'scroll') {
      var onScroll = function () {
        var r = el.getBoundingClientRect();
        var p = 1 - (r.top + r.height) / (innerHeight + r.height);
        set(el, p * 130 - 15);            // full sweep before it leaves view
      };
      addEventListener('scroll', onScroll, { passive: true });
      addEventListener('resize', onScroll);
      onScroll();
    }

    if (mode !== 'scroll') {               // drag works for pointer mode too
      var start = function (e) { dragging = true; el.classList.add('dragging'); fromEvent(e); };
      var move  = function (e) { if (dragging) { fromEvent(e); e.preventDefault(); } };
      var end   = function () { dragging = false; el.classList.remove('dragging'); };
      el.addEventListener('mousedown', start);
      el.addEventListener('touchstart', start, { passive: true });
      addEventListener('mousemove', move);
      addEventListener('touchmove', move, { passive: false });
      addEventListener('mouseup', end);
      addEventListener('touchend', end);
    }

    el.addEventListener('keydown', function (e) {
      var n = parseFloat(el.getAttribute('aria-valuenow'));
      if (e.key === 'ArrowLeft')  { set(el, n - 5); e.preventDefault(); }
      if (e.key === 'ArrowRight') { set(el, n + 5); e.preventDefault(); }
      if (e.key === 'Home') set(el, 0);
      if (e.key === 'End')  set(el, 100);
    });

    if (reduce && mode === 'scroll') set(el, 50);
  });
})();
