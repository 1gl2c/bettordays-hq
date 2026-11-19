import json,re
F='bettordays-hq.html';s=open(F).read()
def rep(a,b,cnt=1):
  global s
  n=s.count(a);assert n==cnt,(n,a[:90]);s=s.replace(a,b)
B=json.load(open('beta/beta_tonight.json'))
BETA={'ts':B['ts'],'sim_ts':B['sim_ts'],'n_lines':B['n_lines'],'n_games':B['n_games'],'all_pos':B['all_pos'],
 'top':[{k:l[k] for k in ('player','st','k','odds','ask','be','sim','se','unc','n','hs','h5','avg','edge','move','g','t')} for l in B['top']]}
# 1) research section: wrap blocks into views + hub
a=s.index('<section class="panel" id="research">');b=s.index('</section>',a)
old=s[a:b]
new='''<section class="panel" id="research">
    <div class="dayhead"><span class="lbl">Deep research · for the analytics nerds</span><h2 class="big">Research</h2>
    <p class="proof">Pick a topic. Every number is counted from picks graded against real box scores, with the record and the number of legs right on the card. Sections marked <b style="color:var(--warn)">EXPERIMENTAL</b> are still being tested.</p></div>
    <a class="rsback" href="#rs-hub">← All research</a>
    <div class="rhub" id="rsHub"></div>
    <div class="rsv" data-v="hits">
    <div class="kpis" id="rsKpi"></div>
    <div class="sech"><h3>What actually hits: hit rate by category</h3><span class="lbl">best first</span></div>
    <div class="scroll"><table id="rsCats" class="rtab"></table></div></div>
    <div class="rsv" data-v="grade"><div class="sech"><h3>Does our grade mean anything?</h3><span class="lbl">grade vs what happened</span></div>
    <div class="scroll"><table id="rsTiers" class="rtab"></table></div></div>
    <div class="rsv" data-v="n70"><div class="sech"><h3>70%+ picks, night by night</h3></div>
    <div class="rdays" id="rsDays"></div></div>
    <div class="rsv" data-v="n80"><div class="sech"><h3>80%+ picks, night by night</h3><span class="lbl">graded 80 or higher</span></div>
    <div class="rdays" id="rsDays80"></div></div>
    <div class="rsv" data-v="lines"><div class="sech"><h3>Results by sport and line type</h3></div>
    <div class="scroll"><table id="rsLines" class="rtab"></table></div><p class="note">Want to slice it yourself? The <a data-go="record" href="/record" style="color:var(--acc)">Record explorer</a> stacks any filters with W-L and sample size.</p></div>
    <div class="rsv" data-v="clues"><div class="sech"><h3>Clues for building a parlay</h3><span class="lbl">what the data says so far</span></div>
    <ol class="algo" id="rsClues"></ol></div>
  '''
assert '<div class="kpis" id="rsKpi"></div>' in old and 'id="rsClues"' in old
s=s[:a]+new+s[b:]
rep('<section class="panel" id="perfect">','<section class="panel rsv" id="perfect" data-v="perfect">')
rep('<span class="lbl">Hindsight lab</span>','<span class="lbl" style="color:var(--warn)">EXPERIMENTAL · hindsight lab</span>')
rep('<section class="panel" id="betalab">','<section class="panel rsv" id="betalab" data-v="ai">')
rep('<span class="lbl" style="color:var(--warn)">Beta · test mode · be cautious</span>','<span class="lbl" style="color:var(--warn)">EXPERIMENTAL · beta · be cautious</span>')
# 2) beta test mode section after betalab
a=s.index('<section class="panel rsv" id="betalab"');b=s.index('</section>',a)+10
beta='''
  <section class="panel rsv" id="betatest" data-v="beta" data-pg="research">
    <div class="dayhead"><span class="lbl" style="color:var(--warn)">BETA · EXPERIMENTAL · not a recommendation</span><h2 class="big">Beta Test Mode</h2>
    <p class="proof">A test of one question: can our model find player lines priced around even money (+100 to -150) that hit more often than the price says? This is separate from the main picks and the Hammer. A simulation is an estimate, not proof a line will hit. Nothing here has beaten the market on new picks yet.</p></div>
    <div class="simbox" id="btSim"></div>
    <div class="sech"><h3>Tonight's Top 15 · Wednesday Nov 18</h3><span class="lbl" id="btTs"></span></div>
    <div class="scroll"><table id="btTop" class="rtab"></table></div>
    <p class="note" id="btNote"></p>
    <div class="sech"><h3>Which methods actually find value?</h3><span class="lbl">tested on picks not used to build them</span></div>
    <p class="note">History: 603 graded legs with an exact Kalshi price, Nov 4 to 17. Each method was built on Nov 4 to 12 (300 legs) and then checked on Nov 13 to 17 (303 legs). ROI means buying at Kalshi's price including its fee. Many legs share a game or a player ladder, so the true uncertainty is wider than the ranges shown.</p>
    <div class="scroll"><table class="rtab" id="btMeth"></table></div>
    <div class="sech"><h3>8-leg ticket</h3><span class="lbl">status</span></div>
    <p class="note"><b style="color:var(--warn)">Not ready.</b> An 8-leg ticket only makes sense once a method has beaten break-even on new picks over a large sample, and once same-game correlation is priced in. We will not force one for the payout. Every Top 15 line is saved with its price, the price time and the simulated hit rate, and graded the next day, so this page builds its own track record.</p>
  </section>'''
