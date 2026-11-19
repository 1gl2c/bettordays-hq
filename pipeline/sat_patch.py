import json,re
p='bettordays-hq.html';s=open(p).read()
SAT=json.load(open('sat/sat.json'))
STIX=[
 {"t":"Power 3 · the core","c":"#04ff9f","legs":["BYU ML v Baylor","Nolan Traore 10+ points","Cade Cunningham 6+ assists"],"stake":"10% of bankroll","lock":"Take 2.0x or better","v":"Three different games, our three best categories: a moneyline, points and assists. Cade has 6+ assists in 10 of 11. Traore has 10+ in 7 of his last 8. If Kalshi shows under 2x, swap Cade 6+ assists for Giannis 25+ points.","hit":"About 51-55%"},
 {"t":"Hammer · 4 legs","c":"#00c8ff","legs":["Giannis Antetokounmpo 20+ points","Penn State ML v Minnesota","Daniss Jenkins 1+ three","Cameron Boozer 4+ assists"],"stake":"8% of bankroll","lock":"About 2.1x, take 2.0x or better","v":"Giannis is 11 of 12 at 20+. Penn State is -12.5 at home. Jenkins has a three in 10 of 11. Boozer runs more offense with Ty Jerome out. None of these come from a blowout game.","hit":"About 45-48%"},
 {"t":"2-3x · value","c":"#ffb020","legs":["Ciryl Gane ML v Hokit","Cade Cunningham 15+ points","P.J. Washington 4+ rebounds"],"stake":"5% of bankroll","lock":"About 2.2x, take 2.0x or better","v":"Gane is the 66% favorite in the main event. Cade is 10 of 11 at 15+. Washington is 11 of 12 at 4+ boards with Lively out.","hit":"About 45%"},
 {"t":"5x · moneyline stretch","c":"#ff4d5e","legs":["Ciryl Gane ML v Hokit","LSU ML v Texas","Uros Medic ML v Holland","BYU ML v Baylor"],"stake":"3% of bankroll","lock":"About 5x, take 4.5x or better","v":"Four favorites, no props. Two UFC, two college football. Every leg is a real chance to lose, so this one stays small.","hit":"About 1 in 5"},
]
ps={x['p'] for x in SAT}
for t in STIX:
  for l in t['legs']: assert l in ps,l
# constants
o="const CUR=FRI,CTIX=FTIX,CURD='2026-11-13';";assert o in s
s=s.replace(o,'const SAT='+json.dumps(SAT)+';\nconst STIX='+json.dumps(STIX)+";\nconst CUR=SAT,CTIX=STIX,CURD='2026-11-14';")
# clone home renderer for Friday history
b=s.index("document.getElementById('thuTix').innerHTML=CTIX.map(");a=s.rindex("(function(){const rb=x=>x.r?",0,b);c=s.index('\n',b)+1
blk=s[a:c];assert 'CUR' in blk
fri=blk.replace('CURD',"'2026-11-13'").replace('CTIX','FTIX').replace('CUR','FRI').replace("'thu","'frh")
s=s[:c]+fri+s[c:]
sec='''
  <section class="panel" id="frihist">
    <h2>Friday board · Nov 13 <small>FINAL · 70%+ legs 42 of 58 · whole board 63 of 97</small></h2>
    <h3>Friday tickets</h3>
    <div class="struct" id="frhTix"></div>
    <div class="two" style="margin-top:18px">
      <div><h3>Top 25: any line</h3><ol class="tueo" id="frhAny" style="margin:8px 0 0;padding-left:22px;font-size:12.5px;line-height:1.75"></ol></div>
      <div><h3>Top 25: regular lines</h3><ol class="tueo" id="frhReg" style="margin:8px 0 0;padding-left:22px;font-size:12.5px;line-height:1.75"></ol></div>
    </div>
    <details class="notes" style="margin-top:12px"><summary class="lbl" style="cursor:pointer">Clean 70 pool</summary><div class="chips" id="frhPool"></div></details>
    <div class="filters" id="frhF" style="margin-top:16px"></div>
    <div class="scroll boardwrap" style="max-height:620px;overflow-y:auto"><table id="frhT" class="board"></table></div>
  </section>
'''
o='\n  <section class="panel" id="thuhist">';assert o in s
s=s.replace(o,sec+o,1)
o="review11:'history',thuhist:'history',";assert o in s
s=s.replace(o,"review11:'history',frihist:'history',thuhist:'history',")
o="const BOARD={d:CURD,rows:CUR,label:'Friday · Nov 13'};";assert o in s
s=s.replace(o,"const BOARD={d:CURD,rows:CUR,label:'Saturday · Nov 14'};")
o='<h2 class="big" id="dayTitle">Friday · Nov 13</h2>';assert o in s
s=s.replace(o,'<h2 class="big" id="dayTitle">Saturday · Nov 14</h2>')
o='Friday graded · 42 of 58 at 70%+ · Saturday board next';assert o in s
s=s.replace(o,'Saturday Nov 14 picks are live · NBA, UFC 334, college football')
o="TEN:'🎾 Tennis',";assert o in s
s=s.replace(o,"TEN:'🎾 Tennis',UFC:'🥊 UFC',")
o="[typeof FRI!=='undefined'&&FRI,";assert o in s
s=s.replace(o,"[typeof SAT!=='undefined'&&SAT,typeof FRI!=='undefined'&&FRI,")
# injury notes
a=s.index('<section class="panel" id="thursday">');b=s.index('</section>',a);secx=s[a:b]
i=secx.index('<details class="notes"');j=secx.index('</details>',i)+10
new='''<details class="notes" style="margin-top:16px"><summary class="lbl" style="cursor:pointer">Injury and matchup notes</summary><div class="flags" style="margin-top:10px">
      <div class="flag w"><b>Already started</b><div class="r warn">marked LIVE</div><p>Georgia, Indiana-USC, Georgia Southern and Rice had kicked off when the picks came in. Syracuse and Coastal Carolina were already final (both won). They are on the chart but off the tickets.</p><div class="who">Prices on those have moved</div></div>
      <div class="flag w"><b>Blowout watch</b><div class="r warn">Model v6</div><p>Denver -12.5 and Wolves -15.5. No Jokic, Murray or Ayo legs on the tickets, either side of those games.</p><div class="who">Two blowouts burned us this week</div></div>
      <div class="flag"><b>Out or questionable</b><div class="r bad">checked 1:50 PM</div><p>Out: Mobley, Ty Jerome, Edwards, Duren, Lively, Dejounte Murray, Trey Murphy. Questionable: Donovan Mitchell, Harden, Allen (Cavs), Edey, Norman Powell. Probable: Giannis (wrist), Traore (calf).</p><div class="who">Check the Cavs before any Tyson leg</div></div>
      <div class="flag"><b>UFC 334</b><div class="r">market price</div><p>UFC grades are the market price, not our own edge. We have almost no UFC record yet. Early prelims 2:00, prelims 4:00, main card 6:00 PT. Gane walks last.</p><div class="who">Keep UFC legs small</div></div>
    </div></details>'''
secx=secx[:i]+new+secx[j:];s=s[:a]+secx+s[b:]
open(p,'w').write(s);print('ok')
