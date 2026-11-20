# -*- coding: utf-8 -*-
"""solver 출력(out*.jsonl) → auto_dt.json (가이드용 전개 스크립트·그룹)"""
import json, glob, itertools, collections, re
FULL = {'MU': '드래곤테일 무루루', 'LU': '드래곤테일 루키아스', 'FA': '드래곤테일 파이메나', 'UR': '드래곤테일 우르굴라', 'KE': '케투 드래곤테일',
        'RA': '라후 드래곤테일', 'FL': '드래곤테일 플레임', 'WD': '하얀 용의 낙윤', 'AZ': '알버스의 낙윤', 'EC': '순백의 성녀 에클레시아',
        'CA': '혁의 성녀 카르테시아', 'BF': '낙인융합', 'FV': 'The Fallen & The Virtuous',
        'GN': '패의 몬스터 (마법사족 이외)', 'GW': '패의 마법사족 몬스터', 'GWL': '패의 빛 속성 마법사족 몬스터', 'GL': '패의 빛·어둠 속성 몬스터 (공격력 2500 이상)',
        'ART': '드래곤테일 알자리온', 'ARX': '드래곤테일 알자리온', 'SEC': '사크라멘툼 드라군', 'MIX': '혼효하는 믹시아', 'GRA': '혁언룡 그랑기뇰',
        'ALB': '낙인룡 알비온', 'TIT': '회신룡 배스터드', 'DEV': '성흔을 먹는 용', 'RIN': '격철룡 린드블룸', 'MJ': '빙검룡 미라제이드',
        'LEN': '심연룡 알버 레나투스', 'VOI': '공극의 원성룡', 'AEO': '초월소환수 아이온', 'EDD': '검은 용의 에클레시아', 'ANA': '프레데터 플랜츠 베르테 아나콘다'}
SH = {'MU': '무루루', 'LU': '루키아스', 'FA': '파이메나', 'UR': '우르굴라', 'KE': '케투', 'RA': '라후', 'FL': '플레임', 'WD': '하얀 용의 낙윤', 'AZ': '알버스의 낙윤',
      'EC': '에클레시아', 'CA': '카르테시아', 'BF': '낙인융합', 'FV': 'F&V', 'GN': '마법사족 이외 몬스터', 'GW': '마법사족 몬스터', 'GWL': '빛 속성 마법사족 몬스터',
      'GL': '빛·어둠 공 2500 이상 몬스터', 'ART': '알자리온', 'ARX': '알자리온', 'SEC': '드라군', 'MIX': '믹시아', 'GRA': '그랑기뇰', 'ALB': '알비온', 'TIT': '배스터드',
      'DEV': '성흔을 먹는 용', 'RIN': '린드블룸', 'MJ': '미라제이드', 'LEN': '레나투스', 'VOI': '공극의 원성룡', 'AEO': '아이온', 'EDD': '검은 용의 에클레시아', 'ANA': '아나콘다'}
GEN = ('GN', 'GW', 'GD')
FULL['GD'] = '패의 드래곤족 몬스터 (드래곤테일 이외)'; SH['GD'] = '드래곤족 몬스터'; FULL['GN'] = '패의 몬스터 (그 외)'; SH['GN'] = '그 외 몬스터'
MAIN = {'MU': 2, 'AZ': 1, 'EC': 2, 'CA': 2, 'LU': 1, 'WD': 2, 'FA': 3, 'UR': 1, 'BF': 1, 'KE': 2, 'RA': 1, 'FV': 2, 'FL': 1}
EXTRA = {'TIT': 1, 'ALB': 1, 'MJ': 1, 'LEN': 1, 'GRA': 1, 'RIN': 1, 'VOI': 1, 'ART': 2, 'SEC': 1, 'DEV': 1, 'MIX': 1, 'AEO': 1, 'EDD': 1, 'ANA': 1}
ORDER = ['WD', 'EC', 'CA', 'BF', 'LU', 'MU', 'FA', 'UR', 'KE', 'RA', 'AZ', 'FV', 'GN', 'GW', 'GD']
LEFT = {'GN': .4, 'GW': .4, 'GD': .4, 'CA': .1, 'EC': .1, 'WD': .08, 'BF': .08, 'MU': .05, 'LU': .05, 'UR': .05, 'FA': .1, 'FV': 1.0}

