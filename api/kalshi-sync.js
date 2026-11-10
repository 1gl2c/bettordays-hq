// Pulls the signed-in admin's Kalshi positions and settlements into their BettorDays tickets.
// Needs these Vercel environment variables (set in the Vercel dashboard, never in code):
//   SUPABASE_SERVICE_ROLE_KEY  from Supabase > Project Settings > API keys (secret)
//   KALSHI_API_KEY_ID          from Kalshi > Account > API keys
//   KALSHI_PRIVATE_KEY         the private key file Kalshi gives you (paste the whole PEM)
import crypto from 'node:crypto';

const SB_URL = 'https://ndcsjhetuasijbgpfhwj.supabase.co';
const SB_PUB = 'sb_publishable_thFDxFfsdTESdl_MzPeE3g_pUqcSMRc';
const KALSHI = 'https://api.elections.kalshi.com';
const BASE = '/trade-api/v2';

function kalshiHeaders(method, path) {
  const ts = String(Date.now());
  const key = (process.env.KALSHI_PRIVATE_KEY || '').replace(/\\n/g, '\n');
  const sig = crypto.sign('sha256', Buffer.from(ts + method + path), {
    key, padding: crypto.constants.RSA_PKCS1_PSS_PADDING, saltLength: crypto.constants.RSA_PSS_SALTLEN_DIGEST
  }).toString('base64');
  return { 'KALSHI-ACCESS-KEY': process.env.KALSHI_API_KEY_ID, 'KALSHI-ACCESS-TIMESTAMP': ts, 'KALSHI-ACCESS-SIGNATURE': sig, Accept: 'application/json' };
}
async function kget(path, query = '') {
  const r = await fetch(KALSHI + BASE + path + query, { headers: kalshiHeaders('GET', BASE + path) });
  if (!r.ok) throw new Error(`Kalshi ${path} ${r.status}`);
  return r.json();
}
async function kall(path, field, extra = '') {
  const out = []; let cursor = '';
  for (let i = 0; i < 10; i++) {
    const j = await kget(path, `?limit=200${extra}${cursor ? '&cursor=' + encodeURIComponent(cursor) : ''}`);
    out.push(...(j[field] || []));
    if (!j.cursor) break; cursor = j.cursor;
  }
  return out;
}
const marketCache = {};
async function market(ticker) {
  if (marketCache[ticker]) return marketCache[ticker];
  const r = await fetch(`${KALSHI}${BASE}/markets/${encodeURIComponent(ticker)}`);
  const m = r.ok ? (await r.json()).market : null;
  return (marketCache[ticker] = m);
}
function legsFrom(m, ticker) {
  if (!m) return [{ text: ticker }];
  const sub = (m.yes_sub_title || '').trim();
  const parts = sub.split(/,(?![^()]*\))/).map(s => s.replace(/^(yes|no)\s+/i, '').trim()).filter(Boolean);
  if (parts.length > 1) return parts.slice(0, 25).map(t => ({ text: t.slice(0, 80) }));
  return [{ text: (m.title + (sub ? ': ' + sub : '')).slice(0, 80) }];
}
const sbAdmin = (path, init = {}) => fetch(SB_URL + '/rest/v1/' + path, { ...init, headers: { apikey: process.env.SUPABASE_SERVICE_ROLE_KEY, Authorization: 'Bearer ' + process.env.SUPABASE_SERVICE_ROLE_KEY, 'Content-Type': 'application/json', ...(init.headers || {}) } });

export default async function handler(req, res) {
  if (req.method !== 'POST') return res.status(405).json({ error: 'POST only' });
  const missing = ['SUPABASE_SERVICE_ROLE_KEY', 'KALSHI_API_KEY_ID', 'KALSHI_PRIVATE_KEY'].filter(k => !process.env[k]);
  if (missing.length) return res.status(503).json({ error: 'Not set up yet. Missing in Vercel: ' + missing.join(', ') });

  const token = (req.headers.authorization || '').replace(/^Bearer /, '');
  const u = await fetch(SB_URL + '/auth/v1/user', { headers: { apikey: SB_PUB, Authorization: 'Bearer ' + token } });
  if (!u.ok) return res.status(401).json({ error: 'Sign in again.' });
  const user = await u.json();
  const s = await (await sbAdmin(`settings?id=eq.${user.id}&select=is_admin,default_visibility`)).json();
  if (!s[0] || !s[0].is_admin) return res.status(403).json({ error: 'Kalshi sync is admin-only for now.' });

  try {
    const [positions, settlements] = await Promise.all([
      kall('/portfolio/positions', 'market_positions', '&count_filter=position'),
      kall('/portfolio/settlements', 'settlements')
    ]);
    const rows = [];
    for (const p of positions) {
      if (!p.position) continue;
      const m = await market(p.ticker);
      const stake = Math.round(Number(p.total_traded || p.market_exposure || 0)) / 100;
      const payout = Math.abs(p.position);
      rows.push({ user_id: user.id, external_id: p.ticker, source: 'kalshi', status: 'open', title: (m && m.title || p.ticker).slice(0, 80), legs: legsFrom(m, p.ticker), stake: stake || null, payout, multiplier: stake ? Math.round(payout / stake * 100) / 100 : null, tail_url: m && m.event_ticker ? `https://kalshi.com/markets/${m.event_ticker.toLowerCase()}` : null, visibility: s[0].default_visibility });
    }
    for (const st of settlements.slice(0, 100)) {
      const m = await market(st.ticker);
      const count = Number(st.yes_count || 0) + Number(st.no_count || 0);
      const cost = (Number(st.yes_total_cost || 0) + Number(st.no_total_cost || 0)) / 100;
      const revenue = Number(st.revenue || 0) / 100;
      rows.push({ user_id: user.id, external_id: st.ticker, source: 'kalshi', status: revenue > 0 ? 'won' : 'lost', title: (m && m.title || st.ticker).slice(0, 80), legs: legsFrom(m, st.ticker), stake: cost || null, payout: revenue || count || null, multiplier: cost && revenue ? Math.round(revenue / cost * 100) / 100 : null, tail_url: null, visibility: s[0].default_visibility });
    }
    const seen = new Set(); const uniq = rows.filter(r => !seen.has(r.external_id) && seen.add(r.external_id));
    const before = await (await sbAdmin(`picks?user_id=eq.${user.id}&source=eq.kalshi&select=external_id`)).json();
    const had = new Set(before.map(x => x.external_id));
    if (uniq.length) {
      const up = await sbAdmin('picks?on_conflict=user_id,external_id', { method: 'POST', headers: { Prefer: 'resolution=merge-duplicates,return=minimal' }, body: JSON.stringify(uniq) });
      if (!up.ok) throw new Error('Save failed ' + up.status);
    }
    const added = uniq.filter(r => !had.has(r.external_id)).length;
    return res.status(200).json({ added, updated: uniq.length - added });
  } catch (e) {
    return res.status(502).json({ error: String(e.message || e) });
  }
}
