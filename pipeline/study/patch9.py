import json,re
p='bettordays-hq.html'; h=open(p).read()
nov8=json.load(open('study/nov8.json')); pend=json.load(open('study/nov8_pending.json'))
def rep(old,new):
    global h
    assert old in h, old[:90]
    h=h.replace(old,new,1)
# ROWS rebuild
m=re.search(r'const ROWS=(\[.*?\]);\n',h,re.S)
rows=json.load(open('study/rows.json'))+nov8
h=h[:m.start()]+'const ROWS='+json.dumps(rows,separators=(',',':'))+';\n'+h[m.end():]
# RES rebuild
res={r['pick']:('W' if r['hit'] else 'L') for r in nov8}
for pp,_ in pend: res[pp]='TBD'
mres=re.search(r"const RES=\{.*?\};",h); h=h[:mres.start()]+'const RES='+json.dumps(res)+';'+h[mres.end():]
# numbers
rep('Process audit · Nov 4 to 8 · 278 graded legs','Process audit · Nov 4 to 8 · 295 graded legs')
rep('<span data-count="51">0</span>/60</b><small>85% across 5 days</small>','<span data-count="52">0</span>/61</b><small>85% across 5 days</small>')
rep('<small>278 graded legs, all tiers</small>','<small>295 graded legs, all tiers</small>')
rep('<span data-count="8">0</span>/8</b><small>every top-tier pick hit</small>','<span data-count="9">0</span>/9</b><small>every top-tier pick hit</small>')
rep('<b><span data-count="71">0</span>%</b><small>20 of 28 verified</small>','<b><span data-count="69">0</span>%</b><small>31 of 45 verified</small>')
rep('<div class="r acc">51 of 60</div><p>Legs graded 70%+ have hit 85% over five days, 8 of 8 on Sunday.','<div class="r acc">52 of 61</div><p>Legs graded 70%+ have hit 85% over five days, 9 of 9 on Sunday.')
rep("['Madness 16','L','$10, paid 100x','3 misses: JT ATD, JSN long, Geno']","['Madness 16','L','$10, paid 100x','4 misses: JT ATD, JSN long, Geno, Nabers 43']")
rep("['Top Board 18','L','$10, paid 300x','3 misses: Patriots, JSN long, Geno']","['Top Board 18','L','$10, paid 300x','4 misses: Patriots, JSN long, Geno, Nabers 43']")
rep('Madness died on J. Taylor ATD, JSN longest and Geno. Top Board died on Patriots ML, JSN and Geno. Two of those three were the QB problem above.','Madness missed J. Taylor ATD, JSN longest, Geno and Nabers 50+ (43). Top Board missed Patriots ML, JSN, Geno and Nabers. Two of the four were the QB problem above.')
rep('<div class="r bad">3 legs</div>','<div class="r bad">4 legs</div>')
rep('<li><b class="cy">Mid-tier grades still don\'t separate.</b> 60s hit 61%, 50s hit 63%.','<li><b class="cy">Mid-tier grades still don\'t separate.</b> 60s hit 63%, 50s hit 61%.')
rep('These legs stay ungraded until Ace confirms them, so they are not in the calibration yet.','Ace sent the 8 that mattered (Lamb 195, St. Brown 86, Milton 64, Breece 3 catches, Kittle 58, Nabers 43, Coker 29, LaPorta 32). These are still open.')
# Ceiling flag added to recap
rep('      <div class="flag g"><b>Favorites, not dogs</b>','''      <div class="flag w"><b>Ceilings keep paying</b><div class="r warn">17 of 29</div><p>Lines above a player's average: graded 32% on average, hit 59%. Lamb o83.5 (graded 45) went for 195. Milton 60+ rushing (graded 13) hit with 64. Careful: 4 of Sunday's 5 ceiling hits are one player's rungs.</p><div class="who">NFL ceilings 8 of 11, NBA 9 of 18. This is the lotto fuel.</div></div>
      <div class="flag g"><b>Favorites, not dogs</b>''')

