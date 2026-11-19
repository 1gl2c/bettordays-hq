import json,re
p='bettordays-hq.html';s=open(p).read()
SUN=json.load(open('sun/sun.json'))
SUTIX=[
 {"t":"Power 3 · the core","c":"#04ff9f","legs":["James Cook 70+ rushing yards","Brock Bowers 50+ receiving yards","Christian Watson 40+ receiving yards"],"stake":"10% of bankroll","lock":"About 2.5x, take 2.0x or better","v":"Three players who have cleared these numbers almost every week. Cook has 70+ in 7 of 8 and Buffalo is favored by 8.5. Bowers has 50+ in all 7 games. Watson has 40+ in all 9 and Jacobs is out, so Green Bay throws. Three different games.","hit":"About 50-55%"},
 {"t":"Hammer · 4 legs","c":"#00c8ff","legs":["Bijan Robinson 50+ rushing yards","Chris Olave 40+ receiving yards","Jacksonville Jaguars ML v Titans","Pascal Siakam 15+ points"],"stake":"8% of bankroll","lock":"About 2.1x, take 2.0x or better","v":"Bijan has 50+ in all 9 games, low of 61. Olave has 40+ in all 8. Jaguars are the biggest favorite on the board. Siakam has 15+ in 11 of 12 and Haliburton is out. All four start at 10:00 AM PT.","hit":"About 45-50%"},
 {"t":"2-3x · value","c":"#ffb020","legs":["Jaxon Smith-Njigba 50+ receiving yards","Buffalo Bills ML v Jets","Trey McBride 40+ receiving yards"],"stake":"5% of bankroll","lock":"About 2.2x, take 2.0x or better","v":"Smith-Njigba has 50+ in all 9 games, but Darnold is out, so that risk is real. Bills are -8.5. McBride has 40+ in 8 of 9 and Arizona will be throwing from behind.","hit":"About 45%"},
 {"t":"5x · yardage stretch","c":"#ff4d5e","legs":["Brock Bowers 60+ receiving yards","Jaxon Smith-Njigba 70+ receiving yards","James Cook 50+ rushing yards","Christian Watson 50+ receiving yards"],"stake":"3% of bankroll","lock":"About 4.5x, take 4.0x or better","v":"The same four players at higher numbers where Kalshi pays more. Bowers 60+ in 7 of 7. Smith-Njigba 70+ in 8 of 9. Watson 50+ in 7 of 9. Every leg can miss, so keep it small.","hit":"About 1 in 4"},
]
ps={x['p'] for x in SUN}
for t in SUTIX:
  for l in t['legs']: assert l in ps,l
