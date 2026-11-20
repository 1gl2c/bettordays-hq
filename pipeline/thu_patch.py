# Publish the Nov 19 board (same steps as wed_patch.py). Content only: board rows, tickets, notes, Beta tonight, Nov 18 moved to history.
import json,re
p='bettordays-hq.html';s=open(p).read()
D=json.load(open('thu/thu.json'));W=[]
for r in D['rows']:
  r=dict(r)
  if r['pct'] is None: r['pct']=0;r['fl']='NO GRADE'
  if r.get('fl')=='RULE': r['fl']='ACE RULE'
  W.append(r)
TIX=[]   # no leg qualifies for the Hammer (80+, Kalshi within 7) and none meets the 78+ second-ticket bar tonight
def rep(a,b,n=1):
  global s
  assert s.count(a)==n,(s.count(a),a[:80]);s=s.replace(a,b)
rep("const CUR=WE18,CTIX=WETIX,CURD='2026-11-18';",'const TH19='+json.dumps(W)+';\nconst THTIX='+json.dumps(TIX)+";\nconst CUR=TH19,CTIX=THTIX,CURD='2026-11-19';")
m=re.search(r'const CURCUT=[^;]*;',s);s=s.replace(m.group(0),'const CURCUT=16*60+25;')
b=s.index("document.getElementById('thuTix').innerHTML=CTIX.map(");a=s.rindex("(function(){const rb=x=>x.r?",0,b);c=s.index('\n',b)+1
blk=s[a:c];wed=blk.replace('CURD',"'2026-11-18'").replace('CTIX','WETIX').replace('CUR','WE18').replace("'thu","'weh")
assert 'CURCUT' not in blk
s=s[:c]+wed+s[c:]
sec='''
  <section class="panel" id="wedhist">
    <h2>Wednesday board · Nov 18 <small>FINAL · 70%+ legs 29 of 42</small></h2>
    <h3>Wednesday tickets</h3>
    <div class="struct" id="wehTix"></div>
    <div class="two" style="margin-top:18px">
      <div><h3>Top 25: any line</h3><ol class="tueo" id="wehAny" style="margin:8px 0 0;padding-left:22px;font-size:12.5px;line-height:1.75"></ol></div>
      <div><h3>Top 25: regular lines</h3><ol class="tueo" id="wehReg" style="margin:8px 0 0;padding-left:22px;font-size:12.5px;line-height:1.75"></ol></div>
    </div>
    <details class="notes" style="margin-top:12px"><summary class="lbl" style="cursor:pointer">Clean 70 pool</summary><div class="chips" id="wehPool"></div></details>
    <div class="filters" id="wehF" style="margin-top:16px"></div>
    <div class="scroll boardwrap" style="max-height:620px;overflow-y:auto"><table id="wehT" class="board"></table></div>
  </section>
'''
o='\n  <section class="panel" id="tuehist">';rep(o,sec+o)
rep("tuehist:'history',","wedhist:'history',tuehist:'history',")
rep("label:'Wednesday · Nov 18'};","label:'Thursday · Nov 19'};")
rep('id="dayTitle">Wednesday · Nov 18</h2>','id="dayTitle">Thursday · Nov 19</h2>')
rep('Wednesday graded · 29 of 42 at 70%+ · Thursday board next','Thursday Nov 19 picks are live · NFL, NBA, hockey and college hoops · no Hammer tonight')
rep("[typeof WE18!=='undefined'&&WE18,","[typeof TH19!=='undefined'&&TH19,typeof WE18!=='undefined'&&WE18,")
rep("const D=[['Nov 18','WE18','WETIX'],","const D=[['Nov 19','TH19','THTIX'],['Nov 18','WE18','WETIX'],")
# tonight's notes
a=s.index('<section class="panel" id="thursday">');b=s.index('</section>',a);secx=s[a:b]
i=secx.index('<details class="notes"');j=secx.index('</details>',i)+10
new='''<details class="notes" style="margin-top:16px"><summary class="lbl" style="cursor:pointer">Injury and matchup notes</summary><div class="flags" style="margin-top:10px">
      <div class="flag"><b>Out tonight</b><div class="r bad">checked 3:45 to 4:15 PM PT</div><p>Myles Turner (both of his assist unders are void), Anthony Edwards, DiVincenzo, Kuzma, Ingram, Beal, Morant, Sharpe, Robert Williams, Curry, Draymond Green, Porzingis, Butler, Edey, Harper, Tobias Harris. Colts: Will Mallory out, Anthony Gould questionable. Texans: Woody Marks and Brevin Jordan out.</p><div class="who">ESPN injury reports</div></div>
      <div class="flag w"><b>No Hammer tonight</b><div class="r warn">rule check</div><p>No leg is graded 80+ with Kalshi within 7. McDaniels 4+ rebounds (84) and Brook Lopez 4+ rebounds (80) both have Kalshi 8 or more below us, so they carry a ⚠. No ticket is suggested tonight.</p><div class="who">Hammer rule is provisional</div></div>
      <div class="flag w"><b>NFL team lines</b><div class="r warn">no grade</div><p>Texans ML and Texans -9.5 have no system grade. Our process has no NFL team-line method. Kalshi is shown for reference only.</p><div class="who">Shown as NO GRADE</div></div>
      <div class="flag w"><b>Ace rule</b><div class="r bad">off every ticket</div><p>Victor Wembanyama under 30 points breaks the no-unders-on-Wemby rule. It is graded for the record only.</p><div class="who">Graded 56</div></div>
      <div class="flag g"><b>Lines read from your list</b><div class="r">notation</div><p>"Over 9.5" became 10+, "over 12.5 rush attempts" became 13+, "over 15 PRA" became 16+, and "Dalton Schultz 25 receiving yards" was read as 25+. Anthony Gould receiving yards had no line, so it is not on the board. Duplicates were graded once.</p><div class="who">Amari Demercado is Emari Demercado (Texans)</div></div>
    </div></details>'''
secx=secx[:i]+new+secx[j:];s=s[:a]+secx+s[b:]
# Beta Test Mode: tonight's run, keep the track record
m=re.search(r'BETA=(\{.*?\});\n',s);old=json.loads(m.group(1))
B=json.load(open('beta19/beta_tonight.json'))
newb={'ts':B['ts'],'sim_ts':B['sim_ts'],'n_lines':B['n_lines'],'n_games':B['n_games'],'all_pos':B['all_pos'],'top':B['top'],'hist':old['hist']}
s=s.replace(m.group(0),'BETA='+json.dumps(newb)+';\n',1)
rep('<h3>Latest Top 15 · Wednesday Nov 18</h3>','<h3>Latest Top list · Thursday Nov 19 · 8 lines (4 games, max 2 per game)</h3>')
# Method page: replace the tip-off-based comparison with the like-for-like one
rep("On the Nov 4 to 17 legs with a Kalshi price, Kalshi's prices were more accurate than our grades (Brier 0.189 vs 0.211, lower is better), and",
    "On 184 like-for-like picks (Nov 16 to 18: same picks, Kalshi price taken when we graded, grades that did not use Kalshi), Kalshi was more accurate than our grades (Brier 0.210 vs 0.224, lower is better; three nights, so provisional), and")
open(p,'w').write(s);print('ok',len(W))
t=open('buildsite.py').read();o="DAYK=[('WE18',";assert o in t
open('buildsite.py','w').write(t.replace(o,"DAYK=[('TH19','2026-11-19','Thursday Nov 19'),('WE18',"))
