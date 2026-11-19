import json,subprocess,datetime
from concurrent.futures import ThreadPoolExecutor
def cu(u):
  for _ in range(3):
    try: return json.loads(subprocess.run(['curl','-s','-m','30',u],capture_output=True,text=True).stdout)
    except Exception: pass
  return {}
days=[(datetime.date(2026,10,20)+datetime.timedelta(d)).strftime('%Y%m%d') for d in range(0,30)]
def sb(d): return [e['id'] for e in cu(f'https://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard?dates={d}').get('events',[]) if e['status']['type']['completed']]
with ThreadPoolExecutor(10) as ex: ids=sorted({i for l in ex.map(sb,days) for i in l})
def box(i):
  s=cu(f'https://site.api.espn.com/apis/site/v2/sports/basketball/nba/summary?event={i}')
  out=[]
  sc={c['team']['abbreviation']:c.get('score') for c in s.get('header',{}).get('competitions',[{}])[0].get('competitors',[])}
  for t in s.get('boxscore',{}).get('teams',[]):
    st={x['name']:x.get('displayValue') for x in t.get('statistics',[])}
    st['points']=sc.get(t['team']['abbreviation'])
    out.append((t['team']['abbreviation'],st))
  return out
with ThreadPoolExecutor(12) as ex: B=list(ex.map(box,ids))
allowed={}
for g in B:
  if len(g)!=2: continue
  for k in (0,1):
    me,_=g[k];_,op=g[1-k]
    def num(x):
      try: return float(str(x).split('-')[0])
      except: return 0
    a=allowed.setdefault(me,{'pts':[],'reb':[],'ast':[],'3pm':[]})
    a['pts'].append(num(op.get('points') or 0)); a['reb'].append(num(op.get('totalRebounds'))); a['ast'].append(num(op.get('assists'))); a['3pm'].append(num(op.get('threePointFieldGoalsMade-threePointFieldGoalsAttempted')))
print(len(ids),'games',len(allowed),'teams', list(B[0][0][1].keys())[:30] if B and B[0] else '')

OPP={}
import statistics as S
for k in ('pts','reb','ast','3pm'):
  avg={t:round(S.mean(v[k]),1) for t,v in allowed.items()}
  order=sorted(avg,key=lambda t:avg[t])
  for i,t in enumerate(order): OPP.setdefault(t,{})[k]=[avg[t],i+1,len(allowed[t][k])]
json.dump(OPP,open('wed/nba_opp.json','w'))
for t in sorted(OPP): print(t,OPP[t])
