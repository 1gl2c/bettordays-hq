import json,math,statistics as S
L=json.load(open('sun/logs.json'))
def phi(z): return 0.5*(1+math.erf(z/math.sqrt(2)))
NBA={'pts':'points','reb':'totalRebounds','ast':'assists','3pm':'threePointFieldGoalsMade-threePointFieldGoalsAttempted'}
def vals(p,stat):
  g=L[p]['games']
  f=lambda x,k: x.get(k,0) if isinstance(x.get(k,0),(int,float)) else 0
  if stat in NBA: return [f(x,NBA[stat]) for x in g]
  if stat=='rr': return [f(x,'rushingYards')+f(x,'receivingYards') for x in g]
  if stat=='td': return [f(x,'rushingTouchdowns')+f(x,'receivingTouchdowns') for x in g]
  return [f(x,stat) for x in g]
def prob(p,stat,k):
  v=vals(p,stat); n=len(v); mu=S.mean(v)
  nfl=L[p]['lg']=='nfl'
  sd=max(S.pstdev(v),(0.35*mu+5) if (nfl and stat not in('receptions','td','interceptions','passingAttempts')) else 1.0+0.25*math.sqrt(max(mu,1)))
  pn=1-phi((k-0.5-mu)/sd); hs=sum(x>=k for x in v); h5=sum(x>=k for x in v[:5]); m5=min(5,n)
  ps=(hs+2*pn)/(n+2); p5=(h5+2*ps)/(m5+2)
  return 0.6*ps+0.4*p5,(mu,hs,n,h5,m5)
G={'ATL':('KC@ATL','10:00'),'KC':('KC@ATL','10:00'),'CLE':('HOU@CLE','10:00'),'HOU':('HOU@CLE','10:00'),'GB':('MIN@GB','10:00'),'MIN':('MIN@GB','10:00'),'TEN':('JAX@TEN','10:00'),'JAX':('JAX@TEN','10:00'),'IND':('MIA@IND','10:00'),'MIA':('MIA@IND','10:00'),'NO':('CAR@NO','10:00'),'CAR':('CAR@NO','10:00'),'NYJ':('BUF@NYJ','10:00'),'BUF':('BUF@NYJ','10:00'),'LV':('SEA@LV','1:05'),'SEA':('SEA@LV','1:05'),'ARI':('LAR@ARI','1:05'),'LAR':('LAR@ARI','1:05'),'DAL':('SF@DAL','1:25'),'SF':('SF@DAL','1:25'),'CIN':('PIT@CIN','5:20'),'PIT':('PIT@CIN','5:20'),
 'PHIb':('IND@PHI','10:00'),'INDb':('IND@PHI','10:00'),'NYb':('NY@TOR','3:00'),'UTAHb':('SA@UTAH','2:00'),'ATLb':('ATL@MIL','5:00')}
