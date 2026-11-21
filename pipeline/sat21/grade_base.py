"""Nov 20 grading (Friday). Same system as Nov 19 (thu/grade.py): logs blend, matchup, Kalshi shown, caps.
Changes for tonight:
- No line given -> we use the Kalshi rung closest to 72 (named in the note).
- A submitted line whose Kalshi price is under 65 also gets a safer rung (Kalshi closest to 80) as its own candidate, marked as a moved line.
- College football props have no Kalshi market, so they are capped at 69 like other college lines.
- Games that tipped before grading are left off (South Dakota State, SFA v Indiana State, GW v UAB)."""
import json,math,re,unicodedata,statistics as S
from collections import defaultdict
D='sat21/'
L=json.load(open(D+'logs.json'));K=json.load(open(D+'kalshi.json'));OPP=json.load(open(D+'nba_opp.json'))
EV='26NOV21'
def phi(z): return 0.5*(1+math.erf(z/math.sqrt(2)))
def nrm(s): return unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode().lower().replace('.','').replace("'",'').strip()
def kmid(m):
  a=float(m['yes_ask_dollars'] or 0);b=float(m['yes_bid_dollars'] or 0);return 100*((a+b)/2 if a and b else a or b)
SER={'pts':'KXNBAPTS','reb':'KXNBAREB','ast':'KXNBAAST','3pm':'KXNBA3PT','pra':'KXNBAPRA'}
KT=defaultdict(dict)
for st,s in SER.items():
  for m in K[s]:
    if EV not in m['event_ticker']: continue
    mm=re.match(r'(.+?): (\d+)\+',m['title'])
    if mm: KT[(nrm(mm.group(1)),st)][int(mm.group(2))]=round(kmid(m))
# ---- NBA games tonight (PT), book spreads/totals from ESPN at 1:10 PM
GM={'MIL@PHI':('10:00 AM','PHI',-10.5,228.5),'POR@NY':('4:30','NY',-3.5,215.5),'LAC@DAL':('5:00','DAL',-5.5,230.5),'MEM@MIN':('5:00','MIN',-6.5,228.5),'NO@SA':('5:00','SA',-18.5,228.5),'BOS@SAC':('7:00','BOS',-13.5,217.5)}
G={}
for g,(t,fav,sp,ou) in GM.items():
  a,b=g.split('@')
  for tm in (a,b): G[tm]=dict(g=g,t=t,sp=(sp if tm==fav else -sp),ou=ou)
OPP_ALIAS={'NY':'NY','SA':'SA','NO':'NO'}
def TK(g): return {'MIL@PHI':'MILPHI','POR@NY':'PORNYK','LAC@DAL':'LACDAL','MEM@MIN':'MEMMIN','NO@SA':'NOPSAS','BOS@SAC':'BOSSAC'}[g]
def opp(t): a,b=G[t]['g'].split('@'); return b if t==a else a
FULL={'MIL':'Milwaukee','PHI':'Philadelphia','POR':'Portland','NY':'New York','LAC':'Los Angeles C','DAL':'Dallas','MEM':'Memphis','MIN':'Minnesota','NO':'New Orleans','SA':'San Antonio','BOS':'Boston','SAC':'Sacramento'}
OPPK={'UTAH':'UTAH','WSH':'WSH','NO':'NO'}
NBAK={'pts':'points','reb':'totalRebounds','ast':'assists','3pm':'threePointFieldGoalsMade-threePointFieldGoalsAttempted'}
FBK={'recyds':'receivingYards','rush':'rushingYards','pass':'passingYards'}
UN={'pts':'pts','reb':'reb','ast':'ast','3pm':'threes','pra':'PRA','recyds':'rec yds','rush':'rush yds','pass':'pass yds'}
WORD={'pts':'points','reb':'rebounds','ast':'assists','3pm':'threes','pra':'points + rebounds + assists','recyds':'receiving yards','rush':'rushing yards','pass':'passing yards'}
def f(x,k):
  v=x.get(k,0)
  if isinstance(v,str):
    try: v=float(v.split('-')[0])
    except: v=0
  return v or 0
