"""Publish Nov 25 results into the site source (run from pipeline/ after wed25/res/grade.py and the ledger load).
Board and grade sheet, record rows, our sim's Top, the paper trackers (Safe Hammer, Miracle, Edge Lab, Daily 2x), status line,
Wednesday recap. Thursday NFL legs on this board stay pending until tomorrow night."""
import json, re, sys
sys.path.insert(0, '.')
from wed25.res_calc import grade, M, RS
F = 'bettordays-hq.html'; s = open(F).read()
LED = [r for r in json.load(open('ledger/ledger_rows.json')) if r['result'] in ('W', 'L')]
def rep(a, b):
    global s; assert s.count(a) == 1, a[:80]; s = s.replace(a, b)
def getconst(n):
    i = s.index('const ' + n + '=') + len('const ' + n + '='); return json.JSONDecoder().raw_decode(s[i:])[0]
def setconst(n, v):
    global s; i = s.index('const ' + n + '=') + len('const ' + n + '='); _, e = json.JSONDecoder().raw_decode(s[i:]); s = s[:i] + json.dumps(v) + s[i + e:]
# 1. board rows and the full grade sheet
T = getconst('WE25')
for r in T:
    g, a = grade(r['p'])
    if g: r['r'] = g; r['act'] = a
setconst('WE25', T)
m = re.search(r'const V7D=(\{.*?\});\n', s); V = json.loads(m.group(1))
for x in V['all']:
    g, a = grade(x['p'])
    if g: x['r'] = g; x['act'] = a
s = s.replace(m.group(0), 'const V7D=' + json.dumps(V) + ';\n')
# 2. record rows (published legs graded tonight; Thursday legs get added tomorrow)
m = re.search(r'const ROWS=(\[.*?\]);\n', s); R = json.loads(m.group(1)); assert not any(r['day'] == 'Nov 25' for r in R)
for l in M['legs']:
    g = RS.get(l['i'])
    if l.get('tier') not in ('G', 'Y', 'N') or l.get('pub') is None or not g or g['r'] not in ('W', 'L'): continue
    t = l['p'].lower(); st = l.get('stat') or l.get('ty')
    R.append({'day': 'Nov 25', 'pick': l['p'], 'est': l['pub'], 'hit': 1 if g['r'] == 'W' else 0, 'sport': l['sp'], 'mkt': l.get('ty'), 'stat': st,
              'dir': 'u' if ' under ' in t else 'o', 'style': 'alt', 'boost': 0, 'star': 0, 'fav': 0})
s = s[:m.start(1)] + json.dumps(R) + s[m.end(1):]
t70 = [r for r in R if r['est'] >= 70]; H = sum(r['hit'] for r in t70); N = len(t70)
pub = [l for l in M['legs'] if l.get('tier') in ('G', 'Y', 'N') and l.get('pub') is not None and RS.get(l['i'], {}).get('r') in ('W', 'L')]
b70 = [l for l in pub if l['pub'] >= 70]; bw = sum(RS[l['i']]['r'] == 'W' for l in b70); pw = sum(RS[l['i']]['r'] == 'W' for l in pub)
k80n = [l for l in M['legs'] if (l.get('k') or 0) >= 80 and RS.get(l['i'], {}).get('r') in ('W', 'L')]; k80w = sum(RS[l['i']]['r'] == 'W' for l in k80n)
# 3. our sim's Top lines
B = getconst('BETA'); SN = {'pts': 'points', 'reb': 'rebounds', 'ast': 'assists', '3pm': 'threes', 'pra': 'PRA'}
for l in B['top']:
    r, a = grade(f"{l['player']} {l['k']}+ {SN[l['st']]}"); l['r'] = None if r == 'V' else r; l['act'] = None if r == 'V' else a