TM={'Justin Jefferson':'MIN','Christian Watson':'GB','Brock Bowers':'LV','Jaxon Smith-Njigba':'SEA',"Ja'Marr Chase":'CIN','Tee Higgins':'CIN','Jaylen Warren':'PIT','Drake London':'ATL','Chris Olave':'NO','Jonathan Taylor':'IND','James Cook':'BUF','Trey McBride':'ARI','CeeDee Lamb':'DAL','Josh Hart':'NYb','Jalen Johnson':'ATLb','Keyonte George':'UTAHb','Anfernee Simons':'PHIb','Pascal Siakam':'INDb','Aaron Rodgers':'PIT','Joe Burrow':'CIN','Christian McCaffrey':'SF','Javonte Williams':'DAL','Kyren Williams':'LAR','Bijan Robinson':'ATL','Patrick Mahomes':'KC','Michael Penix Jr.':'ATL','Jakobi Meyers':'JAX','Trevor Lawrence':'JAX','Cam Ward':'TEN','Aaron Jones':'MIN','Tucker Kraft':'GB','Kenneth Walker III':'KC','Myles Price':'MIN','Xavier Hutchinson':'HOU','Jaylen Brown':'PHIb','Anthony Gould':'IND','Jadarian Price':'SEA','Brock Purdy':'SF','Breece Hall':'NYJ','Seth McGowan':'IND','Tommy Tremble':'CAR','Keenan Allen':'SF','Geno Smith':'NYJ','Emmett Johnson':'KC','Chris Rodriguez Jr.':'JAX','Deshaun Watson':'CLE','Mike Washington':'LV','Josh Allen':'BUF','Chase Brown':'CIN'}
ROOK={'Emmett Johnson','Jadarian Price','Seth McGowan','Mike Washington','Myles Price'}
CTX={'Justin Jefferson':'Kyler Murray is out and the Vikings are on a backup QB. Hockenson and Jennings out too.','Myles Price':'Backup QB. Has topped 20 yards once all year.','Aaron Jones':'Backup QB, but the run game gets leaned on.',
 'Christian Watson':'Josh Jacobs is out, so Green Bay throws more.','Tucker Kraft':'Josh Jacobs is out.',
 'Jaxon Smith-Njigba':'Darnold is out, backup QB. He has 50+ in all 9 games anyway.','Jadarian Price':'Darnold out. Rookie, capped.',
 'Brock Bowers':'Seattle -6.5, so Vegas should be throwing late.','Mike Washington':'Rookie behind Jeanty.',
 'Emmett Johnson':'Kenneth Walker is out, so he should start. But his high this year is 34 rushing yards and Ott is questionable. Role is a guess, so the grade is capped.',
 'Xavier Hutchinson':'Marvin Harrison Jr. and Brevin Jordan are out, so more targets come his way.',
 'Keenan Allen':'Mike Evans and Aiyuk are out.','Kyren Williams':'Rams -9.5. Nacua and Adams are on IR, so the offense runs through him.',
 'James Cook':'Bills -8.5. Good script for carries late.','Trevor Lawrence':'Jaguars -10.5. A big lead means fewer throws late.','Cam Ward':'Titans +10.5, so he should be throwing to catch up. Carnell Tate is out.',
 'Chris Rodriguez Jr.':'Jaguars -10.5. He gets the late carries if they are ahead.','Jakobi Meyers':'Jaguars -10.5. Crowded receiver room.',
 'Keyonte George':'Spurs -16.5. Blowout risk. Markkanen and Jaren Jackson Jr. are out.','Jalen Johnson':'Hawks -8.5 at Milwaukee.','Josh Hart':'','Pascal Siakam':'Haliburton is out, so he carries the scoring. Second night of a back-to-back.','Anfernee Simons':'Comes off the bench, minutes swing a lot.','Jaylen Brown':'Embiid is out.',
 'Jonathan Taylor':'Colts -4.5 at home.','Bijan Robinson':'','Chase Brown':'Sunday night game.','Jaylen Warren':'Sunday night game.','Aaron Rodgers':'Sunday night game. Pittman is on IR.','Joe Burrow':'Sunday night game. Total is 49.5.',"Ja'Marr Chase":'Sunday night game.','Tee Higgins':'Sunday night game.',
 'Breece Hall':'Only 4 games played. Jets +8.5.','Geno Smith':'Jets +8.5, so he should be throwing. Garrett Wilson is questionable.','Josh Allen':'','Deshaun Watson':'','Anthony Gould':'Alec Pierce is on IR. One catch all year.','Seth McGowan':'Rookie behind Taylor.','Tommy Tremble':'','Brock Purdy':'Total is 55.5, highest on the board.','Christian McCaffrey':'Total is 55.5, highest on the board.','Javonte Williams':'Total is 55.5.','CeeDee Lamb':'Total is 55.5. Ferguson is out.','Drake London':'','Michael Penix Jr.':'','Patrick Mahomes':'Walker is out, so more on his arm.','Chris Olave':'','Trey McBride':'Cardinals +9.5, so they will be throwing.'}
