/* Baba Law Firm — site behaviour. No dependencies and no third-party requests
   unless the visitor consents to an optional technology (or loads the map). */
(function () {
  'use strict';

  var doc = document.documentElement;
  window.BLF_READY = true;
  var shotMode = /[?&]shot=1/.test(location.search); // headless screenshots: final state, no banner
  var reduceMotion = shotMode || window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function $(sel, ctx) { return (ctx || document).querySelector(sel); }
  function $$(sel, ctx) { return Array.prototype.slice.call((ctx || document).querySelectorAll(sel)); }
  function store(key, val) {
    try {
      if (val === undefined) return JSON.parse(localStorage.getItem(key));
      localStorage.setItem(key, JSON.stringify(val));
    } catch (e) { return null; }
  }

  var MSG = {
    required: 'This field is required.',
    confirm: 'Please confirm to continue.',
    email: 'Enter an email address in the format name@example.com.',
    tel: 'Enter a telephone number using digits, spaces and an optional +.',
    summary: 'Please correct the following',
    map: 'Map'
  };

  /* ---------- Year ---------- */
  $$('[data-year]').forEach(function (el) { el.textContent = String(new Date().getFullYear()); });

  /* ---------- Header: solid after scrolling past the hero; hides on the way down ---------- */
  var header = $('[data-header]');
  if (header) {
    var overlay = header.classList.contains('is-overlay');
    var lastY = window.scrollY;
    var onScroll = function () {
      var y = window.scrollY;
      if (overlay) header.classList.toggle('is-solid', y > 40);
      if (!doc.classList.contains('menu-open')) {
        header.classList.toggle('is-hidden', y > 480 && y > lastY + 4);
        if (y < lastY - 4) header.classList.remove('is-hidden');
      }
      lastY = y;
    };
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
    header.addEventListener('focusin', function () { header.classList.remove('is-hidden'); });
  }

  /* ---------- Mobile menu (modal, focus-trapped, Esc to close) ---------- */
  var menu = $('[data-menu]');
  var openBtn = $('[data-menu-open]');
  var closeBtn = $('[data-menu-close]');
  function focusables(ctx) {
    return $$('a[href], button:not([disabled]), input:not([disabled]), select, textarea, [tabindex]:not([tabindex="-1"])', ctx)
      .filter(function (el) { return el.offsetParent !== null; });
  }
  function openMenu() {
    menu.hidden = false;
    menu.classList.add('is-open');
    doc.classList.add('menu-open');
    openBtn.setAttribute('aria-expanded', 'true');
    (closeBtn || focusables(menu)[0]).focus();
  }
  function closeMenu(returnFocus) {
    menu.classList.remove('is-open');
    menu.hidden = true;
    doc.classList.remove('menu-open');
    openBtn.setAttribute('aria-expanded', 'false');
    if (returnFocus !== false) openBtn.focus();
  }
  if (menu && openBtn) {
    openBtn.addEventListener('click', openMenu);
    if (closeBtn) closeBtn.addEventListener('click', function () { closeMenu(); });
    menu.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') { e.preventDefault(); closeMenu(); return; }
      if (e.key !== 'Tab') return;
      var f = focusables(menu);
      if (!f.length) return;
      var first = f[0], last = f[f.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    });
    $$('a', menu).forEach(function (a) { a.addEventListener('click', function () { closeMenu(false); }); });
    window.addEventListener('resize', function () { if (!menu.hidden && window.matchMedia('(min-width: 1024px)').matches) closeMenu(false); });
  }

  /* ---------- Consent ----------
     The optional categories come from the build (body[data-optional]); with none,
     there is no banner and Cookie Settings shows the register only.
     Contract: nothing optional loads before an explicit "true" for its category. */
  var OPTIONAL = (document.body.getAttribute('data-optional') || '').split(',').filter(Boolean);
  var CONSENT_KEY = 'blf-consent-v2';
  var banner = $('[data-cookie-banner]');
  var dialog = $('[data-cookie-dialog]');
  var consent = store(CONSENT_KEY);
  if (consent && OPTIONAL.some(function (k) { return !(k in consent); })) consent = null; // new category: ask again

  var loaders = {
    analytics: function () {
      /* Load the chosen analytics tool here, only after consent. */
      if (typeof window.BLF_LOAD_ANALYTICS === 'function') window.BLF_LOAD_ANALYTICS();
    },
    maps: function () { $$('[data-map]').forEach(loadMap); }
  };
  var loaded = {};
  function applyConsent(c) {
    OPTIONAL.forEach(function (k) {
      doc.setAttribute('data-consent-' + k, c && c[k] ? 'granted' : 'denied');
      if (c && c[k] && !loaded[k] && loaders[k]) { loaded[k] = true; loaders[k](); }
    });
  }
  function saveConsent(c) {
    c.ts = new Date().toISOString();
    consent = c;
    store(CONSENT_KEY, c);
    if (banner) banner.hidden = true;
    applyConsent(c);
  }
  function all(v) { var c = {}; OPTIONAL.forEach(function (k) { c[k] = v; }); return c; }
  function openSettings() {
    $$('[data-consent-toggle]').forEach(function (input) {
      input.checked = !!(consent && consent[input.getAttribute('data-consent-toggle')]);
    });
    if (dialog && typeof dialog.showModal === 'function') dialog.showModal();
  }

  if (OPTIONAL.length && !consent && banner && !shotMode) banner.hidden = false;
  applyConsent(consent);

  document.addEventListener('click', function (e) {
    var t = e.target.closest('[data-consent], [data-cookie-settings]');
    if (!t) return;
    if (t.hasAttribute('data-cookie-settings')) { e.preventDefault(); openSettings(); return; }
    var action = t.getAttribute('data-consent');
    if (action === 'accept') saveConsent(all(true));
    if (action === 'reject') saveConsent(all(false));
    if (action === 'save') {
      var c = all(false);
      $$('[data-consent-toggle]').forEach(function (i) { c[i.getAttribute('data-consent-toggle')] = i.checked; });
      saveConsent(c);
    }
  });

  /* ---------- Map: loads only on request (or with Maps consent) ---------- */
  function loadMap(box) {
    if (!box || box.dataset.loaded) return;
    var iframe = document.createElement('iframe');
    iframe.src = box.getAttribute('data-map-src');
    iframe.title = box.getAttribute('data-map-title') || MSG.map;
    iframe.loading = 'lazy';
    iframe.referrerPolicy = 'no-referrer-when-downgrade';
    iframe.setAttribute('allowfullscreen', '');
    box.innerHTML = '';
    box.appendChild(iframe);
    box.dataset.loaded = 'true';
    box.classList.add('is-loaded');
  }
  $$('[data-map-load]').forEach(function (b) {
    b.addEventListener('click', function () { loadMap(b.closest('[data-map]')); });
  });

  /* ---------- Enquiry form: accessible validation, then submission ---------- */
  function control(field) { return $('input:not([type="hidden"]), textarea, select', field); }
  function validateField(field) {
    var input = control(field);
    if (!input) return true;
    var err = $('.field-error', field);
    var msg = '';
    var v = input.type === 'checkbox' ? input.checked : input.value.trim();
    if (input.required && !v) msg = input.type === 'checkbox' ? MSG.confirm : MSG.required;
    if (!msg && input.type === 'email' && v && !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v)) msg = MSG.email;
    if (!msg && input.type === 'tel' && v && !/^[+()\d\s.-]{6,}$/.test(v)) msg = MSG.tel;
    field.classList.toggle('is-invalid', !!msg);
    input.setAttribute('aria-invalid', msg ? 'true' : 'false');
    if (err) err.textContent = msg;
    return !msg;
  }

  $$('form[data-form]').forEach(function (form) {
    var summary = $('[data-error-summary]', form);
    var fields = $$('.field', form);
    fields.forEach(function (field) {
      var input = control(field);
      if (!input) return;
      input.addEventListener('blur', function () { if (field.classList.contains('is-invalid') || (input.type !== 'checkbox' && input.value)) validateField(field); });
      input.addEventListener('change', function () { if (field.classList.contains('is-invalid')) validateField(field); });
    });
    function show(id) {
      var el = document.getElementById(id);
      form.hidden = true;
      if (el) { el.hidden = false; el.focus(); }
    }
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var invalid = fields.filter(function (f) { return !validateField(f); });
      if (invalid.length) {
        if (summary) {
          summary.innerHTML = '';
          var h = document.createElement('p');
          h.className = 'error-summary-title';
          h.textContent = MSG.summary;
          var ul = document.createElement('ul');
          invalid.forEach(function (f) {
            var i = control(f);
            var li = document.createElement('li');
            var a = document.createElement('a');
            a.href = '#' + i.id;
            a.textContent = (f.getAttribute('data-label') || i.name) + ': ' + $('.field-error', f).textContent;
            a.addEventListener('click', function (ev) { ev.preventDefault(); i.focus(); });
            li.appendChild(a);
            ul.appendChild(li);
          });
          summary.appendChild(h);
          summary.appendChild(ul);
          summary.hidden = false;
          summary.focus();
        } else {
          control(invalid[0]).focus();
        }
        return;
      }
      if (summary) summary.hidden = true;
      var hp = $('.hp input', form);
      if (hp && hp.value) return; // bot
      var endpoint = form.getAttribute('data-endpoint');
      if (!endpoint) { show(form.getAttribute('data-success')); return; } // preview: nothing is sent
      var button = $('button[type="submit"]', form);
      if (button) button.disabled = true;
      fetch(endpoint, { method: 'POST', body: new FormData(form), headers: { 'Accept': 'application/json' } })
        .then(function (r) { if (!r.ok) throw new Error(String(r.status)); show(form.getAttribute('data-success')); })
        .catch(function () {
          if (button) button.disabled = false;
          var fail = document.getElementById('enquiry-failure');
          if (fail) { fail.hidden = false; fail.focus(); }      // the form stays, so the visitor can retry
        });
    });
  });

  /* ---------- Reveal on scroll (restrained) ---------- */
  var revealEls = $$('.reveal, .reveal-stagger');
  if (!reduceMotion && 'IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('is-in'); io.unobserve(en.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    revealEls.forEach(function (el) { io.observe(el); });
  } else {
    revealEls.forEach(function (el) { el.classList.add('is-in'); });
  }
})();
