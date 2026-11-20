"""Board card for social (1080x1350 JPG) from daily/DATE/v7_merged.json.
Usage (from pipeline/): python3 v7/card_v7.py DATE "Friday · Nov 20" OUT.jpg
Shows the top board legs (GREEN first), the Hammer or the Core ticket, and the 21+ line. No money, no lock language."""
import json, sys, html, asyncio
day, label, out = sys.argv[1:4]
M = json.load(open(f'daily/{day}/v7_merged.json')); L = {l['i']: l for l in M['legs']}
board = [L[i] for i in M['board']]
top = sorted(board, key=lambda l: (l['tier'] != 'G', -l['pub']))[:8]
ham = [L[i] for i in M['hammer']['legs']]
core = next((t for t in M['perfect'] if t['name'] == 'Core' and t['legs']), None)
tk_name, tk_legs, tk_pay = ('THE HAMMER', ham, M['hammer']['pay']) if ham else (('CORE TICKET', [L[i] for i in core['legs']], core['pay']) if core else (None, [], None))
e = html.escape
rows = ''.join(f"<div class=row><span class=p>{e(l['p'])}</span><span class=g>{e(l['g'])}</span><b>{l['pub']}</b><i class='t {l['tier']}'>{'GREEN' if l['tier']=='G' else 'YELLOW' if l['tier']=='Y' else 'NO KALSHI'}</i></div>" for l in top)
tk = (f"<div class=tk><h3>{tk_name} <small>{len(tk_legs)} legs · about {tk_pay}x at Kalshi prices</small></h3>" + ''.join(f"<div class=tl>{e(l['p'])}</div>" for l in tk_legs) + "</div>") if tk_legs else "<div class=tk><h3>NO HAMMER TONIGHT</h3><div class=tl>Not enough legs passed every check. Passing is a win.</div></div>"
page = f"""<!doctype html><html><head><link href="https://fonts.googleapis.com/css2?family=Archivo+Black&family=Inter:wght@400;600;800&family=JetBrains+Mono:wght@500&display=swap" rel=stylesheet><style>
body{{margin:0;width:1080px;height:1350px;background:#0d0f0e;color:#f2f4f3;font-family:Inter;position:relative;overflow:hidden}}
.wrap{{padding:70px 64px}}.kick{{font:500 22px 'JetBrains Mono';color:#04ff9f;letter-spacing:3px}}
h1{{font:72px/0.98 'Archivo Black';margin:18px 0 10px;letter-spacing:-1px}}h1 em{{font-style:normal;color:#04ff9f}}
.sub{{font-size:24px;color:#9aa3a0;margin-bottom:34px}}
.row{{display:grid;grid-template-columns:1fr 150px 70px 130px;align-items:center;border-top:1px solid #232826;padding:15px 0;font-size:25px}}
.p{{font-weight:600}}.g{{font:500 18px 'JetBrains Mono';color:#8b9490}}b{{font:30px 'Archivo Black';text-align:right;padding-right:16px}}
.t{{font:500 15px 'JetBrains Mono';font-style:normal;text-align:center;padding:6px 0;border-radius:6px}}.G{{background:#04ff9f22;color:#04ff9f}}.Y{{background:#ffb02022;color:#ffb020}}.N{{background:#ffffff14;color:#c9cfcc}}
.tk{{margin-top:30px;border:2px solid #04ff9f;border-radius:14px;padding:22px 26px}}.tk h3{{font:30px 'Archivo Black';margin:0 0 10px;color:#04ff9f}}.tk small{{font:500 18px 'JetBrains Mono';color:#9aa3a0;margin-left:10px}}.tl{{font-size:23px;padding:5px 0;font-weight:600}}
.foot{{position:absolute;bottom:46px;left:64px;right:64px;display:flex;justify-content:space-between;font:500 18px 'JetBrains Mono';color:#7d8582}}.brand{{font:26px 'Archivo Black';color:#f2f4f3}}.brand em{{font-style:normal;color:#04ff9f}}
</style></head><body><div class=wrap><div class=kick>BETTORDAYS.XYZ · ENGINE V8 · 21+</div><h1>TONIGHT'S<br><em>BOARD.</em></h1>
<div class=sub>{e(label)} · Engine v8: 4 AI analysts grade blind, Kalshi referees after. Full board, each agent's sims and reasons free on the site.</div>{rows}{tk}</div>
<div class=foot><span>21+ · NOT A GUARANTEE · PLAY SMALL</span><span class=brand>BETTOR<em>DAYS</em></span></div></body></html>"""
async def main():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={'width': 1080, 'height': 1350})
        await pg.set_content(page); await pg.wait_for_timeout(1500)
        await pg.screenshot(path=out, type='jpeg', quality=92); await b.close()
asyncio.run(main()); print('card ->', out, len(top), 'legs,', tk_name)