def vals(p,st):
  g=L[p]['games']
  if st=='pra': return [f(x,'points')+f(x,'totalRebounds')+f(x,'assists') for x in g]
  return [f(x,(NBAK if st in NBAK else FBK)[st]) for x in g]
def prob(p,st,k):
  v=vals(p,st);n=len(v);mu=S.mean(v);fb=st in FBK
  sd=max(S.pstdev(v),(0.35*mu+5) if fb else 1.0+0.25*math.sqrt(max(mu,1)))
  pn=1-phi((k-0.5-mu)/sd);hs=sum(x>=k for x in v);h5=sum(x>=k for x in v[:5]);m5=min(5,n)
  ps=(hs+2*pn)/(n+2);p5=(h5+2*ps)/(m5+2)
  return 0.6*ps+0.4*p5,(mu,hs,n,h5,m5)
def ordn(n): return f"{n}{'th' if 10<=n%100<=20 else {1:'st',2:'nd',3:'rd'}.get(n%10,'th')}"
def matchup(team,st,under):
  o=opp(team);k='pts' if st=='pra' else st;val,rk=OPP[o][k][0],OPP[o][k][1]
  soft=rk>=23;tough=rk<=8
  txt=f"Matchup: {FULL[o]} allows {val} {UN[k]} a game, {ordn(31-rk)} most in the league"
  if under: soft,tough=tough,soft
  return (3 if soft else -5 if tough else 0),txt+(' (good spot).' if soft else ' (tough spot).' if tough else '.'),('good' if soft else 'bad' if tough else '')
CTX={
 'Tyler Herro':'Now with Milwaukee. Bucks are 10.5-point underdogs at Philly, blowout risk.','Joel Embiid':'76ers -10.5, a big lead could cut his fourth quarter.','Anfernee Simons':'Now with Philadelphia.',
 'LaMelo Ball':'Now with Minnesota.','Karl-Anthony Towns':'Questionable (illness). If he sits, this leg is void.','Devin Vassell':'Spurs -18.5, a blowout could cut his minutes.',
 'Rui Hachimura':'Now with the Clippers.','Kris Dunn':'Clippers +5.5 at Dallas.','Cooper Flagg':'Mavericks -5.5 at home.','Domantas Sabonis':'Kings +13.5 at home against Boston, blowout risk.'}
rows=[];SUB={}
def addp(p,st,k,under=False,label=None,pre='',moved=False,cap=None):
  team=L[p]['team'];g=G[team]
  pr,(mu,hs,n,h5,m5)=prob(p,st,k)
  if under: pr=1-pr;hs=n-hs;h5=m5-h5
  pct=0.8*100*pr+0.2*65
  madj,mtxt,mtag=matchup(team,st,under);pct+=madj
  hard=80 if st=='pra' else 88
  if n<8: pct=0.7*pct+0.3*60
  pct=min(pct,hard)
  if cap: pct=min(pct,cap)
  kk=KT.get((nrm(p),st),{}).get(k);kp=None if kk is None else (100-kk if under else kk)
  knote=''
  if kp is not None:
    if kp<=pct-15: knote=f" Kalshi has this at {kp}, far below us. Look twice."
    elif kp>=pct+15: knote=f" Kalshi has this at {kp}, well above us."
    else: knote=f" Kalshi: {kp}."
  pct=max(5,round(pct))
  disp=L[p].get('disp',p)
  txt=label or (f"{disp} under {k} {WORD[st]}" if under else f"{disp} {k}+ {WORD[st]}")
  note=pre+f"{'Stayed under' if under else 'Hit'} {hs} of {n} this season, {h5} of {m5} last 5 (avg {mu:.1f} {UN[st]}). {mtxt} "+CTX.get(p,'')+knote
  r=dict(p=txt,pct=pct,g=g['g'],t=g['t'],ty='prop',st='alt',n=re.sub(r'\s+',' ',note).strip(),sp='NBA')
  if kp is not None: r['k']=kp
  if mtag: r['mu']=mtag
  if moved: r['moved']=True
  rows.append(r);return len(rows)-1
