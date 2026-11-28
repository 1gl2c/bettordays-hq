"""Open-on-Kalshi buttons for every parlay on tonight's site, in two steps (the combo is created by the kalshi-combo
database function, which never trades; it is reached through Supabase SQL, so step 2 is run by Claude's database tool).
  1. python3 kalshi_autolinks.py DATE make   -> daily/DATE/autolinks.sql (one link call per parlay still missing a button)
  2. run that SQL, save its JSON rows to daily/DATE/autolinks_result.json
  3. python3 kalshi_autolinks.py DATE apply  -> writes the URLs into the site source
Parlays covered: tonight's tickets (CTIX), the Miracle, Edge Lab parlays and the Daily 2x, and the Perfect 3 and 10x
attempts (read from the built page, since the browser builds them). A leg with no Kalshi market (for example a PRA
number Kalshi does not list) is left out of the combo and the result says so."""
import json, re, sys, os, datetime, subprocess
DAY, STEP = sys.argv[1], sys.argv[2]; D = f'daily/{DAY}/'; dd = datetime.date.fromisoformat(DAY)
LBL = f"{dd.strftime('%b')} {dd.day}"
F = 'bettordays-hq.html'; s = open(F).read()
def getc(n):
    i = s.index('const ' + n + '=') + len('const ' + n + '='); return json.JSONDecoder().raw_decode(s[i:])[0]
def setc(n, v):
    global s; i = s.index('const ' + n + '=') + len('const ' + n + '='); _, e = json.JSONDecoder().raw_decode(s[i:]); s = s[:i] + json.dumps(v) + s[i + e:]
cur = re.search(r"const CUR=(\w+),CTIX=(\w+),CURD='([\d-]+)';", s); assert cur and cur.group(3) == DAY, 'site is not on ' + DAY
# leg text -> (market ticker, event ticker, side)
TK = {}
M = json.load(open(D + 'v7_merged.json'))
for l in M['legs']:
    if not l.get('ticker'): continue
    t = l['p'].lower(); side = 'no' if (' under ' in t or re.search(r' \+\d', l['p'])) else 'yes'
    TK[l['p']] = (l['ticker'], l['ticker'].rsplit('-', 1)[0], side)
if os.path.exists(D + 'miracle_ladder.json'):
    for l in json.load(open(D + 'miracle_ladder.json'))['legs']: TK.setdefault(l['p'], (l['t'], l['t'].rsplit('-', 1)[0], 'yes'))

def parlays():
    """(key, [leg texts]) for every parlay on tonight's site that has no button yet."""
    out = []
    for n, t in enumerate(getc(cur.group(2))):
        if not t.get('kl'): out.append((f'tix{n}', t['legs']))
    MIR = getc('MIR')
    if MIR['d'] == LBL and not MIR.get('kl'): out.append(('mir', [l['p'] for l in MIR['legs']]))
    e = next((x for x in getc('EL') if x['d'] == LBL), None)
    if e:
        for n, p in enumerate(e['par']):
            if not p.get('kl'): out.append((f'el{n}', [l['p'] for l in p['legs']]))
        if e.get('two') and not e['two'].get('kl'): out.append(('two', [l['p'] for l in e['two']['legs']]))
    PK = re.search(r"const PERFKL=\{", s) and (f"'{DAY}':" in s[s.index('const PERFKL='):s.index('const PERFKL=') + 20000])
    if not PK:
        js = ("const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage();"
              "await p.goto('file://'+process.argv[1]);await p.waitForTimeout(1500);"
              "const r=await p.evaluate(()=>[...document.querySelectorAll('.pcard')].slice(0,2).map(c=>[...c.querySelectorAll('.pl li > span')].map(x=>x.firstChild.textContent)));"
              "console.log(JSON.stringify(r));await b.close()})()")
        legs = json.loads(subprocess.run(['node', '-e', js, os.path.abspath('../index.html')], capture_output=True, text=True).stdout or '[]')
        for key, ls in zip(('three', 'ten'), legs):
            ls = [x.strip() for x in ls]
            if ls: out.append((key, ls))
    return out
M_P = {l['p'] for l in M['legs']}

if STEP == 'make':
    calls, plan = [], {}
    for key, legs in parlays():
        k = [TK[l] for l in legs if l in TK]; miss = [l for l in legs if l not in TK]
        if len(k) < 2: print('skip', key, 'fewer than 2 legs on Kalshi', miss); continue
        plan[key] = {'legs': legs, 'missing': miss}
        body = {'action': 'link', 'note': f'{DAY} {key}', 'legs': [{'market_ticker': a, 'event_ticker': b, 'side': c} for a, b, c in k]}
        calls.append(f"perform pg_sleep(1.2); insert into combo_tmp select '{key}', public.kalshi_call('{json.dumps(body)}'::jsonb);")
    json.dump(plan, open(D + 'autolinks_plan.json', 'w'), indent=1)
    sql = ("create temp table if not exists combo_tmp(k text, r jsonb);\ndo $$ begin\n" + '\n'.join(calls) +
           "\nend $$;\nselect json_agg(json_build_object('k', k, 'url', r->'body'->>'url', 'err', r->'body'->'err')) from combo_tmp;")
    open(D + 'autolinks.sql', 'w').write(sql)
    for k, v in plan.items(): print(k, len(v['legs']), 'legs', ('missing on Kalshi: ' + ', '.join(v['missing'])) if v['missing'] else '')
elif STEP == 'apply':
    plan = json.load(open(D + 'autolinks_plan.json')); R = {r['k']: r for r in json.load(open(D + 'autolinks_result.json')) if r.get('url')}
    T = getc(cur.group(2))
    for k, r in R.items():
        if k.startswith('tix'): T[int(k[3:])]['kl'] = r['url']
    setc(cur.group(2), T)
    if 'mir' in R: MIR = getc('MIR'); MIR['kl'] = R['mir']['url']; setc('MIR', MIR)
    EL = getc('EL'); e = next((x for x in EL if x['d'] == LBL), None)
    if e:
        for k, r in R.items():
            if k.startswith('el'): e['par'][int(k[2:])]['kl'] = r['url']
        if 'two' in R: e['two']['kl'] = R['two']['url']
        setc('EL', EL)
    pk = {w: {'legs': plan[w]['legs'], 'u': R[w]['url']} for w in ('three', 'ten') if w in R}
    if pk: s = s.replace('const PERFKL={', 'const PERFKL={' + f"'{DAY}':" + json.dumps(pk) + ',', 1)
    open(F, 'w').write(s)
    print('applied', sorted(R), 'missing', sorted(set(plan) - set(R)))
