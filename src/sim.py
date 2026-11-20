"""전개 시뮬레이터: 카드 위치를 추적하고 엑스트라 덱 소환 위치와 링크 소재 수치를 룰에 맞는지 검증한다."""
import json, itertools, sys

# 카드 DB: 이름 -> (종류, 링크수치 또는 레벨, 링크 마커)
A = {'L': (-1, 0), 'R': (1, 0), 'U': (0, -1), 'D': (0, 1), 'UL': (-1, -1), 'UR': (1, -1), 'DL': (-1, 1), 'DR': (1, 1)}
DB = {
 # 유벨
 '새크리파이스 데먼 로터스': ('eff', 1, None), '스피릿 오브 유벨': ('eff', 10, None), '유벨': ('eff', 10, None),
 '유벨－다스 압쇼이리히 리터': ('eff', 11, None), '헬그레이브 스쿼머': ('eff', 1, None),
 '나이트메어 페인': ('spell', 0, None), '나이트메어 쓰론': ('field', 0, None),
 '암흑의 초래신': ('eff', 2, None), '혼돈의 소환신': ('eff', 1, None), '칠정의 해문': ('spell', 0, None),
 # 데먼스미스
 '마를 새기는 데먼스미스': ('eff', 6, None), '홍루의 마 라크리모사': ('eff', 4, None), '마굉신 루리': ('eff', 1, None),
 '데먼스미스 트락투스': ('spell', 0, None),
 '사로스＝난나': ('link', 2, ['UR', 'U']), '데먼스미스 레퀴엠': ('link', 1, ['D']),
 '데먼스미스 세퀜티아': ('link', 2, ['DL', 'DR']), '데먼스미스 라크리모사': ('fusion', 6, None),
 '데먼스미스 디에스이레': ('fusion', 9, None), '에어리얼 이터': ('fusion', 6, None),
 # 언체인드 등
 '언체인드소울킹 야마': ('link', 2, ['DL', 'DR']), '언체인드소울 라기아': ('link', 2, ['D', 'U']),
 '언체인드소울 샤바라': ('eff', 6, None), '언체인드 쌍극': ('trap', 0, None),
 '빛 없는 그림자 아＝바오 아 쿠': ('link', 4, ['L', 'DL', 'DR', 'R']), '에스:피 리틀나이트': ('link', 2, ['L', 'R']),
 'DDD 노도대왕 이그제큐티브 시져': ('xyz', 6, None), '데카네로그－발드라스': ('xyz', 10, None),
 '팬텀 오브 유벨': ('fusion', 9, None),
 # 이빌트윈
 'Live☆Twin 키스킬': ('eff', 2, None), 'Live☆Twin 리일라': ('eff', 2, None), 'Live☆Twin 리일라 스위트': ('eff', 2, None),
 'Evil★Twin Ki-sikil Deal': ('link', 1, ['R']), 'Evil★Twin 키스킬': ('link', 2, ['R', 'D']),
 'Evil★Twin 리일라': ('link', 2, ['L', 'D']), "Evil★Twin's 트러블 써니": ('link', 4, ['L', 'D', 'R', 'U']),
 '트로이메어 그리폰': ('link', 4, ['L', 'U', 'R', 'D']),
 '패사고': ('eff', 0, None),
 '언체인드소울 슈야마': ('eff', 6, None), 'Live☆Twin 키스킬 프로스트': ('eff', 2, None), 'Evil★Twin 키스킬 딜': ('link', 1, ['R']),
 'Live☆Twin 리일라 트리트': ('eff', 2, None), 'No.65 재단마인 저지 버스터': ('xyz', 2, None), '네크로입 프린세스': ('fusion', 6, None), '우:피 팬시볼': ('link', 3, ['U', 'DL', 'DR']),
 # 멜리스
 'M∀LICE＜P＞Cheshire Cat': ('eff', 3, None), 'M∀LICE＜P＞Dormouse': ('eff', 3, None), 'M∀LICE＜P＞March Hare': ('eff', 3, None), 'M∀LICE＜P＞White Rabbit': ('eff', 3, None),
 '백업＠이그니스터': ('eff', 3, None), '위저드＠이그니스터': ('eff', 4, None),
 'M∀LICE＜Q＞HEARTS OF CRYPTER': ('link', 3, ['DL', 'DR', 'U']), 'M∀LICE＜Q＞WHITE BINDER': ('link', 3, ['L', 'R', 'U']),
 '어코드 토커＠이그니스터': ('link', 5, ['DL', 'D', 'DR', 'L', 'R']), '샐러맨그레이트 알미라지': ('link', 1, ['DR']), '링그리보': ('link', 1, ['DL']),
 '링크 디코더': ('link', 1, ['D']), '피안의 흑천사 케루비니': ('link', 2, ['DL', 'DR']), '사이버스 위키드': ('link', 2, ['D', 'DR']),
 '스플래시 메이지': ('link', 2, ['DR', 'UR']), '성취의 리절도즈': ('link', 2, ['D', 'R']), '트라이게이트 위저드': ('link', 3, ['L', 'R', 'U']),
 '트랜스코드 토커': ('link', 3, ['D', 'R', 'U']), '파이어월 드래곤': ('link', 4, ['D', 'L', 'R', 'U']), '액세스코드 토커': ('link', 4, ['D', 'L', 'R', 'U']),
 '디코드 토커 히트소울': ('link', 3, ['DL', 'DR', 'U']), '암영의 암령사 달크': ('link', 2, ['DL', 'DR']),
 '팬텀 나이츠 사일런트부츠': ('eff', 3, None), '팬텀 나이츠 둠솔루렛': ('eff', 3, None), '팬텀 나이츠 엄브레이지베일': ('eff', 3, None), '팬텀 나이츠 디케이클로크': ('eff', 3, None),
 '현람한 스엔': ('eff', 3, None), '현람한 엘담': ('eff', 3, None), '현람한 헌영': ('spell', 0, None), '현람한 견신': ('spell', 0, None), '싸이크론': ('spell', 0, None),
 'M∀LICE＜C＞GWC－06': ('trap', 0, None), 'M∀LICE＜C＞MTP－07': ('trap', 0, None), 'M∀LICE＜C＞TB－11': ('trap', 0, None), 'M∀LICE IN UNDERGROUND': ('field', 0, None), 'M∀LICE IN THE MIRROR': ('spell', 0, None),
 '사이바넷 마이닝': ('spell', 0, None), '하루 우라라': ('eff', 3, None), '패의 아무 몬스터': ('eff', 3, None),
}
POS = {'EL': (1, 0), 'ER': (3, 0), 'M1': (0, 1), 'M2': (1, 1), 'M3': (2, 1), 'M4': (3, 1), 'M5': (4, 1)}
MAIN = ['M1', 'M2', 'M3', 'M4', 'M5']