def ladder(p,st): return KT.get((nrm(p),st),{})
def A(no,p,st,k,under=False,orig=None):
  pre=f"Your line was {orig}. " if orig else ''
  i=addp(p,st,k,under,pre=pre);SUB[no]=i
  kp=rows[i].get('k')
  if not under and kp is not None and kp<65:
    lad={x:v for x,v in ladder(p,st).items() if x<k}
    if lad:
      x=min(lad,key=lambda x:abs(lad[x]-80))
      if lad[x]>=70 and not any(r['p']==f"{L[p]['disp']} {x}+ {WORD[st]}" for r in rows):
        addp(p,st,x,pre=f"Safer line than the {k}+ you sent (Kalshi {kp} there). ",moved=True)
def N(no,p,st):
  lad=ladder(p,st)
  if not lad: SUB[no]=None;print('NO KALSHI LADDER',p,st);return
  x=min(lad,key=lambda x:abs(lad[x]-72))
  SUB[no]=addp(p,st,x,pre=f"No line was given, so we used {x}+, the Kalshi rung priced closest to 72. ",moved=True)
def team(txt,pct,g,t,ty,sp,note,k=None,cap=69,st='reg',fl=None):
  if pct is not None and cap: pct=min(pct,cap)
  r=dict(p=txt,pct=None if pct is None else max(5,round(pct)),g=g,t=t,ty=ty,st=st,n=note,sp=sp)
  if k is not None: r['k']=round(k)
  if fl: r['fl']=fl
  rows.append(r);return len(rows)-1
def kgame(ser,ev,sub):
  for m in K[ser]:
    if ev in m['event_ticker'] and m['yes_sub_title']==sub: return kmid(m)
def kcurve(ser,ev,pat):
  out=[]
  for m in K[ser]:
    if ev in m['event_ticker']:
      mm=re.search(pat,m['title'],re.I)
      if mm: out.append((float(mm.group(1)),kmid(m)))
  return sorted(out)
def kat(c,x):
  for a,p in c:
    if a==x: return p,False
  if c and c[0][0]<x<c[-1][0]:
    for (x0,p0),(x1,p1) in zip(c,c[1:]):
      if x0<=x<=x1: return p0+(p1-p0)*(x-x0)/(x1-x0),True
  return None,False
def kn(k,ki=False,flip=False):
  if k is None: return " No Kalshi price found."
  v=100-k if flip else k
  return f" Kalshi has it at {'about ' if ki else ''}{v:.0f}{' (estimated between two Kalshi lines)' if ki else ''}."
# ---- college football props (no Kalshi market): logs only, capped at 69
CFBG={'Noah Fifita':('ARIZ@KSU','4:00','Arizona -10 at Kansas State, total 53.5.'),'Jesse Legree':('USU@ORST','7:30','Oregon State -7.5 at home, total 51.5.'),
      'L.J. Phillips Jr.':('IOWA@ILL','11:30 AM','Iowa -8.5 at Illinois, total 40.5, a run-first script.'),'Carlos Hernandez':('WAKE@GT','9:00 AM','Started at 9 AM PT.'),
      'Dylan Riley':('SDSU@BOIS','6:30','Boise State -20.5 at home, a big lead could cut his late carries.')}
def CF(no,p,st,k):
  pr,(mu,hs,n,h5,m5)=prob(p,st,k);pct=min(0.8*100*pr+0.2*65,69)
  g,t,c=CFBG[p];disp=L[p]['disp']
  SUB[no]=team(f"{disp} {k}+ {WORD[st]}",pct,g,t,'prop','CFB',f"College football. Hit {hs} of {n} this season, {h5} of {m5} last 5 (avg {mu:.1f} {UN[st]}). {c} No Kalshi market for college player props, so this is capped at 69.",st='alt')
