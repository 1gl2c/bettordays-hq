"""Nov 22 merge (Engine v8 rules on the capper slate, 133 legs: NFL, NBA, NHL, tennis).
Usage (from pipeline/): python3 sun22/merge22.py
  Our grade = median of the four blind AI numbers plus our system grade, then the cap (college 69, NBA sides 88).
  Kalshi referees: GREEN at or above us, YELLOW 1-7 below, REMOVED 8+ below. No Kalshi: max 75, never on a ticket.
  Started games (LIVE) keep their pregame grade, stay off every ticket, and show as STARTED on the board.
  Finished fights (DONE) are settled: off the board, kept for the record only (not in the blind Brier sample).
  The three safer rungs are graded by our system plus any AI that named that exact line in BD_ALT.
Writes daily/2026-11-22/v7_merged.json (publish_v8 input) and v7_candidates.json."""
import json, re, os, sys, statistics
sys.path.insert(0, 'v7')
from v7lib import hammer, perfect, lotto, master_v2, payout, cap_for, stat_of, player_of, ace_rule, BOARD_MIN, NO_K_MAX, GAP_REMOVE
sys.path.insert(0, '.')
from kalshi_links import link as klink
import datetime as _dt

DAY = '2026-11-22'; D = f'daily/{DAY}/'; R = D + 'replies_v8/'
MODELS = ['chatgpt', 'gemini', 'grok', 'claude']
S = json.load(open('sun22/sun22.json')); ROWS = S['rows']; NLEG = len(ROWS)
BK = json.load(open(f'daily/{DAY}/book_fair.json'))
EXTRA, ALTMATCH = {}, {}
# questionable at merge time (AI rooms and team reports, 9:20 AM PT): shown as 'could sit'. Ace, Nov 22: a player who does not play voids the leg (money back), so Q players stay eligible for tickets
QLEGS = {3, 4, 19, 20, 97, 62, 66, 95, 27}   # Towns (illness, missed Saturday), Jeanty (sprain), Tuten, Hockenson (wrist), Tate (shoulder)
# a game counts as started once its kickoff or tip has passed (Pacific time) when this merge runs
NOW = _dt.datetime.now(_dt.timezone(_dt.timedelta(hours=-8)))
def started(t):
    m = re.match(r'(\d{1,2}):(\d{2}) (AM|PM)', t or '')
    if not m: return False
    h = int(m.group(1)) % 12 + (12 if m.group(3) == 'PM' else 0)
    return NOW.hour * 60 + NOW.minute >= h * 60 + int(m.group(2))


def block(text, name):
    m = re.search(rf'{name}_START\s*\n(.*?)\n\s*{name}_END', text, re.S)
    if not m: return []
    rows = [l.strip().strip('`') for l in m.group(1).strip().splitlines() if l.strip() and not l.strip().startswith('```')]
    return [r for r in rows if r.split(',')[0].strip().lower() not in ('leg_no', 'rank', 'tip', 'line_no')]


nums, why, conf, fades, tips, top10, alts, status = {m: {} for m in MODELS}, {}, {}, {}, {}, {}, {}, {}
for m in MODELS:
    if not os.path.exists(R + m + '.md'): status[m] = 'waiting'; top10[m] = []; tips[m] = []; continue
    t = open(R + m + '.md', errors='replace').read()
    for r in block(t, 'BD_V8'):
        c = [x.strip() for x in r.split(',', 4)]
        if c[0].isdigit() and len(c) > 1 and re.fullmatch(r'\d{1,3}', c[1]):
            i = int(c[0]); nums[m][i] = int(c[1])
            if len(c) > 3: why.setdefault(i, {})[m] = c[3][:160]
            if len(c) > 4: conf.setdefault(i, {})[m] = c[4][:10]
    for r in block(t, 'BD_FADE'):
        c = r.split(',', 1)
        if c[0].strip().isdigit(): fades.setdefault(int(c[0]), []).append((m, (c[1] if len(c) > 1 else '').strip()[:160]))
    top10[m] = [int(r.split(',')[1]) for r in block(t, 'BD_TOP10') if len(r.split(',')) > 1 and r.split(',')[1].strip().isdigit()]
    tips[m] = [r.strip().strip('"') for r in block(t, 'BD_TIPS')][:3]
    for r in block(t, 'BD_ALT'):
        c = [x.strip() for x in r.split(',', 3)]
        if len(c) >= 3 and c[2].isdigit(): alts.setdefault(m, []).append((c[0], c[1], int(c[2]), c[3] if len(c) > 3 else ''))
    status[m] = f'{len(nums[m])} of {NLEG} legs graded'

