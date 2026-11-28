"""Daily NBA beta sim, one command for any date (replaces the per-day copies like betawed25/sim.py; same method).
Usage (from pipeline/): python3 beta/run_day.py 2026-11-27
Steps, all automatic:
  1. Tonight's games and tip times from the ESPN scoreboard; games that already tipped are skipped.
  2. Back-to-backs from the ESPN scoreboard for the day before.
  3. OUT and questionable players from the ESPN injury feed.
  4. Fresh Kalshi player-prop markets (points, rebounds, assists, threes, PRA) for the date.
  5. Season game logs from ESPN for every player with a line priced 50 to 60 cents.
  6. 1,000 simulated games per matchup (shared game and team environment, each player's night drawn from his own
     season, last 5 weighted double, opponent rank and back-to-back nudges), exactly as the Nov 25 sim.
  7. Books check: the sportsbooks' no-vig chance at the same number from daily/DATE/book_lines.txt when present.
Writes beta<mon><dd>/ (logs.json, kalshi2.json, all_lines.json, beta_tonight.json)."""
import json, re, math, random, sys, os, datetime, subprocess, urllib.parse, unicodedata, statistics as S
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, '.')
import book_ev as B

DAY = sys.argv[1]; d = datetime.date.fromisoformat(DAY)
OUTD = f"beta{d.strftime('%b').lower()}{d.day:02d}"; os.makedirs(OUTD, exist_ok=True)
KTAG = f"{d.strftime('%y')}{d.strftime('%b').upper()}{d.day:02d}"   # 26NOV27
random.seed(int(d.strftime('%d')))
PT = datetime.timezone(datetime.timedelta(hours=-8)); NOW = datetime.datetime.now(PT)
cu = lambda u: (lambda r: json.loads(r) if r.strip() else {})(subprocess.run(['curl', '-s', '-m', '30', u], capture_output=True, text=True).stdout)
nrm = lambda s: unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode().lower().replace('.', '').replace("'", '').strip()

# 1-2. games, tips, back-to-backs
sb = cu(f"https://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard?dates={DAY.replace('-', '')}")
G, skipped = {}, []
for e in sb.get('events', []):
    tip = datetime.datetime.fromisoformat(e['date'].replace('Z', '+00:00')).astimezone(PT)
    a, h = e['shortName'].split(' @ '); g = f'{a}@{h}'
    if tip <= NOW: skipped.append(g); continue
    for tm in (a, h): G[tm] = (g, tip.strftime('%-I:%M'))
y = (d - datetime.timedelta(days=1)).strftime('%Y%m%d')
B2B = {c['team']['abbreviation'] for e in cu(f'https://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard?dates={y}').get('events', [])
       for c in e['competitions'][0]['competitors']}
# 3. injuries
OUT, Q = set(), set()
for t in cu('https://site.api.espn.com/apis/site/v2/sports/basketball/nba/injuries').get('injuries', []):
    for i in t.get('injuries', []):
        st = (i.get('status') or '').lower(); n = nrm(i['athlete']['displayName'])
        if st == 'out': OUT.add(n)
        elif st in ('questionable', 'doubtful', 'day-to-day'): Q.add(n)
# 4. Kalshi props
SER = {'KXNBAPTS': 'pts', 'KXNBAREB': 'reb', 'KXNBAAST': 'ast', 'KXNBA3PT': '3pm', 'KXNBAPRA': 'pra'}
def kget(s):
    out, cur = [], ''
    for _ in range(12):
        u = f"https://api.elections.kalshi.com/trade-api/v2/markets?series_ticker={s}&status=open&limit=1000" + (f"&cursor={urllib.parse.quote(cur)}" if cur else '')
        dd = cu(u); out += dd.get('markets', []); cur = dd.get('cursor')
        if not cur or not dd.get('markets'): break
    return s, [{k: m.get(k) for k in ('ticker', 'event_ticker', 'title', 'yes_bid_dollars', 'yes_ask_dollars')} for m in out if KTAG in m['event_ticker']]
with ThreadPoolExecutor(5) as ex: K = dict(ex.map(kget, SER))
TS = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds'); json.dump(K, open(f'{OUTD}/kalshi2.json', 'w'))
cand = []
for s, ms in K.items():
    for m in ms:
        a = float(m['yes_ask_dollars'] or 0); b = float(m['yes_bid_dollars'] or 0)
        if 0.50 <= a <= 0.60 and b > 0 and a - b <= 0.05:
            mm = re.match(r'(.+?): (\d+)\+', m['title'])
            if mm: cand.append((m, SER[s], mm.group(1), int(mm.group(2))))
# 5. game logs
def glog(name):
    dd = cu('https://site.web.api.espn.com/apis/common/v3/search?limit=10&type=player&query=' + urllib.parse.quote(name))
    its = [i for i in dd.get('items', []) if i.get('league') == 'nba']
    if not its: return name, None
    pid = its[0]['id']; g = cu(f'https://site.web.api.espn.com/apis/common/v3/sports/basketball/nba/athletes/{pid}/gamelog')
    names = g.get('names', []); ev = g.get('events', {}); games = []
    for st in g.get('seasonTypes', [])[:1]:
        for c in st.get('categories', []):
            for e in c.get('events', []):
                m = ev.get(e['eventId'], {}); row = {'date': m.get('gameDate', '')[:10]}
                for i, n in enumerate(names): row.setdefault(n, e['stats'][i])
                games.append(row)
    games = sorted({r['date']: r for r in games if r['date'] < DAY}.values(), key=lambda r: r['date'], reverse=True)
    team = cu(f'https://site.web.api.espn.com/apis/common/v3/sports/basketball/nba/athletes/{pid}').get('athlete', {}).get('team', {}).get('abbreviation')
    return name, {'disp': its[0]['displayName'], 'team': team, 'games': games}
