import json
d=json.load(open('study/nov12.json'))
old=json.load(open('study/nov12_graded.json'))['graded']
R={x[2]:x[1] for x in old}
W,L=1,0
R.update({
"Daniss Jenkins over 1.5 3 pointers made":W,"Daniss Jenkins over 0.5 3 pointers made":W,"Malik Nabers 50+ receiving yards":L,"Malik Nabers 50+ receiving yards (2)":L,
"Cam Skattebo 40+ rushing yards":W,"Jayden Daniels 25+ rushing yards":W,"Chigoziem Okonkwo 3+ receptions":W,"Devin Singletary Under 8.5 Longest Rush":W,
"Rachaad White over 54.5 Rush + Rec yards":L,"Chigoziem Okonkwo 20+ receiving yards":W,"Malik Nabers 4+ receptions":W,"Rachaad White 5+ receiving yards":W,
"Rachaad White 25+ rushing yards":W,"Austin Ekeler over 25 rushing yards":W,"Austin Ekeler over 30 rushing yards":L,"Austin Ekeler 40+ Rush Yards (+188)":L,
"Austin Ekeler 60+ Rush Yards (+630)":L,"Anthony Davis 20+ points":W,"Trae Young 15 points":W,"Jayden Daniels o30.5 Pass Att":W,"Malik Nabers o67.5 Rec Yds":L,
"Cam Skattebo o64.5 R+R Yds":W,"Stefon Diggs o3.5 Rec":W,"Joel Embiid 6+ rebounds":L,"Anthony Davis 8+ rebounds":W,"Austin Ekeler 30+ rushing yards":L,
"Chig Okonkwo longest catch over 15 yards":L,"Rachaad White over53.5 Rush + Receiving Yards":L,"Malachi Fields over24.5 Receiving Yards":W,
"Ayo Dosunmu over 15 points":W,"Ayo Dosunmu over 20 points":L,"Ayo Dosunmu over 2 assists":L,"Ayo Dosunmu over 4 assists":L,"Sion James 10+ points":L,
"Utah Mammoth ML":L,"Joel Embiid 20+ points":W,"Joel Embiid 15 + points":W,"Alex Sarr 6+ rebounds":W,"Devin Singletary longest rush under 10 yards":W,
"Cam Skattebo 55+ rushing yards":W,"Came SKattebo 50+ rushing yards":W,"Rachaad White under 3 receptions":W,"Detroit -11, -6, -3, ML  v Wizards":L,
"Okonkwo 2+ rec":W,"Ayo 12+ pts":W,"Skattebo 30+ rush":W,"White 40+ R+R":W,"Ekeler 15+ rush":W,"Sion James 8+ pts":L,"Sarr 5+ reb":W,"AD 15+ pts":W,
})
g=[];miss=[]
for r in d:
  if r['p'] in R: g.append((r['pct'],R[r['p']],r['p'],bool(r.get('moved'))))
  else: miss.append(r['p'])
print('graded',len(g),'of',len(d),'missing',miss)
def tier(p): return '90+' if p>=90 else '80-89' if p>=80 else '70-79' if p>=70 else '60-69' if p>=60 else '45-59' if p>=45 else '<45'
from collections import defaultdict
T=defaultdict(lambda:[0,0])
for p,h,_,_ in g: T[tier(p)][0]+=h;T[tier(p)][1]+=1
for k in ['90+','80-89','70-79','60-69','45-59','<45']: print(k,T[k])
a=[x for x in g if x[0]>=70]; print('70+',sum(x[1] for x in a),len(a)); print('70+ misses',[ (x[0],x[2]) for x in a if not x[1]])
print('all',sum(x[1] for x in g),len(g))
mv=[x for x in g if x[3]]; print('moved',sum(x[1] for x in mv),len(mv))
json.dump({'graded':[x[:3] for x in g]},open('study/nov12_graded.json','w'))
