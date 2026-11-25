"""Self-learning Safe Hammer layer (approved by Ace Nov 24 2026). Run nightly after the ledger is rebuilt:
    python3 learn/hammer_learn.py DATE
Reads ledger/ledger_rows.json (graded legs priced before the game, Kalshi 80 to 92 cents, last 30 days).
For each group it compares how often the legs hit with what Kalshi charged:
  level 'stat'   : stat type (ast, 3pm, pra, pts, reb, ml, ...)
  level 'detail' : stat x price band (80-84, 85-88, 89-92) x books gap (books 3+ above Kalshi / within 3 / below / no books)
Shrinkage: 20 pseudo-legs at the group's own average price, so a small sample can't swing it.
Status: 'block' when 25+ legs and the shrunk hit rate is below the fee-adjusted price,
        'prefer' when 25+ legs and the shrunk hit rate beats the fee-adjusted price by 2+ points,
        'watch' otherwise (too few legs, or close to the price).
Writes learn/hammer_learn.json (current state) and appends every status change to learn/hammer_learn_log.json.
Nothing is estimated: every number is counted from graded legs."""
import json, sys, datetime as dt
D = sys.argv[1]; d0 = (dt.date.fromisoformat(D) - dt.timedelta(days=30)).isoformat()
R = [r for r in json.load(open('ledger/ledger_rows.json')) if r['result'] in ('W', 'L') and r['priced_pregame'] and r['kalshi_pick'] is not None
     and 80 <= r['kalshi_pick'] <= 92 and d0 < r['slate_date'] <= D]
band = lambda k: '80-84' if k < 85 else '85-88' if k < 89 else '89-92'
def gap(r):
    if r.get('books_pick') is None: return 'no books'
    g = r['books_pick'] - r['kalshi_pick']; return 'books 3+ above' if g >= 3 else 'books 3+ below' if g <= -3 else 'within 3'
fee = lambda p: p + 0.07 * p * (1 - p)
def summ(rows):
    n = len(rows); w = sum(r['result'] == 'W' for r in rows); p = sum(r['kalshi_pick'] for r in rows) / n / 100
    shr = (w + 20 * p) / (n + 20); fp = fee(p)
    st = 'block' if n >= 25 and shr < fp else 'prefer' if n >= 25 and shr >= fp + 0.02 else 'watch'
    return dict(n=n, w=w, hit=round(100 * w / n, 1), price=round(100 * p, 1), shrunk=round(100 * shr, 1), fee_price=round(100 * fp, 1), status=st)
G = {}
for r in R:
    s = r['stat'] or 'other'
    G.setdefault(('stat', s), []).append(r); G.setdefault(('detail', f"{s} · {band(r['kalshi_pick'])} · {gap(r)}"), []).append(r)
out = {'as_of': D, 'window': f'{d0} to {D}', 'legs': len(R), 'groups': sorted([dict(level=k[0], group=k[1], **summ(v)) for k, v in G.items()], key=lambda x: (x['level'] != 'stat', -x['n']))}
try: old = {g['group']: g['status'] for g in json.load(open('learn/hammer_learn.json'))['groups']}
except FileNotFoundError: old = {}
try: log = json.load(open('learn/hammer_learn_log.json'))
except FileNotFoundError: log = []
for g in out['groups']:
    was = old.get(g['group'], 'new')
    if was != g['status'] and not (was == 'new' and g['status'] == 'watch'):
        log.append(dict(date=D, group=g['group'], was=was, now=g['status'], n=g['n'], hit=g['hit'], shrunk=g['shrunk'], fee_price=g['fee_price']))
json.dump(out, open('learn/hammer_learn.json', 'w'), indent=1); json.dump(log, open('learn/hammer_learn_log.json', 'w'), indent=1)
for g in out['groups'][:12]: print(g)
print('legs', len(R), '| changes logged', sum(1 for x in log if x['date'] == D))
