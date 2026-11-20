import json, sys
sys.path.insert(0, '/home/claude/field')
from sim import run, stats
from ml_names import *

B = '패사고'

# ---- 공통 본체: 성취의 리절도즈가 엑스트라 몬스터 존(왼쪽)에 있고 묘지에 도어마우스가 있는 상태에서 시작 ----
CORE = [
 (f'{LIZ} 효과', f'묘지의 {DOR}(공격력 900)를 제외 → {LIZ} 자신을 대상', f'제외된 {DOR} 효과: 300 LP를 내고 2번째 존에 특수 소환 (이후 이 턴은 엑스트라 덱에서 링크 몬스터만 특수 소환 가능)',
  [('banish', DOR, 'gy'), ('ss', DOR, 'M2', 'ban')]),
 (f'{DOR} 효과', f'덱의 {WR}를 제외', f'제외된 {WR} 효과: 300 LP를 내고 3번째 존에 특수 소환 → 소환 시 효과로 덱의 {TB}를 세트',
  [('banish', WR, 'deck'), ('ss', WR, 'M3', 'ban'), ('st', TB, 'S1', 'deck')]),
 (f'{WB} 링크 소환', f'{WR}(1) + {LIZ}(2)', f'엑스트라 몬스터 존(왼쪽). 메인 페이즈 효과로 덱의 {GWC}를 세트 (특수 소환 시 묘지 제외 효과는 쓰지 않음)',
  [('link', [WR, LIZ], WB, 'EL'), ('st', GWC, 'S2', 'deck')]),
 (f'{TB} 발동', f'세트한 턴 · 비용: 필드의 {WB}를 제외', f'덱에서 {CAT}를 3번째 존에 특수 소환 (이 턴 효과 발동 불가). 제외된 {WB} 효과: 900 LP를 내고 4번째 존에 특수 소환 + 1장 드로우',
  [('st_gy', 'S1'), ('banish', WB, 'field'), ('ss', CAT, 'M3', 'deck'), ('ss', WB, 'M4', 'ban'), ('to_hand', '드로우한 카드 (바인더)')]),
 (f'{WIC} 링크 소환', f'{WB} + {CAT} (사이버스 2장)', '엑스트라 몬스터 존(왼쪽). 마커가 2번째·3번째 존을 가리킴',
  [('link', [WB, CAT], WIC, 'EL')]),
 (f'{DEC} 링크 소환', DOR, f'{WIC}가 가리키는 2번째 존. {WIC} 효과: 묘지의 {CAT}를 제외하고 덱에서 사이버스 튜너 {BK}를 패에 넣음. 제외된 {CAT} 효과: 300 LP를 내고 3번째 존에 특수 소환',
  [('link', [DOR], DEC, 'M2'), ('banish', CAT, 'gy'), ('to_hand', BK), ('ss', CAT, 'M3', 'ban')]),
 (f'{BK} 효과', '엑스트라 덱에서 특수 소환한 사이버스가 있음', f'패에서 4번째 존에 특수 소환 → 덱에서 {HARE}를 패에 넣고 패 1장(패사고)을 버림',
  [('ss', BK, 'M4', 'hand'), ('to_hand', HARE), ('to_gy', B, 'hand')]),
 (f'{CAT} 효과', f'패의 {HARE}를 제외', f'2장 드로우. 제외된 {HARE} 효과: 300 LP를 내고 제외된 {HARE} 자신을 패에 넣음',
  [('banish', HARE, 'hand'), ('to_hand', '드로우한 카드 (체셔 캣)'), ('to_hand', '드로우한 카드 (체셔 캣)'), ('to_hand', HARE, 'ban')]),
 (f'{CRY} 링크 소환', f'{BK} + {CAT} + {DEC} (멜리스 포함 3장)', f'{WIC}가 가리키는 2번째 존. 공격력 2300 이상 사이버스의 소재가 된 {DEC} 효과로 자신을 3번째 존에 특수 소환 (필드를 떠나면 제외)',
  [('link', [BK, CAT, DEC], CRY, 'M2'), ('ss', DEC, 'M3', 'gy')]),
 (f'{FW} 링크 소환', f'{CRY}(3) + {DEC}(1)', f'{WIC}가 가리키는 2번째 존. 필드를 떠난 {DEC}는 제외됨',
  [('link', [CRY, DEC], FW, 'M2'), ('banish', DEC, 'gy')]),
 (f'{HARE} 효과 (패)', f'묘지의 {CRY}를 제외', f'{HARE}를 3번째 존에 특수 소환. 제외된 {CRY} 효과: 900 LP를 내고 4번째 존에 특수 소환 (공격력 2배)',
  [('banish', CRY, 'gy'), ('ss', HARE, 'M3', 'hand'), ('ss', CRY, 'M4', 'ban')]),
 (f'{ALC} 링크 소환', f'{WIC}(1) + {HARE}(1) + {CRY}(3) = 링크 5', f'엑스트라 몬스터 존(왼쪽). 소환 시 효과로 묘지의 공격력 2300 사이버스 {WB}를 가리키는 1번째 존에 특수 소환 (이후 이 턴 특수 소환 불가). {FW}(2번째 존)는 어코드 토커·{WB}와 서로 가리킴',
  [('link', [WIC, HARE, CRY], ALC, 'EL'), ('ss', WB, 'M1', 'gy')]),
 (f'{WB} 효과', '특수 소환 시', f'묘지의 {DOR} · {WR} · {CAT}를 제외. 이 턴은 특수 소환할 수 없어 바로 돌아오지 않고, 상대 턴 {GWC}의 소환 대상과 {CRY}의 제외 효과 비용으로 남음',
  [('banish', DOR, 'gy'), ('banish', WR, 'gy'), ('banish', CAT, 'gy')]),
]

