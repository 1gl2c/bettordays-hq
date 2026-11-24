"""Match every Nov 24 leg to its Kalshi market: price (mid of bid and ask, 0-100), event ticker and market ticker.
Unders price as 100 minus the YES market at the same number; a whole-number under (under 25) is the NO side of 25+.
Usage (from pipeline/): python3 tue24/kmatch.py -> tue24/kmatch.json"""
import json, re, unicodedata
K = json.load(open('tue24/kalshi.json')); LEGS = json.load(open('tue24/legs.json'))
nrm = lambda s: re.sub(r'[^a-z]', '', re.sub(r'\b(jr|sr|ii|iii|iv)\b', '', unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode().lower()))
def mid(m):
    a = float(m['yes_ask_dollars'] or 0); b = float(m['yes_bid_dollars'] or 0)
    return round(100 * ((a + b) / 2 if a and b else a or b), 1)
TODAY = lambda s: [m for m in K.get(s, []) if '26NOV24' in m['event_ticker']]
SER = {'pts': 'KXNBAPTS', 'reb': 'KXNBAREB', 'ast': 'KXNBAAST', '3pm': 'KXNBA3PT', 'pra': 'KXNBAPRA', 'recyds': 'KXNFLRECYDS', 'rec': 'KXNFLREC', 'rush': 'KXNFLRSHYDS',
       'pass': 'KXNFLPASSYDS', 'td': 'KXNFLTD', 'pass td': 'KXNFLPASSTDS', 'int': 'KXNFLPASSINT'}
CITY = {'Penn': 'Penn', 'Louisville': 'Louisville', 'Alabama': 'Alabama', "St. John's": "St. John's", 'Magic': 'Orlando', 'Wizards': 'Washington', 'Mavericks': 'Dallas'}
FAV = {'DET@ORL': 'Detroit', 'BOS@WSH': 'Boston', 'DAL@DEN': 'Denver'}
def code(g): return g.replace('@', '').replace('UTAH', 'UTA').replace('WSH', 'WAS')
out = {}
for i, l in enumerate(LEGS, 1):
    p = l['p']; t = p.lower(); k = ev = tk = None; note = ''
    if l['mkt'] == 'ml':
        team = next(c for c in sorted(CITY, key=len, reverse=True) if p.startswith(c)); ser = {'NBA': 'KXNBAGAME', 'NFL': 'KXNFLGAME', 'CBB': 'KXNCAAMBGAME'}[l['sp']]
        ms = [m for m in TODAY(ser) if (m.get('yes_sub_title') or m['title']).startswith(CITY[team]) and (l['sp'] == 'CBB' or m['event_ticker'].endswith(code(l['g'])))]
        if l['sp'] == 'CBB': ms = [m for m in ms if m['title'] == CITY[team] + ' wins']
        if len(ms) == 1: k, ev, tk = mid(ms[0]), ms[0]['event_ticker'], ms[0]['ticker']
        else: note = f'{len(ms)} markets'
    elif l['mkt'] == 'spread':
        team = p.split(' ')[0]; x = float(re.search(r'([+-]\d+(?:\.5)?)', p).group(1))
        if abs(x) % 1 == 0: note = 'whole-number spread can push; Kalshi lists only .5 lines'
        elif x > 0:   # underdog +x wins unless the favorite wins by more than x: NO on 'favorite wins by over x'
            ms = [m for m in TODAY('KXNBASPREAD') if m['event_ticker'].endswith(code(l['g'])) and m['title'] == f"{FAV[l['g']]} wins by over {abs(x)} points"]
            if len(ms) == 1: k, ev, tk = round(100 - mid(ms[0]), 1), ms[0]['event_ticker'], ms[0]['ticker']
            else: note = f'{len(ms)} spread markets'
    elif l['mkt'] == 'total':
        x = float(re.search(r'over (\d+(?:\.5)?)', t).group(1))
        if x % 1 == 0: note = 'whole-number total can push; Kalshi lists only .5 lines'
    else:
        name = l.get('player') or re.split(r' (?:\d|under|anytime)', p)[0]; under = ' under ' in t
        if 'anytime' in t: n = 1
        elif re.search(r'(\d+)\+', p): n = int(re.search(r'(\d+)\+', p).group(1))
        else:
            x = float(re.search(r'under (\d+(?:\.5)?)', t).group(1)); n = int(x + 0.5) if x % 1 else int(x)   # under 20.5 = NO on 21+; under 20 = NO on 20+
        for m in TODAY(SER[l['mkt']]):
            mm = re.match(r'(.+?): (\d+)\+', m['title'])
            if mm and nrm(mm.group(1)) == nrm(name) and int(mm.group(2)) == n:
                k, ev, tk = (round(100 - mid(m), 1) if under else mid(m)), m['event_ticker'], m['ticker']
        if k is None: note = 'Kalshi does not list this number'
    out[i] = {'p': p, 'k': k, 'ev': ev, 'ticker': tk, 'note': note}
json.dump(out, open('tue24/kmatch.json', 'w'), indent=1)
print(sum(v['k'] is not None for v in out.values()), 'of', len(out), 'priced')
for i, v in out.items(): print(i, v['k'], v['p'], v['note'])
