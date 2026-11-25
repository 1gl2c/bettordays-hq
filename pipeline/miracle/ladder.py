"""Miracle "ladder" version (agreed Nov 24 2026, starts Nov 25). Usage:
  python3 miracle/ladder.py DATE KALSHI_JSON BOOK_LINES_TXT [SKIP_GAMES comma list] [OUT names comma list]
BOOK_LINES_TXT: every posted book line, 'player|market|line|books|fair_over;...' (all lines from book_novig, not only the main one).
Rules:
  - Threes, assists and PRA only (points and rebounds only if Ace approves; pass them with APPROVE='name stat,...' env).
  - Every rung must be a line at least 2 books actually post (no curve estimates), with the books' fair chance beating
    Kalshi's ask plus the fee plus 0.2 points.
  - For each player and stat, climb to the highest qualifying rung (biggest payout that still has the edge).
  - One leg per player and stat, at most 2 legs per player, best edge first, stop at 1,000x (cap 12 legs).
Writes daily/DATE/miracle_ladder.json."""
import json, os, re, sys, unicodedata
D, KJ, BT = sys.argv[1:4]
SKIP = set(sys.argv[4].split(',')) if len(sys.argv) > 4 and sys.argv[4] else set()
OUT = {x.strip() for x in sys.argv[5].split(',')} if len(sys.argv) > 5 else set()
APPROVE = {x.strip().lower() for x in os.environ.get('APPROVE', '').split(',') if x.strip()}
nm = lambda s: re.sub(r'[^a-z ]', '', unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode().lower().replace(' jr', '')).strip()
BK = {}
for r in open(BT).read().strip().split(';'):
    p, m, l, b, f = r.split('|'); m = m.replace('player_', ''); BK[(nm(p), m, int(float(l) + 0.5))] = (int(b), float(f))
SM = {'KXNBA3PT': 'threes', 'KXNBAAST': 'assists', 'KXNBAPRA': 'points_rebounds_assists', 'KXNBAPTS': 'points', 'KXNBAREB': 'rebounds'}
LBL = {'threes': 'threes', 'assists': 'assists', 'points_rebounds_assists': 'PRA', 'points': 'points', 'rebounds': 'rebounds'}
fee = lambda a: a + 0.07 * a * (1 - a)
K = json.load(open(KJ)); tag = '26' + {'11': 'NOV', '12': 'DEC', '01': 'JAN'}[D[5:7]] + D[8:10]
best = {}
for s_, st in SM.items():
    for m in K.get(s_, []):
        if tag not in m['event_ticker']: continue
        g = m['event_ticker'].split('-')[1][7:]
        if g in SKIP: continue
        pl, n = m['yes_sub_title'].rsplit(':', 1); pl = pl.strip(); n = int(n.strip().rstrip('+'))
        if 'harden' in pl.lower() or pl in OUT: continue
        if st in ('points', 'rebounds') and f'{nm(pl)} {LBL[st]}' not in APPROVE: continue
        a = m.get('yes_ask_dollars')
        if not a: continue
        a = float(a)
        if not 0.05 <= a <= 0.92: continue
        b = BK.get((nm(pl), st, n))
        if not b or b[0] < 2 or b[1] < fee(a) + 0.002: continue   # 2+ books on that exact rung
        x = dict(p=f'{pl} {n}+ {LBL[st]}', pl=pl, st=st, n=n, g=g, k=round(a * 100), bk=round(b[1] * 100, 1), books=b[0], e=b[1] / fee(a), t=m['ticker'])
        key = (pl, st)
        if key not in best or n > best[key]['n']: best[key] = x   # highest qualifying rung
pool = sorted(best.values(), key=lambda x: -x['e'])
legs, per = [], {}; cost = prob = 1.0
for x in pool:
    if per.get(x['pl'], 0) >= 2: continue
    legs.append(x); per[x['pl']] = per.get(x['pl'], 0) + 1; cost *= fee(x['k'] / 100); prob *= x['bk'] / 100
    if 1 / cost >= 1000 or len(legs) >= 12: break
T = {'date': D, 'stake': 10, 'pays': round(1 / cost), 'chance': round(1 / prob), 'ev': round(100 * (prob / cost - 1), 1), 'pool': len(pool),
     'legs': [{k: x[k] for k in ('p', 'g', 'k', 'bk', 'books', 't')} for x in legs]}
json.dump(T, open(f'daily/{D}/miracle_ladder.json', 'w'), indent=1)
for x in legs: print(f"{x['p']:<34} {x['g']} Kalshi {x['k']} books {x['bk']} ({x['books']} books)")
print(f"{len(legs)} legs, about {T['pays']}x at single prices, about 1 in {T['chance']} by the books, pool {len(pool)}")
