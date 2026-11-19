import re,json
P='bettordays-hq.html'; s=open(P).read()
W,L='W','L'
MR={
'Under 64 total pts BUF@MIN':W,'Cook 50+ rush yds':W,'Allen 200+ pass yds':W,'Allen o237.5 pass yds':L,
'Allen u23 completions':W,'Allen u21 completions':L,'Allen u19.5 completions':L,'Allen ATD':L,
'Shakir 3+ rec':W,'Under 24.5 1H pts':W,'DJ Moore ATD':L,'Ty Johnson U15.5 rec yds':L,
'Jefferson u8 rec':W,'Jefferson u7 rec':W,'Jefferson ATD':L,'Wentz o0.5 pass TD':L,'Wentz o1.5 pass TDs':L,
'Wentz 200+ pass yds':L,'Wentz o211.5 pass yds':L,'Wentz 15+ completions':L,'Wentz o18.5 completions':L,'Hockenson ATD':L,
'Wemby U55 PRA':W,'Wemby U50 PRA':L,'Wemby U45 PRA':L,'Ziaire Williams 5+ pts':W,'Pistons ML':W,'Cavaliers ML':L,
'Miles Bridges 20+ PRA':L,'Kyshawn George 20+ PRA':L,'Warriors ML':W,'Spurs ML at Suns':W,'Rockets ML':W,
'Booker o18.5 pts':W,'Sengun U0.5 threes':L,'Okongwu o0.5 3PM':W,'Fears o3.5 ast':W,'Siakam U25 pts':L,
'Cam Spencer U4 reb':W,'Kyshawn George o4.5 reb':L,'Booker o1.5 3PM':W,'Mavericks ML':W,'Ja\'Kobe Walter o11.5 pts':W,
'Kessler o23.5 P+R':W,'DeRozan U20 PRA':W,'John Collins o5.5 reb':W,'Cam Spencer U3 reb':W,'Castle o4.5 reb':W,
'Cade o8.5 ast':L,'Okongwu o1.5 3PM':W,'Dylan Harper o21.5 P+R':W,'Jamal Murray U4.5 reb':W,
'Luka U34.5 pts':W,'Lakers ML (live)':W,'Booker 15+ pts':W,'Allen u25 completions':W,
}
m=re.search(r'const MON=(\[.*?\]);\n',s); MON=json.loads(m.group(1))
for r in MON:
    if r['p']=='Cavaliers ML': r['g']='CLE@CHA'; r['n']='Road favorite at Charlotte. Lost 124-112. Ace called it'
    if r['p']=='Miles Bridges 20+ PRA': r['g']='SAS@PHX'; r['n']='Bridges plays for Phoenix, not Charlotte. Went 7/5/0 = 12'
    if r['p']=='Luka U34.5 pts': r['fl']='';r['pct']=0; r['n']='We listed Luka OUT. He played: 32/8/10. Rule now: no Luka unders, ever'
    if r['p'].startswith('Wemby U'): r['n']='Wemby went 40/11/3 = 54 PRA. Rule now: no Wemby unders, ever'
    r['r']=MR.get(r['p'],'')
s=s.replace(m.group(1),json.dumps(MON))
# fix NBA filter regex for CHA home
s=s.replace("/@(DET|CLE|ATL|TOR|DAL|HOU|PHX|GSW)$/","/@(DET|CHA|CLE|ATL|TOR|DAL|HOU|PHX|GSW)$/")
# result badge helper in MON render
s=s.replace("(function(){const fl=x=>x.fl?","(function(){const rb=x=>x.r?` <span class=\"res ${x.r==='W'?'w':'l'}\">${x.r}</span>`:'';const fl=x=>x.fl?",1)
s=s.replace("<li>${r.p} <span style=\"color:#04ff9f\">${r.pct}%</span>${fl(r)}</li>","<li>${r.p} <span style=\"color:#04ff9f\">${r.pct}%</span>${fl(r)}${rb(r)}</li>")
s=s.replace("<li>${r.p} <span style=\"color:#00c8ff\">${r.pct}%</span>${fl(r)}</li>","<li>${r.p} <span style=\"color:#00c8ff\">${r.pct}%</span>${fl(r)}${rb(r)}</li>")
s=s.replace("`<span class=\"chip\">${r.p} <b>${r.pct}</b>","`<span class=\"chip\">${r.p} <b>${r.pct}</b>${rb(r)}")
s=s.replace("<td>${x.p}<span class=\"tag\">${x.st.toUpperCase()}</span>${fl(x)}</td>","<td>${x.p}<span class=\"tag\">${x.st.toUpperCase()}</span>${fl(x)}${rb(x)}</td>")
open(P,'w').write(s)
# ticket results
m=re.search(r'const MTIX=(\[.*?\]);\n',s); T=json.loads(m.group(1))
for t in T:
    res=[MR.get(l,'') for l in t['legs']]
    miss=[l for l in t['legs'] if MR.get(l)=='L']
    t['res']='L' if miss else 'W'
    t['miss']=miss
    if t['t'].startswith('Hammer ·'): t['res']='CO'; t['lock']='Real cost $119.99. Cashed out $39.06 (-$80.93)'
    if t['t'].startswith('Hammer 2.0'): t['lock']='Cashed: $190.96 paid $529.23'
s=s.replace(m.group(1),json.dumps(T))
open(P,'w').write(s)
print(sum(1 for r in MON if r['r']=='W'),sum(1 for r in MON if r['r']=='L'))
top=[r for r in MON if r['pct']>=70 and r['r']]; print('70+',sum(r['r']=='W' for r in top),len(top))
cl=[r for r in top if not r['fl']]; print('clean70',sum(r['r']=='W' for r in cl),len(cl))
json.dump(MON,open('study/nov9.json','w')) if False else None
json.dump([r for r in MON if r['r']],open('nov9_graded.json','w'))
