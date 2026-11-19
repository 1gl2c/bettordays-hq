import json,math
from collections import defaultdict
O=json.load(open('audit/kprops.json'))
for o in O:
  o['raw']=o['pct']
  if 'pulled toward the market' in o['note'] or 'pulled up toward' in o['note']: o['raw']=max(1,min(99,2*o['pct']-o['k']))
  o['hit']=1 if o['r']=='W' else 0
  o['gap']=o['raw']-o['k']
def wil(h,n):
  if n==0: return (0,0)
  z=1.96;p=h/n;d=1+z*z/n;c=p+z*z/(2*n);m=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n));return (round(100*(c-m)/d),round(100*(c+m)/d))
def summ(rows,label):
  n=len(rows)
  if not n: return
  h=sum(o['hit'] for o in rows);ar=sum(o['raw'] for o in rows)/n;ak=sum(o['k'] for o in rows)/n
  lo,hi=wil(h,n)
  print(f"{label:38s} n={n:3d} hit {h}/{n} = {round(100*h/n):3d}% (95% range {lo}-{hi})  avg ours {ar:4.1f}  avg Kalshi {ak:4.1f}")
def bucket(o): return 'ours 8+ above Kalshi' if o['gap']>=8 else ('Kalshi 8+ above ours' if o['gap']<=-8 else 'within 7')
print('=== ALL PROPS WITH A KALSHI PRICE (Nov 16-17)')
summ(O,'all')
for b in ['ours 8+ above Kalshi','within 7','Kalshi 8+ above ours']: summ([o for o in O if bucket(o)==b],b)
print('\n=== by sport x bucket')
for sp in ('NBA','NFL'):
  for b in ['ours 8+ above Kalshi','within 7','Kalshi 8+ above ours']: summ([o for o in O if o['sp']==sp and bucket(o)==b],f'{sp} | {b}')
print('\n=== by stat x bucket (NBA)')
for st in ('points','rebounds','assists','threes','points + rebounds + assists'):
  for b in ['ours 8+ above Kalshi','within 7','Kalshi 8+ above ours']: summ([o for o in O if o['sp']=='NBA' and o['stat']==st and bucket(o)==b],f'{st[:10]} | {b}')
print('\n=== by our grade range x bucket')
for lo,hi in ((80,101),(70,80),(60,70),(0,60)):
  for b in ['ours 8+ above Kalshi','within 7','Kalshi 8+ above ours']: summ([o for o in O if lo<=o['raw']<hi and bucket(o)==b],f'ours {lo}-{hi-1} | {b}')
print('\n=== by day x bucket')
for d in ('Nov 16','Nov 17'):
  for b in ['ours 8+ above Kalshi','within 7','Kalshi 8+ above ours']: summ([o for o in O if o['day']==d and bucket(o)==b],f'{d} | {b}')
print('\n=== other splits (all props)')
summ([o for o in O if o['under']],'unders');summ([o for o in O if o['b2b']],'back-to-back');summ([o for o in O if o['mu']=='good'],'good matchup');summ([o for o in O if o['mu']=='bad'],'bad matchup');summ([o for o in O if o['moved']],'moved or converted lines');summ([o for o in O if not o['moved']],'capper lines as sent')
# accuracy
def brier(key): return sum((o[key]/100-o['hit'])**2 for o in O)/len(O)
def cl(x): return max(.01,min(.99,x/100))
def ll(key): return -sum((math.log(cl(o[key])) if o['hit'] else math.log(1-cl(o[key]))) for o in O)/len(O)
print('\n=== who predicted better (lower is better)')
print('Brier: ours',round(brier('raw'),3),' Kalshi',round(brier('k'),3))
print('LogLoss: ours',round(ll('raw'),3),' Kalshi',round(ll('k'),3))
blend=[dict(o,bl=(o['raw']+o['k'])/2) for o in O]
print('Brier blend 50/50',round(sum((o['bl']/100-o['hit'])**2 for o in blend)/len(blend),3))
# calibration tables
print('\n=== calibration: predicted vs actual')
for key in ('raw','k'):
  for lo,hi in ((80,101),(70,80),(60,70),(50,60),(0,50)):
    b=[o for o in O if lo<=o[key]<hi];
    if b: print(key,f'{lo}-{hi-1}',len(b),'pred',round(sum(o[key] for o in b)/len(b)),'actual',round(100*sum(o['hit'] for o in b)/len(b)))
# movement
C=[o for o in O if 'close' in o]
print('\n=== line movement grade-time -> tip-off (n with close price:',len(C),')')
mv=[o['close']-o['k'] for o in C];print('avg move',round(sum(mv)/len(mv),1),'moved 5+ toward us',sum(1 for o in C if (o['close']-o['k'])*(1 if o['gap']>0 else -1)>=5),'moved 5+ away from us',sum(1 for o in C if (o['close']-o['k'])*(1 if o['gap']>0 else -1)<=-5))
summ([o for o in C if o['close']-o['k']>=5],'Kalshi price rose 5+ before tip');summ([o for o in C if o['close']-o['k']<=-5],'Kalshi price fell 5+ before tip');summ([o for o in C if abs(o['close']-o['k'])<5],'Kalshi price steady')
print('Brier close Kalshi',round(sum((o['close']/100-o['hit'])**2 for o in C)/len(C),3),' open Kalshi same set',round(sum((o['k']/100-o['hit'])**2 for o in C)/len(C),3),' ours same set',round(sum((o['raw']/100-o['hit'])**2 for o in C)/len(C),3))
json.dump(O,open('audit/O.json','w'))
