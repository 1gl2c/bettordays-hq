"""One-time site upgrade for Engine v7 (run once from pipeline/, Nov 20). Code and wording only; no board data changes.
- V7 flag: true when the current board's rows carry a v7 tier.
- Ticket builder: v7 Hammer check on v7 boards (old rule text kept for older boards).
- Research: new "Market check" view (removed legs, GREEN-only tickets, model split, tips) fed by V7D.
- Method page and the marbles rule card describe v7.
"""
F = 'bettordays-hq.html'; s = open(F).read()
assert 'const V7=' not in s, 'already applied'

def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:100]); s = s.replace(a, b)

# 1. flag + data holder (publish_v7.py fills V7D)
rep("const CUR=TH19,CTIX=THTIX,CURD='2026-11-19';",
    "const CUR=TH19,CTIX=THTIX,CURD='2026-11-19';\nconst V7=!!(CUR.length&&CUR[0].tier);\nconst V7D=null;")

# 2. ticket builder Hammer check
rep("const hamBad=rs.filter(r=>!(r.pct>=80&&r.k!=null&&Math.abs(r.pct-r.k)<=7));const ham=!hamBad.length;",
    "const v7s=r=>{const t=r.p.toLowerCase();if(r.ty==='ml'||/ ml /i.test(r.p+' '))return r.k!=null&&r.k>=50;if(/points \\+ rebounds|rushing|receiving|passing|touchdown|rebound/.test(t))return false;return /three|assist|point/.test(t)};"
    "const hamWhy=r=>r.k==null?'no Kalshi price':r.pct<75?'graded '+r.pct:r.k<r.pct-3?'Kalshi '+r.k+' vs our '+r.pct:!v7s(r)?'market type':r.b2b?'back-to-back':/RULE/.test(r.fl||'')?'Ace rule':'';"
    "const hamBad=V7?rs.filter(r=>hamWhy(r)):rs.filter(r=>!(r.pct>=80&&r.k!=null&&Math.abs(r.pct-r.k)<=7));"
    "const hamShape=!V7||(rs.length>=3&&rs.length<=5&&!dup.length);const ham=!hamBad.length&&hamShape;")
rep("${ham?'<b style=\"color:var(--acc)\">Hammer check: every leg is graded 80+ with Kalshi within 7. This rule is provisional, not proven.</b>':`<b style=\"color:var(--warn)\">Not Hammer eligible: ${hamBad.map(r=>r.p+' ('+(r.k==null?'no Kalshi price':r.pct<80?'graded '+r.pct:'Kalshi '+r.k+' vs our '+r.pct)+')').join(', ')}. A Hammer needs every leg graded 80+ with Kalshi within 7.</b>`}",
    "${V7?(ham?'<b style=\"color:var(--acc)\">Hammer check (Engine v7): 3 to 5 legs from different games, each 75+ with Kalshi at or above us or within 3, points, assists, threes or favorite moneylines, no back-to-backs. A rule we are testing, not proof.</b>':`<b style=\"color:var(--warn)\">Not Hammer eligible: ${hamBad.length?hamBad.map(r=>r.p+' ('+hamWhy(r)+')').join(', ')+'. ':''}${hamShape?'':'A Hammer has 3 to 5 legs from different games. '}Engine v7 Hammer: each leg 75+ with Kalshi at or above us or within 3, points, assists, threes or favorite moneylines, no back-to-backs.</b>`):(ham?'<b style=\"color:var(--acc)\">Hammer check: every leg is graded 80+ with Kalshi within 7. This rule is provisional, not proven.</b>':`<b style=\"color:var(--warn)\">Not Hammer eligible: ${hamBad.map(r=>r.p+' ('+(r.k==null?'no Kalshi price':r.pct<80?'graded '+r.pct:'Kalshi '+r.k+' vs our '+r.pct)+')').join(', ')}. A Hammer needs every leg graded 80+ with Kalshi within 7.</b>`)}")