def josa(t):
    def bat(w):
        c = w[-1]
        if c == 'V': return False
        if not ('가' <= c <= '힣'): return False
        return (ord(c) - 0xAC00) % 28 != 0
    for n in set(SH.values()) | set(FULL.values()):
        b = bat(n)
        for a, x in (('를', '을'), ('는', '은'), ('가', '이'), ('와', '과')):
            t = t.replace(n + (a if b else x) + ' ', n + (x if b else a) + ' ')
    return t


import re
DMS = ('LU', 'MU', 'FA', 'UR')
R = {}
for f in sorted(glob.glob('r2/*.jsonl')):
    for l in open(f):
        try: d = json.loads(l)
        except Exception: continue
        if d.get('res'): R[tuple(sorted(d['hand'].split(','), key=ORDER.index))] = d
print('hands', len(R), 'capped', [','.join(h) for h, d in R.items() if d.get('cap')])
sc = lambda h: R[h]['res'][0]['sc'] if h in R else 0.0

def keep(h):
    s = sc(h)
    if len(h) == 1: return s >= 1.5
    base = 0
    for k in range(1, len(h)):
        for sub in itertools.combinations(range(len(h)), k):
            hs = tuple(h[i] for i in sub); rest = [h[i] for i in range(len(h)) if i not in sub]
            base = max(base, sc(hs) + sum(LEFT.get(c, 0) for c in rest))
    base = max(base, sum(LEFT.get(c, 0) for c in h))
    return s >= base + 0.5 and s >= 2.0

def sigf(h, fil):
    r = R[h]['res'][0]; nm = lambda l: tuple(sorted('*' if x == fil else x for x in l))
    return (round(r['sc'], 2), nm(r['fld']), nm(r['st']), nm(r['h']))

kept = sorted([h for h in R if keep(h)], key=lambda h: (len(h), [ORDER.index(c) for c in h]))
# ---- 채우는 패(드래곤테일 몬스터 DM / 그 외 몬스터 NDM)가 달라도 결과가 같으면 묶기 ----
cand = collections.defaultdict(lambda: collections.defaultdict(list))
for h in kept:
    seen = set()
    for i, c in enumerate(h):
        if (c in DMS or c in GEN) and c not in seen:
            seen.add(c); core = h[:i] + h[i+1:]
            if not core: continue
            cand[core][sigf(h, c)].append((c, h))
buckets = [(core, lst) for core, m in cand.items() for lst in m.values() if len(lst) >= 2]
buckets.sort(key=lambda b: (-len(b[1]), len(b[0]), [ORDER.index(c) for c in b[0]]))
used = set(); entries = []   # (rep hand, core, fillers or None, rep filler)
for core, lst in buckets:
    lst = [(c, h) for c, h in lst if h not in used]
    if len(lst) < 2: continue
    for c, h in lst: used.add(h)
    fills = [c for c, h in lst]
    repc, reph = sorted(lst, key=lambda x: (x[0] not in GEN, ORDER.index(x[0])))[0]
    entries.append((reph, core, fills, repc))
for h in kept:
    if h not in used: entries.append((h, h, None, None))

def flabel(core, fills):
    g = [c for c in GEN if c in fills]; d = [c for c in DMS if c in fills]
    poss = [c for c in DMS if core.count(c) < MAIN[c]]
    parts = []
    if len(g) == len(GEN): parts.append('NDM')
    elif g: parts.append(GLAB.get(frozenset(g)) or ' / '.join(SH[t] for t in g))
    if d and len(d) == len(poss) and len(d) >= 2: parts.append('DM')
    elif d: parts.append('DM(' + '·'.join(SH[c] for c in d) + ')')
    return '/'.join(parts)
GLAB = {frozenset(('GN', 'GW')): 'NDM(드래곤족 이외)', frozenset(('GN', 'GD')): 'NDM(마법사족 이외)', frozenset(('GW', 'GD')): 'NDM(마법사족·드래곤족)',
        frozenset(('GN',)): 'NDM(그 외)', frozenset(('GW',)): 'NDM(마법사족)', frozenset(('GD',)): 'NDM(드래곤족)'}
def cname(cards):
    cnt = collections.Counter(cards); out = []
    for c in sorted(cnt, key=ORDER.index):
        nm = GLAB[frozenset((c,))] if c in GEN else SH[c]
        out.append(nm + (f' {cnt[c]}장' if cnt[c] > 1 else ''))
    return out