PRE_SWEN = [
 (f'{SWEN} 특수 소환', '상대 필드에 마법·함정이 없음 → 패에서 3번째 존', f'소환 시 효과로 덱의 {CHANT}를 패에 넣음', [('ss', SWEN, 'M3', 'hand'), ('to_hand', CHANT)]),
 (f'{CHANT} 발동', '마법·함정 1번', f'덱에서 레벨 4 이하 현람 몬스터 {ELD}를 패에 넣음', [('st', CHANT, 'S1', 'hand'), ('to_hand', ELD), ('st_gy', 'S1')]),
 (f'{ELD} 특수 소환', '상대 필드에 마법·함정이 없음 → 패에서 2번째 존', f'소환 시 효과로 덱의 두 번째 {SWEN}를 패에 넣음', [('ss', ELD, 'M2', 'hand'), ('to_hand', SWEN)]),
]
PRE_ELD = [
 (f'{ELD} 특수 소환', '상대 필드에 마법·함정이 없음 → 패에서 2번째 존', f'소환 시 효과로 덱의 {SWEN}를 패에 넣음', [('ss', ELD, 'M2', 'hand'), ('to_hand', SWEN)]),
 (f'{SWEN} 특수 소환', '패에서 3번째 존', f'소환 시 효과로 덱의 {CHANT}를 패에 넣음', [('ss', SWEN, 'M3', 'hand'), ('to_hand', CHANT)]),
 (f'{CHANT} 발동', '마법·함정 1번', f'덱에서 두 번째 {SWEN}를 패에 넣음', [('st', CHANT, 'S1', 'hand'), ('to_hand', SWEN), ('st_gy', 'S1')]),
]
RT_MID = [
 (f'{CHE} 링크 소환', f'{ELD} + {SWEN} (레벨 3 2장)', '엑스트라 몬스터 존(왼쪽)', [('link', [ELD, SWEN], CHE, 'EL')]),
 (f'{CHE} 효과', f'덱의 레벨 3 {DOR}를 묘지로', '', [('to_gy', DOR, 'deck')]),
 (f'두 번째 {SWEN} 일반 소환', '3번째 존', f'스엔 서치 효과는 이미 써서 안 나감', [('ns', SWEN, 'M3')]),
 (f'{LIZ} 링크 소환', f'{SWEN} + {CHE} (이름이 다른 2장)', '엑스트라 몬스터 존(왼쪽)', [('link', [SWEN, CHE], LIZ, 'EL')]),
]
PRE_SOL = [
 (f'{SOL} 특수 소환', '내 필드에 몬스터가 없음 → 패에서 3번째 존', f'소환 시 효과로 덱의 {VEIL}를 세트', [('ss', SOL, 'M3', 'hand'), ('st', VEIL, 'S1', 'deck')]),
 (f'{VEIL} 발동', '세트한 턴 (필드에 팬텀 나이츠 몬스터가 있음)', '자신을 레벨 3 어둠 전사족 일반 몬스터로 2번째 존에 특수 소환', [('st_gy', 'S1'), ('ss', VEIL, 'M2', 'gy')]),
 (f'{CHE} 링크 소환', f'{SOL} + {VEIL} (레벨 3 2장)', '엑스트라 몬스터 존(왼쪽)', [('link', [SOL, VEIL], CHE, 'EL')]),
 (f'{CHE} 효과', f'덱의 레벨 3 {DOR}를 묘지로', '', [('to_gy', DOR, 'deck')]),
 ('패의 몬스터 일반 소환', '3번째 존 (하루 우라라·후와로스 같은 패 트랩 몬스터도 됨)', '', [('ns', '패의 아무 몬스터', 'M3')]),
 (f'{LIZ} 링크 소환', f'{CHE} + 일반 소환한 몬스터 (이름이 다른 2장)', '엑스트라 몬스터 존(왼쪽)', [('link', ['패의 아무 몬스터', CHE], LIZ, 'EL')]),
]

