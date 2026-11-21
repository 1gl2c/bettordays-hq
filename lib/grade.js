// Parlay grader engine: read a slip, then grade every leg with ten signals.
// Signals: 1 our board grade · 2 Kalshi price · 3-6 four AI agents graded blind · 7 last-10 hit rate
//          8 season hit rate · 9 our record for that stat group · 10 flags (injury, unders rule, weak group)
const OR = 'https://openrouter.ai/api/v1/chat/completions';
const KALSHI = 'https://api.elections.kalshi.com/trade-api/v2';
export const AGENTS = (process.env.GRADER_MODELS || 'openai/gpt-6.2-astra-pro,anthropic/claude-fable-5.2,google/gemini-4-neon,x-ai/grok-4.7').split(',').map(s => s.trim()).filter(Boolean);
const READER = process.env.GRADER_READER || 'anthropic/claude-sonnet-5.5';
const NAMES = { openai: 'ChatGPT', anthropic: 'Claude', google: 'Gemini', 'x-ai': 'Grok' };
export const agentName = m => NAMES[m.split('/')[0]] || m;

async function ask(model, messages, maxTokens = 1800, timeoutMs = 40000) {
  const ctl = new AbortController(); const t = setTimeout(() => ctl.abort(), timeoutMs);
  try {
    const r = await fetch(OR, {
      method: 'POST', signal: ctl.signal,
      headers: { Authorization: 'Bearer ' + process.env.OPENROUTER_API_KEY, 'Content-Type': 'application/json', 'HTTP-Referer': 'https://bettordays.xyz', 'X-Title': 'BettorDays Parlay Grader' },
      body: JSON.stringify({ model, messages, max_tokens: maxTokens, temperature: 0.2 })
    });
    if (!r.ok) throw new Error(`${model} ${r.status}`);
    const j = await r.json(); return j.choices?.[0]?.message?.content || '';
  } finally { clearTimeout(t); }
}
const firstJson = s => { const m = String(s).match(/\{[\s\S]*\}|\[[\s\S]*\]/); if (!m) return null; try { return JSON.parse(m[0]); } catch { return null; } };

// ---------- 1. read the slip
export async function readSlip({ image, text }) {
  const instr = `Read this sports betting slip. Return only JSON: {"book":"","stake":null,"payout":null,"legs":[{"player":"","team":"","market":"points|rebounds|assists|threes|pra|moneyline|spread|total|passing yards|rushing yards|receiving yards|receptions|touchdown|other","side":"over|under|yes","line":null,"game":"","sport":"NBA|NFL|NCAAB|NCAAF|NHL|MLB|other","text":"leg exactly as written"}]}.
"20+ points" means market points, side over, line 20 (so 19.5 over). For a moneyline put the team in "player". Use null when a number is not shown. Do not invent legs.`;
  const content = image ? [{ type: 'text', text: instr }, { type: 'image_url', image_url: { url: image } }] : instr + '\n\nSlip:\n' + String(text).slice(0, 4000);
  const out = firstJson(await ask(READER, [{ role: 'user', content }], 2500, 45000));
  if (!out || !Array.isArray(out.legs) || !out.legs.length) throw new Error('Could not read any legs from that slip. Try a clearer screenshot or paste the legs as text.');
  out.legs = out.legs.slice(0, 25);
  return out;
}

