"""Nov 21 grading (Saturday). Same system as Nov 20 (fri20/grade.py) via sat21/grade_base.py.
All 76 capper picks are graded, including games that started before the board (flagged LIVE, never on tickets).
UFC: no fighter model, so the grade is Kalshi's price capped at 69 (reference only)."""
exec(open('sat21/grade_base.py').read())
UN['ra']='reb+ast';WORD['ra']='rebounds + assists'
_vals=vals
def vals(p,st):
  if st=='ra':
    return [f(x,'totalRebounds')+f(x,'assists') for x in L[p]['games']]
  return _vals(p,st)
_matchup=matchup
def matchup(team,st,under):
  return _matchup(team,'reb' if st=='ra' else st,under)
def ev_of(ser,sub):
  for m in K[ser]:
    if EV in m['event_ticker'] and m['yes_sub_title']==sub: return m['event_ticker'].split('-',1)[1]
def kp_game(ser,sub):
  e=ev_of(ser,sub);return (kgame(ser,e,sub) if e else None),e
LIVE=" Game started at 9 AM PT, before this board. Graded for the record and live bettors only, never on a ticket."
def live(i): rows[i]['fl']='LIVE';rows[i]['n']+=LIVE
# NBA props, in the order Ace sent them
A(1,'LaMelo Ball','pts',21,orig='over 20.5 points');A(2,'Domantas Sabonis','ast',5,orig='over 4.5 assists');A(3,'Tyler Herro','reb',4,orig='over 3.5 rebounds')
A(4,'Kris Dunn','ra',6,orig='over 5.5 rebounds + assists');A(5,'Devin Vassell','pts',9,orig='over 8.5 points')
A(6,'LaMelo Ball','pts',20);A(7,'Domantas Sabonis','ast',4);A(8,'Tyler Herro','reb',4)
A(9,'Kris Dunn','reb',2);A(10,'Kris Dunn','reb',4);A(11,'Kris Dunn','ast',2);A(12,'Kris Dunn','ast',4)
def nbaml(no,tm,nick,opn):
  g=G[tm];k=kgame('KXNBAGAME',EV+TK(g['g']),FULL[tm]) if False else None
  for m in K['KXNBAGAME']:
    if EV in m['event_ticker'] and TK(g['g']) in m['event_ticker'] and m['yes_sub_title']==FULL[tm]: k=kmid(m)
  SUB[no]=team(f"{nick} ML v {opn}",100*phi(-g['sp']/12),g['g'],g['t'],'ml','NBA',f"Graded from the betting spread ({nick} {g['sp']:+g})."+kn(k),k=k,cap=88)
nbaml(13,'PHI','76ers','Bucks');nbaml(14,'NY','Knicks','Trail Blazers');nbaml(15,'MIN','Timberwolves','Grizzlies');nbaml(16,'BOS','Celtics','Kings')
# college football props (no Kalshi market, capped at 69)
CF(17,'Noah Fifita','pass',295);CF(18,'Jesse Legree','recyds',112);CF(19,'L.J. Phillips Jr.','rush',102);CF(20,'Carlos Hernandez','recyds',94);CF(21,'Dylan Riley','rush',103)
CF(22,'Noah Fifita','pass',290);CF(23,'Jesse Legree','recyds',110);CF(24,'L.J. Phillips Jr.','rush',100);CF(25,'Carlos Hernandez','recyds',90);CF(26,'Dylan Riley','rush',100)
live(SUB[20]);live(SUB[25])
# college hoops moneylines (spread SD 11, capped 69)
def cbbml(no,txt,g,t,sub,sp,where):
  k,e=kp_game('KXNCAAMBGAME',sub);SUB[no]=team(txt,100*phi(sp/11),g,t,'ml','CBB',f"College hoops. Graded from the betting line, capped under 70. {where}"+kn(k),k=k)
cbbml(27,'Nicholls ML v Southern Miss','USM v NICH','2:00','Nicholls St.',-2.5,'Southern Miss -2.5, neutral site, so Nicholls is a small underdog.')
cbbml(28,'Wofford ML v Winthrop','WIN@WOF','2:00','Wofford',6.5,'Wofford -6.5 at home.')
cbbml(29,'Southern Illinois ML v East Carolina','SIU v ECU','2:30','Southern Illinois',1.5,'Southern Illinois -1.5, neutral site.')
# college football team lines (spread SD 14, total SD 13, capped 69)
def cfml(no,txt,g,t,sub,sp,where,lv=False):
  k,e=kp_game('KXNCAAFGAME',sub);SUB[no]=team(txt,100*phi(sp/14),g,t,'ml','CFB',f"College football. Graded from the betting line, capped under 70. {where}"+kn(k),k=k)
  if lv: live(SUB[no])
  return e
