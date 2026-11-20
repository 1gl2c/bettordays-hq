"""Engine v7, Part B: merge the model replies and grade the board.

Usage (from pipeline/):  python3 v7/merge_v7.py DATE REPLIES_DIR
  DATE: YYYY-MM-DD (reads daily/DATE/v7_candidates.json)
  REPLIES_DIR: folder with the runner's replies (chatgpt.md, gemini.md, grok.md, claude.md)

Writes daily/DATE/v7_merged.json and prints a summary. Rules live in v7lib.py:
  median of the model numbers (2+ needed) -> GREEN (Kalshi at or above), YELLOW (1 to 7 above),
  REMOVED (8+ above, research page only), no Kalshi (max 75, never Hammer).
  Published grade = median capped at Kalshi + 7. Board = GREEN and YELLOW at 70+.
"""
import json, sys, os, re, statistics
sys.path.insert(0, os.path.dirname(__file__))
from v7lib import grade_leg, hammer, perfect, payout, BOARD_MIN, MIN_MODELS

day, rdir = sys.argv[1], sys.argv[2]
C = json.load(open(f'daily/{day}/v7_candidates.json'))['legs']
MODELS = ['chatgpt', 'gemini', 'grok', 'claude']


def block(text, name):
    m = re.search(rf'{name}_START\s*\n(.*?)\n\s*{name}_END', text, re.S)
    if not m: return []
    rows = [l.strip().strip('`') for l in m.group(1).strip().splitlines() if l.strip() and not l.strip().startswith('```')]
    return [r for r in rows if r.split(',')[0].strip().lower() not in ('leg_no', 'rank', 'tip')]


nums, top10, tips, status = {m: {} for m in MODELS}, {}, {}, {}
for m in MODELS:
    f = os.path.join(rdir, m + '.md')
    if not os.path.exists(f) or os.path.getsize(f) < 200:
        status[m] = 'no reply'; continue
    t = open(f, errors='replace').read()
    rows = block(t, 'BD_V7')
    for r in rows:
        c = [x.strip() for x in r.split(',', 3)]
        if not c[0].isdigit(): continue
        i = int(c[0])
        if len(c) > 1 and re.fullmatch(r'\d{1,3}', c[1] or '') and 0 <= int(c[1]) <= 100:
            nums[m][i] = int(c[1])
    top10[m] = [int(r.split(',')[1]) for r in block(t, 'BD_TOP10') if len(r.split(',')) > 1 and r.split(',')[1].strip().isdigit()]
    tips[m] = [r.strip().strip('"') for r in block(t, 'BD_TIPS')][:5]
    status[m] = f'{len(nums[m])} of {len(C)} legs graded' if rows else 'reply had no BD_V7 block'

live = [m for m in MODELS if nums[m]]
if len(live) < MIN_MODELS:
    sys.exit(f'Only {len(live)} model(s) returned usable numbers ({status}). Not enough for a v7 board; fall back to the standard grading and say so on the site.')

for l in C:
    l['models'] = {m: nums[m].get(l['i']) for m in MODELS}
    g = grade_leg(list(l['models'].values()), l['k'])
    if g is None:
        l['med'], l['tier'], l['pub'] = None, 'X', None
    else:
        l['med'], l['tier'], l['pub'] = g
    v = [x for x in l['models'].values() if x is not None]
    l['spread'] = (max(v) - min(v)) if len(v) >= 2 else None

board = sorted([l for l in C if l['tier'] in ('G', 'Y', 'N') and l['pub'] is not None and l['pub'] >= BOARD_MIN], key=lambda l: -l['pub'])
low = sorted([l for l in C if l['tier'] in ('G', 'Y', 'N') and l['pub'] is not None and l['pub'] < BOARD_MIN], key=lambda l: -l['pub'])
removed = sorted([l for l in C if l['tier'] == 'R'], key=lambda l: -(l['med'] - l['k']))
nograde = [l for l in C if l['tier'] == 'X']

ham, ham_why = hammer(board)
perf = perfect(board)  # GREEN legs on the board (70+) only
# where the models agreed and split (legs with 2+ numbers)
split = sorted([l for l in C if l['spread'] is not None and l['spread'] >= 15], key=lambda l: -l['spread'])[:8]
agree = sorted([l for l in C if l['spread'] is not None and l['spread'] <= 5 and l['pub'] and l['pub'] >= 70], key=lambda l: -l['pub'])[:8]
# consensus top 10: count how many models put each leg in their top 10
votes = {}
for m, t in top10.items():
    for i in t[:10]: votes[i] = votes.get(i, 0) + 1

res = {'date': day, 'models': status, 'legs': C, 'board': [l['i'] for l in board], 'low': [l['i'] for l in low],
       'removed': [l['i'] for l in removed], 'nograde': [l['i'] for l in nograde],
       'hammer': {'legs': [l['i'] for l in ham] if ham else [], 'pay': round(payout(ham), 2) if ham else None, 'none': ham_why},
       'perfect': perf, 'split': [l['i'] for l in split], 'agree': [l['i'] for l in agree],
       'votes': votes, 'tips': tips}
json.dump(res, open(f'daily/{day}/v7_merged.json', 'w'), indent=1)

L = {l['i']: l for l in C}
print('models:', status)
print(f'board {len(board)} (GREEN {sum(l["tier"]=="G" for l in board)}, YELLOW {sum(l["tier"]=="Y" for l in board)}, no Kalshi {sum(l["tier"]=="N" for l in board)}) · under 70 {len(low)} · REMOVED {len(removed)} · no grade {len(nograde)}')
print('hammer:', [L[i]['p'] for i in res['hammer']['legs']], res['hammer']['pay'] or res['hammer']['none'])
for t in perf: print(t['name'], [L[i]['p'] for i in t['legs']], t['pay'], t['hit'], t['none'] or '')
