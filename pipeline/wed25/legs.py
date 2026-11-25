"""Ace's Nov 25 capper lines, cleaned (spelling fixed, one line per leg, in his order), mapped to tonight's ESPN games.
Player teams come from today's ESPN rosters, never guessed. Usage: python3 wed25/legs.py -> wed25/legs.json"""
import json, re, subprocess, unicodedata
from concurrent.futures import ThreadPoolExecutor
RAW = """Blake Corum anytime touchdown
Christian Watson 80+ receiving yards
Christian Watson 70+ receiving yards
Christian Watson 60+ receiving yards
Christian Watson 50+ receiving yards
James Cook anytime touchdown
Sam LaPorta anytime touchdown
Amon-Ra St. Brown 100+ receiving yards
Amon-Ra St. Brown 90+ receiving yards
Amon-Ra St. Brown 80+ receiving yards
Amon-Ra St. Brown 70+ receiving yards
Amon-Ra St. Brown 60+ receiving yards
Amon-Ra St. Brown 50+ receiving yards
Josh Allen anytime touchdown
Jared Goff 300+ passing yards
Jared Goff 275+ passing yards
Jared Goff 250+ passing yards
Jared Goff 225+ passing yards
Jared Goff 200+ passing yards
Jordan Love 200+ passing yards
Jordan Love 225+ passing yards
Jordan Love 250+ passing yards
Christian Watson 4+ receptions
Blake Corum 2+ receptions
Tutu Atwell 20+ receiving yards
Matthew Golden 50+ receiving yards
Blake Corum 40+ rushing yards
VJ Edgecombe 6+ rebounds
VJ Edgecombe 4+ rebounds
VJ Edgecombe 4+ assists
VJ Edgecombe 2+ assists
Mikel Brown Jr. 6+ assists
Mikel Brown Jr. 4+ assists
Mikel Brown Jr. 2+ assists
Mikel Brown Jr. 4+ rebounds
Mikel Brown Jr. 2+ rebounds
Matthew Stafford 200+ passing yards
Blake Corum 50+ rushing yards
Matthew Golden 5+ receptions
Konata Mumpfield 3+ receptions
Christian Watson anytime touchdown
Matthew Golden anytime touchdown
Amon-Ra St. Brown anytime touchdown
CeeDee Lamb anytime touchdown
Packers ML at Rams
Packers at Rams over 35.5 total points
Jonathan Kuminga 1+ threes
Jonathan Kuminga 2+ threes
Tyrese Maxey 3+ threes (over 2.5)
Buddy Hield 14+ points (over 13.5)
Jaden McDaniels 2+ threes (over 1.5)
Mikel Brown Jr. 20+ points + assists (over 19.5)
Landry Shamet 3+ threes (over 2.5)
Collin Gillespie 9+ points (over 8.5)
Tyrese Maxey 2+ threes
Tyrese Maxey 1+ threes
Buddy Hield 10+ points
Jaden McDaniels 1+ threes
Landry Shamet 2+ threes
Landry Shamet 1+ threes
Collin Gillespie 5+ points
Collin Gillespie 10+ points
Ajay Mitchell under 25 points
Ajay Mitchell under 20 points
Ajay Mitchell under 4 assists
Ajay Mitchell under 6 assists
Ajay Mitchell under 8 assists
Amen Thompson 10+ points
Amen Thompson 15+ points
Amen Thompson 6+ rebounds
Amen Thompson 4+ rebounds
VJ Edgecombe 10+ points
Jaden McDaniels 2+ assists
Jaden McDaniels 4+ assists
Jaden McDaniels 6+ rebounds
Jaden McDaniels 4+ rebounds
Jaden McDaniels 2+ rebounds
MarShawn Lloyd 10+ receiving yards
Rams ML v Packers
Matthew Golden 70+ receiving yards
Matthew Golden 100+ receiving yards
Blake Corum 60+ rushing yards
Matthew Stafford 225+ passing yards
Konata Mumpfield 40+ receiving yards
Konata Mumpfield 30+ receiving yards
LaMelo Ball 15+ points
Josh Giddey 8+ assists
LaMelo Ball 10+ points
Josh Giddey 6+ assists
Cedric Coward 6+ rebounds
Cedric Coward 4+ rebounds
Brandon Miller 15+ points
Brandon Miller 10+ points
Chase Brown under 15 rushing attempts
Packers +3 at Rams
Packers +10 at Rams
Penn State +5.5 v Memphis
Penn State +10.5 v Memphis
Kyren Williams 13+ rushing attempts (over 12.5)
Jordan Love under 267.5 passing yards
Matthew Stafford under 1.5 passing touchdowns
Kyren Williams 11+ rushing attempts
Jordan Love under 275 passing yards
Matthew Stafford under 2.5 passing touchdowns
Jordan Love under 300 passing yards
Jordan Love under 350 passing yards
Ty Jerome 3+ threes (over 2.5)
Josh Giddey 9+ assists (over 8.5)
Tyler Herro under 5.5 assists
Marcus Smart 5+ points
Marcus Smart 2+ rebounds
Tyler Herro under 8 assists
Tyler Herro under 10 assists
Ty Jerome 1+ threes
Ty Jerome 2+ threes
Josh Hart under 6 assists
Domantas Sabonis 12+ rebounds
Domantas Sabonis 10+ rebounds
Michael Porter Jr. 15+ points
Michael Porter Jr. 20+ points
Josh Hart under 8 assists
Isaiah Stewart 4+ rebounds
Isaiah Stewart 2+ rebounds
Fred VanVleet under 6 assists
Fred VanVleet under 8 assists"""
# Ace's dupes dropped: "Keyonte George 6+ assists" (listed twice), "Jakob Poeltl 8+ rebounds" (same as 7.5 over), "Ty Jerome over 22.5" kept as 23+,
# "Cam Spencer 6+ assists" (same as over 5.5), "Tyler Herro 4+ assists" (same as over 3.5), "Jayden Daniels under 1 interceptions" (same as under 0.5).
cu = lambda u: json.loads(subprocess.run(['curl', '-s', '-m', '30', u], capture_output=True, text=True).stdout)
nrm = lambda s: re.sub(r'[^a-z]', '', re.sub(r'\b(jr|sr|ii|iii|iv)\b', '', unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode().lower()))
GAMES = {}
for sp in ('basketball/nba', 'football/nfl'):
  for dd in (('20261125', '20261126') if 'nfl' in sp else ('20261125',)):
    for e in cu(f'https://site.api.espn.com/apis/site/v2/sports/{sp}/scoreboard?dates={dd}')['events']:
        c = e['competitions'][0]; ab = {x['homeAway']: x['team']['abbreviation'] for x in c['competitors']}
        g = f"{ab['away']}@{ab['home']}"
        for x in c['competitors']: GAMES.setdefault(x['team']['abbreviation'] + ('' if 'nba' in sp else '_nfl'), (g, e['date'], 'NBA' if 'nba' in sp else 'NFL', x['team']['id'], sp))
