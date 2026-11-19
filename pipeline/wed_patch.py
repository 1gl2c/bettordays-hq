import json,re
p='bettordays-hq.html';s=open(p).read()
W=json.load(open('wed/wed.json'))
kp={r['p']:r.get('k') for r in W};gr={r['p']:r for r in W}
def est(legs):
  x=1
  for l in legs: x*=kp[l]/100
  return 1/x
TIX=[
 {"t":"Hammer · 5 legs","c":"#04ff9f","legs":["Darius Acuff 1+ threes","Los Angeles Lakers ML v Jazz","Shai Gilgeous-Alexander 25+ points","Gui Santos 2+ rebounds","LeBron James 4+ rebounds"],"stake":"Biggest share","v":"Every leg passes the Hammer filter: graded 80+, Kalshi within 7 of us, no ⚠. Five different games. Acuff has a three in 12 of 13. SGA has 25+ in 12 of 14 with Jalen Williams and Holmgren out. Santos has 2+ boards in 10 of 11 with Curry and Porzingis out. LeBron has 4+ boards in 10 of 11, but Orlando is a tough rebounding matchup. The filter is a provisional rule, not proof these hit."},
 {"t":"Second ticket · 4 legs","c":"#00c8ff","legs":["Isaiah Hartenstein 2+ assists","Luka Doncic 30+ points","Zach Edey 6+ rebounds","Julius Randle 4+ assists"],"stake":"Medium","v":"Graded 78 to 88 with Kalshi within 7 on every leg, four different games. Luka is on a back-to-back and the Lakers are -12.5, so a blowout could cut his fourth quarter. Luka also shares a game with the Hammer's Lakers ML, so the two tickets lean the same way."},
]
for t in TIX:
  for l in t['legs']:
    r=gr[l];assert r['pct']>=78 and r.get('k') is not None and abs(r['pct']-r['k'])<=7 and not r.get('fl'),(l,r['pct'],r.get('k'))
  e=est(t['legs']);t['lock']=f"About {e:.2f}x at Kalshi's prices"
  pr=1
  for l in t['legs']: pr*=gr[l]['pct']/100
  t['hit']=f"About {round(pr*100)}% by our grades"
  print(t['t'],round(e,2),t['hit'])
