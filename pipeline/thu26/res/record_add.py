"""Append graded, published legs to record.json: Nov 26 (Thanksgiving) and the 16 Nov 25 board legs that played Thursday."""
import json, re
R = json.load(open('../record.json')); L = R['legs']; n0 = len(L)
assert not any(x['d'] == 'Nov 26' for x in L)
have25 = {x['p'] for x in L if x['d'] == 'Nov 25'}
def add(day, M, RS, skip=()):
    for l in M['legs']:
        r = RS.get(l['i'], {}).get('r')
        if l.get('tier') not in ('G', 'Y', 'N') or l.get('pub') is None or r not in ('W', 'L') or l['p'] in skip: continue
        st = {'td': 'atd'}.get(l.get('stat') or l.get('ty'), l.get('stat') or l.get('ty'))
        L.append({'d': day, 'wk': 'Nov 23-29', 'sp': l['sp'], 'st': st, 'dir': 'u' if ' under ' in l['p'].lower() else 'o', 'g': l['pub'], 'res': r, 'k': l.get('k'), 'ln': None, 'p': l['p']})
ld = lambda d, f: (json.load(open(f'daily/{d}/{f}')), {x['i']: x for x in json.load(open(f'daily/{d}/results.json'))['legs']})
add('Nov 25', *ld('2026-11-25', 'v7_merged_pick.json'), skip=have25)
add('Nov 26', *ld('2026-11-26', 'v7_merged.json'))
n = len(L); nk = sum(1 for x in L if x['k'] is not None)
R['meta'] = R['meta'].replace('Nov 4 to Nov 25', 'Nov 4 to Nov 26')
R['meta'] = re.sub(r'<b>\d+</b> graded legs', f'<b>{n}</b> graded legs', R['meta'], 1); R['meta'] = re.sub(r'<b>\d+</b> have a Kalshi', f'<b>{nk}</b> have a Kalshi', R['meta'], 1)
json.dump(R, open('../record.json', 'w'))
a = L[n0:]; print('added', len(a), 'W', sum(x['res'] == 'W' for x in a), {d: sum(x['d'] == d for x in a) for d in ('Nov 25', 'Nov 26')}, 'total', n, 'priced', nk)
