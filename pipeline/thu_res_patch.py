"""Publish Nov 19 results into the site source. Run from pipeline/ after thu/res/grade.py and the Beta backfill.
Adds results to TH19, BETA top, AIP19; appends graded legs to ROWS; Beta track record; Thursday recap; status line."""
import json, re
F = 'bettordays-hq.html'; s = open(F).read()
G = json.load(open('thu/thu_graded.json'))['rows']; GR = {r['p']: r for r in G}
BF = {a['ticker']: a for a in json.load(open('beta19/beta_backfill_nov19.json'))}

def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:90]); s = s.replace(a, b)

def setconst(name, val):
    global s
    i = s.index('const ' + name + '=') + len('const ' + name + '=')
    _, e = json.JSONDecoder().raw_decode(s[i:]); s = s[:i] + json.dumps(val) + s[i + e:]

def getconst(name):
    i = s.index('const ' + name + '=') + len('const ' + name + '=')
    return json.JSONDecoder().raw_decode(s[i:])[0]

# 1. board rows get results
T = getconst('TH19')
for r in T:
    g = GR[r['p']]
    if g.get('r'): r['r'] = g['r']; r['act'] = g.get('act')
setconst('TH19', T)

# 2. record rows (graded legs with a grade; voids and NFL team lines with no grade stay out)
m = re.search(r'const ROWS=(\[.*?\]);\n', s); R = json.loads(m.group(1))
assert not any(r['day'] == 'Nov 19' for r in R)
def stat(t, ty):
    t = t.lower()
    if ty != 'prop': return ty
    if 'touchdown' in t: return 'atd'
    if 'points + rebounds + assists' in t: return 'pra'
    if 'rushing + receiving' in t: return 'prop'
    if 'attempt' in t: return 'prop'
    for k, v in [('three', '3pm'), ('assist', 'ast'), ('rebound', 'reb'), ('reception', 'rec'), ('receiving y', 'recyds'), ('rushing y', 'rush'), ('point', 'pts')]:
        if k in t: return v
    return 'prop'
add = 0
for r in T:
    if r.get('r') not in ('W', 'L') or not r['pct']: continue  # pct 0 = no system grade (NFL team lines)
    st = stat(r['p'], r['ty'])
    R.append({'day': 'Nov 19', 'pick': r['p'], 'est': r['pct'], 'hit': 1 if r['r'] == 'W' else 0, 'sport': r['sp'],
              'mkt': 'atd' if st == 'atd' else r['ty'], 'stat': st, 'dir': 'u' if 'under' in r['p'].lower() else 'o',
              'style': r['st'], 'boost': 0, 'star': 0, 'fav': 0})  # every Nov 19 "moved" flag was a notation rewrite, not a real move
    add += 1
s = s[:m.start(1)] + json.dumps(R) + s[m.end(1):]
t70 = [r for r in R if r['est'] >= 70]; H = sum(r['hit'] for r in t70); N = len(t70)
print('ROWS', len(R), 'added', add, '70+ all time', H, N)

# 3. Beta results and track record
B = getconst('BETA')
for l in B['top']:
    o = BF[l['ticker']]; l['r'] = o['outcome']; l['act'] = o['actual']
w = sum(l['r'] == 'W' for l in B['top']); lo = sum(l['r'] == 'L' for l in B['top'])
t5 = B['top'][:5]; t5s = f"{sum(l['r']=='W' for l in t5)}-{sum(l['r']=='L' for l in t5)}"
tot = 0
for l in B['top']:
    p = l['ask']; c = p + 0.07 * p * (1 - p); tot += (1 / c - 1) if l['r'] == 'W' else -1
roi = round(100 * tot / len(B['top']), 1)
assert not any(h['d'] == 'Nov 19' for h in B['hist'])
B['hist'].append({'d': 'Nov 19', 'w': w, 'l': lo, 'top5': t5s, 'roi': roi})
setconst('BETA', B)
hw = sum(h['w'] for h in B['hist']); hl = sum(h['l'] for h in B['hist'])
print('beta', w, lo, t5s, roi, 'all', hw, hl)
rep("`Nov 18: 9-6, top 5 went 5-0`", f"`Nov 19: {w}-{lo} · two nights: {hw}-{hl}`")

