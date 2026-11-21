// One bottom tab bar for every BettorDays page that is not the home app (grade, bonuses, legal).
// Same tabs, same order, same look as the home page: Board, Grader, Proof, Me (Nov 20: "it should all be one app").
(function () {
  if (document.querySelector('.bdt-bar')) return;
  const path = location.pathname.replace(/\/$/, '') || '/';
  const on = t => (t === 'grade' && /^\/grade/.test(path)) ? ' on' : '';
  const css = `
  .bdt-bar{display:none}
  @media (max-width:900px){
    body{padding-bottom:calc(78px + env(safe-area-inset-bottom,0px))}
    .bdt-bar{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));align-items:start;position:fixed;left:0;right:0;bottom:0;z-index:45;background:rgba(8,12,10,.96);backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px);border-top:1px solid #1f2724;padding:6px max(6px,env(safe-area-inset-left,0px)) calc(6px + env(safe-area-inset-bottom,0px))}
    .bdt-bar a,.bdt-bar button{display:flex;flex-direction:column;align-items:center;gap:3px;padding:6px 2px;background:none;border:0;color:#8a9a93;font:600 10px 'Geist Mono',ui-monospace,monospace;letter-spacing:.04em;text-transform:uppercase;text-decoration:none;cursor:pointer;min-width:0;white-space:nowrap}
    .bdt-bar i{font-style:normal;font-size:21px;line-height:1;filter:grayscale(1);opacity:.75;width:30px;height:30px;display:grid;place-items:center}
    .bdt-bar .on{color:#04ff9f}.bdt-bar .on i{filter:none;opacity:1}
    .bdt-bar .post i{background:#04ff9f;border-radius:50%;filter:none;opacity:1}
    .bdt-bar a:focus-visible,.bdt-bar button:focus-visible{outline:2px solid #04ff9f;outline-offset:-2px}
    header.top nav{display:none}
  }
  .bdt-sheet{position:fixed;inset:0;z-index:60;background:rgba(0,0,0,.55);backdrop-filter:blur(3px)}
  .bdt-sheet[hidden]{display:none}
  .bdt-sheet .in{position:absolute;left:0;right:0;bottom:0;background:#111513;border-top:1px solid #04ff9f;padding:18px max(16px,env(safe-area-inset-left,0px)) calc(18px + env(safe-area-inset-bottom,0px));display:grid;grid-template-columns:1fr 1fr;gap:8px;max-height:80vh;overflow:auto}
  .bdt-sheet .in a{display:flex;align-items:center;gap:10px;padding:16px 14px;border:1px solid #1f2724;background:rgba(255,255,255,.02);color:#eef3f0;font:600 15px Geist,system-ui,sans-serif;text-decoration:none}
  .bdt-sheet .lbl{grid-column:1/-1;font:600 11px 'Geist Mono',monospace;letter-spacing:.12em;text-transform:uppercase;color:#04ff9f}`;
  const st = document.createElement('style'); st.textContent = css; document.head.appendChild(st);
  const bar = document.createElement('nav'); bar.className = 'bdt-bar'; bar.setAttribute('aria-label', 'App');
  bar.innerHTML = `<a href="/"><i>🎯</i>Board</a><a class="post${on('grade')}" href="/grade"${on('grade') ? ' aria-current="page"' : ''}><i>📸</i>Grader</a><a href="/record"><i>📈</i>Proof</a><button type="button" aria-haspopup="dialog"><i>👤</i>Me</button>`;
  const sh = document.createElement('div'); sh.className = 'bdt-sheet'; sh.hidden = true;
  sh.innerHTML = `<div class="in" role="dialog" aria-label="Me"><span class="lbl">Me</span>
    <a href="/app#/me" style="color:#04ff9f">👤 Profile and invites <small style="opacity:.6">· account</small></a><a href="/board">📋 Full board and top 25</a>
    <a href="/research">🔬 Research lab</a><a href="/app#/board">➕ Pick &amp; post <small style="opacity:.6">· account</small></a>
    <a href="/history">🗂 Past nights</a><a href="/results">🧾 Older recaps</a>
    <a href="/method">🧠 How it works</a><a href="/bonuses">🎁 Sign-up offers</a>
    <a href="/app#/leaders">🏆 Leaderboard <small style="opacity:.6">· account</small></a><a href="/app#/feed">🎟 Feed <small style="opacity:.6">· account</small></a>
    <a href="/app#/chat">💬 Chat <small style="opacity:.6">· account</small></a><a href="/founders">⭐ Founders list</a>
    <a href="/legal">📄 Terms and privacy</a><a href="/#talk">✋ Talk to Ace</a></div>`;
  bar.querySelector('button').onclick = () => { sh.hidden = false; };
  sh.onclick = e => { if (e.target === sh || e.target.closest('a')) sh.hidden = true; };
  document.addEventListener('keydown', e => { if (e.key === 'Escape') sh.hidden = true; });
  const mount = () => { document.body.appendChild(bar); document.body.appendChild(sh); };
  if (document.body) mount(); else document.addEventListener('DOMContentLoaded', mount);
  // the same desktop links as the home page
  const top = document.querySelector('header.top nav');
  if (top) top.innerHTML = '<a href="/">Board</a><a href="/grade">Grader</a><a href="/record">Proof</a><a href="/research">Research lab</a><a href="/method">How it works</a>';
})();
