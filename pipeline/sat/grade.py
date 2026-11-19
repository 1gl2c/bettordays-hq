import json,math,statistics as S
L=json.load(open('sat/logs.json'))
def phi(z): return 0.5*(1+math.erf(z/math.sqrt(2)))
def prob(p,stat,k):
  g=L[p]; vals=[(x['pts']+x['reb']+x['ast']) if stat=='pra' else x[stat] for x in g]
  n=len(vals); mu=S.mean(vals); sd=max(S.pstdev(vals),1.0+0.25*math.sqrt(max(mu,1)))
  pn=1-phi((k-0.5-mu)/sd); hs=sum(v>=k for v in vals); h5=sum(v>=k for v in vals[:5]); m5=min(5,n)
  ps=(hs+2*pn)/(n+2); p5=(h5+2*ps)/(m5+2)
  return 0.6*ps+0.4*p5,(mu,hs,n,h5,m5)
GM={'DEN':('DEN@NOP','4:00'),'DAL':('DAL@CLE','4:30'),'CLE':('DAL@CLE','4:30'),'DET':('DET@MIA','5:00'),'MIA':('DET@MIA','5:00'),'BKN':('BKN@MEM','5:00'),'MEM':('BKN@MEM','5:00'),'MIN':('CHI@MIN','5:00')}
TM={'John Collins':'DET','Jaylon Tyson':'CLE','Nolan Traore':'BKN','Jamal Murray':'DEN','Ayo Dosunmu':'MIN','Nikola Jokic':'DEN','Cameron Boozer':'MEM','Cade Cunningham':'DET','P.J. Washington':'DAL','Giannis Antetokounmpo':'MIA','Daniss Jenkins':'DET'}
ROOK={'Nolan Traore','Cameron Boozer'}
CTX={'Jamal Murray':'Denver -12.5. Blowout risk, starters may sit the 4th.','Nikola Jokic':'Denver -12.5. Blowout risk, starters may sit the 4th.','Ayo Dosunmu':'Wolves -15.5. Blowout risk cuts his minutes.',
 'John Collins':'Duren out, but his scoring swings a lot game to game.','Jaylon Tyson':'Mitchell, Harden and Allen are all questionable. If they sit he gets more shots. Check before lock.',
 'Nolan Traore':'Probable (calf). Rookie, grade capped at 80.','Cameron Boozer':'Ty Jerome out, so more of the offense runs through him. Second night of a back-to-back. Rookie, capped at 80.',
 'Cade Cunningham':'','P.J. Washington':'Lively out.','Giannis Antetokounmpo':'Probable (wrist).','Daniss Jenkins':''}
SN={'pts':'pts','reb':'reb','ast':'ast','3pm':'threes','pra':'PRA'}
rows=[]
def add(text,p,stat,k,under=False,moved=False,st='alt',adj=0,cap=None):
  pr,(mu,hs,n,h5,m5)=prob(p,stat,k)
  if under: pr=1-pr; hs=n-hs; h5=m5-h5
  pct=100*pr
  pct=0.8*pct+0.2*65   # v6: small samples pulled toward the middle
  pct+=adj
  pct=min(pct,88)
  if p in ROOK: pct=min(pct,80)
  if cap: pct=min(pct,cap)
  pct=max(5,round(pct))
  g,t=GM[TM[p]]
  note=f"{'Stayed under' if under else 'Hit'} {hs} of {n} this season, {h5} of {m5} last 5 (avg {mu:.1f} {SN[stat]}). {CTX.get(p,'')}".strip()
  if cap and pct==cap: note+=f" Capped at {cap}."
  r=dict(p=text,pct=pct,g=g,t=t,ty='prop',st=st,n=('Moved line. ' if moved else '')+note,sp='NBA')
  if moved: r['moved']=True
  rows.append(r)
