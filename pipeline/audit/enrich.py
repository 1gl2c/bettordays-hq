import json,re
from datetime import datetime
P=json.load(open('audit/picks.json')); K=json.load(open('audit/kprice_cache.json'))
GT={'2026-11-16':'2026-11-16T23:28:23+00:00','2026-11-17':'2026-11-17T23:04:52+00:00'}
CORR={  # verified against ESPN box scores on Nov 18
 '2026-11-13|alperensengunover5assists':('result','W','P','Exactly 5 assists on a whole-number line (over 5). That is a push, not a win. ESPN box score.'),
 '2026-11-11|juliusrandleover5assists':('result','W','P','Exactly 5 assists on over 5. Push. ESPN box score.'),
 '2026-11-11|jeremiahfearsover5assists':('result','W','P','Exactly 5 assists on over 5. Push. ESPN box score.'),
 '2026-11-04|herrou25pts':('result','L','P','Exactly 25 points on under 25. Push. Nov 4 recap ledger.'),
 '2026-11-04|dameu5ast':('result','L','P','Exactly 5 assists on under 5. Push. Nov 4 recap ledger.'),
 '2026-11-10|donovanclinganunder13rebounds':('result','L','P','Exactly 13 rebounds on under 13. Push. ESPN box score.'),
 '2026-11-10|karlanthonytownsunder2threesmade':('result','L','P','Exactly 2 threes on under 2. Push. ESPN box score.'),
 '2026-11-16|jakobilaneunder3receptions':('result','L','P','Exactly 3 catches on under 3. Push. ESPN box score.'),
 '2026-11-04|kingsml':('sport','NBA','NHL','This was the LA Kings (NHL, won 7-2), logged as NBA.'),
}
fixes=[]
for p in P:
  c=CORR.get(p['pick_key'])
  if c:
    f,old,new,why=c
    assert str(p.get(f))==old,(p['pick_key'],p.get(f))
    p[f]=new; fixes.append({'pick_key':p['pick_key'],'field':f,'old':old,'new':new,'reason':why})
    if f=='sport': p.pop('k_match',None)
  k=p.get('k_match')
  p['k_tip']=None
  if k:
    if 'ticker' in k:
      c=K.get(k['ticker'],{})
      if 'mid' in c: v=c['mid']; p['k_tip_ts']=c['ts']; p['k_spread']=c['spread']; p['k_ticker']=k['ticker']; p['k_interp']=False
      else: v=None
    else:
      a,b=[K.get(t,{}) for t in k['interp']]; lo,hi=k['interp_thr']
      if 'mid' in a and 'mid' in b:
        w=(p['threshold']-lo)/(hi-lo); v=a['mid']+(b['mid']-a['mid'])*w; p['k_tip_ts']=b['ts']; p['k_spread']=max(a['spread'],b['spread']); p['k_ticker']=' / '.join(k['interp']); p['k_interp']=True
      else: v=None
    if v is not None:
      if k['invert']: v=100-v
      p['k_tip']=round(v,1)
    p['k_result']=k.get('result')
  # grading-time Kalshi (board column), Nov 16-17 only
  if p.get('x_k') is not None and p['slate_date'] in GT:
    p['k_grade']=p['x_k']; p['k_grade_ts']=GT[p['slate_date']]
  if p['slate_date']=='2026-11-16' and 'pulled' in (p.get('notes') or '') and 'market' in (p.get('notes') or ''): p['grade_version']='v8 (pulled toward Kalshi, later withdrawn)'
  else: p['grade_version']={'2026-11-16':'v7+','2026-11-17':'v7 original'}.get(p['slate_date'],'v1-v7 (pre-audit)')
json.dump(P,open('audit/picks2.json','w')); json.dump(fixes,open('audit/fixes.json','w'))
g=[p for p in P if p['status']=='graded']
print('graded',len(g),'pushes',sum(p['result']=='P' for p in g),'with tip price',sum(p['k_tip'] is not None for p in g),'exact',sum(p.get('k_interp') is False and p['k_tip'] is not None for p in g),'wide spread>20',sum((p.get('k_spread') or 0)>20 for p in g if p['k_tip'] is not None))
from collections import Counter
print(Counter(p['slate_date'] for p in g if p['k_tip'] is not None))
