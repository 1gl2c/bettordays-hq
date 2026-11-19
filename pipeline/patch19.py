import re,json
s=open('bettordays-hq.html').read()
assert 'id="thursday"' not in s
TH=json.load(open('study/nov12.json')); P={x['p']:x for x in TH}
L=lambda *a:list(a)
T=[
 dict(t="Power 3 · the core",c="#04ff9f",legs=L("Cade Cunningham 20+ points","Rudy Gobert 8+ rebounds","Phx Suns ML v Hornets"),stake="$120",lock="About 2.3x, take 2.2x or better",v="Your Wednesday build, done again. Three legs 75-82 in three different games. Cade with Ivey and Joe out, Gobert with Lively out, Suns vs a Hornets team missing three starters."),
 dict(t="Hammer · 5 legs",c="#00c8ff",legs=L("Daniels 15+ rush yds","Dean Wade 4+ rebounds","Pistons ML v Wizards","Ayo Dosunmu over 10 points","Okonkwo 2+ rec"),stake="$120",lock="About 2.3x, take 2.0x or better",v="No leg under 80. Daniels ran for 103 in the first meeting. Wizards on a back-to-back. Ayo starts with Ant out."),
 dict(t="2-3x · value",c="#ffb020",legs=L("76ers ML v Raptors","Alex Sarr 4+ rebounds","Naz Reid 15+ points","A. Williams 15+ rec yds"),stake="$80",lock="About 2.8x, take 2.4x or better",v="Raptors on a back-to-back with no Kawhi, Barnes or Jackson-Davis. Naz gets shots with three Hornets out. Washington's WR room is empty, so Williams gets targets."),
 dict(t="5-10x · real lines",c="#ff4d5e",legs=L("Skattebo 30+ rush","White 40+ R+R","Zvada 5+ kick pts","Sion James 8+ pts","Ausar 3+ ast","Timberwolves ML v Mavericks"),stake="$60",lock="About 6x, take 5x or better",v="Every leg 66-72, no coin flips. Six different spots."),
 dict(t="100x · the 50-60 zone",c="#c77dff",legs=L("Washighton Comanders ML v Giants","Malik Nabers 50+ receiving yards","Naz Reid 20+ points","WAS / NY Giants over 40 total points","Daniel Gafford 10+ points","Ayo Dosunmu over 15 points","Charlotte Hornets v Phx Suns under 220","Jayden Daniels Under 0.5 Interceptions"),stake="$10",lock="80x or better",v="Only legs we grade a bit above where Kalshi should price them. Check each leg's Kalshi %: if one shows 75+, swap it out."),
]
for t in T:
  for l in t['legs']: assert l in P,l
  h=1
  for l in t['legs']: h*=P[l]['pct']/100
  t['hit']=f"About {round(h*100)}%" if h>.1 else f"About 1 in {round(1/h)}"
  print(t['t'],t['hit'])
# section
a=s.index('  <section class="panel" id="wednesday">');b=s.index('  <section class="panel" id="review10">')
sec=s[a:b].replace('id="wednesday"','id="thursday"')
for k in ['wedTix','wedPool','wedAny','wedReg','wedF','wedT']: sec=sec.replace(k,k.replace('wed','thu'))
sec=re.sub(r'<h2>Wednesday board.*?</h2>','<h2>Thursday board · Nov 12 <small>92 capper picks + 14 moved lines · 4 NBA games, TNF Commanders at Giants, NHL</small></h2>',sec,flags=re.S)
i=sec.index('<div class="flags"');j=sec.index('<h3>',i)
sec=sec[:i]+'''<div class="flags" style="margin-bottom:14px">
      <div class="flag w"><b>Out tonight</b><div class="r warn">checked</div><p>Anthony Edwards, DiVincenzo (MIN). Lively (DAL). Miller, Knueppel, Schroder (CHA). Kawhi, Barnes, Jackson-Davis (TOR). Duren, Ivey, Joe (DET). LeBron (PHI). McLaurin, Dyami Brown on IR (WAS).</p><div class="who">Embiid questionable · Skattebo expected back</div></div>
      <div class="flag"><b>Back-to-backs</b><div class="r warn">flagged</div><p>Raptors and Wizards both played last night. AD props are flagged: he could sit.</p><div class="who">Fade tired teams, not tired stars</div></div>
      <div class="flag"><b>Rosters moved</b><div class="r warn">verified</div><p>Naz Reid is a Hornet. Ayo Dosunmu is a Wolf and starting. Miles Bridges is a Sun. Trae Young and AD are Wizards. J.J. McCarthy starts for the Giants.</p><div class="who">Graded on the right team</div></div>
      <div class="flag g"><b>TNF read</b><div class="r acc">Giants -1.5 · 42.5</div><p>Daniels ran for 103 in the first meeting and has 0 picks all year. Washington's top WRs are hurt, so Okonkwo, Antonio Williams and White soak up targets.</p><div class="who">Coin-flip side, props are the play</div></div>
    </div>
    '''+sec[j:]
sec=re.sub(r'<h3>Wednesday tickets.*?</h3>','<h3>Thursday tickets · Model v4 · $390 plan</h3>',sec)
sec=sec.replace('Hit chances use our real top-tier rate (about 88% per leg), not the raw grades.','Hit chances multiply our raw grades.')
s=s.replace('  <section class="panel" id="review11">',sec+'  <section class="panel" id="review11">',1)
# drop nextboard placeholder
a=s.index('  <section class="panel" id="nextboard">');b=s.index('  <section class="panel" id="thursday">')
s=s[:a]+s[b:]
# JS clone
a=s.index('const WED=');b=s.index("document.getElementById('wedTix').innerHTML");e=s.index('\n',b)+1
js=s[a:e].replace('WED','THU').replace('WTIX','HTIX').replace("'2026-11-11'","'2026-11-12'")
for k in ['wedTix','wedPool','wedAny','wedReg','wedF','wedT']: js=js.replace(k,k.replace('wed','thu'))
js=re.sub(r'const THU=\[.*?\];\n',lambda m:'const THU='+json.dumps(TH)+';\n',js,count=1,flags=re.S)
js=re.sub(r'const HTIX=\[.*?\];\n',lambda m:'const HTIX='+json.dumps(T)+';\n',js,count=1,flags=re.S)
js=js.replace('<div class="row"><span>Stake</span><b>${t.stake}</b></div><div class="row"><span>Result</span><b>${t.lock}</b></div>','<div class="row"><span>Hit chance</span><b>${t.hit}</b></div><div class="row"><span>Stake</span><b>${t.stake}</b></div><div class="row"><span>Lock at</span><b>${t.lock}</b></div>')
s=s[:e]+js+s[e:]
s=s.replace("const MAP={drop:'home',nextboard:'home',review11:'home',","const MAP={drop:'home',thursday:'home',review11:'home',")
s=s.replace("Thursday board drops 2 PM PT · 502 graded legs since Nov 4","Thursday Nov 12 board live · 502 graded legs since Nov 4")
s=s.replace("const S=[['.nav [data-go=\"home\"]'","const S=[['.nav [data-go=\"home\"]'")
open('bettordays-hq.html','w').write(s)
print('ok')
