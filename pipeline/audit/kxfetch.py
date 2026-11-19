import json,time,urllib.request,urllib.parse,os,sys
B='https://api.elections.kalshi.com/trade-api/v2'
SER=sys.argv[1:] or ['KXNBAPTS','KXNBAREB','KXNBAAST','KXNBA3PT','KXNBAPRA','KXNBAGAME','KXNBASPREAD','KXNBATOTAL',
 'KXNFLRECYDS','KXNFLRSHYDS','KXNFLPASSYDS','KXNFLREC','KXNFLANYTD','KXNFLGAME','KXNFLSPREAD','KXNFLTOTAL',
 'KXNHLGAME','KXNHLSPREAD','KXNHLTOTAL','KXNCAAMBGAME','KXNCAAMBSPREAD','KXNCAAMBTOTAL','KXNCAAFGAME','KXNCAAFSPREAD','KXNCAAFTOTAL','KXUFCFIGHT']
lo=int(time.mktime(time.strptime('2026-11-03','%Y-%m-%d'))); hi=int(time.mktime(time.strptime('2026-11-19','%Y-%m-%d')))
def get(u):
  for a in range(8):
    try:
      with urllib.request.urlopen(u,timeout=40) as r: return json.load(r)
    except urllib.error.HTTPError as e:
      if e.code==429: time.sleep(2+a*2); continue
      if e.code==404: return {}
      time.sleep(2)
    except Exception: time.sleep(2)
  return {}
for s in SER:
  fn=f'audit/kx/{s}.json'
  if os.path.exists(fn): continue
  out=[];cur=''
  while True:
    q={'series_ticker':s,'status':'settled','min_close_ts':lo,'max_close_ts':hi,'limit':1000}
    if cur: q['cursor']=cur
    d=get(B+'/markets?'+urllib.parse.urlencode(q))
    ms=d.get('markets',[]) or []
    for m in ms: out.append({k:m.get(k) for k in ('ticker','event_ticker','title','yes_sub_title','result','open_time','close_time','expiration_value','last_price_dollars','previous_price_dollars','volume_fp','volume')})
    cur=d.get('cursor') or ''
    time.sleep(0.35)
    if not cur or not ms: break
  json.dump(out,open(fn,'w')); print(s,len(out),flush=True)
