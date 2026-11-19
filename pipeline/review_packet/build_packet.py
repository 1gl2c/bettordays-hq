"""Build the historical data packet for the independent AI review runs (v2).

Usage (from pipeline/):
  python3 review_packet/build_packet.py OUT_DIR HIST_END RS_EXPORT_JSON

- HIST_END: last slate date included in the history (e.g. 2026-11-18). Later slates are left out.
- Reads model_picks, model_tickets, model_pick_corrections and model_beta_lines from Supabase
  with the site's public (publishable) key in ../sb.js. These tables are public-read.
- RS_EXPORT_JSON: Perfect Parlays backtest/hindsight export from the built page
  (review_packet/rs_export.cjs). Pass '-' to skip.
- It only reads data and writes CSVs. It does not change grades, results or the site.
- Columns starting with d_ are derived here; the rules for each are written next to them below.
"""
import csv, json, os, re, subprocess, sys
from collections import Counter

OUT, HIST_END, RSX = sys.argv[1], sys.argv[2], sys.argv[3]
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
def blank(v): return '' if v is None else v

# ---------------- picks
P = [p for p in get('model_picks') if p['slate_date'] <= HIST_END]

def record_status(p):
    """Which statistic a row can be counted in."""
    r = p['result']
    if r == 'W': return 'settled_win', ''
    if r == 'L': return 'settled_loss', ''
    if r == 'P': return 'push', ''
    if r == 'V': return 'void', ''
    gaps = p['data_gaps'] or []; n = p['notes'] or ''
    if any('started before' in g for g in gaps): return 'unresolved', 'game started before the list arrived; never graded'
    if any('void' in g for g in gaps): return 'unresolved', 'player ruled out; marked void in the note but result field never set'
    if re.search(r'Actual: ?\d', n): return 'unresolved', 'an actual stat is in the note but no W/L was entered'
    if re.search(r'\bOUT\b|ruled out|Do not play|Skip', n, re.I): return 'unresolved', 'player out or flagged skip before games; no result logged'
    return 'unresolved', 'graded before games; result never logged'

def grade_uses_market(p):
    """True when the grade itself was taken from, or pulled toward, the Kalshi price."""
    n = p['notes'] or ''; v = p['grade_version'] or ''; d = p['slate_date']
    if 'v8' in v: return True, 'v8 grade pulled toward Kalshi (withdrawn method)'
    if re.search(r"Graded at Kalshi's price|Graded off the market price|^Market price", n): return True, 'grade set at the Kalshi price (no own model for this market)'
    if d in ('2026-11-16', '2026-11-17') and p['sport'] == 'NBA' and p['market'] in ('ml', 'spread') and (p['kalshi_price_grade'] is not None):
        return True, 'NBA team line graded as the average of the spread model and Kalshi'
    return False, ''

def grade_price_estimated(p):
    n = p['notes'] or ''
    if 'estimated between two Kalshi lines' in n: return True
    if p['slate_date'] == '2026-11-16' and p['market'] in ('spread', 'total'): return True   # mon/grade.py interp() on Kalshi ladders
    return False

cols = ['pick_key','slate_date','game_time_text','sport','event','player','market','stat','direction','line','line_style','pick_text','capper_line','moved','grade','grade_version','b2b','matchup','kalshi_ticker','kalshi_price_grade','kalshi_price_grade_ts','kalshi_price_close','kalshi_price_close_ts','kalshi_result','result','actual','status','data_source','data_gaps','notes']
dcols = ['d_record_status','d_unresolved_reason','d_in_win_loss_record','d_game_key','d_ladder_key','d_real_line_move',
         'd_kalshi_tip_observed','d_kalshi_tip_estimated','d_kalshi_tip_ts','d_kalshi_grade_observed','d_kalshi_grade_estimated','d_kalshi_grade_ts',
         'd_grade_uses_market','d_grade_uses_market_reason','d_head_to_head_eligible']
