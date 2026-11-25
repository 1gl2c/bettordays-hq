"""Publish Nov 24 results into the site source (run from pipeline/ after tue24/res/grade.py and the ledger load).
Board and grade sheet, record rows, our sim's Top, the paper trackers (Safe Hammer, Miracle, Edge Lab), status line, Tuesday recap."""
import json, re, sys
sys.path.insert(0, '.')
from tue24.res.box import grade
F = 'bettordays-hq.html'; s = open(F).read()
M = json.load(open('daily/2026-11-24/v7_merged_pick.json')); RS = {x['i']: x for x in json.load(open('daily/2026-11-24/results.json'))['legs']}
BYP = {l['p']: RS[l['i']] for l in M['legs']}
LED = [r for r in json.load(open('ledger/ledger_rows.json')) if r['result'] in ('W', 'L')]
def rep(a, b):
    global s; assert s.count(a) == 1, a[:80]; s = s.replace(a, b)
def getconst(n):
    i = s.index('const ' + n + '=') + len('const ' + n + '='); return json.JSONDecoder().raw_decode(s[i:])[0]
def setconst(n, v):
    global s; i = s.index('const ' + n + '=') + len('const ' + n + '='); _, e = json.JSONDecoder().raw_decode(s[i:]); s = s[:i] + json.dumps(v) + s[i + e:]
fmt = lambda a: (int(a) if isinstance(a, float) and a.is_integer() else a)
# 1. board rows and the full grade sheet
T = getconst('TU24')
for r in T:
    g = BYP.get(r['p'])
    if g: r['r'] = {'void': 'V', 'push': 'P'}.get(g['r'], g['r']); r['act'] = fmt(g['act'])
setconst('TU24', T)
m = re.search(r'const V7D=(\{.*?\});\n', s); V = json.loads(m.group(1))
for x in V['all']:
    g = BYP.get(x['p'])
    if g: x['r'] = {'void': 'V', 'push': 'P'}.get(g['r'], g['r']); x['act'] = fmt(g['act'])
s = s.replace(m.group(0), 'const V7D=' + json.dumps(V) + ';\n')
# 2. record rows (published legs only)
m = re.search(r'const ROWS=(\[.*?\]);\n', s); R = json.loads(m.group(1)); assert not any(r['day'] == 'Nov 24' for r in R)
for l in M['legs']:
    g = RS[l['i']]
    if l.get('tier') not in ('G', 'Y', 'N') or l.get('pub') is None or g['r'] not in ('W', 'L'): continue
    t = l['p'].lower(); st = l.get('stat') or l.get('ty')
    R.append({'day': 'Nov 24', 'pick': l['p'], 'est': l['pub'], 'hit': 1 if g['r'] == 'W' else 0, 'sport': l['sp'], 'mkt': l.get('ty'), 'stat': st,
              'dir': 'u' if ' under ' in t else 'o', 'style': 'alt', 'boost': 0, 'star': 0, 'fav': 0})
s = s[:m.start(1)] + json.dumps(R) + s[m.end(1):]
t70 = [r for r in R if r['est'] >= 70]; H = sum(r['hit'] for r in t70); N = len(t70)
pub = [l for l in M['legs'] if l.get('tier') in ('G', 'Y', 'N') and l.get('pub') is not None and RS[l['i']]['r'] in ('W', 'L')]
b70 = [l for l in pub if l['pub'] >= 70]; bw = sum(RS[l['i']]['r'] == 'W' for l in b70); pw = sum(RS[l['i']]['r'] == 'W' for l in pub)
# 3. our sim's Top lines
B = getconst('BETA'); SN = {'pts': 'points', 'reb': 'rebounds', 'ast': 'assists', '3pm': 'threes', 'pra': 'PRA'}
for l in B['top']:
    r, a = grade(f"{l['player']} {l['k']}+ {SN[l['st']]}"); l['r'] = None if r == 'V' else r; l['act'] = None if r == 'V' else int(a)
gt = [l for l in B['top'] if l.get('r')]; w = sum(l['r'] == 'W' for l in gt); lo = len(gt) - w
t5 = [l for l in B['top'][:5] if l.get('r')]; t5s = f"{sum(l['r'] == 'W' for l in t5)}-{sum(l['r'] == 'L' for l in t5)}"
askp = lambda a: a if a <= 1 else a / 100
roi = round(100 * sum(((1 / (askp(l['ask']) + 0.07 * askp(l['ask']) * (1 - askp(l['ask']))) - 1) if l['r'] == 'W' else -1) for l in gt) / len(gt), 1)
assert not any(h['d'] == 'Nov 24' for h in B['hist']); B['hist'].append({'d': 'Nov 24', 'w': w, 'l': lo, 'top5': t5s, 'roi': roi}); setconst('BETA', B)
BH = getconst('BETAH'); assert not any(h['d'] == 'Nov 24' for h in BH)
BH.append({'d': 'Nov 24', 'rec': B['hist'][-1], 'picks': [{'p': f"{l['player']} {l['k']}+ {SN[l['st']]}", 'g': l.get('g', ''), 'k': round(askp(l['ask']) * 100), 'sim': round(l['sim']), 'r': l.get('r'), 'act': l.get('act')} for l in B['top']]}); setconst('BETAH', BH)
hw = sum(h['w'] for h in B['hist']); hl = sum(h['l'] for h in B['hist'])
simtxt = ', '.join(f"{l['player']} {l['k']}+ {SN[l['st']]} {'✓' if l['r'] == 'W' else '✗'} ({l['act']})" for l in gt)
# 4. paper trackers
MIR = getconst('MIR')
for grp in [MIR['legs'], MIR['swap']] + [t['legs'] for t in MIR['add']]:
    for l in grp: l['r'], l['act'] = grade(l['p'])