UN={'receivingYards':'rec yds','rushingYards':'rush yds','passingYards':'pass yds','receptions':'catches','rr':'rush+rec yds','td':'TDs','passingAttempts':'attempts','interceptions':'INTs','pts':'pts','reb':'reb','ast':'ast','3pm':'threes'}
rows=[]
def add(text,p,stat,k,under=False,moved=False,st='alt',adj=0,cap=None,ty='prop'):
  pr,(mu,hs,n,h5,m5)=prob(p,stat,k)
  if under: pr=1-pr; hs=n-hs; h5=m5-h5
  pct=100*pr; pct=0.8*pct+0.2*65; pct+=adj
  nfl=L[p]['lg']=='nfl'
  pct=min(pct,85 if nfl else 88)
  if p in ROOK: pct=min(pct,80)
  if cap: pct=min(pct,cap)
  pct=max(5,round(pct)); g,t=G[TM[p]]
  if stat=='td': note=f"Scored in {hs} of {n} games, {h5} of {m5} last 5. {CTX.get(p,'')}".strip()
  else: note=f"{'Stayed under' if under else 'Hit'} {hs} of {n} this season, {h5} of {m5} last 5 (avg {mu:.1f} {UN[stat]}). {CTX.get(p,'')}".strip()
  if cap and pct==cap: note+=f" Capped at {cap}."
  r=dict(p=text,pct=pct,g=g,t=t,ty=ty,st=st,n=('Moved line. ' if moved else '')+note,sp='NFL' if nfl else 'NBA')
  if moved: r['moved']=True
  rows.append(r)
RY,RU,PY='receivingYards','rushingYards','passingYards'
for p in ['Justin Jefferson','Christian Watson','Brock Bowers','Jaxon Smith-Njigba',"Ja'Marr Chase",'Tee Higgins','Drake London','Chris Olave','Trey McBride','CeeDee Lamb','Jakobi Meyers']:
  add(f"{p} 50+ receiving yards",p,RY,50,adj=-8 if p=='Justin Jefferson' else (-4 if p=='Jaxon Smith-Njigba' else 0))
for p in ['Jaylen Warren','Jonathan Taylor','James Cook']: add(f"{p} 50+ rushing yards",p,RU,50)
add("Josh Hart 10+ points",'Josh Hart','pts',10)
add("Jalen Johnson 6+ assists",'Jalen Johnson','ast',6)
add("Keyonte George 3+ rebounds",'Keyonte George','reb',3,adj=-4);add("Keyonte George 4+ rebounds",'Keyonte George','reb',4,adj=-4)
add("Anfernee Simons 3+ rebounds",'Anfernee Simons','reb',3);add("Anfernee Simons 4+ rebounds",'Anfernee Simons','reb',4)
add("Pascal Siakam 15+ points",'Pascal Siakam','pts',15);add("Pascal Siakam 20+ points",'Pascal Siakam','pts',20)
for p in ["Ja'Marr Chase",'Christian McCaffrey','Javonte Williams','Kyren Williams','Jaxon Smith-Njigba','Bijan Robinson']:
  add(f"{p} anytime touchdown",p,'td',1,cap=62,ty='prop',adj=-12 if p=='Jaxon Smith-Njigba' else -8)
