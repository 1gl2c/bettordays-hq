// "Talk to us" messages. Saved in the database (only HQ admins can read them) and emailed to the boss.
import { SB_URL, SB_PUB, getUser, emailBoss } from '../lib/server.js';

const MAX = 1500;
const clean = (v, n) => String(v ?? '').replace(/[\u0000-\u0008\u000B-\u001F]/g, '').trim().slice(0, n);
async function readBody(req) {
  if (req.body && typeof req.body === 'object') return req.body;
  const chunks = []; for await (const c of req) chunks.push(c);
  try { return JSON.parse(Buffer.concat(chunks).toString('utf8') || '{}'); } catch { return {}; }
}

export default async function handler(req, res) {
  res.setHeader('Cache-Control', 'no-store');
  if (req.method !== 'POST') { res.setHeader('Allow', 'POST'); return res.status(405).json({ ok: false }); }
  const b = await readBody(req);
  if (b.website) return res.status(200).json({ ok: true }); // honeypot
  const msg = clean(b.msg, MAX);
  if (msg.length < 2) return res.status(400).json({ ok: false, error: 'Message is empty' });
  const user = await getUser(req);
  const row = { name: clean(b.name, 60) || 'Anonymous', kind: ['idea', 'pick', 'feature', 'other'].includes(b.kind) ? b.kind : 'other', msg, page: clean(b.page, 120) || null, user_id: user ? user.id : null };
  const r = await fetch(SB_URL + '/rest/v1/feedback', { method: 'POST', headers: { apikey: SB_PUB, Authorization: 'Bearer ' + (user ? user.token : SB_PUB), 'Content-Type': 'application/json', Prefer: 'return=minimal' }, body: JSON.stringify(row) });
  if (!r.ok) { const e = await r.json().catch(() => ({})); return res.status(429).json({ ok: false, error: e.message || 'Could not send right now.' }); }
  await emailBoss(`💬 New message from ${row.name}`, `${row.name} (${row.kind}) wrote:\n\n${msg}\n\nInbox: https://bettordays.xyz/app#/inbox`);
  return res.status(200).json({ ok: true });
}
