"""Publish Nov 22 results into the site source (run from pipeline/ after sun22/res/grade.py and the ledger load).
Board and grade-sheet results, record rows, our sim's Top results, status line, Sunday recap with the edge clues from the ledger."""
import json, re, subprocess, unicodedata
F = 'bettordays-hq.html'; s = open(F).read()
M = json.load(open('daily/2026-11-22/v7_merged_pick.json')); RS = {x['i']: x for x in json.load(open('daily/2026-11-22/results.json'))['legs']}
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
T = getconst('SN22')
for r in T:
    g = BYP.get(r['p'])
    if g: r['r'] = {'void': 'V', 'push': 'P'}.get(g['r'], g['r']); r['act'] = fmt(g['act'])
setconst('SN22', T)
m = re.search(r'const V7D=(\{.*?\});\n', s); V = json.loads(m.group(1))
for x in V['all']:
    g = BYP.get(x['p'])
    if g: x['r'] = {'void': 'V', 'push': 'P'}.get(g['r'], g['r']); x['act'] = fmt(g['act'])
s = s.replace(m.group(0), 'const V7D=' + json.dumps(V) + ';\n')
# 2. record rows (published GREEN/YELLOW/no-Kalshi legs only)
m = re.search(r'const ROWS=(\[.*?\]);\n', s); R = json.loads(m.group(1)); assert not any(r['day'] == 'Nov 22' for r in R)
for l in M['legs']:
    g = RS[l['i']]
    if l.get('tier') not in ('G', 'Y', 'N') or l.get('pub') is None or g['r'] not in ('W', 'L'): continue
    t = l['p'].lower(); st = l.get('stat') or l.get('ty')
    R.append({'day': 'Nov 22', 'pick': l['p'], 'est': l['pub'], 'hit': 1 if g['r'] == 'W' else 0, 'sport': l['sp'], 'mkt': l.get('ty'), 'stat': st,
              'dir': 'u' if ' under ' in t else 'o', 'style': 'alt', 'boost': 0, 'star': 0, 'fav': 0})
s = s[:m.start(1)] + json.dumps(R) + s[m.end(1):]
t70 = [r for r in R if r['est'] >= 70]; H = sum(r['hit'] for r in t70); N = len(t70)
# 3. our sim's Top lines, graded from ESPN NBA box scores
nm = lambda n: re.sub(r'[^a-z]', '', re.sub(r'\b(jr|sr|ii|iii|iv)\b', '', unicodedata.normalize('NFKD', n).encode('ascii', 'ignore').decode().lower()))
box = {}
for e in json.loads(subprocess.run(['curl', '-s', '-m', '30', 'https://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard?dates=20261122'], capture_output=True, text=True).stdout)['events']:
    d = json.loads(subprocess.run(['curl', '-s', '-m', '30', f"https://site.api.espn.com/apis/site/v2/sports/basketball/nba/summary?event={e['id']}"], capture_output=True, text=True).stdout)
    for t in d['boxscore'].get('players', []):
        for st in t['statistics']:
            for a in st['athletes']:
                if a.get('stats'): box[nm(a['athlete']['displayName'])] = dict(zip(st['keys'], a['stats']))
num = lambda v: float(str(v).split('-')[0]) if v not in (None, '') else 0.0
B = getconst('BETA')
for l in B['top']:
    b = box.get(nm(l['player']))
    if not b: l['r'] = None; l['act'] = 'did not play'; continue
    v = {'pts': num(b.get('points')), 'reb': num(b.get('rebounds')), 'ast': num(b.get('assists')), '3pm': num(b.get('threePointFieldGoalsMade-threePointFieldGoalsAttempted'))}[l['st']]
    l['r'] = 'W' if v >= l['k'] else 'L'; l['act'] = int(v)
