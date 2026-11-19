"""Outcome backfill for every Beta Test Mode line of one night.

Usage (from pipeline/):  python3 review_packet/beta_backfill.py 20261118 beta/all_lines.json beta/beta_backfill_nov18.json

- Reads the saved pregame predictions (all_lines.json). It never edits that file.
- Outcome source 1: ESPN game summaries (box scores, including did-not-play entries).
- Outcome source 2: Kalshi's own settlement of the exact market ticker.
- Classification:
    W / L     box score stat is known and Kalshi settled the same way
    V         player listed as did not play, or not in the box score of a completed game
              (BettorDays voids legs whose player did not play)
    P         not possible here: every line is N+ on a whole number
    UNVERIFIABLE  the two sources disagree, the game is not final, or a source is missing
- Writes one record per line with the stat, both sources and the reason.
"""
import json, subprocess, sys, unicodedata
from concurrent.futures import ThreadPoolExecutor

DATE, SRC, OUT = sys.argv[1], sys.argv[2], sys.argv[3]

def cu(u):
    r = subprocess.run(['curl', '-s', '-m', '40', u], capture_output=True, text=True).stdout
    try: return json.loads(r)
    except Exception: return {}

def nrm(s): return unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode().lower().replace('.', '').replace("'", '').strip()

A = json.load(open(SRC))
sb = cu(f'https://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard?dates={DATE}')
events = [(e['id'], e['shortName'], e['status']['type']['completed']) for e in sb.get('events', [])]

def box(ev):
    i, name, done = ev
    d = cu(f'https://site.api.espn.com/apis/site/v2/sports/basketball/nba/summary?event={i}')
    players = {}
    for t in d.get('boxscore', {}).get('players', []):
        ab = t['team']['abbreviation']
        for s in t.get('statistics', []):
            keys = s.get('keys', [])
            for a in s.get('athletes', []):
                nm = nrm(a['athlete']['displayName'])
                rec = {'team': ab, 'dnp': bool(a.get('didNotPlay')), 'reason': a.get('reason')}
                if a.get('stats'): rec.update(dict(zip(keys, a['stats'])))
                players[nm] = rec
    return name, {'id': i, 'completed': done, 'players': players}

with ThreadPoolExecutor(8) as ex: BOX = dict(ex.map(box, events))
TEAMS = {}
for g, b in BOX.items():
    for t in g.replace(' @ ', '@').split('@'): TEAMS[t.strip()] = g

def stat(rec, st):
    def n(k):
        v = rec.get(k)
        if v in (None, '', '--'): return None
        return float(str(v).split('-')[0])
    if st == 'pts': return n('points')
    if st == 'reb': return n('rebounds')
    if st == 'ast': return n('assists')
    if st == '3pm': return n('threePointFieldGoalsMade-threePointFieldGoalsAttempted')
    if st == 'pra':
        p, r, a = n('points'), n('rebounds'), n('assists')
        return None if None in (p, r, a) else p + r + a

def kal(t):
    m = cu(f'https://api.elections.kalshi.com/trade-api/v2/markets/{t}').get('market', {})
    return t, {'status': m.get('status'), 'result': m.get('result'), 'settlement_ts': m.get('settlement_ts') or m.get('close_time')}
with ThreadPoolExecutor(10) as ex: KAL = dict(ex.map(kal, [a['ticker'] for a in A]))

out = []
for a in A:
    team = a['team']
    g = TEAMS.get(team) or TEAMS.get({'UTAH': 'UTAH', 'GS': 'GS', 'NO': 'NO', 'SA': 'SA', 'NY': 'NY'}.get(team, team))
    b = BOX.get(g) if g else None
    k = KAL.get(a['ticker'], {})
    kres = k.get('result') if k.get('status') in ('settled', 'finalized', 'determined') else None
    rec = b['players'].get(a['nm']) if b else None
    val = None; cls = 'UNVERIFIABLE'; why = ''
    if not b: why = 'game box score not found'
    elif not b['completed']: why = 'game not final in ESPN'
    elif rec is None: cls, why = 'V', 'player not in the box score of the completed game (did not play)'
    elif rec['dnp']: cls, why = 'V', f"did not play ({rec.get('reason') or 'no reason given'})"
    else:
        val = stat(rec, a['st'])
        if val is None: why = 'stat missing in box score'
        else:
            box_res = 'W' if val >= a['k'] else 'L'
            if kres in ('yes', 'no'):
                if (kres == 'yes') == (box_res == 'W'): cls, why = box_res, 'ESPN box score and Kalshi settlement agree'
                else: cls, why = 'UNVERIFIABLE', f'sources disagree: box score {val:g} vs Kalshi settled {kres}'
            else: cls, why = box_res, f'ESPN box score only (Kalshi status {k.get("status")}, result {k.get("result")!r})'
    if cls == 'V' and kres: why += f'; Kalshi settled {kres}'
    out.append({'ticker': a['ticker'], 'player': a['player'], 'team': team, 'game': a['g'], 'stat': a['st'], 'line': a['k'],
                'actual': val, 'outcome': cls, 'reason': why, 'espn_game': g, 'espn_event_id': b['id'] if b else None,
                'kalshi_status': k.get('status'), 'kalshi_result': k.get('result'), 'kalshi_settlement_ts': k.get('settlement_ts'),
                'outcome_source': 'ESPN NBA game summary box score + Kalshi market settlement',
                'outcome_backfilled': True})
json.dump(out, open(OUT, 'w'), indent=0)
from collections import Counter
print(Counter(o['outcome'] for o in out))
print(Counter(o['reason'].split(';')[0] for o in out).most_common())