class Duel:
    def __init__(self, hand):
        self.z = {}            # 존 -> 카드명
        self.hand = list(hand)
        self.gy, self.ban, self.mats = [], [], {}
        self.snaps, self.err = [], []
        self.step_no = 0

    def _take(self, name, src):
        if src == 'field':
            for k, v in self.z.items():
                if v == name and not k.startswith('S'):
                    del self.z[k]; self.mats.pop(k, None); return
            raise ValueError(f'필드에 {name} 없음')
        lst = {'hand': self.hand, 'gy': self.gy, 'ban': self.ban}.get(src)
        if lst is None:
            return  # deck / extra 는 추적하지 않음
        if name not in lst:
            raise ValueError(f'{src}에 {name} 없음')
        lst.remove(name)

    def pointed(self):
        s = set()
        for k, v in self.z.items():
            if k in POS and DB[v][0] == 'link':
                x, y = POS[k]
                for a in DB[v][2]:
                    dx, dy = A[a]
                    for kk, p in POS.items():
                        if p == (x + dx, y + dy):
                            s.add(kk)
        return s

    def _place_check(self, name, zone, from_extra):
        if zone in self.z:
            raise ValueError(f'{zone}에 이미 {self.z[zone]} 있음')
        if zone in ('EL', 'ER'):
            if not from_extra:
                raise ValueError('엑스트라 몬스터 존은 엑스트라 덱 소환만 가능')
            other = 'ER' if zone == 'EL' else 'EL'
            if other in self.z:
                raise ValueError('엑스트라 몬스터 존은 1개만 사용 가능')
        elif from_extra and DB[name][0] == 'link' and zone not in self.pointed():
            raise ValueError(f'링크 {name}: {zone}은 링크 마커가 가리키는 존이 아님 (가리키는 존: {sorted(self.pointed())})')

    # ---- 동작 ----
    def put(self, name, zone, src, from_extra=False):
        self._take(name, src) if src != 'extra' else None
        self._place_check(name, zone, from_extra)
        self.z[zone] = name

    def ns(self, name, zone): self.put(name, zone, 'hand')
    def ss(self, name, zone, src): self.put(name, zone, src)
    def ssm(self, lst):
        for n, z, src in lst: self.put(n, z, src)
    def to_gy(self, name, src):
        self._take(name, src); self.gy.append(name)
    def to_hand(self, name, src='deck'):
        self._take(name, src); self.hand.append(name)
    def banish(self, name, src):
        self._take(name, src); self.ban.append(name)
    def shuffle(self, name, src):
        self._take(name, src)
    def link(self, mats, name, zone):
        r = DB[name][1]
        opts = [[1, DB[m][1]] if DB[m][0] == 'link' else [1] for m in mats]
        if not any(sum(c) == r for c in itertools.product(*opts)):
            raise ValueError(f'{name} 링크 {r}: 소재 {mats} 수치 불일치')
        for m in mats: self.to_gy(m, 'field')
        self.put(name, zone, 'extra', from_extra=True)
    def xyz(self, mats, name, zone):
        for m in mats: self._take(m, 'field')
        self.put(name, zone, 'extra', from_extra=True); self.mats[zone] = list(mats)
    def fusion(self, mats, name, zone, src='field'):
        for m in mats:
            if src == 'field': self.to_gy(m, 'field')
            else: self._take(m, src)  # 묘지에서 덱으로
        self.put(name, zone, 'extra', from_extra=True)
    def synchro(self, mats, name, zone):
        for m in mats: self.to_gy(m, 'field')
        self.put(name, zone, 'extra', from_extra=True)
    def st(self, name, zone, src='hand'):
        self._take(name, src) if src != 'deck' else None
        if zone in self.z: raise ValueError(f'{zone} 사용 중')
        self.z[zone] = name
    def st_gy(self, zone):
        self.gy.append(self.z.pop(zone).replace(' (장착)', ''))
    def equip(self, name, zone, src='gy'):
        self._take(name, src); self.z[zone] = name + ' (장착)'

    def snap(self, title, act, desc='', changed=()):
        self.step_no += 1
        linked = set()
        for k, v in self.z.items():
            if k in POS and DB.get(v, ('',))[0] == 'link':
                for p in self.pointed_by(k):
                    if p in self.z:
                        linked.add(p); linked.add(k)
        self.snaps.append({
            'n': self.step_no, 'title': title, 'act': act, 'desc': desc,
            'zones': {k: {'name': v, 'kind': DB.get(v.replace(' (장착)', ''), ('equip',))[0] if '(장착)' not in v else 'equip',
                          'arrows': DB.get(v, (0, 0, None))[2], 'mats': len(self.mats.get(k, [])),
                          'linked': k in linked} for k, v in self.z.items()},
            'hand': list(self.hand), 'gy': list(self.gy), 'ban': list(self.ban), 'changed': list(changed)})

    def pointed_by(self, k):
        x, y = POS[k]; out = []
        for a in DB[self.z[k]][2]:
            dx, dy = A[a]
            for kk, p in POS.items():
                if p == (x + dx, y + dy): out.append(kk)
        return out


