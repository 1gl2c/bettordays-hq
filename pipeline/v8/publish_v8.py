"""Engine v8 publisher (copy of v7/publish_v7.py with v8 wording; same site edits and database load). Engine v7, Part C: publish a merged v7 board to the site source (bettordays-hq.html), and write the database load.

Usage (from pipeline/):
  python3 v7/publish_v7.py DATE CONST "Day label" PREV_CONST PREV_DATE "Prev label" "Prev history title" [NOTES_HTML]
  e.g. python3 v7/publish_v7.py 2026-11-20 FR20 "Friday · Nov 20" TH19 2026-11-19 "Thursday · Nov 19" "Thursday board · Nov 19 <small>FINAL · 70%+ legs 2 of 6</small>"

Reads daily/DATE/v7_merged.json (from merge_v7.py) and optional NOTES_HTML (injury and lineup flags for tonight).
Board: GREEN and YELLOW legs (and no-Kalshi legs) published 70+. Under-70 legs sit in a closed list under the board.
REMOVED legs never touch the board, the Hammer, tickets or the ticket builder; they go to V7D for the Research page.
Writes daily/DATE/v7_db.sql (model_v7_legs rows + model_picks rows for every published leg).
"""
import json, re, sys, os, datetime, html
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'v7'))
from v7lib import payout

day, K, label, PK, pday, plabel, ptitle = sys.argv[1:8]
notes = open(sys.argv[8]).read() if len(sys.argv) > 8 else ''
M = json.load(open(f'daily/{day}/v7_merged.json')); L = {l['i']: l for l in M['legs']}
MN = {'chatgpt': 'ChatGPT', 'gemini': 'Gemini', 'grok': 'Grok', 'claude': 'Claude'}
TIERN = {'G': 'GREEN', 'Y': 'YELLOW', 'N': 'no Kalshi price'}
F = 'bettordays-hq.html'; s = open(F).read()
assert f'const {K}=' not in s, f'{K} already published'


def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:100]); s = s.replace(a, b)


def mtext(l):
    v = ', '.join(f"{MN[m]} {x}" for m, x in l['models'].items() if x is not None)
    cap = (' Capped at Kalshi + 7.' if l['k'] is not None else ' Capped at 75.') if l['pub'] is not None and l['med'] is not None and l['pub'] < l['med'] else ''
    k = f"Kalshi {l['k']} ({TIERN[l['tier']]})." if l['k'] is not None else 'No Kalshi price, so the grade can be no higher than 75 and the leg is never on the Hammer.'
    if l.get('eng') == 'v8':
        w = next((x for x in (l.get('why') or {}).values() if x), '')
        fd = '; '.join(f"{MN[m]}: {t}" for m, t in (l.get('fade') or [])[:2])
        return (f"Engine v8 blind grades (no price shown): {v}. Our system {l['sys'] if l.get('sys') else 'none'}. Our grade, the middle of all of them: {l['med']}."
                + (' Capped at 75 (no Kalshi price).' if l['k'] is None and l['pub'] is not None and l['pub'] < l['med'] else '') + f" {k}" + (f" Agent note: {w}." if w else '') + (f" Fade flag, {fd}." if fd else ''))
    return f"Engine v7 (game started before the v8 run): {v}. Middle {l['med']}.{cap} {k} Our system grade: {l['sys'] if l.get('sys') else 'none'}."


def row(l):
    r = {'p': l['p'], 'pct': l['pub'], 'g': l['g'], 't': l['t'], 'ty': l['ty'], 'st': l.get('st') or 'reg', 'sp': l['sp'],
         'n': (l.get('n', '') + ' ' + mtext(l)).strip(), 'tier': l['tier'], 'med': l['med'], 'ms': l['models']}
    if l.get('k') is not None: r['k'] = l['k']
    if l.get('b2b'): r['b2b'] = True
    if l.get('sys'): r['sys'] = l['sys']
    if l.get('rule'): r['fl'] = 'ACE RULE'
    return r


board = [row(L[i]) for i in M['board']]
low = [L[i] for i in M['low']]
H = M['hammer']
TIX = []
if H['legs']:
    hl = [L[i] for i in H['legs']]
    TIX.append({'t': f"{H.get('kind') or 'Hammer'} · {len(hl)} legs", 'c': '#04ff9f', 'legs': [l['p'] for l in hl], 'stake': 'Play small',
                'v': 'EV Hammer: legs Kalshi prices at 80 to 92 cents that our grade agrees with, from different games, paying 1.5x or more after fees. Favorites at that price hit 88.5% on our record, a bit more than the price says. The ticket goes up only if that math beats the payout after fees. Being tracked as $1 bets from Nov 21; it switches itself off if it loses.',
                'lock': f"About {H['pay']:.2f}x at Kalshi's prices", 'hit': f"About {H['hit']}% to hit · {H['ev']:+.1f}% expected after fees" if H.get('hit') else ''})
    # Nov 20 ChatGPT audit: every ticket shows the win rate it needs next to the win rate we expect
    TIX[-1]['be'] = round(100 / H['pay_net'], 1) if H.get('pay_net') else None


