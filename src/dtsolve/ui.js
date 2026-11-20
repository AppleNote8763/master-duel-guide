// ---- 탐색 탭 (드래곤테일 낙인) ----
(0, eval)(SV_ENGINE);
const SVBK = 'dt-sv-ban';
const SVNK = 'dt-sv-nos';
const SV = { nos: (() => { try { return JSON.parse(localStorage.getItem(SVNK) || '[]') } catch (e) { return [] } })(), bt: { open: false, n: 3, par: 2, lim: 180, run: false, done: 0, total: 0, cur: [], ws: [], sz: 0, shown: 60 }, bidx: null, bcfg: '', mopen: false, ban: (() => { try { return JSON.parse(localStorage.getItem(SVBK) || '[]') } catch (e) { return [] } })(), nof: [], bopen: false, cached: false, xopen: false, hand: [], lim: 60, res: null, busy: false, flt: 'all', sort: 'score', open: null, prog: '', info: '', w: null, shown: 30 };
const SVK = 'dt-found-v1';
const svShort = n => n.replace('드래곤테일 ', '').replace(' 드래곤테일', '').replace('순백의 성녀 ', '').replace('혁의 성녀 ', '').replace('패의 ', '').replace('프레데터 플랜츠 베르테 ', '').replace('The Fallen & The Virtuous', 'F&V');
function svStore() { try { return JSON.parse(localStorage.getItem(SVK) || '[]') } catch (e) { return [] } }
function svSaveStore(a) { try { localStorage.setItem(SVK, JSON.stringify(a)) } catch (e) { } }
function svInject() {
  if (!D.solver || !CU) return;
  for (const f of svStore()) {
    if (D.combos.some(c => c.id === f.combo.id)) continue;
    D.combos.push(f.combo); CU.req[f.combo.id] = f.req;
    let g = CU.groups.find(g => g.name === f.group); if (!g) { g = { name: f.group, items: [], size: f.size, cards: f.cards }; CU.groups.push(g) }
    g.items.push([f.combo.id, f.label]);
  }
  NAMES = null;
}
function svRemove(id) {
  svSaveStore(svStore().filter(f => f.combo.id !== id));
  const i = D.combos.findIndex(c => c.id === id); if (i >= 0) D.combos.splice(i, 1); delete CU.req[id];
  for (const g of CU.groups) g.items = g.items.filter(it => it[0] !== id);
  CU.groups = CU.groups.filter(g => g.items.length); NAMES = null;
}
function svSnap(s, n, title, act, desc, prev, fill) {
  const zones = {}; const N = DTE.N;
  for (const m of s.field) zones[m.z] = { name: N[m.c], kind: kindOf(N[m.c]) || (DTE.C[m.c].k === 'x' ? DTE.C[m.c].x : 'eff'), arrows: m.c === 'ANA' ? ['DL', 'DR'] : null, mats: 0, linked: false };
  for (const m of s.st) zones[m.z] = { name: N[m.c], kind: kindOf(N[m.c]) || (DTE.C[m.c].k === 't' ? 'trap' : 'spell'), arrows: null, mats: 0, linked: false };
  const changed = Object.keys(zones).filter(z => !prev || !prev.zones[z] || prev.zones[z].name !== zones[z].name);
  return { n, title, act: act || '', desc: desc || '', zones, hand: s.hand.map(c => N[c]).concat(Array(fill).fill('패사고')), gy: s.gy.map(c => N[c]), ban: s.ban.map(c => N[c]), changed: prev ? changed : [], from: [] };
}
function svCombo(r, id) {
  const N = DTE.N, fill = Math.max(0, 5 - r.start.hand.length); const steps = []; let prev = null, n = 1;
  const add = (s, t, a, d) => { const sn = svSnap(s, n++, t, a, d, prev, fill); steps.push(sn); prev = sn };
  add(r.start, '시작 패', '', '선공 1턴, 나머지 패는 전부 안 쓰는 카드로 가정');
  for (const st of r.steps) add(st.s, st.title, st.act, st.desc);
  for (const st of r.end) add(st.s, st.title, st.act, st.desc);
  // 필요한 카드: 손패 + 덱·엑스트라 덱에서 빠져나간 최대 장수
  const req = { main: {}, extra: {} };
  for (const c of r.start.hand) if (c !== 'X') req.main[N[c]] = (req.main[N[c]] || 0) + 1;
  const all = r.steps.map(x => x.s).concat(r.end.map(x => x.s));
  const base = Object.assign({}, req.main);
  for (const c in r.start.deck) { let mx = 0; for (const s of all) mx = Math.max(mx, r.start.deck[c] - (s.deck[c] || 0)); if (mx > 0) req.main[N[c]] = (base[N[c]] || 0) + mx }
  for (const c in r.start.extra) { let mx = 0; for (const s of all) mx = Math.max(mx, r.start.extra[c] - (s.extra[c] || 0)); if (mx > 0) req.extra[N[c]] = mx }
  const hn = r.start.hand.map(c => N[c]); const gen = hn.filter(x => x === N.X).length;
  const group = hn.map(svShort).join(' + ');
  const board = r.field.join(' · ') + (r.set.length ? ' + ' + r.set.join('·') + ' 세트' : '') + (r.handCards.length ? ', 패에 ' + r.handCards.join('·') : '');
  const label = '[탐색] ' + r.field.map(svShort).join(' · ') + (r.set.length ? ' + ' + r.set.map(svShort).join('·') + ' 세트' : '');
  const combo = { id, deck: 'base', title: group, sub: '탐색기로 찾은 수순 · 방해 ' + r.score + '개 · 카드 원문 검증 전이니 실전 전에 한 번 확인하세요', board, opp: r.items.map(i => [i[0], i[1], i[2]]), steps, mc: { sr: 0, pu: 0, fu: 0 }, need: '필요한 패: ' + hn.join(' + '), gen };
  return { combo, group, label, req, size: hn.length, cards: hn.map(svShort).filter(x => !['우르굴라', '파이메나', '알버스의 낙윤', '아무 몬스터'].includes(x)) };
}
function svAdd(r) {
  const id = 'sv' + Date.now().toString(36); const f = svCombo(r, id); const a = svStore(); a.push(f); svSaveStore(a); svInject(); cuSync(); return id;
}
// ---- 탐색 결과 자동 저장 (IndexedDB, 안 되면 메모리) ----
const SVM = new Map(); let SVDB = null;
const SVV = (() => { let h = 0; for (let i = 0; i < SV_ENGINE.length; i++) h = (Math.imul(h, 31) + SV_ENGINE.charCodeAt(i)) | 0; return (h >>> 0).toString(36) })();
function svEff(o) { const r = {}; for (const n in o) if (o[n] > 0 && !SV.ban.includes(n)) r[n] = o[n]; return r }
function svKey(hand) { const f = o => Object.keys(o).filter(n => o[n] > 0 && DTE.CODE[n]).sort().map(n => DTE.CODE[n] + o[n]).join(','); return SVV + '|' + hand.slice().sort().map(n => DTE.CODE[n] || n).join(',') + '|' + f(DS.main) + '|' + f(DS.extra) + '|' + svBN() }
function svBN() { const g = a => a.map(n => DTE.CODE[n]).filter(Boolean).sort().join(','); return g(SV.ban) + '/' + g(SV.nos) }
// ---- 일괄 계산: 후보 엑스트라 카드를 모두 넣고 한 번 계산해 두고, 볼 때 지금 엑스트라 덱으로 거른다 ----
function svSup() { const b = Object.fromEntries(CU.base.extra), r = {}; for (const n of (CU.pool.extra || [])) if (DTE.CODE[n]) r[n] = Math.max(DS.extra[n] || 0, b[n] || 0, 1); for (const n in DS.extra) if (DS.extra[n] > 0 && DTE.CODE[n]) r[n] = Math.max(r[n] || 0, DS.extra[n]); return r }
function svOptMain() { const b = Object.fromEntries(CU.base.main); return (CU.pool.main || []).filter(n => DTE.CODE[n] && DTE.C[DTE.CODE[n]].k !== 'x' && !(b[n] > 0)) }
function svMainOf(m) { if (!m) return DS.main; const r = Object.assign({}, DS.main); for (const n of svOptMain()) r[n] = 1; return r }
function svCfg(m) { const f = o => Object.keys(o).filter(n => o[n] > 0 && DTE.CODE[n]).sort().map(n => DTE.CODE[n] + o[n]).join(','); return SVV + '|' + f(svMainOf(m)) + '|' + f(svSup()) + '|' + svBN() }
function svHK(hand) { return hand.map(n => DTE.CODE[n] || 'X').sort().join(',') }
function svCanon(hand) { return hand.slice().sort((a, b) => (DTE.CODE[a] || 'X') < (DTE.CODE[b] || 'X') ? -1 : 1) }
function svDC() { const d = {}; for (const n in DS.extra) if (DS.extra[n] > 0 && DTE.CODE[n]) d[DTE.CODE[n]] = DS.extra[n]; for (const n of svOptMain()) if (DS.main[n] > 0) d[DTE.CODE[n]] = DS.main[n]; return d }
function svHandOk(h) { const c = {}; for (const n of h) { if (n === DTE.N.X) continue; c[n] = (c[n] || 0) + 1; if (c[n] > (DS.main[n] || 0)) return false } return true }
function svOkU(u, d) { const c = {}; for (const x of u) { c[x] = (c[x] || 0) + 1; if (c[x] > (d[x] || 0)) return false } return true }
function svHands(maxN, MM) { MM = MM || DS.main; const N = DTE.N; const pool = Object.keys(MM).filter(n => MM[n] > 0 && DTE.CODE[n] && DTE.C[DTE.CODE[n]].k !== 'x' && !SV.ban.includes(n)).map(n => [n, MM[n]]); pool.push([N.X, 3]); pool.sort((a, b) => svHK([a[0]]) < svHK([b[0]]) ? -1 : 1);
  const out = []; const rec = (i, cur) => { if (cur.length) out.push(cur.slice()); if (cur.length >= maxN) return; for (let j = i; j < pool.length; j++) { const c = cur.filter(x => x === pool[j][0]).length; if (c >= pool[j][1]) continue; cur.push(pool[j][0]); rec(j, cur); cur.pop() } }; rec(0, []); return out.sort((a, b) => a.length - b.length) }