NAMES = sorted(set(SH.values()) | {'알자리온(소생)'}, key=len, reverse=True)
NRE = re.compile('|'.join(re.escape(n) for n in NAMES))
def br(t): return NRE.sub(lambda m: '[' + m.group(0) + ']', t)
def board(r, gl=None):
    b = lambda l: ', '.join('[' + (gl if (gl and x in GEN) else SH[x]) + ']' for x in l)
    p = ['패: ' + (b(r['h']) if r['h'] else '-'), '필드: ' + (b(r['fld']) if r['fld'] else '-')]
    if r['st']: p.append('세트: ' + b(r['st']))
    if 'RIN' in r['gy']: p.append('묘지: [린드블룸]')
    return ' / '.join(p)

WHY = {'알버스의 낙윤 호출': ('검은 용의 에클레시아 / 에클레시아', '상대 메인 페이즈 (프리 체인)', '덱·묘지의 알버스의 낙윤을 불러 패 1장을 버리고 상대 몬스터와 융합 (알버스의 낙윤 효과는 1턴에 1번)'),
       '검은 용의 에클레시아(': ('검은 용의 에클레시아', '상대 메인 페이즈 (프리 체인)', '자신을 엔드 페이즈까지 제외하고 덱·묘지의 카르테시아·하얀 용의 낙윤·알버스의 낙윤 특수 소환'),
       '드라군': ('사크라멘툼 드라군', '상시', '상대 필드의 특수 소환된 드래곤족·마법사족 몬스터는 효과를 발동할 수 없음'),
       '미라제이드': ('빙검룡 미라제이드', '상대 턴 (프리 체인)', '엑스트라 덱의 알버스 융합 몬스터를 묘지로 보내고 필드의 몬스터 1장 제외'),
       '플레임': ('세트한 드래곤테일 플레임', '상대가 마법을 발동했을 때 등 (일반 함정)', '앞면 마법 1장 효과 무효 → 묘지·제외의 드래곤테일 카드 1장을 덱으로 → 1장 드로우'),
       'F&V': ('세트한 The Fallen & The Virtuous', '상대 턴 (속공 마법)', '엑스트라 덱의 알버스 표기 몬스터를 묘지로 보내 앞면 카드 1장 파괴, 또는 에클레시아가 필드·묘지에 있으면 묘지의 몬스터 소생'),
       '믹시아 → 아이온': ('혼효하는 믹시아', '상대 메인 페이즈 (프리 체인)', '믹시아 효과로 융합'),
       '카르테시아 → 믹시아': ('필드의 카르테시아', '상대 메인 페이즈 (프리 체인)', '카르테시아(마법사족) + 패·필드의 마법사족 이외 몬스터로 믹시아 융합'),
       '카르테시아 상대 턴': ('필드의 카르테시아', '상대 메인 페이즈 (프리 체인)', '패·필드의 몬스터로 레벨 8 이상 융합'),
       '파이메나 → 믹시아': ('패의 파이메나', '상대 메인 페이즈 (프리 체인)', '자신을 버리고 패·필드의 마법사족 + 마법사족 이외로 믹시아 융합'),
       '파이메나 → 알자리온': ('패의 파이메나', '상대 메인 페이즈 (프리 체인)', '자신을 버리고 드래곤테일 몬스터 + 패의 몬스터로 알자리온 융합 → 패에서 쓴 소재 수만큼 상대 몬스터를 패로 + 소재가 된 드래곤테일의 세트 효과'),
       '무루루 → 알자리온': ('필드의 무루루', '상대 메인 페이즈 (프리 체인)', '무루루 + 패의 몬스터로 알자리온 융합 → 상대 몬스터를 패로, 무루루 효과로 드래곤테일 마법·함정 세트 후 상대 몬스터 1장 효과 무효'),
       '린드블룸': ('묘지의 격철룡 린드블룸', '상대 턴', '묘지의 하얀 용의 낙윤을 소생(→ 에클레시아 → 알버스의 낙윤 융합)하거나 린드블룸을 소생해 엑스트라 덱 몬스터 효과 무효 후 몬스터 1장 바운스')}
