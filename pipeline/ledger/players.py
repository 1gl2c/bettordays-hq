"""Resolve each prop leg's player to an ESPN athlete id, then save that athlete's full season game log (ESPN), with the
game date in Pacific time, home or away, opponent and minutes. A name that matches more than one player stays unresolved
(no guessing). Usage: python3 ledger/players.py -> ledger/players.json, ledger/gamelogs.json"""
import json, re, subprocess, unicodedata, urllib.parse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone, timedelta
L = json.load(open('ledger/legs.json'))
def cu(u):
    for _ in range(3):
        try: return json.loads(subprocess.run(['curl', '-s', '-m', '30', u], capture_output=True, text=True).stdout)
        except Exception: pass
    return {}
nrm = lambda s: re.sub(r'[^a-z ]', '', unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode().lower().replace('-', ' ')).strip()
SP = {'NBA': ('basketball/nba', 'nba'), 'NFL': ('football/nfl', 'nfl'), 'CFB': ('football/college-football', 'college-football'), 'NCAAF': ('football/college-football', 'college-football')}
ALIAS = {'kd': 'kevin durant', 'luka': 'luka doncic', 'mpj': 'michael porter jr', 'bam': 'bam adebayo', 'lebron': 'lebron james', 'trae': 'trae young', 'giannis': 'giannis antetokounmpo',
         'wcj': 'wendell carter jr', 'podz': 'brandin podziemski', 'dame': 'damian lillard', 'franz': 'franz wagner', 'jalen brunsun': 'jalen brunson', 'micheal porter': 'michael porter jr',
         'og annuouby': 'og anunoby', 'stepon castle': 'stephon castle', 'alperen senguun': 'alperen sengun', 'yaxel lenderborg': 'yaxel lendeborg', 'ausar thomspon': 'ausar thompson', 'herb jones': 'herbert jones',
         'lamelo': 'lamelo ball', 'zion': 'zion williamson', 'cade': 'cade cunningham', 'jaquez': 'jaime jaquez jr', 'ayo': 'ayo dosunmu', 'jabari': 'jabari smith jr', 'ausar': 'ausar thompson', 'ziaire': 'ziaire williams',
         'jsn': 'jaxon smith njigba', 'came skattebo': 'cam skattebo', 'chig': 'chigoziem okonkwo', 'chigoziem': 'chigoziem okonkwo', 'geno': 'geno smith', 'shedeur': 'shedeur sanders', 'dj moore': 'dj moore',
         'jayden daniels any time touchdowns': 'jayden daniels', 'jj mccarthy any time touchdowns': 'jj mccarthy', 'cam skattebo any time touchdown': 'cam skattebo', 'devin singletary longest rush': 'devin singletary',
         'scheierman dd': 'baylor scheierman',
         'sga': 'shai gilgeous alexander', 'ad': 'anthony davis', 'jokic': 'nikola jokic', 'wemby': 'victor wembanyama', 'kat': 'karl anthony towns', 'cp3': 'chris paul', 'jjj': 'jaren jackson jr', 'pg': 'paul george'}
# NBA rosters: every current player, by full and last name
ros = {}
teams = cu('https://site.api.espn.com/apis/site/v2/sports/basketball/nba/teams')['sports'][0]['leagues'][0]['teams']
def roster(t):
    t = t['team']; d = cu(f"https://site.api.espn.com/apis/site/v2/sports/basketball/nba/teams/{t['id']}/roster")
    return [(a['id'], a['displayName'], t['abbreviation']) for a in d.get('athletes', [])]
with ThreadPoolExecutor(10) as ex:
    for rs in ex.map(roster, teams):
        for aid, nm, ab in rs: ros.setdefault(nrm(nm), []).append((aid, nm, ab)); ros.setdefault('LAST:' + nrm(nm).split()[-1], []).append((aid, nm, ab))
def player_name(l):
    if l.get('player'): return l['player']
    m = re.match(r"(.+?) (?:\d|under |over |anytime|to |ml\b)", l['pick'], re.I)
    return m.group(1) if m else None
