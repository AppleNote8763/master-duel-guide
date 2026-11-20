import json, io, contextlib, collections, sys
sys.path.insert(0, '.')
import build
with contextlib.redirect_stdout(io.StringIO()):
    import combos as CB
    exec(open('kinds.py').read())
dat = json.load(open('data.json'))
decks = dat['decks']
img = json.load(open('img2.json'))
dt = json.load(open('bundle_dt.json'))
GENPOOL = dt['custom']['gen']
for n in GENPOOL:
    if n in dt['img']: img.setdefault(n, dt['img'][n])
    if n in dt['kinds']: dat['kinds'].setdefault(n, dt['kinds'][n])
GENSET = set(GENPOOL) | set(build.GEN)
HAND = {s[0]: s[4] for s in CB.SETS}
SCRIPT = {s[0]: s[5] for s in CB.SETS}
SHORT = {'Live☆Twin 키스킬': '키스킬', 'Live☆Twin 리일라': '리일라', 'Live☆Twin 키스킬 프로스트': '프로스트', 'Live☆Twin 리일라 스위트': '스위트',
         'Live☆Twin 트러블상': '트러블상', 'Live☆Twin 리일라 트리트': '트리트', '새크리파이스 데먼 로터스': '로터스', '암흑의 초래신': '초래신',
         '마를 새기는 데먼스미스': '마를 새기는 데먼스미스', '칠정의 해문': '해문', '시크릿 패스프레이즈': '패스프레이즈', '나이트메어 쓰론': '쓰론', '데먼스미스 트락투스': '트락투스', '마굉신 루리': '루리', '스피릿 오브 유벨': '스피릿', '홍루의 마 라크리모사': '홍루의 마 라크리모사'}

# ---- 상대 턴 무브 (순서 없음) ----
AB, CAE, SUN, GRY, RA, CH, DES, DJ = CB.AB, CB.CAE, CB.SUN, CB.GRY, CB.RA, CB.CH, CB.DES, CB.DJ
LK = '에스:피 리틀나이트'
O = {
 'AB': (AB, '메인 페이즈 (프리 체인, 1턴에 1번)', '패 1장을 버리고 필드의 카드 1장 파괴, 또는 자신을 엔드 페이즈까지 제외하고 묘지의 빛·어둠 속성 몬스터 특수 소환'),
 'CAE': (CAE, '특수 소환하는 카드·효과가 발동했을 때 (프리 체인)', '소재 1개를 떼고 그 발동을 무효로 하고 파괴. 소재 수만큼 쓸 수 있음'),
 'SUN': (SUN, '프리 체인', '자신을 릴리스하고 묘지의 키스킬·리일라를 1장씩 특수 소환 → Evil★Twin 리일라 효과로 상대 카드 1장 파괴, Evil★Twin 키스킬 효과로 1장 드로우'),
 'RA': (RA, '상대 메인 페이즈 (프리 체인)', '상대가 특수 소환한 앞면 몬스터 1장을 대상으로, 그 몬스터와 라기아만 소재로 어둠 속성 링크 몬스터 링크 소환 (상대 몬스터를 소재로 치움)'),
 'GRY': (GRY, '상시', '필드의 특수 소환된 몬스터는 링크 상태가 아니면 효과를 발동할 수 없음 (내 몬스터도 해당하므로 링크 상태 유지)'),
 'DES': (DES, '프리 체인 (1턴에 1번)', '장착된 링크 몬스터의 링크 수 합계만큼 필드의 앞면 카드 효과를 턴 끝까지 무효'),
 'CH': (f'세트한 {CH}', '상대 턴', f'묘지의 {RA} 특수 소환 → 상대 메인 페이즈에 상대 몬스터와 링크해 {LK}로 (리틀나이트: 상대가 카드·효과를 발동하면 내 몬스터를 포함한 앞면 몬스터 2장을 엔드 페이즈까지 제외)'),
 'DJ': (DJ, '상대가 몬스터 효과를 발동했을 때', '소재 2개를 떼고 그 발동을 무효로 하고 500 데미지 (니비루 대비)'),
 'PH': ('팬텀 오브 유벨', '상대가 몬스터 효과를 발동했을 때', '자신을 릴리스하고, 상대가 발동한 효과를 "내가 내 패·덱·필드의 유벨 몬스터 1장을 파괴"로 바꿈 (덱의 스피릿 오브 유벨을 깨면 유벨을 꺼낼 수 있음)'),
 'VA': ('데카네로그－발드라스', '상대가 카드·효과를 발동했을 때 (1턴에 1번)', '소재 1개를 떼고 그 발동을 무효 → 소재를 1개 더 떼면 필드의 카드 1장 파괴. 엑시즈 소환한 이 카드가 파괴되면 필드의 카드 1장 파괴'),
 'LAC': ('데먼스미스 라크리모사 (필드)', '상시', '상대 몬스터 공격력 -600'),
}
OPP = {'fr1': ['GRY', 'CAE', 'AB', 'CH'], 'fr2': ['CAE', 'SUN', 'AB'], 'fr3': ['GRY', 'SUN', 'AB'], 'gm1': ['GRY', 'DES', 'SUN', 'AB'], 'ap1': ['GRY', 'CAE', 'SUN', 'AB'], 'y1': ['VA', 'PH', 'AB', 'CH'], 'y2': ['VA', 'PH', 'AB', 'CH'], 'y3': ['VA', 'PH', 'AB', 'CH'], 'y4': ['CAE', 'VA', 'PH', 'AB', 'CH'],
       'my': ['RA', 'SUN', 'CAE', 'AB'], 'g1': ['GRY', 'SUN', 'AB', 'LAC'], 'g2': ['GRY', 'CAE', 'AB'], 'f1': ['CAE', 'AB'], 'f2': ['CAE', 'SUN', 'AB'],
       'v1': ['RA', 'CAE', 'SUN', 'AB'], 'o1': ['DJ', 'AB'], 'o2': ['CAE'], 't1': ['GRY', 'DES', 'AB', 'CH'], 'fs1': ['CAE'], 'fs2': ['CAE'], 'fs3': ['CAE'], 'fs4': ['CAE'], 'ph1': ['PH', 'VA', 'AB', 'CH'], 'ph2': ['PH', 'VA', 'AB', 'CH'], 'ph3': ['PH', 'VA', 'AB', 'CH'], 'yd1': ['PH', 'CAE', 'CH'], 'yt1': ['VA', 'PH', 'AB', 'CH'], 'yf1': ['VA', 'PH', 'AB', 'CH'], 'ts1': ['RA', 'SUN', 'CAE', 'AB'], 'sp1': ['RA', 'SUN', 'CAE', 'AB']}

