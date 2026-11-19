import json,math,random
from collections import defaultdict,Counter
P=json.load(open('audit/picks2.json'))
G=[p for p in P if p['status']=='graded' and p['result'] in ('W','L')]
for p in G: p['hit']=1 if p['result']=='W' else 0
def wk(d): dd=int(d[-2:]); return 'Wk1 Nov 4-8' if dd<=8 else 'Wk2 Nov 9-15' if dd<=15 else 'Wk3 Nov 16-17'
def band(g): return '85+' if g>=85 else '80-84' if g>=80 else '75-79' if g>=75 else '70-74' if g>=70 else '65-69' if g>=65 else '60-64' if g>=60 else '50-59' if g>=50 else '<50'
BO=['85+','80-84','75-79','70-74','65-69','60-64','50-59','<50']
def kb(p,key='k_tip'):
  k=p.get(key)
  if k is None: return 'no price'
  return 'ours 8+ above' if p['grade']>=k+8 else 'Kalshi 8+ above' if k>=p['grade']+8 else 'within 7'
KB=['ours 8+ above','within 7','Kalshi 8+ above','no price']
def stat(p):
  s=p.get('stat') or p['market']
  return {'prop':'other prop','other':'other prop','yds':'yards (other)'}.get(s,s)
def wil(h,n):
  if not n: return (0,0)
  z=1.96;q=h/n;d=1+z*z/n;c=q+z*z/(2*n);m=z*math.sqrt(q*(1-q)/n+z*z/(4*n*n));return (round(100*(c-m)/d),round(100*(c+m)/d))
def roi(rs):
  r=[p for p in rs if p.get('k_tip') is not None and 3<=p['k_tip']<=97]
  if not r: return None,0
  return round(100*sum(p['hit']/(p['k_tip']/100)-1 for p in r)/len(r),1),len(r)
def line(rs):
  n=len(rs);h=sum(p['hit'] for p in rs);lo,hi=wil(h,n)
  kr=[p for p in rs if p.get('k_tip') is not None]
  R,rn=roi(rs)
  return dict(n=n,w=h,l=n-h,hit=round(100*h/n) if n else 0,lo=lo,hi=hi,ours=round(sum(p['grade'] for p in rs)/n,1) if n else 0,kn=len(kr),kal=round(sum(p['k_tip'] for p in kr)/len(kr),1) if kr else None,khit=round(100*sum(p['hit'] for p in kr)/len(kr)) if kr else None,roi=R)
OUT={}
def table(name,keyf,order=None,rows=G):
  m=defaultdict(list)
  for p in rows: m[keyf(p)].append(p)
  ks=[k for k in (order or sorted(m)) if k in m]
  OUT[name]={k:line(m[k]) for k in ks}
table('all',lambda p:'all')
table('date',lambda p:p['slate_date'])
table('week',lambda p:wk(p['slate_date']))
table('sport',lambda p:p['sport'])
table('stat',lambda p:stat(p))
table('dir',lambda p:'under' if p.get('direction')=='u' else 'over / side')
table('grade',lambda p:band(p['grade']),BO)
table('kalshi',lambda p:kb(p),KB)
table('kalshi_exact_only',lambda p:kb(p),KB,[p for p in G if p.get('k_interp') is False or p.get('k_tip') is None])
table('kalshi_x_week',lambda p:wk(p['slate_date'])+' | '+kb(p),rows=[p for p in G if p.get('k_tip') is not None])
table('kalshi_x_sport',lambda p:p['sport']+' | '+kb(p),rows=[p for p in G if p.get('k_tip') is not None])
table('kalshi_x_stat',lambda p:stat(p)+' | '+kb(p),rows=[p for p in G if p.get('k_tip') is not None])
table('kalshi_x_grade',lambda p:band(p['grade'])+' | '+kb(p),rows=[p for p in G if p.get('k_tip') is not None])
table('grade_x_week',lambda p:band(p['grade'])+' | '+wk(p['slate_date']))
table('kalshi_band',lambda p:band(p['k_tip']),BO,[p for p in G if p.get('k_tip') is not None])
table('style',lambda p:p.get('line_style'))
# grading-time price buckets (Nov 16-17 only)
table('kgrade_nov16_17',lambda p:kb(p,'k_grade'),KB,[p for p in G if p.get('k_grade') is not None])
# Brier / calibration
def brier(rs,key): return round(sum((p[key]/100-p['hit'])**2 for p in rs)/len(rs),4)
KP=[p for p in G if p.get('k_tip') is not None]
OUT['brier']={'all priced':{'n':len(KP),'ours':brier(KP,'grade'),'kalshi_tip':brier(KP,'k_tip'),'base_rate':round(sum(((sum(q['hit'] for q in KP)/len(KP))-p['hit'])**2 for p in KP)/len(KP),4)}}
for w in sorted({wk(p['slate_date']) for p in KP}):
  r=[p for p in KP if wk(p['slate_date'])==w]; OUT['brier'][w]={'n':len(r),'ours':brier(r,'grade'),'kalshi_tip':brier(r,'k_tip')}
