# -*- coding: utf-8 -*-
"""드래곤테일 낙인(기본 파츠) 선공 1턴 전수 탐색기.
카드 텍스트(ko-KR.cdb) 기준으로 효과를 규칙화. 상대 필드는 비어 있다고 가정."""
import sys, itertools
from collections import Counter

# race: W=wizard D=dragon O=other / attr: L,D(ark),E,Wa,F,Wi
P = {
 'MU': dict(r='D', a='D', lv=3, atk=1100, dt=1), 'LU': dict(r='W', a='E', lv=4, atk=1800, dt=1),
 'FA': dict(r='W', a='Wa', lv=5, atk=1300, dt=1), 'UR': dict(r='D', a='F', lv=6, atk=2400, dt=1),
 'WD': dict(r='D', a='D', lv=4, atk=1800, az=1), 'AZ': dict(r='D', a='D', lv=4, atk=1800, az=1),
 'EC': dict(r='W', a='L', lv=4, atk=1500, tuner=1), 'CA': dict(r='W', a='L', lv=4, atk=1500, tuner=1),
 'GN': dict(r='O', a='F', lv=3, atk=0), 'GW': dict(r='W', a='Wi', lv=1, atk=0),
 'GWL': dict(r='W', a='L', lv=1, atk=0), 'GL': dict(r='O', a='L', lv=11, atk=3000),
 # extra
 'ART': dict(r='D', a='E', lv=8, atk=3000, dt=1, fus=1), 'SEC': dict(r='D', a='L', lv=8, atk=3000, fus=1),
 'MIX': dict(r='W', a='D', lv=8, atk=2700, fus=1), 'GRA': dict(r='W', a='L', lv=8, atk=2500, fus=1),
 'ALB': dict(r='D', a='D', lv=8, atk=2500, fus=1, maz=1), 'TIT': dict(r='D', a='D', lv=8, atk=2500, fus=1, maz=1),
 'DEV': dict(r='O', a='D', lv=8, atk=3000, fus=1, maz=1), 'RIN': dict(r='O', a='D', lv=8, atk=2500, fus=1, maz=1),
 'MJ': dict(r='O', a='D', lv=8, atk=3000, fus=1, maz=1), 'LEN': dict(r='D', a='D', lv=8, atk=2500, fus=1, maz=1),
 'VOI': dict(r='D', a='L', lv=8, atk=3000, fus=1), 'AEO': dict(r='O', a='D', lv=10, atk=3800, fus=1),
 'EDD': dict(r='W', a='L', lv=8, atk=2500, syn=1), 'ANA': dict(r='O', a='D', lv=0, atk=500, link=1),
}
SPELLS = {'KE', 'RA', 'FL', 'BF', 'FV'}
MAIN = {'MU': 2, 'AZ': 1, 'EC': 2, 'CA': 2, 'LU': 1, 'WD': 2, 'FA': 3, 'UR': 1, 'BF': 1, 'KE': 2, 'RA': 1, 'FV': 2, 'FL': 1}
EXTRA = {'TIT': 1, 'ALB': 1, 'MJ': 1, 'LEN': 1, 'GRA': 1, 'RIN': 1, 'VOI': 1, 'ART': 2, 'SEC': 1, 'DEV': 1, 'MIX': 1, 'AEO': 1, 'EDD': 1, 'ANA': 1}
KO = {'MU': '무루루', 'LU': '루키아스', 'FA': '파이메나', 'UR': '우르굴라', 'KE': '케투', 'RA': '라후', 'FL': '플레임',
      'WD': '하얀 용의 낙윤', 'AZ': '알버스의 낙윤', 'EC': '에클레시아', 'CA': '카르테시아', 'BF': '낙인융합', 'FV': 'F&V',
      'GN': '비드테몹(기타)', 'GW': '비드테몹(마법사족)', 'GWL': '비드테몹(빛 마법사족)', 'GL': '비드테몹(빛·어둠, 공 2500+)',
      'ART': '알자리온', 'SEC': '드라군', 'MIX': '믹시아', 'GRA': '그랑기뇰', 'ALB': '알비온', 'TIT': '배스터드', 'DEV': '성흔을 먹는 용',
      'RIN': '린드블룸', 'MJ': '미라제이드', 'LEN': '레나투스', 'VOI': '공극의 원성룡', 'AEO': '아이온', 'EDD': '검은 용의 에클레시아', 'ANA': '아나콘다'}