def perf_out(t):
    o = {'name': t['name'], 'none': t['none'], 'legs': [], 'pay': t['pay'], 'hit': t['hit'], 'ev': t.get('ev')}
    for i in t['legs']:
        l = L[i]; o['legs'].append({'p': l['p'], 'pub': l['pub'], 'k': l['k'], 'g': l['g']})
    if t['legs']:
        o['why'] = f"Favorite-edge legs from different games. About {t['hit']}% to hit at {t['pay']}x after fees, {t['ev']:+.1f}% expected." 
    return o


tips = []
for m, ts in M['tips'].items():
    for t in ts: tips.append({'tip': html.escape(t), 'who': MN[m]})
seen, tips2 = set(), []
for t in tips:
    k = t['tip'].lower()[:40]
    if k not in seen: seen.add(k); tips2.append(t)
lite = lambda l: {'p': l['p'], 'g': l['g'], 't': l['t'], 'k': l['k'], 'med': l['med'], 'ms': l['models']}
V7D = {'d': day, 'label': label, 'models': M['models'], 'rm': [lite(L[i]) for i in M['removed']],
       'perf': [perf_out(t) for t in M['perfect']], 'agree': [lite(L[i]) for i in M['agree']],
       'split': [lite(L[i]) for i in M['split']], 'tips': tips2[:5]}

# board consts, previous board to history
pk = PK.lower()
rep(f"const CUR={PK},CTIX={PK[:2]}TIX,CURD='{pday}';" if f"const CUR={PK},CTIX={PK[:2]}TIX,CURD='{pday}';" in s else re.search(r"const CUR=[^;]*;", s).group(0),
    f"const {K}={json.dumps(board)};\nconst {K[:2]}TIX={json.dumps(TIX)};\nconst CUR={K},CTIX={K[:2]}TIX,CURD='{day}';")