def cfsp(no,txt,g,t,fav_sub,fav_sp,line,dog=False,lv=False):
  e=ev_of('KXNCAAFGAME',fav_sub);c=kcurve('KXNCAAFSPREAD',e or 'x',rf"{re.escape(fav_sub)} wins by over ([\d.]+)") if e else []
  if dog:   # underdog +line: covers unless the favorite wins by more than line
    k,ki=kat(c,line);pct=100*phi((line-fav_sp)/14);k2=None if k is None else 100-k
  else:
    k,ki=kat(c,line+0.5 if line==int(line) else line);pct=100*phi((fav_sp-line)/14);k2=k
  SUB[no]=team(txt,pct,g,t,'spread','CFB',f"College football. Graded from the betting line, capped under 70. Book spread is {fav_sub} -{fav_sp:g}."+kn(k,ki,flip=dog),k=k2)
  if lv: live(SUB[no])
def cftot(no,txt,g,t,anchor_sub,line,book,over,lv=False):
  e=ev_of('KXNCAAFGAME',anchor_sub);c=kcurve('KXNCAAFTOTAL',e or 'x',r'Over ([\d.]+) points') if e else []
  k,ki=kat(c,(line+0.5 if over else line-0.5) if line==int(line) else line)
  z=(book-line)/13 if over else (line-book)/13
  SUB[no]=team(txt,100*phi(z),g,t,'total','CFB',f"College football. Graded from the betting total, capped under 70. Book total is {book}."+kn(k,ki,flip=not over),k=None if k is None else (k if over else 100-k))
  if lv: live(SUB[no])
cfml(30,'Army ML v East Carolina','ECU@ARMY','9:00 AM','Army',4.5,'Army -4.5 at home.',lv=True)
cfml(31,'Ohio State ML at Nebraska','OSU@NEB','9:00 AM','Ohio St.',3.5,'Ohio State -3.5 on the road.',lv=True)
cfsp(32,'West Virginia +8.5 v Houston','HOU@WVU','10:00 AM','Houston',7,8.5,dog=True)
cfsp(33,'UAB +7.5 v UTSA','UTSA@UAB','5:00','UTSA',4.5,7.5,dog=True)
cfml(34,'Oklahoma ML v Texas A&M','TA&M@OU','12:45','Oklahoma',7,'Oklahoma -7 at home.')
cfsp(35,'Oklahoma -7.5 v Texas A&M','TA&M@OU','12:45','Oklahoma',7,7.5);cfsp(36,'Oklahoma -3 v Texas A&M','TA&M@OU','12:45','Oklahoma',7,3)
cfml(37,'Houston ML at West Virginia','HOU@WVU','10:00 AM','Houston',7,'Houston -7 on the road.')
cfml(38,'Indiana ML at Washington','IU@WASH','12:30','Indiana',9.5,'Indiana -9.5 on the road.')
cfml(39,'UCLA ML at Michigan','UCLA@MICH','12:30','UCLA',3.5,'UCLA -3.5 on the road.')
cfml(40,'Oklahoma State ML at Arizona State','OKST@ASU','7:15','Oklahoma St.',2.5,'Oklahoma State -2.5 on the road.')
cftot(41,'Ohio State at Nebraska under 45 total points','OSU@NEB','9:00 AM','Ohio St.',45,42.5,False,lv=True)
cftot(42,'Northwestern at Minnesota under 45 total points','NU@MINN','9:00 AM','Northwestern',45,41.5,False,lv=True)
cftot(43,'Iowa at Illinois under 45 total points','IOWA@ILL','11:30 AM','Iowa',45,40.5,False)
cftot(44,'Wisconsin at Purdue under 50 total points','WIS@PUR','9:00 AM','Wisconsin',50,46.5,False,lv=True)
cftot(45,'UCLA at Michigan under 45 total points','UCLA@MICH','12:30','UCLA',45,36.5,False)
cftot(46,'Indiana at Washington under 50 total points','IU@WASH','12:30','Indiana',50,43.5,False)
cftot(47,'Arkansas at Texas under 55 total points','ARK@TEX','12:30','Texas',55,46.5,False)
cftot(48,'Texas A&M at Oklahoma under 45 total points','TA&M@OU','12:45','Oklahoma',45,36.5,False)
cfml(49,'Cincinnati ML v Colorado','COLO@CIN','9:00 AM','Cincinnati',3,'Cincinnati -3 at home.',lv=True)
cftot(50,'Syracuse at Boston College over 50 total points','SYR@BC','9:00 AM','Syracuse',50,52.5,True,lv=True)
SUB[51]=team('Wake Forest -14 at Georgia Tech',None,'WAKE@GT','9:00 AM','spread','CFB','College football. No book line found for this game before kickoff, so no grade.',cap=69);live(SUB[51])
cftot(52,'Vanderbilt at Florida under 50 total points','VAN@FLA','9:00 AM','Florida',50,47.5,False,lv=True)
cfsp(53,'Kansas +7.5 v BYU','BYU@KU','9:00 AM','BYU',4.5,7.5,dog=True,lv=True)
A(54,'Karl-Anthony Towns','reb',14,under=True,orig='under 14 rebounds (13 or fewer)')
A(55,'Anfernee Simons','pts',10);A(56,'Anfernee Simons','ast',2);A(57,'Joel Embiid','reb',8);A(58,'Joel Embiid','reb',6);A(59,'Joel Embiid','ast',2);A(60,'Joel Embiid','ast',4)
A(61,'Cooper Flagg','ast',6);A(62,'Rui Hachimura','reb',4)
# UFC: Kalshi's price is the only number we have, capped at 69 (reference only, never on a ticket)
def ufc(no,txt,sub,lv=False,done=False):
  k=None
  for m in K['KXUFCFIGHT']:
    if EV in m['event_ticker'] and m['yes_sub_title']==sub: k=kmid(m)
  SUB[no]=team(txt,None if k is None else min(k,69),'UFC','today','ml','UFC',"UFC. We have no fighter model, so this shows Kalshi's price capped at 69, for reference only."+kn(k),k=k,cap=69)
  if done: rows[SUB[no]]['fl']='DONE';rows[SUB[no]]['n']+=' Fight finished before the board.'
  elif lv: live(SUB[no])
