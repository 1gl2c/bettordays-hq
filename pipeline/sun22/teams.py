import json,subprocess,urllib.parse
from concurrent.futures import ThreadPoolExecutor
P=["Caleb Williams","Jordyn Tyson","Kyle Monangai","Fernando Mendoza","Ashton Jeanty","Brock Purdy","Ryan Flournoy","Malachi Fields","Carnell Tate","James Cook","CeeDee Lamb","D'Andre Swift","Emmett Johnson","Josh Downs","Tony Pollard","Isaiah Likely","Christian McCaffrey","Trey McBride","Justice Hill","Javonte Williams","Adonai Mitchell","Dak Prescott","Justin Jefferson","Kenneth Walker III","Zay Flowers","Chuba Hubbard","Bhayshul Tuten","Jonah Coleman","Josh Allen","Jahmyr Gibbs","T.J. Hockenson","George Kittle","Joe Milton","Jauan Jennings","Ollie Gordon","Amon-Ra St. Brown","Devin Bush","Caleb Douglas","Breece Hall","Derrick Henry","Jakobi Meyers","DeVonta Smith","Courtland Sutton","Jaylen Warren","Khalil Shakir","J.J. McCarthy","George Pickens"]
N=["Karl-Anthony Towns","Wendell Carter Jr."]
def cu(u):
  try: return json.loads(subprocess.run(['curl','-s','-m','25',u],capture_output=True,text=True).stdout)
  except Exception: return {}
def one(a):
  n,lg=a;d=cu("https://site.web.api.espn.com/apis/common/v3/search?limit=8&type=player&query="+urllib.parse.quote(n))
  its=[i for i in d.get('items',[]) if i.get('league')==lg]
  if not its: return n,None
  it=its[0];sp='football/nfl' if lg=='nfl' else 'basketball/nba'
  a=cu(f"https://site.web.api.espn.com/apis/common/v3/sports/{sp}/athletes/{it['id']}")
  at=a.get('athlete',{});return n,{'id':it['id'],'disp':it['displayName'],'team':(at.get('team') or {}).get('abbreviation'),'pos':(at.get('position') or {}).get('abbreviation'),'status':(at.get('status') or {}).get('type'),'inj':[x.get('status') for x in at.get('injuries',[])][:1]}
with ThreadPoolExecutor(10) as ex: R=dict(ex.map(one,[(n,'nfl') for n in P]+[(n,'nba') for n in N]))
json.dump(R,open('sun22/teams.json','w'),indent=1)
for n,v in R.items(): print(n,v and (v['disp'],v['team'],v['pos'],v['inj']))
