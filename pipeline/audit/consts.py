import json,re,sys
s=open(sys.argv[1]).read()
dec=json.JSONDecoder()
out={}
for m in re.finditer(r'const ([A-Z0-9_]+)=',s):
  name=m.group(1); j=m.end()
  if s[j] not in '[{': continue
  try: v,_=dec.raw_decode(s[j:])
  except Exception as e: continue
  out[name]=v
json.dump(out,open(sys.argv[2],'w'))
for k,v in out.items():
  n=len(v); smp=v[0] if isinstance(v,list) and v else (list(v)[:6] if isinstance(v,dict) else v)
  print(k,type(v).__name__,n,str(smp)[:220])
