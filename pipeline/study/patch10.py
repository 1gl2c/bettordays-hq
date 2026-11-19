import json,sys
sys.path.insert(0,'study'); from mon import M
p='bettordays-hq.html'; h=open(p).read()
def rep(a,b):
    global h
    assert a in h,a[:80]; h=h.replace(a,b,1)
MON=[dict(p=a,pct=b,g=c,t=d,ty=e,st=f,n=g,fl=fl) for a,b,c,d,e,f,g,fl in M]
FLN={'QB':'Backup QB passing leg','PRA':'PRA combo (big cushion)','AST':'Assist over','GREB':'Guard rebound over','CBB':'College','NHL':'Hockey','VERIFY':'Team not verified','OUT':'Player OUT'}
sec='''
  <section class="panel" id="monday">
    <h2>Monday board · Nov 9 <small>'''+str(len(MON))+''' picks graded</small></h2>
    <div class="flags" style="margin-bottom:14px">
      <div class="flag"><b>Luka is OUT</b><div class="r bad">dead leg</div><p>Lakers list Luka out with a back injury. His under 34.5 voids at best. Ziaire Williams and Kessler get more shots.</p><div class="who">Source: Lakers vs Hawks injury report, Nov 9</div></div>
      <div class="flag w"><b>Wentz starts for Minnesota</b><div class="r warn">QB check</div><p>Kyler Murray is out with a hamstring. Wentz's start was announced Thursday, so the prices already have him in. Vikings passing overs are tagged, Bills legs are clean.</p><div class="who">BUF -3, total 43.5. MIN is No. 1 in scoring and pass defense</div></div>
      <div class="flag w"><b>Nuggets and Raptors in flux</b><div class="r warn">day-to-day</div><p>Jokic, Murray, Gordon, Braun and DeRozan all day-to-day. Barnes and Quickley questionable, Kawhi out. Check status at lock.</p><div class="who">Pelicans without Zion and Trey Murphy. Hornets without Miller, Knueppel, Schroder</div></div>
    </div>
    <h3>Clean 70 pool · today's Lotto Lab legs</h3>
    <p class="note" style="margin:4px 0 8px">Graded 70%+, NBA and NFL only, no flags. One leg per player. This is the pool the lotto gets built from.</p>
    <div class="chips" id="monPool"></div>
    <div class="two" style="margin-top:18px">
      <div><h3>Top 25: any line</h3><ol class="mono" id="monAny" style="margin:8px 0 0;padding-left:22px;font-size:12.5px;line-height:1.75"></ol></div>
      <div><h3>Top 25: regular lines</h3><ol class="mono" id="monReg" style="margin:8px 0 0;padding-left:22px;font-size:12.5px;line-height:1.75"></ol></div>
    </div>
    <div class="filters" id="monF" style="margin-top:16px"></div>
    <div class="scroll" style="max-height:620px;overflow-y:auto"><table id="monT"></table></div>
  </section>
'''
rep('\n  <section class="panel reveal" id="recap">',sec+'\n  <section class="panel reveal" id="recap">')
rep('<a class="btn" href="#recap">Results</a>','<a class="btn" href="#monday">Monday</a><a class="btn" href="#recap">Results</a>')
rep('Process audit · Nov 4 to 8 · 295 graded legs','Monday Nov 9 board live · 295 graded legs since Nov 4')
css='''.chips{display:flex;flex-wrap:wrap;gap:8px}
.chip{border:1px solid rgba(4,255,159,.45);background:rgba(4,255,159,.06);padding:7px 10px;font-size:12.5px;display:flex;gap:8px;align-items:baseline}
.chip b{font-family:var(--mono);color:var(--acc)}.chip small{color:var(--mute);font-family:var(--mono);font-size:10px}
.fl{font-family:var(--mono);font-size:10px;letter-spacing:.06em;text-transform:uppercase;border:1px solid var(--warn);color:var(--warn);padding:1px 5px;margin-left:6px;white-space:nowrap}
.fl.x{border-color:var(--bad);color:var(--bad)}
'''
rep('</style>',css+'</style>')
js='''
const MON='''+json.dumps(MON,separators=(',',':'))+''';
const FLN='''+json.dumps(FLN)+''';
(function(){const fl=x=>x.fl?`<span class="fl ${x.fl==='OUT'?'x':''}">${FLN[x.fl]||x.fl}</span>`:'';
 const live=MON.filter(r=>r.pct>0);
 const seen=new Set(),pool=live.filter(r=>r.pct>=70&&!r.fl).sort((a,b)=>b.pct-a.pct).filter(r=>{const k=r.p.split(' ')[0]+(r.p.includes('Wemby')?'W':'');if(r.p.startsWith('Wemby')){if(seen.has('wemby'))return false;seen.add('wemby');return r.p==='Wemby U50 PRA'}return true});
 document.getElementById('monPool').innerHTML=pool.map(r=>`<span class="chip">${r.p} <b>${r.pct}</b><small>${r.g} ${r.t}</small></span>`).join('')+`<span class="chip" style="border-color:var(--line);background:none"><small>${pool.length} legs · all hit about ${(Math.pow(.88,pool.length)*100).toFixed(1)}% at 88% per leg</small></span>`;
 document.getElementById('monAny').innerHTML=[...live].sort((a,b)=>b.pct-a.pct).slice(0,25).map(r=>`<li>${r.p} <span style="color:#04ff9f">${r.pct}%</span>${fl(r)}</li>`).join('');
 document.getElementById('monReg').innerHTML=live.filter(r=>r.st==='reg').sort((a,b)=>b.pct-a.pct).slice(0,25).map(r=>`<li>${r.p} <span style="color:#00c8ff">${r.pct}%</span>${fl(r)}</li>`).join('');
 let F='all';const L=[['all','All'],['clean','Clean (no flags)'],['nfl','MNF'],['nba','NBA'],['ml','Moneylines'],['prop','Props'],['reg','Regular lines'],['alt','Alts'],['flag','Flagged']];
 const fe=document.getElementById('monF');fe.innerHTML=L.map(([k,n])=>`<button class="btn ${k===F?'on':''}" data-f="${k}" type="button">${n}</button>`).join('');
 const ok=x=>F==='all'||(F==='clean'&&!x.fl)||(F==='nfl'&&x.g==='BUF@MIN')||(F==='nba'&&/@(DET|CLE|ATL|TOR|DAL|HOU|PHX|GSW)$/.test(x.g))||(F==='flag'&&x.fl)||x.ty===F||x.st===F;
 const draw=()=>{const r=MON.filter(ok).sort((a,b)=>b.pct-a.pct);document.getElementById('monT').innerHTML='<thead><tr><th>#</th><th>Pick</th><th>Grade</th><th>Hit %</th><th>Game</th><th>PT</th><th>Note</th></tr></thead><tbody>'+r.map((x,i)=>`<tr><td class="mono" style="color:#5b6b64">${i+1}</td><td>${x.p}<span class="tag">${x.st.toUpperCase()}</span>${fl(x)}</td><td class="mono">${x.pct?SG(x.pct):'X'}</td><td class="mono"><span class="minibar"><i style="width:${x.pct}%"></i></span>${x.pct||'OUT'}</td><td class="lbl">${x.g}</td><td class="mono">${x.t}</td><td style="color:#8a9a93;white-space:normal;min-width:180px">${x.n}</td></tr>`).join('')+'</tbody>'};
 fe.onclick=e=>{const b=e.target.closest('button');if(!b)return;F=b.dataset.f;fe.querySelectorAll('.btn').forEach(x=>x.classList.toggle('on',x===b));draw()};draw();})();
'''
i=h.rindex('</script>'); h=h[:i]+js+h[i:]
open(p,'w').write(h.replace('—',','))
print('ok',len(MON))
