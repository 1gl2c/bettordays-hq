import json,math,statistics as S
L=json.load(open('logs.json'))
def nm(x): return x
G={'ATL':('ATL@CHI','5:00'),'CHI':('ATL@CHI','5:00'),'CLE':('CLE@MIA','5:00'),'MIA':('CLE@MIA','5:00'),'NY':('NYK@IND','4:00'),'IND':('NYK@IND','4:00'),
'MIL':('MIL@ORL','4:00'),'ORL':('MIL@ORL','4:00'),'MEM':('MEM@NOP','5:00'),'NO':('MEM@NOP','5:00'),'HOU':('UTA@HOU','5:30'),'UTAH':('UTA@HOU','5:30'),
'SA':('GSW@SAS','6:30'),'GS':('GSW@SAS','6:30'),'SAC':('POR@SAC','7:00'),'POR':('POR@SAC','7:00'),'LAC':('OKC@LAC','7:30'),'OKC':('OKC@LAC','7:30')}
R=json.load(open('roster.json'))
TEAM={'Yaxel Lendeborg':'GS','Darius Acuff Jr.':'SAC','Cameron Boozer':'MEM','Brayden Burries':'MIL'}
def team(p): return TEAM.get(p) or R[p][1]
def pos(p): return (R.get(p) or ['','','F'])[2]
# context adjustment (points of probability) per player, per stat ('*' all)
ADJ={
 'Donovan Mitchell':{'pts':3,'_':'Mobley out, more shots.'},
 'Jarrett Allen':{'reb':6,'_':'Mobley out, he owns the glass.'},
 'Peyton Watson':{'pts':2,'_':'Mobley out, more minutes.'},
 'Alperen Sengun':{'reb':3,'ast':0,'*':-6,'_':'Capela and Adams out, but Houston -15.5 means the 4th quarter may be bench time.'},
 'Jabari Smith Jr.':{'reb':4,'*':-6,'_':'Bigs out, but Houston -15.5 is blowout risk.'},
 'Kevin Durant':{'*':-6,'_':'Houston -15.5. Blowout risk, he could sit the 4th.'},
 'Fred VanVleet':{'*':-6,'_':'Houston -15.5. Blowout risk.'},
 'Reed Sheppard':{'*':4,'_':'Smart suspended and a likely blowout. More minutes.'},
 'Shai Gilgeous-Alexander':{'*':2,'_':'Jalen Williams and Holmgren out. Everything runs through him.'},
 'Isaiah Hartenstein':{'*':3,'_':'Holmgren out.'},
 'Deni Avdija':{'*':-4,'_':'Portland -10.5. Some blowout risk.'},
 'Donovan Clingan':{'*':-4,'_':'Portland -10.5. Some blowout risk.'},
 'Sidy Cissoko':{'*':-3,'_':'Portland -10.5.'},
 'Domantas Sabonis':{'reb':3,'_':'Achiuwa out.'},
 'Dylan Harper':{'pts':1,'_':'Fox and Vassell questionable, but Spurs -12.5 blowout risk.'},
 'Yaxel Lendeborg':{'pts':4,'_':'Curry out. More shots.'},
 'Pascal Siakam':{'pts':2,'_':'Haliburton out. He carries Indiana.'},
 'Josh Hart':{'*':-3,'_':'Knicks -7.5.'},'Karl-Anthony Towns':{'*':-2,'_':'Knicks -7.5.'},
 'Cameron Boozer':{'reb':5,'_':'Edey and Post out. More boards.'},
 'Herbert Jones':{'reb':5,'_':'Murphy, Missi and Watford out. Big minutes.'},
 'Darius Garland':{'*':2,'_':'Ingram out. More usage.'},
 'Jalen Johnson':{'*':2,'_':'245.5 total, fastest game on the board.'},'Dyson Daniels':{'*':2,'_':'245.5 total.'},'Nickeil Alexander-Walker':{'*':2,'_':'245.5 total.'},
 'Onyeka Okongwu':{'*':2,'_':'245.5 total.'},'Josh Giddey':{'*':2,'_':'245.5 total.'},'Matas Buzelis':{'*':2,'_':'245.5 total.'},
}
def phi(z): return 0.5*(1+math.erf(z/math.sqrt(2)))
def prob(p,stat,k,under=False):
  g=L.get(p) or []
  if not g: return None,None
  vals=[ (x['pts']+x['reb']+x['ast']) if stat=='pra' else x[stat] for x in g]
  n=len(vals); mu=S.mean(vals); sd=max(S.pstdev(vals),1.0+0.25*math.sqrt(max(mu,1)))
  pn=1-phi((k-0.5-mu)/sd)
  hs=sum(v>=k for v in vals); h5=sum(v>=k for v in vals[:5]); m5=min(5,n)
  ps=(hs+2*pn)/(n+2); p5=(h5+2*ps)/(m5+2)
  pr=0.6*ps+0.4*p5
  if under: pr=1-pr
  return pr, (mu,hs,n,h5,m5,vals[:5])
