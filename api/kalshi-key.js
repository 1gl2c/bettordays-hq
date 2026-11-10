// Connect or disconnect your own Kalshi API key. The private key is encrypted here before it is stored,
// and the database never hands it back in readable form.
import { getUser, asUser, encrypt, normalizePem, kalshiClient, json } from '../lib/server.js';

export default async function handler(req, res) {
  const user = await getUser(req);
  if (!user) return json(res, 401, { error: 'Sign in again.' });
  const db = asUser(user);
  if (req.method === 'DELETE') {
    await db(`kalshi_keys?user_id=eq.${user.id}`, { method: 'DELETE' });
    return json(res, 200, { ok: true });
  }
  if (req.method !== 'POST') return json(res, 405, { error: 'POST or DELETE' });
  if (!process.env.KEY_ENCRYPTION_SECRET) return json(res, 503, { error: 'Key storage is not set up yet.' });
  try {
    const { key_id, private_key } = req.body || {};
    const id = String(key_id || '').trim();
    if (!/^[A-Za-z0-9-]{8,100}$/.test(id)) return json(res, 400, { error: 'That key ID doesn\'t look right.' });
    const pem = normalizePem(private_key);
    const bal = await kalshiClient(id, pem).get('/portfolio/balance');
    const r = await db('kalshi_keys?on_conflict=user_id', { method: 'POST', headers: { Prefer: 'resolution=merge-duplicates,return=minimal' }, body: JSON.stringify({ user_id: user.id, key_id: id, enc: encrypt(pem), last_sync: null }) });
    if (!r.ok) return json(res, 500, { error: 'Could not save the key.' });
    return json(res, 200, { ok: true, balance: typeof bal.balance === 'number' ? bal.balance / 100 : null });
  } catch (e) {
    return json(res, 400, { error: String(e.message || e) });
  }
}
