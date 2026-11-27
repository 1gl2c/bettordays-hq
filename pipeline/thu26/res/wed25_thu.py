"""Grade the 16 Nov 25 board legs that played Thursday (Bears at Lions, Chiefs at Bills) from the Nov 26 results, matched by
pick text, and add them to daily/2026-11-25/results.json. Usage (from pipeline/, after thu26/res/grade.py): python3 thu26/res/wed25_thu.py"""
import json
T = json.load(open('thu26/legs.json')); R26 = {x['i']: x for x in json.load(open('daily/2026-11-26/results.json'))['legs']}
BYP = {l['p']: R26[i] for i, l in enumerate(T, 1) if i in R26}
F = 'daily/2026-11-25/results.json'; R = json.load(open(F)); have = {x['i'] for x in R['legs']}
M = json.load(open('daily/2026-11-25/v7_merged_pick.json')); add = []
for l in M['legs']:
    if l['i'] in have: continue
    g = BYP[l['p']]; add.append(dict(i=l['i'], r=g['r'], act=g['act']))
R['legs'] = sorted(R['legs'] + add, key=lambda x: x['i']); json.dump(R, open(F, 'w'), indent=0)
print('added', len(add), [(a['i'], a['r']) for a in add])
