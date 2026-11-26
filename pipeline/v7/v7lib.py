"""Engine v7 rules (docs/DAILY_ENGINE_V7.md), in one place so merge, publish and tests share them."""
import re, statistics, itertools

GAP_REMOVE = 8      # median 8+ above Kalshi -> REMOVED (market disagrees)
CAP_OVER_K = 7      # published grade never above Kalshi + 7
NO_K_MAX = 75       # no Kalshi price: max published grade
BOARD_MIN = 70      # board shows GREEN and YELLOW legs at 70+
HAM_MIN = 75        # Hammer legs published 75+
HAM_WITHIN = 3      # Hammer legs GREEN or within 3 of Kalshi
MIN_MODELS = 2      # a leg needs at least 2 model numbers to get a v7 grade
MIN_PAY = 1.5       # Ace, Nov 20: the Hammer pays at least 1.5x after fees, so a miss never costs 6 wins
SAFE_PAY = 1.35     # if no 1.5x Hammer makes money, the best +EV ticket at 1.35x+ posts as the Safe Hammer
SPLIT_MAX = 12      # models 12+ points apart: the leg stays off the Hammer and the parlays (Nov 20 audit)


def cap_for(leg):
    """Highest grade a leg may ever publish, applied AFTER any model blend (Nov 20 audit: Oregon ML,
    system 69, was published at 87 because the v8 median skipped the cap)."""
    sp, ty, st = leg.get('sp'), leg.get('ty'), leg.get('stat')
    if sp in ('CFB', 'CBB', 'NCAAF', 'NCAAB'): return 69          # every college line and prop
    if sp == 'NBA' and ty in ('ml', 'spread'): return 88
    if sp == 'NBA' and ty == 'total': return 80
    if st == 'pra': return 80
    return 88


def stat_of(p, ty):
    """Market type from the pick text, same names as the site record."""
    t = p.lower()
    if ty in ('ml', 'spread', 'total'):
        return ty
    if 'touchdown' in t: return 'atd'
    if 'points + rebounds + assists' in t: return 'pra'
    if 'rushing + receiving' in t: return 'combo'
    if 'attempt' in t: return 'other'
    for k, v in [('three', '3pm'), ('assist', 'ast'), ('rebound', 'reb'), ('reception', 'rec'),
                 ('receiving y', 'recyds'), ('rushing y', 'rush'), ('passing y', 'pass'), ('point', 'pts')]:
        if k in t: return v
    return 'other'


def strong_market(leg):
    """v7 strong spots: points, assists, threes, moneylines (favorites only)."""
    st = leg['stat']
    if st in ('pts', 'ast', '3pm'):
        return True
    if st == 'ml':   # NBA favorites only: college moneylines went 24-16 (Nov 4-19)
        return leg.get('sp') == 'NBA' and leg.get('k') is not None and leg['k'] >= 50
    return False


def ticket_ok(l):
    """A leg may go on a published ticket: strong market, no rule, not void, not a back-to-back, models not split."""
    return (strong_market(l) and not l.get('b2b') and not l.get('rule') and not l.get('void')
            and (l.get('spread') is None or l['spread'] < SPLIT_MAX))


def ace_rule(p):
    t = p.lower()
    if 'harden' in t: return 'Never James Harden'
    if 'under' in t and ('wembanyama' in t or 'doncic' in t or 'luka' in t): return 'No unders on Wemby or Luka'
    return None


def tier(pub_med, k):
    if k is None: return 'N'
    gap = pub_med - k
    if gap >= GAP_REMOVE: return 'R'
    if gap > 0: return 'Y'
    return 'G'


def grade_leg(nums, k):
    """nums: model numbers. Returns (median, tier, published) or None if too few numbers."""
    nums = [n for n in nums if n is not None]
    if len(nums) < MIN_MODELS:
        return None
    med = round(statistics.median(nums))
    t = tier(med, k)
    if t == 'N':
        pub = min(med, NO_K_MAX)
    elif t == 'R':
        pub = None
    else:
        pub = min(med, k + CAP_OVER_K)
    return med, t, pub


def payout(legs):
    """1 / product of Kalshi prices (before fees). None if any leg has no price."""
    p = 1.0
    for l in legs:
        if l.get('k') is None: return None
        p *= max(1, min(99, l['k'])) / 100
    return 1 / p


def _calib():
    """Calibration weights and ticket mode from calib.json (built daily by pipeline/calib.py)."""
    import sys, os
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
    import calib
    return calib, calib.load()


