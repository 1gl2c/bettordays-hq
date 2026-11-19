import re,json
s=open('bettordays-hq.html').read()
assert 'id="review10"' not in s, 'already patched'
G=json.load(open('study/nov10_graded.json'))
for x in G:
  r=x.pop('r'); a=x.pop('act')
  if r in 'WL': x['r']=r
  if a: x['n']=x['n']+f' <b style="color:#cfe">Final: {a}</b>'
  if r=='P': x['n']+=' <i style="color:#ffb020">Result pending</i>'
s=re.sub(r'const TUE=\[.*?\];\n', lambda m:'const TUE='+json.dumps(G)+';\n', s, count=1, flags=re.S)

T=json.loads(re.search(r'const TTIX=(\[.*?\]);\n',s).group(1))
res={'Hammer':('L','Missed by one leg: Jaylen Brown under 15. The other five hit.'),
 '2x':('?','Not played. Four legs hit; SGA boards still unverified.'),
 '9-leg':('W','Paid 5.34x: $534.18 back on $100. Built by Ace from the 70%+ list.'),
 '5-leg · sharp':('L','Missed by one leg: 76ers ML (graded 54). Would have paid about $625.'),
 '20x':('L','Brown 20+, OKC ML and Brunson 6+ assists missed. Bailey, Maluach and Deni hit.'),
 'Late 5':('L','Missed by one leg: OKC ML (graded 55). Without it, about 2.6x and a cash.'),
 'Late 3':('W','Paid 2.29x: $229.30 back on $99.98.'),
 '5-10x':('L','Not played. Brown 20+ would have sunk it.'),
 'Normal':('L','Not played. Brown 20+ would have sunk it.'),
 '100x':('L','Not played. Brown 20+ would have sunk it.'),
 'Lotto #2':('L','Not played. Brown 15+ would have sunk it.')}
for t in T:
  for k,(r,v) in res.items():
    if t['t'].startswith(k): t['res']=r; t['v']=v+' '+t['v'] if r!='?' else v; break
  if t['t'].startswith('9-leg'):
    t['legs']=["Deni Avdija over 0.5 3 pointers made","Donovan Clingan under 14 rebounds","Darius Acuff Jr. o1.5 Threes Made","ORLANDO ML V KINGS","Rui Hachimura 10+ points","Maluach 4+ reb","Ace Bailey 10+ pts","Darryn Peterson 15 + points","Joel Embiid 6+ rebounds"]
    t['lock']='Kalshi paid 5.34x ($534.18)'; t['t']='9-leg · Ace build · PLAYED'
s=re.sub(r'const TTIX=\[.*?\];\n', lambda m:'const TTIX='+json.dumps(T)+';\n', s, count=1, flags=re.S)
old_r=re.search(r"document\.getElementById\('tueTix'\)\.innerHTML=TTIX\.map\(.*?\.join\(''\);\n",s,re.S).group(0)
new_r="""const XR={'Ace Bailey 10+ pts':'W'};
document.getElementById('tueTix').innerHTML=TTIX.map(t=>{const pl=t.t.includes('PLAYED');const lab=t.res==='W'?'CASHED':t.res==='L'?(pl?'MISSED':'WOULD MISS'):'NOT PLAYED';return `<div class="st"${pl?' style="border-color:'+(t.res==='W'?'var(--acc)':'var(--line)')+';box-shadow:'+(t.res==='W'?'0 0 22px rgba(4,255,159,.22)':'none')+'"':' style="opacity:.6"'}>${pl?'<span class="lbl acc" style="display:block;margin-bottom:4px">● Placed</span>':''}<h3 style="color:${t.c}">${t.t} <span class="res ${t.res==='W'?'w':'l'}">${lab}</span></h3>${t.legs.map(l=>{const r=TUE.find(x=>x.p===l);const k=(r&&r.r)||XR[l];return `<div class="row"${k==='L'?' style="color:var(--bad)"':''}><span>${k==='W'?'✓ ':k==='L'?'✗ ':'· '}${l}</span><b>${r?r.pct:''}</b></div>`}).join('')}<div class="row"><span>Stake</span><b>${t.stake}</b></div><div class="row"><span>Price</span><b>${t.lock}</b></div><p class="note" style="margin:10px 0 0">${t.v}</p></div>`}).join('');
"""
s=s.replace(old_r,new_r)

# ROWS
def stat(p):
  p=p.lower()
  for k,v in [('three','3pm'),('3 point','3pm'),('assist','ast'),(' ast','ast'),('reb','reb'),('pra','pra'),('rush','rush'),('rec yard','rec'),('pass','pass'),('total','total'),('point','pts'),('pts','pts')]:
    if k in p: return v
  return 'ml' if ' ml' in p else 'other'