P=[] # (text, player, stat, k, under)
def add(t,p,s,k,u=False,moved=False): P.append((t,p,s,k,u,moved))
for t,p,s,k in [
("Jalen Johnson 6+ assists","Jalen Johnson","ast",6),("Jalen Johnson 8+ assists","Jalen Johnson","ast",8),
("Darius Garland over 2.5 3 pointers made","Darius Garland","3pm",3),("Darius Garland over 1.5 3 pointers made","Darius Garland","3pm",2),("Darius Garland over 0.5 3 pointers made","Darius Garland","3pm",1),
("Sabonis 30+ PRA","Domantas Sabonis","pra",30),("Sabonis 25+ PRA","Domantas Sabonis","pra",25),
("Shai Gilgeous-Alexander over 35 PRA","Shai Gilgeous-Alexander","pra",35),("Shai Gilgeous-Alexander over 40 PRA","Shai Gilgeous-Alexander","pra",40),("Shai Gilgeous-Alexander over 30 PRA","Shai Gilgeous-Alexander","pra",30),
("Dylan Harper over 15 points","Dylan Harper","pts",15),("Dylan Harper over 10 points","Dylan Harper","pts",10),
("Peyton Watson 10+ points","Peyton Watson","pts",10),("Peyton Watson 15+ points","Peyton Watson","pts",15),
("Sidy Cissoko over 1.5 3PM","Sidy Cissoko","3pm",2),("Sidy Cissoko over 0.5 3PM","Sidy Cissoko","3pm",1),
("Darius Garland 2.5 3PM O (dup)","Darius Garland","3pm",3),
("Josh Hart 10+ points","Josh Hart","pts",10),("Matas Buzelis 15+ points","Matas Buzelis","pts",15),("Matas Buzelis 10+ points","Matas Buzelis","pts",10),
("Peyton Watson o13.5 points","Peyton Watson","pts",14),
("Alperen Sengun over 6 assists","Alperen Sengun","ast",6),("Alperen Sengun over 5 assists","Alperen Sengun","ast",5),("Alperen Sengun over 7 assists","Alperen Sengun","ast",7),
("Isaiah Jackson o6 rebounds","Isaiah Jackson","reb",6),("Isaiah Jackson o7 rebounds","Isaiah Jackson","reb",7),("Isaiah Jackson o4 rebounds","Isaiah Jackson","reb",4),
("Herbert Jones o1.5 rebounds","Herbert Jones","reb",2),("Herbert Jones o2.5 rebounds","Herbert Jones","reb",3),
("Jaylen Wells o7.5 points","Jaylen Wells","pts",8),("Jaylen Wells 10+ points","Jaylen Wells","pts",10),
("Okongwu o0.5 3PM","Onyeka Okongwu","3pm",1),
("Jaime Jaquez 10+ points","Jaime Jaquez Jr.","pts",10),("Jaime Jaquez 2+ assists","Jaime Jaquez Jr.","ast",2),
("Peyton Watson over 10 points (dup)","Peyton Watson","pts",10),
("Shai Gilgeous-Alexander 25+ points","Shai Gilgeous-Alexander","pts",25),
("Donovan Mitchell 25+ points","Donovan Mitchell","pts",25),("Donovan Mitchell 20+ points","Donovan Mitchell","pts",20),("Donovan Mitchell 4+ assists","Donovan Mitchell","ast",4),("Donovan Mitchell 6+ assists","Donovan Mitchell","ast",6),
("Pascal Siakam 15+ points","Pascal Siakam","pts",15),("Karl-Anthony Towns 10+ rebounds","Karl-Anthony Towns","reb",10),("Tyler Herro 15+ points","Tyler Herro","pts",15),
("Brayden Burries over 0.5 3PM","Brayden Burries","3pm",1),("Davion Mitchell 10+ points","Davion Mitchell","pts",10),("Jarrett Allen 6+ rebounds","Jarrett Allen","reb",6),
("Nickeil Alexander-Walker 15+ points","Nickeil Alexander-Walker","pts",15),("Josh Giddey 6+ assists","Josh Giddey","ast",6),("Ty Jerome 15+ points","Ty Jerome","pts",15),
("Cameron Boozer 4+ assists","Cameron Boozer","ast",4),("Cameron Boozer 10+ rebounds","Cameron Boozer","reb",10),("Cameron Boozer 8+ rebounds","Cameron Boozer","reb",8),
("Jabari Smith 15+ points","Jabari Smith Jr.","pts",15),("Jabari Smith 10+ points","Jabari Smith Jr.","pts",10),("Jabari Smith 6+ rebounds","Jabari Smith Jr.","reb",6),("Jabari Smith 4+ rebounds","Jabari Smith Jr.","reb",4),
("Kevin Durant 15+ points","Kevin Durant","pts",15),("Yaxel Lendeborg 15+ points","Yaxel Lendeborg","pts",15),("Dylan Harper 15+ points (dup)","Dylan Harper","pts",15),
("Isaiah Hartenstein 15+ PRA","Isaiah Hartenstein","pra",15),("Isaiah Hartenstein 20+ PRA","Isaiah Hartenstein","pra",20),
("Deni Avdija 20+ points","Deni Avdija","pts",20),("Darius Acuff Jr 30+ PRA","Darius Acuff Jr.","pra",30),
("Donovan Mitchell 25+ points (dup)","Donovan Mitchell","pts",25),("Donovan Clingan o11.5 points","Donovan Clingan","pts",12),
("Dyson Daniels 6+ assists","Dyson Daniels","ast",6),("Dyson Daniels 4+ assists","Dyson Daniels","ast",4),("Dyson Daniels 6+ rebounds","Dyson Daniels","reb",6),("Dyson Daniels 4+ rebounds","Dyson Daniels","reb",4),
("Domantas Sabonis o11.5 rebounds","Domantas Sabonis","reb",12),("Jabari Smith o6.5 rebounds","Jabari Smith Jr.","reb",7),
("Fred VanVleet 15+ points","Fred VanVleet","pts",15),("Fred VanVleet 10+ points","Fred VanVleet","pts",10),("Reed Sheppard 10+ points","Reed Sheppard","pts",10),
("Donovan Clingan 10+ points","Donovan Clingan","pts",10),("Jabari Smith 6+ rebounds (dup)","Jabari Smith Jr.","reb",6),
]: add(t,p,s,k)
# moved lines (our own, Kalshi-style rungs)
for t,p,s,k in [("Jalen Johnson 4+ assists","Jalen Johnson","ast",4),("Alperen Sengun 4+ assists","Alperen Sengun","ast",4),("Domantas Sabonis 10+ rebounds","Domantas Sabonis","reb",10),
 ("Karl-Anthony Towns 8+ rebounds","Karl-Anthony Towns","reb",8),("Shai Gilgeous-Alexander 20+ points","Shai Gilgeous-Alexander","pts",20),("Darius Acuff Jr 20+ points","Darius Acuff Jr.","pts",20),
 ("Yaxel Lendeborg 10+ points","Yaxel Lendeborg","pts",10),("Davion Mitchell 6+ assists","Davion Mitchell","ast",6),("Isaiah Hartenstein 8+ rebounds","Isaiah Hartenstein","reb",8),
 ("Jarrett Allen 8+ rebounds","Jarrett Allen","reb",8),("Cameron Boozer 6+ rebounds","Cameron Boozer","reb",6),("Pascal Siakam 20+ points","Pascal Siakam","pts",20),
 ("Deni Avdija 15+ points","Deni Avdija","pts",15),("Tyler Herro 20+ points","Tyler Herro","pts",20),("Nickeil Alexander-Walker 2+ threes","Nickeil Alexander-Walker","3pm",2)]:
  add(t,p,s,k,moved=True)
