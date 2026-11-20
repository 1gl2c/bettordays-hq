"""Engine v8 merge: our own grade first, Kalshi as referee after.
Usage (from pipeline/): python3 v8/merge_v8.py DATE V8_REPLIES_DIR
  Our grade = median of the blind model numbers (BD_V8 blocks, no price shown) plus our system grade.
  Needs 2+ model numbers, otherwise the leg keeps its v7 result (games that started before the v8 run do too).
  Referee: GREEN Kalshi at or above our grade · YELLOW we are 1 to 7 above · REMOVED we are 8+ above (Research only)
           no Kalshi price: max 75, never on the Hammer. Published grade = our grade (not copied from Kalshi).
  Simulations: BD_SIM blocks per model -> daily/DATE/v8_sims.json (each agent's lines, consensus, edge vs break-even).
Writes daily/DATE/v7_merged.json (the publisher's input; the v7-only file is kept as v7_merged_v7only.json)."""
import json, sys, os, re, statistics, shutil
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'v7'))
from v7lib import hammer, perfect, payout, BOARD_MIN, NO_K_MAX, GAP_REMOVE
day, rdir = sys.argv[1], sys.argv[2]
D = f'daily/{day}/'
MODELS = ['chatgpt', 'gemini', 'grok', 'claude']
if not os.path.exists(D + 'v7_merged_v7only.json'): shutil.copy(D + 'v7_merged.json', D + 'v7_merged_v7only.json')
V7 = json.load(open(D + 'v7_merged_v7only.json'))
CAND = {l['i']: l for l in json.load(open(D + 'v7_candidates.json'))['legs']}
v8legs = {int(l.split('|')[0]) for l in open(D + 'v8_lines.txt') if l.strip()}

def block(text, name):
    m = re.search(rf'{name}_START\s*\n(.*?)\n\s*{name}_END', text, re.S)
    if not m: return []
    rows = [l.strip().strip('`') for l in m.group(1).strip().splitlines() if l.strip() and not l.strip().startswith('```')]
    return [r for r in rows if r.split(',')[0].strip().lower() not in ('leg_no', 'rank', 'tip', 'line_no')]

nums, why, conf, fades, tips, top10, status = {m: {} for m in MODELS}, {}, {}, {}, {}, {}, {}
for m in MODELS:
    f = os.path.join(rdir, m + '.md')
    if not os.path.exists(f) or os.path.getsize(f) < 200: status[m] = 'no reply'; continue
    t = open(f, errors='replace').read()
    for r in block(t, 'BD_V8'):
        c = [x.strip() for x in r.split(',', 4)]
        if not c[0].isdigit(): continue
        if len(c) > 1 and re.fullmatch(r'\d{1,3}', c[1] or '') and int(c[1]) <= 100:
            i = int(c[0]); nums[m][i] = int(c[1])
            if len(c) > 3: why.setdefault(i, {})[m] = c[3][:140]
            if len(c) > 4: conf.setdefault(i, {})[m] = c[4][:10]
    for r in block(t, 'BD_FADE'):
        c = r.split(',', 1)
        if c[0].strip().isdigit(): fades.setdefault(int(c[0]), []).append((m, (c[1] if len(c) > 1 else '').strip()[:140]))
    top10[m] = [int(r.split(',')[1]) for r in block(t, 'BD_TOP10') if len(r.split(',')) > 1 and r.split(',')[1].strip().isdigit()]
    tips[m] = [r.strip().strip('"') for r in block(t, 'BD_TIPS')][:3]
    status[m] = f'{len(nums[m])} of {len(v8legs)} legs graded blind'
live = [m for m in MODELS if nums[m]]
if len(live) < 2: sys.exit(f'Only {len(live)} v8 analyst report(s): {status}')

legs = []
for l in V7['legs']:
    i = l['i']; c = CAND[i]; l = dict(l); l['sys'] = c.get('sys'); l['v7models'] = l['models']
    if i in v8legs:
        ms = {m: nums[m].get(i) for m in MODELS}; v = [x for x in ms.values() if x is not None]
        if len(v) >= 2:
            voices = v + ([c['sys']] if c.get('sys') is not None else [])
            ours = round(statistics.median(voices)); k = l['k']
            if k is None: t, pub = 'N', min(ours, NO_K_MAX)
            elif ours - k >= GAP_REMOVE: t, pub = 'R', None
            elif ours > k: t, pub = 'Y', ours
            else: t, pub = 'G', ours
            l.update(models=ms, med=ours, tier=t, pub=pub, eng='v8', spread=max(v) - min(v), why=why.get(i, {}), conf=conf.get(i, {}), fade=fades.get(i, []))
        else: l['eng'] = 'v7'
    else: l['eng'] = 'v7 (game started before the v8 run)'
    legs.append(l)
