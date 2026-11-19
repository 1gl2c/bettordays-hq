import json,subprocess
def cu(u):
  try: return json.loads(subprocess.run(['curl','-s','-m','30',u],capture_output=True,text=True).stdout)
  except Exception: return {}
out={}
for k,lg in [('nba','basketball/nba'),('nhl','hockey/nhl'),('cbb','basketball/mens-college-basketball')]:
  d=cu(f'https://site.api.espn.com/apis/site/v2/sports/{lg}/scoreboard?dates=20261118&limit=400'+('&groups=50' if k=='cbb' else ''))
  out[k]=d
json.dump(out,open('wed/sb.json','w'))
inj=cu('https://site.api.espn.com/apis/site/v2/sports/basketball/nba/injuries');json.dump(inj,open('wed/nba_inj.json','w'))
for k in out:
  for e in out[k].get('events',[]):
    c=e['competitions'][0];o=(c.get('odds') or [{}])[0]
    if k=='cbb' and not any(x in e['name'] for x in ('Eastern Michigan','Detroit Mercy','James Madison','Towson','Wichita','Loyola','Florida','Houston','Kansas','West Virginia','UConn','Arizona')): continue
    print(k,e['shortName'],e['date'],e['status']['type']['name'],o.get('details'),o.get('overUnder'))
