/* Baba Law Firm — photograph alignment tool. Loaded by site.js only when the address ends in ?align=1.
   Drag the photograph inside an arched frame, zoom with the wheel or the slider, then copy the values and
   send them to whoever maintains the site: they go into PHOTOS[...]["place"] in src/site_config.py.
   Nothing is saved by this page. */
(function () {
  'use strict';
  var frame = document.querySelector('.arch-crop');
  var img = frame && frame.querySelector('img');
  if (!img) return;

  function start() {
    var ratio = img.naturalHeight / img.naturalWidth;
    var fr = frame.getBoundingClientRect();
    var ir = img.getBoundingClientRect();
    // State in frame widths: s = picture width, x = left edge, y = top edge.
    var st = { s: ir.width / fr.width, x: (ir.left - fr.left) / fr.width, y: (ir.top - fr.top) / fr.width };
    var first = { s: st.s, x: st.x, y: st.y };
    var frameRatio = fr.height / fr.width;

    var reveal = frame.closest('.reveal');
    if (reveal) reveal.classList.add('is-in');
    frame.style.cursor = 'grab';
    frame.style.touchAction = 'none';
    frame.style.outline = '2px dashed #b08d57';
    frame.style.outlineOffset = '6px';
    img.draggable = false;
    img.style.userSelect = 'none';

    var panel = document.createElement('div');
    panel.setAttribute('style', 'position:fixed;right:16px;bottom:96px;z-index:9999;width:min(340px,calc(100vw - 32px));padding:16px;' +
      'background:#101c2c;color:#f5f2ec;font:14px/1.5 system-ui,sans-serif;border-radius:6px;box-shadow:0 8px 30px rgba(0,0,0,.35)');
    panel.innerHTML =
      '<strong style="display:block;margin-bottom:6px">Align the photograph</strong>' +
      '<span style="display:block;margin-bottom:10px;opacity:.85">Drag the picture to move it. Zoom with the slider or the mouse wheel.</span>' +
      '<label style="display:block;margin-bottom:10px">Zoom <input type="range" min="100" max="200" step="0.1" style="width:100%"></label>' +
      '<textarea readonly rows="2" style="width:100%;box-sizing:border-box;font:12px/1.4 ui-monospace,monospace;background:#0b1420;color:#f5f2ec;border:1px solid #44556b;border-radius:4px;padding:6px;resize:none"></textarea>' +
      '<span data-warn style="display:block;min-height:1.5em;color:#ffb4a2"></span>' +
      '<span style="display:flex;gap:8px;margin-top:6px">' +
      '<button type="button" data-copy style="flex:1;padding:10px;border:0;border-radius:4px;background:#f5f2ec;color:#101c2c;font-weight:600;cursor:pointer">Copy values</button>' +
      '<button type="button" data-reset style="padding:10px 14px;border:1px solid #f5f2ec;border-radius:4px;background:none;color:#f5f2ec;cursor:pointer">Reset</button></span>';
    document.body.appendChild(panel);
    var slider = panel.querySelector('input');
    var out = panel.querySelector('textarea');
    var warn = panel.querySelector('[data-warn]');

    function pct(v) { return (Math.round(v * 10000) / 100).toFixed(2) + '%'; }
    function render() {
      var width = pct(st.s), left = pct(st.x), top = pct(st.y / frameRatio);   // top is a share of the frame's height
      img.style.cssText = 'position:absolute;max-width:none;height:auto;user-select:none;width:' + width + ';left:' + left + ';top:' + top;
      slider.value = String(st.s * 100);
      out.value = 'door: width ' + width + ', left ' + left + ', top ' + top;
      var gap = st.x > 0.0005 || st.y > 0.0005 || st.x + st.s < 0.9995 || st.y + st.s * ratio < frameRatio - 0.0005;
      warn.textContent = gap ? 'The picture no longer fills the frame.' : '';
    }
    function zoom(next, cxFrame, cyFrame) {      // keep the point under (cxFrame, cyFrame) where it is
      next = Math.max(1, Math.min(2, next));
      var k = next / st.s;
      st.x = cxFrame - (cxFrame - st.x) * k;
      st.y = cyFrame - (cyFrame - st.y) * k;
      st.s = next;
      render();
    }

    var drag = null;
    frame.addEventListener('pointerdown', function (e) {
      drag = { px: e.clientX, py: e.clientY, x: st.x, y: st.y, w: frame.getBoundingClientRect().width };
      frame.setPointerCapture(e.pointerId);
      frame.style.cursor = 'grabbing';
      e.preventDefault();
    });
    frame.addEventListener('pointermove', function (e) {
      if (!drag) return;
      st.x = drag.x + (e.clientX - drag.px) / drag.w;
      st.y = drag.y + (e.clientY - drag.py) / drag.w;
      render();
    });
    function end() { drag = null; frame.style.cursor = 'grab'; }
    frame.addEventListener('pointerup', end);
    frame.addEventListener('pointercancel', end);
    frame.addEventListener('wheel', function (e) {
      e.preventDefault();
      var r = frame.getBoundingClientRect();
      zoom(st.s * (e.deltaY < 0 ? 1.01 : 1 / 1.01), (e.clientX - r.left) / r.width, (e.clientY - r.top) / r.width);
    }, { passive: false });
    slider.addEventListener('input', function () { zoom(Number(slider.value) / 100, 0.5, 0.5); });
    panel.querySelector('[data-reset]').addEventListener('click', function () { st = { s: first.s, x: first.x, y: first.y }; render(); });
    panel.querySelector('[data-copy]').addEventListener('click', function (e) {
      var b = e.currentTarget;
      function done() { b.textContent = 'Copied'; setTimeout(function () { b.textContent = 'Copy values'; }, 1500); }
      if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(out.value).then(done, function () { out.select(); });
      else { out.select(); document.execCommand('copy'); done(); }
    });
    render();
    frame.scrollIntoView({ block: 'center' });
  }
  img.loading = 'eager';
  if (img.complete && img.naturalWidth) start(); else img.addEventListener('load', start, { once: true });
})();