# Lotto Lab section
lab='''
  <section class="panel" id="lotto">
    <h2>Lotto Lab <small>Ace's mission</small></h2>
    <blockquote class="ace">"The hammers are great, let's keep winning. But let's also find a way to win a lotto, even if it's 20 70%s."<cite>Ace, Nov 8</cite></blockquote>
    <div class="two">
      <div>
        <h3>Was the 17 of 20 just variance?</h3>
        <p class="note">Partly. The three misses on Nov 6 were Luka over 6.5 assists (5), Castle 4+ rebounds (3) and Naz Reid 15+ (14). Naz was a true hook. Luka and Castle were categories we now flag: assist overs and guard rebound overs. Two of three were the ticket, not luck.</p>
        <h3 style="margin-top:14px">The clean 70 pool</h3>
        <p class="note">Every 70%+ leg from Nov 4 to 8, NBA and NFL only: <b class="acc">44 of 50 hit (88%)</b>. All six misses sit in a flagged category: Huerter and Castle guard rebounds, Fagnano backup QB, Harden and McCollum on new teams, Avdija on a back-to-back. Take those out and every day's pool went perfect.</p>
        <div class="verdict w">Honest read: those filters were written after we saw the misses, so 100% is the best case, not the forecast. Plan around 88 to 90% per leg until the next two weeks confirm it.</div>
      </div>
      <div>
        <h3>What a 70%-only lotto hits</h3>
        <div class="bars" id="ladderBars" style="margin-top:10px"></div>
        <p class="note" style="margin-top:10px">Each bar is the chance every leg hits, at 88% per leg (white tick: 85%). A 20-leg of clean 70s is about 1 in 13. A 12-leg is about 1 in 5.</p>
      </div>
    </div>
    <h3 style="margin-top:16px">The algorithm · run this on every capper board</h3>
    <ol class="algo">
      <li><b>Pool.</b> Only legs I grade 70%+. NBA and NFL. No college football, no UFC.</li>
      <li><b>Filter.</b> Cut any leg that hits a flag: backup or new QB on passing and receiving legs, guard rebound overs, assist overs, PRA combos, back-to-backs, players new to a team, James Harden.</li>
      <li><b>Hook check.</b> If the line sits within one of the player's average, drop one rung.</li>
      <li><b>Spread it out.</b> Separate games. Two legs from one game only when they share a script, like a favorite's ML plus its lead back.</li>
      <li><b>Build the ladder.</b> Core 8 (about 1 in 3), Ladder 12 (about 1 in 5), and the 20 only on slates with 20 clean legs. Never pad with 60s to reach 20.</li>
      <li><b>Spice, max two.</b> One star ceiling line in a good script and one top TD pick. Each roughly doubles the payout. Top 4 TDs went 3 of 4 Sunday.</li>
      <li><b>Shop the price.</b> Kalshi paid 10 to 30% of fair on long combos. Price the 12 and the 20 somewhere else before locking.</li>
      <li><b>Size it.</b> $10 to $25 a lotto. The hammer stays the main bet.</li>
    </ol>
  </section>
'''
rep('\n  <section class="panel" id="sunday">',lab+'\n  <section class="panel" id="sunday">')
rep('<a class="btn" href="#sunday">Sunday</a>','<a class="btn" href="#lotto">Lotto Lab</a><a class="btn" href="#sunday">Sunday</a>')