ros = {}
def roster(item):
    ab, (g, d, lg, tid, sp) = item
    r = cu(f'https://site.api.espn.com/apis/site/v2/sports/{sp}/teams/{tid}/roster')
    ath = r.get('athletes', [])
    if ath and isinstance(ath[0], dict) and 'items' in ath[0]: ath = [a for grp in ath for a in grp['items']]
    return [(nrm(a['displayName']), a['displayName'], ab.replace('_nfl', '')) for a in ath]
with ThreadPoolExecutor(12) as ex:
    for rs in ex.map(roster, GAMES.items()):
        for k, n, ab in rs: ros.setdefault(k, []).append((n, ab))
TEAM = {'Packers': 'GB', 'Rams': 'LAR'}
from datetime import datetime, timezone, timedelta
PT = timezone(timedelta(hours=-8))
CBB = {'Penn State': ('MEM@PSU', '2:00', 'CBB')}
legs = []; miss = []
for p in RAW.split('\n'):
    t = p.lower(); l = dict(p=p)
    first = p.split(' ')[0]
    if any(p.startswith(k) for k in CBB):
        k = next(k for k in CBB if p.startswith(k)); l.update(g=CBB[k][0], t=CBB[k][1], sp='CBB', mkt='spread' if re.search(r' [+-]\d', p) else 'ml'); legs.append(l); continue
    if first in TEAM:
        ab = TEAM[first]; g, d, lg, _, _ = GAMES[ab + '_nfl']
        mkt = 'total' if 'total points' in t else ('spread' if re.search(r' [+-]\d', p) else 'ml')
    else:
        name = re.split(r' (?:\d|under|anytime)', p)[0]; hit = ros.get(nrm(name), [])
        if len(hit) != 1: miss.append((p, hit)); legs.append(dict(l, g=None, t=None, sp=None, mkt='prop', player=name)); continue
        disp, ab = hit[0]; g, d, lg, _, _ = GAMES.get(ab + '_nfl') if (ab + '_nfl') in GAMES and ab not in GAMES else GAMES[ab]; l['player'] = disp; l['team'] = ab
        mkt = next((v for k, v in [('points + rebounds + assists', 'pra'), ('passing touchdowns', 'pass td'), ('touchdown', 'td'), ('rushing attempts', 'rushatt'), ('points + assists', 'pa'), ('receiving yards', 'recyds'), ('receptions', 'rec'),
                                   ('rushing yards', 'rush'), ('passing yards', 'pass'), ('interceptions', 'int'), ('threes', '3pm'), ('rebounds', 'reb'), ('assists', 'ast'), ('points', 'pts')] if k in t), 'prop')
    l.update(g=g, t=datetime.fromisoformat(d.replace('Z', '+00:00')).astimezone(PT).strftime('%a %-I:%M' if datetime.fromisoformat(d.replace('Z', '+00:00')).astimezone(PT).day != 25 else '%-I:%M'), sp=lg, mkt=mkt, start=d)
    legs.append(l)
json.dump(legs, open('wed25/legs.json', 'w'), indent=1)
print(len(legs), 'legs'); print('NOT FOUND:', miss)
for i, l in enumerate(legs, 1): print(i, l['p'], '|', l.get('team'), l['g'], l['t'], l['mkt'])
