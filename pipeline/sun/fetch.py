import json,subprocess,urllib.parse,sys
from concurrent.futures import ThreadPoolExecutor
NFL=["Justin Jefferson","Christian Watson","Brock Bowers","Jaxon Smith-Njigba","Ja'Marr Chase","Tee Higgins","Jaylen Warren","Drake London","Chris Olave","Jonathan Taylor","James Cook","Trey McBride","CeeDee Lamb","Aaron Rodgers","Joe Burrow","Christian McCaffrey","Javonte Williams","Kyren Williams","Bijan Robinson","Patrick Mahomes","Michael Penix Jr.","Jakobi Meyers","Trevor Lawrence","Cam Ward","Aaron Jones","Tucker Kraft","Kenneth Walker III","Myles Price","Xavier Hutchinson","Anthony Gould","Jadarian Price","Brock Purdy","Breece Hall","Seth McGowan","Tommy Tremble","Keenan Allen","Geno Smith","Emmett Johnson","Chris Rodriguez Jr.","Deshaun Watson","Mike Washington Jr.","Josh Allen","Chase Brown"]
NBA=["Josh Hart","Jalen Johnson","Keyonte George","Anfernee Simons","Pascal Siakam","Jaylen Brown"]
def cu(u):
  r=subprocess.run(['curl','-s','-m','25',u],capture_output=True,text=True).stdout
  try: return json.loads(r)
  except Exception: return {}
def one(a):
  name,lg=a
  sp='football/nfl' if lg=='nfl' else 'basketball/nba'
  d=cu("https://site.web.api.espn.com/apis/common/v3/search?limit=8&type=player&query="+urllib.parse.quote(name))
  its=[i for i in d.get('items',[]) if i.get('league')==lg]
  if not its: return name,{'err':'notfound'}
  it=its[0]
  g=cu(f"https://site.web.api.espn.com/apis/common/v3/sports/{sp}/athletes/{it['id']}/gamelog")
  names=g.get('names',[]); ev=g.get('events',{}); games=[]
  for st in g.get('seasonTypes',[]):
    if 'Regular' not in st.get('displayName',''): continue
    if '2026' not in st.get('displayName','') and '2026-27' not in st.get('displayName',''): continue
    for c in st['categories']:
      for e in c.get('events',[]):
        m=ev.get(e['eventId'],{})
        row={'date':m.get('gameDate','')[:10],'opp':m.get('opponent',{}).get('abbreviation'),'team':m.get('team',{}).get('abbreviation'),'wk':m.get('week'),'res':m.get('gameResult'),'score':m.get('score')}
        for i,n in enumerate(names):
          if n not in row: row[n]=e['stats'][i]
        games.append(row)
  games.sort(key=lambda r:r['date'],reverse=True)
  return name,{'id':it['id'],'disp':it['displayName'],'games':games,'seasons':[s.get('displayName') for s in g.get('seasonTypes',[])][:3]}
with ThreadPoolExecutor(8) as ex: out=dict(ex.map(one,[(n,'nfl') for n in NFL]+[(n,'nba') for n in NBA]))
json.dump(out,open('logs.json','w'))
for k,v in out.items():
  g=v.get('games',[]); print(k,'|',v.get('disp'),v.get('err',''),len(g),g[0]['team'] if g else '',g[0]['date'] if g else '',v.get('seasons',[''])[:1])
