import json,subprocess
from concurrent.futures import ThreadPoolExecutor
def cu(u): return json.loads(subprocess.run(['curl','-s','-m','30',u],capture_output=True,text=True).stdout)
nfl=cu("https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard?dates=20261115")
nba=cu("https://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard?dates=20261115")
games={}
for lg,d in (('nfl',nfl),('nba',nba)):
  for e in d['events']:
    c=e['competitions'][0]
    games[e['shortName']]={'lg':lg,'id':e['id'],'st':e['status']['type']['detail'],'sc':{t['team']['abbreviation']:int(t['score']) for t in c['competitors']},'win':[t['team']['abbreviation'] for t in c['competitors'] if t.get('winner')]}
def box(k):
  g=games[k]; sp='football/nfl' if g['lg']=='nfl' else 'basketball/nba'
  s=cu(f"https://site.api.espn.com/apis/site/v2/sports/{sp}/summary?event={g['id']}"); out={}
  for tm in s['boxscore']['players']:
    for st in tm['statistics']:
      keys=st.get('keys') or st.get('labels')
      for a in st['athletes']:
        n=a['athlete']['displayName']; o=out.setdefault(n,{'team':tm['team']['abbreviation']})
        if not a.get('stats'): o['dnp']=1; continue
        pre=(st.get('name')+'.') if g['lg']=='nfl' else ''
        for kk,v in zip(keys,a['stats']): o[pre+kk]=v
  return k,out
with ThreadPoolExecutor(8) as ex: B=dict(ex.map(box,games))
json.dump({'games':games,'box':B},open('all.json','w'))
for k,g in games.items(): print(k,g['st'],g['sc'],g['win'])
P={n:v for b in B.values() for n,v in b.items()}
for n in ['Joe Burrow','Jaylen Warren','Trey McBride','Luka Doncic','Jalen Johnson','Chris Olave']: print(n,P.get(n))
