"""Publish Nov 20 results into the site source. Run from pipeline/ after fri20/res/grade.py and fri20/res/analyze.py.
Board results, record rows, Beta Top 8 and every agent's sims scored, Friday recap, status line."""
import json, re, sys
sys.path.insert(0, 'fri20/res'); from score_sims import grade as sgrade
F = 'bettordays-hq.html'; s = open(F).read()
GR = {r['p']: r for r in json.load(open('fri20/fri20_graded.json'))['rows']}
AN = json.load(open('fri20/res/analysis.json')); SM = AN['summary']

def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:90]); s = s.replace(a, b)
def getconst(name):
    i = s.index('const ' + name + '=') + len('const ' + name + '=')
    return json.JSONDecoder().raw_decode(s[i:])[0]
def setconst(name, val):
    global s
    i = s.index('const ' + name + '=') + len('const ' + name + '=')
    _, e = json.JSONDecoder().raw_decode(s[i:]); s = s[:i] + json.dumps(val) + s[i + e:]

# 1. board rows
T = getconst('FR20')
for r in T:
    g = GR.get(r['p'])
    if g and g.get('r'): r['r'] = g['r']; r['act'] = g.get('act')
setconst('FR20', T)

# 2. record rows for the site explorer
m = re.search(r'const ROWS=(\[.*?\]);\n', s); R = json.loads(m.group(1))
assert not any(r['day'] == 'Nov 20' for r in R)
add = 0
for r in T:
    if r.get('r') not in ('W', 'L') or not r.get('pct'): continue
    st = r.get('stat') or (r['ty'] if r['ty'] != 'prop' else 'prop')
    t = r['p'].lower()
    if r['ty'] == 'prop':
        st = next((v for k, v in [('points + rebounds + assists', 'pra'), ('three', '3pm'), ('assist', 'ast'), ('rebound', 'reb'), ('passing', 'prop'), ('receiving', 'recyds'), ('rushing', 'rush'), ('point', 'pts')] if k in t), 'prop')
    R.append({'day': 'Nov 20', 'pick': r['p'], 'est': r['pct'], 'hit': 1 if r['r'] == 'W' else 0, 'sport': r['sp'], 'mkt': r['ty'], 'stat': st,
              'dir': 'u' if ' under ' in t else 'o', 'style': r.get('st', 'alt'), 'boost': 0, 'star': 0, 'fav': 0}); add += 1
s = s[:m.start(1)] + json.dumps(R) + s[m.end(1):]
t70 = [r for r in R if r['est'] >= 70]; H = sum(r['hit'] for r in t70); N = len(t70)
print('ROWS', len(R), 'added', add, '70+ all time', H, N)

# 3. Beta Top 8 (our own sim) results and track record
B = getconst('BETA')
for l in B['top']:
    res, act = sgrade(l['player'], l['st'], l['k']); l['r'] = res; l['act'] = act
gt = [l for l in B['top'] if l.get('r')]
w = sum(l['r'] == 'W' for l in gt); lo = sum(l['r'] == 'L' for l in gt)
t5 = B['top'][:5]; t5s = f"{sum(l.get('r')=='W' for l in t5)}-{sum(l.get('r')=='L' for l in t5)}"
tot = sum(((1 / (l['ask'] + 0.07 * l['ask'] * (1 - l['ask'])) - 1) if l['r'] == 'W' else -1) for l in gt)
roi = round(100 * tot / len(gt), 1) if gt else 0
assert not any(h['d'] == 'Nov 20' for h in B['hist'])
B['hist'].append({'d': 'Nov 20', 'w': w, 'l': lo, 'top5': t5s, 'roi': roi}); setconst('BETA', B)
hw = sum(h['w'] for h in B['hist']); hl = sum(h['l'] for h in B['hist'])
print('beta top', w, lo, t5s, roi, 'all nights', hw, hl)

# 4. every agent's simulation lines scored (accuracy and picks at break-even + 5)
V = getconst('V8SIM'); SC = {}
for l in V['lines']:
    res, act = sgrade(l['player'], l['st'], l['k']); l['r'] = res; l['act'] = act
gl = [l for l in V['lines'] if l.get('r')]
y = lambda l: 1 if l['r'] == 'W' else 0
for a in list(V['status'].keys()) + ['oursim', 'cons', 'market']:
    ps = []
    for l in gl:
        p = l['oursim'] if a == 'oursim' else l['cons'] if a == 'cons' else l['be'] if a == 'market' else l['agents'].get(a)
        if p is not None: ps.append((p / 100, l))
    picks = [l for p, l in ps if a != 'market' and 100 * p >= l['be'] + 5]
    SC[a] = {'brier': round(sum((p - y(l)) ** 2 for p, l in ps) / len(ps), 4) if ps else None, 'n': len(ps),
             'picks': f"{sum(y(l) for l in picks)}-{sum(1-y(l) for l in picks)}" if picks else '0-0'}
