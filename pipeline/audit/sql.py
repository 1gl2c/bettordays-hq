import json,re
P=json.load(open('audit/picks2.json')); F=json.load(open('audit/fixes.json')); T=json.load(open('audit/tickets.json'))
def q(v):
  if v is None or (isinstance(v,float) and v!=v): return 'null'
  if isinstance(v,bool): return 'true' if v else 'false'
  if isinstance(v,(int,float)): return repr(v)
  if isinstance(v,list): return "array["+",".join(q(x) for x in v)+"]::text[]" if v else "'{}'::text[]"
  return "'"+str(v).replace("'","''")+"'"
cols=['pick_key','slate_date','game_time_text','sport','event','player','market','stat','direction','line','line_style','pick_text','moved','added_by_model','grade','grade_version','matchup','b2b','notes','kalshi_ticker','kalshi_price_grade','kalshi_price_grade_ts','kalshi_price_close','kalshi_price_close_ts','kalshi_result','result','actual','result_source','status','data_source','data_gaps']
rows=[]
fk={f['pick_key'] for f in F}
for p in P:
  gaps=list(p.get('data_gaps') or [])
  if p.get('k_interp'): gaps.append('Kalshi price interpolated between the two nearest Kalshi lines')
  if p.get('k_tip') is None and p['status']=='graded': gaps.append('no matching Kalshi market found')
  km=p.get('k_match') or {}
  ev=p.get('event') or km.get('event')
  act=p.get('actual')
  try: act=float(act) if act not in (None,'') else None
  except: act=None
  added=bool(re.search(r'added by us|not on (your|the cappers)',(p.get('notes') or ''),re.I))
  v=[p['pick_key'],p['slate_date'],p.get('game_time_text'),p.get('sport'),ev,p.get('player'),p.get('market'),p.get('stat'),p.get('direction'),p.get('line'),p.get('line_style'),p['pick_text'],
     p.get('x_moved') if isinstance(p.get('x_moved'),bool) else (bool(p['x_moved']) if p.get('x_moved') is not None else None),added,p.get('grade'),p.get('grade_version'),p.get('x_mu') or None,
     bool(p['x_b2b']) if p.get('x_b2b') is not None else None,p.get('notes'),p.get('k_ticker'),
     int(round(p['k_grade'])) if p.get('k_grade') is not None else None,p.get('k_grade_ts'),
     int(round(p['k_tip'])) if p.get('k_tip') is not None else None,p.get('k_tip_ts'),p.get('k_result'),p.get('result'),act,
     ('corrected Nov 18 2026 from box score' if p['pick_key'] in fk else 'BettorDays grading from box scores') if p['status']=='graded' else None,
     p['status'],p.get('data_source'),gaps]
  rows.append('('+','.join(q(x) for x in v)+')')
up=','.join(f'{c}=excluded.{c}' for c in cols if c!='pick_key')+',updated_at=now()'
chunks=[rows[i:i+400] for i in range(0,len(rows),400)]
for i,c in enumerate(chunks):
  open(f'audit/load_{i}.sql','w').write(f"insert into public.model_picks ({','.join(cols)}) values\n"+",\n".join(c)+f"\non conflict (pick_key) do update set {up};")
fx="insert into public.model_pick_corrections (pick_id,field,old_value,new_value,reason,corrected_at) select id,v.f,v.o,v.n,v.r,'2026-11-18T22:00:00Z' from public.model_picks m join (values "+",".join(f"({q(f['pick_key'])},{q(f['field'])},{q(f['old'])},{q(f['new'])},{q(f['reason'])})" for f in F)+") v(k,f,o,n,r) on m.pick_key=v.k where not exists (select 1 from public.model_pick_corrections c where c.pick_id=m.id and c.field=v.f);"
tk="insert into public.model_tickets (slate_date,name,legs,played,result) values "+",".join(f"({q(t['slate_date'])},{q(t['name'])},{q(t['legs'])},{q(t['played'])},{q(t.get('result'))})" for t in T)+" on conflict (slate_date,name) do update set legs=excluded.legs,played=excluded.played,result=excluded.result;"
open('audit/load_fix.sql','w').write(fx+"\n"+tk)
print(len(chunks),[len(open(f'audit/load_{i}.sql').read()) for i in range(len(chunks))],len(fx+tk))