# 3. research: Market check view
rep("const CARDS=[['hits','What actually hits',",
    "const CARDS=[['v7','Market check (Engine v7)','Legs the market disagrees with, GREEN-only tickets, and where the AI models split.',V7D?V7D.label:'Starts with the Nov 20 board',1],\n  ['hits','What actually hits',")
sec = '''<section class="panel rsv" id="v7lab" data-v="v7">
    <h2>Market check <small>Engine v7</small></h2>
    <p class="note" style="max-width:780px">Four AI models grade every leg starting from the Kalshi price. We publish the middle number, capped at Kalshi + 7. When the models' middle number is 8 or more above Kalshi, the leg is removed from the board, the Hammer and every ticket, and listed here as <b>market disagrees</b>. It is still graded the next morning, so we can see whether the market or the models were right.</p>
    <div id="v7body"></div>
  </section>
  '''
rep('<section class="panel rsv" id="betalab" data-v="perfect">', sec + '<section class="panel rsv" id="betalab" data-v="perfect">')
rep("const MAP={", "const MAP={v7lab:'research',")
js = r'''
(function(){const el=document.getElementById('v7body');if(!el)return;
 if(!V7D){el.innerHTML='<p class="note">Engine v7 starts with the Nov 20 board. Each night this page will show the legs we removed because the market disagrees, the GREEN-only tickets (Safe, Core, Stretch), where the AI models agreed and split, and their best tips for the site.</p>';return}
 const MN={chatgpt:'ChatGPT',gemini:'Gemini',grok:'Grok',claude:'Claude'};const ms=o=>Object.keys(MN).map(k=>o&&o[k]!=null?`${MN[k]} ${o[k]}`:null).filter(Boolean).join(' · ')||'-';
 const rs=x=>x.r?` <span class="res ${x.r==='W'?'w':'l'}">${x.r}</span>${x.act!=null?' <small>'+x.act+'</small>':''}`:'';
 const st=Object.entries(V7D.models||{}).map(([k,v])=>`${MN[k]||k}: ${v}`).join(' · ');
 let h=`<p class="tiny" style="margin:0 0 12px">${V7D.label} · ${st}</p>`;
 h+=`<h3>Market disagrees <small>${V7D.rm.length} leg${V7D.rm.length===1?'':'s'} removed</small></h3>`;
 h+=V7D.rm.length?`<div class="scroll"><table class="board"><thead><tr><th>Leg</th><th>Game</th><th>Models' middle</th><th>Kalshi</th><th>Gap</th><th>Each model</th><th>Result</th></tr></thead><tbody>${V7D.rm.map(x=>`<tr><td>${x.p}</td><td class="lbl">${x.g} ${x.t||''}</td><td class="mono">${x.med}</td><td class="mono">${x.k}</td><td class="mono" style="color:var(--warn)">+${x.med-x.k}</td><td><small>${ms(x.ms)}</small></td><td class="mono">${rs(x)||'-'}</td></tr>`).join('')}</tbody></table></div>`:'<p class="note">No leg was 8 or more above Kalshi today.</p>';
 h+=`<h3 style="margin-top:20px">Perfect parlays <small>GREEN legs only (Kalshi at or above our grade), different games</small></h3><div class="struct">`+V7D.perf.map(t=>`<div class="st"><h3>${t.name}${t.res?` <span class="res ${t.res==='W'?'w':'l'}">${t.res==='W'?'CASHED':'MISSED'}</span>`:''}</h3>${t.legs.length?t.legs.map(l=>`<div class="row"${l.r==='L'?' style="color:var(--bad)"':''}><span>${l.r==='W'?'✓ ':l.r==='L'?'✗ ':''}${l.p}</span><b>${l.pub}<small class="kp">K ${l.k}</small></b></div>`).join('')+`<div class="row"><span>Payout at Kalshi's prices</span><b>about ${t.pay}x</b></div><div class="row"><span>Hit chance by our grades</span><b>about ${t.hit}%</b></div><p class="note" style="margin:10px 0 0">${t.why||''} Every leg is from a different game, so no two legs share a game script, but they can all miss on the same night.${t.name==='Stretch'?' Higher risk.':''}</p>`:`<p class="note" style="margin:0">${t.none}</p>`}</div>`).join('')+'</div>';
 const row=x=>`<li>${x.p} <small class="kp">K ${x.k==null?'none':x.k}</small> <small>${ms(x.ms)}</small>${rs(x)}</li>`;
 h+=`<div class="two" style="margin-top:20px"><div><h3>Where the models agreed</h3><ul class="tueo" style="font-size:12.5px;line-height:1.75">${V7D.agree.map(row).join('')||'<li>No 70+ leg had all models within 5.</li>'}</ul></div><div><h3>Where they split (15+ apart)</h3><ul class="tueo" style="font-size:12.5px;line-height:1.75">${V7D.split.map(row).join('')||'<li>No big splits today.</li>'}</ul></div></div>`;
 h+=`<h3 style="margin-top:20px">Site tips from the models</h3><ul class="tueo" style="font-size:12.5px;line-height:1.75">${V7D.tips.map(t=>`<li>${t.tip} <small>(${t.who})</small></li>`).join('')||'<li>None today.</li>'}</ul>`;
 el.innerHTML=h})();
'''
rep("\n(function(){\n\n // every suggested ticket we posted, graded leg by leg", js + "\n(function(){\n\n // every suggested ticket we posted, graded leg by leg")

