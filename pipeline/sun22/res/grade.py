"""Grade every Nov 22 leg. Player props from each player's ESPN game log row for Nov 22 (ledger/gamelogs.json, refreshed
after the games); team legs from ESPN finals (with half scores for the first-half spread); tennis and NHL from ESPN.
A player whose team played but who has no row for the game did not play: the leg is void (Kalshi voids it).
Writes daily/2026-11-22/results.json ({"legs": [{"i", "r", "act"}]}). Usage (from pipeline/): python3 sun22/res/grade.py"""
import json, re, subprocess, unicodedata
D = '2026-11-22'
LEGS = json.load(open('sun22/legs.json')); PL = json.load(open('ledger/players.json')); GL = json.load(open('ledger/gamelogs.json'))
cu = lambda u: json.loads(subprocess.run(['curl', '-s', '-m', '30', u], capture_output=True, text=True).stdout)
nrm = lambda s: re.sub(r'[^a-z]', '', unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode().lower())
SC = {}
for sp in ('football/nfl', 'basketball/nba', 'hockey/nhl'):
    for e in cu(f"https://site.api.espn.com/apis/site/v2/sports/{sp}/scoreboard?dates={D.replace('-', '')}")['events']:
        c = e['competitions'][0]; tm = {x['team']['abbreviation']: x for x in c['competitors']}
        SC[frozenset(tm)] = dict(final=c['status']['type']['completed'], sc={k: int(v['score']) for k, v in tm.items()},
                                 h1={k: sum(int(q['value']) for q in (v.get('linescores') or [])[:2]) for k, v in tm.items()}, name={k: v['team']['displayName'] for k, v in tm.items()})
NICK = {'Bears': 'CHI', 'Saints': 'NO', 'Lions': 'DET', 'Buccaneers': 'TB', 'Jaguars': 'JAX', 'Giants': 'NYG', 'Eagles': 'PHI', 'Steelers': 'PIT', 'Ravens': 'BAL', 'Panthers': 'CAR',
        'Chargers': 'LAC', 'Jets': 'NYJ', 'Raiders': 'LV', 'Broncos': 'DEN', 'Bills': 'BUF', '49ers': 'SF', 'Vikings': 'MIN', 'Chiefs': 'KC', 'Cowboys': 'DAL', 'Heat': 'MIA', 'Thunder': 'OKC',
        'Oilers': 'EDM', 'Blues': 'STL', 'Mavericks': 'DAL', 'Jazz': 'UTAH'}
GAME = {'MIA@BUF': 'MIA BUF', 'NO@CHI': 'NO CHI', 'TEN@DAL': 'TEN DAL', 'TB@DET': 'TB DET', 'ARI@KC': 'ARI KC', 'PIT@PHI': 'PIT PHI', 'BAL@CAR': 'BAL CAR', 'NYJ@LAC': 'NYJ LAC',
        'LV@DEN': 'LV DEN', 'JAX@NYG': 'JAX NYG', 'MIN v SF': 'MIN SF', 'IND@NY': 'IND NY', 'ORL@WSH': 'ORL WSH', 'OKC@MIA': 'OKC MIA', 'DAL@UTAH': 'DAL UTAH', 'EDM@STL': 'EDM STL'}
def game(g): return SC.get(frozenset(GAME[g].split()))
f = lambda x: float(str(x).split('-')[0]) if x not in (None, '', '-') else 0.0
STAT = [('rushing + receiving', ['rushingYards', 'receivingYards']), ('receiving yards', ['receivingYards']), ('receptions', ['receptions']), ('rushing yards', ['rushingYards']),
        ('rushing attempts', ['rushingAttempts']), ('passing yards', ['passingYards']), ('interceptions', ['interceptions']), ('longest reception', ['longReception']), ('longest rush', ['longRushing']),
        ('touchdown', ['rushingTouchdowns', 'receivingTouchdowns']), ('threes', ['threePointFieldGoalsMade-threePointFieldGoalsAttempted']), ('rebounds', ['totalRebounds']), ('tackles', ['totalTackles'])]
