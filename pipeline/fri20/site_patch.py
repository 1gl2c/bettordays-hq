"""Nov 20 site pass after Ace's review: Beta sims for tonight, full grade sheet (every leg, our system grade vs each model vs Kalshi), clearer Research labels."""
import json,re
F='bettordays-hq.html';s=open(F).read()
def rep(a,b,n=1):
  global s;c=s.count(a);assert c==n,(c,a[:90]);s=s.replace(a,b)
# 1. Beta: tonight's run, keep the track record
m=re.search(r'const BETA=(\{.*?\});\n',s);B=json.loads(m.group(1))
T=json.load(open('betafri20/beta_tonight.json'));A=json.load(open('betafri20/all_lines.json'))
T['hist']=B['hist'];T['avg']=round(sum(l['edge'] for l in A)/len(A),1)
s=s.replace(m.group(0),'const BETA='+json.dumps(T)+';\n')
rep("Across all ${BETA.n_lines} lines the sim averaged 4.3 points <i>below</i> break-even.","Across all ${BETA.n_lines} lines the sim averaged ${Math.abs(BETA.avg??4.3)} points <i>${(BETA.avg??-4.3)<0?'below':'above'}</i> break-even.")
rep("`Nov 19: 3-5 · two nights: 12-11`","`Tonight: ${BETA.n_games} games, ${BETA.n_lines} lines simmed · record ${BETA.hist.reduce((a,h)=>a+h.w,0)}-${BETA.hist.reduce((a,h)=>a+h.l,0)}`")
# 2. full grade sheet data
M=json.load(open('daily/2026-11-20/v7_merged.json'))
C={l['i']:l for l in json.load(open('daily/2026-11-20/v7_candidates.json'))['legs']}
place={**{i:'board' for i in M['board']},**{i:'under 70' for i in M['low']},**{i:'removed' for i in M['removed']}}
ALL=[{'p':l['p'],'g':l['g'],'t':l['t'],'k':l['k'],'sys':C[l['i']].get('sys'),'ms':l['models'],'pub':l['pub'],'tier':l['tier'],'pl':place.get(l['i'],''),'rule':bool(l.get('rule')),'fl':l.get('fl') or ''} for l in M['legs']]
ALL.sort(key=lambda x:(x['pub'] is None,-(x['pub'] or 0)))
m=re.search(r'const V7D=(\{.*?\});\n',s);V=json.loads(m.group(1));V['all']=ALL
s=s.replace(m.group(0),'const V7D='+json.dumps(V)+';\n')
rep(" el.innerHTML=h})();\n",""" if(V7D.all){const gap=x=>x.sys==null||x.k==null?'':(x.sys-x.k>0?'+':'')+(x.sys-x.k);
  h+=`<h3 style="margin-top:20px">Full grade sheet <small>all ${V7D.all.length} legs, under 70 included</small></h3><p class="note" style="max-width:780px">Published = what the board shows (the models' middle number, capped at Kalshi + 7). <b>Our system</b> is our own grade from game logs and matchup, computed before the models ran. Gap = our system minus Kalshi. Through Nov 19, legs where our system sat 8+ above Kalshi hit far less often than the rest, so a big plus gap is a warning, not an edge.</p><div class="scroll"><table class="board"><thead><tr><th>Leg</th><th>Game</th><th>Published</th><th>Kalshi</th><th>Our system</th><th>Gap</th><th>ChatGPT · Gemini · Grok · Claude</th><th>Where</th></tr></thead><tbody>${V7D.all.map(x=>`<tr${x.rule?' style="opacity:.55"':''}><td>${x.p}${x.rule?' <small>(Ace rule)</small>':''}${x.fl==='Q'?' <small>(questionable)</small>':''}</td><td class="lbl">${x.g} ${x.t}</td><td class="mono"><b>${x.pub??'-'}</b></td><td class="mono">${x.k??'none'}</td><td class="mono">${x.sys??'-'}</td><td class="mono" style="color:${(x.sys-x.k)>=8?'var(--warn)':'inherit'}">${gap(x)}</td><td class="mono"><small>${['chatgpt','gemini','grok','claude'].map(k=>x.ms[k]??'-').join(' · ')}</small></td><td class="lbl">${x.pl}</td></tr>`).join('')}</tbody></table></div>`}
 el.innerHTML=h})();
""")
# 3. tips up top, and clearer labels
rep("h+=`<h3>Market disagrees <small>","h+=`<h3>Site tips from the models <small>each model's top ideas tonight</small></h3><ul class=\"tueo\" style=\"font-size:12.5px;line-height:1.75\">${V7D.tips.map(t=>`<li>${t.tip} <small>(${t.who})</small></li>`).join('')||'<li>None today.</li>'}</ul>`;\n h+=`<h3 style=\"margin-top:20px\">Market disagrees <small>")
rep("['v7','Market check (Engine v7)','Legs the market disagrees with, GREEN-only tickets, and where the AI models split.',V7D?V7D.label:'Starts with the Nov 20 board',1]",
    "['v7','Tonight: full grade sheet','Every leg, under 70 included: our own grade, each AI model, Kalshi, the AI tips, GREEN-only parlays and legs the market disagrees with.',V7D?V7D.label:'Starts with the Nov 20 board','TONIGHT']")
rep("['beta','Beta Test Mode','+100 to -150 player lines, 1,000 sims per game, tested against the price.',","['beta','Beta Test Mode','+100 to -150 player lines, 1,000 sims per game, tested against the price.',")
s=s.replace("`Nov 19: 3-5 · two nights: 12-11`,1]","`x`,1]")
s=re.sub(r"(\['beta','Beta Test Mode'.*?),1\]",r"\1,'SIMS TONIGHT']",s,count=1)
s=re.sub(r"(\['perfect','Perfect parlays'.*?),1\]",r"\1,'TEST']",s,count=1)
rep("${e?'<span class=\"ex\">EXPERIMENTAL</span>':''}","${e?`<span class=\"ex\">${e===1?'EXPERIMENTAL':e}</span>`:''}")
open(F,'w').write(s);print('ok',len(ALL))