gt = [l for l in B['top'] if l.get('r')]; w = sum(l['r'] == 'W' for l in gt); lo = len(gt) - w
t5 = [l for l in B['top'][:5] if l.get('r')]; t5s = f"{sum(l['r'] == 'W' for l in t5)}-{sum(l['r'] == 'L' for l in t5)}"
askp = lambda a: a if a <= 1 else a / 100
roi = round(100 * sum(((1 / (askp(l['ask']) + 0.07 * askp(l['ask']) * (1 - askp(l['ask']))) - 1) if l['r'] == 'W' else -1) for l in gt) / len(gt), 1)
assert not any(h['d'] == 'Nov 25' for h in B['hist']); B['hist'].append({'d': 'Nov 25', 'w': w, 'l': lo, 'top5': t5s, 'roi': roi}); setconst('BETA', B)
BH = getconst('BETAH'); assert not any(h['d'] == 'Nov 25' for h in BH)
BH.append({'d': 'Nov 25', 'rec': B['hist'][-1], 'picks': [{'p': f"{l['player']} {l['k']}+ {SN[l['st']]}", 'g': l.get('g', ''), 'k': round(askp(l['ask']) * 100), 'sim': round(l['sim']), 'r': l.get('r'), 'act': l.get('act')} for l in B['top']]}); setconst('BETAH', BH)
hw = sum(h['w'] for h in B['hist']); hl = sum(h['l'] for h in B['hist'])
bkn = [l for l in gt if l.get('bk') is not None and l['bk'] > 100 * askp(l['ask'])]
# 4. paper trackers
MIR = getconst('MIR')
for grp in [MIR['legs'], MIR['lad']['legs']]:
    for l in grp: l['r'], l['act'] = grade(l['p'])
live = [l for l in MIR['legs'] if l['r'] != 'V']; mw = sum(l['r'] == 'W' for l in live)
MIR['res'] = 'W' if mw == len(live) else 'L'; setconst('MIR', MIR)
P = getconst('PAPER'); p25 = next(x for x in P if x['d'] == 'Nov 25'); p25['ham']['res'] = 'L'; p25['mir']['res'] = MIR['res']; setconst('PAPER', P)
EL = getconst('EL'); e = next(x for x in EL if x['d'] == 'Nov 25')
res = lambda legs: 'V' if all(l['res'] == 'V' for l in legs) else ('L' if any(l['res'] == 'L' for l in legs) else 'W')
for p in e['par']:
    for l in p['legs']: l['res'], l['act'] = grade(l['p'])
    p['res'] = res(p['legs'])
for x in e['sing']: x['res'], x['act'] = grade(x['p'])
for l in e['two']['legs']: l['res'], l['act'] = grade(l['p'])
e['two']['res'] = res(e['two']['legs']); setconst('EL', EL)
pp = sum((p['stake'] * (p['pays'] - 1) if p['res'] == 'W' else -p['stake']) for p in e['par']); sp = sum((x['stake'] * (x['pays'] - 1) if x['res'] == 'W' else -x['stake']) for x in e['sing'])
pr = f"{sum(p['res'] == 'W' for p in e['par'])}-{sum(p['res'] == 'L' for p in e['par'])}"; sr = f"{sum(x['res'] == 'W' for x in e['sing'])}-{sum(x['res'] == 'L' for x in e['sing'])}"
# 5. ledger clues
PL = [r for r in LED if r['priced_pregame'] and r['kalshi_pick'] is not None]
def band(lo_, hi):
    x = [r for r in PL if lo_ <= r['kalshi_pick'] < hi]; wv = sum(r['result'] == 'W' for r in x)
    return wv, len(x) - wv, round(100 * wv / len(x)), round(sum(r['kalshi_pick'] for r in x) / len(x))
