"""Beta Test Mode: filters on the agent simulation table (Ace, Nov 20).
View buttons: All lines · ★ Master filter · each agent's picks · our sim's picks.
Master filter = at least 3 of the 4 agents above break-even, consensus above break-even, and only points, assists or threes
(rebounds and PRA have been the weakest groups on both our board and the sim record). Shows what the record says so far."""
import re
F='bettordays-hq.html';s=open(F).read()
a=s.index("(function(){const el=document.getElementById('v8sims');");E2="V=b.dataset.sv;draw()});draw()})();"
b=(s.index(E2,a)+len(E2)) if E2 in s[a:a+20000] else s.index("el.innerHTML=h})();",a)+len("el.innerHTML=h})();")
js=r'''(function(){const el=document.getElementById('v8sims');if(!el||typeof V8SIM==='undefined'||!V8SIM)return;
 const MN={chatgpt:'ChatGPT',gemini:'Gemini',grok:'Grok',claude:'Claude'},W={pts:'points',reb:'rebounds',ast:'assists','3pm':'threes',pra:'PRA'};
 const ag=Object.keys(MN).filter(k=>V8SIM.status[k]&&V8SIM.status[k]!=='no reply');
 const ts=document.getElementById('v8simTs');if(ts)ts.textContent=Object.entries(V8SIM.status).map(([k,v])=>`${MN[k]}: ${v}`).join(' · ');
 const nm=z=>`${z.player} ${z.k}+ ${W[z.st]}`;const c=(v,be)=>v==null?'-':`<span style="color:${v>be?'var(--acc)':'inherit'}">${v}</span>`;
 const MS=z=>z.cons!=null&&z.nagree>=3&&z.edge>0&&['pts','ast','3pm'].includes(z.st);
 const SIMS=z=>[...Object.values(z.agents),z.oursim].filter(v=>v!=null);
 const TOP=z=>{const v=SIMS(z);return z.cons!=null&&v.length>=4&&z.cons>=60&&Math.min(...v)>=50&&Math.max(...v)-Math.min(...v)<=25};
 const VIEWS=[['all','All lines'],['top','▲ Highest hit %, sims agree'],['ms','★ Master filter'],...ag.map(k=>[k,MN[k]+' picks']),['ours','Our sim picks']];
 const gapOf=(z,v)=>v==='top'?z.cons:v==='ours'?z.oursim-z.be:ag.includes(v)?(z.agents[v]==null?-99:z.agents[v]-z.be):z.edge;
 const pass=(z,v)=>v==='all'?true:v==='top'?TOP(z):v==='ms'?MS(z):v==='ours'?z.oursim>=z.be+5:(z.agents[v]!=null&&z.agents[v]>=z.be+5);
 let V='ms';
 const draw=()=>{const L=V8SIM.lines.filter(z=>pass(z,V)).sort((x,y)=>gapOf(y,V)-gapOf(x,V));
  let h=`<div class="bfrow" style="margin:0 0 10px"><span class="lbl" style="color:var(--acc)">View</span>${VIEWS.map(([k,n])=>`<button class="btn sm ${k===V?'on':''}" data-sv="${k}" type="button">${n} (${V8SIM.lines.filter(z=>pass(z,k)).length})</button>`).join('')}</div>`;
  h+=`<p class="note" style="max-width:860px">${V==='top'?`<b style="color:var(--acc)">Highest hit %, sims agree:</b> lines where the consensus is 60%+ and every sim (all four agents and ours) has it at 50%+ with no more than 25 points between the highest and lowest, so no wild 80-versus-30 splits. Sorted by consensus hit %. A high hit % is not the same as value: most of these are priced at -150, so the price already expects them to hit about 62% of the time.`:V==='ms'?`<b style="color:var(--acc)">Master filter:</b> at least 3 of the 4 agents above break-even, the consensus above break-even, and only points, assists or threes. Rebounds and PRA are left out because they have been our weakest groups.`:V==='all'?'Every line simmed tonight, best consensus gap first.':V==='ours'?'Lines where our own sim is 5+ points above break-even.':`Lines where ${MN[V]}'s sim is 5+ points above break-even, sorted by ${MN[V]}'s gap.`} <b>What the record says so far:</b> our own sim has not found an edge yet. On Nov 18 and 19, 308 graded sim lines went 164-144 (53%) against an average break-even of 57%, and lines the sim liked most (10+ above break-even) went 14-16. Threes where the sim was above break-even went 18-12, the only group above break-even. Hot last-5 streaks went 36-40, so a hot streak alone is already in the price. The agents' sims start tonight and get graded tomorrow. Treat this page as a test, not a pick list.</p>`;
  h+=L.length?`<div class="scroll"><table class="rtab"><thead><tr><th>#</th><th>Line</th><th>Odds</th><th>Break-even</th>${ag.map(k=>`<th>${MN[k]}</th>`).join('')}<th>Our sim</th><th>Consensus</th><th>Gap</th><th>Agents above</th><th>Game</th></tr></thead><tbody>${L.map((z,i)=>`<tr><td class="mono">${i+1}</td><td>${nm(z)}<br><small>avg ${z.avg} · hit ${z.hs}/${z.n} games</small></td><td class="mono">${z.odds}</td><td class="mono">${z.be}%</td>${ag.map(k=>`<td class="mono">${c(z.agents[k],z.be)}</td>`).join('')}<td class="mono">${c(z.oursim,z.be)}</td><td class="mono"><b>${z.cons??'-'}%</b></td><td class="mono" style="color:${z.edge>0?'var(--acc)':'var(--warn)'}">${z.edge>0?'+':''}${z.edge}</td><td class="mono">${z.nagree} of ${ag.length}</td><td class="lbl">${z.g} ${z.t}</td></tr>`).join('')}</tbody></table></div>`:'<p class="note">No lines pass this view tonight. Passing is a win.</p>';
  el.innerHTML=h};
 el.addEventListener('click',e=>{const b=e.target.closest('button[data-sv]');if(!b)return;V=b.dataset.sv;draw()});draw()})();'''
s=s[:a]+js+s[b:];open(F,'w').write(s);print('sim filters applied')
