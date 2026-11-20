import sys, itertools
from collections import Counter
sys.setrecursionlimit(100000)
CFG = sys.argv[1]            # base | sh | shch
XYZ_SHY = len(sys.argv) < 3 or sys.argv[2] != 'noxyz'   # 자기 효과로 나온 슈야마를 엑시즈 소재로 쓸 수 있는가
FOD = 3
LINK = {'DEAL':1,'REQ':1,'SEQ':2,'EK':2,'EL':2,'YA':2,'RA':2,'SUN':4,'GRY':4,'AB':4}
LF = {'LCT','ENG','LUR','DEAL','REQ','SEQ','FLA','EK','SUN','GRY'}
DARK = {'SW','EL','YA','RA','AB','LL'}
NONFIEND = {'FRO','SW'}
KIS = {'FRO','DEAL','EK'}; LIL = {'SW','EL','LL'}; ET = {'DEAL','EK','EL'}
LV6 = {'ENG','FLA','SHY','SH'}
UNS = {'YA','SHY','SH'}   # Unchained Soul (라기아 소재 조건)
EXTRA0 = ('AB','CAE','DEAL','EK','EL','FLA','GRY','RA','REQ','SEQ','SUN','YA')
def base(c): return c.rstrip('*')
def fiend(c): return base(c) not in NONFIEND
# state: (hand, fod, deck, field, st, gy, ban, extra, used, abret)
def T(c): return tuple(sorted(c))
def init():
    deck = ['SW','LL','LCT','ENG','ENG','LUR','TRA','TRA','SHY']
    if CFG in ('sh','shch'): deck.append('SH')
    if CFG in ('shch','ch'): deck.append('CH')
    return (('FRO',), FOD, T(deck), (), (), (), (), EXTRA0, frozenset(), False)
def rm(t, c):
    l = list(t); l.remove(c); return tuple(l)
def ad(t, c): return T(t + (c,))
class S:
    __slots__=('hand','fod','deck','field','st','gy','ban','extra','used','abret')
    def __init__(s, t): s.hand,s.fod,s.deck,s.field,s.st,s.gy,s.ban,s.extra,s.used,s.abret = t
    def t(s): return (s.hand,s.fod,s.deck,s.field,s.st,s.gy,s.ban,s.extra,s.used,s.abret)
    def cp(s): return S(s.t())
    def use(s, f): s.used = s.used | {f}
def locked(s): return 'SH*' in s.field
def can_ss(s, c): return len(s.field) < 6 and (fiend(c) or not locked(s))
def to_gy(s, c):
    """몬스터/카드가 필드에서 묘지로 (c는 필드 코드). 반환: 가능한 후속 상태들 (샤바라 세트 선택)."""
    b = base(c)
    if c == 'SHY*': s.deck = ad(s.deck, 'SHY'); return [s]
    s.gy = ad(s.gy, b)
    return sent(s, b)
def sent(s, b):
    out = [s]
    if b == 'SH' and 'SHset' not in s.used and 'CH' in s.deck and len(s.st) < 5:
        n = s.cp(); n.use('SHset'); n.deck = rm(n.deck, 'CH'); n.st = ad(n.st, 'CHs'); out.append(n)
    if b == 'FLA' and 'FLAg' not in s.used:
        for x in set(s.gy):
            if x in LF and x != 'FLA':
                n = s.cp(); n.use('FLAg'); n.gy = rm(n.gy, x)
                if x in LINK or x == 'FLA': n.extra = ad(n.extra, x)
                else: n.deck = ad(n.deck, x)
                out.append(n)
    return out
