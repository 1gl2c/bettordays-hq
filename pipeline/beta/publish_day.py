"""Put tonight's beta sim (beta/run_day.py output) on the site source. Keeps the graded history (hist) untouched.
Usage (from pipeline/): python3 beta/publish_day.py 2026-11-27"""
import json, sys, datetime
DAY = sys.argv[1]; d = datetime.date.fromisoformat(DAY)
T = json.load(open(f"beta{d.strftime('%b').lower()}{d.day:02d}/beta_tonight.json"))
F = 'bettordays-hq.html'; s = open(F).read()
i = s.index('const BETA=') + len('const BETA='); B, e = json.JSONDecoder().raw_decode(s[i:])
assert B['sim_ts'] != T['sim_ts']
B.update({k: T[k] for k in ('sim_ts', 'ts', 'ts0', 'n_lines', 'n_games', 'top', 'all_pos', 'avg')})
s = s[:i] + json.dumps(B) + s[i + e:]
open(F, 'w').write(s)
print('BETA', DAY, len(T['top']), 'top lines from', T['n_lines'], 'in', T['n_games'], 'games')
