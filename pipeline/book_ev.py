"""Sportsbook fair chance for any Kalshi rung, from the no-vig book consensus (Nov 20 EV engine, step 2).

Books post one main line per player (Over 22.5 points at a fair 51%). Kalshi sells rungs (20+, 25+).
We fit the player's distribution to the book's fair Over, then read off P(stat >= rung):
  threes, assists, rebounds: Poisson with the mean that matches the fair Over
  points: normal with sd = max(3.5, 0.33 * mean), mean solved the same way (continuity-corrected)
Then EV on Kalshi = fair / (Kalshi price + fee) - 1.

Input: rows from the Supabase view public.book_novig (market, player, line, books, fair_over), saved by the
daily run as daily/DATE/book_novig.json. Output: fair_rung(rows, player, stat, rung) -> (p, books) or None.
"""
import math, json, re, unicodedata

MARKET = {'pts': 'player_points', 'reb': 'player_rebounds', 'ast': 'player_assists', '3pm': 'player_threes'}


def norm_name(n):
    n = unicodedata.normalize('NFKD', n).encode('ascii', 'ignore').decode().lower()
    n = re.sub(r'\b(jr|sr|ii|iii|iv)\b\.?', '', n)
    return re.sub(r'[^a-z]', '', n)


def pois_ge(lam, k):
    """P(X >= k) for Poisson(lam), k an integer >= 0."""
    if k <= 0: return 1.0
    term, cdf = math.exp(-lam), 0.0
    for i in range(k):
        cdf += term; term *= lam / (i + 1)
    return max(0.0, 1 - cdf)


def norm_ge(mu, sd, k):
    """P(X >= k) for a whole-number stat, continuity corrected."""
    return 0.5 * math.erfc((k - 0.5 - mu) / (sd * math.sqrt(2)))


def _solve(f, target, lo, hi):
    for _ in range(80):
        mid = (lo + hi) / 2
        if f(mid) < target: lo = mid
        else: hi = mid
    return (lo + hi) / 2


def fair_rung(rows, player, stat, rung):
    """rows: book_novig rows. stat: pts/reb/ast/3pm. rung: Kalshi 'N+' as an int. Returns (p, books, line) or None.
    Uses the book line with the most books (ties: closest to the rung)."""
    mk, pn = MARKET.get(stat), norm_name(player)
    cand = [r for r in rows if r['market'] == mk and norm_name(r['player']) == pn and r.get('fair_over') is not None]
    if not mk or not cand: return None
    r = sorted(cand, key=lambda r: (-int(r['books']), abs(float(r['line']) + 0.5 - rung)))[0]
    line, p = float(r['line']), float(r['fair_over'])
    need = math.floor(line) + 1                     # Over 22.5 means 23 or more
    if stat == 'pts':
        sdf = lambda mu: max(3.5, 0.33 * mu)
        mu = _solve(lambda m: norm_ge(m, sdf(m), need), p, 0.0, 80.0)
        q = norm_ge(mu, sdf(mu), rung)
    else:
        lam = _solve(lambda l: pois_ge(l, need), p, 0.0, 40.0)
        q = pois_ge(lam, rung)
    return round(q, 4), int(r['books']), line


def fee(q): return 0.07 * q * (1 - q)


def ev(p, k):
    """Expected profit per $1 at Kalshi price k (0-100) when the book fair chance is p (0-1)."""
    q = k / 100; return p / (q + fee(q)) - 1


if __name__ == '__main__':
    rows = [{'market': 'player_points', 'player': 'Deni Avdija', 'line': 22.5, 'books': 4, 'fair_over': 0.5119},
            {'market': 'player_threes', 'player': 'OG Anunoby', 'line': 1.5, 'books': 4, 'fair_over': 0.6009}]
    for pl, st, rg, k in [('Deni Avdija', 'pts', 15, 88), ('Deni Avdija', 'pts', 20, 70), ('Deni Avdija', 'pts', 25, 38), ('OG Anunoby', '3pm', 1, 85), ('OG Anunoby', '3pm', 3, 30)]:
        p, b, ln = fair_rung(rows, pl, st, rg)
        print(f'{pl} {rg}+ {st}: books say {100*p:.1f}% (from Over {ln}, {b} books) · Kalshi {k} -> EV {100*ev(p, k):+.1f}%')