def destroy(s, zone, c, yama_ok=True):
    """내 카드 c 를 효과로 파괴. zone: 'f' 몬스터 / 's' 마함."""
    s = s.cp(); res = []
    trig_ra = (zone == 'f' and c == 'RA' and 'RAadd' not in s.used)
    trig_ch = (zone == 's' and c == 'CHs' and 'CH2' not in s.used)
    trig_ya = ('YA' in s.gy and 'YA2' not in s.used and yama_ok and not (zone == 'f' and c == 'YA'))
    if zone == 'f':
        s.field = rm(s.field, c); sts = to_gy(s, c)
    else:
        s.st = rm(s.st, c); s.gy = ad(s.gy, {'CHs':'CH','REQe':'REQ','SEQe':'SEQ','TRAs':'TRA'}[c]); sts = [s]
    def ch(st):
        o = [st]
        if trig_ch:
            for u in ('SHY','SH'):
                if u in st.deck and can_ss(st, u):
                    n = st.cp(); n.use('CH2'); n.deck = rm(n.deck, u); n.field = ad(n.field, u); o.append(n)
        return o
    def ra(st):
        o = [st]
        if trig_ra:
            for x in set(st.gy):
                if x != 'RA' and fiend(x) and x not in ('CH','TRA'):
                    n = st.cp(); n.use('RAadd'); n.gy = rm(n.gy, x)
                    if x in LINK or x in ('FLA','CAE'): n.extra = ad(n.extra, x)
                    else: n.hand = ad(n.hand, x)
                    o.append(n)
        return o
    def ya(st):
        o = [st]
        if trig_ya and 'YA' in st.gy:
            cands = [('h', x) for x in set(st.hand) if x not in ('TRA','CH')] + [('g', x) for x in set(st.gy) if x not in ('TRA','CH','YA') and fiend(x)]
            for src, x in cands:
                if not fiend(x) or not can_ss(st, x): continue
                n = st.cp(); n.use('YA2'); n.gy = rm(n.gy, 'YA'); n.ban = ad(n.ban, 'YA')
                if src == 'h': n.hand = rm(n.hand, x)
                else: n.gy = rm(n.gy, x)
                n.field = ad(n.field, x); o.append(n)
                for c2 in set(n.field): o += destroy(n, 'f', c2, False)
                for c2 in set(n.st): o += destroy(n, 's', c2, False)
        return o
    for st in sts:
        for a in ch(st):
            for b in ra(a): res += ya(b)
            for b in ya(a): res += ra(b)
    return res
def discards(s):
    """패 1장 버림: (새 상태들)"""
    out = []
    if s.fod > 0: n = s.cp(); out.append(n)
    for c in set(s.hand):
        n = s.cp(); n.hand = rm(n.hand, c); n.gy = ad(n.gy, c)
        if c == 'LUR' and can_ss(n, 'LUR'): n.gy = rm(n.gy, 'LUR'); n.field = ad(n.field, 'LUR'); out.append(n)
        else: out += sent(n, c)
    return out
def link_sets(s, target):
    R = LINK[target]; f = list(s.field); res = set()
    for k in range(1, 5):
        for idx in itertools.combinations(range(len(f)), k):
            ms = [f[i] for i in idx]; bs = [base(m) for m in ms]
            if target in ('DEAL','REQ'):
                if k != 1: continue
                if target == 'DEAL' and bs[0] not in KIS: continue
                if target == 'REQ' and bs[0] not in LF: continue
            elif R == 2:
                if k != 2: continue
                if target == 'SEQ' and not any(b in LF for b in bs): continue
                if target == 'EK' and not any(b in KIS for b in bs): continue
                if target == 'EL' and not any(b in LIL for b in bs): continue
                if target == 'YA' and not all(fiend(b) for b in bs): continue
                if target == 'RA' and not any(b in UNS for b in bs): continue
            else:
                if k < 2: continue
                lo = k; hi = sum(LINK.get(b, 1) for b in bs)
                # 합이 4가 되는 조합이 있는지
                ok = False
                for choice in itertools.product(*[(1, LINK.get(b, 1)) for b in bs]):
                    if sum(choice) == 4: ok = True; break
                if not ok: continue
                if target == 'SUN' and not any(b in ET for b in bs): continue
                if target == 'AB' and not any(fiend(b) for b in bs): continue
                if target == 'GRY' and len(set(bs)) != len(bs): continue
            res.add(T(ms))
    return res
