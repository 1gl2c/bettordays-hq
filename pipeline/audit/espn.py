import json,urllib.request,sys,os,re
def get(u):
  with urllib.request.urlopen(u,timeout=30) as r: return json.load(r)
def box(sp,date,players):
  lg={'nba':'basketball/nba','cbb':'basketball/mens-college-basketball'}[sp]
  sb=get(f'https://site.api.espn.com/apis/site/v2/sports/{lg}/scoreboard?dates={date.replace("-","")}&limit=300&groups=50')
  out={}
  for e in sb['events']:
    s=get(f'https://site.api.espn.com/apis/site/v2/sports/{lg}/summary?event={e["id"]}')
    for t in s.get('boxscore',{}).get('players',[]):
      st=t['statistics'][0]; keys=st['keys']
      for a in st['athletes']:
        n=a['athlete']['displayName']
        if any(p.lower() in n.lower() for p in players): out[n+' '+e['shortName']]=dict(zip(keys,a.get('stats',[])))
  return out
if __name__=='__main__':
  print(json.dumps(box(sys.argv[1],sys.argv[2],sys.argv[3:]),indent=0)[:3000])
