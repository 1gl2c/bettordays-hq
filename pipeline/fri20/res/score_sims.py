"""Grade tonight's simulation lines (agent sims V8SIM and our Beta Top) from ESPN box scores."""
import json, re, unicodedata
B = json.load(open('fri20/res/all.json'))['box']
def nm(n): n = unicodedata.normalize('NFKD', n).encode('ascii', 'ignore').decode().lower(); return re.sub(r'[^a-z]', '', re.sub(r'\b(jr|sr|ii|iii|iv)\b', '', n))
P = {}
for b in B.values():
    for n, v in b.items(): P[nm(n)] = v
def num(v):
    try: return float(str(v).split('/')[0].split('-')[0])
    except Exception: return 0.0
def val(player, st):
    s = P.get(nm(player))
    if not s or (s.get('dnp') and 'points' not in s): return None
    pts, reb, ast, tpm = num(s.get('points')), num(s.get('rebounds')), num(s.get('assists')), num(s.get('threePointFieldGoalsMade-threePointFieldGoalsAttempted'))
    return {'pts': pts, 'reb': reb, 'ast': ast, '3pm': tpm, 'pra': pts + reb + ast, 'pr': pts + reb, 'pa': pts + ast, 'ra': reb + ast}.get(st)
def grade(player, st, k):
    v = val(player, st)
    return (None, None) if v is None else ('W' if v >= k else 'L', int(v))
if __name__ == '__main__':
    print(grade('Sam Merrill', 'pra', 10), grade('Kyshawn George', 'pra', 25))
