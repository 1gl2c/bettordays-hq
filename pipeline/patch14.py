import re,json,math
exec(open('study/tue.py').read())
P='bettordays-hq.html'; s=open(P).read()
FLMAP={'status':'STATUS','star-under':'STARU','filler':'FILL','college':'CBB','unverified':'VERIFY','assist-over':'AST','guard-reb':'GREB','PRA':'PRA','no-line':'NOLINE','conflict':'CONFLICT'}
NBA={'BOS@PHI','MIL@NYK','LAC@PHX','MIA@UTA','ORL@SAC','OKC@POR'}
TUE=[]
for p,pct,g,t,ty,st,n,fl,mv in T:
    f=fl.split(',')[0] if fl else ''
    if g in ('KENT@BGSU','WMU@AKR','OHIO@M-OH','MAC') : sp='CFB'
    elif g in NBA: sp='NBA'
    else: sp='CBB'
    TUE.append({"p":p,"pct":pct,"g":g,"t":t,"ty":ty,"st":st,"n":n,"fl":FLMAP.get(f,'') if f else '',"sp":sp,"mv":mv if mv and '·' in mv else ('' if not mv else mv)})
# moved lines as their own rows
for p,pct,g,n in [("Maluach 4+ reb",76,"LAC@PHX","Moved down from 5.5. Mark Williams out."),("Buckley 75+ rush yds",66,"WMU@AKR","Moved down from 99.5. WMU is a 7-in-8 favorite."),("Wayne Harris 50+ rec yds",62,"KENT@BGSU","Moved down from 75.5."),("Ace Bailey 12+ pts",72,"MIA@UTA","Moved down from 15.5. Usage up."),("Tatum 5+ reb",68,"BOS@PHI","Moved down from 7.5. He averages 6.0."),("Franz Wagner 5+ ast",70,"ORL@SAC","Moved down from 8. Main creator with Banchero out.")]:
    TUE.append({"p":p,"pct":pct,"g":g,"t":"","ty":"prop","st":"move","n":n,"fl":"CBB" if g in('WMU@AKR','KENT@BGSU') else '',"sp":"CFB" if g in('WMU@AKR','KENT@BGSU') else 'NBA',"mv":""})
tm={'BOS@PHI':'5:00','MIL@NYK':'4:30','LAC@PHX':'6:00','MIA@UTA':'6:00','ORL@SAC':'7:00','OKC@POR':'8:00','WMU@AKR':'4:00','KENT@BGSU':'4:00'}
for r in TUE:
    if not r['t']: r['t']=tm.get(r['g'],'')
by={r['p']:r for r in TUE}
def tix(name,c,legs,stake,v):
    pr=1; mk=1
    for l in legs: pr*=min(by[l]['pct'],88)/100; mk*=by[l]['pct']/100
    k=len(legs); f=.85 if k<=4 else .75 if k<=8 else .6 if k<=12 else .5
    pay=f/mk
    hit=f"About {round(pr*100)}%" if pr>=.1 else f"About 1 in {round(1/pr)}"
    return {"t":name,"c":c,"legs":legs,"hit":hit,"stake":stake,"lock":f"About {pay:.1f}x on Kalshi or better" if pay<20 else f"{int(pay//10*10)}x or better","v":v}
