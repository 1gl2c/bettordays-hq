"""Builds the Nov 20 audit page (audit.html) from the agent replies and record.json.
Usage (from repo root): python3 pipeline/reviews/2026-11-20-audit/build_page.py"""
import re, json, html, os
D = os.path.dirname(os.path.abspath(__file__))
R = os.path.join(D, '..', '..', '..')

def clean(s): return s.replace('—', ', ').replace('--', ', ').replace('already knows', 'already sees').strip()
def block(t, name):
    m = re.search(rf'{name}_START\s*\n(.*?)\n\s*{name}_END', t, re.S)
    rows = [l.strip() for l in m.group(1).splitlines() if l.strip()] if m else []
    return [r for r in rows if not r.lower().startswith(('rank,', 'idea,', 'tab_order,'))]

CLAUDE_AUDIT = """1,grading,Enforce every cap after the blend (CFB ML 69 and no-line legs 75) so the model median can never publish past it,Confirmed in tonight's file: Oregon ML had system grade 69 and was published at 87 and put on the Hammer,0.5
2,trust,Show ROI after Kalshi fees next to every hit rate and drop hit rate as the headline,GREEN singles made +6.5% overall but -10.2% last week; the whole edge came from Nov 9-15 at 73-2,1
3,compliance,Remove FREE MONEY and making people money and the 8-10% bankroll line and add 1-800-GAMBLER to every page and post,All three auditors flagged the same lines and the fix takes an hour,0.5
4,grading,Default the board to the Master filter and take PRA and receiving yards and TDs and college ML off it,70+ PRA returned -20.4% and rebounds -5.7% while assists +6.1% threes +10.8% NBA ML +12.8%,0.5
5,grading,Keep any leg with a 12+ point model split off the Hammer and fall back to the system grade,Hartenstein 10+ reb was Claude 30 vs Grok 68; a median of a split is a guess,0.5
6,ux,First phone screen = Tonight: Hammer or We passed plus Copy plus last night's result in the same size,Home is 26 screens; a new user must find tonight's play in under 30 seconds,3
7,data,Build one fact pack per game (injury PDF + last 10 logs + minutes + spread + Kalshi) and stop paying models to browse,Browsing is what cost $9 in a day; a fixed pack also makes the models comparable,3
8,grading,Run all simulations in our own Python code and drop the AI-written sims,308 sim lines went 164-144 vs a 57% break-even and the AI sims disagreed by up to 45 points on one line,2
9,trust,Drive every record number from one query and restart the ledger,Pages show 343/442 next to 345/448 and /results prints 0/6 before it loads,2
10,ux,Split the one 516 KB page into real pages and page History by night,History is 275 phone screens and the rulebook is pasted on four pages,4
11,growth,Make Grade a main tab with a 3-a-day free cap and delete slip images after reading,It is the only one-screen page and both auditors called it the best lead magnet,2
12,ops,Auto-pull legs at 3:45 PM from the official injury report,Maxey and Grayson Allen were late scratches that a manual check missed,2
13,data,Ask cappers to send picks to a BettorDays Telegram or form and use X pay-per-use search only as backup,Cheapest legal path; scraping a logged-in X account breaks X rules,2
14,money,No paid tier and no paid affiliate links until 60 logged nights beat the closing price,Paid picks turn the site into a gambling ad and paid links need state licenses,0
15,compliance,Name no prediction market for states with active enforcement and geo-block that card,Ohio fined Kalshi and several states are in court; the bonuses page lists all 50,1
16,trust,Timestamp every board before tip with a public GitHub commit,Lets a skeptic check nothing was edited after games,1
17,ux,Ticket builder loads the Hammer and warns at the 3rd leg from one game,Nov 18 one Lakers ML sank five tickets,2
18,grading,Log the Kalshi price at grade time and at tip and report closing line value,Beating the close is the only proof of edge a sharp accepts,2
19,growth,One 3 PM card and one 9 AM receipt every day including misses and passes,Honest receipts are the brand; 23 members each asked for 5 friends gets to 100 fast,1
20,ops,Weight each model by its Brier score only after 150 graded legs on the same slates,Two nights is noise; Gemini calling Claude the outlier came from one night""".splitlines()
CLAUDE_VERDICT = ["parlay grader,keep,Cheap vision read then lookup against our graded board; cap free uses and circle the leg that kills the slip",
 "bonus finder,keep unpaid and rewrite,Rename it Sign-up offers by state and remove free money and the Kalshi card in contested states",
 "referral program,later,Leave the code live but stop promoting it until people open the app daily",
 "paid tier,not yet,60 logged nights that beat the close first",
 "multi-model blend,rebuild,One fact pack per game and 2 to 3 cheap models plus our code sim; weights only after 150 legs",
 "X capper automation,ask first then API,Cappers send picks to a BettorDays Telegram or form; X pay-per-use search for the rest"]