with ThreadPoolExecutor(12) as ex: LOG = dict(ex.map(glog, sorted({c[2] for c in cand})))
json.dump(LOG, open(f'{OUTD}/logs.json', 'w'))
OPP = json.load(open('sat21/nba_opp.json'))   # opponent per-game allowed ranks (refresh when stale)

def f(x, k):
    v = x.get(k, 0)
    if isinstance(v, str):
        try: v = float(v.split('-')[0])
        except ValueError: v = 0
    return v or 0
def val(x, st):
    if st == 'pra': return f(x, 'points') + f(x, 'totalRebounds') + f(x, 'assists')
    return f(x, {'pts': 'points', 'reb': 'totalRebounds', 'ast': 'assists', '3pm': 'threePointFieldGoalsMade-threePointFieldGoalsAttempted'}[st])
lines = []
for m, st, name, k in cand:
    p = LOG.get(name)
    if not p or len(p['games']) < 8 or nrm(name) in OUT or p['team'] not in G: continue
    a = float(m['yes_ask_dollars']); b = float(m['yes_bid_dollars'])
    lines.append(dict(ticker=m['ticker'], ev=m['event_ticker'], player=name, nm=nrm(name), team=p['team'], st=st, k=k, ask=a, bid=b, mid=round(100 * (a + b) / 2, 1), games=p['games']))
# 6. simulate
N = 1000; byg = defaultdict(list)
for l in lines: byg[G[l['team']][0]].append(l)
def opprank(team, st):
    a, b = G[team][0].split('@'); o = b if team == a else a
    return (OPP.get(o) or {}).get('pts' if st == 'pra' else st, [0, 15])[1]
for g, ls in byg.items():
    hits = {id(l): 0 for l in ls}
    for _ in range(N):
        ge = random.gauss(1, 0.04); te = {t: ge * random.gauss(1, 0.07) for t in g.split('@')}
        for l in ls:
            gl = l['games']; x = random.choices(gl, weights=[2 if i < 5 else 1 for i in range(len(gl))])[0]; v = val(x, l['st'])
            e = te[l['team']]; rk = opprank(l['team'], l['st']); e *= 1.03 if rk >= 23 else 0.97 if rk <= 8 else 1.0
            if l['team'] in B2B and l['st'] in ('pts', 'pra', '3pm'): e *= 0.97
            if l['st'] in ('reb', 'ast'): e = e ** 0.7
            v = v * e + random.gauss(0, 0.6 if l['st'] in ('3pm', 'ast', 'reb') else 1.5)
            if v >= l['k'] - 0.5: hits[id(l)] += 1
    for l in ls:
        pp = hits[id(l)] / N; l['sim'] = round(100 * pp, 1); l['se'] = round(100 * math.sqrt(pp * (1 - pp) / N), 1)
# 7. books at the same number
BL = f'daily/{DAY}/book_lines.txt'; ROWS = []
if os.path.exists(BL):
    for r in open(BL).read().strip().split(';'):
        pl, mk, ln, nb, fo = r.split('|'); ROWS.append({'player': pl, 'market': 'player_' + mk, 'line': float(ln), 'books': int(nb), 'fair_over': float(fo)})
for l in lines:
    q = l['ask']; l['be'] = round(100 * (q + 0.07 * q * (1 - q)), 1)
    l['odds'] = '+100' if q == 0.5 else f"-{round(100 * q / (1 - q))}" if q > 0.5 else f"+{round(100 * (1 - q) / q)}"
    vs = [val(x, l['st']) for x in l['games']]; l['n'] = len(vs); l['hs'] = sum(v >= l['k'] for v in vs); l['h5'] = sum(v >= l['k'] for v in vs[:5]); l['avg'] = round(S.mean(vs), 1)
    pp = l['sim'] / 100; l['unc'] = round(100 * 1.96 * math.sqrt(max(pp * (1 - pp), 0.04) / l['n']), 1)
    l['edge'] = round(l['sim'] - l['be'], 1); l['mid0'] = l['mid']; l['move'] = 0.0
    l['g'], l['t'] = G[l['team']]; l['q'] = l['nm'] in Q
    r = B.fair_rung(ROWS, l['player'], l['st'], l['k']) if ROWS and l['st'] in B.MARKET else None
    l['bk'], l['bkn'] = (round(100 * r[0], 1), r[1]) if r else (None, None)
top, seen, pg = [], set(), defaultdict(int)
for l in sorted(lines, key=lambda l: -l['edge']):
    if l['nm'] in seen or pg[l['g']] >= 2 or l['q']: continue
    top.append(l); seen.add(l['nm']); pg[l['g']] += 1
    if len(top) == 15: break
strip = lambda l: {k: v for k, v in l.items() if k != 'games'}
json.dump([strip(l) for l in lines], open(f'{OUTD}/all_lines.json', 'w'))
json.dump({'sim_ts': TS, 'ts': TS, 'ts0': TS, 'n_lines': len(lines), 'n_games': len(byg), 'skipped': skipped, 'b2b': sorted(B2B & set(G)),
           'top': [strip(l) for l in top], 'all_pos': sum(l['edge'] > 0 for l in lines), 'avg': round(sum(l['edge'] for l in lines) / max(len(lines), 1), 1)},
          open(f'{OUTD}/beta_tonight.json', 'w'), indent=1)
print(f'{OUTD}: {len(lines)} lines in {len(byg)} games (skipped started: {skipped}; back-to-back: {sorted(B2B & set(G))})')
for l in top: print(f"{l['edge']:>5} sim {l['sim']} BE {l['be']} books {l['bk']} {l['player']} {l['k']}+ {l['st']} {l['g']} {l['t']}{' Q' if l['q'] else ''}")
