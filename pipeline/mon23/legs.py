"""Ace's Nov 23 capper lines, cleaned (spelling fixed, one line per leg, in his order), mapped to tonight's ESPN games.
Player teams come from today's ESPN rosters, never guessed. Usage: python3 mon23/legs.py -> mon23/legs.json"""
import json, re, subprocess, unicodedata
from concurrent.futures import ThreadPoolExecutor
RAW = """Tee Higgins 50+ receiving yards
Mike Gesicki 25+ receiving yards
Jayden Daniels 25+ rushing yards
Stefon Diggs 50+ receiving yards
Joe Burrow 2+ passing touchdowns (over 1.5)
Joe Burrow 3+ passing touchdowns (over 2.5)
Lakers ML v Jazz
Luka Doncic 30+ points
Santa Clara ML v Illinois State
LaMelo Ball 20+ points
LaMelo Ball 15+ points
Donovan Mitchell 4+ assists
Walker Kessler 10+ rebounds
Keyonte George 6+ assists
Keyonte George 4+ assists
Ivica Zubac 8+ rebounds
Ivica Zubac 6+ rebounds
Mike Gesicki anytime touchdown
Antonio Williams anytime touchdown
Ja'Marr Chase anytime touchdown
Joe Burrow 275+ passing yards
Ja'Marr Chase 90+ receiving yards
Stefon Diggs 4+ receptions
Chase Brown 3+ receptions
Jayden Daniels 3+ rushing yards
Ja'Marr Chase 2+ touchdowns
Ja'Marr Chase 9+ receptions
Ja'Marr Chase 150+ receiving yards
Jeremiah Fears 25+ points + rebounds + assists
VJ Edgecombe 10+ points
Amen Thompson 20+ points + rebounds + assists
Amen Thompson 4+ rebounds
Amen Thompson 6+ rebounds
Amen Thompson 10+ points
Amen Thompson 15+ points
Isaiah Hartenstein 4+ assists
Isaiah Hartenstein 2+ assists
Quentin Grimes 2+ rebounds
Quentin Grimes 2+ assists
Quentin Grimes 4+ rebounds
Quentin Grimes 4+ assists
Devin Booker 6+ assists
Devin Booker 4+ assists
Andrew Nembhard 1+ threes
Andrew Nembhard 2+ threes
Immanuel Quickley 6+ assists
Immanuel Quickley 4+ assists
Mikel Brown Jr. 10+ points
Bengals ML at Commanders
Bengals -3 at Commanders
Joe Burrow under 304.5 passing yards
Ben Sinnott 3+ receiving yards (over 2.5)
Jayden Daniels under 0.5 interceptions
Chase Brown under 4.5 receptions
Joe Burrow under 325 passing yards
Chase Brown under 6 receptions
Chase Brown under 4 receptions
Ty Jerome 23+ points (over 22.5)
Jakob Poeltl 8+ rebounds (over 7.5)
Tyler Herro 4+ assists (over 3.5)
Jaylen Brown under 20.5 points
Cam Spencer 6+ assists (over 5.5)
Ty Jerome 20+ points
Ty Jerome 15+ points
Jakob Poeltl 6+ rebounds
Tyler Herro 2+ assists
Jaylen Brown under 25 points
Jaylen Brown under 20 points
Cam Spencer 4+ assists
Providence ML v VCU
Commanders +14 v Bengals
Bengals v Commanders over 45 total points
Josh Giddey 8+ assists
Josh Giddey 10+ assists
Moussa Diabate under 10 points
Coby White under 6 assists
Coby White under 4 assists
Brayden Burries 10+ points"""
# Ace's dupes dropped: "Keyonte George 6+ assists" (listed twice), "Jakob Poeltl 8+ rebounds" (same as 7.5 over), "Ty Jerome over 22.5" kept as 23+,
# "Cam Spencer 6+ assists" (same as over 5.5), "Tyler Herro 4+ assists" (same as over 3.5), "Jayden Daniels under 1 interceptions" (same as under 0.5).
cu = lambda u: json.loads(subprocess.run(['curl', '-s', '-m', '30', u], capture_output=True, text=True).stdout)
nrm = lambda s: re.sub(r'[^a-z]', '', re.sub(r'\b(jr|sr|ii|iii|iv)\b', '', unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode().lower()))
GAMES = {}
for sp in ('basketball/nba', 'football/nfl'):
    for e in cu(f'https://site.api.espn.com/apis/site/v2/sports/{sp}/scoreboard?dates=20261123')['events']:
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
TEAM = {'Lakers': 'LAL', 'Jazz': 'UTAH', 'Bengals': 'CIN', 'Commanders': 'WSH'}
from datetime import datetime, timezone, timedelta
PT = timezone(timedelta(hours=-8))
CBB = {'Santa Clara': ('ILST@SCU', '4:00', 'CBB'), 'Providence': ('VCU@PROV', '6:00', 'CBB')}
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
json.dump(legs, open('mon23/legs.json', 'w'), indent=1)
print(len(legs), 'legs'); print('NOT FOUND:', miss)
for i, l in enumerate(legs, 1): print(i, l['p'], '|', l.get('team'), l['g'], l['t'], l['mkt'])
