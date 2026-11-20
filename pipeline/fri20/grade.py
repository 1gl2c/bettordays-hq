"""Nov 20 grading (Friday). Same system as Nov 19 (thu/grade.py): logs blend, matchup, Kalshi shown, caps.
Changes for tonight:
- No line given -> we use the Kalshi rung closest to 72 (named in the note).
- A submitted line whose Kalshi price is under 65 also gets a safer rung (Kalshi closest to 80) as its own candidate, marked as a moved line.
- College football props have no Kalshi market, so they are capped at 69 like other college lines.
- Games that tipped before grading are left off (South Dakota State, SFA v Indiana State, GW v UAB)."""
import json,math,re,unicodedata,statistics as S
from collections import defaultdict
D='fri20/'
L=json.load(open(D+'logs.json'));K=json.load(open(D+'kalshi.json'));OPP=json.load(open(D+'nba_opp.json'))
EV='26NOV20'
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
GM={'CHA@ATL':('4:00','ATL',-7.5,218.5),'ORL@BKN':('4:30','ORL',-6.5,223.5),'IND@CLE':('4:30','CLE',-5.5,234.5),'TOR@DET':('4:30','DET',-6.5,215.5),
    'WSH@CHI':('5:00','CHI',-2.5,238.5),'NO@OKC':('5:00','OKC',-11.5,227.5),'PHX@UTAH':('6:30','PHX',-4.5,225.5),'HOU@DEN':('7:00','DEN',-1.5,226.5),'SAC@LAL':('7:00','LAL',-14.5,228.5)}
G={}
for g,(t,fav,sp,ou) in GM.items():
  a,b=g.split('@')
  for tm in (a,b): G[tm]=dict(g=g,t=t,sp=(sp if tm==fav else -sp),ou=ou)
