import json,subprocess,urllib.parse,datetime
from concurrent.futures import ThreadPoolExecutor
SER=['KXNBAGAME','KXNBASPREAD','KXNBAPTS','KXNBAREB','KXNBAAST','KXNBA3PT','KXNBAPRA','KXNCAAMBGAME']
def get(s):
  out=[];cur=''
  for _ in range(20):
    u=f"https://api.elections.kalshi.com/trade-api/v2/markets?series_ticker={s}&status=open&limit=1000"+(f"&cursor={urllib.parse.quote(cur)}" if cur else '')
    r=subprocess.run(['curl','-s','-m','40',u],capture_output=True,text=True).stdout
    try: d=json.loads(r)
    except Exception: break
    out+=d.get('markets',[]);cur=d.get('cursor')
    if not cur or not d.get('markets'): break
  return s,[{k:m.get(k) for k in ('ticker','event_ticker','title','yes_sub_title','no_sub_title','yes_bid_dollars','yes_ask_dollars','last_price_dollars','volume')} for m in out]
ts=datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds')
with ThreadPoolExecutor(10) as ex: K=dict(ex.map(get,SER))
json.dump(K,open('tue24/kalshi.json','w'));open('tue24/kalshi_ts.txt','w').write(ts)
for s,m in K.items(): print(s,len(m),len([x for x in m if '26NOV22' in x['event_ticker']]),len([x for x in m if '26NOV24' in x['event_ticker']]))
