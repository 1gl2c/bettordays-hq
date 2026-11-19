import json,math,re,unicodedata,statistics as S
from collections import defaultdict
L=json.load(open('mon/logs.json'));M=json.load(open('mon/meta.json'));K=json.load(open('mon/kalshi.json'))
OPP=json.load(open('mon/nba_opp.json'));TS=json.load(open('mon/teamstats.json'))
def phi(z): return 0.5*(1+math.erf(z/math.sqrt(2)))
def nrm(s): return unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode().lower().replace('.','').replace("'",'').strip()
# ---- Kalshi tables
SER={'pts':'KXNBAPTS','reb':'KXNBAREB','ast':'KXNBAAST','3pm':'KXNBA3PT','pra':'KXNBAPRA','recyds':'KXNFLRECYDS','rush':'KXNFLRSHYDS','pass':'KXNFLPASSYDS','rec':'KXNFLREC','rr':'KXNFLRRYDS'}
KT=defaultdict(dict)
for st,s in SER.items():
  for m in K[s]:
    if '26NOV16' not in m['event_ticker']: continue
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
for t,(g,tm,sp,ou) in {'ORL':('ORL@BOS','4:00',9.5,214.5),'BOS':('ORL@BOS','4:00',-9.5,214.5),'CHI':('CHI@CLE','4:00',8.5,241.5),'CLE':('CHI@CLE','4:00',-8.5,241.5),'MEM':('MEM@WSH','4:00',-3.5,232.5),'WSH':('MEM@WSH','4:00',3.5,232.5),
  'PHI':('PHI@BKN','4:30',-4.5,226.5),'BKN':('PHI@BKN','4:30',4.5,226.5),'HOU':('HOU@MIA','4:30',-2.5,232.5),'MIA':('HOU@MIA','4:30',2.5,232.5),'POR':('POR@MIN','5:00',2.5,227.5),'MIN':('POR@MIN','5:00',-2.5,227.5),
  'GS':('GS@NO','5:00',-3.5,223.5),'NO':('GS@NO','5:00',3.5,223.5),'PHX':('PHX@DEN','6:00',9.5,229.5),'DEN':('PHX@DEN','6:00',-9.5,229.5),'LAC':('LAC@BAL','5:15',4.5,39.5),'BAL':('LAC@BAL','5:15',-4.5,39.5)}.items(): G[t]=dict(g=g,t=tm,sp=sp,ou=ou)