s = re.sub(r"const V7D=[^\n]*;\n", lambda m: 'const V7D=' + json.dumps(V7D) + ';\n', s, count=1)
# why there is no Hammer tonight, for the Tonight hero (empty when there is one)
hn = 'var HAMNOTE=' + json.dumps('' if H['legs'] else (H['none'] or '')) + ';'
s = re.sub(r"var HAMNOTE=[^\n]*;", lambda m: hn, s, count=1) if 'var HAMNOTE=' in s else s.replace("const V7D=", hn + "\nconst V7D=", 1)
from zoneinfo import ZoneInfo
pt = datetime.datetime.now(ZoneInfo('America/Los_Angeles'))
m = re.search(r'const CURCUT=[^;]*;\n', s)
if m: s = s.replace(m.group(0), '', 1)
s = s.replace('const V7=', f'const CURCUT={pt.hour}*60+{pt.minute};\nconst V7=', 1)  # posting time, PT: the learning model only uses legs that start after it
b = s.index("document.getElementById('thuTix').innerHTML=CTIX.map("); a = s.rindex("(function(){const rb=x=>x.r?", 0, b); c = s.index('\n', b) + 1
blk = s[a:c]; assert 'CURCUT' not in blk
hist = blk.replace('CURD', f"'{pday}'").replace('CTIX', f'{PK[:2]}TIX').replace('CUR', PK).replace("'thu", f"'{pk}")
s = s[:c] + hist + s[c:]
sec = f'''
  <section class="panel" id="{pk}hist">
    <h2>{ptitle}</h2>
    <h3>Tickets</h3>
    <div class="struct" id="{pk}Tix"></div>
    <div class="two" style="margin-top:18px">
      <div><h3>Top 25: any line</h3><ol class="tueo" id="{pk}Any" style="margin:8px 0 0;padding-left:22px;font-size:12.5px;line-height:1.75"></ol></div>
      <div><h3>Top 25: regular lines</h3><ol class="tueo" id="{pk}Reg" style="margin:8px 0 0;padding-left:22px;font-size:12.5px;line-height:1.75"></ol></div>
    </div>
    <details class="notes" style="margin-top:12px"><summary class="lbl" style="cursor:pointer">Clean 70 pool</summary><div class="chips" id="{pk}Pool"></div></details>
    <div class="filters" id="{pk}F" style="margin-top:16px"></div>
    <div class="scroll boardwrap" style="max-height:620px;overflow-y:auto"><table id="{pk}T" class="board"></table></div>
  </section>
'''
o = '\n  <section class="panel" id="wedhist">'; rep(o, sec + o)
rep("wedhist:'history',", f"{pk}hist:'history',wedhist:'history',")
rep(f"label:'{plabel}'}};", f"label:'{label}'}};")
rep(f'id="dayTitle">{plabel}</h2>', f'id="dayTitle">{label}</h2>')
rep(f"[typeof {PK}!=='undefined'&&{PK},", f"[typeof {K}!=='undefined'&&{K},typeof {PK}!=='undefined'&&{PK},")
pd = datetime.date.fromisoformat(pday); dd = datetime.date.fromisoformat(day)
rep(f"const D=[['{pd.strftime('%b')} {pd.day}','{PK}','{PK[:2]}TIX'],", f"const D=[['{dd.strftime('%b')} {dd.day}','{K}','{K[:2]}TIX'],['{pd.strftime('%b')} {pd.day}','{PK}','{PK[:2]}TIX'],")
# status line
m = re.search(r'<span class="lbl">[^<]*</span>', s[s.index('class="sys"'):] if 'class="sys"' in s else s)
nh = len(H['legs'])
status = f"{label.split(' · ')[0]} {dd.strftime('%b')} {dd.day} picks are live · Engine v8 · {len(board)} legs at 70+ · " + (f'Hammer: {nh} legs' if nh else 'no Hammer tonight')
s = re.sub(r'(<span class="lbl">)(Thursday graded[^<]*|[A-Z][a-z]+day [A-Z][a-z]{2} \d+ picks are live[^<]*|[A-Z][a-z]+day graded[^<]*)(</span>)', lambda m: m.group(1) + status + m.group(3), s, count=1)
# legend + notes on the board
a = s.index('<section class="panel" id="thursday">'); e = s.index('</section>', a); secx = s[a:e]
i = secx.index('<p class="note" style="margin:6px 0 0">Kalshi ='); j = secx.index('</p>', i) + 4
legend = ('<p class="note" style="margin:6px 0 0">Engine v8. Four AI analysts grade every leg blind (no market price shown), and our grade is the middle of their numbers plus our own system grade. Kalshi is the referee after that. '
          'Kalshi in green: the market has it at or above our grade (GREEN). Grey: we are 1 to 7 above (YELLOW). Legs where we are 8+ above Kalshi are pulled (that gap has lost most often); see '
          '<a href="/research" data-go="research">Research, Tonight</a>. Games that started before the v8 run keep their v7 grade. No Kalshi price: capped at 75 and never on the Hammer. Grades are estimates, not promises. Prices move, so check the slip.</p>')
secx = secx[:i] + legend + secx[j:]
kchip = lambda l: f'<small class="kp">K {l["k"]}</small>' if l['k'] is not None else ''
lowh = ''.join(f'<li>{html.escape(l["p"])} <span style="color:#8a9a93">{l["pub"]}%</span>{kchip(l)}</li>' for l in low)
nogr = [L[i] for i in M['nograde']]
flags = []
flags.append(f'<div class="flag{" g" if nh else " w"}"><b>{"Hammer" if nh else "No Hammer tonight"}</b><div class="r{" acc" if nh else " warn"}">Engine v7</div><p>' +
             (f"{nh} legs, about {H['pay']:.2f}x at Kalshi's prices. Every leg passes the v7 Hammer rule." if nh else html.escape(H['none'])) + '</p><div class="who">Passing is a win</div></div>')
flags.append(f'<div class="flag w"><b>Market disagrees</b><div class="r warn">{len(M["removed"])} removed</div><p>{len(M["removed"])} leg{"s" if len(M["removed"])!=1 else ""} had the models 8 or more above Kalshi, so {"they are" if len(M["removed"])!=1 else "it is"} off the board, the Hammer and every ticket. Listed on Research, Market check, and graded tomorrow.</p><div class="who">Engine v7</div></div>')
flags.append('<div class="flag"><b>Models</b><div class="r">who answered</div><p>' + html.escape(' · '.join(f"{MN[k]}: {v}" for k, v in M['models'].items())) + (f" {len(nogr)} leg{'s' if len(nogr)!=1 else ''} got fewer than 2 model numbers and {'are' if len(nogr)!=1 else 'is'} not graded." if nogr else '') + '</p><div class="who">Run through Hermes</div></div>')
rules = [L[i] for i in M['board'] if L[i].get('rule')]
if rules:
    flags.append('<div class="flag w"><b>Ace rule</b><div class="r bad">off every ticket</div><p>' + html.escape(', '.join(f"{l['p']} ({l['rule']})" for l in rules)) + '. Graded for the record only.</p><div class="who">Ace rule</div></div>')
