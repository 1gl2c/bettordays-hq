import json,subprocess,urllib.parse
from concurrent.futures import ThreadPoolExecutor
NBA=["Quentin Grimes","Grayson Allen","Victor Wembanyama","Darius Garland","Sandro Mamukelashvili","Karl-Anthony Towns","Donovan Clingan","Keyonte George","Scottie Barnes","Brook Lopez","Mikal Bridges","Ausar Thompson","Rudy Gobert","Zaire Williams","Darryn Peterson","Luka Doncic","Keldon Johnson","LaMelo Ball","Ayo Dosunmu","Toumani Camara"]
CFB=["Jalen Buckley","Wayne Harris","Donovan Hamilton","D'Shawntae Jones","Riley Neer"]
LG={'nba':('basketball/nba','nba'),'cfb':('football/college-football','college-football')}
def cu(u):
  try: return json.loads(subprocess.run(['curl','-s','-m','25',u],capture_output=True,text=True).stdout)
  except Exception: return {}
def one(a):
  name,lg=a;sp,lgk=LG[lg]
  d=cu("https://site.web.api.espn.com/apis/common/v3/search?limit=10&type=player&query="+urllib.parse.quote(name))
  its=[i for i in d.get('items',[]) if i.get('league')==lgk]
  if not its: return name,{'err':'notfound','leagues':[i.get('league') for i in d.get('items',[])][:5]}
  it=its[0];g=cu(f"https://site.web.api.espn.com/apis/common/v3/sports/{sp}/athletes/{it['id']}/gamelog")
  names=g.get('names',[]);ev=g.get('events',{});games=[]
  for st in g.get('seasonTypes',[])[:1]:
    for c in st['categories']:
      for e in c.get('events',[]):
        m=ev.get(e['eventId'],{});row={'date':m.get('gameDate','')[:10],'opp':m.get('opponent',{}).get('abbreviation'),'team':m.get('team',{}).get('abbreviation'),'res':m.get('gameResult')}
        for i,n in enumerate(names):
          if n not in row: row[n]=e['stats'][i]
        games.append(row)
  games.sort(key=lambda r:r['date'],reverse=True)
  a=cu(f"https://site.web.api.espn.com/apis/common/v3/sports/{sp}/athletes/{it['id']}").get('athlete',{})
  inj=a.get('injuries') or []
  return name,{'id':it['id'],'disp':it['displayName'],'team':a.get('team',{}).get('abbreviation'),'pos':a.get('position',{}).get('abbreviation'),'inj':[(i.get('status'),(i.get('shortComment') or '')[:150]) for i in inj][:1],'season':g.get('seasonTypes',[{}])[0].get('displayName') if g.get('seasonTypes') else None,'games':games}
with ThreadPoolExecutor(10) as ex: out=dict(ex.map(one,[(n,'nba') for n in NBA]+[(n,'cfb') for n in CFB]))
json.dump(out,open('logs.json','w'))
for k,v in out.items():
  g=v.get('games',[]);print(k,'|',v.get('disp'),v.get('team'),v.get('pos'),v.get('season'),len(g),v.get('inj'),v.get('err',''),v.get('leagues',''))
