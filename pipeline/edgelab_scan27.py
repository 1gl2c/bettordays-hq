import json,re,unicodedata
nm=lambda s: re.sub(r'[^a-z ]','',unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode().lower().replace(' jr','')).strip()
BK={}
for r in open('daily/2026-11-27/book_lines.txt').read().strip().split(';'):
    p,m,l,b,f=r.split('|'); BK[(nm(p),m,int(float(l)+0.5))]=(int(b),float(f))
SM={'KXNBA3PT':'threes','KXNBAAST':'assists','KXNBAPRA':'points_rebounds_assists','KXNBAPTS':'points','KXNBAREB':'rebounds'}
LBL={'threes':'threes','assists':'assists','points_rebounds_assists':'PRA','points':'points','rebounds':'rebounds'}
OUT=set(json.load(open('betafri27/inj_sets.json'))['out']); Q=set(json.load(open('betafri27/inj_sets.json')).get('q',[]))
fee=lambda a:a+0.07*a*(1-a)
K=json.load(open('fri27/kalshi.json')); rows=[]
for s_,st in SM.items():
    for m in K.get(s_,[]):
        if '26NOV27' not in m['event_ticker']: continue
        g=m['event_ticker'].split('-')[1][7:]
        pl,n=m['yes_sub_title'].rsplit(':',1); pl=pl.strip(); n=int(n.strip().rstrip('+'))
        if 'harden' in pl.lower() or pl in OUT: continue
        a=float(m.get('yes_ask_dollars') or 0)
        if not 0.5<=a<=0.95: continue
        b=BK.get((nm(pl),st,n))
        if not b or b[0]<2: continue
        rows.append(dict(p=f'{pl} {n}+ {LBL[st]}',pl=pl,st=st,g=g,k=round(a*100),bk=round(b[1]*100,1),books=b[0],gap=round(100*(b[1]-fee(a)),1),q=pl in Q))
rows.sort(key=lambda r:-r['gap'])
json.dump(rows,open('daily/2026-11-27/edge_scan.json','w'),indent=1)
for r in rows[:30]: print(r['gap'],r['k'],r['bk'],r['books'],r['p'],r['g'],'Q' if r['q'] else '')