def opp(t): a,b=G[t]['g'].split('@'); return b if t==a else a
B2B={'PHI','PHX','BOS','HOU','WSH'}
FULL={'BOS':'Boston','ORL':'Orlando','CLE':'Cleveland','CHI':'Chicago','MEM':'Memphis','WSH':'Washington','PHI':'Philadelphia','BKN':'Brooklyn','HOU':'Houston','MIA':'Miami','POR':'Portland','MIN':'Minnesota','GS':'Golden State','NO':'New Orleans','PHX':'Phoenix','DEN':'Denver','BAL':'Baltimore','LAC':'the Chargers'}
NBAK={'pts':'points','reb':'totalRebounds','ast':'assists','3pm':'threePointFieldGoalsMade-threePointFieldGoalsAttempted'}
NFLK={'recyds':'receivingYards','rush':'rushingYards','pass':'passingYards','rec':'receptions'}
UN={'pts':'pts','reb':'reb','ast':'ast','3pm':'threes','pra':'PRA','recyds':'rec yds','rush':'rush yds','pass':'pass yds','rec':'catches','rr':'rush+rec yds','td':'TDs'}
WORD={'td':'touchdowns','pts':'points','reb':'rebounds','ast':'assists','3pm':'threes','pra':'points + rebounds + assists','recyds':'receiving yards','rush':'rushing yards','pass':'passing yards','rec':'receptions','rr':'rushing + receiving yards'}
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
  v=vals(p,st);n=len(v);mu=S.mean(v);nfl=st in('recyds','rush','pass','rec','rr','td')
  sd=max(S.pstdev(v),(0.35*mu+5) if (nfl and st not in('rec','td')) else 1.0+0.25*math.sqrt(max(mu,1)))
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
CTX={'Franz Wagner':'Banchero is out, so the offense runs through him.','Wendell Carter Jr.':'Banchero is out.','Jayson Tatum':'Second night of a back-to-back.','Jordan Walsh':'Second night of a back-to-back.',
 'Donovan Mitchell':'Mobley is out. Chicago gives up the most points in the league.','Zion Williamson':'Murphy, Murray and Mathurin are out, so he carries the offense. Warriors are missing Curry, Butler and Porzingis.',
 'Draymond Green':'Curry, Butler, Porzingis and Moody are all out.','Jaden McDaniels':'Anthony Edwards is out, so more shots come his way.','Ayo Dosunmu':'Edwards and DiVincenzo are out, so he handles the ball more. That hurts an assists under.',
 'Nikola Jokic':'Nuggets -9.5. A big lead could cut his fourth quarter.','Fred VanVleet':'Rockets played last night. Check he is active.','Alex Sarr':'Second night of a back-to-back.',
 'Toumani Camara':'Morant and Sharpe are out.','Donovan Clingan':'Morant and Sharpe are out.','Michael Porter Jr.':'','Cam Spencer':'Pippen and Jerome are out, so he runs the offense.',
 'Dillon Brooks':'Second night of a back-to-back. Suns +9.5.','Collin Gillespie':'Second night of a back-to-back. Suns +9.5.','Jordan Goodwin':'Second night of a back-to-back. Suns +9.5.','Jalen Green':'Second night of a back-to-back.',
 'Derrick Henry':'Ravens -4.5 at home against an 0-8 team. Lamar is out, so the run game carries more.','Jacoby Brissett':'Starting for Lamar Jackson. Total is only 39.5.','Zay Flowers':'Brissett at QB, not Lamar.','Mark Andrews':'Brissett at QB, not Lamar.',
 'Justice Hill':'','Omarion Hampton':'Chargers are 0-8 and +4.5.','Kimani Vidal':'Shares carries with Hampton.','Quentin Johnston':'McConkey is out, so he is the top target.','KeAndre Lambert-Smith':'McConkey is out. Only 4 games played.',
 'Justin Herbert':'McConkey is out.',"Ja'Kobi Lane":'Rookie, 5 games.'}