CAT = {'알버스의 낙윤 호출': '제거 · 융합 소재로', '검은 용의 에클레시아(': '상대 턴 발동', '드라군': '락 · 조건부', '미라제이드': '제외 · 필드 몬스터', '플레임': '무효 · 필드 앞면 마법', 'F&V': '파괴 · 앞면 카드',
       '믹시아 → 아이온': '제외', '카르테시아 → 믹시아': '제외', '카르테시아 상대 턴': '상대 턴 발동', '파이메나 → 믹시아': '제외', '파이메나 → 알자리온': '바운스 · 패로', '무루루 → 알자리온': '바운스 + 몬스터 효과 무효', '린드블룸': '무효 · 엑스트라 덱 몬스터 효과'}
def opp(r):
    out = []
    for w in r['why']:
        for k, v in WHY.items():
            if w.startswith(k):
                cat = CAT[k]; txt = v[2]
                if '아이온(' in w:
                    det = w[w.index('아이온(') + 4:-1]; cat = '제외 · ' + det.split(': ')[0]
                    txt = v[2] + ' → 같은 메인 페이즈에 믹시아와 속성이 다른 융합 몬스터(필드·묘지)를 제외해 아이온 융합 소환 → ' + det.split(': ')[1]
                out.append(['[' + cat + '] ' + v[0], v[1], txt]); break
    return out

MZ = ['M3', 'M2', 'M4', 'M1', 'M5']; SZ = ['S1', 'S2', 'S3', 'S4', 'S5']
CPP = {'GN': '비드테몹(기타)', 'GW': '비드테몹(마법사족)', 'GD': '비드테몹(드래곤족)'}
def script(handc, r, gl=None):
    FULLX = dict(FULL); SHX = dict(SH)
    if gl:
        for g in GEN: FULLX[g] = '패의 ' + gl + ' 몬스터'; SHX[g] = gl
    else:
        for g in GEN: SHX[g] = GLAB[frozenset((g,))]
    D = list(collections.Counter(MAIN).elements())
    for c in handc:
        if c in D: D.remove(c)
    prev = {'H': list(handc), 'F': [], 'T': [], 'G': [], 'D': D, 'X': list(collections.Counter(EXTRA).elements())}
    z = {}; out = []
    for st in r['steps']:
        cur = {k: ['ART' if x == 'ARX' else x for x in st[k]] for k in 'HFTGDX'}
        lg = st['lg']
        segs = lg.split(' / ')
        def segof(c):
            key = CPP.get(c, SH[c])
            for i, s in enumerate(segs):
                if key in s: return i
            return 0
        bins = [dict(rm=[], mid=[], pl=[]) for _ in segs]
        cards = set(x for k in 'HFTGDX' for x in cur[k] + prev[k])
        for c in sorted(cards):
            neg, pos = [], []
            for k in 'HFTGDX':
                d = cur[k].count(c) - prev[k].count(c)
                (pos if d > 0 else neg).extend([k] * abs(d))
            si = segof(c)
            while neg or pos:
                s = neg.pop(0) if neg else 'B'; t = pos.pop(0) if pos else 'B'
                n = FULLX[c]
                srcn = {'H': 'hand', 'F': 'field', 'G': 'gy', 'D': 'deck', 'X': 'extra', 'B': 'ban'}.get(s)
                if s == 'T':
                    zn = next(k for k, v in z.items() if v == n and k[0] == 'S'); del z[zn]
                    bins[0]['rm'].append(('st_gy', zn)); continue
                b = bins[si]
                if t == 'G': (b['rm'] if s == 'F' else b['mid']).append(('to_gy', n, srcn))
                elif t == 'H': (b['rm'] if s == 'F' else b['mid']).append(('to_hand', n, srcn))
                elif t == 'D': (b['rm'] if s == 'F' else b['mid']).append(('shuffle', n, srcn))
                elif t == 'B': (b['rm'] if s == 'F' else b['mid']).append(('banish', n, srcn))
                elif t == 'F': b['pl'].append((c, n, srcn))
                elif t == 'T': b['pl'].append((c, n, srcn, 'T'))
        # 제거를 먼저 전부 처리해야 존이 비므로 rm 은 세그먼트 순서대로 앞에서부터 적용
        first = True
        # 패에서 발동한 마법은 마법·함정 존에 놓인 것을 먼저 보여 준 뒤 처리
        for c in ('KE', 'RA', 'BF', 'FV'):
            o = ('to_gy', FULLX[c], 'hand')
            if o in bins[0]['mid'] and (segs[0].startswith(SH[c] + ' 발동')):
                zn = next(k for k in SZ if k not in z)
                bins[0]['mid'].remove(o); bins[0]['rm'].insert(0, ('st_gy', zn))
                t0 = josa(segs[0].split(': ')[0] + ' ').strip()
                out.append([br(t0), '', '패에서 마법·함정 존에 발동', [['st', FULLX[c], zn, 'hand']], True])
                segs[0] = segs[0].replace(' 발동(패)', ' 효과 처리').replace('낙인융합 발동', '낙인융합 효과 처리')
                break
        for i, s in enumerate(segs):
            b = bins[i]; ops = b['rm'] + b['mid']
            for o in b['rm']:
                if o[0] != 'st_gy' and o[-1] == 'field':
                    zn = next(k for k, v in z.items() if v == o[1] and k[0] != 'S'); del z[zn]
            b['pl'].sort(key=lambda p: (lambda j: j if j >= 0 else 10**6)(s.find(CPP.get(p[0], SH[p[0]]))))
            for p in b['pl']:
                c, n, srcn = p[:3]
                if len(p) == 4:
                    zn = next(k for k in SZ if k not in z); z[zn] = n; ops.append(('st', n, zn, srcn)); continue
                zn = 'ER' if c == 'ANA' else next(k for k in MZ if k not in z)
                z[zn] = n
                if srcn == 'extra': ops.append(('put', n, zn, 'extra', True))
                elif srcn == 'hand' and s.startswith(SH[c] + ' 일반 소환'): ops.append(('ns', n, zn))
                else: ops.append(('ss', n, zn, srcn))
            txt = s
            for g in GEN: txt = txt.replace(CPP[g], SHX[g])
            txt = josa(txt + ' ').strip()
            title, res = txt, ''
            if ': ' in txt: title, res = txt.split(': ', 1)
            title, res = br(title), br(res)
            if not ops and out and not first:
                out[-1][2] = (out[-1][2] + ' · ' if out[-1][2] else '') + title + (': ' + res if res else '')
                continue
            if not ops and out and first:
                pass
            out.append([('체인 · ' if (not first and not lg.startswith(('엔드 페이즈', '메인 페이즈 종료'))) else '') + title, '', res, [list(o) for o in ops], True])
            first = False
        prev = cur
    return out