def remove_mats(s, ms):
    sts = [s]
    for m in ms:
        nx = []
        for st in sts:
            st = st.cp(); st.field = rm(st.field, m); nx += to_gy(st, m)
        sts = nx
    return sts
def moves(s0):
    s = S(s0); out = []
    def A(st, lg): out.append((st.t(), lg))
    U = s.used
    # 일반 소환
    if 'NS' not in U and 'FRO' in s.hand:
        n = s.cp(); n.use('NS'); n.hand = rm(n.hand, 'FRO'); n.field = ad(n.field, 'FRO'); A(n, 'NS FRO')
    # 링크 소환
    for tg in LINK:
        if tg not in s.extra: continue
        if tg == 'DEAL' and 'DEALls' in U: continue
        if tg == 'REQ' and 'REQss' in U: continue
        for ms in link_sets(s, tg):
            for st in remove_mats(s, ms):
                if len(st.field) >= 6: continue
                st = st.cp(); st.extra = rm(st.extra, tg); st.field = ad(st.field, tg)
                if tg == 'DEAL': st.use('DEALls')
                if tg == 'REQ': st.use('REQss')
                lg = f'LINK {tg} <- {"+".join(ms)}'
                if tg == 'YA' and 'YA1' not in st.used:
                    A(st, lg)
                    for u in ('SHY','SH'):
                        if u in st.deck: n = st.cp(); n.use('YA1'); n.deck = rm(n.deck, u); n.hand = ad(n.hand, u); A(n, lg + f' / 야마 서치 {u}(덱)')
                        if u in st.gy: n = st.cp(); n.use('YA1'); n.gy = rm(n.gy, u); n.hand = ad(n.hand, u); A(n, lg + f' / 야마 회수 {u}(묘지)')
                elif tg == 'GRY':
                    A(st, lg)
                    if 'GRY1' not in st.used:
                        for d in discards(st):
                            for x in set(d.gy):
                                if x in ('TRA','CH') and len(d.st) < 5:
                                    n = d.cp(); n.use('GRY1'); n.gy = rm(n.gy, x)
                                    if x == 'CH': n.st = ad(n.st, 'CHs')
                                    else: n.st = ad(n.st, 'TRAs')
                                    A(n, lg + f' / 그리폰: 1장 버리고 {x} 세트')
                else: A(st, lg)
    # 엑시즈
    if 'CAE' in s.extra:
        l6 = [m for m in s.field if base(m) in LV6 and (XYZ_SHY or m != 'SHY*')]
        for a, b in set(itertools.combinations(sorted(l6), 2)):
            n = s.cp(); n.field = rm(rm(n.field, a), b); n.extra = rm(n.extra, 'CAE'); n.field = ad(n.field, 'CAE'); A(n, f'XYZ CAE <- {a}+{b}')
    F = s.field
    # 딜
    if 'DEAL' in F and 'DEAL1' not in U:
        for x in ('SW','LL'):
            if x in s.deck: n = s.cp(); n.use('DEAL1'); n.deck = rm(n.deck, x); n.gy = ad(n.gy, x); A(n, f'딜: 덱의 {x} 묘지로')
    # 스위트
    if 'SW' in s.gy and 'SW2' not in U and any(base(m) in KIS for m in F) and can_ss(s, 'SW'):
        n = s.cp(); n.use('SW2'); n.gy = rm(n.gy, 'SW'); n.field = ad(n.field, 'SW'); A(n, '스위트 묘지 효과: 특소')
    # 레퀴엠
    if 'REQ' in F and 'REQ1' not in U:
        for x in ('LCT','ENG'):
            for src in ('deck','hand'):
                pool = s.deck if src == 'deck' else s.hand
                if x in pool:
                    n = s.cp(); n.use('REQ1'); n.field = rm(n.field, 'REQ'); n.gy = ad(n.gy, 'REQ')
                    if src == 'deck': n.deck = rm(n.deck, x)
                    else: n.hand = rm(n.hand, x)
                    n.field = ad(n.field, x); lg = f'레퀴엠 릴리스: {src}의 {x} 특소'
                    if x == 'LCT' and 'LCT1' not in n.used:
                        A(n, lg)
                        for y in ('ENG','TRA'):
                            if y in n.deck: m = n.cp(); m.use('LCT1'); m.deck = rm(m.deck, y); m.gy = ad(m.gy, y); A(m, lg + f' / 홍루: 덱의 {y} 묘지로')
                    else: A(n, lg)
    # 장착 (레퀴엠/세퀜티아)
    tgt = any(base(m) in ('ENG','LCT','LUR','FLA') for m in F)
    for e, fl in (('REQ','REQ2'),('SEQ','SEQ2')):
        if fl in U or not tgt or len(s.st) >= 5: continue
        if e in s.gy: n = s.cp(); n.use(fl); n.gy = rm(n.gy, e); n.st = ad(n.st, e + 'e'); A(n, f'{e} 묘지에서 장착')
        if e in F: n = s.cp(); n.use(fl); n.field = rm(n.field, e); n.st = ad(n.st, e + 'e'); A(n, f'{e} 필드에서 장착')
    # 마새데
    if 'ENG' in s.hand and 'ENG1' not in U and 'TRA' in s.deck:
        n = s.cp(); n.use('ENG1'); n.hand = rm(n.hand, 'ENG'); n.gy = ad(n.gy, 'ENG'); n.deck = rm(n.deck, 'TRA'); n.hand = ad(n.hand, 'TRA'); A(n, '마새데 버림: 트락투스 서치')
    if 'ENG' in s.gy and 'ENG3' not in U and can_ss(s, 'ENG'):
        g1 = rm(s.gy, 'ENG')
        for x in set(g1):
            if x in LF:
                n = s.cp(); n.use('ENG3'); n.gy = rm(g1, x)
                if x in LINK or x == 'FLA': n.extra = ad(n.extra, x)
                else: n.deck = ad(n.deck, x)
                n.field = ad(n.field, 'ENG'); A(n, f'마새데 묘지 효과: {x} 되돌리고 특소')
    # 트락투스
    for src in ('hand','st'):
        if 'TRA1' in U: break
        if (src == 'hand' and 'TRA' in s.hand) or (src == 'st' and 'TRAs' in s.st and False):
            for x in ('ENG','LUR','LCT'):
                if x in s.deck:
                    n = s.cp(); n.use('TRA1'); n.hand = rm(n.hand, 'TRA'); n.gy = ad(n.gy, 'TRA'); n.deck = rm(n.deck, x); n.hand = ad(n.hand, x)
                    for d in discards(n): A(d, f'트락투스: {x} 서치 후 1장 버림 (패 {d.hand}, 패사고 {d.fod})')
    if 'TRA' in s.gy and 'TRA2' not in U and 'FLA' in s.extra:
        cand = [('f', m) for m in F if base(m) in LF] + [('h', m) for m in s.hand if m in LF]
        for a, b in set(itertools.combinations(sorted(cand), 2)):
            n = s.cp(); n.use('TRA2'); n.gy = rm(n.gy, 'TRA'); n.ban = ad(n.ban, 'TRA'); sts = [n]
            for src, m in (a, b):
                nx = []
                for st in sts:
                    st = st.cp()
                    if src == 'f': st.field = rm(st.field, m); nx += to_gy(st, m)
                    else: st.hand = rm(st.hand, m); st.gy = ad(st.gy, m); nx += sent(st, m)
                sts = nx
            for st in sts: fla_summon(st, f'트락투스 묘지 효과: {a}+{b} 융합', A)
    # 세퀜티아 융합
    if 'SEQ' in F and 'SEQ1' not in U and 'FLA' in s.extra and len(F) < 6:
        lf = sorted(x for x in s.gy if x in LF)
        for a, b in set(itertools.combinations(lf, 2)):
            n = s.cp(); n.use('SEQ1')
            for x in (a, b):
                n.gy = rm(n.gy, x)
                if x in LINK or x == 'FLA': n.extra = ad(n.extra, x)
                else: n.deck = ad(n.deck, x)
            fla_summon(n, f'세퀜티아: 묘지 {a}+{b} 되돌려 융합', A)
    # E키스킬 / E리일라 소생
    if 'EK' in F and 'EK2' not in U and not any(base(m) in LIL for m in F):
        for x in set(s.gy):
            if x in LIL and can_ss(s, x):
                n = s.cp(); n.use('EK2'); n.gy = rm(n.gy, x); n.field = ad(n.field, x); el_ss(n, x, f'E키스킬: 묘지의 {x} 특소', A)
    if 'EL' in F and 'EL2' not in U and not any(base(m) in KIS for m in F):
        for x in set(s.gy):
            if x in KIS and can_ss(s, x):
                n = s.cp(); n.use('EL2'); n.gy = rm(n.gy, x); n.field = ad(n.field, x); A(n, f'E리일라: 묘지의 {x} 특소')
    # 써니
    if 'SUN' in F and 'SUN1' not in U:
        b0 = s.cp(); b0.use('SUN1'); b0.field = rm(b0.field, 'SUN'); b0.gy = ad(b0.gy, 'SUN')
        ks = [None] + [x for x in set(b0.gy) if x in KIS]; ls = [None] + [x for x in set(b0.gy) if x in LIL]
        for k in ks:
            for l in ls:
                if k is None and l is None: continue
                n = b0.cp(); ok = True
                for x in (k, l):
                    if x is None: continue
                    if not can_ss(n, x): ok = False; break
                    n.gy = rm(n.gy, x); n.field = ad(n.field, x)
                if not ok: continue
                lg = f'써니 릴리스: {k}, {l} 특소'
                if l == 'EL' and k is not None: el_ss(n, 'EL', lg, A)
                elif l == 'EL': el_ss(n, 'EL', lg, A)
                else: A(n, lg)
    # 아바오
    if 'AB' in F and 'AB1' not in U:
        for d in discards(s):
            d.use('AB1')
            for c in set(d.field):
                for r in destroy(d, 'f', c): A(r, f'아바오: 1장 버리고 {c} 파괴')
            for c in set(d.st):
                if c == 'TRAs': continue
                for r in destroy(d, 's', c): A(r, f'아바오: 1장 버리고 {c} 파괴')
            n = d.cp(); n.field = rm(n.field, 'AB'); n.abret = True
            for x in set(n.gy):
                if (x in LF or x in DARK or x == 'FRO') and can_ss(n, x):
                    m = n.cp(); m.gy = rm(m.gy, x); m.field = ad(m.field, x); el_ss(m, x, f'아바오: 1장 버리고 자신 제외, 묘지의 {x} 특소', A)
    # 슈야마
    if any(base(m) == 'SHY' for m in F) and 'SHY1' not in U:
        for c in set(F):
            for r in destroy(s, 'f', c): r.use('SHY1'); A(r, f'슈야마 필드 효과: {c} 파괴')
        for c in set(s.st):
            if c == 'TRAs': continue
            for r in destroy(s, 's', c): r.use('SHY1'); A(r, f'슈야마 필드 효과: {c} 파괴')
    for nm, zone, fl, code in (('SHY','gy','SHY2','SHY*'), ('SH','hand','SH1','SH*')):
        pool = s.gy if zone == 'gy' else s.hand
        if nm in pool and fl not in U:
            tg = [('f', c) for c in set(F) if fiend(c)] + [('s', c) for c in set(s.st) if c == 'CHs']
            for z, c in tg:
                b0 = s.cp(); b0.use(fl)
                if zone == 'gy': b0.gy = rm(b0.gy, nm)
                else: b0.hand = rm(b0.hand, nm)
                # 파괴하고 그 뒤 특소: 특소를 먼저 반영(자리 확보)한 뒤 유발 처리
                b1 = b0.cp()
                if z == 'f': b1.field = rm(b1.field, c); b1.field = ad(b1.field, code); b1.field = ad(b1.field, c)
                else: b1.field = ad(b1.field, code)
                if len(b1.field) > 6 + (1 if z == 'f' else 0): continue
                for r in destroy(b1, z, c): A(r, f'{nm} 효과({zone}): {c} 파괴하고 특소')
    return out
