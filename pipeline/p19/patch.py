import re
F='bettordays-hq.html'; s=open(F).read()
def rep(a,b,cnt=1):
  global s
  n=s.count(a); assert n==cnt,(n,a[:80]); s=s.replace(a,b)
# CSS
rep('/* popup v2 */','''.tbg{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:8px;width:100%}.tbg div{border:1px solid var(--line);padding:8px 10px}.tbg small{display:block;font-family:var(--mono);font-size:10.5px;color:var(--mute);letter-spacing:.04em;text-transform:uppercase}.tbg b{font-family:var(--display);font-size:24px;color:var(--fg)}
@media (max-width:560px){.tbg{grid-template-columns:repeat(2,minmax(0,1fr))}}
.tbnote{margin:8px 0 0;font-size:12.5px;color:var(--mute)}.tbw{margin:8px 0 0;padding-left:18px;font-size:13px;color:var(--warn);display:grid;gap:4px}
.ezbar{flex-direction:column;align-items:stretch}.ezbar .top{display:flex;align-items:center;gap:12px;flex-wrap:wrap}.ezbar .t{min-width:0}
.ez .kp{position:static;transform:none;display:inline-block;margin-left:6px}
.rbig{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:8px;margin:8px 0}.rbig div{border:1px solid var(--line);padding:12px}.rbig small{display:block;font-family:var(--mono);font-size:11px;color:var(--mute);text-transform:uppercase;letter-spacing:.05em}.rbig b{font-family:var(--display);font-size:32px;color:var(--acc)}
@media (max-width:560px){.rbig{grid-template-columns:repeat(2,minmax(0,1fr))}}
#recT{overflow-x:auto}#recT .tbl{min-width:560px}
.wl{border:1px solid var(--acc);background:rgba(4,255,159,.05);padding:18px;margin-top:18px}.wl form{display:grid;gap:8px;max-width:440px}.wl label.ck{display:flex;gap:8px;align-items:flex-start;font-size:13px;color:var(--mute)}
/* popup v2 */''')
# Ticket builder section
a=s.index('  <section class="panel" id="easy">'); b=s.index('</section>',a)+len('</section>')
s=s[:a]+'''  <section class="panel" id="easy">
    <div class="dayhead"><span class="lbl" id="ezTag">Ticket builder</span><h2 class="big">Build your ticket.</h2>
    <p class="proof">Tap 2 to 8 legs from the board. You see our grade, our real record at that grade, Kalshi's price, an estimated payout, and every warning. BettorDays never places bets. Check your slip before you lock anything.</p></div>
    <div class="easy" id="easyList"></div>
    <div class="ezbar" id="ezBar"><div class="top"><div class="big" id="ezN">0 legs</div><button class="btn on" id="ezCopy" type="button" disabled>Copy ticket</button><button class="btn" id="ezClear" type="button" disabled>Clear</button></div><div class="t" id="ezT">Tap legs to build a ticket.</div></div>
  </section>
  <section class="panel" id="record">
    <div class="dayhead"><span class="lbl acc">Record explorer</span><h2 class="big">Every graded leg. Filter it any way.</h2>
    <p class="proof">Stack filters across sport, grade, prop type, over or under, Kalshi agreement, week and line type. Each group can take more than one choice. You always see wins, losses, sample size and the likely range, so a hot streak on 12 legs doesn't look like proof.</p>
    <p class="note" id="recMeta">Loading the record...</p></div>
    <div class="bfil" id="recF"></div>
    <div id="recS"></div><div id="recT"></div>
  </section>
  <section class="panel" id="founders">
    <div class="dayhead"><span class="lbl acc">Founders list</span><h2 class="big">Get in before it's paid.</h2>
    <p class="proof">BettorDays is free while we build it in public. When paid plans open, the founders list hears first and gets the founders price. No card needed to join. <span class="mono" id="wlCount"></span></p></div>
    <div class="wl"><form id="wlForm" autocomplete="on">
      <input class="fin" name="email" type="email" maxlength="200" placeholder="Email" required autocomplete="email">
      <input class="fin" name="name" maxlength="80" placeholder="Name (optional)" autocomplete="name">
      <input class="fin" name="handle" maxlength="60" placeholder="Instagram or X handle (optional)">
      <input type="text" name="website" tabindex="-1" autocomplete="off" class="hp" aria-hidden="true">
      <label class="ck"><input type="checkbox" name="age" required> I'm 21 or older. I understand picks are not guarantees.</label>
      <button class="btn on" type="submit" style="padding:12px">Join the founders list</button>
      <p class="mono" id="wlMsg" style="font-size:12px;margin:4px 0 0;min-height:1em" aria-live="polite"></p>
    </form></div>
  </section>'''+s[b:]
