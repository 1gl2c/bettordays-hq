"""Engine v7 rules (docs/DAILY_ENGINE_V7.md), in one place so merge, publish and tests share them."""
import re, statistics, itertools

GAP_REMOVE = 8      # median 8+ above Kalshi -> REMOVED (market disagrees)
CAP_OVER_K = 7      # published grade never above Kalshi + 7
NO_K_MAX = 75       # no Kalshi price: max published grade
BOARD_MIN = 70      # board shows GREEN and YELLOW legs at 70+
HAM_MIN = 75        # Hammer legs published 75+
HAM_WITHIN = 3      # Hammer legs GREEN or within 3 of Kalshi
MIN_MODELS = 2      # a leg needs at least 2 model numbers to get a v7 grade
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


def hammer(legs):
    """v7 Hammer: 3 to 5 legs, each GREEN or within 3 of Kalshi, published 75+, strong market,
    no two from the same game, no back-to-backs, no Ace-rule legs, pays 2x or more (Ace's rule).
    Returns (ticket_legs, reason_if_none)."""
    ok = [l for l in legs if l['pub'] is not None and l['pub'] >= HAM_MIN and l.get('k') is not None
          and l['k'] >= l['pub'] - HAM_WITHIN and ticket_ok(l)]
    ok.sort(key=lambda l: (-l['pub'], -l['k']))
    pick, games, players = [], set(), set()
    for l in ok:
        if l['g'] in games or l['player'] in players: continue
        pick.append(l); games.add(l['g']); players.add(l['player'])
        pay = payout(pick)
        if len(pick) >= 3 and pay >= 2: break
        if len(pick) == 5: break
    if len(pick) < 3:
        return None, f"Only {len(pick)} leg{'s' if len(pick)!=1 else ''} qualif{'y' if len(pick)!=1 else 'ies'} (GREEN or within 3 of Kalshi, 75+, points, assists, threes or NBA favorite moneylines, different games, no back-to-backs, models within 12 points). Passing is a win."
    pay = payout(pick)
    if pay < 2:
        return None, f"The best {len(pick)} qualifying legs pay only {pay:.2f}x at Kalshi's prices, under the 2x minimum. Passing is a win."
    return pick, None


def perfect(legs):
    """Safe / Core / Stretch from GREEN legs only, one leg per game and player.
    Chooses the combo with the highest product of published grades inside each payout window."""
    g = [l for l in legs if l['tier'] == 'G' and l['pub'] is not None and l.get('k') is not None and ticket_ok(l)]
    g.sort(key=lambda l: -l['pub']); g = g[:22]
    spec = [('Safe', (2, 2), (2.0, 2.5)), ('Core', (3, 4), (2.5, 4.0)), ('Stretch', (4, 5), (4.0, 99))]
    out = []   # only points, assists, threes and NBA favorite MLs since the Nov 20 audit (rebound parlays were a loss by our own grades)
    for name, (lo, hi), (pmin, pmax) in spec:
        best = None
        for n in range(lo, hi + 1):
            for c in itertools.combinations(g, n):
                if len({l['g'] for l in c}) < n or len({l['player'] for l in c}) < n: continue
                pay = payout(c)
                if pay is None or not (pmin <= pay <= pmax): continue
                prob = 1
                for l in c: prob *= l['pub'] / 100
                if best is None or prob > best[0]: best = (prob, c, pay)
        out.append({'name': name, 'legs': [l['i'] for l in best[1]] if best else [], 'pay': round(best[2], 2) if best else None,
                    'hit': round(100 * best[0]) if best else None,
                    'none': None if best else f"Not enough GREEN legs at 70+ from different games to reach {pmin:g}x" + (" or more." if pmax >= 99 else f" to {pmax:g}x.")})
    return out


def player_of(p):
    m = re.match(r"(.+?) (?:\d+\+|under|over|anytime|ML|[+-]\d)", p)
    return (m.group(1) if m else p).strip()
