// 일괄 계산 묶음 저장소. 계산은 하지 않고 파일만 보관한다.
//  GET  /api/batch?f=<이름>  : 저장된 묶음으로 넘겨 준다 (없으면 404)
//  PUT  /api/batch?f=<이름>  : 묶음을 올린다 (x-upload-key 필요, 4MB 이하)
import { put, head } from '@vercel/blob';

const NAME = /^[a-z0-9][a-z0-9._-]{0,80}$/;

export default async function handler(req, res) {
  const f = String(req.query.f || '');
  if (!NAME.test(f)) return res.status(400).json({ error: 'bad name' });
  const path = 'batch/' + f;
  if (req.method === 'GET') {
    try {
      const h = await head(path);
      res.setHeader('Cache-Control', 'no-store');
      return res.redirect(302, h.url + '?v=' + new Date(h.uploadedAt).getTime());
    } catch (e) {
      return res.status(404).json({ error: 'not found' });
    }
  }
  if (req.method === 'PUT') {
    if (!process.env.UPLOAD_KEY || req.headers['x-upload-key'] !== process.env.UPLOAD_KEY) return res.status(403).json({ error: 'forbidden' });
    const chunks = []; let n = 0;
    for await (const c of req) { n += c.length; if (n > 4300000) return res.status(413).json({ error: 'too large' }); chunks.push(c); }
    const b = await put(path, Buffer.concat(chunks), { access: 'public', addRandomSuffix: false, allowOverwrite: true, cacheControlMaxAge: 60, contentType: 'application/octet-stream' });
    return res.status(200).json({ ok: true, size: n, url: b.url });
  }
  res.setHeader('Allow', 'GET, PUT');
  return res.status(405).json({ error: 'method' });
}

export const config = { api: { bodyParser: false } };
