import json,subprocess
from concurrent.futures import ThreadPoolExecutor
def cu(u): return json.loads(subprocess.run(['curl','-s','-m','30',u],capture_output=True,text=True).stdout)
SP={'nba':'basketball/nba','nfl':'football/nfl','nhl':'hockey/nhl','cbb':'basketball/mens-college-basketball','cfb':'football/college-football'}
games={}
for lg,q in (('nba',''),('cbb','&groups=50&limit=400'),('cfb','&groups=80&limit=400')):
  for e in cu(f"https://site.api.espn.com/apis/site/v2/sports/{SP[lg]}/scoreboard?dates=20261121{q}")['events']:
    c=e['competitions'][0]
    games[e['shortName']]={'lg':lg,'id':e['id'],'st':e['status']['type']['detail'],'sc':{t['team']['abbreviation']:int(t['score'] or 0) for t in c['competitors']},'win':[t['team']['abbreviation'] for t in c['competitors'] if t.get('winner')]}
def box(k):
  g=games[k]
  if g['lg'] not in ('nba','nfl','cfb'): return k,{}
  
  s=cu(f"https://site.api.espn.com/apis/site/v2/sports/{SP[g['lg']]}/summary?event={g['id']}");out={}
  for tm in s.get('boxscore',{}).get('players',[]):
    for st in tm['statistics']:
      keys=st.get('keys') or st.get('labels')
      for a in st['athletes']:
        n=a['athlete']['displayName'];o=out.setdefault(n,{'team':tm['team']['abbreviation']})
        if not a.get('stats'): o['dnp']=1;continue
        pre=(st.get('name')+'.') if g['lg'] in ('nfl','cfb') else ''
        for kk,v in zip(keys,a['stats']): o[pre+kk]=v
  return k,out
with ThreadPoolExecutor(8) as ex: B=dict(ex.map(box,games))
json.dump({'games':games,'box':B},open('sat21/res/all.json','w'))
for k,g in games.items():
  if g['lg']=='nba': print(k,g['st'],g['sc'])
print(len(games),'games')
