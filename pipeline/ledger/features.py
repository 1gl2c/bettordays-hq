"""Pick-time context for every leg (Phase 1). Strict no-leak rule: a game log row counts only if it started before the
leg's own game (ESPN start time, so a game later the same night never leaks in). Opponent and home or away come from the
schedule row of the leg's own game (known before tip). Injuries only from snapshots saved BEFORE that game started.
Usage: python3 ledger/features.py -> ledger/features.json"""
import json, re, csv, statistics as S, sys, os
from datetime import datetime, date
sys.path.insert(0, '.')
L = json.load(open('ledger/legs.json')); P = json.load(open('ledger/players.json')); G = json.load(open('ledger/gamelogs.json'))
ts = lambda s: datetime.fromisoformat(s.replace('Z', '+00:00'))
def f(x):
    if x in (None, '', '-'): return None
    try: return float(str(x).split('-')[0])
    except Exception: return None
NBA = {'pts': ['points'], 'reb': ['totalRebounds'], 'ast': ['assists'], '3pm': ['threePointFieldGoalsMade-threePointFieldGoalsAttempted'], 'blk': ['blocks'], 'stl': ['steals'],
       'pra': ['points', 'totalRebounds', 'assists'], 'pr': ['points', 'totalRebounds'], 'pa': ['points', 'assists'], 'ra': ['totalRebounds', 'assists']}
NFL = {'recyds': ['receivingYards'], 'rec': ['receptions'], 'rush': ['rushingYards'], 'rushatt': ['rushingAttempts'], 'att': ['rushingAttempts'], 'pass': ['passingYards'],
       'rr': ['rushingYards', 'receivingYards'], 'td': ['rushingTouchdowns', 'receivingTouchdowns'], 'atd': ['rushingTouchdowns', 'receivingTouchdowns'], 'int': ['interceptions'], 'passtd': ['passingTouchdowns']}
WORDS = [('points + rebounds + assists', 'pra'), ('pra', 'pra'), ('rebounds', 'reb'), ('rebs', 'reb'), ('reb', 'reb'), ('assists', 'ast'), ('ast', 'ast'), ('threes', '3pm'), ('3pm', '3pm'), ('3pt', '3pm'), ('blocks', 'blk'),
         ('points', 'pts'), ('pts', 'pts'), ('rushing + receiving', 'rr'), ('receiving yards', 'recyds'), ('rec yds', 'recyds'), ('receptions', 'rec'), ('rushing yards', 'rush'), ('rush yds', 'rush'), ('rushing attempts', 'rushatt'),
         ('passing yards', 'pass'), ('pass yds', 'pass'), ('interceptions', 'int'), ('touchdown', 'atd'), (' td', 'atd')]
def stat_key(l):
    st = (l.get('stat') or '').lower(); tl = ' ' + l['pick'].lower()
    if st in ('3pm',) or st in NBA or st in NFL: return {'reg': None}.get(st, st)
    return next((v for k, v in WORDS if k in tl), None)
def val(row, keys):
    v = [f(row.get(k)) for k in keys]
    return None if any(x is None for x in v) else sum(v)
# injury snapshots taken before games (file, time saved, game date)
SNAP = {'2026-11-16': 'mon/nba_inj.json', '2026-11-17': 'tue/nba_inj.json', '2026-11-18': 'wed/nba_inj.json', '2026-11-19': 'beta19/nba_inj.json',
        '2026-11-20': 'betafri20/nba_inj.json', '2026-11-21': 'betasat21/nba_inj.json', '2026-11-22': 'betasun22/nba_inj.json'}
import subprocess
_T = json.loads(subprocess.run(['curl', '-s', '-m', '30', 'https://site.api.espn.com/apis/site/v2/sports/basketball/nba/teams'], capture_output=True, text=True).stdout)
TEAMNAME = {t['team']['abbreviation']: t['team']['displayName'] for t in _T['sports'][0]['leagues'][0]['teams']}
INJ = {}
for d, fn in SNAP.items():
    j = json.load(open(fn)); t = j.get('timestamp')
    rows = {}
    for tm in j.get('injuries', []):
        for i in tm.get('injuries', []):
            rows[i['athlete']['displayName']] = dict(team=tm.get('displayName'), status=i.get('status'), note=(i.get('shortComment') or '')[:200], updated=i.get('date'))
    INJ[d] = (t, rows)
