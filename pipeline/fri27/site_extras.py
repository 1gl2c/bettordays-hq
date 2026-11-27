"""Nov 27 extras on the site source after publish_v8: tonight's Miracle (archive Nov 26 to MIRH), Daily 2x (Edge Lab entry with no
parlays or singles, since no line had the books beating Kalshi after the fee), paper tracker row. Kalshi combo links from kalshi-combo."""
import json
F = 'bettordays-hq.html'; s = open(F).read()
def getc(n):
    i = s.index('const ' + n + '=') + len('const ' + n + '='); v, e = json.JSONDecoder().raw_decode(s[i:]); return v
def setc(n, v):
    global s; i = s.index('const ' + n + '=') + len('const ' + n + '='); _, e = json.JSONDecoder().raw_decode(s[i:]); s = s[:i] + json.dumps(v) + s[i + e:]
fee = lambda q: q + 0.07 * q * (1 - q)
K = json.load(open('fri27/kmatch.json')); BKF = json.load(open('daily/2026-11-27/book_fair.json'))
M = json.load(open('daily/2026-11-27/v7_merged.json')); L = {l['i']: l for l in M['legs']}
GT = {'DALPHX': 'DAL@PHX · 6:00', 'PHIIND': 'PHI@IND · 4:30', 'LALSAS': 'LAL@SA · 6:30', 'GSWPOR': 'GS@POR · 6:30'}
GS = {'DALPHX': '2026-11-28T02:00:00Z', 'PHIIND': '2026-11-28T00:30:00Z'}
# Miracle
MIR = getc('MIR'); MH = getc('MIRH'); assert MIR['d'] == 'Nov 26' and not any(x['d'] == 'Nov 26' for x in MH)
MH.append(MIR); setc('MIRH', MH)
ML = json.load(open('daily/2026-11-27/miracle_ladder.json'))
setc('MIR', {'d': 'Nov 27', 'pays': ML['pays'], 'chance': ML['chance'], 'stake': 10, 'add': [], 'swap': [], 'leg_math': None, 'res': None,
             'kl': 'https://kalshi.com/markets/kxmvecrosscategory/combo/KXMVECROSSCATEGORY-S2026XJ3OMIK54REEDCCH?marketTicker=KXMVECROSSCATEGORY-S2026XJ3OMIK54REEDCCH-TIRXMLT6X',
             'legs': [{'p': l['p'], 'g': GT[l['g']], 'k': l['k'], 'bk': l['bk'], 's': GS[l['g']]} for l in ML['legs']],
             'notes': ['Only 5 lines had at least 2 books posting the exact number and beating Kalshi after the fee, so tonight tops out around 42x at single prices. Kalshi prices the combo itself and can pay less, since three legs share Mavericks at Suns and two share 76ers at Pacers.',
                       'Heat at Knicks had already tipped, so it is left out. This is a $10 paper ticket.']})
# Daily 2x
two_i = [3, 15, 44]; legs = []
for i in two_i:
    l = L[i]; legs.append({'p': l['p'], 'g': GT[K[str(i)]['ev'].split('-')[1][7:]], 'k': l['k'], 'bk': BKF[str(i)]['bk'], 'g8': l['pub']})
pays = 1
for x in legs: pays /= fee(x['k'] / 100)
hit = 1
for x in legs: hit *= x['bk'] / 100
EL = getc('EL'); assert not any(x['d'] == 'Nov 27' for x in EL)
prev2 = next(x for x in reversed(EL) if x.get('two'))['two']
EL.append({'d': 'Nov 27', 'ts': '3:45 PM PT Kalshi prices', 'par': [], 'sing': [],
           'two': {'legs': [{k: v for k, v in x.items() if k != 'g8'} for x in legs], 'pays': round(pays, 2), 'hit': round(100 * hit), 'stake': prev2['stake'], 'res': None,
                   'kl': 'https://kalshi.com/markets/kxmvecrosscategory/combo/KXMVECROSSCATEGORY-S2026AWVMRDT4LTQW5UY6?marketTicker=KXMVECROSSCATEGORY-S2026AWVMRDT4LTQW5UY6-DFFU5HW4Z'}})
setc('EL', EL)
P = getc('PAPER'); assert not any(x['d'] == 'Nov 27' for x in P)
P.append({'d': 'Nov 27', 'ham': {'pays': None, 'res': 'NONE'}, 'mir': {'pays': ML['pays'], 'res': None}}); setc('PAPER', P)
open(F, 'w').write(s)
print('two', [x['p'] for x in legs], round(pays, 2), round(100 * hit), [x['g8'] for x in legs], 'stake', prev2['stake'])
