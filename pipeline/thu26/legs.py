"""Ace's Nov 26 (Thanksgiving) capper lines, cleaned (spelling fixed, one line per leg, in his order), mapped to tonight's ESPN games.
Player teams come from today's ESPN rosters, never guessed. Usage: python3 wed25/legs.py -> thu26/legs.json"""
import json, re, subprocess, unicodedata
from concurrent.futures import ThreadPoolExecutor
RAW = """James Cook anytime touchdown
Sam LaPorta anytime touchdown
Amon-Ra St. Brown 100+ receiving yards
Amon-Ra St. Brown 90+ receiving yards
Amon-Ra St. Brown 80+ receiving yards
Amon-Ra St. Brown 70+ receiving yards
Amon-Ra St. Brown 60+ receiving yards
Amon-Ra St. Brown 50+ receiving yards
Josh Allen anytime touchdown
Jared Goff 300+ passing yards
Jared Goff 280+ passing yards
Jared Goff 275+ passing yards
Jared Goff 250+ passing yards
Jared Goff 225+ passing yards
Jared Goff 200+ passing yards
Amon-Ra St. Brown anytime touchdown
CeeDee Lamb anytime touchdown
Josh Allen 40+ rushing yards
Joe Milton 30+ rushing yards
Caleb Williams 25+ rushing yards
Rashee Rice anytime touchdown
Luther Burden anytime touchdown
Javonte Williams anytime touchdown
Lions ML v Bears
Lions +1.5 v Bears
Cowboys ML v Eagles
Chiefs ML at Bills
Amon-Ra St. Brown under 8 receptions
Colston Loveland 50+ receiving yards
Rome Odunze 100+ receiving yards
Caleb Williams 15+ rushing yards
Jahmyr Gibbs 70+ rushing yards
Kyle Monangai anytime touchdown
Jahmyr Gibbs anytime touchdown
Javonte Williams 2+ touchdowns
George Pickens anytime touchdown
Saquon Barkley anytime touchdown
Emmett Johnson anytime touchdown
James Cook 80+ rushing yards
CeeDee Lamb 80+ receiving yards
Kenneth Walker 70+ rushing yards
Luther Burden 60+ receiving yards
Eagles at Cowboys under 50 total points
Bears ML at Lions
Chiefs +3 at Bills
Kyle Monangai 8+ rushing attempts
Caleb Williams 2+ passing touchdowns
Jared Goff 2+ passing touchdowns
Patrick Mahomes 2+ passing touchdowns
Josh Allen 2+ passing touchdowns
Dak Prescott 2+ passing touchdowns
Caleb Williams 225+ passing yards
Rome Odunze 25+ receiving yards
Rome Odunze 45+ receiving yards
Jameson Williams 20+ receiving yards
Javonte Williams 60+ rushing yards
Khalil Shakir 25+ receiving yards
Travis Kelce 30+ receiving yards
Josh Allen 1+ interceptions
D'Andre Swift anytime touchdown
Jameson Williams anytime touchdown
Travis Kelce anytime touchdown
DeVonta Smith anytime touchdown
Joe Milton 15+ rushing yards
Jashaun Corbin 10+ rushing yards
Dak Prescott 10+ rushing yards
Joe Milton under 35 rushing yards
Will Shipley under 2 receptions
Josh Downs under 4 receptions"""
# Ace's dupes dropped: "Keyonte George 6+ assists" (listed twice), "Jakob Poeltl 8+ rebounds" (same as 7.5 over), "Ty Jerome over 22.5" kept as 23+,
# "Cam Spencer 6+ assists" (same as over 5.5), "Tyler Herro 4+ assists" (same as over 3.5), "Jayden Daniels under 1 interceptions" (same as under 0.5).
cu = lambda u: json.loads(subprocess.run(['curl', '-s', '-m', '30', u], capture_output=True, text=True).stdout)
nrm = lambda s: re.sub(r'[^a-z]', '', re.sub(r'\b(jr|sr|ii|iii|iv)\b', '', unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode().lower()))
GAMES = {}
for sp in ('basketball/nba', 'football/nfl'):
  for dd in (('20261126',) if 'nfl' in sp else ()):
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
TEAM = {'Lions': 'DET', 'Bears': 'CHI', 'Cowboys': 'DAL', 'Eagles': 'PHI', 'Chiefs': 'KC', 'Bills': 'BUF'}
from datetime import datetime, timezone, timedelta
PT = timezone(timedelta(hours=-8))
CBB = {}
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
        mkt = next((v for k, v in [('points + rebounds + assists', 'pra'), ('passing touchdowns', 'pass td'), ('touchdowns', 'td'), ('touchdown', 'td'), ('rushing attempts', 'rushatt'), ('points + assists', 'pa'), ('receiving yards', 'recyds'), ('receptions', 'rec'),
                                   ('rushing yards', 'rush'), ('passing yards', 'pass'), ('interceptions', 'int'), ('threes', '3pm'), ('rebounds', 'reb'), ('assists', 'ast'), ('points', 'pts')] if k in t), 'prop')
    l.update(g=g, t=datetime.fromisoformat(d.replace('Z', '+00:00')).astimezone(PT).strftime('%-I:%M'), sp=lg, mkt=mkt, start=d)
    legs.append(l)
json.dump(legs, open('thu26/legs.json', 'w'), indent=1)
print(len(legs), 'legs'); print('NOT FOUND:', miss)
for i, l in enumerate(legs, 1): print(i, l['p'], '|', l.get('team'), l['g'], l['t'], l['mkt'])
