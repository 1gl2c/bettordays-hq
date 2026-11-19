import json,re
p='bettordays-hq.html';s=open(p).read()
G=json.load(open('fri/fri_graded.json'))
res={r['p']:r.get('r','') for r in G}
act={r['p']:r.get('act') for r in G}
i=s.index('const FRI=');j=s.index(';\n',i);a=json.loads(s[i+10:j])
for r in a:
  r['r']=res.get(r['p'],'')
  if act.get(r['p']) is not None: r['n']=f"Actual: {act[r['p']]}. "+r['n']
s=s[:i+10]+json.dumps(a)+s[j:]
i=s.index('const FTIX=');j=s.index(';\n',i);t=json.loads(s[i+11:j])
for x,v in zip(t,['L','L','W','L']): x['res']=v
s=s[:i+11]+json.dumps(t)+s[j:]
# ROWS
m=re.search(r'const ROWS=(\[.*?\]);\n',s);R=json.loads(m.group(1))
def stat(t):
  t=t.lower()
  for k,v in [('pra','pra'),('3pm','3pm'),('three','3pm'),('pointers','3pm'),('assist','ast'),('rebound','reb'),('point','pts')]:
    if k in t: return v
  return 'other'
for r in a:
  if not r.get('r'): continue
  R.append({'day':'Nov 13','pick':r['p'],'est':r['pct'],'hit':1 if r['r']=='W' else 0,'sport':r['sp'],'mkt':'prop' if r['ty']=='prop' else r['ty'],'stat':stat(r['p']) if r['ty']=='prop' else r['ty'],'dir':'o','style':r['st'],'boost':1 if r.get('moved') else 0,'star':0,'fav':0})
s=s[:m.start(1)]+json.dumps(R)+s[m.end(1):]
t70=[r for r in R if r['est']>=70];print('rows',len(R),sum(r['hit'] for r in t70),len(t70),sum(r['hit'] for r in R))
rep=[('<b class="acc"><span data-count="18">0</span>-12</b><small>hammers and main parlays, Nov 4 to 12</small>','<b class="acc"><span data-count="19">0</span>-20</b><small>hammers and main parlays, Nov 4 to 13</small>'),
('+$<span data-count="3813">0</span></b><small>Thursday added +$548 on main tickets</small>','+$<span data-count="3023">0</span></b><small>Friday lost $790. Our first losing night in 5.</small>'),
('<span data-count="156">0</span>/183</b><small>85% across 9 days · Thursday 30 of 35</small>','<span data-count="198">0</span>/241</b><small>82% across 10 days · Friday 42 of 58</small>'),
('<span data-count="66">0</span>%</b><small>612 graded legs, all tiers</small>','<span data-count="66">0</span>%</b><small>709 graded legs, all tiers</small>'),
('<p class="proof"><b>85%</b> of our 70%+ picks hit · 156 of 183 graded · last night <b>86%</b></p>','<p class="proof"><b>82%</b> of our 70%+ picks hit · 198 of 241 graded · last night <b>72%</b>, our worst night</p>'),
('Friday Nov 13 picks are live · 9 NBA games + college','Friday graded · 42 of 58 at 70%+ · Saturday board next')]
for o,n in rep:
  assert o in s,o[:60]; s=s.replace(o,n)
sec=open('sec13.html').read()
s=s.replace('<section class="panel" id="review12">',sec+'<section class="panel" id="review12">',1)
s=s.replace("review12:'results',","review13:'results',review12:'results',")
assert "review13:'results'" in s
day=open('day13.txt').read()
s=s.replace("const DAYS=[\n","const DAYS=[\n"+day,1)
open(p,'w').write(s);print('ok')
