"""Engine v8 inputs for the Hermes runner: blind lines (no market price) and simulation lines.
Usage (from pipeline/): python3 v8/build_v8.py DATE BETA_DIR [AFTER_HHMM]
  reads daily/DATE/v7_candidates.json (graded legs) and BETA_DIR/all_lines.json (Kalshi lines near +100)
  AFTER_HHMM (optional, PT 24h): keep only games that start at or after this time (for a late rerun)
Writes daily/DATE/v8_lines.txt, v8_sim_lines.txt, v8_sim_index.json, v8_slate.txt. No prices go to the models."""
import json, sys
day, bdir = sys.argv[1], sys.argv[2]
after = int(sys.argv[3]) if len(sys.argv) > 3 else 0
def hhmm(t):  # '7:00' PT evening -> 1900; college '2:30' -> 1430
    h, m = map(int, t.split(':')); h = h + 12 if h < 12 else h; return h * 100 + m
C = json.load(open(f'daily/{day}/v7_candidates.json'))['legs']
legs = [l for l in C if hhmm(l['t']) >= after]
W = {'pts': 'points', 'reb': 'rebounds', 'ast': 'assists', '3pm': 'threes', 'pra': 'points + rebounds + assists'}
with open(f'daily/{day}/v8_lines.txt', 'w') as f:
    for l in legs:
        f.write(f"{l['i']} | {l['p']} | {l.get('sp','')} {l['g']} {l['t']} PM PT | market: {l['stat']}" + (" | QUESTIONABLE" if l.get('fl') == 'Q' else '') + "\n")
A = [x for x in json.load(open(f'{bdir}/all_lines.json')) if hhmm(x['t']) >= after]
A.sort(key=lambda x: (x['g'], x['player'], x['st'], x['k']))
idx = {}
with open(f'daily/{day}/v8_sim_lines.txt', 'w') as f:
    for n, x in enumerate(A, 1):
        idx[n] = {'ticker': x['ticker'], 'player': x['player'], 'team': x['team'], 'st': x['st'], 'k': x['k'], 'g': x['g'], 't': x['t'],
                  'ask': x['ask'], 'mid': x['mid'], 'be': x['be'], 'odds': x['odds'], 'oursim': x['sim'], 'avg': x['avg'], 'hs': x['hs'], 'n': x['n']}
        f.write(f"{n} | {x['player']} ({x['team']}) {x['k']}+ {W[x['st']]} | {x['g']} {x['t']} PM PT\n")
json.dump(idx, open(f'daily/{day}/v8_sim_index.json', 'w'))
games = sorted({(l['t'], l['g'], l.get('sp', '')) for l in legs}, key=lambda g: hhmm(g[0]))
open(f'daily/{day}/v8_slate.txt', 'w').write('; '.join(f"{sp} {g} {t} PM PT" for t, g, sp in games))
print(f'{len(legs)} legs, {len(A)} sim lines, {len(games)} games, after {after or "all"}')
