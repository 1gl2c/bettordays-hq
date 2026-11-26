import json, sys
sys.path.insert(0, '.')
from wed25.res.box import grade as bgrade
M = json.load(open('daily/2026-11-25/v7_merged_pick.json')); RS = {x['i']: x for x in json.load(open('daily/2026-11-25/results.json'))['legs']}
BYP = {l['p']: RS.get(l['i']) for l in M['legs']}
fmt = lambda a: (int(a) if isinstance(a, float) and a.is_integer() else a)
def grade(p):
    g = BYP.get(p)
    if g: return {'void': 'V', 'push': 'P'}.get(g['r'], g['r']), fmt(g['act'])
    if p in BYP: return None, None   # on the board, still pending (Thursday)
    r, a = bgrade(p); return r, (None if r == 'V' else int(a))