def TK(g): return g.replace('@','').replace('UTAH','UTA').replace('NO','NOP').replace('WSH','WAS')
def opp(t): a,b=G[t]['g'].split('@'); return b if t==a else a
FULL={'CHA':'Charlotte','ATL':'Atlanta','ORL':'Orlando','BKN':'Brooklyn','IND':'Indiana','CLE':'Cleveland','TOR':'Toronto','DET':'Detroit','WSH':'Washington','CHI':'Chicago','NO':'New Orleans','OKC':'Oklahoma City','PHX':'Phoenix','UTAH':'Utah','HOU':'Houston','DEN':'Denver','SAC':'Sacramento','LAL':'the Lakers'}
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
 'Saddiq Bey':'New Orleans is without Dejounte Murray, Mathurin and Watford, and Trey Murphy is listed questionable, so more shots go his way. Thunder -11.5, blowout risk.',
 'Jeremiah Fears':'Dejounte Murray and Mathurin are out, so he runs more of the offense. Thunder -11.5, blowout risk.',
 'Nickeil Alexander-Walker':'CJ McCollum is out at least four weeks, so Atlanta needs his scoring.',
 'Dyson Daniels':'McCollum is out for Atlanta.','Jalen Johnson':'McCollum is out for Atlanta.',
 'Fred VanVleet':'Capela is out and Sengun is questionable (eye) for Houston. Nuggets -1.5.',
 'Kevin Durant':'Sengun is questionable (eye) and Capela is out, so Houston may lean on him more.',
 'Alperen Sengun':'Questionable with an eye issue. If he sits, this leg is void. Capela is out, so his rebounding share would be big if he plays.',
 'Donovan Mitchell':'Evan Mobley and Jaylon Tyson are out, so Cleveland is thin up front and on the wing.','Tyrese Proctor':'Mobley and Tyson are out, so his minutes should hold.',
 'Moussa Diabate':'Charlotte is without Knueppel, Schroder, Grayson Allen and Grant Williams.','Sion James':'Schroder, Knueppel and Allen are out, so he handles the ball more.',
 'Miles Bridges':'Now with Phoenix. Mark Williams is out, so the Suns are short a big.',
 'Trae Young':'Now with Washington.','Anthony Davis':'Now with Washington.','AJ Dybantsa':'Rookie with Washington.',
 'Nikola Jokic':'Houston is without Capela, and Sengun is questionable.','DeMar DeRozan':'Now with Denver.','Jamal Murray':'Houston plays big, and Capela is out.',
 'Darryn Peterson':'Utah is without Markkanen, Jaren Jackson Jr. and Nurkic, so the young guards carry the scoring.','Keyonte George':'Utah is without Markkanen, Jaren Jackson Jr. and Nurkic.',
 'Devin Booker':'Utah is missing three starters.','Dillon Brooks':'Utah is missing three starters.',
 'Matas Buzelis':'Wizards at Bulls, highest total on the slate (238.5).','Josh Giddey':'Highest total on the slate (238.5).','Norman Powell':'Now with Chicago.',
 'Scottie Barnes':'Kawhi Leonard, RJ Barrett and Murray-Boyles are out for Toronto, so he carries more.',
 'Ausar Thompson':'Jalen Duren is out, so more rebounds are there for him.','Cade Cunningham':'Listed with a knee issue but expected to play. Duren is out.',
 'Shai Gilgeous-Alexander':'Jalen Williams and Chet Holmgren are out. Thunder -11.5, so a big lead could cut his fourth quarter.',
 'Isaiah Hartenstein':'Holmgren is out, so he is the main big. Thunder -11.5, blowout risk.',
 'Luka Doncic':'Austin Reaves is out, so even more of the offense runs through him. Lakers -14.5, so a big lead could cut his fourth quarter. Ace rule: no unders on Luka.',
 'Michael Porter Jr.':'Now with Brooklyn. Nets +6.5 at home.','Franz Wagner':'Paolo Banchero is out four to six weeks, so Franz runs the offense.',
 'Jalen Suggs':'Banchero is out. Only 6 games logged this season.','Tristan da Silva':'Banchero is out, so his minutes are up.'}
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
  SUB[no]=addp(p,st,x,pre=f"No line was given, so we used {x}+, where Kalshi is near 72. ",moved=True)
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
CFBG={'Dylan Raiola':('ORE@MSU','5:00','Oregon -17.5 at Michigan State. A big lead could mean fewer second-half throws. He had two games under 60 yards this season.'),
      'Aidan Flora':('ISU@UCF','3:00','Iowa State -1.5 at UCF. Over 180 rushing yards in 4 of his last 5 full workloads.'),
      'Josh Derry':('ISU@UCF','3:00','137 and 143 receiving yards his last two games.'),
      'Nate Sheppard':('CLEM@DUKE','4:30','Duke -11.5 at home, so a lead should keep him running late.'),
      'Adjatay Dabbs':('BGSU@TOL','4:30','Toledo -16.5 at home. Toledo leads by a lot could mean fewer late targets.')}
def CF(no,p,st,k):
  pr,(mu,hs,n,h5,m5)=prob(p,st,k);pct=min(0.8*100*pr+0.2*65,69)
  g,t,c=CFBG[p];disp=L[p]['disp']
  SUB[no]=team(f"{disp} {k}+ {WORD[st]}",pct,g,t,'prop','CFB',f"College football. Hit {hs} of {n} this season, {h5} of {m5} last 5 (avg {mu:.1f} {UN[st]}). {c} No Kalshi market for college player props, so this is capped at 69.",st='alt')
