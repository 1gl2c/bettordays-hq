"""Our system grade for every Nov 27 leg, computed before the AI numbers are merged (same model as Nov 22, sun22/grade.py).
Props: this season's ESPN game log, hit rate plus last 5 blended with a normal or Poisson curve around the average, shrunk
toward 65, capped (NBA 88, NFL 85, anytime TD 62, 2+ TD 30). Team legs: ESPN betting spread and total turned into a chance
(NFL margin spread 13.5, NBA 12, college 11; totals 13 NFL). Usage: python3 fri27/grade.py -> fri27/wed25.json, fri27/logs.json"""
import json, math, re, subprocess, statistics as S, urllib.parse
from concurrent.futures import ThreadPoolExecutor
LEGS = json.load(open('fri27/legs.json'))
phi = lambda z: 0.5 * (1 + math.erf(z / math.sqrt(2)))
cu = lambda u: json.loads(subprocess.run(['curl', '-s', '-m', '30', u], capture_output=True, text=True).stdout or '{}')
LINE = {'TEX@TAMU': ('TEX', 10.5, 41.5, 14.5), 'MINN@WIS': ('WIS', 9.5, 37.5, 14.5), 'TENN@LOU': ('LOU', 3.5, 148.5, 11.0)}   # ESPN, 3:50 PM PT; NBA team legs have no ESPN line today, so they get no system grade
TEAMAB = {'Louisville': 'LOU', 'Texas': 'TEX', 'Wisconsin': 'WIS'}
def glog(item):
    name, sp = item; lg, path, season = ('nba', 'basketball/nba', 2027) if sp == 'NBA' else ('nfl', 'football/nfl', 2026)
    d = cu('https://site.web.api.espn.com/apis/common/v3/search?limit=8&type=player&query=' + urllib.parse.quote(name))
    its = [i for i in d.get('items', []) if i.get('league') == lg and i['displayName'].replace('.', '') == name.replace('.', '')] or [i for i in d.get('items', []) if i.get('league') == lg]
    if not its: return name, None
    g = cu(f"https://site.web.api.espn.com/apis/common/v3/sports/{path}/athletes/{its[0]['id']}/gamelog?season={season}")
    names = g.get('names', []); ev = g.get('events', {}); rows = []
    for st in g.get('seasonTypes', []):
        if 'Regular' not in st.get('displayName', ''): continue
        for c in st.get('categories', []):
            for e in c.get('events', []):
                r = {'date': ev.get(e['eventId'], {}).get('gameDate', '')}; r.update({n: e['stats'][i] for i, n in enumerate(names) if i < len(e['stats'])}); rows.append(r)
    rows = sorted({r['date']: r for r in rows}.values(), key=lambda r: r['date'], reverse=True)
    return name, {'id': its[0]['id'], 'games': [r for r in rows if r['date'] < '2026-11-27T20:00']}
need = sorted({(l['player'], l['sp']) for l in LEGS if l.get('player')})
with ThreadPoolExecutor(10) as ex: LOG = dict(ex.map(glog, need))
json.dump(LOG, open('fri27/logs.json', 'w'))
f = lambda v: float(str(v).split('-')[0]) if v not in (None, '', '-') else 0.0
KEYS = {'pts': ['points'], 'reb': ['totalRebounds'], 'ast': ['assists'], '3pm': ['threePointFieldGoalsMade-threePointFieldGoalsAttempted'], 'pra': ['points', 'totalRebounds', 'assists'],
        'recyds': ['receivingYards'], 'rec': ['receptions'], 'rush': ['rushingYards'], 'pass': ['passingYards'], 'pass td': ['passingTouchdowns'], 'int': ['interceptions'], 'td': ['rushingTouchdowns', 'receivingTouchdowns'], 'rushatt': ['rushingAttempts'], 'pa': ['points', 'assists']}
COUNT = {'reb', 'ast', '3pm', 'rec', 'pass td', 'int', 'td', 'rushatt'}
rows = []
for i, l in enumerate(LEGS, 1):
    p = l['p']; t = p.lower(); r = dict(i=i, p=p, sp=l['sp'], g=l['g'], t=l['t'], mkt=l['mkt'], sys=None, n='')
    if l['mkt'] in ('ml', 'spread', 'total'):
        if l['g'] not in LINE: r['n'] = 'No independent line; graded by the agents and Kalshi.'; rows.append(r); continue
        fav, sp_, tot, sd = LINE[l['g']]
        if l['mkt'] == 'total':
            x = float(re.search(r'over (\d+(?:\.5)?)', t).group(1)); pr = 1 - phi((x - tot) / (13.0 if l['sp'] == 'NFL' else 15.0)) - (0.02 if x == int(x) else 0); r.update(sys=round(100 * pr), n=f'Book total {tot}.')
        else:
            team = TEAMAB[next(k for k in sorted(TEAMAB, key=len, reverse=True) if p.startswith(k))]; exp = sp_ if team == fav else -sp_
            if l['mkt'] == 'ml': pr = phi(exp / sd)
            else:
                x = float(re.search(r'([+-]\d+(?:\.5)?)', p).group(1)); pr = phi((exp + x) / sd) - (0.02 if x == int(x) else 0)
            r.update(sys=round(100 * pr), n=f'Book line {fav} -{sp_}.')
        rows.append(r); continue
    lg = LOG.get(l['player'])
    if not lg or not lg['games']: r['n'] = 'No game log found.'; rows.append(r); continue
    v = [sum(f(g.get(k)) for k in KEYS[l['mkt']]) for g in lg['games']]; nn = len(v); mu = S.mean(v); under = ' under ' in t
    if 'anytime' in t: k = 1
    elif re.search(r'(\d+)\+', p): k = int(re.search(r'(\d+)\+', p).group(1))
    else:
        x = float(re.search(r'under (\d+(?:\.5)?)', t).group(1)); k = int(x + 0.5) if x % 1 else int(x)
    if l['mkt'] in COUNT:
        lam = max(mu, 0.05); pn = 1 - sum(math.exp(-lam) * lam ** j / math.factorial(j) for j in range(k))
    else:
        sd = max(S.pstdev(v), 0.3 * mu + (5 if l['sp'] == 'NFL' else 2)); pn = 1 - phi((k - 0.5 - mu) / sd)
    hs = sum(x >= k for x in v); h5 = sum(x >= k for x in v[:5]); m5 = min(5, nn)
    ps = (hs + 2 * pn) / (nn + 2); p5 = (h5 + 2 * ps) / (m5 + 2); pr = 0.6 * ps + 0.4 * p5
    if under: pr = 1 - pr; hs = nn - hs; h5 = m5 - h5
    cap = 88 if l['sp'] == 'NBA' else 85
    if l['mkt'] == 'td': cap = 62 if k == 1 else 30
    pct = max(3, min(round(0.8 * 100 * pr + 0.2 * 65), cap))
    r.update(sys=pct, n=f"{'Stayed under' if under else 'Hit'} {hs} of {nn} this season, {h5} of {m5} last 5 (avg {mu:.1f}).")
    rows.append(r)
json.dump({'rows': rows}, open('fri27/wed25.json', 'w'), indent=1)
for r in rows: print(r['i'], r['sys'], r['p'], '|', r['n'])
