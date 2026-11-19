import json,math,re,unicodedata,statistics as S
from collections import defaultdict
L=json.load(open('thu/logs.json'));M={p:{'team':v.get('team')} for p,v in L.items()};K=json.load(open('thu/kalshi.json'));K.setdefault('KXNFLPASSYDS',[])
OPP=json.load(open('thu/nba_opp.json'));TS=json.load(open('thu/teamstats.json'))
def phi(z): return 0.5*(1+math.erf(z/math.sqrt(2)))
def nrm(s): return unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode().lower().replace('.','').replace("'",'').strip()
# ---- Kalshi tables
SER={'pts':'KXNBAPTS','reb':'KXNBAREB','ast':'KXNBAAST','3pm':'KXNBA3PT','pra':'KXNBAPRA','recyds':'KXNFLRECYDS','rush':'KXNFLRSHYDS','pass':'KXNFLPASSYDS','rec':'KXNFLREC','rr':'KXNFLRRYDS'}
KT=defaultdict(dict)
for st,s in SER.items():
  for m in K[s]:
    if '26NOV19' not in m['event_ticker']: continue
    mm=re.match(r'(.+?): (\d+)\+',m['title'])
    if mm:
      a=float(m['yes_ask_dollars'] or 0);b=float(m['yes_bid_dollars'] or 0)
      KT[(nrm(mm.group(1)),st)][int(mm.group(2))]=round(100*((a+b)/2 if a and b else a or b))
def curve(series,ev,pat):
  out=[]
  for m in K[series]:
    if ev in m['event_ticker']:
      mm=re.search(pat,m['title'],re.I)
      if mm:
        a=float(m['yes_ask_dollars'] or 0);b=float(m['yes_bid_dollars'] or 0)
        out.append((float(mm.group(1)),100*((a+b)/2 if a and b else a or b)))
  return sorted(out)
def interp(c,x):
  if not c: return None
  if x<=c[0][0]: return c[0][1]
  if x>=c[-1][0]: return c[-1][1]
  for (x0,p0),(x1,p1) in zip(c,c[1:]):
    if x0<=x<=x1: return p0+(p1-p0)*(x-x0)/(x1-x0)
def ml(series,ev,name):
  for m in K[series]:
    if ev in m['event_ticker'] and m['title'].lower().startswith(name.lower()):
      a=float(m['yes_ask_dollars'] or 0);b=float(m['yes_bid_dollars'] or 0);return round(100*((a+b)/2 if a and b else a or b))
# ---- games
G={}
for t,(g,tm,sp,ou) in {'GS':('GS@MEM','5:00',5.5,225.5),'MEM':('GS@MEM','5:00',-5.5,225.5),'POR':('POR@MIL','5:00',-11.5,230.5),'MIL':('POR@MIL','5:00',11.5,230.5),'NY':('NY@MIN','5:00',-1.5,216.5),'MIN':('NY@MIN','5:00',1.5,216.5),'LAC':('LAC@SA','5:00',15.5,224.5),'SA':('LAC@SA','5:00',-15.5,224.5),'IND':('IND@HOU','5:15',12.5,44.5),'HOU':('IND@HOU','5:15',-12.5,44.5)}.items(): G[t]=dict(g=g,t=tm,sp=sp,ou=ou)
def opp(t): a,b=G[t]['g'].split('@'); return b if t==a else a
B2B={'MEM','MIL','GS'}
FULL={'GS':'Golden State','MEM':'Memphis','POR':'Portland','MIL':'Milwaukee','NY':'New York','MIN':'Minnesota','LAC':'the Clippers','SA':'San Antonio','IND':'Indianapolis','HOU':'Houston'}
NBAK={'pts':'points','reb':'totalRebounds','ast':'assists','3pm':'threePointFieldGoalsMade-threePointFieldGoalsAttempted'}
NFLK={'recyds':'receivingYards','rush':'rushingYards','pass':'passingYards','rec':'receptions','rushatt':'rushingAttempts'}
UN={'pts':'pts','reb':'reb','ast':'ast','3pm':'threes','pra':'PRA','recyds':'rec yds','rush':'rush yds','pass':'pass yds','rec':'catches','rr':'rush+rec yds','td':'TDs','rushatt':'rush attempts'}
WORD={'td':'touchdowns','pts':'points','reb':'rebounds','ast':'assists','3pm':'threes','pra':'points + rebounds + assists','recyds':'receiving yards','rush':'rushing yards','pass':'passing yards','rec':'receptions','rr':'rushing + receiving yards','rushatt':'rushing attempts'}
def vals(p,st):
  g=L[p]['games']
  def f(x,k):
    v=x.get(k,0)
    if isinstance(v,str):
      try: v=float(v.split('-')[0])
      except: v=0
    return v or 0
  if st=='pra': return [f(x,'points')+f(x,'totalRebounds')+f(x,'assists') for x in g]
  if st=='rr': return [f(x,'rushingYards')+f(x,'receivingYards') for x in g]
  if st=='td': return [f(x,'rushingTouchdowns')+f(x,'receivingTouchdowns') for x in g]
  return [f(x,(NBAK if st in NBAK else NFLK)[st]) for x in g]
