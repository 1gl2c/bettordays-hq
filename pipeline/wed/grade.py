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
CTX={'Ivica Zubac':'Plays for Indiana now. Haliburton and Nembhard are out, Houston is missing Capela. Rockets -8.5.',
 'Jabari Smith Jr.':'Capela is out, so more frontcourt minutes. Rockets -8.5, so a big lead could cut his fourth quarter.',
 'Alperen Sengun':'Capela is out, so he carries the frontcourt. Amen Thompson is questionable. Rockets -8.5.',
 'Julius Randle':'Chicago allows the most points and assists in the league. Nets -1.5.','Nolan Traore':'Chicago allows the most points in the league. Nets -1.5.','Michael Porter Jr.':'Chicago allows the most assists in the league.',
 'Dean Wade':'Questionable with a hamstring. Check that he plays before you lock it.','LeBron James':'Plays for Philadelphia now. Jaylen Brown is out. Orlando is missing Banchero. 76ers -1.5.',
 'Joel Embiid':'Jaylen Brown is out, so more shots. Orlando is missing Banchero.','Tyrese Maxey':'Jaylen Brown is out, so the ball runs through him and LeBron.',
 'Jalen Suggs':'Only 5 games this season. Banchero is out, so more shots, but the sample is small.','Anthony Black':'Banchero is out, so he handles more.',
 'Aaron Wiggins':'Plays for Atlanta now. McCollum, Landale, Flemings and Newell are out, so more minutes.','Luguentz Dort':'Plays for Atlanta now. McCollum is out. Thunder -6.5.',
 'Shai Gilgeous-Alexander':'Jalen Williams, Holmgren and Wallace are out, so he carries the offense. Thunder -6.5.','Isaiah Hartenstein':'Holmgren is out, so he is the main big. Atlanta is missing Landale.',
 'Gui Santos':'Curry and Porzingis are out, Draymond and Horford are questionable, so more minutes.','Yaxel Lendeborg':'Rookie. Curry and Porzingis are out, Draymond and Horford are questionable.',
 'Cooper Flagg':'Lively is out for Dallas. Mavericks -4.5.','Kyrie Irving':'Golden State is missing Curry. Under on threes: he takes a lot of them.',
 'Giannis Antetokounmpo':'Plays for Miami now. Heat -12.5, so a big lead could cut his fourth quarter. Milwaukee allows the most rebounds in the league.',
 'Davion Mitchell':'Heat -12.5, so a blowout could cut his minutes.','Tyler Herro':'Plays for Milwaukee now. Rollins is out, so more shots. Bucks +12.5.',
 'Zach Edey':'Cleveland is missing Mobley, so the paint is open. Memphis is missing Jerome and Stewart.',
 'Ausar Thompson':'Second night of a back-to-back. Cade is questionable, Duren, Holland and Prince are out, so more ball in his hands.',
 'Yves Missi':'Only 4 games this season. Murphy, Mathurin and Watford are out for New Orleans.','Saddiq Bey':'Murphy, Mathurin and Watford are out, so more minutes.',
 'Paul George':'Plays for Boston now. Celtics -2.5 in Denver.','Jamal Murray':'Denver is home against Boston, a top defense (fewest points allowed).',
 'Luka Doncic':'Second night of a back-to-back. Reaves is out. Lakers -12.5 against a short-handed Utah team, so a big lead could cut his fourth quarter.',
 'Ace Bailey':'Second night of a back-to-back. Markkanen, Jaren Jackson Jr. and Nurkic are out. Jazz +12.5.','Darryn Peterson':'Rookie. Second night of a back-to-back. Markkanen, Jackson Jr. and Nurkic are out.',
 'Domantas Sabonis':'Raynaud and Simmons are out. Kings +6.5.','Zach LaVine':'Kings +6.5 at home.','Darius Acuff':'Rookie. Kings +6.5.','Miles Bridges':'Plays for Phoenix now. Mark Williams is out, so more rebounds. Suns -6.5.',
 'Scottie Barnes':'Ruled out tonight (injury management).'}
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
add('Ivica Zubac','pts',10);add('Ivica Zubac','reb',8);add('Ivica Zubac','pra',20)
add('Jabari Smith Jr.','pts',15)
add('Julius Randle','ast',4);add('Julius Randle','ast',5,orig='over 4 assists')
add('Dean Wade','reb',4)
add('Aaron Wiggins','reb',3)
add('Domantas Sabonis','pts',10)
add('Luka Doncic','pts',30);add('Luka Doncic','pts',25,moved=True);add('Luka Doncic','pra',50)
add('LeBron James','ast',6);add('LeBron James','ast',8);add('LeBron James','ast',10);add('LeBron James','reb',6);add('LeBron James','reb',4)
add('Joel Embiid','pts',20);add('Joel Embiid','pts',25);add('Joel Embiid','pts',30)
add('Jalen Suggs','pts',10)
add('Tyrese Maxey','pts',20);add('Tyrese Maxey','pts',25);add('Tyrese Maxey','pra',35);add('Tyrese Maxey','pra',30,moved=True)
add('Alperen Sengun','pra',30);add('Alperen Sengun','pra',25,moved=True)
add('Giannis Antetokounmpo','pra',40);add('Giannis Antetokounmpo','pts',30);add('Giannis Antetokounmpo','pts',25,moved=True)
add('Zach Edey','reb',6)
add('Nolan Traore','pts',10)
add('Scottie Barnes','pra',30)
add('Shai Gilgeous-Alexander','pts',25);add('Shai Gilgeous-Alexander','pts',30)
add('Ausar Thompson','reb',6);add('Ausar Thompson','reb',8);add('Ausar Thompson','ast',4);add('Ausar Thompson','ast',6)
add('Paul George','pra',25);add('Paul George','pts',15);add('Paul George','pts',20);add('Paul George','reb',4)
add('Gui Santos','reb',4);add('Gui Santos','reb',2);add('Gui Santos','ast',2)
add('Miles Bridges','pra',20);add('Miles Bridges','pra',15,moved=True)
add('Ace Bailey','pts',10);add('Ace Bailey','reb',4)
add('Isaiah Hartenstein','reb',10);add('Isaiah Hartenstein','reb',8);add('Isaiah Hartenstein','ast',2);add('Isaiah Hartenstein','ast',4)
add('Yaxel Lendeborg','pts',20)
add('Zach LaVine','pra',20);add('Zach LaVine','pra',15,moved=True)
add('Darryn Peterson','pts',15)
add('Davion Mitchell','pts',10);add('Davion Mitchell','ast',8)
add('Anthony Black','pra',25);add('Anthony Black','pra',20,moved=True)
add('Jamal Murray','pra',30);add('Jamal Murray','pra',25,moved=True)
add('Tyler Herro','pts',15);add('Tyler Herro','pts',20);add('Tyler Herro','pts',25)
add('Yves Missi','reb',9,orig='over 8 rebounds');add('Yves Missi','reb',7,orig='over 6 rebounds');add('Yves Missi','reb',6,moved=True)
add('Cooper Flagg','ast',7,orig='over 6 assists');add('Cooper Flagg','ast',5,orig='over 4 assists');add('Cooper Flagg','ast',4,moved=True)
add('Darius Acuff','3pm',3,orig='over 2.5 threes');add('Darius Acuff','3pm',2,orig='over 1.5 threes');add('Darius Acuff','3pm',1,orig='over 0.5 threes')
add('Michael Porter Jr.','ast',2)
add('Kyrie Irving','3pm',4,under=True)
add('Luguentz Dort','3pm',2,orig='over 1.5 threes');add('Luguentz Dort','3pm',1,orig='over 0.5 threes')
add('Saddiq Bey','reb',4);add('Saddiq Bey','ast',2)
for r in rows:
  if r['p'].startswith('Scottie Barnes'): r['fl']='OUT';r['pct']=0;r['n']='Ruled out tonight (injury management). This leg is void.'
  if r['p'].startswith('Dean Wade'): r['fl']='Q'