# ================= picks in the order Ace sent them
A(1,'Saddiq Bey','3pm',2);A(2,'Saddiq Bey','3pm',1);A(3,'Nickeil Alexander-Walker','pts',20);A(4,'Fred VanVleet','ast',4);A(5,'Donovan Mitchell','reb',4)
A(6,'Moussa Diabate','reb',8);A(7,'Trae Young','pts',10);A(8,'Trae Young','pts',15)
CF(9,'Dylan Raiola','pass',250);CF(10,'Dylan Raiola','pass',260);CF(11,'Aidan Flora','rush',130);CF(12,'Josh Derry','recyds',85);CF(13,'Nate Sheppard','rush',115)
CF(14,'Adjatay Dabbs','recyds',65);CF(15,'Adjatay Dabbs','recyds',60)
N(16,'Nikola Jokic','pts');N(17,'Kevin Durant','pts');N(18,'DeMar DeRozan','pts');N(19,'Alperen Sengun','reb');N(20,'Darryn Peterson','pts');N(21,'Darryn Peterson','3pm')
N(22,'Keyonte George','pts');N(23,'Keyonte George','3pm');N(24,'Devin Booker','pts');N(25,'Dillon Brooks','pts');N(26,'Miles Bridges','reb');N(27,'Anthony Davis','pts')
N(28,'Trae Young','ast');N(29,'Matas Buzelis','pts');N(30,'AJ Dybantsa','pts');N(31,'Scottie Barnes','pts');N(32,'Scottie Barnes','reb');N(33,'Ausar Thompson','pts');N(34,'Ausar Thompson','reb')
SUB[35]=None  # South Dakota State: tipped at 1 PM PT, before grading
A(36,'Fred VanVleet','pts',10);SUB[37]=SUB[4]
A(38,'Norman Powell','reb',2);A(39,'Norman Powell','ast',2);A(40,'Jalen Suggs','pra',20);A(41,'Jeremiah Fears','3pm',1);A(42,'Jeremiah Fears','3pm',2)
A(43,'Nikola Jokic','pts',20);A(44,'Nikola Jokic','pts',25);A(45,'Cade Cunningham','pra',35);A(46,'Scottie Barnes','pra',35);A(47,'Jalen Johnson','pra',35)
A(48,'Shai Gilgeous-Alexander','pra',40);A(49,'Luka Doncic','pra',50);A(50,'Nikola Jokic','pra',40);A(51,'AJ Dybantsa','pra',25)
# ---- college hoops (spread SD 11, total SD 15, capped at 69)
def cbbml(no,txt,g,t,ev,sub,sp,where):
  k=kgame('KXNCAAMBGAME',ev,sub);SUB[no]=team(txt,100*phi(sp/11),g,t,'ml','CBB',f"College hoops. Graded from the betting line, capped under 70. {where}"+kn(k),k=k)
cbbml(52,'Utah ML v Dayton','DAY v UTAH','2:30','26NOV20DAYUTAH','Utah',1.5,'Utah -1.5, neutral site. Tips at 2:30 PM PT, before the board goes up.')
cbbml(53,'Wisconsin ML v Murray State','WIS v MUR','4:00','26NOV20MURRWIS','Wisconsin',3.5,'Wisconsin -3.5, neutral site.')
cbbml(54,'Mississippi State ML v Tulsa','TLSA v MSST','4:30','26NOV20TLSAMSST','Mississippi State',7.5,'Mississippi State -7.5, neutral site.')
cbbml(55,'Indiana ML v Kentucky','UK v IU','5:00','26NOV20UKIND','Indiana',3.5,'Indiana -3.5, neutral site.')
cbbml(56,'Georgia ML at Georgia Tech','UGA@GT','5:00','26NOV20UGAGT','Georgia',8.5,'Georgia -8.5 on the road.')
cbbml(57,'Xavier ML v Iowa','IOWA@XAV','4:30','26NOV20IOWAXAV','Xavier',3.5,'Xavier -3.5 at home.')
A(58,'Josh Giddey','ast',8)
# ---- college football team lines (spread SD 14, capped at 69)
def cfml(no,txt,g,t,ev,sub,sp,where):
  k=kgame('KXNCAAFGAME',ev,sub);SUB[no]=team(txt,100*phi(sp/14),g,t,'ml','CFB',f"College football. Graded from the betting line, capped under 70. {where}"+kn(k),k=k)
