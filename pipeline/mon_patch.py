import json,re
p='bettordays-hq.html';s=open(p).read()
MN=json.load(open('mon/mon.json'))
kp={r['p']:r.get('k') for r in MN}
def est(legs):
  x=1
  for l in legs: x*=kp[l]/100
  return 0.93/x
TIX=[
 {"t":"Power 3 · the core","c":"#04ff9f","legs":["Wendell Carter Jr. 6+ rebounds","Nikola Jokic 8+ assists","Zion Williamson 20+ points"],"stake":"40% of tonight's money","v":"Three legs where our grade is well above Kalshi's price. Carter has 6+ rebounds in 11 of 12 and Banchero is out. Jokic has 8+ assists in 8 of 11 and Phoenix is on a back-to-back. Zion carries the Pelicans with Murphy, Murray and Mathurin out, against a Warriors team missing Curry, Butler and Porzingis. Three different games.","hit":"About 50-55%"},
 {"t":"Hammer · 4 legs","c":"#00c8ff","legs":["Franz Wagner 4+ rebounds","Jaden McDaniels 10+ points","Michael Porter Jr. 15+ points","Cleveland Cavaliers ML v Bulls"],"stake":"30% of tonight's money","v":"Four different games, no bad matchups, nobody on a back-to-back. Wagner and McDaniels both move up with their stars out (Banchero, Edwards). Porter has 15+ in 10 of 11. Cleveland is home against a 3-9 Bulls team that allows the most points in the league.","hit":"About 45-50%"},
 {"t":"2-3x · value","c":"#ffb020","legs":["Zion Williamson 15+ points","Denver Nuggets ML v Suns","Donovan Mitchell 20+ points","Donovan Clingan 8+ rebounds"],"stake":"20% of tonight's money","v":"Zion at the safer number. Denver is home against a Suns team on the second night of a back-to-back. Mitchell gets the softest defense in the league. Clingan has 8+ rebounds in 10 of 12. Four different games.","hit":"About 40%"},
 {"t":"20x · long shot","c":"#ff4d5e","legs":["Wendell Carter Jr. 6+ rebounds","Nikola Jokic 8+ assists","Jaden McDaniels 15+ points","Franz Wagner 6+ assists","Jayson Tatum 2+ threes","Mark Andrews 3+ receptions","Justin Herbert 175+ passing yards"],"stake":"10% of tonight's money, at most","v":"Seven legs graded 70 or higher where Kalshi's price is at or below ours. A 20x hits about 1 time in 15 to 25 even when every leg is good, so this is the smallest ticket of the night. Tatum is on a back-to-back and the two NFL legs are capped at 75.","hit":"About 1 in 15"},
]
ps={x['p'] for x in MN}
for t in TIX:
  for l in t['legs']: assert l in ps,l
  e=est(t['legs']);t['lock']=f"About {e:.1f}x at Kalshi's prices, take {max(2.0,round(e*0.85,1)):.1f}x or better" if e<10 else f"About {e:.0f}x at Kalshi's prices"
  print(t['t'],round(e,2),[ (l,kp[l],next(r['pct'] for r in MN if r['p']==l)) for l in t['legs']])
