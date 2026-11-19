import json,re
p='bettordays-hq.html';s=open(p).read()
G=json.load(open('sat/sat_graded.json'))
res={r['p']:r.get('r','') for r in G}; act={r['p']:r.get('act') for r in G}
i=s.index('const SAT=');j=s.index(';\n',i);a=json.loads(s[i+10:j])
for r in a:
  r['r']=res.get(r['p'],'')
  if act.get(r['p']) is not None: r['n']=f"Actual: {act[r['p']]}. "+r['n']
s=s[:i+10]+json.dumps(a)+s[j:]
i=s.index('const STIX=');j=s.index(';\n',i);t=json.loads(s[i+11:j])
for x,v in zip(t,['W','W','W','L']): x['res']=v
s=s[:i+11]+json.dumps(t)+s[j:]
m=re.search(r'const ROWS=(\[.*?\]);\n',s);R=json.loads(m.group(1))
assert not any(r['day']=='Nov 14' for r in R)
def stat(t):
  t=t.lower()
  for k,v in [('pra','pra'),('three','3pm'),('assist','ast'),('rebound','reb'),('point','pts')]:
    if k in t: return v
  return 'other'
for r in a:
  if not r.get('r'): continue
  R.append({'day':'Nov 14','pick':r['p'],'est':r['pct'],'hit':1 if r['r']=='W' else 0,'sport':r['sp'],'mkt':'prop' if r['ty']=='prop' else r['ty'],'stat':stat(r['p']) if r['ty']=='prop' else r['ty'],'dir':'u' if 'under' in r['p'].lower() else 'o','style':r['st'],'boost':1 if r.get('moved') else 0,'star':0,'fav':0})
s=s[:m.start(1)]+json.dumps(R)+s[m.end(1):]
t70=[r for r in R if r['est']>=70];H=sum(r['hit'] for r in t70);N=len(t70);A=sum(r['hit'] for r in R)
print('rows',len(R),H,N,round(100*H/N),A,round(100*A/len(R)))
rep=[('<b class="acc"><span data-count="19">0</span>-20</b><small>hammers and main parlays, Nov 4 to 13</small>','<b class="acc"><span data-count="24">0</span>-23</b><small>hammers and main parlays, Nov 4 to 14</small>'),
('+$<span data-count="3023">0</span></b><small>Friday lost $790. Our first losing night in 5.</small>','+$<span data-count="4195">0</span></b><small>Saturday added +$1,172. 5 of 8 tickets cashed.</small>'),
('<span data-count="198">0</span>/241</b><small>82% across 10 days · Friday 42 of 58</small>',f'<span data-count="{H}">0</span>/{N}</b><small>{round(100*H/N)}% across 11 days · Saturday 22 of 24</small>'),
('<span data-count="66">0</span>%</b><small>709 graded legs, all tiers</small>',f'<span data-count="{round(100*A/len(R))}">0</span>%</b><small>{len(R)} graded legs, all tiers</small>'),
('<p class="proof"><b>82%</b> of our 70%+ picks hit · 198 of 241 graded · last night <b>72%</b>, our worst night</p>',f'<p class="proof"><b>{round(100*H/N)}%</b> of our 70%+ picks hit · {H} of {N} graded · last night <b>92%</b></p>'),
('Saturday Nov 14 picks are live · NBA, UFC 334, college football','Saturday graded · 22 of 24 at 70%+ · Sunday board next')]
for o,n in rep:
  assert o in s,o[:60]; s=s.replace(o,n)
sec=open('sec14.html').read()
s=s.replace('<section class="panel" id="review13">',sec+'<section class="panel" id="review13">',1)
s=s.replace("review13:'results',","review14:'results',review13:'results',",1)
assert "review14:'results'" in s
day=""" {d:'Sat Nov 14 · NBA, UFC 334, college',pl:'+$1,172',tix:[
  ['Ace 2-leg Utah + Gane (Kalshi)','$429.93','2.50x','W','Utah 40-39, Gane by decision. Paid $1,075.95'],
  ['Power 2-leg BYU + Traore (Kalshi)','$193.70','2.20x','W','Traore 11, BYU 28-7. Paid $426.45'],
  ['Hammer (Kalshi)','$99.99','2.12x','W','Jenkins 1 three, Boozer 5 ast, Giannis 34, Penn State 42-14. Paid $211.68'],
  ['8-leg (Kalshi)','$34.98','6.13x','W','8 for 8. Paid $214.45'],
  ['Ace 7-leg 10x build (Kalshi)','$99.98','6.51x','W','7 for 7. Ayo 0 assists, Mesquita and Costa won. Paid $650.61'],
  ['Ace 6-leg (Kalshi)','$199.97','','L','Five hit. Murray 7 rebounds on under 6'],
  ['Ace 7-leg (Kalshi)','$195.38','','L','Six hit. Murray 7 rebounds on under 6'],
  ['Ace 2-leg Gane + Nunes (Kalshi)','$153.18','','L','Gane won. Harrison submitted Nunes in R4'],
 ]},
"""
s=s.replace("const DAYS=[\n","const DAYS=[\n"+day,1)
open(p,'w').write(s);print('ok')
