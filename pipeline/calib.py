"""BettorDays calibration: turn a raw grade into a true hit chance, then price it (Nov 20 audit).

Why: our raw grades are overconfident above 80 (85+ legs hit 72.5% Nov 4-19). Hand-written caps patched that.
Calibration replaces the caps with math learned from our own graded record, refit every day:
  1. Platt scaling with a learned shrunk offset per stat group:  p_cal = sigmoid(a + b*logit(grade) + off[group])
  2. Market blend where Kalshi has a price:                      p_true = sigmoid(c + w1*logit(p_cal) + w2*logit(kalshi))
Every weight is chosen to minimise the Brier score (squared error) on past nights only (walk-forward), which is
the number Ace wants as low as possible. EV after fees = p_true / (price + fee) - 1 for a $1 Kalshi contract.

Usage:  python3 pipeline/calib.py            -> walk-forward Brier report + writes calib.json (repo root)
        from calib import load, true_chance, ev   (merge/publish/grader use the saved weights)
"""
import json, math, os, datetime
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
GROUPS = ['nba_pts', 'nba_ast', 'nba_3pm', 'nba_reb', 'nba_pra', 'nba_ml', 'nba_side', 'college', 'nfl_yds', 'nfl_td', 'other']


def group(sp, st):
    sp = (sp or '').upper()
    if sp in ('CFB', 'CBB', 'NCAAF', 'NCAAB'): return 'college'
    if sp == 'NBA':
        if st in ('pts', 'ast', '3pm', 'reb', 'pra', 'ml'): return 'nba_' + st
        if st in ('spread', 'total'): return 'nba_side'
        return 'other'
    if sp == 'NFL':
        if st in ('recyds', 'rush', 'pass'): return 'nfl_yds'
        if st == 'atd': return 'nfl_td'
    return 'other'


sig = lambda z: 1 / (1 + math.exp(-max(-30, min(30, z))))
def logit(p): p = min(0.99, max(0.01, p)); return math.log(p / (1 - p))
fee = lambda k: 0.07 * k * (1 - k)          # Kalshi taker fee per $1 contract at price k (0-1)


def fit(rows, steps=3000, lr=0.05, lam=4.0):
    """rows: dicts with g (0-100), grp, y (0/1), k (0-100 or None). Gradient descent on mean Brier + L2 on group offsets."""
    a, b, off = 0.0, 1.0, {g: 0.0 for g in GROUPS}
    n = len(rows)
    for _ in range(steps):
        ga = gb = 0.0; go = {g: 0.0 for g in GROUPS}
        for r in rows:
            x = logit(r['g'] / 100); p = sig(a + b * x + off[r['grp']]); d = 2 * (p - r['y']) * p * (1 - p) / n
            ga += d; gb += d * x; go[r['grp']] += d
        a -= lr * 10 * ga; b -= lr * 10 * gb
        for g in GROUPS: off[g] -= lr * 10 * (go[g] + lam * off[g] / n)
    # market blend on rows with a Kalshi price
    km = [r for r in rows if r.get('k')]
    c, w1, w2 = 0.0, 0.5, 0.5
    for _ in range(steps):
        gc = g1 = g2 = 0.0; m = len(km) or 1
        for r in km:
            x1 = logit(sig(a + b * logit(r['g'] / 100) + off[r['grp']])); x2 = logit(r['k'] / 100)
            p = sig(c + w1 * x1 + w2 * x2); d = 2 * (p - r['y']) * p * (1 - p) / m
            gc += d; g1 += d * x1; g2 += d * x2
        c -= lr * 10 * gc; w1 -= lr * 10 * g1; w2 -= lr * 10 * g2
    return {'a': a, 'b': b, 'off': off, 'c': c, 'w1': w1, 'w2': w2, 'n': n, 'nk': len(km)}


def p_cal(W, g, grp): return sig(W['a'] + W['b'] * logit(g / 100) + W['off'].get(grp, 0.0))


def true_chance(W, g, grp, k=None):
    """g: raw grade 0-100, k: Kalshi price 0-100 or None. Returns 0-1."""
    pc = p_cal(W, g, grp)
    return pc if not k else sig(W['c'] + W['w1'] * logit(pc) + W['w2'] * logit(k / 100))


def ev(p, k):
    """Expected profit per $1 spent on a Kalshi contract priced k (0-100) when the true chance is p (0-1)."""
    if not k: return None
    c = k / 100; return p / (c + fee(c)) - 1


def ticket_ev(ps, pay):
    """ps: true chances of independent legs, pay: total payout multiple (stake included). Same-game legs are not independent."""
    h = 1.0
    for p in ps: h *= p
    return h * pay - 1, h