# home CTA
rep('  <section class="panel" id="easy">','''  <section class="panel" data-pg="home" style="padding-top:0"><div class="wl" style="display:flex;gap:12px;align-items:center;flex-wrap:wrap;justify-content:space-between"><div><span class="lbl acc">Founders list</span><p style="margin:4px 0 0">Free for now. Join the list to lock the founders price when paid plans open.</p></div><a class="btn on" data-go="founders" href="/founders">Join free</a></div></section>
  <section class="panel" id="easy">''')
# router
rep("const MAP={drop:'off',","const MAP={drop:'off',record:'record',founders:'founders',")
rep("const PAGES=['home','easy','research','history','results','method'];","const PAGES=['home','easy','research','history','results','method','record','founders'];")
# nav
rep('<a data-go="easy" href="/easy"><i>✌️</i>Tap 3</a>','<a data-go="easy" href="/easy"><i>🧩</i>Build</a>')
rep('data-go="easy" href="/easy">Tap 3</a>','data-go="easy" href="/easy">Ticket builder</a>')
rep('<a data-go="results" href="/results">📈 Results</a>','<a data-go="record" href="/record">📊 Record explorer</a><a data-go="founders" href="/founders">⭐ Founders list</a><a data-go="results" href="/results">📈 Results</a>')
rep("['.tabbar [data-go=\"easy\"]','Tap 3','The easy way: tap any 3 picks from the 70 pool and play them.']","['.tabbar [data-go=\"easy\"]','Build','Build a ticket from the board. See our grade, Kalshi, the payout and every warning.']")
rep("if(et)et.textContent='Tap 3 · '+BOARD.label+(graded?' · results in':'');","if(et)et.textContent='Ticket builder · '+BOARD.label+(graded?' · results in':'');")
# builder JS
a=s.index(' // tap 3\n'); b=s.index(" draw();setInterval(()=>{if(only)draw()},60000);\n",a)+len(" draw();setInterval(()=>{if(only)draw()},60000);\n")
s=s[:a]+open('p19/builder.js').read()+s[b:]
# current board combinable filters
a=s.index(" let F='all',SP='all',TM='any';const L=[['all','All'],['70','70%+'],['clean','Clean (no flags)'],['move','Moved lines'],['ml','Moneylines'],['prop','Props'],['reg','Regular lines'],['alt','Alts'],['flag','Flagged']];\n const fe=document.getElementById('thuF')")
b=s.index("const ok=x=>BF.pass(x)",a); b=s.index('\n',b)+1
s=s[:a]+open('p19/board.js').read()+s[b:]
a=s.index("document.getElementById('thuT').innerHTML=")
s=s[:a]+"{const N0=document.getElementById('thuN');if(N0)N0.textContent=`Showing ${r.length} of ${CUR.length} picks. Filters stack, so 80+ and NBA and Kalshi within 7 shows only legs that pass all three.`}"+s[a:]
a=s.index(" fe.onclick=e=>{const b=e.target.closest('button');if(!b)return;F=b.dataset.f;",a); b=s.index('\n',a)
s=s[:a]+" fe.onclick=e=>{const b=e.target.closest('button[data-g]');if(!b)return;G[b.dataset.g]=b.dataset.v;drawF();draw()};draw();})();"+s[b:]
# record + waitlist scripts before </body> or at end
s=s.replace('<script>\n/* Deep Research:',open('p19/record.js').read()+'<script>\n/* Deep Research:',1)
# Hammer rule note in the Kalshi legend
rep("so think twice before putting one in a parlay. Prices move, so check the slip.","so they are not used in Hammer tickets while we test this on the full record. Prices move, so check the slip.")
open(F,'w').write(s); print('patched')
