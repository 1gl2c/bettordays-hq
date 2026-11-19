const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage();
await p.route(/supabase|jsdelivr|sb\.js|gate\.js|install\.js/,r=>r.abort());
await p.goto('file://'+require('path').resolve(__dirname,'../../index.html')+'#/research');await p.waitForTimeout(900);
const o=await p.evaluate(()=>{const S=x=>x.legs.map(r=>({pick:r.pick,grade:r.est,hit:r.hit,stat:r.stat,game:r.g||null}));return {bt:__RS.bt.map(b=>({d:b.d,three:{x:b.three.x,legs:S(b.three)},ten:{x:b.ten.x,legs:S(b.ten)}})),perfect:__RS.perfect.map(q=>({d:q.d,h:q.h,n:q.n,a:{x:q.a.x,legs:q.a.legs.map(r=>({pick:r.pick,grade:r.est}))},b:{x:q.b.x,legs:q.b.legs.map(r=>({pick:r.pick,grade:r.est}))}}))}});
require('fs').writeFileSync(process.argv[2]||'rs_export.json',JSON.stringify(o));console.log(o.bt.length,o.perfect.length,JSON.stringify(o.perfect[0]).slice(0,300));await b.close()})();
