"""Closing Kalshi price for a slate's legs (Phase 1). For each leg priced at pick time, find its exact Kalshi market, then
read the last quoted bid/ask mid at or before the game's start from Kalshi's candlesticks (1-minute bars over the final hour,
hourly bars as fallback). Unders and underdog spreads use 100 minus the YES side. Never estimated: no quote, no close.
Usage: python3 ledger/kclose.py 2026-11-22 -> ledger/close_<date>.json"""
import json, re, subprocess, sys, time, unicodedata
from datetime import datetime, timezone, timedelta
from concurrent.futures import ThreadPoolExecutor
D = sys.argv[1]; dd = datetime.fromisoformat(D); TAG = dd.strftime('%y%b%d').upper()   # 26NOV22
B = 'https://api.elections.kalshi.com/trade-api/v2'
def cu(u):
    for i in range(6):
        try:
            d = json.loads(subprocess.run(['curl', '-s', '-m', '30', u], capture_output=True, text=True).stdout)
            if 'too_many' in str(d.get('error', '')): time.sleep(1.5 + i); continue
            return d
        except Exception: time.sleep(1.5)
    return {}
nrm = lambda s: re.sub(r'[^a-z]', '', re.sub(r'\b(jr|sr|ii|iii|iv)\b', '', unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode().lower()))
import os
KMF = f'daily/{D}/kmatch.json' if os.path.exists(f'daily/{D}/kmatch.json') else ('sun22/kmatch.json' if D == '2026-11-22' else None)
KM = json.load(open(KMF)) if KMF else {}   # leg number -> Kalshi event ticker, saved by that day's kmatch step
LEGS = [l for l in json.load(open('ledger/legs.json')) if l['date'] == D]
FEAT = json.load(open('ledger/features.json'))
CITY = {'Bears': 'Chicago', 'Lions': 'Detroit', 'Jaguars': 'Jacksonville', 'Eagles': 'Philadelphia', 'Ravens': 'Baltimore', 'Buccaneers': 'Tampa Bay', 'Chargers': 'Los Angeles C',
        'Giants': 'New York G', 'Steelers': 'Pittsburgh', 'Panthers': 'Carolina', 'Raiders': 'Las Vegas', 'Bills': 'Buffalo', 'Broncos': 'Denver', '49ers': 'San Francisco',
        'Vikings': 'Minnesota', 'Chiefs': 'Kansas City', 'Cowboys': 'Dallas', 'Heat': 'Miami', 'Mavericks': 'Dallas', 'Oilers': 'Edmonton', 'Thunder': 'Oklahoma', 'Jazz': 'Utah', 'Blues': 'St. Louis'}
EVM = {}
def evm(ev):
    if ev not in EVM:
        d = cu(f'{B}/events/{ev}?with_nested_markets=true'); EVM[ev] = d.get('markets') or (d.get('event') or {}).get('markets') or []
    return EVM[ev]
# game starts from ESPN scoreboards
START = {}
for sp in ('football/nfl', 'basketball/nba', 'hockey/nhl', 'tennis/atp'):
    s = cu(f"https://site.api.espn.com/apis/site/v2/sports/{sp}/scoreboard?dates={D.replace('-', '')}")
    for e in s.get('events', []): START[frozenset(re.findall(r'[A-Z]{2,4}', e.get('shortName', ''))) - {'VS'}] = e['date']
def start_of(l):
    f = FEAT.get(l['key'], {})
    if f.get('game_start'): return f['game_start']
    return START.get(frozenset(re.findall(r'[A-Z]{2,4}', l['event'] or '')) - {'VS'})
