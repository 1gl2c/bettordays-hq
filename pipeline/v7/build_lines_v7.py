"""Make today's v7 candidate list for the Hermes runner.

Usage (from pipeline/):  python3 v7/build_lines_v7.py DAY_JSON DATE
  DAY_JSON: the graded board file from the usual grading scripts (e.g. fri/fri.json), with Kalshi prices in `k`.
  DATE: YYYY-MM-DD

Writes daily/DATE/v7_candidates.json (for the merge) and daily/DATE/v7_lines.txt + v7_slate.txt
(what the runner pastes into the prompt). Our own grade is NOT in the lines file, so the models stay blind to it.
Legs that are void (player out) are left out.
"""
import json, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from v7lib import stat_of, ace_rule, player_of

src, day = sys.argv[1], sys.argv[2]
D = json.load(open(src)); rows = D['rows'] if isinstance(D, dict) else D
out = f'daily/{day}'; os.makedirs(out, exist_ok=True)
C, lines, games = [], [], {}
for r in rows:
    if r.get('fl') in ('OUT', 'VOID') or r.get('void'):
        continue
    i = len(C) + 1
    leg = {'i': i, 'p': r['p'], 'player': player_of(r['p']), 'g': r['g'], 't': r['t'], 'sp': r['sp'], 'ty': r['ty'],
           'st': r.get('st'), 'stat': stat_of(r['p'], r['ty']), 'k': r.get('k'), 'b2b': bool(r.get('b2b')),
           'sys': r.get('pct'), 'n': r.get('n', ''), 'rule': ace_rule(r['p']), 'fl': r.get('fl')}
    C.append(leg)
    games.setdefault(r['g'], (r['sp'], r['t']))
    lines.append(f"{i} | {r['p']} | {r['sp']} {r['g']} {r['t']} PM PT | market: {leg['stat']} | Kalshi {leg['k'] if leg['k'] is not None else 'none'} | back-to-back: {'yes' if leg['b2b'] else 'no'}" + (' | line moved by us (no line given, or a safer rung)' if r.get('moved') else '') + (' | QUESTIONABLE, check status' if r.get('fl')=='Q' else ''))
json.dump({'date': day, 'legs': C}, open(f'{out}/v7_candidates.json', 'w'), indent=1)
open(f'{out}/v7_lines.txt', 'w').write('\n'.join(lines) + '\n')
slate = '; '.join(f"{sp} {g} {t} PM PT" for g, (sp, t) in sorted(games.items(), key=lambda x: x[1][1]))
open(f'{out}/v7_slate.txt', 'w').write(slate + '\n')
print(len(C), 'legs,', len(games), 'games ->', out)
