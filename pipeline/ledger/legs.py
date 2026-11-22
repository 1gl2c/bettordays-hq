"""Every graded leg since Nov 4 in one list (Phase 1 backfill input).
Sources, in order: daily/2026-11-19/picks_history.csv (Nov 4-18, the audited history export), thu/thu_graded.json (Nov 19),
daily/<date>/v7_merged.json (Nov 20-22, engine v7/v8). Nothing is invented: a field missing at the source stays None.
Usage: python3 ledger/legs.py -> ledger/legs.json"""
import csv, json, re
L = []
num = lambda x: float(x) if x not in (None, '', 'None') else None
for r in csv.DictReader(open('daily/2026-11-19/picks_history.csv')):
    L.append(dict(key=r['pick_key'], date=r['slate_date'], src='model_picks', sport=r['sport'] or None, event=r['event'] or None,
                  t=r['game_time_text'] or None, player=r['player'] or None, market=r['market'] or None, stat=r['stat'] or None,
                  dir=r['direction'] or None, line=num(r['line']), pick=r['pick_text'], ticker=r['kalshi_ticker'] or None,
                  grade=num(r['grade']), grade_version=r['grade_version'] or None, grade_uses_market=r['d_grade_uses_market'] == 'True',
                  k_pick=num(r['d_kalshi_grade_observed']) if r['d_kalshi_grade_observed'] else num(r['kalshi_price_grade']),
                  k_pick_kind='observed' if r['d_kalshi_grade_observed'] else ('logged' if r['kalshi_price_grade'] else None),
                  k_pick_ts=r['d_kalshi_grade_ts'] or r['kalshi_price_grade_ts'] or None,
                  k_close=num(r['d_kalshi_tip_observed']) if r['d_kalshi_tip_observed'] else num(r['d_kalshi_tip_estimated']),
                  k_close_kind='observed at tip' if r['d_kalshi_tip_observed'] else ('estimated at tip' if r['d_kalshi_tip_estimated'] else None),
                  k_close_ts=r['d_kalshi_tip_ts'] or None, b2b=(r['b2b'] == 'True') if r['b2b'] else None, matchup=r['matchup'] or None,
                  notes=r['notes'] or None, result=r['result'] or None, actual=num(r['actual']), status=r['d_record_status']))
T = json.load(open('thu/thu_graded.json'))['rows']
for i, r in enumerate(T, 1):
    L.append(dict(key=f"2026-11-19|thu|{i}", date='2026-11-19', src='model_picks', sport=r.get('sp'), event=r.get('g'), t=r.get('t'), player=None,
                  market=r.get('ty'), stat=None, dir=None, line=None, pick=r['p'], ticker=None, grade=r.get('pct'), grade_version='v9 original process (Nov 19)',
                  grade_uses_market=False, k_pick=r.get('k'), k_pick_kind='logged' if r.get('k') is not None else None, k_pick_ts='2026-11-19T23:41:24+00:00' if r.get('k') is not None else None,
                  k_close=None, k_close_kind=None, k_close_ts=None, b2b=None, matchup=r.get('mu'), notes=r.get('n'), result=r.get('r'), actual=r.get('act'), status=None))
RES = {'2026-11-20': 'fri20/res/analysis.json', '2026-11-21': 'sat21/res/analysis.json'}
for d in ('2026-11-20', '2026-11-21', '2026-11-22'):
    import os   # the board as posted (frozen copy) wins over any later re-merge of the same day
    M = json.load(open(f'daily/{d}/v7_merged_pick.json' if os.path.exists(f'daily/{d}/v7_merged_pick.json') else f'daily/{d}/v7_merged.json'))
    R = {x['i']: x for x in json.load(open(RES[d]))['legs']} if d in RES else {}
    for l in M['legs']:
        rr = R.get(l['i'], {})
        L.append(dict(key=f"{d}|v7|{l['i']}", date=d, src='model_v7_legs', leg_no=l['i'], sport=l.get('sp'), event=l.get('g'), t=l.get('t'), player=l.get('player'),
                      market=l.get('ty'), stat=l.get('stat'), dir=None, line=None, pick=l['p'], ticker=None, event_ticker=None,
                      grade=l.get('pub') if l.get('pub') is not None else l.get('med'), grade_version=l.get('eng'), grade_uses_market=False,
                      k_pick=l.get('k'), k_pick_kind='logged at merge' if l.get('k') is not None else None, k_pick_ts=M.get('kalshi_ts') if l.get('k') is not None else None,
                      k_close=None, k_close_kind=None, k_close_ts=None, b2b=l.get('b2b'), matchup=None, notes=l.get('n'),
                      result=rr.get('r'), actual=rr.get('act'), status=None, fl=l.get('fl'), tier=l.get('tier'), placement=l.get('pl'),
                      sys=l.get('sys'), med=l.get('med'), models=l.get('models'), why=l.get('why'), conf=l.get('conf'), bk=l.get('bk')))
# parse line and direction from the pick text where the source did not store them
for l in L:
    p = l['pick']; tl = p.lower()
    if l['line'] is None:
        m = re.search(r'(\d+(?:\.\d)?)\+', p) or re.search(r'(?:over|under) (\d+(?:\.\d)?)', tl)
        if m: l['line'] = float(m.group(1))
    if l['dir'] is None: l['dir'] = 'u' if ' under ' in f' {tl} ' else 'o'
json.dump(L, open('ledger/legs.json', 'w'), indent=0)
from collections import Counter
print(len(L), Counter(l['date'] for l in L))
