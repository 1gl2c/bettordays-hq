import json,re,unicodedata
D=json.load(open('fri20/res/all.json'));G=D['games']
P={}
for b in D['box'].values():
  for n,v in b.items(): P[unicodedata.normalize('NFKD',n).encode('ascii','ignore').decode().lower().replace('.','').replace("'",'')]=v
J=json.load(open('fri20/fri20.json'));S=J['rows']
# every pick text that appears anywhere tonight: the board rows and the published v7/v8 legs (safer rungs included)
_M=json.load(open('daily/2026-11-20/v7_merged.json'));_seen={r['p'] for r in S}
for l in _M['legs']:
  if l['p'] not in _seen: S.append({'p':l['p'],'g':l.get('g',''),'ty':l.get('ty','prop'),'sp':l.get('sp','NBA'),'pct':l.get('pub'),'extra':1});_seen.add(l['p'])
TEAM={'Utah Valley':'UVU','Utah':'UTAH','Wisconsin':'WIS','Mississippi State':'MSST','Indiana':'IU','Georgia':'UGA','Xavier':'XAV','UCF':'UCF','Duke':'DUKE','Oregon':'ORE','New Mexico':'UNM','Iona':'IONA','Bulls':'CHI','Thunder':'OKC','Cavs':'CLE','Pistons':'DET','Nets':'BKN','Lakers':'LAL','Rockets':'HOU','Nuggets':'DEN','Suns':'PHX'}
def num(v):
  try: return float(str(v).split('/')[0].split('-')[0])
  except: return 0.0
def find(p):
  k=unicodedata.normalize('NFKD',p).encode('ascii','ignore').decode().lower().replace('.','').replace("'",'')
  c=[n for n in P if k.startswith(n)]
  if not c:
    c=[n for n in P if k.startswith(n.replace(' iii','').replace(' jr','').replace(' ii',''))]
  return (max(c,key=len),P[max(c,key=len)]) if c else (None,None)
miss=[]
for r in S:
  p=r['p'];t=p.lower()
  if r.get('fl') in ('OUT','LIVE','VERIFY'): r['r']='';continue
  tg=set(x.strip() for x in re.split(r'@| v ',r.get('g') or ''))
  gk=[k for k in G if set(G[k]['sc'])==tg] or [k for k in G if k.replace(' ','').replace('VS','v')==(r.get('g') or '').replace(' ','')]
  if r['ty']=='total':
    g=G[gk[0]];v=sum(g['sc'].values());m=re.search(r'(over|under) (\d+(?:\.5)?)',p);n=float(m.group(2))
    r['r']='P' if v==n else ('W' if (v>n)==(m.group(1)=='over') else 'L');r['act']=f'{v} total';continue
  g=G[gk[0]] if gk else None
  if r['ty'] in ('ml','spread'):
    tm=next((a for n,a in sorted(TEAM.items(),key=lambda x:-len(x[0])) if p.startswith(n)),None)
    if not tm or not g: miss.append(p);continue
    opp=[x for x in g['sc'] if x!=tm][0]; mar=g['sc'][tm]-g['sc'][opp]
    if r['ty']=='ml': hit=mar>0; r['act']=f"{'Won' if hit else 'Lost'} {g['sc'][tm]}-{g['sc'][opp]}"
    else:
      mm=re.search(r'win by over (\d+(?:\.5)?)',p)
      sp=-float(mm.group(1)) if mm else float(re.search(r'([+-]\d+(?:\.5)?)',p).group(1)); hit=mar+sp>0; r['act']=f"{'Won' if mar>0 else 'Lost'} by {abs(mar)}"
      if mar+sp==0: r['r']='P';continue
    r['r']='W' if hit else 'L';continue
  n,s=find(p)
  if s is None: miss.append(p);continue
  rest=t[len(n):] if t.startswith(n) else t
  if 'touchdown' in t: v=num(s.get('rushing.rushingTouchdowns'))+num(s.get('receiving.receivingTouchdowns')); hit=v>=1; r['act']=f"{int(v)} TD"; r['r']='W' if hit else 'L'; continue
  if 'points + rebounds + assists' in t: v=num(s.get('points'))+num(s.get('rebounds'))+num(s.get('assists'))
  elif 'rushing + receiving' in t or 'rush + rec' in t: v=num(s.get('rushing.rushingYards'))+num(s.get('receiving.receivingYards'))
  elif 'passing attempt' in t: v=num(str(s.get('passing.completions/passingAttempts','0/0')).split('/')[1])
  elif 'passing' in t: v=num(s.get('passing.passingYards'))
  elif 'rushing attempt' in t: v=num(s.get('rushing.rushingAttempts'))
  elif 'rushing' in t or 'rush y' in t: v=num(s.get('rushing.rushingYards'))
  elif 'reception' in t: v=num(s.get('receiving.receptions'))
  elif 'receiving' in t: v=num(s.get('receiving.receivingYards'))
  elif 'int' in rest and 'point' not in rest: v=num(s.get('passing.interceptions'))
  elif 'three' in t: v=num(s.get('threePointFieldGoalsMade-threePointFieldGoalsAttempted'))
  elif 'assist' in t: v=num(s.get('assists'))
  elif 'rebound' in t: v=num(s.get('rebounds'))
  elif 'point' in t: v=num(s.get('points'))
  else: miss.append(p);continue
  if s.get('dnp') and 'points' not in s and not any(k.startswith(('passing','rushing','receiving')) for k in s): miss.append('DNP '+p);continue
  x=float(re.search(r'(\d+(?:\.5)?)',rest).group(1))
  if 'under' in t: hit=v<x
  elif re.search(r'\d\+',rest): hit=v>=x
  elif '.5' in rest: hit=v>x
  else: hit=v>x  # "over N"
  r['r']='W' if hit else 'L'; r['act']=int(v)
json.dump(J,open('fri20/fri20_graded.json','w'))
print('MISSING',miss)
g=[r for r in S if r.get('r') and r.get('pct') is not None]; a7=[r for r in g if r['pct']>=70 and not r.get('fl')]
a7all=[r for r in g if r['pct']>=70]
print('graded',len(g),'hits',sum(r['r']=='W' for r in g),'| 70+ (all)',sum(r['r']=='W' for r in a7all),len(a7all))
for lo,hi in [(88,101),(80,88),(70,80),(60,70),(50,60),(0,50)]:
  b=[r for r in g if lo<=r['pct']<hi]; print(lo,hi,sum(r['r']=='W' for r in b),len(b))
for r in sorted(g,key=lambda r:-r['pct']):
  if r['pct']>=70: print(r['r'],r['pct'],r['p'],'->',r['act'],r.get('fl',''))
