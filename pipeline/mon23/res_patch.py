"""Publish Nov 23 results into the site source (run from pipeline/ after sun22/res/grade.py and the ledger load).
Board and grade-sheet results, record rows, our sim's Top results, status line, Sunday recap with the edge clues from the ledger."""
import json, re, subprocess, unicodedata
F = 'bettordays-hq.html'; s = open(F).read()
M = json.load(open('daily/2026-11-23/v7_merged_pick.json')); RS = {x['i']: x for x in json.load(open('daily/2026-11-23/results.json'))['legs']}
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
T = getconst('MO23')
for r in T:
    g = BYP.get(r['p'])
    if g: r['r'] = {'void': 'V', 'push': 'P'}.get(g['r'], g['r']); r['act'] = fmt(g['act'])
setconst('MO23', T)
m = re.search(r'const V7D=(\{.*?\});\n', s); V = json.loads(m.group(1))
for x in V['all']:
    g = BYP.get(x['p'])
    if g: x['r'] = {'void': 'V', 'push': 'P'}.get(g['r'], g['r']); x['act'] = fmt(g['act'])
s = s.replace(m.group(0), 'const V7D=' + json.dumps(V) + ';\n')
# 2. record rows (published GREEN/YELLOW/no-Kalshi legs only)
m = re.search(r'const ROWS=(\[.*?\]);\n', s); R = json.loads(m.group(1)); assert not any(r['day'] == 'Nov 23' for r in R)
for l in M['legs']:
    g = RS[l['i']]
    if l.get('tier') not in ('G', 'Y', 'N') or l.get('pub') is None or g['r'] not in ('W', 'L'): continue
    t = l['p'].lower(); st = l.get('stat') or l.get('ty')
    R.append({'day': 'Nov 23', 'pick': l['p'], 'est': l['pub'], 'hit': 1 if g['r'] == 'W' else 0, 'sport': l['sp'], 'mkt': l.get('ty'), 'stat': st,
              'dir': 'u' if ' under ' in t else 'o', 'style': 'alt', 'boost': 0, 'star': 0, 'fav': 0})
s = s[:m.start(1)] + json.dumps(R) + s[m.end(1):]
t70 = [r for r in R if r['est'] >= 70]; H = sum(r['hit'] for r in t70); N = len(t70)
# 3. our sim's Top lines, graded from ESPN NBA box scores
nm = lambda n: re.sub(r'[^a-z]', '', re.sub(r'\b(jr|sr|ii|iii|iv)\b', '', unicodedata.normalize('NFKD', n).encode('ascii', 'ignore').decode().lower()))
box = {}
for e in json.loads(subprocess.run(['curl', '-s', '-m', '30', 'https://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard?dates=20261123'], capture_output=True, text=True).stdout)['events']:
    d = json.loads(subprocess.run(['curl', '-s', '-m', '30', f"https://site.api.espn.com/apis/site/v2/sports/basketball/nba/summary?event={e['id']}"], capture_output=True, text=True).stdout)
    for t in d['boxscore'].get('players', []):
        for st in t['statistics']:
            for a in st['athletes']:
                if a.get('stats'): box[nm(a['athlete']['displayName'])] = dict(zip(st['keys'], a['stats']))
num = lambda v: float(str(v).split('-')[0]) if v not in (None, '') else 0.0
B0 = getconst('BETA'); B = json.load(open('betamon23/beta_tonight.json')); B['hist'] = B0['hist']
A = json.load(open('betamon23/all_lines.json')); B['avg'] = round(sum(l['edge'] for l in A) / len(A), 1)
for l in B['top']:
    b = box.get(nm(l['player']))
    if not b: l['r'] = None; l['act'] = 'did not play'; continue
    v = {'pts': num(b.get('points')), 'reb': num(b.get('rebounds')), 'ast': num(b.get('assists')), '3pm': num(b.get('threePointFieldGoalsMade-threePointFieldGoalsAttempted')), 'pra': num(b.get('points')) + num(b.get('rebounds')) + num(b.get('assists'))}[l['st']]
    l['r'] = 'W' if v >= l['k'] else 'L'; l['act'] = int(v)
