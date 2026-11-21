"""Picks page: MASTER FILTER (Ace, Nov 20). One tap shows only legs in the groups our record says to lean on:
  graded 70+, Kalshi at or above our grade (GREEN: 124-17, 88% through Nov 19), and a best group:
  NBA points overs, NBA assists (overs and unders), NBA threes, NBA favorite moneylines, NFL receptions.
  Left out on purpose: rebounds (middle of the pack), PRA, NFL yardage, touchdowns, college lines, spreads, totals, flagged legs."""
F='bettordays-hq.html';s=open(F).read()
def rep(a,b,n=1):
  global s;c=s.count(a);assert c==n,(c,a[:90]);s=s.replace(a,b)
if 'Master filter' not in s:
  rep("const drawF=()=>{fe.innerHTML='<div class=\"bfil\" style=\"margin:0\">'+grp('gr','Grade',[['all','All'],['80','80+'],['70','70-79'],['60','60-69'],['0','Under 60']])+grp('ty','Bet type',[['all','All'],['prop','Props'],['ml','Moneylines'],['spread','Spreads'],['total','Totals']].filter(([k])=>k==='all'||CUR.some(x=>x.ty===k)))",
      "const MS=x=>{const st=statOf(x),u=/\\bunder\\b/i.test(x.p);return x.pct>=70&&x.k!=null&&x.k>=x.pct&&!x.fl&&((x.sp==='NBA'&&((st==='pts'&&!u)||st==='ast'||(st==='3pm'&&!u)||(x.ty==='ml'&&x.k>=50)))||(x.sp==='NFL'&&/reception/i.test(x.p)&&!u))};\n const drawF=()=>{fe.innerHTML='<div class=\"bfil\" style=\"margin:0\">'+`<div class=\"bfrow\"><span class=\"lbl\" style=\"color:var(--acc)\">Master filter</span><button class=\"btn sm ${G.ms!=='on'?'on':''}\" data-g=\"ms\" data-v=\"all\" type=\"button\">Off</button><button class=\"btn sm ${G.ms==='on'?'on':''}\" data-g=\"ms\" data-v=\"on\" type=\"button\" title=\"70+, Kalshi at or above our grade, and only our best groups\">★ Master filter (${CUR.filter(MS).length})</button></div>`+grp('gr','Grade',[['all','All'],['80','80+'],['70','70-79'],['60','60-69'],['0','Under 60']])+grp('ty','Bet type',[['all','All'],['prop','Props'],['ml','Moneylines'],['spread','Spreads'],['total','Totals']].filter(([k])=>k==='all'||CUR.some(x=>x.ty===k)))")
  i=s.index("const MS=x=>");a="const ok=x=>BF.pass(x)&&(G.gr==='all'||";j=s.index(a,i);assert j-i<3000
  s=s[:j]+"const ok=x=>BF.pass(x)&&(G.ms!=='on'||MS(x))&&(G.gr==='all'||"+s[j+len(a):]
  rep("{const N0=document.getElementById('thuN');if(N0)N0.textContent=`Showing ${r.length} of ${CUR.length} picks. Filters stack, so 80+ and NBA and Kalshi within 7 shows only legs that pass all three.`}",
      "{const N0=document.getElementById('thuN');if(N0)N0.innerHTML=G.ms==='on'?`<b style=\"color:var(--acc)\">Master filter on:</b> ${r.length} legs graded 70+ with Kalshi at or above our grade (that group went 124-17, 88%, Nov 4 to 19), only from our best groups: NBA points, assists and threes, NBA favorite moneylines, NFL receptions. Rebounds, PRA, NFL yardage, touchdowns, college lines, spreads and totals are left out. Legs still lose sometimes, and legs from the same game win and lose together.`:`Showing ${r.length} of ${CUR.length} picks. Filters stack, so 80+ and NBA and Kalshi within 7 shows only legs that pass all three.`}")
  open(F,'w').write(s);print('master filter added')
else: print('already there')
