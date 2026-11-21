"""Nov 21: filters on the full grade sheet (Research, Tonight) and research cards that jump straight to their page.
Usage (from pipeline/): python3 sat21/gs_filters.py DATE   (idempotent)"""
import json, re, sys
day = sys.argv[1] if len(sys.argv) > 1 else '2026-11-21'
F = 'bettordays-hq.html'; s = open(F).read()

# 1) research hub hides when a card is open, and the page jumps straight to that card's section
a = "body[data-rsv] #rsHub{display:none}"
if a in s: s = s.replace(a, "body[data-rsv] #rsHub{display:none!important}")
a = "const apply=()=>{const m=/^#rs-([a-z0-9]+)/.exec(location.hash);if(m&&m[1]!=='hub')document.body.dataset.rsv=m[1];else delete document.body.dataset.rsv};"
if a in s:
    s = s.replace(a, "const apply=()=>{const m=/^#rs-([a-z0-9]+)/.exec(location.hash);if(m&&m[1]!=='hub'){document.body.dataset.rsv=m[1];"
                  "requestAnimationFrame(()=>requestAnimationFrame(()=>{const t=[...document.querySelectorAll('.rsv[data-v=\"'+m[1]+'\"]')].find(e=>e.offsetParent!==null);"
                  "if(t)window.scrollTo({top:Math.max(0,t.getBoundingClientRect().top+scrollY-12),behavior:'auto'})}))}else delete document.body.dataset.rsv};")

# 2) sport on every grade-sheet row
M = json.load(open(f'daily/{day}/v7_merged.json')); SP = {l['p']: l['sp'] for l in M['legs']}
m = re.search(r'const V7D=(\{.*?\});\n', s); V = json.loads(m.group(1))
for x in V['all']: x['sp'] = SP.get(x['p'], '')
s = s.replace(m.group(0), 'const V7D=' + json.dumps(V) + ';\n')

# 3) CSS for the filter buttons
if '.gsc{' not in s:
    s = s.replace('</style>', '.gsf .row{display:flex;gap:6px;flex-wrap:wrap}.gsc{border:1px solid var(--line);background:transparent;color:var(--mute);padding:7px 10px;font:600 12px var(--mono);cursor:pointer;border-radius:999px}'
                  '.gsc small{opacity:.65;margin-left:3px}.gsc.on{border-color:var(--acc);color:var(--acc);background:rgba(4,255,159,.08)}.gsc:focus-visible{outline:2px solid var(--acc);outline-offset:2px}\n</style>', 1)

# 4) the grade sheet with filters
i = s.index(" if(V7D.all){"); j = s.index(" el.innerHTML=h})();", i)
new = open('sat21/gs_block.js').read()
s = s[:i] + new + s[j:]
open(F, 'w').write(s); print('ok', len(V['all']))
