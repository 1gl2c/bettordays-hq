"""Sim picks that need a second source (Nov 22). A sim line becomes a pick only when:
 1) our sim is 5+ points above break-even after fees,
 2) the sportsbooks' no-vig chance is also 2+ above break-even (independent agreement that Kalshi is cheap),
 3) the gap is 15 or less (bigger gaps are usually news the sim has not seen: flagged 'check the news').
Chance used for the pick = the average of the sim and the books."""
import json, sys
sys.path.insert(0, '.')
import book_ev as B
A = json.load(open('betamon23/all_lines.json')); rows = json.load(open('daily/2026-11-23/book_novig.json'))
picks, news = [], []
for x in A:
    be = x['be']; sim = x['sim']
    if sim < be + 5: continue
    r = B.fair_rung(rows, x['player'], x['st'], x['k']) if x['st'] in B.MARKET else None
    bk = round(100 * r[0], 1) if r else None
    row = {k: x[k] for k in ('player', 'team', 'st', 'k', 'ask', 'be', 'sim', 'edge', 'g', 'ticker')}; row['books'] = bk
    if sim - be > 15: news.append(row); continue
    if bk is None or bk < be + 2: continue
    row['p_pick'] = round((sim + bk) / 2, 1); row['edge_pick'] = round(row['p_pick'] - be, 1); picks.append(row)
picks.sort(key=lambda r: -r['edge_pick'])
json.dump({'picks': picks, 'check_news': news}, open('betamon23/confirmed.json', 'w'), indent=1)
for r in picks: print('PICK', r['player'], r['k'], r['st'], 'sim', r['sim'], 'books', r['books'], 'BE', r['be'], '->', r['p_pick'])
for r in news: print('NEWS', r['player'], r['k'], r['st'], 'sim', r['sim'], 'books', r['books'], 'BE', r['be'])