CF_SWEN = PRE_SWEN + RT_MID + CORE
CF_ELD = PRE_ELD + RT_MID + CORE
CF_SOL = PRE_SOL + CORE

BOARD = '최종: 어코드 토커＠이그니스터 · 파이어월 드래곤 · WHITE BINDER + GWC－06 세트 / 드로우 3장'
SETS = [
 ('m1', 'rt', '현람한 스엔 1장', '현람 구축 · Master Duel Meta 콤보(Himekami) 기준 · 엑스트라는 Kyo 덱리로 마무리', [SWEN, B, B, B, B], CF_SWEN, BOARD),
 ('m2', 'rt', '현람한 엘담 1장', '현람 구축 · 엘담으로 시작해 헌영으로 두 번째 스엔', [ELD, B, B, B, B], CF_ELD, BOARD),
 ('m3', 'pk', '둠솔루렛 + 아무 몬스터', '팬텀 나이츠 구축 · 패의 몬스터(패 트랩 포함) 1장이 일반 소환용으로 필요', [SOL, '패의 아무 몬스터', B, B, B], CF_SOL, BOARD),
]

O = {
 'ALC': (ALC, '상대가 카드·효과를 발동했을 때 (1턴에 1번)', f'가리키는 링크 몬스터({WB} 또는 {FW}) 1장을 릴리스해서 그 발동을 무효로 하고 제외'),
 'FW': (FW, '프리 체인 (필드에 있는 동안 1번)', '서로 가리키는 몬스터 수(어코드 토커·바인더 = 2)만큼 필드·묘지의 몬스터를 패로 되돌림'),
 'FW2': (f'{FW} (가리키는 몬스터가 묘지로)', '어코드 토커로 바인더를 릴리스했을 때 등', '패의 사이버스 몬스터 1장을 특수 소환'),
 'GWC': (GWC, '상대 턴 (필드의 멜리스 몬스터 1장을 제외하고 발동)', f'제외·묘지의 멜리스 몬스터 1장을 특수 소환. {WB}를 비용으로 제외하면 {WB} 자신 효과로 다시 소환 + 1장 드로우'),
 'WB': (f'{WB} (제외되었을 때)', '1턴에 1번', '900 LP를 내고 특수 소환 + 1장 드로우 → 소환 시 묘지 카드 최대 3장 제외'),
 'CRY': (f'{CRY} ({GWC}로 묘지에서 소환한 경우)', '프리 체인 (1턴에 1번)', '제외된 멜리스 카드 1장을 덱으로 되돌리고 필드의 카드 1장을 제외 (몬스터를 가리키고 있으면 무효 불가)'),
}
OPP = {'m1': ['ALC', 'FW', 'FW2', 'GWC', 'WB', 'CRY'], 'm2': ['ALC', 'FW', 'FW2', 'GWC', 'WB', 'CRY'], 'm3': ['ALC', 'FW', 'FW2', 'GWC', 'WB', 'CRY']}

base_main = [(CAT, 1), (DOR, 1), (HARE, 3), (WR, 1), (BK, 3), (WIZ, 1), (UND, 1), (GWC, 1), (MTP, 1), (TB, 1), (CYN, 1),
             (DROLL, 1), (MAXC, 1), (OGRE, 1), (ASH, 3), (FUWA, 3), (GS, 1), (ALL, 1), (XOUT, 1), (IMP, 3), (DOM, 3)]
extra = [(CRY, 1), (ALC, 1), (ALM, 1), (LIN, 1), (DEC, 1), (CHE, 1), (WIC, 1), (SPL, 1), (LKN, 1), (LIZ, 1), (TRI, 1), (TRC, 1), (WB, 1), (FW, 1), (ACC, 1)]
DECKS = {
 'base': {'title': '멜리스 기본 파츠', 'note': '', 'main': base_main, 'extra': extra},
 'pk': {'title': '팬텀 나이츠 구축 (Kyo, 2026년 11월 Master V)', 'note': '', 'main': base_main + [(BOOT, 3), (SOL, 3), (VEIL, 1)], 'extra': extra},
 'rt': {'title': '현람 구축', 'note': '', 'main': base_main + [(SWEN, 3), (ELD, 1), (CHANT, 3)], 'extra': extra},
}

if __name__ == '__main__':
    out = {'combos': [], 'decks': DECKS}
    for cid, deck, title, sub, hand, script, board in SETS:
        d = run(title, hand, script)
        out['combos'].append({'id': cid, 'deck': deck, 'title': title, 'sub': sub, 'board': board, 'steps': d.snaps, 'mc': stats(script),
                              'opp': [list(O[k]) for k in OPP.get(cid, [])]})
        print('OK', title, len(d.snaps), stats(script))
    json.dump(out, open('/home/claude/field/data_ml.json', 'w'), ensure_ascii=False)