out = []; miss = []
for i, l in enumerate(LEGS, 1):
    p = l['p']; t = p.lower(); r = act = None
    if l['sp'] == 'TENNIS':
        miss.append((i, p)); continue
    g = game(l['g'])
    if l['mkt'] in ('ml', 'spread', 'total', '1h spread', 'team total'):
        if not g or not g['final']: miss.append((i, p)); continue
        sc = g['h1'] if 'first half' in t else g['sc']
        if 'total points' in t and 'team' not in t:
            m = re.search(r'(over|under) (\d+(?:\.5)?)', t); v = sum(sc.values()); x = float(m.group(2))
            r = 'push' if v == x else ('W' if (v > x) == (m.group(1) == 'over') else 'L'); act = v
        elif 'team total' in t:
            tm = NICK[p.split(' ')[0]]; v = sc[tm]; x = float(re.search(r'over (\d+\.5)', t).group(1)); r = 'W' if v > x else 'L'; act = v
        else:
            tm = NICK[p.split(' ')[0]]; opp = [k for k in sc if k != tm][0]; mar = sc[tm] - sc[opp]
            if ' ML' in p: r = 'W' if mar > 0 else 'L'
            else:
                x = float(re.search(r'([+-]\d+(?:\.5)?)', p).group(1)); r = 'push' if mar + x == 0 else ('W' if mar + x > 0 else 'L')
            act = mar
        out.append(dict(i=i, r=r, act=act)); continue
    key = f'{D}|v7|{i}'; pl = PL.get(key)
    if not pl or not pl['espn_id']: miss.append((i, p)); continue
    rows = [x for x in GL.get(f"{pl['sport']}:{pl['espn_id']}", []) if x['date_pt'] == D]
    if not rows:
        if g and g['final']: out.append(dict(i=i, r='void', act=None)); continue   # his team played, he did not
        miss.append((i, p)); continue
    if g and not g['final']: miss.append((i, p)); continue
    keys = next((v for k, v in STAT if k in t), None)
    if not keys: miss.append((i, p)); continue
    v = sum(f(rows[0].get(k)) for k in keys)
    if 'longest' in t or (' under ' in t and re.search(r'under (\d+\.5)', t)):
        x = float(re.search(r'(\d+\.5)', t).group(1)); r = 'W' if ((v > x) != (' under ' in t)) else 'L'
    elif ' under ' in t:
        x = float(re.search(r'under (\d+)', t).group(1)); r = 'push' if v == x else ('W' if v < x else 'L')
    else:
        n = 1 if 'anytime' in t else int(re.search(r'(\d+)\+', p).group(1)); r = 'W' if v >= n else 'L'
    out.append(dict(i=i, r=r, act=v))
# tennis (ATP Finals final, Nov 22): ESPN tennis scoreboard
for e in cu("https://site.api.espn.com/apis/site/v2/sports/tennis/atp/scoreboard?dates=20261122").get('events', []):
    for gr in e.get('groupings', []):
        for c in gr.get('competitions', []):
            names = {nrm(x['athlete']['displayName']): x for x in c.get('competitors', []) if x.get('athlete')}
            if 'carlosalcaraz' in names and 'alexanderzverev' in names and c['status']['type']['completed']:
                a = names['carlosalcaraz']; z = names['alexanderzverev']; sets = len(a.get('linescores', []))
                for i, l in enumerate(LEGS, 1):
                    if l['sp'] == 'TENNIS':
                        won = bool(a.get('winner')); hit = won if 'ML' in l['p'] else (won and sets == 2)
                        out.append(dict(i=i, r='W' if hit else 'L', act=f"{'won' if won else 'lost'} in {sets} sets"))
                        miss[:] = [m for m in miss if m[0] != i]
json.dump({'legs': sorted(out, key=lambda x: x['i'])}, open(f'daily/{D}/results.json', 'w'), indent=0)
from collections import Counter
print(len(out), 'graded', Counter(x['r'] for x in out)); print('not graded:', miss)
