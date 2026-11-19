import json,re
p='bettordays-hq.html'; h=open(p).read()
nov8=json.load(open('study/nov8.json')); pend=json.load(open('study/nov8_pending.json'))
def rep(old,new,cnt=1):
    global h
    assert old in h, old[:80]
    h=h.replace(old,new,cnt)

# 1 ROWS append
m=re.search(r'const ROWS=(\[.*?\]);\n',h,re.S)
rows=json.loads(m.group(1))+nov8
h=h[:m.start()]+'const ROWS='+json.dumps(rows,separators=(',',':'))+';\n'+h[m.end():]

# 2 filters
rep("['Nov 7','Nov 7']];","['Nov 7','Nov 7'],['Nov 8','Nov 8']];")

# 3 header + nav
rep('Process audit · Nov 4 to 7 · 211 graded legs','Process audit · Nov 4 to 8 · 278 graded legs')
rep('<a class="btn" href="#sunday">Sunday</a>','<a class="btn" href="#recap">Results</a><a class="btn" href="#sunday">Sunday</a>')

# 4 tiles
old_tiles=h[h.index('<section class="tiles"'):h.index('</section>',h.index('<section class="tiles"'))+10]
tiles='''<section class="tiles" aria-label="Record">
    <div class="tile"><span class="lbl">Main tickets</span><b class="acc"><span data-count="5">0</span>-2</b><small>hammers and main parlays, Nov 4 to 8</small></div>
    <div class="tile"><span class="lbl">Main ticket P&amp;L</span><b class="mono acc">+$<span data-count="1527">0</span></b><small>after Sunday's two 5-legs cashed</small></div>
    <div class="tile"><span class="lbl">70%+ legs</span><b class="mono acc"><span data-count="51">0</span>/60</b><small>85% across 5 days</small></div>
    <div class="tile"><span class="lbl">Capper boards hit</span><b class="mono"><span data-count="62">0</span>%</b><small>278 graded legs, all tiers</small></div>
    <div class="tile"><span class="lbl">Lottos cashed</span><b class="mono bad"><span data-count="0">0</span>/11</b><small>Kalshi pays 10-30% of fair on long ones</small></div>
  </section>'''
h=h.replace(old_tiles,tiles)

# 5 recap section
P=lambda s:s.replace('—',',')
recap='''
  <section class="panel reveal" id="recap">
    <h2>Sunday Nov 8 · results <small>the reanalysis screen</small></h2>
    <div class="kpis">
      <div class="kpi"><span class="lbl">Net on the day</span><b class="acc">+$<span data-count="571">0</span></b><small>2 of 2 main tickets cashed, lottos -$20</small></div>
      <div class="kpi"><span class="lbl">70%+ legs</span><b class="acc"><span data-count="8">0</span>/8</b><small>every top-tier pick hit</small></div>
      <div class="kpi"><span class="lbl">Non-TD legs graded</span><b><span data-count="71">0</span>%</b><small>20 of 28 verified</small></div>
      <div class="kpi"><span class="lbl">Anytime TDs</span><b class="warn"><span data-count="15">0</span>/39</b><small>graded 32%, hit 38%. Top 4: 3 of 4</small></div>
    </div>
    <div class="tickets" id="recapTix"></div>
    <div class="flags" style="margin-top:16px">
      <div class="flag g"><b>The top tier carried again</b><div class="r acc">51 of 60</div><p>Legs graded 70%+ have hit 85% over five days, 8 of 8 on Sunday. Both 5-legs were built entirely from this tier plus McDaniels, and both cashed.</p><div class="who">Chiefs 35-12, 49ers 38-17, Lions 19-9, Rams 20-13, Lamb 50+, McDaniels 16</div></div>
      <div class="flag"><b>QB changes kill the passing legs</b><div class="r bad">2 of 2</div><p>Seattle won with Drew Lock, but its longest catch all day was 18 yards, so JSN o25.5 longest missed. Geno o200 missed because Kirk Cousins was the Raiders QB. Same story as Fagnano on Nov 5.</p><div class="who">Team ML survives a QB change. Receivers and passing overs don't.</div></div>
      <div class="flag w"><b>Kalshi taxes long parlays hard</b><div class="r warn">10-30%</div><p>Madness 16 paid 100x against about 1,100x fair. Top Board 18 paid 300x against about 980x. The 5-legs paid 3.36x against about 4.1x, so short tickets keep about 80% of fair.</p><div class="who">On Kalshi, the lotto is the most expensive ticket we buy.</div></div>
      <div class="flag g"><b>Old news is already priced</b><div class="r acc">17-3</div><p>Darnold was ruled out Wednesday, so the -440 already had Lock in it. Seattle won easily. Pulling them cost nothing because the hammer was never played, but news from days earlier isn't a reason to cut.</p><div class="who">Original hammer and original 6-leg 5x would both have cashed.</div></div>
      <div class="flag g"><b>Favorites, not dogs</b><div class="r acc">7 of 8</div><p>Every NFL favorite we graded 59%+ won except New England. All four underdog moneylines on the board lost.</p><div class="who">Moneyline favorites all days: 24 of 34. Dogs: 4 of 9.</div></div>
      <div class="flag"><b>What sank the lottos</b><div class="r bad">3 legs</div><p>Madness died on J. Taylor ATD, JSN longest and Geno. Top Board died on Patriots ML, JSN and Geno. Two of those three were the QB problem above.</p><div class="who">Gibbs, Walker and Javonte all scored. Saquon, Puka, Barner, Estime too.</div></div>
    </div>
    <div class="two" style="margin-top:16px">
      <div><h3>Still waiting on stats</h3><p class="note">The scores feed has no NFL player yardage. These legs stay ungraded until Ace confirms them, so they are not in the calibration yet.</p><div class="mono" id="pendList" style="font-size:12px;line-height:1.8;color:var(--mute)"></div></div>
      <div><h3>Are we on the right path?</h3><ol class="mono" style="margin:8px 0 0;padding-left:20px;font-size:12.5px;line-height:1.85;color:var(--mute)">
        <li><b class="acc">Yes on the core.</b> The money comes from 70%+ legs in short tickets. That has now paid on 5 of 7 main tickets.</li>
        <li><b class="warn">Lottos need a rethink on Kalshi.</b> At 10-30% of fair, even a hit barely pays for the misses. 6 to 8 legs, or a different book for long ones.</li>
        <li><b class="cy">Add a QB check</b> to roster verification: confirm the starting QB for every passing or receiving leg.</li>
        <li><b class="cy">Mid-tier grades still don't separate.</b> 60s hit 61%, 50s hit 63%. The 70% line is where the edge starts.</li>
      </ol></div>
    </div>
  </section>
'''
rep('\n  <section class="panel" id="sunday">',recap+'\n  <section class="panel" id="sunday">')

