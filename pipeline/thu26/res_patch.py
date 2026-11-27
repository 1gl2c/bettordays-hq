"""Publish Thanksgiving (Nov 26) results into the site source (run from pipeline/ after thu26/res/grade.py, thu26/res/wed25_thu.py
and the ledger). Board, grade sheet, the three Nov 25 legs that played Thursday, record rows, Miracle, Edge Lab, paper tracker,
status line, Thanksgiving recap. No NFL sim ran tonight, so the Beta Sim history is untouched."""
import json, re, sys
sys.path.insert(0, '.')
from thu26.res_calc import grade, M, RS
F = 'bettordays-hq.html'; s = open(F).read()
LED = [r for r in json.load(open('ledger/ledger_rows.json')) if r['result'] in ('W', 'L')]
def rep(a, b):
    global s; assert s.count(a) == 1, a[:80]; s = s.replace(a, b)
def getconst(n):
    i = s.index('const ' + n + '=') + len('const ' + n + '='); return json.JSONDecoder().raw_decode(s[i:])[0]
def setconst(n, v):
    global s; i = s.index('const ' + n + '=') + len('const ' + n + '='); _, e = json.JSONDecoder().raw_decode(s[i:]); s = s[:i] + json.dumps(v) + s[i + e:]
# 1. Thanksgiving board, grade sheet, and the Nov 25 board legs that played Thursday
T = getconst('TH26')
for r in T: r['r'], r['act'] = grade(r['p'])
setconst('TH26', T); tw = sum(r['r'] == 'W' for r in T)
m = re.search(r'const V7D=(\{.*?\});\n', s); V = json.loads(m.group(1)); assert V['d'] == '2026-11-26'
for x in V['all']: x['r'], x['act'] = grade(x['p'])
s = s.replace(m.group(0), 'const V7D=' + json.dumps(V) + ';\n')
W = getconst('WE25')
for r in W:
    if not r.get('r'): r['r'], r['act'] = grade(r['p'])
setconst('WE25', W); w25 = sum(r['r'] == 'W' for r in W); n25 = sum(r['r'] in ('W', 'L') for r in W)
# 2. record rows
m = re.search(r'const ROWS=(\[.*?\]);\n', s); R = json.loads(m.group(1)); assert not any(r['day'] == 'Nov 26' for r in R)
have25 = {r['pick'] for r in R if r['day'] == 'Nov 25'}
def addrows(day, MM, RR, skip=()):
    for l in MM['legs']:
        g = RR.get(l['i'])
        if l.get('tier') not in ('G', 'Y', 'N') or l.get('pub') is None or not g or g['r'] not in ('W', 'L') or l['p'] in skip: continue
        t = l['p'].lower()
        R.append({'day': day, 'pick': l['p'], 'est': l['pub'], 'hit': 1 if g['r'] == 'W' else 0, 'sport': l['sp'], 'mkt': l.get('ty'), 'stat': l.get('stat') or l.get('ty'),
                  'dir': 'u' if ' under ' in t else 'o', 'style': 'alt', 'boost': 0, 'star': 0, 'fav': 0})
M25 = json.load(open('daily/2026-11-25/v7_merged_pick.json')); RS25 = {x['i']: x for x in json.load(open('daily/2026-11-25/results.json'))['legs']}
addrows('Nov 25', M25, RS25, have25); addrows('Nov 26', M, RS)
s = s[:m.start(1)] + json.dumps(R) + s[m.end(1):]
t70 = [r for r in R if r['est'] >= 70]; H = sum(r['hit'] for r in t70); N = len(t70)
pub = [l for l in M['legs'] if l.get('tier') in ('G', 'Y', 'N') and l.get('pub') is not None and RS.get(l['i'], {}).get('r') in ('W', 'L')]; pw = sum(RS[l['i']]['r'] == 'W' for l in pub)
k70n = [l for l in M['legs'] if (l.get('k') or 0) >= 70 and RS.get(l['i'], {}).get('r') in ('W', 'L')]; k70w = sum(RS[l['i']]['r'] == 'W' for l in k70n)
# 3. Miracle, paper tracker, Edge Lab
MIR = getconst('MIR'); assert MIR['d'] == 'Nov 26'
for l in MIR['legs']: l['r'], l['act'] = grade(l['p'])
live = [l for l in MIR['legs'] if l['r'] != 'V']; mw = sum(l['r'] == 'W' for l in live)
MIR['res'] = 'W' if mw == len(live) else 'L'; setconst('MIR', MIR)
P = getconst('PAPER'); p26 = next(x for x in P if x['d'] == 'Nov 26'); p26['mir']['res'] = MIR['res']; setconst('PAPER', P)
EL = getconst('EL'); e = next(x for x in EL if x['d'] == 'Nov 26')
res = lambda legs: 'V' if all(l['res'] == 'V' for l in legs) else ('L' if any(l['res'] == 'L' for l in legs) else 'W')
for p in e['par']:
    for l in p['legs']: l['res'], l['act'] = grade(l['p'])
    p['res'] = res(p['legs'])