gt = [l for l in B['top'] if l.get('r')]; w = sum(l['r'] == 'W' for l in gt); lo = len(gt) - w
t5 = [l for l in B['top'][:5] if l.get('r')]; t5s = f"{sum(l['r'] == 'W' for l in t5)}-{sum(l['r'] == 'L' for l in t5)}"
askp = lambda a: a if a <= 1 else a / 100
roi = round(100 * sum(((1 / (askp(l['ask']) + 0.07 * askp(l['ask']) * (1 - askp(l['ask']))) - 1) if l['r'] == 'W' else -1) for l in gt) / len(gt), 1)
assert not any(h['d'] == 'Nov 23' for h in B['hist']); B['hist'].append({'d': 'Nov 23', 'w': w, 'l': lo, 'top5': t5s, 'roi': roi}); setconst('BETA', B)
hw = sum(h['w'] for h in B['hist']); hl = sum(h['l'] for h in B['hist'])
simtxt = ', '.join(f"{l['player']} {l['k']}+ {l['st']} {'✓' if l['r'] == 'W' else '✗'} ({l['act']})" for l in gt[:5])
# 4. edge clues from the ledger (every night, legs priced before the game)
P = [r for r in LED if r['priced_pregame'] and r['kalshi_pick'] is not None]
def band(lo, hi):
    x = [r for r in P if lo <= r['kalshi_pick'] < hi]; wv = sum(r['result'] == 'W' for r in x)
    return wv, len(x) - wv, round(100 * wv / len(x)), round(sum(r['kalshi_pick'] for r in x) / len(x))
