import json
M = json.load(open('daily/2026-11-26/v7_merged.json')); RS = {x['i']: x for x in json.load(open('daily/2026-11-26/results.json'))['legs']}
BYP = {l['p']: RS.get(l['i']) for l in M['legs']}
fmt = lambda a: (int(a) if isinstance(a, float) and a.is_integer() else a)
def grade(p):
    g = BYP[p]   # every Thanksgiving ticket leg is on the board; a KeyError means a typo, not a pending leg
    return {'void': 'V', 'push': 'P'}.get(g['r'], g['r']), fmt(g['act'])
