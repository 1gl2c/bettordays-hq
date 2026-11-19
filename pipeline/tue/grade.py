import json,math,re,unicodedata,statistics as S
from collections import defaultdict
L=json.load(open('tue/logs.json'));K=json.load(open('tue/kalshi.json'));OPP=json.load(open('mon/nba_opp.json'))
def phi(z): return 0.5*(1+math.erf(z/math.sqrt(2)))
def nrm(s): return unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode().lower().replace('.','').replace("'",'').strip()
SER={'pts':'KXNBAPTS','reb':'KXNBAREB','ast':'KXNBAAST','3pm':'KXNBA3PT','pra':'KXNBAPRA'}
def mid(m):
  a=float(m['yes_ask_dollars'] or 0);b=float(m['yes_bid_dollars'] or 0);return round(100*((a+b)/2 if a and b else a or b))
KT=defaultdict(dict)
for st,s in SER.items():
  for m in K[s]:
    if '26NOV17' not in m['event_ticker']: continue
    mm=re.match(r'(.+?): (\d+)\+',m['title'])
    if mm: KT[(nrm(mm.group(1)),st)][int(mm.group(2))]=mid(m)
G={'NY':('NY@TOR','4:30',-2.5),'TOR':('NY@TOR','4:30',2.5),'POR':('POR@MIN','5:00',2.5),'MIN':('POR@MIN','5:00',-2.5),'DET':('DET@SA','5:00',9.5),'SA':('DET@SA','5:00',-9.5),
   'UTAH':('UTAH@LAC','7:30',6.5),'LAC':('UTAH@LAC','7:30',-6.5),'CHA':('CHA@LAL','8:00',7.5),'LAL':('CHA@LAL','8:00',-7.5),
   'WMU':('EMU@WMU','3:00',0),'KENT':('M-OH@KENT','4:00',9.5),'M-OH':('M-OH@KENT','4:00',-9.5),'BALL':('BALL@OHIO','4:00',10),'OHIO':('BALL@OHIO','4:00',-10)}
def opp(t): a,b=G[t][0].split('@'); return b if t==a else a
B2B={'POR','MIN'}
FULL={'NY':'New York','TOR':'Toronto','POR':'Portland','MIN':'Minnesota','DET':'Detroit','SA':'San Antonio','UTAH':'Utah','LAC':'the Clippers','CHA':'Charlotte','LAL':'the Lakers'}
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
  txt=f"Matchup: {FULL[o]} allows {val} {UN[k]} a game, {ordn(31-rk)} most in the league"
  if under: soft,tough=tough,soft
  return (3 if soft else -5 if tough else 0),txt+(' (good spot).' if soft else ' (tough spot).' if tough else '.'),('good' if soft else 'bad' if tough else '')
CTX={'Luka Doncic':'Austin Reaves is out. Lakers -7.5 against a 4-9 Charlotte team, so a big lead could cut his fourth quarter.','Quentin Grimes':'Reaves is out, so he starts.','Sandro Mamukelashvili':'Kessler is out, so he gets more minutes.','Ziaire Williams':'Reaves is out.',
 'Grayson Allen':'Knueppel and Schroder are out, so more shots come his way. Hornets +7.5.','LaMelo Ball':'Plays for Minnesota now. Edwards and DiVincenzo are out.','Ayo Dosunmu':'Edwards and DiVincenzo are out, so he handles the ball more. That hurts an assists under.',
 'Rudy Gobert':'Second night of a back-to-back against the same Portland team.','Donovan Clingan':'Second night of a back-to-back against the same Minnesota team.','Toumani Camara':'Morant and Sharpe are out, so he takes more threes.',
 'Darius Garland':'Ingram and Beal are out, so the offense runs through him. Utah is 1-13.','Brook Lopez':'Ingram and Beal are out.','Keyonte George':'Markkanen, Jaren Jackson Jr. and Nurkic are out, so he carries the offense. Jazz +6.5.',
 'Darryn Peterson':'Rookie. Markkanen, Jaren Jackson Jr. and Nurkic are out.','Scottie Barnes':'Kawhi Leonard is out.','Karl-Anthony Towns':'Knicks -2.5 in Toronto.','Mikal Bridges':'Scoring has dropped this year (avg 6.8 pts).',
 'Victor Wembanyama':'Spurs -9.5, so a big lead could cut his minutes. Duren is out for Detroit.','Keldon Johnson':'Tobias Harris is out.','Ausar Thompson':'Duren, Holland and Prince are out for Detroit.'}