mw = sum(l['r'] == 'W' for l in MIR['legs']); MIR['res'] = 'W' if mw == len(MIR['legs']) else 'L'; setconst('MIR', MIR)
P = getconst('PAPER'); P[0]['ham']['res'] = 'L'; P[0]['mir']['res'] = MIR['res']; setconst('PAPER', P)
EL = getconst('EL')
for p in EL[0]['par']:
    for l in p['legs']: l['res'], l['act'] = grade(l['p'])
    p['res'] = 'V' if all(l['res'] == 'V' for l in p['legs']) else ('L' if any(l['res'] == 'L' for l in p['legs']) else 'W')
for x in EL[0]['sing']: x['res'], x['act'] = grade(x['p'])
setconst('EL', EL)
pp = sum((p['stake'] * (p['pays'] - 1) if p['res'] == 'W' else -p['stake']) for p in EL[0]['par']); sp = sum((x['stake'] * (x['pays'] - 1) if x['res'] == 'W' else -x['stake']) for x in EL[0]['sing'])
pr = f"{sum(p['res'] == 'W' for p in EL[0]['par'])}-{sum(p['res'] == 'L' for p in EL[0]['par'])}"; sr = f"{sum(x['res'] == 'W' for x in EL[0]['sing'])}-{sum(x['res'] == 'L' for x in EL[0]['sing'])}"
# 5. ledger clues
PL = [r for r in LED if r['priced_pregame'] and r['kalshi_pick'] is not None]
def band(lo_, hi):
    x = [r for r in PL if lo_ <= r['kalshi_pick'] < hi]; wv = sum(r['result'] == 'W' for r in x)
    return wv, len(x) - wv, round(100 * wv / len(x)), round(sum(r['kalshi_pick'] for r in x) / len(x))
k80, k70 = band(80, 101), band(70, 80)
bk = [r for r in PL if r.get('books_pick') is not None and r['books_pick'] - r['kalshi_pick'] >= 3]; bkw = sum(r['result'] == 'W' for r in bk)
# 6. status line and the Tuesday recap
rep('<span class="lbl">Tuesday Nov 24 picks are live · Engine v8 · 27 legs at 70+ · Safe Hammer updated 3:35 PM</span>',
    f'<span class="lbl">Tuesday graded · {bw}-{len(b70) - bw} at 70%+ · Safe Hammer missed by 1 rebound · Wednesday board next</span>')
