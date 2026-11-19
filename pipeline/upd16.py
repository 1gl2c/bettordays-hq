import json,re
p='bettordays-hq.html';s=open(p).read()
G=json.load(open('sun/sun_graded.json'))
res={r['p']:(r.get('r','') if r.get('fl')!='VERIFY' else '') for r in G}; act={r['p']:r.get('act') for r in G}
i=s.index('const SN15=');j=s.index(';\n',i);a=json.loads(s[i+11:j])
for r in a:
  r['r']=res.get(r['p'],'')
  if act.get(r['p']) is not None: r['n']=f"Actual: {act[r['p']]}. "+r['n']
s=s[:i+11]+json.dumps(a)+s[j:]
i=s.index('const SUTIX=');j=s.index(';\n',i);t=json.loads(s[i+12:j])
for x in t: x['res']='L'
s=s[:i+12]+json.dumps(t)+s[j:]
# research: new stat categories
o="/rec\\b|recept/i.test(r.p)?'rec':/rush/i.test(r.p)?'rush':"
assert s.count(o)==1
s=s.replace(o,"/rushing \\+ receiving/i.test(r.p)?'prop':/receiving y/i.test(r.p)?'recyds':/passing y/i.test(r.p)?'pass':/rec\\b|recept/i.test(r.p)?'rec':/rush/i.test(r.p)?'rush':")
o="rec:'Receptions',rush:'Rushing',";assert s.count(o)==1
s=s.replace(o,"rec:'Receptions',recyds:'Receiving yards',pass:'Passing yards',rush:'Rushing',")
m=re.search(r'const ROWS=(\[.*?\]);\n',s);R=json.loads(m.group(1))
assert not any(r['day']=='Nov 15' for r in R)
def stat(t):
  t=t.lower()
  if 'rushing + receiving' in t: return 'prop'
  for k,v in [('pra','pra'),('three','3pm'),('assist','ast'),('rebound','reb'),('receiving y','recyds'),('passing y','pass'),('recept','rec'),('rush','rush'),('point','pts')]:
    if k in t: return v
  return 'prop'
for r in a:
  if not r.get('r'): continue
  atd='touchdown' in r['p'].lower()
  R.append({'day':'Nov 15','pick':r['p'],'est':r['pct'],'hit':1 if r['r']=='W' else 0,'sport':r['sp'],'mkt':'atd' if atd else r['ty'],'stat':'atd' if atd else (stat(r['p']) if r['ty']=='prop' else r['ty']),'dir':'u' if 'under' in r['p'].lower() else 'o','style':r['st'],'boost':1 if r.get('moved') else 0,'star':0,'fav':0})
s=s[:m.start(1)]+json.dumps(R)+s[m.end(1):]
t70=[r for r in R if r['est']>=70];H=sum(r['hit'] for r in t70);N=len(t70);A=sum(r['hit'] for r in R)
print('rows',len(R),H,N,round(100*H/N),A,round(100*A/len(R)))
assert (H,N)==(255,317)
rep=[('<span data-count="24">0</span>-23</b><small>hammers and main parlays, Nov 4 to 14','<span data-count="26">0</span>-35</b><small>hammers and main parlays, Nov 4 to 15'),
('<span data-count="4195">0</span></b><small>Saturday added +$1,172. 5 of 8 tickets cashed.','<span data-count="2733">0</span></b><small>Sunday lost $1,462. 2 of 14 tickets cashed. Our worst day.'),
('<span data-count="220">0</span>/265</b><small>83% across 11 days · Saturday 22 of 24',f'<span data-count="{H}">0</span>/{N}</b><small>{round(100*H/N)}% across 12 days · Sunday 35 of 52'),
('<span data-count="66">0</span>%</b><small>769 graded legs, all tiers',f'<span data-count="{round(100*A/len(R))}">0</span>%</b><small>{len(R)} graded legs, all tiers'),
('<p class="proof"><b>83%</b> of our 70%+ picks hit · 220 of 265 graded · last night <b>92%</b></p>',f'<p class="proof"><b>{round(100*H/N)}%</b> of our 70%+ picks hit · {H} of {N} graded · Sunday <b>67%</b>, our worst day</p>'),
('Sunday Nov 15 picks are live · NFL Week 10 and NBA','Sunday graded · 35 of 52 at 70%+ · our worst day · Monday board next')]
for o,n in rep:
  assert s.count(o)>=1,o[:60]; s=s.replace(o,n)
sec=open('sec15.html').read()
s=s.replace('<section class="panel" id="review14">',sec+'<section class="panel" id="review14">',1)
s=s.replace("review14:'results',","review15:'results',review14:'results',",1)
day=""" {d:'Sun Nov 15 · NFL Week 10, NBA',pl:'-$1,462',tix:[
  ['Ace 4-leg hammer (Kalshi)','$687.85','','L','Rodgers 143, Warren 15, Johnson 14 points. Only Johnson rebounds hit'],
  ['Ace 4-leg Luka, Bills, Jaguars, Chiefs (Kalshi)','$369.98','1.86x','W','Luka 43 and three favorites. Paid $688.37'],
  ['Ace 3-leg Luka, McBride, Kyren (Kalshi)','$299.99','','L','Luka 43. McBride 37 on 40+, Kyren 23'],
  ['Ace 4-leg Bills, Jaguars, Olave, Bijan (Kalshi)','$249.99','','L','Olave 30 on 40+. The Beta 3 with McCaffrey would have cashed'],
  ['2-3x (Kalshi)','$100.00','','L','Luka 43, Bills won. McBride 37 on 40+'],
  ['Hammer (Kalshi)','$99.98','','L','Bijan 71, Jaguars, Luka 43. Olave 30 on 40+'],
  ['Power 3 (Kalshi)','$99.98','','L','Cook 157. Bowers 18, Watson 37 on 40+'],
  ['5x stretch (Kalshi)','$99.98','','L','Smith-Njigba 171, Cook 157. Bowers 18, Watson 37'],
  ['Ace 8-leg (Kalshi)','$99.96','','L','Six hit. Kyren 23, Warren 15'],
  ['Friend 3-leg (Kalshi)','$34.99','2.50x','W','Hutchinson, Taylor 40+, Purdy 15+. Paid $87.36'],
  ['Friend 7-leg (Kalshi)','$34.99','','L','Six hit. Watson 37 on 40+'],
  ['Friend 5-leg (Kalshi)','$20.00','','L','Burrow 409, Chase 231. Olave 30, Bowers 18, Warren 41 total'],
  ['Friend 10-leg (Kalshi)','$20.00','','L','Allen 196 on 200+, Olave 30, McBride 37'],
  ['Friend 9-leg (Kalshi)','$19.99','','L','Allen 196 on 200+, McBride 37'],
 ]},
"""
s=s.replace("const DAYS=[\n","const DAYS=[\n"+day,1)
open(p,'w').write(s);print('ok')