// ---------- helpers
const nrm = s => String(s || '').normalize('NFKD').replace(/[̀-ͯ]/g, '').toLowerCase().replace(/[.'’]/g, '').trim();
const STAT = { points: 'pts', rebounds: 'reb', assists: 'ast', threes: '3pm', pra: 'pra', moneyline: 'ml', spread: 'spread', total: 'total', 'passing yards': 'pass', 'rushing yards': 'rush', 'receiving yards': 'recyds', receptions: 'rec', touchdown: 'atd' };
const SER = { pts: 'KXNBAPTS', reb: 'KXNBAREB', ast: 'KXNBAAST', '3pm': 'KXNBA3PT', pra: 'KXNBAPRA' };
const ESPNK = { pts: 'points', reb: 'totalRebounds', ast: 'assists', '3pm': 'threePointFieldGoalsMade-threePointFieldGoalsAttempted' };
const thr = l => l.line == null ? null : (Number.isInteger(+l.line) && l.side !== 'under' ? +l.line : Math.floor(+l.line) + (l.side === 'under' ? 0 : 1));

function matchBoard(leg, board) {
  const p = nrm(leg.player), last = p.split(' ').slice(-1)[0], st = STAT[leg.market] || 'other', k = thr(leg);
  return board.find(b => { const t = nrm(b.text); if (!t.includes(last) || (p.split(' ')[0] && !t.includes(p.split(' ')[0]))) return false;
    if (st === 'ml') return /\bml\b/.test(t);
    const w = { pts: 'point', reb: 'rebound', ast: 'assist', '3pm': 'three', pra: 'rebounds + assists' }[st]; if (w && !t.includes(w)) return false;
    if (st === 'pts' && t.includes('rebounds +')) return false;
    const n = (t.match(/(\d+)\+/) || [])[1]; return k == null || (n && +n === k); });
}
const SERIES_CACHE = new Map();
function seriesMarkets(s) { if (!SERIES_CACHE.has(s)) SERIES_CACHE.set(s, fetch(`${KALSHI}/markets?series_ticker=${s}&status=open&limit=1000`).then(r => r.ok ? r.json() : { markets: [] }).then(j => j.markets || []).catch(() => [])); return SERIES_CACHE.get(s); }
async function kalshiPrice(leg, dateCode) {
  const st = STAT[leg.market]; const s = SER[st]; const k = thr(leg); if (!s || k == null) return null;
  try {
    const ms = await seriesMarkets(s); const p = nrm(leg.player);
    const m = ms.find(x => (!dateCode || x.event_ticker.includes(dateCode)) && nrm(x.title).startsWith(p + ':') && new RegExp(`: ${k}\\+`).test(x.title));
    if (!m) return null; const a = +m.yes_ask_dollars || 0, b = +m.yes_bid_dollars || 0; const mid = a && b ? (a + b) / 2 : a || b; if (!mid) return null;
    const ladder = ms.filter(x => x.event_ticker === m.event_ticker && nrm(x.title).startsWith(p + ':')).map(x => { const n = +(x.title.match(/: (\d+)\+/) || [])[1]; const aa = +x.yes_ask_dollars || 0, bb = +x.yes_bid_dollars || 0; return { k: n, p: Math.round(100 * (aa && bb ? (aa + bb) / 2 : aa || bb)) }; }).filter(x => x.k && x.p).sort((x, y) => x.k - y.k);
    const yes = Math.round(100 * mid); return { k: leg.side === 'under' ? 100 - yes : yes, ladder };
  } catch { return null; }
}

// NBA team names -> Kalshi's game-market label (city, with L/C for the two LA teams)
const TEAMK = {hawks:'Atlanta',celtics:'Boston',nets:'Brooklyn',hornets:'Charlotte',bulls:'Chicago',cavaliers:'Cleveland',cavs:'Cleveland',mavericks:'Dallas',mavs:'Dallas',nuggets:'Denver',pistons:'Detroit',warriors:'Golden State',rockets:'Houston',pacers:'Indiana',clippers:'Los Angeles C',lakers:'Los Angeles L',grizzlies:'Memphis',heat:'Miami',bucks:'Milwaukee',timberwolves:'Minnesota',wolves:'Minnesota',pelicans:'New Orleans',knicks:'New York',thunder:'Oklahoma City',magic:'Orlando','76ers':'Philadelphia',sixers:'Philadelphia',suns:'Phoenix','trail blazers':'Portland',blazers:'Portland',kings:'Sacramento',spurs:'San Antonio',raptors:'Toronto',jazz:'Utah',wizards:'Washington'};
async function kalshiML(leg, dateCode) {
  const t = nrm(leg.player); const key = Object.keys(TEAMK).find(k => t.includes(k)); if (!key) return null;
  const ms = await seriesMarkets('KXNBAGAME');
  const m = ms.find(x => (!dateCode || x.event_ticker.includes(dateCode)) && x.yes_sub_title === TEAMK[key]); if (!m) return null;
  const a = +m.yes_ask_dollars || 0, b = +m.yes_bid_dollars || 0; const mid = a && b ? (a + b) / 2 : a || b; return mid ? { k: Math.round(100 * mid), ladder: [] } : null;
}
async function espnForm(leg) {
  const st = STAT[leg.market]; const key = ESPNK[st] || (st === 'pra' ? 'pra' : null); const k = thr(leg);
  if (!key || k == null || !leg.player) return null;
  try {
    const s = await (await fetch('https://site.web.api.espn.com/apis/common/v3/search?limit=5&type=player&query=' + encodeURIComponent(leg.player))).json();
    const it = (s.items || []).find(i => i.league === 'nba'); if (!it) return null;
    const [g, a] = await Promise.all([fetch(`https://site.web.api.espn.com/apis/common/v3/sports/basketball/nba/athletes/${it.id}/gamelog`).then(r => r.json()), fetch(`https://site.web.api.espn.com/apis/common/v3/sports/basketball/nba/athletes/${it.id}`).then(r => r.json())]);
    const names = g.names || []; const ev = g.events || {}; const rows = [];
    for (const c of (g.seasonTypes || [])[0]?.categories || []) for (const e of c.events || []) { const o = { date: ev[e.eventId]?.gameDate || '' }; names.forEach((n, i) => { o[n] = e.stats[i]; }); rows.push(o); }
    rows.sort((x, y) => y.date.localeCompare(x.date));
    const num = (r, n) => parseFloat(String(r[n] || '0').split('-')[0]) || 0;
    const val = r => key === 'pra' ? num(r, 'points') + num(r, 'totalRebounds') + num(r, 'assists') : num(r, key);
    const vs = rows.map(val); if (!vs.length) return null;
    const hit = v => leg.side === 'under' ? v < k : v >= k;
    const l10 = vs.slice(0, 10); const inj = (a.athlete?.injuries || [])[0];
    return { n: vs.length, season: Math.round(100 * vs.filter(hit).length / vs.length), l10n: l10.length, l10: l10.filter(hit).length, avg: +(vs.reduce((x, y) => x + y, 0) / vs.length).toFixed(1),
             inj: inj ? `${inj.status}${inj.shortComment ? ': ' + inj.shortComment.slice(0, 120) : ''}` : null, team: a.athlete?.team?.abbreviation || null };
  } catch { return null; }
}
function groupRecord(leg, record) {
  const sp = { NCAAB: 'CBB', NCAAF: 'CFB' }[leg.sport] || leg.sport; const st = STAT[leg.market] || 'other'; const dir = leg.side === 'under' ? 'u' : 'o';
  const L = record.filter(l => l.sp === sp && l.st === st && l.dir === dir && (l.res === 'W' || l.res === 'L'));
  if (L.length < 10) return null; const w = L.filter(l => l.res === 'W').length;
  return { w, l: L.length - w, pct: Math.round(100 * w / L.length), label: `${sp} ${leg.market}${dir === 'u' ? ' unders' : ''}` };
}

// ---------- 3. AI panel, blind (no price shown)
async function panel(legs, facts) {
  const list = legs.map((l, i) => `${i + 1}. ${l.text || `${l.player} ${l.side} ${l.line} ${l.market}`} (${l.game || l.sport || ''})` + (facts[i]?.form ? ` | season hit ${facts[i].form.season}% in ${facts[i].form.n} games, last 10: ${facts[i].form.l10}/${facts[i].form.l10n}, avg ${facts[i].form.avg}` : '') + (facts[i]?.form?.inj ? ` | injury: ${facts[i].form.inj}` : '')).join('\n');
  const prompt = `You are a sharp sports betting analyst. Today is ${new Date().toLocaleDateString('en-US', { timeZone: 'America/Los_Angeles', dateStyle: 'full' })}. Give an honest probability (1 to 99) that each leg hits tonight, using what you know about the player's role, minutes, matchup, injuries and recent form. No market prices are shown on purpose. Be calibrated: 70 means 7 in 10.
${list}
Return only JSON: {"legs":[{"n":1,"prob":70,"why":"one short reason"}]}`;
  const outs = await Promise.allSettled(AGENTS.map(m => ask(m, [{ role: 'user', content: prompt }], 1500, 40000).then(t => ({ m, j: firstJson(t) }))));
  const res = {};
  outs.forEach(o => { if (o.status === 'fulfilled' && o.value.j?.legs) res[o.value.m] = Object.fromEntries(o.value.j.legs.filter(x => x && x.n).map(x => [x.n, { p: Math.max(1, Math.min(99, Math.round(+x.prob) || 0)), why: String(x.why || '').slice(0, 140) }])); });
  return res;
}

const median = a => { const s = [...a].sort((x, y) => x - y); const n = s.length; return n ? (n % 2 ? s[(n - 1) / 2] : (s[n / 2 - 1] + s[n / 2]) / 2) : null; };
const WEAK = new Set(['pra', 'recyds', 'atd', 'spread']);

// ---------- 2 + 4. enrich and combine
export async function gradeSlip(slip, { board, record, dateCode }) {
  const legs = slip.legs;
  SERIES_CACHE.clear(); // fresh Kalshi prices for every slip
  const facts = await Promise.all(legs.map(async l => ({ board: matchBoard(l, board), kalshi: l.market === 'moneyline' && (l.sport || 'NBA') === 'NBA' ? await kalshiML(l, dateCode) : await kalshiPrice(l, dateCode), form: await espnForm(l), group: groupRecord(l, record) })));
  const ai = await panel(legs, facts);
  const out = legs.map((l, i) => {
    const f = facts[i]; const n = i + 1; const agents = Object.fromEntries(Object.entries(ai).map(([m, r]) => [agentName(m), r[n] || null]));
    const k = f.kalshi?.k ?? (f.board?.k ?? null); const ours = f.board?.pct ?? null;
    const aiNums = Object.values(agents).filter(Boolean).map(a => a.p);
    const formP = f.form ? Math.round(0.6 * (100 * f.form.l10 / Math.max(1, f.form.l10n)) + 0.4 * f.form.season) : null;
    const voices = [...aiNums, ...(ours != null ? [ours] : []), ...(formP != null ? [formP] : [])];
    let grade = voices.length ? Math.round(median(voices)) : (k ?? null);
    const flags = [];
    let tier = 'N';
    if (k != null && grade != null) { const gap = grade - k; tier = gap >= 8 ? 'R' : gap > 0 ? 'Y' : 'G'; if (tier === 'R') flags.push(`We are ${gap} above Kalshi. That gap has lost most often in our record.`); }
    if (f.form?.inj) flags.push('Injury report: ' + f.form.inj);
    const st = STAT[l.market] || 'other'; if (WEAK.has(st)) flags.push(`${l.market} has been one of our weakest groups.`);
    if (l.side === 'under' && /doncic|luka|wembanyama/i.test(l.player || '')) flags.push('Unders on Luka or Wemby: our house rule says no.');
    if (/harden/i.test(l.player || '')) flags.push('James Harden leg: our house rule says no.');
    // safer rung on the same player (same side), from the Kalshi ladder
    let swap = null; const lad = f.kalshi?.ladder || []; const kk = thr(l);
    if (l.side !== 'under' && lad.length && kk != null) { const lower = lad.filter(x => x.k < kk && x.p >= 75); const best = lower.sort((a, b) => Math.abs(a.p - 82) - Math.abs(b.p - 82))[0]; if (best) swap = { line: `${best.k}+`, k: best.p }; }
    const signals = (ours != null) + (k != null) + aiNums.length + (f.form ? 2 : 0) + (f.group ? 1 : 0) + 1; // 10 max
    return { n, text: l.text || `${l.player} ${l.line ?? ''} ${l.market}`, game: l.game || '', grade, tier, kalshi: k, ours, agents, form: f.form, group: f.group, flags, swap, signals: Math.min(10, signals) };
  });
  const probs = out.map(o => (o.grade ?? 50) / 100); const hit = probs.reduce((a, b) => a * b, 1);
  const mkt = out.every(o => o.kalshi != null) ? out.reduce((a, o) => a * o.kalshi / 100, 1) : null;
  const pay = slip.stake && slip.payout ? slip.payout / slip.stake : null;
  const weakest = [...out].sort((a, b) => (a.grade ?? 0) - (b.grade ?? 0))[0];
  const score = Math.round(Math.max(1, Math.min(10, 10 * Math.pow(hit, 1 / Math.max(1, out.length)) - out.filter(o => o.tier === 'R').length - out.filter(o => o.flags.length > 1).length * 0.5)));
  return { book: slip.book || '', stake: slip.stake ?? null, payout: slip.payout ?? null, legs: out,
    ticket: { hit: +(100 * hit).toFixed(1), fair: +(1 / Math.max(hit, 1e-6)).toFixed(2), pays: pay ? +pay.toFixed(2) : null, market_hit: mkt ? +(100 * mkt).toFixed(1) : null,
      value: pay ? (pay * hit >= 1 ? 'Pays more than our grades say it should.' : 'Pays less than our grades say it should.') : null,
      weakest: weakest ? { n: weakest.n, text: weakest.text, grade: weakest.grade, swap: weakest.swap } : null, score },
    agents: Object.keys(ai).map(agentName) };
}