ufc(63,'Jiri Prochazka ML v Navajo Stirling','Jiri Prochazka');ufc(64,'Kevin Vallejos ML v Aljamain Sterling','Kevin Vallejos');ufc(65,'Dan Hooker ML v Brian Ortega','Daniel Hooker')
ufc(66,'Kyoji Horiguchi ML v Asu Almabayev','Kyoji Horiguchi');ufc(67,'Ikram Aliskerov ML v Jared Cannonier','Ikram Aliskerov')
SUB[68]=team('Ikram Aliskerov wins by decision',None,'UFC','today','prop','UFC','UFC method of victory. No Kalshi market and no fighter model, so no grade.',cap=69)
ufc(69,'Aleksandre Topuria ML v Santiago Luna','Aleksandre Topuria');ufc(70,'Shamil Gaziev ML v Tallison Teixeira','Shamil Gaziev');ufc(71,'Alessandro Costa ML v Amir Albazi','Alessandro Costa',lv=True)
for no,txt in [(72,'Jake Matthews wins by decision v Tahir Abdullayev'),(73,'Jake Matthews ML v Tahir Abdullayev'),(74,'Dom Mar Fan ML v Nikolas Motta'),(75,'Alik Lorenz ML v Diyar Nurgozhay'),(76,'John Mitchell ML v Shoaib Yousaf')]:
  SUB[no]=team(txt,None,'UFC','today','ml','UFC','UFC prelim. Fight finished before the board, graded for the record only.',cap=69,fl='DONE')
# dedupe (same as fri20)
seen={};remap={}
for i,r in enumerate(rows):
  if r['p'] in seen:
    j=seen[r['p']]
    if rows[j].get('moved') and 'Safer' in rows[j]['n'] and not (r.get('moved') and 'Safer' in r['n']): rows[j]=r
    remap[i]=j;continue
  seen[r['p']]=i;remap[i]=i
new=[];pos={}
for i,r in enumerate(rows):
  if remap[i]==i: pos[i]=len(new);new.append(r)
SUB={no:(None if i is None else pos[remap[i]]) for no,i in SUB.items()};rows=new
r=rows[SUB[54]];r['fl']='Q';r['n']+=' Towns is questionable (illness). Check before you play it.'
json.dump({'rows':rows,'sub':SUB},open(D+'sat21.json','w'))
for no in sorted(SUB):
  i=SUB[no];r=rows[i] if i is not None else None
  print(no,'-' if r is None else (r['pct'],'K'+str(r.get('k','-')),r.get('fl',''),'|',r['p']))
print(len(rows),'rows')
for r in rows:
  if r.get('moved') and 'Safer' in r['n']: print('ALT',r['pct'],'K',r.get('k'),r['p'])