legs = []
for i in range(1, NLEG + 1):
    r = ROWS[i - 1]
    ty = r['ty']; stat = stat_of(r['p'], ty)
    sysg = r.get('sys')
    if True: ms = {m: nums[m].get(i) for m in MODELS}
    else:
        ms = {m: None for m in MODELS}
        for m, al in alts.items():
            for (_, line, p, _) in al:
                if re.search(ALTMATCH[i], line.lower().replace('lamelo ball', 'lamelo').replace('cooper ', '').replace('tyler ', '')): ms[m] = p
    fl = r.get('fl') or ('LIVE' if started(r['t']) else ('Q' if i in QLEGS else None))
    l = {'i': i, 'p': r['p'], 'player': player_of(r['p']), 'g': r['g'], 't': r['t'].replace(' PM', '') if r['t'].endswith('PM') else r['t'], 'sp': r['sp'], 'ty': ty, 'st': r.get('st') or 'reg',
         'bk': BK.get(str(i)), 'ku': klink(r.get('ev')),
         'stat': stat, 'k': r.get('k'), 'b2b': False, 'sys': sysg, 'n': r.get('n', ''), 'rule': ace_rule(r['p']), 'fl': fl, 'models': ms,
         'why': why.get(i, {}), 'conf': conf.get(i, {}), 'fade': fades.get(i, []), 'alt_rung': False}
    if fl == 'OUT':
        l.update(med=0, tier='X', pub=None, eng='v8 (OUT)', spread=None); legs.append(l); continue
    if fl == 'DONE':
        l.update(med=None, tier='S', pub=None, eng='settled before the board', spread=None); legs.append(l); continue
    v = [x for x in ms.values() if x is not None]
    voices = v + ([sysg] if sysg is not None else [])
    if not voices:
        l.update(med=None, tier='X', pub=None, eng='v8', spread=None); legs.append(l); continue
    blend = round(statistics.median(voices)); cap = cap_for(l); ours = min(blend, cap); k = l['k']
    if k is None: t, pub = 'N', min(ours, NO_K_MAX)
    elif fl == 'LIVE': t, pub = ('G' if ours <= k else 'Y'), ours        # live price moves with the score; no pull on a started game
    elif ours - k >= GAP_REMOVE: t, pub = 'R', None
    elif ours > k: t, pub = 'Y', ours
    else: t, pub = 'G', ours
    l.update(med=ours, blend=blend, cap=cap if blend > cap else None, tier=t, pub=pub, eng='v8' + (' (started, pregame grade)' if fl == 'LIVE' else ''),
             spread=(max(v) - min(v)) if len(v) > 1 else None, solo=len(v) == 0)
    legs.append(l)

L = {l['i']: l for l in legs}
pubd = [l for l in legs if l['tier'] in ('G', 'Y', 'N') and l['pub'] is not None]
board = sorted([l for l in pubd if l['pub'] >= BOARD_MIN], key=lambda l: -l['pub'])
low = sorted([l for l in pubd if l['pub'] < BOARD_MIN], key=lambda l: -l['pub'])
removed = sorted([l for l in legs if l['tier'] == 'R'], key=lambda l: -(l['med'] - l['k']))
# tickets: games not started, at least one AI number, no fade flag from 2+ agents, not UFC (no system grade)
fresh = [l for l in board if l.get('fl') not in ('LIVE', 'DONE') and not l.get('solo') and l['sp'] not in ('UFC', 'TENNIS', 'NHL') and len(l['fade']) < 2]
open_all = [l for l in pubd if l.get('fl') not in ('LIVE', 'DONE') and not l.get('solo') and l['sp'] not in ('UFC', 'TENNIS', 'NHL') and len(l['fade']) < 2]
lot, lot_why = lotto(open_all)
ms2 = [l['i'] for l in pubd if master_v2(l)]
ham, ham_why = hammer(fresh)
perf = perfect(fresh)
split = sorted([l for l in legs if l.get('spread') is not None and l['spread'] >= 15], key=lambda l: -l['spread'])[:10]
agree = sorted([l for l in legs if l.get('spread') is not None and l['spread'] <= 5 and (l['pub'] or 0) >= 70], key=lambda l: -l['pub'])[:10]
votes = {}
for m, tt in top10.items():
    for i in tt[:10]: votes[i] = votes.get(i, 0) + 1
res = {'date': DAY, 'engine': 'v8', 'models': status, 'legs': legs, 'board': [l['i'] for l in board], 'low': [l['i'] for l in low],
       'removed': [l['i'] for l in removed], 'nograde': [l['i'] for l in legs if l['tier'] == 'X'], 'settled': [l['i'] for l in legs if l['tier'] == 'S'],
       'hammer': {'legs': [l['i'] for l in ham] if ham else [], 'pay': round(payout(ham), 2) if ham else None, 'none': ham_why,
                  'hit': ham[0]['_ham'][0] if ham else None, 'pay_net': ham[0]['_ham'][1] if ham else None, 'ev': ham[0]['_ham'][2] if ham else None,
                  'kind': ham[0]['_ham'][3] if ham else None},
       'perfect': perf, 'split': [l['i'] for l in split], 'agree': [l['i'] for l in agree], 'votes': votes, 'tips': tips,
       'fades': {str(i): v for i, v in fades.items()}, 'alts': alts, 'kalshi_ts': open('sun22/kalshi_ts.txt').read().strip(),
       'lotto': lot, 'lotto_none': lot_why, 'master_v2': ms2, 'merged_at': NOW.strftime('%H:%M PT')}
json.dump(res, open(D + 'v7_merged.json', 'w'), indent=1)
json.dump({'legs': [{k: l[k] for k in ('i', 'p', 'g', 't', 'sp', 'ty', 'stat', 'k', 'sys', 'fl')} for l in legs]}, open(D + 'v7_candidates.json', 'w'), indent=1)
print('models:', status)
print(f"board {len(board)} · under 70 {len(low)} · removed {len(removed)} · settled {len(res['settled'])} · no grade {len(res['nograde'])}")
for l in board: print(f"  {l['pub']:>3} {l['tier']} K{l['k']} sys{l['sys']} {l['models']} {l['p']} {l['g']} {l['t']} {l.get('fl') or ''}")
print('removed:', [(L[i]['p'], L[i]['med'], L[i]['k']) for i in res['removed']])
print('hammer:', [L[i]['p'] for i in res['hammer']['legs']], res['hammer'])
for t in perf: print(t['name'], [L[i]['p'] for i in t['legs']], t['pay'], t['hit'], t['ev'], t['none'] or '')
print('lotto:', lot, lot_why); print('master v2:', [L[i]['p'] for i in ms2])
print('votes:', sorted(((n, L[i]['p']) for i, n in votes.items()), reverse=True)[:10])