for c in dat['combos']:
    c['opp'] = [list(O[k]) for k in OPP.get(c['id'], [])]


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
        if '또는 리일라' in g['name'] and '리일라' not in g['cards']: g['cards'].append('리일라')
    basemap = {p: dict(decks[base][p]) for p in ('main', 'extra')}
    bl = []
    for bk, dk, cids, name, how in builds:
        cards = []
        for p in ('main', 'extra'):
            for n, c in decks[dk][p]:
                if c > basemap[p].get(n, 0) and n not in GENSET:
                    cards.append([p, n, c, c])
        bl.append({'key': bk, 'name': name, 'cards': cards, 'combos': cids, 'how': how})
    # 추가 구축을 카드 1장 단위로 쪼갬 (드래곤테일과 같은 방식)
    if key == 'tw':
        seen = []
        for b in bl:
            for p, n, c, mn in b['cards']:
                if (p, n) not in seen: seen.append((p, n))
        bids = [c for b in bl for c in b['combos']]
        bl = []
        for p, n in seen:
            cids = [s for s in bids if req[s][p].get(n, 0) > basemap[p].get(n, 0)]
            if not cids: continue
            bl.append({'key': 'c:' + n, 'name': n, 'cards': [[p, n, 1, 0]], 'uses': [], 'combos': cids, 'how': CARD_HOW.get(n, [])})
    custom = {'baseCombos': base_combos, 'gen': gen, 'notes': notes, 'key': f'{key}-deck-v' + ('3' if key == 'yb' else '2' if key == 'tw' else '1'),
              'base': {'main': decks[base]['main'], 'extra': decks[base]['extra']}, 'baseMap': basemap, 'pool': pool, 'req': req,
              'groups': groups, 'clinks': clinks, 'builds': bl, 'cut': []}
    allids = [i[0] for g in groups for i in g['items']]
    sel = [{'key': 'my', 'name': short, 'sub': '', 'deck': 'my', 'combos': allids, 'groups': groups, 'clinks': clinks}]
    d = build.page(None, title, sel, img, dat, None, custom)
    d['short'] = short
    return d


