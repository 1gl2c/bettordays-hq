"""Append Nov 25 graded, published legs (GREEN, YELLOW, no-Kalshi tiers with a published grade) to record.json, from the board as posted."""
import json
R = json.load(open('../record.json')); L = R['legs']
assert not any(x['d'] == 'Nov 25' for x in L)
M = json.load(open('daily/2026-11-25/v7_merged_pick.json')); RS = {x['i']: x for x in json.load(open('daily/2026-11-25/results.json'))['legs']}
n0 = len(L)
for l in M['legs']:
    r = RS.get(l['i'], {}).get('r')
    if l.get('tier') not in ('G', 'Y', 'N') or l.get('pub') is None or r not in ('W', 'L'): continue
    st = {'td': 'atd'}.get(l.get('stat') or l.get('ty'), l.get('stat') or l.get('ty'))
    L.append({'d': 'Nov 25', 'wk': 'Nov 23-29', 'sp': l['sp'], 'st': st, 'dir': 'u' if ' under ' in l['p'].lower() else 'o', 'g': l['pub'], 'res': r, 'k': l.get('k'), 'ln': None, 'p': l['p']})
n = len(L); nk = sum(1 for x in L if x['k'] is not None)
R['meta'] = R['meta'].replace('Nov 4 to Nov 24', 'Nov 4 to Nov 25')
import re; R['meta'] = re.sub(r'<b>\d+</b> graded legs', f'<b>{n}</b> graded legs', R['meta'], 1); R['meta'] = re.sub(r'<b>\d+</b> have a Kalshi', f'<b>{nk}</b> have a Kalshi', R['meta'], 1)
json.dump(R, open('../record.json', 'w'))
add = L[n0:]; print('added', len(add), 'W', sum(x['res'] == 'W' for x in add), 'total', n, 'priced', nk)
