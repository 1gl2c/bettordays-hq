"""Match every Nov 22 leg to its Kalshi market: price (mid of bid and ask, 0-100) and event ticker for the 'Open on Kalshi' link.
Unders and underdog spreads are priced as 100 minus the matching YES market. Lines Kalshi does not list get no price.
Usage (from pipeline/): python3 sun22/kmatch.py  ->  sun22/kmatch.json"""
import json, re, unicodedata
K = json.load(open('sun22/kalshi.json')); LEGS = json.load(open('sun22/legs.json'))
nrm = lambda s: re.sub(r'[^a-z]', '', re.sub(r'\b(jr|sr|ii|iii|iv)\b', '', unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode().lower()))
def mid(m):
    a = float(m['yes_ask_dollars'] or 0); b = float(m['yes_bid_dollars'] or 0)
    return round(100 * ((a + b) / 2 if a and b else a or b), 1)
TODAY = lambda s: [m for m in K.get(s, []) if '26NOV22' in m['event_ticker']]
CITY = {'Bears': 'Chicago', 'Lions': 'Detroit', 'Jaguars': 'Jacksonville', 'Eagles': 'Philadelphia', 'Ravens': 'Baltimore', 'Buccaneers': 'Tampa Bay', 'Chargers': 'Los Angeles C',
        'Giants': 'New York G', 'Steelers': 'Pittsburgh', 'Panthers': 'Carolina', 'Raiders': 'Las Vegas', 'Bills': 'Buffalo', 'Broncos': 'Denver', '49ers': 'San Francisco',
        'Vikings': 'Minnesota', 'Chiefs': 'Kansas City', 'Cowboys': 'Dallas', 'Heat': 'Miami', 'Mavericks': 'Dallas', 'Oilers': 'Edmonton'}
GT = {'MIA@BUF': 'MIABUF', 'NO@CHI': 'NOCHI', 'TEN@DAL': 'TENDAL', 'TB@DET': 'TBDET', 'ARI@KC': 'ARIKC', 'PIT@PHI': 'PITPHI', 'BAL@CAR': 'BALCAR', 'NYJ@LAC': 'NYJLAC',
      'LV@DEN': 'LVDEN', 'JAX@NYG': 'JACNYG', 'MIN v SF': 'MINSF', 'IND@NY': 'INDNYK', 'ORL@WSH': 'ORLWAS', 'OKC@MIA': 'OKCMIA', 'DAL@UTAH': 'DALUTA', 'EDM@STL': 'EDMSTL'}
SER = {'receiving yards': 'KXNFLRECYDS', 'receptions': 'KXNFLREC', 'rushing yards': 'KXNFLRSHYDS', 'rushing attempts': 'KXNFLRSHATT', 'passing yards': 'KXNFLPASSYDS',
       'touchdown': 'KXNFLTD', 'interceptions': 'KXNFLPASSINT', 'threes': 'KXNBA3PT', 'rebounds': 'KXNBAREB'}
def prop(player, ser, n):
    for m in TODAY(ser):
        t = m['title']; mm = re.match(r'(.+?): (\d+)\+', t)
        if mm and nrm(mm.group(1)) == nrm(player) and int(mm.group(2)) == n: return mid(m), m['event_ticker']
    return None, None
def evt(g, ser):
    code = GT.get(g)
    return next((m['event_ticker'] for m in TODAY(ser) if code and m['event_ticker'].endswith(code)), None)
