import json,re
B=json.load(open('fri/box_fri.json'))
F=json.load(open('fri/fri.json'))
PL={'Jalen Johnson':'Jalen Johnson','Darius Garland':'Darius Garland','Garland':'Darius Garland','Sabonis':'Domantas Sabonis','Domantas Sabonis':'Domantas Sabonis','Shai Gilgeous-Alexander':'Shai Gilgeous-Alexander','Dylan Harper':'Dylan Harper','Peyton Watson':'Peyton Watson','Sidy Cissoko':'Sidy Cissoko','Josh Hart':'Josh Hart','Matas Buzelis':'Matas Buzelis','Alperen Sengun':'Alperen Sengun','Isaiah Jackson':'Isaiah Jackson','Herbert Jones':'Herbert Jones','Jaylen Wells':'Jaylen Wells','Okongwu':'Onyeka Okongwu','Jaime Jaquez':'Jaime Jaquez Jr.','Donovan Mitchell':'Donovan Mitchell','Pascal Siakam':'Pascal Siakam','Karl-Anthony Towns':'Karl-Anthony Towns','Tyler Herro':'Tyler Herro','Brayden Burries':'Brayden Burries','Davion Mitchell':'Davion Mitchell','Jarrett Allen':'Jarrett Allen','Nickeil Alexander-Walker':'Nickeil Alexander-Walker','Josh Giddey':'Josh Giddey','Ty Jerome':'Ty Jerome','Cameron Boozer':'Cameron Boozer','Jabari Smith':'Jabari Smith Jr.','Kevin Durant':'Kevin Durant','Yaxel Lendeborg':'Yaxel Lendeborg','Isaiah Hartenstein':'Isaiah Hartenstein','Deni Avdija':'Deni Avdija','Darius Acuff Jr':'Darius Acuff Jr.','Donovan Clingan':'Donovan Clingan','Dyson Daniels':'Dyson Daniels','Fred VanVleet':'Fred VanVleet','Reed Sheppard':'Reed Sheppard'}
GL={"CLE Cavs ML v Heat":0,"Samford +2.5 v Wright State":0,"Samford +4.5 v Wright State":0,"Samford +7.5 v Wright State":0,"Hofstra ML v Iona":1,"UConn ML v Ohio State":1,"UConn -1.5 v Ohio State":1,"UConn -3.5 v Ohio State":1,"Houston v Colorado over 44.5 total points":1,"Houston v Colorado over 40 total points":1,"Yale ML v Northeastern":0}
out=[]
for r in F:
  p=r['p']
  if r.get('fl')=='OUT': r['r']='';continue
  if p in GL: r['r']='W' if GL[p] else 'L'; out.append(r); continue
  name=max((k for k in PL if p.startswith(k)),key=len)
  s=B[PL[name]]
  t=p.lower()
  if 'pra' in t: v=s['pts']+s['reb']+s['ast']
  elif '3pm' in t or 'three' in t or 'pointers' in t: v=s['3pm']
  elif 'assist' in t: v=s['ast']
  elif 'rebound' in t: v=s['reb']
  else: v=s['pts']
  m=re.search(r'(?:o|over|over )\s*(\d+\.5)',t)
  if m: k=int(float(m.group(1))+0.5)
  else: k=int(re.search(r'(\d+)\s*\+|over (\d+)|o\s?(\d+)',t).group(0).strip('+ overo').strip())
  r['r']='W' if v>=k else 'L'; r['act']=v; r['k']=k; out.append(r)
json.dump(F,open('fri/fri_graded.json','w'))
g=[r for r in F if r.get('r')]
a7=[r for r in g if r['pct']>=70]
print('graded',len(g),'hits',sum(r['r']=='W' for r in g),'| 70+',sum(r['r']=='W' for r in a7),len(a7))
for r in sorted(g,key=lambda r:-r['pct']):
  if r['pct']>=70 and r['r']=='L' or r['p'] in ('Pascal Siakam 20+ points','Yaxel Lendeborg 15+ points'): print('MISS' if r['r']=='L' else 'hit ',r['pct'],r['p'],'->',r.get('act'))