def fla_summon(n, lg, A):
    if len(n.field) >= 6 or 'FLA' not in n.extra: return
    n = n.cp(); n.extra = rm(n.extra, 'FLA'); n.field = ad(n.field, 'FLA'); A(n, lg)
    if 'FLA1' in n.used: return
    for x in set(n.gy):
        if x in LF:
            m = n.cp(); m.use('FLA1'); m.gy = rm(m.gy, x)
            if x in LINK or x == 'FLA':
                h = None
            else:
                h = m.cp(); h.hand = ad(h.hand, x); A(h, lg + f' / 라크리모사: {x} 패로')
            if can_ss(m, x): m.field = ad(m.field, x); A(m, lg + f' / 라크리모사: {x} 특소')
def el_ss(n, x, lg, A):
    """E리일라가 특소된 경우 파괴 효과 분기."""
    A(n, lg)
    if x != 'EL' or 'EL1' in n.used or not any(base(m) in KIS for m in n.field): return
    b = n.cp(); b.use('EL1')
    for c in set(b.field):
        for r in destroy(b, 'f', c): A(r, lg + f' / E리일라: {c} 파괴')
    for c in set(b.st):
        if c == 'TRAs': continue
        for r in destroy(b, 's', c): A(r, lg + f' / E리일라: {c} 파괴')
