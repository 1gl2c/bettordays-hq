import json,re
B=json.load(open('sat/res/box.json'))
S=json.load(open('sat/sat.json'))
NAME={'John Collins':'John Collins','Jaylon Tyson':'Jaylon Tyson','Nolan Traore':'Nolan Traore','Jamal Murray':'Jamal Murray','Ayo Dosunmu':'Ayo Dosunmu','Nikola Jokic':'Nikola Jokic','Cameron Boozer':'Cameron Boozer','Cade Cunningham':'Cade Cunningham','P.J. Washington':'P.J. Washington','Giannis Antetokounmpo':'Giannis Antetokounmpo','Daniss Jenkins':'Daniss Jenkins'}
OTHER={ # UFC + CFB
"Ciryl Gane ML v Hokit":'W',"Amanda Nunes ML v Harrison":'L',"Yousri Belgaroui ML v Borralho":'L',"Uros Medic ML v Holland":'L',
"Medic v Holland under 1.5 rounds":'L',"Medic v Holland under 2 rounds":'L',"Hasan v Gurule under 1.5 rounds":'L',
"Stephen Thompson ML v Radtke":'W',"Drew Dober ML v Duncan":'L',"Melquizael Costa ML v Gordon":'W',
"Costa by KO or decision (double chance)":'W',"Costa by KO":'L',"Costa by decision":'W',"Bia Mesquita ML v Chiasson":'W',"Mesquita by submission":'W',
"Juan Diaz ML v Alatengheili":'W',"Diaz by decision":'W',"Evan Elder ML v Sanches":'W',
"Penn State ML v Minnesota":'W',"Oregon State v Boise State over 50 total points":'W',"LSU ML v Texas":'L',"Utah ML v Arizona":'W',
"BYU ML v Baylor":'W',"BYU -2.5 v Baylor":'W',"BYU -6.5 v Baylor":'W'}
ACT={"Ciryl Gane ML v Hokit":'Gane by decision (5 rounds)',"Amanda Nunes ML v Harrison":'Harrison by submission, R4',"Yousri Belgaroui ML v Borralho":'Borralho by decision',"Uros Medic ML v Holland":"Draw after 3 rounds",
"Medic v Holland under 1.5 rounds":'Went 3 rounds',"Medic v Holland under 2 rounds":'Went 3 rounds',"Hasan v Gurule under 1.5 rounds":'Gurule by decision',
"Stephen Thompson ML v Radtke":'Thompson by KO, R3',"Drew Dober ML v Duncan":'Duncan by decision',"Melquizael Costa ML v Gordon":'Costa by decision',
"Costa by KO or decision (double chance)":'Costa by decision',"Costa by KO":'Costa by decision',"Costa by decision":'Costa by decision',"Bia Mesquita ML v Chiasson":'Mesquita by submission, R1',"Mesquita by submission":'Submission, R1',
"Juan Diaz ML v Alatengheili":'Diaz by decision',"Diaz by decision":'Decision',"Evan Elder ML v Sanches":'Elder by decision',
"Penn State ML v Minnesota":'Penn State 42-14',"Oregon State v Boise State over 50 total points":'Boise State 46-41 (87 total)',"LSU ML v Texas":'Texas 22-21',"Utah ML v Arizona":'Utah 40-39',
"BYU ML v Baylor":'BYU 28-7',"BYU -2.5 v Baylor":'BYU by 21',"BYU -6.5 v Baylor":'BYU by 21'}
for r in S:
  p=r['p']
  if r.get('fl') in ('LIVE','FINAL'): r['r']='';continue
  if p in OTHER: r['r']=OTHER[p]; r['act']=ACT[p]; continue
  nm=max((k for k in NAME if p.startswith(k)),key=len); s=B[NAME[nm]]; t=p.lower()
  if 'pra' in t: v=s['pts']+s['reb']+s['ast']
  elif 'three' in t: v=s['3pm']
  elif 'assist' in t: v=s['ast']
  elif 'rebound' in t: v=s['reb']
  else: v=s['pts']
  m=re.search(r'(\d+(?:\.5)?)',t[len(nm):]); x=float(m.group(1))
  if 'under' in t: hit=v<x
  elif '.5' in m.group(1): hit=v>x
  else: hit=v>=x
  r['r']='W' if hit else 'L'; r['act']=v
json.dump(S,open('sat/sat_graded.json','w'))
g=[r for r in S if r.get('r')]; a7=[r for r in g if r['pct']>=70]
print('graded',len(g),'hits',sum(r['r']=='W' for r in g),'| 70+',sum(r['r']=='W' for r in a7),len(a7))
for lo,hi in [(90,101),(80,90),(70,80),(60,70),(50,60),(0,50)]:
  b=[r for r in g if lo<=r['pct']<hi]; print(lo,hi,sum(r['r']=='W' for r in b),len(b))
for r in sorted(g,key=lambda r:-r['pct']): print(r['r'],r['pct'],r['p'],'->',r['act'])
