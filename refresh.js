/* BettorDays: keep the installed app fresh.
   Home-screen apps have no refresh button, so this does three things:
   1. When the app comes back to the screen, it checks /version.json. If a new build is out and you
      are not in the middle of a slip, it reloads right away.
   2. While the app is open it checks every 60 seconds. If there is a new build, it shows a
      "New picks are up" bar to tap, so it never yanks the page while you are reading or building.
   3. In the installed app only, pull down from the top of the page to refresh, like a normal app.
   Never blocks the site: any failure just does nothing. */
(function () {
  var d = document, w = window;
  var meta = d.querySelector('meta[name="bd-version"]');
  var mine = meta ? meta.getAttribute('content') : null;
  if (!mine) return;
  var standalone = (w.matchMedia && matchMedia('(display-mode: standalone)').matches) || navigator.standalone === true;
  var busy = function () {
    var a = d.activeElement;
    return !!d.querySelector('.ez.on') || (a && /INPUT|TEXTAREA|SELECT/.test(a.tagName));
  };
  var reload = function () { try { w.location.reload(); } catch (e) {} };

  var css = '.bdr{position:fixed;left:50%;transform:translateX(-50%);top:calc(env(safe-area-inset-top,0px) + 10px);z-index:95;' +
    'background:#04ff9f;color:#04130c;font:700 14px/1.2 system-ui,-apple-system,sans-serif;padding:11px 16px;border:0;' +
    'box-shadow:0 6px 24px rgba(4,255,159,.35);max-width:calc(100vw - 32px);cursor:pointer}' +
    '.bdr[hidden]{display:none}' +
    '.bdp{position:fixed;left:50%;top:calc(env(safe-area-inset-top,0px) + 6px);z-index:94;transform:translate(-50%,-60px);' +
    'background:#151917;color:#04ff9f;border:1px solid #04ff9f;font:600 12px/1 system-ui,-apple-system,sans-serif;' +
    'letter-spacing:.06em;text-transform:uppercase;padding:9px 13px;transition:transform .15s ease;pointer-events:none}';
  var st = d.createElement('style'); st.textContent = css; d.head.appendChild(st);
  var bar = d.createElement('button'); bar.type = 'button'; bar.className = 'bdr'; bar.hidden = true;
  bar.textContent = 'New picks are up · Tap to refresh';
  bar.onclick = reload;
  d.body.appendChild(bar);

  var checking = false;
  function check(autoReload) {
    if (checking || !w.fetch) return;
    checking = true;
    fetch('/version.json?t=' + Date.now(), { cache: 'no-store' }).then(function (r) { return r.ok ? r.json() : null; })
      .then(function (j) {
        checking = false;
        if (!j || !j.v || j.v === mine) return;
        if (autoReload && !busy()) reload(); else bar.hidden = false;
      }).catch(function () { checking = false; });
  }

  d.addEventListener('visibilitychange', function () { if (d.visibilityState === 'visible') check(true); });
  w.addEventListener('pageshow', function (e) { if (e.persisted) check(true); });
  w.addEventListener('focus', function () { check(true); });
  setInterval(function () { if (d.visibilityState === 'visible') check(false); }, 60000);

  /* pull to refresh, installed app only (browsers already have their own) */
  if (!standalone) return;
  var pill = d.createElement('div'); pill.className = 'bdp'; pill.textContent = 'Pull to refresh'; d.body.appendChild(pill);
  var y0 = null, dy = 0, LIMIT = 90;
  d.addEventListener('touchstart', function (e) {
    y0 = (w.scrollY <= 0 && e.touches.length === 1) ? e.touches[0].clientY : null; dy = 0;
  }, { passive: true });
  d.addEventListener('touchmove', function (e) {
    if (y0 === null) return;
    dy = e.touches[0].clientY - y0;
    if (dy <= 0 || w.scrollY > 0) { pill.style.transform = 'translate(-50%,-60px)'; return; }
    var p = Math.min(dy, LIMIT * 1.4);
    pill.style.transform = 'translate(-50%,' + (p * 0.6 - 50) + 'px)';
    pill.textContent = dy >= LIMIT ? 'Release to refresh' : 'Pull to refresh';
  }, { passive: true });
  d.addEventListener('touchend', function () {
    if (y0 !== null && dy >= LIMIT && w.scrollY <= 0) { pill.textContent = 'Refreshing…'; reload(); return; }
    pill.style.transform = 'translate(-50%,-60px)'; y0 = null; dy = 0;
  }, { passive: true });
})();
