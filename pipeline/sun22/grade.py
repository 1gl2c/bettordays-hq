"""Our system grade for every Nov 22 leg (computed before the AI numbers are merged).
Player props: this season's game log (hit rate, last 5, and a normal or Poisson curve around the average), the same model the
NFL Sundays have used since Nov 9 (sun/grade.py), shrunk toward 65 and capped (NFL 85, rookies 80, anytime TD 62, 2+ TD 30).
Sides and totals: the betting spread and total turned into a chance with an NFL margin spread of 13.5 points and a total spread of 13.
Tennis and NHL: no system grade (the AIs and Kalshi only). Usage: python3 sun22/grade.py -> sun22/sun22.json"""
import json, math, re, statistics as S
L = json.load(open('sun22/logs.json')); LEGS = json.load(open('sun22/legs.json')); KM = json.load(open('sun22/kmatch.json'))
TM = json.load(open('sun22/teams.json'))
phi = lambda z: 0.5 * (1 + math.erf(z / math.sqrt(2)))
# ESPN lines at 9:00 AM PT (favorite, spread, total)
LINE = {'MIA@BUF': ('BUF', 16.5, 45.5), 'NO@CHI': ('CHI', 11.5, 47.5), 'TEN@DAL': ('DAL', 7.5, 54.5), 'TB@DET': ('DET', 3.5, 48.5), 'ARI@KC': ('KC', 15.5, 40.5),
        'PIT@PHI': ('PIT', 3.5, 37.5), 'BAL@CAR': ('CAR', 2.5, 44.5), 'NYJ@LAC': ('LAC', 3, 43.5), 'LV@DEN': ('DEN', 10.5, 40.5), 'JAX@NYG': ('JAX', 6, 45.5), 'MIN v SF': ('SF', 3.5, 46.5)}
NICK = {'Bears': 'CHI', 'Lions': 'DET', 'Jaguars': 'JAX', 'Eagles': 'PHI', 'Ravens': 'BAL', 'Buccaneers': 'TB', 'Chargers': 'LAC', 'Giants': 'NYG', 'Steelers': 'PIT', 'Panthers': 'CAR',
        'Raiders': 'LV', 'Bills': 'BUF', 'Broncos': 'DEN', '49ers': 'SF', 'Vikings': 'MIN', 'Chiefs': 'KC', 'Cowboys': 'DAL'}
ROOK = {'Jordyn Tyson', 'Fernando Mendoza', 'Carnell Tate', 'Emmett Johnson', 'Jonah Coleman', 'Malachi Fields', 'Caleb Douglas', 'Kyle Monangai'}
OUT = {n for n, v in TM.items() if v and 'Out' in (v.get('inj') or [])}
NBA = {'threes': 'threePointFieldGoalsMade-threePointFieldGoalsAttempted', 'rebounds': 'totalRebounds'}
def f(x, k):
    v = x.get(k, 0)
    if isinstance(v, str): v = v.split('-')[0]
    try: return float(v)
    except Exception: return 0.0
def vals(p, stat):
    g = L[p]['games']
    if stat == 'td': return [f(x, 'rushingTouchdowns') + f(x, 'receivingTouchdowns') + (f(x, 'passingTouchdowns') * 0 if True else 0) for x in g]
    if stat == 'rr': return [f(x, 'rushingYards') + f(x, 'receivingYards') for x in g]
    return [f(x, stat) for x in g]
def prob(p, stat, k, nfl=True):
    v = vals(p, stat); n = len(v); mu = S.mean(v)
    count = stat in ('receptions', 'td', 'interceptions', 'rushingAttempts', 'longReception', 'longRushing') or not nfl
    if count and stat not in ('longReception', 'longRushing'):
        lam = max(mu, 0.05); pn = 1 - sum(math.exp(-lam) * lam ** i / math.factorial(i) for i in range(int(k)))
    else:
        sd = max(S.pstdev(v), 0.35 * mu + 5); pn = 1 - phi((k - 0.5 - mu) / sd)
    hs = sum(x >= k for x in v); h5 = sum(x >= k for x in v[:5]); m5 = min(5, n)
    ps = (hs + 2 * pn) / (n + 2); p5 = (h5 + 2 * ps) / (m5 + 2)
    return 0.6 * ps + 0.4 * p5, (mu, hs, n, h5, m5)
