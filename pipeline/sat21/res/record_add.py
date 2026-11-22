"""Append Nov 21 graded legs to record.json (Proof explorer): the 108 published legs in model_picks (the REMOVED KD 20+ is not published)."""
import json
R = json.load(open('../record.json')); L = R['legs']
assert not any(x['d'] == 'Nov 21' for x in L)
A = json.load(open('sat21/res/analysis.json'))['legs']
n0 = len(L)
for l in A:
    if l['tier'] not in ('G', 'Y', 'N') or l['pub'] is None or l['r'] not in ('W', 'L'): continue
    g = l['pub'] if l['pub'] is not None else l['med']
    if g is None: continue
    st = l.get('stat') or l.get('ty')
    st = {'td': 'atd'}.get(st, st)
    L.append({'d': 'Nov 21', 'wk': 'Nov 16-22', 'sp': l['sp'], 'st': st, 'dir': 'u' if ' under ' in l['p'].lower() else 'o',
              'g': g, 'res': l['r'], 'k': l['k'], 'ln': None, 'p': l['p']})
n = len(L); nk = sum(1 for x in L if x['k'] is not None)
R['meta'] = f"Source: the model_picks database. <b>{n}</b> graded legs from Nov 4 to Nov 21, 2026. <b>{nk}</b> have a Kalshi price. Nov 4 to 17 use the last Kalshi quote before tip-off; Nov 18 on uses the price at the moment we graded (timestamped). Pushes on whole-number lines are not counted. Results corrected after box-score checks are logged in the database."
json.dump(R, open('../record.json', 'w'))
print('added', n - n0, 'total', n, 'priced', nk)
