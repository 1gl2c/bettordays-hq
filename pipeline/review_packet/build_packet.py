"""Build the historical data packet for the independent AI review runs.

Usage (from pipeline/):
  python3 review_packet/build_packet.py OUT_DIR BETA_DATE RS_EXPORT_JSON BETA_GRADED_JSON

- Reads model_picks, model_tickets and model_pick_corrections from Supabase using the
  site's public (publishable) key in ../sb.js. These tables are public-read.
- Reads Beta lines from beta/all_lines.json and the graded Top 15 file (e.g. beta/beta_graded_nov18.json).
- RS_EXPORT_JSON is the Perfect Parlays backtest/hindsight export from the live page
  (review_packet/rs_export.cjs). It is optional: pass '-' to skip.
- It only reads data and writes CSVs. It does not change grades, results or the site.
"""
import csv, json, os, re, subprocess, sys

OUT, BETA_DATE, RSX, GF = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
os.makedirs(OUT, exist_ok=True)
KEY = re.search(r"sb_publishable_[A-Za-z0-9_-]+", open('../sb.js').read()).group(0)
URL = 'https://ndcsjhetuasijbgpfhwj.supabase.co/rest/v1/'

def get(table):
    rows, off = [], 0
    while True:
        r = subprocess.run(['curl', '-s', '-m', '60', f'{URL}{table}?select=*&order=id.asc&offset={off}&limit=1000',
                            '-H', f'apikey: {KEY}', '-H', f'Authorization: Bearer {KEY}'], capture_output=True, text=True).stdout
        page = json.loads(r)
        rows += page
        if len(page) < 1000: return rows
        off += 1000

def nz(s): return re.sub(r'[^a-z0-9]', '', (s or '').lower())

P = get('model_picks')
cols = ['pick_key','slate_date','game_time_text','sport','event','player','market','stat','direction','line','line_style','pick_text','capper_line','moved','grade','grade_version','b2b','matchup','kalshi_ticker','kalshi_price_grade','kalshi_price_grade_ts','kalshi_price_close','kalshi_price_close_ts','kalshi_result','result','actual','status','data_source','data_gaps','notes']
with open(f'{OUT}/picks_history.csv', 'w', newline='') as f:
    w = csv.writer(f); w.writerow(cols + ['d_game_key','d_ladder_key','d_kalshi_price_interpolated','d_real_line_move'])
    for p in sorted(P, key=lambda p: (p['slate_date'], p['id'])):
        gaps = p['data_gaps'] or []
        row = [('; '.join(p[c]) if c == 'data_gaps' and p[c] else p[c]) for c in cols]
        gk = p['slate_date'] + '|' + p['event'] if p['event'] else ''
        lk = f"{p['slate_date']}|{nz(p['player'])}|{p['stat']}|{p['direction'] or ''}" if p['player'] and p['stat'] else ''
        real = '' if p['moved'] is None else (bool(p['moved']) and p['capper_line'] is None)
        w.writerow(['' if v is None else v for v in row] + [gk, lk, any('interpolated' in g for g in gaps), real])

T = get('model_tickets')
with open(f'{OUT}/tickets_history.csv', 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['slate_date','name','n_legs','legs','played','result','note'])
    for t in sorted(T, key=lambda t: (t['slate_date'], t['id'])):
        w.writerow([t['slate_date'], t['name'], len(t['legs'] or []), ' || '.join(t['legs'] or []), t['played'], t['result'], t['note'] or ''])

C = get('model_pick_corrections'); byid = {p['id']: p['pick_key'] for p in P}
with open(f'{OUT}/corrections.csv', 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['pick_key','field','old_value','new_value','reason','corrected_at'])
    for c in C: w.writerow([byid.get(c['pick_id'], c['pick_id']), c['field'], c['old_value'], c['new_value'], c['reason'], c['corrected_at']])

A = json.load(open('beta/all_lines.json'))
G = {(g['player'], g['stat'], g['line']): g for g in json.load(open(GF))}
with open(f'{OUT}/beta_sim_lines_{BETA_DATE}.csv', 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['slate_date','game','tip_local','player','team','stat','line_n_plus','kalshi_ask','kalshi_bid','american_odds','breakeven_pct','sim_hit_pct','mc_se','season_games','season_hits','last5_hits','sample_unc_95','edge_pct','price_move_since_first_snapshot','questionable','top15_rank','result','actual'])
    for a in sorted(A, key=lambda a: -a['edge']):
        g = G.get((a['player'], a['st'], a['k']))
        w.writerow([BETA_DATE, a['g'], a['t'], a['player'], a['team'], a['st'], a['k'], a['ask'], a['bid'], a['odds'], a['be'], a['sim'], a['se'], a['n'], a['hs'], a['h5'], a['unc'], a['edge'], a.get('move'), a.get('q'), g['rank'] if g else '', g['result'] if g else 'NOT GRADED', g['actual'] if g else ''])

if RSX != '-':
    X = json.load(open(RSX))
    with open(f'{OUT}/perfect_parlays_backtest_and_hindsight.csv', 'w', newline='') as f:
        w = csv.writer(f); w.writerow(['night','kind','how_built','est_payout_x','leg','leg_grade','leg_hit'])
        for b in X['bt']:
            for k, lab in (('three', 'Beta 3 backtest rebuild'), ('ten', 'Beta 10x backtest rebuild')):
                for l in b[k]['legs']:
                    w.writerow([b['d'], lab, 'rules applied to that night using only earlier nights; rules were written after seeing these nights; no Kalshi prices for past nights', round(b[k]['x'], 2), l['pick'], l['grade'], l['hit']])
        for q in X['perfect']:
            for k, lab in (('a', 'Hindsight perfect 3-5x'), ('b', 'Hindsight perfect 10x+')):
                for l in q[k]['legs']:
                    w.writerow([q['d'], lab, 'chosen AFTER results were known, from legs that hit; not a prediction', round(q[k]['x'], 2), l['pick'], l['grade'], 1])

wl = [p for p in P if p['result'] in ('W', 'L')]
print(json.dumps({'rows': len(P), 'W': sum(p['result'] == 'W' for p in wl), 'L': sum(p['result'] == 'L' for p in wl),
                  '70+': [sum(p['result'] == 'W' for p in wl if p['grade'] >= 70), sum(p['result'] == 'L' for p in wl if p['grade'] >= 70)],
                  '80+': [sum(p['result'] == 'W' for p in wl if p['grade'] >= 80), sum(p['result'] == 'L' for p in wl if p['grade'] >= 80)],
                  'tickets': len(T), 'beta_lines': len(A), 'beta_graded': len(G)}))
