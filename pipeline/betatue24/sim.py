# Nov 24 run of beta/sim.py (3 games from 4:00 PM PT): inputs only (paths, date, games and ESPN spreads at 3:05 PM PT, OUT/Q from the ESPN injury feed at 3:10 PM PT, no back-to-backs). Method unchanged.
import json,re,math,random,unicodedata,statistics as S
from collections import defaultdict
random.seed(24)
L=json.load(open('betatue24/logs.json'));K=json.load(open('betatue24/kalshi2.json'));K0=json.load(open('betatue24/kalshi2.json'));OPP=json.load(open('sat21/nba_opp.json'))
TS=open('betatue24/kalshi2_ts.txt').read().strip();TS0=open('betatue24/kalshi2_ts.txt').read().strip()
def nrm(s): return unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode().lower().replace('.','').replace("'",'').strip()
LN={nrm(v.get('disp') or k):v for k,v in L.items()}
G={}
for g,t,sp in [('DET@ORL','4:00',('DET',-2.5)),('BOS@WSH','5:00',('BOS',-10.5)),('DAL@DEN','7:00',('DEN',-8.5))]:
  for tm in g.split('@'): G[tm]=(g,t,sp[1] if tm==sp[0] else -sp[1])
B2B=set()  # none of the six teams played Nov 23 (ESPN scoreboard)
_I=json.load(open('betatue24/inj_sets.json'));OUT=set(_I['out'])
Q=set(_I['q'])
SER={'KXNBAPTS':'pts','KXNBAREB':'reb','KXNBAAST':'ast','KXNBA3PT':'3pm','KXNBAPRA':'pra'}
WORD={'pts':'points','reb':'rebounds','ast':'assists','3pm':'threes','pra':'PRA'}
def f(x,k):
  v=x.get(k,0)
  if isinstance(v,str):
    try: v=float(v.split('-')[0])
    except: v=0
  return v or 0
def val(x,st):
  if st=='pra': return f(x,'points')+f(x,'totalRebounds')+f(x,'assists')
  return f(x,{'pts':'points','reb':'totalRebounds','ast':'assists','3pm':'threePointFieldGoalsMade-threePointFieldGoalsAttempted'}[st])
def mid(m):
  a=float(m['yes_ask_dollars'] or 0);b=float(m['yes_bid_dollars'] or 0);return round(100*(a+b)/2,1)
old={m['ticker']:m for s in SER for m in K0.get(s,[])}
lines=[]
for s,ms in K.items():
  st=SER[s]
  for m in ms:
    if '26NOV24' not in m['event_ticker']: continue
    a=float(m['yes_ask_dollars'] or 0);b=float(m['yes_bid_dollars'] or 0)
    if not(0.50<=a<=0.60 and b>0 and a-b<=0.05): continue
    mm=re.match(r'(.+?): (\d+)\+',m['title']);nm=nrm(mm.group(1));k=int(mm.group(2))
    p=LN.get(nm)
    if not p or len(p.get('games',[]))<8 or nm in OUT: continue
    team=p['team']
    if team not in G: continue
    o=old.get(m['ticker'])
    lines.append(dict(ticker=m['ticker'],player=mm.group(1),nm=nm,team=team,st=st,k=k,ask=a,bid=b,mid=mid(m),mid0=mid(o) if o else None,games=p['games']))
# simulate each game 1,000 times: shared game and team environment, each player's night drawn from his own season
N=1000
byg=defaultdict(list)
for l in lines: byg[G[l['team']][0]].append(l)
def opprank(team,st):
  a,b=G[team][0].split('@');o=b if team==a else a
  return OPP[o]['pts' if st=='pra' else st][1]
for g,ls in byg.items():
  hits={id(l):0 for l in ls}
  for _ in range(N):
    ge=random.gauss(1,0.04);te={t:ge*random.gauss(1,0.07) for t in g.split('@')}
    for l in ls:
      gl=l['games'];w=[2 if i<5 else 1 for i in range(len(gl))]
      x=random.choices(gl,weights=w)[0];v=val(x,l['st'])
      e=te[l['team']]
      rk=opprank(l['team'],l['st']);e*= 1.03 if rk>=23 else 0.97 if rk<=8 else 1.0
      if l['team'] in B2B and l['st'] in('pts','pra','3pm'): e*=0.97
      if l['st'] in('reb','ast'): e=e**0.7
      v=v*e+random.gauss(0,0.6 if l['st'] in('3pm','ast','reb') else 1.5)
      if v>=l['k']-0.5: hits[id(l)]+=1
  for l in ls:
    p=hits[id(l)]/N;l['sim']=round(100*p,1);l['se']=round(100*math.sqrt(p*(1-p)/N),1)
for l in lines:
  q=l['ask'];be=q+0.07*q*(1-q);l['be']=round(100*be,1)
  l['odds']=f"{'-' if q>=0.5 else '+'}{round(100*q/(1-q)) if q>=0.5 else round(100*(1-q)/q)}" if q!=0.5 else '+100'
  if l['odds']=='-100': l['odds']='+100'
  vs=[val(x,l['st']) for x in l['games']];l['n']=len(vs);l['hs']=sum(v>=l['k'] for v in vs);l['h5']=sum(v>=l['k'] for v in vs[:5]);l['avg']=round(S.mean(vs),1)
  pp=l['sim']/100;l['unc']=round(100*1.96*math.sqrt(max(pp*(1-pp),0.04)/l['n']),1)
  l['edge']=round(l['sim']-l['be'],1);l['move']=None if l['mid0'] is None else round(l['mid']-l['mid0'],1)
  l['g'],l['t'],_=G[l['team']];l['q']=l['nm'] in Q
# Top 15: one line per player, best edge, at most 2 per game, skip questionable players
top=[];seenp=set();pg=defaultdict(int)
for l in sorted(lines,key=lambda l:-l['edge']):
  if l['nm'] in seenp or pg[l['g']]>=2 or l['q']: continue
  top.append(l);seenp.add(l['nm']);pg[l['g']]+=1
  if len(top)==15: break
print('lines',len(lines),'games',len(byg),'priced at',TS)
for l in top: print(l['player'],l['k'],WORD[l['st']],l['odds'],'ask',l['ask'],'BE',l['be'],'sim',l['sim'],'±',l['se'],'edge',l['edge'],'n',l['n'],l['hs'],'/',l['n'],'L5',l['h5'],'move',l['move'],l['g'])
print('lines with sim >= break-even:',sum(l['edge']>0 for l in lines),'of',len(lines),' avg edge',round(sum(l['edge'] for l in lines)/len(lines),1))
import datetime
SIMTS=datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds')
json.dump([{k:v for k,v in l.items() if k!='games'} for l in lines],open('betatue24/all_lines.json','w'))
json.dump({'sim_ts':SIMTS,'ts':TS,'ts0':TS0,'n_lines':len(lines),'n_games':len(byg),'top':[{k:v for k,v in l.items() if k!='games'} for l in top],'all_pos':sum(l['edge']>0 for l in lines)},open('betatue24/beta_tonight.json','w'))
