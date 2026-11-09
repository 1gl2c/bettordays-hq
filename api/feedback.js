import { put, list, get } from '@vercel/blob';

const MAX = 1500;
const clean = (v, n) => String(v ?? '').replace(/[\u0000-\u0008\u000B-\u001F]/g, '').trim().slice(0, n);

async function readBody(req) {
  if (req.body && typeof req.body === 'object') return req.body;
  const chunks = [];
  for await (const c of req) chunks.push(c);
  try { return JSON.parse(Buffer.concat(chunks).toString('utf8') || '{}'); } catch { return {}; }
}

export default async function handler(req, res) {
  res.setHeader('Cache-Control', 'no-store');

  if (req.method === 'POST') {
    const b = await readBody(req);
    if (b.website) return res.status(200).json({ ok: true }); // honeypot
    const msg = clean(b.msg, MAX);
    if (msg.length < 2) return res.status(400).json({ ok: false, error: 'Message is empty' });
    const entry = {
      at: new Date().toISOString(),
      name: clean(b.name, 60) || 'Anonymous',
      kind: ['idea', 'pick', 'feature', 'other'].includes(b.kind) ? b.kind : 'other',
      msg,
      page: clean(b.page, 120),
    };
    const id = `${entry.at.replace(/[:.]/g, '-')}-${Math.random().toString(36).slice(2, 8)}`;
    await put(`feedback/${id}.json`, JSON.stringify(entry), {
      access: 'private', contentType: 'application/json', addRandomSuffix: false,
    });
    return res.status(200).json({ ok: true });
  }

  if (req.method === 'GET') {
    const key = req.query?.key || new URL(req.url, 'http://x').searchParams.get('key');
    if (!process.env.FEEDBACK_ADMIN_KEY || key !== process.env.FEEDBACK_ADMIN_KEY) {
      return res.status(401).json({ ok: false });
    }
    const out = [];
    let cursor;
    do {
      const page = await list({ prefix: 'feedback/', cursor, limit: 1000 });
      for (const blob of page.blobs) {
        const r = await get(blob.pathname, { access: 'private' });
        if (r && r.statusCode === 200) out.push(JSON.parse(await new Response(r.stream).text()));
      }
      cursor = page.hasMore ? page.cursor : undefined;
    } while (cursor);
    out.sort((a, b) => (a.at < b.at ? 1 : -1));
    return res.status(200).json({ ok: true, count: out.length, entries: out });
  }

  res.setHeader('Allow', 'GET, POST');
  return res.status(405).json({ ok: false });
}