async function svIdx() { const cfg = svCfg(SV.bt.mm); if (SV.bcfg === cfg && SV.bidx) return SV.bidx; const r = await svGet('BI|' + cfg); SV.bcfg = cfg; SV.bidx = r || { hands: {} }; return SV.bidx }
// ---- 내보내기 / 가져오기: 일괄 계산 결과를 묶음 파일 하나로 ----
const SVWEB = location.protocol === 'file:' || /(^localhost$|\.vercel\.app$)/.test(location.hostname);
async function svAllB() { const db = await svDb(); if (!db) return []; return new Promise(res => { try { const st = db.transaction('res').objectStore('res'); const kq = st.getAllKeys(), vq = st.getAll(); vq.onsuccess = () => { const out = []; kq.result.forEach((k, i) => { if (typeof k === 'string' && (k.startsWith('B|') || k.startsWith('BI|'))) out.push([k, vq.result[i]]) }); res(out) }; vq.onerror = () => res([]) } catch (e) { res([]) } }) }
function svPack(items, sz) { // sz: 0 전체, 1~3 손패 장수
  const out = []; for (const [k, v] of items) { if (!k.includes('|' + SVV + '|') && !k.startsWith('B|' + SVV) && !k.startsWith('BI|' + SVV)) continue;
    if (k.startsWith('BI|')) { const h = {}; for (const hk in v.hands) if (!sz || v.hands[hk].h.length === sz) h[hk] = v.hands[hk]; if (Object.keys(h).length) out.push([k, { hands: h }]) }
    else if (!sz || v.hand.length === sz) out.push([k, v]) }
  return { v: 1, svv: SVV, when: Date.now(), items: out } }
async function svGz(obj) { const b = new Blob([JSON.stringify(obj)]); if (typeof CompressionStream === 'undefined') return b; return new Response(b.stream().pipeThrough(new CompressionStream('gzip'))).blob() }
async function svUngz(blob) { const head = new Uint8Array(await blob.slice(0, 2).arrayBuffer()); if (head[0] === 0x1f && head[1] === 0x8b) return JSON.parse(await new Response(blob.stream().pipeThrough(new DecompressionStream('gzip'))).text()); return JSON.parse(await blob.text()) }
function svBetter(a, b) { if (!b) return true; if (a.c !== undefined || b.c !== undefined) return (a.c && !b.c) || (!!a.c === !!b.c && (a.lim || 0) > (b.lim || 0)); return (a.complete && !b.complete) || (!!a.complete === !!b.complete && (a.lim || 0) > (b.lim || 0)) }
async function svMerge(pack) { // 더 끝까지 탐색한 쪽을 남긴다. 반환: [새로 넣은 손패 수, 건너뛴 수]
  if (!pack || pack.v !== 1 || !Array.isArray(pack.items)) throw new Error('일괄 계산 묶음 파일이 아닙니다');
  if (pack.svv !== SVV) throw new Error('이 파일은 다른 버전의 탐색기로 계산한 것이라 쓸 수 없습니다');
  let add = 0, skip = 0;
  for (const [k, v] of pack.items) { if (k.startsWith('BI|')) { const cur0 = await svGet(k) || { hands: {} }; for (const hk in v.hands) if (svBetter(v.hands[hk], cur0.hands[hk])) cur0.hands[hk] = v.hands[hk]; await svPut(k, cur0) } else { const c0 = await svGet(k); if (svBetter(v, c0)) { await svPut(k, v); add++ } else skip++ } }
  SV.bidx = null; SV.bcfg = ''; return [add, skip] }
async function svExport(sz) { const pack = svPack(await svAllB(), sz); const n = pack.items.filter(x => x[0].startsWith('B|')).length; if (!n) { SV.bt.msg = '내보낼 일괄 계산 결과가 없습니다.'; renderSolve(); return }
  const blob = await svGz(pack); const a = document.createElement('a'); a.href = URL.createObjectURL(blob); const d = new Date(); a.download = 'dt-batch-' + (sz ? sz + 'card-' : '') + d.getFullYear() + String(d.getMonth() + 1).padStart(2, '0') + String(d.getDate()).padStart(2, '0') + '.json.gz'; document.body.appendChild(a); a.click(); a.remove(); setTimeout(() => URL.revokeObjectURL(a.href), 60000);
  SV.bt.msg = `손패 ${n}개를 파일 하나로 내보냈습니다 (${(blob.size / 1048576).toFixed(1)}MB).` + (SVWEB ? '' : ' 이 화면(Claude 아티팩트)에서는 내려받기가 막혀 파일이 저장되지 않을 수 있습니다.'); renderSolve() }
