"""Engine v8 site pass. Run after v8/publish_v8.py and fri20/site_patch.py (from pipeline/):
  python3 v8/site_v8.py DATE
- Beta Test Mode: tonight's agent simulations (each agent's hit rate per line, consensus, edge vs break-even, each agent's top 10)
- Research hub split into Tonight and Track record; no more vague EXPERIMENTAL header
- Beta list heading no longer hard-coded to Nov 19
- Method page and the Research Tonight view describe v8"""
import json, re, sys
day = sys.argv[1]
F = 'bettordays-hq.html'; s = open(F).read()
def rep(a, b, n=1):
    global s; c = s.count(a); assert c == n, (c, a[:100]); s = s.replace(a, b)
SIM = json.load(open(f'daily/{day}/v8_sims.json'))
keep = ['player', 'team', 'st', 'k', 'g', 't', 'odds', 'be', 'oursim', 'avg', 'hs', 'n', 'agents', 'why', 'cons', 'edge', 'nagree', 'n_line']
SIM['lines'] = [{k: z[k] for k in keep} for z in SIM['lines']]
if 'const V8SIM=' in s: s = re.sub(r"const V8SIM=[^\n]*;\n", lambda m: 'const V8SIM=' + json.dumps(SIM) + ';\n', s, count=1)
else: rep('const BETA=', 'const V8SIM=' + json.dumps(SIM) + ';\nconst BETA=')
# Beta section: agent simulations block + live heading
if 'id="v8sims"' not in s:
    rep('<div class="sech"><h3>Track record so far</h3><span class="lbl">graded the next morning</span></div><div class="kpis" id="btRec"></div>',
        '<div class="sech"><h3>Tonight\'s agent simulations</h3><span class="lbl" id="v8simTs"></span></div><div id="v8sims"></div>\n    '
        '<div class="sech"><h3>Track record so far</h3><span class="lbl">graded the next morning</span></div><div class="kpis" id="btRec"></div>')
    s = re.sub(r'<div class="sech"><h3>Latest Top list · [^<]*</h3>', '<div class="sech"><h3 id="btHead">Our own sim · Top list</h3>', s, count=1)
    js = r'''
(function(){const el=document.getElementById('v8sims');if(!el||typeof V8SIM==='undefined'||!V8SIM)return;
 const MN={chatgpt:'ChatGPT',gemini:'Gemini',grok:'Grok',claude:'Claude'},W={pts:'points',reb:'rebounds',ast:'assists','3pm':'threes',pra:'PRA'};
 const ag=Object.keys(MN).filter(k=>V8SIM.status[k]&&V8SIM.status[k]!=='no reply');
 const ts=document.getElementById('v8simTs');if(ts)ts.textContent=Object.entries(V8SIM.status).map(([k,v])=>`${MN[k]}: ${v}`).join(' · ');
 const nm=z=>`${z.player} ${z.k}+ ${W[z.st]}`;const c=(v,be)=>v==null?'-':`<span style="color:${v>be?'var(--acc)':'inherit'}">${v}</span>`;
 const top=V8SIM.lines.filter(z=>z.cons!=null).slice(0,15);
 let h=`<p class="note" style="max-width:820px">Each agent researched minutes, matchup and injuries, then ran 1,000 simulations of every game below without seeing any price. We compare their hit rates to Kalshi's break-even (the price plus the fee). <b>Consensus</b> is the middle of the agents and our own sim. Green numbers are above break-even. When 3 or 4 agents clear break-even on the same line, that is the signal worth a look. A simulation is an estimate, not proof.</p>`;
 h+=`<div class="scroll"><table class="rtab"><thead><tr><th>#</th><th>Line</th><th>Odds</th><th>Break-even</th>${ag.map(k=>`<th>${MN[k]}</th>`).join('')}<th>Our sim</th><th>Consensus</th><th>Gap</th><th>Agents above</th><th>Game</th></tr></thead><tbody>${top.map((z,i)=>`<tr><td class="mono">${i+1}</td><td>${nm(z)}<br><small>avg ${z.avg} · hit ${z.hs}/${z.n} games</small></td><td class="mono">${z.odds}</td><td class="mono">${z.be}%</td>${ag.map(k=>`<td class="mono">${c(z.agents[k],z.be)}</td>`).join('')}<td class="mono">${c(z.oursim,z.be)}</td><td class="mono"><b>${z.cons}%</b></td><td class="mono" style="color:${z.edge>0?'var(--acc)':'var(--warn)'}">${z.edge>0?'+':''}${z.edge}</td><td class="mono">${z.nagree} of ${ag.length}</td><td class="lbl">${z.g} ${z.t}</td></tr>`).join('')}</tbody></table></div>`;
 const byn={};V8SIM.lines.forEach(z=>byn[z.n_line]=z);
 h+=`<div class="struct" style="margin-top:14px">${ag.map(k=>`<div class="st"><h3>${MN[k]} top 10</h3>${(V8SIM.agent_top[k]||[]).map(n=>byn[n]).filter(Boolean).map(z=>`<div class="row"><span>${nm(z)} <small>${z.g}</small></span><b>${z.agents[k]??'-'}%<small class="kp">BE ${z.be}</small></b></div>`).join('')||'<p class="note" style="margin:0">No top 10 returned.</p>'}</div>`).join('')}</div>`;
 el.innerHTML=h})();
'''
    rep("\n(function(){\n\n // every suggested ticket we posted, graded leg by leg", js + "\n(function(){\n\n // every suggested ticket we posted, graded leg by leg")