H2H = Counter(); STAT = Counter()
with open(f'{OUT}/picks_history.csv', 'w', newline='') as f:
    w = csv.writer(f); w.writerow(cols + dcols)
    for p in sorted(P, key=lambda p: (p['slate_date'], p['id'])):
        gaps = p['data_gaps'] or []
        row = [('; '.join(p[c]) if c == 'data_gaps' and p[c] else p[c]) for c in cols]
        st, why = record_status(p); STAT[(st, why)] += 1
        gk = p['slate_date'] + '|' + p['event'] if p['event'] else ''
        lk = f"{p['slate_date']}|{nz(p['player'])}|{p['stat']}|{p['direction'] or ''}" if p['player'] and p['stat'] else ''
        real = '' if p['moved'] is None else (bool(p['moved']) and p['capper_line'] is None)
        tip_est = any('interpolated' in g for g in gaps)          # audit backfill flagged interpolated tip prices
        tip = p['kalshi_price_close']; gp = p['kalshi_price_grade']; gest = gp is not None and grade_price_estimated(p)
        um, umr = grade_uses_market(p)
        h2h = st in ('settled_win', 'settled_loss') and gp is not None and not gest and not um
        if h2h: H2H[p['slate_date']] += 1
        w.writerow([blank(v) for v in row] + [st, why, st in ('settled_win', 'settled_loss'), gk, lk, real,
            blank(tip if tip is not None and not tip_est else None), blank(tip if tip is not None and tip_est else None), blank(p['kalshi_price_close_ts']),
            blank(gp if gp is not None and not gest else None), blank(gp if gest else None), blank(p['kalshi_price_grade_ts']),
            um, umr, h2h])

# ---------------- tickets, corrections
T = [t for t in get('model_tickets') if t['slate_date'] <= HIST_END]
with open(f'{OUT}/tickets_history.csv', 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['slate_date','name','n_legs','legs','played','result','note'])
    for t in sorted(T, key=lambda t: (t['slate_date'], t['id'])):
        w.writerow([t['slate_date'], t['name'], len(t['legs'] or []), ' || '.join(t['legs'] or []), t['played'], t['result'], t['note'] or ''])
C = get('model_pick_corrections'); byid = {p['id']: p['pick_key'] for p in get('model_picks')}
with open(f'{OUT}/corrections.csv', 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['pick_key','field','old_value','new_value','reason','corrected_at'])
    for c in C: w.writerow([byid.get(c['pick_id'], c['pick_id']), c['field'], c['old_value'], c['new_value'], c['reason'], c['corrected_at']])

# ---------------- Beta lines (all nights in the database up to HIST_END)
B = [b for b in get('model_beta_lines') if b['slate_date'] <= HIST_END]
bcols = ['slate_date','ticker','player','team','event','game_time_text','stat','line','ask','bid','american_odds','breakeven','sim_prob','sim_runs','mc_se','sample_games','sample_hits','last5_hits','sample_unc','edge','price_move','price_ts','sim_ts','rank','shown_on_site','pregame_record','outcome_class','actual','outcome_source','outcome_backfilled','outcome_note']
with open(f'{OUT}/beta_sim_lines.csv', 'w', newline='') as f:
    w = csv.writer(f); w.writerow(bcols + ['d_game_key','d_player_key'])
    for b in sorted(B, key=lambda b: (b['slate_date'], -(b['edge'] or 0))):
        w.writerow([blank(b[c]) for c in bcols] + [f"{b['slate_date']}|{b['event']}", f"{b['slate_date']}|{nz(b['player'])}"])

# ---------------- Perfect Parlays
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
                  'status': {f'{a}|{b}': n for (a, b), n in sorted(STAT.items())},
                  'head_to_head_eligible_by_date': dict(sorted(H2H.items())),
                  'tickets': len(T), 'beta_lines': len(B), 'beta_outcomes': dict(Counter(b['outcome_class'] for b in B))}, indent=1))