CLAUDE_NAV = ["1,Tonight,Hammer or We passed with Copy and the Master board", "2,Ticket,Builder with payout and same-game warnings",
 "3,Grade,Screenshot any slip and see the weakest leg", "4,Record,Last 7 nights ROI and hit rate and the explorer",
 "5,More,Sign-up offers and how it works and account"]

agents = {}
for name in ['gemini', 'grok', 'chatgpt']:
    t = open(os.path.join(D, name + '.md'), errors='replace').read()
    agents[name] = {'audit': block(t, 'BD_AUDIT'), 'verdict': block(t, 'BD_VERDICT'), 'nav': block(t, 'BD_NAV'), 'bytes': len(t)}
agents['claude'] = {'audit': CLAUDE_AUDIT, 'verdict': CLAUDE_VERDICT, 'nav': CLAUDE_NAV, 'bytes': 0}

# ---- ROI from the record
L = [l for l in json.load(open(os.path.join(R, 'record.json')))['legs'] if l.get('k') and l['res'] in ('W', 'L')]
def roi(ls):
    n = len(ls); w = sum(l['res'] == 'W' for l in ls)
    cost = sum(l['k'] / 100 + 0.07 * (l['k'] / 100) * (1 - l['k'] / 100) for l in ls)
    return dict(n=n, w=w, hit=round(100 * w / n, 1) if n else 0, k=round(sum(l['k'] for l in ls) / n, 1) if n else 0, roi=round(100 * (w - cost) / cost, 1) if n else 0)
g70 = [l for l in L if l['g'] >= 70]
tiers = [('GREEN (Kalshi at or above us)', [l for l in g70 if l['k'] >= l['g']]),
         ('YELLOW (we are 1 to 7 above)', [l for l in g70 if 1 <= l['g'] - l['k'] <= 7]),
         ('REMOVED (we are 8+ above)', [l for l in g70 if l['g'] - l['k'] >= 8]),
         ('All 70+ legs', g70)]
weeks = [(w, [l for l in g70 if l['wk'] == w and l['k'] >= l['g']]) for w in ['Nov 4-8', 'Nov 9-15', 'Nov 16-22']]
names = {'3pm': 'Threes', 'ast': 'Assists', 'ml': 'Moneylines', 'pts': 'Points', 'reb': 'Rebounds', 'pra': 'PRA'}
stats = sorted([(names[s], [l for l in g70 if l['st'] == s]) for s in names], key=lambda x: -roi(x[1])['roi'])
ROI = {'tiers': [(a, roi(b)) for a, b in tiers], 'weeks': [(a, roi(b)) for a, b in weeks], 'stats': [(a, roi(b)) for a, b in stats]}
json.dump(ROI, open(os.path.join(D, 'roi.json'), 'w'), indent=1)

def bars(rows, lo=-25, hi=25):
    W, H, pad = 360, 56, 34
    sx = lambda v: pad + (max(lo, min(hi, v)) - lo) / (hi - lo) * (W - 2 * pad)
    z = sx(0); h = len(rows) * H; out = [f'<svg viewBox="0 0 {W} {h+22}" role="img" class="chart">']
    for t in range(lo, hi + 1, 5):
        x = sx(t); lab = '0%' if t == 0 else f'{t:+d}%'
        out.append(f'<line x1="{x:.1f}" y1="0" x2="{x:.1f}" y2="{h}" class="{"axis" if t == 0 else "grid"}"/>')
        if t % 10 == 5 or t == 0 or abs(t) == 25: out.append(f'<text x="{x:.1f}" y="{h+16}" class="tick" text-anchor="middle">{lab}</text>')
    for i, (name, r) in enumerate(rows):
        y = i * H; v = r['roi']; x = sx(v); cls = 'pos' if v > 0 else 'neg'
        out.append(f'<text x="0" y="{y+13}" class="lab">{html.escape(name)}</text>'
                   f'<text x="{W}" y="{y+13}" class="sub" text-anchor="end">{r["w"]}-{r["n"]-r["w"]} · {r["hit"]}% · avg {r["k"]:.0f}¢</text>'
                   f'<rect x="{min(x,z):.1f}" y="{y+22}" width="{max(abs(x-z),1.5):.1f}" height="16" rx="3" class="{cls}"/>'
                   f'<text x="{(x+5 if v>=0 else x-5):.1f}" y="{y+34}" class="val" text-anchor="{"start" if v>=0 else "end"}">{v:+.1f}%</text>')
    out.append('</svg>'); return ''.join(out)