def team(txt,pct,g,t,ty,sp,note,k=None,cap=None,fl=None):
  if cap: pct=min(pct,cap)
  r=dict(p=txt,pct=max(5,round(pct)),g=g,t=t,ty=ty,st='reg',n=note,sp=sp)
  if k is not None: r['k']=round(k)
  if fl: r['fl']=fl
  rows.append(r)
def kinterp(ser,ev,team_or_over,x):
  # Kalshi lists set lines; estimate a line between two of them by straight-line interpolation
  pts=[]
  for m in K[ser]:
    if ev not in m['event_ticker']: continue
    mm=re.search(r'(?:'+team_or_over+r') (?:wins by over|points scored|)\s*([\d.]+)',m['title']) if team_or_over!='Over' else re.search(r'Over ([\d.]+) points',m['title'])
    if mm and (team_or_over=='Over' or m['title'].startswith(team_or_over)): pts.append((float(mm.group(1)),mid(m)))
  pts.sort();lo=[p for p in pts if p[0]<=x];hi=[p for p in pts if p[0]>=x]
  if not lo or not hi: return None
  a,b=lo[-1],hi[0]
  return a[1] if a[0]==b[0] else a[1]+(b[1]-a[1])*(x-a[0])/(b[0]-a[0])
def km(ser,ev,pred):
  for m in K[ser]:
    if ev in m['event_ticker'] and pred(m): return mid(m)
