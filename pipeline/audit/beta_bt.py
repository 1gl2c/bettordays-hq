import json,math,random
P=json.load(open('audit/picks2.json'));K=json.load(open('audit/kprice_cache.json'))
G=[p for p in P if p['status']=='graded' and p['result'] in('W','L') and p.get('k_tip') is not None and p.get('k_interp') is False]
for p in G:
  p['hit']=p['result']=='W'
  c=K.get(p['k_ticker'],{})
  e=c.get('early_mid')
  if e is not None and p['k_match']['invert']: e=100-e
  p['k_early']=e
fee=lambda q:0.07*q*(1-q)       # Kalshi taker fee per $1 contract, q = price 0-1
def roi(rs,price='k_tip'):
  rs=[p for p in rs if p.get(price) is not None]
  if not rs: return (0,None,None)
  r=[ (1/(p[price]/100+fee(p[price]/100)))*p['hit']-1 for p in rs]
  m=sum(r)/len(r); sd=(sum((x-m)**2 for x in r)/max(1,len(r)-1))**.5
  return (len(rs),round(100*m,1),round(100*1.96*sd/math.sqrt(len(rs)),1))
def hr(rs): return f"{sum(p['hit'] for p in rs)}-{len(rs)-sum(p['hit'] for p in rs)}"
near=lambda p:50<=p['k_tip']<=60   # +100 to -150
train=[p for p in G if p['slate_date']<='2026-11-12'];test=[p for p in G if p['slate_date']>='2026-11-13']
print('legs with exact Kalshi price',len(G),'train',len(train),'test',len(test))
print('near-even (+100 to -150) all:',hr([p for p in G if near(p)]),roi([p for p in G if near(p)]))
# A. our grade above price by >= t
for t in (0,5,8,12):
  for lab,rs in (('train',train),('test',test)):
    s=[p for p in rs if near(p) and p['grade']>=p['k_tip']+t]
    print(f'A ours>=price+{t:<2} {lab}',hr(s),roi(s))
# E. market-anchored blend: est = k + w*(ours-k); choose w on train maximizing log-score
def ll(rs,w):
  t=0
  for p in rs:
    q=min(.97,max(.03,(p['k_tip']+w*(p['grade']-p['k_tip']))/100)); t+=math.log(q if p['hit'] else 1-q)
  return t/len(rs)
ws=[i/20 for i in range(0,21)]
best=max(ws,key=lambda w:ll(train,w)); print('E best blend weight on our grade (train):',best,' train ll',round(ll(train,best),4),' w=0',round(ll(train,0),4),'| test ll w=best',round(ll(test,best),4),' w=0',round(ll(test,0),4),' w=1',round(ll(test,1),4))
# D. line movement early->tip
mv=[p for p in G if p['k_early'] is not None]
print('D legs with early+tip price',len(mv),'median hours early?')
for lab,rs in (('train',[p for p in mv if p['slate_date']<='2026-11-12']),('test',[p for p in mv if p['slate_date']>='2026-11-13'])):
  up=[p for p in rs if p['k_tip']-p['k_early']>=4];dn=[p for p in rs if p['k_tip']-p['k_early']<=-4];fl=[p for p in rs if abs(p['k_tip']-p['k_early'])<4]
  print(' ',lab,'rose 4+',hr(up),roi(up,'k_early'),'| fell 4+',hr(dn),roi(dn,'k_early'),'| flat',hr(fl),roi(fl,'k_early'))
  # buying at early price when it later rose = the value of being early
# C. simple calibrated model check: hit rate vs price buckets (is Kalshi priced fair?)
for lo,hi in ((50,55),(55,60),(60,70),(70,80),(80,95)):
  s=[p for p in G if lo<=p['k_tip']<hi]; print('price',lo,hi,hr(s),'avg price',round(sum(p['k_tip'] for p in s)/len(s),1),'roi',roi(s))
# B. stat-type within near-even
from collections import defaultdict
d=defaultdict(list)
for p in G:
  if near(p): d[p['stat']].append(p)
for k,v in d.items(): print('near-even',k,hr(v),roi(v))
