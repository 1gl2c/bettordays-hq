"""Nov 21 results: board record, tiers, Brier for each AI / our system / our grade / Kalshi / sportsbooks on the same legs,
favorite-edge legs, the Safe Hammer, our Python sim, and what a stricter Master filter would have done."""
import json, sys
sys.path.insert(0, 'sat21/res')
from score_sims import grade as sgrade   # noqa
DAY = '2026-11-21'
M = json.load(open(f'daily/{DAY}/v7_merged.json')); L = M['legs']
G = {r['p']: r for r in json.load(open('sat21/sat21_graded.json'))['rows']}
BK = json.load(open(f'daily/{DAY}/book_fair.json'))
for l in L: l['r'] = G[l['p']].get('r'); l['act'] = G[l['p']].get('act'); l['bk'] = BK.get(str(l['i']))
gr = [l for l in L if l['r'] in ('W', 'L')]
y = lambda l: 1 if l['r'] == 'W' else 0
rec = lambda ls: f"{sum(y(l) for l in ls)}-{sum(1 - y(l) for l in ls)}" + (f" ({round(100 * sum(y(l) for l in ls) / len(ls))}%)" if ls else '')
fee = lambda q: 0.07 * q * (1 - q)
def roi(ls):
    ls = [l for l in ls if l.get('k')]
    if not ls: return None
    return round(100 * sum((1 / (l['k'] / 100 + fee(l['k'] / 100)) - 1) if y(l) else -1 for l in ls) / len(ls), 1)
def br(ps): return round(sum((p - y(l)) ** 2 for p, l in ps) / len(ps), 4) if ps else None
out = {}
board = [l for l in gr if l['i'] in M['board']]
out['board_70'] = (rec(board), roi(board))
out['board_70_pregame_only'] = rec([l for l in board if l.get('fl') not in ('LIVE', 'DONE')])
for t in 'GYNR':
    ls = [l for l in gr if l['tier'] == t and (t == 'R' or (l['pub'] or 0) >= 70)]; out['tier_' + t + ('' if t == 'R' else '_70+')] = (rec(ls), roi(ls))
out['all_published'] = (rec([l for l in gr if l['tier'] in 'GYN' and l['pub'] is not None]), roi([l for l in gr if l['tier'] in 'GYN' and l['pub'] is not None]))
for lo, hi in [(85, 101), (80, 85), (75, 80), (70, 75), (60, 70), (50, 60), (0, 50)]:
    ls = [l for l in gr if l['pub'] is not None and lo <= l['pub'] < hi]; out[f'pub_{lo}-{hi - 1}'] = (rec(ls), roi(ls))
fav = [l for l in gr if l.get('k') and 80 <= l['k'] <= 92 and (l['pub'] or 0) >= 75 and l['tier'] in ('G', 'Y')]
out['favorite_edge_legs'] = (rec(fav), roi(fav), [f"{l['p']} {l['r']}" for l in fav])
out['by_sport_published'] = {sp: rec([l for l in gr if l['sp'] == sp and l['tier'] in 'GYN' and l['pub'] is not None]) for sp in ('NBA', 'CFB', 'CBB', 'UFC')}
# Brier: blind AI legs that were graded before their game started (started/finished legs are not blind tests)
blind = [l for l in gr if l.get('fl') not in ('LIVE', 'DONE') and not l.get('alt_rung')]
B = {}
for m in ['chatgpt', 'gemini', 'grok', 'claude']:
    ps = [(l['models'][m] / 100, l) for l in blind if l['models'].get(m) is not None]
    pk = [(l['k'] / 100, l) for _, l in ps if l.get('k')]
    B[m] = {'brier': br(ps), 'n': len(ps), 'brier_priced': br([(l['models'][m] / 100, l) for _, l in pk]), 'kalshi_same': br(pk), 'n_priced': len(pk)}
pk = [l for l in blind if l.get('k')]
B['system'] = {'brier_priced': br([(l['sys'] / 100, l) for l in pk if l.get('sys') is not None]), 'n': sum(1 for l in pk if l.get('sys') is not None)}
B['our_grade'] = {'brier_priced': br([(l['med'] / 100, l) for l in pk if l.get('med') is not None]), 'n': len(pk)}
B['kalshi'] = {'brier_priced': br([(l['k'] / 100, l) for l in pk]), 'n': len(pk)}
bb = [l for l in gr if l.get('bk') is not None]
B['books_vs_others_same_legs'] = {'n': len(bb), 'books': br([(l['bk'] / 100, l) for l in bb]), 'kalshi': br([(l['k'] / 100, l) for l in bb if l.get('k')]),
                                  'our_grade': br([(l['med'] / 100, l) for l in bb if l.get('med') is not None]), 'legs': [(l['p'], l['bk'], l.get('k'), l.get('med'), l['r']) for l in bb]}
out['brier'] = B
LL = {l['i']: l for l in L}
out['hammer'] = {'kind': M['hammer'].get('kind'), 'legs': [(LL[i]['p'], LL[i]['r'], LL[i]['act']) for i in M['hammer']['legs']],
                 'hit': all(LL[i]['r'] == 'W' for i in M['hammer']['legs']), 'pay_net': M['hammer'].get('pay_net')}
out['misses_on_board'] = [(l['pub'], l['p'], l['act'], l['tier'], l.get('k'), l.get('bk')) for l in board if l['r'] == 'L']
out['removed_results'] = [(l['p'], l['med'], l.get('k'), l['r'], l['act']) for l in gr if l['tier'] == 'R']
# "Master filter" what-ifs on the published NBA/pregame legs
pre = [l for l in gr if l['tier'] in 'GY' and l['pub'] is not None and l.get('fl') not in ('LIVE', 'DONE')]
W = {}
W['pub>=75 & G/Y'] = rec([l for l in pre if l['pub'] >= 75])
W['pub>=75 & k>=80'] = rec([l for l in pre if l['pub'] >= 75 and l['k'] >= 80])
W['pub>=75 & k>=80 & AIs within 12'] = rec([l for l in pre if l['pub'] >= 75 and l['k'] >= 80 and (l.get('spread') or 0) < 12])
W['pub>=75 & k>=80 & books>=80'] = rec([l for l in pre if l['pub'] >= 75 and l['k'] >= 80 and (l.get('bk') or 0) >= 80])
W['k>=85 any grade'] = rec([l for l in pre if l['k'] >= 85])
out['filter_whatifs'] = W
json.dump({'legs': [{k: l.get(k) for k in ('i', 'p', 'pub', 'sys', 'med', 'k', 'bk', 'tier', 'eng', 'fl', 'models', 'r', 'act', 'sp', 'stat', 'ty', 'spread')} for l in L], 'summary': out},
          open('sat21/res/analysis.json', 'w'), indent=1)
for k, v in out.items(): print(k, '=>', json.dumps(v) if not isinstance(v, str) else v)
