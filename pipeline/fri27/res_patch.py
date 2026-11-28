"""Publish Friday (Nov 27) results into the site source (run from pipeline/ after fri27/res/grade.py, fri27/res/record_add.py and
the ledger). Board, grade sheet, record rows, our sim's top lines, Miracle, Daily 2x, paper tracker, status line, recap."""
import json, re, sys
sys.path.insert(0, '.')
from fri27.res_calc import grade, M, RS
F = 'bettordays-hq.html'; s = open(F).read()
LED = [r for r in json.load(open('ledger/ledger_rows.json')) if r['result'] in ('W', 'L')]
def rep(a, b):
    global s; assert s.count(a) == 1, a[:80]; s = s.replace(a, b)
def getconst(n):
    i = s.index('const ' + n + '=') + len('const ' + n + '='); return json.JSONDecoder().raw_decode(s[i:])[0]
def setconst(n, v):
    global s; i = s.index('const ' + n + '=') + len('const ' + n + '='); _, e = json.JSONDecoder().raw_decode(s[i:]); s = s[:i] + json.dumps(v) + s[i + e:]
fee = lambda q: q + 0.07 * q * (1 - q)
# 1. board and grade sheet
T = getconst('FR27')
for r in T: r['r'], r['act'] = grade(r['p'])
setconst('FR27', T); tw = sum(r['r'] == 'W' for r in T); tn = sum(r['r'] in ('W', 'L') for r in T)
miss = [f"{r['p']} ({r['act']})" for r in T if r['r'] == 'L']
m = re.search(r'const V7D=(\{.*?\});\n', s); V = json.loads(m.group(1)); assert V['d'] == '2026-11-27'
for x in V['all']: x['r'], x['act'] = grade(x['p'])
s = s.replace(m.group(0), 'const V7D=' + json.dumps(V) + ';\n')
# 2. record rows
m = re.search(r'const ROWS=(\[.*?\]);\n', s); R = json.loads(m.group(1)); assert not any(r['day'] == 'Nov 27' for r in R)
for l in M['legs']:
    g = RS.get(l['i'])
    if l.get('tier') not in ('G', 'Y', 'N') or l.get('pub') is None or not g or g['r'] not in ('W', 'L'): continue
    t = l['p'].lower()
    R.append({'day': 'Nov 27', 'pick': l['p'], 'est': l['pub'], 'hit': 1 if g['r'] == 'W' else 0, 'sport': l['sp'], 'mkt': l.get('ty'), 'stat': l.get('stat') or l.get('ty'),
              'dir': 'u' if ' under ' in t else 'o', 'style': 'alt', 'boost': 0, 'star': 0, 'fav': 0})
s = s[:m.start(1)] + json.dumps(R) + s[m.end(1):]
t70 = [r for r in R if r['est'] >= 70]; H = sum(r['hit'] for r in t70); N = len(t70)
pub = [l for l in M['legs'] if l.get('tier') in ('G', 'Y', 'N') and l.get('pub') is not None and RS.get(l['i'], {}).get('r') in ('W', 'L')]; pw = sum(RS[l['i']]['r'] == 'W' for l in pub)
# 3. our sim's top lines
B = getconst('BETA'); SN = {'pts': 'points', 'reb': 'rebounds', 'ast': 'assists', '3pm': 'threes', 'pra': 'PRA'}
for l in B['top']:
    r, a = grade(f"{l['player']} {l['k']}+ {SN[l['st']]}"); l['r'] = None if r == 'V' else r; l['act'] = None if r == 'V' else a
