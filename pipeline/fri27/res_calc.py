"""grade(p) for any Nov 27 leg: board legs from daily/2026-11-27/results.json, anything else (sim lines, Miracle legs) from the
ESPN box scores saved in fri27/res/box_all.json. A player with no box line did not play: void."""
import json, re, unicodedata
M = json.load(open('daily/2026-11-27/v7_merged.json')); RS = {x['i']: x for x in json.load(open('daily/2026-11-27/results.json'))['legs']}
BYP = {l['p']: RS.get(l['i']) for l in M['legs']}
BOX = json.load(open('fri27/res/box_all.json'))
nrm = lambda s: unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode().lower().replace('.', '').replace("'", '').strip()
fmt = lambda a: (int(a) if isinstance(a, float) and a.is_integer() else a)
ST = [('points, rebounds and assists', ('pts', 'reb', 'ast')), ('pra', ('pts', 'reb', 'ast')), ('points', ('pts',)), ('rebounds', ('reb',)), ('assists', ('ast',)), ('threes', ('3pm',))]
def grade(p):
    if p in BYP and BYP[p]:
        g = BYP[p]; return {'void': 'V', 'push': 'P'}.get(g['r'], g['r']), fmt(g['act'])
    t = p.lower(); under = ' under ' in t
    name = re.split(r' (?:\d|under )', p)[0]; b = BOX.get(nrm(name))
    if b is None: return 'V', None
    keys = next(k for s, k in ST if s in t); v = sum(b[k] for k in keys)
    if under: n = int(re.search(r'under (\d+)', t).group(1)); return ('W' if v < n else 'L'), v
    n = int(re.search(r'(\d+)\+', p).group(1)); return ('W' if v >= n else 'L'), v