# 4. AI panel gets results and a score line
A = getconst('AIP19')
for p in A:
    g = GR.get(p['pick'])
    if g and g.get('r'): p['r'] = g['r']; p['act'] = g.get('act')
setconst('AIP19', A)
sc = [p for p in A if p.get('r') in ('W', 'L') and all(p.get(k) is not None for k in ('ours', 'k', 'gpt', 'gem', 'grok', 'med')) and p['ours'] > 0]
def br(k): return sum((p[k] / 100 - (p['r'] == 'W')) ** 2 for p in sc) / len(sc)
S = {k: round(br(k), 3) for k in ('ours', 'k', 'gpt', 'gem', 'grok', 'med')}
print('scores', len(sc), S)
rep("<th>Panel</th></tr></thead>", "<th>Panel</th><th>Result</th></tr></thead>")
rep("<br><small>${r.lo!=null?Math.round(r.lo)+' to '+Math.round(r.hi):''}</small></td></tr>`",
    "<br><small>${r.lo!=null?Math.round(r.lo)+' to '+Math.round(r.hi):''}</small></td><td class=\"mono\">${r.r?`<span class=\"res ${r.r==='W'?'w':'l'}\">${r.r}</span>${r.act!=null?' <small>'+r.act+'</small>':''}`:'-'}</td></tr>`")
order = sorted([('Grok', S['grok']), ('Kalshi', S['k']), ('the panel middle', S['med']), ('Gemini', S['gem']), ('ChatGPT', S['gpt']), ('our grades', S['ours'])], key=lambda x: x[1])
otxt = ', '.join(f'{n} {v:.3f}' for n, v in order)
rep('<div class="flags" style="margin-top:12px">\n      <div class="flag w"><b>Where we were highest</b>',
    f'<div class="flags" style="margin-top:12px">\n      <div class="flag"><b>Scored after the games</b><div class="r bad">nobody beat a coin flip</div><p>On the {len(sc)} legs every source graded, the accuracy score (lower is better; always guessing 50% scores 0.250) came out: {otxt}. Our grades were the least accurate. One night is noise, so every model keeps being scored.</p><div class="who">Graded from ESPN box scores, Nov 19 night</div></div>\n      <div class="flag w"><b>Where we were highest</b>')

# 5. status line, headings
rep('<span class="lbl">Thursday Nov 19 picks are live · NFL, NBA, hockey and college hoops · no Hammer tonight</span>',
    '<span class="lbl">Thursday graded · 2 of 6 at 70%+, our worst night yet · Friday board next</span>')
rep("<h2 class=\"big\">Tonight's perfect parlay attempt</h2>", "<h2 class=\"big\">Latest perfect parlay attempt</h2>")

# 6. Method page: add Nov 19 like-for-like legs to the warning note
rep("Those 37 legs came from 20 games, so this is still a small sample.</span><em>SET NOV 18</em>",
    "Those 37 legs came from 20 games, so this is still a small sample. Nov 19 added 30 more like-for-like legs: ⚠ legs hit 2 of 8, 0 to 7 above Kalshi 0 of 4, below Kalshi 7 of 18. Kalshi's prices were closer to the results than our grades again (accuracy score 0.279 vs 0.313, lower is better).</span><em>SET NOV 18 · UPDATED NOV 19</em>")