add("Aaron Rodgers 200+ passing yards",'Aaron Rodgers',PY,200)
add("Joe Burrow 275+ passing yards",'Joe Burrow',PY,275);add("Joe Burrow over 290 passing yards",'Joe Burrow',PY,291,st='reg')
add("Tee Higgins 60+ receiving yards",'Tee Higgins',RY,60)
add("Patrick Mahomes 175+ passing yards",'Patrick Mahomes',PY,175);add("Michael Penix Jr. 175+ passing yards",'Michael Penix Jr.',PY,175)
add("Drake London 40+ receiving yards",'Drake London',RY,40)
add("Trevor Lawrence 200+ passing yards",'Trevor Lawrence',PY,200,adj=-3);add("Trevor Lawrence 250+ passing yards",'Trevor Lawrence',PY,250,adj=-3)
add("Cam Ward 200+ passing yards",'Cam Ward',PY,200,adj=3)
add("Aaron Jones 20+ rushing yards",'Aaron Jones',RU,20)
add("Tucker Kraft 30+ receiving yards",'Tucker Kraft',RY,30)
add("CeeDee Lamb over 90 receiving yards",'CeeDee Lamb',RY,91,st='reg')
add("Justin Jefferson over 80 receiving yards",'Justin Jefferson',RY,81,st='reg',adj=-8)
add("Bijan Robinson over 80 rushing yards",'Bijan Robinson',RU,81,st='reg')
add("Myles Price over 10 receiving yards",'Myles Price',RY,11,st='reg');add("Myles Price 25+ receiving yards",'Myles Price',RY,25);add("Myles Price 40+ receiving yards",'Myles Price',RY,40);add("Myles Price 60+ receiving yards",'Myles Price',RY,60)
add("Xavier Hutchinson over 30 receiving yards",'Xavier Hutchinson',RY,31,st='reg',adj=5);add("Xavier Hutchinson 50+ receiving yards",'Xavier Hutchinson',RY,50,adj=5);add("Xavier Hutchinson 80+ receiving yards",'Xavier Hutchinson',RY,80,adj=3)
add("Jaylen Brown over 0.5 threes",'Jaylen Brown','3pm',1,st='reg');add("Jaylen Brown over 1.5 threes",'Jaylen Brown','3pm',2,st='reg')
add("Anthony Gould over 0.5 receptions",'Anthony Gould','receptions',1,st='reg');add("Anthony Gould over 1.5 receptions",'Anthony Gould','receptions',2,st='reg');add("Anthony Gould 3+ receptions",'Anthony Gould','receptions',3);add("Anthony Gould 4+ receptions",'Anthony Gould','receptions',4)
add("Jaylen Warren over 90 rushing + receiving yards",'Jaylen Warren','rr',91,st='reg')
add("Jadarian Price 10+ receiving yards",'Jadarian Price',RY,10)
add("Brock Purdy over 19.5 rushing yards",'Brock Purdy',RU,20,st='reg');add("Brock Purdy 20+ rushing yards",'Brock Purdy',RU,20)
add("Breece Hall over 15 receiving yards",'Breece Hall',RY,16,st='reg',cap=70)
add("Joe Burrow over 6.5 rushing yards",'Joe Burrow',RU,7,st='reg')
add("Seth McGowan over 24.5 rushing yards",'Seth McGowan',RU,25,st='reg')
add("Tommy Tremble over 10 receiving yards",'Tommy Tremble',RY,11,st='reg')
add("Keenan Allen over 20 receiving yards",'Keenan Allen',RY,21,st='reg',adj=3)
add("Geno Smith 30+ passing attempts",'Geno Smith','passingAttempts',30,adj=3)
add("Emmett Johnson over 70 rushing yards",'Emmett Johnson',RU,71,st='reg',adj=18,cap=45)
add("Jonathan Taylor over 70 rushing yards",'Jonathan Taylor',RU,71,st='reg')
add("Chris Rodriguez Jr. over 30 rushing yards",'Chris Rodriguez Jr.',RU,31,st='reg',adj=3)
add("Deshaun Watson under 25 rushing yards",'Deshaun Watson',RU,25,under=True);add("Deshaun Watson under 30 rushing yards",'Deshaun Watson',RU,30,under=True)
add("Mike Washington under 30 rushing yards",'Mike Washington',RU,30,under=True)
add("Tucker Kraft under 5 receptions",'Tucker Kraft','receptions',5,under=True)
add("Josh Allen under 0.5 interceptions",'Josh Allen','interceptions',1,under=True,st='reg')
add("Jaylen Warren over 60 rushing yards",'Jaylen Warren',RU,61,st='reg')
add("Chase Brown over 45 rushing yards",'Chase Brown',RU,46,st='reg');add("Chase Brown 40+ rushing yards",'Chase Brown',RU,40)
# moved lines
MV=[("Christian Watson 40+ receiving yards",'Christian Watson',RY,40,0),("Brock Bowers 60+ receiving yards",'Brock Bowers',RY,60,0),("Jaxon Smith-Njigba 70+ receiving yards",'Jaxon Smith-Njigba',RY,70,-4),
 ("Chris Olave 40+ receiving yards",'Chris Olave',RY,40,0),("Trey McBride 40+ receiving yards",'Trey McBride',RY,40,0),("James Cook 70+ rushing yards",'James Cook',RU,70,0),("Bijan Robinson 50+ rushing yards",'Bijan Robinson',RU,50,0),("Bijan Robinson 60+ rushing yards",'Bijan Robinson',RU,60,0),
 ("Jaylen Warren 40+ rushing yards",'Jaylen Warren',RU,40,0),("Joe Burrow 225+ passing yards",'Joe Burrow',PY,225,0),("Joe Burrow 250+ passing yards",'Joe Burrow',PY,250,0),("Patrick Mahomes 200+ passing yards",'Patrick Mahomes',PY,200,0),("Brock Purdy 200+ passing yards",'Brock Purdy',PY,200,0),
 ("Josh Allen 200+ passing yards",'Josh Allen',PY,200,0),("Christian McCaffrey 40+ rushing yards",'Christian McCaffrey',RU,40,0),("Kyren Williams 40+ rushing yards",'Kyren Williams',RU,40,0),("Tee Higgins 40+ receiving yards",'Tee Higgins',RY,40,0),("Ja'Marr Chase 40+ receiving yards","Ja'Marr Chase",RY,40,0),
 ("Jalen Johnson 6+ rebounds",'Jalen Johnson','reb',6,0),("Jalen Johnson 10+ points",'Jalen Johnson','pts',10,0),("Jalen Johnson 15+ points",'Jalen Johnson','pts',15,0),("Jaylen Brown 15+ points",'Jaylen Brown','pts',15,0),("Josh Hart 4+ rebounds",'Josh Hart','reb',4,0),("Keyonte George 15+ points",'Keyonte George','pts',15,-4),("Keyonte George 4+ assists",'Keyonte George','ast',4,-4)]
