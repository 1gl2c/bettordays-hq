"""Ace's Nov 24 capper lines, cleaned (spelling fixed, one line per leg, in his order), mapped to tonight's ESPN games.
Player teams come from today's ESPN rosters, never guessed. Usage: python3 tue24/legs.py -> tue24/legs.json"""
import json, re, subprocess, unicodedata
from concurrent.futures import ThreadPoolExecutor
RAW = """Trae Young 16+ points (over 15.5)
Cooper Flagg 6+ assists (over 5.5)
Paul Reed 7+ rebounds (over 6.5)
Jayson Tatum 5+ assists (over 4.5)
Wendell Carter Jr. 6+ rebounds (over 5.5)
Trae Young 15+ points
Cooper Flagg 4+ assists
Paul Reed 6+ rebounds
Jayson Tatum 4+ assists
Franz Wagner 6+ rebounds
Franz Wagner 6+ assists
Penn ML v Drexel
Louisville ML v Texas Tech
Alabama ML v Baylor
St. John's ML v Oregon
Magic +3.5 v Pistons
Wizards +10.5 v Celtics
Mavericks +9.5 at Nuggets
Derrick White 5+ assists (over 4.5)
Magic +15 v Pistons
Wizards +20 v Celtics
Mavericks +19.5 at Nuggets
Derrick White 4+ assists
Derrick White 2+ assists
Neemias Queta 8+ rebounds
Neemias Queta 6+ rebounds
Cooper Flagg 20+ points
Cooper Flagg 15+ points
Cooper Flagg 10+ points
Franz Wagner 20+ points
Daniss Jenkins 4+ rebounds
Daniss Jenkins 2+ rebounds
Cade Cunningham 20+ points
Cade Cunningham 15+ points
Cade Cunningham 4+ rebounds
Cade Cunningham 25+ points
Nikola Jokic 6+ assists
Nikola Jokic 8+ assists
Nikola Jokic 10+ assists
Nikola Jokic 8+ rebounds
Nikola Jokic 10+ rebounds
Nikola Jokic 12+ rebounds
Cooper Flagg 35+ points + rebounds + assists
Cade Cunningham 35+ points + rebounds + assists
Franz Wagner 35+ points + rebounds + assists
Cooper Flagg 30+ points + rebounds + assists
Cade Cunningham 30+ points + rebounds + assists
Franz Wagner 30+ points + rebounds + assists
Nikola Jokic 45+ points + rebounds + assists
Nikola Jokic 40+ points + rebounds + assists
Jayson Tatum 35+ points + rebounds + assists
Jayson Tatum 30+ points + rebounds + assists
AJ Dybantsa 25+ points + rebounds + assists
AJ Dybantsa 20+ points + rebounds + assists
Ausar Thompson 6+ assists
Ausar Thompson 8+ rebounds
AJ Dybantsa 8+ rebounds
AJ Dybantsa 4+ assists
Derrick White 1+ threes
Derrick White 2+ threes
DeMar DeRozan under 4 assists
Payton Pritchard 4+ assists
Payton Pritchard 2+ assists"""
# Ace's duplicates dropped: Trae Young 15+ (kept, the 15.5 over is 16+), Cooper Flagg 6+ assists (same as over 5.5), Wendell Carter 6+ rebounds (same as over 5.5),
# Derrick White over 4.5 assists kept as 5+. Ace's 'Paul Reed o6.5' is 7+.
cu = lambda u: json.loads(subprocess.run(['curl', '-s', '-m', '30', u], capture_output=True, text=True).stdout)
nrm = lambda s: re.sub(r'[^a-z]', '', re.sub(r'\b(jr|sr|ii|iii|iv)\b', '', unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode().lower()))
GAMES = {}
for sp in ('basketball/nba',):
    for e in cu(f'https://site.api.espn.com/apis/site/v2/sports/{sp}/scoreboard?dates=20261124')['events']:
        c = e['competitions'][0]; ab = {x['homeAway']: x['team']['abbreviation'] for x in c['competitors']}
        g = f"{ab['away']}@{ab['home']}"
        for x in c['competitors']: GAMES[x['team']['abbreviation']] = (g, e['date'], 'NBA' if 'nba' in sp else 'NFL', x['team']['id'], sp)
ros = {}
def roster(item):
    ab, (g, d, lg, tid, sp) = item
    r = cu(f'https://site.api.espn.com/apis/site/v2/sports/{sp}/teams/{tid}/roster')
    ath = r.get('athletes', [])
    if ath and isinstance(ath[0], dict) and 'items' in ath[0]: ath = [a for grp in ath for a in grp['items']]
    return [(nrm(a['displayName']), a['displayName'], ab) for a in ath]
with ThreadPoolExecutor(12) as ex:
    for rs in ex.map(roster, GAMES.items()):
        for k, n, ab in rs: ros.setdefault(k, []).append((n, ab))
TEAM = {'Magic': 'ORL', 'Wizards': 'WSH', 'Mavericks': 'DAL'}
from datetime import datetime, timezone, timedelta
PT = timezone(timedelta(hours=-8))
CBB = {'Penn': ('DREX@PENN', '5:00', 'CBB'), 'Louisville': ('TTU@LOU', '5:00', 'CBB'), 'Alabama': ('BAY@ALA', '7:00', 'CBB'), "St. John's": ('ORE@SJU', '7:30', 'CBB')}
legs = []; miss = []
for p in RAW.split('\n'):
    t = p.lower(); l = dict(p=p)
    first = p.split(' ')[0]
    if any(p.startswith(k) for k in CBB):
        k = next(k for k in CBB if p.startswith(k)); l.update(g=CBB[k][0], t=CBB[k][1], sp='CBB', mkt='ml'); legs.append(l); continue
    if first in TEAM:
        ab = TEAM[first]; g, d, lg, _, _ = GAMES[ab]
        mkt = 'total' if 'total points' in t else ('spread' if re.search(r' [+-]\d', p) else 'ml')
    else:
        name = re.split(r' (?:\d|under|anytime)', p)[0]; hit = ros.get(nrm(name), [])
        if len(hit) != 1: miss.append((p, hit)); legs.append(dict(l, g=None, t=None, sp=None, mkt='prop', player=name)); continue
        disp, ab = hit[0]; g, d, lg, _, _ = GAMES[ab]; l['player'] = disp; l['team'] = ab
        mkt = next((v for k, v in [('points + rebounds + assists', 'pra'), ('passing touchdowns', 'pass td'), ('touchdown', 'td'), ('receiving yards', 'recyds'), ('receptions', 'rec'),
                                   ('rushing yards', 'rush'), ('passing yards', 'pass'), ('interceptions', 'int'), ('threes', '3pm'), ('rebounds', 'reb'), ('assists', 'ast'), ('points', 'pts')] if k in t), 'prop')
    l.update(g=g, t=datetime.fromisoformat(d.replace('Z', '+00:00')).astimezone(PT).strftime('%-I:%M'), sp=lg, mkt=mkt, start=d)
    legs.append(l)
json.dump(legs, open('tue24/legs.json', 'w'), indent=1)
print(len(legs), 'legs'); print('NOT FOUND:', miss)
for i, l in enumerate(legs, 1): print(i, l['p'], '|', l.get('team'), l['g'], l['t'], l['mkt'])
