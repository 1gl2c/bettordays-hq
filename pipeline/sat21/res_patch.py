"""Publish Nov 21 results into the site source. Run from pipeline/ after sat21/res/grade.py and sat21/res/analyze.py.
Board results, record rows, our sim's Top 10 scored, Saturday recap on Proof, status line."""
import json, re, sys
sys.path.insert(0, 'sat21/res'); from score_sims import grade as sgrade
F = 'bettordays-hq.html'; s = open(F).read()
GR = {r['p']: r for r in json.load(open('sat21/sat21_graded.json'))['rows']}
AN = json.load(open('sat21/res/analysis.json')); SM = AN['summary']; AL = {l['p']: l for l in AN['legs']}

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

# 1. board rows and the full grade sheet get their results
T = getconst('SA21')
for r in T:
    g = GR.get(r['p'])
    if g and g.get('r'): r['r'] = g['r']; r['act'] = g.get('act')
setconst('SA21', T)
m = re.search(r'const V7D=(\{.*?\});\n', s); V = json.loads(m.group(1))
for x in V.get('all', []):
    g = GR.get(x['p'])
    if g and g.get('r'): x['r'] = g['r']; x['act'] = g.get('act')
s = s.replace(m.group(0), 'const V7D=' + json.dumps(V) + ';\n')

# 2. record rows for the site explorer (published legs only; REMOVED and voids stay out)
m = re.search(r'const ROWS=(\[.*?\]);\n', s); R = json.loads(m.group(1))
assert not any(r['day'] == 'Nov 21' for r in R)
add = 0
for p, l in AL.items():
    if l['tier'] not in ('G', 'Y', 'N') or l['pub'] is None or l['r'] not in ('W', 'L'): continue
    t = p.lower()
    st = l['ty'] if l['ty'] != 'prop' else next((v for k, v in [('rebounds + assists', 'ra'), ('assist', 'ast'), ('rebound', 'reb'), ('passing', 'prop'), ('receiving', 'recyds'), ('rushing', 'rush'), ('point', 'pts'), ('decision', 'prop')] if k in t), 'prop')
    R.append({'day': 'Nov 21', 'pick': p, 'est': l['pub'], 'hit': 1 if l['r'] == 'W' else 0, 'sport': l['sp'], 'mkt': l['ty'], 'stat': st,
              'dir': 'u' if ' under ' in t else 'o', 'style': 'alt', 'boost': 0, 'star': 0, 'fav': 0}); add += 1
s = s[:m.start(1)] + json.dumps(R) + s[m.end(1):]
t70 = [r for r in R if r['est'] >= 70]; H = sum(r['hit'] for r in t70); N = len(t70)
print('ROWS', len(R), 'added', add, '70+ all time', H, N)

# 3. our sim's Top 10 results and track record
B = getconst('BETA')
for l in B['top']:
    res, act = sgrade(l['player'], l['st'], l['k']); l['r'] = res; l['act'] = act
gt = [l for l in B['top'] if l.get('r')]
w = sum(l['r'] == 'W' for l in gt); lo = sum(l['r'] == 'L' for l in gt)
t5 = B['top'][:5]; t5s = f"{sum(l.get('r') == 'W' for l in t5)}-{sum(l.get('r') == 'L' for l in t5)}"
askp = lambda a: a if a <= 1 else a / 100
roi = round(100 * sum(((1 / (askp(l['ask']) + 0.07 * askp(l['ask']) * (1 - askp(l['ask']))) - 1) if l['r'] == 'W' else -1) for l in gt) / len(gt), 1) if gt else 0
assert not any(h['d'] == 'Nov 21' for h in B['hist'])
B['hist'].append({'d': 'Nov 21', 'w': w, 'l': lo, 'top5': t5s, 'roi': roi}); setconst('BETA', B)
hw = sum(h['w'] for h in B['hist']); hl = sum(h['l'] for h in B['hist'])
print('sim top', w, lo, t5s, roi, 'all nights', hw, hl)

# 4. status line
st_old = re.search(r'<span class="lbl">Saturday Nov 21 picks are live[^<]*</span>', s)
if st_old: s = s.replace(st_old.group(0), f'<span class="lbl">Saturday graded · {SM["board_70"][0].split(" ")[0]} at 70%+ · Safe Hammer hit · Sunday board next</span>', 1)