for t,p,s,k,a in MV: add(t,p,s,k,moved=True,adj=a)
add("Emmett Johnson 30+ rushing yards",'Emmett Johnson',RU,30,moved=True,adj=35,cap=70);add("Emmett Johnson 50+ rushing yards",'Emmett Johnson',RU,50,moved=True,adj=30,cap=55)
def M(p,pct,g,t,ty,n,st='reg',fl=None):
  r=dict(p=p,pct=pct,g=g,t=t,ty=ty,st=st,n=n,sp='NFL')
  if fl: r['fl']=fl
  rows.append(r)
M("Green Bay Packers ML v Vikings",58,'MIN@GB','10:00','ml','Packers -2.5 at home. Vikings are on a backup QB, but Jacobs is out for Green Bay. Both sides of this game were sent. Packers are the side.')
M("Minnesota Vikings ML v Packers",42,'MIN@GB','10:00','ml','Vikings +2.5 with Kyler Murray out. Both sides were sent. Packers are the side.')
M("Houston Texans ML v Browns",63,'HOU@CLE','10:00','ml','Texans -4.5 on the road. Harrison Jr. and Montgomery are out. Both sides were sent. Texans are the side.')
M("Cleveland Browns ML v Texans",37,'HOU@CLE','10:00','ml','Browns +4.5 at home. Underdog. Both sides were sent.')
M("Kansas City Chiefs ML v Falcons",59,'KC@ATL','10:00','ml','Chiefs -3 on the road. Walker is out. Both sides were sent. Chiefs are the side.')
M("Kansas City Chiefs -2.5 v Falcons",51,'KC@ATL','10:00','spread','Line is -3, so -2.5 is a coin flip plus a hair.')
M("Atlanta Falcons ML v Chiefs",41,'KC@ATL','10:00','ml','Falcons +3 at home. Underdog. Both sides were sent.')
M("Miami Dolphins ML v Colts",37,'MIA@IND','10:00','ml','Dolphins +4.5 on a backup QB. Total is 37.5. Underdog.')
M("Buffalo Bills ML v Jets",77,'BUF@NYJ','10:00','ml','Bills -8.5 on the road.')
M("Jacksonville Jaguars ML v Titans",81,'JAX@TEN','10:00','ml','Jaguars -10.5 on the road. Biggest favorite on the NFL board.')
M("Seattle Seahawks ML v Raiders",68,'SEA@LV','1:05','ml','Seahawks -6.5, but Darnold is out. The line already has that in it.')
M("Las Vegas Raiders ML v Seahawks",32,'SEA@LV','1:05','ml','Raiders +6.5 at home. Underdog. Both sides were sent. Seahawks are the side.')
M("San Francisco 49ers ML v Cowboys",63,'SF@DAL','1:25','ml','49ers -4.5 on the road. Evans and Aiyuk are out.')
r=dict(p="Kenneth Walker III over 90 rushing yards",pct=0,g='KC@ATL',t='10:00',ty='prop',st='reg',n='OUT (groin). Do not play.',sp='NFL',fl='OUT');rows.append(r)
json.dump(rows,open('sun/sun.json','w'))
for r in sorted(rows,key=lambda r:-r['pct']): print(f"{r['pct']:3d} {('M' if r.get('moved') else r.get('fl','')):3s} {r['p'][:44]:44s} {r['g']:8s} {r['t']:5s} {r['n'][:95]}")
print(len(rows))