rows=[]
for t,p,s,k,u,mv in P:
  pr,info=prob(p,s,k,u)
  tm=team(p); g,tt=G[tm]; a=ADJ.get(p,{})
  adj=a.get(s,0)+a.get('*',0)
  pct=pr*100+adj
  note=a.get('_','')
  flags=[]
  if s=='reb' and pos(p)=='G': pct=min(pct,65); note=(note+' Guard rebounds capped at 65.').strip()
  if p=='Herbert Jones' and s=='reb': pct=min(pct,65); note=(note+' Wing rebounds capped at 65.').strip()
  if s=='pra' and p in ('Isaiah Hartenstein',): pct=min(pct,65); note=(note+' Non-star PRA capped at 65.').strip()
  if p in ('Darius Garland',) and s=='3pm': pass
  pct=max(5,min(95,round(pct)))
  mu,hs,n,h5,m5,last=info
  stat={'pts':'pts','reb':'reb','ast':'ast','3pm':'threes','pra':'PRA'}[s]
  rec=f"Hit {hs} of {n} this season, {h5} of {m5} last 5 (avg {mu:.1f} {stat}). {note}".strip()
  rows.append(dict(p=t,pct=pct,g=g,t=tt,sp='nba',ty='prop',moved=mv,n=rec,dup='(dup)' in t))
