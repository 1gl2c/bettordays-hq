// HQ admins post an announcement: saved for the in-app banner and emailed to every member who opted in.
import { getUser, asUser, json } from '../lib/server.js';
const esc = s => String(s ?? '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));

export default async function handler(req, res) {
  if (req.method !== 'POST') return json(res, 405, { error: 'POST only' });
  const user = await getUser(req);
  if (!user) return json(res, 401, { error: 'Sign in again.' });
  const db = asUser(user);
  const b = req.body || {};
  let id = b.id;
  if (!id) {
    const title = String(b.title || '').trim().slice(0, 80), body = String(b.body || '').trim().slice(0, 400);
    if (!title) return json(res, 400, { error: 'Add a title.' });
    const r = await db('announcements', { method: 'POST', headers: { Prefer: 'return=representation' }, body: JSON.stringify({ title, body: body || null, link: /^\/[\w#-]*$/.test(b.link || '') ? b.link : '/', created_by: user.id }) });
    if (!r.ok) return json(res, 403, { error: 'Only HQ can post announcements.' });
    id = (await r.json())[0].id;
  }
  const a = (await (await db(`announcements?id=eq.${Number(id)}&select=*`)).json())[0];
  if (!a) return json(res, 404, { error: 'Announcement not found.' });
  if (!b.email) return json(res, 200, { ok: true, id: a.id, emailed: 0 });
  if (!process.env.RESEND_API_KEY) return json(res, 503, { error: 'Email is not set up.' });
  const list = await (await db('rpc/admin_mailing_list', { method: 'POST', body: '{}' })).json();
  if (!Array.isArray(list)) return json(res, 403, { error: 'Only HQ can email members.' });
  const url = 'https://bettordays.xyz' + (a.link && a.link.startsWith('/') ? a.link : '/');
  let sent = 0;
  for (let i = 0; i < list.length; i += 100) {
    const batch = list.slice(i, i + 100).map(m => ({
      from: process.env.RESEND_FROM || 'BettorDays HQ <hq@bettordays.xyz>', to: [m.email], subject: a.title,
      html: `<div style="font-family:Arial,sans-serif;background:#0b0d0c;color:#eef3f0;padding:28px"><h1 style="margin:0 0 10px;font-size:26px">${esc(a.title)}</h1><p style="color:#c8d3ce;font-size:16px;line-height:1.5">Hey @${esc(m.username)}, ${esc(a.body || '')}</p><p><a href="${url}" style="display:inline-block;background:#04ff9f;color:#0b0d0c;padding:12px 18px;font-weight:bold;text-decoration:none">Open the board</a></p><p style="color:#5b6b64;font-size:12px">21+. Bet what you can lose. You're getting this because you opted in to BettorDays updates. Turn them off anytime in the app under Me.</p></div>`,
      text: `${a.title}\n\n${a.body || ''}\n\n${url}\n\n21+. Turn off emails in the app under Me.`
    }));
    const r = await fetch('https://api.resend.com/emails/batch', { method: 'POST', headers: { Authorization: 'Bearer ' + process.env.RESEND_API_KEY, 'Content-Type': 'application/json' }, body: JSON.stringify(batch) });
    if (r.ok) sent += batch.length; else console.error('resend batch', r.status, await r.text());
  }
  await db(`announcements?id=eq.${a.id}`, { method: 'PATCH', body: JSON.stringify({ emailed: a.emailed + sent }) });
  return json(res, 200, { ok: true, id: a.id, emailed: sent, of: list.length });
}