fm = lambda v: f"+${round(v):,}" if v >= 0 else f"-${round(-v):,}"
sec = f'''<section class="panel" id="review24">
    <h2>Tuesday recap · Nov 24 <small>{bw}-{len(b70) - bw} on the board, the Safe Hammer missed by one rebound</small></h2>
    <div class="kpis">
      <div class="kpi"><span class="lbl">70%+ legs</span><b><span data-count="{bw}">{bw}</span>/{len(b70)}</b><small>Misses: Queta 6+ rebounds (5), Jokic 6+ and 8+ assists (5), Jokic 40+ PRA (34), Magic +15 (lost by 18). Cade sat with knee soreness, so his legs are void. Season: {H} of {N}</small></div>
      <div class="kpi"><span class="lbl">Safe Hammer</span><b>2/3</b><small>Flagg 4+ assists (12) and Jokic 8+ rebounds (11) hit. Queta scored 21 but had 5 rebounds in a blowout, one short. The streak ends at 4. The first ticket we pulled at 3:35 would have lost too: Jokic had 5 assists</small></div>
      <div class="kpi"><span class="lbl">Kalshi 80 cents and up</span><b><span data-count="{sum(RS[l['i']]['r']=='W' for l in M['legs'] if (l.get('k') or 0)>=80 and RS[l['i']]['r'] in ('W','L'))}">{sum(RS[l['i']]['r']=='W' for l in M['legs'] if (l.get('k') or 0)>=80 and RS[l['i']]['r'] in ('W','L'))}</span>/{sum(1 for l in M['legs'] if (l.get('k') or 0)>=80 and RS[l['i']]['r'] in ('W','L'))}</b><small>Queta rebounds and Jokic assists missed</small></div>
      <div class="kpi"><span class="lbl">Every published leg</span><b><span data-count="{pw}">{pw}</span>/{len(pub)}</b><small>{round(100 * pw / len(pub))}%, under 70 included</small></div>
    </div>
    <div class="flags" style="margin-top:14px">
      <div class="flag"><b>What we changed for Wednesday</b><div class="r acc">No rebounds or points on the Hammer</div><p>Rebound legs at 80 cents and up have hit less often than their price, and Queta was one. From Wednesday the Safe Hammer uses threes, assists and PRA unless Ace approves a points or rebounds leg. The same rules tonight would have built Flagg 4+ assists, Derrick White 1+ threes and Tatum 4+ assists at about 1.49x. All three hit.</p><div class="who">Self-learning Hammer, starts Wednesday</div></div>
      <div class="flag"><b>Books edge side play</b><div class="r warn">5 of 6</div><p>Flagg 6+ assists (12), Franz Wagner 6+ rebounds (9), Jokic 8+ rebounds (11), Derrick White 1+ threes (2) and Pritchard 2+ assists (2) hit. Queta 8+ rebounds (5) missed.</p><div class="who">Side play built from books vs Kalshi gaps</div></div>
      <div class="flag"><b>Miracle Parlay</b><div class="r warn">{mw} of {len(MIR['legs'])}</div><p>Dybantsa 2+ threes, Tatum 3+ threes (6), Trae 8+ assists (12) and Cam Johnson 4+ rebounds hit. Sarr went 7 points and 1 three, Marshall 1 rebound, Hauser 1 three, Jokic 5 assists. Kalshi's real combo price was 445x.</p><div class="who">Paper ticket, $10 a night</div></div>
      <div class="flag"><b>Edge Lab, night one</b><div class="r warn">Parlays {pr} · singles {sr}</div><p>Dybantsa 20+ PRA (38) with Jokic 8+ rebounds cashed. Queta rebounds and Jokic 6+ assists sank the other two. Paper: parlays {fm(pp)}, singles {fm(sp)} on $2,000 each.</p><div class="who">Paper tracker, home page</div></div>
      <div class="flag"><b>Perfect 3 attempt</b><div class="r acc">3 of 3</div><p>Derrick White 1+ threes (2), Flagg 4+ assists (12) and Franz Wagner 20+ points (20) all hit, about 2.0x. The 10x attempt went 5 of 6: Jokic had 5 assists. First night with the live attempt frozen before the games.</p><div class="who">Research page, learning model</div></div>
    </div>
    <h3 style="margin-top:18px">Where the edge is <small>every night since Nov 16, only legs priced before the game</small></h3>
    <div class="flags">
      <div class="flag"><b>Kalshi 80 cents and up</b><div class="r acc">{k80[0]}-{k80[1]} · {k80[2]}%</div><p>Priced at {k80[3]} cents on average and hit {k80[2]}%.</p><div class="who">Ledger, every graded night</div></div>
      <div class="flag"><b>Kalshi 70 to 79 cents</b><div class="r warn">{k70[0]}-{k70[1]} · {k70[2]}%</div><p>Priced at {k70[3]} cents, hit {k70[2]}%. Only with the books above Kalshi.</p><div class="who">Ledger, every graded night</div></div>
      <div class="flag"><b>Books 3+ above Kalshi</b><div class="r acc">{bkw}-{len(bk) - bkw}</div><p>Legs where the sportsbooks priced the same line at least 3 points higher than Kalshi. Our best signal, still a small sample.</p><div class="who">Books column on the grade sheet</div></div>
      <div class="flag"><b>Accuracy (lower is better)</b><div class="r acc">Our system 0.183 · Kalshi 0.197</div><p>Tuesday on 47 legs priced before the game: our system 0.183, blended grade 0.191, ChatGPT 0.194, Kalshi 0.197, Gemini and Claude 0.200, books 0.203, Grok 0.218. First night our system beat Kalshi. All nights Kalshi still leads, and the books beat it over 131 legs.</p><div class="who">Scorecard rebuilt every night from the ledger</div></div>
      <div class="flag"><b>Our Python sim</b><div class="r warn">Top {w}-{lo}</div><p>{simtxt}. {roi:+.1f}% flat after fees. All nights: {hw}-{hl}. Still experimental.</p><div class="who">Beta Sim page</div></div>
    </div>
  </section>
  '''
rep('<section class="panel" id="review23">', sec + '<section class="panel" id="review23">')
rep("review23:'record',review22:'record',review21:'record',review20:'results'", "review24:'record',review23:'record',review22:'record',review21:'results',review20:'results'")
open(F, 'w').write(s)
print('board', bw, len(b70), 'season', H, N, '| pub', pw, len(pub), '| sim', w, lo, roi, hw, hl, '| mir', mw, '| EL', pr, round(pp), sr, round(sp), '| k80', k80, 'k70', k70, 'bk3', bkw, len(bk))