# 4. Method page and marbles card
rep('<h2>How we grade now <small>updated Nov 19</small></h2>', '<h2>How we grade now <small>updated Nov 20 · Engine v7</small></h2>')
rep('<li><b>Grades come from our original process</b><span>Each pick is graded',
    '''<li><b>Engine v7 (from the Nov 20 board)</b><span>Four AI models grade every leg, starting from the Kalshi price and moving off it only for a named reason. We publish the middle of their numbers, capped at Kalshi + 7. If that middle number is 8 or more above Kalshi, the leg is removed from the board, the Hammer and every ticket, and shown on Research as "market disagrees". Legs with no Kalshi price max out at 75 and never go on the Hammer. The board shows GREEN legs (Kalshi at or above us) and YELLOW legs (1 to 7 above) graded 70+. Our own system grade is still computed and saved next to the models' numbers.</span><em>FROM NOV 20</em></li>
      <li><b>Hammer under v7</b><span>3 to 5 legs from different games, each published 75+ with Kalshi at or above us or within 3, points, assists, threes or favorite moneylines, no back-to-backs, paying 2x or more. If fewer than 3 legs qualify, there is no Hammer that night. Passing is a win.</span><em>FROM NOV 20</em></li>
      <li><b>Through Nov 19, grades came from our original process</b><span>Each pick is graded''')
rep('<li class="obs"><b>Hammer: every leg 80+ with Kalshi within 7</b><span>67-7 on Nov 4 to 17, against 23-22 for 80+ legs outside it. The rule was picked after seeing that data, so it is provisional until it holds on new nights.</span><em>PROVISIONAL</em></li>',
    '<li class="obs"><b>Old Hammer rule: every leg 80+ with Kalshi within 7</b><span>67-7 on Nov 4 to 17, against 23-22 for 80+ legs outside it. The rule was picked after seeing that data. Replaced by the v7 Hammer from Nov 20.</span><em>RETIRED NOV 20</em></li>')
rep('<p>Tickets are built from 70%+ legs, but legs where our grade is 8 or more above Kalshi (⚠) stay out, because those have hit less often. A Hammer needs every leg graded 80+ with Kalshi within 7. Fewer legs means more green-only pulls.</p>',
    '<p>From Nov 20 (Engine v7), legs where the models are 8 or more above Kalshi are removed before the board goes up, and every published grade is capped at Kalshi + 7. A Hammer needs 3 to 5 legs graded 75+ with Kalshi at or above us or within 3. Fewer legs means more green-only pulls.</p>')
open(F, 'w').write(s); print('v7 code applied')