for d in sorted({p['slate_date'] for p in KP}):
  r=[p for p in KP if p['slate_date']==d]; OUT['brier'][d]={'n':len(r),'ours':brier(r,'grade'),'kalshi_tip':brier(r,'k_tip')}
OUT['brier']['all graded legs (ours only)']={'n':len(G),'ours':brier(G,'grade')}
KG=[p for p in G if p.get('k_grade') is not None and p.get('k_tip') is not None]
OUT['brier']['Nov16-17 grading-time vs tip']={'n':len(KG),'ours':brier(KG,'grade'),'kalshi_grading_time':brier(KG,'k_grade'),'kalshi_tip':brier(KG,'k_tip')}
cal={}
for key,rs in (('ours',G),('ours_priced',KP),('kalshi_tip',KP)):
  k='grade' if key.startswith('ours') else 'k_tip'
  m=defaultdict(list)
  for p in rs: m[band(p[k])].append(p)
  cal[key]={b:{'n':len(m[b]),'pred':round(sum(p[k] for p in m[b])/len(m[b]),1),'actual':round(100*sum(p['hit'] for p in m[b])/len(m[b]),1)} for b in BO if b in m}
OUT['calibration']=cal
# correlation and repetition
ev=defaultdict(list)
for p in G: ev[(p['slate_date'],(p.get('k_match') or {}).get('event') or p.get('event') or 'unknown:'+p['pick_key'])].append(p)
known=[v for k,v in ev.items() if not str(k[1]).startswith('unknown')]
pl=defaultdict(list)
for p in G:
  if p.get('player'): pl[(p['slate_date'],p['player'].lower(),stat(p))].append(p)
lad=[v for v in pl.values() if len(v)>1]
# within-game agreement: pairs of legs in same game, how often same result vs expected
same=0;pairs=0;exp=0
for v in known:
  for i in range(len(v)):
    for j in range(i+1,len(v)):
      a,b=v[i],v[j];pairs+=1;same+=a['hit']==b['hit'];pa,pb=a['grade']/100,b['grade']/100;exp+=pa*pb+(1-pa)*(1-pb)
# ladder agreement
lsame=lp=0
for v in lad:
  for i in range(len(v)):
    for j in range(i+1,len(v)): lp+=1;lsame+=v[i]['hit']==v[j]['hit']
T=json.load(open('audit/tickets.json'))
norm=lambda s:''.join(c for c in s.lower() if c.isalnum() or c in '+.')
key2={(p['slate_date'],norm(p['pick_text'])):p for p in P}
use=Counter();tl=0;tmiss=0;twarn=0;tkp=0
for t in T:
  for l in t['legs']:
    p=key2.get((t['slate_date'],norm(l)));tl+=1
    if not p: tmiss+=1;continue
    use[p['pick_key']]+=1
    if p.get('k_tip') is not None:
      tkp+=1; twarn+= p['grade']>=p['k_tip']+8
OUT['correlation']={'graded legs':len(G),'game clusters (known event)':len(known),'legs with known event':sum(len(v) for v in known),'avg legs per game':round(sum(len(v) for v in known)/len(known),2),
 'max legs one game':max(len(v) for v in known),'same player same stat ladders':len(lad),'legs inside ladders':sum(len(v) for v in lad),
 'same-game pairs':pairs,'same-game pairs same result %':round(100*same/pairs,1),'expected if independent %':round(100*exp/pairs,1),'ladder pairs same result %':round(100*lsame/lp,1) if lp else None,
 'tickets':len(T),'ticket legs':tl,'ticket legs not matched to a graded leg':tmiss,'distinct legs used on tickets':len(use),'legs used on 2+ tickets':sum(1 for v in use.values() if v>1),'max tickets one leg':max(use.values()) if use else 0,
 'ticket legs with a Kalshi price':tkp,'ticket legs that were ⚠ (8+ above Kalshi at tip)':twarn}