cfml(59,'UCF ML v Iowa State','ISU@UCF','3:00','26NOV20ISUUCF','UCF',-1.5,'Iowa State -1.5 on the road, so UCF is a slight home underdog. Kicks off at 3 PM PT.')
cfml(60,'Duke ML v Clemson','CLEM@DUKE','4:30','26NOV20CLEMDUKE','Duke',11.5,'Duke -11.5 at home.')
cfml(61,'Oregon ML at Michigan State','ORE@MSU','5:00','26NOV20OREMSU','Oregon',17.5,'Oregon -17.5 on the road.')
c=kcurve('KXNCAAFSPREAD','26NOV20OREMSU',r'Oregon wins by over ([\d.]+)');k,ki=kat(c,14)
SUB[62]=team('Oregon -14 at Michigan State',100*phi((17.5-14)/14),'ORE@MSU','5:00','spread','CFB',"College football. Graded from the betting line, capped under 70. Book spread is Oregon -17.5, so -14 is 3.5 points better."+kn(k,ki),k=k)
cfml(63,'New Mexico ML at Wyoming','UNM@WYO','6:00','26NOV20UNMWYO','New Mexico',9.5,'New Mexico -9.5 on the road.')
c=kcurve('KXNCAAFSPREAD','26NOV20UNMWYO',r'New Mexico wins by over ([\d.]+)');k,ki=kat(c,6.5)
SUB[64]=team('New Mexico -6.5 at Wyoming',100*phi((9.5-6.5)/14),'UNM@WYO','6:00','spread','CFB',"College football. Graded from the betting line, capped under 70. Book spread is New Mexico -9.5, so -6.5 is 3 points better."+kn(k,ki),k=k)
A(65,'Michael Porter Jr.','pts',21,orig='over 20.5 points');A(66,'Tyrese Proctor','3pm',2,orig='over 1.5 threes')
A(67,'Luka Doncic','pts',37,under=True,orig='under 36.5 points');A(68,'Tristan da Silva','pts',12,orig='over 11.5 points');A(69,'Sion James','ast',4,orig='over 3.5 assists')
A(70,'Michael Porter Jr.','pts',20);A(71,'Tyrese Proctor','3pm',1);A(72,'Luka Doncic','pts',40,under=True,orig='under 40 points (39 or fewer)')
A(73,'Tristan da Silva','pts',10);A(74,'Sion James','ast',3)
A(75,'Isaiah Hartenstein','ast',4);A(76,'Isaiah Hartenstein','ast',2);A(77,'Isaiah Hartenstein','reb',10);A(78,'Isaiah Hartenstein','reb',8)
A(79,'Dyson Daniels','reb',6);A(80,'Dyson Daniels','ast',4);A(81,'Franz Wagner','ast',8);A(82,'Franz Wagner','ast',6);A(83,'Cade Cunningham','ast',8);A(84,'Cade Cunningham','ast',6)
A(85,'Jamal Murray','reb',6,under=True,orig='under 6 rebounds (5 or fewer)')
cbbml(86,'Utah Valley ML v East Carolina','UVU v ECU','5:00','26NOV20ECUUVU','Utah Valley',3.5,'Utah Valley -3.5, neutral site.')
SUB[87]=None  # SFA v Indiana State tipped at noon PT
cbbml(88,'Iona ML v Kansas City','KC@IONA','4:00','26NOV20UMKCIONA','Iona',4.5,'Iona -4.5 at home.')
SUB[89]=SUB[57]
def cbbtot(no,txt,g,t,ev,line,book,over):
  c=kcurve('KXNCAAMBTOTAL',ev,r'Over ([\d.]+) points');k,ki=kat(c,line)
  z=(book-line)/15 if over else (line-book)/15
  SUB[no]=team(txt,100*phi(z),g,t,'total','CBB',f"College hoops. Graded from the betting line, capped under 70. Book total is {book}."+kn(k,ki,flip=not over),k=None if k is None else (k if over else 100-k))
cbbtot(90,'Eastern Illinois v Illinois under 170 total points','EIU@ILL','6:00','26NOV20EIUILL',170,165.5,False)
cbbtot(91,'Sam Houston v Boise State under 175 total points','SHSU@BOIS','6:00','26NOV20SHSUBSU',175,170.5,False)
cbbtot(92,'UT Martin v Southern Illinois over 145 total points','UTM v SIU','2:30','26NOV20UTMSIU',145,149.5,True)
cbbtot(93,"Saint Joseph's v Drexel over 135 total points",'JOES@DREX','4:00','26NOV20JOESDREX',135,138.5,True)
SUB[94]=None  # GW v UAB tipped at 11 AM PT
# ---- NBA team lines (win and spread SD 12, total SD 17), capped at 80 for moneylines like before
def nbaml(no,tm,nick,opn):
  g=G[tm];k=kgame('KXNBAGAME',EV,FULL[tm].replace('the ',''))
  SUB[no]=team(f"{nick} ML v {opn}",100*phi(-g['sp']/12),g['g'],g['t'],'ml','NBA',f"Graded from the betting spread ({nick} {g['sp']:+g})."+kn(k),k=k,cap=88)