rows=[]
def add(p,st,k,under=False,moved=False,style='alt',adj=0,cap=None,label=None,orig=None):
  team=M[p]['team'];nfl=st in('recyds','rush','pass','rec','rr','td');g=G[team]
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
# ---------- NBA props
add('Franz Wagner','reb',6);add('Franz Wagner','reb',4,moved=True);add('Franz Wagner','pts',15);add('Franz Wagner','pts',20,moved=True);add('Franz Wagner','ast',6);add('Franz Wagner','ast',4,moved=True)
add('Jayson Tatum','3pm',2);add('Jayson Tatum','3pm',1,moved=True);add('Jayson Tatum','pts',20);add('Jayson Tatum','pts',15,moved=True);add('Jayson Tatum','ast',4)
add('Davion Mitchell','3pm',2);add('Davion Mitchell','3pm',1,moved=True)
add('Fred VanVleet','pts',10);add('Fred VanVleet','pts',15)
add('Nikola Jokic','pts',20);add('Nikola Jokic','pts',25);add('Nikola Jokic','pts',15,moved=True);add('Nikola Jokic','reb',8);add('Nikola Jokic','reb',10);add('Nikola Jokic','reb',12);add('Nikola Jokic','ast',6,moved=True);add('Nikola Jokic','ast',8,moved=True)
add('Jaden McDaniels','pra',20);add('Jaden McDaniels','pts',10);add('Jaden McDaniels','pts',15)
add('Wendell Carter Jr.','reb',6);add('Wendell Carter Jr.','reb',4,moved=True)
add('Dillon Brooks','pts',15);add('Dillon Brooks','pts',10,moved=True)
add('Draymond Green','ast',6,orig='over 5 assists');add('Draymond Green','ast',4,moved=True)
add('Jordan Walsh','reb',2,orig='over 2 rebounds');add('Jordan Walsh','reb',4,orig='over 3 rebounds')
add('Noah Clowney','reb',4,orig='over 3 rebounds');add('Noah Clowney','reb',6,orig='over 4 rebounds')
add('Cam Spencer','ast',6,orig='over 6 assists');add('Cam Spencer','ast',8,orig='over 7 assists');add('Cam Spencer','ast',10,orig='over 8 assists');add('Cam Spencer','ast',4,moved=True)
add('Collin Gillespie','pts',10)
add("Day'Ron Sharpe",'ast',4,orig='over 3 assists');add("Day'Ron Sharpe",'ast',2,moved=True);add("Day'Ron Sharpe",'reb',6,moved=True)
add('Ayo Dosunmu','ast',4,under=True);add('Ayo Dosunmu','ast',6,under=True)
add('Donovan Mitchell','pts',25);add('Donovan Mitchell','pts',20)
add('Zion Williamson','pts',20);add('Zion Williamson','pts',15)
add('Michael Porter Jr.','pts',15);add('Michael Porter Jr.','pts',20)
add('Alex Sarr','reb',6);add('Alex Sarr','reb',4,moved=True)
add('Jordan Goodwin','3pm',1,orig='over 0.5 threes');add('Jordan Goodwin','3pm',2,orig='over 1.5 threes')
add('Donovan Clingan','3pm',1,orig='over 0.5 threes');add('Donovan Clingan','reb',8,moved=True)
add('Toumani Camara','3pm',3,under=True)
add('Jalen Green','ast',4,under=True);add('Jalen Green','ast',6,under=True)
# ---------- NFL props
add('KeAndre Lambert-Smith','recyds',10)
add('Mark Andrews','rec',3);add('Mark Andrews','rec',2)
for k in (40,50,60,80): add('Derrick Henry','rush',k,orig='over 80.5 rushing yards' if k==80 else None)
add('Jacoby Brissett','pass',200);add('Jacoby Brissett','pass',175);add('Jacoby Brissett','pass',150,orig='150+ passing + rushing yards');add('Jacoby Brissett','pass',225,orig='over 214.5 passing yards')
add('Zay Flowers','td',1);add('Zay Flowers','recyds',70,orig='over 69.5 receiving yards');add('Zay Flowers','recyds',30);add('Zay Flowers','recyds',40,moved=True);add('Zay Flowers','rec',6,orig='over 5 receptions');add('Zay Flowers','rec',7,orig='over 6 receptions');add('Zay Flowers','rec',4,moved=True)
add('Kimani Vidal','rush',20)
add('Quentin Johnston','recyds',20);add('Quentin Johnston','recyds',40,under=True)
add('Justice Hill','rec',2);add('Justice Hill','rr',30,orig='over 25 and over 30 rushing + receiving yards');add('Justice Hill','td',1)
add('Omarion Hampton','rush',15,orig='15+ rushing + receiving yards');add('Omarion Hampton','rush',25,orig='25+ rushing + receiving yards');add('Omarion Hampton','rr',40,moved=True);add('Omarion Hampton','td',1)
add('Justin Herbert','pass',150,orig='150+ passing + rushing yards');add('Justin Herbert','pass',175,moved=True);add('Justin Herbert','td',1)
add("Ja'Kobi Lane",'rec',3,under=True)
# ---------- team lines
def team(txt,pct,g,t,ty,sp,note,k=None,st='reg',fl=None,cap=None):
  if cap: pct=min(pct,cap)
  r=dict(p=txt,pct=max(5,round(pct)),g=g,t=t,ty=ty,st=st,n=note,sp=sp)
  if k is not None: r['k']=round(k)
  if fl: r['fl']=fl
  rows.append(r)
