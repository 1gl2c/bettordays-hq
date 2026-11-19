import json,re,os,math
C=json.load(open('audit/consts.json'))
R=C['ROWS']
DM={'SUN':'Nov 8','MON':'Nov 9','TUE':'Nov 10','WED':'Nov 11','THU':'Nov 12','FRI':'Nov 13','SAT':'Nov 14','SN15':'Nov 15','MN16':'Nov 16','TU17':'Nov 17'}
TIXK={'Nov 8':'TIX','Nov 9':'MTIX','Nov 10':'TTIX','Nov 11':'WTIX','Nov 12':'HTIX','Nov 13':'FTIX','Nov 14':'STIX','Nov 15':'SUTIX','Nov 16':'MNTIX','Nov 17':'TUTIX'}
def nz(s): return re.sub(r'[^a-z0-9+.]','',s.lower())
def iso(d): return '2026-11-%02d'%int(d.split()[1])
# graded files with extra fields (k, act, mu, b2b, moved)
EXTRA={}
for d,f in [('Nov 16','mon/mon_graded.json'),('Nov 17','tue/tue_graded.json'),('Nov 15','sun/sun_graded.json'),('Nov 14','sat/sat_graded.json'),('Nov 13','fri/fri_graded.json'),('Nov 12','study/nov12_graded.json'),('Nov 10','study/nov10_graded.json'),('Nov 9','nov9_graded.json')]:
  if os.path.exists(f):
    for x in json.load(open(f)):
      if isinstance(x,dict) and 'p' in x: EXTRA[(d,nz(x['p']))]=x
# Nov 4 recap ledger: [pick, team, est, actual, hit, ?, dir]
s=open('nov4-recap.html').read(); i=s.index('L=[')+2; L4,_=json.JSONDecoder().raw_decode(s[i:])
N4={nz(x[0]):x for x in L4}
B={}
for k,d in DM.items():
  for x in C[k]: B[(d,nz(x['p']))]=x
STATW=[('points + rebounds + assists','pra'),('pts + reb + ast','pra'),('pra','pra'),('p+r+a','pra'),('rebounds','reb'),('rebound','reb'),('reb','reb'),('assists','ast'),('assist','ast'),('ast','ast'),
 ('3 pointers','3pm'),('three','3pm'),('3pm','3pm'),('3pt','3pm'),('points','pts'),('point','pts'),('pts','pts'),('receiving yards','recyds'),('rec yds','recyds'),('rushing yards','rush'),('rush yds','rush'),('rush','rush'),('passing yards','pass'),('pass yds','pass'),('receptions','rec'),('rec','rec'),('sog','sog'),('blocks','blk')]
def parse(text,row):
  t=text.lower().replace('(-105)','').replace('(-110)','')
  out={'direction':row['dir'],'stat':row['stat'],'line':None,'threshold':None,'player':None}
  if row['mkt'] in ('prop',) or row['stat'] in ('pts','reb','ast','3pm','pra','recyds','rush','pass','rec','prop'):
    st=None
    for w,c in STATW:
      if re.search(r'(?<![a-z])'+re.escape(w)+r'(?![a-z])',t): st=c;break
    if re.search(r'pts \+ reb|points \+ rebounds(?! \+)|points \+ assists|pts \+ ast|rebounds \+ assists|pts\+reb|rush \+ rec|rushing \+ receiving',t): out['stat']='combo'
    elif st: out['stat']=st
    m=re.search(r'(\d+(?:\.\d)?)\s*\+',t)
    if m: out['line']=float(m.group(1)); out['threshold']=int(float(m.group(1))); out['direction']='o'
    else:
      m=re.search(r'(?:^|\s)(o|u|over|under)\s*(\d+(?:\.\d)?)',t)
      if m:
        x=float(m.group(2)); out['line']=x; dirn='u' if m.group(1) in ('u','under') else 'o'; out['direction']=dirn
        if dirn=='o': out['threshold']=math.floor(x)+1
        else: out['threshold']=math.ceil(x) if x%1 else int(x)   # under X: v<X  -> NOT (thr+)
    nm=re.split(r'\s(?:o|u|over|under|\d)',text,maxsplit=1,flags=re.I)[0].strip()
    nm=re.sub(r'\s(ATD|ML|KO.*|double double)$','',nm,flags=re.I).strip()
    out['player']=nm
  return out