# 7. Thursday recap section
g = [r for r in G if r.get('r') in ('W', 'L') and r['pct'] is not None]
a70 = [r for r in g if r['pct'] >= 70]; h70 = sum(r['r'] == 'W' for r in a70)
gw = sum(r['r'] == 'W' for r in g); exp = round(sum(r['pct'] for r in g) / 100)
wk = [r for r in g if r.get('k') is not None and r['pct'] >= r['k'] + 8]; hwk = sum(r['r'] == 'W' for r in wk)
sec = f'''<section class="panel" id="review19">
    <h2>Thursday recap · Nov 19 <small>our worst night on the record</small></h2>
    <div class="kpis">
      <div class="kpi"><span class="lbl">70%+ legs</span><b><span data-count="{h70}">0</span>/{len(a70)}</b><small>{round(100*h70/len(a70))}%. All time: {H} of {N} ({round(100*H/N)}%)</small></div>
      <div class="kpi"><span class="lbl">All graded legs</span><b><span data-count="{gw}">0</span>/{len(g)}</b><small>{round(100*gw/len(g))}%. Our grades expected about {exp} hits</small></div>
      <div class="kpi"><span class="lbl">⚠ legs</span><b><span data-count="{hwk}">0</span>/{len(wk)}</b><small>Graded 8+ above Kalshi. None were on a ticket</small></div>
      <div class="kpi"><span class="lbl">Beta Test Top 8</span><b><span data-count="{w}">0</span>/{len(B['top'])}</b><small>Top 5 went {t5s}. Flat bets: {roi:+.1f}% after fees. Two nights: {hw}-{hl}</small></div>
    </div>
    <h3 style="margin-top:18px">What happened</h3>
    <div class="flags">
      <div class="flag"><b>A blowout killed the NFL props</b><div class="r bad">receiving legs 1 of 8</div><p>Houston beat Indianapolis 26-3. Stroud threw only 27 passes for 194 yards, so the receiving lines missed: Collins had 58 on a 60+ line, Tank Dell 27, Schultz 11, Warren 22. Taylor ran 11 times for 21 yards as the Colts trailed. Stroud's rushing legs (27 yards) and Montgomery 10+ receiving (17) hit.</p><div class="who">The game-script warning was in Taylor's note</div></div>
      <div class="flag"><b>Both 80+ legs missed</b><div class="r bad">McDaniels 3, Lopez 3</div><p>Jaden McDaniels (84) had 3 rebounds in 39 minutes and Brook Lopez (80) had 3. Fox had 2. Both 80+ legs carried a ⚠ because Kalshi was 8 or more below us, which is why no Hammer was posted and no ticket was suggested.</p><div class="who">The ⚠ rule kept them off tickets</div></div>
      <div class="flag w"><b>Kalshi was closer than we were</b><div class="r warn">again</div><p>On the 30 like-for-like legs, Kalshi's prices scored 0.279 and our grades 0.313 (lower is better; guessing 50% every time scores 0.250). ⚠ legs went {hwk} of {len(wk)}. Same pattern as the Nov 16 to 18 comparison, and it is why Kalshi sits next to every grade.</p><div class="who">Recorded on the Method page</div></div>
      <div class="flag w"><b>Experiments</b><div class="r warn">all lost</div><p>Perfect 3 went 1 of 3 and Perfect 10x 1 of 4: Stroud 5+ rushing hit, Pepperdine +4.5 and Wisconsin ML lost. Beta Test Top 8 went {w}-{lo}, with Towns, Shamet and Coward hitting. The outside AI panel did no better than us or Kalshi on accuracy.</p><div class="who">Experimental, graded every night</div></div>
    </div>
  </section>
  '''
rep('<section class="panel" id="review18">', sec + '<section class="panel" id="review18">')
rep("review18:'results',", "review19:'results',review18:'results',")
# 8. wording that read as live before the games
rep("No suggested ticket tonight. No leg passes","No suggested ticket for this board. No leg passes")
rep("ChatGPT, Gemini and Grok each graded tonight's picks blind","ChatGPT, Gemini and Grok each graded the Nov 19 picks blind")
rep("'Tonight\\'s attempt, every suggested ticket graded leg by leg","'The latest attempt, every suggested ticket graded leg by leg")
open(F, 'w').write(s); print('patched')