def edge_pool(legs):
    """Favorite-edge legs (Ace, Nov 20): Kalshi 80-92c, our grade 75+ and not 8+ above Kalshi, clean flags, models within 12.
    Each gets p_true (calibrated favorite curve) and ev (per $1 after Kalshi fees)."""
    C, D = _calib()
    out = []
    for l in legs:
        k = l.get('k')
        if k is None or not (C.FAV_LO <= k <= C.FAV_HI) or l.get('pub') is None or l['pub'] < 75 or l.get('tier') not in ('G', 'Y'): continue
        if l.get('b2b') or l.get('rule') or l.get('void') or (l.get('spread') is not None and l['spread'] >= SPLIT_MAX): continue
        p = C.fav_chance(D['kalshi'], k)
        out.append(dict(l, p_true=round(p, 4), ev=round(C.ev(p, k), 4)))
    out.sort(key=lambda l: (-l['p_true'], -l['ev']))
    return out, C, D


def _combo_stats(c, C):
    hit, cost = 1.0, 1.0
    for l in c:
        hit *= l['p_true']; q = l['k'] / 100; cost *= q + C.fee(q)
    return hit, 1 / cost, hit / cost - 1     # hit chance, payout after fees, EV per $1


def _best(pool, C, sizes, min_hit, key, min_pay=MIN_PAY):
    best = None
    for n in sizes:
        for c in itertools.combinations(pool[:24 if n <= 3 else 16], n):   # ChatGPT audit: search more than the first 14 legs
            if len({l['g'] for l in c}) < n or len({l['player'] for l in c}) < n: continue
            hit, pay, e = _combo_stats(c, C)
            if e < 0.02 or hit < min_hit or pay < min_pay: continue
            sc = key(hit, e)
            if best is None or sc > best[0]: best = (sc, c, hit, pay, e)
    return best


def hammer(legs):
    """EV Hammer (replaces the 2x minimum, Ace Nov 20): 2 to 5 favorite-edge legs from different games paying 1.5x+
    after fees, the highest hit chance whose expected value after Kalshi fees is at least +2%. Returns (legs, reason)."""
    pool, C, D = edge_pool(legs)
    import json as _j, os as _o   # Nov 25 rule (learn/hammer_rules.json): NBA legs only unless the NFL stat group has earned 'prefer'
    R = _j.load(open('learn/hammer_rules.json')) if _o.path.exists('learn/hammer_rules.json') else {}
    if R.get('nba_only'):
        HL = _j.load(open('learn/hammer_learn.json')) if _o.path.exists('learn/hammer_learn.json') else {}
        ok = {g['group'] for g in HL.get('groups', []) if isinstance(g, dict) and g.get('level') == 'sport' and g.get('status') == 'prefer'}
        pool = [l for l in pool if l.get('sp') == 'NBA' or l.get('sp') in ok]
    if D.get('mode') == 'pass':
        f = D.get('forward', {})
        return None, f"Pass mode: the favorite-edge tickets lost money over {f.get('legs')} tracked legs ({f.get('roi')}% after fees), so we only post tickets again once sharp-book prices show a real edge."
    b = _best(pool, C, (2, 3, 4, 5), 0.45, lambda h, e: (round(h, 3), e)); kind = 'Hammer'
    if not b:   # Ace, Nov 20: don't pass on a money-making ticket just because it pays 1.35x to 1.5x
        b = _best(pool, C, (2, 3, 4), 0.6, lambda h, e: (round(h, 3), e), min_pay=SAFE_PAY); kind = 'Safe Hammer'
    if not b:
        return None, f"No 2 to 5 legs from different games priced 80-92 cents paid {SAFE_PAY}x or more after fees with a 45%+ hit chance and a profit by our math ({len(pool)} leg{'s' if len(pool) != 1 else ''} qualified). Passing is a win."
    for l in b[1]: l['_ham'] = (round(100 * b[2]), round(b[3], 2), round(100 * b[4], 1), kind)
    return list(b[1]), None


