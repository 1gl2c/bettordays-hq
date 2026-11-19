import json,re
p='bettordays-hq.html';s=open(p).read()
G=json.load(open('tue/tue_graded.json'))
res={r['p']:r.get('r','') for r in G}; act={r['p']:r.get('act') for r in G}
i=s.index('const TU17=')+11;a,end=json.JSONDecoder().raw_decode(s[i:])
for r in a:
  r['r']=res.get(r['p'],'')
  if r['p'].startswith('Grayson Allen'): r['n']='Did not play, not graded. '+r['n']
  elif act.get(r['p']) is not None: r['n']=f"Actual: {act[r['p']]}. "+r['n']
s=s[:i]+json.dumps(a)+s[i+end:]
i=s.index('const TUTIX=')+12;t,end=json.JSONDecoder().raw_decode(s[i:])
t[0]['res']='L';t[2]['res']='L';t[1]['v']+=' Allen did not play.'
s=s[:i]+json.dumps(t)+s[i+end:]
m=re.search(r'const ROWS=(\[.*?\]);\n',s);R=json.loads(m.group(1))
assert not any(r['day']=='Nov 17' for r in R)
def stat(t):
  t=t.lower()
  if 'points + rebounds + assists' in t: return 'pra'
  for k,v in [('three','3pm'),('assist','ast'),('rebound','reb'),('receiving y','recyds'),('rush','rush'),('point','pts')]:
    if k in t: return v
  return 'prop'
for r in a:
  if not r.get('r'): continue
  R.append({'day':'Nov 17','pick':r['p'],'est':r['pct'],'hit':1 if r['r']=='W' else 0,'sport':r['sp'],'mkt':r['ty'],'stat':stat(r['p']) if r['ty']=='prop' else r['ty'],'dir':'u' if 'under' in r['p'].lower() else 'o','style':r['st'],'boost':1 if r.get('moved') else 0,'star':0,'fav':0})
s=s[:m.start(1)]+json.dumps(R)+s[m.end(1):]
t70=[r for r in R if r['est']>=70];H=sum(r['hit'] for r in t70);N=len(t70);A=sum(r['hit'] for r in R)
print('rows',len(R),H,N,round(100*H/N),A,round(100*A/len(R)))
rep=[('<span data-count="295">0</span>/372</b><small>79% across 13 days · Monday 40 of 55',f'<span data-count="{H}">0</span>/{N}</b><small>{round(100*H/N)}% across 14 days · Tuesday 18 of 27'),
('<span data-count="66">0</span>%</b><small>993 graded legs, all tiers',f'<span data-count="{round(100*A/len(R))}">0</span>%</b><small>{len(R)} graded legs, all tiers'),
('<p class="proof"><b>79%</b> of our 70%+ picks hit · 295 of 372 graded · Monday <b>73%</b></p>',f'<p class="proof"><b>{round(100*H/N)}%</b> of our 70%+ picks hit · {H} of {N} graded · Tuesday <b>67%</b></p>'),
('Tuesday Nov 17 picks are live · NBA, hockey, college hoops and MACtion','Tuesday graded · 18 of 27 at 70%+ · Wednesday board next')]
for o,n in rep:
  assert s.count(o)>=1,o[:70]; s=s.replace(o,n)
sec=open('sec17.html').read()
s=s.replace('<section class="panel" id="review16">',sec+'<section class="panel" id="review16">',1)
s=s.replace("review16:'results',","review17:'results',review16:'results',",1)
# warning marker on rows where our grade is 8+ above Kalshi
o="${r&&r.k!=null?`<small class=\"kp\">K ${r.k}</small>`:''}";n=s.count(o);assert n>=1
s=s.replace(o,"${r&&r.k!=null?`<small class=\"kp\">${r.pct>=r.k+8?'⚠ ':''}K ${r.k}</small>`:''}")
o="${x.k==null?'-':'Kalshi '+x.k}";m2=s.count(o);assert m2>=1
s=s.replace(o,"${x.k==null?'-':(x.pct>=x.k+8?'⚠ ':'')+'Kalshi '+x.k}")
for col in ('#04ff9f','#00c8ff'):
  o=f'${{r.p}} <span style="color:{col}">${{r.pct}}%</span>'+"${r.k!=null?`<small class=\"kp\">K ${r.k}</small>`:''}"
  if o in s: s=s.replace(o,f'${{r.p}} <span style="color:{col}">${{r.pct}}%</span>'+"${r.k!=null?`<small class=\"kp\">${r.pct>=r.k+8?'⚠ ':''}K ${r.k}</small>`:''}")
o="Green means Kalshi has it at or above our grade. Red means Kalshi has it 10 or more below us."
assert o in s;s=s.replace(o,"Green means Kalshi has it at or above our grade. ⚠ means our grade is 8 or more above Kalshi's: those legs hit 3 of 11 over Monday and Tuesday, so think twice before putting one in a parlay.")
open(p,'w').write(s);print('ok',n,m2)