P=[]
for r in R:
  d=r['day']; key=(d,nz(r['pick'])); b=B.get(key,{}); e=EXTRA.get(key,{})
  gaps=[]
  rec={'pick_key':iso(d)+'|'+nz(r['pick']),'slate_date':iso(d),'pick_text':r['pick'],'sport':r['sport'],'market':r['mkt'],
       'line_style':r['style'],'grade':r['est'],'result':'W' if r['hit'] else 'L','status':'graded'}
  rec.update({k:v for k,v in parse(r['pick'],r).items()})
  if b:
    rec['event']=b.get('g'); rec['game_time_text']=b.get('t'); rec['notes']=re.sub('<[^>]+>','',b.get('n') or '')[:600]
    rec['data_source']='site board '+[k for k,v in DM.items() if v==d][0]
    if b.get('pct')!=r['est']: rec['board_grade']=b.get('pct')
  elif d=='Nov 4' and nz(r['pick']) in N4:
    x=N4[nz(r['pick'])]; rec['event']=x[1]+' (team)'; rec['actual']=x[3]; rec['data_source']='Nov 4 recap ledger'
  else:
    rec['data_source']='recap ledger (study/data.py)'
  for kk in ('k','act','mu','b2b','moved','sp'):
    v=e.get(kk) if kk in e else b.get(kk)
    if v is not None: rec['x_'+kk]=v
  if 'x_act' in rec and rec.get('actual') is None:
    try: rec['actual']=float(re.sub(r'[^0-9.\-]','',str(rec['x_act'])) or 'nan')
    except: pass
  if not rec.get('event'): gaps.append('event')
  if not rec.get('game_time_text'): gaps.append('game time')
  if rec.get('actual') is None: gaps.append('actual stat')
  if not rec.get('notes'): gaps.append('grading notes')
  gaps.append('grading timestamp')
  rec['data_gaps']=gaps
  P.append(rec)
# ungraded board legs
seen={p['pick_key'] for p in P}
for k,d in DM.items():
  for b in C[k]:
    pk=iso(d)+'|'+nz(b['p'])
    if pk in seen: continue
    seen.add(pk)
    P.append({'pick_key':pk,'slate_date':iso(d),'pick_text':b['p'],'sport':b.get('sp'),'market':b.get('ty'),'line_style':b.get('st'),'grade':b.get('pct'),
      'event':b.get('g'),'game_time_text':b.get('t'),'notes':re.sub('<[^>]+>','',b.get('n') or '')[:600],'result':None,'status':'ungraded','data_source':'site board '+k,
      'data_gaps':['result never recorded','grading timestamp']})
# tickets
T=[]
for d,k in TIXK.items():
  for t in C.get(k,[]) or []:
    if isinstance(t,dict) and t.get('legs'): T.append({'slate_date':iso(d),'name':re.sub('<[^>]+>','',t.get('t',''))[:80],'legs':t['legs'],'played':'PLAYED' in t.get('t','').upper(),'result':t.get('res')})
json.dump(P,open('audit/picks.json','w')); json.dump(T,open('audit/tickets.json','w'))
from collections import Counter
print(len(P),Counter(p['status'] for p in P),len(T))
print(Counter(p['data_source'].split(' SUN')[0][:30] for p in P))
g=[p for p in P if p['status']=='graded']
print('no threshold among props',sum(1 for p in g if p['market']=='prop' and p.get('threshold') is None))
print([p['pick_text'] for p in g if p['market']=='prop' and p.get('threshold') is None][:30])