STAT = [('rushing + receiving', 'rr'), ('receiving yards', 'receivingYards'), ('receptions', 'receptions'), ('rushing yards', 'rushingYards'), ('rushing attempts', 'rushingAttempts'),
        ('passing yards', 'passingYards'), ('interceptions', 'interceptions'), ('longest reception', 'longReception'), ('longest rush', 'longRushing'), ('touchdown', 'td'),
        ('threes', 'threes'), ('rebounds', 'rebounds')]
rows = []
for i, l in enumerate(LEGS, 1):
    p = l['p']; t = p.lower(); r = dict(i=i, p=p, sp=l['sp'], g=l['g'], t=l['t'], mkt=l['mkt'], k=KM[str(i)]['k'], ev=KM[str(i)]['ev'], sys=None, n='')
    if l['sp'] in ('TENNIS', 'NHL') or (l['sp'] == 'NBA' and ' ML ' in p): r['ty'] = 'ml'; rows.append(r); continue
    if ' ML ' in p or l['mkt'] in ('spread', '1h spread') or 'total points' in t or 'team total' in t:
        fav, sp, tot = LINE[l['g']]
        team = NICK.get(p.split(' ')[0])
        if 'total points' in t:
            mm = re.search(r'(over|under) (\d+(?:\.5)?)', t); x = float(mm.group(2)); z = (tot - x) / 13.0
            pr = phi(z) if mm.group(1) == 'over' else 1 - phi(z)
            if x == int(x): pr -= 0.02   # a push on a whole number is not a win
            r.update(ty='total', sys=round(100 * pr), n=f'Book total {tot}.')
        elif 'team total' in t:
            exp = tot / 2 + sp / 2; x = float(re.search(r'over (\d+\.5)', t).group(1)); pr = 1 - phi((x - exp) / 9.5)
            r.update(ty='total', sys=round(100 * pr), n=f'Implied {exp:.1f} points from the {sp}-point spread and {tot} total.')
        else:
            exp = sp if team == fav else -sp     # expected margin for this team
            if 'first half' in t: exp, sd = exp / 2, 9.5
            else: sd = 13.5
            if ' ML ' in p: pr = phi(exp / sd); r['ty'] = 'ml'
            else:
                line = float(re.search(r'([+-]\d+(?:\.5)?)', p).group(1)); pr = phi((exp + line) / sd); r['ty'] = 'spread'
                if line == int(line): pr -= 0.02
            r.update(sys=round(100 * pr), n=f"Book line {fav} -{sp}.")
        rows.append(r); continue
    name = re.split(r' (?:\d|under|anytime)', p)[0]
    lp = next((n for n in L if n == name or L[n].get('disp') == name), None)
    st = next((v for kk, v in STAT if kk in t), None)
    r['ty'] = 'prop'
    if name in OUT or (lp and lp in OUT): r.update(sys=0, n='OUT', fl='OUT'); rows.append(r); continue
    if not lp or not st: rows.append(r); continue
    under = ' under ' in t
    if 'longest' in t: k = int(float(re.search(r'(\d+\.5)', t).group(1)) + 0.5)
    elif 'anytime' in t: k = 1
    else:
        mm = re.search(r'(\d+)\+', p); un = re.search(r'under (\d+(?:\.5)?)', t)
        k = int(mm.group(1)) if mm else int(float(un.group(1)) + 0.5)
    nba = l['sp'] == 'NBA'
    pr, (mu, hs, n, h5, m5) = prob(lp, NBA.get(st, st) if nba else st, k, nfl=not nba)
    if under: pr = 1 - pr; hs = n - hs; h5 = m5 - h5
    pct = 0.8 * 100 * pr + 0.2 * 65
    cap = 88 if nba else 85
    if lp in ROOK: cap = min(cap, 80)
    if st == 'td': cap = 62 if k == 1 else 30
    pct = max(3, min(round(pct), cap))
    r.update(sys=pct, n=(f"Scored in {hs} of {n} games, {h5} of {m5} last 5." if st == 'td' else f"{'Stayed under' if under else 'Hit'} {hs} of {n} this season, {h5} of {m5} last 5 (avg {mu:.1f})."))
    rows.append(r)
json.dump({'rows': rows}, open('sun22/sun22.json', 'w'), indent=1)
for r in rows: print(r['i'], r['sys'], r['k'], r['p'], '|', r['n'][:70])