async function svB64(blob) { const u = new Uint8Array(await blob.arrayBuffer()); let t = ''; for (let i = 0; i < u.length; i += 32768) t += String.fromCharCode.apply(null, u.subarray(i, i + 32768)); return 'DTB1:' + btoa(t) }
async function svCopyOut(sz) { const pack = svPack(await svAllB(), sz); const n = pack.items.filter(x => x[0].startsWith('B|')).length; if (!n) { SV.bt.msg = '내보낼 일괄 계산 결과가 없습니다.'; renderSolve(); return } const t = await svB64(await svGz(pack)); try { await navigator.clipboard.writeText(t); SV.bt.msg = `손패 ${n}개를 복사했습니다 (${(t.length / 1048576).toFixed(1)}MB). 다른 기기의 "붙여넣어 가져오기" 칸에 붙여넣으세요.` } catch (e) { SV.bt.msg = '복사하지 못했습니다: ' + (e.message || e) } renderSolve() }
async function svPasteIn(t) { t = (t || '').trim(); if (!t.startsWith('DTB1:')) { SV.bt.msg = '가져오기 실패: 복사한 일괄 계산 묶음이 아닙니다.'; renderSolve(); return } const bin = atob(t.slice(5)); const u = new Uint8Array(bin.length); for (let i = 0; i < bin.length; i++) u[i] = bin.charCodeAt(i); SV.bt.pin = false; await svImport(new Blob([u])) }
async function svImport(file) { try { const [add, skip] = await svMerge(await svUngz(file)); SV.bt.msg = `가져오기 완료: 손패 ${add}개를 넣었고, 이미 더 나은 결과가 있는 ${skip}개는 그대로 두었습니다.` } catch (e) { SV.bt.msg = '가져오기 실패: ' + (e.message || e) } SV.bt.open = true; await svIdx(); if (cur === 'solve') renderSolve() }
// ---- 서버 보관: 묶음을 올려 두고 다른 기기에서 한 번 받아 쓴다 ----
const SVSRV = /\.vercel\.app$/.test(location.hostname) || location.hostname === 'localhost' ? '/api/batch' : null;
const SVUK = 'dt-up-key';
(() => { try { const q = new URLSearchParams(location.search); const k = q.get('k'); if (k) { localStorage.setItem(SVUK, k); q.delete('k'); history.replaceState(null, '', location.pathname + (q.toString() ? '?' + q : '') + location.hash) } } catch (e) { } })();
function svUpKey() { try { return localStorage.getItem(SVUK) || '' } catch (e) { return '' } }
async function svPutSrv(name, blob) { const r = await fetch(SVSRV + '?f=' + encodeURIComponent(name), { method: 'PUT', headers: { 'x-upload-key': svUpKey(), 'content-type': 'application/octet-stream' }, body: blob }); if (!r.ok) throw new Error(r.status === 403 ? '올리기 권한이 없습니다' : '서버 오류 ' + r.status) }
async function svPush(quiet) { if (!SVSRV || !svUpKey() || SV.bt.pushing) return; const B = SV.bt; B.pushing = true; const say = m => { B.smsg = m; const e = document.getElementById('svbs'); if (e) e.textContent = m };
  try { const all = await svAllB(); const files = []; let sig0 = {}; try { sig0 = JSON.parse(localStorage.getItem('dt-up-sig') || '{}') } catch (e) { } const sig = {}; let sent = 0;
    for (const sz of [1, 2, 3]) { const pack = svPack(all, sz); const its = pack.items.filter(x => x[0].startsWith('B|')); if (!its.length) continue; const sg = its.length + ':' + its.filter(x => x[1].complete).length + ':' + its.reduce((a, x) => a + (x[1].lim || 0), 0);
      let parts = 1, blobs; for (; ;) { blobs = []; const idxs = pack.items.filter(x => x[0].startsWith('BI|')); for (let i = 0; i < parts; i++) blobs.push(await svGz({ v: 1, svv: SVV, when: pack.when, items: its.filter((_, j) => j % parts === i).concat(i ? [] : idxs) })); if (blobs.every(b => b.size < 3800000)) break; parts *= 2 }
      const old = (sig0[SVV + sz] || '').split('|'); const names = blobs.map((_, i) => SVV + '-' + sz + '-' + i + '.gz');
      if (old[0] !== sg) { for (let i = 0; i < blobs.length; i++) { say(`서버에 올리는 중: ${sz}장 묶음 ${i + 1}/${blobs.length}`); await svPutSrv(names[i], blobs[i]); sent++ } }
      sig[SVV + sz] = sg + '|' + (old[0] === sg && old[1] ? old[1] : Date.now()); for (const n of names) files.push({ name: n, sz, t: +sig[SVV + sz].split('|')[1], n: its.length }) }
    if (sent) { await svPutSrv(SVV + '-manifest.json', new Blob([JSON.stringify({ svv: SVV, files })])); localStorage.setItem('dt-up-sig', JSON.stringify(sig)); for (const f of files) localStorage.setItem('dt-dl-' + f.name, String(f.t)) }
    const d = new Date(); say(sent ? `서버에 올렸습니다 (${d.getHours()}시 ${String(d.getMinutes()).padStart(2, '0')}분 · 손패 ${files.reduce((a, f) => a + (f.name.endsWith('-0.gz') ? f.n : 0), 0)}개)` : (quiet ? B.smsg || '' : '서버에 이미 같은 내용이 올라가 있습니다'))
  } catch (e) { say('서버에 올리지 못했습니다: ' + (e.message || e)) } B.pushing = false }
async function svPull() { if (!SVSRV || SV.pulled) return; SV.pulled = true; const B = SV.bt; try { let add = 0, got = 0; for (const [mu, fu] of [[SVSRV + '?f=' + SVV + '-manifest.json', n => SVSRV + '?f=' + n], ['/batch/' + SVV + '-manifest-gh.json', n => '/batch/' + n]]) { const r = await fetch(mu, { cache: 'no-store' }); if (!r.ok) continue; let man; try { man = await r.json() } catch (e) { continue }
    for (const f of man.files || []) { let t0 = 0; try { t0 = +localStorage.getItem('dt-dl-' + f.name) || 0 } catch (e) { } if (t0 >= f.t) continue; B.smsg = '저장된 일괄 계산 결과를 받는 중…'; const el = document.getElementById('svbs'); if (el) el.textContent = B.smsg; const q = await fetch(fu(f.name), { cache: 'no-store' }); if (!q.ok) continue; const [a] = await svMerge(await svUngz(await q.blob())); add += a; got++; try { localStorage.setItem('dt-dl-' + f.name, String(f.t)) } catch (e) { } } }
    if (got) { B.smsg = `서버에서 일괄 계산 결과를 받았습니다 (새로 넣은 손패 ${add}개)`; await svIdx(); if (cur === 'solve') { const y = window.scrollY; renderSolve(); window.scrollTo(0, y) } } } catch (e) { SV.pulled = false } }
