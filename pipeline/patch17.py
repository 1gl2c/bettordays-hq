import re,json
s=open('bettordays-hq.html').read()
W=json.loads(re.search(r'const WED=(\[.*?\]);\n',s).group(1))
R={"Michael Porter Over 21.5 Points":("W","22 pts"),"Draymond Green Over 9.5 Pts + Reb":("W","7 pts 5 reb"),"Alex Sarr Over 6.5 Rebounds":("P",""),"Jeremiah Fears Over 4.5 Assists":("W","5 ast"),
"Karl-Anthony Towns Under 3.5 Assists":("L","8 ast"),"Cameron Boozer over 9 rebounds":("W","11 reb"),"Cameron Boozer over 8 rebounds":("W","11 reb"),"Micheal Porter over 20 points":("W","22 pts"),
"Julius Randle over 4 assists":("W","5 ast"),"Julius Randle over 5 assists":("W","5 ast"),"Jeremiah Fears over 4 assists":("W","5 ast"),"Jeremiah Fears over 5 assists":("W","5 ast"),
"De’Aaron Fox under 7 assists":("L","9 ast"),"De’Aaron fox under 8 assists":("L","9 ast"),"Andre Drummond under 5 points":("W","0 pts"),"Karl Anthony Towns under 4 assists":("L","8 ast"),"Karl Anthony Towns under 5 assists":("L","8 ast"),
"Jayson Tatum 20+ points":("W","24 pts"),"Neemias Queta 4+ rebounds":("W","13 reb"),"Evan Mobley over 10 points":("W","10 pts"),"Evan Mobley over 15 points":("L","10 pts"),"Og Annuouby over 4 rebounds":("W","6 reb"),
"Anthony Davis over 15 points":("W","15+ per Kalshi"),"Alex Sarr over 4 rebounds":("W","4+ per Kalshi"),"Walker Kessler over 10 points":("W","10 pts"),"Walker Kessler over 10 rebounds":("W","11 reb"),"Walker Kessler over 8 rebounds":("W","11 reb"),"Walker Kessler over 6 rebounds":("W","11 reb"),
"Brayden Burries over 0.5 3 pointers made":("W","1 three"),"Zion Williamson 15+ points":("W","29 pts"),"Julius Randle 15+ points":("W","17 pts"),"Nikola Jokic double double":("W","DD per Kalshi"),
"Caleb Wilson 20+ PRA":("W","15/5/0 = 20"),"Stepon Castle 20+ PRA":("L","11/1/3 = 15"),"Desmond Bane 2 + 3 pointers made":("W","7 threes"),"Franz Wagner over 15 points":("W","38 pts"),"Franz Wagner over 20 points":("W","38 pts"),
"Alperen Senguun over 15 points":("W","19 pts"),"Yaxel LEnderborg 20+ PRA":("W","25/10/0 = 35"),"Shai Gilgeous Alexander 25+ points":("W","25+ per Kalshi"),"Isaiah Hartenstein over 8 rebounds":("W","11 reb"),
"Payton Pritchard over 20+ PRA":("L","14/1/1 = 16"),"Zion Williamson over 20+ points":("W","29 pts"),"Stephen Castle 4+ rebounds":("L","1 reb"),"Stephon Castle 4+ rebounds":("L","1 reb"),"Buffalo ML v Ball State":("W","BUF 28-7"),
"Sacramento State +20 v Central Michigan":("L","CMU 28-7, by 21"),"Ivica Zubac over 9.5 Rebs":("W","12 reb"),"Cedric Coward over 1.5 3PM":("L","1 three"),"Isaiah Hartenstein over 3.5 Asts":("W","6 ast"),
"Jalen Brunson 20+ points":("W","27 pts"),"Donovan Mitchell 20+ points":("W","23 pts"),"Jalen Brunson 6+ assists":("L","5 ast"),"Karl Anthony Towns 15+ points":("W","21 pts, played"),
"Ja’Kobe Walter o12.5 PTS":("W","17 pts"),"Cameron Boozer o4.5 AST":("W","5 ast"),"Quenton Jackson o2.5 REB":("L","2 reb"),"Mikal Bridges o2.5 REB":("L","1 reb"),"Zion Williamson o14.5 PTS":("W","29 pts"),
"Yaxel Lendeborg o22.5 Points + Assists":("W","25 + 0"),"Walker Kessler o24.5 Points + Rebounds":("L","10 + 11 = 21"),"Ziaire Williams o1.5 Threes Made":("L","1 three"),"Dylan Harper o17.5 Points":("W","18 pts"),
"Kyshawn George o19.5 Points + Assists":("W","25 + 3"),"Tampa Bay Lightning ML":("W","TB 8-3"),"NY Rangers ML v Flames":("W","NYR 3-1"),"Jaylon Tyson o7.5 Points (-105)":("L","3 pts"),"Jaylon Tyson 10+ Points (+180)":("L","3 pts"),"Jaylon Tyson 15+ Points":("L","3 pts"),
"Boston Celtics ML":("W","BOS 98-93"),"Houston Rockets ML":("W","HOU 115-108"),"LA Lakers ML":("W","LAL 123-112"),"SA Spurs ML":("W","SAS 124-119"),"WAS Wizards ML":("L","IND 114-101"),"Jalen Brunson 25+":("W","27 pts"),"NY KNicks ML":("L","CLE 115-107"),
"MPJ 15+ pts":("W","22 pts"),"Sarr 4+ reb":("W","4+"),"Boozer 7+ reb":("W","11 reb"),"Fears 3+ ast":("W","5 ast"),"Randle 3+ ast":("W","5 ast"),"SGA 20+ pts":("W","25+"),"Hartenstein 6+ reb":("W","11 reb"),"Coward 1+ three":("W","1 three"),
"Brunson 4+ ast":("W","5 ast"),"Walter 8+ pts":("W","17 pts"),"Boozer 3+ ast":("W","5 ast"),"Lendeborg 18+ P+A":("W","25"),"Kessler 15+ P+R":("W","21"),"Ziaire 1+ three":("W","1 three"),"Harper 12+ pts":("W","18 pts"),"George 14+ P+A":("W","28"),
"Lendeborg 25+ PRA":("W","35"),"Boozer 6+ reb":("W","11 reb"),"Bridges 2+ reb":("L","1 reb"),"Lendeborg 30+ PRA":("W","35"),
"Coco to win a set":("P",""),"Sabalenka to win a set":("P",""),"Sabalenka ML":("P",""),"Nolan Traore over 10.5 Pts":("P","")}
miss=[x['p'] for x in W if x['p'] not in R and x['pct']>0]
print('ungraded:',miss)
for x in W:
  r=R.get(x['p'])
  if not r: continue
  x.pop('r',None)
  if r[0] in 'WL': x['r']=r[0]
  if r[1]: x['n']=(x['n']+' ' if x['n'] else '')+f'<b style="color:#cfe">Final: {r[1]}</b>'
  if r[0]=='P': x['n']+=' <i style="color:#ffb020">Result pending</i>'