# NBA moneylines: our number comes from the betting spread (12-point spread spread-to-win curve). Kalshi is shown, not used.
for nm,ab,ev,kn,ex in [('Los Angeles Lakers ML v Jazz','LAL','26NOV18UTALAL','Los Angeles L','Reaves is out. Utah is missing Markkanen, Jaren Jackson Jr. and Nurkic. Both teams are on the second night of a back-to-back.'),
  ('Philadelphia 76ers ML v Magic','PHI','26NOV18PHIORL','Philadelphia','Jaylen Brown is out for Philly, Banchero is out for Orlando. Close to a coin flip.'),
  ('Cleveland Cavaliers ML v Grizzlies','CLE','26NOV18MEMCLE','Cleveland','Mobley, Tyson and Merrill are out for Cleveland. Memphis is missing Jerome and Stewart.'),
  ('Brooklyn Nets ML v Bulls','BKN','26NOV18CHIBKN','Brooklyn','Chicago allows the most points in the league. Close to a coin flip.'),
  ('Boston Celtics ML v Nuggets','BOS','26NOV18BOSDEN','Boston','Road favorite in Denver. Boston allows the fewest points in the league.'),
  ('Dallas Mavericks ML v Warriors','DAL','26NOV18GSWDAL','Dallas','Curry and Porzingis are out, Draymond and Horford questionable. Lively is out for Dallas.')]:
  g=G[ab];pct=100*phi(-g[2]/12);kp=km('KXNBAGAME',ev,lambda m:m['yes_sub_title']==kn)
  team(nm,pct,g[0],g[1],'ml','NBA',f"Favored by {-g[2]} at the books. {ex} Kalshi has it at {kp}.",k=kp)
# NHL: no hockey model; graded from the betting line, capped under 70
for nm,ev,kn,g,t,ex,pct in [('Boston Bruins ML v Red Wings','26NOV18BOSDET','Boston','BOS@DET','4:30','Detroit is -110 at home, so this is close to a coin flip.',48),('Colorado Avalanche ML v Mammoth','26NOV18COLUTA','Colorado','COL@UTAH','7:00','Utah is -110 at home, so this is close to a coin flip.',48)]:
  kp=km('KXNHLGAME',ev,lambda m:m['yes_sub_title']==kn)
  team(nm,pct,g,t,'ml','NHL',f"Hockey. We have no hockey model, so this is graded from the betting line and capped under 70. {ex} Kalshi has it at {kp}.",k=kp,cap=69)