rows=[]
def add(p,st,k,under=False,moved=False,orig=None,style=None):
  team=L[p]['team'];cf=st in('rush','recyds');g=G[team]
  pr,(mu,hs,n,h5,m5)=prob(p,st,k)
  if under: pr=1-pr;hs=n-hs;h5=m5-h5
  pct=0.8*100*pr+0.2*65
  madj,mtxt,mtag=(0,'','') if cf else matchup(team,st,under)
  pct+=madj
  b2b=team in B2B
  if b2b: pct-=(3 if st in('pts','3pm','pra') else 2)*(-1 if under else 1)
  hard=70 if cf else (80 if st=='pra' else 88)
  if n<8: pct=0.7*pct+0.3*60
  pct=max(5,round(min(pct,hard)))
  kk=None if cf else KT.get((nrm(L[p]['disp']),st),{}).get(k)
  kp=None if kk is None else (100-kk if under else kk)
  txt=f"{p} under {k} {WORD[st]}" if under else f"{p} {k}+ {WORD[st]}"
  note=f"{'Stayed under' if under else 'Hit'} {hs} of {n} this season, {h5} of {m5} last 5 (avg {mu:.1f} {UN[st]}). {mtxt} {CTX.get(p,'')}"
  if b2b and 'back-to-back' not in note: note+=' Second night of a back-to-back.'
  if cf: note+=' College football. Kalshi does not offer this market, so it is capped at 70.'
  if kp is not None:
    if kp<=pct-15: note+=f" Kalshi has this at {kp}, far below us. Look twice."
    elif kp>=pct+15: note+=f" Kalshi has this at {kp}, well above us."
  if orig: note=f"Your line was {orig}. "+note
  elif moved: note='Moved line. '+note
  r=dict(p=txt,pct=pct,g=g[0],t=g[1],ty='prop',st=style or ('alt' if moved else 'reg'),n=re.sub(r'\s+',' ',note).strip(),sp='CFB' if cf else 'NBA')
  if kp is not None: r['k']=kp
  if mtag: r['mu']=mtag
  if moved or orig: r['moved']=True
  if b2b: r['b2b']=1
  if team=='WMU': r['fl']='LIVE'
  rows.append(r)
# NBA from the list (over N with no + becomes N+1)
add('Quentin Grimes','pts',10);add('Quentin Grimes','pts',5,moved=True)
add('Grayson Allen','pts',10);add('Grayson Allen','ast',4,orig='over 3 assists');add('Grayson Allen','ast',5,orig='over 4 assists');add('Grayson Allen','ast',3,moved=True)
add('Victor Wembanyama','pts',25);add('Victor Wembanyama','pts',20,moved=True)
add('Darius Garland','pts',20);add('Darius Garland','pts',15,moved=True);add('Darius Garland','ast',8,under=True)
add('Sandro Mamukelashvili','3pm',3);add('Sandro Mamukelashvili','3pm',2);add('Sandro Mamukelashvili','3pm',1)
add('Karl-Anthony Towns','pts',20);add('Karl-Anthony Towns','pts',15)
add('Donovan Clingan','reb',10);add('Donovan Clingan','reb',8,moved=True);add('Donovan Clingan','pts',10);add('Donovan Clingan','pts',5,moved=True)
add('Keyonte George','pts',20);add('Keyonte George','pts',15,moved=True)
add('Scottie Barnes','ast',6,orig='over 5 assists');add('Scottie Barnes','ast',4,moved=True)
add('Brook Lopez','reb',6,orig='over 6 rebounds');add('Brook Lopez','reb',4,moved=True)
add('Mikal Bridges','reb',4,orig='over 3 rebounds');add('Mikal Bridges','reb',3,orig='over 2 rebounds');add('Mikal Bridges','pra',15,orig='over 15 PRA')
add('Ausar Thompson','pts',10);add('Ausar Thompson','pts',8,moved=True)
add('Rudy Gobert','reb',8);add('Rudy Gobert','reb',10)
add('Ziaire Williams','pts',10);add('Ziaire Williams','pts',9,orig='over 8.5 points');add('Ziaire Williams','pts',8,moved=True)
add('Darryn Peterson','pts',20);add('Darryn Peterson','pts',15,moved=True)
add('Luka Doncic','ast',9,orig='over 8 assists');add('Luka Doncic','ast',8,moved=True);add('Luka Doncic','ast',6,moved=True);add('Luka Doncic','pts',30);add('Luka Doncic','pts',25,moved=True);add('Luka Doncic','pts',35,moved=True)
add('Keldon Johnson','reb',5,orig='over 4 rebounds');add('Keldon Johnson','reb',6,orig='over 5 rebounds');add('Keldon Johnson','reb',4,moved=True)
add('LaMelo Ball','pts',25,under=True)
add('Ayo Dosunmu','ast',4,under=True)
add('Toumani Camara','3pm',3,under=True);add('Toumani Camara','3pm',4,under=True)
# CFB
add('Jalen Buckley','rush',96,orig='over 95.5 rushing yards');add('Jalen Buckley','rush',60,moved=True)
add('Wayne Harris','recyds',68,orig='over 67.5 receiving yards');add('Wayne Harris','recyds',30,moved=True)
add('Donovan Hamilton','recyds',56,orig='over 55.5 receiving yards');add('Donovan Hamilton','recyds',35,moved=True)
add("D'Shawntae Jones",'rush',66,orig='over 65.5 rushing yards');add("D'Shawntae Jones",'rush',25,moved=True)
add('Riley Neer','recyds',60,orig='over 59.5 receiving yards');add('Riley Neer','recyds',40,moved=True)
# team lines
def team(txt,pct,g,t,ty,sp,note,k=None,cap=None,fl=None):
  if cap: pct=min(pct,cap)
  r=dict(p=txt,pct=max(5,round(pct)),g=g,t=t,ty=ty,st='reg',n=note,sp=sp)
  if k is not None: r['k']=round(k)
  if fl: r['fl']=fl
  rows.append(r)
