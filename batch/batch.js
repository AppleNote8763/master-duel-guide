// 일괄 계산을 브라우저 밖(Node)에서 돌린다. 사이트의 일괄 계산과 같은 형식의 묶음을 만든다.
//   node batch.js <조각 번호> <조각 수> <출력 파일> [설정 파일]
const fs = require('fs'), path = require('path'), zlib = require('zlib');
const engPath = path.join(__dirname, '..', 'src', 'dtsolve', 'engine.js');
const SRC = fs.readFileSync(engPath, 'utf8');
const DTE = require(engPath);
// 사이트(ui.js)의 SVV·SVREV와 같은 값. 탐색기를 고쳐도 기존 수의 순서가 유지되면 SVV는 그대로 둔다.
const SVV = '14didan', REV = 3;
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
const { spawnSync } = require('child_process'), os = require('os');
const MAXS = CF.maxStates || 5000000;
// 자식 모드: 손패 하나만 계산해 파일로 쓴다 (메모리가 넘쳐 죽어도 나머지 손패는 살린다)
if (process.argv.includes('--one')) {
  const i = +process.argv[process.argv.indexOf('--one') + 1], ms = +process.argv[process.argv.indexOf('--one') + 2], st = +process.argv[process.argv.indexOf('--one') + 3], of = process.argv[process.argv.indexOf('--one') + 4];
  const r = DTE.search(svCanon(all[i]), CF.main, CF.extra, { group: true, optMain: CF.om, maxMs: ms * 1000, maxStates: st, ban: CF.ban, nos: CF.nos });
  fs.writeFileSync(of, JSON.stringify(r)); process.exit(0);
}
// --redo <폴더>: 이미 끝까지 탐색한 손패는 빼고, 덜 끝난 것만 다시 계산한다
let targets = all.map((h, i) => [h, i]);
const prev = {};
if (process.argv.includes('--redo')) {
  const dir = process.argv[process.argv.indexOf('--redo') + 1];
  for (const fn of fs.readdirSync(dir).filter(x => /^gh-.*-p\d+\.gz$/.test(x))) for (const [k, v] of JSON.parse(zlib.gunzipSync(fs.readFileSync(path.join(dir, fn)))).items) if (k.startsWith('B|')) prev[k] = { complete: v.complete, states: v.states };
  targets = targets.filter(([h]) => { const v = prev['B|' + cfg + '|' + svHK(h)]; return !(v && v.complete); });
  console.log('다시 계산할 손패', targets.length);
}
const mine = targets.filter((_, i) => i % nsh === shard);
const items = [], hands = {}; const t0 = Date.now(); const tmp = path.join(os.tmpdir(), 'one-' + shard + '-' + process.pid + '.json');
const runOne = (i, ms, st) => { try { fs.unlinkSync(tmp); } catch (e) { } const p = spawnSync(process.execPath, ['--max-old-space-size=' + (process.env.HEAP || '4800'), __filename, String(shard), String(nsh), 'x', cfgFile, '--one', String(i), String(ms), String(st), tmp], { stdio: 'ignore' }); if (p.status !== 0 || !fs.existsSync(tmp)) return null; return JSON.parse(fs.readFileSync(tmp, 'utf8')); };
for (let k = 0; k < mine.length; k++) {
  const [hand, gi] = mine[k], ch = svCanon(hand);
  let r = runOne(gi, CF.lim, MAXS), lim = CF.lim, note = '';
  if (!r && process.env.HEAP) { r = runOne(gi, CF.lim, Math.round(MAXS * 0.65)); note = ' · 국면 한도를 줄여 재시도'; }
  if (!r) { r = runOne(gi, 180, 3000000); lim = 180; note = ' · 메모리 부족으로 줄여서 재시도'; }
  const old = prev['B|' + cfg + '|' + svHK(hand)]; if (old && r && !r.error && !r.done && r.states <= old.states) { console.log('유지', ch.join(' + ')); continue; }
  if (!r || r.error) { console.log('skip', ch.join(' + '), r ? r.error : '실패'); continue; }
  items.push(['B|' + cfg + '|' + svHK(hand), { hand: ch, groups: r.groups, complete: r.done, lim, states: r.states, ms: r.ms, gi, rev: REV }]);
  const best = {}; for (const x of r.groups) { const u = x.u.join(',') + '~' + (x.x || []).join(','); if (!(best[u] >= x.sc)) best[u] = x.sc; }
  hands[svHK(hand)] = { h: ch, g: Object.entries(best), c: r.done, lim };
  console.log(`[${shard}/${nsh}] ${k + 1}/${mine.length} ${ch.join(' + ')} · ${r.states} 국면 · ${(r.ms / 1000).toFixed(1)}s${r.done ? '' : ' · 한도'}${note} · 누적 ${((Date.now() - t0) / 60000).toFixed(1)}분`);
}
items.push(['BI|' + cfg, { hands }]);
fs.writeFileSync(out, zlib.gzipSync(JSON.stringify({ v: 1, svv: SVV, when: Date.now(), items })));
console.log('wrote', out, items.length - 1, 'hands');
