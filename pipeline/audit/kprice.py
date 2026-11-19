import json,subprocess,time,os
from datetime import datetime,timedelta,timezone
from concurrent.futures import ThreadPoolExecutor
P=json.load(open('audit/picks.json'))
CF='audit/kprice_cache.json'
cache=json.load(open(CF)) if os.path.exists(CF) else {}
B='https://api.elections.kalshi.com/trade-api/v2'
def curl(u):
  for i in range(6):
    r=subprocess.run(['curl','-s','-m','25',u],capture_output=True,text=True).stdout
    try:
      d=json.loads(r)
      if 'error' in d and 'too_many' in str(d['error']): time.sleep(1.5+i); continue
      return d
    except Exception: time.sleep(1.5)
  return {}
def price(tk):
  if tk in cache: return cache[tk]
  ser=tk.split('-')[0]
  m=curl(f'{B}/markets/{tk}').get('market',{})
  le=m.get('latest_expiration_time'); 
  if not le: cache[tk]={'err':'no market'}; return cache[tk]
  tip=datetime.fromisoformat(le.replace('Z','+00:00'))-timedelta(days=2)
  op=datetime.fromisoformat(m['open_time'].replace('Z','+00:00'))
  a=int(min(tip-timedelta(hours=8),op).timestamp()); b=int(tip.timestamp())
  c=curl(f'{B}/series/{ser}/markets/{tk}/candlesticks?start_ts={a}&end_ts={b}&period_interval=60').get('candlesticks',[])
  out={'tip':tip.isoformat(),'open':m['open_time'],'result':m.get('result')}
  for x in reversed(c):
    yb=(x.get('yes_bid') or {}).get('close_dollars');ya=(x.get('yes_ask') or {}).get('close_dollars')
    if yb is not None and ya is not None and float(ya)>0:
      yb,ya=float(yb),float(ya)
      out['mid']=round(100*(yb+ya)/2,1); out['spread']=round(100*(ya-yb),1); out['ts']=datetime.fromtimestamp(x['end_period_ts'],timezone.utc).isoformat(); break
  # earliest quoted price (closest to when a board would be built) 
  for x in c:
    yb=(x.get('yes_bid') or {}).get('close_dollars');ya=(x.get('yes_ask') or {}).get('close_dollars')
    if yb is not None and ya is not None and float(ya)>0 and float(ya)-float(yb)<=0.15:
      out['early_mid']=round(100*(float(yb)+float(ya))/2,1); out['early_ts']=datetime.fromtimestamp(x['end_period_ts'],timezone.utc).isoformat(); break
  cache[tk]=out; time.sleep(0.15); return out
tks=set()
for p in P:
  k=p.get('k_match')
  if not k: continue
  if 'ticker' in k: tks.add(k['ticker'])
  for t in k.get('interp',[]): tks.add(t)
tks=sorted(tks); print('tickers',len(tks),'cached',sum(t in cache for t in tks),flush=True)
with ThreadPoolExecutor(4) as ex:
  for i,_ in enumerate(ex.map(price,tks)):
    if i%100==0: json.dump(cache,open(CF,'w')); print(i,flush=True)
json.dump(cache,open(CF,'w')); print('done',sum('mid' in cache[t] for t in tks))