gt = [l for l in B['top'] if l.get('r')]; w = sum(l['r'] == 'W' for l in gt); lo = len(gt) - w
t5 = [l for l in B['top'][:5] if l.get('r')]; t5s = f"{sum(l['r'] == 'W' for l in t5)}-{sum(l['r'] == 'L' for l in t5)}"
askp = lambda a: a if a <= 1 else a / 100
roi = round(100 * sum(((1 / (askp(l['ask']) + 0.07 * askp(l['ask']) * (1 - askp(l['ask']))) - 1) if l['r'] == 'W' else -1) for l in gt) / len(gt), 1)
assert not any(h['d'] == 'Nov 22' for h in B['hist']); B['hist'].append({'d': 'Nov 22', 'w': w, 'l': lo, 'top5': t5s, 'roi': roi}); setconst('BETA', B)
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
# 5. status line and the Sunday recap
st_old = re.search(r'<span class="lbl">Sunday Nov 22 picks are live[^<]*</span>', s)
rep(st_old.group(0), '<span class="lbl">Sunday graded · 5-0 at 70%+ · Safe Hammer hit, 3 days straight · Monday board next</span>')
sec = f'''<section class="panel" id="review22">
    <h2>Sunday recap · Nov 22 <small>5-0 on the board, the Safe Hammer cashed for the third day straight</small></h2>
    <div class="kpis">
      <div class="kpi"><span class="lbl">70%+ legs</span><b><span data-count="5">5</span>/5</b><small>Towns 1+ threes (4), Wendell Carter Jr. 6+ rebounds (6), Bears ML, James Cook 70+ rushing (89), James Cook anytime TD. Season: {H} of {N}</small></div>
      <div class="kpi"><span class="lbl">Safe Hammer</span><b>2/2</b><small>Bears ML (won by 8) and Karl-Anthony Towns 1+ threes (4 of 4). About 1.41x after fees. Three days straight</small></div>
      <div class="kpi"><span class="lbl">Kalshi 70 cents and up</span><b><span data-count="10">10</span>/11</b><small>Every leg Kalshi priced at 70+ on Sunday. Only the Jaguars ML lost</small></div>
      <div class="kpi"><span class="lbl">Every published leg</span><b><span data-count="{pw}">{pw}</span>/{len(pub)}</b><small>{round(100 * pw / len(pub))}%, under 70 included. Mostly NFL near coin flips</small></div>
    </div>
    <h3 style="margin-top:18px">Where the edge is <small>every night since Nov 16, only legs priced before the game</small></h3>
    <div class="flags">
      <div class="flag"><b>Kalshi 80 cents and up</b><div class="r acc">{k80[0]}-{k80[1]} · {k80[2]}%</div><p>Priced at {k80[3]} cents on average and hit {k80[2]}%. The strongest favorites hit a little more often than their price says. This is where the Hammer comes from.</p><div class="who">Ledger, every graded night</div></div>
      <div class="flag"><b>Kalshi 70 to 79 cents</b><div class="r warn">{k70[0]}-{k70[1]} · {k70[2]}%</div><p>Priced at {k70[3]} cents but hit only {k70[2]}%. This band has been overpriced. Be pickier here: use it only when our grade and the books agree.</p><div class="who">Ledger, every graded night</div></div>
      <div class="flag"><b>GREEN beats YELLOW</b><div class="r acc">{gw}-{len(gr) - gw} vs {yw}-{len(ye) - yw}</div><p>At 70+, legs where Kalshi is at or above our grade (GREEN) hit {round(100 * gw / len(gr))}%. Legs where we are higher than Kalshi (YELLOW) hit {round(100 * yw / len(ye))}%. When the market agrees, trust it more.</p><div class="who">Filter: GREEN on the grade sheet</div></div>
      <div class="flag"><b>Longshots under 50 cents</b><div class="r warn">{kl[0]}-{kl[1]} · {kl[2]}%</div><p>Priced at {kl[3]} cents but hit {kl[2]}%. Cheap legs have been overpriced. Keep them for small lottos only.</p><div class="who">Ledger, every graded night</div></div>
      <div class="flag"><b>Anytime touchdowns</b><div class="r warn">{aw}-{len(atd) - aw}</div><p>Coin flips, including 9-9 on Sunday. Lotto legs, never Hammer legs.</p><div class="who">Every graded TD leg</div></div>
      <div class="flag"><b>Sportsbooks vs Kalshi</b><div class="r acc">Books 0.188 · Kalshi 0.193</div><p>On Sunday's 33 legs with a sportsbook price, the books' no-vig chance was more accurate than Kalshi (lower is better). When the books price a leg higher than Kalshi, it is worth a look.</p><div class="who">Books column on the grade sheet</div></div>
      <div class="flag"><b>Accuracy (lower is better)</b><div class="r warn">Kalshi 0.213 · our blend 0.218</div><p>On the 89 legs priced before kickoff: Claude 0.208, Kalshi 0.213, our blended grade 0.218, Gemini 0.219, ChatGPT 0.221, our system 0.251. Our NFL system grade had its worst night, so Kalshi and the books lead on NFL until it improves.</p><div class="who">Scorecard rebuilt every night from the ledger</div></div>
      <div class="flag"><b>Our Python sim</b><div class="r warn">Top {w}-{lo}</div><p>{simtxt}. {roi:+.1f}% flat after fees. All nights: {hw}-{hl}. Still experimental.</p><div class="who">Beta Sim page</div></div>
    </div>
  </section>
  '''
rep('<section class="panel" id="review21">', sec + '<section class="panel" id="review21">')
rep("review21:'record',review20:'record',review19:'record',review18:'results'", "review22:'record',review21:'record',review20:'record',review19:'results',review18:'results'")
open(F, 'w').write(s)
print('season 70+', H, N, '| sim', w, lo, t5s, roi, hw, hl, '| clues', k80, k70, kl, gw, len(gr), yw, len(ye), aw, len(atd), '| published', pw, len(pub))