out = {}
for i, l in enumerate(LEGS, 1):
    p = l['p']; t = p.lower(); k = ev = None; note = ''
    if l['sp'] == 'TENNIS':
        ser = 'KXATPMATCH' if 'ML' in p else 'KXATPEXACTMATCH'
        for m in K.get(ser, []):
            if ('ML' in p and m['ticker'].endswith('-ALC')) or ('straight' in t and m['ticker'].endswith('-ALC20')): k, ev = mid(m), m['event_ticker']
    elif ' ML ' in p:
        team = p.split(' ML')[0]; ser = {'NFL': 'KXNFLGAME', 'NBA': 'KXNBAGAME', 'NHL': 'KXNHLGAME'}[l['sp']]
        code = GT.get(l['g'])
        for m in TODAY(ser):
            if code and m['event_ticker'].endswith(code) and m['title'].startswith(CITY[team]): k, ev = mid(m), m['event_ticker']
    elif 'total points' in t and 'team' not in t:
        mm = re.search(r'(over|under) (\d+(?:\.5)?)', t); x = float(mm.group(2)); ev = evt(l['g'], 'KXNFLTOTAL')
        if x % 1:
            for m in TODAY('KXNFLTOTAL'):
                if m['event_ticker'] == ev and re.search(rf'over {x}\b', m['title']): k = mid(m) if mm.group(1) == 'over' else round(100 - mid(m), 1)
        else: note = 'whole-number total can push; Kalshi lists only .5 lines'
    elif 'team total' in t:
        x = float(re.search(r'over (\d+\.5)', t).group(1)); ev = evt(l['g'], 'KXNFLTEAMTOTAL')
        for m in TODAY('KXNFLTEAMTOTAL'):
            if m['event_ticker'] == ev and m['title'].startswith('Buffalo') and re.search(rf'over {x} ', m['title']): k = mid(m)
    elif l['mkt'] in ('spread', '1h spread'):
        team = p.split(' ')[0]; x = float(re.search(r'([+-]\d+(?:\.5)?)', p).group(1)); ser = 'KXNFL1HSPREAD' if 'first half' in t else 'KXNFLSPREAD'
        ev = evt(l['g'], ser); opp = [c for c in CITY if c != team and evt(l['g'], ser) and c in ('Bears', 'Saints')]   # placeholder, replaced below
        if abs(x) % 1:
            line = abs(x)
            if x < 0:   # favorite must win by more than the line
                for m in TODAY(ser):
                    if m['event_ticker'] == ev and m['title'].startswith(CITY[team]) and re.search(rf'over {line} ', m['title']): k = mid(m)
            else:       # underdog covers unless the favorite wins by more than the line
                for m in TODAY(ser):
                    if m['event_ticker'] == ev and not m['title'].startswith(CITY[team]) and re.search(rf'over {line} ', m['title']): k = round(100 - mid(m), 1)
        else: note = 'whole-number spread can push; Kalshi lists only .5 lines'
    else:
        name = re.split(r' (?:\d|under|anytime)', p)[0]
        under = ' under ' in t
        mm = re.search(r'(\d+)\+', p); un = re.search(r'under (\d+(?:\.5)?)', t)
        st = next((v for kk, v in SER.items() if kk in t), None)
        if 'anytime' in t: n = 1; st = 'KXNFLTD'
        elif mm: n = int(mm.group(1))
        elif un: n = int(float(un.group(1)) + 0.5)
        else: n = None
        if 'longest' in t:
            x = float(re.search(r'(\d+\.5)', t).group(1)); ser = 'KXNFLLONGREC' if 'reception' in t else 'KXNFLLONGRSH'
            for m in TODAY(ser):
                mt = re.match(r'(.+?): longest', m['title'])
                if mt and nrm(mt.group(1)) == nrm(name) and re.search(rf'over {x} ', m['title']): k, ev = (round(100 - mid(m), 1) if under else mid(m)), m['event_ticker']
        elif 'tackles' in t or 'rushing + receiving' in t: note = 'Kalshi does not list this market'
        elif st and n is not None:
            k, ev = prop(name, st, n)
            if k is not None and under: k = round(100 - k, 1)
    if ev is None and l['g'] in GT:
        ev = evt(l['g'], {'NFL': 'KXNFLGAME', 'NBA': 'KXNBAGAME', 'NHL': 'KXNHLGAME'}.get(l['sp'], 'KXNFLGAME'))   # game page as the fallback link
    out[i] = {'p': p, 'k': k, 'ev': ev, 'note': note}
json.dump(out, open('sun22/kmatch.json', 'w'), indent=1)
priced = [v for v in out.values() if v['k'] is not None]
print(f'{len(priced)} of {len(out)} legs priced')
for i, v in out.items(): print(i, v['k'], v['p'], v['note'] or '')
