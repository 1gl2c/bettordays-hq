import re,json
s=open('bettordays-hq.html').read()
# ROI after Kalshi fees for priced 70+ legs ($1 singles at the logged price), shown next to the hit rate (Nov 20 audit)
_L=[l for l in json.load(open('/home/claude/bettordays-hq/record.json'))['legs'] if l.get('k') and l['res'] in ('W','L') and l['g']>=70]
def _roi(ls):
  c=sum(l['k']/100+0.07*(l['k']/100)*(1-l['k']/100) for l in ls);w=sum(l['res']=='W' for l in ls);return round(100*(w-c)/c,1) if ls else 0
_R={'all':_roi(_L),'green':_roi([l for l in _L if l['k']>=l['g']]),'n':len(_L)}
s=re.sub(r'var BD_ROI=\{[^}]*\};','var BD_ROI='+json.dumps(_R,separators=(',',':'))+';',s,count=1)
_C=json.load(open('/home/claude/bettordays-hq/calib.json'))['kalshi']
s=re.sub(r'var BD_CAL=\{[^}]*\};','var BD_CAL='+json.dumps({'c':round(_C['c'],4),'w':round(_C['w'],4)},separators=(',',':'))+';',s,count=1)
open('bettordays-hq.html','w').write(s)
DAYK=[('FR20','2026-11-20','Friday Nov 20'),('TH19','2026-11-19','Thursday Nov 19'),('WE18','2026-11-18','Wednesday Nov 18'),('TU17','2026-11-17','Tuesday Nov 17'),('MN16','2026-11-16','Monday Nov 16'),('SN15','2026-11-15','Sunday Nov 15'),('SAT','2026-11-14','Saturday Nov 14'),('FRI','2026-11-13','Friday Nov 13'),('THU','2026-11-12','Thursday Nov 12'),('WED','2026-11-11','Wednesday Nov 11'),('TUE','2026-11-10','Tuesday Nov 10')]
for k,day,lab in DAYK:
  m=re.search(r'const '+k+r'=(\[.*?\]);\n',s)
  if m: MON=json.loads(m.group(1)); break
board=[{"text":r['p'],"pct":r['pct'],"game":r['g'],"t":r.get('t',''),"sp":r.get('sp',''),"r":r.get('r',''),"fl":r.get('fl',''),"k":r.get('k'),"day":day,"label":lab} for r in sorted(MON,key=lambda r:-r['pct']) if r['pct']>0]
json.dump(board,open('/home/claude/bettordays-hq/board.json','w'))
head='<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">\n<link rel="manifest" href="/manifest.webmanifest">\n<link rel="apple-touch-icon" href="/apple-touch-icon.png">\n<link rel="icon" type="image/png" href="/icon-192.png">\n<meta name="apple-mobile-web-app-capable" content="yes">\n<meta name="mobile-web-app-capable" content="yes">\n<meta name="apple-mobile-web-app-title" content="BettorDays">\n<meta name="apple-mobile-web-app-status-bar-style" content="black">\n<meta name="theme-color" content="#0b0d0c">\n<meta name="description" content="Graded sports picks, a ticket builder with Kalshi odds and warnings, and a public record you can filter. Free while we build. 21+.">\n<meta property="og:title" content="BettorDays: picks with a receipt">\n<meta property="og:description" content="Every pick graded before tip. Every result counted after. Wins and losses, in public. 21+.">\n<meta property="og:image" content="https://bettordays.xyz/og.png">\n<meta property="og:url" content="https://bettordays.xyz/">\n<meta property="og:type" content="website">\n<meta name="twitter:card" content="summary_large_image">\n<meta name="twitter:image" content="https://bettordays.xyz/og.png">\n'
tail='\n<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2.45.4/dist/umd/supabase.min.js"></script>\n<script src="/sb.js"></script>\n<script src="/gate.js"></script>\n<script src="/install.js" defer></script>\n</html>\n'
open('/home/claude/bettordays-hq/index.html','w').write(head+s+tail)
print(len(board))
R=json.loads(re.search(r'const ROWS=(\[.*?\]);\n',s).group(1))
t70=[r for r in R if r['est']>=70]; h70=sum(r['hit'] for r in t70); p=h70/len(t70)
mains=re.search(r'<span data-count="(\d+)">0</span>-(\d+)</b><small>hammers and main parlays',s)
json.dump({"n":len(R),"h70":h70,"n70":len(t70),"p70":round(100*p),"three":round(100*p**3),"mains":f"{mains.group(1)}-{mains.group(2)}" if mains else "","last":R[-1]['day']},open('/home/claude/bettordays-hq/stats.json','w'))
print(open('/home/claude/bettordays-hq/stats.json').read())
