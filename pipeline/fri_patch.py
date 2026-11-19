import json,re
p='bettordays-hq.html';s=open(p).read()
FRI=json.load(open('fri/fri.json'))
FTIX=[
 {"t":"Power 3 · the core","c":"#04ff9f","legs":["Pascal Siakam 20+ points","Darius Acuff Jr 30+ PRA","Yaxel Lendeborg 15+ points"],"stake":"10% of bankroll","lock":"About 2.5x, take 2.2x or better","v":"Three different games, three guys whose team needs their shots. Siakam with Haliburton out, Acuff averaging 37 PRA, Lendeborg with Curry out. All three are on the underdog side, so no blowout benching.","hit":"About 61-66%"},
 {"t":"Hammer · 4 legs","c":"#00c8ff","legs":["Ty Jerome 15+ points","Davion Mitchell 6+ assists","Tyler Herro 15+ points","Cameron Boozer 6+ rebounds"],"stake":"8% of bankroll","lock":"About 2.2x, take 2.0x or better","v":"Jerome is 9 of 10 at 15+. Davion 9 of 11 at 6+ assists. Boozer 11 of 11 at 6+ boards with Edey and Post out. Four different games.","hit":"About 52-62%"},
 {"t":"2-3x · value","c":"#ffb020","legs":["Shai Gilgeous-Alexander 25+ points","Hofstra ML v Iona","Nickeil Alexander-Walker 15+ points","Jaime Jaquez 10+ points"],"stake":"5% of bankroll","lock":"About 2.6x, take 2.4x or better","v":"SGA with Jalen Williams and Holmgren out. Hofstra -7.5 at home. NAW in the fastest game on the board (245.5).","hit":"About 45-52%"},
 {"t":"5-10x · the stretch","c":"#ff4d5e","legs":["Sabonis 30+ PRA","Tyler Herro 20+ points","Donovan Mitchell 20+ points","Cameron Boozer 8+ rebounds","Samford +7.5 v Wright State"],"stake":"3% of bankroll","lock":"About 7-12x, take 6x or better","v":"Every leg 72-75, five different games. Mitchell gets more shots with Mobley out. No 100x tonight. That's retired.","hit":"About 1 in 5"},
]
ps={x['p'] for x in FRI}
for t in FTIX:
  for l in t['legs']: assert l in ps,l
# 1 insert FRI/FTIX constants before THU
i=s.index('const THU=')
s=s[:i]+'const FRI='+json.dumps(FRI)+';\nconst FTIX='+json.dumps(FTIX)+';\nconst CUR=FRI,CTIX=FTIX,CURD=\'2026-11-13\';\n'+s[i:]
# 2 home renderer -> CUR; history clone with THU
a=s.index("(function(){const rb=x=>x.r?",s.index('const HTIX='))
b=s.index("document.getElementById('thuTix').innerHTML=HTIX.map(",a)
c=s.index('\n',b)+1
blk=s[a:c]
hist=blk.replace("'thu","'thh").replace("2026-11-12","2026-11-12")
home=blk.replace('THU','CUR').replace('HTIX','CTIX').replace("'2026-11-12'",'CURD')
s=s[:a]+home+hist+s[c:]
# 3 history section html for Thursday, cloned ids
sec='''
  <section class="panel" id="thuhist">
    <h2>Thursday board · Nov 12 <small>FINAL · 70%+ legs 30 of 35 · whole board 78 of 110</small></h2>
    <h3>Thursday tickets</h3>
    <div class="struct" id="thhTix"></div>
    <div class="two" style="margin-top:18px">
      <div><h3>Top 25: any line</h3><ol class="tueo" id="thhAny" style="margin:8px 0 0;padding-left:22px;font-size:12.5px;line-height:1.75"></ol></div>
      <div><h3>Top 25: regular lines</h3><ol class="tueo" id="thhReg" style="margin:8px 0 0;padding-left:22px;font-size:12.5px;line-height:1.75"></ol></div>
    </div>
    <details class="notes" style="margin-top:12px"><summary class="lbl" style="cursor:pointer">Clean 70 pool</summary><div class="chips" id="thhPool"></div></details>
    <div class="filters" id="thhF" style="margin-top:16px"></div>
    <div class="scroll boardwrap" style="max-height:620px;overflow-y:auto"><table id="thhT" class="board"></table></div>
  </section>
'''
s=s.replace('  <section class="panel" id="wednesday">',sec+'  <section class="panel" id="wednesday">',1)
s=s.replace("review11:'history',","review11:'history',thuhist:'history',",1)
assert "thuhist:'history'" in s
# 4 app.js BOARD + tap3
s=s.replace("const BOARD={d:'2026-11-12',rows:typeof THU!=='undefined'?THU:[],label:'Thursday · Nov 12'};","const BOARD={d:CURD,rows:CUR,label:'Friday · Nov 13'};")
assert "label:'Friday · Nov 13'" in s
# 5 header + proof
s=s.replace('Thursday fully graded · 30 of 35 at 70%+ · Friday board next','Friday Nov 13 picks are live · 9 NBA games + college')
s=s.replace('<h2 class="big" id="dayTitle">Thursday · Nov 12</h2>','<h2 class="big" id="dayTitle">Friday · Nov 13</h2>')
open(p,'w').write(s);print('ok')