# Feedback widget
fb='''
<button class="fbtn" id="fbOpen" type="button" aria-haspopup="dialog">Talk to us</button>
<div class="fbwrap" id="fbWrap" hidden>
  <div class="fbcard" role="dialog" aria-modal="true" aria-labelledby="fbTitle">
    <button class="fbx" id="fbClose" type="button" aria-label="Close">×</button>
    <span class="lbl acc">BettorDays · from Ace</span>
    <h3 id="fbTitle" style="font-size:24px;margin:6px 0 4px">Let's get everybody this money</h3>
    <p class="note" style="margin:0 0 12px">This board is built to help all of us win. Tell me what you think, what picks or sports you want, and what to add. I read every message.</p>
    <form id="fbForm">
      <input class="fin" name="name" maxlength="60" placeholder="Your name (optional)" autocomplete="name">
      <div class="fkinds" role="radiogroup" aria-label="Type">
        <label><input type="radio" name="kind" value="idea" checked><span>Idea</span></label>
        <label><input type="radio" name="kind" value="pick"><span>Pick request</span></label>
        <label><input type="radio" name="kind" value="feature"><span>Add to the site</span></label>
        <label><input type="radio" name="kind" value="other"><span>Other</span></label>
      </div>
      <textarea class="fin" name="msg" rows="5" maxlength="1500" placeholder="What do you think? What do you want?" required></textarea>
      <input type="text" name="website" tabindex="-1" autocomplete="off" class="hp" aria-hidden="true">
      <button class="btn on" type="submit" style="width:100%;padding:12px">Send it</button>
      <p class="mono" id="fbMsg" style="font-size:12px;margin:10px 0 0;min-height:1em" aria-live="polite"></p>
    </form>
  </div>
</div>
'''
rep('\n<script>',fb+'\n<script>')
css='''blockquote.ace{margin:4px 0 16px;padding:16px 18px;border-left:3px solid var(--acc);background:linear-gradient(90deg,rgba(4,255,159,.08),transparent);font-family:var(--display);font-size:clamp(18px,2.6vw,26px);font-weight:700;line-height:1.25}
blockquote.ace cite{display:block;margin-top:8px;font-family:var(--mono);font-size:11px;font-style:normal;letter-spacing:.14em;text-transform:uppercase;color:var(--mute)}
.algo{margin:8px 0 0;padding-left:22px;display:grid;gap:8px;font-size:13.5px;color:var(--mute)}
.algo b{color:var(--fg);font-family:var(--display);text-transform:uppercase;letter-spacing:.02em;margin-right:4px}
.fbtn{position:fixed;right:max(16px,env(safe-area-inset-right,0px));bottom:max(16px,env(safe-area-inset-bottom,0px));z-index:40;font-family:var(--display);font-weight:800;text-transform:uppercase;letter-spacing:.04em;background:var(--acc);color:#04130c;border:0;padding:12px 18px;cursor:pointer;box-shadow:0 0 0 0 rgba(4,255,159,.6);animation:fbp 2.4s infinite}
@keyframes fbp{70%{box-shadow:0 0 0 14px rgba(4,255,159,0)}100%{box-shadow:0 0 0 0 rgba(4,255,159,0)}}
.fbtn:focus-visible{outline:2px solid #fff;outline-offset:3px}
.fbwrap{position:fixed;inset:0;z-index:50;background:rgba(0,0,0,.6);backdrop-filter:blur(4px);display:grid;place-items:center;padding:16px}
.fbwrap[hidden]{display:none}
.fbcard{position:relative;width:min(480px,100%);background:var(--panel);border:1px solid var(--acc);padding:22px;box-shadow:0 0 40px rgba(4,255,159,.15);animation:fbin .35s cubic-bezier(.2,.8,.2,1)}
@keyframes fbin{from{opacity:0;transform:translateY(16px) scale(.98)}}
.fbx{position:absolute;top:8px;right:10px;background:none;border:0;color:var(--mute);font-size:24px;cursor:pointer;line-height:1}
.fin{width:100%;background:var(--panel2);border:1px solid var(--line);color:var(--fg);font:inherit;padding:10px 12px;margin-bottom:10px}
.fin:focus{outline:none;border-color:var(--acc)}
.fkinds{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:10px}
.fkinds input{position:absolute;opacity:0}
.fkinds span{display:inline-block;font-family:var(--mono);font-size:11px;letter-spacing:.06em;text-transform:uppercase;border:1px solid var(--line);padding:6px 10px;cursor:pointer}
.fkinds input:checked+span{background:var(--acc);color:#04130c;border-color:var(--acc)}
.fkinds input:focus-visible+span{outline:2px solid var(--acc);outline-offset:2px}
.hp{position:absolute;left:-9999px;width:1px;height:1px}
'''
rep('</style>',css+'</style>')
js='''
(function(){const L=[[8,'Core 8'],[12,'Ladder 12'],[16,'Big 16'],[20,'Madness 20']];
 document.getElementById('ladderBars').innerHTML=L.map(([n,t])=>{const p=Math.pow(.88,n)*100,q=Math.pow(.85,n)*100,c=p>=20?'#04ff9f':p>=10?'#ffb020':'#ff4d5e';
  return `<div class="br"><div class="n">${t}<small>1 in ${Math.round(100/p)} at 88%</small></div><div class="track"><i style="width:${p}%;background:${c}"></i><b style="left:${q}%"></b></div><div class="p" style="color:${c}">${p.toFixed(p<10?1:0)}%</div></div>`}).join('');})();
(function(){const w=document.getElementById('fbWrap'),o=document.getElementById('fbOpen'),x=document.getElementById('fbClose'),f=document.getElementById('fbForm'),m=document.getElementById('fbMsg');
 const open=()=>{w.hidden=false;setTimeout(()=>f.msg.focus(),50)},close=()=>{w.hidden=true;o.focus()};
 o.onclick=open;x.onclick=close;w.addEventListener('click',e=>{if(e.target===w)close()});document.addEventListener('keydown',e=>{if(e.key==='Escape'&&!w.hidden)close()});
 try{if(!sessionStorage.getItem('bdfb')){setTimeout(()=>{if(w.hidden){open();sessionStorage.setItem('bdfb','1')}},20000)}}catch(e){}
 f.onsubmit=async e=>{e.preventDefault();const d=Object.fromEntries(new FormData(f));d.page=location.hostname;m.textContent='Sending...';m.style.color='var(--mute)';
  try{const r=await fetch('/api/feedback',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(d)});const j=await r.json().catch(()=>({}));
   if(!r.ok||!j.ok)throw new Error(j.error||'fail');m.textContent='Got it. Ace will see this. Let\\'s get this money.';m.style.color='var(--acc)';f.reset();setTimeout(close,2200)}
  catch(err){m.textContent=location.hostname.includes('bettordays')||location.hostname.includes('vercel')?'Could not send. Try again in a minute.':'Send this from bettordays.xyz, the live site.';m.style.color='var(--bad)'}};
})();
'''
i=h.rindex('</script>'); h=h[:i]+js+h[i:]
open(p,'w').write(h.replace('—',','))
print('ok')
