import json,re,os,unicodedata
from collections import defaultdict
P=json.load(open('audit/picks.json'))
SER={'pts':'KXNBAPTS','reb':'KXNBAREB','ast':'KXNBAAST','3pm':'KXNBA3PT','pra':'KXNBAPRA'}
NFLS={'recyds':'KXNFLRECYDS','rush':'KXNFLRSHYDS','pass':'KXNFLPASSYDS','rec':'KXNFLREC'}
MON={'NOV':11}
def strip(s): return unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode().lower()
def evdate(t):
  m=re.search(r'-(\d\d)([A-Z]{3})(\d\d)',t); return '2026-11-%s'%m.group(3) if m else None
IDX=defaultdict(list)   # (series,date) -> markets
for f in os.listdir('audit/kx'):
  if not f.endswith('.json'): continue
  s=f[:-5]
  for m in json.load(open('audit/kx/'+f)):
    IDX[(s,evdate(m['event_ticker']))].append(m)
ALIAS={'luka':'luka doncic','kd':'kevin durant','dame':'damian lillard','bam':'bam adebayo','mpj':'michael porter','sga':'shai gilgeous','lebron':'lebron james','wemby':'victor wembanyama',
 'giannis':'giannis antetokounmpo','jokic':'nikola jokic','ant':'anthony edwards','cade':'cade cunningham','trae':'trae young','zion':'zion williamson','ja':'ja morant','jjj':'jaren jackson','kat':'karl-anthony towns',
 'jabari':'jabari smith','flagg':'cooper flagg','shai':'shai gilgeous','tatum':'jayson tatum','herro':'tyler herro','ad':'anthony davis','pg':'paul george','embiid':'joel embiid','maxey':'tyrese maxey','wcj':'wendell carter','herb jones':'herbert jones','fox':'de\'aaron fox','bane':'desmond bane','cp3':'chris paul'}
def cands(name,ms):
  n=strip(name).replace('.',' ').replace('  ',' ').strip()
  n=ALIAS.get(n,n)
  toks=[t for t in re.split(r'[\s\-]+',n) if t and t not in ('jr','sr','ii','iii','iv')]
  out=[]
  for m in ms:
    pn=strip(m['title'].split(':')[0]).replace('.',' ')
    pt=[t for t in re.split(r'[\s\-]+',pn) if t]
    if not toks: continue
    if len(toks)==1:
      ok=toks[0] in pt or (len(toks[0])>3 and any(t.startswith(toks[0]) for t in pt))
    else:
      ok=all(any(t==q or (len(q)>2 and t.startswith(q)) for t in pt) for q in toks if len(q)>1) or (toks[-1] in pt and toks[0][0]==pt[0][0])
    if ok: out.append(m)
  return out
def thr(m):
  x=re.search(r':\s*([\d.]+)\+',m['title']); return int(float(x.group(1))) if x else None
stats=defaultdict(int); fails=[]
for p in P:
  p.pop('k_match',None)
  ser=SER.get(p.get('stat')) if p.get('sport')=='NBA' else NFLS.get(p.get('stat')) if p.get('sport')=='NFL' else None
  if not ser or p.get('threshold') is None or not p.get('player'): continue
  ms=IDX.get((ser,p['slate_date']),[])
  if not ms: stats['no series/date']+=1; continue
  c=cands(p['player'],ms)
  names={m['title'].split(':')[0] for m in c}
  if len(names)!=1: stats['name '+('none' if not names else 'ambiguous')]+=1; fails.append((p['slate_date'],p['pick_text'],sorted(names)[:4])); continue
  hit=[m for m in c if thr(m)==p['threshold']]
  if not hit:
    ts=sorted({thr(m):m for m in c if thr(m) is not None}.items())
    lo=[x for x in ts if x[0]<p['threshold']]; hi=[x for x in ts if x[0]>p['threshold']]
    if lo and hi:
      p['k_match']={'interp':[lo[-1][1]['ticker'],hi[0][1]['ticker']],'interp_thr':[lo[-1][0],hi[0][0]],'series':ser,'event':c[0]['event_ticker'],'name':c[0]['title'].split(':')[0],'invert':p['direction']=='u'}
      stats['interpolated']+=1
    else: stats['no threshold']+=1; fails.append((p['slate_date'],p['pick_text'],'thr',p['threshold'],[x[0] for x in ts]))
    continue
  m=hit[0]
  p['k_match']={'ticker':m['ticker'],'series':ser,'event':m['event_ticker'],'name':m['title'].split(':')[0],'result':m['result'],'invert':p['direction']=='u'}
  stats['matched']+=1
