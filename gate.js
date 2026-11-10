// 5 minute free preview, then a free account is required. Signed-in members never see the timer.
(function () {
  const sb = window.BD_SB;
  const PREVIEW = 300;
  const css = `
  .bdg-pill{position:fixed;left:16px;bottom:16px;z-index:60;display:flex;align-items:center;gap:10px;background:rgba(11,13,12,.92);border:1px solid #1f2724;padding:9px 12px;font:500 12px/1 'Geist Mono',monospace;letter-spacing:.08em;text-transform:uppercase;color:#8a9a93;backdrop-filter:blur(8px)}
  .bdg-pill b{color:#04ff9f;font-weight:700}
  .bdg-pill a,.bdg-pill button{background:#04ff9f;color:#0b0d0c;border:0;padding:7px 10px;font:700 11px/1 'Geist Mono',monospace;letter-spacing:.1em;text-transform:uppercase;cursor:pointer;text-decoration:none}
  @media (max-width:560px){.bdg-pill{bottom:76px;left:12px}}
  .bdg-wall{position:fixed;inset:0;z-index:100;display:none;align-items:center;justify-content:center;padding:16px;background:rgba(6,8,7,.72);backdrop-filter:blur(14px)}
  .bdg-wall.on{display:flex}
  .bdg-card{width:100%;max-width:440px;max-height:calc(100vh - 32px);overflow:auto;background:#0f1311;border:1px solid #04ff9f;box-shadow:0 0 60px rgba(4,255,159,.18);padding:26px 24px;color:#eef3f0;font-family:Geist,system-ui,sans-serif}
  .bdg-card h2{font:900 34px/1 Kanit,sans-serif;text-transform:uppercase;margin:0 0 8px}
  .bdg-card h2{display:block!important;padding:0!important;border:0!important}
  .bdg-card h2::before,.bdg-card h2::after{display:none!important;content:none!important}
  .bdg-card h2 span{color:#04ff9f}
  .bdg-card p{color:#8a9a93;font-size:14px;line-height:1.5;margin:0 0 14px}
  .bdg-tabs{display:flex;gap:6px;margin:6px 0 16px}
  .bdg-tabs button{flex:1;background:none;border:1px solid #1f2724;color:#8a9a93;padding:10px;font:700 12px 'Geist Mono',monospace;letter-spacing:.1em;text-transform:uppercase;cursor:pointer}
  .bdg-tabs button.on{border-color:#04ff9f;color:#04ff9f}
  .bdg-card label{display:block;font:500 11px 'Geist Mono',monospace;letter-spacing:.12em;text-transform:uppercase;color:#8a9a93;margin:10px 0 5px}
  .bdg-card input[type=email],.bdg-card input[type=password],.bdg-card input[type=text],.bdg-card input[type=tel]{width:100%;background:#0b0d0c;border:1px solid #1f2724;color:#eef3f0;padding:11px 12px;font:15px Geist,sans-serif;outline:none}
  .bdg-card input:focus{border-color:#04ff9f}
  .bdg-chk{display:flex!important;gap:10px;align-items:flex-start;text-transform:none!important;letter-spacing:0!important;font:14px/1.4 Geist,sans-serif!important;color:#c8d3ce!important;margin:12px 0 0!important;cursor:pointer}
  .bdg-chk input{margin-top:3px;accent-color:#04ff9f}
  .bdg-go{width:100%;margin-top:18px;background:#04ff9f;color:#0b0d0c;border:0;padding:14px;font:900 18px Kanit,sans-serif;text-transform:uppercase;letter-spacing:.04em;cursor:pointer}
  .bdg-go:disabled{opacity:.5;cursor:wait}
  .bdg-msg{min-height:20px;margin-top:10px;font-size:13px}
  .bdg-msg.bad{color:#ff4d5e}.bdg-msg.ok{color:#04ff9f}
  .bdg-hint{font-size:12px;color:#5b6b64;margin-top:4px}
  .bdg-link{background:none;border:0;color:#8a9a93;text-decoration:underline;cursor:pointer;font-size:13px;padding:0;margin-top:10px}
  .bdg-joke{border-left:2px solid #04ff9f;padding:8px 12px;background:rgba(4,255,159,.05);font-size:13px;color:#c8d3ce;margin:0 0 14px}
  `;
  const st = document.createElement('style'); st.textContent = css; document.head.appendChild(st);

  const pill = document.createElement('div'); pill.className = 'bdg-pill'; pill.setAttribute('role', 'status');
  const wall = document.createElement('div'); wall.className = 'bdg-wall'; wall.setAttribute('role', 'dialog'); wall.setAttribute('aria-modal', 'true'); wall.setAttribute('aria-labelledby', 'bdgT');
  wall.innerHTML = `<div class="bdg-card">
    <h2 id="bdgT">Welcome to the <span>family</span></h2>
    <p>Your free preview is up. Make a free account to keep using the board, the grades and every tool. Still free. Always free.</p>
    <div class="bdg-joke">Relax, we're not stealing your data. We're stealing your weekends. Your email gets picks and updates, nothing else, and we never sell it.</div>
    <div class="bdg-tabs" role="tablist"><button type="button" class="on" data-t="join" role="tab">Join free</button><button type="button" data-t="login" role="tab">Log in</button></div>
    <form id="bdgJoin" novalidate>
      <label for="bdgE">Email</label><input id="bdgE" type="email" autocomplete="email" required>
      <label for="bdgP">Password</label><input id="bdgP" type="password" autocomplete="new-password" minlength="8" required><div class="bdg-hint">8+ characters</div>
      <label for="bdgU">Username</label><input id="bdgU" type="text" autocomplete="username" maxlength="20" required><div class="bdg-hint" id="bdgUH">3 to 20 letters, numbers or _</div>
      <label for="bdgPh">Phone (optional)</label><input id="bdgPh" type="tel" autocomplete="tel" maxlength="25">
      <label class="bdg-chk"><input type="checkbox" id="bdgAge" required> I'm 21 or older.</label>
      <label class="bdg-chk"><input type="checkbox" id="bdgOpt" checked> Send me picks, results and BettorDays updates. Unsubscribe anytime.</label>
      <button class="bdg-go" type="submit">Join the family</button>
    </form>
    <form id="bdgLogin" novalidate hidden>
      <label for="bdgLE">Email</label><input id="bdgLE" type="email" autocomplete="email" required>
      <label for="bdgLP">Password</label><input id="bdgLP" type="password" autocomplete="current-password" required>
      <button class="bdg-go" type="submit">Log in</button>
      <button class="bdg-link" type="button" id="bdgForgot">Forgot password?</button>
    </form>
    <div class="bdg-msg" id="bdgM" aria-live="polite"></div>
  </div>`;

  const store = {
    get(k) { try { return localStorage.getItem(k); } catch (e) { return null; } },
    set(k, v) { try { localStorage.setItem(k, v); } catch (e) {} }
  };
  const $ = id => wall.querySelector('#' + id);
  const msg = (t, ok) => { const m = $('bdgM'); m.textContent = t; m.className = 'bdg-msg ' + (ok ? 'ok' : 'bad'); };

  function mount() { document.body.appendChild(pill); document.body.appendChild(wall); }
  function lock() { wall.classList.add('on'); document.documentElement.style.overflow = 'hidden'; setTimeout(() => $('bdgE').focus(), 50); }

  wall.querySelector('.bdg-tabs').onclick = e => {
    const b = e.target.closest('button'); if (!b) return;
    wall.querySelectorAll('.bdg-tabs button').forEach(x => x.classList.toggle('on', x === b));
    $('bdgJoin').hidden = b.dataset.t !== 'join'; $('bdgLogin').hidden = b.dataset.t !== 'login'; msg('', 1);
  };

  let ut;
  $('bdgU').addEventListener('input', () => {
    clearTimeout(ut); const u = $('bdgU').value.trim().toLowerCase(); const h = $('bdgUH');
    if (!/^[a-z0-9_]{3,20}$/.test(u)) { h.textContent = '3 to 20 letters, numbers or _'; h.style.color = ''; return; }
    ut = setTimeout(async () => { const { data } = await sb.rpc('username_available', { u }); h.textContent = data ? '@' + u + ' is open' : '@' + u + ' is taken'; h.style.color = data ? '#04ff9f' : '#ff4d5e'; }, 350);
  });

  $('bdgJoin').onsubmit = async e => {
    e.preventDefault();
    const email = $('bdgE').value.trim(), password = $('bdgP').value, username = $('bdgU').value.trim().toLowerCase(), phone = $('bdgPh').value.trim();
    if (!/^\S+@\S+\.\S+$/.test(email)) return msg('Enter a real email.');
    if (password.length < 8) return msg('Password needs 8+ characters.');
    if (!/^[a-z0-9_]{3,20}$/.test(username)) return msg('Username: 3 to 20 letters, numbers or _.');
    if (!$('bdgAge').checked) return msg('You have to be 21+ to join.');
    const btn = $('bdgJoin').querySelector('.bdg-go'); btn.disabled = true;
    const { data: free } = await sb.rpc('username_available', { u: username });
    if (!free) { btn.disabled = false; return msg('That username is taken.'); }
    const { data, error } = await sb.auth.signUp({ email, password, options: { emailRedirectTo: location.origin + '/app', data: { username, phone, age_confirmed: true, email_opt_in: $('bdgOpt').checked } } });
    btn.disabled = false;
    if (error) return msg(/rate limit/i.test(error.message) ? 'Too many sign ups right now. Wait a few minutes and try again.' : error.message);
    if (data.session) { location.href = '/app#welcome'; return; }
    msg('Almost in. Check your email and tap the confirm link, then log in.', 1);
  };
  $('bdgLogin').onsubmit = async e => {
    e.preventDefault();
    const btn = $('bdgLogin').querySelector('.bdg-go'); btn.disabled = true;
    const { error } = await sb.auth.signInWithPassword({ email: $('bdgLE').value.trim(), password: $('bdgLP').value });
    btn.disabled = false;
    if (error) return msg(error.message === 'Email not confirmed' ? 'Confirm your email first. Check your inbox.' : error.message);
    location.reload();
  };
  $('bdgForgot').onclick = async () => {
    const email = $('bdgLE').value.trim(); if (!email) return msg('Type your email above first.');
    const { error } = await sb.auth.resetPasswordForEmail(email, { redirectTo: location.origin + '/app#reset' });
    msg(error ? error.message : 'Reset link sent. Check your email.', !error);
  };

  async function start() {
    mount();
    const { data: { session } } = await sb.auth.getSession();
    if (session) {
      const { data: p } = await sb.from('profiles').select('username').eq('id', session.user.id).maybeSingle();
      pill.innerHTML = `<span>Member <b>@${p ? p.username : 'you'}</b></span><a href="/app">Open the app</a>`;
      return;
    }
    let t0 = +store.get('bd_preview_start');
    if (!t0) { t0 = Date.now(); store.set('bd_preview_start', String(t0)); }
    const tick = () => {
      const left = Math.max(0, PREVIEW - Math.floor((Date.now() - t0) / 1000));
      const mm = Math.floor(left / 60), ss = String(left % 60).padStart(2, '0');
      pill.innerHTML = `<span>Free preview <b>${mm}:${ss}</b></span><button type="button" id="bdgJoinNow">Join free</button>`;
      pill.querySelector('#bdgJoinNow').onclick = lock;
      if (left === 0) { clearInterval(iv); lock(); }
    };
    const iv = setInterval(tick, 1000); tick();
    if (/[?&]join=1/.test(location.search)) lock();
  }
  sb.auth.onAuthStateChange((ev) => { if (ev === 'SIGNED_IN' && wall.classList.contains('on')) location.reload(); });
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start); else start();
})();