gt = [l for l in B['top'] if l.get('r')]; sw = sum(l['r'] == 'W' for l in gt); sl = len(gt) - sw
t5 = [l for l in B['top'][:5] if l.get('r')]; t5s = f"{sum(l['r'] == 'W' for l in t5)}-{sum(l['r'] == 'L' for l in t5)}"
sroi = round(100 * sum(((1 / fee(l['ask']) - 1) if l['r'] == 'W' else -1) for l in gt) / len(gt), 1)
assert not any(h['d'] == 'Nov 27' for h in B['hist']); B['hist'].append({'d': 'Nov 27', 'w': sw, 'l': sl, 'top5': t5s, 'roi': sroi}); setconst('BETA', B)
BH = getconst('BETAH'); assert not any(h['d'] == 'Nov 27' for h in BH)
BH.append({'d': 'Nov 27', 'rec': B['hist'][-1], 'picks': [{'p': f"{l['player']} {l['k']}+ {SN[l['st']]}", 'g': l.get('g', ''), 'k': round(l['ask'] * 100), 'sim': round(l['sim']), 'r': l.get('r'), 'act': l.get('act')} for l in B['top']]}); setconst('BETAH', BH)
hw = sum(h['w'] for h in B['hist']); hl = sum(h['l'] for h in B['hist'])
bkc = [l for l in gt if l.get('bk') is not None and l['bk'] >= 100 * l['be'] / 100 + 2]
# 4. Miracle, Daily 2x, paper tracker
MIR = getconst('MIR'); assert MIR['d'] == 'Nov 27'
for l in MIR['legs']: l['r'], l['act'] = grade(l['p'])
live = [l for l in MIR['legs'] if l['r'] != 'V']; mw = sum(l['r'] == 'W' for l in live); MIR['res'] = 'W' if mw == len(live) else 'L'; setconst('MIR', MIR)
EL = getconst('EL'); e = next(x for x in EL if x['d'] == 'Nov 27')
for l in e['two']['legs']: l['res'], l['act'] = grade(l['p'])
e['two']['res'] = 'L' if any(l['res'] == 'L' for l in e['two']['legs']) else 'W'; setconst('EL', EL)
P = getconst('PAPER'); p27 = next(x for x in P if x['d'] == 'Nov 27'); p27['mir']['res'] = MIR['res']; setconst('PAPER', P)
PB = {'three': {'legs': ['Luka Doncic 25+ points', 'Tyrese Maxey 20+ points', 'Donovan Clingan 8+ rebounds']}, 'ten': {'legs': ['Luka Doncic 25+ points', 'Tyrese Maxey 20+ points', 'Donovan Clingan 8+ rebounds', 'Brice Sensabaugh 2+ rebounds', 'DeMar DeRozan under 4 assists', 'Cooper Flagg 30+ points, rebounds and assists', 'Zion Williamson 25+ points, rebounds and assists', 'Cam Spencer 4+ assists']}}   # frozen in BETAPOST['Nov 27'] (a JS object, not JSON)
perf = {k: [grade(p) for p in PB[k]['legs']] for k in ('three', 'ten')}
pres = {k: ('Cashed' if all(r == 'W' for r, _ in v) else f"{sum(r == 'W' for r, _ in v)} of {len(v)}") for k, v in perf.items()}
# 5. ledger clues
PL = [r for r in LED if r['priced_pregame'] and r['kalshi_pick'] is not None]
def band(lo_, hi):
    x = [r for r in PL if lo_ <= r['kalshi_pick'] < hi]; wv = sum(r['result'] == 'W' for r in x)
    return wv, len(x) - wv, round(100 * wv / len(x)), round(sum(r['kalshi_pick'] for r in x) / len(x))
k80 = band(80, 101)
bk = [r for r in PL if r.get('books_pick') is not None and r['books_pick'] - r['kalshi_pick'] >= 3]; bkw = sum(r['result'] == 'W' for r in bk)
bkt = [r for r in bk if r['slate_date'] == '2026-11-27']; bktw = sum(r['result'] == 'W' for r in bkt)
au = [r for r in PL if r['sport'] == 'NBA' and r['stat'] == 'ast' and r['kalshi_pick'] >= 75]; auw = sum(r['result'] == 'W' for r in au)
# 6. status line and recap
A = lambda p: grade(p)[1]
rep('<span class="lbl">Friday Nov 27 picks are live · 16 legs at 70%+ · Daily 2x up · no Safe Hammer tonight</span>',
    f'<span class="lbl">Friday graded · {tw}-{tn - tw} at 70%+ · Clingan, Luka, Rui, DeRozan, Draymond all hit · Maxey 14 sank the Daily 2x</span>')