ZL = {'EL': '엑스트라 몬스터 존(왼쪽)', 'ER': '엑스트라 몬스터 존(오른쪽)', 'M1': '1번째 존', 'M2': '2번째 존', 'M3': '3번째 존', 'M4': '4번째 존', 'M5': '5번째 존',
      'S1': '마법·함정 1번', 'S2': '마법·함정 2번', 'S3': '마법·함정 3번', 'S4': '마법·함정 4번', 'S5': '마법·함정 5번'}
SRC = {'deck': '덱에서', 'gy': '묘지에서', 'hand': '패에서', 'ban': '제외 상태에서', 'extra': '엑스트라 덱에서'}
SUMMON = {'ns', 'ss', 'ssm', 'synchro', 'link', 'xyz', 'fusion', 'put', 'st', 'equip'}


def _kind(op):
    if op[0] in SUMMON:
        return 'S'
    if op[0] in ('to_gy', 'banish', 'shuffle') and len(op) > 2 and op[2] == 'field':
        return 'R'
    if op[0] == 'st_gy':
        return 'R'
    return 'N'


def _auto(op):
    t = op[0]
    if t == 'ns': return f'{op[1]} 일반 소환', f'패에서 → {ZL[op[2]]}'
    if t == 'ssm': return f'{" + ".join(x[0] for x in op[1])} 동시 특수 소환', ' / '.join(f'{x[0]}: {SRC.get(x[2], "")} → {ZL[x[1]]}' for x in op[1])
    if t == 'ss': return f'{op[1]} 특수 소환', f'{SRC.get(op[3], "")} → {ZL[op[2]]}'
    if t == 'link': return f'{op[2]} 링크 소환', f'소재: {" + ".join(op[1])} → {ZL[op[3]]}'
    if t == 'synchro': return f'{op[2]} 싱크로 소환', f'소재: {" + ".join(op[1])} → {ZL[op[3]]}'
    if t == 'xyz': return f'{op[2]} 엑시즈 소환', f'소재: {" + ".join(op[1])} → {ZL[op[3]]}'
    if t == 'fusion':
        how = '묘지의 소재를 덱/엑스트라 덱으로 되돌려' if (len(op) > 4 and op[4] == 'gy') else '필드의 소재로'
        return f'{op[2]} 융합 소환', f'{how}: {" + ".join(op[1])} → {ZL[op[3]]}'
    if t == 'put': return f'{op[1]} 소환', f'→ {ZL[op[2]]}'
    if t == 'st':
        if len(op) > 3 and op[3] == 'deck': return f'{op[1]} 세트', f'덱에서 → {ZL[op[2]]}'
        return f'{op[1]} 발동', f'→ {ZL[op[2]]}'
    if t == 'equip': return f'{op[1]} 장착', f'→ {ZL[op[2]]}'
    return '', ''