# cluster bootstrap for main kalshi bucket difference
random.seed(7)
cl=defaultdict(list)
for p in KP: cl[(p['slate_date'],(p.get('k_match') or {}).get('event'))].append(p)
ckeys=list(cl)
def boot(f,B=2000):
  vals=[]
  for _ in range(B):
    s=[x for k in random.choices(ckeys,k=len(ckeys)) for x in cl[k]]
    v=f(s)
    if v is not None: vals.append(v)
  vals.sort();return (round(vals[int(.025*len(vals))],1),round(vals[int(.975*len(vals))],1))
def hr(s,b): r=[p for p in s if kb(p)==b]; return 100*sum(p['hit'] for p in r)/len(r) if r else None
OUT['bootstrap_by_game']={b:boot(lambda s,b=b:hr(s,b)) for b in KB[:3]}
OUT['bootstrap_by_game']['ours-above minus within']=boot(lambda s:(hr(s,'ours 8+ above') or 0)-(hr(s,'within 7') or 0))
OUT['bootstrap_by_game']['brier ours minus kalshi']=boot(lambda s:1000*(sum((p['grade']/100-p['hit'])**2 for p in s)-sum((p['k_tip']/100-p['hit'])**2 for p in s))/len(s))
# OUT-OF-SAMPLE tests
def rule_test(name,rule,rows,desc):
  a=[p for p in rows if rule(p)];b=[p for p in rows if not rule(p)]
  OUT.setdefault('oos',{})[name]={'desc':desc,'flagged':line(a),'not flagged':line(b)}
pre=[p for p in KP if p['slate_date']<='2026-11-15']
rule_test('warn rule on Nov 4-15 (rule made from Nov 16-17)',lambda p:p['grade']>=p['k_tip']+8,pre,'Legs where our grade was 8+ above Kalshi tip price. None of these legs were used to make the rule.')
rule_test('hammer pool on Nov 4-15 (80+ and within 7)',lambda p:p['grade']>=80 and abs(p['grade']-p['k_tip'])<=7,[p for p in pre if p['grade']>=80],'Among 80+ legs: Kalshi within 7 vs not.')
rule_test('market-likes-it on Nov 4-15',lambda p:p['k_tip']>=p['grade']+8,pre,'Kalshi 8+ above our grade.')
early=[p for p in G if p['slate_date']<='2026-11-10'];late=[p for p in G if p['slate_date']>'2026-11-10']
for nm,rule,desc in [('85+ cap',lambda p:p['grade']>=85,'85+ legs vs 80-84 legs'),]:
  for lab,rows in (('Nov 4-10',early),('Nov 11-17',late)):
    rule_test(f'{nm} | {lab}',rule,[p for p in rows if p['grade']>=80],desc)
for lab,rows in (('Nov 4-10',early),('Nov 11-17',late)):
  rule_test(f'NFL yardage 70+ | {lab}',lambda p:p['sport']=='NFL' and stat(p) in ('recyds','rush','pass','yards (other)'),[p for p in rows if p['grade']>=70],'NFL yardage vs all other 70+ legs')
  rule_test(f'rebounds 80+ | {lab}',lambda p:stat(p)=='reb',[p for p in rows if p['grade']>=80],'rebounds vs other 80+ legs')
json.dump(OUT,open('audit/full_out.json','w'),indent=1)
def pr(name):
  print('\n==',name)
  for k,v in OUT[name].items(): print(f"  {k:38s} {v['w']:>3}-{v['l']:<3} {v['hit']:>3}% n={v['n']:<4} ({v['lo']}-{v['hi']}) ours {v['ours']}  K {v['kal']} (kn {v['kn']}) roi {v['roi']}")
for n in ['all','week','date','sport','stat','dir','grade','kalshi','kalshi_exact_only','kalshi_x_week','kalshi_x_sport','kalshi_x_grade','kalshi_band','grade_x_week','style','kgrade_nov16_17']: pr(n)
print(json.dumps({k:OUT[k] for k in ('brier','calibration','correlation','bootstrap_by_game')},indent=0))
for k,v in OUT['oos'].items(): print('\nOOS',k,'|',v['desc']); [print('   ',x,y['w'],'-',y['l'],y['hit'],'% n',y['n'],(y['lo'],y['hi']),'ours',y['ours'],'K',y['kal']) for x,y in (('flagged',v['flagged']),('not',v['not flagged']))]