k80, k70 = band(80, 101), band(70, 80)
bk = [r for r in PL if r.get('books_pick') is not None and r['books_pick'] - r['kalshi_pick'] >= 3]; bkw = sum(r['result'] == 'W' for r in bk)
bkt = [r for r in bk if r['slate_date'] == '2026-11-25']; bktw = sum(r['result'] == 'W' for r in bkt)
nfl = [r for r in LED if r['sport'] == 'NFL']; nflw = sum(r['result'] == 'W' for r in nfl)
# 6. status line and the Wednesday recap
rep('<span class="lbl">Wednesday Nov 25 picks are live · Engine v8 · 45 legs at 70+ · Hammer: 3 legs</span>',
    f'<span class="lbl">Wednesday graded · {bw}-{len(b70) - bw} at 70%+ · Safe Hammer 5 of 6, Love 2 yards short · Thanksgiving board next</span>')
fm = lambda v: f"+${round(v):,}" if v >= 0 else f"-${round(-v):,}"
sec = f'''<section class="panel" id="review25">
    <h2>Wednesday recap · Nov 25 <small>{bw}-{len(b70) - bw} on the board, the Safe Hammer missed by 2 passing yards</small></h2>
    <div class="kpis">
      <div class="kpi"><span class="lbl">70%+ legs</span><b><span data-count="{bw}">{bw}</span>/{len(b70)}</b><small>Misses: Love 200+ passing yards (198), Stafford 200+ (140), Golden 50+ yards and 5+ catches, Packers +10 (lost by 13), Kuminga 1+ threes (0), Ajay Mitchell under 25 (scored 25), Ty Jerome 2+ threes (1), MPJ 15+ (12), Josh Hart under 8 assists (11). Three Thursday legs are still to play. Season: {H} of {N}</small></div>
      <div class="kpi"><span class="lbl">Safe Hammer</span><b>5/6</b><small>Every NBA leg hit: Ajay Mitchell under 8 assists (3), Shamet 1+ threes (3), Mikel Brown 2+ assists (2), Stewart 2+ rebounds (3), Giddey 6+ assists (7). Jordan Love threw for 198 as the Rams ran it 44 times</small></div>
      <div class="kpi"><span class="lbl">Kalshi 80 cents and up</span><b><span data-count="{k80w}">{k80w}</span>/{len(k80n)}</b><small>Love yards, Ajay Mitchell under 25, MPJ 15+ and Hart under 8 assists missed</small></div>
      <div class="kpi"><span class="lbl">Every published leg</span><b><span data-count="{pw}">{pw}</span>/{len(pub)}</b><small>{round(100 * pw / len(pub))}%, under 70 included</small></div>
    </div>
    <div class="flags" style="margin-top:14px">
      <div class="flag"><b>What we changed for the next NBA night</b><div class="r acc">Safe Hammer: NBA legs only</div><p>The NBA side of the Hammer went 5 for 5 and the one football leg sank it. Our record already showed NFL legs hitting {round(100 * nflw / len(nfl))}% ({nflw} of {len(nfl)}), the weakest group we track. From now on the Safe Hammer uses NBA legs only, until an NFL group earns its way back in the data. Thanksgiving has no NBA games, so there is no Safe Hammer on Thursday.</p><div class="who">Self-learning Hammer rule, Nov 25</div></div>
      <div class="flag"><b>Self-learning update</b><div class="r acc">Points in, rebounds out</div><p>Points legs at 80 to 92 cents moved to prefer: 25 of 28 (89%), above their price after fees. Rebounds moved to block: 24 of 28 (86%), right at their price after fees, so no edge. Assists stay preferred at 32 of 35 (91%).</p><div class="who">hammer_learn, rebuilt every night</div></div>
      <div class="flag"><b>Daily 2x</b><div class="r acc">Cashed · {e['two']['pays']}x</div><p>Giddey 6+ assists (7), Shamet 2+ threes (3) and McDaniels 2+ assists (5) all hit. First graded night for the Daily 2x.</p><div class="who">Paper, Edge Lab</div></div>
      <div class="flag"><b>Edge Lab, night two</b><div class="r warn">Parlays {pr} · singles {sr}</div><p>Gillespie 5+ points (5) with Sabonis 10+ rebounds (10) cashed. Love and Hield (9 points) sank Parlay 1, Ajay Mitchell scoring exactly 25 sank Parlay 3. Paper: parlays {fm(pp)}, singles {fm(sp)} on $2,000 each.</p><div class="who">Paper tracker, home page</div></div>
      <div class="flag"><b>Miracle Parlay</b><div class="r warn">{mw} of {len(live)}</div><p>Jalen Smith sat, so his two legs void. Avdija 6+ assists (7), Maluach 6+ rebounds (6), Castle 20+ points (20), Davion Mitchell 3+ threes (3) and Wemby 30+ (44) hit. Simons (6), Eason (7), Bassey (7 rebounds) and Jaylen Brown (1 rebound) missed.</p><div class="who">Paper ticket, $10 a night</div></div>
      <div class="flag"><b>Perfect 3 attempt</b><div class="r acc">2 of 2 so far</div><p>Love under 350 passing yards (198) and Maxey 1+ threes (3) hit. Goff 200+ passing yards plays Thursday at 10:00 AM PT. The 10x attempt is out: Stafford threw for 140 and Kuminga went 0 for 3 from three.</p><div class="who">Research page, learning model</div></div>
    </div>
    <h3 style="margin-top:18px">Where the edge is <small>every night since Nov 16, only legs priced before the game</small></h3>
    <div class="flags">
      <div class="flag"><b>Kalshi 80 cents and up</b><div class="r acc">{k80[0]}-{k80[1]} · {k80[2]}%</div><p>Priced at {k80[3]} cents on average and hit {k80[2]}%.</p><div class="who">Ledger, every graded night</div></div>
      <div class="flag"><b>Kalshi 70 to 79 cents</b><div class="r warn">{k70[0]}-{k70[1]} · {k70[2]}%</div><p>Priced at {k70[3]} cents, hit {k70[2]}%. Only with the books above Kalshi.</p><div class="who">Ledger, every graded night</div></div>
      <div class="flag"><b>Books 3+ above Kalshi</b><div class="r warn">{bkw}-{len(bk) - bkw} · {round(100 * bkw / len(bk))}%</div><p>Tonight {bktw} of {len(bkt)}: most of the gaps came from book lines stretched far from the posted number, and those ran hot. Still our best signal, but it cooled from 79% to {round(100 * bkw / len(bk))}%.</p><div class="who">Books column on the grade sheet</div></div>
      <div class="flag"><b>Accuracy (lower is better)</b><div class="r warn">Kalshi 0.215 · Grok 0.195</div><p>Tonight on 96 legs priced before the game: Grok 0.195 and ChatGPT 0.206 beat Kalshi (0.215). Our system 0.228, Gemini 0.225, Claude 0.221. Over all 708 legs Kalshi still leads at 0.207.</p><div class="who">Scorecard rebuilt every night from the ledger</div></div>
      <div class="flag"><b>Our Python sim</b><div class="r acc">Top {w}-{lo}</div><p>Its best night: Sengun 1+ threes (3), Watson 2+ assists (2), Avdija 2+ threes (5), Bridges 6+ rebounds (8), Dunn 5+ points (12) and more hit, with Danny Wolf and Brunson threes the only misses. The books did not beat Kalshi on any of its top picks, so one night does not prove an edge. {roi:+.1f}% flat after fees tonight. All nights: {hw}-{hl}.</p><div class="who">Beta Sim page</div></div>
    </div>
  </section>
  '''
rep('<section class="panel" id="review24">', sec + '<section class="panel" id="review24">')
rep("review24:'record',review23:'record',review22:'record',review21:'results'", "review25:'record',review24:'record',review23:'record',review22:'record',review21:'results'")
open(F, 'w').write(s)
print('board', bw, len(b70), 'season', H, N, '| pub', pw, len(pub), '| k80', k80w, len(k80n), '| sim', w, lo, roi, hw, hl, '| mir', mw, len(live), '| EL', pr, round(pp), sr, round(sp), '| two', e['two']['res'], '| k80', k80, 'k70', k70, 'bk3', bkw, len(bk), 'tonight', bktw, len(bkt), '| nfl', nflw, len(nfl))
