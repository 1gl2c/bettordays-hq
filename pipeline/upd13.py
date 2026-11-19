import json
p='bettordays-hq.html';s=open(p).read()
G=json.load(open('study/nov12_graded.json'))['graded']
res={x[2]:x[1] for x in G}
for k in ["Joel Embiid 20+ points","Joel Embiid 15 + points","Joel Embiid 6+ rebounds"]: res.pop(k,None)
i=s.index('const THU=');j=s.index(';\n',i)
a=json.loads(s[i+10:j]);n=0
for r in a:
  if r['p'] in res: r['r']='W' if res[r['p']] else 'L'; n+=1
  else: r['r']=''
s=s[:i+10]+json.dumps(a)+s[j:]
print('THU graded',n)
day=open('day.txt').read()
assert "const DAYS=[\n" in s
s=s.replace("const DAYS=[\n","const DAYS=[\n"+day,1)
rep=json.load(open('rep.json'))
for o,nw in rep:
  assert o in s,o[:60]; s=s.replace(o,nw)
sec=open('sec.html').read()
s=s.replace('<section class="panel" id="thursday">',sec+'<section class="panel" id="thursday">',1)
o="thursday:'home',review11:'history',"; assert o in s
s=s.replace(o,"thursday:'home',review12:'home',review11:'history',")
open(p,'w').write(s);print('ok')