def prob(p,st,k):
  v=vals(p,st);n=len(v);mu=S.mean(v);nfl=st in('recyds','rush','pass','rec','rr','td','rushatt')
  sd=max(S.pstdev(v),(0.35*mu+5) if (nfl and st not in('rec','td','rushatt')) else 1.0+0.25*math.sqrt(max(mu,1)))
  pn=1-phi((k-0.5-mu)/sd);hs=sum(x>=k for x in v);h5=sum(x>=k for x in v[:5]);m5=min(5,n)
  ps=(hs+2*pn)/(n+2);p5=(h5+2*ps)/(m5+2)
  return 0.6*ps+0.4*p5,(mu,hs,n,h5,m5)
def ordn(n): return f"{n}{'th' if 10<=n%100<=20 else {1:'st',2:'nd',3:'rd'}.get(n%10,'th')}"
def matchup(team,st,under):
  o=opp(team)
  if st in ('pts','reb','ast','3pm','pra'):
    k='pts' if st=='pra' else st; val,rk=OPP[o][k][0],OPP[o][k][1]
    soft=rk>=23;tough=rk<=8
    txt=f"Matchup: {FULL[o]} allows {val} {UN[k]} a game, {ordn(31-rk)} most in the league"
  else:
    key={'recyds':'opponent.passing.passingYardsPerGame','pass':'opponent.passing.passingYardsPerGame','rec':'opponent.passing.passingYardsPerGame','rush':'opponent.rushing.rushingYardsPerGame','rr':'opponent.rushing.rushingYardsPerGame'}.get(st)
    if not key or key not in TS[o]: return 0,'',''
    _,val,rk=TS[o][key]; rk=int(rk or 16)   # ESPN rank: 1 = fewest allowed
    soft=rk>=23;tough=rk<=8
    txt=f"Matchup: {FULL[o].replace('the ','')} allows {val:.0f} {'passing' if 'passing' in key else 'rushing'} yards a game, {ordn(33-rk)} most in the league"
  if under: soft,tough=tough,soft
  tag='good' if soft else 'bad' if tough else ''
  adj=3 if soft else -5 if tough else 0
  return adj,txt+(' (good spot).' if soft else ' (tough spot).' if tough else '.'),tag
CTX={'LaMelo Ball':'Anthony Edwards and DiVincenzo are out for Minnesota, so more of the offense runs through him. His season log may include games before he joined Minnesota.','Jaden McDaniels':'Edwards and DiVincenzo are out.',
 'Donovan Clingan':'Milwaukee is on a back-to-back and without Turner and Kuzma. Portland is missing Morant, Sharpe and Robert Williams. Portland -11.5, so a big lead could cut minutes.',
 'Jalen Brunson':'Edwards is out for Minnesota. Knicks -1.5.','Mikal Bridges':'Edwards is out for Minnesota.','Brook Lopez':'Ingram and Beal are out for the Clippers. Spurs -15.5, blowout risk.',
 "De'Aaron Fox":'Harper and Harris are out for San Antonio. Spurs -15.5, a big lead could cut his fourth quarter.','Victor Wembanyama':'Spurs -15.5, a big lead could cut his minutes. Ace rule: no unders on Wemby, so this stays off every ticket.',
 'Myles Turner':'Ruled out (shoulder).','C.J. Stroud':'Texans -12.5 at home.','Jonathan Taylor':'Colts +12.5, so trailing could cut his carries late.','David Montgomery':'ESPN log shows only 5 games this season, the last on Oct 11. Woody Marks is out, so he should carry the load.',
 'Tank Dell':'Only 3 games this season.','Nico Collins':'','Dalton Schultz':'Brevin Jordan is out.','Tyler Warren':'Will Mallory is out, so fewer tight end snaps are shared.','Anthony Gould':'Questionable (toe).','Emari Demercado':'Woody Marks is out.'}
