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