# ML
CITY={'hawks':'Atlanta','celtics':'Boston','nets':'Brooklyn','hornets':'Charlotte','bulls':'Chicago','cavaliers':'Cleveland','cavs':'Cleveland','mavericks':'Dallas','mavs':'Dallas','nuggets':'Denver','pistons':'Detroit','warriors':'Golden State',
 'rockets':'Houston','pacers':'Indiana','clippers':'Los Angeles C','lakers':'Los Angeles L','grizzlies':'Memphis','heat':'Miami','bucks':'Milwaukee','timberwolves':'Minnesota','wolves':'Minnesota','pelicans':'New Orleans','knicks':'New York',
 'thunder':'Oklahoma City','magic':'Orlando','76ers':'Philadelphia','sixers':'Philadelphia','suns':'Phoenix','blazers':'Portland','trail blazers':'Portland','kings':'Sacramento','spurs':'San Antonio','raptors':'Toronto','jazz':'Utah','wizards':'Washington'}
NFLC={'cardinals':'Arizona','falcons':'Atlanta','ravens':'Baltimore','bills':'Buffalo','panthers':'Carolina','bears':'Chicago','bengals':'Cincinnati','browns':'Cleveland','cowboys':'Dallas','broncos':'Denver','lions':'Detroit','packers':'Green Bay',
 'texans':'Houston','colts':'Indianapolis','jaguars':'Jacksonville','chiefs':'Kansas City','raiders':'Las Vegas','chargers':'Los Angeles C','rams':'Los Angeles R','dolphins':'Miami','vikings':'Minnesota','patriots':'New England','saints':'New Orleans',
 'giants':'New York G','jets':'New York J','eagles':'Philadelphia','steelers':'Pittsburgh','49ers':'San Francisco','niners':'San Francisco','seahawks':'Seattle','buccaneers':'Tampa Bay','bucs':'Tampa Bay','titans':'Tennessee','commanders':'Washington'}
GSER={'NBA':'KXNBAGAME','NFL':'KXNFLGAME','NHL':'KXNHLGAME','CBB':'KXNCAAMBGAME','NCAAB':'KXNCAAMBGAME','CFB':'KXNCAAFGAME','NCAAF':'KXNCAAFGAME'}
for p in P:
  if p.get('market')!='ml' or p.get('sport') not in GSER: continue
  t=strip(p['pick_text']); side=re.split(r'\sml\b',t)[0].strip()
  side=re.sub(r'^(la|ny|phx)\s','',side)
  ms=IDX.get((GSER[p['sport']],p['slate_date']),[])
  lab=None
  M=CITY if p['sport']=='NBA' else NFLC if p['sport']=='NFL' else {}
  for k,v in M.items():
    if re.search(r'\b'+k+r'\b',side): lab=v;break
  if lab is None and p['sport'] in M.__class__.__name__: pass
  side2=re.split(r'\s(?:v|vs|at|@)\s',side)[0].strip(); side2=re.sub(r'\(.*?\)','',side2).strip()
  cand=[m for m in ms if (lab and m['yes_sub_title']==lab) or (not lab and p['sport'] not in ('NBA','NFL') and strip(m['yes_sub_title']).replace('.','')==side2.replace('.',''))]
  if lab=='Los Angeles C' and p['sport']=='NBA' and not cand: pass
  evs={m['event_ticker'] for m in cand}
  if len(evs)==1:
    m=cand[0]; p['k_match']={'ticker':m['ticker'],'series':GSER[p['sport']],'event':m['event_ticker'],'name':m['yes_sub_title'],'result':m['result'],'invert':False}; stats['ml matched']+=1
  else: stats['ml unmatched']+=1; fails.append((p['slate_date'],p['pick_text'],'ML',lab,len(evs)))
json.dump(P,open('audit/picks.json','w'))
print(dict(stats))
for f in fails[:60]: print(f)
