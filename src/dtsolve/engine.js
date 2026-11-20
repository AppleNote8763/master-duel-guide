// 드래곤테일 낙인 선공 1턴 탐색 엔진 (상대 필드·묘지는 비어 있다고 가정)
// 브라우저(Web Worker)와 Node 양쪽에서 같은 코드로 돌아감
(function (root) {
'use strict';
const N = {
  MU: '드래곤테일 무루루', LU: '드래곤테일 루키아스', FA: '드래곤테일 파이메나', UR: '드래곤테일 우르굴라', PA: '드래곤테일 판',
  KE: '케투 드래곤테일', RA: '라후 드래곤테일', FL: '드래곤테일 플레임', HO: '드래곤테일 혼', ST: '드래곤테일 스팅',
  AZ: '알버스의 낙윤', WD: '하얀 용의 낙윤', EC: '순백의 성녀 에클레시아', CA: '혁의 성녀 카르테시아', BF: '낙인융합', FV: 'The Fallen & The Virtuous',
  ART: '드래곤테일 알자리온', GUL: '드래곤테일 그라멜', SEC: '사크라멘툼 드라군', ANA: '프레데터 플랜츠 베르테 아나콘다', EDD: '검은 용의 에클레시아',
  ALB: '낙인룡 알비온', MJ: '빙검룡 미라제이드', SAN: '진염룡 알비온', MIX: '혼효하는 믹시아', TIT: '회신룡 배스터드', AEON: '초월소환수 아이온',
  LEN: '심연룡 알버 레나투스', DEV: '성흔을 먹는 용', RIN: '격철룡 린드블룸',
  RET: '낙인단죄', SHR: '흑의룡 알비온', OPN: '낙인개막', ALU: '데스피아의 도화 알베르', RED: '혁의 낙인', LUW: '데스피아안 루루와릴리스', LUB: '신염룡 루벨리온', KHA: '공극의 원성룡',
  NAD: '천저의 사도', SPI: '낙인의 기염', QU: '인도하는 성녀 쿠엠', GRG: '혁언룡 그랑기뇰',
  X: '패의 아무 몬스터',
};
const CODE = {}; for (const k in N) CODE[N[k]] = k;
// r: 종족(D 드래곤 / S 마법사 / W 환룡 / O 기타), a: 속성, lv, dt: 드래곤테일, al: 알버스의 낙윤 취급, men: 알버스의 낙윤이 적힌 카드
const C = {
  MU: { k: 'm', r: 'D', a: 'DARK', lv: 3, dt: 1, atk: 1100 }, LU: { k: 'm', r: 'S', a: 'EARTH', lv: 4, dt: 1, atk: 1800 },
  FA: { k: 'm', r: 'S', a: 'WATER', lv: 5, dt: 1, atk: 1300 }, UR: { k: 'm', r: 'D', a: 'FIRE', lv: 6, dt: 1, atk: 2400 }, PA: { k: 'm', r: 'D', a: 'WIND', lv: 7, dt: 1, atk: 2700 },
  AZ: { k: 'm', r: 'D', a: 'DARK', lv: 4, al: 1, atk: 1800 }, WD: { k: 'm', r: 'D', a: 'DARK', lv: 4, al: 1, atk: 1800 },
  EC: { k: 'm', r: 'S', a: 'LIGHT', lv: 4, tun: 1, men: 1, atk: 1500 }, CA: { k: 'm', r: 'S', a: 'LIGHT', lv: 4, tun: 1, men: 1, atk: 1500 },
  QU: { k: 'm', r: 'S', a: 'LIGHT', lv: 4, tun: 1, men: 1, atk: 1500 },
  X: { k: 'm', r: 'O', a: '?', lv: 0, gen: 1, atk: 0 },
  NAD: { k: 's' }, SPI: { k: 's', br: 1 }, RET: { k: 't', br: 1 }, OPN: { k: 's', br: 1 }, RED: { k: 's', br: 1 },
  SHR: { k: 'm', r: 'D', a: 'DARK', lv: 8, al2: 1, atk: 2500 }, ALU: { k: 'm', r: 'F', a: 'DARK', lv: 4, atk: 1800 },
  LUW: { k: 'x', x: 'synchro', r: 'S', a: 'LIGHT', lv: 12, atk: 2500 }, LUB: { k: 'x', x: 'fusion', r: 'D', a: 'LIGHT', lv: 8, men: 1, atk: 2500 }, KHA: { k: 'x', x: 'fusion', r: 'D', a: 'LIGHT', lv: 8, atk: 2500, sp: 1 },
  GRG: { k: 'x', x: 'fusion', r: 'S', a: 'LIGHT', lv: 8, atk: 2500, sp: 1 },
  LEN: { k: 'x', x: 'fusion', r: 'D', a: 'DARK', lv: 8, men: 1, atk: 2500, nomat: 1, sp: 1 }, DEV: { k: 'x', x: 'fusion', r: 'B', a: 'DARK', lv: 8, men: 1, atk: 3000 }, RIN: { k: 'x', x: 'fusion', r: 'WB', a: 'DARK', lv: 8, men: 1, atk: 2500 },
  KE: { k: 's', dts: 1 }, RA: { k: 's', dts: 1 }, FL: { k: 't', dts: 1 }, HO: { k: 't', dts: 1 }, ST: { k: 't', dts: 1 }, BF: { k: 's', br: 1 }, FV: { k: 's', br: 1 },
  ART: { k: 'x', x: 'fusion', r: 'D', a: 'EARTH', lv: 8, dt: 1, atk: 3000, sp: 1 }, GUL: { k: 'x', x: 'fusion', r: 'S', a: 'WATER', lv: 7, dt: 1, atk: 2800 },
  SEC: { k: 'x', x: 'fusion', r: 'D', a: 'LIGHT', lv: 8, atk: 3000 }, ANA: { k: 'x', x: 'link', r: 'O', a: 'DARK', lv: 0, atk: 500 },
  EDD: { k: 'x', x: 'synchro', r: 'S', a: 'LIGHT', lv: 8, men: 1, atk: 2500 }, ALB: { k: 'x', x: 'fusion', r: 'D', a: 'DARK', lv: 8, men: 1, atk: 2500, sp: 1 },
  MJ: { k: 'x', x: 'fusion', r: 'W', a: 'DARK', lv: 8, men: 1, atk: 3000 }, SAN: { k: 'x', x: 'fusion', r: 'D', a: 'LIGHT', lv: 8, men: 1, atk: 3000, nomat: 1, sp: 1 },
  MIX: { k: 'x', x: 'fusion', r: 'S', a: 'DARK', lv: 8, atk: 2700 }, TIT: { k: 'x', x: 'fusion', r: 'D', a: 'DARK', lv: 8, men: 1, atk: 2500, sp: 1 },
  AEON: { k: 'x', x: 'fusion', r: 'O', a: 'DARK', lv: 10, atk: 3800 },
};
const DTST = ['RA', 'KE', 'FL', 'HO', 'ST'];
const MZ = ['M3', 'M2', 'M4', 'M1', 'M5'], SZ = ['S1', 'S2', 'S3', 'S4', 'S5'];
const isMon = c => C[c].k === 'm' || C[c].k === 'x';
const AL = c => !!(C[c].al || C[c].al2); // 필드·묘지에서 알버스의 낙윤으로 취급
const alp = (c, p) => !!(c.al || (c.al2 && (p.from === 'field' || p.from === 'gy')));

// ---------- 상태 ----------
// hand: [code], deck: {code:n}, extra: {code:n}, field: [{c,z}], st: [{c,z}], gy: [code], ban: [code]
// used: 정렬된 문자열 배열, lockF, lock8, noSS, ns, nfx(융합 이외를 엑스트라에서 특소함), fgy(융합 몬스터가 묘지로 감), albgy, titgy, eddb, pend: [..]
function clone(s) {
  return { hand: s.hand.slice(), deck: Object.assign({}, s.deck), extra: Object.assign({}, s.extra), field: s.field.map(m => ({ c: m.c, z: m.z })), st: s.st.map(m => ({ c: m.c, z: m.z })),
    gy: s.gy.slice(), ban: s.ban.slice(), used: s.used.slice(), lockF: s.lockF, lock8: s.lock8, noSS: s.noSS, noEX: s.noEX, ns: s.ns, nfx: s.nfx, fgy: s.fgy, albgy: s.albgy, titgy: s.titgy, eddb: s.eddb, pend: s.pend.map(p => Object.assign({}, p)) };
}
function hkey(s) { // 53비트 해시 (문자열 키를 그대로 들고 있으면 메모리가 큼)
  const k = key(s); let h1 = 0x811c9dc5, h2 = 0x1b873593;
  for (let i = 0; i < k.length; i++) { const ch = k.charCodeAt(i); h1 = Math.imul(h1 ^ ch, 16777619); h2 = Math.imul(h2 ^ ch, 0x5bd1e995) ^ (h2 >>> 13); }
  return ((h1 >>> 0) & 0x1fffff) * 4294967296 + (h2 >>> 0);
}
function key(s) {
  const d = Object.keys(s.deck).filter(k => s.deck[k] > 0).sort().map(k => k + s.deck[k]).join(',');
  const e = Object.keys(s.extra).filter(k => s.extra[k] > 0).sort().map(k => k + s.extra[k]).join(',');
  return [s.hand.slice().sort().join(','), d, e, s.field.map(m => m.c).sort().join(','), s.st.map(m => m.c).sort().join(','), s.gy.slice().sort().join(','), s.ban.slice().sort().join(','), s.used.join(','),
    (s.lockF ? 'F' : '') + (s.lock8 ? '8' : '') + (s.noSS ? 'N' : '') + (s.noEX ? 'X' : '') + (s.ns ? 'n' : '') + (s.nfx ? 'x' : '') + (s.fgy ? 'g' : '') + (s.albgy ? 'a' : '') + (s.titgy ? 't' : '') + (s.eddb ? 'e' : ''),
    s.pend.map(p => p.t + (p.by || '') + (p.n || '')).join(',')].join('|');
}
const has = (s, f) => s.used.indexOf(f) >= 0;
function use(s, f) { if (!has(s, f)) { s.used.push(f); s.used.sort(); } }
function rm(arr, c) { const i = arr.indexOf(c); if (i < 0) throw new Error('rm ' + c); arr.splice(i, 1); }
function freeM(s, forLink) {
  if (forLink) return s.field.some(m => m.z === 'ER') ? null : 'ER';
  for (const z of MZ) if (!s.field.some(m => m.z === z)) return z;
  return null;
}
function freeX(s) { // 엑스트라 덱 몬스터(링크 제외): 메인 존 우선, 없으면 엑스트라 몬스터 존
  const z = freeM(s); if (z) return z; return s.field.some(m => m.z === 'ER') ? null : 'ER';
}
function freeS(s) { for (const z of SZ) if (!s.st.some(m => m.z === z)) return z; return null; }
function canExtra(s, c) {
  if (s.noSS || s.noEX || NOSS[c]) return false; const x = C[c].x;
  if (s.lockF && x !== 'fusion') return false;
  if (s.lock8 && !((x === 'fusion' || x === 'synchro') && C[c].lv === 8)) return false;
  return (s.extra[c] || 0) > 0;
}
function toGY(s, c) { // 몬스터 1장이 묘지로
  s.gy.push(c); if (C[c].x === 'fusion') s.fgy = true; if (c === 'ALB') s.albgy = true; if (c === 'TIT') s.titgy = true;
}

// ---------- 융합 소재 열거 ----------
// src: {hand, field, deck, gy}. 반환: [{t, mats:[{c,from}], hm(패 소재 수)}]
function pools(s, src, exclHandIdx) {
  const P = [];
  if (src.hand) { const seen = {}; s.hand.forEach((c, i) => { if (i === exclHandIdx) return; if (!isMon(c)) return; P.push({ c, from: 'hand', i }); }); }
  if (src.field) s.field.forEach((m, i) => { if (C[m.c].nomat) return; P.push({ c: m.c, from: 'field', i }); });
  if (src.deck) for (const c in s.deck) if (s.deck[c] > 0 && C[c].k === 'm') P.push({ c, from: 'deck', i: 0 });
  if (src.gy) { const seen = {}; s.gy.forEach((c, i) => { if (!isMon(c) || seen[c] || C[c].nomat) return; seen[c] = 1; P.push({ c, from: 'gy', i }); }); }
  if (src.ban) { const seen = {}; s.ban.forEach((c, i) => { if (!isMon(c) || seen[c] || C[c].nomat) return; seen[c] = 1; P.push({ c, from: 'ban', i }); }); }
  return P;
}
function fusionChoices(s, src, targets, exclHandIdx) {
  const P = pools(s, src, exclHandIdx), out = [], seen = {};
  const add = (t, mats) => {
    const k = t + ':' + mats.map(m => m.c + '@' + m.from).sort().join('+'); if (seen[k]) return; seen[k] = 1;
    out.push({ t, mats, hm: mats.filter(m => m.from === 'hand').length });
  };
  const two = (t, fa, fb) => { for (const a of P) { if (C[a.c].gen || !fa(C[a.c], a)) continue; for (const b of P) { if (b === a || C[b.c].gen || !fb(C[b.c], b)) continue; if (a.from === 'deck' && b.from === 'deck' && a.c === b.c && s.deck[a.c] < 2) continue; add(t, [a, b]); } } };
  for (const t of targets) {
    if (!canExtra(s, t)) continue;
    if (!(C[t].x === 'synchro' || C[t].x === 'link') && !freeX(s) && !P.some(p => p.from === 'field')) continue;
    if (t === 'ART' || t === 'GUL') {
      const H = P.filter(p => p.from === 'hand');
      for (const a of P) {
        if (!C[a.c].dt) continue;
        for (let i = 0; i < H.length; i++) {
          if (H[i] === a) continue; add(t, [a, H[i]]);
          if (t === 'ART') for (let j = i + 1; j < H.length; j++) { if (H[j] === a) continue; add(t, [a, H[i], H[j]]); }
        }
      }
    } else if (t === 'SEC') two(t, c => c.r === 'D', c => c.r === 'S');
    else if (t === 'ALB') two(t, alp, c => c.a === 'LIGHT');
    else if (t === 'MJ') two(t, alp, c => c.k === 'x');
    else if (t === 'SAN') two(t, alp, c => c.a === 'LIGHT' && c.r === 'S');
    else if (t === 'TIT') two(t, alp, c => c.atk >= 2500);
    else if (t === 'LUB') two(t, alp, c => c.a === 'DARK');
    else if (t === 'KHA') two(t, c => c.r === 'D' && (c.a === 'LIGHT' || c.a === 'DARK'), c => c.r === 'D');
    else if (t === 'MIX') two(t, c => c.r === 'S', c => c.r !== 'S');
    else if (t === 'GRG') two(t, (c, p) => p.c === 'CA', c => c.a === 'LIGHT' || c.a === 'DARK');
  }
  return out;
}
// 융합 실행: 소재를 묘지(또는 제외)로 보내고 융합 몬스터를 놓음. 유발 효과는 pend에 쌓음
function doFusion(s, ch, banish) {
  const idxH = ch.mats.filter(m => m.from === 'hand').map(m => m.i).sort((a, b) => b - a);
  const idxF = ch.mats.filter(m => m.from === 'field').map(m => m.i).sort((a, b) => b - a);
  for (const i of idxH) s.hand.splice(i, 1);
  for (const i of idxF) s.field.splice(i, 1);
  for (const m of ch.mats) {
    if (m.from === 'deck') s.deck[m.c]--;
    if (m.from === 'gy') rm(s.gy, m.c);
    if (m.from === 'ban') rm(s.ban, m.c);
    if (banish === 'deck') { if (C[m.c].k === 'x') s.extra[m.c] = (s.extra[m.c] || 0) + 1; else if (!C[m.c].gen) s.deck[m.c] = (s.deck[m.c] || 0) + 1; }
    else if (banish) s.ban.push(m.c); else toGY(s, m.c);
  }
  s.extra[ch.t]--; s.field.push({ c: ch.t, z: freeX(s) });
  if (!banish) for (const m of ch.mats) if (C[m.c].dt && C[m.c].k === 'm' && !has(s, m.c + 'S') && !s.pend.some(p => p.t === 'set' && p.by === m.c)) s.pend.push({ t: 'set', by: m.c });
  if (ch.t === 'ART' && !has(s, 'ART1') && ch.hm > 0) s.pend.push({ t: 'ret', n: ch.hm });
  if (ch.t === 'ALB' && !has(s, 'ALB1')) s.pend.push({ t: 'alb' });
  if (ch.t === 'GRG' && !has(s, 'GRG1')) s.pend.push({ t: 'grg' });
  if (ch.t === 'LUB' && !has(s, 'LUB1') && s.hand.length) s.pend.push({ t: 'lub' });
}
function matText(ch) { return ch.mats.map(m => N[m.c] + '(' + ({ hand: '패', field: '필드', deck: '덱', gy: '묘지', ban: '제외' })[m.from] + ')').join(' + '); }
function onSummon(s, c) { // 일반·특수 소환 시 유발
  if (c === 'LU' && !has(s, 'LU1')) s.pend.push({ t: 'lu' });
  if (c === 'WD' && !has(s, 'WD2')) s.pend.push({ t: 'wd' });
  if (c === 'QU' && !has(s, 'QU1')) s.pend.push({ t: 'qu1' });
  if (c === 'ALU' && !has(s, 'ALU')) s.pend.push({ t: 'alu' });
}
function combos(arr, k) { const out = []; const rec = (st, cur) => { if (cur.length === k) { out.push(cur.slice()); return; } for (let i = st; i < arr.length; i++) { cur.push(arr[i]); rec(i + 1, cur); cur.pop(); } }; rec(0, []); return out; }

// ---------- 수 생성 ----------
// 반환: [{s, title, act, desc, g}]  g: 'd' 드래곤테일 기믹 / 'b' 낙인 기믹
function moves(s0) {
  const out = [];
  const exN = s => { let n = 0; for (const k in s.extra) n += s.extra[k]; return n; };
  const ex0 = exN(s0), qu0 = s0.field.some(m => m.c === 'QU');
  const push = (s, title, act, desc, g) => {
    if (qu0 && exN(s) < ex0 && s.field.some(m => m.c === 'QU') && !has(s, 'QU2') && !s.pend.some(p => p.t === 'qu2')) s.pend.push({ t: 'qu2' });
    out.push({ s, title, act, desc, g });
  };
  // ---- 대기 중인 유발 효과부터 처리 ----
  if (s0.pend.length) {
    const p = s0.pend[0];
    if (p.t === 'set') {
      // 함정 3종은 이 턴 안에서는 차이가 없으므로 플레임 → 혼 → 스팅 순으로 하나만 후보로 둠
      const tr = ['FL', 'HO', 'ST'].find(c => (s0.deck[c] || 0) > 0); const opts = ['RA', 'KE'].filter(c => (s0.deck[c] || 0) > 0).concat(tr ? [tr] : []);
      if (!opts.length || !freeS(s0)) { const s = clone(s0); s.pend.shift(); push(s, null); return out; }
      for (const c of opts) { const s = clone(s0); s.pend.shift(); use(s, p.by + 'S'); s.deck[c]--; s.st.push({ c, z: freeS(s) }); push(s, N[p.by] + ' 효과', '융합 소재로 묘지행', '덱에서 ' + N[c] + ' 세트', 'd'); }
      return out;
    }
    if (p.t === 'ret') {
      const cand = []; const seen = {}; s0.gy.forEach(c => { if (isMon(c) && !seen[c]) { seen[c] = 1; cand.push(c); } });
      { const s = clone(s0); s.pend.shift(); push(s, null); }
      for (let k = 1; k <= Math.min(p.n, cand.length); k++) for (const pick of combos(cand, k)) {
        const s = clone(s0); s.pend.shift(); use(s, 'ART1');
        for (const c of pick) { rm(s.gy, c); if (C[c].k === 'x') s.extra[c] = (s.extra[c] || 0) + 1; else s.hand.push(c); }
        push(s, N.ART + ' 효과', '융합 소환 시 · 패에서 쓴 소재 ' + p.n + '장', '묘지의 ' + pick.map(c => N[c]).join('·') + '를 ' + (pick.every(c => C[c].k === 'x') ? '엑스트라 덱으로' : '패로'), 'd');
      }
      return out;
    }
    if (p.t === 'lu') {
      const opts = ['MU', 'FA', 'UR', 'PA'].filter(c => (s0.deck[c] || 0) > 0);
      if (!opts.length) { const s = clone(s0); s.pend.shift(); push(s, null); return out; }
      for (const c of opts) { const s = clone(s0); s.pend.shift(); use(s, 'LU1'); s.deck[c]--; s.hand.push(c); push(s, N.LU + ' 효과', '소환 시', '덱에서 ' + N[c] + '를 패에 넣음', 'd'); }
      return out;
    }
    if (p.t === 'wd') {
      const srcs = []; if (s0.deck.EC > 0) srcs.push('deck'); if (s0.gy.indexOf('EC') >= 0) srcs.push('gy'); if (s0.hand.indexOf('EC') >= 0) srcs.push('hand');
      if (!srcs.length || s0.noSS || !freeM(s0)) { const s = clone(s0); s.pend.shift(); push(s, null); return out; }
      for (const src of srcs) { const s = clone(s0); s.pend.shift(); use(s, 'WD2'); if (src === 'deck') s.deck.EC--; else if (src === 'gy') rm(s.gy, 'EC'); else rm(s.hand, 'EC'); s.field.push({ c: 'EC', z: freeM(s) });
        push(s, N.WD + ' 소환 시 효과', '', ({ deck: '덱', gy: '묘지', hand: '패' })[src] + '의 ' + N.EC + ' 특수 소환', 'b'); }
      return out;
    }
    if (p.t === 'qu1') {
      const opts = ['AZ', 'WD', 'EC', 'CA'].filter(c => (s0.deck[c] || 0) > 0);
      if (!opts.length) { const s = clone(s0); s.pend.shift(); push(s, null); return out; }
      for (const c of opts) { const s = clone(s0); s.pend.shift(); use(s, 'QU1'); s.deck[c]--; s.gy.push(c); push(s, N.QU + ' 소환 시 효과', '', '덱의 ' + N[c] + '를 묘지로', 'b'); }
      return out;
    }
    if (p.t === 'qu2') {
      { const s = clone(s0); s.pend.shift(); push(s, null); }
      if (!s0.noSS && freeM(s0) && s0.field.some(m => m.c === 'QU')) for (const c of ['AZ', 'WD', 'EC', 'CA']) if (s0.gy.indexOf(c) >= 0) {
        const s = clone(s0); s.pend.shift(); use(s, 'QU2'); rm(s.gy, c); s.field.push({ c, z: freeM(s) }); onSummon(s, c);
        push(s, N.QU + ' 효과', '엑스트라 덱에서 카드가 나감', '묘지의 ' + N[c] + ' 특수 소환', 'b');
      }
      return out;
    }
    if (p.t === 'alu') {
      const opts = ['BF', 'SPI', 'OPN', 'RED', 'FV', 'RET'].filter(c => (s0.deck[c] || 0) > 0);
      if (!opts.length) { const s = clone(s0); s.pend.shift(); push(s, null); return out; }
      for (const c of opts) { const s = clone(s0); s.pend.shift(); use(s, 'ALU'); s.deck[c]--; s.hand.push(c); push(s, N.ALU + ' 효과', '소환 시', '덱에서 ' + N[c] + '를 패에 넣음', 'b'); }
      return out;
    }
    if (p.t === 'lub') {
      { const s = clone(s0); s.pend.shift(); push(s, null); }
      for (const d of new Set(s0.hand)) { const b0 = clone(s0); b0.pend.shift(); rm(b0.hand, d); b0.gy.push(d); b0.lockF = true;
        for (const ch of fusionChoices(b0, { field: 1, gy: 1, ban: 1 }, ['SEC', 'ALB', 'MJ', 'SAN', 'MIX', 'TIT', 'GRG', 'KHA'])) {
          if (ch.mats.some(m => m.from === 'field' && m.c === 'LUB')) continue;
          const s = clone(b0); use(s, 'LUB1'); doFusion(s, ch, 'deck');
          push(s, N.LUB + ' 소환 시 효과', '패의 ' + N[d] + '를 버림', matText(ch) + '를 덱으로 되돌리고 ' + N[ch.t] + ' 융합 소환. 이후 이 턴은 엑스트라 덱에서 융합 몬스터만', 'b');
        } }
      return out;
    }
    if (p.t === 'grg') {
      { const s = clone(s0); s.pend.shift(); push(s, null); }
      for (const c of ['ALB', 'TIT', 'DEV', 'RIN', 'LUW']) if ((s0.extra[c] || 0) > 0) { const s = clone(s0); s.pend.shift(); use(s, 'GRG1'); s.extra[c]--; toGY(s, c); push(s, N.GRG + ' 소환 시 효과', '', '엑스트라 덱의 ' + N[c] + '를 묘지로', 'b'); }
      return out;
    }
    if (p.t === 'alb') {
      { const s = clone(s0); s.pend.shift(); push(s, null); }
      for (const ch of fusionChoices(s0, { hand: 1, field: 1, gy: 1 }, ['ART', 'SEC', 'MJ', 'SAN', 'MIX', 'TIT', 'GUL', 'GRG', 'KHA'])) {
        if (ch.mats.some(m => m.from === 'field' && s0.field[m.i].c === 'ALB' && false)) continue;
        if ((ch.t === 'ART' || ch.t === 'GUL')) continue; // 패 소재 조건이 있는 융합은 제외 소재로 다루지 않음
        const s = clone(s0); s.pend.shift(); use(s, 'ALB1'); doFusion(s, ch, true);
        push(s, N.ALB + ' 소환 시 효과', matText(ch) + ' 제외', N[ch.t] + ' 융합 소환', 'b');
      }
      return out;
    }
  }
  const s0h = s0.hand;
  // ---- 일반 소환 ----
  if (!s0.ns && freeM(s0)) for (const c of ['MU', 'LU', 'AZ', 'WD', 'EC', 'CA', 'QU', 'ALU']) if (s0h.indexOf(c) >= 0) {
    const s = clone(s0); s.ns = true; rm(s.hand, c); s.field.push({ c, z: freeM(s) }); onSummon(s, c); push(s, N[c] + ' 일반 소환', '패 → 일반 소환', '', C[c].dt ? 'd' : 'b');
  }
  const onField = c => s0.field.some(m => m.c === c);
  // ---- 무루루 (필드) ----
  if (onField('MU') && !has(s0, 'MU1') && !s0.noSS) for (const ch of fusionChoices(s0, { hand: 1, field: 1 }, ['ART', 'GUL'])) {
    const s = clone(s0); use(s, 'MU1'); doFusion(s, ch); s.lockF = true; push(s, N.MU + ' 효과 (필드)', matText(ch), N[ch.t] + ' 융합 소환. 이후 이 턴은 엑스트라 덱에서 융합 몬스터만', 'd');
  }
  // ---- 파이메나 (패) ----
  if (!has(s0, 'FA1') && !s0.noSS) { const fi = s0h.indexOf('FA'); if (fi >= 0) for (const ch of fusionChoices(s0, { hand: 1, field: 1 }, ['ART', 'GUL', 'SEC', 'ALB', 'SAN', 'MIX', 'TIT', 'GRG', 'LUB', 'KHA'], fi)) {
    const s = clone(s0); use(s, 'FA1');
    // 버리는 파이메나의 패 위치가 소재 위치보다 앞이면 소재 인덱스 보정
    const ch2 = { t: ch.t, hm: ch.hm, mats: ch.mats.map(m => m.from === 'hand' ? { c: m.c, from: 'hand', i: m.i > fi ? m.i - 1 : m.i } : m) };
    s.hand.splice(fi, 1); s.gy.push('FA'); doFusion(s, ch2);
    push(s, N.FA + ' 효과 (패)', '비용: ' + N.FA + ' 자신을 버림', matText(ch) + '로 ' + N[ch.t] + ' 융합 소환', 'd');
  } }
  // ---- 카르테시아 (필드) ----
  if (onField('CA') && !has(s0, 'CA2') && !s0.noSS) for (const ch of fusionChoices(s0, { hand: 1, field: 1 }, ['ART', 'SEC', 'ALB', 'MJ', 'SAN', 'MIX', 'TIT', 'GRG', 'LUB', 'KHA'])) {
    const s = clone(s0); use(s, 'CA2'); doFusion(s, ch); push(s, N.CA + ' 효과', matText(ch), N[ch.t] + ' 융합 소환 (레벨 8 이상)', 'b');
  }
  // ---- 케투 ----
  const kz = s0.st.findIndex(m => m.c === 'KE'), kh = s0h.indexOf('KE');
  if (!has(s0, 'KE') && (kz >= 0 || kh >= 0)) for (const c of ['MU', 'LU', 'FA', 'UR', 'PA']) if ((s0.deck[c] || 0) > 0) {
    const s = clone(s0); use(s, 'KE'); if (kz >= 0) s.st.splice(kz, 1); else rm(s.hand, 'KE'); s.gy.push('KE'); s.deck[c]--; s.hand.push(c);
    push(s, N.KE + ' 발동', kz >= 0 ? '세트한 카드' : '패에서', '덱에서 ' + N[c] + '를 패에 넣음', 'd');
  }
  // ---- 라후 ----
  const rz = s0.st.findIndex(m => m.c === 'RA'), rh = s0h.indexOf('RA');
  if (!has(s0, 'RA') && (rz >= 0 || rh >= 0) && !s0.noSS) {
    const base = clone(s0); if (rz >= 0) base.st.splice(rz, 1); else rm(base.hand, 'RA');
    for (const ch of fusionChoices(base, { hand: 1, field: 1, deck: 1 }, ['ART', 'GUL'])) {
      if (ch.mats.filter(m => m.from === 'deck').length > 1) continue;
      const s = clone(base); use(s, 'RA'); s.gy.push('RA'); doFusion(s, ch); s.lockF = true;
      push(s, N.RA + ' 발동', matText(ch), N[ch.t] + ' 융합 소환. 이후 이 턴은 엑스트라 덱에서 융합 몬스터만', 'd');
    }
  }
  // ---- 낙인융합 (패) ----
  const BFT = ['ALB', 'MJ', 'SAN', 'TIT', 'LUB'];
  if (!has(s0, 'BF') && s0h.indexOf('BF') >= 0 && !s0.nfx && !s0.noSS) {
    const base = clone(s0); rm(base.hand, 'BF'); base.lockF = true;
    for (const ch of fusionChoices(base, { hand: 1, field: 1, deck: 1 }, BFT)) {
      const s = clone(base); use(s, 'BF'); s.gy.push('BF'); doFusion(s, ch);
      push(s, N.BF + ' 발동', matText(ch), N[ch.t] + ' 융합 소환. 이 턴은 엑스트라 덱에서 융합 몬스터만', 'b');
    }
  }
  // ---- 아나콘다 ----
  if (onField('ANA') && !has(s0, 'ANA1') && (s0.deck.BF || 0) > 0 && !s0.noSS) {
    const base = clone(s0); base.deck.BF--; base.gy.push('BF');
    for (const ch of fusionChoices(base, { hand: 1, field: 1, deck: 1 }, BFT)) {
      const s = clone(base); use(s, 'ANA1'); doFusion(s, ch); s.noSS = true;
      push(s, N.ANA + ' 효과', 'LP 2000을 지불하고 덱의 ' + N.BF + '을 묘지로 → ' + N.BF + '의 효과가 됨', matText(ch) + '로 ' + N[ch.t] + ' 융합 소환. 이후 이 턴은 특수 소환 불가', 'b');
    }
  }
  if (canExtra(s0, 'ANA') && s0.field.length >= 2 && !s0.field.some(m => m.z === 'ER')) {
    const seen = {};
    for (let i = 0; i < s0.field.length; i++) for (let j = i + 1; j < s0.field.length; j++) {
      const a = s0.field[i].c, b = s0.field[j].c, k = [a, b].sort().join('+'); if (seen[k]) continue; seen[k] = 1;
      const s = clone(s0); s.field.splice(j, 1); s.field.splice(i, 1); toGY(s, a); toGY(s, b); s.extra.ANA--; s.field.push({ c: 'ANA', z: 'ER' }); s.nfx = true;
      push(s, N.ANA + ' 링크 소환', N[a] + ' + ' + N[b] + ' (효과 몬스터 2장)', '엑스트라 몬스터 존', 'b');
    }
  }
  // ---- 검은 용의 에클레시아 ----
  if (canExtra(s0, 'EDD')) {
    const seen = {};
    for (let i = 0; i < s0.field.length; i++) for (let j = 0; j < s0.field.length; j++) {
      const a = s0.field[i].c, b = s0.field[j].c; if (i === j || !C[a].tun || C[b].tun || C[a].k !== 'm' || C[b].k !== 'm' || C[a].lv + C[b].lv !== 8) continue;
      const k = a + '+' + b; if (seen[k]) continue; seen[k] = 1;
      const s = clone(s0); const hi = Math.max(i, j), lo = Math.min(i, j); s.field.splice(hi, 1); s.field.splice(lo, 1); toGY(s, a); toGY(s, b); s.extra.EDD--; s.field.push({ c: 'EDD', z: freeX(s) }); s.nfx = true;
      push(s, N.EDD + ' 싱크로 소환', N[a] + '(레벨 4 튜너) + ' + N[b] + '(레벨 4)', '레벨 8 싱크로', 'b');
    }
  }
  if (onField('EDD') && !has(s0, 'EDD1') && !s0.noSS) for (const c of ['AZ', 'WD', 'CA', 'EC']) for (const src of ['deck', 'gy']) {
    if (src === 'deck' ? !(s0.deck[c] > 0) : s0.gy.indexOf(c) < 0) continue;
    const s = clone(s0); use(s, 'EDD1'); s.field.splice(s.field.findIndex(m => m.c === 'EDD'), 1); s.eddb = true;
    if (src === 'deck') s.deck[c]--; else rm(s.gy, c); s.field.push({ c, z: freeM(s) }); onSummon(s, c);
    push(s, N.EDD + ' 효과', '자신을 엔드 페이즈까지 제외', (src === 'deck' ? '덱' : '묘지') + '의 ' + N[c] + ' 특수 소환', 'b');
  }
  // ---- 하얀 용의 낙윤 (패) ----
  if (!has(s0, 'WD1') && s0h.indexOf('WD') >= 0 && !s0.noSS && freeM(s0)) {
    let costs = ['ALB', 'TIT', 'DEV', 'RIN', 'GRG'].filter(c => (s0.extra[c] || 0) > 0); if (!costs.length) costs = ['LEN', 'MJ', 'SAN', 'EDD'].filter(c => (s0.extra[c] || 0) > 0).slice(0, 1);
    for (const c of costs) {
      const s = clone(s0); use(s, 'WD1'); s.extra[c]--; toGY(s, c);
      rm(s.hand, 'WD'); s.field.push({ c: 'WD', z: freeM(s) }); s.lock8 = true; onSummon(s, 'WD');
      push(s, N.WD + ' 효과 (패)', '비용: 엑스트라 덱의 ' + N[c] + '를 묘지로', '자신을 특수 소환. 이후 이 턴은 엑스트라 덱에서 레벨 8 융합·싱크로만', 'b');
    }
  }
  // ---- 에클레시아 (필드) ----
  if (onField('EC') && !has(s0, 'EC2') && !s0.noSS) for (const c of ['AZ', 'WD']) for (const src of ['deck', 'hand']) {
    if (src === 'deck' ? !(s0.deck[c] > 0) : s0h.indexOf(c) < 0) continue;
    const s = clone(s0); use(s, 'EC2'); s.field.splice(s.field.findIndex(m => m.c === 'EC'), 1); s.gy.push('EC');
    if (src === 'deck') s.deck[c]--; else rm(s.hand, c); s.field.push({ c, z: freeM(s) }); onSummon(s, c);
    push(s, N.EC + ' 효과', '자신을 릴리스', (src === 'deck' ? '덱' : '패') + '의 ' + N[c] + ' 특수 소환', 'b');
  }
  // ---- 카르테시아 (패) ----
  if (!has(s0, 'CA1') && s0h.indexOf('CA') >= 0 && !s0.noSS && freeM(s0) && (s0.field.some(m => AL(m.c)) || s0.gy.some(c => AL(c)))) {
    const s = clone(s0); use(s, 'CA1'); rm(s.hand, 'CA'); s.field.push({ c: 'CA', z: freeM(s) });
    push(s, N.CA + ' 효과 (패)', '필드나 묘지에 알버스의 낙윤이 있음', '자신을 특수 소환', 'b');
  }
  // ---- 심연룡 알버 레나투스: 필드의 알버스의 낙윤 + 드래곤족을 묘지로 보내고 특수 소환 ----
  if (canExtra(s0, 'LEN')) { const seen = {};
    for (let i = 0; i < s0.field.length; i++) for (let j = 0; j < s0.field.length; j++) {
      const a = s0.field[i].c, b = s0.field[j].c; if (i === j || !AL(a) || C[b].r !== 'D' || C[b].nomat) continue; const k = a + '+' + b; if (seen[k] || seen[b + '+' + a]) continue; seen[k] = 1;
      const s = clone(s0); const hi = Math.max(i, j), lo = Math.min(i, j); s.field.splice(hi, 1); s.field.splice(lo, 1); toGY(s, a); toGY(s, b); s.extra.LEN--; s.field.push({ c: 'LEN', z: freeX(s) });
      push(s, N.LEN + ' 특수 소환', '필드의 ' + N[a] + ' + ' + N[b] + '(드래곤족)를 묘지로 보냄', '융합 카드 없이 엑스트라 덱에서 특수 소환', 'b');
    }
  }
  // ---- 루루와릴리스: 레벨 4 튜너 + 레벨 8 비튜너 ----
  if (canExtra(s0, 'LUW')) { const seen = {};
    for (let i = 0; i < s0.field.length; i++) for (let j = 0; j < s0.field.length; j++) {
      const a = s0.field[i].c, b = s0.field[j].c; if (i === j || !C[a].tun || C[a].k !== 'm' || C[b].tun || C[b].lv !== 8 || C[b].x === 'link') continue; const k = a + '+' + b; if (seen[k]) continue; seen[k] = 1;
      const s = clone(s0); const hi = Math.max(i, j), lo = Math.min(i, j); s.field.splice(hi, 1); s.field.splice(lo, 1); toGY(s, a); toGY(s, b); s.extra.LUW--; s.field.push({ c: 'LUW', z: freeX(s) }); s.nfx = true;
      push(s, N.LUW + ' 싱크로 소환', N[a] + '(레벨 4 튜너) + ' + N[b] + '(레벨 8)', '레벨 12 싱크로', 'b');
    }
  }
  // ---- 흑의룡 알비온 (패·묘지) ----
  if (!has(s0, 'SHR')) for (const loc of ['hand', 'gy']) { if ((loc === 'hand' ? s0h : s0.gy).indexOf('SHR') < 0) continue;
    // 패에서 보냄 → 자신 특수 소환
    if (!s0.noSS && freeM(s0)) for (const c of new Set(s0h)) { if (!(C[c].al || C[c].br)) continue;
      const s = clone(s0); use(s, 'SHR'); rm(s.hand, c); s.gy.push(c); rm(loc === 'hand' ? s.hand : s.gy, 'SHR'); s.field.push({ c: 'SHR', z: freeM(s) });
      push(s, N.SHR + ' 효과 (' + (loc === 'hand' ? '패' : '묘지') + ')', '패의 ' + N[c] + '를 묘지로', '자신을 특수 소환 (필드·묘지에서는 알버스의 낙윤 취급)', 'b'); }
    // 덱에서 보냄 → 자신은 덱 맨 아래로 (패에서 썼다면 1장 드로우: 무엇을 뽑는지는 계산하지 않음)
    for (const c of ['AZ', 'WD', 'BF', 'FV', 'RET', 'SPI', 'OPN', 'RED']) { if (!((s0.deck[c] || 0) > 0)) continue; if (C[c].k !== 'm' && c !== 'RET') continue;
      const s = clone(s0); use(s, 'SHR'); s.deck[c]--; s.gy.push(c); rm(loc === 'hand' ? s.hand : s.gy, 'SHR'); s.deck.SHR = (s.deck.SHR || 0) + 1;
      push(s, N.SHR + ' 효과 (' + (loc === 'hand' ? '패' : '묘지') + ')', '덱의 ' + N[c] + '를 묘지로', '자신은 덱 맨 아래로' + (loc === 'hand' ? ' → 1장 드로우 (뽑는 카드는 계산에 넣지 않음)' : ''), 'b'); }
  }
  // ---- 낙인개막 ----
  if (!has(s0, 'OPN') && s0h.indexOf('OPN') >= 0) for (const d of new Set(s0h)) { if (d === 'OPN' && s0h.filter(x => x === 'OPN').length < 2) continue;
    for (const c of ['ALU', 'QU']) { if (!((s0.deck[c] || 0) > 0)) continue; for (const mode of ['hand', 'ss']) { if (mode === 'ss' && (s0.noSS || !freeM(s0))) continue;
      const s = clone(s0); use(s, 'OPN'); rm(s.hand, 'OPN'); s.gy.push('OPN'); rm(s.hand, d); s.gy.push(d); s.deck[c]--; s.lockF = true;
      if (mode === 'ss') { s.field.push({ c, z: freeM(s) }); onSummon(s, c); } else s.hand.push(c);
      push(s, N.OPN + ' 발동', '패의 ' + N[d] + '를 버림', '덱의 ' + N[c] + '를 ' + (mode === 'ss' ? '수비 표시로 특수 소환' : '패에 넣음') + '. 이후 이 턴은 엑스트라 덱에서 융합 몬스터만', 'b'); } } }
  // ---- 혁의 낙인 ----
  if (!has(s0, 'RED') && s0h.indexOf('RED') >= 0) for (const c of new Set(s0.gy.filter(x => ['ALU', 'QU', 'AZ', 'WD', 'SHR'].indexOf(x) >= 0))) {
    const b0 = clone(s0); use(b0, 'RED'); rm(b0.hand, 'RED'); b0.gy.push('RED'); rm(b0.gy, c); b0.hand.push(c);
    push(clone(b0), N.RED + ' 발동', '묘지의 ' + N[c] + ' 대상', N[c] + '를 패에 넣음', 'b');
    if (!b0.noSS) for (const ch of fusionChoices(b0, { hand: 1, field: 1 }, ['SEC', 'ALB', 'MJ', 'SAN', 'MIX', 'TIT', 'GRG', 'LUB', 'KHA'])) {
      const s = clone(b0); doFusion(s, ch, true);
      push(s, N.RED + ' 발동', '묘지의 ' + N[c] + ' 대상', N[c] + '를 패에 넣고, ' + matText(ch) + '를 제외해 ' + N[ch.t] + ' 융합 소환', 'b'); }
  }
  // ---- 천저의 사도 ----
  if (!has(s0, 'NAD') && s0h.indexOf('NAD') >= 0) {
    let costs = ['ALB', 'TIT', 'DEV', 'RIN', 'LUW', 'GRG'].filter(c => (s0.extra[c] || 0) > 0); if (!costs.length) costs = Object.keys(s0.extra).filter(c => s0.extra[c] > 0 && C[c].atk >= 1800).slice(0, 1);
    for (const x of costs) for (const c of ['AZ', 'WD', 'QU']) for (const src of ['deck', 'gy']) {
      if (C[c].atk > C[x].atk) continue; if (src === 'deck' ? !(s0.deck[c] > 0) : s0.gy.indexOf(c) < 0) continue;
      const s = clone(s0); use(s, 'NAD'); rm(s.hand, 'NAD'); s.gy.push('NAD'); s.extra[x]--; toGY(s, x);
      if (src === 'deck') s.deck[c]--; else rm(s.gy, c); s.hand.push(c); s.noEX = true;
      push(s, N.NAD + ' 발동', '엑스트라 덱의 ' + N[x] + '를 묘지로', (src === 'deck' ? '덱' : '묘지') + '의 ' + N[c] + '를 패에 넣음. 이후 이 턴은 엑스트라 덱에서 특수 소환 불가', 'b');
    }
  }
  // ---- 낙인의 기염 ----
  if (!has(s0, 'SPI') && s0h.indexOf('SPI') >= 0) {
    const seenR = {};
    for (const h of new Set(s0h)) { if (!isMon(h) || C[h].gen) continue;
      for (const x in s0.extra) { if (!(s0.extra[x] > 0) || !C[x].sp || C[x].r !== C[h].r) continue;
        if (x !== 'ALB' && x !== 'TIT' && (s0.extra.ALB > 0 || s0.extra.TIT > 0) && C[h].r === 'D') continue; // 드래곤족이면 엔드 페이즈 효과가 있는 카드만 후보
        for (const c of ['AZ', 'WD', 'EC', 'CA', 'QU']) { if (!(s0.deck[c] > 0)) continue;
          const s = clone(s0); use(s, 'SPI'); rm(s.hand, 'SPI'); s.gy.push('SPI'); s.extra[x]--; toGY(s, x); rm(s.hand, h); s.gy.push(h); s.deck[c]--; s.hand.push(c);
          push(s, N.SPI + ' 발동', '패의 ' + N[h] + '를 보여 주고 같은 종족의 ' + N[x] + '를 엑스트라 덱에서 묘지로', N[h] + '를 버리고 덱에서 ' + N[c] + '를 패에 넣음', 'b');
        }
      }
    }
  }
  // ---- 우르굴라 (묘지) ----
  if (!has(s0, 'UR2') && s0.gy.indexOf('UR') >= 0) for (const c of ['LU', 'FA']) if (s0.gy.indexOf(c) >= 0) {
    const s = clone(s0); use(s, 'UR2'); rm(s.gy, 'UR'); s.deck.UR = (s.deck.UR || 0) + 1; rm(s.gy, c); s.hand.push(c);
    push(s, N.UR + ' 묘지 효과', '묘지의 ' + N[c] + '(마법사족 드래곤테일) 대상', N.UR + '를 덱 맨 아래로 되돌리고 ' + N[c] + '를 패에 넣음', 'd');
  }
  // ---- 사크라멘툼 ----
  if (onField('SEC') && !has(s0, 'SEC1') && !s0.noSS) {
    const D = [...new Set(s0.gy.filter(c => isMon(c) && C[c].r === 'D'))], S = [...new Set(s0.gy.filter(c => isMon(c) && C[c].r === 'S'))];
    for (const d of D) for (const sp of S) for (const [up, down] of [[d, sp], [sp, d]]) {
      if (!freeM(s0) && !(C[up].k === 'x' && freeX(s0))) continue;
      const s = clone(s0); use(s, 'SEC1'); rm(s.gy, up); rm(s.gy, down);
      if (C[down].k === 'x') s.extra[down] = (s.extra[down] || 0) + 1; else s.deck[down] = (s.deck[down] || 0) + 1;
      s.field.push({ c: up, z: C[up].k === 'x' ? freeX(s) : freeM(s) }); onSummon(s, up);
      push(s, N.SEC + ' 효과', '묘지의 ' + N[d] + '(드래곤족) + ' + N[sp] + '(마법사족) 대상', N[up] + '를 특수 소환하고 ' + N[down] + '는 ' + (C[down].k === 'x' ? '엑스트라 덱으로' : '덱 맨 아래로'), d === 'MU' || C[up].dt ? 'd' : 'b');
    }
  }
  return out;
}

// ---------- 엔드 페이즈 ----------
function endPhase(s0) {
  const s = clone(s0), log = [];
  if (s.gy.indexOf('DEV') >= 0) {
    const g = (s.deck.FV || 0) > 0 ? 'FV' : (s.deck.QU || 0) > 0 ? 'QU' : null;
    if (g) { s.deck[g]--; s.hand.push(g); log.push({ title: '엔드 페이즈: ' + N.DEV, act: '이 턴에 묘지로 간 상태', desc: '덱에서 ' + N[g] + '(드래그마 취급)를 패에 넣음', s: clone(s) }); }
    // 패의 F&V를 바로 발동: 낙인룡 알비온을 묘지로 보내 2장째 F&V를 세트 (없어도 되는 내 몬스터 1장을 파괴)
    if (g === 'FV' && !s.albgy && (s.extra.ALB || 0) > 0 && (s.deck.FV || 0) > 0) {
      const d = ['WD', 'AZ', 'LU', 'UR', 'PA', 'FA', 'ANA', 'LEN', 'ART'].find(c => s.field.some(m => m.c === c));
      if (d) { rm(s.hand, 'FV'); s.gy.push('FV'); s.extra.ALB--; toGY(s, 'ALB'); s.field.splice(s.field.findIndex(m => m.c === d), 1); toGY(s, d);
        log.push({ title: '엔드 페이즈: ' + N.FV + ' 발동 (패)', act: '엑스트라 덱의 ' + N.ALB + '를 묘지로', desc: '필드의 ' + N[d] + ' 파괴 (낙인룡 알비온의 엔드 페이즈 효과를 켜기 위한 발동)', s: clone(s) }); }
    }
  }
  if (s.gy.indexOf('LUW') >= 0 && !s.noSS && freeM(s)) { const g = ['QU', 'CA', 'EC'].find(c => (s.deck[c] || 0) > 0);
    if (g) { s.deck[g]--; s.field.push({ c: g, z: freeM(s) }); log.push({ title: '엔드 페이즈: ' + N.LUW, act: '이 턴에 묘지로 간 상태', desc: '덱에서 ' + N[g] + '(공격력 1500 빛 속성 마법사족) 특수 소환', s: clone(s) }); } }
  if (s.gy.indexOf('LEN') >= 0 && (s.deck.BF || 0) > 0) { s.deck.BF--; s.hand.push('BF'); log.push({ title: '엔드 페이즈: ' + N.LEN, act: '이 턴에 묘지로 간 상태', desc: '덱에서 ' + N.BF + '을 패에 넣음', s: clone(s) }); }
  if (s.albgy && freeS(s)) { const g = (s.deck.FV || 0) > 0 ? 'FV' : (s.deck.RET || 0) > 0 ? 'RET' : null;
    if (g) { s.deck[g]--; s.st.push({ c: g, z: freeS(s) }); log.push({ title: '엔드 페이즈: ' + N.ALB, act: '이 턴에 묘지로 간 상태', desc: '덱에서 ' + N[g] + ' 세트', s: clone(s) }); } }
  if (s.titgy) {
    if ((s.deck.QU || 0) > 0 && !s.noSS && freeM(s)) {
      s.deck.QU--; s.field.push({ c: 'QU', z: freeM(s) }); let d = '덱에서 ' + N.QU + '(드래그마 취급) 특수 소환';
      const g = ['AZ', 'WD', 'CA', 'EC'].find(c => (s.deck[c] || 0) > 0 && !(C[c].al && s.gy.some(x => AL(x))) ) || ['AZ', 'WD', 'CA', 'EC'].find(c => (s.deck[c] || 0) > 0);
      if (g) { s.deck[g]--; s.gy.push(g); d += ' → 소환 시 효과로 덱의 ' + N[g] + '를 묘지로'; }
      log.push({ title: '엔드 페이즈: ' + N.TIT, act: '이 턴에 묘지로 간 상태', desc: d, s: clone(s) });
    } else if ((s.deck.AZ || 0) > 0) { s.deck.AZ--; s.hand.push('AZ'); log.push({ title: '엔드 페이즈: ' + N.TIT, act: '이 턴에 묘지로 간 상태', desc: '덱에서 ' + N.AZ + '을 패에 넣음', s: clone(s) }); }
  }
  if (s.fgy) { const back = ['CA', 'EC'].filter(c => s.gy.indexOf(c) >= 0); if (back.length) { for (const c of back) { rm(s.gy, c); s.hand.push(c); } log.push({ title: '엔드 페이즈: ' + back.map(c => N[c]).join(' · '), act: '이 턴에 융합 몬스터가 묘지로 감', desc: '묘지에서 패로', s: clone(s) }); } }
  if (s.fgy && s.gy.indexOf('SPI') >= 0) { rm(s.gy, 'SPI'); s.hand.push('SPI'); log.push({ title: '엔드 페이즈: ' + N.SPI, act: '이 턴에 융합 몬스터가 묘지로 감', desc: '묘지에서 패로', s: clone(s) }); }
  if (s.eddb && freeX(s)) { s.field.push({ c: 'EDD', z: freeX(s) }); s.eddb = false; log.push({ title: '엔드 페이즈: ' + N.EDD + ' 복귀', act: '', desc: '', s: clone(s) }); }
  const sets = s0.hand.filter(c => C[c].k === 't' || c === 'FV').filter(c => s.hand.indexOf(c) >= 0);
  if (sets.length) { for (const c of sets) { if (!freeS(s)) break; rm(s.hand, c); s.st.push({ c, z: freeS(s) }); } log.push({ title: '패의 함정·속공 마법 세트', act: '', desc: sets.map(c => N[c]).join(' · ') + ' 세트', s: clone(s) }); }
  return { s, log };
}

// ---------- 평가: 상대 턴 방해 ----------
function evaluate(s) { const _n = NOSS; NOSS = {}; try { return evaluate0(s); } finally { NOSS = _n; } }
function evaluate0(s) {
  const it = []; const F = s.field.map(m => m.c), H = s.hand, ST = s.st.map(m => m.c);
  const dtTrig = ST.some(c => C[c].k === 't' && C[c].dts) || H.indexOf('FA') >= 0 || F.indexOf('MU') >= 0;
  const s_in = s; s = clone(s); for (const c in RES) s.extra[c] = (s.extra[c] || 0) + RES[c];
  const probe = clone(s); probe.lockF = probe.lock8 = probe.noSS = probe.noEX = false; probe.used = []; probe.pend = [];
  const faI = H.indexOf('FA');
  const faF = faI >= 0 ? fusionChoices(probe, { hand: 1, field: 1 }, ['ART', 'GUL', 'SEC', 'ALB', 'SAN', 'MIX', 'TIT'], faI) : [];
  if (F.indexOf('GUL') >= 0 && dtTrig) it.push([N.GUL, '파괴', '드래곤테일 카드·효과 발동에 체인해 상대 카드 1장 파괴']);
  if (F.indexOf('MJ') >= 0) it.push([N.MJ, '제외', '엑스트라 덱의 알버스 관련 융합 몬스터를 묘지로 보내고 몬스터 1장 제외']);
  if (F.indexOf('SAN') >= 0) it.push([N.SAN, '상대 턴 효과', '양쪽 묘지의 몬스터 2장을 양쪽 필드에 1장씩 특수 소환']);
  if (F.indexOf('SEC') >= 0) it.push([N.SEC, '락', '상대가 특수 소환한 드래곤족·마법사족은 효과 발동 불가']);
  if (F.indexOf('EDD') >= 0) it.push([N.EDD, '상대 턴 효과', '자신을 제외하고 덱·묘지의 알버스의 낙윤 등 특수 소환']);
  if (F.indexOf('MU') >= 0 && fusionChoices(probe, { hand: 1, field: 1 }, ['ART', 'GUL']).length) it.push([N.MU + ' (필드)', '상대 턴 효과', '패·필드 소재로 드래곤테일 융합']);
  if (F.indexOf('CA') >= 0 && fusionChoices(probe, { hand: 1, field: 1 }, ['ART', 'SEC', 'ALB', 'MJ', 'SAN', 'MIX', 'TIT', 'GRG']).length) it.push([N.CA + ' (필드)', '상대 턴 효과', '패·필드 소재로 레벨 8 이상 융합']);
  if (F.indexOf('QU') >= 0 && s.gy.some(c => AL(c))) it.push([N.QU + ' (필드)', '상대 턴 효과', '엑스트라 덱에서 카드가 나가면 묘지의 알버스의 낙윤 특수 소환']);
  if (F.indexOf('GRG') >= 0 || s.gy.indexOf('GRG') >= 0) it.push([N.GRG, '상대 턴 효과', '상대가 몬스터 효과로 특수 소환하면 자신을 제외하고 덱의 쿠엠 등 특수 소환']);
  if (s.gy.indexOf('RIN') >= 0 && s.gy.some(c => AL(c))) it.push(['묘지의 ' + N.RIN, '상대 턴 효과', '묘지의 알버스의 낙윤을 특수 소환하고 자신은 제외']);
  if (F.indexOf('LUW') >= 0) it.push([N.LUW, '무효', '엑스트라 덱에서 카드가 나가면 앞면 카드 1장의 효과를 턴 끝까지 무효']);
  if (F.indexOf('EC') >= 0) it.push([N.EC + ' (필드)', '상대 턴 효과', '자신을 릴리스하고 알버스의 낙윤 특수 소환']);
  for (const [c, kind, tx] of [['FL', '무효', '앞면 마법 1장 효과 무효'], ['HO', '바운스', '공격 표시 몬스터 1장을 패·엑스트라 덱으로'], ['ST', '제외', '상대 묘지의 몬스터와 마법·함정을 제외']]) if (ST.indexOf(c) >= 0) it.push(['세트한 ' + N[c], kind, tx]);
  if (ST.indexOf('FV') >= 0 && Object.keys(s.extra).some(c => s.extra[c] > 0 && C[c].men && C[c].x === 'fusion')) it.push(['세트한 F&V', '파괴', '엑스트라 덱의 알버스 관련 융합 몬스터를 묘지로 보내고 앞면 카드 1장 파괴']);
  if (ST.indexOf('RET') >= 0) { const am = c => C[c].x === 'fusion' && C[c].men;
    if (F.some(am) || s.gy.filter(am).length >= 2) it.push(['세트한 ' + N.RET, '무효', '특수 소환을 포함한 효과 발동을 무효로 하고 파괴 (알버스 관련 융합 몬스터를 엑스트라 덱으로 되돌림)']); }
  if (faF.length) {
    it.push(['패의 ' + N.FA, '상대 턴 효과', '자신을 버리고 패·필드 소재로 융합']);
    // 믹시아 → 아이온: 파이메나로 믹시아를 낸 뒤 속성이 다른 융합 몬스터 2장 이상이 묘지·필드에 있어야 함
    if ((s.extra.AEON || 0) > 0) for (const ch of faF) { if (ch.t !== 'MIX') continue;
      const fus = s.gy.filter(c => C[c].x === 'fusion').concat(ch.mats.filter(m => C[m.c].x === 'fusion').map(m => m.c)).concat(F.filter(c => C[c].x === 'fusion' && !ch.mats.some(m => m.from === 'field' && m.c === c)));
      const attrs = new Set(fus.map(c => C[c].a)); attrs.delete('DARK');
      if (attrs.size >= 2) { it.push([N.MIX + ' → ' + N.AEON, '제외', '파이메나로 믹시아를 내고, 믹시아 효과로 속성이 다른 융합 몬스터 3장을 제외해 아이온 → 카드 3장 + 상대 엑스트라 덱 3장 제외']); break; }
    }
  }
  return it;
}

// ---------- 탐색 ----------
let NOSS = {}; // 비용으로는 보내지만 내 턴에 소환하지는 않는 엑스트라 카드
let RES = {}; // 전개 중에는 쓰지 않지만 엑스트라 덱에는 들어 있는 카드 (상대 턴 방해 계산에만 반영)
function evalWith(s, avail, deckOver) { const t = clone(s); t.extra = Object.assign({}, avail); if (deckOver) Object.assign(t.deck, deckOver); const r0 = RES; RES = {}; try { return evaluate(t); } finally { RES = r0; } }
function initState(hand, main, extra, ban, nos) {
  NOSS = {}; for (const n of (nos || [])) if (CODE[n]) NOSS[CODE[n]] = 1;
  const deck = {}, ex = {};
  for (const n in main) if (CODE[n] && C[CODE[n]].k !== 'x') deck[CODE[n]] = main[n];
  for (const n in extra) if (CODE[n]) ex[CODE[n]] = extra[n];
  const h = [];
  for (const n of hand) { const c = n === '패의 드래곤테일 이외 몬스터' ? 'X' : CODE[n]; if (!c) continue; h.push(c); if (c !== 'X') { if (!(deck[c] > 0)) return null; deck[c]--; } }
  RES = {}; for (const n of (ban || [])) { const c = CODE[n]; if (!c) continue; if (C[c].k === 'x') { if (ex[c] > 0) { RES[c] = ex[c]; delete ex[c]; } } else delete deck[c]; }
  return { hand: h, deck, extra: ex, field: [], st: [], gy: [], ban: [], used: [], lockF: false, lock8: false, noSS: false, noEX: false, ns: false, nfx: false, fgy: false, albgy: false, titgy: false, eddb: false, pend: [] };
}
function boardKey(s) { return s.field.map(m => m.c).sort().join(',') + '|' + s.st.map(m => m.c).sort().join(',') + '|' + s.hand.slice().sort().join(','); }
// opts: {maxStates, maxMs, onProgress}
function search(hand, main, extra, opts) {
  opts = opts || {}; const maxStates = opts.maxStates || 400000, maxMs = opts.maxMs || 60000, t0 = Date.now();
  const s0 = initState(hand, main, extra, opts.ban, opts.nos); const X0 = Object.assign({}, s0.extra), grp = !!opts.group;
  const M0 = {}; for (const n of (opts.optMain || [])) { const c = CODE[n]; if (c) M0[c] = (s0.deck[c] || 0) + s0.hand.filter(x => x === c).length; }
  const usedOf = s => { const u = []; for (const c in X0) { const d = X0[c] - (s.extra[c] || 0); for (let i = 0; i < d; i++) u.push(c); } for (const c in M0) { const d = M0[c] - (s.deck[c] || 0); for (let i = 0; i < d; i++) u.push(c); } return u.sort(); }; if (!s0) return { error: '손패의 카드가 덱에 없습니다', results: [] };
  const NP = new Int32Array(maxStates + 2), NM = new Uint16Array(maxStates + 2); let nn = 1; // 부모 포인터 + 부모의 moves() 안에서 몇 번째 수인지
  let frontier = [{ s: s0, id: 0 }]; const seen = new Set([hkey(s0)]); const boards = new Map(); let done = true, depth = 0;
  const consider = (s, id, d) => {
    if (s.pend.length) return; const ep = endPhase(s); const bk = boardKey(ep.s) + (grp ? '#' + usedOf(ep.s).join(',') : ''); const ev = evaluate(ep.s);
    const cur = boards.get(bk); if (!cur || d < cur.d) boards.set(bk, { id, d, ev });
  };
  consider(s0, 0, 0);
  outer: while (frontier.length) {
    const next = []; depth++;
    for (const f of frontier) {
      const ms = moves(f.s);
      for (let mi = 0; mi < ms.length; mi++) {
        const m = ms[mi]; const k = hkey(m.s); if (seen.has(k)) continue; seen.add(k);
        const id = nn++; NP[id] = f.id; NM[id] = mi;
        next.push({ s: m.s, id }); consider(m.s, id, depth);
        if (seen.size >= maxStates || (seen.size % 2000 === 0 && Date.now() - t0 > maxMs)) { done = false; break outer; }
      }
    }
    frontier = next; if (opts.onProgress) opts.onProgress(seen.size, depth);
  }
  const pathOf = b => { const idx = []; let id = b.id; while (id > 0) { idx.push(NM[id]); id = NP[id]; } return idx.reverse(); };
  if (grp) { // 일괄 계산: 쓴 엑스트라 카드 묶음별로 상위만, 수순은 번호로만 저장
    const G = new Map();
    for (const [bk, b] of boards) { const u = bk.slice(bk.indexOf('#') + 1); if (!G.has(u)) G.set(u, []); G.get(u).push({ bk, b }); }
    const out = [];
    for (const [u, a] of G) {
      a.sort((p, q) => q.b.ev.length - p.b.ev.length || p.b.d - q.b.d);
      const pick = new Set(a.slice(0, 5)); const ua = u ? u.split(',') : [];
      // 필드 구성이 다른 것도 조금 남긴다
      const seenF = new Set(); for (const x of a) { const fk = x.bk.split('|')[0]; if (!seenF.has(fk)) { seenF.add(fk); pick.add(x); if (seenF.size >= 8) break; } }
      for (const x of pick) out.push({ u: ua, sc: x.b.ev.length, d: x.b.d, p: pathOf(x.b) });
    }
    return { groups: out, boards: boards.size, states: seen.size, done, ms: Date.now() - t0 };
  }
  const results = [];
  for (const [bk, b] of boards) {
    const idx = pathOf(b);
    const path = []; let cur = s0; for (const mi of idx) { const m = moves(cur)[mi]; cur = m.s; if (m.title !== null) path.push({ title: m.title, act: m.act, desc: m.desc, g: m.g, s: m.s }); }
    const ep = endPhase(cur); const E = ep.s;
    const g = new Set(path.map(p => p.g)); const kind = g.has('d') && g.has('b') ? 'mix' : g.has('b') ? 'brand' : 'dt';
    results.push({ key: bk, score: b.ev.length, items: b.ev, kind, steps: path, end: ep.log, hand: E.hand.length, handCards: E.hand.map(c => N[c]),
      field: E.field.map(m => N[m.c]), set: E.st.map(m => N[m.c]), nsteps: path.length, final: E, start: s0 });
  }
  results.sort((a, b) => b.score - a.score || b.hand - a.hand || a.nsteps - b.nsteps);
  return { results, states: seen.size, done, ms: Date.now() - t0 };
}
// 저장된 수 번호로 결과를 다시 만든다. avail: 상대 턴에 쓸 수 있는 엑스트라 카드(코드→장수), 없으면 그대로
function replay(hand, main, extra, opts, idx, availOf) {
  const s0 = initState(hand, main, extra, opts.ban, opts.nos); if (!s0) return null;
  const path = []; let cur = s0; for (const mi of idx) { const m = moves(cur)[mi]; if (!m) return null; cur = m.s; if (m.title !== null) path.push({ title: m.title, act: m.act, desc: m.desc, g: m.g, s: m.s }); }
  if (cur.pend.length) return null;
  const ep = endPhase(cur); const E = ep.s; let ev; if (availOf) { const av = availOf(E, s0); ev = evalWith(E, av.x, av.d); } else ev = evaluate(E);
  const g = new Set(path.map(p => p.g)); const kind = g.has('d') && g.has('b') ? 'mix' : g.has('b') ? 'brand' : 'dt';
  return { key: boardKey(E) + '#' + idx.join('.'), score: ev.length, items: ev, kind, steps: path, end: ep.log, hand: E.hand.length, handCards: E.hand.map(c => N[c]),
    field: E.field.map(m => N[m.c]), set: E.st.map(m => N[m.c]), nsteps: path.length, final: E, start: s0 };
}
const api = { N, C, CODE, search, replay, evalWith, initState, moves, endPhase, evaluate, key, clone, res: () => RES };
if (typeof module !== 'undefined' && module.exports) module.exports = api; else root.DTE = api;
})(typeof self !== 'undefined' ? self : this);