o="const CUR=TU17,CTIX=TUTIX,CURD='2026-11-17';";assert o in s
s=s.replace(o,'const WE18='+json.dumps(W)+';\nconst WETIX='+json.dumps(TIX)+";\nconst CUR=WE18,CTIX=WETIX,CURD='2026-11-18';")
m=re.search(r'const CURCUT=[^;]*;',s);s=s.replace(m.group(0),'const CURCUT=15*60+30;')
b=s.index("document.getElementById('thuTix').innerHTML=CTIX.map(");a=s.rindex("(function(){const rb=x=>x.r?",0,b);c=s.index('\n',b)+1
blk=s[a:c];tue=blk.replace('CURD',"'2026-11-17'").replace('CTIX','TUTIX').replace('CUR','TU17').replace("'thu","'tuh")
assert 'CURCUT' not in blk
s=s[:c]+tue+s[c:]
sec='''
  <section class="panel" id="tuehist">
    <h2>Tuesday board · Nov 17 <small>FINAL · 70%+ legs 18 of 27</small></h2>
    <h3>Tuesday tickets</h3>
    <div class="struct" id="tuhTix"></div>
    <div class="two" style="margin-top:18px">
      <div><h3>Top 25: any line</h3><ol class="tueo" id="tuhAny" style="margin:8px 0 0;padding-left:22px;font-size:12.5px;line-height:1.75"></ol></div>
      <div><h3>Top 25: regular lines</h3><ol class="tueo" id="tuhReg" style="margin:8px 0 0;padding-left:22px;font-size:12.5px;line-height:1.75"></ol></div>
    </div>
    <details class="notes" style="margin-top:12px"><summary class="lbl" style="cursor:pointer">Clean 70 pool</summary><div class="chips" id="tuhPool"></div></details>
    <div class="filters" id="tuhF" style="margin-top:16px"></div>
    <div class="scroll boardwrap" style="max-height:620px;overflow-y:auto"><table id="tuhT" class="board"></table></div>
  </section>
'''
o='\n  <section class="panel" id="monhist">';assert o in s
s=s.replace(o,sec+o,1)
o="monhist:'history',";assert s.count(o)==1;s=s.replace(o,"tuehist:'history',monhist:'history',")
o="label:'Tuesday · Nov 17'};";assert o in s;s=s.replace(o,"label:'Wednesday · Nov 18'};")
o='id="dayTitle">Tuesday · Nov 17</h2>';assert o in s;s=s.replace(o,'id="dayTitle">Wednesday · Nov 18</h2>')
o='Tuesday graded · 18 of 27 at 70%+ · Wednesday board next';assert o in s
s=s.replace(o,'Wednesday Nov 18 picks are live · NBA, hockey and college hoops')
o="[typeof TU17!=='undefined'&&TU17,";assert o in s;s=s.replace(o,"[typeof WE18!=='undefined'&&WE18,typeof TU17!=='undefined'&&TU17,")
o="those legs hit 3 of 11 over Monday and Tuesday, so they are not used in Hammer tickets while we test this on the full record."
assert o in s
s=s.replace(o,"on Nov 4 to 15, picks that were not used to make this rule, those legs hit 60 of 106 (57%) against 69% for everything else. So ⚠ legs stay out of Hammers and main tickets. Hammer filter (provisional): graded 80+ and Kalshi within 7. That is a selection rule we are still testing, not proof a leg is safe.")
a=s.index('<section class="panel" id="thursday">');b=s.index('</section>',a);secx=s[a:b]
i=secx.index('<details class="notes"');j=secx.index('</details>',i)+10
new='''<details class="notes" style="margin-top:16px"><summary class="lbl" style="cursor:pointer">Injury and matchup notes</summary><div class="flags" style="margin-top:10px">
      <div class="flag"><b>Out tonight</b><div class="r bad">checked 2:46 PM PT</div><p>Scottie Barnes (his 30+ PRA leg is void), Kawhi Leonard, Jaylen Brown, Paolo Banchero, Haliburton, Nembhard, Capela, Curry, Porzingis, Jalen Williams, Holmgren, Cason Wallace, Austin Reaves, Markkanen, Jaren Jackson Jr., Nurkic, Mobley, Jaylon Tyson, McCollum, Landale, Duren, Holland, Prince, Trey Murphy, Mathurin, Lively, Mark Williams.</p><div class="who">Questionable: Dean Wade, Cade Cunningham, Amen Thompson, Draymond Green, Al Horford, RJ Barrett</div></div>
      <div class="flag w"><b>Back-to-back</b><div class="r warn">played last night</div><p>Lakers, Jazz, Pistons and Raptors played Tuesday. Their players are marked down a few points.</p><div class="who">Luka, Ausar Thompson, Ace Bailey, Darryn Peterson</div></div>
      <div class="flag w"><b>Florida v Houston</b><div class="r bad">started before the list</div><p>Tipped at 1:48 PM PT. Florida led 40-37 at half when the board was built, so both legs are shown but not graded or counted.</p><div class="who">Not in the record</div></div>
      <div class="flag w"><b>Hockey and college hoops</b><div class="r warn">no model of our own</div><p>Graded from the betting line and capped under 70. Kalshi is shown next to each one. Close to coin flips except Eastern Michigan and Kansas.</p><div class="who">No edge claimed</div></div>
      <div class="flag g"><b>Lines that moved</b><div class="r">your list</div><p>"Over 8 rebounds" means 9 or more, so those became the 9+ line. A few lines were also moved down in the same stat (Luka 25+, Giannis 25+, Maxey 30+ PRA and others), each marked "Moved line". No new players or stats.</p><div class="who">Each note shows your original line</div></div>
    </div></details>'''
secx=secx[:i]+new+secx[j:];s=s[:a]+secx+s[b:]
open(p,'w').write(s);print('ok')
t=open('buildsite.py').read();o="DAYK=[('TU17',";assert o in t
open('buildsite.py','w').write(t.replace(o,"DAYK=[('WE18','2026-11-18','Wednesday Nov 18'),('TU17',"))