g=[x for x in W if x.get('r')]; t70=[x for x in g if x['pct']>=70]
print('graded',len(g),sum(x['r']=='W' for x in g),'70+',sum(x['r']=='W' for x in t70),len(t70),[x['p'] for x in t70 if x['r']=='L'])
mv=[x for x in g if x.get('moved')];print('moved',sum(x['r']=='W' for x in mv),len(mv))
b=[x for x in g if 45<=x['pct']<60];print('45-59',sum(x['r']=='W' for x in b),len(b))
s=re.sub(r'const WED=\[.*?\];\n',lambda m:'const WED='+json.dumps(W)+';\n',s,count=1,flags=re.S)
L=lambda *a:list(a)
T=[
 dict(t="Hammer · model · PLAYED",c="#04ff9f",res="W",legs=L("Nikola Jokic double double","Houston Rockets ML","Alperen Senguun over 15 points","LA Lakers ML","Franz Wagner over 15 points"),hit="About 40%",stake="$139.96",lock="Paid 2.55x ($357.59)",v="5 for 5. Franz 38, Sengun 19, Jokic double-double, Lakers and Rockets both won."),
 dict(t="2x · model · PLAYED",c="#00c8ff",res="W",legs=L("SA Spurs ML","Lendeborg 25+ PRA","MPJ 15+ pts","Jalen Brunson 20+ points","Anthony Davis over 15 points"),hit="About 39%",stake="$119.98",lock="Paid 2.30x ($275.79)",v="5 for 5. Lendeborg 35 PRA, Brunson 27, MPJ 22."),
 dict(t="5-10x · model · PLAYED",c="#ffb020",res="L",legs=L("Boston Celtics ML","Jayson Tatum 20+ points","Evan Mobley over 15 points","Boozer 6+ reb","Walker Kessler over 8 rebounds"),hit="About 1 in 5",stake="$99.99",lock="Would have paid 4.04x",v="4 of 5. Mobley scored 10 on 8 shots. The 62% leg was the one that missed."),
 dict(t="3-leg · Ace build · PLAYED",c="#04ff9f",res="W",legs=L("Houston Rockets ML","Lendeborg 25+ PRA","Alperen Senguun over 15 points"),hit="About 45%",stake="$260.04",lock="Paid 2.76x ($718.65)",v="The night's best ticket. Three 74-82 legs where Kalshi priced lower than us. Biggest stake of the day, biggest win."),
 dict(t="7-leg · Ace build · PLAYED",c="#04ff9f",res="W",legs=L("Houston Rockets ML","Alperen Senguun over 15 points","LA Lakers ML","Walker Kessler over 8 rebounds","SA Spurs ML","Anthony Davis over 15 points","Franz Wagner over 20 points"),hit="About 1 in 4",stake="$30.00",lock="Paid 3.82x ($114.46)",v="7 for 7. All legs from the 70%+ list plus Franz 20+ at 66."),
 dict(t="Lotto 13 · model · PLAYED",c="#ff4d5e",res="L",legs=L("Coward 1+ three","Brayden Burries over 0.5 3 pointers made","Boston Celtics ML","Payton Pritchard over 20+ PRA","Neemias Queta 4+ rebounds","Donovan Mitchell 20+ points","Bridges 2+ reb","Julius Randle 15+ points","Zion Williamson 15+ points","Shai Gilgeous Alexander 25+ points","Hartenstein 6+ reb","Alex Sarr over 4 rebounds","Stephon Castle 4+ rebounds"),hit="About 1 in 25",stake="$53.52",lock="Would have paid 14.4x",v="10 of 13. Bridges (1 reb), Castle (1 reb), Pritchard (16 PRA)."),
 dict(t="Lotto 14 · model · PLAYED",c="#c77dff",res="L",legs=L("Coward 1+ three","Brayden Burries over 0.5 3 pointers made","Desmond Bane 2 + 3 pointers made","Franz Wagner over 20 points","Payton Pritchard over 20+ PRA","Neemias Queta 4+ rebounds","Donovan Mitchell 20+ points","Bridges 2+ reb","Julius Randle 15+ points","Zion Williamson 15+ points","Shai Gilgeous Alexander 25+ points","Hartenstein 6+ reb","Alex Sarr over 4 rebounds","Stephon Castle 4+ rebounds"),hit="About 1 in 40",stake="$49.97",lock="Would have paid 14.4x",v="11 of 14. Same three misses."),
 dict(t="12-leg · Ace build · PLAYED",c="#c77dff",res="L",legs=L("Nikola Jokic double double","Cameron Boozer over 8 rebounds","Jeremiah Fears over 4 assists","MPJ 15+ pts","Zion Williamson 15+ points","SA Spurs ML","Jayson Tatum 20+ points","Donovan Mitchell 20+ points","Evan Mobley over 10 points","Jalen Brunson 20+ points","Bridges 2+ reb","Shai Gilgeous Alexander 25+ points"),hit="About 1 in 12",stake="$9.99",lock="Would have paid 12.5x",v="11 of 12. Mikal Bridges 2+ rebounds again."),
]
P={x['p'] for x in W}
for t in T:
  for l in t['legs']: assert l in P,l