add("John Collins 10+ points","John Collins",'pts',10);add("John Collins over 10.5 points","John Collins",'pts',11,st='reg');add("John Collins 15+ points","John Collins",'pts',15)
add("Jaylon Tyson over 11.5 points","Jaylon Tyson",'pts',12,st='reg');add("Jaylon Tyson 10+ points","Jaylon Tyson",'pts',10);add("Jaylon Tyson 15+ points","Jaylon Tyson",'pts',15)
add("Nolan Traore 10+ points","Nolan Traore",'pts',10);add("Nolan Traore over 11.5 points","Nolan Traore",'pts',12,st='reg');add("Nolan Traore 15+ points","Nolan Traore",'pts',15)
add("Jamal Murray under 5 rebounds","Jamal Murray",'reb',5,under=True,adj=3);add("Jamal Murray under 6 rebounds","Jamal Murray",'reb',6,under=True,adj=3);add("Jamal Murray under 4.5 rebounds","Jamal Murray",'reb',5,under=True,st='reg',adj=3)
add("Ayo Dosunmu under 5 assists","Ayo Dosunmu",'ast',5,under=True,adj=3);add("Ayo Dosunmu under 6 assists","Ayo Dosunmu",'ast',6,under=True,adj=3);add("Ayo Dosunmu under 4.5 assists","Ayo Dosunmu",'ast',5,under=True,st='reg',adj=3)
add("Nikola Jokic 25+ points","Nikola Jokic",'pts',25,adj=-5)
add("Cameron Boozer 4+ assists","Cameron Boozer",'ast',4,adj=3)
add("Cade Cunningham 4+ rebounds","Cade Cunningham",'reb',4,cap=65);add("Cade Cunningham 6+ rebounds","Cade Cunningham",'reb',6,cap=65)
add("P.J. Washington 20+ PRA","P.J. Washington",'pra',20,cap=65)
add("Giannis Antetokounmpo 20+ points","Giannis Antetokounmpo",'pts',20);add("Giannis Antetokounmpo 25+ points","Giannis Antetokounmpo",'pts',25)
add("Daniss Jenkins 1+ three","Daniss Jenkins",'3pm',1);add("Daniss Jenkins 2+ threes","Daniss Jenkins",'3pm',2)
# moved lines
for a in [("Cade Cunningham 6+ assists","Cade Cunningham",'ast',6),("Cade Cunningham 15+ points","Cade Cunningham",'pts',15),("Cade Cunningham 20+ points","Cade Cunningham",'pts',20),
 ("Giannis Antetokounmpo 8+ rebounds","Giannis Antetokounmpo",'reb',8),("Jamal Murray 2+ threes","Jamal Murray",'3pm',2),("Nikola Jokic 6+ assists","Nikola Jokic",'ast',6),("Nikola Jokic 20+ points","Nikola Jokic",'pts',20),
 ("Ayo Dosunmu 10+ points","Ayo Dosunmu",'pts',10),("Cameron Boozer 6+ rebounds","Cameron Boozer",'reb',6),("P.J. Washington 4+ rebounds","P.J. Washington",'reb',4),("Nolan Traore 8+ points","Nolan Traore",'pts',8)]:
  add(*a,moved=True,adj=-4 if a[1] in('Jamal Murray','Nikola Jokic','Ayo Dosunmu') else 0)
def G(p,pct,g,t,ty,n,sp,fl=None,st='reg'):
  r=dict(p=p,pct=pct,g=g,t=t,ty=ty,st=st,n=n,sp=sp)
  if fl: r['fl']=fl
  rows.append(r)