def score(t):
    s = S(t); f = set(s.field)
    return (('CAE' in f), ('GRY' in f), ('AB' in f or s.abret), ('SUN' in f))
WANT={(True,False,True,True),(False,True,True,True)}
def main():
    import time
    t0=time.time(); LIMIT=float(sys.argv[3]) if len(sys.argv)>3 else 540
    s0 = init(); seen = {hash(s0)}; stack = [(s0, 0, '')]; path = []; best = {}; n = 0; done = True
    while stack:
        cur, dep, lg = stack.pop()
        del path[dep:]; path.append(lg)
        sc = score(cur)
        if sc not in best:
            best[sc] = (list(path), cur)
            if sc[0] and sc[1] and sc[2]: 
                print('GOAL FOUND', sc); break
            if sc in WANT:
                print('PATH', sc); [print('  ', i, l) for i, l in enumerate(path) if l]; print('FINAL', cur, flush=True)
                WANT.discard(sc)
                if not WANT: break
        for nt, l2 in moves(cur):
            h = hash(nt)
            if h not in seen:
                seen.add(h); stack.append((nt, dep + 1, l2))
        n += 1
        if n % 100000 == 0:
            print('..', n, len(seen), len(stack), round(time.time()-t0), flush=True)
            if time.time()-t0 > LIMIT: done = False; print('TIME LIMIT'); break
    print(CFG, 'xyzSHY', XYZ_SHY, 'expanded', n, 'seen', len(seen), 'exhausted', done and not stack)
    for sc in sorted(best, reverse=True):
        print(' 시져/그리폰/아바오/써니 =', sc)
    goal = [sc for sc in best if sc[0] and sc[1] and sc[2]]
    if goal:
        p, fin = best[max(goal)]
        print('PATH'); [print('  ', i, l) for i, l in enumerate(p) if l]
        print('FINAL', fin)
main()
