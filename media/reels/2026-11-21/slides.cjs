const {chromium}=require('playwright');
const css=`body{margin:0;width:1080px;height:1920px;background:radial-gradient(1200px 900px at 80% 0%,#0f3a2a 0%,#0d0f0e 55%);color:#f2f4f3;font-family:Inter;overflow:hidden;position:relative}
.w{position:absolute;inset:0;padding:150px 80px;display:flex;flex-direction:column;justify-content:center}
.k{font:500 30px 'JetBrains Mono';color:#04ff9f;letter-spacing:5px}
h1{font:118px/0.95 'Archivo Black';margin:26px 0;letter-spacing:-2px}h1 em{font-style:normal;color:#04ff9f}
.big{font:300px/1 'Archivo Black';color:#04ff9f;letter-spacing:-8px;margin:10px 0}
.s{font-size:44px;line-height:1.35;color:#c9cfcc}.s b{color:#fff}
.m{font:500 34px 'JetBrains Mono';color:#8b9490;margin-top:30px}
.ft{position:absolute;left:80px;right:80px;bottom:90px;font:500 26px 'JetBrains Mono';color:#6f7874;display:flex;justify-content:space-between}
.grid{position:absolute;inset:0;background-image:linear-gradient(#ffffff08 1px,transparent 1px),linear-gradient(90deg,#ffffff08 1px,transparent 1px);background-size:90px 90px}
li{margin:18px 0}ul{padding-left:40px}`;
const S=[
`<div class=k>LAST GAME TONIGHT</div><h1>CELTICS<br>AT <em>KINGS</em></h1><div class=s>7:00 PM PT. Two legs on our board.</div>`,
`<div class=k>LEG 1 · MONEYLINE</div><h1>Celtics<br>to win</h1><div class=big>84</div><div class=s>Our grade. Kalshi has it at <b>86</b>.</div><div class=m>Kings 1-14 · 0-9 at home · back-to-back</div>`,
`<div class=k>LEG 2 · PLAYER PROP</div><h1>Domantas Sabonis<br><em>4+ assists</em></h1><div class=big>72</div><div class=s>Over 3.5 assists. Kalshi <b>71</b>, sportsbooks near <b>74</b>.</div><div class=m>8 assists in 2 of his last 3</div>`,
`<div class=k>HOW WE GRADE</div><h1>4 AIs.<br>Blind.</h1><ul class=s><li>Every leg graded with <b>no price shown</b></li><li>Our own model joins in</li><li>Kalshi referees after</li><li><b>Every miss gets posted</b></li></ul>`,
`<div class=k>BETTORDAYS</div><h1>Full board<br><em>free.</em></h1><div class=s>bettordays.xyz · link in bio</div><div class=m>21+ · Grades are estimates, not guarantees.<br>Bet small. 1-800-MY-RESET</div>`];
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
for(let i=0;i<S.length;i++){await p.setContent(`<html><head><link href="https://fonts.googleapis.com/css2?family=Archivo+Black&family=Inter:wght@400;600;800&family=JetBrains+Mono:wght@500&display=swap" rel=stylesheet><style>${css}</style></head><body><div class=grid></div><div class=w>${S[i]}</div><div class=ft><span>@BETTORDAYS</span><span>SAT · NOV 21</span></div></body></html>`,{waitUntil:'networkidle'});
await p.screenshot({path:`s${i}.jpg`,type:'jpeg',quality:92});}await b.close()})();
