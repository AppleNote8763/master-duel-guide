// 조각별 결과를 사이트의 /batch/ 폴더로 옮기고 목록 파일을 만든다.
const fs = require('fs'), path = require('path'), zlib = require('zlib');
const [inDir, outDir, PRE] = [process.argv[2], process.argv[3], process.argv[4] || 'gh'];
const files = []; let svv = null; const t = Date.now();
for (const f of fs.readdirSync(inDir).filter(x => x.endsWith('.json.gz')).sort()) {
  const buf = fs.readFileSync(path.join(inDir, f)); const pack = JSON.parse(zlib.gunzipSync(buf)); svv = pack.svv;
  const n = pack.items.filter(x => x[0].startsWith('B|')).length; if (!n) continue;
  const name = PRE + '-' + svv + '-' + f.replace('.json.gz', '') + '.gz'; fs.writeFileSync(path.join(outDir, name), buf); files.push({ name, sz: 0, t, n });
}
if (svv) { for (const f of fs.readdirSync(outDir)) if (f.startsWith(PRE + '-') && !f.startsWith(PRE + '-' + svv + '-')) fs.unlinkSync(path.join(outDir, f)); fs.writeFileSync(path.join(outDir, svv + '-manifest-' + PRE + '.json'), JSON.stringify({ svv, files })); }
console.log('files', files.length, 'hands', files.reduce((a, f) => a + f.n, 0));