ko = lambda xs: '·'.join(KO[x] for x in xs)
isld = lambda n: P[n]['a'] in ('L', 'D')
isaz = lambda n: P[n].get('az')
isdt = lambda n: P[n].get('dt')
ised = lambda n: n in EXTRA

def add(t, *xs): return tuple(sorted(t + xs))
def rem(t, *xs):
    l = list(t)
    for x in xs: l.remove(x)
    return tuple(l)

class S:
    __slots__ = ('ph', 'hand', 'fld', 'st', 'gy', 'ban', 'deck', 'ex', 'fl', 'sent')
    def __init__(s, **k):
        for a in S.__slots__: setattr(s, a, k[a])
    def key(s): return (s.ph, s.hand, s.fld, s.st, s.gy, s.ban, s.deck, s.ex, s.fl, s.sent)
    def cp(s, **k):
        d = {a: getattr(s, a) for a in S.__slots__}; d.update(k); return S(**d)
    def has(s, f): return f in s.fl
    def flag(s, *f): return s.cp(fl=s.fl | frozenset(f))

def start(hand):
    deck = Counter(MAIN)
    for c in hand:
        if c in deck:
            deck[c] -= 1
            if deck[c] < 0: return None
    return S(ph='main', hand=tuple(sorted(hand)), fld=(), st=(), gy=(), ban=(), deck=tuple(sorted(deck.elements())),
             ex=tuple(sorted(Counter(EXTRA).elements())), fl=frozenset(), sent=frozenset())

# ---- 융합 소재 조합 ----
def mats_for(target, pools, s):
    """pools: dict origin->tuple of names. return list of material lists [(origin,name),...]"""
    items = [(o, n) for o, ns in pools.items() for n in sorted(set(ns)) for _ in range(min(2, ns.count(n))) if n in P]
    out = set()
    def pairs(pa, pb):
        for i, x in enumerate(items):
            for j, y in enumerate(items):
                if i == j: continue
                if pa(x) and pb(y): out.add(tuple(sorted((x, y))))
    nm = lambda x: x[1]
    if target == 'ART':
        dts = [x for x in items if isdt(x[1])]
        hs = [x for x in items if x[0] == 'hand']
        for d in dts:
            rest = [h for h in hs if h is not d]
            for k in (1, 2):
                for c in itertools.combinations(rest, k):
                    if d in c: continue
                    cc = tuple(sorted((d,) + c))
                    if len(set(map(id, (d,) + c))) == len(cc): out.add(cc)
    elif target == 'SEC': pairs(lambda x: P[nm(x)]['r'] == 'D', lambda y: P[nm(y)]['r'] == 'W')
    elif target == 'MIX': pairs(lambda x: P[nm(x)]['r'] == 'W', lambda y: P[nm(y)]['r'] != 'W')
    elif target == 'GRA': pairs(lambda x: nm(x) == 'CA', lambda y: isld(nm(y)))
    elif target == 'ALB': pairs(lambda x: isaz(nm(x)), lambda y: P[nm(y)]['a'] == 'L')
    elif target == 'TIT': pairs(lambda x: isaz(nm(x)), lambda y: P[nm(y)]['atk'] >= 2500)
    elif target == 'MJ': pairs(lambda x: isaz(nm(x)), lambda y: ised(nm(y)))
    elif target == 'LEN': pairs(lambda x: isaz(nm(x)), lambda y: P[nm(y)]['r'] == 'D' and nm(y) != 'LEN')
    elif target == 'VOI': pairs(lambda x: P[nm(x)]['r'] == 'D' and isld(nm(x)), lambda y: P[nm(y)]['r'] == 'D')
    elif target == 'DEV':
        for c in itertools.combinations(range(len(items)), 3):
            xs = [items[i] for i in c]
            for p in itertools.permutations(xs):
                if isaz(nm(p[0])) and isld(nm(p[1])): out.add(tuple(sorted(xs))); break
    # 같은 origin·이름 중복은 실제 장수 초과 금지
    res = []
    for m in out:
        ok = True
        for (o, n), c in Counter(m).items():
            if pools[o].count(n) < c: ok = False
        if 'LEN' in [n for _, n in m]: ok = False  # 레나투스는 소재 불가
        if ok: res.append(list(m))
    return res

DTSET = ('KE', 'RA', 'FL')

