// Pulls the signed-in member's Kalshi positions and settlements into their BettorDays tickets.
import { getUser, asUser, decrypt, kalshiClient, json } from '../lib/server.js';

function legsFrom(m, ticker) {
  if (!m) return [{ text: ticker }];
  const sub = (m.yes_sub_title || '').trim();
  const parts = sub.split(/,(?![^()]*\))/).map(s => s.replace(/^(yes|no)\s+/i, '').trim()).filter(Boolean);
  if (parts.length > 1) return parts.slice(0, 25).map(t => ({ text: t.slice(0, 80) }));
  return [{ text: (m.title + (sub ? ': ' + sub : '')).slice(0, 80) }];
}

export default async function handler(req, res) {
  if (req.method !== 'POST') return json(res, 405, { error: 'POST only' });
  const user = await getUser(req);
  if (!user) return json(res, 401, { error: 'Sign in again.' });
  const db = asUser(user);
  try {
    const k = await (await db('rpc/my_kalshi_key', { method: 'POST', body: '{}' })).json();
    if (!Array.isArray(k) || !k[0]) return json(res, 400, { error: 'Connect your Kalshi key first.' });
    const ks = kalshiClient(k[0].key_id, decrypt(k[0].enc));
    const st = await (await db(`settings?id=eq.${user.id}&select=default_visibility`)).json();
    const vis = (st[0] && st[0].default_visibility) || 'public';
    const [positions, settlements] = await Promise.all([
      ks.all('/portfolio/positions', 'market_positions', '&count_filter=position'),
      ks.all('/portfolio/settlements', 'settlements')
    ]);
    const rows = [];
    for (const p of positions) {
      if (!p.position) continue;
      const m = await ks.market(p.ticker);
      const stake = Math.round(Number(p.total_traded || p.market_exposure || 0)) / 100;
      const payout = Math.abs(p.position);
      rows.push({ user_id: user.id, external_id: p.ticker, source: 'kalshi', status: 'open', title: (m && m.title || p.ticker).slice(0, 80), legs: legsFrom(m, p.ticker), stake: stake || null, payout, multiplier: stake ? Math.round(payout / stake * 100) / 100 : null, tail_url: m && m.event_ticker ? `https://kalshi.com/markets/${m.event_ticker.toLowerCase()}` : null, visibility: vis });
    }
    for (const s of settlements.slice(0, 100)) {
      const m = await ks.market(s.ticker);
      const cost = (Number(s.yes_total_cost || 0) + Number(s.no_total_cost || 0)) / 100;
      const revenue = Number(s.revenue || 0) / 100;
      rows.push({ user_id: user.id, external_id: s.ticker, source: 'kalshi', status: revenue > 0 ? 'won' : 'lost', title: (m && m.title || s.ticker).slice(0, 80), legs: legsFrom(m, s.ticker), stake: cost || null, payout: revenue || null, multiplier: cost && revenue ? Math.round(revenue / cost * 100) / 100 : null, tail_url: null, visibility: vis });
    }
    const seen = new Set(); const uniq = rows.filter(r => !seen.has(r.external_id) && seen.add(r.external_id));
    const before = await (await db(`picks?user_id=eq.${user.id}&source=eq.kalshi&select=external_id`)).json();
    const had = new Set((before || []).map(x => x.external_id));
    if (uniq.length) {
      const up = await db('picks?on_conflict=user_id,external_id', { method: 'POST', headers: { Prefer: 'resolution=merge-duplicates,return=minimal' }, body: JSON.stringify(uniq) });
      if (!up.ok) throw new Error('Save failed ' + up.status);
    }
    await db(`kalshi_keys?user_id=eq.${user.id}`, { method: 'PATCH', body: JSON.stringify({ last_sync: new Date().toISOString() }) });
    const added = uniq.filter(r => !had.has(r.external_id)).length;
    return json(res, 200, { added, updated: uniq.length - added });
  } catch (e) {
    return json(res, 502, { error: String(e.message || e) });
  }
}
