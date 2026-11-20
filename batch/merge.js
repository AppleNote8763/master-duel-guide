// 다시 계산한 결과를 기존 조각 파일에 합친다.  node merge.js <다시 계산한 묶음 폴더> <site/batch>
// 조각 파일이 커서 한 번에 하나씩만 읽는다.
const fs = require('fs'), path = require('path'), zlib = require('zlib');
const [inDir, outDir] = [process.argv[2], process.argv[3]];
const rd = f => JSON.parse(zlib.gunzipSync(fs.readFileSync(f)));
const files = fs.readdirSync(outDir).filter(x => /^gh-.*-p\d+\.gz$/.test(x)).sort();
const m0 = files[0].match(/^gh-(.*)-p(\d+)\.gz$/), svv = m0[1], pad = m0[2].length;
const nsh = Math.max(...files.map(f => +f.match(/-p(\d+)\.gz$/)[1])) + 1;
const byFile = {}; let n = 0;
for (const f of fs.readdirSync(inDir).filter(x => x.endsWith('.json.gz'))) { const pk = rd(path.join(inDir, f)); if (pk.svv !== svv) continue;
  for (const [k, v] of pk.items) if (k.startsWith('B|')) { const name = 'gh-' + svv + '-p' + String(v.gi % nsh).padStart(pad, '0') + '.gz'; (byFile[name] = byFile[name] || []).push([k, v]); n++; } }
const man = path.join(outDir, svv + '-manifest-gh.json'); let old = { files: [] }; try { old = JSON.parse(fs.readFileSync(man, 'utf8')); } catch (e) { }
const t = Date.now(), list = []; let tot = 0, cap = 0;
for (const name of [...new Set(files.concat(Object.keys(byFile)))].sort()) {
  const fp = path.join(outDir, name); const o = (old.files || []).find(x => x.name === name);
  if (!byFile[name]) { if (o) { list.push(o); tot += o.n; cap += o.cap || 0; } continue; }
  const P = fs.existsSync(fp) ? rd(fp) : { v: 1, svv, when: t, items: [] };
  for (const [k, v] of byFile[name]) { const cfg = k.slice(2, k.lastIndexOf('|')), hk = k.slice(k.lastIndexOf('|') + 1);
    const i = P.items.findIndex(x => x[0] === k); if (i >= 0 && (P.items[i][1].rev || 1) > (v.rev || 1)) continue; // 예전 탐색기 결과로 새 결과를 덮지 않는다
    if (i >= 0) P.items[i] = [k, v]; else P.items.unshift([k, v]);
    let bi = P.items.find(x => x[0] === 'BI|' + cfg); if (!bi) { bi = ['BI|' + cfg, { hands: {} }]; P.items.push(bi); }
    const best = {}; for (const x of v.groups) { const u = x.u.join(',') + '~' + (x.x || []).join(','); if (!(best[u] >= x.sc)) best[u] = x.sc; }
    bi[1].hands[hk] = { h: v.hand, g: Object.entries(best), c: v.complete, lim: v.lim }; }
  fs.writeFileSync(fp, zlib.gzipSync(JSON.stringify(P)));
  const bs = P.items.filter(x => x[0].startsWith('B|')); list.push({ name, sz: 0, t, n: bs.length, cap: bs.filter(x => !x[1].complete).length }); tot += bs.length; cap += bs.filter(x => !x[1].complete).length;
}
fs.writeFileSync(man, JSON.stringify({ svv, files: list }));
console.log('합친 손패', n, '바뀐 조각', Object.keys(byFile).length, '전체', tot, '바뀐 조각 안의 덜 끝난 것', cap);