fl = lambda r: f"{r[0]}-{r[1]} · {r[2]}%"
sec = f'''<section class="panel" id="review27">
    <h2>Friday recap · Nov 27 <small>{tw}-{tn - tw} on the board, Tyrese Maxey's 14 points the miss that mattered</small></h2>
    <div class="kpis">
      <div class="kpi"><span class="lbl">70%+ legs</span><b><span data-count="{tw}">{tw}</span>/{tn}</b><small>Hits: Luka 25+ ({A('Luka Doncic 25+ points')}), Clingan 8+ rebounds ({A('Donovan Clingan 8+ rebounds')}), Sensabaugh 2+ rebounds ({A('Brice Sensabaugh 2+ rebounds')}), Wembanyama 10+ rebounds ({A('Victor Wembanyama 10+ rebounds')}), Rui 10+ ({A('Rui Hachimura 10+ points')}), DeRozan under 4 assists ({A('DeMar DeRozan under 4 assists')}), Draymond under 8 assists ({A('Draymond Green under 8 assists')}), Zion 25+ PRA ({A('Zion Williamson 25+ points, rebounds and assists')}). Misses: {', '.join(miss)}. Season: {H} of {N}</small></div>
      <div class="kpi"><span class="lbl">Daily 2x</span><b>2/3</b><small>Luka and Clingan hit, Maxey scored 14 with Jaylen Brown out. Perfect 3: {pres['three']}. Perfect 10x: {pres['ten']}</small></div>
      <div class="kpi"><span class="lbl">Our sim</span><b>{sw}-{sl}</b><small>Top 5 {t5s}. Since we started tracking: {hw}-{hl}</small></div>
      <div class="kpi"><span class="lbl">Every published leg</span><b><span data-count="{pw}">{pw}</span>/{len(pub)}</b><small>{round(100 * pw / len(pub))}%, the long shots included. Texas, Wisconsin and Louisville all won</small></div>
    </div>
    <div class="flags" style="margin-top:14px">
      <div class="flag"><b>Kalshi 80 cents and up</b><div class="r acc">{fl(k80)}</div><p>Tonight 6 for 6. Priced at {k80[3]} cents on average across every graded night.</p><div class="who">Ledger, every graded night</div></div>
      <div class="flag"><b>Books 3+ above Kalshi</b><div class="r acc">{bkw}-{len(bk) - bkw}</div><p>Tonight {bktw} for {len(bkt)}. Still the signal we trust first.</p><div class="who">Books column on the grade sheet</div></div>
      <div class="flag"><b>NBA assists at 75 cents and up</b><div class="r acc">{auw}-{len(au) - auw}</div><p>Overs and unders together. Draymond and DeRozan unders both cashed tonight. Assists stay our strongest group.</p><div class="who">Self-learning, every graded night</div></div>
      <div class="flag"><b>Miracle Parlay</b><div class="r warn">{mw} of {len(live)}</div><p>Jordan Goodwin 15+ PRA ({A('Jordan Goodwin 15+ points, rebounds and assists')}) and Maxey 6+ assists ({A('Tyrese Maxey 6+ assists')}) hit. LeBron 8+ assists ({A('LeBron James 8+ assists')}), P.J. Washington 20+ PRA ({A('P.J. Washington 20+ points, rebounds and assists')}) and Miles Bridges 25+ PRA ({A('Miles Bridges 25+ points, rebounds and assists')}) missed.</p><div class="who">Paper ticket, $10 a night</div></div>
    </div>
  </section>
  '''
rep('<section class="panel" id="review26">', sec + '<section class="panel" id="review26">')
rep("review26:'record',", "review27:'record',review26:'record',")
open(F, 'w').write(s)
print('board', tw, tn, miss, '| season', H, N, '| pub', pw, len(pub), '| sim', sw, sl, t5s, sroi, 'all', hw, hl, '| sim books-confirmed', [(l['player'], l['k'], l['st'], l['r']) for l in bkc],
      '| mir', mw, len(live), '| 2x', e['two']['res'], '| perf', pres, '| k80', k80, '| bk', bkw, len(bk), bktw, len(bkt), '| ast75', auw, len(au))
print([(l['player'], l['k'], l['st'], l['r'], l['act']) for l in B['top']])