def market(l, ev):
    p = l['pick']; t = p.lower(); ms = evm(ev); under = ' under ' in t
    if ' ML ' in p or p.endswith(' ML'):
        team = p.split(' ML')[0]; c = CITY.get(team, team)
        m = [x for x in ms if (x.get('yes_sub_title') or x['title']).startswith(c)]
        return (m[0], False) if len(m) == 1 else (None, None)
    if 'total points' in t and 'team' not in t:
        x = re.search(r'(over|under) (\d+(?:\.5)?)', t).group(2)
        m = [y for y in ms if re.search(rf'over {x}\b', y['title'])]
        return (m[0], under) if len(m) == 1 else (None, None)
    if 'longest' in t:
        x = re.search(r'(\d+\.5)', t).group(1); name = re.split(r' (?:\d|under|longest)', p)[0]
        m = [y for y in ms if nrm(y['title'].split(':')[0]) == nrm(name) and re.search(rf'over {x} ', y['title'])]
        return (m[0], under) if len(m) == 1 else (None, None)
    if re.search(r' [+-]\d+(?:\.5)? ', p):
        team = p.split(' ')[0]; x = abs(float(re.search(r'([+-]\d+(?:\.5)?)', p).group(1))); fav = '-' in p.split(' ')[1]
        m = [y for y in ms if re.search(rf'over {x} ', y['title']) and (y['title'].startswith(CITY.get(team, team)) == fav)]
        return (m[0], not fav) if len(m) == 1 else (None, None)
    name = re.split(r' (?:\d|under|anytime)', p)[0]
    n = 1 if 'anytime' in t else (int(re.search(r'(\d+)\+', p).group(1)) if re.search(r'(\d+)\+', p) else int(float(re.search(r'under (\d+(?:\.5)?)', t).group(1)) + 0.5) if under else None)
    m = [y for y in ms if (mm := re.match(r'(.+?): (\d+)\+', y['title'])) and nrm(mm.group(1)) == nrm(name) and int(mm.group(2)) == n]
    return (m[0], under) if len(m) == 1 else (None, None)
def close(tk, st):
    ser = tk.split('-')[0]; s = datetime.fromisoformat(st.replace('Z', '+00:00'))
    for a, iv in ((s - timedelta(hours=1), 1), (s - timedelta(hours=24), 60)):
        c = cu(f'{B}/series/{ser}/markets/{tk}/candlesticks?start_ts={int(a.timestamp())}&end_ts={int(s.timestamp())}&period_interval={iv}').get('candlesticks', [])
        for x in reversed(c):
            yb = (x.get('yes_bid') or {}).get('close_dollars'); ya = (x.get('yes_ask') or {}).get('close_dollars')
            if yb is not None and ya is not None and float(ya) > 0:
                return round(100 * (float(yb) + float(ya)) / 2, 1), datetime.fromtimestamp(x['end_period_ts'], timezone.utc).isoformat(), round(100 * (float(ya) - float(yb)), 1)
    return None, None, None
out = {}
def one(l):
    i = str(l.get('leg_no')); ev = (KM.get(i) or {}).get('ev')
    if l.get('k_pick') is None or not ev: return l['key'], {'why': 'no pick-time Kalshi price' if l.get('k_pick') is None else 'no Kalshi event'}
    m, inv = market(l, ev); st = start_of(l)
    if not m: return l['key'], {'why': 'no unique market match', 'ev': ev}
    if not st: return l['key'], {'why': 'no game start', 'ticker': m['ticker']}
    if datetime.fromisoformat(st.replace('Z', '+00:00')) > datetime.now(timezone.utc): return l['key'], {'why': 'game not started yet', 'ticker': m['ticker'], 'start': st}
    mid, ts, spr = close(m['ticker'], st)
    if mid is None: return l['key'], {'why': 'no quote before start', 'ticker': m['ticker']}
    return l['key'], {'ticker': m['ticker'], 'invert': inv, 'k_close': round(100 - mid, 1) if inv else mid, 'k_close_ts': ts, 'spread': spr, 'start': st, 'result': m.get('result')}
for l in LEGS: evm((KM.get(str(l.get('leg_no'))) or {}).get('ev')) if (KM.get(str(l.get('leg_no'))) or {}).get('ev') else None
with ThreadPoolExecutor(4) as ex: out = dict(ex.map(one, LEGS))
prev = json.load(open(f'ledger/close_{D}.json')) if os.path.exists(f'ledger/close_{D}.json') else {}
for k, v in prev.items():   # a close already captured is never replaced
    if 'k_close' in v: out[k] = v
json.dump(out, open(f'ledger/close_{D}.json', 'w'), indent=0)
from collections import Counter
print(Counter('close' if 'k_close' in v else v['why'] for v in out.values()))
for l in LEGS[:200]:
    v = out[l['key']]
    if 'k_close' in v and abs(v['k_close'] - l['k_pick']) > 12: print('big move', l['pick'], l['k_pick'], '->', v['k_close'])
