"""Kalshi page links for every leg (Nov 22). Kalshi market pages follow
https://kalshi.com/markets/<series ticker>/<series title slug>/<event ticker>, all lower case
(e.g. kalshi.com/markets/kxnbagame/nba-game/kxnbagame-26apr09bosnyk). The slug comes from the series title in Kalshi's
public API, cached in kalshi_series.json so each series is looked up once.
Usage: from kalshi_links import link; link('KXNBAPTS-26NOV21LACDAL')  ->  url or None"""
import json, os, re, subprocess
CACHE = os.path.join(os.path.dirname(__file__), 'kalshi_series.json')
_C = json.load(open(CACHE)) if os.path.exists(CACHE) else {}
REF_URL = 'https://kalshi.com/r/27715b4c-2e36-431e-a6e4-18391eba78c0'   # Ace's Kalshi referral link (Nov 22): used on 'Join Kalshi' buttons, not on market links


def slug(t): return re.sub(r'[^a-z0-9]+', '-', t.lower()).strip('-')


def title(series):
    if series not in _C:
        r = subprocess.run(['curl', '-s', '-m', '20', f'https://api.elections.kalshi.com/trade-api/v2/series/{series}'], capture_output=True, text=True).stdout
        try: _C[series] = json.loads(r)['series']['title']
        except Exception: return None
        json.dump(_C, open(CACHE, 'w'), indent=1)
    return _C[series]


def link(event_ticker):
    if not event_ticker: return None
    series = event_ticker.split('-')[0]
    t = title(series)
    if not t: return None
    u = f'https://kalshi.com/markets/{series.lower()}/{slug(t)}/{event_ticker.lower()}'
    return u


if __name__ == '__main__':
    for e in ['KXNBAGAME-26NOV21BOSSAC', 'KXNBAPTS-26NOV21LACDAL', 'KXNBAAST-26NOV21LACDAL', 'KXNBAREB-26NOV21MILPHI']: print(link(e))
