# Nov 19 run: the list was fetched once (with 'Amari Demercado', not found), then 'Emari Demercado' was fetched alone and merged into thu/logs.json.
import json,subprocess,urllib.parse
from concurrent.futures import ThreadPoolExecutor
NFL=["C.J. Stroud","Dalton Schultz","Xavier Hutchinson","Laquon Treadwell","Tyler Warren","Jonathan Taylor","David Montgomery","Nico Collins","Tank Dell","Emari Demercado","Anthony Gould","Seth McGowan"]
NBA=["LaMelo Ball","Donovan Clingan","Jalen Brunson","Brook Lopez","De'Aaron Fox","Jaden McDaniels","Myles Turner","Victor Wembanyama","Mikal Bridges"]
def cu(u):
  r=subprocess.run(['curl','-s','-m','25',u],capture_output=True,text=True).stdout
  try: return json.loads(r)
  except Exception: return {}
def one(a):
  name,lg=a;sp='football/nfl' if lg=='nfl' else 'basketball/nba'
  d=cu("https://site.web.api.espn.com/apis/common/v3/search?limit=8&type=player&query="+urllib.parse.quote(name))
  its=[i for i in d.get('items',[]) if i.get('league')==lg]
  if not its: return name,{'err':'notfound','leagues':[i.get('league') for i in d.get('items',[])][:5]}
  it=its[0];g=cu(f"https://site.web.api.espn.com/apis/common/v3/sports/{sp}/athletes/{it['id']}/gamelog")
  names=g.get('names',[]);ev=g.get('events',{});games=[]
  for st in g.get('seasonTypes',[])[:1]:
    if 'Regular' not in st.get('displayName',''): continue
    for c in st['categories']:
      for e in c.get('events',[]):
        m=ev.get(e['eventId'],{});row={'date':m.get('gameDate','')[:10],'opp':m.get('opponent',{}).get('abbreviation'),'team':m.get('team',{}).get('abbreviation'),'res':m.get('gameResult')}
        for i,n in enumerate(names):
          if n not in row: row[n]=e['stats'][i]
        games.append(row)
  games.sort(key=lambda r:r['date'],reverse=True)
  a=cu(f"https://site.web.api.espn.com/apis/common/v3/sports/{sp}/athletes/{it['id']}").get('athlete',{})
  inj=a.get('injuries') or []
  return name,{'id':it['id'],'disp':it['displayName'],'team':a.get('team',{}).get('abbreviation'),'pos':a.get('position',{}).get('abbreviation'),'inj':[(i.get('status'),(i.get('shortComment') or '')[:200]) for i in inj][:1],'season':g.get('seasonTypes',[{}])[0].get('displayName') if g.get('seasonTypes') else None,'games':games}
with ThreadPoolExecutor(10) as ex: out=dict(ex.map(one,[(n,'nfl') for n in NFL]+[(n,'nba') for n in NBA]))
json.dump(out,open('thu/logs.json','w'))
for k,v in out.items():
  g=v.get('games',[]);print(k,'|',v.get('disp'),v.get('team'),v.get('pos'),v.get('season'),len(g),g[0]['date'] if g else '',v.get('inj'),v.get('err',''),v.get('leagues',''))