def run(name, hand, script):
    d = Duel(hand)
    d.snap('시작 패', '', '선공 1턴, 나머지 패는 전부 패사고로 가정')
    for item in script:
        title, act, desc, ops = item[0], item[1], item[2], item[3]
        groups, cur, has_s = [], [], False
        for op in ops:
            k = _kind(op)
            if k in ('S', 'R') and has_s:
                groups.append(cur); cur, has_s = [], False
            cur.append(op)
            if k == 'S':
                has_s = True
        if cur:
            groups.append(cur)
        if len(item) > 4 and item[4]:
            groups = [list(ops)]
        for gi, g in enumerate(groups):
            before = dict(d.z)
            moves = []
            for op in g:
                t = op[0]
                if t in ('link', 'xyz', 'fusion', 'synchro'): moves.append([op[2], 'extra'])
                elif t == 'put' and len(op) > 3 and op[3] == 'extra': moves.append([op[1], 'extra'])
                elif t == 'ssm': moves += [[x[0], x[2]] for x in op[1] if x[2] in ('deck', 'extra')]
                elif t in ('ss', 'put') and len(op) > 3 and op[3] in ('deck', 'extra'): moves.append([op[1], op[3]])
                elif t in ('to_gy', 'banish') and len(op) > 2 and op[2] in ('deck', 'extra'): moves.append([op[1], op[2]])
                elif t == 'to_hand' and (len(op) < 3 or op[2] == 'deck'): moves.append([op[1], 'deck'])
                elif t == 'st' and len(op) > 3 and op[3] == 'deck': moves.append([op[1], 'deck'])
            try:
                for op in g:
                    getattr(d, op[0])(*op[1:])
            except Exception as e:
                d.err.append(f'[{name}] {title}: {e}')
                raise
            changed = [k for k in set(before) | set(d.z) if before.get(k) != d.z.get(k)]
            if len(groups) == 1:
                d.snap(title, act, desc, changed); d.snaps[-1]['from'] = moves
            else:
                main = next((op for op in g if op[0] in SUMMON), None)
                at, aa = _auto(main) if main else (title, act)
                if main and (main[0] == 'fusion' or (main[0] == 'put' and len(main) > 3 and main[3] == 'extra')) and not (main[0] == 'fusion' and len(main) > 4 and main[4] == 'gy'):
                    mi = g.index(main)
                    ex = [op for i, op in enumerate(g) if op[0] == 'to_gy' and len(op) > 2 and op[2] in ('hand', 'deck') and (main[0] == 'put' or i > mi)]
                    if ex:
                        parts = ([f'필드의 {m}' for m in main[1]] if main[0] == 'fusion' else []) + [('패의 ' if op[2] == 'hand' else '덱의 ') + op[1] for op in ex]
                        zone = ZL[main[3]] if main[0] == 'fusion' else ZL[main[2]]
                        aa = '소재: ' + ' + '.join(parts) + ' → ' + zone
                pre = [f'{op[1]} 묘지로' if op[0] == 'to_gy' else (f'{op[1]} 제외' if op[0] == 'banish' else '') for op in g if _kind(op) == 'R' and op[0] != 'st_gy']
                pre = [p for p in pre if p]
                if pre and main:
                    aa = ' · '.join(pre) + ' → ' + aa
                d.snap(at, aa, f'({gi + 1}/{len(groups)}) {title}: {desc}'.strip(), changed); d.snaps[-1]['from'] = moves
    return d


def stats(script):
    """내 턴 동안: 덱→패 서치 횟수, 패에서 소환 횟수(푸루리아), 덱·엑스트라 덱에서 소환 횟수(후와로스)."""
    sr = pu = fu = 0
    for item in script:
        if str(item[0]).startswith('상대 턴'):
            continue
        for op in item[3]:
            o = op[0]
            if o == 'to_hand' and (len(op) < 3 or op[2] == 'deck') and '드로우' not in op[1]:
                sr += 1
            elif o == 'ns':
                pu += 1
            elif o in ('ss', 'put'):
                src = op[3] if len(op) > 3 else ''
                if src == 'hand': pu += 1
                elif src in ('deck', 'extra'): fu += 1
            elif o == 'ssm':
                srcs = {x[2] for x in op[1]}
                if 'hand' in srcs: pu += 1
                if srcs & {'deck', 'extra'}: fu += 1
            elif o in ('link', 'xyz', 'fusion', 'synchro'):
                fu += 1
    return {'sr': sr, 'pu': pu, 'fu': fu}
