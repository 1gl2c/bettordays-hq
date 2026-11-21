// Parlay grader: POST { image: "data:image/...;base64,...", text } with the member's token.
// Reads the slip, grades every leg with ten signals and four AI agents, saves it, and returns the breakdown.
import { getUser, asUser, json } from '../lib/server.js';
import { readSlip, gradeSlip } from '../lib/grade.js';
export const config = { maxDuration: 120, api: { bodyParser: { sizeLimit: '6mb' } } };
const DAILY = +(process.env.GRADER_DAILY_LIMIT || 10);

export default async function handler(req, res) {
  res.setHeader('Cache-Control', 'no-store');
  if (req.method !== 'POST') return json(res, 405, { error: 'POST only' });
  if (!process.env.OPENROUTER_API_KEY) return json(res, 503, { error: 'The grader is being set up. Try again soon.' });
  const user = await getUser(req);
  if (!user) return json(res, 401, { error: 'Sign in (free) to grade a slip.' });
  const db = asUser(user);
  const since = new Date(Date.now() - 24 * 3600e3).toISOString();
  const cr = await db(`slip_grades?select=id&user_id=eq.${user.id}&created_at=gte.${since}`, { headers: { Prefer: 'count=exact', Range: '0-0' } });
  const used = +((cr.headers.get('content-range') || '').split('/')[1] || 0);
  if (used >= DAILY) return json(res, 429, { error: `You've used today's ${DAILY} free grades. Back tomorrow.` });
  const b = req.body || {};
  const image = typeof b.image === 'string' && /^data:image\/(png|jpe?g|webp);base64,/.test(b.image) ? b.image : null;
  const text = !image && typeof b.text === 'string' ? b.text.trim().slice(0, 4000) : '';
  if (!image && text.length < 4) return json(res, 400, { error: 'Add a screenshot or paste your legs.' });
  try {
    const host = 'https://' + (req.headers.host || 'bettordays.xyz');
    const [board, rec] = await Promise.all([fetch(host + '/board.json').then(r => r.json()).catch(() => []), fetch(host + '/record.json').then(r => r.json()).catch(() => ({ legs: [] }))]);
    const now = new Date(new Date().toLocaleString('en-US', { timeZone: 'America/Los_Angeles' }));
    const dateCode = String(now.getFullYear()).slice(2) + ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC'][now.getMonth()] + String(now.getDate()).padStart(2, '0');
    const slip = await readSlip({ image, text });
    const out = await gradeSlip(slip, { board, record: rec.legs || [], dateCode });
    await db('slip_grades', { method: 'POST', headers: { Prefer: 'return=minimal' }, body: JSON.stringify({ user_id: user.id, legs: out.legs, ticket: out.ticket, models: out.agents }) });
    return json(res, 200, { ok: true, ...out, left: Math.max(0, DAILY - used - 1) });
  } catch (e) {
    console.error('grade-slip', e);
    return json(res, 422, { error: e.message && e.message.length < 200 ? e.message : 'Could not grade that slip. Try again.' });
  }
}
