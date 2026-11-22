"""Sportsbook no-vig fair chance for every Nov 22 player-prop leg the books price (yards, receptions, attempts, INTs, NBA)."""
import json, re, sys
sys.path.insert(0, '.')
import book_ev as B
rows = json.load(open('daily/2026-11-22/book_novig.json')); L = json.load(open('sun22/legs.json'))
ST = {'receiving yards': 'recyds', 'receptions': 'rec', 'rushing yards': 'rushyds', 'rushing attempts': 'rushatt', 'passing yards': 'passyds', 'interceptions': 'int', 'threes': '3pm', 'rebounds': 'reb'}
ALIAS = {'James Cook': 'James Cook III', 'Wendell Carter Jr.': 'Wendell Carter Jr'}
out = {}
for i, l in enumerate(L, 1):
    p = l['p']; t = p.lower()
    st = next((v for k, v in ST.items() if k in t), None)
    if not st or 'longest' in t or 'rushing + receiving' in t: continue
    name = re.split(r' (?:\d|under)', p)[0]
    m = re.search(r'(\d+)\+', p); u = re.search(r'under (\d+(?:\.5)?)', t)
    n = int(m.group(1)) if m else int(float(u.group(1)) + 0.5) if u else None
    if n is None: continue
    r = B.fair_rung(rows, ALIAS.get(name, name), st, n)
    if not r: continue
    q = r[0] if not u else 1 - r[0]
    out[i] = round(100 * q, 1)
json.dump(out, open('daily/2026-11-22/book_fair.json', 'w')); print(len(out), 'legs priced by the books')
