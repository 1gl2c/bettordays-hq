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
