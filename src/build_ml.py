import json, io, contextlib, collections, sys, os
sys.path.insert(0, '.')
import build
with contextlib.redirect_stdout(io.StringIO()):
    import combos_ml as CB
from ml_names import *
from sim import DB
import subprocess
subprocess.run([sys.executable, 'combos_ml.py'], check=True, capture_output=True)
dat = json.load(open('data_ml.json'))
decks = dat['decks']
dt = json.load(open('bundle_dt.json')); tw = json.load(open('bundle_tw.json'))
GENPOOL = dt['custom']['gen']
GENSET = set(GENPOOL) | set(build.GEN) | {DROLL, MAXC, OGRE, ASH, FUWA, GS, ALL, XOUT, IMP, DOM, '패의 아무 몬스터'}
img = {}
for k, i in IDS.items():
    n = globals()[k]
    if os.path.exists(f'site_all/card/{i}.jpg'): img[n] = f'card/{i}.jpg'
for src in (dt, tw):
    for n, p in src['img'].items(): img.setdefault(n, p)
kinds = {n: v[0] for n, v in DB.items()}
for src in (dt, tw):
    for n, k in src['kinds'].items(): kinds.setdefault(n, k)
kinds.update({DOM: 'eff', XOUT: 'spell', GS: 'spell', ALL: 'spell', IMP: 'trap', DROLL: 'eff', MAXC: 'eff', FUWA: 'eff', OGRE: 'eff', CYN: 'spell'})
dat['kinds'] = kinds
HAND = {s[0]: s[4] for s in CB.SETS}
SCRIPT = {s[0]: s[5] for s in CB.SETS}
SHORT = {SWEN: '스엔', ELD: '엘담', SOL: '둠솔루렛', '패의 아무 몬스터': '아무 몬스터'}

def make(key, short, title, base, builds, base_combos, groups, clinks, notes):
    order = [base] + [b[1] for b in builds]
    pool = {'main': [], 'extra': []}
    for dk in order:
        for p in ('main', 'extra'):
            for n, _ in decks[dk][p]:
                if n not in pool[p]: pool[p].append(n)
    gen = [n for n in GENPOOL] + [n for n in pool['main'] if n in GENSET and n not in GENPOOL]
    allm, alle = set(pool['main']) | set(gen), set(pool['extra'])
    ids = base_combos + [c for b in builds for c in b[2]]
    req = {}
    for sid in ids:
        hm = collections.Counter(h for h in HAND[sid] if h in allm)
        cur = collections.Counter(); mx = collections.Counter(); ex = collections.Counter()
        def take(n):
            cur[n] += 1; mx[n] = max(mx[n], cur[n])
        for st in SCRIPT[sid]:
            for op in st[3]:
                o = op[0]
                if o == 'to_hand' and (len(op) < 3 or op[2] == 'deck'): take(op[1])
                elif o in ('ss', 'put') and len(op) > 3 and op[3] == 'deck': take(op[1])
                elif o == 'to_gy' and op[2] == 'deck': take(op[1])
                elif o == 'st' and len(op) > 3 and op[3] == 'deck': take(op[1])
                elif o == 'ssm':
                    for n, z, src in op[1]:
                        if src == 'deck': take(n)
                elif o == 'shuffle' and op[2] in ('gy', 'ban') and op[1] in allm: cur[op[1]] -= 1
                if o == 'put' and len(op) > 3 and op[3] == 'extra': ex[op[1]] += 1
                elif o in ('fusion', 'synchro', 'link', 'xyz'): ex[op[2]] += 1
                elif o in ('to_gy', 'banish') and op[2] == 'extra': ex[op[1]] += 1
        m = {n: hm[n] + mx[n] for n in set(hm) | set(mx) if n in allm and n not in GENSET and hm[n] + mx[n] > 0}
        e = {n: c for n, c in ex.items() if n in alle}
        req[sid] = {'main': m, 'extra': e}
    for g in groups:
        h = [x for x in HAND[g['items'][0][0]] if x != '패사고']
        g['size'] = len(h); g['cards'] = [SHORT.get(x, x) for x in h]
    basemap = {p: dict(decks[base][p]) for p in ('main', 'extra')}
    bl = []
    for bk, dk, cids, name, how in builds:
        cards = []
        for p in ('main', 'extra'):
            for n, c in decks[dk][p]:
                if c > basemap[p].get(n, 0) and n not in GENSET:
                    cards.append([p, n, c, c])
        bl.append({'key': bk, 'name': name, 'cards': cards, 'combos': cids, 'how': how})
    custom = {'baseCombos': base_combos, 'gen': gen, 'notes': notes, 'key': f'{key}-deck-v' + ('2' if key == 'yb' else '1'),
              'base': {'main': decks[base]['main'], 'extra': decks[base]['extra']}, 'baseMap': basemap, 'pool': pool, 'req': req,
              'groups': groups, 'clinks': clinks, 'builds': bl, 'cut': []}
    allids = [i[0] for g in groups for i in g['items']]
    sel = [{'key': 'my', 'name': short, 'sub': '', 'deck': 'my', 'combos': allids, 'groups': groups, 'clinks': clinks}]
    d = build.page(None, title, sel, img, dat, None, custom)
    d['short'] = short
    return d


ML = make('ml', '멜리스', '멜리스 전개 필드 가이드', 'base',
    [('rt', 'rt', ['m1', 'm2'], '현람', ['현람한 스엔·엘담·헌영으로 레벨 3 2장을 만들어 피안의 흑천사 케루비니 → 성취의 리절도즈로 도어마우스를 제외시키는 다리를 놓는 구축입니다. 초동이 7장 늘지만 덱에서 패에 넣는 효과가 많아 드롤에 약합니다.']),
     ('pk', 'pk', ['m3'], '팬텀 나이츠', ['팬텀 나이츠 둠솔루렛으로 엄브레이지베일을 세트해 레벨 3 2장을 만드는 구축입니다. 서치가 적어 드롤에 강하지만, 리절도즈 소재로 패의 몬스터 1장이 더 필요합니다.'])],
    [],
    [{'name': '현람한 스엔 1장', 'items': [['m1', '어코드 토커 · 파이어월 · 바인더 + GWC']]},
     {'name': '현람한 엘담 1장', 'items': [['m2', '어코드 토커 · 파이어월 · 바인더 + GWC']]},
     {'name': '둠솔루렛 + 아무 몬스터', 'items': [['m3', '어코드 토커 · 파이어월 · 바인더 + GWC']]}],
    {'m1': [{'t': 'Charmer Quartet Combo (Master Duel Meta, Himekami)', 'u': 'https://www.masterduelmeta.com/combo/6ad8a53248005456a59385e9'}],
     'm2': [{'t': 'Charmer Quartet Combo (Master Duel Meta, Himekami)', 'u': 'https://www.masterduelmeta.com/combo/6ad8a53248005456a59385e9'}],
     'm3': [{'t': 'Charmer Quartet Combo (Master Duel Meta, Himekami)', 'u': 'https://www.masterduelmeta.com/combo/6ad8a53248005456a59385e9'}, {'t': '덱 리스트 (Kyo, 2026년 11월)', 'u': 'https://www.masterduelmeta.com/top-decks/master-v/november-2026/maliss/kyo/LOaE8/'}]},
    [])
ML['custom']['defOn'] = ['pk']
json.dump(ML, open('bundle_ml.json', 'w'), ensure_ascii=False)
print('ok', len(ML['combos']))