# game lines
for t,pct,g,tt,ty,n in [
 ("CLE Cavs ML v Heat",42,"CLE@MIA","5:00","ml","Miami -2.5 at home and Mobley is out. Underdog."),
 ("Samford +2.5 v Wright State",58,"WRST@SAM","5:00","spread","Wright State -1.5. Samford at home."),("Samford +4.5 v Wright State",64,"WRST@SAM","5:00","spread",""),("Samford +7.5 v Wright State",72,"WRST@SAM","5:00","spread",""),
 ("Hofstra ML v Iona",77,"IONA@HOF","4:00","ml","Hofstra -7.5 at home."),
 ("UConn ML v Ohio State",87,"OSU@UCONN","4:30","ml","UConn -12.5 at home."),("UConn -1.5 v Ohio State",85,"OSU@UCONN","4:30","spread",""),("UConn -3.5 v Ohio State",81,"OSU@UCONN","4:30","spread",""),
 ("Houston v Colorado over 44.5 total points",66,"HOU@COL","7:15","total","Total is 51.5."),("Houston v Colorado over 40 total points",77,"HOU@COL","7:15","total","Total is 51.5."),
 ("Yale ML v Northeastern",54,"YALE@NE","4:00","ml","Yale -1.5. Basically a coin flip."),
]: rows.append(dict(p=t,pct=pct,g=g,t=tt,sp='ncaab' if g!='HOU@COL' else 'ncaaf',ty=ty,moved=False,n=n,dup=False))
rows.append(dict(p="Dejounte Murray under 25 PRA",pct=0,g='MEM@NOP',t='5:00',sp='nba',ty='prop',moved=False,n='OUT tonight (ankle). Skip.',dup=False,fl='OUT'))
rows.append(dict(p="Dejounte Murray under 30 PRA",pct=0,g='MEM@NOP',t='5:00',sp='nba',ty='prop',moved=False,n='OUT tonight (ankle). Skip.',dup=False,fl='OUT'))
json.dump(rows,open('rows.json','w'))
for r in sorted(rows,key=lambda r:-r['pct']): print(f"{r['pct']:3d} {'M' if r['moved'] else ' '} {r['p'][:44]:44s} {r['g']:9s} {r['n'][:95]}")
