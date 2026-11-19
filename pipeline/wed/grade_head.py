import json,math,re,unicodedata,statistics as S
from collections import defaultdict
L=json.load(open('wed/logs.json'));K=json.load(open('wed/kalshi.json'));OPP=json.load(open('wed/nba_opp.json'))
def phi(z): return 0.5*(1+math.erf(z/math.sqrt(2)))
def nrm(s): return unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode().lower().replace('.','').replace("'",'').strip()
SER={'pts':'KXNBAPTS','reb':'KXNBAREB','ast':'KXNBAAST','3pm':'KXNBA3PT','pra':'KXNBAPRA'}
def mid(m):
  a=float(m['yes_ask_dollars'] or 0);b=float(m['yes_bid_dollars'] or 0);return round(100*((a+b)/2 if a and b else a or b))
KT=defaultdict(dict)
for st,s in SER.items():
  for m in K[s]:
    if '26NOV18' not in m['event_ticker']: continue
    mm=re.match(r'(.+?): (\d+)\+',m['title'])
    if mm: KT[(nrm(mm.group(1)),st)][int(mm.group(2))]=mid(m)
G={}
for g,t,sp in [('MEM@CLE','4:00',('CLE',-4.5)),('HOU@IND','4:00',('HOU',-8.5)),('MIL@MIA','4:00',('MIA',-12.5)),('PHI@ORL','4:00',('PHI',-1.5)),('CHI@BKN','4:30',('BKN',-1.5)),('WSH@TOR','4:30',('TOR',-4.5)),
  ('DET@NO','5:00',('DET',-4.5)),('ATL@OKC','5:00',('OKC',-6.5)),('GS@DAL','5:00',('DAL',-4.5)),('BOS@DEN','6:30',('BOS',-2.5)),('UTAH@LAL','7:00',('LAL',-12.5)),('PHX@SAC','7:00',('PHX',-6.5))]:
  for tm in g.split('@'): G[tm]=(g,t,sp[1] if tm==sp[0] else -sp[1])
def opp(t): a,b=G[t][0].split('@'); return b if t==a else a
B2B={'TOR','DET','UTAH','LAL'}
FULL={'MEM':'Memphis','CLE':'Cleveland','HOU':'Houston','IND':'Indiana','MIL':'Milwaukee','MIA':'Miami','PHI':'Philadelphia','ORL':'Orlando','CHI':'Chicago','BKN':'Brooklyn','WSH':'Washington','TOR':'Toronto','DET':'Detroit','NO':'New Orleans','ATL':'Atlanta','OKC':'Oklahoma City','GS':'Golden State','DAL':'Dallas','BOS':'Boston','DEN':'Denver','UTAH':'Utah','LAL':'the Lakers','PHX':'Phoenix','SAC':'Sacramento'}
NBAK={'pts':'points','reb':'totalRebounds','ast':'assists','3pm':'threePointFieldGoalsMade-threePointFieldGoalsAttempted'}
CFK={'rush':'rushingYards','recyds':'receivingYards'}
UN={'pts':'pts','reb':'reb','ast':'ast','3pm':'threes','pra':'PRA','rush':'rush yds','recyds':'rec yds'}
WORD={'pts':'points','reb':'rebounds','ast':'assists','3pm':'threes','pra':'points + rebounds + assists','rush':'rushing yards','recyds':'receiving yards'}
def f(x,k):
  v=x.get(k,0)
  if isinstance(v,str):
    try: v=float(v.split('-')[0])
    except: v=0
  return v or 0
def vals(p,st):
  g=L[p]['games']
  if st=='pra': return [f(x,'points')+f(x,'totalRebounds')+f(x,'assists') for x in g]
  return [f(x,(NBAK if st in NBAK else CFK)[st]) for x in g]
def prob(p,st,k):
  v=vals(p,st);n=len(v);mu=S.mean(v);cf=st in('rush','recyds')
  sd=max(S.pstdev(v),(0.35*mu+5) if cf else 1.0+0.25*math.sqrt(max(mu,1)))
  pn=1-phi((k-0.5-mu)/sd);hs=sum(x>=k for x in v);h5=sum(x>=k for x in v[:5]);m5=min(5,n)
  ps=(hs+2*pn)/(n+2);p5=(h5+2*ps)/(m5+2)
  return 0.6*ps+0.4*p5,(mu,hs,n,h5,m5)
def ordn(n): return f"{n}{'th' if 10<=n%100<=20 else {1:'st',2:'nd',3:'rd'}.get(n%10,'th')}"
def matchup(team,st,under):
  o=opp(team);k='pts' if st=='pra' else st;val,rk=OPP[o][k][0],OPP[o][k][1]
  soft=rk>=23;tough=rk<=8
  txt=f"Matchup: {FULL[o]} allows {val} {UN[k]} a game, "+(f"{ordn(rk)} fewest in the league" if rk<=15 else f"{ordn(31-rk)} most in the league")
  if under: soft,tough=tough,soft
  return (3 if soft else -5 if tough else 0),txt+(' (good spot).' if soft else ' (tough spot).' if tough else '.'),('good' if soft else 'bad' if tough else '')