TTIX=[
 tix("Hammer","#04ff9f",["Tyrese Maxey 15+ points","Jaylen BRown 15+ points","Miami Heat ML V Utah","Bam Adebayo o6.5 REB"],"$100","Four legs from two games we trust most. Sixers stars at home, and Miami vs a Jazz team missing four starters. Every leg 82%+."),
 tix("2x · stars score","#00c8ff",["Jayson Tatum 20+ points","Jalen Brunson 20+ points","Karl Anthony Towns 15+ points","Joel Embiid 6+ rebounds"],"$50","Four big names at lines well under their averages. No unders, no college."),
 tix("5-10x · anchors + real lines","#ffb020",["Tyrese Maxey 15+ points","Jayson Tatum 20+ points","Jalen Brunson 20+ points","Miami Heat ML V Utah","Jaylen Brown over 20 points","Darryn Peterson 15 + points","Darius Acuff Jr. o1.5 Threes Made"],"$20","Four anchors plus three sharper lines in the 60s, like Ace asked. Brown 20+ in his revenge game, Peterson with Utah's starters out, Acuff two threes."),
 tix("Normal lotto · about 25x","#c77dff",["Tyrese Maxey 15+ points","Jayson Tatum 20+ points","Jalen Brunson 20+ points","Miami Heat ML V Utah","Jaylen Brown over 20 points","Darryn Peterson 15 + points","Darius Acuff Jr. o1.5 Threes Made","Deni Avdija over 1.5 3 pointers made","Khaman Maluach Over 5.5 Rebounds","Ace Bailey o15.5 PTS"],"$10","The 5-10x plus three regular lines at their real numbers. Ten legs, all NBA."),
 tix("100x lotto #1 · sharper lines","#ff4d5e",["Tyrese Maxey 15+ points","Jayson Tatum 20+ points","Jalen Brunson 20+ points","Miami Heat ML V Utah","Jaylen Brown over 20 points","Darryn Peterson 15 + points","Darius Acuff Jr. o1.5 Threes Made","Deni Avdija over 1.5 3 pointers made","Khaman Maluach Over 5.5 Rebounds","Ace Bailey o15.5 PTS","Darius Acuff 6+ assists","Shai Gilgeous Alexander 5+ Rebounds","Jalen Brunsun 6+ assists"],"$10","Thirteen legs, every one a real line or close to it. No unders on stars, no college, no PRA."),
 tix("Lotto #2 · the whole clean pool · 70x+","#04ff9f",["Tyrese Maxey 15+ points","Jaylen BRown 15+ points","Joel Embiid 6+ rebounds","Jayson Tatum 20+ points","Jalen Brunson 20+ points","Karl Anthony Towns 15+ points","Miami Heat ML V Utah","Bam Adebayo o6.5 REB","Rui Hachimura 10+ points","Shai Gilgeous Alexander 4+ Rebounds","Deni Avdija over 0.5 3 pointers made","Maluach 4+ reb","Ace Bailey 12+ pts","Franz Wagner 5+ ast","Donovan Clingan under 14 rebounds","Darryn Peterson 15 + points","Darius Acuff Jr. o1.5 Threes Made","Jaylen Brown over 20 points","Kansas ML v Kentucky","Michigan State /Duke over 130 + total points"],"$10","Ace's mission: a lotto built from 70%s. All 15 clean NBA legs, three 60s lines and two Champions Classic legs. Twenty legs."),
]
pool=[r for r in TUE if r['pct']>=70 and not r['fl'] and r['sp']=='NBA']
print('pool',len(pool),[r['p'] for r in pool])
for t in TTIX: print(t['t'],t['hit'],t['lock'])
json.dump(TUE,open('study/nov10.json','w'))
sec=re.search(r'  <section class="panel" id="monday">.*?</section>\n',s,re.S).group(0)
new=sec.replace('id="monday"','id="tuesday"').replace('mon','tue')
new=re.sub(r'<h2>.*?</h2>','<h2>Tuesday board · Nov 10 <small>%d picks graded · 6 NBA games, Champions Classic, MACtion</small></h2>'%len(TUE),new,1,flags=re.S)
flags='''    <div class="flags" style="margin-bottom:14px">
      <div class="flag"><b>Rosters moved. We checked.</b><div class="r warn">verified</div><p>Jaylen Brown is a Sixer now (traded for Paul George). Giannis is on Miami. Rui is a Clipper. Darryn Peterson is a Jazz rookie and Darius Acuff Jr. is a King. Every leg is graded on the right team.</p><div class="who">Lesson from Monday: verify team, venue and status first</div></div>
      <div class="flag w"><b>Utah is gutted</b><div class="r warn">4 starters</div><p>Keyonte George, Jaren Jackson Jr. and Nurkic out, Markkanen questionable. Heat -9.5. That's why Heat ML and Bam boards are anchors, and Peterson and Bailey get more shots.</p><div class="who">Giannis probable (wrist)</div></div>
      <div class="flag w"><b>Thunder short-handed</b><div class="r warn">-130 only</div><p>OKC is missing Jalen Williams, Chet, Cason Wallace and more. SGA overs get a boost; OKC ML is just 55%. Josh Hart is out for New York, Da Silva questionable for Orlando.</p><div class="who">Blazers without Morant and Sharpe</div></div>
      <div class="flag"><b>Bad lines we moved</b><div class="r acc">smarter</div><p>Tatum o7.5 reb (he averages 6.0) moves to 5+. Brown o22.5 moves to 15+. Maluach o5.5 to 4+. Buckley 99.5 to 75+. Kentucky ML and Texas Tech ML are faded (both underdogs). KAT threes unders are star unders and stay small.</p><div class="who">Model v2 rules applied</div></div>
    </div>
'''
new=re.sub(r'    <div class="flags" style="margin-bottom:14px">.*?\n    </div>\n',flags,new,1,flags=re.S)
new=new.replace(re.search(r'<h3>Monday tickets.*?</h3>',new) .group(0) if re.search(r'<h3>Monday tickets.*?</h3>',new) else 'XX','<h3>Tuesday tickets · built for Kalshi</h3>')
new=re.sub(r'<h3>tueday tickets[^<]*</h3>','<h3>Tuesday tickets · built for Kalshi</h3>',new)
new=new.replace('Graded 70%+, NBA and NFL only','Graded 70%+, NBA only')
s=s.replace('  <section class="panel reveal" id="marbles">',new+'\n  <section class="panel reveal" id="marbles">',1)
# JS
js=re.search(r'\(function\(\)\{const rb=x=>.*?draw\(\);\}\)\(\);\n',s,re.S).group(0)
tj=js.replace('MON','TUE').replace("'mon","'tue").replace('monPool','tuePool').replace('monAny','tueAny').replace('monReg','tueReg').replace('monF','tueF').replace('monT','tueT')
tj=tj.replace(".filter(r=>r.pct>=70&&!r.fl&&!['Wemby U55 PRA','Wemby U45 PRA'].includes(r.p))",".filter(r=>r.pct>=70&&!r.fl&&r.sp==='NBA')")
tj=tj.replace("['nfl','MNF'],['nba','NBA']","['nba','NBA'],['cbb','College hoops'],['cfb','MACtion'],['move','Moved lines']")
tj=tj.replace("(F==='nfl'&&x.g==='BUF@MIN')||(F==='nba'&&/@(DET|CHA|CLE|ATL|TOR|DAL|HOU|PHX|GSW)$/.test(x.g))","(F==='nba'&&x.sp==='NBA')||(F==='cbb'&&x.sp==='CBB')||(F==='cfb'&&x.sp==='CFB')")
tj=tj.replace("<td style=\"color:#8a9a93;white-space:normal;min-width:180px\">${x.n}</td>","<td style=\"color:#8a9a93;white-space:normal;min-width:180px\">${x.n}${x.mv?`<br><b style=\"color:var(--acc)\">Better: ${x.mv}</b>`:''}</td>")
tix_js="document.getElementById('tueTix').innerHTML=TTIX.map(t=>`<div class=\"st\"><h3 style=\"color:${t.c}\">${t.t}</h3>${t.legs.map(l=>{const r=TUE.find(x=>x.p===l);return `<div class=\"row\"><span>${l}</span><b>${r?r.pct:''}</b></div>`}).join('')}<div class=\"row\"><span>Hit chance</span><b>${t.hit}</b></div><div class=\"row\"><span>Suggested stake</span><b>${t.stake}</b></div><div class=\"row\"><span>Lock at</span><b>${t.lock}</b></div><p class=\"note\" style=\"margin:10px 0 0\">${t.v}</p></div>`).join('');\n"
fl2='const FLN2=Object.assign({},FLN,{STATUS:"Status check",STARU:"Star under",FILL:"Filler",NOLINE:"No line given",CONFLICT:"Both sides picked"});\n'
tj=tj.replace('FLN[x.fl]','FLN2[x.fl]')
data='const TUE='+json.dumps(TUE)+';\nconst TTIX='+json.dumps(TTIX)+';\n'
s=s.replace('/* marbles */',data+fl2+tj+tix_js+'\n/* marbles */',1)
s=s.replace('Nov 9 graded · 350 legs since Nov 4 · Ace +$625 Monday','Tuesday Nov 10 board live · 350 graded legs since Nov 4')
open(P,'w').write(s)