function svBWorker() { const glue = `self.onmessage=e=>{const q=e.data;const r=DTE.search(q.hand,q.main,q.extra,{group:true,optMain:q.om,maxMs:q.lim*1000,maxStates:q.lim>=86400?9000000:5000000,ban:q.ban,nos:q.nos,onProgress:(n,d)=>self.postMessage({p:n,d})});self.postMessage({done:1,r})}`; return new Worker(URL.createObjectURL(new Blob([SV_ENGINE, '\n', glue], { type: 'text/javascript' }))) }
async function svBatch() { const B = SV.bt; if (B.run) return; const cfg = svCfg(B.mm), idx = await svIdx(); const main = Object.assign({}, svMainOf(B.mm)), om = svOptMain(), extra = svSup(), ban = SV.ban.slice(), nos = SV.nos.slice(), lim = B.lim;
  const all = svHands(B.n, main); const todo = all.filter(h => { const e = idx.hands[svHK(h)]; return !(e && (e.c || e.lim >= lim)) }); B.total = all.length; B.done = all.length - todo.length; B.run = true; B.since = 0; B.cur = []; B.ws = []; B.t0 = Date.now(); B.d0 = B.done; let stop = false; B.stopped = false; B.stop = () => { stop = true; B.stopped = true; try { localStorage.removeItem('dt-bt-q') } catch (e) { } B.ws.forEach(w => w.terminate()); B.ws = []; B.run = false; B.cur = []; if (cur === 'solve') renderSolve() };
  const upd = () => { const e = document.getElementById('svbp'); if (e) e.textContent = svBProg() };
  const one = () => new Promise(res => { const hand = todo.shift(); if (!hand || stop) return res(false); const ch = svCanon(hand); const w = svBWorker(); B.ws.push(w); const tag = { h: ch.map(svShort).join(' + '), p: 0 }; B.cur.push(tag); upd();
    const fin = () => { w.terminate(); B.ws = B.ws.filter(x => x !== w); B.cur = B.cur.filter(x => x !== tag); B.done++; upd(); res(true) };
    w.onmessage = async ev => { const m = ev.data; if (!m.done) { tag.p = m.p; upd(); return } const r = m.r; if (!r.error) { await svPut('B|' + cfg + '|' + svHK(hand), { hand: ch, groups: r.groups, complete: r.done, lim, states: r.states, ms: r.ms }); const best = {}; for (const g of r.groups) { const k = g.u.join(','); if (!(best[k] >= g.sc)) best[k] = g.sc } idx.hands[svHK(hand)] = { h: ch, g: Object.entries(best), c: r.done, lim }; await svPut('BI|' + cfg, idx); if (++B.since >= 50) { B.since = 0; svPush(true) } } fin() };
    w.onerror = () => fin(); w.postMessage({ hand: ch, main, extra, ban, nos, lim, om }) });
  if (cur === 'solve') renderSolve(); const lane = async () => { while (!stop && await one()); }; await Promise.all(Array.from({ length: B.par }, lane)); if (!stop) { B.run = false; B.cur = []; if (cur === 'solve') renderSolve(); svPush(true) } }
// 여러 구성을 차례로 돌리고, 탭이 다시 열려도 이어서 한다
function svQSave() { const B = SV.bt; try { if (B.q && B.q.length) localStorage.setItem('dt-bt-q', JSON.stringify({ q: B.q, n: B.n, lim: B.lim, par: B.par })); else localStorage.removeItem('dt-bt-q') } catch (e) { } }
async function svQueue(q) { const B = SV.bt; if (B.run) return; B.q = q.slice(); svQSave(); while (B.q.length) { B.mm = B.q[0]; SV.bidx = null; await svBatch(); if (B.stopped) return; B.q.shift(); svQSave() } }
setTimeout(() => { try { if (!D.solver || SV.bt.run) return; const s = JSON.parse(localStorage.getItem('dt-bt-q') || 'null'); if (s && s.q && s.q.length) { Object.assign(SV.bt, { n: s.n, lim: s.lim, par: s.par }); svQueue(s.q) } } catch (e) { } }, 2500);
function svBProg() { const B = SV.bt; const el = (Date.now() - B.t0) / 1000, dn = B.done - B.d0; const eta = dn > 0 ? (B.total - B.done) * el / dn : 0; const f = t => t >= 3600 ? Math.floor(t / 3600) + '시간 ' + Math.round(t % 3600 / 60) + '분' : t >= 60 ? Math.round(t / 60) + '분' : Math.round(t) + '초'; return (B.q && B.q.length > 1 ? `[${B.mm ? '추가 카드 포함' : '지금 덱'} · 뒤에 ${B.q.length - 1}개 구성 대기] ` : B.mm ? '[추가 카드 포함] ' : '') + `${B.done} / ${B.total} 완료` + (eta ? ` · 남은 시간 약 ${f(eta)}` : '') + (B.cur.length ? ' · 계산 중: ' + B.cur.map(c => c.h + (c.p ? ' (' + (c.p / 10000).toFixed(0) + '만)' : '')).join(', ') : '') }
async function svFromBatch(hand) { let rec = null, m = 0; for (m of [0, 1]) { rec = await svGet('B|' + svCfg(m) + '|' + svHK(hand)); if (rec) break } if (!rec) return null; const d = svDC(), omc = svOptMain().map(n => DTE.CODE[n]); const ok = rec.groups.filter(g => svOkU(g.u, d)).sort((a, b) => b.sc - a.sc || a.d - b.d).slice(0, 400);
  const main = svMainOf(m), extra = svSup(), o = { ban: SV.ban, nos: SV.nos }; const best = new Map();
  for (const g of ok) { const cu = {}; for (const x of g.u) cu[x] = (cu[x] || 0) + 1; const r = DTE.replay(rec.hand, main, extra, o, g.p, E => { const R = DTE.res(), a = {}, dk = {}; for (const c in d) { if (omc.includes(c)) continue; const v = Math.min((E.extra[c] || 0) + (R[c] || 0), d[c] - (cu[c] || 0)); if (v > 0) a[c] = v } for (const c of omc) dk[c] = Math.max(0, Math.min(E.deck[c] || 0, (d[c] || 0) - (cu[c] || 0))); return { x: a, d: dk } }); if (!r) continue; const k = r.field.slice().sort().join(',') + '|' + r.set.slice().sort().join(',') + '|' + r.handCards.slice().sort().join(','); const c0 = best.get(k); if (!c0 || r.score > c0.score || (r.score === c0.score && r.nsteps < c0.nsteps)) best.set(k, r) }
  return { rec, results: [...best.values()].sort((a, b) => b.score - a.score || b.hand - a.hand || a.nsteps - b.nsteps) } }
