"""Sportsbook no-vig fair chance for each Nov 25 prop leg (The Odds API pull at 3:05 PM PT, book_novig view).
The database returned, per leg, the book line at the exact rung if any book offers it, else the line with the most books.
Exact rung: the books' own number. Otherwise moved to the rung with book_ev's curves (normal for points and yards,
Poisson for counts). Unders = 1 minus the over. Usage: python3 wed25/books.py -> daily/2026-11-25/book_fair.json"""
import json, re, sys
sys.path.insert(0, '.')
import book_ev as B
RAW = open('wed25/book_rows.txt').read().strip()
L = json.load(open('wed25/legs.json'))
CURVE = {'pts': 'pts', 'recyds': 'recyds', 'rush': 'rushyds', 'pass': 'passyds', 'pra': 'pra'}
SD = dict(B.SD, pra=lambda mu: max(4.5, 0.25 * mu))
out = {}
for part in RAW.split(';'):
    i, r = part.split(':', 1); i = int(i); r = json.loads(r)
    if r is None: continue
    line, books, p = float(r[0]), int(r[1]), float(r[2]); l = L[i - 1]; t = l['p'].lower()
    if re.search(r'(\d+)\+', l['p']): n = int(re.search(r'(\d+)\+', l['p']).group(1))
    else:
        x = float(re.search(r'under (\d+(?:\.5)?)', t).group(1)); n = int(x + 0.5) if x % 1 else int(x)
    need = int(line) + 1
    if need == n: q = p
    else:
        c = CURVE.get(l['mkt'])
        if c:
            f = SD[c]; mu = B._solve(lambda m: B.norm_ge(m, f(m), need), p, 0.0, 700.0); q = B.norm_ge(mu, f(mu), n)
        else:
            lam = B._solve(lambda x: B.pois_ge(x, need), p, 0.0, 40.0); q = B.pois_ge(lam, n)
    if ' under ' in t: q = 1 - q
    out[i] = {'bk': round(100 * q, 1), 'books': books, 'line': line, 'exact': need == n}
json.dump(out, open('daily/2026-11-25/book_fair.json', 'w'), indent=0)
K = json.load(open('wed25/kmatch.json'))
for i, v in out.items(): print(i, L[i - 1]['p'], '| books', v['bk'], '| Kalshi', K[str(i)]['k'], '| exact' if v['exact'] else f"| from {v['line']}")