def nbasp(no,tm,nick,opn,line):
  g=G[tm];fav=g['sp']<0
  if fav:
    c=kcurve('KXNBASPREAD',EV+TK(g['g']),rf"{FULL[tm].replace('the ','')} wins by over ([\d.]+)");k,ki=kat(c,line+0.5 if line==int(line) else line)
  pct=100*phi((-g['sp']-line)/12) if line>0 else 0
  SUB[no]=team(f"{nick} -{line:g} v {opn}",pct,g['g'],g['t'],'spread','NBA',f"Book spread is {nick} {g['sp']:+g}. Graded from the betting spread."+kn(k,ki),k=k,cap=88)
nbaml(95,'CHI','Bulls','Wizards');nbaml(96,'OKC','Thunder','Pelicans');nbasp(97,'OKC','Thunder','Pelicans',9)
nbaml(98,'CLE','Cavs','Pacers');nbasp(99,'CLE','Cavs','Pacers',6);nbaml(100,'DET','Pistons','Raptors');nbasp(101,'DET','Pistons','Raptors',6)
g=G['BKN'];c=kcurve('KXNBASPREAD',EV+'ORLBKN',r'Orlando wins by over ([\d.]+)');k,ki=kat(c,6.5)
SUB[102]=team('Nets +6.5 v Magic',100*phi((6.5-6.5)/12),'ORL@BKN','4:30','spread','NBA',"Book spread is Magic -6.5, so +6.5 is right on the number, a coin flip. Banchero is out for Orlando."+kn(k,ki,flip=True),k=None if k is None else 100-k,cap=88)
def nbatot(no,txt,gk,line,over):
  g=GM[gk];c=kcurve('KXNBATOTAL',EV+TK(gk),r'Over ([\d.]+) points');k,ki=kat(c,(line+0.5 if over else line-0.5) if line==int(line) else line)
  z=(g[3]-line)/17 if over else (line-g[3])/17
  SUB[no]=team(txt,100*phi(z),gk,g[0],'total','NBA',f"Book total is {g[3]}. Graded from the betting total."+kn(k,ki,flip=not over),k=None if k is None else (k if over else 100-k),cap=80)
nbatot(103,'Wizards v Bulls under 240 total points','WSH@CHI',240,False);nbatot(104,'Pacers v Cavs under 235 total points','IND@CLE',235,False)
nbatot(105,'Raptors v Pistons over 215 total points','TOR@DET',215,True);nbatot(106,'Hornets v Hawks over 215 total points','CHA@ATL',215,True)
nbatot(107,'Magic v Nets over 220 total points','ORL@BKN',220,True)
# ---- one row per leg: an alt rung that matches a submitted pick points to the submitted row
seen={};keep=[];remap={}
for i,r in enumerate(rows):
  if r['p'] in seen:
    j=seen[r['p']]
    if r.get('moved') and 'Safer' in r['n']: remap[i]=j;continue
    if rows[j].get('moved') and 'Safer' in rows[j]['n']: rows[j]=r;remap[i]=j;continue
    remap[i]=j;continue
  seen[r['p']]=i;remap[i]=i
new=[];pos={}
for i,r in enumerate(rows):
  if remap[i]==i: pos[i]=len(new);new.append(r)
SUB={no:(None if i is None else pos[remap[i]]) for no,i in SUB.items()};rows=new
# ---- flags
for no in (67,72): rows[SUB[no]]['fl']='RULE';rows[SUB[no]]['n']+=" Breaks Ace's no-unders-on-Luka rule. Graded for the record only."
r=rows[SUB[19]];r['fl']='Q';r['n']+=' Sengun is questionable (eye). Check before you play it.'
json.dump({'rows':rows,'sub':SUB},open(D+'fri20.json','w'))
for no in sorted(SUB):
  i=SUB[no];r=rows[i] if i is not None else None
  print(no,'-' if r is None else (r['pct'],'K'+str(r.get('k','-')),r.get('fl',''),'|',r['p']))
print(len(rows),'rows')
for r in rows:
  if r.get('moved') and 'Safer' in r['n']: print('ALT',r['pct'],'K',r.get('k'),r['p'])