# College hoops: no team model; graded from the betting spread/total (11-pt spread SD, 15-pt total SD), capped under 70
def cbb(nm,g,t,ty,pct,ex,ev,pred,ser='KXNCAAMBGAME',fl=None):
  kp=km(ser,ev,pred) if ev else None
  team(nm,pct,g,t,ty,'CBB',f"College hoops. Graded from the betting line, capped under 70. {ex}"+(f" Kalshi has it at {kp}." if kp is not None else " No Kalshi price found."),k=kp,cap=69,fl=fl)
cbb('Eastern Michigan ML v Detroit Mercy','DETM@EMU','3:30','ml',100*phi(10.5/11),'Eastern Michigan -10.5 at home.','26NOV18DETEMU',lambda m:'Eastern' in m['yes_sub_title'])
def cbbk(nm,g,t,ty,pct,ex,kp):
  team(nm,pct,g,t,ty,'CBB',f"College hoops. Graded from the betting line, capped under 70. {ex}"+(f" Kalshi has it at about {round(kp)} (estimated between two Kalshi lines)." if kp is not None else " No Kalshi price found."),k=kp,cap=69)
cbbk('Eastern Michigan -10 v Detroit Mercy','DETM@EMU','3:30','spread',100*phi(0.5/11),'Book spread is -10.5, so -10 is a half point better. Basically a coin flip.',kinterp('KXNCAAMBSPREAD','26NOV18DETEMU','Eastern Michigan',9.5))
cbbk('James Madison v Towson over 130 total points','JMU@TOW','4:00','total',100*phi((138.5-130.5)/15),'Book total is 138.5.',kinterp('KXNCAAMBTOTAL','26NOV18JMUTOWS','Over',130.5))
cbbk('James Madison v Towson over 139.5 total points','JMU@TOW','4:00','total',100*phi((138.5-139.5)/15),'Book total is 138.5, so this is just over the number.',kinterp('KXNCAAMBTOTAL','26NOV18JMUTOWS','Over',139.5))
cbb('Wichita State ML v Loyola Chicago','WICH@LUC','5:00','ml',100*phi(1.5/11),'Wichita State -1.5 on the road. Close to a coin flip.','26NOV18WICHLCHI',lambda m:'Wichita' in m['yes_sub_title'])
cbb('Kansas ML v West Virginia','KU v WVU','4:30','ml',100*phi(7.5/11),'Kansas -7.5, neutral site.','26NOV18KUWVU',lambda m:m['yes_sub_title']=='Kansas')
_a=kinterp('KXNCAAMBSPREAD','26NOV18CONNARIZ','Arizona',7.5)
cbbk('UConn +8 v Arizona','CONN@ARIZ','6:00','spread',100*phi((8-3.5)/11),'Arizona -3.5 at home, so +8 gives UConn 4.5 extra points.',None if _a is None else 100-_a)
cbb('Florida ML v Houston','HOU v FLA','1:48','ml',50,'This game tipped at 1:48 PM PT, before the list came in. Florida led 40-37 at halftime. Not graded and not counted in the record.',None,None,fl='LIVE')
cbb('Florida v Houston over 140 total points','HOU v FLA','1:48','total',50,'This game tipped at 1:48 PM PT, before the list came in. 77 points at halftime. Not graded and not counted in the record.',None,None,fl='LIVE')
json.dump(rows,open('wed/wed.json','w'))
print(len(rows))
for r in sorted(rows,key=lambda r:-r['pct']): print(r['pct'],'K'+str(r.get('k','-')),r.get('mu',''),r.get('fl',''),'|',r['p'],'|',r['n'][-140:])
