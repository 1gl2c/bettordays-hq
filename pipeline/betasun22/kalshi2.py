import json,subprocess,urllib.parse
from concurrent.futures import ThreadPoolExecutor
SER=['KXNBAPTS','KXNBAREB','KXNBAAST','KXNBA3PT','KXNBAPRA']
def get(s):
  out=[];cur=''
  for _ in range(12):
    u=f"https://api.elections.kalshi.com/trade-api/v2/markets?series_ticker={s}&status=open&limit=1000"+(f"&cursor={urllib.parse.quote(cur)}" if cur else '')
    r=subprocess.run(['curl','-s','-m','40',u],capture_output=True,text=True).stdout
    try: d=json.loads(r)
    except Exception: break
    out+=d.get('markets',[]);cur=d.get('cursor')
    if not cur or not d.get('markets'): break
  return s,[{k:m.get(k) for k in ('ticker','event_ticker','title','yes_sub_title','no_sub_title','yes_bid_dollars','yes_ask_dollars','last_price_dollars','volume','close_time','expected_expiration_time')} for m in out]
with ThreadPoolExecutor(8) as ex: K=dict(ex.map(get,SER))
json.dump(K,open('betasun22/kalshi2.json','w'))
for s,m in K.items():
  ev=sorted(set(x['event_ticker'] for x in m))
  print(s,len(m),[e for e in ev if '26NOV22' in e][:12])
