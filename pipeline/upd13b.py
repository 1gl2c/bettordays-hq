import json
p='bettordays-hq.html';s=open(p).read()
res={x[2]:x[1] for x in json.load(open('study/nov12_graded.json'))['graded']}
i=s.index('const THU=');j=s.index(';\n',i);a=json.loads(s[i+10:j])
for r in a: r['r']='W' if res[r['p']] else 'L'
s=s[:i+10]+json.dumps(a)+s[j:]
rep=[
('<span data-count="148">0</span>/173</b><small>86% across 9 days · Thursday 22 of 25</small>','<span data-count="154">0</span>/182</b><small>85% across 9 days · Thursday 28 of 34</small>'),
('<span data-count="66">0</span>%</b><small>557 graded legs, all tiers</small>','<span data-count="66">0</span>%</b><small>608 graded legs, all tiers</small>'),
('<div class="k big"><b>86%</b><span>Our 70%+ picks hit, all time<br>148 of 173</span></div>\n      <div class="k"><b>88%</b><span>Thursday<br>22 of 25</span></div>',
 '<div class="k big"><b>85%</b><span>Our 70%+ picks hit, all time<br>154 of 182</span></div>\n      <div class="k"><b>82%</b><span>Thursday<br>28 of 34</span></div>'),
('<b class="acc"><span data-count="22">0</span>/25</b><small>88%. All time: 148 of 173 (86%)</small>','<b class="acc"><span data-count="28">0</span>/34</b><small>82%. All time: 154 of 182 (85%)</small>'),
('<span class="lbl">Last 3 nights at 70%+</span><b class="acc">89%</b><small>Tue 90% · Wed 89% · Thu 88%</small>','<span class="lbl">Last 3 nights at 70%+</span><b class="acc">87%</b><small>Tue 90% · Wed 89% · Thu 82% · 86 of 99</small>'),
('<div class="flag g"><b>Points and assists</b><div class="r acc">6 for 6</div><p>Cade 20+ (52), Naz 15+ (16), Ayo 10+, Bridges 8+, Ausar 2+ and 3+ assists (11). All time: points 44 of 48, assists 10 of 10.</p><div class="who">Still near perfect</div></div>',
 '<div class="flag g"><b>Points and NFL</b><div class="r acc">16 of 18</div><p>Cade 20+ (52), Ayo 10+ and 12+ (18), Naz 15+ (16), Bridges 8+ (11), plus 11 of 12 NFL legs at 70%+. Misses: Sion James 8+ (3) and Ayo 2+ assists (1). All time at 70%+: points 45 of 50, assists 10 of 11.</p><div class="who">Still the core</div></div>'),
('<div class="who">2 of our 3 misses at 70%+</div>','<div class="who">2 of our 6 misses at 70%+</div>'),
('<span class="lbl">Thursday graded · 22 of 25 at 70%+ · Friday board next</span>','<span class="lbl">Thursday fully graded · 28 of 34 at 70%+ · Friday board next</span>'),
("['5-10x real lines (Kalshi)','$59.97','5.53x','L','Four hit. Sion James 10+ the likely miss'],","['5-10x real lines (Kalshi)','$59.97','5.53x','L','Four hit. Sion James 10+ (3 pts) the only miss'],"),
]
for o,n in rep:
  assert o in s,o[:70]; s=s.replace(o,n)
open(p,'w').write(s);print('ok')
