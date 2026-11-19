import json,re
P='bettordays-hq.html'; s=open(P).read()
G=json.load(open('nov9_graded.json'))
# ROWS append
m=re.search(r'const ROWS=(\[.*?\]);\n',s); R=json.loads(m.group(1))
nfl=lambda g:g=='BUF@MIN'
for x in G:
    if x['p']=='Luka U34.5 pts': continue
    R.append({"day":"Nov 9","pick":x['p'],"est":x['pct'],"hit":1 if x['r']=='W' else 0,"sport":"NFL" if nfl(x['g']) else "NBA","mkt":"ml" if x['ty']=='ml' else "prop","stat":x['ty'],"dir":"u" if (' U' in x['p'] or ' u' in x['p'] or x['p'].startswith('Under')) else "o","style":x['st'] if x['st'] in ('alt','reg','ceil') else 'reg',"boost":0,"star":0,"fav":1 if x['ty']=='ml' else 0})
s=s.replace(m.group(1),json.dumps(R))
n=len(R); h=sum(r['hit'] for r in R); pct=round(100*h/n)
t70=[r for r in R if r['est']>=70]; h70=sum(r['hit'] for r in t70)
print(n,h,pct,h70,len(t70))
s=s.replace("['Nov 8','Nov 8']];","['Nov 8','Nov 8'],['Nov 9','Nov 9']];")
s=s.replace('Monday Nov 9 board live · 295 graded legs since Nov 4',f'Nov 9 graded · {n} legs since Nov 4 · Ace +$625 Monday')
s=s.replace('<span data-count="5">0</span>-2</b><small>hammers and main parlays, Nov 4 to 8</small>','<span data-count="7">0</span>-3</b><small>hammers and main parlays, Nov 4 to 9</small>')
s=s.replace('+$<span data-count="1527">0</span></b><small>after Sunday\'s two 5-legs cashed</small>','+$<span data-count="2207">0</span></b><small>after Monday\'s 9-leg and Hammer 2.0 cashed</small>')
s=s.replace(f'<span data-count="52">0</span>/61</b><small>85% across 5 days</small>',f'<span data-count="{h70}">0</span>/{len(t70)}</b><small>{round(100*h70/len(t70))}% across 6 days</small>')
s=s.replace('<span data-count="62">0</span>%</b><small>295 graded legs, all tiers</small>',f'<span data-count="{pct}">0</span>%</b><small>{n} graded legs, all tiers</small>')
s=s.replace('<span data-count="0">0</span>/11</b>','<span data-count="0">0</span>/15</b>')
# DAYS
s=s.replace("const DAYS=[\n","""const DAYS=[
 {d:'Mon Nov 9 · NBA, MNF',pl:'+$625',tix:[
  ['Hammer 2.0 · no Cavs (Kalshi)','$190.96','2.77x','W','Lakers, Warriors, Spurs ML, Booker 15+, Allen u25 comps, Cook 50+. Paid $529.23'],
  ['Ace 9-leg (Kalshi)','$99.99','5.22x','W','Paid $522.46'],
  ['Original hammer (Kalshi)','$119.99','2.16x','L','Cavs lost 124-112 at Charlotte, Wemby 54 PRA on a U50. Cashed out at $39.06'],
  ['13-leg (Kalshi)','$19.93','51x','L','Cavs, Wemby U50'],
  ['Madness + spice (Kalshi)','$9.88','100x+','L','Cavs, Wemby U50, Bridges, George PRA, Wentz 15+'],
  ['100x lotto #1 · Bills TD','$9.97','98x','L','Cavs, Wemby U50, Allen/JJ/DJ Moore TDs'],
  ['No TDs, no Cavs','$14.93','80x+','L','Wemby U50, Bridges and George PRA, Wentz 15+, Sengun, Siakam'],
 ]},
""",1)
# rules
s=s.replace("const RULES=[\n","""const RULES=[
 ['Never take unders on Wemby or Luka','Wemby 40/11/3 (54 PRA) killed U50. Luka went 32/8/10 the night we had him out. Ace\\'s rule.','Set Nov 9',0],
 ['Ace\\'s gut on a bad team kills the leg','He called the Cavs. They lost by 12 and took four tickets with them.','Set Nov 9',0],
 ['Verify team, home and away, status at lock','Cavs were on the road, Bridges plays for Phoenix, Luka played.','Set Nov 9',0],
 ['No 90%+ filler legs','Under 64 at 97% added almost nothing to the price. Swap for a 70s leg that pays.','Set Nov 9',0],
 ['NBA regular lines in the 45-60 zone','7 of 8 Monday: Kessler, Harper, Castle, Collins, Walter, DeRozan, Murray. NFL in that zone: 1 of 7.','Testing Nov 9',1],
""",1)
s=s.replace("['Backup QB: no receivers, no pass overs','Ravens with Fagnano: 57 receiving yards.','Set Nov 5',0]","['Backup QB: no receivers, no pass overs','Fagnano: 57 receiving yards. Wentz Nov 9: 14 of 32, 139 yards, 0 TDs.','Set Nov 5',0]")
s=s.replace("['Fade PRA combos and assist overs in the 50s','1 of 6 and 5 of 12.','Testing',1]","['Fade PRA combos, even at 80%','Bridges and George both missed 20+ PRA Monday after we overrode the flag.','Set Nov 9',0]")
open(P,'w').write(s)