for x in e['sing']: x['res'], x['act'] = grade(x['p'])
setconst('EL', EL)
pp = sum((p['stake'] * (p['pays'] - 1) if p['res'] == 'W' else -p['stake']) for p in e['par']); sp = sum((x['stake'] * (x['pays'] - 1) if x['res'] == 'W' else -x['stake']) for x in e['sing'])
pr = f"{sum(p['res'] == 'W' for p in e['par'])}-{sum(p['res'] == 'L' for p in e['par'])}"; sr = f"{sum(x['res'] == 'W' for x in e['sing'])}-{sum(x['res'] == 'L' for x in e['sing'])}"
FUN = [(t['t'], [grade(p) for p in t['legs']]) for t in getconst('TH26TIX')]
# 4. ledger clues
PL = [r for r in LED if r['priced_pregame'] and r['kalshi_pick'] is not None]
def band(lo_, hi):
    x = [r for r in PL if lo_ <= r['kalshi_pick'] < hi]; wv = sum(r['result'] == 'W' for r in x)
    return wv, len(x) - wv, round(100 * wv / len(x)), round(sum(r['kalshi_pick'] for r in x) / len(x))
k80, k70 = band(80, 101), band(70, 80)
bk = [r for r in PL if r.get('books_pick') is not None and r['books_pick'] - r['kalshi_pick'] >= 3]; bkw = sum(r['result'] == 'W' for r in bk)
bkt = [r for r in bk if r['slate_date'] == '2026-11-26']; bktw = sum(r['result'] == 'W' for r in bkt)
nfl = [r for r in LED if r['sport'] == 'NFL']; nflw = sum(r['result'] == 'W' for r in nfl)
atd = [r for r in nfl if r.get('stat') == 'atd']; atdw = sum(r['result'] == 'W' for r in atd)
# 5. Nov 25 recap: the Thursday legs are in now
rep('Josh Hart under 8 assists (11). Three Thursday legs are still to play. Season: 458 of 585</small>',
    f'Josh Hart under 8 assists (11). The three Thursday legs all hit: Goff 200+ and 225+ (313), St. Brown 50+ (146)</small>')
rep('<b><span data-count="32">32</span>/42</b>', f'<b><span data-count="{w25}">{w25}</span>/{n25}</b>')
rep('<small>32-10 on the board, the Safe Hammer missed by 2 passing yards</small>', f'<small>{w25}-{n25 - w25} on the board, the Safe Hammer missed by 2 passing yards</small>')
rep('<div class="r acc">2 of 2 so far</div><p>Love under 350 passing yards (198) and Maxey 1+ threes (3) hit. Goff 200+ passing yards plays Thursday at 10:00 AM PT.',
    '<div class="r acc">Cashed · 3 of 3</div><p>Love under 350 passing yards (198), Maxey 1+ threes (3) and Goff 200+ passing yards (313 on Thanksgiving) all hit.')
# 6. status line and the Thanksgiving recap
rep('<span class="lbl">Thanksgiving Nov 26 picks are live · Engine v8 · 7 legs at 70+ · no Hammer tonight</span>',
    f'<span class="lbl">Thanksgiving graded · {tw}-{len(T) - tw} at 70%+ · Miracle cashed, 9 of 9 · Edge Lab 9 for 9 · NBA back Friday</span>')
