"""Make the SQL that loads learn/hammer_learn.json and new log rows into Supabase (hammer_learn, hammer_learn_log)."""
import json, sys
L = json.load(open('learn/hammer_learn.json')); G = json.load(open('learn/hammer_learn_log.json'))
q = lambda x: 'null' if x is None else ("'" + str(x).replace("'", "''") + "'" if isinstance(x, str) else str(x))
v = ','.join(f"({q(L['as_of'])},{q(g['level'])},{q(g['group'])},{g['n']},{g['w']},{g['hit']},{g['price']},{g['shrunk']},{g['fee_price']},{q(g['status'])})" for g in L['groups'])
sql = f"delete from public.hammer_learn where as_of={q(L['as_of'])};\ninsert into public.hammer_learn (as_of,level,group_name,n,w,hit,price,shrunk,fee_price,status) values {v};\n"
lg = [x for x in G if x['date'] == L['as_of']]
if lg:
    sql += f"delete from public.hammer_learn_log where date={q(L['as_of'])};\ninsert into public.hammer_learn_log (date,group_name,was,now,n,hit,shrunk,fee_price) values " + ','.join(f"({q(x['date'])},{q(x['group'])},{q(x['was'])},{q(x['now'])},{x['n']},{x['hit']},{x['shrunk']},{x['fee_price']})" for x in lg) + ";\n"
open('learn/load.sql', 'w').write(sql); print(len(L['groups']), 'groups', len(lg), 'log rows')