for ab,nm,kn in [('CLE','Cleveland Cavaliers ML v Bulls','Cleveland'),('BOS','Boston Celtics ML v Magic','Boston'),('MEM','Memphis Grizzlies ML v Wizards','Memphis'),('PHI','Philadelphia 76ers ML v Nets','Philadelphia'),('DEN','Denver Nuggets ML v Suns','Denver'),('HOU','Houston Rockets ML v Heat','Houston'),('MIN','Minnesota Timberwolves ML v Trail Blazers','Minnesota')]:
  g=G[ab];ev=g['g'].replace('@','').replace('GS','GSW').replace('NO','NOP').replace('WSH','WAS')
  kp=ml('KXNBAGAME','26NOV16',kn+' wins');sp=100*phi(-g['sp']/12)
  pct=(sp+kp)/2 if kp else sp
  o=opp(ab);note=f"{'Favored by '+str(-g['sp']) if g['sp']<0 else 'Underdog by '+str(g['sp'])}. Kalshi has it at {kp}."
  if ab in B2B: pct-=3;note+=' Second night of a back-to-back.'
  if o in B2B: pct+=1;note+=f" {FULL[o]} is on a back-to-back."
  extra={'CLE':' Mobley is out for Cleveland, but Chicago is 3-9 and allows the most points in the league.','BOS':' Banchero is out for Orlando.','MEM':' Memphis is missing Pippen, Jerome and Jackson.','PHI':' Embiid is day to day and LeBron is out.','DEN':'','HOU':' Smart is suspended, Thompson is day to day.','MIN':' Edwards is out. Portland is without Morant and Sharpe.'}[ab]
  team(nm,pct,g['g'],g['t'],'ml','NBA',note+extra,k=kp)
# NFL team
bal=curve('KXNFLSPREAD','26NOV16LACBAL',r'Baltimore wins by over ([\d.]+)');tot=curve('KXNFLTOTAL','26NOV16LACBAL',r'over ([\d.]+) points')
for sp_ in (4.5,7,9,9.5):
  kp=100-interp(bal,sp_+ (0.5 if sp_==int(sp_) else 0) if False else sp_)
  team(f"Chargers +{sp_:g} v Ravens",kp,'LAC@BAL','5:15','spread','NFL',f"Market price. Kalshi has it at {kp:.0f}. The Chargers are 0-8 and McConkey is out. Ravens -4.5 with Brissett at QB. No edge claimed, so it is capped under 70.",k=kp,cap=69)
for u in (40,45,50):
  kp=100-interp(tot,u-0.5)
  team(f"Chargers v Ravens under {u} total points",kp,'LAC@BAL','5:15','total','NFL',f"Market price. Kalshi has it at {kp:.0f}. The total is 39.5 with two backup-level passing games. No edge claimed, so it is capped under 70.",k=kp,cap=69)
# CBB
CB={'WIUMINN':('WIU@MINN','5:00','Minnesota','Western Illinois'),'MONTKSU':('MONT@KSU','5:00','Kansas St','Montana'),'WKUTLSA':('WKU@TLSA','4:00','Tulsa','Western Kentucky'),'CLMBNW':('CLMB@NW','5:00','Northwestern','Columbia'),
 'TXSOUCSD':('TXSO@UCSD','7:00','UC San Diego','Texas Southern'),'EKYKENT':('EKU@KENT','4:00','Kent St','Eastern Kentucky'),'ACMOSU':('AC@MOST','5:00','Missouri St','Abilene Christian'),'CARKOKST':('CARK@OKST','5:00','Oklahoma St','Central Arkansas'),
 'SELATXAM':('SELA@TXAM','5:30','Texas A&M','SE Louisiana'),'PVOSU':('PV@OSU','3:30','Ohio St','Prairie View A&M'),'IONAUMBC':('IONA@UMBC','3:00','UMBC','Iona')}
def favc(ev):
  best=[]
  names=set(re.match(r'(.+?) wins by over',m['title']).group(1) for m in K['KXNCAAMBSPREAD'] if ev in m['event_ticker'] and ' wins by over' in m['title'])
  cs={n:curve('KXNCAAMBSPREAD','26NOV16'+ev,re.escape(n)+r' wins by over ([\d.]+)') for n in names}
  return cs