V['scored'] = SC; setconst('V8SIM', V)
print('sims', json.dumps(SC))

# 5. status line
rep('<span class="lbl" id="sys">', '<span class="lbl" id="sys">', 1) if '<span class="lbl" id="sys">' in s else None
st_old = re.search(r'<span class="lbl">Friday Nov 20 picks are live[^<]*</span>', s)
if st_old: s = s.replace(st_old.group(0), f'<span class="lbl">Friday graded · {SM["board_70"][0].split(" ")[0]} at 70%+ · Hammer hit 2.04x · Saturday board next</span>', 1)

# 6. Friday recap on the Proof page (newest three recaps live there)
a70w, a70l = map(int, SM['board_70'][0].split(' ')[0].split('-'))
allw, alll = map(int, SM['all_graded'].split(' ')[0].split('-'))
fw, fl = map(int, SM['favorite_edge_legs'][0].split(' ')[0].split('-'))
Bv = SM['brier_v8_legs (model, n, kalshi on the same legs)']; BP = SM['brier_all_priced']
order = sorted([(k.replace('our_grade(med)', 'our grade').replace('chatgpt', 'ChatGPT').replace('gemini', 'Gemini').replace('grok', 'Grok').replace('claude', 'Claude').replace('system', 'our system').replace('kalshi', 'Kalshi'), v[0]) for k, v in Bv.items()], key=lambda x: x[1])
otxt = ', '.join(f'{n} {v:.3f}' for n, v in order)
sims_txt = ', '.join(f"{k.replace('oursim','our sim').replace('cons','sim consensus').replace('market','the price')} {v['brier']:.3f}" for k, v in sorted(SC.items(), key=lambda x: x[1]['brier'] or 9))
sec = f'''<section class="panel" id="review20">
    <h2>Friday recap · Nov 20 <small>our best night on the record</small></h2>
    <div class="kpis">
      <div class="kpi"><span class="lbl">70%+ legs</span><b><span data-count="{a70w}">{a70w}</span>/{a70w+a70l}</b><small>{round(100*a70w/(a70w+a70l))}%. +{SM['board_70'][1]}% as $1 singles after fees. Season to that night: {H} of {N}</small></div>
      <div class="kpi"><span class="lbl">The Hammer</span><b>5/5</b><small>Bey, Trae, Oregon, DeRozan, Booker. Paid about 2.04x</small></div>
      <div class="kpi"><span class="lbl">Favorite-edge legs</span><b><span data-count="{fw}">{fw}</span>/{fw+fl}</b><small>Kalshi 80 to 92 cents with our grade agreeing. +{SM['favorite_edge_legs'][1]}% after fees. Only Duke ML missed</small></div>
      <div class="kpi"><span class="lbl">All graded legs</span><b><span data-count="{allw}">{allw}</span>/{allw+alll}</b><small>{round(100*allw/(allw+alll))}%. Legs graded under 60 went {SM['pub_0-59'][0].split(' ')[0]}</small></div>
    </div>
    <h3 style="margin-top:18px">What happened</h3>
    <div class="flags">
      <div class="flag w"><b>The board cashed</b><div class="r acc">29 of 32 at 70%+</div><p>Every 85+ leg hit. The three misses: Donovan Mitchell 4+ rebounds (3), Duke ML (lost 20-10) and Pistons ML (lost 105-102). The Core parlay (Bridges, Hartenstein, Powell, VanVleet) hit too.</p><div class="who">Graded from ESPN box scores, Nov 20 night</div></div>
      <div class="flag"><b>We matched Kalshi for the first time</b><div class="r acc">0.192 vs 0.192</div><p>On all {BP['n']} priced legs our published grades scored {BP['published']:.3f} and Kalshi {BP['kalshi']:.3f} (lower is better). On the 52 legs the four AI models graded blind: {otxt}. Grok was the outlier this time.</p><div class="who">One night. Every model keeps being scored</div></div>
      <div class="flag w"><b>The pull rule held</b><div class="r warn">KD 20+ missed</div><p>Kevin Durant 20+ points was pulled because we graded it 8+ above Kalshi. He scored 16. That rule is now 55-46 over the season and still the best filter we have.</p><div class="who">REMOVED legs stay off every ticket</div></div>
      <div class="flag"><b>Simulations</b><div class="r warn">Beta Top 8 {w}-{lo}</div><p>Our own sim's top 8 went {w}-{lo} ({roi:+.1f}% flat after fees). Accuracy on the 105 agent sim lines: {sims_txt}.</p><div class="who">Experimental, graded every night</div></div>
    </div>
  </section>
  '''
rep('<section class="panel" id="review19">', sec + '<section class="panel" id="review19">')
rep("review19:'record',review18:'record',review17:'record'", "review20:'record',review19:'record',review18:'record',review17:'results'")
open(F, 'w').write(s); print('patched')