o="const CUR=SAT,CTIX=STIX,CURD='2026-11-14';";assert o in s
s=s.replace(o,'const SUN='+json.dumps(SUN)+';\nconst SUTIX='+json.dumps(SUTIX)+";\nconst CUR=SUN,CTIX=SUTIX,CURD='2026-11-15';")
o="const CURCUT=14*60+15;";assert o in s;s=s.replace(o,"const CURCUT=8*60+24;")
b=s.index("document.getElementById('thuTix').innerHTML=CTIX.map(");a=s.rindex("(function(){const rb=x=>x.r?",0,b);c=s.index('\n',b)+1
blk=s[a:c];assert 'CUR' in blk
sat=blk.replace('CURD',"'2026-11-14'").replace('CTIX','STIX').replace('CUR','SAT').replace("'thu","'sah")
s=s[:c]+sat+s[c:]
sec='''
  <section class="panel" id="sathist">
    <h2>Saturday board · Nov 14 <small>FINAL · 70%+ legs 22 of 24 · whole board 39 of 60</small></h2>
    <h3>Saturday tickets</h3>
    <div class="struct" id="sahTix"></div>
    <div class="two" style="margin-top:18px">
      <div><h3>Top 25: any line</h3><ol class="tueo" id="sahAny" style="margin:8px 0 0;padding-left:22px;font-size:12.5px;line-height:1.75"></ol></div>
      <div><h3>Top 25: regular lines</h3><ol class="tueo" id="sahReg" style="margin:8px 0 0;padding-left:22px;font-size:12.5px;line-height:1.75"></ol></div>
    </div>
    <details class="notes" style="margin-top:12px"><summary class="lbl" style="cursor:pointer">Clean 70 pool</summary><div class="chips" id="sahPool"></div></details>
    <div class="filters" id="sahF" style="margin-top:16px"></div>
    <div class="scroll boardwrap" style="max-height:620px;overflow-y:auto"><table id="sahT" class="board"></table></div>
  </section>
'''
o='\n  <section class="panel" id="frihist">';assert o in s
s=s.replace(o,sec+o,1)
o="review11:'history',frihist:'history',";assert o in s
s=s.replace(o,"review11:'history',sathist:'history',frihist:'history',")
o="const BOARD={d:CURD,rows:CUR,label:'Saturday · Nov 14'};";assert o in s
s=s.replace(o,"const BOARD={d:CURD,rows:CUR,label:'Sunday · Nov 15'};")
o='<h2 class="big" id="dayTitle">Saturday · Nov 14</h2>';assert o in s
s=s.replace(o,'<h2 class="big" id="dayTitle">Sunday · Nov 15</h2>')
o='Saturday graded · 22 of 24 at 70%+ · Sunday board next';assert o in s
s=s.replace(o,'Sunday Nov 15 picks are live · NFL Week 10 and NBA')
o="[typeof SAT!=='undefined'&&SAT,";assert o in s
s=s.replace(o,"[typeof SUN!=='undefined'&&SUN,typeof SAT!=='undefined'&&SAT,")
a=s.index('<section class="panel" id="thursday">');b=s.index('</section>',a);secx=s[a:b]
i=secx.index('<details class="notes"');j=secx.index('</details>',i)+10
new='''<details class="notes" style="margin-top:16px"><summary class="lbl" style="cursor:pointer">Injury and matchup notes</summary><div class="flags" style="margin-top:10px">
      <div class="flag"><b>Backup quarterbacks</b><div class="r bad">3 teams</div><p>Vikings (Kyler Murray out), Seahawks (Darnold out) and Dolphins are all on backups. Jefferson and Myles Price are marked down. Smith-Njigba is trimmed a little, he has 50+ in all 9 games.</p><div class="who">Fade Vikings pass catchers</div></div>
      <div class="flag"><b>Out today</b><div class="r bad">checked 8:35 AM</div><p>Kenneth Walker (do not play his line), Josh Jacobs, Marvin Harrison Jr., David Montgomery, Hockenson, Jauan Jennings, Mike Evans, Aiyuk, Jake Ferguson, Carnell Tate. NBA: Embiid, Haliburton, Markkanen, Jaren Jackson Jr., Scottie Barnes.</p><div class="who">Questionable: Garrett Wilson, Addison, Travis Etienne</div></div>
      <div class="flag w"><b>Emmett Johnson</b><div class="r warn">role is a guess</div><p>He should start with Walker out, but his season high is 34 rushing yards. Over 70 is a long shot. If you want him, 30+ is the number.</p><div class="who">Off the tickets</div></div>
      <div class="flag w"><b>Blowout watch</b><div class="r warn">Model v6</div><p>Spurs -16.5 at Utah and Celtics -13.5. No Keyonte George legs on the tickets. In the NFL a big favorite helps its running back and hurts its quarterback's yards: Jaguars -10.5, Rams -9.5, Bills -8.5.</p><div class="who">Unders are fine, overs are not</div></div>
      <div class="flag w"><b>Both sides sent</b><div class="r warn">3 games</div><p>Packers and Vikings, Texans and Browns, Chiefs and Falcons all came in on both sides. We graded each and marked the side: Packers, Texans, Chiefs. None are strong enough for a main ticket.</p><div class="who">Best moneylines: Jaguars 81, Bills 77</div></div>
      <div class="flag w"><b>Touchdowns</b><div class="r warn">15 of 43</div><p>Our anytime touchdown picks have hit 35% all year. They are capped at 62 and kept off the main tickets.</p><div class="who">Yards over touchdowns</div></div>
    </div></details>'''
secx=secx[:i]+new+secx[j:];s=s[:a]+secx+s[b:]
open(p,'w').write(s);print('ok')