# 5. Saturday recap on the Proof page
bw, bl = map(int, SM['board_70'][0].split(' ')[0].split('-'))
pw, pl = map(int, SM['all_published'][0].split(' ')[0].split('-'))
fw, fl = map(int, SM['favorite_edge_legs'][0].split(' ')[0].split('-'))
Bb = SM['brier']; BK = Bb['books_vs_others_same_legs']
ais = sorted([(n, Bb[k]['brier_priced']) for k, n in [('chatgpt', 'ChatGPT'), ('gemini', 'Gemini'), ('grok', 'Grok'), ('claude', 'Claude')]], key=lambda x: x[1])
aitxt = ', '.join(f'{n} {v:.3f}' for n, v in ais)
sec = f'''<section class="panel" id="review21">
    <h2>Saturday recap · Nov 21 <small>the Safe Hammer cashed, two legs on the board missed</small></h2>
    <div class="kpis">
      <div class="kpi"><span class="lbl">70%+ legs</span><b><span data-count="{bw}">{bw}</span>/{bw + bl}</b><small>{round(100 * bw / (bw + bl))}%. {SM['board_70'][1]:+.1f}% as $1 singles after fees. Season: {H} of {N}</small></div>
      <div class="kpi"><span class="lbl">Safe Hammer</span><b>2/2</b><small>Cooper Flagg 4+ assists (8) and Joel Embiid 6+ rebounds (17). About 1.45x after fees</small></div>
      <div class="kpi"><span class="lbl">Favorite-edge legs</span><b><span data-count="{fw}">{fw}</span>/{fw + fl}</b><small>Kalshi 80 to 92 cents with our grade agreeing. Celtics ML lost by 1</small></div>
      <div class="kpi"><span class="lbl">Every published leg</span><b><span data-count="{pw}">{pw}</span>/{pw + pl}</b><small>{round(100 * pw / (pw + pl))}%, all sports, under 70 included. NBA {SM['by_sport_published']['NBA'].split(' ')[0]}, college football {SM['by_sport_published']['CFB'].split(' ')[0]}</small></div>
    </div>
    <h3 style="margin-top:18px">What happened</h3>
    <div class="flags">
      <div class="flag"><b>The two misses</b><div class="r warn">Celtics ML, LaMelo 15+</div><p>The Kings beat Boston 97-96 on the second night of a back-to-back. LaMelo Ball scored 12 with Anthony Edwards out. Both were GREEN with Kalshi at or above our grade, so the market missed them too.</p><div class="who">Graded from ESPN box scores, Nov 21 night</div></div>
      <div class="flag"><b>Accuracy (lower is better)</b><div class="r acc">Our system {Bb['system']['brier_priced']:.3f} · Kalshi {Bb['kalshi']['brier_priced']:.3f}</div><p>On the {Bb['kalshi']['n']} priced legs graded before their games: our own system {Bb['system']['brier_priced']:.3f}, Kalshi {Bb['kalshi']['brier_priced']:.3f}, our blended grade {Bb['our_grade']['brier_priced']:.3f}. The four AIs: {aitxt}. The AIs pulled our blend away from the market on a hard college slate.</p><div class="who">Every model keeps being scored</div></div>
      <div class="flag"><b>First night with sportsbook prices</b><div class="r acc">{BK['n']} NBA props</div><p>On the same {BK['n']} legs: books {BK['books']:.3f}, Kalshi {BK['kalshi']:.3f}, our grade {BK['our_grade']:.3f}. Both Safe Hammer legs were priced higher by the books than by Kalshi, and both hit.</p><div class="who">Books shown on the grade sheet from Nov 21</div></div>
      <div class="flag"><b>Pulled legs</b><div class="r warn">3-2</div><p>Kris Dunn 2+ rebounds hit (4) after we pulled it for grading 14 above Kalshi. Prochazka and Gaziev were pulled and lost. The rule keeps running and keeps being graded.</p><div class="who">REMOVED legs stay off every ticket</div></div>
      <div class="flag"><b>Our Python sim</b><div class="r warn">Top 10 {w}-{lo}</div><p>Accuracy on 80 near-even lines: our sim 0.252, Kalshi 0.258, the second night in a row it beat the price. Its Top 10 went {w}-{lo} ({roi:+.1f}% flat after fees). All nights: {hw}-{hl}.</p><div class="who">Experimental, graded every night</div></div>
    </div>
  </section>
  '''
rep('<section class="panel" id="review20">', sec + '<section class="panel" id="review20">')
rep("review20:'record',review19:'record',review18:'record',review17:'results'", "review21:'record',review20:'record',review19:'record',review18:'results',review17:'results'")
open(F, 'w').write(s); print('patched')
