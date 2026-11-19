import re,json
s=open('bettordays-hq.html').read()
assert 'id="wednesday"' not in s
W=json.load(open('study/nov11.json'))
P={x['p']:x for x in W}
def prod(legs,key): 
  r=1
  for l in legs: r*=key(l)
  return r
TIX=[
 dict(t="Hammer · 5 legs",c="#04ff9f",legs=["LA Lakers ML","Nikola Jokic double double","Franz Wagner over 15 points","Alperen Senguun over 15 points","Houston Rockets ML"],stake="$140",lock="About 2.3x on Kalshi, take 2.1x or better",v="Two moneylines the market already loves, plus three stars in great spots. Bucks have no Turner, Warriors are missing four guys, Jazz are gutted. No leg under 74."),
 dict(t="2x · anchors",c="#00c8ff",legs=["Yaxel LEnderborg 20+ PRA","SA Spurs ML","Jalen Brunson 20+ points","Anthony Davis over 15 points","MPJ 15+ pts"],stake="$120",lock="About 2.1x, take 2.0x or better",v="Zero overlap with the hammer. Lendeborg averages 32 PRA with Butler and Porzingis out. MPJ moved from 21.5 down to 15."),
 dict(t="5-10x · real lines",c="#ffb020",legs=["Evan Mobley over 15 points","Jayson Tatum 20+ points","Walker Kessler over 8 rebounds","Boozer 7+ reb","Boston Celtics ML"],stake="$100",lock="About 5.5x, take 5x or better",v="Every leg 62 to 74. No coin flips. Kessler gets a Bucks team with no Myles Turner. Tatum and the Celtics ML move together."),
 dict(t="Lotto · 13 legs · about 20x",c="#ff4d5e",legs=["Draymond Green Over 9.5 Pts + Reb","Neemias Queta 4+ rebounds","Alex Sarr over 4 rebounds","Zion Williamson 15+ points","Stephon Castle 4+ rebounds","Mikal Bridges o2.5 REB","Brayden Burries over 0.5 3 pointers made","Payton Pritchard over 20+ PRA","Donovan Mitchell 20+ points","SGA 20+ pts","Boston Celtics ML","Hartenstein 6+ reb","Julius Randle 15+ points"],stake="$30",lock="20x or better",v="Built from legs that aren't on the main tickets. Celtics ML is the only repeat (2 tickets max)."),
 dict(t="100x · optional",c="#c77dff",legs=["Draymond Green Over 9.5 Pts + Reb","Neemias Queta 4+ rebounds","Alex Sarr over 4 rebounds","Zion Williamson 15+ points","Stephon Castle 4+ rebounds","Mikal Bridges o2.5 REB","Brayden Burries over 0.5 3 pointers made","Payton Pritchard over 20+ PRA","Donovan Mitchell 20+ points","SGA 20+ pts","Hartenstein 6+ reb","Julius Randle 15+ points","Franz Wagner over 20 points","Desmond Bane 2 + 3 pointers made","Julius Randle over 4 assists"],stake="$10",lock="90x or better",v="The lotto plus three real lines in the 60s. Fun money only."),
]
for t in TIX:
  for l in t['legs']: assert l in P,l
  h=prod(t['legs'],lambda l:P[l]['pct']/100)
  t['hit']=f"About {round(h*100)}%" if h>.1 else f"About 1 in {round(1/h)}"
s=s.replace('  <section class="panel" id="review10">', open('wed_section.html').read()+'\n  <section class="panel" id="review10">',1)
js=open('wed_js.js').read().replace('__WED__',json.dumps(W)).replace('__WTIX__',json.dumps(TIX))
s=s.replace('/* daily drop countdown, Pacific time */',js+'\n/* daily drop countdown, Pacific time */',1)
s=s.replace('<a class="btn" href="#drop">Next drop</a>','<a class="btn" href="#drop">Next drop</a><a class="btn" href="#wednesday">Wednesday</a>')
s=re.sub(r'Wednesday Nov 11 · board drops 2 PM PT · ','Wednesday Nov 11 board live · ',s)
open('bettordays-hq.html','w').write(s)
for t in TIX: print(t['t'],t['hit'])
