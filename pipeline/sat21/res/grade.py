"""Grade every Nov 21 leg from ESPN box scores and finals (NBA, CFB, CBB) and the UFC card.
Usage (from pipeline/): python3 sat21/res/grade.py  ->  sat21/sat21_graded.json"""
import json, re, unicodedata
D = json.load(open('sat21/res/all.json')); G = D['games']
nrm = lambda s: unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode().lower().replace('.', '').replace("'", '')
P = {}
for b in D['box'].values():
    for n, v in b.items(): P[nrm(n)] = v
J = json.load(open('sat21/sat21.json')); S = J['rows']
TEAM = {'76ers': 'PHI', 'Knicks': 'NY', 'Timberwolves': 'MIN', 'Celtics': 'BOS', 'Nicholls': 'NICH', 'Wofford': 'WOF', 'Southern Illinois': 'SIU',
        'Army': 'ARMY', 'Ohio State': 'OSU', 'West Virginia': 'WVU', 'UAB': 'UAB', 'Oklahoma State': 'OKST', 'Oklahoma': 'OU', 'Houston': 'HOU',
        'Indiana': 'IU', 'UCLA': 'UCLA', 'Cincinnati': 'CIN', 'Wake Forest': 'WAKE', 'Kansas': 'KU'}
# UFC card (ESPN scoreboard + UFC results): winner and method for the two method legs
U = json.load(open('sat21/res/ufc.json')); WIN = set()
for e in U['events']:
    for c in e['competitions']:
        for x in c['competitors']:
            if x.get('winner'): WIN.add(nrm(x['athlete']['displayName']))
METHOD = {'ikram aliskerov': 'decision', 'tahir abdullayev': 'decision'}   # ufcalendar.com: Aliskerov UD 30-27 x3; Abdullayev UD
def gkey(g):
    tg = set(x.strip() for x in re.split(r'@| v ', g))
    return next((k for k in G if set(G[k]['sc']) == tg and G[k]['lg'] != 'nba' or (set(G[k]['sc']) == tg)), None)
def num(v):
    try: return float(str(v).split('/')[0].split('-')[0])
    except Exception: return 0.0
def find(p):
    k = nrm(p); c = [n for n in P if k.startswith(n)] or [n for n in P if k.startswith(n.replace(' jr', '').replace(' iii', '').replace(' ii', ''))]
    return (max(c, key=len), P[max(c, key=len)]) if c else (None, None)
miss = []
for r in S:
    p = r['p']; t = p.lower(); r.pop('r', None); r.pop('act', None)
    if r['sp'] == 'UFC':
        f = nrm(p.split(' ML')[0].split(' wins')[0])
        won = f in WIN
        if 'by decision' in t: won = won and METHOD.get(f) == 'decision'; r['act'] = ('won by decision' if won else ('won, not by decision' if f in WIN else 'lost'))
        else: r['act'] = 'won' if won else 'lost'
        r['r'] = 'W' if won else 'L'; continue
    k = gkey(r['g'])
    if r['ty'] == 'total':
        g = G[k]; v = sum(g['sc'].values()); m = re.search(r'(over|under) (\d+(?:\.5)?)', p); n = float(m.group(2))
        r['r'] = 'P' if v == n else ('W' if (v > n) == (m.group(1) == 'over') else 'L'); r['act'] = f'{v} total'; continue
    if r['ty'] in ('ml', 'spread'):
        g = G.get(k); tm = next((a for n, a in sorted(TEAM.items(), key=lambda x: -len(x[0])) if p.startswith(n)), None)
        if not tm or not g: miss.append(p); continue
        opp = [x for x in g['sc'] if x != tm][0]; mar = g['sc'][tm] - g['sc'][opp]
        if r['ty'] == 'ml': hit = mar > 0; r['act'] = f"{'Won' if hit else 'Lost'} {g['sc'][tm]}-{g['sc'][opp]}"
        else:
            sp = float(re.search(r'([+-]\d+(?:\.5)?)', p).group(1)); r['act'] = f"{'Won' if mar > 0 else 'Lost'} by {abs(mar)}"
            if mar + sp == 0: r['r'] = 'P'; continue
            hit = mar + sp > 0
        r['r'] = 'W' if hit else 'L'; continue
    n, s = find(p)
    if s is None:
        if r['sp'] == 'NBA' and k and D['box'].get(k): r['r'] = 'V'; r['act'] = 'did not play'; continue   # not in the box score: void
        miss.append(p); continue
    rest = t[len(n):] if t.startswith(n) else t
    if 'rebounds + assists' in t: v = num(s.get('rebounds')) + num(s.get('assists'))
    elif 'passing' in t: v = num(s.get('passing.passingYards'))
    elif 'rushing' in t: v = num(s.get('rushing.rushingYards'))
    elif 'receiving' in t: v = num(s.get('receiving.receivingYards'))
    elif 'assist' in t: v = num(s.get('assists'))
    elif 'rebound' in t: v = num(s.get('rebounds'))
    elif 'point' in t: v = num(s.get('points'))
    else: miss.append(p); continue
    if s.get('dnp') and 'points' not in s and not any(kk.startswith(('passing', 'rushing', 'receiving')) for kk in s): r['r'] = 'V'; r['act'] = 'DNP'; continue
    x = float(re.search(r'(\d+(?:\.5)?)', rest).group(1))
    hit = v < x if 'under' in t else v >= x
    r['r'] = 'W' if hit else 'L'; r['act'] = int(v)
json.dump(J, open('sat21/sat21_graded.json', 'w'))
print('MISSING', miss)
for r in S: print(r.get('r'), r['p'], '->', r.get('act'))