CARD_HOW = {
 '언체인드소울 샤바라': ['언체인드소울 샤바라: 야마로 서치해 패에서 특수 소환합니다. 언체인드 쌍극과 같이 넣으면 프로스트 1장 전개(arca.live 강의)와 디에스이레·쌍극 전개가 켜집니다.'],
 '언체인드 쌍극': ['언체인드 쌍극: 샤바라가 묘지로 가면 덱에서 세트합니다. 세트한 쌍극을 리일라로 파괴해 덱에서 슈야마를 꺼내고, 상대 턴에는 라기아를 되살립니다.'],
 '데먼스미스 디에스이레': ['데먼스미스 디에스이레: 세퀜티아 융합으로 세우는 무효 몬스터입니다. 넣으면 엑스트라 덱에서 1장을 빼야 합니다.'],
 'Live☆Twin 리일라 트리트': ['Live☆Twin 리일라 트리트: 재단마인 저지 버스터(랭크 2)를 내기 위한 레벨 2 몬스터입니다.'],
 'No.65 재단마인 저지 버스터': ['No.65 재단마인 저지 버스터: 먼저 깔아 두고 전개해서 니비루를 맞아도 무효 1장이 남게 합니다. 리일라 트리트와 같이 넣습니다.'],
}
TW = make('tw', '이빌트윈 데먼스미스', '이빌트윈 데먼스미스 전개 필드 가이드', 'mine',
    [('shch', 'd_shch', ['fr1'], '샤바라 · 쌍극', ['언체인드소울 샤바라와 언체인드 쌍극을 넣으면 프로스트 1장으로 시져 · 그리폰 · 아＝바오 아 쿠를 세우는 전개(arca.live 강의)가 켜집니다. 메인 덱에서 2장을 빼야 합니다.']),
     ('des', 'd_des', ['gm1'], '데먼스미스 디에스이레', ['데먼스미스 디에스이레를 넣으면 세퀜티아 융합으로 디에스이레를 세우고 그리폰까지 내는 전개(game8)가 켜집니다. 엑스트라 덱에서 1장을 빼야 합니다.']),
     ('kim', 'vid_own', ['o1'], '재단마인', ['No.65 재단마인 저지 버스터를 먼저 깔아 두고 전개해서, 니비루를 맞아도 무효 1장이 남게 하는 니비루 대비 구축입니다. 저지 버스터를 내기 위해 리일라 트리트를 같이 넣습니다.']),
     ('ref', 'twin', ['t1'], '언체인드 쌍극', ['언체인드 쌍극과 디에스이레를 넣어 디에스이레 무효 3과 그리폰 봉인을 같이 세우는 구축입니다.'])],
    ['my', 'ap1', 'fr2', 'fr3', 'ts1', 'sp1'],
    [{'name': '키스킬 또는 리일라 1장', 'items': [['my', '기본: 시져·써니·아바오 → 상대 턴 그리폰'], ['ap1', '시져 · 그리폰 · 써니 · 아바오 (선턴 그리폰)'], ['gm1', '써니 · 디에스이레 · 그리폰 · 아바오']]},
     {'name': '프로스트 1장', 'items': [['fr2', '시져 · 써니 · 아바오'], ['fr3', '그리폰 · 써니 · 아바오'], ['fr1', '시져 · 그리폰 · 아바오 + 쌍극 (샤바라 · 쌍극 필요)']]},
     {'name': '트러블상 1장', 'items': [['ts1', '기본: 시져·써니·아바오 → 상대 턴 그리폰 (키스킬 1장과 같음)']]},
     {'name': '시크릿 패스프레이즈 1장', 'items': [['sp1', '기본: 시져·써니·아바오 → 상대 턴 그리폰 (키스킬 1장과 같음)']]},
     {'name': '키스킬 + 트리트 (니비루 대비)', 'items': [['o1', '저지 버스터 · 레퀴엠 · 아바오']]},
     {'name': '키스킬 1장 (디에스이레·쌍극)', 'items': [['t1', '그리폰 · 디에스이레 무효 3 · 아바오 + 쌍극']]}],
    {'my': [{'t': '기본 엔진 영상 (김빠방 1판)', 'u': 'https://www.youtube.com/watch?v=NBOZD7IEm6Q&t=29s'}], 'ts1': [{'t': '기본 엔진 영상 (김빠방 1판, 트러블상 시작)', 'u': 'https://www.youtube.com/watch?v=NBOZD7IEm6Q&t=29s'}], 'sp1': [{'t': '기본 엔진 영상 (김빠방 1판)', 'u': 'https://www.youtube.com/watch?v=NBOZD7IEm6Q&t=29s'}],
     'fr1': [{'t': 'arca.live: [4금 마듀] 데먼트윈 강의 (3-2 프로스트 전개 영상)', 'u': 'https://arca.live/b/yugioh/166421796'}],
     'gm1': [{'t': 'game8: イビルツインデッキの回し方 (2026-08 갱신)', 'u': 'https://game8.jp/yugioh-masterduel/437636'}, {'t': 'game8: デモンスミスイビルツイン (2026-11 갱신 구축)', 'u': 'https://game8.jp/yugioh-masterduel/667670'}],
     'ap1': [{'t': 'appmedia: イビルツインデッキの回し方', 'u': 'https://appmedia.jp/master_duel/27311569'}], 'v1': [{'t': '영상 1판 0:29~1:58', 'u': 'https://www.youtube.com/watch?v=NBOZD7IEm6Q&t=29s'}],
     'o1': [{'t': '전개 설명 글 (콤보 1)', 'u': 'https://ygoprodeck.com/deck/fiendsmith-live-twins-post-alin-593378'}],
     't1': [{'t': '전개 설명 글 (Master Duel Meta)', 'u': 'https://www.masterduelmeta.com/top-decks/dice-rally---fusion-synchro-link/february-2026/live%E2%98%86twin/waffle/doT4a'}]},
    [])