# 6 css
css='''.kpis{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px;margin:6px 0 16px}
@media(max-width:860px){.kpis{grid-template-columns:repeat(2,minmax(0,1fr))}}
.kpi{background:linear-gradient(160deg,rgba(4,255,159,.07),transparent 60%),var(--panel2);border:1px solid var(--line);padding:14px;min-width:0}
.kpi b{display:block;font-family:var(--display);font-size:38px;font-weight:900;line-height:1.05}
.kpi small{color:var(--mute);font-size:12px}
.tickets{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px}
@media(max-width:900px){.tickets{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media(max-width:520px){.tickets{grid-template-columns:1fr}}
.tk{border:1px solid var(--line);background:var(--panel2);padding:12px;min-width:0;position:relative;overflow:hidden}
.tk.w{border-color:rgba(4,255,159,.55);box-shadow:0 0 22px rgba(4,255,159,.12)}
.tk .st8{font-family:var(--display);font-weight:900;font-size:20px;text-transform:uppercase}
.tk .st8.w{color:var(--acc)} .tk .st8.l{color:var(--bad)} .tk .st8.n{color:var(--dim)}
.tk p{margin:4px 0 0;font-size:12px;color:var(--mute)}
.tk .nm{font-family:var(--mono);font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:var(--fg)}
.reveal{opacity:0;transform:translateY(18px);transition:opacity .7s ease,transform .7s cubic-bezier(.2,.8,.2,1)}
.reveal.in{opacity:1;transform:none}
'''
rep('</style>',css+'</style>')

# 7 thesis first tile
rep('<div class="big acc">90%</div><div class="vs">80%+ grades · 18 of 20 hit</div>','<div class="big acc">85%</div><div class="vs">70%+ grades · 51 of 60 hit</div>')
rep('what 4 days of data says','what 5 days of data says')

# 8 rules
rep(" ['Coin-flip picks at regular lines, not alts',",
""" ['QB check on every passing leg','Geno, JSN longest, Fagnano. Team ML can survive a QB change, receivers can\\'t.','Testing Nov 8',1],
 ['Lottos on Kalshi: 6 to 8 legs max','Long combos paid 10-30% of fair. Short ones about 80%.','Testing Nov 8',1],
 ['Don\\'t cut on news that\\'s days old','Seattle -440 already had Lock priced. Won 17-3.','Testing Nov 8',1],
 ['Coin-flip picks at regular lines, not alts',""")