L = {l['i']: l for l in legs}
board = sorted([l for l in legs if l['tier'] in ('G', 'Y', 'N') and l['pub'] is not None and l['pub'] >= BOARD_MIN], key=lambda l: -l['pub'])
low = sorted([l for l in legs if l['tier'] in ('G', 'Y', 'N') and l['pub'] is not None and l['pub'] < BOARD_MIN], key=lambda l: -l['pub'])
removed = sorted([l for l in legs if l['tier'] == 'R'], key=lambda l: -(l['med'] - l['k']))
# the Hammer and the parlays only use legs from games that have not started (v8 legs)
fresh = [l for l in board if l['eng'] == 'v8']
ham, ham_why = hammer(fresh)
perf = perfect(fresh)
split = sorted([l for l in legs if l.get('eng') == 'v8' and l.get('spread') is not None and l['spread'] >= 15], key=lambda l: -l['spread'])[:10]
agree = sorted([l for l in legs if l.get('eng') == 'v8' and l.get('spread') is not None and l['spread'] <= 5 and (l['pub'] or 0) >= 70], key=lambda l: -l['pub'])[:10]
votes = {}
for m, t in top10.items():
    for i in t[:10]: votes[i] = votes.get(i, 0) + 1
alltips = {m: tips.get(m, []) for m in MODELS}
res = {'date': day, 'engine': 'v8', 'models': status, 'legs': legs, 'board': [l['i'] for l in board], 'low': [l['i'] for l in low],
       'removed': [l['i'] for l in removed], 'nograde': [l['i'] for l in legs if l['tier'] == 'X'],
       'hammer': {'legs': [l['i'] for l in ham] if ham else [], 'pay': round(payout(ham), 2) if ham else None, 'none': ham_why},
       'perfect': perf, 'split': [l['i'] for l in split], 'agree': [l['i'] for l in agree], 'votes': votes, 'tips': alltips,
       'fades': {str(i): v for i, v in fades.items()}}
json.dump(res, open(D + 'v7_merged.json', 'w'), indent=1)
print('models:', status)
v8b = [l for l in board if l['eng'] == 'v8']
print(f"board {len(board)} ({len(v8b)} regraded by v8: GREEN {sum(l['tier']=='G' for l in v8b)}, YELLOW {sum(l['tier']=='Y' for l in v8b)}) · REMOVED {len(removed)}")
print('hammer:', [L[i]['p'] for i in res['hammer']['legs']], res['hammer']['pay'] or res['hammer']['none'])
for t in perf: print(t['name'], [L[i]['p'] for i in t['legs']], t['pay'], t['hit'], t['none'] or '')

# ---- simulations
IDX = json.load(open(D + 'v8_sim_index.json'))
sims, simtop, simstat = {}, {}, {}
for m in MODELS:
    f = os.path.join(rdir, m + '_sim.md')
    if not os.path.exists(f) or os.path.getsize(f) < 200: simstat[m] = 'no reply'; continue
    t = open(f, errors='replace').read(); sims[m] = {}
    for r in block(t, 'BD_SIM'):
        c = [x.strip() for x in r.split(',', 3)]
        try: n = int(c[0]); p = float(c[1])
        except Exception: continue
        if str(n) in IDX and 0 <= p <= 100: sims[m][n] = {'p': p, 'min': c[2] if len(c) > 2 else '', 'why': (c[3] if len(c) > 3 else '')[:140]}
    simtop[m] = [int(r.split(',')[1]) for r in block(t, 'BD_SIMTOP') if len(r.split(',')) > 1 and r.split(',')[1].strip().isdigit()][:10]
    simstat[m] = f"{len(sims[m])} of {len(IDX)} lines" + (' · ran code' if re.search(r'ran (the )?code|executed', t[:600], re.I) else '')
lines = []
for n, x in IDX.items():
    n = int(n); per = {m: sims[m][n]['p'] for m in sims if n in sims[m]}
    vals = list(per.values()) + [x['oursim']]
    cons = round(statistics.median(vals), 1) if per else None
    lines.append({**x, 'n_line': n, 'agents': per, 'why': {m: sims[m][n]['why'] for m in sims if n in sims[m]},
                  'cons': cons, 'edge': None if cons is None else round(cons - x['be'], 1), 'nagree': sum(1 for v in per.values() if v > x['be'])})
lines.sort(key=lambda z: -(z['edge'] if z['edge'] is not None else -99))
out = {'date': day, 'status': simstat, 'n_lines': len(IDX), 'lines': lines,
       'agent_top': {m: [n for n in simtop.get(m, []) if str(n) in IDX] for m in sims}}
json.dump(out, open(D + 'v8_sims.json', 'w'))
print('sims:', simstat)
for z in lines[:10]: print(z['edge'], z['cons'], 'BE', z['be'], z['odds'], z['nagree'], 'agents', z['agents'], '|', z['player'], z['k'], z['st'], z['g'])
