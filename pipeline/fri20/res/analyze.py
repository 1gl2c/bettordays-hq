"""Nov 20 results: board record, tiers, each model's Brier vs Kalshi on the same legs, favorite-edge legs, tickets."""
import json, statistics
M = json.load(open('daily/2026-11-20/v7_merged.json')); L = M['legs']
G = {r['p']: r for r in json.load(open('fri20/fri20_graded.json'))['rows']}
for l in L: l['r'] = G[l['p']].get('r'); l['act'] = G[l['p']].get('act')
gr = [l for l in L if l['r'] in ('W', 'L')]
y = lambda l: 1 if l['r'] == 'W' else 0
rec = lambda ls: f"{sum(y(l) for l in ls)}-{sum(1-y(l) for l in ls)}" + (f" ({round(100*sum(y(l) for l in ls)/len(ls))}%)" if ls else '')
fee = lambda q: 0.07 * q * (1 - q)
def roi(ls):
    ls = [l for l in ls if l.get('k')]
    if not ls: return None
    return round(100 * sum((1 / (l['k']/100 + fee(l['k']/100)) - 1) if y(l) else -1 for l in ls) / len(ls), 1)   # equal $1 stakes
out = {}
board = [l for l in gr if l['i'] in M['board']]
out['board_70'] = (rec(board), roi(board))
for t in 'GYNR': ls = [l for l in gr if l['tier'] == t and (t == 'R' or (l['pub'] or 0) >= 70)]; out['tier_' + t] = (rec(ls), roi(ls))
out['all_graded'] = rec([l for l in gr if l['tier'] != 'R'])
for lo, hi in [(85, 101), (80, 85), (75, 80), (70, 75), (60, 70), (0, 60)]:
    ls = [l for l in gr if l['pub'] is not None and lo <= l['pub'] < hi]; out[f'pub_{lo}-{hi-1}'] = (rec(ls), roi(ls))
fav = [l for l in gr if l.get('k') and 80 <= l['k'] <= 92 and (l['pub'] or 0) >= 75 and l['tier'] in ('G', 'Y')]
out['favorite_edge_legs'] = (rec(fav), roi(fav), [l['p'] + ' ' + l['r'] for l in fav])
k80 = [l for l in gr if l.get('k') and 80 <= l['k'] <= 92]; out['all_kalshi_80_92'] = (rec(k80), roi(k80))
# Brier on v8 legs (blind agent grades), same legs for every source
v8 = [l for l in gr if l.get('eng') == 'v8' and l.get('k')]
def br(ps): return round(sum((p - y(l)) ** 2 for p, l in ps) / len(ps), 4) if ps else None
B = {}
for m in ['chatgpt', 'gemini', 'grok', 'claude']:
    ps = [(l['models'][m] / 100, l) for l in v8 if l['models'].get(m) is not None]
    B[m] = (br(ps), len(ps), br([(l['k'] / 100, l) for _, l in ps]))
B['system'] = (br([(l['sys'] / 100, l) for l in v8 if l.get('sys') is not None]), len(v8))
B['our_grade(med)'] = (br([(l['med'] / 100, l) for l in v8]), len(v8))
B['kalshi'] = (br([(l['k'] / 100, l) for l in v8]), len(v8))
out['brier_v8_legs (model, n, kalshi on the same legs)'] = B
pk = [l for l in gr if l.get('k') and l['tier'] != 'R' and l['pub'] is not None]
out['brier_all_priced'] = {'published': br([(l['pub'] / 100, l) for l in pk if l['pub'] is not None]), 'system': br([(l['sys'] / 100, l) for l in pk if l.get('sys') is not None]), 'kalshi': br([(l['k'] / 100, l) for l in pk]), 'n': len(pk)}
LL = {l['i']: l for l in L}
out['hammer'] = [(LL[i]['p'], LL[i]['r']) for i in M['hammer']['legs']]
out['perfect'] = {t['name']: [(LL[i]['p'], LL[i]['r']) for i in t['legs']] for t in M['perfect']}
out['misses_70'] = [(l['pub'], l['p'], l['act'], l['tier'], l.get('k')) for l in board if l['r'] == 'L']
json.dump({'legs': [{k: l.get(k) for k in ('i', 'p', 'pub', 'sys', 'med', 'k', 'tier', 'eng', 'models', 'r', 'act', 'sp', 'stat', 'ty')} for l in L], 'summary': out}, open('fri20/res/analysis.json', 'w'), indent=1)
for k, v in out.items(): print(k, '=>', v)