STARS=['brown','tatum','maxey','embiid','brunson','towns','gilgeous','giannis','adebayo','franz']
new=[]
for x in G:
  if x.get('r') not in ('W','L'): continue
  p=x['p'];pl=p.lower()
  mkt='ml' if ' ml' in pl else 'spread' if re.search(r'[+-]\d+\.5$',p) else 'total' if 'total' in pl else 'prop'
  new.append({"day":"Nov 10","pick":p,"est":x['pct'],"hit":1 if x['r']=='W' else 0,"sport":x['sp'],"mkt":mkt,"stat":stat(p),"dir":"u" if 'under' in pl or ' u1' in pl else 'o',"style":x['st'],"boost":0,"star":1 if any(k in pl for k in STARS) else 0,"fav":0})
R=json.loads(re.search(r'const ROWS=(\[.*?\]);\n',s).group(1))
R=[r for r in R if r['day']!='Nov 10']+new
s=re.sub(r'const ROWS=\[.*?\];\n', lambda m:'const ROWS='+json.dumps(R)+';\n', s, count=1, flags=re.S)
s=s.replace("['Nov 9','Nov 9']];","['Nov 9','Nov 9'],['Nov 10','Nov 10']];")
h70=sum(r['hit'] for r in R if r['est']>=70); n70=sum(1 for r in R if r['est']>=70)
hit=sum(r['hit'] for r in R); n=len(R); p70=round(100*h70/n70)
print('rows',n,hit,h70,n70,p70)

# DAYS
s=s.replace("const DAYS=[\n","""const DAYS=[
 {d:'Tue Nov 10 · NBA, Champions Classic, MACtion',pl:'+$186',tix:[
  ['9-leg Ace build (Kalshi)','$100','5.34x','W','All 70%+ list legs plus Peterson 15+ (25) and Magic ML. Paid $534.18'],
  ['Late 3-leg (Kalshi)','$99.98','2.29x','W','Acuff 2+ threes (4), Magic ML, Heat ML. Paid $229.30'],
  ['Hammer 6-leg (Kalshi)','$123','2.44x','L','Five hit. Jaylen Brown under 15 in his first Philly-Boston game'],
  ['Sharp 5-leg (Kalshi)','$99.98','~6.3x','L','Four hit. 76ers lost by 22 (graded 54)'],
  ['Late 5-leg (Kalshi)','$99.99','4.53x','L','Four hit. OKC lost by 20 (graded 55)'],
  ['20x lotto (Kalshi)','$54.96','19.1x','L','Brown 20+, OKC ML, Brunson 6+ ast (2)'],
 ]},
""",1)

# tiles
s=s.replace('<span data-count="7">0</span>-3</b><small>hammers and main parlays, Nov 4 to 9</small>','<span data-count="9">0</span>-6</b><small>hammers and main parlays, Nov 4 to 10</small>')
s=s.replace('+$<span data-count="2207">0</span></b><small>after Monday\'s 9-leg and Hammer 2.0 cashed</small>','+$<span data-count="2448">0</span></b><small>Tuesday added +$241 on main tickets</small>')
s=s.replace('<span data-count="68">0</span>/83</b><small>82% across 6 days</small>',f'<span data-count="{h70}">0</span>/{n70}</b><small>{p70}% across 7 days · Tuesday 19 of 21</small>')
s=s.replace('<span data-count="61">0</span>%</b><small>350 graded legs, all tiers</small>',f'<span data-count="{round(100*hit/n)}">0</span>%</b><small>{n} graded legs, all tiers</small>')
s=s.replace('<span data-count="0">0</span>/15</b>','<span data-count="0">0</span>/16</b>')
s=s.replace('Tuesday Nov 10 board live · 350 graded legs since Nov 4',f'Wednesday Nov 11 · board drops 2 PM PT · {n} graded legs since Nov 4')
s=s.replace('<h2>Tuesday board · Nov 10 <small>80 picks graded · 6 NBA games, Champions Classic, MACtion</small></h2>','<h2>Tuesday board · Nov 10 <small>FINAL · 39 hit, 19 missed, 16 pending · 70%+ went 19 of 21</small></h2>')
s=s.replace('<h3>Tuesday tickets · 6 placed · every ticket pays 2x or more</h3>','<h3>Tuesday tickets · 6 placed · 2 cashed · +$185.57 on the day</h3>')
s=s.replace('Picture a jar of 100 marbles. 82 are green, 18 are red.',f'Picture a jar of 100 marbles. {p70} are green, {100-p70} are red.')
s=s.replace('<a class="btn" href="#monday">Monday</a>','<a class="btn" href="#drop">Next drop</a><a class="btn" href="#review10">Tue review</a><a class="btn" href="#tuesday">Tuesday</a><a class="btn" href="#monday">Monday</a>')

drop=open('drop_section.html').read()
review=open('review_section.html').read().replace('{H70}',str(h70)).replace('{N70}',str(n70)).replace('{P70}',str(p70))
s=s.replace('  <section class="tiles" aria-label="Record">', drop+'\n  <section class="tiles" aria-label="Record">',1)
s=s.replace('  <section class="panel" id="tuesday">', review+'\n  <section class="panel" id="tuesday">',1)
s=s.replace('/* marbles */', open('drop_js.js').read()+'\n/* marbles */',1)
open('bettordays-hq.html','w').write(s)
print('ok')