# 9 ledger
rep("const DAYS=[\n","""const DAYS=[
 {d:'Sun Nov 8 · NFL, NBA',pl:'+$571',tix:[
  ['5-leg #1 (Kalshi)','$124.96','3.36x','W','Chiefs, 49ers, Lions, Rams ML + McDaniels 10+ (16). Paid $420.45'],
  ['5-leg #2 (Kalshi)','$124.96','3.36x','W','Chiefs, 49ers, Lions, Rams ML + Lamb 50+. Paid $420.45'],
  ['Madness 16 (Kalshi)','$10','100x','L','J. Taylor ATD, JSN o25.5 longest, Geno o200 (Cousins started)'],
  ['Top Board 18 (Kalshi)','$10','300x','L','Patriots ML (lost 45-27), JSN longest, Geno'],
  ['Hammer: Chiefs, 49ers, McDaniels','not played','1.62x','W','Would have cashed. Passed on the price'],
 ]},
""")

# 10 RES map: full results
res={r['pick']:('W' if r['hit'] else 'L') for r in nov8}
for pp,_ in pend: res[pp]='TBD'
mres=re.search(r"const RES=\{.*?\};",h)
h=h[:mres.start()]+'const RES='+json.dumps(res)+';'+h[mres.end():]

# 11 TIX results
TR={"Hammer · no Seahawks":"W","Played #1 · McDaniels 5":"W","Played #2 · Lamb 5":"W","Original hammer · pulled":"W","Original 5x · pulled":"W","Value 3 · regular lines":"L","TD trio":"L","Madness 16 · ~1,000x":"L","Top Board 18 · no TDs":"L"}
h=h.replace("const RES=","const TR="+json.dumps(TR)+";\nconst RES=",1)
rep("document.getElementById('sunTix').innerHTML=TIX.map(t=>`<div class=\"st\"${t.live?",
    "document.getElementById('sunTix').innerHTML=TIX.map(t=>`<div class=\"st\"${TR[t.t]==='W'?' style=\"border-color:var(--acc);box-shadow:0 0 18px rgba(4,255,159,.18)\"':t.live?")
rep('<h3 style="color:${t.c}">${t.t}</h3>${t.legs.map(','<h3 style="color:${t.c}">${t.t}</h3>${TR[t.t]?`<div class="st8 ${TR[t.t]===\'W\'?\'acc\':\'bad\'}" style="font-family:var(--display);font-weight:900;font-size:18px;margin:2px 0 6px">${TR[t.t]===\'W\'?(t.stake.includes(\'$\')?\'CASHED\':\'WOULD HAVE CASHED\'):\'MISSED\'}</div>`:\'\'}${t.legs.map(')

# 12 recap tickets + pending + top25 badges + table result col
js='''
const RT=[['5-leg #1','W','$124.96 → $420.45','Chiefs, 49ers, Lions, Rams, McDaniels 16'],['5-leg #2','W','$124.96 → $420.45','Chiefs, 49ers, Lions, Rams, Lamb 50+'],['Madness 16','L','$10, paid 100x','3 misses: JT ATD, JSN long, Geno'],['Top Board 18','L','$10, paid 300x','3 misses: Patriots, JSN long, Geno']];
document.getElementById('recapTix').innerHTML=RT.map(t=>`<div class="tk ${t[1]==='W'?'w':''}"><div class="nm">${t[0]}</div><div class="st8 ${t[1]==='W'?'w':'l'}">${t[1]==='W'?'Cashed':'Missed'}</div><p>${t[2]}</p><p>${t[3]}</p></div>`).join('');
document.getElementById('pendList').innerHTML=Object.keys(RES).filter(k=>RES[k]==='TBD').slice(0,40).join(' · ');
document.querySelectorAll('#topAny li,#topReg li').forEach(li=>{const n=li.firstChild.textContent.trim();li.insertAdjacentHTML('beforeend',badge(n))});
(function(){const io='IntersectionObserver' in window?new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}}),{threshold:.08}):null;
 document.querySelectorAll('.panel').forEach(p=>{p.classList.add('reveal');if(io)io.observe(p);else p.classList.add('in')});
 const red=matchMedia('(prefers-reduced-motion: reduce)').matches;
 document.querySelectorAll('[data-count]').forEach(e=>{const to=+e.dataset.count;if(red||!to){e.textContent=to.toLocaleString();return}const t0=performance.now(),d=1400;
  const f=t=>{const k=Math.min(1,(t-t0)/d),v=Math.round(to*(1-Math.pow(1-k,3)));e.textContent=v.toLocaleString();if(k<1)requestAnimationFrame(f)};requestAnimationFrame(f)});
 setTimeout(()=>document.querySelectorAll('.panel').forEach(p=>p.classList.add('in')),2500);
})();
'''
i=h.rindex('</script>'); h=h[:i]+js+h[i:]
open(p,'w').write(h.replace('—',','))
print('ok', len(h))