def ed_ok(s, name):
    if s.has('noss'): return False
    p = P[name]
    if s.has('l8') and not (p['lv'] == 8 and (p.get('fus') or p.get('syn'))): return False
    if s.has('fonly') and not p.get('fus'): return False
    return name in s.ex and len(s.fld) < 5 + 0

def after_ed(s, name):
    return s if P[name].get('fus') else s.flag('nf')

def resolve_sets(s, names, log):
    """소재로 묘지에 간 드래곤테일의 세트 효과(이름당 1턴 1번). 분기 리스트 반환."""
    states = [(s, log)]
    for n in sorted(set(names)):
        if n not in ('MU', 'LU', 'FA', 'UR'): continue
        nxt = []
        for st, lg in states:
            if st.has('set' + n): nxt.append((st, lg)); continue
            opts = [c for c in DTSET if c in st.deck]
            if not opts or len(st.st) >= 5: nxt.append((st, lg)); continue
            for c in opts:
                nxt.append((st.cp(deck=rem(st.deck, c), st=add(st.st, c)).flag('set' + n), lg + f' / {KO[n]} 효과: 덱에서 {KO[c]} 세트'))
        states = nxt
    return states

def do_fusion(s, target, mats, how, banish=False):
    """mats: [(origin,name)] origin in hand/fld/deck/gy. 결과 분기 [(state, log)]"""
    hand, fld, deck, gy, ban = s.hand, s.fld, s.deck, s.gy, s.ban
    nh = 0
    for o, n in mats:
        if o == 'hand': hand = rem(hand, n); nh += 1
        elif o == 'fld': fld = rem(fld, n)
        elif o == 'deck': deck = rem(deck, n)
        elif o == 'gy': gy = rem(gy, n)
        if banish: ban = add(ban, n)
        else: gy = add(gy, n)
    if len(fld) >= 5: return []
    sent = s.sent
    fl = s.fl
    names = [n for _, n in mats]
    if not banish:
        if any(P[n].get('fus') for n in names): fl = fl | {'fgy'}
        sent = sent | frozenset(n for n in names if n in ('TIT', 'ALB', 'DEV', 'LEN'))
    s2 = s.cp(hand=hand, fld=add(fld, target), deck=deck, gy=gy, ban=ban, ex=rem(s.ex, target), sent=sent, fl=fl)
    s2 = after_ed(s2, target)
    src = ', '.join(f"{KO[n]}({ {'hand':'패','fld':'필드','deck':'덱','gy':'묘지'}[o]})" for o, n in mats)
    log = f"{how}: {src} → {KO[target]} 융합 소환" + (' (소재 제외)' if banish else '')
    outs = [(s2, log)] if banish else resolve_sets(s2, names, log)
    res = []
    for st, lg in outs:
        res += on_fusion_summon(st, target, nh, lg)
    return res

def on_fusion_summon(s, target, nh, log):
    if target == 'ART' and not s.has('artB') and nh > 0:
        cand = sorted(set(n for n in s.gy if n in P and not ised(n)))
        pool = [n for n in cand for _ in range(min(nh, s.gy.count(n)))]
        k = min(nh, len(pool))
        res = []
        seen = set()
        for c in itertools.combinations(pool, k):
            c = tuple(sorted(c))
            if c in seen: continue
            seen.add(c)
            st = s.cp(gy=rem(s.gy, *c), hand=add(s.hand, *c)).flag('artB')
            res.append((st, log + f' / 알자리온 효과: 묘지의 {ko(c)}를 패로'))
        return res or [(s, log)]
    if target == 'GRA' and not s.has('graS'):
        res = []
        for c in ('TIT', 'ALB', 'DEV', 'RIN', 'LEN'):
            if c in s.ex:
                st = s.cp(ex=rem(s.ex, c), gy=add(s.gy, c), sent=s.sent | {c}).flag('graS', 'fgy')
                res.append((st, log + f' / 그랑기뇰 효과: 엑스트라 덱의 {KO[c]}를 묘지로'))
        return res or [(s, log)]
    if target == 'ALB' and not s.has('albF'):
        res = [(s, log)]
        s1 = s.flag('albF')
        pools = {'hand': s1.hand, 'fld': s1.fld, 'gy': tuple(n for n in s1.gy if n in P)}
        for t in ('GRA', 'SEC', 'MIX', 'TIT', 'MJ', 'LEN', 'DEV', 'VOI', 'ART'):
            if not ed_ok(s1, t): continue
            for m in mats_for(t, pools, s1):
                res += do_fusion(s1, t, m, log + ' / 알비온 효과', banish=True)
        return res
    return [(s, log)]