s=re.sub(r'const WTIX=\[.*?\];\n',lambda m:'const WTIX='+json.dumps(T)+';\n',s,count=1,flags=re.S)
# wed ticket renderer: show result labels
s=s.replace("${k?` <span class=\"res ${k==='W'?'w':'l'}\">${k==='W'?'CASHED':'MISSED'}</span>`:''}","${k?` <span class=\"res ${k==='W'?'w':'l'}\">${k==='W'?'CASHED':'MISSED'}</span>`:''}")
s=s.replace("<div class=\"row\"><span>Hit chance</span><b>${t.hit}</b></div><div class=\"row\"><span>Stake</span><b>${t.stake}</b></div><div class=\"row\"><span>Lock at</span><b>${t.lock}</b></div>","<div class=\"row\"><span>Stake</span><b>${t.stake}</b></div><div class=\"row\"><span>Result</span><b>${t.lock}</b></div>")
s=s.replace("const pl=t.t.includes('PLAYED'),k=t.res;return `<div class=\"st\"${pl?' style=\"border-color:var(--acc);box-shadow:0 0 22px rgba(4,255,159,.22)\"':''}>","const pl=t.t.includes('PLAYED'),k=t.res;return `<div class=\"st\"${k==='W'?' style=\"border-color:var(--acc);box-shadow:0 0 22px rgba(4,255,159,.22)\"':''}>")
s=s.replace('<h3>Wednesday tickets · 5 placed · $463.42 in · max $2,531</h3>','<h3>Wednesday tickets · 8 placed · 4 cashed · +$703.04 on the day</h3>')
s=s.replace('<h2>Wednesday board · Nov 11 <small>82 capper picks + 16 moved lines · 10 NBA games, WTA Finals, MACtion, NHL</small></h2>','<h2>Wednesday board · Nov 11 <small>FINAL · moved lines went 20 of 21 · 70%+ legs __W70__</small></h2>')
s=s.replace('__W70__',f"{sum(x['r']=='W' for x in t70)} of {len(t70)}")
# ROWS
def stat(p):
  p=p.lower()
  for k,v in [('three','3pm'),('3pm','3pm'),('3 point','3pm'),('assist','ast'),(' ast','ast'),('asts','ast'),('reb','reb'),('pra','pra'),('p+a','pa'),('p+r','pr'),('double','dd'),('point','pts'),('pts','pts')]:
    if k in p: return v
  return 'ml' if ' ml' in p else 'other'
