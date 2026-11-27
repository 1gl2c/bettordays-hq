"""Match every Nov 27 leg to its Kalshi market (mid of bid and ask, 0-100). Unders price as 100 minus the YES market at the same
number (under 5 = NO on 5+). Whole-number spreads price from the nearest Kalshi .5 line and say so.
Usage (from pipeline/): python3 fri27/kmatch.py -> fri27/kmatch.json"""
import json, re, unicodedata
K = json.load(open('fri27/kalshi.json')); LEGS = json.load(open('fri27/legs.json'))
nrm = lambda s: re.sub(r'[^a-z]', '', re.sub(r'\b(jr|sr|ii|iii|iv)\b', '', unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode().lower()))
def mid(m):
    a = float(m['yes_ask_dollars'] or 0); b = float(m['yes_bid_dollars'] or 0)
    return round(100 * ((a + b) / 2 if a and b else a or b), 1)
TODAY = lambda s: [m for m in K.get(s, []) if '26NOV27' in m['event_ticker']]
SER = {'pts': 'KXNBAPTS', 'reb': 'KXNBAREB', 'ast': 'KXNBAAST', '3pm': 'KXNBA3PT', 'pra': 'KXNBAPRA'}
# leg -> (series, event suffix, yes_sub_title, side)
GAME = {'Louisville ML v Tennessee': ('KXNCAAMBGAME', 'TENNLOU', 'Louisville', 'yes', ''),
        'Louisville -3 v Tennessee': ('KXNCAAMBSPREAD', 'TENNLOU', 'Louisville wins by over 2.5 points', 'yes', 'priced at -2.5, Kalshi has no -3 (a 3-point win pushes on -3)'),
        'Texas ML at Texas A&M': ('KXNCAAFGAME', 'TEXTXAM', 'Texas', 'yes', ''),
        'Wisconsin ML v Minnesota': ('KXNCAAFGAME', 'MINNWIS', 'Wisconsin', 'yes', ''),
        'Lakers +8 at Spurs': ('KXNBASPREAD', 'LALSAS', 'San Antonio wins by over 8.5 points', 'no', 'priced at +8.5, Kalshi has no +8 (an 8-point loss pushes on +8)'),
        'Suns ML v Mavericks': ('KXNBAGAME', 'DALPHX', 'Phoenix', 'yes', ''),
        'Nets +10.5 at Raptors': ('KXNBASPREAD', 'BKNTOR', 'Toronto wins by over 10.5 points', 'no', ''),
        '76ers ML at Pacers': ('KXNBAGAME', 'PHIIND', 'Philadelphia', 'yes', ''),
        '76ers -1.5 at Pacers': ('KXNBASPREAD', 'PHIIND', 'Philadelphia wins by over 1.5 points', 'yes', '')}
out = {}
for i, l in enumerate(LEGS, 1):
    p = l['p']; t = p.lower(); k = ev = tk = side = None; note = ''
    if p in GAME:
        ser, suf, sub, side, note = GAME[p]
        ms = [m for m in TODAY(ser) if m['event_ticker'].endswith(suf) and (m.get('yes_sub_title') or '') == sub]
        if len(ms) == 1: m = ms[0]; k = mid(m) if side == 'yes' else round(100 - mid(m), 1); ev, tk = m['event_ticker'], m['ticker']
        else: note = f'{len(ms)} markets'
    else:
        name = re.split(r' (?:\d|under)', p)[0]; under = ' under ' in t; side = 'no' if under else 'yes'
        n = int(re.search(r'(\d+)\+', p).group(1)) if not under else int(re.search(r'under (\d+)', t).group(1))
        for m in TODAY(SER[l['mkt']]):
            mm = re.match(r'(.+?): (\d+)\+', m['title'])
            if mm and nrm(mm.group(1)) == nrm(name) and int(mm.group(2)) == n:
                k, ev, tk = (round(100 - mid(m), 1) if under else mid(m)), m['event_ticker'], m['ticker']
        if k is None: note = 'Kalshi does not list this number'
    out[i] = {'p': p, 'k': k, 'ev': ev, 'ticker': tk, 'side': side, 'note': note}
json.dump(out, open('fri27/kmatch.json', 'w'), indent=1)
print(sum(v['k'] is not None for v in out.values()), 'of', len(out), 'priced')
for i, v in out.items(): print(i, v['k'], v['p'], v['note'])