o="const CUR=SN15,CTIX=SUTIX,CURD='2026-11-15';";assert o in s
s=s.replace(o,'const MN16='+json.dumps(MN)+';\nconst MNTIX='+json.dumps(TIX)+";\nconst CUR=MN16,CTIX=MNTIX,CURD='2026-11-16';")
m=re.search(r'const CURCUT=[^;]*;',s);s=s.replace(m.group(0),'const CURCUT=15*60+55;')
b=s.index("document.getElementById('thuTix').innerHTML=CTIX.map(");a=s.rindex("(function(){const rb=x=>x.r?",0,b);c=s.index('\n',b)+1
blk=s[a:c];assert 'CUR' in blk
sun=blk.replace('CURD',"'2026-11-15'").replace('CTIX','SUTIX').replace('CUR','SN15').replace("'thu","'suh")
s=s[:c]+sun+s[c:]
sec='''
  <section class="panel" id="sunhist">
    <h2>Sunday board · Nov 15 <small>FINAL · 70%+ legs 35 of 52 · our worst day</small></h2>
    <h3>Sunday tickets</h3>
    <div class="struct" id="suhTix"></div>
    <div class="two" style="margin-top:18px">
      <div><h3>Top 25: any line</h3><ol class="tueo" id="suhAny" style="margin:8px 0 0;padding-left:22px;font-size:12.5px;line-height:1.75"></ol></div>
      <div><h3>Top 25: regular lines</h3><ol class="tueo" id="suhReg" style="margin:8px 0 0;padding-left:22px;font-size:12.5px;line-height:1.75"></ol></div>
    </div>
    <details class="notes" style="margin-top:12px"><summary class="lbl" style="cursor:pointer">Clean 70 pool</summary><div class="chips" id="suhPool"></div></details>
    <div class="filters" id="suhF" style="margin-top:16px"></div>
    <div class="scroll boardwrap" style="max-height:620px;overflow-y:auto"><table id="suhT" class="board"></table></div>
  </section>
'''
o='\n  <section class="panel" id="sathist">';assert o in s
s=s.replace(o,sec+o,1)
o="sathist:'history',";assert s.count(o)==1
s=s.replace(o,"sunhist:'history',sathist:'history',")
o="const BOARD={d:CURD,rows:CUR,label:'Sunday · Nov 15'};";assert o in s
s=s.replace(o,"const BOARD={d:CURD,rows:CUR,label:'Monday · Nov 16'};")
o='<h2 class="big" id="dayTitle">Sunday · Nov 15</h2>';assert o in s
s=s.replace(o,'<h2 class="big" id="dayTitle">Monday · Nov 16</h2>')
o='Sunday graded · 35 of 52 at 70%+ · our worst day · Monday board next';assert o in s
s=s.replace(o,'Monday Nov 16 picks are live · NBA, Monday Night Football, college hoops · Model v7')
o="[typeof SN15!=='undefined'&&SN15,";assert o in s
s=s.replace(o,"[typeof MN16!=='undefined'&&MN16,typeof SN15!=='undefined'&&SN15,")
a=s.index('<section class="panel" id="thursday">');b=s.index('</section>',a);secx=s[a:b]
i=secx.index('<details class="notes"');j=secx.index('</details>',i)+10
new='''<details class="notes" style="margin-top:16px"><summary class="lbl" style="cursor:pointer">Injury and matchup notes</summary><div class="flags" style="margin-top:10px">
      <div class="flag g"><b>Model v7 is live</b><div class="r">new today</div><p>Every pick now shows the matchup (what the opponent allows at that stat and where that ranks) and Kalshi's price. When Kalshi is 15 or more points away from our grade, our grade moves halfway to it. NFL props are capped at 75.</p><div class="who">Built after Sunday</div></div>
      <div class="flag"><b>Out tonight</b><div class="r bad">checked 3:30 PM</div><p>Banchero, Anthony Edwards, DiVincenzo, Curry, Jimmy Butler, Porzingis, Mobley, Ja Morant, Shaedon Sharpe, LeBron James, Trey Murphy, Dejounte Murray, Mathurin, Lamar Jackson, Ladd McConkey. Marcus Smart is suspended.</p><div class="who">Day to day: Embiid, Amen Thompson</div></div>
      <div class="flag w"><b>Back-to-backs</b><div class="r warn">5 teams</div><p>Celtics, 76ers, Rockets, Suns and Wizards all played last night. Their players are marked down a few points and kept off the Power 3 and Hammer.</p><div class="who">Tatum, VanVleet, Sarr, Brooks, Green</div></div>
      <div class="flag w"><b>College basketball</b><div class="r warn">market price only</div><p>We have no team data of our own for these games, so each line is graded at Kalshi's price and capped under 70. They stay off the main tickets.</p><div class="who">No edge claimed</div></div>
      <div class="flag w"><b>Monday Night Football</b><div class="r warn">total 39.5</div><p>Ravens -4.5 with Brissett at quarterback for Lamar Jackson. The Chargers are 0-8 and McConkey is out. A low total means fewer yards for everyone. If the Ravens lead, Henry runs more and Herbert throws more.</p><div class="who">NFL props capped at 75</div></div>
      <div class="flag w"><b>Already started</b><div class="r warn">live</div><p>Iona at UMBC and Prairie View at Ohio State tipped before the board went up. Those lines are marked live and will not count in our record.</p><div class="who">Not graded</div></div>
    </div></details>'''
secx=secx[:i]+new+secx[j:];s=s[:a]+secx+s[b:]
open(p,'w').write(s);print('ok')
t=open('buildsite.py').read();o="DAYK=[('SN15',";assert o in t
open('buildsite.py','w').write(t.replace(o,"DAYK=[('MN16','2026-11-16','Monday Nov 16'),('SN15',"))
