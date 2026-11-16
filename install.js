/* BettorDays: Add to Home Screen walkthrough. Self-contained. Never blocks the site. */
(function () {
  var d = document, ua = navigator.userAgent || '';
  var standalone = (window.matchMedia && matchMedia('(display-mode: standalone)').matches) || navigator.standalone === true;

  /* head tags, so the saved icon and full-screen mode work */
  function tag(name, attrs) { var e = d.createElement(name); for (var k in attrs) e.setAttribute(k, attrs[k]); d.head.appendChild(e); }
  if (!d.querySelector('link[rel="manifest"]')) tag('link', { rel: 'manifest', href: '/manifest.webmanifest' });
  if (!d.querySelector('link[rel="apple-touch-icon"]')) tag('link', { rel: 'apple-touch-icon', href: '/apple-touch-icon.png' });
  if (!d.querySelector('link[rel="icon"]')) tag('link', { rel: 'icon', type: 'image/png', href: '/icon-192.png' });
  [['apple-mobile-web-app-capable', 'yes'], ['mobile-web-app-capable', 'yes'], ['apple-mobile-web-app-title', 'BettorDays'],
   ['apple-mobile-web-app-status-bar-style', 'black'], ['theme-color', '#0b0d0c']].forEach(function (m) {
    if (!d.querySelector('meta[name="' + m[0] + '"]')) tag('meta', { name: m[0], content: m[1] });
  });
  if (standalone) return;

  var isIOS = /iPhone|iPad|iPod/.test(ua) || (/Macintosh/.test(ua) && navigator.maxTouchPoints > 1);
  var isAndroid = /Android/.test(ua);
  var inApp = /Instagram|FBAN|FBAV|FB_IAB|Twitter|TikTok|musical_ly|Snapchat|Line\/|LinkedInApp/i.test(ua);
  var iosOther = isIOS && /CriOS|FxiOS|EdgiOS/.test(ua);
  var mobile = isIOS || isAndroid;
  var deferred = null;
  window.addEventListener('beforeinstallprompt', function (e) { e.preventDefault(); deferred = e; });
  window.addEventListener('appinstalled', function () { close(); set('bd_inst', 'done'); });

  function get(k) { try { return localStorage.getItem(k); } catch (e) { return null; } }
  function set(k, v) { try { localStorage.setItem(k, v); } catch (e) {} }

  var css = '.bdi{position:fixed;inset:0;z-index:90;background:rgba(0,0,0,.62);backdrop-filter:blur(4px);display:flex;align-items:flex-end;justify-content:center}' +
    '.bdi[hidden]{display:none}' +
    '.bdi .c{width:100%;max-width:480px;background:#101412;border-top:2px solid #04ff9f;color:#eef3f0;padding:20px 18px calc(22px + env(safe-area-inset-bottom,0px));font:400 15px/1.45 Geist,system-ui,sans-serif;animation:bdiu .28s cubic-bezier(.2,.8,.2,1)}' +
    '@keyframes bdiu{from{transform:translateY(24px);opacity:0}to{transform:none;opacity:1}}' +
    '@media (prefers-reduced-motion:reduce){.bdi .c{animation:none}}' +
    '.bdi .top{display:flex;align-items:center;gap:12px;margin-bottom:10px}' +
    '.bdi .top img{width:52px;height:52px;border-radius:12px;border:1px solid #1f2724}' +
    '.bdi h3{margin:0;font:900 22px/1.05 Kanit,system-ui,sans-serif;letter-spacing:.01em;text-transform:uppercase}' +
    '.bdi .sub{margin:2px 0 0;color:#8a9a93;font-size:13.5px}' +
    '.bdi ol{list-style:none;margin:14px 0 16px;padding:0;display:grid;gap:8px}' +
    '.bdi li{display:grid;grid-template-columns:30px 1fr;gap:10px;align-items:center;border:1px solid #1f2724;background:rgba(255,255,255,.02);padding:11px 12px}' +
    '.bdi li b.n{display:grid;place-items:center;width:28px;height:28px;background:#04ff9f;color:#06110c;font:700 13px "Geist Mono",ui-monospace,monospace}' +
    '.bdi li span b{color:#04ff9f;font-weight:600}' +
    '.bdi .ic{display:inline-block;vertical-align:-4px;margin:0 2px}' +
    '.bdi .row{display:grid;gap:8px}' +
    '.bdi button{font:600 15px Geist,system-ui,sans-serif;padding:13px;border:1px solid #1f2724;background:transparent;color:#8a9a93;cursor:pointer;width:100%}' +
    '.bdi button.go{background:#04ff9f;border-color:#04ff9f;color:#06110c}' +
    '.bdi .why{color:#8a9a93;font-size:12.5px;margin:10px 0 0;text-align:center}';
  var st = d.createElement('style'); st.textContent = css; d.head.appendChild(st);

  var share = '<svg class="ic" width="18" height="20" viewBox="0 0 18 20" fill="none" stroke="#04ff9f" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 13V2M5 5.5 9 1.8l4 3.7M4 9H2.5v9.2h13V9H14"/></svg>';
  var plus = '<svg class="ic" width="18" height="18" viewBox="0 0 18 18" fill="none" stroke="#04ff9f" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><rect x="1.5" y="1.5" width="15" height="15" rx="3"/><path d="M9 5.5v7M5.5 9h7"/></svg>';

  function steps() {
    if (inApp) return ['Tap the <b>••• menu</b> at the top or bottom of this screen.',
      'Choose <b>Open in ' + (isIOS ? 'Safari' : 'Chrome') + '</b>. Apps like Instagram can\'t save a site to your phone.',
      'Then open <b>More</b> and tap <b>Add to Home Screen</b> to finish.'];
    if (iosOther) return ['Tap the <b>Share</b> button ' + share + ' next to the address bar.',
      'Scroll down and tap <b>Add to Home Screen</b> ' + plus + '.',
      'Tap <b>Add</b>. If you don\'t see it, open bettordays.xyz in <b>Safari</b>.'];
    if (isIOS) return ['Tap the <b>Share</b> button ' + share + ' at the bottom of Safari.',
      'Scroll down and tap <b>Add to Home Screen</b> ' + plus + '.',
      'Tap <b>Add</b> in the top corner. BettorDays is now on your phone.'];
    if (isAndroid) return ['Tap the <b>⋮ menu</b> in the top corner of Chrome.',
      'Tap <b>Add to Home screen</b> or <b>Install app</b>.',
      'Tap <b>Install</b>. BettorDays is now on your phone.'];
    return ['On your phone, open <b>bettordays.xyz</b> in Safari or Chrome.',
      'Tap <b>Share</b> (iPhone) or the <b>⋮ menu</b> (Android).',
      'Tap <b>Add to Home Screen</b>.'];
  }

  var box = null;
  function open() {
    if (!box) {
      box = d.createElement('div'); box.className = 'bdi'; box.hidden = true;
      box.setAttribute('role', 'dialog'); box.setAttribute('aria-modal', 'true'); box.setAttribute('aria-label', 'Add BettorDays to your home screen');
      box.addEventListener('click', function (e) {
        if (e.target === box || e.target.getAttribute('data-bdi') === 'x') { close(); set('bd_inst', String(Date.now())); }
        if (e.target.getAttribute('data-bdi') === 'go' && deferred) {
          deferred.prompt(); deferred.userChoice.then(function () { deferred = null; close(); set('bd_inst', String(Date.now())); });
        }
      });
      d.body.appendChild(box);
    }
    var s = steps(), can = !!deferred;
    box.innerHTML = '<div class="c"><div class="top"><img src="/icon-192.png" alt="" width="52" height="52"><div><h3>Make it an app</h3>' +
      '<p class="sub">Put BettorDays on your home screen. Takes 10 seconds.</p></div></div>' +
      (can ? '' : '<ol>' + s.map(function (t, i) { return '<li><b class="n">' + (i + 1) + '</b><span>' + t + '</span></li>'; }).join('') + '</ol>') +
      '<div class="row">' + (can ? '<button class="go" type="button" data-bdi="go" style="margin-top:14px">Install BettorDays</button>' : '') +
      '<button type="button" data-bdi="x">' + (can ? 'Not now' : 'Got it') + '</button></div>' +
      '<p class="why">Opens full screen, one tap from your home screen. Free.</p></div>';
    box.hidden = false;
  }
  function close() { if (box) box.hidden = true; }
  window.bdInstall = open;

  /* a row in the More sheet, on both the site and the app */
  function addRow() {
    var host = d.querySelector('#moreSheet .in') || (d.getElementById('mTour') && d.getElementById('mTour').parentElement);
    if (!host || host.querySelector('[data-bdi-row]')) return;
    var b = d.createElement('button'); b.type = 'button'; b.setAttribute('data-bdi-row', '1'); b.textContent = '📲 Add to Home Screen';
    b.style.borderColor = '#04ff9f';
    b.addEventListener('click', function () { var sh = b.closest('.sheet'); if (sh) sh.hidden = true; open(); });
    host.appendChild(b);
  }

  /* show once on phones, after the tour and never on top of another popup; ask again after 7 days */
  function busy() {
    var fb = d.getElementById('fbWrap');
    if (fb && !fb.hidden) return true;
    var sheets = d.querySelectorAll('.sheet');
    for (var i = 0; i < sheets.length; i++) if (!sheets[i].hidden) return true;
    return !!d.querySelector('.tbox,.tring,#gate:not([hidden])');
  }
  function auto(tries) {
    var last = get('bd_inst');
    if (last === 'done' || (last && Date.now() - +last < 7 * 864e5)) return;
    if (!get('bd_tour') && !get('bd_app_tour') && tries < 20) return void setTimeout(function () { auto(tries + 1); }, 3000);
    if (busy() && tries < 20) return void setTimeout(function () { auto(tries + 1); }, 3000);
    if (busy()) return;
    open();
  }
  function init() { addRow(); setTimeout(addRow, 1500); if (mobile) setTimeout(function () { auto(0); }, 6000); }
  if (d.readyState === 'loading') d.addEventListener('DOMContentLoaded', init); else init();
})();