def perfect(legs):
    """Safe / Core / Stretch from favorite-edge legs, one leg per game and player, each +2% EV or better after fees.
    Safe: 2 legs, highest hit chance. Core: 3 legs, highest EV with 45%+ hit. Stretch: 4-5 legs, highest EV with 30%+ hit."""
    pool, C, D = edge_pool(legs)
    spec = [('Safe', (2, 3), 0.55, lambda h, e: (h, e)), ('Core', (3, 4), 0.4, lambda h, e: (e, h)), ('Stretch', (4, 5), 0.3, lambda h, e: (e, h))]
    out = []
    for name, sizes, mh, key in spec:
        b = None if D.get('mode') == 'pass' else _best(pool, C, sizes, mh, key)
        out.append({'name': name, 'legs': [l['i'] for l in b[1]] if b else [], 'pay': round(b[3], 2) if b else None,
                    'hit': round(100 * b[2]) if b else None, 'ev': round(100 * b[4], 1) if b else None,
                    'none': None if b else ('Pass mode until sharp-book prices are live.' if D.get('mode') == 'pass' else
                                            f"No {'-'.join(map(str, sizes))}-leg combo from different games made +2% after fees at a {round(100*mh)}%+ hit chance.")})
    return out


LOTTO_PAY = (5.0, 10.0)   # Ace, Nov 22: the best 5-10x ticket, built like the Hammer, never forced
LOTTO_MAX_LEGS = 8


def lotto_pool(legs):
    """Lotto legs: every favorite-edge leg, plus legs priced 50-79 cents where BOTH our grade and the sportsbooks' no-vig
    price sit 4+ above Kalshi (two independent sources agree the price is cheap). Chance for those = the average of
    the books and Kalshi, so the edge we count is half of what the books see."""
    pool, C, D = edge_pool(legs)
    seen = {l['i'] for l in pool}
    for l in legs:
        k, bk, pub = l.get('k'), l.get('bk'), l.get('pub')
        if l['i'] in seen or k is None or bk is None or pub is None or not (50 <= k < C.FAV_LO): continue
        if l.get('tier') not in ('G', 'Y') or l.get('rule') or l.get('void') or l.get('fl') or (l.get('spread') is not None and l['spread'] >= SPLIT_MAX): continue
        if pub - k < 4 or bk - k < 4: continue
        p = (bk + k) / 200
        pool.append(dict(l, p_true=round(p, 4), ev=round(C.ev(p, k), 4)))
    pool.sort(key=lambda l: (-l['ev'], -l['p_true']))
    return pool, C, D


def lotto(legs):
    """The best 5-10x ticket after fees: 3 to 8 legs from different games and players, expected value +5% or better by our
    math, highest hit chance among those. Returns (ticket dict or None, reason)."""
    pool, C, D = lotto_pool(legs)
    if D.get('mode') == 'pass': return None, 'Pass mode: favorite-edge tickets are off until the forward record turns positive.'
    best = None
    for n in range(3, LOTTO_MAX_LEGS + 1):
        top = pool[:16 if n <= 5 else 13]
        for c in itertools.combinations(top, n):
            if len({l['g'] for l in c}) < n or len({l['player'] for l in c}) < n: continue
            hit, pay, e = _combo_stats(c, C)
            if not (LOTTO_PAY[0] <= pay <= LOTTO_PAY[1]) or e < 0.05: continue
            sc = (round(hit, 3), e, -n)
            if best is None or sc > best[0]: best = (sc, c, hit, pay, e)
    if not best:
        return None, f"No 3 to {LOTTO_MAX_LEGS} legs from different games paid 5-10x after fees with +5% or better by our math ({len(pool)} legs qualified). No lotto beats a forced lotto."
    return {'legs': [l['i'] for l in best[1]], 'pay_net': round(best[3], 2), 'hit': round(100 * best[2], 1), 'ev': round(100 * best[4], 1)}, None


def master_v2(l):
    """Master filter v2 (Nov 22, from the record): NBA overs on points, assists or threes, our grade 70+, Kalshi 80+ and at or
    above our grade, no flags. Nov 4-21: 55-3 (95%), +11% as $1 singles after fees. Tracked forward from Nov 22."""
    st = l.get('stat') or ''
    return (l.get('sp') == 'NBA' and l.get('ty') == 'prop' and ' under ' not in l['p'].lower() and st in ('pts', 'ast', '3pm')
            and (l.get('pub') or 0) >= 70 and l.get('k') is not None and l['k'] >= 80 and l['k'] >= l['pub'] and not l.get('fl') and not l.get('rule'))


def player_of(p):
    m = re.match(r"(.+?) (?:\d+\+|under|over|anytime|ML|[+-]\d)", p)
    return (m.group(1) if m else p).strip()
