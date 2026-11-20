// 일괄 계산을 브라우저 밖(Node)에서 돌린다. 사이트의 일괄 계산과 같은 형식의 묶음을 만든다.
//   node batch.js <조각 번호> <조각 수> <출력 파일> [설정 파일]
const fs = require('fs'), path = require('path'), zlib = require('zlib');
const engPath = path.join(__dirname, '..', 'src', 'dtsolve', 'engine.js');
const SRC = fs.readFileSync(engPath, 'utf8');
const DTE = require(engPath);
const SVV = (() => { let h = 0; for (let i = 0; i < SRC.length; i++) h = (Math.imul(h, 31) + SRC.charCodeAt(i)) | 0; return (h >>> 0).toString(36); })();
const [shard, nsh, out, cfgFile] = [+process.argv[2] || 0, +process.argv[3] || 1, process.argv[4] || 'out.json.gz', (process.argv[5] && !process.argv[5].startsWith('--') ? process.argv[5] : null) || path.join(__dirname, 'config.json')];
const CF = JSON.parse(fs.readFileSync(cfgFile, 'utf8'));
const f = o => Object.keys(o).filter(n => o[n] > 0 && DTE.CODE[n]).sort().map(n => DTE.CODE[n] + o[n]).join(',');
const g = a => a.map(n => DTE.CODE[n]).filter(Boolean).sort().join(',');
const cfg = SVV + '|' + f(CF.main) + '|' + f(CF.extra) + '|' + g(CF.ban) + '/' + g(CF.nos);
const svHK = hand => hand.map(n => DTE.CODE[n] || 'X').sort().join(',');
const svCanon = hand => hand.slice().sort((a, b) => (DTE.CODE[a] || 'X') < (DTE.CODE[b] || 'X') ? -1 : 1);
function svHands(maxN, MM) {
  const N = DTE.N; const pool = Object.keys(MM).filter(n => MM[n] > 0 && DTE.CODE[n] && DTE.C[DTE.CODE[n]].k !== 'x' && !CF.ban.includes(n)).map(n => [n, MM[n]]); pool.push([N.X, 3]); pool.sort((a, b) => svHK([a[0]]) < svHK([b[0]]) ? -1 : 1);
  const o = []; const rec = (i, cur) => { if (cur.length) o.push(cur.slice()); if (cur.length >= maxN) return; for (let j = i; j < pool.length; j++) { const c = cur.filter(x => x === pool[j][0]).length; if (c >= pool[j][1]) continue; cur.push(pool[j][0]); rec(j, cur); cur.pop(); } }; rec(0, []); return o.sort((a, b) => a.length - b.length);
}
const all = svHands(CF.maxN, CF.main);
if (process.argv.includes('--info')) { console.log(JSON.stringify({ svv: SVV, cfg, hands: all.length })); process.exit(0); }
const mine = all.filter((_, i) => i % nsh === shard);
const items = [], hands = {}; const t0 = Date.now();
for (let k = 0; k < mine.length; k++) {
  const hand = mine[k], ch = svCanon(hand);
  const r = DTE.search(ch, CF.main, CF.extra, { group: true, optMain: CF.om, maxMs: CF.lim * 1000, maxStates: 5000000, ban: CF.ban, nos: CF.nos });
  if (r.error) { console.log('skip', ch.join(' + '), r.error); continue; }
  items.push(['B|' + cfg + '|' + svHK(hand), { hand: ch, groups: r.groups, complete: r.done, lim: CF.lim, states: r.states, ms: r.ms }]);
  const best = {}; for (const x of r.groups) { const u = x.u.join(','); if (!(best[u] >= x.sc)) best[u] = x.sc; }
  hands[svHK(hand)] = { h: ch, g: Object.entries(best), c: r.done, lim: CF.lim };
  console.log(`[${shard}/${nsh}] ${k + 1}/${mine.length} ${ch.join(' + ')} · ${r.states} 국면 · ${(r.ms / 1000).toFixed(1)}s${r.done ? '' : ' · 제한'} · 누적 ${((Date.now() - t0) / 60000).toFixed(1)}분`);
}
items.push(['BI|' + cfg, { hands }]);
fs.writeFileSync(out, zlib.gzipSync(JSON.stringify({ v: 1, svv: SVV, when: Date.now(), items })));
console.log('wrote', out, items.length - 1, 'hands');