def summon_triggers(s, name, log):
    """일반/특수 소환 시 유발: 루키아스 서치, 하얀 용의 낙윤 → 에클레시아"""
    if name == 'LU' and not s.has('luS'):
        res = []
        for c in ('MU', 'FA', 'UR'):
            if c in s.deck:
                res.append((s.cp(deck=rem(s.deck, c), hand=add(s.hand, c)).flag('luS'), log + f' / 루키아스 효과: 덱에서 {KO[c]} 서치'))
        return res or [(s, log)]
    if name == 'WD' and not s.has('wdE') and len(s.fld) < 5:
        res = []
        for o, pool in (('패', s.hand), ('덱', s.deck), ('묘지', s.gy)):
            if 'EC' in pool:
                kw = dict(hand=rem(s.hand, 'EC')) if o == '패' else dict(deck=rem(s.deck, 'EC')) if o == '덱' else dict(gy=rem(s.gy, 'EC'))
                res.append((s.cp(fld=add(s.fld, 'EC'), **kw).flag('wdE'), log + f' / 하얀 용의 낙윤 효과: {o}의 에클레시아 특수 소환'))
        return res or [(s, log)]
    return [(s, log)]

def moves(s):
    out = []
    A = out.extend
    if s.ph == 'main':
        noss = s.has('noss')
        # 일반 소환
        if not s.has('ns') and len(s.fld) < 5:
            for n in sorted(set(s.hand)):
                if n in P and P[n]['lv'] <= 4 and not ised(n) and n[0] != 'G':
                    s2 = s.cp(hand=rem(s.hand, n), fld=add(s.fld, n)).flag('ns')
                    A(summon_triggers(s2, n, f'{KO[n]} 일반 소환'))
        # 하얀 용의 낙윤 ①
        if 'WD' in s.hand and not s.has('wdS') and not noss and len(s.fld) < 5 and not (s.has('nf') and False):
            for c in sorted(set(x for x in s.ex if P[x].get('maz'))):
                s2 = s.cp(hand=rem(s.hand, 'WD'), fld=add(s.fld, 'WD'), ex=rem(s.ex, c), gy=add(s.gy, c), sent=s.sent | {c}).flag('wdS', 'l8', 'fgy')
                A(summon_triggers(s2, 'WD', f'하얀 용의 낙윤 효과(패): 비용 {KO[c]} → 특수 소환'))
        # 에클레시아 ②
        if 'EC' in s.fld and not s.has('ecR') and not noss:
            for o, pool in (('패', s.hand), ('덱', s.deck)):
                for c in ('WD', 'AZ'):
                    if c in pool:
                        kw = dict(hand=rem(s.hand, c)) if o == '패' else dict(deck=rem(s.deck, c))
                        s2 = s.cp(fld=add(rem(s.fld, 'EC'), c), gy=add(s.gy, 'EC'), **kw).flag('ecR')
                        A(summon_triggers(s2, c, f'에클레시아 효과: 자신 릴리스 → {o}의 {KO[c]} 특수 소환'))
        # 카르테시아 ①
        if 'CA' in s.hand and not s.has('caS') and not noss and len(s.fld) < 5 and any(isaz(x) for x in s.fld + s.gy if x in P):
            out.append((s.cp(hand=rem(s.hand, 'CA'), fld=add(s.fld, 'CA')).flag('caS'), '카르테시아 효과(패): 특수 소환'))
        # 카르테시아 ②
        if 'CA' in s.fld and not s.has('caF'):
            s1 = s.flag('caF'); pools = {'hand': s1.hand, 'fld': s1.fld}
            for t in ('GRA', 'SEC', 'MIX', 'ALB', 'TIT', 'MJ', 'LEN', 'DEV', 'VOI', 'ART'):
                if ed_ok(s1, t):
                    for m in mats_for(t, pools, s1): A(do_fusion(s1, t, m, '카르테시아 효과'))
        # 파이메나 ①
        if 'FA' in s.hand and not s.has('faF'):
            s1 = s.cp(hand=rem(s.hand, 'FA'), gy=add(s.gy, 'FA')).flag('faF'); pools = {'hand': s1.hand, 'fld': s1.fld}
            for t in ('ART', 'SEC', 'MIX', 'GRA', 'ALB', 'TIT', 'LEN', 'VOI'):
                if ed_ok(s1, t):
                    for m in mats_for(t, pools, s1): A(do_fusion(s1, t, m, '파이메나 효과(패에서 버림)'))
        # 무루루 ①
        if 'MU' in s.fld and not s.has('muF') and ed_ok(s, 'ART'):
            s1 = s.flag('muF', 'fonly'); pools = {'hand': s1.hand, 'fld': s1.fld}
            for m in mats_for('ART', pools, s1): A(do_fusion(s1, 'ART', m, '무루루 효과(필드)'))
        # 케투
        if not s.has('ke') and ('KE' in s.hand or 'KE' in s.st):
            src = 'hand' if 'KE' in s.hand else 'st'
            base = s.cp(hand=rem(s.hand, 'KE')) if src == 'hand' else s.cp(st=rem(s.st, 'KE'))
            base = base.cp(gy=add(base.gy, 'KE')).flag('ke')
            for c in ('MU', 'LU', 'FA', 'UR'):
                if c in base.deck:
                    out.append((base.cp(deck=rem(base.deck, c), hand=add(base.hand, c)), f"케투 발동({'패' if src=='hand' else '세트'}): 덱에서 {KO[c]} 서치"))
        # 라후
        if not s.has('ra') and ('RA' in s.hand or 'RA' in s.st) and ed_ok(s, 'ART'):
            src = 'hand' if 'RA' in s.hand else 'st'
            base = s.cp(hand=rem(s.hand, 'RA')) if src == 'hand' else s.cp(st=rem(s.st, 'RA'))
            base = base.cp(gy=add(base.gy, 'RA')).flag('ra', 'fonly')
            pools = {'hand': base.hand, 'fld': base.fld, 'deck': tuple(n for n in base.deck if n in P)}
            for m in mats_for('ART', pools, base):
                if sum(1 for o, _ in m if o == 'deck') > 1: continue
                A(do_fusion(base, 'ART', m, f"라후 발동({'패' if src=='hand' else '세트'})"))
        # 낙인융합
        if 'BF' in s.hand and not s.has('bf') and not s.has('nf') and not noss:
            base = s.cp(hand=rem(s.hand, 'BF'), gy=add(s.gy, 'BF')).flag('bf', 'fonly')
            A(bf_effect(base, '낙인융합 발동'))
        # 우르굴라 ②
        if 'UR' in s.gy and not s.has('urG'):
            for c in ('LU', 'FA'):
                if c in s.gy:
                    out.append((s.cp(gy=rem(s.gy, 'UR', c), deck=add(s.deck, 'UR'), hand=add(s.hand, c)).flag('urG'), f'우르굴라 묘지 효과: 자신을 덱으로, 묘지의 {KO[c]}를 패로'))
        # 드라군 ③
        if 'SEC' in s.fld and not s.has('secR') and not noss and len(s.fld) < 5:
            ds = sorted(set(n for n in s.gy if n in P and P[n]['r'] == 'D' and not ised(n)))
            ws = sorted(set(n for n in s.gy if n in P and P[n]['r'] == 'W' and not ised(n)))
            for d in ds:
                for w in ws:
                    for up, dn in ((d, w), (w, d)):
                        s2 = s.cp(gy=rem(s.gy, d, w), fld=add(s.fld, up), deck=add(s.deck, dn)).flag('secR')
                        A(summon_triggers(s2, up, f'드라군 효과: 묘지의 {KO[up]} 특수 소환, {KO[dn]}는 덱 맨 아래로'))
        # 검은 용의 에클레시아 싱크로
        if ed_ok(s, 'EDD'):
            for t in ('EC', 'CA'):
                if t in s.fld:
                    for n in sorted(set(s.fld)):
                        if n != t and P[n]['lv'] == 4 and not P[n].get('tuner') and not ised(n):
                            s2 = s.cp(fld=add(rem(s.fld, t, n), 'EDD'), gy=add(s.gy, t, n), ex=rem(s.ex, 'EDD')).flag('nf')
                            out.append((s2, f'검은 용의 에클레시아 싱크로 소환: {KO[t]} + {KO[n]}'))
        # 검은 용의 에클레시아 ①
        if 'EDD' in s.fld and not s.has('eddB') and not noss:
            base = s.cp(fld=rem(s.fld, 'EDD')).flag('eddB', 'eddOut')
            for o, pool in (('덱', s.deck), ('묘지', s.gy)):
                for c in ('CA', 'EC', 'WD', 'AZ'):
                    if c in pool:
                        kw = dict(deck=rem(s.deck, c)) if o == '덱' else dict(gy=rem(s.gy, c))
                        s2 = base.cp(fld=add(base.fld, c), **kw)
                        A(summon_triggers(s2, c, f'검은 용의 에클레시아 효과: 자신을 엔드 페이즈까지 제외 → {o}의 {KO[c]} 특수 소환'))
        # 아나콘다
        if ed_ok(s, 'ANA') and not s.has('l8'):
            effs = [n for n in s.fld]
            for a, b in set(itertools.combinations(sorted(effs), 2)):
                gy = add(s.gy, a, b); fl = s.fl | {'nf'}
                if P[a].get('fus') or P[b].get('fus'): fl = fl | {'fgy'}
                sent = s.sent | frozenset(x for x in (a, b) if x in ('TIT', 'ALB', 'DEV', 'LEN'))
                s2 = s.cp(fld=add(rem(s.fld, a, b), 'ANA'), gy=gy, ex=rem(s.ex, 'ANA'), fl=fl, sent=sent)
                out.append((s2, f'아나콘다 링크 소환: {KO[a]} + {KO[b]}'))
        if 'ANA' in s.fld and not s.has('anaE') and 'BF' in s.deck and not noss:
            base = s.cp(deck=rem(s.deck, 'BF'), gy=add(s.gy, 'BF')).flag('anaE')
            for st, lg in bf_effect(base, '아나콘다 효과(LP 2000, 덱의 낙인융합을 묘지로)'):
                out.append((st.flag('noss'), lg + ' → 이후 특수 소환 불가'))
        # F&V (패, 내 턴)
        A(fv_moves(s))
    else:
        # 엔드 페이즈
        if 'TIT' in s.sent and 'TIT' in s.gy and not s.has('titE'):
            for c in ('WD', 'AZ'):
                if c in s.deck:
                    if len(s.fld) < 5 and not s.has('noss'):
                        s2 = s.cp(deck=rem(s.deck, c), fld=add(s.fld, c)).flag('titE')
                        A(summon_triggers(s2, c, f'엔드 페이즈 배스터드: 덱의 {KO[c]} 특수 소환'))
                    out.append((s.cp(deck=rem(s.deck, c), hand=add(s.hand, c)).flag('titE'), f'엔드 페이즈 배스터드: 덱의 {KO[c]}를 패로'))
        if 'ALB' in s.sent and 'ALB' in s.gy and not s.has('albE'):
            if 'FV' in s.deck and len(s.st) < 5:
                out.append((s.cp(deck=rem(s.deck, 'FV'), st=add(s.st, 'FV')).flag('albE'), '엔드 페이즈 알비온: 덱의 F&V 세트'))
            for c in ('FV', 'BF'):
                if c in s.deck:
                    out.append((s.cp(deck=rem(s.deck, c), hand=add(s.hand, c)).flag('albE'), f'엔드 페이즈 알비온: 덱의 {KO[c]}를 패로'))
        A(fv_moves(s))
    return out

