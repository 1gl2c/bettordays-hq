import json,re
p='bettordays-hq.html';s=open(p).read()
TU=json.load(open('tue/tue.json'))
kp={r['p']:r.get('k') for r in TU}
def est(legs):
  x=1
  for l in legs: x*=kp[l]/100
  return 0.93/x
TIX=[
 {"t":"Hammer · 4 legs","c":"#04ff9f","legs":["Karl-Anthony Towns 15+ points","Keldon Johnson 4+ rebounds","Darius Garland 15+ points","LaMelo Ball under 25 points"],"stake":"Biggest share","v":"Four different games, every leg graded 82 or higher. Towns has 15+ in all 13 games. Keldon has 4+ rebounds in all 14. Garland has 15+ in 9 of 12 and runs the offense with Ingram and Beal out. LaMelo has stayed under 25 in 13 of 14.","hit":"About 50%"},
 {"t":"2x · Luka","c":"#00c8ff","legs":["Luka Doncic 30+ points","Brook Lopez 4+ rebounds","Grayson Allen 10+ points"],"stake":"Medium","v":"Luka has 30+ in 10 of 12 and Reaves is out. Lopez has 4+ rebounds in 9 of 12 against a Utah team missing its bigs. Allen has 10+ in 10 of 13 with Knueppel and Schroder out.","hit":"About 45%"},
 {"t":"Long shot · 8 legs","c":"#ff4d5e","legs":["Karl-Anthony Towns 15+ points","Keldon Johnson 4+ rebounds","Darius Garland 15+ points","LaMelo Ball under 25 points","Luka Doncic 30+ points","Brook Lopez 4+ rebounds","Donovan Clingan 8+ rebounds","Toumani Camara under 4 threes"],"stake":"A few dollars","v":"Both tickets above plus Clingan 8+ rebounds (10 of 13) and Camara under 4 threes. Every leg graded 78 or higher. Clingan and Camara are on the second night of a back-to-back.","hit":"About 1 in 6"},
]
ps={x['p'] for x in TU}
for t in TIX:
  for l in t['legs']: assert l in ps,l
  e=est(t['legs']);t['lock']=f"About {e:.1f}x at Kalshi's prices"
  print(t['t'],round(e,2))
o="const CUR=MN16,CTIX=MNTIX,CURD='2026-11-16';";assert o in s
s=s.replace(o,'const TU17='+json.dumps(TU)+';\nconst TUTIX='+json.dumps(TIX)+";\nconst CUR=TU17,CTIX=TUTIX,CURD='2026-11-17';")
m=re.search(r'const CURCUT=[^;]*;',s);s=s.replace(m.group(0),'const CURCUT=15*60+30;')
b=s.index("document.getElementById('thuTix').innerHTML=CTIX.map(");a=s.rindex("(function(){const rb=x=>x.r?",0,b);c=s.index('\n',b)+1
blk=s[a:c];mon=blk.replace('CURD',"'2026-11-16'").replace('CTIX','MNTIX').replace('CUR','MN16').replace("'thu","'mnh")
s=s[:c]+mon+s[c:]
sec='''
  <section class="panel" id="monhist">
    <h2>Monday board · Nov 16 <small>FINAL · 70%+ legs 40 of 55 · Hammer cashed</small></h2>
    <h3>Monday tickets</h3>
    <div class="struct" id="mnhTix"></div>
    <div class="two" style="margin-top:18px">
      <div><h3>Top 25: any line</h3><ol class="tueo" id="mnhAny" style="margin:8px 0 0;padding-left:22px;font-size:12.5px;line-height:1.75"></ol></div>
      <div><h3>Top 25: regular lines</h3><ol class="tueo" id="mnhReg" style="margin:8px 0 0;padding-left:22px;font-size:12.5px;line-height:1.75"></ol></div>
    </div>
    <details class="notes" style="margin-top:12px"><summary class="lbl" style="cursor:pointer">Clean 70 pool</summary><div class="chips" id="mnhPool"></div></details>
    <div class="filters" id="mnhF" style="margin-top:16px"></div>
    <div class="scroll boardwrap" style="max-height:620px;overflow-y:auto"><table id="mnhT" class="board"></table></div>
  </section>
'''
o='\n  <section class="panel" id="sunhist">';assert o in s
s=s.replace(o,sec+o,1)
o="sunhist:'history',";assert s.count(o)==1;s=s.replace(o,"monhist:'history',sunhist:'history',")
o="label:'Monday · Nov 16'};";assert o in s;s=s.replace(o,"label:'Tuesday · Nov 17'};")
o='id="dayTitle">Monday · Nov 16</h2>';assert o in s;s=s.replace(o,'id="dayTitle">Tuesday · Nov 17</h2>')
o='Monday graded · 40 of 55 at 70%+ · Kalshi prices now shown next to every grade';assert o in s
s=s.replace(o,'Tuesday Nov 17 picks are live · NBA, hockey, college hoops and MACtion')
o="[typeof MN16!=='undefined'&&MN16,";assert o in s;s=s.replace(o,"[typeof TU17!=='undefined'&&TU17,typeof MN16!=='undefined'&&MN16,")
a=s.index('<section class="panel" id="thursday">');b=s.index('</section>',a);secx=s[a:b]
i=secx.index('<details class="notes"');j=secx.index('</details>',i)+10
new='''<details class="notes" style="margin-top:16px"><summary class="lbl" style="cursor:pointer">Injury and matchup notes</summary><div class="flags" style="margin-top:10px">
      <div class="flag"><b>Out tonight</b><div class="r bad">checked 3:10 PM</div><p>Austin Reaves, Walker Kessler, Kon Knueppel, Dennis Schroder, Brandon Ingram, Bradley Beal, Lauri Markkanen, Jaren Jackson Jr., Jusuf Nurkic, Anthony Edwards, DiVincenzo, Ja Morant, Shaedon Sharpe, Kawhi Leonard, Jalen Duren, Tobias Harris.</p><div class="who">Day to day: Deni Avdija</div></div>
      <div class="flag w"><b>Back-to-back</b><div class="r warn">POR at MIN again</div><p>Portland and Minnesota played each other last night and do it again tonight. Their players are marked down a few points.</p><div class="who">Gobert, Clingan, LaMelo, Ayo, Camara</div></div>
      <div class="flag w"><b>College football yardage</b><div class="r warn">not on Kalshi</div><p>Kalshi has no college player props, so these are capped at 70 and graded off each player's season log. Western Michigan kicked off at 3 PM, so Buckley is marked live.</p><div class="who">MACtion</div></div>
      <div class="flag w"><b>Hockey and college hoops</b><div class="r warn">market price only</div><p>We have no record in these yet, so they are graded at Kalshi's price and capped under 70. All six are close to coin flips.</p><div class="who">No edge claimed</div></div>
      <div class="flag g"><b>Lines that moved</b><div class="r">your list</div><p>"Over 5 assists" means 6 or more, so those became the 6+ line. We moved some lines down in the same stat for a safer number. No new stats or players were added.</p><div class="who">Each note shows your original line</div></div>
    </div></details>'''
secx=secx[:i]+new+secx[j:];s=s[:a]+secx+s[b:]
open(p,'w').write(s);print('ok')
t=open('buildsite.py').read();o="DAYK=[('MN16',";assert o in t
open('buildsite.py','w').write(t.replace(o,"DAYK=[('TU17','2026-11-17','Tuesday Nov 17'),('MN16',"))
