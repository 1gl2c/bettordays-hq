import json,re,subprocess,datetime,unicodedata
from concurrent.futures import ThreadPoolExecutor
def nrm(s): return unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode().lower().replace('.','').replace("'",'').strip()
def ts(s): return int(datetime.datetime.fromisoformat(s.replace('Z','+00:00')).timestamp())
out=[]
for day,d,dt in (('Nov 16','mon','26NOV16'),('Nov 17','tue','26NOV17')):
  K=json.load(open(f'{d}/kalshi.json'));R=json.load(open(f'{d}/{d}_graded.json'))
  SB=json.load(open(f'{d}/nba_sb.json'));tips={}
  for e in SB['events']:
    c=e['competitions'][0];ab=[t['team']['abbreviation'] for t in c['competitors']]
    for a in ab: tips[a]=e['date']
  idx={}
  for s,ms in K.items():
    for m in ms:
      if dt not in m['event_ticker']: continue
      mm=re.match(r'(.+?): (\d+)\+',m['title'] or '')
      if mm: idx[(nrm(mm.group(1)),s,int(mm.group(2)))]=(m['ticker'],s,m['event_ticker'])
  SER={'points':'KXNBAPTS','rebounds':'KXNBAREB','assists':'KXNBAAST','threes':'KXNBA3PT','points + rebounds + assists':'KXNBAPRA','receiving yards':'KXNFLRECYDS','rushing yards':'KXNFLRSHYDS','passing yards':'KXNFLPASSYDS','receptions':'KXNFLREC'}
  for r in R:
    if not r.get('r') or r['ty']!='prop' or r.get('k') is None: continue
    m=re.match(r"(.+?) (under )?(\d+)\+? (.+)$",r['p'])
    if not m: continue
    name,und,k,stat=m.group(1),m.group(2),int(m.group(3)),m.group(4)
    s=SER.get(stat)
    key=(nrm(name),s,k)
    if key not in idx: continue
    out.append(dict(day=day,p=r['p'],pct=r['pct'],k=r['k'],r=r['r'],under=bool(und),sp=r['sp'],stat=stat,mu=r.get('mu',''),b2b=r.get('b2b',0),moved=r.get('moved',False),ticker=idx[key][0],series=s,g=r['g'],note=r['n']))
def close(o):
  try:
    team=o['g'].split('@')[1]; 
    SB=json.load(open(('mon' if o['day']=='Nov 16' else 'tue')+'/nba_sb.json'))
    tip=None
    for e in SB['events']:
      if team in [t['team']['abbreviation'] for t in e['competitions'][0]['competitors']]: tip=ts(e['date'])
    if tip is None: return o
    a=tip-6*3600;b=tip
    r=subprocess.run(['curl','-s','-m','25',f"https://api.elections.kalshi.com/trade-api/v2/series/{o['series']}/markets/{o['ticker']}/candlesticks?start_ts={a}&end_ts={b}&period_interval=60"],capture_output=True,text=True).stdout
    c=json.loads(r).get('candlesticks',[])
    for x in reversed(c):
      yb=x.get('yes_bid',{}).get('close_dollars');ya=x.get('yes_ask',{}).get('close_dollars')
      if yb and ya:
        v=round(100*(float(yb)+float(ya))/2); o['close']=100-v if o['under'] else v;break
  except Exception as e: o['err']=str(e)
  return o
with ThreadPoolExecutor(10) as ex: out=list(ex.map(close,out))
json.dump(out,open('audit/kprops.json','w'))
print(len(out),sum('close' in o for o in out))
print(out[0])