def fv_moves(s):
    out = []
    if 'FV' not in s.hand or s.has('fv'): return out
    base = s.cp(hand=rem(s.hand, 'FV'), gy=add(s.gy, 'FV')).flag('fv')
    # ① 엑스트라 덱의 알버스 표기 몬스터를 묘지로, 앞면 카드 1장 파괴
    for t in sorted(set(s.fld)):
        if t in ('EDD', 'SEC', 'MIX', 'MJ'): continue  # 굳이 파괴하지 않을 카드
        for c in sorted(set(x for x in s.ex if P[x].get('maz') and x in ('TIT', 'ALB', 'DEV', 'LEN', 'RIN'))):
            fl = base.fl | {'fgy'}
            sent = base.sent | {c} | ({t} if t in ('TIT', 'ALB', 'DEV', 'LEN') else frozenset())
            s2 = base.cp(ex=rem(base.ex, c), fld=rem(base.fld, t), gy=add(base.gy, c, t), sent=sent, fl=fl)
            out.append((s2, f'F&V 발동(패): 엑스트라 덱의 {KO[c]}를 묘지로, 자신의 {KO[t]} 파괴'))
    # ② 에클레시아가 필드·묘지에 있으면 묘지의 몬스터 소생 (메인 덱 몬스터만 취급)
    if any(x in ('EC', 'EDD') for x in s.fld + s.gy) and not s.has('noss') and len(s.fld) < 5:
        for c in sorted(set(n for n in s.gy if n in P and not ised(n))):
            s2 = base.cp(gy=rem(base.gy, c), fld=add(base.fld, c))
            out += summon_triggers(s2, c, f'F&V 발동(패): 묘지의 {KO[c]} 특수 소환')
    return out

