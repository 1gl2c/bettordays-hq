"""Grade every Nov 27 leg. Player props from each player's ESPN game log row for Nov 26 (ledger/gamelogs.json, refreshed after
the games); team legs from ESPN finals (NBA, NFL, men's college basketball). A player whose team played but who has no row did
not play: void. Writes daily/2026-11-27/results.json. Usage (from pipeline/): python3 fri27/res/grade.py"""
import json, re, subprocess
D = '2026-11-27'
LEGS = json.load(open('fri27/legs.json')); PL = json.load(open('ledger/players.json')); GL = json.load(open('ledger/gamelogs.json'))
cu = lambda u: json.loads(subprocess.run(['curl', '-s', '-m', '30', u], capture_output=True, text=True).stdout)
SC = {}
for sp, q in (('basketball/nba', ''), ('football/college-football', '&groups=80&limit=300'), ('basketball/mens-college-basketball', '&groups=50&limit=400')):
    for e in cu(f"https://site.api.espn.com/apis/site/v2/sports/{sp}/scoreboard?dates={D.replace('-', '')}{q}")['events']:
        c = e['competitions'][0]; tm = {x['team']['abbreviation']: x for x in c['competitors']}
        SC[frozenset(tm) | {sp}] = dict(sp={'basketball/nba': 'NBA', 'football/college-football': 'CFB', 'basketball/mens-college-basketball': 'NCAAB'}[sp], final=c['status']['type']['completed'], sc={k: int(v['score']) for k, v in tm.items()}, name={k: v['team'].get('location', '') for k, v in tm.items()})
TEAM = {'Lakers': 'LAL', 'Suns': 'PHX', 'Nets': 'BKN', '76ers': 'PHI', 'Louisville': None, 'Texas': None, 'Wisconsin': None}
ESPN = {'UTA': 'UTAH'}
def game(l):
    g = SC.get(frozenset(ESPN.get(x, x) for x in l['g'].split('@')) | {'basketball/nba'})
    if g: return g
    if l['sp'] in ('NCAAB', 'CFB'):   # college codes differ: find the game by school name
        name = next(k for k in TEAM if l['p'].startswith(k))
        for k, v in SC.items():
            if any(n.startswith(name) for n in v['name'].values()) and v.get('sp') == l['sp']: return v
    return None
f = lambda x: float(str(x).split('-')[0]) if x not in (None, '', '-') else 0.0
KEYS = {'pts': ['points'], 'reb': ['totalRebounds'], 'ast': ['assists'], '3pm': ['threePointFieldGoalsMade-threePointFieldGoalsAttempted'], 'pra': ['points', 'totalRebounds', 'assists'],
        'recyds': ['receivingYards'], 'rec': ['receptions'], 'rush': ['rushingYards'], 'pass': ['passingYards'], 'pass td': ['passingTouchdowns'], 'int': ['interceptions'], 'td': ['rushingTouchdowns', 'receivingTouchdowns'], 'pa': ['points', 'assists'], 'rushatt': ['rushingAttempts']}
out = []; miss = []
for i, l in enumerate(LEGS, 1):
    p = l['p']; t = p.lower(); g = game(l)
    if l['mkt'] in ('ml', 'spread', 'total'):
        if not g or not g['final']: miss.append((i, p)); continue
        sc = g['sc']
        if l['mkt'] == 'total':
            x = float(re.search(r'(?:over|under) (\d+(?:\.5)?)', t).group(1)); v = sum(sc.values()); un = ' under ' in t; r = 'push' if v == x else ('W' if (v < x if un else v > x) else 'L'); act = v
        else:
            if l['sp'] in ('NCAAB', 'CFB'):
                name = next(k for k in TEAM if p.startswith(k)); tm = next((k for k, n in g['name'].items() if n == name), None) or next(k for k, n in g['name'].items() if n.startswith(name))   # exact school first: Texas is not Texas A&M
            else: tm = TEAM[next(k for k in TEAM if p.startswith(k))]
            opp = [k for k in sc if k != tm][0]; mar = sc[tm] - sc[opp]
            if l['mkt'] == 'ml': r = 'W' if mar > 0 else 'L'
            else:
                x = float(re.search(r'([+-]\d+(?:\.5)?)', p).group(1)); r = 'push' if mar + x == 0 else ('W' if mar + x > 0 else 'L')
            act = mar
        out.append(dict(i=i, r=r, act=act)); continue
    pl = PL.get(f'{D}|v7|{i}')
    if not pl or not pl['espn_id']: miss.append((i, p)); continue
    rows = [x for x in GL.get(f"{pl['sport']}:{pl['espn_id']}", []) if x['date_pt'] == D]
    if not rows:
        if g and g['final']: out.append(dict(i=i, r='void', act=None)); continue
        miss.append((i, p)); continue
    if g and not g['final']: miss.append((i, p)); continue
    v = sum(f(rows[0].get(k)) for k in KEYS[l['mkt']])
    if 'anytime' in t: n, under = 1, False
    elif re.search(r'(\d+)\+', p): n, under = int(re.search(r'(\d+)\+', p).group(1)), False
    else:
        x = float(re.search(r'under (\d+(?:\.5)?)', t).group(1)); under = True
    if under: r = 'W' if v < x else 'L'   # Nov 27 under legs are Kalshi NO on N+: N or more loses, no push
    else: r = 'W' if v >= n else 'L'
    out.append(dict(i=i, r=r, act=v))
json.dump({'legs': sorted(out, key=lambda x: x['i'])}, open(f'daily/{D}/results.json', 'w'), indent=0)
from collections import Counter
print(len(out), 'graded', Counter(x['r'] for x in out)); print('not graded:', miss)
