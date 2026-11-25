"""Before posting a new night's Miracle: move the current MIR (with its graded legs) into MIRH so past nights stay on the site.
Usage (from pipeline/): python3 miracle/archive.py"""
import json
F = 'bettordays-hq.html'; s = open(F).read()
def get(n):
    i = s.index('const ' + n + '=') + len('const ' + n + '='); v, e = json.JSONDecoder().raw_decode(s[i:]); return v, i, i + e
mir, _, _ = get('MIR'); h, a, b = get('MIRH')
if not any(x['d'] == mir['d'] for x in h):
    h.append({k: mir[k] for k in ('d', 'pays', 'chance', 'legs') if k in mir} | {'res': mir.get('res')})
    s = s[:a] + json.dumps(h) + s[b:]; open(F, 'w').write(s); print('archived', mir['d'])
else: print('already archived', mir['d'])