# Research hub: Tonight / Track record groups, clear header
rep('<p class="proof">Pick a topic. Every number is counted from picks graded against real box scores, with the record and the number of legs right on the card. Sections marked <b style="color:var(--warn)">EXPERIMENTAL</b> are still being tested.</p></div>',
    '<p class="proof"><b>Tonight</b> is everything for today\'s slate: the full grade sheet, each AI agent\'s simulations and the parlays. <b>Track record</b> is every pick we have graded against real box scores, with the record and sample size on each card.</p></div>')
rep("hub.innerHTML=CARDS.map(([k,t,d,x,e])=>`<a class=\"rcard\" ${k==='record'?'data-go=\"record\" href=\"/record\"':`href=\"#rs-${k}\"`}>${e?`<span class=\"ex\">${e===1?'EXPERIMENTAL':e}</span>`:''}<h4>${t}</h4><p>${d}</p><span class=\"st\">${x}</span></a>`).join('');",
    "const card=([k,t,d,x,e])=>`<a class=\"rcard\" ${k==='record'?'data-go=\"record\" href=\"/record\"':`href=\"#rs-${k}\"`}>${e?`<span class=\"ex\">${e===1?'EXPERIMENTAL':e}</span>`:''}<h4>${t}</h4><p>${d}</p><span class=\"st\">${x}</span></a>`;\n const TON=['v7','beta','perfect'];\n hub.innerHTML=`<h3 class=\"rgrp\">Tonight</h3><div class=\"rhubg\">${CARDS.filter(c=>TON.includes(c[0])).sort((a,b)=>TON.indexOf(a[0])-TON.indexOf(b[0])).map(card).join('')}</div><h3 class=\"rgrp\">Track record</h3><div class=\"rhubg\">${CARDS.filter(c=>!TON.includes(c[0])).map(card).join('')}</div>`;")
rep('.rcard{display:block;', '.rhub{display:block!important}.rhubg{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:12px;margin-bottom:8px}.rgrp{font-family:var(--mono,monospace);font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--acc);margin:18px 0 10px}\n.rcard{display:block;')
s = s.replace("['beta','Beta Test Mode','+100 to -150 player lines, 1,000 sims per game, tested against the price.'", "['beta','Beta Test Mode: simulations','Each AI agent and our own model run 1,000 sims per game on near-even lines, compared to the price.'")
s = s.replace("['perfect','Perfect parlays','The latest attempt, every suggested ticket graded leg by leg, and the hindsight builds.'", "['perfect','Perfect parlays','Tonight\\'s attempt, every suggested ticket graded leg by leg, and the hindsight builds.'")
# Tonight view wording
s = s.replace('<h2>Market check <small>Engine v7</small></h2>', '<h2>Tonight <small>Engine v8</small></h2>')
s = s.replace('<p class="note" style="max-width:780px">Four AI models grade every leg starting from the Kalshi price. We publish the middle number, capped at Kalshi + 7. When the models\' middle number is 8 or more above Kalshi,',
              '<p class="note" style="max-width:780px">Four AI analysts grade every leg blind, with no market price shown, and our grade is the middle of their numbers plus our own system grade. Kalshi referees after that. When our grade is 8 or more above Kalshi,')
# Method page
if 'Engine v8 (from the Nov 20 late games)' not in s:
    rep('<h2>How we grade now <small>updated Nov 20 · Engine v7</small></h2>', '<h2>How we grade now <small>updated Nov 20 · Engine v8</small></h2>')
    rep('<li><b>Engine v7 (from the Nov 20 board)</b>',
        '<li><b>Engine v8 (from the Nov 20 late games)</b><span>Four AI analysts grade every leg blind: no Kalshi or sportsbook price is shown, so they have to do the research (minutes and role, injuries and news, the matchup and primary defender, shot zones, rest and travel, pace, and weather for football). Our grade is the middle of their four numbers plus our own system grade. Then Kalshi referees: at or above us is GREEN, 1 to 7 below us is YELLOW, and 8 or more below us is pulled, because that gap has lost most often in our record. Each agent also runs 1,000 simulations per game on near-even lines, shown on Research, Beta Test Mode.</span><em>FROM NOV 20</em></li>\n      <li><b>Engine v7 (Nov 20 early games)</b>')
open(F, 'w').write(s); print('v8 site pass applied')