def teams_of(ev): return set(re.findall(r'[A-Z]{2,4}', ev or ''))
def resolve(nm, sport, ev):
    n = nrm(nm); n = ALIAS.get(n, n)
    if sport == 'NBA':
        hit = ros.get(n) or (ros.get('LAST:' + n) if ' ' not in n else None)
        if hit:
            if len(hit) == 1: return hit[0][0], hit[0][1], 'roster'
            tt = teams_of(ev); h2 = [h for h in hit if h[2] in tt]
            if len(h2) == 1: return h2[0][0], h2[0][1], 'roster+event'
            return None, None, f'ambiguous ({len(hit)} players)'
    sp, lg = SP[sport]
    d = cu('https://site.web.api.espn.com/apis/common/v3/search?limit=10&type=player&query=' + urllib.parse.quote(n))
    its = [i for i in d.get('items', []) if i.get('league') == lg]
    ex = [i for i in its if nrm(i['displayName']) == n]
    if len(ex) == 1: return ex[0]['id'], ex[0]['displayName'], 'search exact'
    if len(its) == 1 and ' ' in n: return its[0]['id'], its[0]['displayName'], 'search single'
    cand = ex or [i for i in its if nrm(i['displayName']).split()[-1] == n.split()[-1]]
    tt = teams_of(ev)
    if cand and tt:   # several players share the name: keep the one whose team is in this game
        tm = lambda i: (cu(f"https://site.web.api.espn.com/apis/common/v3/sports/{sp}/athletes/{i['id']}").get('athlete', {}).get('team') or {}).get('abbreviation')
        h2 = [i for i in cand if tm(i) in tt]
        if len(h2) == 1: return h2[0]['id'], h2[0]['displayName'], 'search+event team'
    return None, None, f'unresolved ({len(its)} search hits)'
need = {}
for l in L:
    if l['sport'] not in SP or l.get('market') in ('ml', 'spread', 'total', 'team'): continue
    if re.search(r'\b(ML|total points|team total|spread|win by|\+\d+(?:\.5)? v|-\d+(?:\.5)? v)\b', l['pick']): continue
    nm = player_name(l)
    if nm and nrm(nm) == 'under': continue   # pick text starting with 'Under' has no player name
    if nm: need.setdefault((nm, l['sport'], l['event'] or ''), []).append(l['key'])
print('names to resolve', len(need))
with ThreadPoolExecutor(12) as ex: res = dict(zip(need, ex.map(lambda k: resolve(*k), need)))
P = {}
for k, keys in need.items():
    aid, disp, how = res[k]
    for key in keys: P[key] = dict(name_raw=k[0], espn_id=aid, name=disp, how=how, sport=k[1])
json.dump(P, open('ledger/players.json', 'w'), indent=0)
ids = {(v['espn_id'], v['sport']) for v in P.values() if v['espn_id']}
print('resolved legs', sum(1 for v in P.values() if v['espn_id']), 'of', len(P), '| athletes', len(ids))
PT = timezone(timedelta(hours=-8))
def glog(a):
    aid, sport = a; sp, _ = SP[sport]; out = []
    for season in ([2027] if sport == 'NBA' else [2026]):
        g = cu(f'https://site.web.api.espn.com/apis/common/v3/sports/{sp}/athletes/{aid}/gamelog?season={season}')
        names = g.get('names', []); ev = g.get('events', {})
        for st in g.get('seasonTypes', []):
            if 'Regular' not in st.get('displayName', '') and 'Postseason' not in st.get('displayName', ''): continue
            for c in st.get('categories', []):
                for e in c.get('events', []):
                    m = ev.get(e['eventId'], {}); gd = m.get('gameDate')
                    if not gd: continue
                    dpt = datetime.fromisoformat(gd.replace('Z', '+00:00')).astimezone(PT)
                    row = {'eid': e['eventId'], 'start': gd, 'date_pt': dpt.date().isoformat(), 'opp': (m.get('opponent') or {}).get('abbreviation'), 'team': (m.get('team') or {}).get('abbreviation'), 'at': m.get('atVs')}
                    row.update({n: e['stats'][i] for i, n in enumerate(names) if i < len(e['stats'])})
                    out.append(row)
    return f'{sport}:{aid}', sorted({r['eid']: r for r in out}.values(), key=lambda r: r['start'])
with ThreadPoolExecutor(12) as ex: G = dict(ex.map(glog, sorted(ids)))
json.dump(G, open('ledger/gamelogs.json', 'w'))
print('game logs', len(G), 'empty', sum(1 for v in G.values() if not v))
from collections import Counter
print(Counter(v['how'].split(' (')[0] for v in P.values()))
