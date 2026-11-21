import json,subprocess,urllib.parse,sys
from concurrent.futures import ThreadPoolExecutor
NBA=["LaMelo Ball","Domantas Sabonis","Tyler Herro","Kris Dunn","Devin Vassell","Karl-Anthony Towns","Anfernee Simons","Joel Embiid","Cooper Flagg","Rui Hachimura"]
CFB=["Noah Fifita","Jesse Legree","L.J. Phillips Jr.","Carlos Hernandez","Dylan Riley"]
def cu(u):
  r=subprocess.run(['curl','-s','-m','25',u],capture_output=True,text=True).stdout
  try: return json.loads(r)
  except Exception: return {}
def one(a):
  name,lg=a;sp={'nba':'basketball/nba','college-football':'football/college-football'}[lg]
  d=cu("https://site.web.api.espn.com/apis/common/v3/search?limit=10&type=player&query="+urllib.parse.quote(name))
  its=[i for i in d.get('items',[]) if i.get('league')==lg]
  if not its: return name,{'err':'notfound','cands':[(i.get('displayName'),i.get('league')) for i in d.get('items',[])][:6]}
  it=its[0];g=cu(f"https://site.web.api.espn.com/apis/common/v3/sports/{sp}/athletes/{it['id']}/gamelog")
  names=g.get('names',[]);ev=g.get('events',{});games=[]
  for st in g.get('seasonTypes',[])[:1]:
    for c in st['categories']:
      for e in c.get('events',[]):
        m=ev.get(e['eventId'],{});row={'date':m.get('gameDate','')[:10],'opp':m.get('opponent',{}).get('abbreviation'),'team':m.get('team',{}).get('abbreviation'),'res':m.get('gameResult'),'min':None}
        for i,n in enumerate(names):
          if n not in row or row[n] is None: row[n]=e['stats'][i]
        games.append(row)
  games.sort(key=lambda r:r['date'],reverse=True)
  a=cu(f"https://site.web.api.espn.com/apis/common/v3/sports/{sp}/athletes/{it['id']}").get('athlete',{})
  inj=a.get('injuries') or []
  return name,{'id':it['id'],'disp':it['displayName'],'team':a.get('team',{}).get('abbreviation'),'pos':a.get('position',{}).get('abbreviation'),'inj':[(i.get('status'),(i.get('shortComment') or '')[:220]) for i in inj][:1],'season':g.get('seasonTypes',[{}])[0].get('displayName') if g.get('seasonTypes') else None,'games':games,'names':names}
with ThreadPoolExecutor(12) as ex: out=dict(ex.map(one,[(n,'nba') for n in NBA]+[(n,'college-football') for n in CFB]))
json.dump(out,open('sat21/logs.json','w'))
for k,v in out.items():
  g=v.get('games',[]);print(k,'|',v.get('disp'),v.get('team'),v.get('pos'),v.get('season'),len(g),g[0]['date'] if g else '',v.get('inj'),v.get('err',''),v.get('cands',''))
