import json, sys
sys.path.insert(0,'.')
from nfl import B
R = {
# moneylines / spreads
"Chiefs ML vs Jets":1,"49ers ML vs Raiders":1,"Seahawks ML vs Cardinals":1,"Lions ML at Dolphins":1,
"Seahawks -3":1,"49ers -3":1,"Rams ML at Commanders":1,"Saints ML vs Browns":1,"Patriots ML vs Packers":0,
"Giants ML at Eagles":1,"Panthers +3":0,"Seahawks -8.5":1,"49ers -9.5":1,"Commanders ML":0,"Browns ML":0,
"Colts ML":0,"Bucs ML at Bears":0,
# verified props
"Lamb 50+ rec yds":1,"Geno o200 pass yds":0,"JSN o25.5 longest rec":0,"Shedeur 30+ longest comp":1,
"Shedeur o180 pass yds":1,"Luther Burden 50+ rec yds":1,
"McDaniels 10+ pts":1,"McDaniels o12.5 pts":1,"McDaniels 15+ pts":1,"Fears o3.5 reb":1,"Reaves o3.5 reb":1,
# ATDs from scoring plays
"Gibbs ATD":1,"Walker ATD":1,"J. Taylor ATD":0,"Javonte Williams ATD":1,"St. Brown ATD":0,"JSN ATD":0,
"Rashee Rice ATD":0,"Puka ATD":1,"Saquon ATD":1,"Lamb ATD":1,"Swift ATD":0,"Chuba ATD":0,"Kittle ATD":0,
"Stevenson ATD":1,"Breece Hall ATD":0,"Odunze ATD":1,"Woody Marks ATD":0,"Bowers ATD":1,"Olave ATD":0,
"Tet McMillan ATD":1,"LaPorta ATD":0,"Nabers ATD":0,"Estime ATD":1,"Charbonnet ATD":0,"Jameson Williams ATD":0,
"Christian Watson ATD":1,"Coleman ATD":1,"Worthy ATD":0,"Loveland ATD":0,"Jayden Daniels ATD":0,
"Juwan Johnson ATD":1,"Schultz ATD":0,"D. Robinson ATD":0,"Douglas ATD":0,"Higbee ATD":0,"Barner ATD":1,
"Shedeur ATD":0,"Malik Willis ATD":0,"Flournoy ATD":0,
}
names={b[0] for b in B}
bad=[k for k in R if k not in names]; print('unmatched:',bad)
mk={'ml':'ml','spread':'spread','prop':'prop','atd':'atd','long':'prop'}
rows=[]; pend=[]
for p,pct,g,t,ty,st,n in B:
    if pct==0 or t=='MON': continue
    if p in R:
        rows.append(dict(day='Nov 8',pick=p,est=pct,hit=R[p],sport='NBA' if g=='NBA' else 'NFL',mkt=mk[ty],stat=ty,dir='u' if ' U' in ' '+p.split(' ',1)[-1] and 'U' in p else 'o',style=st,boost=0,star=0,fav=1 if ty=='ml' and pct>=55 else 0))
    else: pend.append((p,pct))
print('graded',len(rows),'pending',len(pend))
h=sum(r['hit'] for r in rows); print('hit',h,len(rows),round(h/len(rows)*100))
def tier(lo,hi):
    s=[r for r in rows if lo<=r['est']<hi]; 
    return (len(s), sum(r['hit'] for r in s), round(sum(r['est'] for r in s)/max(1,len(s))))
for lo,hi in [(80,101),(70,80),(60,70),(50,60),(40,50),(0,40)]: print(lo,hi,tier(lo,hi))
from collections import defaultdict
d=defaultdict(lambda:[0,0])
for r in rows: d[r['mkt']][0]+=1; d[r['mkt']][1]+=r['hit']
print(dict(d))
a=[r for r in rows if r['mkt']=='atd']; print('ATD est avg',sum(r['est'] for r in a)/len(a),'hit',sum(r['hit'] for r in a),len(a))
json.dump(rows,open('nov8.json','w'))
json.dump(pend,open('nov8_pending.json','w'))
print(pend)