def fit_kalshi(rows, steps=1500):
    """Kalshi price recalibrated on our legs: p = sigmoid(c + w*logit(price)). w > 1 means favorites hit more than their price."""
    km = [r for r in rows if r.get('k')]; c, w = 0.0, 1.0
    for _ in range(steps):
        gc = gw = 0.0
        for r in km:
            x = logit(r['k'] / 100); p = sig(c + w * x); d = 2 * (p - r['y']) * p * (1 - p) / len(km); gc += d; gw += d * x
        c -= 0.5 * gc; w -= 0.5 * gw
    return {'c': c, 'w': w, 'n': len(km)}


def fav_chance(K, k):
    """True chance of a leg priced k (0-100) under the favorite-edge model."""
    return sig(K['c'] + K['w'] * logit(k / 100))


# Ticket mode (Ace, Nov 20): 'favorite' builds tickets from 80-92c legs our grade agrees with, tracked flat $1 from
# Nov 21; it switches itself to 'pass' once 60+ forward legs show a loss, until sharp-book odds give a real EV source.
FAV_LO, FAV_HI, MODE_START, MODE_MIN_LEGS = 80, 92, datetime.date(2026, 11, 21), 60


def load(path=os.path.join(ROOT, 'calib.json')):
    return json.load(open(path))


def _rows():
    L = [l for l in json.load(open(os.path.join(ROOT, 'record.json')))['legs'] if l['res'] in ('W', 'L') and l.get('g')]
    for l in L:
        l['grp'] = group(l['sp'], l['st']); l['y'] = 1 if l['res'] == 'W' else 0
        l['date'] = datetime.datetime.strptime(l['d'] + ' 2026', '%b %d %Y').date()
    return L


if __name__ == '__main__':
    L = _rows(); days = sorted({l['date'] for l in L})
    br = lambda ps, ys: sum((p - y) ** 2 for p, y in zip(ps, ys)) / len(ys)
    out = {'raw': [], 'cal': [], 'kal': [], 'true': [], 'y': [], 'rawk': [], 'yk': [], 'calk': []}
    for d in days[4:]:                      # walk-forward: fit on every night before d, score night d
        W = fit([l for l in L if l['date'] < d], steps=1200)
        for l in (x for x in L if x['date'] == d):
            out['raw'].append(l['g'] / 100); out['cal'].append(p_cal(W, l['g'], l['grp'])); out['y'].append(l['y'])
            if l.get('k'):
                out['rawk'].append(l['g'] / 100); out['calk'].append(p_cal(W, l['g'], l['grp']))
                out['kal'].append(l['k'] / 100); out['true'].append(true_chance(W, l['g'], l['grp'], l['k'])); out['yk'].append(l['y'])
    rep = {'all_legs': {'n': len(out['y']), 'raw_grade': round(br(out['raw'], out['y']), 4), 'calibrated': round(br(out['cal'], out['y']), 4)},
           'priced_legs': {'n': len(out['yk']), 'raw_grade': round(br(out['rawk'], out['yk']), 4), 'calibrated': round(br(out['calk'], out['yk']), 4),
                           'kalshi': round(br(out['kal'], out['yk']), 4), 'true_blend': round(br(out['true'], out['yk']), 4)},
           'scored_from': str(days[4]), 'through': str(days[-1])}
    W = fit(L); K = fit_kalshi(L)
    # forward record of the favorite-edge legs since the mode started (flat $1 singles at the logged price, after fees)
    fw = [l for l in L if l['date'] >= MODE_START and l.get('k') and FAV_LO <= l['k'] <= FAV_HI and l['g'] >= 75 and l['g'] - l['k'] < 8]
    cost = sum(l['k'] / 100 + fee(l['k'] / 100) for l in fw); roi = (sum(l['y'] for l in fw) - cost) / cost if fw else None
    mode = 'pass' if (len(fw) >= MODE_MIN_LEGS and roi is not None and roi < 0) else 'favorite'
    json.dump({'built': str(datetime.date.today()), 'walk_forward_brier': rep, 'weights': W, 'kalshi': K,
               'mode': mode, 'forward': {'since': str(MODE_START), 'legs': len(fw), 'wins': sum(l['y'] for l in fw), 'roi': None if roi is None else round(100 * roi, 1)}},
              open(os.path.join(ROOT, 'calib.json'), 'w'), indent=1)
    print('mode', mode, 'kalshi recal', K)
    print(json.dumps(rep, indent=1))
    print('weights', {k: (round(v, 3) if isinstance(v, float) else v) for k, v in W.items() if k != 'off'})
    print('group offsets', {g: round(v, 3) for g, v in W['off'].items()})
    for g, grp in [(70, 'nba_pts'), (80, 'nba_pts'), (88, 'nba_pts'), (80, 'nba_ast'), (80, 'nba_reb'), (80, 'college'), (85, 'nba_3pm')]:
        print(g, grp, 'calibrated', round(100 * p_cal(W, g, grp), 1), '| with Kalshi 80:', round(100 * true_chance(W, g, grp, 80), 1))