nn = (f'<details class="notes" style="margin-top:16px"><summary class="lbl" style="cursor:pointer">Graded under 70 ({len(low)}), not recommended</summary><ol class="tueo" style="margin:8px 0 0;padding-left:22px;font-size:12.5px;line-height:1.75">{lowh}</ol></details>'
      f'<details class="notes" style="margin-top:12px"><summary class="lbl" style="cursor:pointer">Injury, lineup and rule notes</summary><div class="flags" style="margin-top:10px">\n      ' + notes + '\n      ' + '\n      '.join(flags) + '\n    </div></details>')
i = secx.index('<details class="notes"'); j = secx.rindex('</details>') + 10
secx = secx[:i] + nn + secx[j:]
s = s[:a] + secx + s[e:]
nohm = "No Hammer tonight. " + html.escape(H['none'] or '') + " Build your own in the ticket builder, which checks every leg against the v7 rules."
s = re.sub(r"if\(!CTIX\.length\)document\.getElementById\('thuTix'\)\.innerHTML='<p class=\"note\" style=\"margin:0\">[^']*</p>';",
           lambda m: "if(!CTIX.length)document.getElementById('thuTix').innerHTML='<p class=\"note\" style=\"margin:0\">" + nohm.replace("'", "\\'") + "</p>';", s, count=1)
open(F, 'w').write(s)
t = open('buildsite.py').read(); o = f"DAYK=[('{PK}',"; assert o in t
open('buildsite.py', 'w').write(t.replace(o, f"DAYK=[('{K}','{day}','{label.replace(' · ', ' ')}'),('{PK}',"))

# database load
def q(v): return 'null' if v is None else "'" + str(v).replace("'", "''") + "'"
now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%S+00:00')
place = {i: 'board' for i in M['board']} | {i: 'under70' for i in M['low']} | {i: 'removed' for i in M['removed']} | {i: 'nograde' for i in M['nograde']}
perfm = {}
for t in M['perfect']:
    for i in t['legs']: perfm.setdefault(i, []).append(t['name'])
v = []
for l in M['legs']:
    ms = l['models']
    v.append('(' + ','.join([q(day), str(l['i']), q(l['p']), q(l['g']), q(l['sp']), q(l['stat']), q(l['k']), 'true' if l.get('b2b') else 'false', q(l.get('sys')),
                             q(ms.get('chatgpt')), q(ms.get('gemini')), q(ms.get('grok')), q(ms.get('claude')), q(l['med']), q(l['tier']), q(l['pub']),
                             q(place[l['i']]), 'true' if l['i'] in H['legs'] else 'false', q('/'.join(perfm.get(l['i'], [])) or None), q(l.get('rule'))]) + ')')
sql = ['insert into model_v7_legs (slate_date,leg_no,pick_text,event,sport,market,kalshi,b2b,sys_grade,chatgpt,gemini,grok,claude,median,tier,published,placement,on_hammer,perfect,ace_rule) values\n' + ',\n'.join(v) + ';']
pv = []
for i in M['board'] + M['low']:
    l = L[i]
    key = day + '|' + re.sub(r'[^a-z0-9+]', '', l['p'].lower())
    pv.append('(' + ','.join([q(key), q(day), q(now), q(l['t']), q(l['sp']), q(l['g']), q(l['player']), q(l['ty'] if l['ty'] != 'prop' or l['stat'] != 'atd' else 'atd'), q(l['stat']),
                              q('u' if 'under' in l['p'].lower() else 'o'), q(l.get('st') or 'reg'), q(l['p']), 'false', q(l['pub']), q('v7 engine: median of AI models capped at Kalshi + 7 (' + day + ')'),
                              'true' if l.get('b2b') else 'false', q(mtext(l)), q(l['k']), q(now if l['k'] is not None else None), q('ungraded'), q('v7/merge_v7.py board')]) + ')')
sql.append('insert into model_picks (pick_key,slate_date,posted_at,game_time_text,sport,event,player,market,stat,direction,line_style,pick_text,added_by_model,grade,grade_version,b2b,notes,kalshi_price_grade,kalshi_price_grade_ts,status,data_source) values\n' + ',\n'.join(pv) + '\non conflict do nothing;')
open(f'daily/{day}/v7_db.sql', 'w').write('\n'.join(sql))
print('published', K, len(board), 'board legs,', len(low), 'under 70,', len(M['removed']), 'removed, hammer', nh, '· status:', status)
