/* Baba Law Firm — site behaviour. No dependencies, no third-party requests
   until the visitor consents (analytics) or clicks (map). */
(function () {
  'use strict';

  var doc = document.documentElement;
  window.BLF_READY = true;
  var shotMode = /[?&]shot=1/.test(location.search); // headless screenshots: final state, no banner
  if (shotMode && window.parent !== window) {        // report page height to the review-pack harness
    window.addEventListener('load', function () {
      setTimeout(function () {
        window.parent.postMessage({ blfHeight: document.body.scrollHeight, blfPath: location.pathname }, '*');
      }, 400);
    });
  }
  var reduceMotion = shotMode || window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function $(sel, ctx) { return (ctx || document).querySelector(sel); }
  function $$(sel, ctx) { return Array.prototype.slice.call((ctx || document).querySelectorAll(sel)); }
  function store(key, val) {
    try {
      if (val === undefined) return JSON.parse(localStorage.getItem(key));
      localStorage.setItem(key, JSON.stringify(val));
    } catch (e) { return null; }
  }

  /* ---------- Messages ---------- */
  var MSG = {
    required: 'This field is required.',
    confirm: 'Please confirm to continue.',
    cvMissing: 'Please attach your CV.',
    email: 'Enter an email address in the format name@example.com.',
    tel: 'Enter a telephone number using digits, spaces and an optional +.',
    cvType: 'Your CV must be a PDF, DOC or DOCX file.',
    cvSize: 'Your CV must be smaller than 5 MB.',
    summary: 'Please correct the following',
    map: 'Map'
  };

  /* ---------- Year ---------- */
  $$('[data-year]').forEach(function (el) { el.textContent = String(new Date().getFullYear()); });

  /* ---------- Header: solid after scrolling past the hero ---------- */
  var header = $('[data-header]');
  if (header) {
    var overlay = header.classList.contains('is-overlay');
    var lastY = window.scrollY;
    var onScroll = function () {
      var y = window.scrollY;
      if (overlay) header.classList.toggle('is-solid', y > 40);
      // Hide on scroll down, show on scroll up (only once well past the top).
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
    var current = $('[aria-current="page"]', menu) || focusables(menu)[0];
    (closeBtn || current).focus();
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
     Production: replace with the chosen consent plugin (WP Consent API) and
     Site Kit. The contract stays the same: Google Analytics must not load
     before an explicit "analytics: true". */
  var CONSENT_KEY = 'blf-consent-v1';
  var banner = $('[data-cookie-banner]');
  var dialog = $('[data-cookie-dialog]');
  var consent = store(CONSENT_KEY);

  function applyConsent(c) {
    doc.dataset.consentAnalytics = c && c.analytics ? 'granted' : 'denied';
    doc.dataset.consentMaps = c && c.maps ? 'granted' : 'denied';
    if (c && c.analytics) loadAnalytics();
    if (c && c.maps) $$('[data-map]').forEach(loadMap);
  }
  function saveConsent(c) {
    c.ts = new Date().toISOString();
    consent = c;
    store(CONSENT_KEY, c);
    if (banner) banner.hidden = true;
    applyConsent(c);
  }
  var analyticsLoaded = false;
  function loadAnalytics() {
    if (analyticsLoaded) return;
    analyticsLoaded = true;
    /* Design build: no request is made. In production Site Kit injects
       gtag.js (GA4) here, only after consent. */
    if (window.console) console.info('[consent] Analytics granted — GA4 (Site Kit) would load now.');
  }
  function syncToggles() {
    $$('[data-consent-toggle]').forEach(function (input) {
      input.checked = !!(consent && consent[input.getAttribute('data-consent-toggle')]);
    });
  }
  function openPreferences() {
    syncToggles();
    if (dialog && typeof dialog.showModal === 'function') dialog.showModal();
  }

  if (!consent && banner && !shotMode) banner.hidden = false;
  applyConsent(consent);

  document.addEventListener('click', function (e) {
    var t = e.target.closest('[data-consent], [data-cookie-settings]');
    if (!t) return;
    if (t.hasAttribute('data-cookie-settings')) { e.preventDefault(); openPreferences(); return; }
    var action = t.getAttribute('data-consent');
    if (action === 'accept') saveConsent({ analytics: true, maps: !!(consent && consent.maps) });
    if (action === 'reject') saveConsent({ analytics: false, maps: false });
    if (action === 'save') {
      var c = {};
      $$('[data-consent-toggle]').forEach(function (i) { c[i.getAttribute('data-consent-toggle')] = i.checked; });
      saveConsent(c);
    }
  });

  /* ---------- Map: loads only on click (or with Maps consent) ---------- */
  function loadMap(box) {
    if (!box || box.dataset.loaded) return;
    var src = box.getAttribute('data-map-src');
    var iframe = document.createElement('iframe');
    iframe.src = src;
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

  /* ---------- Forms: accessible validation + demo submission ---------- */
  var MAX_CV = 5 * 1024 * 1024;
  var CV_TYPES = /\.(pdf|doc|docx)$/i;

  function validateField(field) {
    var input = $('input, textarea, select', field);
    if (!input || input.type === 'hidden') return true;
    var err = $('.field-error', field);
    var msg = '';
    var v = input.type === 'file' ? input.files : (input.type === 'checkbox' ? input.checked : input.value.trim());
    if (input.required) {
      if (input.type === 'checkbox' && !v) msg = field.getAttribute('data-msg-required') || MSG.confirm;
      else if (input.type === 'file' && (!v || !v.length)) msg = MSG.cvMissing;
      else if (input.type !== 'checkbox' && input.type !== 'file' && !v) msg = field.getAttribute('data-msg-required') || MSG.required;
    }
    if (!msg && input.type === 'email' && v && !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v)) msg = MSG.email;
    if (!msg && input.type === 'tel' && v && !/^[+()\d\s.-]{6,}$/.test(v)) msg = MSG.tel;
    if (!msg && input.type === 'file' && v && v.length) {
      if (!CV_TYPES.test(v[0].name)) msg = MSG.cvType;
      else if (v[0].size > MAX_CV) msg = MSG.cvSize;
    }
    field.classList.toggle('is-invalid', !!msg);
    input.setAttribute('aria-invalid', msg ? 'true' : 'false');
    if (err) err.textContent = msg;
    return !msg;
  }

  $$('form[data-form]').forEach(function (form) {
    var summary = $('[data-error-summary]', form);
    $$('.field', form).forEach(function (field) {
      var input = $('input, textarea, select', field);
      if (!input) return;
      input.addEventListener('blur', function () { if (field.classList.contains('is-invalid') || input.value) validateField(field); });
      input.addEventListener('change', function () { if (field.classList.contains('is-invalid')) validateField(field); });
    });
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var hp = $('.hp input', form);
      var invalid = $$('.field', form).filter(function (f) { return !validateField(f); });
      if (invalid.length) {
        if (summary) {
          var list = invalid.map(function (f) {
            var i = $('input, textarea, select', f);
            var label = f.getAttribute('data-label') || ($('label', f) ? $('label', f).textContent.replace(/\s+/g, ' ').trim() : i.name);
            return '<li><a href="#' + i.id + '">' + label + ': ' + $('.field-error', f).textContent + '</a></li>';
          }).join('');
          summary.innerHTML = '<h3>' + MSG.summary + '</h3><ul>' + list + '</ul>';
          summary.hidden = false;
          summary.focus();
        } else {
          $('input, textarea, select', invalid[0]).focus();
        }
        return;
      }
      if (summary) summary.hidden = true;
      if (hp && hp.value) return; // bot
      /* Design build: nothing is sent. Production: the form plugin emails the
         submission (info@ / careers@) behind reCAPTCHA and sends the
         automatic confirmation. */
      var success = document.getElementById(form.getAttribute('data-success'));
      form.hidden = true;
      if (success) { success.hidden = false; success.focus(); }
    });
  });

  /* ---------- Reveal on scroll ---------- */
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