def cbb(ev,kind,num,txt,side=None,fl=None):
  g,t,fav,dog=CB[ev];cs=favc(ev);tc=curve('KXNCAAMBTOTAL','26NOV16'+ev,r'Over ([\d.]+) points')
  favn=max(cs,key=lambda n:len(cs[n])) if cs else None
  if kind=='dog': kp=100-interp(cs[favn],num)   # dog +num
  elif kind=='dogx': kp=100-interp(cs.get('Iona',[]),num) if cs.get('Iona') else None
  elif kind=='fav': kp=interp(cs[favn],num)
  elif kind=='over': kp=interp(tc,num-0.5)
  elif kind=='under': kp=100-interp(tc,num-0.5)
  elif kind=='ml': kp=ml('KXNCAAMBGAME','26NOV16'+ev,side)
  if kp is None: kp=50
  note=f"College basketball. Graded at Kalshi's price ({kp:.0f}) because we have no team data of our own. No edge claimed, so it is capped under 70 and stays off the main tickets."
  team(txt,kp,g,t,{'dog':'spread','dogx':'spread','fav':'spread','over':'total','under':'total','ml':'ml'}[kind],'CBB',note,k=kp,cap=69,fl=fl)
cbb('PVOSU','fav',30,'Ohio State -30 v Prairie View A&M',fl='LIVE')
cbb('IONAUMBC','over',140,'Iona v UMBC over 140 total points',fl='LIVE');cbb('IONAUMBC','over',130,'Iona v UMBC over 130 total points',fl='LIVE')
cbb('IONAUMBC','dogx',3,'UMBC +3 v Iona',fl='LIVE');cbb('IONAUMBC','dogx',5,'UMBC +5 v Iona',fl='LIVE')
cbb('WIUMINN','dog',40,'Western Illinois +40 v Minnesota')
for n in (135,130,125): cbb('WIUMINN','over',n,f'Western Illinois v Minnesota over {n} total points')
cbb('MONTKSU','dog',17.5,'Montana +17.5 v Kansas State');cbb('MONTKSU','dog',20,'Montana +20 v Kansas State')
cbb('WKUTLSA','ml',0,'Tulsa ML v Western Kentucky',side='Tulsa');cbb('WKUTLSA','fav',1.5,'Tulsa -1.5 v Western Kentucky');cbb('WKUTLSA','fav',2.5,'Tulsa -2.5 v Western Kentucky');cbb('WKUTLSA','fav',6,'Tulsa -6 v Western Kentucky')
cbb('CLMBNW','dog',11.5,'Columbia +11.5 v Northwestern');cbb('CLMBNW','dog',15,'Columbia +15 v Northwestern')
cbb('TXSOUCSD','dog',20,'Texas Southern +20 v UC San Diego');cbb('TXSOUCSD','dog',25,'Texas Southern +25 v UC San Diego')
for n in (165,170,175): cbb('EKYKENT','under',n,f'Eastern Kentucky v Kent State under {n} total points')
for n in (140,135,130): cbb('ACMOSU','over',n,f'Abilene Christian v Missouri State over {n} total points')
for n in (165,170,175): cbb('CARKOKST','under',n,f'Central Arkansas v Oklahoma State under {n} total points')
for n in (160,165,170,175): cbb('SELATXAM','under',n,f'SE Louisiana v Texas A&M under {n} total points')
rows.append(dict(p='Alexander Zverev +1.5 sets',pct=55,g='ATP',t='',ty='spread',st='reg',n='Not graded. We have no tennis data and no Kalshi price pulled for this match. Leave it off tickets.',sp='TEN',fl='VERIFY'))
json.dump(rows,open('mon/mon.json','w'))
print(len(rows))
for r in sorted(rows,key=lambda r:-r['pct']): print(r['pct'],'K'+str(r.get('k','-')),r.get('mu',''),'|',r['p'],'|',r['g'],r['t'],r.get('fl',''))