def bf_effect(base, how):
    out = []
    pools = {'hand': base.hand, 'fld': base.fld, 'deck': tuple(n for n in base.deck if n in P)}
    for t in ('ALB', 'TIT', 'MJ', 'LEN'):
        if ed_ok(base, t):
            for m in mats_for(t, pools, base): out += do_fusion(base, t, m, how)
    return out

# ---- 평가: 상대 턴 방해 수 추정 ----
def finalize(s):
    """엔드 페이즈 자동 처리: 성흔을 먹는 용·레나투스 서치, 카르테시아·에클레시아 회수, 검은 용의 에클레시아 복귀"""
    lg = []
    if 'DEV' in s.sent and 'DEV' in s.gy and 'FV' in s.deck and not s.has('devE'):
        s = s.cp(deck=rem(s.deck, 'FV'), hand=add(s.hand, 'FV')).flag('devE'); lg.append('엔드 페이즈 성흔을 먹는 용: 덱의 F&V를 패로')
    if 'LEN' in s.sent and 'LEN' in s.gy and 'BF' in s.deck:
        s = s.cp(deck=rem(s.deck, 'BF'), hand=add(s.hand, 'BF')); lg.append('엔드 페이즈 레나투스: 덱의 낙인융합을 패로')
    if s.has('fgy'):
        for c in ('CA', 'EC'):
            if c in s.gy:
                s = s.cp(gy=rem(s.gy, c), hand=add(s.hand, c)); lg.append(f'엔드 페이즈 {KO[c]}: 묘지에서 패로')
    if s.has('eddOut') and len(s.fld) < 5:
        s = s.cp(fld=add(s.fld, 'EDD'), fl=s.fl - {'eddOut'}); lg.append('엔드 페이즈: 검은 용의 에클레시아 복귀')
    if 'FV' in s.hand and len(s.st) < 5:
        s = s.cp(hand=rem(s.hand, 'FV'), st=add(s.st, 'FV')); lg.append('패의 F&V는 세트해 둠')
    return s, lg

