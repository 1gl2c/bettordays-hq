// Ring the bell: a member sends an order to HQ. Saved in the database; emailed to the boss when email is set up.
import { getUser, asUser, json } from '../lib/server.js';
const KINDS = { picks: "Ready for today's picks", update: 'Wants an update', recap: 'Wants the recap' };

export default async function handler(req, res) {
  if (req.method !== 'POST') return json(res, 405, { error: 'POST only' });
  const user = await getUser(req);
  if (!user) return json(res, 401, { error: 'Sign in to ring the bell.' });
  const db = asUser(user);
  const kind = KINDS[req.body && req.body.kind] ? req.body.kind : 'picks';
  const note = String((req.body && req.body.note) || '').slice(0, 200);
  const r = await db('pings', { method: 'POST', headers: { Prefer: 'return=minimal' }, body: JSON.stringify({ user_id: user.id, kind, note: note || null }) });
  if (!r.ok) { const e = await r.json().catch(() => ({})); return json(res, 429, { error: e.message || 'Could not ring the bell.' }); }
  if (process.env.RESEND_API_KEY && process.env.BOSS_EMAIL) {
    const p = await (await db(`profiles?id=eq.${user.id}&select=username`)).json();
    const who = p[0] ? '@' + p[0].username : 'A member';
    await fetch('https://api.resend.com/emails', {
      method: 'POST', headers: { Authorization: 'Bearer ' + process.env.RESEND_API_KEY, 'Content-Type': 'application/json' },
      body: JSON.stringify({ from: process.env.RESEND_FROM || 'BettorDays HQ <onboarding@resend.dev>', to: [process.env.BOSS_EMAIL], subject: `🛎️ Order up: ${who} ${KINDS[kind].toLowerCase()}`, text: `${who} rang the bell at HQ.\n\n${KINDS[kind]}${note ? '\nNote: ' + note : ''}\n\nOrders: https://bettordays.xyz/app#/orders` })
    }).catch(() => {});
  }
  return json(res, 200, { ok: true });
}
