rows=[]
def add(p,st,k,under=False,moved=False,orig=None,style=None):
  team=L[p]['team'];cf=st in('rush','recyds');g=G[team]
  pr,(mu,hs,n,h5,m5)=prob(p,st,k)
  if under: pr=1-pr;hs=n-hs;h5=m5-h5
  pct=0.8*100*pr+0.2*65
  madj,mtxt,mtag=(0,'','') if cf else matchup(team,st,under)
  pct+=madj
  b2b=team in B2B
  if b2b: pct-=(3 if st in('pts','3pm','pra') else 2)*(-1 if under else 1)
  hard=70 if cf else (80 if st=='pra' else 88)
  if n<8: pct=0.7*pct+0.3*60
  pct=max(5,round(min(pct,hard)))
  kk=None if cf else KT.get((nrm(L[p]['disp']),st),{}).get(k)
  kp=None if kk is None else (100-kk if under else kk)
  txt=f"{p} under {k} {WORD[st]}" if under else f"{p} {k}+ {WORD[st]}"
  note=f"{'Stayed under' if under else 'Hit'} {hs} of {n} this season, {h5} of {m5} last 5 (avg {mu:.1f} {UN[st]}). {mtxt} {CTX.get(p,'')}"
  if b2b and 'back-to-back' not in note: note+=' Second night of a back-to-back.'
  if cf: note+=' College football. Kalshi does not offer this market, so it is capped at 70.'
  if kp is not None:
    if kp<=pct-15: note+=f" Kalshi has this at {kp}, far below us. Look twice."
    elif kp>=pct+15: note+=f" Kalshi has this at {kp}, well above us."
  if orig: note=f"Your line was {orig}. "+note
  elif moved: note='Moved line. '+note
  r=dict(p=txt,pct=pct,g=g[0],t=g[1],ty='prop',st=style or ('alt' if moved else 'reg'),n=re.sub(r'\s+',' ',note).strip(),sp='CFB' if cf else 'NBA')
  if kp is not None: r['k']=kp
  if mtag: r['mu']=mtag
  if moved or orig: r['moved']=True
  if b2b: r['b2b']=1
  if team=='WMU': r['fl']='LIVE'
  rows.append(r)