def end_results(s):
    """메인 페이즈 상태 s에서 엔드 페이즈로 넘어갔을 때의 최종 상태들 [(state, logs)]"""
    e0 = s.cp(ph='end')
    if 'DEV' in e0.sent and 'DEV' in e0.gy and 'FV' in e0.deck:
        e0 = e0.cp(deck=rem(e0.deck, 'FV'), hand=add(e0.hand, 'FV')).flag('devE'); pre = ['엔드 페이즈 성흔을 먹는 용: 덱의 F&V를 패로']
    else: pre = []
    res = []; seen = {e0.key()}; stack = [(e0, pre)]
    while stack:
        e, lg = stack.pop()
        ms = moves(e)
        f, lg2 = finalize(e)
        res.append((f, lg + lg2))
        for e2, l in ms:
            k = e2.key()
            if k not in seen:
                seen.add(k); stack.append((e2, lg + [l]))
    return res

def score(s):
    f, h, g, st = s.fld, s.hand, s.gy, s.st
    v = 0.0; why = []
    def a(x, t):
        nonlocal v; v += x; why.append(t)
    azdeck = any(c in s.deck or c in g for c in ('AZ', 'WD'))
    if 'EDD' in f and azdeck: a(1.0, '검은 용의 에클레시아(알버스의 낙윤 호출 → 상대 몬스터 융합)')
    if 'EC' in f and ('AZ' in s.deck or 'WD' in s.deck or 'AZ' in h): a(1.0, '에클레시아 릴리스 → 알버스의 낙윤 융합')
    if 'SEC' in f: a(1.0, '드라군(특수 소환된 드래곤·마법사족 효과 봉인)')
    if 'MJ' in f: a(1.2, '미라제이드 제외')
    if 'FL' in st: a(0.8, '플레임(마법 무효)')
    if 'FV' in st: a(1.0, 'F&V')
    fus_other = [x for x in f + g if x in P and P[x].get('fus') and x != 'MIX']
    mixaeon = False
    if 'MIX' in f and 'AEO' in s.ex and fus_other: a(2.0, '믹시아 → 아이온(2장 제외)'); mixaeon = True
    elif 'MIX' in f: a(0.2, '믹시아')
    # 필드 카르테시아: 상대 턴 융합
    if 'CA' in f:
        wiz = True; non = [x for x in f + h if x in P and P[x]['r'] != 'W']
        if 'MIX' in s.ex and non and 'AEO' in s.ex and not mixaeon and (fus_other or any(P[x].get('fus') for x in non)):
            a(2.0, '카르테시아 → 믹시아 → 아이온'); mixaeon = True
        else: a(0.5, '카르테시아 상대 턴 융합')
    # 패의 파이메나
    if 'FA' in h:
        h2 = rem(h, 'FA')
        wizs = [x for x in f + h2 if x in P and P[x]['r'] == 'W']
        nons = [x for x in f + h2 if x in P and P[x]['r'] != 'W']
        dts = [x for x in f + h2 if x in P and isdt(x)]
        hm = [x for x in h2 if x in P]
        if not mixaeon and 'MIX' in s.ex and 'AEO' in s.ex and wizs and nons and (fus_other or any(P[x].get('fus') for x in f)):
            a(2.0, '파이메나 → 믹시아 → 아이온'); mixaeon = True
        elif 'ART' in s.ex and dts and hm and not (len(hm) == 1 and dts == hm):
            a(1.0, '파이메나 → 알자리온(상대 몬스터 바운스)')
        else: a(0.2, '파이메나(다음 턴)')
    if 'MU' in f and 'ART' in s.ex and [x for x in h if x in P and x != 'FA']: a(1.0, '무루루 → 알자리온(바운스)')
    if 'RIN' in g and any(x in g for x in ('WD', 'AZ')): a(1.0, '린드블룸(하얀 용의 낙윤 소생 또는 무효)')
    if 'GRA' in f: a(0.2, '그랑기뇰')
    for x in f:
        if x in ('ART', 'ALB', 'TIT', 'VOI', 'DEV', 'LEN', 'WD', 'LU'): v += 0.15
    v += 0.3 * h.count('CA') + 0.3 * h.count('EC') + 0.2 * h.count('WD') + 0.2 * h.count('BF') + 0.15 * sum(1 for x in h if x in ('MU', 'LU', 'UR'))
    v += 0.4 * sum(1 for x in h if x in ('GN', 'GW', 'GWL', 'GL'))
    v += 0.15 * (('KE' in st) + ('RA' in st))
    return round(v, 2), why

