"""Daily Miracle Parlay (paper ticket, $10 a day). Usage:
  python3 miracle/build.py DATE KALSHI_JSON BOOKS_TXT [SKIP_GAMES comma list] [OUT names comma list]
KALSHI_JSON: live Kalshi markets by series (same shape as dayXX/kalshi.json).
BOOKS_TXT: 'player|market|line|books|fair_over;...' main book line per player and stat (book_novig, most books).
Rules (fixed so the ticket is not hand-picked):
  - NBA player props only. A leg qualifies if the books offer that exact line, or for counts
    (rebounds, assists, threes) one step either side of it. Points/PRA: exact book line only, so
    curve guesses never drive the pick.
  - At least 3 books, Kalshi ask 30 to 90 cents, books' fair chance at or above the Kalshi ask plus
    Kalshi's fee (a 52 vs 52.1 leg like Nov 24 Jokic 10+ assists no longer qualifies).
  - Never: James Harden, players listed OUT, unders on Wemby or Luka (overs only here anyway).
  - One leg per player and stat, at most 2 legs per player.
  - Add legs in tiers: the books' exact line first, then one step above it, then one step below it
    (Poisson runs a little hot one step below the line, so those go last). Inside a tier, best edge first
    (books chance / Kalshi cost after fees). Stop once the ticket pays 1,000x,
    capped at 16 legs. If the pool can't reach 1,000x, post what it reaches.
Writes daily/DATE/miracle.json."""
import json, sys, re, unicodedata
sys.path.insert(0, '.')
import book_ev as B
D, KJ, BT = sys.argv[1:4]
SKIP = set(sys.argv[4].split(',')) if len(sys.argv) > 4 and sys.argv[4] else set()
OUT = {x.strip().lower() for x in sys.argv[5].split(',')} if len(sys.argv) > 5 else set()
nm = lambda s: re.sub(r'[^a-z ]', '', unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode().lower().replace(' jr', '')).strip()
BK = {}
for r in open(BT).read().strip().split(';'):
    p, m, l, b, f = r.split('|'); BK[(nm(p), m.replace('player_', ''))] = (float(l), int(b), float(f))
SM = {'KXNBAPTS': 'points', 'KXNBAREB': 'rebounds', 'KXNBAAST': 'assists', 'KXNBA3PT': 'threes', 'KXNBAPRA': 'points_rebounds_assists'}
LBL = {'points': 'points', 'rebounds': 'rebounds', 'assists': 'assists', 'threes': 'threes', 'points_rebounds_assists': 'PRA'}
K = json.load(open(KJ)); tag = '26' + {'11': 'NOV', '12': 'DEC', '01': 'JAN'}[D[5:7]] + D[8:10]
fee = lambda a: a + 0.07 * a * (1 - a)
pool = []
for s, st in SM.items():
    for m in K.get(s, []):
        if tag not in m['event_ticker']: continue
        g = m['event_ticker'].split('-')[1][7:]
        if g in SKIP: continue
        pl, n = m['yes_sub_title'].rsplit(':', 1); pl = pl.strip(); n = int(n.strip().rstrip('+'))
        if 'harden' in pl.lower() or nm(pl) in {nm(x) for x in OUT}: continue
        a = m.get('yes_ask_dollars')
        if not a: continue
        a = float(a)
        if not 0.30 <= a <= 0.90: continue
        b = BK.get((nm(pl), st))
        if not b or b[1] < 3: continue
        line, books, p = b; need = int(line) + 1
        if st in ('points', 'points_rebounds_assists'):
            if n != need: continue
            q = p
        else:
            if abs(n - need) > 1: continue
            lam = B._solve(lambda x: B.pois_ge(x, need), p, 0, 40); q = B.pois_ge(lam, n)
        if q < fee(a): continue  # Nov 24: the books must beat Kalshi's price after the fee, not just tie it
        tier = 0 if n == need else (1 if n > need else 2)
        pool.append(dict(tier=tier, p=f'{pl} {n}+ {LBL[st]}', pl=pl, st=st, g=g, k=round(a * 100), bk=round(q * 100, 1), exact=n == need, books=books, e=q / fee(a), t=m['ticker']))
pool.sort(key=lambda x: (x['tier'], -x['e']))
legs, used, per = [], set(), {}
cost = prob = 1.0
for x in pool:
    if (x['pl'], x['st']) in used or per.get(x['pl'], 0) >= 2: continue
    legs.append(x); used.add((x['pl'], x['st'])); per[x['pl']] = per.get(x['pl'], 0) + 1
    cost *= fee(x['k'] / 100); prob *= x['bk'] / 100
    if 1 / cost >= 1000 or len(legs) >= 16: break
T = {'date': D, 'stake': 10, 'pays': round(1 / cost), 'chance': round(1 / prob), 'ev': round(100 * (prob / cost - 1), 1), 'pool': len(pool),
     'legs': [{k: x[k] for k in ('p', 'g', 'k', 'bk', 'exact', 'tier', 'books', 't')} for x in legs]}
json.dump(T, open(f'daily/{D}/miracle.json', 'w'), indent=1)
for x in legs: print(f"{x['p']:<34} {x['g']} Kalshi {x['k']} books {x['bk']}{'' if x['exact'] else (' (one step above book line)' if x['tier']==1 else ' (one step below book line)')}")
print(f"{len(legs)} legs, pays about {T['pays']}x, about 1 in {T['chance']}, EV {T['ev']:+}% by the books, pool {len(pool)}")