# books (no-vig sportsbook chance) where we pulled them: Nov 21 and Nov 22, from the merged files (already pick time)
# Nov 19 AI panel grades (they looked up market prices themselves, so these are not blind)
PANEL = {r['pick']: r for r in csv.DictReader(open('daily/2026-11-19/ai_reviews/merged_grades_2026-11-19.csv'))}
out = {}
for l in L:
    o = {}
    pl = P.get(l['key']); sk = stat_key(l)
    if pl and pl['espn_id']:
        g = G.get(f"{pl['sport']}:{pl['espn_id']}", [])
        own = [r for r in g if r['date_pt'] == l['date']]
        start = ts(own[0]['start']) if own else None
        cut = start or ts(l['date'] + 'T00:00:00-08:00')
        prev = [r for r in g if ts(r['start']) < cut]
        o.update(player=pl['name'], espn_id=pl['espn_id'], resolve=pl['how'])
        if own: o.update(team=own[0]['team'], opponent=own[0]['opp'], home_away='away' if own[0]['at'] == '@' else 'home', game_start=own[0]['start'])
        elif prev and re.fullmatch(r'[A-Z]{2,4}@[A-Z]{2,4}', l.get('event') or ''):   # game not in the log yet: schedule from the event, team from his last game
            aw, hm = l['event'].split('@'); tm = prev[-1]['team']; AL = {'NYK': 'NY', 'GSW': 'GS', 'SAS': 'SA', 'UTA': 'UTAH', 'WAS': 'WSH', 'NOP': 'NO'}
            tm = AL.get(tm, tm)
            if tm in (aw, hm): o.update(team=tm, opponent=hm if tm == aw else aw, home_away='away' if tm == aw else 'home', schedule_from='event text')
        if prev:
            last = ts(prev[-1]['start']).date(); gd = (start or cut).date() if start else date.fromisoformat(l['date'])
            o['rest_days'] = (date.fromisoformat(l['date']) - date.fromisoformat(prev[-1]['date_pt'])).days - 1
            o['b2b'] = o['rest_days'] == 0
            o['games_before'] = len(prev)
            if pl['sport'] == 'NBA':
                mins = [f(r.get('minutes')) for r in prev[-5:]]
                o['min_l5'] = [m for m in mins]; o['min_avg_l5'] = round(S.mean([m for m in mins if m is not None]), 1) if any(m is not None for m in mins) else None
                o['min_avg_season'] = round(S.mean([f(r.get('minutes')) for r in prev if f(r.get('minutes')) is not None]), 1) if prev else None
            keys = (NBA if pl['sport'] == 'NBA' else NFL).get(sk)
            if keys:
                vs = [val(r, keys) for r in prev]; vs = [v for v in vs if v is not None]
                if vs:
                    o['stat'] = sk; o['vals_l5'] = vs[-5:]; o['avg_l5'] = round(S.mean(vs[-5:]), 2); o['avg_season'] = round(S.mean(vs), 2); o['n'] = len(vs)
                    ln = l.get('line')
                    if ln is not None:
                        thr = ln if float(ln).is_integer() else ln + 0.5   # '6+' means 6 or more; 'over 5.5' means 6 or more
                        if sk == 'atd': thr = 1
                        hit = (lambda v: v >= thr) if l['dir'] == 'o' else (lambda v: v < thr if float(ln).is_integer() else v <= ln)
                        o['hit_season'] = f"{sum(hit(v) for v in vs)}/{len(vs)}"; o['hit_l5'] = f"{sum(hit(v) for v in vs[-5:])}/{len(vs[-5:])}"
        if l['date'] in INJ and pl['sport'] == 'NBA':
            t, rows = INJ[l['date']]
            if t and start and ts(t) < start:
                me = rows.get(pl['name'])
                tm_full = None
                o['injury_snapshot_at'] = t
                o['injury_self'] = me
                if own:
                    # teammates and opponents on the same pre-game snapshot (Out, doubtful, questionable or day-to-day)
                    tn = {TEAMNAME.get(own[0]['team']): 'team', TEAMNAME.get(own[0]['opp']): 'opp'}
                    for k, v in rows.items():
                        side = tn.get(v['team'])
                        if side and k != pl['name'] and v['status'] in ('Out', 'Doubtful', 'Questionable', 'Day-To-Day'):
                            o.setdefault('injuries_' + side, []).append(f"{k} ({v['status']})")
    if l['date'] == '2026-11-19' and l['pick'] in PANEL:
        r = PANEL[l['pick']]
        o['panel'] = {k: f(r[k]) for k in ('chatgpt', 'gemini', 'grok')}; o['panel_saw_market'] = True
    out[l['key']] = o
json.dump(out, open('ledger/features.json', 'w'))
from collections import Counter
c = Counter()
for k, o in out.items():
    for kk in ('player', 'opponent', 'avg_l5', 'hit_l5', 'min_avg_l5', 'rest_days', 'injury_snapshot_at', 'injuries_team', 'injuries_opp', 'panel'): c[kk] += kk in o
print(len(out), dict(c))
