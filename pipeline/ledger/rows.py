"""One permanent row per leg (Phase 1): joins legs.json, features.json and close_<date>.json into the exact columns of
the leg_ledger table. Every missing field is listed in data_gaps so the gaps stay visible. Usage: python3 ledger/rows.py"""
import json, glob, os
L = json.load(open('ledger/legs.json')); F = json.load(open('ledger/features.json'))
C = {}
for fn in glob.glob('ledger/close_*.json'): C.update(json.load(open(fn)))
SYS_VERSIONS = ('v9 original process', 'v1-v7 (pre-audit)')
rows = []
for l in L:
    f = F.get(l['key'], {}); c = C.get(l['key'], {})
    m = l.get('models') or {}; pan = f.get('panel') or {}
    res = l.get('result'); res = {'W': 'W', 'L': 'L', 'V': 'void', 'P': 'push', 'push': 'push', 'void': 'void'}.get(res, res) or None
    if l.get('status') == 'void': res = 'void'
    if l.get('status') == 'push': res = 'push'
    stats = {k: f[k] for k in ('stat', 'vals_l5', 'avg_l5', 'avg_season', 'n', 'hit_season', 'hit_l5', 'min_l5', 'min_avg_l5', 'min_avg_season', 'games_before') if k in f} or None
    inj = {k: f[k] for k in ('injury_snapshot_at', 'injury_self', 'injuries_team', 'injuries_opp') if k in f} or None
    reasons = {k: v for k, v in (l.get('why') or {}).items() if v} or None
    r = dict(leg_key=l['key'], slate_date=l['date'], source=l['src'], sport=l.get('sport'), event=l.get('event'), game_time_text=l.get('t'),
             game_start=f.get('game_start') or c.get('start'), pick_text=l['pick'], player=f.get('player') or l.get('player'), espn_id=f.get('espn_id'),
             team=f.get('team'), opponent=f.get('opponent'), home_away=f.get('home_away'), market=l.get('market'), stat=f.get('stat') or l.get('stat'),
             direction=l.get('dir'), line=l.get('line'), capture_mode='backfill',
             kalshi_ticker=l.get('ticker') or c.get('ticker'), kalshi_pick=l.get('k_pick'), kalshi_pick_ts=l.get('k_pick_ts'), kalshi_pick_kind=l.get('k_pick_kind'),
             books_pick=l.get('bk'),
             grade_published=l.get('grade'), grade_median=l.get('med'), grade_system=l.get('sys') if l['src'] == 'model_v7_legs' else (l.get('grade') if (l.get('grade_version') or '').startswith(SYS_VERSIONS) else None),
             grade_chatgpt=m.get('chatgpt', pan.get('chatgpt')), grade_gemini=m.get('gemini', pan.get('gemini')), grade_grok=m.get('grok', pan.get('grok')), grade_claude=m.get('claude'),
             grades_saw_market=True if f.get('panel_saw_market') else (bool(l.get('grade_uses_market')) or None), grade_version=l.get('grade_version'),
             tier=l.get('tier'), placement=l.get('placement'), flag=l.get('fl'), reasons=reasons, system_note=l.get('notes'),
             stats=stats, rest_days=f.get('rest_days'), b2b=f.get('b2b') if f.get('b2b') is not None else l.get('b2b'), injuries=inj,
             kalshi_close=l.get('k_close') if l.get('k_close') is not None else c.get('k_close'), kalshi_close_ts=l.get('k_close_ts') or c.get('k_close_ts'),
             kalshi_close_kind=l.get('k_close_kind') or ('last quote before start' if c.get('k_close') is not None else None),
             result=res, actual=l.get('actual') if isinstance(l.get('actual'), (int, float)) else None)
    # priced before the game? price time vs game start when both are known, else the merge-time flag
    st = r['game_start'] or None
    if r['kalshi_pick'] is None: pre = None
    elif r['kalshi_pick_ts'] and st: pre = r['kalshi_pick_ts'].replace('Z', '+00:00') < st.replace('Z', '+00:00') if False else __import__('datetime').datetime.fromisoformat(r['kalshi_pick_ts'].replace('Z', '+00:00')) < __import__('datetime').datetime.fromisoformat(st.replace('Z', '+00:00'))
    else: pre = r['flag'] not in ('LIVE', 'DONE', 'started', 'finished')
    r['priced_pregame'] = pre
    gaps = [k for k in ('kalshi_pick', 'books_pick', 'grade_chatgpt', 'reasons', 'stats', 'injuries', 'opponent', 'rest_days', 'kalshi_close', 'result') if r[k] in (None, [], {})]
    r['data_gaps'] = gaps
    rows.append(r)
json.dump(rows, open('ledger/ledger_rows.json', 'w'))
from collections import Counter
g = Counter(x for r in rows for x in r['data_gaps']); print(len(rows), 'rows; missing counts:', dict(g))
print('results', Counter(r['result'] for r in rows))