def board(s):
    parts = []
    if s.fld: parts.append(ko(s.fld))
    if s.st: parts.append(ko(s.st) + ' 세트')
    if s.hand: parts.append('패: ' + ko(s.hand))
    key = [x for x in s.gy if x in ('RIN',)]
    if key: parts.append('묘지: ' + ko(key))
    return ' + '.join(parts)

def solve(hand, limit=int(__import__('os').environ.get('LIM','3000000'))):
    s0 = start(hand)
    if s0 is None: return None
    par = {s0.key(): None}
    stack = [s0]
    best = {}
    n = 0; capped = False
    while stack:
        s = stack.pop()
        n += 1
        if n > limit: capped = True; break
        for fs, elog in end_results(s):
            sc, why = score(fs)
            sig = (fs.fld, fs.st, fs.hand, 'RIN' in fs.gy)
            if sig not in best or best[sig][0] < sc: best[sig] = (sc, s.key(), why, board(fs), elog)
        for s2, lg in moves(s):
            k = s2.key()
            if k not in par:
                par[k] = (s.key(), lg); stack.append(s2)
    res = sorted(best.values(), key=lambda x: -x[0])
    def path(k):
        out = []
        while par[k]:
            k, lg = par[k]; out.append(lg)
        return out[::-1]
    return [(sc, bd, why, path(k) + elog) for sc, k, why, bd, elog in res[:8]], n, capped

if __name__ == '__main__':
    hand = sys.argv[1].split(',')
    import time; t = time.time()
    res, n, cap = solve(hand)
    print('states', n, round(time.time() - t, 1), 's')
    for sc, bd, why, p in res[:int(sys.argv[2]) if len(sys.argv) > 2 else 3]:
        print('\n==', sc, bd); print('   방해:', ' | '.join(why))
        for l in p: print('   -', l)
