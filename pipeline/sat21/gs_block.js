 if(V7D.all){h+=`<h3 style="margin-top:20px" id="gsTop">Full grade sheet <small id="gsCount">all ${V7D.all.length} legs, under 70 included</small></h3><p class="note" style="max-width:780px">Published = what the board shows. Our grade is the middle of the four blind AI numbers plus our system grade. <b>Our system</b> is our own grade from game logs and matchup, computed before the models ran. <b>Books</b> = the sportsbooks' fair chance with the vig removed (NBA props only, from Nov 21). <b>Kalshi vs ours</b> = Kalshi minus our published grade: plus means the market likes the leg more than we do. When our grade is 8+ above Kalshi the leg is pulled (market disagrees).</p><div id="gsF" class="gsf"></div><div class="scroll"><table class="rtab"><thead><tr><th>Leg</th><th>Game</th><th>Published</th><th>Kalshi</th><th>Kalshi vs ours</th><th title="DraftKings, FanDuel and other books with the vig removed">Books</th><th>Our system</th><th>ChatGPT · Gemini · Grok · Claude</th><th>AI split</th><th>Where</th></tr></thead><tbody id="gsB"></tbody></table></div>`;
  setTimeout(gsInit,0)}
 function gsInit(){const A=V7D.all,box=document.getElementById('gsF'),tb=document.getElementById('gsB');if(!box||!tb)return;
  const ai=x=>['chatgpt','gemini','grok','claude'].map(k=>x.ms[k]).filter(v=>v!=null);
  const split=x=>{const v=ai(x);return v.length>1?Math.max(...v)-Math.min(...v):null};
  const kv=x=>x.k!=null&&x.pub!=null?x.k-x.pub:null;
  const live=x=>x.fl==='started'||x.fl==='finished';
  const VIEWS=[['all','All'],['pub','On the board (70+)'],['kup','Kalshi higher than ours'],['kdown','Ours higher than Kalshi'],['rem','Market disagrees (pulled)'],['G','GREEN'],['Y','YELLOW'],['N','No Kalshi'],['low','Under 70'],['agree','AIs agree (within 5)'],['split','AIs split (15+ apart)'],['fade','Fade flagged'],['books','Has sportsbook price'],['open','Not started'],['live','Started or finished']];
  const PASS={all:()=>true,pub:x=>x.pl==='board',kup:x=>kv(x)!=null&&kv(x)>0,kdown:x=>kv(x)!=null&&kv(x)<0,rem:x=>x.pl==='removed',G:x=>x.tier==='G'&&x.pub!=null,Y:x=>x.tier==='Y',N:x=>x.tier==='N',low:x=>x.pl==='under 70',agree:x=>split(x)!=null&&split(x)<=5,split:x=>split(x)!=null&&split(x)>=15,fade:x=>x.fade>0,books:x=>x.bk!=null,open:x=>!live(x),live};
  const SPS=['All',...new Set(A.map(x=>x.sp).filter(Boolean))];
  const SORTS=[['pub','Published, high to low'],['kup','Kalshi minus ours, biggest first'],['k','Kalshi, high to low'],['bk','Books, high to low'],['split','AI split, biggest first'],['game','Game time']];
  let st={v:'all',sp:'All',so:'pub',q:''};try{Object.assign(st,JSON.parse(sessionStorage.getItem('bd_gs')||'{}'))}catch(e){}
  if(!PASS[st.v])st.v='all';if(!SPS.includes(st.sp))st.sp='All';
  const esc=x=>String(x).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
  const chip=(grp,k,l,on)=>`<button type="button" class="gsc${on?' on':''}" data-g="${grp}" data-k="${esc(k)}" aria-pressed="${on}">${l}</button>`;
  const cnt=k=>A.filter(x=>PASS[k](x)&&(st.sp==='All'||x.sp===st.sp)).length;
  const tmin=x=>{const r=typeof ptStart==='function'?ptStart(x.t):null;return r==null?9e15:+r};
  box.innerHTML=`<div class="row" id="gsV"></div><div class="row" id="gsSp" style="margin-top:6px"></div><div style="display:flex;gap:8px;flex-wrap:wrap;margin:8px 0 10px"><input id="gsQ" type="search" placeholder="Search a player or team" aria-label="Search a player or team" style="flex:1;min-width:180px;padding:9px 10px;background:transparent;border:1px solid var(--line);color:inherit;font:inherit"><select id="gsS" aria-label="Sort" style="padding:9px;background:var(--bg);border:1px solid var(--line);color:inherit;font:inherit">${SORTS.map(([k,l])=>`<option value="${k}">${l}</option>`).join('')}</select></div>`;
  const qi=document.getElementById('gsQ'),so=document.getElementById('gsS');qi.value=st.q;so.value=st.so;
  const draw=()=>{try{sessionStorage.setItem('bd_gs',JSON.stringify(st))}catch(e){}
   document.getElementById('gsV').innerHTML=VIEWS.map(([k,l])=>chip('v',k,`${l}<small>${cnt(k)}</small>`,st.v===k)).join('');
   document.getElementById('gsSp').innerHTML=SPS.map(k=>chip('sp',k,k,st.sp===k)).join('');
   const q=st.q.trim().toLowerCase();
   let R=A.filter(x=>PASS[st.v](x)&&(st.sp==='All'||x.sp===st.sp)&&(!q||(x.p+' '+x.g).toLowerCase().includes(q)));
   const key={pub:x=>-(x.pub??-1),kup:x=>-(kv(x)??-99),k:x=>-(x.k??-1),bk:x=>-(x.bk??-1),split:x=>-(split(x)??-1),game:tmin}[st.so];
   R=R.slice().sort((a,b)=>key(a)-key(b));
   document.getElementById('gsCount').textContent=`${R.length} of ${A.length} legs`;
   tb.innerHTML=R.map(x=>{const d=kv(x),sp=split(x);return `<tr${x.rule?' style="opacity:.55"':''}><td>${x.p}${x.rule?' <small>(Ace rule)</small>':''}${x.fl==='Q'?' <small>(questionable)</small>':x.fl==='started'?' <small style="color:var(--warn)">(started, pregame grade)</small>':x.fl==='finished'?' <small>(finished before the board)</small>':''}${x.fade?` <small style="color:var(--warn)">fade flag x${x.fade}</small>`:''}${x.why?`<br><small>${x.why}</small>`:''}</td><td class="lbl">${x.g} ${x.t}</td><td class="mono"><b>${x.pub??'-'}</b></td><td class="mono">${x.k??'none'}</td><td class="mono" style="color:${d==null?'inherit':d>0?'var(--acc)':d<0?'var(--warn)':'inherit'}">${d==null?'-':(d>0?'+':'')+d}</td><td class="mono">${x.bk??'-'}</td><td class="mono">${x.sys??'-'}</td><td class="mono"><small>${['chatgpt','gemini','grok','claude'].map(k=>x.ms[k]??'-').join(' · ')}</small></td><td class="mono" style="color:${sp!=null&&sp>=15?'var(--warn)':'inherit'}">${sp??'-'}</td><td class="lbl">${x.pl}</td></tr>`}).join('')||'<tr><td colspan="10" class="note">No legs match these filters.</td></tr>'};
  box.addEventListener('click',e=>{const b=e.target.closest('button.gsc');if(!b)return;if(b.dataset.g==='v')st.v=b.dataset.k;else st.sp=b.dataset.k;draw()});
  qi.addEventListener('input',()=>{st.q=qi.value;draw()});so.addEventListener('change',()=>{st.so=so.value;draw()});
  draw()}
