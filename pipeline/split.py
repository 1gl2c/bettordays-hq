import json,copy
SPL={"Detroit -11, -6, -3, ML  v Wizards":[("Pistons -11 v Wizards",35,"L"),("Pistons -6 v Wizards",52,"L"),("Pistons -3 v Wizards",72,"W"),("Pistons ML v Wizards (ladder)",80,"W")],
"Phi 76ers -2 , -4 v Toronto":[("76ers -2 v Raptors",66,"W"),("76ers -4 v Raptors",61,"W")]}
def split(a):
  out=[]
  for r in a:
    if r['p'] in SPL:
      for p,pct,res in SPL[r['p']]:
        x=copy.deepcopy(r);x['p']=p;x['pct']=pct;x['r']=res;x['n']=(r.get('n') or '')+' Split from a ladder pick.';out.append(x)
    else: out.append(r)
  return out
# study file
d=json.load(open('study/nov12.json'));d2=split(d);json.dump(d2,open('study/nov12.json','w'))
gr=json.load(open('study/nov12_graded.json'))['graded']
gr=[x for x in gr if x[2] not in SPL]
for v in SPL.values():
  for p,pct,res in v: gr.append([pct,1 if res=='W' else 0,p])
json.dump({'graded':gr},open('study/nov12_graded.json','w'))
a7=[x for x in gr if x[0]>=70];print('rows',len(d2),'graded',len(gr),'hits',sum(x[1] for x in gr),'70+',sum(x[1] for x in a7),len(a7))
p='bettordays-hq.html';s=open(p).read()
i=s.index('const THU=');j=s.index(';\n',i);a=json.loads(s[i+10:j]);a=split(a)
s=s[:i+10]+json.dumps(a)+s[j:]
open(p,'w').write(s);print('site rows',len(a))