k80, k70, kl = band(80, 101), band(70, 80), band(0, 50)
gr = [r for r in P if (r['grade_published'] or 0) >= 70 and r['kalshi_pick'] >= r['grade_published']]; ye = [r for r in P if (r['grade_published'] or 0) >= 70 and r['kalshi_pick'] < r['grade_published']]
gw = sum(r['result'] == 'W' for r in gr); yw = sum(r['result'] == 'W' for r in ye)
atd = [r for r in LED if 'anytime' in r['pick_text'].lower()]; aw = sum(r['result'] == 'W' for r in atd)
pub = [l for l in M['legs'] if l.get('tier') in ('G', 'Y', 'N') and l.get('pub') is not None and RS[l['i']]['r'] in ('W', 'L')]
pw = sum(RS[l['i']]['r'] == 'W' for l in pub)
# 5. status line and the Monday recap
st_old = re.search(r'<span class="lbl">Monday Nov 23 picks are live[^<]*</span>', s)
rep(st_old.group(0), '<span class="lbl">Monday graded · 18-4 at 70%+ · Hammer hit, 4 days straight · Tuesday board next</span>')
sec = f'''<section class="panel" id="review23">
    <h2>Monday recap · Nov 23 <small>18-4 on the board, the Hammer cashed for the fourth day straight</small></h2>
    <div class="kpis">
      <div class="kpi"><span class="lbl">70%+ legs</span><b><span data-count="18">18</span>/22</b><small>Misses: Keyonte George 4+ assists (2), Tee Higgins 50+ yards (43), Luka Doncic 30+ points (28), Bengals and Commanders over 45 (42). Season: {H} of {N}</small></div>
      <div class="kpi"><span class="lbl">Hammer</span><b>3/3</b><small>Tyler Herro 2+ assists (8), Devin Booker 4+ assists (8), Ivica Zubac 6+ rebounds (15). About 1.56x. Four days straight</small></div>
      <div class="kpi"><span class="lbl">Kalshi 80 cents and up</span><b><span data-count="14">14</span>/15</b><small>Only Keyonte George 4+ assists missed</small></div>
      <div class="kpi"><span class="lbl">Every published leg</span><b><span data-count="{pw}">{pw}</span>/{len(pub)}</b><small>{round(100 * pw / len(pub))}%, under 70 included</small></div>
    </div>
    <div class="flags" style="margin-top:14px">
      <div class="flag"><b>Books edge 8x</b><div class="r warn">6 of 7</div><p>Kessler 10+ rebounds (12), Ty Jerome 15+ (29), VJ Edgecombe 10+ (12), Amen Thompson 10+ (20), Quickley 4+ assists (6) and Chase Brown 3+ catches (5) all hit. Stefon Diggs finished with 45 yards, 5 short of 50.</p><div class="who">Side play built from books vs Kalshi gaps</div></div>
      <div class="flag"><b>Ace's parlay</b><div class="r warn">5 of 6</div><p>Lakers ML, Ty Jerome 15+, Coby White under 6 assists (2), Burrow under 325 (300) and Jaylen Brown under 25 (20) all hit. The Bengals lost by 2. Luka finished with 28, so leaving him off was right.</p><div class="who">Ace's own build, posted with honest odds</div></div>
    </div>
    <h3 style="margin-top:18px">Where the edge is <small>every night since Nov 16, only legs priced before the game</small></h3>
    <div class="flags">
      <div class="flag"><b>Kalshi 80 cents and up</b><div class="r acc">{k80[0]}-{k80[1]} · {k80[2]}%</div><p>Priced at {k80[3]} cents on average and hit {k80[2]}%. The strongest favorites keep hitting a little more often than their price. This is where the Hammer comes from.</p><div class="who">Ledger, every graded night</div></div>
      <div class="flag"><b>Kalshi 70 to 79 cents</b><div class="r warn">{k70[0]}-{k70[1]} · {k70[2]}%</div><p>Priced at {k70[3]} cents, hit {k70[2]}%. Since Monday a 70 to 79 cent leg rides the Hammer only when the books price it higher than Kalshi.</p><div class="who">Ledger, every graded night</div></div>
      <div class="flag"><b>GREEN beats YELLOW</b><div class="r acc">{gw}-{len(gr) - gw} vs {yw}-{len(ye) - yw}</div><p>At 70+, legs where Kalshi is at or above our grade hit {round(100 * gw / len(gr))}%. Legs where we are higher than Kalshi hit {round(100 * yw / len(ye))}%.</p><div class="who">Filter: GREEN on the grade sheet</div></div>
      <div class="flag"><b>Longshots under 50 cents</b><div class="r warn">{kl[0]}-{kl[1]} · {kl[2]}%</div><p>Priced at {kl[3]} cents, hit {kl[2]}%. Lotto legs only.</p><div class="who">Ledger, every graded night</div></div>
      <div class="flag"><b>Sportsbooks vs Kalshi</b><div class="r acc">Books beat Kalshi 3 nights running</div><p>Monday: books 0.165, Kalshi 0.171 on 60 legs (lower is better). All nights: books 0.173 vs Kalshi 0.178 on 93 legs. When the books price a leg higher than Kalshi on the same line, Kalshi is cheap.</p><div class="who">Books column on the grade sheet</div></div>
      <div class="flag"><b>Accuracy (lower is better)</b><div class="r warn">Kalshi 0.171 · our blend 0.185</div><p>Monday on 68 legs priced before the game: Kalshi 0.171, ChatGPT 0.184, Gemini 0.184, our blended grade 0.185, Claude 0.189, our system 0.192, Grok 0.207. Kalshi and the books lead; our grades are a filter, not the price.</p><div class="who">Scorecard rebuilt every night from the ledger</div></div>
      <div class="flag"><b>Our Python sim</b><div class="r warn">Top {w}-{lo}</div><p>{simtxt}. {roi:+.1f}% flat after fees. All nights: {hw}-{hl}. Still experimental.</p><div class="who">Beta Sim page</div></div>
    </div>
  </section>
  '''
rep('<section class="panel" id="review22">', sec + '<section class="panel" id="review22">')
rep("review22:'record',review21:'record',review20:'record',review19:'results',review18:'results'", "review23:'record',review22:'record',review21:'record',review20:'results',review19:'results',review18:'results'")
open(F, 'w').write(s)
print('season 70+', H, N, '| sim', w, lo, t5s, roi, hw, hl, '| clues', k80, k70, kl, gw, len(gr), yw, len(ye), '| published', pw, len(pub))