rows=[]
def add(p,st,k,under=False,moved=False,style='alt',adj=0,cap=None,label=None,orig=None):
  team=M[p]['team'];nfl=st in('recyds','rush','pass','rec','rr','td','rushatt');g=G[team]
  pr,(mu,hs,n,h5,m5)=prob(p,st,k)
  if under: pr=1-pr;hs=n-hs;h5=m5-h5
  pct=0.8*100*pr+0.2*65
  madj,mtxt,mtag=matchup(team,st,under) if st!='td' else (0,'','')
  pct+=madj+adj
  b2b=team in B2B and not nfl
  if b2b: pct-=(3 if st in('pts','3pm','pra') else 2)*(-1 if under else 1)
  hard=75 if nfl else 88
  if st=='td': hard=62
  if st=='pra': hard=80
  if n<8: pct=0.7*pct+0.3*60
  pct=min(pct,hard)
  if cap: pct=min(pct,cap)
  kk=KT.get((nrm(p),st),{}).get(k)
  kp=None if kk is None else (100-kk if under else kk)
  knote=''
  if kp is not None:
    if kp<=pct-15: knote=f" Kalshi has this at {kp}, far below us. Look twice."
    elif kp>=pct+15 and st!='td': knote=f" Kalshi has this at {kp}, well above us."
    else: knote=f" Kalshi: {kp}." 
  pct=max(5,round(pct))
  name=p
  txt=label or (f"{name} under {k} {WORD[st]}" if under else f"{name} {k}+ {WORD[st]}")
  if st=='td': txt=f"{name} anytime touchdown";note=f"Scored in {hs} of {n} games, {h5} of {m5} last 5. Touchdown picks have hit 37% all season, so this is capped at 62."
  else: note=f"{'Stayed under' if under else 'Hit'} {hs} of {n} this season, {h5} of {m5} last 5 (avg {mu:.1f} {UN[st]}). {mtxt}"
  c=CTX.get(p,'')
  if c and not (b2b and 'back-to-back' in c): note+=' '+c
  elif c: note+=' '+c
  if b2b and 'back-to-back' not in note: note+=' Second night of a back-to-back.'
  if nfl and st!='td' and pct==75: note+=' NFL props are capped at 75.'
  note+=knote
  if orig: note=f"Your line was {orig}. Kalshi offers this number. "+note
  elif moved: note='Moved line. '+note
  r=dict(p=txt,pct=pct,g=g['g'],t=g['t'],ty='prop',st=style,n=re.sub(r'\s+',' ',note).strip(),sp='NFL' if nfl else 'NBA')
  if kp is not None: r['k']=kp
  if mtag: r['mu']=mtag
  if moved or orig: r['moved']=True
  if b2b: r['b2b']=1
  rows.append(r)
# ---------- Nov 19 picks, in the order Ace sent them (SUB maps submitted number -> row)
SUB={}
def A(no,*a,**k):
  add(*a,**k);SUB[no]=len(rows)-1
def team(txt,pct,g,t,ty,sp,note,k=None,st='reg',fl=None,cap=None):
  if pct is not None and cap: pct=min(pct,cap)
  r=dict(p=txt,pct=None if pct is None else max(5,round(pct)),g=g,t=t,ty=ty,st=st,n=note,sp=sp)
  if k is not None: r['k']=round(k)
  if fl: r['fl']=fl
  rows.append(r)
def T(no,*a,**k):
  team(*a,**k);SUB[no]=len(rows)-1
def kmid(m):
  a=float(m['yes_ask_dollars'] or 0);b=float(m['yes_bid_dollars'] or 0);return 100*((a+b)/2 if a and b else a or b)
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
  if c and c[0][0]<x<c[-1][0]: return interp(c,x),True
  return None,False