function svDb() { return new Promise(res => { if (SVDB) return res(SVDB); try { const q = indexedDB.open('dtsolve', 1); q.onupgradeneeded = () => q.result.createObjectStore('res'); q.onsuccess = () => { SVDB = q.result; res(SVDB) }; q.onerror = () => res(null) } catch (e) { res(null) } }) }
async function svGet(k) { if (SVM.has(k)) return SVM.get(k); const db = await svDb(); if (!db) return null; return new Promise(res => { try { const q = db.transaction('res').objectStore('res').get(k); q.onsuccess = () => { if (q.result) SVM.set(k, q.result); res(q.result || null) }; q.onerror = () => res(null) } catch (e) { res(null) } }) }
async function svPut(k, v) { SVM.set(k, v); const db = await svDb(); if (!db) return; try { db.transaction('res', 'readwrite').objectStore('res').put(v, k) } catch (e) { } }
async function svClearCache() { SVM.clear(); const db = await svDb(); if (db) try { db.transaction('res', 'readwrite').objectStore('res').clear() } catch (e) { } }
function svWorker() {
  const glue = `self.onmessage=e=>{const q=e.data;const r=DTE.search(q.hand,q.main,q.extra,{maxMs:q.lim?q.lim*1000:864e5,maxStates:q.lim?5000000:9000000,ban:q.ban,nos:q.nos,onProgress:(n,d)=>self.postMessage({p:n,d})});
if(r.error){self.postMessage({done:1,error:r.error,results:[]});return}
const best=new Map();for(const x of r.results){const k=x.field.slice().sort().join(',')+'|'+x.set.slice().sort().join(',');if(!best.has(k))best.set(k,x)}
const all=[...best.values()];const pick=new Set();const top=(a,n)=>a.slice(0,n).forEach(x=>pick.add(x));
for(const kd of['dt','brand','mix',null]){const a=kd?all.filter(x=>x.kind===kd):all;top(a,100);top(a.slice().sort((p,q)=>q.hand-p.hand||q.score-p.score),30);top(a.filter(x=>x.score>0).sort((p,q)=>p.nsteps-q.nsteps||q.score-p.score),30);top(a.slice().sort((p,q)=>q.field.length-p.field.length||q.score-p.score),30)}
self.postMessage({done:1,results:[...pick],states:r.states,complete:r.done,ms:r.ms,total:all.length})}`;
  return new Worker(URL.createObjectURL(new Blob([SV_ENGINE, '\n', glue], { type: 'text/javascript' })));
}
async function svRun(force) {
  if (SV.busy) return; const hand = SV.hand.slice(); if (!hand.length) return;
  const ck = svKey(hand); SV.cached = false;
  if (force !== true) { const hit = await svGet(ck); if (hit && (hit.complete || (SV.lim && hit.lim >= SV.lim) || (!SV.lim && !hit.lim))) { SV.res = hit.results; SV.cached = true; SV.open = null; SV.shown = 30; SV.info = '저장된 결과를 불러왔습니다 (' + hit.when + ' 계산) · ' + hit.info; renderSolve(); return }
    const bt = await svFromBatch(hand); if (bt) { SV.res = bt.results; SV.cached = true; SV.open = null; SV.shown = 30; SV.info = '일괄 계산 결과에서 불러왔습니다 · 지금 엑스트라 덱으로 가능한 것만 표시 · 국면 ' + bt.rec.states.toLocaleString() + '개' + (bt.rec.complete ? ' · 끝까지 탐색함' : ' · 제한에 걸려 찾은 것까지만'); renderSolve(); return } }
  SV.busy = true; SV.res = null; SV.prog = '탐색 시작'; SV.info = ''; SV.open = null; SV.shown = 30; renderSolve();
  const lim0 = SV.lim;
  const w = SV.w = svWorker(); const t0 = Date.now();
  w.onmessage = e => {
    const m = e.data;
    if (m.done) { SV.busy = false; SV.w = null; w.terminate(); if (m.error) { SV.info = m.error; SV.res = [] } else { SV.res = m.results; SV.info = `국면 ${m.states.toLocaleString()}개 확인 · ${(m.ms / 1000).toFixed(1)}초 · 최종 필드 ${m.total.toLocaleString()}종` + (m.complete ? ' · 끝까지 탐색함' : lim0 ? ' · 시간 제한으로 중단 (찾은 것까지만 표시)' : ' · 국면 수 한도(900만)에서 중단 (찾은 것까지만 표시)'); const dd = new Date(); svPut(ck, { results: m.results, complete: m.complete, lim: lim0, info: SV.info, when: (dd.getMonth() + 1) + '월 ' + dd.getDate() + '일' }) } if (cur === 'solve') renderSolve(); return }
    SV.prog = `국면 ${m.p.toLocaleString()}개 · ${m.d}단계째 · ${((Date.now() - t0) / 1000).toFixed(0)}초`; const p = document.getElementById('svprog'); if (p) p.textContent = SV.prog;
  };
  w.onerror = e => { SV.busy = false; SV.w = null; SV.info = '탐색 중 오류: ' + (e.message || ''); SV.res = []; if (cur === 'solve') renderSolve() };
  w.postMessage({ hand, main: DS.main, extra: DS.extra, ban: SV.ban.slice(), nos: SV.nos.slice(), lim: SV.lim });
}
function svStop() { if (SV.w) { SV.w.terminate(); SV.w = null } SV.busy = false; SV.info = '중단했습니다'; renderSolve() }
function svKeep(b, attr, fn) { // 누른 버튼이 화면에서 같은 높이에 머물도록 다시 그린 뒤 스크롤 보정
  const t = b.getBoundingClientRect().top, v = b.getAttribute(attr), d = b.dataset.d; fn();
  const nb = [...view.querySelectorAll('[' + attr + ']')].find(x => x.getAttribute(attr) === v && (d === undefined || x.dataset.d === d));
  if (nb) window.scrollTo(0, window.scrollY + nb.getBoundingClientRect().top - t);
}
function svBPanel() {
  const B = SV.bt, cfg = svCfg(B.mm); if (SV.bcfg !== cfg || !SV.bidx) { svIdx().then(() => { if (cur === 'solve') { const y = window.scrollY; renderSolve(); window.scrollTo(0, y) } }); }
  svPull();
  const idx = SV.bcfg === cfg && SV.bidx ? SV.bidx : { hands: {} }; const d = svDC(); const tot = svHands(B.n, svMainOf(B.mm)).length; const omn = svOptMain();
  const rows = Object.values(idx.hands).filter(e => (!B.sz || e.h.length === B.sz) && svHandOk(e.h)).map(e => { let b = -1; for (const [u, sc] of e.g) if (sc > b && svOkU(u ? u.split(',') : [], d)) b = sc; return { e, b } }).sort((a, b) => b.b - a.b || a.e.h.length - b.e.h.length);
  const nDone = Object.keys(idx.hands).length; const sup = Object.keys(svSup()).filter(n => !(DS.extra[n] > 0));
  return `<details class="svp svx svbx"${B.open ? ' open' : ''}><summary><b>일괄 계산</b> <small>저장된 손패 ${nDone}개 · 눌러서 ${B.open ? '접기' : '열기'}</small></summary>
<p class="svm svbh">지금 메인 덱으로 만들 수 있는 손패 조합을 차례로 전부 계산해 이 브라우저에 저장합니다. 엑스트라 덱은 고를 수 있는 카드를 모두 넣고 계산하므로, 나중에 엑스트라 덱 구성을 바꿔도 다시 계산하지 않습니다${sup.length ? ' (지금 덱에 없지만 같이 계산하는 카드: ' + esc(sup.map(svShort).join(', ')) + ')' : ''}. 위의 "쓰지 않을 카드" 설정은 그대로 따릅니다. 메인 덱을 "추가 카드 포함"으로 돌려 두면 혼·스팅·판 같은 추가 카드를 넣은 구성도 다시 계산하지 않습니다(종류마다 1장까지). 기본 카드의 장수나 쓰지 않을 카드를 바꾸면 따로 저장됩니다. 계산하는 동안 이 탭을 닫지 말아 주세요. 중단해도 끝난 것은 남고, 다시 시작하면 이어서 합니다.</p>
<div class="svbo"><label>메인 덱 <select id="svbmm"${B.run ? ' disabled' : ''}><option value="0"${B.mm ? '' : ' selected'}>지금 덱 그대로</option><option value="1"${B.mm ? ' selected' : ''}>추가 카드 ${omn.length}종 포함 (각 1장)</option></select></label><label>손패 장수 <select id="svbn"${B.run ? ' disabled' : ''}>${[1, 2, 3].map(v => `<option value="${v}"${B.n === v ? ' selected' : ''}>${v}장까지</option>`).join('')}</select></label><label>조합당 제한 <select id="svbl"${B.run ? ' disabled' : ''}>${[60, 180, 600, 86400].map(v => `<option value="${v}"${B.lim === v ? ' selected' : ''}>${v >= 86400 ? '무제한' : v / 60 + '분'}</option>`).join('')}</select></label><label>동시에 <select id="svbpar"${B.run ? ' disabled' : ''}>${[1, 2, 3, 4].map(v => `<option value="${v}"${B.par === v ? ' selected' : ''}>${v}개</option>`).join('')}</select></label>${B.run ? '<button class="btn" id="svbstop">중단</button>' : `<button class="btn pri" id="svbgo">일괄 계산 시작 (${tot}개)</button>`}</div>
${B.run ? `<p class="svm" id="svbp">${esc(svBProg())}</p>` : ''}
<div class="svbo svbe"><label>내보낼 범위 <select id="svbes">${[0, 1, 2, 3].map(v => `<option value="${v}"${(B.esz || 0) === v ? ' selected' : ''}>${v ? v + '장만' : '전체'}</option>`).join('')}</select></label><button class="btn" id="svbex">파일로 내보내기</button><button class="btn" id="svbim">파일에서 가져오기</button><button class="btn" id="svbcp">복사로 내보내기</button><button class="btn" id="svbpi">붙여넣어 가져오기</button><input type="file" id="svbf" accept=".gz,.json,application/gzip,application/json" hidden></div>${B.pin ? '<textarea id="svbta" class="svbta" placeholder="복사한 묶음을 여기에 붙여넣으세요"></textarea>' : ''}${B.msg ? `<p class="svm svbmsg">${esc(B.msg)}</p>` : ''}${SVSRV ? `<div class="svbo svbe">${svUpKey() ? '<button class="btn" id="svbup">서버에 올리기</button>' : ''}<span class="svm" id="svbs">${esc(B.smsg || (svUpKey() ? '이 브라우저는 계산 결과를 서버에 올릴 수 있습니다.' : '서버에 저장된 결과가 있으면 자동으로 받아옵니다.'))}</span></div>` : ''}
${nDone ? `<div class="svf"><div class="hr">${[0, 1, 2, 3].map(v => `<button data-bsz="${v}" class="${B.sz === v ? 'on' : ''}">${v ? v + '장' : '전체'}</button>`).join('')}</div></div><p class="svm">지금 엑스트라 덱으로 가능한 최대 방해 수 순서입니다. 누르면 그 손패의 결과를 엽니다.</p><div class="svbl">${rows.slice(0, B.shown).map(r => `<button class="svbr" data-bh="${esc(JSON.stringify(r.e.h))}"><span class="svs">${r.b < 0 ? '없음' : '방해 ' + r.b}</span><b>${esc(r.e.h.map(svShort).join(' + '))}</b>${r.e.c ? '' : '<i>제한에 걸림</i>'}</button>`).join('')}</div>${rows.length > B.shown ? `<button class="btn svmore" id="svbmore">더 보기 (${rows.length - B.shown}개 남음)</button>` : ''}` : ''}</details>`;
}
function renderSolve() {
  const N = DTE.N, C = DTE.C;
  const pool = Object.keys(DS.main).filter(n => DS.main[n] > 0 && DTE.CODE[n] && C[DTE.CODE[n]].k !== 'x'); pool.push(N.X);
  SV.hand = SV.hand.filter(n => pool.includes(n));
  const cnt = n => SV.hand.filter(x => x === n).length;
  const extraNames = Object.keys(DS.extra).filter(n => DS.extra[n] > 0);
  const unk = Object.keys(DS.main).filter(n => DS.main[n] > 0 && !DTE.CODE[n] && !(CU.gen || []).includes(n)).concat(extraNames.filter(n => !DTE.CODE[n]));
  const exPool = (CU.pool.extra || []).slice().sort((a, b) => (DTE.CODE[b] ? 1 : 0) - (DTE.CODE[a] ? 1 : 0)); const exTot = Object.values(DS.extra).reduce((a, b) => a + b, 0);
  const mnPool = (CU.pool.main || []).filter(n => DTE.CODE[n]); const mnTot = mnPool.reduce((a, n) => a + (DS.main[n] || 0), 0);
  const HG = { dt: ['MU', 'LU', 'FA', 'UR', 'PA', 'KE', 'RA', 'FL', 'HO', 'ST'], br: ['AZ', 'WD', 'SHR', 'EC', 'CA', 'QU', 'ALU', 'BF', 'FV', 'NAD', 'SPI', 'OPN', 'RED', 'RET'], etc: ['X'] };
  const XB = ['낙인룡 알비온', '빙검룡 미라제이드', '진염룡 알비온', '회신룡 배스터드', '검은 용의 에클레시아', '혁언룡 그랑기뇰', '심연룡 알버 레나투스', '격철룡 린드블룸', '성흔을 먹는 용', '신염룡 루벨리온', '데스피아안 루루와릴리스'];
  const KN = { all: '전체', dt: '드테 기믹만', brand: '낙인 기믹만', mix: '합쳐진 것' }, SN = { score: '방해 수', hand: '남는 패', steps: '짧은 수순', field: '필드 몬스터 수' };
  const fnames = [...new Set((SV.res || []).flatMap(r => r.field))].sort();
  SV.nof = SV.nof.filter(n => fnames.includes(n));
  let list = (SV.res || []).filter(r => SV.flt === 'all' || r.kind === SV.flt).filter(r => !r.field.some(n => SV.nof.includes(n)));
  const cmp = { score: (a, b) => b.score - a.score || b.hand - a.hand || a.nsteps - b.nsteps, hand: (a, b) => b.hand - a.hand || b.score - a.score, steps: (a, b) => a.nsteps - b.nsteps || b.score - a.score, field: (a, b) => b.field.length - a.field.length || b.score - a.score }[SV.sort];
  list = list.slice().sort(cmp); if (SV.sort === 'steps') list = list.filter(r => r.score > 0);
  const found = svStore();
  const card = (r, i) => {
    const open = SV.open === r.key;
    return `<div class="svr${open ? ' on' : ''}"><button class="svh" data-k="${esc(r.key)}"><span class="svs">방해 ${r.score}</span><span class="svk svk-${r.kind}">${{ dt: '드테', brand: '낙인', mix: '혼합' }[r.kind]}</span><b>${hl(r.field.join(' · ') || '필드 없음')}</b>${r.set.length ? `<i>세트: ${hl(r.set.join(' · '))}</i>` : ''}<i>패 ${r.hand}장${r.handCards.length ? ': ' + hl(r.handCards.join(' · ')) : ''}</i><i>묘지 ${r.final.gy.length}장${r.final.gy.length ? ': ' + [['몬스터', c => DTE.C[c].k === 'm'], ['엑스트라 덱 몬스터', c => DTE.C[c].k === 'x'], ['마법·함정', c => DTE.C[c].k === 's' || DTE.C[c].k === 't']].map(([t, f]) => { const a = r.final.gy.filter(f); return a.length ? t + ' ' + hl(a.map(c => DTE.N[c]).join(' · ')) : '' }).filter(Boolean).join(' / ') : ''}</i>${r.final.ban.length ? `<i>제외: ${hl(r.final.ban.map(c => DTE.N[c]).join(' · '))}</i>` : ''}<i>${r.nsteps}단계</i></button>
${open ? `<div class="svb"><h5>상대 턴 방해</h5>${r.items.length ? r.items.map(it => `<div class="svi"><b>${hl(it[0])}</b><em>${esc(it[1])}</em><span>${hl(it[2])}</span></div>`).join('') : '<p class="svm">없음</p>'}
<h5>수순</h5><ol class="svst">${r.steps.concat(r.end).map(s => `<li><b>${hl(s.title)}</b>${s.act ? ` <i>(${hl(s.act)})</i>` : ''}${s.desc ? `<span>${hl(s.desc)}</span>` : ''}</li>`).join('')}</ol>
<div class="sva"><button class="btn pri" data-add="${i}">전개법에 추가하고 보기</button></div></div>` : ''}</div>`;
  };
  view.innerHTML = `<div class="hd"><b>전개 탐색</b><span>손패를 고르고 탐색을 누르면, 지금 덱 리스트로 선공 1턴에 만들 수 있는 최종 필드를 찾아 줍니다. 이 컴퓨터에서 계산합니다. 상대의 방해가 없다고 가정합니다.</span></div>
<div class="svp"><h4 class="svhh"><span>손패 <small>${SV.hand.length}장 선택 · 최대 5장</small></span><button class="rst3" id="svrh"${SV.hand.length ? '' : ' disabled'}>초기화</button></h4>${[['드래곤테일 카드', HG.dt], ['낙인 카드', HG.br], ['그 외', HG.etc]].map(([t, order]) => { const ns = order.map(c => N[c]).filter(n => pool.includes(n)); return ns.length ? `<h5 class="svg">${t}</h5><div class="svhand">${ns.map(n => { const c = cnt(n), mx = n === N.X ? 3 : DS.main[n]; return `<div class="svc${c ? ' on' : ''}"><span>${esc(svShort(n))}</span><span class="bq"><button class="bqm" data-h="${esc(n)}" data-d="-1"${c ? '' : ' disabled'}>−</button><b>${c}</b><button class="bqm" data-h="${esc(n)}" data-d="1"${c >= mx || SV.hand.length >= 5 ? ' disabled' : ''}>+</button></span></div>` }).join('')}</div>` : '' }).join('')}

${unk.length ? `<p class="svm">탐색기가 아직 모르는 카드(있어도 쓰지 않음): ${esc(unk.join(', '))}</p>` : ''}</div>
<details class="svp svx svmn"${SV.mopen ? ' open' : ''}><summary><b>메인 덱 카드</b> <small>전개 카드 ${mnTot}장 · 눌러서 ${SV.mopen ? '접기' : '고르기'} · 덱 리스트 탭과 같이 바뀝니다</small></summary><div class="svxr"><button class="rst3" id="svrm">기본 구성으로 초기화</button></div>${[['드래곤테일 카드', HG.dt], ['낙인 카드', HG.br]].map(([t, order]) => { const ns = order.map(c => N[c]).filter(n => mnPool.includes(n)); return ns.length ? `<h5 class="svg">${t}</h5><div class="svhand">${ns.map(n => { const c = DS.main[n] || 0; return `<div class="svc${c ? ' on' : ''}"><span>${esc(svShort(n))}</span><span class="bq"><button class="bqm" data-m="${esc(n)}" data-d="-1"${c ? '' : ' disabled'}>−</button><b>${c}</b><button class="bqm" data-m="${esc(n)}" data-d="1"${c >= 3 ? ' disabled' : ''}>+</button></span></div>` }).join('')}</div>` : '' }).join('')}</details>
<details class="svp svx svex"${SV.xopen ? ' open' : ''}><summary><b>엑스트라 덱</b> <small>${exTot}장 / 15장 · 눌러서 ${SV.xopen ? '접기' : '고르기'} · 덱 리스트 탭과 같이 바뀝니다</small></summary><div class="svxr"><button class="rst3" id="svrx">기본 구성으로 초기화</button></div>${[['드래곤테일', n => /드래곤테일/.test(n)], ['낙인', n => XB.includes(n)], ['그 외', n => !/드래곤테일/.test(n) && !XB.includes(n)]].map(([t, f]) => { const ns = exPool.filter(f); return ns.length ? `<h5 class="svg">${t}</h5><div class="svhand">${ns.map(n => { const c = DS.extra[n] || 0, known = !!DTE.CODE[n]; return `<div class="svc${c ? ' on' : ''}${known ? '' : ' unk'}"><span>${esc(svShort(n))}${known ? '' : ' <i>(모름)</i>'}</span><span class="bq"><button class="bqm" data-x="${esc(n)}" data-d="-1"${c ? '' : ' disabled'}>−</button><b>${c}</b><button class="bqm" data-x="${esc(n)}" data-d="1"${c >= 3 || exTot >= 15 ? ' disabled' : ''}>+</button></span></div>` }).join('')}</div>` : '' }).join('')}</details>
<details class="svp svx svbn"${SV.bopen ? ' open' : ''}><summary><b>쓰지 않을 카드</b> <small>안 씀 ${SV.ban.length}장 · 비용만 ${SV.nos.length}장 · 눌러서 ${SV.bopen ? '접기' : '고르기'}</small></summary><p class="svm svbh"><b>안 씀</b>: 내 턴 전개에 쓰지 않습니다. 상대 턴 방해 계산에는 넣습니다. <b>비용만</b>(엑스트라 덱 카드): 내 턴에 소환하지 않고, 엑스트라 덱에서 묘지로 보내는 비용으로만 씁니다.</p><div class="svxr"><button class="rst3" id="svrb"${SV.ban.length || SV.nos.length ? '' : ' disabled'}>초기화</button></div>${(() => { const mn = Object.keys(DS.main).filter(n => DS.main[n] > 0 && DTE.CODE[n]), ex = Object.keys(svSup()); const dtO = HG.dt.map(c => N[c]), brO = HG.br.map(c => N[c]);
  const secs = [['메인 덱 · 드래곤테일 카드', dtO.filter(n => mn.includes(n))], ['메인 덱 · 낙인 카드', brO.filter(n => mn.includes(n))], ['엑스트라 덱 · 드래곤테일', ex.filter(n => /드래곤테일/.test(n))], ['엑스트라 덱 · 낙인', ex.filter(n => XB.includes(n))], ['엑스트라 덱 · 그 외', ex.filter(n => !/드래곤테일/.test(n) && !XB.includes(n))]];
  return secs.map(([t, ns]) => ns.length ? `<h5 class="svg">${t}</h5><div class="svhand">${ns.map(n => { const on = SV.ban.includes(n), co = SV.nos.includes(n); return `<button class="svc svbt${on ? ' off' : co ? ' cost' : ''}" data-ban="${esc(n)}"><span>${esc(svShort(n))}</span><em>${on ? '안 씀' : co ? '비용만' : '사용'}</em></button>` }).join('')}</div>` : '').join('') })()}</details>
${svBPanel()}
${SV.info ? `<p class="svinfo">${esc(SV.info)}${SV.cached ? ' <button class="rst3" id="svre">다시 계산</button>' : ''}</p>` : ''}
${SV.res ? `<div class="svf"><div class="hr">${Object.keys(KN).map(k => `<button data-f="${k}" class="${SV.flt === k ? 'on' : ''}">${KN[k]} ${k === 'all' ? SV.res.length : SV.res.filter(r => r.kind === k).length}</button>`).join('')}</div><div class="hr">${Object.keys(SN).map(k => `<button data-s="${k}" class="${SV.sort === k ? 'on' : ''}">${SN[k]} 순</button>`).join('')}</div></div>
${fnames.length ? `<div class="svnf"><span>최종 필드에 남기지 않을 카드</span><div class="svtg">${fnames.map(n => `<button data-nof="${esc(n)}" class="${SV.nof.includes(n) ? 'on' : ''}">${esc(svShort(n))}</button>`).join('')}</div></div>` : ''}
<div class="svl">${list.length ? list.slice(0, SV.shown).map(card).join('') : '<p class="svm">조건에 맞는 결과가 없습니다.</p>'}</div>${list.length > SV.shown ? `<button class="btn svmore" id="svmore">더 보기 (${list.length - SV.shown}개 남음)</button>` : ''}` : ''}
${found.length ? `<div class="svp"><h4>전개법에 추가한 탐색 결과 <small>${found.length}개 · 이 브라우저에 저장됨</small></h4>${found.map(f => `<div class="svfd"><span><b>${esc(f.group)}</b> ${esc(f.label)}</span><span><button class="btn" data-go="${f.combo.id}">보기</button><button class="btn" data-del="${f.combo.id}">삭제</button></span></div>`).join('')}</div>` : ''}
<div class="foot svfoot"><div class="svfh">${SV.hand.length ? '손패 ' + SV.hand.length + '장: ' + esc(SV.hand.map(svShort).join(' + ')) : '손패를 골라 주세요'}</div><div class="svgo"><label>시간 제한 <select id="svlim">${[20, 60, 180, 600, 0].map(v => `<option value="${v}"${SV.lim === v ? ' selected' : ''}>${v === 0 ? '무제한' : v < 60 ? v + '초' : v / 60 + '분'}</option>`).join('')}</select></label>${SV.busy ? `<button class="btn" id="svstop">중단</button><span class="svm" id="svprog">${esc(SV.prog)}</span>` : `<button class="btn pri" id="svrun"${SV.hand.length ? '' : ' disabled'}>탐색</button>`}</div></div>`;
  view.querySelectorAll('[data-h]').forEach(b => b.onclick = () => svKeep(b, 'data-h', () => { const n = b.dataset.h; if (+b.dataset.d > 0) SV.hand.push(n); else { const i = SV.hand.lastIndexOf(n); if (i >= 0) SV.hand.splice(i, 1) } renderSolve() }));
  view.querySelectorAll('[data-x]').forEach(b => b.onclick = () => svKeep(b, 'data-x', () => { const n = b.dataset.x; DS.extra[n] = Math.max(0, Math.min(3, (DS.extra[n] || 0) + +b.dataset.d)); SV.xopen = true; cuSave(); cuSync(); draw() }));
  const xd = view.querySelector('.svex'); if (xd) xd.ontoggle = () => { SV.xopen = xd.open };
  const rh = document.getElementById('svrh'); if (rh) rh.onclick = () => { SV.hand = []; SV.res = null; SV.info = ''; SV.open = null; renderSolve() };
  const rx = document.getElementById('svrx'); if (rx) rx.onclick = () => { DS.extra = Object.fromEntries(CU.base.extra); SV.xopen = true; cuSave(); cuSync(); const y = window.scrollY; draw(); window.scrollTo(0, y) };
  view.querySelectorAll('[data-ban]').forEach(b => b.onclick = () => svKeep(b, 'data-ban', () => { const n = b.dataset.ban; const i = SV.ban.indexOf(n), j = SV.nos.indexOf(n), isX = DTE.C[DTE.CODE[n]].k === 'x'; if (i >= 0) SV.ban.splice(i, 1); else if (j >= 0) { SV.nos.splice(j, 1); SV.ban.push(n) } else if (isX) SV.nos.push(n); else SV.ban.push(n); SV.bopen = true; try { localStorage.setItem(SVBK, JSON.stringify(SV.ban)); localStorage.setItem(SVNK, JSON.stringify(SV.nos)) } catch (e) { } renderSolve() }));
  const rb = document.getElementById('svrb'); if (rb) rb.onclick = () => { SV.ban = []; SV.nos = []; SV.bopen = true; try { localStorage.setItem(SVBK, '[]'); localStorage.setItem(SVNK, '[]') } catch (e) { } renderSolve() };
  const bd = view.querySelector('.svbn'); if (bd) bd.ontoggle = () => { SV.bopen = bd.open };
  view.querySelectorAll('[data-nof]').forEach(b => b.onclick = () => { const n = b.dataset.nof; const i = SV.nof.indexOf(n); if (i >= 0) SV.nof.splice(i, 1); else SV.nof.push(n); SV.shown = 30; const y = window.scrollY; renderSolve(); window.scrollTo(0, y) });
  view.querySelectorAll('[data-m]').forEach(b => b.onclick = () => svKeep(b, 'data-m', () => { const n = b.dataset.m; DS.main[n] = Math.max(0, Math.min(3, (DS.main[n] || 0) + +b.dataset.d)); SV.mopen = true; cuSave(); cuSync(); draw() }));
  const rm2 = document.getElementById('svrm'); if (rm2) rm2.onclick = () => { const bm = Object.fromEntries(CU.base.main); for (const n of mnPool) DS.main[n] = bm[n] || 0; SV.mopen = true; cuSave(); cuSync(); const y = window.scrollY; draw(); window.scrollTo(0, y) };
  const md = view.querySelector('.svmn'); if (md) md.ontoggle = () => { SV.mopen = md.open };
  const lim = document.getElementById('svlim'); if (lim) lim.onchange = () => { SV.lim = +lim.value };
  const run = document.getElementById('svrun'); if (run) run.onclick = () => svRun(); const re = document.getElementById('svre'); if (re) re.onclick = () => svRun(true); const stp = document.getElementById('svstop'); if (stp) stp.onclick = svStop;
  view.querySelectorAll('[data-f]').forEach(b => b.onclick = () => { SV.flt = b.dataset.f; SV.shown = 30; renderSolve() });
  view.querySelectorAll('[data-s]').forEach(b => b.onclick = () => { SV.sort = b.dataset.s; SV.shown = 30; renderSolve() });
  view.querySelectorAll('.svh').forEach(b => b.onclick = () => { SV.open = SV.open === b.dataset.k ? null : b.dataset.k; const y = window.scrollY; renderSolve(); window.scrollTo(0, y) });
  view.querySelectorAll('[data-add]').forEach(b => b.onclick = () => { const id = svAdd(list[+b.dataset.add]); if (cuOk(id)) go(dk + '/' + id); else { SV.info = '추가했습니다. 지금 덱 구성으로는 필요한 카드가 모자라 전개법에 표시되지 않습니다.'; renderSolve() } });
  view.querySelectorAll('[data-go]').forEach(b => b.onclick = () => go(dk + '/' + b.dataset.go));
  view.querySelectorAll('[data-del]').forEach(b => b.onclick = () => { svRemove(b.dataset.del); cuSync(); draw() });
  const more = document.getElementById('svmore'); if (more) more.onclick = () => { SV.shown += 30; const y = window.scrollY; renderSolve(); window.scrollTo(0, y) };
  view.querySelectorAll('.svf .hr').forEach(hscroll);
  const B = SV.bt, bx = view.querySelector('.svbx'); if (bx) bx.ontoggle = () => { B.open = bx.open };
  const keepY = fn => { const y = window.scrollY; fn(); renderSolve(); window.scrollTo(0, y) };
  for (const [id, k] of [['svbmm', 'mm'], ['svbn', 'n'], ['svbl', 'lim'], ['svbpar', 'par']]) { const e = document.getElementById(id); if (e) e.onchange = () => keepY(() => { B[k] = +e.value; B.open = true }) }
  const bgo = document.getElementById('svbgo'); if (bgo) bgo.onclick = () => { B.open = true; svQueue([B.mm ? 1 : 0]) }; const bst = document.getElementById('svbstop'); if (bst) bst.onclick = () => B.stop && B.stop();
  view.querySelectorAll('[data-bsz]').forEach(b => b.onclick = () => keepY(() => { B.sz = +b.dataset.bsz; B.shown = 60; B.open = true }));
  const bes = document.getElementById('svbes'); if (bes) bes.onchange = () => { B.esz = +bes.value };
  const bex = document.getElementById('svbex'); if (bex) bex.onclick = () => { B.open = true; svExport(B.esz || 0) };
  const bim = document.getElementById('svbim'), bf = document.getElementById('svbf'); if (bim && bf) { bim.onclick = () => bf.click(); bf.onchange = () => { if (bf.files[0]) svImport(bf.files[0]) } }
  const bcp = document.getElementById('svbcp'); if (bcp) bcp.onclick = () => { B.open = true; svCopyOut(B.esz || 0) };
  const bpi = document.getElementById('svbpi'); if (bpi) bpi.onclick = () => keepY(() => { B.pin = !B.pin; B.open = true });
  const bta = document.getElementById('svbta'); if (bta) { bta.focus({ preventScroll: true }); bta.onpaste = ev => { const t = (ev.clipboardData || window.clipboardData).getData('text'); ev.preventDefault(); bta.value = '불러오는 중…'; svPasteIn(t) } }
  const bup = document.getElementById('svbup'); if (bup) bup.onclick = () => { B.open = true; svPush(false) };
  const bm = document.getElementById('svbmore'); if (bm) bm.onclick = () => keepY(() => { B.shown += 60; B.open = true });
  view.querySelectorAll('[data-bh]').forEach(b => b.onclick = async () => { SV.hand = JSON.parse(b.dataset.bh); SV.res = null; B.open = false; await svRun(); const l = view.querySelector('.svinfo'); if (l) l.scrollIntoView({ block: 'start' }) });
}