def kml(ser,ev,nm):
  for m in K[ser]:
    if ev in m['event_ticker'] and m['title'].lower().startswith(nm.lower()): return mid(m)
def kspread(ev,nm,x):
  for m in K['KXNBASPREAD']:
    if ev in m['event_ticker']:
      mm=re.match(re.escape(nm)+r' wins by over ([\d.]+)',m['title'])
      if mm and abs(float(mm.group(1))-x)<0.01: return mid(m)
NBAML=[('NY','New York Knicks ML v Raptors','New York','26NOV17NYKTOR','Toronto is without Kawhi Leonard.'),('MIN','Minnesota Timberwolves ML v Trail Blazers','Minnesota','26NOV17PORMIN','Edwards and DiVincenzo are out. Portland is missing Morant and Sharpe. Both teams on a back-to-back, same matchup as last night.'),
 ('LAL','Los Angeles Lakers ML v Hornets','Los Angeles L','26NOV17CHALAL','Lakers are 12-2. Reaves is out. Charlotte is missing Knueppel and Schroder.'),('LAC','Los Angeles Clippers ML v Jazz','Los Angeles C','26NOV17UTALAC','Utah is 1-13 and missing Markkanen, Jaren Jackson Jr. and Nurkic. Clippers are 4-12... missing Ingram and Beal.')]
for ab,nm,kn,ev,ex in NBAML:
  g=G[ab];kp=kml('KXNBAGAME',ev,kn);sp=100*phi(-g[2]/12);pct=(sp+kp)/2 if kp else sp
  ex=ex.replace('Clippers are 4-12... missing','Clippers are 4-8 and missing')
  team(nm,pct,g[0],g[1],'ml','NBA',f"Favored by {-g[2]}. Kalshi has it at {kp}. {ex}",k=kp)
for ab,nm,kn,ev,sp_,ex in [('LAL','Los Angeles Lakers -6.5 v Hornets','Los Angeles L','26NOV17CHALAL',6.5,'Spread is 7.5 at the books.'),('LAC','Los Angeles Clippers -5.5 v Jazz','Los Angeles C','26NOV17UTALAC',5.5,'Spread is 6.5 at the books.')]:
  g=G[ab];kp=kspread(ev,kn,sp_);model=100*phi((-g[2]-sp_)/12);pct=(model+kp)/2 if kp else model
  team(nm,pct,g[0],g[1],'spread','NBA',f"{ex} Kalshi has this at {kp}. NBA spreads have been our weakest category, so this is capped under 70.",k=kp,cap=69)
for nm,ev,kn,t,g,ex in [('New York Islanders ML v Blue Jackets','26NOV17CBJNYI','New York I','4:00','CBJ@NYI','Islanders -135 at home. Columbus is 7-11.'),('Toronto Maple Leafs ML v Blackhawks','26NOV17TORCHI','Toronto','4:30','TOR@CHI','Leafs -142. Chicago is 5-13-2, but Toronto is only 8-12-2.')]:
  kp=kml('KXNHLGAME',ev,kn)
  team(nm,kp or 55,g,t,'ml','NHL',f"Hockey. Graded at Kalshi's price ({kp}). {ex} We have no hockey record, so it is capped under 70.",k=kp,cap=69)
for nm,ev,kn,t,g,ex in [('Mississippi State ML v UCF','26NOV17MSSTUCF','Mississippi','4:00','MSST@UCF','UCF -1.5 at home. Both teams have one loss or none.'),('Villanova ML v Pittsburgh','26NOV17VILLPITT','Villanova','4:00','VILL@PITT','Villanova -1.5 on the road.'),
 ('Arkansas ML v Indiana','26NOV17ARKIND','Arkansas','4:30','ARK v IU','Indiana -1.5, neutral site.'),('Michigan State ML v Tennessee','26NOV17MSUTENN','Michigan','6:00','MSU@TENN','Michigan State -2.5 on the road.')]:
  kp=kml('KXNCAAMBGAME',ev,kn)
  team(nm,kp or 50,g,t,'ml','CBB',f"College basketball. Graded at Kalshi's price ({kp}) because we have no team data of our own. {ex} Close to a coin flip, capped under 70.",k=kp,cap=69)
json.dump(rows,open('tue/tue.json','w'))
print(len(rows))
for r in sorted(rows,key=lambda r:-r['pct']): print(r['pct'],'K'+str(r.get('k','-')),r.get('mu',''),'|',r['p'],'|',r['g'],r['t'],r.get('fl',''))
