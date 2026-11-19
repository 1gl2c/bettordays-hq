import json
d=json.load(open('study/nov12.json'))
R={ # exact p -> 1/0, with actual note
"76ers ML v Raptors":(1,"won 123-112"),"Pistons ML v Wizards":(1,"won 144-140 2OT"),"Timberwolves ML v Mavericks":(1,"won 133-94"),"Phx Suns ML v Hornets":(1,"won 101-96"),
"Cade Cunningham 20+ points":(1,"52"),"Rudy Gobert 8+ rebounds":(0,"6"),"Naz Reid 8+ rebounds":(1,"8"),"Dean Wade 4+ rebounds":(1,"5"),"Dean Wade 2+ rebounds":(1,"5"),
"Naz Reid 20+ points":(0,"16"),"Naz Reid 15+ points":(1,"16"),"Ayo Dosunmu over 10 points":(1,"cashed"),"Daniel Gafford 10+ points":(0,"3"),
"Joel Embiid 20+ points":(1,"20"),"Joel Embiid 15 + points":(1,"20"),"Joel Embiid 6+ rebounds":(0,"4"),"Miles Bridges 15+ points":(0,"11"),"Miles Bridges 10+ points":(1,"11"),
"Alex Sarr 4+ rebounds":(1,"cashed"),"Jaden Mcdaniels 4+ rebounds":(1,"9"),"Ausar THomspon 4+ assists":(1,"11"),"Ausar Thompson 2+ assist":(1,"11"),
"Dallas +6 v Timberwolves":(0,"lost by 39"),"Dallas +11 v Timberwolves":(0,"lost by 39"),"Phx Suns -6 v Hornets":(0,"won by 5"),"Phx Suns -2 hornets":(1,"won by 5"),
"Phi 76ers -8 v Toronto":(1,"won by 11"),"Phi 76ers -6 v Toronto":(1,"won by 11"),"Phi 76ers -2 , -4 v Toronto":(1,"won by 11"),
"DET / Wizards under 225":(0,"284"),"Toronto v Phil 76ers over 220":(1,"235"),"Charlotte Hornets v Phx Suns under 215":(1,"197"),"Charlotte Hornets v Phx Suns under 220":(1,"197"),
"Mavs v Timberwolves over 225":(1,"227"),"Mavs v Timberwolves over 220":(1,"227"),
"Under 60 total points":(1,"45"),"WAS / NY Giants over 40 total points":(1,"45"),"WAS / NY Giants over 35 total points":(1,"45"),"WAS / NY Giants over 30 total points":(1,"45"),
"Washighton Comanders +3.5 v Giants":(1,"won 24-21"),"Washighton Comanders +5.5 v Giants":(1,"won"),"Washighton Comanders +7 v Giants":(1,"won"),"Washighton Comanders ML v Giants":(1,"won 24-21"),
"Jayden Daniels any time touchdowns":(0,"0 rush TD"),"J.J. McCarthy any time touchdowns":(0,"0"),"Cam Skattebo any time touchdown":(1,"2 TD"),"Jayden Daniels Under 0.5 Interceptions":(0,"2 INT"),
"Malachi Fields 2+ receptions":(1,"cashed"),"Daniels 15+ rush yds":(1,"cashed"),"A. Williams 15+ rec yds":(1,"31-yd TD"),"Antonio Williams 25+ receiving yards":(1,"31-yd TD"),
"Nabers 3+ rec":(1,"cashed"),"Stefon Diggs 25+ receiving yards":(1,"32-yd TD"),"Dominic Zvada o6.5 Kick Points":(0,"3"),"Zvada 5+ kick pts":(0,"3"),
"Tampa Bay Lightning ML":(1,"won"),"Bridges 8+ pts":(1,"11"),"Ausar 3+ ast":(1,"11"),
}
g=[];u=[]
for r in d:
  if r['p'] in R: g.append((r['pct'],R[r['p']][0],r['p']))
  else: u.append((r['pct'],r['p']))
def tier(p): return '90+' if p>=90 else '80-89' if p>=80 else '70-79' if p>=70 else '60-69' if p>=60 else '45-59' if p>=45 else '<45'
from collections import defaultdict
T=defaultdict(lambda:[0,0])
for p,h,_ in g: T[tier(p)][0]+=h;T[tier(p)][1]+=1
print(len(g),'graded',sum(h for _,h,_ in g))
for k in ['90+','80-89','70-79','60-69','45-59','<45']: print(k,T[k])
a=[x for x in g if x[0]>=70]; print('70+',sum(h for _,h,_ in a),len(a))
print('misses 70+',[x for x in a if not x[1]])
print('ungraded 70+',[x for x in u if x[0]>=70])
json.dump({'graded':g,'ungraded':u},open('study/nov12_graded.json','w'))