s=s[:b]+beta+s[b:]
# 3) CSS
rep('/* popup v2 */','''.rhub{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:10px;margin-top:6px}
.rcard{display:block;border:1px solid var(--line);background:rgba(255,255,255,.02);padding:14px 14px 12px;color:var(--fg);text-decoration:none;position:relative;min-height:118px}
.rcard:hover,.rcard:focus-visible{border-color:var(--acc);outline:none}
.rcard h4{margin:0 0 6px;font:800 17px/1.15 var(--display);text-transform:uppercase;letter-spacing:.01em}
.rcard p{margin:0;font-size:13px;color:var(--mute);line-height:1.4}.rcard .st{display:block;margin-top:10px;font:600 12px var(--mono);color:var(--acc)}
.rcard .ex{position:absolute;top:10px;right:10px;font:700 10px var(--mono);letter-spacing:.06em;color:var(--warn);border:1px solid var(--warn);padding:1px 5px}
.rsv{display:none}.rsback{display:none;margin:4px 0 10px;font:600 13px var(--mono);color:var(--acc);text-decoration:none}
body[data-rsv] .rsback{display:inline-block}body[data-rsv] #rsHub{display:none}
body[data-rsv="hits"] .rsv[data-v="hits"]:not([hidden]),body[data-rsv="grade"] .rsv[data-v="grade"]:not([hidden]),body[data-rsv="n70"] .rsv[data-v="n70"]:not([hidden]),body[data-rsv="n80"] .rsv[data-v="n80"]:not([hidden]),body[data-rsv="lines"] .rsv[data-v="lines"]:not([hidden]),body[data-rsv="clues"] .rsv[data-v="clues"]:not([hidden]),body[data-rsv="perfect"] .rsv[data-v="perfect"]:not([hidden]),body[data-rsv="ai"] .rsv[data-v="ai"]:not([hidden]),body[data-rsv="beta"] .rsv[data-v="beta"]:not([hidden]){display:block}
.simbox{border:1px solid var(--warn);background:rgba(255,176,32,.04);padding:14px;margin:6px 0 14px}
.simbox .row{display:flex;justify-content:space-between;gap:10px;flex-wrap:wrap;font:600 12.5px var(--mono);color:var(--mute)}
.simbox canvas{width:100%;height:120px;display:block;margin-top:10px}
#btTop td small{color:var(--mute)}
/* popup v2 */''')
# 4) JS: hub + views + 80 nights + beta
js='''<script>
const BETA='''+json.dumps(BETA)+''';
(function(){
 const R=typeof ROWS!=='undefined'?ROWS:[];const rec=f=>{const x=R.filter(f);return [x.filter(r=>r.hit).length,x.length]};
 const days=[...new Set(R.map(r=>r.day))];const span=days.length?days[0]+' to '+days[days.length-1]:'';
 const st=([h,n])=>`${h}-${n-h} · ${n?Math.round(100*h/n):0}% · ${n} legs`;
 const CARDS=[['hits','What actually hits','Hit rate by category, best first.',st(rec(()=>1))],
  ['grade','Does our grade mean anything?','Our grade bands against what really happened.',st(rec(r=>r.est>=70))+' at 70+'],
  ['n70','70+ picks by night','Every night\\'s 70%+ legs.',st(rec(r=>r.est>=70))],
  ['n80','80+ picks by night','Every night\\'s 80%+ legs.',st(rec(r=>r.est>=80))],
  ['lines','Results by sport and line type','Regular lines, alts, and each sport.',days.length+' nights · '+span],
  ['clues','Clues for building a parlay','What the data says so far.','Updated each graded night'],
  ['perfect','Perfect parlays','Hindsight: what the winning legs had in common.','Hindsight only',1],
  ['ai','AI perfect parlay','The beta model builds tonight\\'s parlay before games.','Not proven',1],
  ['beta','Beta Test Mode','+100 to -150 player lines, 1,000 sims per game, tested against the price.',`${BETA.top.length} lines tonight · 0 graded so far`,1],
  ['record','Record explorer','Stack any filters, see W-L and sample size.',R.length+' graded legs']];
 const hub=document.getElementById('rsHub');if(!hub)return;
 hub.innerHTML=CARDS.map(([k,t,d,x,e])=>`<a class="rcard" ${k==='record'?'data-go="record" href="/record"':`href="#rs-${k}"`}>${e?'<span class="ex">EXPERIMENTAL</span>':''}<h4>${t}</h4><p>${d}</p><span class="st">${x}</span></a>`).join('');
 const apply=()=>{const m=/^#rs-([a-z0-9]+)/.exec(location.hash);if(m&&m[1]!=='hub')document.body.dataset.rsv=m[1];else delete document.body.dataset.rsv};
 window.addEventListener('hashchange',apply);apply();
 document.addEventListener('click',e=>{const a=e.target.closest('a[data-go]');if(a){delete document.body.dataset.rsv}});
 // 80+ nights
 const d80=document.getElementById('rsDays80');
 if(d80)d80.innerHTML=days.map(d=>{const x=R.filter(r=>r.day===d&&r.est>=80),h=x.filter(r=>r.hit).length;return x.length?`<div class="rday"><b>${d}</b><span class="mono">${h}/${x.length}</span><div class="minibar"><i style="width:${Math.round(100*h/x.length)}%"></i></div><small>${Math.round(100*h/x.length)}%</small></div>`:''}).join('')+`<p class="note">80+ legs, ${span}: ${st(rec(r=>r.est>=80))}. Some nights include ladders on the same player and several legs from one game, which win or lose together.</p>`;
 // beta table
 const W={pts:'points',reb:'rebounds',ast:'assists','3pm':'threes',pra:'PRA'};
 const fmt=iso=>new Date(iso).toLocaleTimeString([], {hour:'numeric',minute:'2-digit'});
 const ts=document.getElementById('btTs');if(ts)ts.textContent='Kalshi prices at '+fmt(BETA.ts)+' · sims run '+fmt(BETA.sim_ts);
 const T=document.getElementById('btTop');
 if(T)T.innerHTML='<thead><tr><th>#</th><th>Line</th><th>Odds</th><th>Break-even</th><th>Sim hit %</th><th>Gap</th><th>Sample</th><th>Game</th></tr></thead><tbody>'+BETA.top.map((l,i)=>`<tr><td class="mono">${i+1}</td><td>${l.player} ${l.k}+ ${W[l.st]}<br><small>avg ${l.avg} · last 5: ${l.h5}/5</small></td><td class="mono">${l.odds}</td><td class="mono">${l.be}%</td><td class="mono">${l.sim}%<br><small>±${l.se} sim, ±${l.unc} sample</small></td><td class="mono" style="color:${l.edge>l.unc?'var(--acc)':'var(--warn)'}">+${l.edge}</td><td class="mono">${l.hs}/${l.n} games</td><td class="lbl">${l.g} ${l.t}</td></tr>`).join('')+'</tbody>';
 const N=document.getElementById('btNote');
 if(N)N.innerHTML=`How it works: each of tonight's ${BETA.n_games} NBA games was simulated 1,000 times. Each run draws a shared pace for the game and each team, then each player's night from his own season (last 5 games count double), nudged for matchup and back-to-backs. ${BETA.n_lines} Kalshi lines priced +100 to -150 were checked. ${BETA.all_pos} of them came out above break-even. Across all ${BETA.n_lines} lines the sim averaged 4.3 points <i>below</i> break-even. The Top 15 is the biggest gap per player, at most 2 per game. <b>Read the ±sample column:</b> these players have 9 to 15 games, so the honest range on each hit rate is about ±20 points. That is bigger than every gap on the list, so none of these is a proven edge. Big gaps against the market usually mean the model is missing something (a role change, minutes, an injury), not that the market is wrong. Break-even includes Kalshi's fee.`;
 const M=document.getElementById('btMeth');
 if(M)M.innerHTML='<thead><tr><th>Method</th><th>What it assumes</th><th>Built on Nov 4-12</th><th>Checked on Nov 13-17</th><th>Verdict</th></tr></thead><tbody>'+[
  ['Our grade vs price','When our grade is 5+ above Kalshi on a near-even line, Kalshi has it wrong.','8-1, +55% ROI (9 legs)','14-8, +11% ROI, range ±36 (22 legs)','Not proven. Shrank a lot on new picks.'],
  ['Blend our grade into the price','Some mix of our grade and Kalshi predicts better than either.','Best mix: 0% our grade','Kalshi alone beat our grade (log loss 0.556 vs 0.627)','Our grade added nothing on top of the price.'],
  ['Line movement','A price that rises before tip keeps rising for a reason. Buy early, before the move.','Rose 4+: 71-23, +36% (94 legs). Fell 4+: -13%','Rose 4+: +24%, range ±51 (64 legs). Fell 4+: -11%','Most promising. Same direction both halves, still too noisy. Needs a second price snapshot each night.'],
  ['1,000-sim per game','Same inputs as our grade, run as full games so same-game legs move together.','No separate test yet','Starts tonight (15 lines saved)','Useful for parlay correlation. Adds no new information for a single leg.'],
  ['Near-even legs overall','Lines priced 50 to 60 cents are fairly priced.','71-43 on all near-even legs we picked','+8.7% ROI, range ±16 (114 legs)','Not proven. The range includes zero.']].map(r=>`<tr>${r.map((c,i)=>`<td${i===4?' style="color:var(--warn)"':''}>${c}</td>`).join('')}</tr>`).join('')+'</tbody>';
 // simulation animation: runs once when the section is opened
 const box=document.getElementById('btSim');if(!box)return;
 box.innerHTML='<div class="row"><span id="btRun">Ready</span><span id="btCnt">0 / '+(BETA.n_games*1000).toLocaleString()+' runs</span></div><canvas id="btCv" aria-label="Simulation animation: dots fill in as runs complete" role="img"></canvas>';
 const cv=document.getElementById('btCv'),cx=cv.getContext('2d');let ran=false;
 const run=()=>{if(ran)return;ran=true;const w=cv.width=cv.clientWidth*devicePixelRatio,h=cv.height=120*devicePixelRatio;const total=BETA.n_games*1000,bins=new Array(40).fill(0);let done=0;const red=matchMedia('(prefers-reduced-motion: reduce)').matches;
  const step=()=>{const n=red?total:Math.min(total-done,180);for(let i=0;i<n;i++){let u=0;for(let j=0;j<6;j++)u+=Math.random();bins[Math.min(39,Math.floor(u/6*40))]++}done+=n;
   cx.clearRect(0,0,w,h);const mx=Math.max(...bins);bins.forEach((b,i)=>{const bh=(b/mx)*(h-8);cx.fillStyle=i>=22?'#04ff9f':'#2b3a33';cx.fillRect(i*w/40+1,h-bh,w/40-2,bh)});
   document.getElementById('btCnt').textContent=done.toLocaleString()+' / '+total.toLocaleString()+' runs';document.getElementById('btRun').textContent=done<total?'Simulating game '+Math.min(BETA.n_games,1+Math.floor(done/1000))+' of '+BETA.n_games:'Done · illustration of the run, results below';
   if(done<total)requestAnimationFrame(step)};step()};
 const chk=()=>{if(document.body.dataset.rsv==='beta')setTimeout(run,150)};window.addEventListener('hashchange',chk);chk();
})();
</script>
'''
s=s.replace('<script>\n/* Record explorer:',js+'<script>\n/* Record explorer:',1)
open(F,'w').write(s);print('ok')