AG = [('chatgpt', 'ChatGPT', ''), ('grok', 'Grok 4.7', ''), ('gemini', 'Gemini 4 Neon', ''), ('claude', 'Claude', '')]
VIDEAS = ['parlay grader', 'bonus finder', 'referral program', 'paid tier', 'multi-model blend', 'X capper automation']
def vmap(rows):
    m = {}
    for r in rows:
        c = r.split(',', 2)
        if len(c) == 3: m[c[0].strip().lower()] = (clean(c[1]), clean(c[2]))
    return m
V = {a: vmap(agents[a]['verdict']) for a, _, _ in AG}
def tone(v):
    v = v.lower()
    if any(k in v for k in ['pause', 'later', 'not', 'delay', 'after']): return 'wait'
    if any(k in v for k in ['rebuild', 're-architect', 'ask', 'rewrite', 'unpaid', 'informational', 'shadow', 'pilot', 'opt-in']): return 'fix'
    return 'go'

vt = ['<div class="tblwrap"><table class="vt"><thead><tr><th>Idea</th>' + ''.join(f'<th>{n}</th>' for _, n, _ in AG) + '</tr></thead><tbody>']
for idea in VIDEAS:
    vt.append(f'<tr><th scope="row">{idea[0].upper()+idea[1:]}</th>')
    for a, _, _ in AG:
        v, why = V[a].get(idea.lower(), ('n/a', ''))
        vt.append(f'<td><span class="pill {tone(v)}">{html.escape(v.lower())}</span><p>{html.escape(why)}</p></td>')
    vt.append('</tr>')
vt.append('</tbody></table></div>')

def navs(a):
    out = []
    for r in agents[a]['nav']:
        c = r.split(',', 2)
        if len(c) == 3: out.append(f'<li><b>{html.escape(clean(c[1]))}</b><span>{html.escape(clean(c[2]))}</span></li>')
    return '<ol class="nav">' + ''.join(out) + '</ol>'

AREA = {'grading': 'Grading', 'compliance': 'Legal', 'ux': 'Design', 'growth': 'Growth', 'money': 'Money', 'trust': 'Trust', 'data': 'Data', 'ops': 'Automation'}
def lists(a):
    out = ['<ol class="list">']
    for r in agents[a]['audit']:
        c = r.split(',', 4)
        if len(c) < 5 or not c[0].strip().isdigit(): continue
        out.append(f'<li><span class="area a-{c[1].strip()}">{AREA.get(c[1].strip(), c[1])}</span><div><b>{html.escape(clean(c[2]))}</b>'
                   f'<p>{html.escape(clean(c[3]))}</p></div><span class="eff">{html.escape(c[4].strip())} d</span></li>')
    out.append('</ol>'); return ''.join(out)

page = open(os.path.join(D, 'template.html')).read()
page = (page.replace('{{TIERS}}', bars(ROI['tiers'])).replace('{{WEEKS}}', bars(ROI['weeks']))
            .replace('{{STATS}}', bars(ROI['stats'])).replace('{{VERDICTS}}', ''.join(vt))
            .replace('{{NAV_claude}}', navs('claude')).replace('{{NAV_chatgpt}}', navs('chatgpt')).replace('{{NAV_grok}}', navs('grok')).replace('{{NAV_gemini}}', navs('gemini'))
            .replace('{{LIST_claude}}', lists('claude')).replace('{{LIST_chatgpt}}', lists('chatgpt')).replace('{{LIST_grok}}', lists('grok')).replace('{{LIST_gemini}}', lists('gemini')))
assert '—' not in page, 'em dash in page'
open(os.path.join(D, 'audit.html'), 'w').write(page)
print('ok', {k: (len(v['audit']), len(v['verdict']), len(v['nav'])) for k, v in agents.items()})
print(json.dumps(ROI))