U='Graded off the market price (Kalshi {}%). We have almost no UFC record yet, so there is no edge claim here.'
G("Ciryl Gane ML v Hokit",66,"UFC 334","6:00",'ml',U.format(66)+' Main event, walks last.','UFC')
G("Amanda Nunes ML v Harrison",41,"UFC 334","6:00",'ml',U.format(41)+' Underdog.','UFC')
G("Yousri Belgaroui ML v Borralho",42,"UFC 334","6:00",'ml',U.format(42)+' Underdog.','UFC')
G("Uros Medic ML v Holland",61,"UFC 334","6:00",'ml',U.format(61),'UFC')
G("Medic v Holland under 1.5 rounds",40,"UFC 334","6:00",'total','Two finishers, but a fight ending inside 7:30 is under a coin flip. No market price to check against.','UFC')
G("Medic v Holland under 2 rounds",48,"UFC 334","6:00",'total','Ends before the 2nd round is over. No market price to check against.','UFC',st='alt')
G("Hasan v Gurule under 1.5 rounds",45,"UFC 334","6:00",'total','Hasan is an 89% favorite, but a quick finish is still a guess. No market price.','UFC')
G("Stephen Thompson ML v Radtke",57,"UFC 334","4:00",'ml',U.format(57),'UFC')
G("Drew Dober ML v Duncan",38,"UFC 334","4:00",'ml',U.format(38)+' Underdog.','UFC')
G("Melquizael Costa ML v Gordon",78,"UFC 334","2:00",'ml',U.format(78)+' Early prelim.','UFC')
G("Costa by KO or decision (double chance)",62,"UFC 334","2:00",'prop','Costa wins, just not by submission. He has subs on his record, so this gives some back.','UFC')
G("Costa by KO",22,"UFC 334","2:00",'prop','One method only. Long shot.','UFC')
G("Costa by decision",40,"UFC 334","2:00",'prop','Gordon is durable. Most likely single method.','UFC')
G("Bia Mesquita ML v Chiasson",70,"UFC 334","2:00",'ml',U.format(70)+' Early prelim.','UFC')
G("Mesquita by submission",44,"UFC 334","2:00",'prop','World-class jiu-jitsu, most of her wins are subs. Still one method only.','UFC')
G("Juan Diaz ML v Alatengheili",77,"UFC 334","2:00",'ml',U.format(77)+' Early prelim.','UFC')
G("Diaz by decision",35,"UFC 334","2:00",'prop','One method only.','UFC')
G("Evan Elder ML v Sanches",48,"UFC 334","2:00",'ml',U.format(48)+' Coin flip.','UFC')
LV='Game already started when the picks came in. The price has moved.'
G("Georgia ML v Missouri",97,"MIZ@UGA","12:30",'ml',LV+' Georgia led 24-0 in the 2nd.','CFB','LIVE')
G("Georgia -3.5 v Missouri",95,"MIZ@UGA","12:30",'spread',LV,'CFB','LIVE',st='alt')
G("Georgia -4.5 v Missouri",95,"MIZ@UGA","12:30",'spread',LV,'CFB','LIVE')
G("Georgia -7 v Missouri",93,"MIZ@UGA","12:30",'spread',LV,'CFB','LIVE',st='alt')
G("Georgia -14 v Missouri",85,"MIZ@UGA","12:30",'spread',LV,'CFB','LIVE',st='alt')
G("Indiana ML v USC",68,"USC@IU","12:30",'ml',LV+' Indiana led 7-3 in the 2nd.','CFB','LIVE')
G("USC ML v Indiana",32,"USC@IU","12:30",'ml',LV+' Both sides of this game were sent. Indiana is the side.','CFB','LIVE')
G("Georgia Southern ML v Georgia State",50,"GASO@GAST","12:30",'ml',LV+' Tied 14-14 in the 2nd.','CFB','LIVE')
G("Rice ML v Tulane",30,"TULN@RICE","1:30",'ml',LV+' Tulane is the better team.','CFB','LIVE')
G("Syracuse ML v NC State",99,"SYR@NCSU","12:00",'ml','Already final. Syracuse won 34-31.','CFB','FINAL')
G("Coastal Carolina ML v Arkansas State",99,"ARST@CCU","12:00",'ml','Already final. Coastal won 28-21.','CFB','FINAL')
G("Penn State ML v Minnesota",83,"MINN@PSU","4:00",'ml','Penn State -12.5 at home.','CFB')
G("Oregon State v Boise State over 50 total points",82,"ORST@BOIS","3:00",'total','Listed as Oregon v Boise State. Boise plays Oregon State today. Total is 65.5.','CFB',st='alt')
G("LSU ML v Texas",65,"TEX@LSU","4:30",'ml','LSU -4.5 at home.','CFB')
G("Utah ML v Arizona",53,"UTAH@ARIZ","7:30",'ml','Utah -1.5 on the road. Close to a coin flip.','CFB')
G("BYU ML v Baylor",76,"BAY@BYU","4:00",'ml','BYU -8.5 at home.','CFB')
G("BYU -2.5 v Baylor",68,"BAY@BYU","4:00",'spread','BYU -8.5 at home.','CFB',st='alt')
G("BYU -6.5 v Baylor",56,"BAY@BYU","4:00",'spread','BYU -8.5 at home.','CFB')
json.dump(rows,open('sat/sat.json','w'))
for r in sorted(rows,key=lambda r:-r['pct']): print(f"{r['pct']:3d} {r.get('fl','') or ('M' if r.get('moved') else ''):5s} {r['p'][:46]:46s} {r['g']:9s} {r['t']:5s} {r['n'][:70]}")