fm = lambda v: f"+${round(v):,}" if v >= 0 else f"-${round(-v):,}"
A = lambda p: grade(p)[1]
sec = f'''<section class="panel" id="review26">
    <h2>Thanksgiving recap · Nov 26 <small>{tw}-{len(T) - tw} on the board, and the Miracle Parlay cashed</small></h2>
    <div class="kpis">
      <div class="kpi"><span class="lbl">70%+ legs</span><b><span data-count="{tw}">{tw}</span>/{len(T)}</b><small>Goff 200+ and 225+ ({A('Jared Goff 200+ passing yards')}), Odunze 25+ ({A('Rome Odunze 25+ receiving yards')}), St. Brown 50+ ({A('Amon-Ra St. Brown 50+ receiving yards')}), Gibbs 70+ ({A('Jahmyr Gibbs 70+ rushing yards')}), Jameson Williams 20+ ({A('Jameson Williams 20+ receiving yards')}). The miss: Cowboys ML, lost 39-38. Season: {H} of {N}</small></div>
      <div class="kpi"><span class="lbl">Miracle Parlay</span><b>{mw}/{len(live)}</b><small>About {MIR["pays"]}x at the Kalshi combo price. Paper $10 returns about ${MIR['stake'] * MIR['pays']:,}</small></div>
      <div class="kpi"><span class="lbl">Edge Lab</span><b>{pr} · {sr}</b><small>Every parlay and every single hit. Paper: parlays {fm(pp)}, singles {fm(sp)} on $2,000 each</small></div>
      <div class="kpi"><span class="lbl">Every published leg</span><b><span data-count="{pw}">{pw}</span>/{len(pub)}</b><small>{round(100 * pw / len(pub))}%, the long shots included</small></div>
    </div>
    <div class="flags" style="margin-top:14px">
      <div class="flag"><b>Miracle Parlay</b><div class="r acc">Cashed · 9 of 9</div><p>Caleb Williams 225+ ({A('Caleb Williams 225+ passing yards')}), Joe Milton 15+ rushing ({A('Joe Milton 15+ rushing yards')}, right on the number), Goff 275+ ({A('Jared Goff 275+ passing yards')}), Odunze 25+ ({A('Rome Odunze 25+ receiving yards')}), Shakir 25+ ({A('Khalil Shakir 25+ receiving yards')}), Javonte Williams 60+ ({A('Javonte Williams 60+ rushing yards')}), Jameson Williams 20+ ({A('Jameson Williams 20+ receiving yards')}), St. Brown 90+ ({A('Amon-Ra St. Brown 90+ receiving yards')}) and Josh Allen 40+ rushing ({A('Josh Allen 40+ rushing yards')}). The books had it at about 1 in {MIR['chance']}. One night, not a pattern: it is still a long shot every time.</p><div class="who">Paper ticket, $10 a night</div></div>
      <div class="flag"><b>Fun tickets</b><div class="r warn">Both missed</div><p>Lions +1.5 (lost by 4) and Josh Allen to score (no touchdown) sank the Fun 10x and 25x. Odunze, Javonte Williams to score and Shakir all hit. Saquon did not score either.</p><div class="who">Thanksgiving fun tickets</div></div>
      <div class="flag"><b>Perfect attempt</b><div class="r warn">Missed by 1 point</div><p>Goff 200+ ({A('Jared Goff 200+ passing yards')}) hit, the Cowboys lost 39-38 to the Eagles. Wednesday's Perfect 3 finished 3 for 3 on Goff's yards.</p><div class="who">Learning model</div></div>
      <div class="flag"><b>Touchdown props</b><div class="r warn">{atdw}-{len(atd) - atdw} all time</div><p>Anytime touchdowns stay our weakest NFL group at {round(100 * atdw / len(atd))}%. Tonight Gibbs, Javonte Williams, Emmett Johnson and Swift scored, while Allen, St. Brown, Lamb, Pickens and Saquon did not. Yards lines carried the night.</p><div class="who">Ledger, every graded night</div></div>
    </div>
    <h3 style="margin-top:18px">Where the edge is <small>every night since Nov 16, only legs priced before the game</small></h3>
    <div class="flags">
      <div class="flag"><b>Kalshi 80 cents and up</b><div class="r acc">{k80[0]}-{k80[1]} · {k80[2]}%</div><p>Priced at {k80[3]} cents on average and hit {k80[2]}%.</p><div class="who">Ledger, every graded night</div></div>
      <div class="flag"><b>Kalshi 70 to 79 cents</b><div class="r warn">{k70[0]}-{k70[1]} · {k70[2]}%</div><p>Priced at {k70[3]} cents, hit {k70[2]}%. Only with the books above Kalshi.</p><div class="who">Ledger, every graded night</div></div>
      <div class="flag"><b>Books 3+ above Kalshi</b><div class="r acc">{bkw}-{len(bk) - bkw} · {round(100 * bkw / len(bk))}%</div><p>Tonight {bktw} of {len(bkt)}, back on track after Wednesday. Still our best signal, and the one we lean on first.</p><div class="who">Books column on the grade sheet</div></div>
      <div class="flag"><b>Accuracy (lower is better)</b><div class="r acc">Books 0.163 · Kalshi 0.203</div><p>Tonight on 61 legs priced before the game the sportsbooks beat Kalshi (0.163 against 0.168 on the same 38 legs). Every AI model and our system were worse than Kalshi on football. Over all 785 legs Kalshi still leads the models at 0.207.</p><div class="who">Scorecard rebuilt every night from the ledger</div></div>
    </div>
  </section>
  '''
rep('<section class="panel" id="review25">', sec + '<section class="panel" id="review25">')
rep("review25:'record',review24:'record'", "review26:'record',review25:'record',review24:'record'")
open(F, 'w').write(s)
print('board', tw, len(T), '| nov25', w25, n25, '| season', H, N, '| pub', pw, len(pub), '| k70+ legs tonight', k70w, len(k70n), '| mir', mw, len(live), MIR['res'], '| EL', pr, round(pp), sr, round(sp), '| fun', FUN, '| k80', k80, 'k70', k70, 'bk3', bkw, len(bk), 'tonight', bktw, len(bkt), '| nfl', nflw, len(nfl), 'atd', atdw, len(atd))
