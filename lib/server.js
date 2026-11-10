// Shared server helpers. Requests run as the signed-in user (their own token), so database row rules still apply.
import crypto from 'node:crypto';
export const SB_URL = 'https://ndcsjhetuasijbgpfhwj.supabase.co';
export const SB_PUB = 'sb_publishable_thFDxFfsdTESdl_MzPeE3g_pUqcSMRc';

export async function getUser(req) {
  const token = (req.headers.authorization || '').replace(/^Bearer /, '');
  if (!token) return null;
  const r = await fetch(SB_URL + '/auth/v1/user', { headers: { apikey: SB_PUB, Authorization: 'Bearer ' + token } });
  if (!r.ok) return null;
  return { ...(await r.json()), token };
}
export function asUser(user) {
  return (path, init = {}) => fetch(SB_URL + '/rest/v1/' + path, { ...init, headers: { apikey: SB_PUB, Authorization: 'Bearer ' + user.token, 'Content-Type': 'application/json', ...(init.headers || {}) } });
}
function secret() {
  const s = process.env.KEY_ENCRYPTION_SECRET;
  if (!s) throw new Error('KEY_ENCRYPTION_SECRET missing');
  return crypto.createHash('sha256').update(s).digest();
}
export function encrypt(text) {
  const iv = crypto.randomBytes(12);
  const c = crypto.createCipheriv('aes-256-gcm', secret(), iv);
  const enc = Buffer.concat([c.update(text, 'utf8'), c.final()]);
  return ['v1', iv.toString('base64'), c.getAuthTag().toString('base64'), enc.toString('base64')].join('.');
}
export function decrypt(blob) {
  const [v, iv, tag, enc] = blob.split('.');
  if (v !== 'v1') throw new Error('Unknown key format');
  const d = crypto.createDecipheriv('aes-256-gcm', secret(), Buffer.from(iv, 'base64'));
  d.setAuthTag(Buffer.from(tag, 'base64'));
  return Buffer.concat([d.update(Buffer.from(enc, 'base64')), d.final()]).toString('utf8');
}
export function normalizePem(p) {
  let s = String(p || '').trim().replace(/\\n/g, '\n').replace(/\r/g, '');
  if (!/-----BEGIN [A-Z ]*PRIVATE KEY-----/.test(s)) throw new Error('That doesn\'t look like a private key file. Paste everything, including the BEGIN and END lines.');
  crypto.createPrivateKey(s);
  return s;
}
const KALSHI = 'https://api.elections.kalshi.com', BASE = '/trade-api/v2';
export function kalshiClient(keyId, pem) {
  const headers = (method, path) => {
    const ts = String(Date.now());
    const sig = crypto.sign('sha256', Buffer.from(ts + method + path), { key: pem, padding: crypto.constants.RSA_PKCS1_PSS_PADDING, saltLength: crypto.constants.RSA_PSS_SALTLEN_DIGEST }).toString('base64');
    return { 'KALSHI-ACCESS-KEY': keyId, 'KALSHI-ACCESS-TIMESTAMP': ts, 'KALSHI-ACCESS-SIGNATURE': sig, Accept: 'application/json' };
  };
  const get = async (path, query = '') => {
    const r = await fetch(KALSHI + BASE + path + query, { headers: headers('GET', BASE + path) });
    if (r.status === 401 || r.status === 403) throw new Error('Kalshi said no to that key. Check the key ID and private key.');
    if (!r.ok) throw new Error(`Kalshi ${path} ${r.status}`);
    return r.json();
  };
  const all = async (path, field, extra = '') => {
    const out = []; let cursor = '';
    for (let i = 0; i < 10; i++) {
      const j = await get(path, `?limit=200${extra}${cursor ? '&cursor=' + encodeURIComponent(cursor) : ''}`);
      out.push(...(j[field] || [])); if (!j.cursor) break; cursor = j.cursor;
    }
    return out;
  };
  const cache = {};
  const market = async t => {
    if (t in cache) return cache[t];
    const r = await fetch(`${KALSHI}${BASE}/markets/${encodeURIComponent(t)}`);
    return (cache[t] = r.ok ? (await r.json()).market : null);
  };
  return { get, all, market };
}
export function json(res, code, body) { res.status(code).json(body); }