YB = make('yb', '유벨 데먼스미스', '유벨 데먼스미스 전개 필드 가이드', 'yb_mine', [], ['y1', 'y2', 'y3', 'yf1', 'y4', 'yt1', 'yd1', 'ph1', 'ph2', 'ph3'],
    [{'name': '로터스 1장', 'items': [['y1', '발드라스 · 팬텀 오브 유벨 · 아바오 · 쌍극'], ['yd1', '드롤 맞았을 때: 팬텀 · 시져 · 페인 · 쌍극']]},
     {'name': '나이트메어 쓰론 1장', 'items': [['yt1', '발드라스 · 팬텀 오브 유벨 · 아바오(필드 잔류) · 쌍극']]},
     {'name': '초래신 또는 해문 1장', 'items': [['y2', '발드라스 · 팬텀 오브 유벨 · 아바오(필드 잔류) · 쌍극']]},
     {'name': '마를 새기는 데먼스미스 1장', 'items': [['y3', '발드라스 · 팬텀 오브 유벨 · 아바오 · 쌍극']]},
     {'name': '트락투스 1장', 'items': [['yf1', '발드라스 · 팬텀 오브 유벨 · 아바오 · 쌍극 (유벨 콤보 3과 같은 흐름)']]},
     {'name': '초래신 + 로터스', 'items': [['y4', '시져 2 · 발드라스 · 팬텀 오브 유벨 · 아바오 · 쌍극 (최강)']]},
     {'name': '로터스 + 스피릿 + 0/0 악마족 (팬텀 선출)', 'items': [['ph1', '유발 없음: 팬텀 2 · 발드라스 · 아바오 · 쌍극'], ['ph2', '로터스에 하루 우라라: 팬텀이 받아냄 → 발드라스 · 팬텀 · 아바오(잔류) · 쌍극'], ['ph3', '스쿼머 서치에 드롤: 팬텀이 받아냄 → 평소 로터스 필드']]}],
    {}, [])
json.dump(TW, open('bundle_tw.json', 'w'), ensure_ascii=False)
json.dump(YB, open('bundle_yb.json', 'w'), ensure_ascii=False)
print('ok', len(TW['combos']), len(YB['combos']))