A(1,'C.J. Stroud','rush',5)
A(2,'Dalton Schultz','recyds',25,orig='25 receiving yards')
A(3,'Xavier Hutchinson','recyds',30)
A(4,'Laquon Treadwell','recyds',20)
A(5,'Tyler Warren','recyds',30)
A(6,'Jonathan Taylor','rush',50)
A(7,'David Montgomery','td',1)
# CBB (v9 rules: spread SD 11, total SD 15, capped at 69; Kalshi shown only)
k=kgame('KXNCAAMBGAME','26NOV19','Charleston');T(8,'Charleston ML at Drake',100*phi(-1.5/11),'COFC@DRKE','4:30','ml','CBB',"College hoops. Graded from the betting line, capped under 70. Drake -1.5 at home, so Charleston is a slight underdog."+(f" Kalshi has it at {k:.0f}." if k else " No Kalshi price found."),k=k,cap=69)
k=kgame('KXNCAAMBGAME','26NOV19','St. Thomas');T(9,'St. Thomas ML v SE Missouri',100*phi(6.5/11),'SEMO@STMN','5:00','ml','CBB',"College hoops. Graded from the betting line, capped under 70. St. Thomas -6.5 at home."+(f" Kalshi has it at {k:.0f}." if k else " No Kalshi price found."),k=k,cap=69)
k=kgame('KXNCAAMBGAME','26NOV19','Wisconsin');T(10,'Wisconsin ML v Seton Hall',100*phi(5.5/11),'HALL v WIS','5:30','ml','CBB',"College hoops. Graded from the betting line, capped under 70. Wisconsin -5.5, neutral site."+(f" Kalshi has it at {k:.0f}." if k else " No Kalshi price found."),k=k,cap=69)
c=kcurve('KXNCAAMBSPREAD','26NOV19',r'St\. Thomas wins by over ([\d.]+)');k,ki=kat(c,6.5)
T(11,'St. Thomas -6.5 v SE Missouri',100*phi((6.5-6.5)/11),'SEMO@STMN','5:00','spread','CBB',"College hoops. Graded from the betting line, capped under 70. Book spread is also -6.5, so this is a coin flip."+(f" Kalshi has it at about {k:.0f}{' (estimated between two Kalshi lines)' if ki else ''}." if k is not None else " No Kalshi price found."),k=k,cap=69)
c=kcurve('KXNCAAMBSPREAD','26NOV19',r'Wisconsin wins by over ([\d.]+)');k,ki=kat(c,4.5)
T(12,'Wisconsin -4.5 v Seton Hall',100*phi((5.5-4.5)/11),'HALL v WIS','5:30','spread','CBB',"College hoops. Graded from the betting line, capped under 70. Book spread is -5.5, so -4.5 is a point better."+(f" Kalshi has it at about {k:.0f}{' (estimated between two Kalshi lines)' if ki else ''}." if k is not None else " No Kalshi price found."),k=k,cap=69)
c=kcurve('KXNCAAMBSPREAD','26NOV19',r'UC Santa Barbara wins by over ([\d.]+)');k,ki=kat(c,4.5)
T(13,'Pepperdine +4.5 v UC Santa Barbara',100*phi((4.5-1.5)/11),'UCSB@PEPP','6:00','spread','CBB',"College hoops. Graded from the betting line, capped under 70. UCSB -1.5 on the road, so +4.5 gives Pepperdine 3 extra points."+(f" Kalshi has it at about {100-k:.0f}{' (estimated between two Kalshi lines)' if ki else ''}." if k is not None else " No Kalshi price found."),k=None if k is None else 100-k,cap=69)
c=kcurve('KXNCAAMBTOTAL','26NOV19SACSTAN',r'Over ([\d.]+) points');k,ki=kat(c,149.5)
T(14,'Sacramento State v Stanford under 150 total points',100*phi((149.5-154.5)/15),'SAC@STAN','7:00','total','CBB',"College hoops. Graded from the betting line, capped under 70. Book total is 154.5, so under 150 needs it 5 points lower. Exactly 150 would push at most books."+(f" Kalshi has it at about {100-k:.0f}{' (estimated between two Kalshi lines)' if ki else ''}." if k is not None else " No Kalshi price found."),k=None if k is None else 100-k,cap=69)
A(15,'Nico Collins','recyds',60)
A(16,'David Montgomery','rr',60)
SUB[17]=SUB[6]
A(18,'Tyler Warren','rec',5)
SUB[19]=SUB[7]
A(20,'C.J. Stroud','rush',10,orig='over 9.5 rushing yards')
A(21,'Jonathan Taylor','rushatt',13,orig='over 12.5 rushing attempts')
# NBA spread: same spread-to-win curve as the NBA moneyline (SD 12)
c=kcurve('KXNBASPREAD','26NOV19',r'New York wins by over ([\d.]+)');k,ki=kat(c,2.5)
T(22,'Minnesota Timberwolves +2.5 v Knicks',100*phi((2.5-1.5)/12),'NY@MIN','5:00','spread','NBA',"Knicks -1.5, so +2.5 gives Minnesota one extra point. Anthony Edwards and DiVincenzo are out for Minnesota. Graded from the betting spread."+(f" Kalshi has it at about {100-k:.0f}{' (estimated between two Kalshi lines)' if ki else ''}." if k is not None else " No Kalshi price found."),k=None if k is None else 100-k)
k=kgame('KXNHLGAME','26NOV19','Washington');T(23,'Washington Capitals ML v Sabres',100*(142/242)-2,'BUF@WSH','4:00','ml','NHL',"Hockey. We have no hockey model, so this is graded from the betting line (-142, about 59% before the book's cut) and capped under 70."+(f" Kalshi has it at {k:.0f}." if k else " No Kalshi price found."),k=k,cap=69)
T(24,'Ducks v Avalanche over 6 total goals',48,'ANA@COL','6:00','total','NHL',"Hockey. We have no hockey model, so this is graded from the betting line and capped under 70. Book total is 6.5. Over 6 means 7 or more goals, the same as over 6.5 (exactly 6 would push at a book that offers 6). No Kalshi hockey total found.",cap=69)
A(25,'Tank Dell','td',1)
A(26,'Emari Demercado','rr',31,orig='Amari Demercado over 30 rushing + receiving yards')
SUB[27]=None  # Anthony Gould receiving yards: no line given
A(28,'LaMelo Ball','pts',20);A(29,'LaMelo Ball','reb',4);A(30,'LaMelo Ball','pts',15)
A(31,'Dalton Schultz','td',1);A(32,'Seth McGowan','td',1)
A(33,'Donovan Clingan','pts',10);A(34,'Donovan Clingan','pts',15)
A(35,'Jalen Brunson','ast',6)
A(36,'Brook Lopez','reb',6);A(37,'Brook Lopez','reb',4)
A(38,"De'Aaron Fox",'reb',4);A(39,'Jaden McDaniels','reb',4)
A(40,'Tank Dell','recyds',40)
k=kat(kcurve('KXNFLSPREAD','26NOV19',r'Houston wins by over ([\d.]+)'),9.5)[0]
T(41,'Houston Texans to win by over 9.5 points v Colts',None,'IND@HOU','5:15','spread','NFL',"No system grade. Our original process has no NFL team-line method. Book spread is Texans -12.5, so -9.5 is 3 points better."+(f" Kalshi has it at {k:.0f} (shown for reference, not used as a grade)." if k is not None else " No Kalshi price found."),k=k)
SUB[42]=SUB[7];SUB[43]=SUB[6]
k=kgame('KXNFLGAME','26NOV19','Houston');T(44,'Houston Texans ML v Colts',None,'IND@HOU','5:15','ml','NFL',"No system grade. Our original process has no NFL team-line method. Texans -12.5 at home."+(f" Kalshi has it at {k:.0f} (shown for reference, not used as a grade)." if k else " No Kalshi price found."),k=k)
A(45,'Myles Turner','ast',3,under=True);A(46,'Myles Turner','ast',4,under=True)
A(47,'Victor Wembanyama','pts',30,under=True);A(48,'Jalen Brunson','pts',30,under=True)
A(49,'Mikal Bridges','pra',16,orig='over 15 PRA')
A(50,'David Montgomery','recyds',10,orig='over 9.5 receiving yards')
# ---------- after-grading flags (no grade changes)
for no in (45,46):
  r=rows[SUB[no]];r['pct']=0;r['fl']='OUT';r['n']='Myles Turner was ruled out (shoulder) before grading. This leg is void.'
rows[SUB[47]]['fl']='RULE';rows[SUB[47]]['n']+=' Breaks Ace\'s no-unders-on-Wemby rule. Graded for the record only.'
for r in rows:
  if 'Kalshi offers this number. ' in r['n'] and r.get('k') is None: r['n']=r['n'].replace('Kalshi offers this number. ','')
json.dump({'rows':rows,'sub':SUB},open('thu/thu.json','w'))
for no in sorted(SUB):
  i=SUB[no];r=rows[i] if i is not None else None
  print(no, '-' if r is None else (r['pct'],'K'+str(r.get('k','-')),r.get('fl',''),r.get('mu',''),'|',r['p'],'|',r['n'][-150:]))