def tagof(r): return ('성흔 보존' if 'DEV' in r['ex'] else '성흔 사용') + ' · ' + ('드라군 남김' if 'SEC' in r['fld'] else '드라군 안 남김')
auto = []; groups = []
entries.sort(key=lambda e: (len(e[0]), [ORDER.index(c) for c in e[1]], e[2] is None))
for rep, core, fills, repc in entries:
    res = R[rep]['res']; n = len(rep); best = res[0]
    m1, m2 = (0.5, 0.5) if n < 3 else (0.3, -1)
    cand = [best]
    bd = 'DEV' in best['ex']; bs = 'SEC' in best['fld']
    o = [r for r in res if ('DEV' in r['ex']) != bd and r['sc'] >= best['sc'] - m1]
    if o: cand.append(o[0])
    o = [r for r in res if ('DEV' in r['ex']) == bd and ('SEC' in r['fld']) != bs and r['sc'] >= best['sc'] - m2]
    if o: cand.append(o[0])
    gl = None
    if fills:
        lab = flabel(core, fills); name = ' + '.join(cname(core) + [lab])
        if repc in GEN: gl = lab
    else:
        name = ' + '.join(cname(rep)) + (' 1장' if n == 1 else '')
    items = []
    for i, r in enumerate(cand):
        cid = 'x_' + '_'.join(c.lower() for c in rep) + f'_{i+1}'
        handn = [('패의 ' + gl + ' 몬스터' if (gl and c in GEN) else FULL[c]) for c in rep]
        tg = tagof(r) if len(cand) > 1 else ''
        auto.append({'id': cid, 'title': name + (f' ({tg})' if tg else ''), 'sub': f'전수 탐색 결과 · 평가 {r["sc"]:.1f}', 'hand': handn,
                     'script': script(rep, r, gl), 'board': board(r, gl), 'opp': opp(r)})
        items.append([cid, (tg + ' → ' if tg else '') + board(r, gl)])
    groups.append({'name': name, 'items': items})
json.dump({'combos': auto, 'groups': groups}, open('auto_dt.json', 'w'), ensure_ascii=False)
print('entries', len(entries), 'merged', sum(1 for e in entries if e[2]), 'combos', len(auto), 'by size', collections.Counter(len(e[0]) for e in entries))
