"""Append Nov 19 graded legs to record.json (record explorer), in the same format as earlier nights.
Source rows: thu/res/db_rows.json, built from thu/thu_graded.json with the same fields as model_picks for 2026-11-19 (result and grade set; checked against the database)."""
import json
R=json.load(open('../record.json')); L=R['legs']
assert not any(x['d']=='Nov 19' for x in L)
rows=json.load(open('thu/res/db_rows.json'))
M={'td':'atd','rr':'combo','rushatt':'other'}
for r in rows:
    st=r['st'] if r['st'] else r['mkt']
    st=M.get(st,st)
    L.append({'d':'Nov 19','wk':'Nov 16-22','sp':r['sp'],'st':st,'dir':r['dir'],'g':r['g'],'res':r['res'],'k':r['k'],'ln':r['ln'],'p':r['p']})
n=len(L); nk=sum(1 for x in L if x['k'] is not None)
R['meta']=f"Source: the model_picks database. <b>{n}</b> graded legs from Nov 4 to Nov 19, 2026. <b>{nk}</b> have a Kalshi price. Nov 4 to 17 use the last Kalshi quote before tip-off; Nov 18 on uses the price at the moment we graded (timestamped). Pushes on whole-number lines are not counted. Results corrected after box-score checks are logged in the database."
json.dump(R,open('../record.json','w'),separators=(',',':') if False else None)
print(n,nk,len(rows))
