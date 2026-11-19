import json,re
p='bettordays-hq.html';s=open(p).read()
G=json.load(open('mon/mon_graded.json'))
res={r['p']:r.get('r','') for r in G}; act={r['p']:r.get('act') for r in G}
i=s.index('const MN16=')+11;a,end=json.JSONDecoder().raw_decode(s[i:])
for r in a:
  r['r']=res.get(r['p'],'')
  if act.get(r['p']) is not None: r['n']=f"Actual: {act[r['p']]}. "+r['n']
  if r['p']=='KeAndre Lambert-Smith 10+ receiving yards': r['n']='No stats, did not play. '+r['n']
s=s[:i]+json.dumps(a)+s[i+end:]
i=s.index('const MNTIX=')+12;t,end=json.JSONDecoder().raw_decode(s[i:])
for x,v in zip(t,['L','W','L','L']): x['res']=v
s=s[:i]+json.dumps(t)+s[i+end:]
m=re.search(r'const ROWS=(\[.*?\]);\n',s);R=json.loads(m.group(1))
assert not any(r['day']=='Nov 16' for r in R)
def stat(t):
  t=t.lower()
  if 'points + rebounds + assists' in t: return 'pra'
  if 'rushing + receiving' in t: return 'prop'
  for k,v in [('three','3pm'),('assist','ast'),('rebound','reb'),('receiving y','recyds'),('passing y','pass'),('recept','rec'),('rush','rush'),('point','pts')]:
    if k in t: return v
  return 'prop'
for r in a:
  if not r.get('r'): continue
  atd='touchdown' in r['p'].lower() and 'anytime' in r['p'].lower()
  R.append({'day':'Nov 16','pick':r['p'],'est':r['pct'],'hit':1 if r['r']=='W' else 0,'sport':r['sp'],'mkt':'atd' if atd else r['ty'],'stat':'atd' if atd else (stat(r['p']) if r['ty']=='prop' else r['ty']),'dir':'u' if 'under' in r['p'].lower() else 'o','style':r['st'],'boost':1 if r.get('moved') else 0,'star':0,'fav':0})
s=s[:m.start(1)]+json.dumps(R)+s[m.end(1):]
t70=[r for r in R if r['est']>=70];H=sum(r['hit'] for r in t70);N=len(t70);A=sum(r['hit'] for r in R)
print('rows',len(R),H,N,round(100*H/N),A,round(100*A/len(R)))
rep=[(f'<span data-count="255">0</span>/317</b><small>80% across 12 days · Sunday 35 of 52',f'<span data-count="{H}">0</span>/{N}</b><small>{round(100*H/N)}% across 13 days · Monday 40 of 55'),
('<span data-count="65">0</span>%</b><small>887 graded legs, all tiers',f'<span data-count="{round(100*A/len(R))}">0</span>%</b><small>{len(R)} graded legs, all tiers'),
('<p class="proof"><b>80%</b> of our 70%+ picks hit · 255 of 317 graded · Sunday <b>67%</b>, our worst day</p>',f'<p class="proof"><b>{round(100*H/N)}%</b> of our 70%+ picks hit · {H} of {N} graded · Monday <b>73%</b></p>'),
('Monday Nov 16 picks are live · NBA, Monday Night Football, college hoops · Model v7','Monday graded · 40 of 55 at 70%+ · Model v8 starts Tuesday')]
for o,n in rep:
  assert s.count(o)>=1,o[:70]; s=s.replace(o,n)
sec=open('sec16.html').read()
s=s.replace('<section class="panel" id="review15">',sec+'<section class="panel" id="review15">',1)
s=s.replace("review15:'results',","review16:'results',review15:'results',",1)
open(p,'w').write(s);print('ok')
