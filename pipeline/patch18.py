import re
s=open('bettordays-hq.html').read()
# 1. nav
a=s.index('    <nav class="nav" aria-label="Sections">'); b=s.index('    </nav>',a)+len('    </nav>')
s=s[:a]+'''    <nav class="nav" aria-label="Pages">
      <a class="btn" data-go="home" href="/">Home</a><a class="btn" data-go="history" href="/history">History</a><a class="btn" data-go="results" href="/results">Results</a><a class="btn" data-go="method" href="/method">How it works</a><a class="btn hot" href="/app#/board">Pick &amp; post</a><a class="btn" href="/app#/chat">Chat</a><a class="btn" href="/app#/leaders">Leaders</a><button class="btn" id="tourBtn" type="button" aria-label="Take the tour">? Tour</button>
    </nav>'''+s[b:]
s=s.replace('.nav{display:flex;flex-wrap:wrap;gap:6px}','.nav{display:flex;flex-wrap:wrap;gap:6px}.nav .btn.on{border-color:var(--acc);color:var(--acc);box-shadow:0 0 14px rgba(4,255,159,.18)}.nav .btn.hot{background:var(--acc);color:#04120b;border-color:var(--acc);font-weight:700}[data-pg][hidden]{display:none!important}',1)
s=re.sub(r'<span class="lbl">Wednesday Nov 11 board live · \d+ graded legs since Nov 4</span>','<span class="lbl">Thursday board drops 2 PM PT · 502 graded legs since Nov 4</span>',s)
# 2. next-board placeholder on home
nb='''  <section class="panel" id="nextboard">
    <h2>Thursday board · Nov 12 <small>lands here when the cappers drop</small></h2>
    <p class="note" style="max-width:720px">Every capper pick, graded with a real hit %, plus the lines we move. When it lands you'll be able to filter by sport and by tip time, so at 4:30 you can pull up just the games that haven't started. Yesterday's graded board lives in <a href="#wednesday">History</a>.</p>
  </section>
'''
s=s.replace('  <section class="panel" id="review11">',nb+'  <section class="panel" id="review11">',1)
# 3. board filters (generic: sport + time)
old=re.search(r"let F='all';const L=\[\['all','All'\],\['70','70%\+'\],\['clean','Clean \(no flags\)'\],\['nba','NBA'\],\['late'.*?\n const fe=document.getElementById\('wedF'\);fe.innerHTML=L.map\(\(\[k,n\]\)=>`<button class=\"btn \$\{k===F\?'on':''\}\" data-f=\"\$\{k\}\" type=\"button\">\$\{n\}</button>`\).join\(''\);\n const ok=x=>.*?;\n",s,re.S).group(0)
new='''let F='all',SP='all',TM='any';const L=[['all','All'],['70','70%+'],['clean','Clean (no flags)'],['move','Moved lines'],['ml','Moneylines'],['prop','Props'],['reg','Regular lines'],['alt','Alts'],['flag','Flagged']];
 const fe=document.getElementById('wedF');fe.innerHTML=L.map(([k,n])=>`<button class="btn ${k===F?'on':''}" data-f="${k}" type="button">${n}</button>`).join('');
 const BF=boardFilters(fe,WED,'2026-11-11',(sp,tm)=>{SP=sp;TM=tm;draw()});
 const ok=x=>BF.pass(x)&&(F==='all'||(F==='clean'&&!x.fl)||(F==='70'&&x.pct>=70)||(F==='move'&&x.moved)||(F==='flag'&&x.fl)||x.ty===F||x.st===F);
'''
s=s.replace(old,new)
helper=r'''/* board filters: sport + tip time (PT) */
function boardFilters(after,rows,day,cb){const SPN={NBA:'🏀 NBA',NHL:'🏒 NHL',CFB:'🏈 College FB',CBB:'🏀 College hoops',TEN:'🎾 Tennis',NFL:'🏈 NFL',MLB:'⚾ MLB'};
 const mins=t=>{const m=/^(\d{1,2}):(\d{2})/.exec(t||'');if(!m)return null;let h=+m[1];if(h<12)h+=12;return h*60+ +m[2]};
 const fmt=new Intl.DateTimeFormat('en-US',{timeZone:'America/Los_Angeles',hourCycle:'h23',year:'numeric',month:'2-digit',day:'2-digit',hour:'2-digit',minute:'2-digit'});
 const now=()=>{const p={};fmt.formatToParts(new Date()).forEach(x=>p[x.type]=x.value);return{d:`${p.year}-${p.month}-${p.day}`,m:(+p.hour)*60+(+p.minute)}};
 const sports=[...new Set(rows.map(r=>r.sp))];const times=[...new Set(rows.map(r=>mins(r.t)).filter(x=>x!=null))].sort((a,b)=>a-b);
 const lab=m=>`${(Math.floor(m/60)%12)||12}:${String(m%60).padStart(2,'0')}`;
 let sp='all',tm='any';const box=document.createElement('div');box.className='bfil';after.after(box);
 const draw=()=>{box.innerHTML=`<div class="bfrow"><span class="lbl">Sport</span>${[['all','All sports'],...sports.map(k=>[k,SPN[k]||k])].map(([k,n])=>`<button class="btn sm ${k===sp?'on':''}" data-sp="${k}" type="button">${n}</button>`).join('')}</div><div class="bfrow"><span class="lbl">Tip time</span>${[['any','Any time'],['up','⏱ Not started yet'],...times.map(m=>['t'+m,lab(m)+' PM & later'])].map(([k,n])=>`<button class="btn sm ${k===tm?'on':''}" data-tm="${k}" type="button">${n}</button>`).join('')}</div>`};
 draw();box.onclick=e=>{const b=e.target.closest('button');if(!b)return;if(b.dataset.sp)sp=b.dataset.sp;if(b.dataset.tm)tm=b.dataset.tm;draw();cb(sp,tm)};
 return{pass:x=>{if(sp!=='all'&&x.sp!==sp)return false;if(tm==='any')return true;const m=mins(x.t);if(m==null)return false;if(tm==='up'){const n=now();if(n.d<day)return true;if(n.d>day)return false;return m>n.m}return m>=+tm.slice(1)}}}
'''
s=s.replace('const WED=',helper+'const WED=',1)
s=s.replace('.fl.x{border-color:var(--bad);color:var(--bad)}','.fl.x{border-color:var(--bad);color:var(--bad)}\n.bfil{display:grid;gap:6px;margin:8px 0 10px}.bfrow{display:flex;flex-wrap:wrap;gap:6px;align-items:center}.bfrow .lbl{min-width:70px}.btn.sm{font-size:11px;padding:6px 9px}.btn.on{border-color:var(--acc);color:var(--acc)}',1)
# 4. router + tour
router=r'''/* pages router */
(function(){const MAP={drop:'home',nextboard:'home',review11:'home',wednesday:'history',review10:'history',tuesday:'history',monday:'history',recap9:'history',recap:'history',sunday:'history',ledger:'results',legs:'results',marbles:'method',thesis:'method',edge:'method',structure:'method',lotto:'method'};
 const T=document.querySelector('.tiles');if(T)T.dataset.pg='home';
 Object.entries(MAP).forEach(([id,p])=>{const e=document.getElementById(id);if(e)e.dataset.pg=p});
 document.querySelectorAll('.wrap > section').forEach(e=>{if(!e.dataset.pg)e.dataset.pg='history'});
 const PAGES=['home','history','results','method'];
 const cur=()=>{const h=location.hash.replace(/^#\/?/,'');if(PAGES.includes(h))return h;const e=h&&document.getElementById(h);if(e&&e.dataset.pg)return e.dataset.pg;const p=location.pathname.replace(/^\/|\/$/g,'');return PAGES.includes(p)?p:'home'};
 const go=(p,id)=>{document.querySelectorAll('[data-pg]').forEach(e=>e.hidden=e.dataset.pg!==p);document.querySelectorAll('.nav [data-go]').forEach(a=>a.classList.toggle('on',a.dataset.go===p));const e=id&&document.getElementById(id);if(e)e.scrollIntoView({block:'start'});else window.scrollTo(0,0)};
 window.BDgo=go;
 document.addEventListener('click',e=>{const a=e.target.closest('a[data-go]');if(!a)return;e.preventDefault();const p=a.dataset.go;try{history.pushState(null,'',p==='home'?'/':'/'+p)}catch(_){location.hash='#/'+p}go(p)});
 window.addEventListener('popstate',()=>go(cur()));
 window.addEventListener('hashchange',()=>{const h=location.hash.slice(1);const e=document.getElementById(h);if(e)go(e.dataset.pg||'home',h);else go(cur())});
 const h0=location.hash.slice(1);go(cur(),document.getElementById(h0)?h0:null);})();
/* guided tour */
(function(){const S=[['.nav [data-go="home"]','Home','Today lives here: the countdown to the next drop, the record, yesterday\'s recap, and today\'s board once it lands.'],
 ['#drop','The countdown','Board drops by 2 PM PT, tickets by 3. When it hits zero, today\'s picks are up. Members get the bell.'],
 ['.tiles','The record','Every number here is graded against the real box score. Wins and losses.'],
 ['.nav [data-go="history"]','History','Every past day: the board, every ticket, and what we learned.'],
 ['.nav [data-go="results"]','Results','The full ledger and every single leg we have ever graded.'],
 ['.nav [data-go="method"]','How it works','How a pick gets its hit %, and why 3 legs at 70%+ is the play.'],
 ['.nav .hot','Pick & post','Make a free account, tap legs straight off the board, and post your ticket to the feed.']];
 let i=0,box,ring;const end=()=>{box&&box.remove();ring&&ring.remove();try{localStorage.setItem('bd_tour','1')}catch(e){}};
 const show=()=>{const [sel,h,t]=S[i];const el=document.querySelector(sel);if(!el||el.offsetParent===null&&sel!=='.nav .hot'){i++;return i<S.length?show():end()}
  el.scrollIntoView({block:'center'});const r=el.getBoundingClientRect();
  ring=ring||document.body.appendChild(Object.assign(document.createElement('div'),{className:'tring'}));box=box||document.body.appendChild(Object.assign(document.createElement('div'),{className:'tbox'}));
  Object.assign(ring.style,{top:r.top+scrollY-6+'px',left:r.left+scrollX-6+'px',width:r.width+12+'px',height:Math.min(r.height,320)+12+'px'});
  box.innerHTML=`<span class="lbl acc">${i+1} of ${S.length}</span><b>${h}</b><p>${t}</p><div class="row"><button class="btn sm" data-x="skip" type="button">Skip</button><button class="btn sm hot" data-x="next" type="button">${i===S.length-1?'Done':'Next'}</button></div>`;
  const top=r.bottom+scrollY+14,fits=r.bottom+170<innerHeight;Object.assign(box.style,{top:(fits?top:Math.max(scrollY+10,r.top+scrollY-170))+'px',left:Math.max(10,Math.min(r.left+scrollX,scrollX+innerWidth-330))+'px'});
  box.onclick=e=>{const x=e.target.dataset.x;if(x==='skip')end();if(x==='next'){i++;i<S.length?show():end()}}};
 const start=()=>{i=0;if(window.BDgo)window.BDgo('home');setTimeout(show,150)};
 document.getElementById('tourBtn').onclick=start;
 let seen=false;try{seen=!!localStorage.getItem('bd_tour')}catch(e){seen=true}
 if(!seen&&!/join=1/.test(location.search))setTimeout(start,1800);})();
'''
s=s.replace('/* daily drop countdown, Pacific time */',router+'/* daily drop countdown, Pacific time */',1)
s=s.replace('.bfil{','.tring{position:absolute;z-index:9998;border:2px solid var(--acc);box-shadow:0 0 0 9999px rgba(0,0,0,.55),0 0 24px rgba(4,255,159,.5);pointer-events:none;transition:all .25s}.tbox{position:absolute;z-index:9999;width:320px;max-width:calc(100vw - 20px);background:#0e1412;border:1px solid var(--acc);padding:14px;box-shadow:0 10px 40px rgba(0,0,0,.6)}.tbox b{display:block;font-family:var(--display);font-size:20px;text-transform:uppercase;margin:4px 0}.tbox p{margin:0 0 10px;color:#cfd8d4;font-size:14px;line-height:1.45}.tbox .row{display:flex;justify-content:flex-end;gap:8px}.btn.hot{background:var(--acc);color:#04120b;border-color:var(--acc)}\n.bfil{',1)
open('bettordays-hq.html','w').write(s)
print('ok')
