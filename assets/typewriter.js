// typewriter.js -- types out .hero-statement's text node-by-node so any
// inline markup inside it (e.g. the emphasised close) survives untouched.
(function () {
  // Fenced divs wrap their content in a <p> -- type into that, not the div,
  // so the caret lands inline after the text instead of on its own line.
  var el = document.querySelector('.hero-statement > p') || document.querySelector('.hero-statement');
  if (!el) return;

  var reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;

  // Snapshot the original child nodes (text + elements) before clearing.
  var nodes = Array.prototype.map.call(el.childNodes, function (n) {
    return { node: n, text: n.textContent };
  });
  if (reduce || !nodes.length) return;

  nodes.forEach(function (entry) { entry.node.textContent = ''; });

  var caret = document.createElement('span');
  caret.className = 'caret';
  el.appendChild(caret);

  var flat = [];
  nodes.forEach(function (entry, i) {
    for (var c = 0; c < entry.text.length; c++) {
      flat.push({ node: entry.node, ch: entry.text[c] });
    }
  });

  var i = 0;
  var speed = 32;
  function step() {
    if (i >= flat.length) return;
    flat[i].node.textContent += flat[i].ch;
    i++;
    setTimeout(step, speed + Math.random() * 40);
  }
  setTimeout(step, 300);
})();