STARS=['tatum','brunson','towns','gilgeous','sga','jokic','mitchell','davis','zion','franz','sengun','senguun','fox','mobley']
new=[]
for x in g:
  p=x['p'];pl=p.lower()
  mkt='ml' if ' ml' in pl else 'spread' if re.search(r'[+-]\d+',p) and 'v ' in pl else 'prop'
  new.append({"day":"Nov 11","pick":p,"est":x['pct'],"hit":1 if x['r']=='W' else 0,"sport":x['sp'],"mkt":mkt,"stat":stat(p),"dir":"u" if 'under' in pl else 'o',"style":x['st'],"boost":0,"star":1 if any(k in pl for k in STARS) else 0,"fav":0})
RW=json.loads(re.search(r'const ROWS=(\[.*?\]);\n',s).group(1))
RW=[r for r in RW if r['day']!='Nov 11']+new
s=re.sub(r'const ROWS=\[.*?\];\n',lambda m:'const ROWS='+json.dumps(RW)+';\n',s,count=1,flags=re.S)
s=s.replace("['Nov 10','Nov 10']];","['Nov 10','Nov 10'],['Nov 11','Nov 11']];")
h70=sum(r['hit'] for r in RW if r['est']>=70); n70=sum(1 for r in RW if r['est']>=70); hit=sum(r['hit'] for r in RW); n=len(RW); p70=round(100*h70/n70)
print('ROWS',n,hit,round(100*hit/n),'70+',h70,n70,p70)
json.dump(dict(h70=h70,n70=n70,p70=p70,n=n,hit=hit),open('study/cum11.json','w'))
s=s.replace("const DAYS=[\n","""const DAYS=[
 {d:'Wed Nov 11 · 10 NBA games, NHL, MACtion',pl:'+$703',tix:[
  ['3-leg Ace build (Kalshi)','$260.04','2.76x','W','Rockets ML, Lendeborg 25+ PRA, Sengun 15+. Paid $718.65'],
  ['Hammer 5-leg (Kalshi)','$139.96','2.55x','W','5 for 5. Paid $357.59'],
  ['2x 5-leg (Kalshi)','$119.98','2.30x','W','5 for 5. Paid $275.79'],
  ['7-leg Ace build (Kalshi)','$30','3.82x','W','7 for 7. Paid $114.46'],
  ['5-10x (Kalshi)','$99.99','4.04x','L','Mobley 15+ (10 pts) the only miss'],
  ['Lotto 13 (Kalshi)','$53.52','14.4x','L','Bridges, Castle rebounds and Pritchard PRA'],
  ['Lotto 14 (Kalshi)','$49.97','14.4x','L','Same three'],
  ['12-leg Ace build (Kalshi)','$9.99','12.5x','L','Bridges 2+ rebounds (1)'],
 ]},
""",1)
s=s.replace('<span data-count="9">0</span>-6</b><small>hammers and main parlays, Nov 4 to 10</small>','<span data-count="13">0</span>-7</b><small>hammers and main parlays, Nov 4 to 11</small>')
s=s.replace('+$<span data-count="2448">0</span></b><small>Tuesday added +$241 on main tickets</small>','+$<span data-count="3265">0</span></b><small>Wednesday added +$817 on main tickets</small>')
s=re.sub(r'<span data-count="\d+">0</span>/\d+</b><small>\d+% across 7 days · Tuesday 19 of 21</small>',f'<span data-count="{h70}">0</span>/{n70}</b><small>{p70}% across 8 days · Wednesday __W70__</small>'.replace('__W70__',f"{sum(x['r']=='W' for x in t70)} of {len(t70)}"),s)
s=re.sub(r'<span data-count="\d+">0</span>%</b><small>\d+ graded legs, all tiers</small>',f'<span data-count="{round(100*hit/n)}">0</span>%</b><small>{n} graded legs, all tiers</small>',s)
s=s.replace('<span data-count="0">0</span>/16</b>','<span data-count="0">0</span>/19</b>')
s=re.sub(r'Picture a jar of 100 marbles\. \d+ are green, \d+ are red\.',f'Picture a jar of 100 marbles. {p70} are green, {100-p70} are red.',s)
open('bettordays-hq.html','w').write(s)
