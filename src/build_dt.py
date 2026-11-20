import json,os
from PIL import Image
import build
K={}
def k(kind,*names):
    for n in names: K[n]=kind
k('eff','데스피아의 도화 알베르','드래곤테일 판','드래곤테일 무루루','알버스의 낙윤','순백의 성녀 에클레시아','드래곤테일 판','혁의 성녀 카르테시아','드래곤테일 루키아스','하얀 용의 낙윤','드래곤테일 파이메나','드래곤테일 우르굴라','흑의룡 알비온','인도하는 성녀 쿠엠','드롤 & 로크 버드','증식의 G','하루 우라라','마루챠미 푸루리아','마루챠미 후와로스')
k('spell','낙인개막','혁의 낙인','낙인융합','케투 드래곤테일','라후 드래곤테일','The Fallen & The Virtuous','초융합','낙인의 기염','천저의 사도')
k('trap','드래곤테일 혼','드래곤테일 스팅','드래곤테일 플레임','낙인단죄')
k('fusion','신염룡 루벨리온','진염룡 알비온','드래곤테일 그라멜','회신룡 배스터드','낙인룡 알비온','빙검룡 미라제이드','심연룡 알버 레나투스','혁언룡 그랑기뇰','격철룡 린드블룸','공극의 원성룡','드래곤테일 알자리온','사크라멘툼 드라군','성흔을 먹는 용','혼효하는 믹시아','초월소환수 아이온')
k('synchro','검은 용의 에클레시아','데스피아안 루루와릴리스')
k('link','프레데터 플랜츠 베르테 아나콘다')
BASE_MAIN=[('드래곤테일 무루루',2),('알버스의 낙윤',1),('순백의 성녀 에클레시아',2),('혁의 성녀 카르테시아',2),('드래곤테일 루키아스',1),('하얀 용의 낙윤',2),('드래곤테일 파이메나',3),('드래곤테일 우르굴라',1),('낙인융합',1),('케투 드래곤테일',2),('라후 드래곤테일',1),('The Fallen & The Virtuous',2),('드래곤테일 플레임',1)]
EXTRA=[('회신룡 배스터드',1),('낙인룡 알비온',1),('빙검룡 미라제이드',1),('심연룡 알버 레나투스',1),('혁언룡 그랑기뇰',1),('격철룡 린드블룸',1),('공극의 원성룡',1),('드래곤테일 알자리온',2),('사크라멘툼 드라군',1),('성흔을 먹는 용',1),('혼효하는 믹시아',1),('초월소환수 아이온',1),('검은 용의 에클레시아',1),('프레데터 플랜츠 베르테 아나콘다',1)]
GENS=[('드롤 & 로크 버드',2),('증식의 G',1),('하루 우라라',3),('마루챠미 푸루리아',3),('마루챠미 후와로스',3)]
def add(base,extra):
    d=dict(base);[d.__setitem__(n,d.get(n,0)+c) for n,c in extra];return list(d.items())
decks={
 'sanana':{'title':'진염룡 알비온 + 아나콘다 구축','note':'아나콘다로 덱의 낙인융합을 써서 진염룡 알비온까지 내는 구축입니다. 메인 덱에 드래곤테일 판·혼·스팅을 더하고, 엑스트라 덱은 초월소환수 아이온을 빼고 진염룡 알비온을 넣는 기준입니다.',
   'main':add(BASE_MAIN,[('드래곤테일 판',1),('드래곤테일 혼',1),('드래곤테일 스팅',1)]),'extra':[x for x in EXTRA if x[0]!='초월소환수 아이온']+[('진염룡 알비온',1)],
   'how':['라후를 쓰면 그 턴은 융합 몬스터만 낼 수 있어서, 검은 용의 에클레시아(싱크로)와 아나콘다(링크)를 라후보다 먼저 냅니다.','아나콘다 효과로 덱의 낙인융합을 묘지로 보내 그 효과만 쓰는 것은 발동이 아니라서, 싱크로·링크를 한 턴에도 쓸 수 있습니다. 소재는 덱의 알버스의 낙윤 + 카르테시아(빛 속성 마법사족)입니다.']},
 'bfpost':{'title':'낙인융합 초동 (프리클 금지 후)','note':'낙인융합으로 프리클 대신 판을 보내는 전개에 쓰는 구축입니다. 메인 덱에 드래곤테일 판·인도하는 성녀 쿠엠을 1장씩 더합니다.',
   'main':add(BASE_MAIN,[('드래곤테일 판',1),('인도하는 성녀 쿠엠',1)]),'extra':EXTRA,
   'how':['낙인융합으로 하얀 용의 낙윤 + 판(공격력 2700)을 보내 회신룡 배스터드를 냅니다. 판이 라후를 세트해서 바로 드래곤테일 전개로 이어집니다.','회신룡 배스터드는 사크라멘툼 드라군이나 알버 레나투스의 소재로 묘지에 보내 두면, 엔드 페이즈에 쿠엠을 특수 소환합니다.']},
 'shrmu':{'title':'흑의룡 알비온 (무루루 전개)','note':'흑의룡 알비온으로 덱의 하얀 용의 낙윤을 묘지에 보내고 알자리온으로 회수하는 구축입니다. 메인 덱에 흑의룡 알비온·드래곤테일 스팅·낙인단죄를 더합니다.',
   'main':add(BASE_MAIN,[('흑의룡 알비온',1),('드래곤테일 스팅',1),('낙인단죄',1)]),'extra':EXTRA,'range':{'흑의룡 알비온':'1~3'},
   'how':['흑의룡 알비온: 패에서 효과를 발동하며 비용으로 덱의 하얀 용의 낙윤을 묘지에 보냅니다. 여기에 체인해서 흑의룡을 융합 소재로 쓰면 덱으로 돌아가지 않습니다.','낙인단죄(카운터 함정): 묘지의 알버스 관련 융합 몬스터 2장을 엑스트라 덱으로 되돌리고, 특수 소환을 포함한 효과의 발동을 무효로 합니다.']},
 'base':{'title':'드래곤테일 낙인 기본 파츠','note':'보내주신 "드테낙인" 기본 파츠 화면(메인 21장 · 엑스트라 15장) 그대로입니다.','main':BASE_MAIN,'extra':EXTRA,
   'how':['모든 구축에 공통으로 들어가는 전개 카드입니다. 나머지 칸은 추가 구축 카드나 범용 카드로 채웁니다.','11월 5일 금제로 드래곤테일 프리클이 금지되어, 이 가이드의 전개는 프리클 없이 되는 것만 골랐습니다. 엑스트라 덱은 진염룡 알비온 대신 혼효하는 믹시아·초월소환수 아이온을 넣는 요즘 구성 기준입니다.','선택 카드 · 드래곤테일 판: 전개에는 영향이 없습니다. 서치해 두었다가 상대 턴에 융합 소재로 쓰면, 덱에서 드래곤테일 마법·함정 1장을 세트한 뒤 필드의 몬스터 1장을 파괴하는 방해가 됩니다.']},
 'nadir':{'title':'천저의 사도 추가 구축','note':'천저의 사도는 1~3장 사이에서 조절합니다. 엑스트라 덱은 루루와릴리스를 넣고 공극의 원성룡(또는 프레데터 플랜츠 베르테 아나콘다)을 뺍니다.',
   'main':add(BASE_MAIN,[('천저의 사도',1),('인도하는 성녀 쿠엠',1)]),'extra':[x for x in EXTRA if x[0]!='공극의 원성룡']+[('데스피아안 루루와릴리스',1)],'range':{'천저의 사도':'1~3'},
   'how':['천저의 사도: 엑스트라 덱의 몬스터 1장을 묘지로 보내고, 그 몬스터 이하 공격력의 "드래그마" 몬스터나 알버스의 낙윤을 덱·묘지에서 패에 넣습니다. 하얀 용의 낙윤(알버스의 낙윤 취급, 공격력 1800)과 인도하는 성녀 쿠엠(드래그마 취급, 공격력 1500)도 가져올 수 있습니다.','단 처리 후 이 턴은 엑스트라 덱에서 특수 소환할 수 없어서, 엑스트라 덱을 다 쓴 전개 마지막에 씁니다. 묘지로 보낼 카드는 엔드 페이즈 효과가 있는 낙인룡 알비온(낙인 마법·함정 서치·세트), 회신룡 배스터드(알버스의 낙윤 서치·특수 소환), 성흔을 먹는 용(드래그마 카드 서치 → The Fallen & The Virtuous)이 좋습니다.','같이 넣는 카드 · 인도하는 성녀 쿠엠: 소환 시 알버스의 낙윤 또는 그 이름이 쓰인 카드를 덱에서 묘지로 보냅니다. 엑스트라 덱에서 카드가 나가면(천저의 사도로 보낼 때도 해당) 묘지의 알버스의 낙윤이나 그 이름이 쓰인 몬스터를 특수 소환합니다. 레벨 4 튜너라 검은 용의 에클레시아·루루와릴리스의 소재도 됩니다.','같이 넣는 카드 · 데스피아안 루루와릴리스(엑스트라): 레벨 4 튜너 + 튜너 이외 1장 이상의 레벨 12 싱크로입니다. 묘지로 간 턴의 엔드 페이즈에 패·덱에서 공격력과 수비력이 같은 빛 속성 마법사족(카르테시아·에클레시아·쿠엠, 모두 1500/1500)을 특수 소환합니다.']},
 'sanct':{'title':'진염룡 알비온 추가 구축','note':'요즘은 진염룡 알비온 대신 혼효하는 믹시아·초월소환수 아이온을 쓰는 구성이 많습니다. 환경에 따라 다시 넣을 때 참고용입니다.',
   'main':BASE_MAIN,'extra':[x for x in EXTRA if x[0]!='초월소환수 아이온']+[('진염룡 알비온',1)],
   'how':['진염룡 알비온: 알버스의 낙윤 + 빛 속성 마법사족 융합. 상대 카드 효과의 대상이 되지 않습니다. 상대 턴에 양쪽 묘지의 몬스터 2장을 대상으로 1장씩 양쪽 필드에 특수 소환합니다(상대 쪽에 꺼낸 몬스터는 알버스의 낙윤 융합 소재로 씀).','프리클 없이도 카르테시아·에클레시아가 빛 속성 마법사족이라 소재로 쓸 수 있습니다. 엑스트라 덱은 아이온을 빼고 넣는 기준으로 적었습니다.']},
 'gal':{'title':'갤러리 전개 31종','note':'','main':add(BASE_MAIN,[('드래곤테일 판',1),('드래곤테일 혼',1),('드래곤테일 스팅',1)]),'extra':[x for x in EXTRA if x[0]!='공극의 원성룡']+[('드래곤테일 그라멜',1)],'how':[]},
 'gulpan':{'title':'그라멜 · 판 추가 구축','note':'환경에 따라 넣는 구축입니다. 엑스트라 덱은 공극의 원성룡을 빼고 그라멜을 넣는 기준입니다.',
   'main':add(BASE_MAIN,[('드래곤테일 판',1)]),'extra':[x for x in EXTRA if x[0]!='공극의 원성룡']+[('드래곤테일 그라멜',1)],
   'how':['드래곤테일 그라멜: 드래곤테일 몬스터 + 패의 몬스터 1장 융합. 드래곤테일 카드나 효과를 발동할 때마다 상대 카드 1장을 파괴하는 상시 방해입니다.','드래곤테일 판: 전개 자체에는 거의 영향이 없고, 서치해 두었다가 상대 턴 융합 소재로 쓰면 드래곤테일 마법·함정을 세트한 뒤 필드의 몬스터 1장을 파괴합니다. 아나콘다로 미라제이드까지 가는 루키아스 전개에서는 알자리온 소재로 씁니다.']},
 'sting':{'title':'드래곤테일 스팅','note':'혼 대신 스팅을 세트하는 구축입니다.','main':add(BASE_MAIN,[('드래곤테일 스팅',1)]),'extra':EXTRA,'how':['드래곤테일 스팅(함정): 상대 묘지의 몬스터 1장과 마법·함정 1장을 제외하고, 묘지·제외의 드래곤테일 카드 1장을 덱 맨 아래로 돌린 뒤 1장 드로우합니다.']},
 'trap3':{'title':'드래곤테일 함정 3장','note':'플레임·혼·스팅을 모두 넣는 구축입니다.','main':add(BASE_MAIN,[('드래곤테일 혼',1),('드래곤테일 스팅',1),('드래곤테일 판',1)]),'extra':EXTRA,'how':['라후로 드래곤테일 3장(덱 1장 + 패 2장)을 한 번에 소재로 보내면 세 장이 각각 함정을 세트해 플레임·혼·스팅이 모두 섭니다.']},
 'horn':{'title':'드래곤테일 혼 추가 구축','note':'해외 공략의 표준 필드(플레임 + 혼 2장 세트)를 쓰는 구축입니다. 메인 덱에 드래곤테일 혼 1장만 더합니다.',
   'main':add(BASE_MAIN,[('드래곤테일 혼',1)]),'extra':EXTRA,
   'how':['드래곤테일 혼(함정): 공격 표시 몬스터 1장을 패·엑스트라 덱으로 되돌리고, 묘지·제외의 드래곤테일 카드 1장을 덱 맨 아래로 돌린 뒤 1장 드로우합니다.','드래곤테일 몬스터가 융합 소재로 묘지에 갈 때 플레임 다음으로 세트할 함정이 생겨서, 케투·라후가 세트되던 자리가 방해 1장으로 바뀝니다.']},
 'opening':{'title':'낙인개막 · 알베르 추가 구축','note':'하얀 용의 낙윤 1장 전개를 끝까지 하기 위한 카드를 모두 넣은 구축입니다. 엑스트라 덱은 공극의 원성룡을 빼고 신염룡 루벨리온을 넣는 기준입니다.',
   'main':add(BASE_MAIN,[('인도하는 성녀 쿠엠',1),('낙인개막',1),('데스피아의 도화 알베르',1),('혁의 낙인',1)]),'extra':[x for x in EXTRA if x[0]!='공극의 원성룡']+[('신염룡 루벨리온',1)],
   'how':['낙인개막(속공 마법): 패 1장을 버리고 덱의 데스피아 몬스터를 패에 넣거나 수비 표시로 특수 소환합니다. 엔드 페이즈에도 쓸 수 있어서, 낙인룡 알비온 엔드 페이즈 효과로 가져와 바로 발동합니다.','데스피아의 도화 알베르: 소환 시 덱의 낙인 마법·함정을 서치합니다(혁의 낙인).','혁의 낙인(속공 마법): 묘지의 데스피아나 알버스의 낙윤을 패에 넣은 뒤, 패·필드의 소재를 제외해서 레벨 8 이상 융합 소환을 합니다(알베르 + 하얀 용의 낙윤 → 신염룡 루벨리온).','신염룡 루벨리온: 융합 소환 시 패 1장을 버리고, 필드·묘지·제외된 소재를 덱으로 되돌려 다른 레벨 8 이하 융합을 냅니다(루벨리온 + 하얀 용의 낙윤 → 빙검룡 미라제이드).','인도하는 성녀 쿠엠: 이 전개의 시작점(검은 용의 에클레시아로 소환)이자, 미라제이드가 나올 때 카르테시아를 소생하는 역할입니다.']},
 'gulsan':{'title':'그라멜 · 진염룡 알비온 추가 구축','note':'프리클 금지 전 기본 무브를 지금 덱으로 하는 구축입니다. 엑스트라 덱은 공극의 원성룡·초월소환수 아이온을 빼고 그라멜·진염룡 알비온을 넣는 기준입니다. 이 구축은 드래곤테일 함정 플레임·혼·스팅을 모두 씁니다.',
   'main':add(BASE_MAIN,[('드래곤테일 혼',1),('드래곤테일 스팅',1)]),'extra':[x for x in EXTRA if x[0] not in ('공극의 원성룡','초월소환수 아이온')]+[('드래곤테일 그라멜',1),('진염룡 알비온',1)],
   'how':['라후는 처리 후 융합 몬스터만 엑스트라 덱에서 낼 수 있어서, 아나콘다(링크)를 라후보다 먼저 냅니다.','낙인융합은 직접 발동하면 그 턴 융합 이외 엑스트라 덱 소환이 막히지만, 아나콘다 효과로 덱의 낙인융합을 묘지로 보내 그 효과만 쓰는 건 발동이 아니라서 아나콘다를 낸 뒤에도 쓸 수 있습니다.','진염룡 알비온 소재로 덱에서 보내는 빛 속성 마법사족은 예전엔 프리클(세 번째 함정 세트)이었지만, 금지 이후에는 카르테시아나 순백의 성녀 에클레시아를 보냅니다. 세 번째 함정 세트는 빠지는 대신, 보낸 카드가 엔드 페이즈에 패로 돌아옵니다.','드래곤테일 혼: 공격 표시 몬스터 1장을 패·엑스트라 덱으로 되돌리고 1장 드로우. 드래곤테일 스팅: 상대 묘지의 몬스터·마법함정을 제외하고 1장 드로우. 드래곤테일 플레임: 앞면 마법 1장 무효 후 1장 드로우.']},
 'spirits':{'title':'낙인의 기염 추가 구축','note':'낙인의 기염은 보통 2장 넣습니다.',
   'main':add(BASE_MAIN,[('낙인의 기염',2)]),'extra':EXTRA,
   'how':['낙인의 기염: 패의 몬스터 1장을 공개하고, 그와 같은 종족에 공격력이나 수비력이 2500인 레벨 8 융합 몬스터를 엑스트라 덱에서 묘지로 보냅니다. 그 뒤 공개한 몬스터를 버리고 알버스의 낙윤이나 그 이름이 쓰인 몬스터를 덱에서 패에 넣습니다.','공개는 드래곤족(무루루·판·우르굴라·하얀 용의 낙윤 등)으로 합니다. 마법사족 쪽에는 조건에 맞는 레벨 8 융합이 없습니다. 묘지로는 엔드 페이즈 효과를 예약하는 낙인룡 알비온이나 회신룡 배스터드를 보냅니다.','묘지에서 패로 돌아오는 효과도 있지만, 낙인의 기염은 효과를 1턴에 1개만 쓸 수 있습니다. 그래서 서치 효과를 쓴 턴의 엔드 페이즈에는 돌아오지 않습니다. 돌아오는 것은 서치를 쓰지 않은 턴(예: 상대 턴에 내 융합 몬스터가 묘지로 간 경우)의 엔드 페이즈입니다.']},
 'shrouded':{'title':'흑의룡 알비온 추가 구축','note':'흑의룡 알비온은 1~3장 사이에서 조절합니다.',
   'main':add(BASE_MAIN,[('흑의룡 알비온',2)]),'extra':EXTRA,'range':{'흑의룡 알비온':'1~3'},
   'how':['흑의룡 알비온: 패나 묘지에 있을 때 알버스의 낙윤 또는 "낙인" 마법·함정을 패·덱에서 묘지로 보냅니다. 패에서 보냈으면 자신을 특수 소환하고, 덱에서 보냈으면 자신을 덱 맨 아래로 되돌립니다. 이 효과를 패에서 썼다면 1장 드로우합니다.','필드·묘지에서는 이름이 알버스의 낙윤이 되고, 레벨 8 어둠 드래곤족 공격력 2500입니다. 그래서 회신룡 배스터드(알버스의 낙윤 + 공격력 2500 이상) 같은 알버스 융합의 소재로 바로 쓰입니다.','기본 파츠에서 보낼 수 있는 카드는 알버스의 낙윤, 낙인융합, The Fallen & The Virtuous(낙인 취급)입니다. 패에 이 중 1장이 같이 잡히면 그 카드를 묘지로 보내고 흑의룡 알비온을 특수 소환합니다.','같이 잡힌 카드가 없을 때는 덱의 The Fallen & The Virtuous나 알버스의 낙윤을 묘지로 보내고 1장 드로우하는 패 교환으로 씁니다. 낙인융합은 초동이라 덱에서 보내지 않습니다.']},
}
gen=[n for n,_ in GENS]
# images
ids={'드래곤테일 혼':69932023,'드래곤테일 스팅':80208225,'낙인개막':36637374,'데스피아의 도화 알베르':62962630,'혁의 낙인':82738008,'신염룡 루벨리온':70534340,'진염룡 알비온':38811586,'드래곤테일 그라멜':79755671,'드래곤테일 판':44482554,'드래곤테일 무루루':7375867,'알버스의 낙윤':68468459,'순백의 성녀 에클레시아':55273560,'혁의 성녀 카르테시아':95515789,'드래곤테일 루키아스':75003700,'드래곤테일 파이메나':1498449,'드래곤테일 우르굴라':70871153,'흑의룡 알비온':25451383,'인도하는 성녀 쿠엠':45883110,'낙인융합':44362883,'케투 드래곤테일':6153210,'라후 드래곤테일':32548318,'초융합':48130397,'낙인의 기염':29948294,'천저의 사도':1984618,'드래곤테일 플레임':5431722,'낙인단죄':17751597,'회신룡 배스터드':41373230,'낙인룡 알비온':87746184,'빙검룡 미라제이드':44146295,'심연룡 알버 레나투스':3410461,'혁언룡 그랑기뇰':24915933,'격철룡 린드블룸':51409648,'공극의 원성룡':72578374,'드래곤테일 알자리온':33760966,'사크라멘툼 드라군':89851827,'프레데터 플랜츠 베르테 아나콘다':70369116,'데스피아안 루루와릴리스':53971455}
GENPOOL=[('하루 우라라',14558127,'eff'),('증식의 G',23434538,'eff'),('마루챠미 후와로스',42141493,'eff'),('마루챠미 푸루리아',84192580,'eff'),('마루챠미 냐루스',87126721,'eff'),('이펙트 뵐러',97268402,'eff'),('무한포영',10045474,'trap'),('유령토끼',59438930,'eff'),('저택 와라시',73642296,'eff'),('드롤 & 로크 버드',94145021,'eff'),('원시생명체 니비루',27204311,'eff'),('금지된 일적',24299458,'spell'),('삼전의 재',25311006,'spell')]
for n,i,kd in GENPOOL:
    K[n]=kd; ids[n]=i
img={}
for n,i in ids.items():
    p=f'/home/claude/dimg/{i}.jpg'
    if os.path.exists(p):
        Image.open(p).convert('RGB').resize((160,233),Image.LANCZOS).save(f'site_dt/card/{i}.jpg',quality=80);img[n]=f'card/{i}.jpg'
for n,f in {'하얀 용의 낙윤':'wd','The Fallen & The Virtuous':'fv','성흔을 먹는 용':'dd','혼효하는 믹시아':'mx','초월소환수 아이온':'ae','검은 용의 에클레시아':'ed'}.items(): img[n]=f'card/{f}.jpg'
dat={'combos':json.load(open('data_dt.json'))['combos'],'decks':decks,'kinds':K}
SEL=[
 {'key':'base','name':'기본 파츠','sub':'모든 구축에 공통으로 들어가는 전개 카드 (메인 21장 · 엑스트라 15장). 이 카드들만으로 하는 전개를 기준으로 함','deck':'base','combos':['d1','d1b','d2','d3','d4','l1','l2','ec1','ec2'],'groups':[{'name':'하얀 용의 낙윤 1장','items':[['d1r','검은 용의 에클레시아 · 카르테시아, 패에 에클레시아, 묘지에 린드블룸 (성흔을 먹는 용·알비온 보존)'],['d1','성흔을 먹는 용을 보냄: 검은 용의 에클레시아 + F&V 세트, 패에 카르테시아·에클레시아'],['d1b','낙인룡 알비온을 보냄: 검은 용의 에클레시아 + 카르테시아(필드) + F&V 세트, 패에 에클레시아'],['d2','에클레시아 소환에 패 트랩을 맞았을 때: 상대 턴 미라제이드']]},{'name':'하얀 용의 낙윤 + 무루루','items':[['d3m','믹시아 버전: 검은 용 · 믹시아 · 루키아스 + F&V, 패에 카르테시아·에클레시아·파이메나 → 상대 턴 아이온'],['d3','사크라멘툼 · 알자리온 · 무루루 보드']]},{'name':'하얀 용의 낙윤 + 루키아스','items':[['d4m','믹시아 버전: 검은 용 · 카르테시아 · 믹시아 · 알자리온 + 플레임·F&V, 패에 파이메나·루키아스·에클레시아'],['d4','사크라멘툼 · 알자리온 · 무루루 · 카르테시아 보드']]},{'name':'루키아스 + 아무 몬스터','items':[['l1','알자리온 2장 + 플레임·케투 세트, 패에 파이메나']]},{'name':'루키아스 + 파이메나','items':[['l2','알자리온 · 미라제이드 + 플레임·케투 세트, 패에 파이메나·무루루']]},{'name':'에클레시아 + 카르테시아','items':[['ec2','에클레시아 · 미라제이드 + F&V 세트, 패에 F&V'],['ec1','에클레시아 · 그랑기뇰 + F&V 세트, 묘지에 린드블룸']]}],'clinks':{'ec1':[{'t':'Master Duel Meta 낙인 콤보 모음','u':'https://www.masterduelmeta.com/spreadsheet/6a9ea9e254346dd0c0c7555c'}],'l1':[{'t':'Master Duel Meta 드래곤테일 콤보 모음 (dominick)','u':'https://www.masterduelmeta.com/spreadsheet/6a20d431c3038d6b28c66ace'}],'d1b':[{'t':'마듀 갤러리: 낙인드테 질문 (백낙윤 원핸드)','u':'https://gall.dcinside.com/mgallery/board/view/?id=masterduel&no=5859249'}],'d1':[{'t':'Master Duel Meta 드래곤테일 콤보 모음 (dominick)','u':'https://www.masterduelmeta.com/spreadsheet/6a20d431c3038d6b28c66ace'}],'d2':[{'t':'Master Duel Meta 드래곤테일 콤보 모음 (dominick)','u':'https://www.masterduelmeta.com/spreadsheet/6a20d431c3038d6b28c66ace'}],'d3':[{'t':'Master Duel Meta 드래곤테일 콤보 모음 (langhorst · Cyden 콤보)','u':'https://www.masterduelmeta.com/spreadsheet/6ab54b80cf2cf431de94bba6'}],'d4':[{'t':'Master Duel Meta 드래곤테일 콤보 모음 (langhorst · Cyden 콤보)','u':'https://www.masterduelmeta.com/spreadsheet/6ab54b80cf2cf431de94bba6'}]}},
 {'key':'sanana','name':'진염룡 알비온 + 아나콘다 구축','sub':'','deck':'sanana','combos':['mg3'],'base':'base','baseName':'기본 파츠','groups':[{'name':'카르테시아 + 루키아스 + 무루루','items':[['mg3','아나콘다 · 진염룡 알비온 · 드라군 · 하얀 용의 낙윤 · 알자리온 · 검은 용 + 플레임·혼·스팅·F&V 세트']]}],'clinks':{'mg3':[{'t':'magu6o: 白き竜で強化された新規烙印ドラゴンテイルの展開 (YouTube, 8:02~)','u':'https://www.youtube.com/watch?v=_6TuHJORXMY&t=482s'}]}},
 {'key':'bfpost','name':'낙인융합 초동 (프리클 금지 후)','sub':'','deck':'bfpost','combos':['bfp','bfp2'],'base':'base','baseName':'기본 파츠','groups':[{'name':'낙인융합 + 아무 몬스터','items':[['bfp','에클레시아 · 카르테시아 · 쿠엠 · 드라군 · 루키아스 + 플레임·F&V 세트, 패에 파이메나·무루루'],['bfp2','루키아스가 무효될 때: 에클레시아 · 카르테시아 · 쿠엠 · 알자리온 + F&V 세트']]}],'clinks':{'bfp':[{'t':'potato4d: 新制限ドラゴンテイル 烙印初動紹介 (YouTube, 0:28~)','u':'https://www.youtube.com/watch?v=cXkP2SAb9OI'}],'bfp2':[{'t':'potato4d: 新制限ドラゴンテイル 烙印初動紹介 (YouTube, 2:33~)','u':'https://www.youtube.com/watch?v=cXkP2SAb9OI&t=153s'}]}},
 {'key':'shrmu','name':'흑의룡 알비온 (무루루 전개)','sub':'','deck':'shrmu','combos':['shm'],'base':'base','baseName':'기본 파츠','groups':[{'name':'무루루 + 파이메나 + 우르굴라 + 흑의룡 알비온','items':[['shm','알자리온 + 플레임·스팅·낙인단죄 세트, 패에 무루루·파이메나']]}],'clinks':{'shm':[{'t':'ねへほもん: 烙印ドラゴンテイル 先攻展開 (YouTube)','u':'https://www.youtube.com/watch?v=fUQhdlyxVa4'},{'t':'ねへほもん 블로그: 烙印ドラゴンテイル紹介','u':'https://ameblo.jp/nehe-blog/entry-12969136833.html'}]}},
 {'key':'nadir','name':'천저의 사도 추가 구축','sub':'기본 파츠에 천저의 사도와 함께 쓰는 쿠엠·루루와릴리스를 더한 구축. 엑스트라 덱의 엔드 페이즈 카드를 묘지로 보내며 알버스의 낙윤·쿠엠을 서치','deck':'nadir','combos':['n1','n2','qwd'],'groups':[{'name':'쿠엠 + 하얀 용의 낙윤','items':[['qwd','검은 용의 에클레시아 · 카르테시아 · 그랑기뇰 + F&V, 패에 카르테시아·에클레시아, 묘지에 린드블룸']]},{'name':'천저의 사도 1장','items':[['n1','회신룡을 보냄: 하얀 용의 낙윤 · 카르테시아 · 쿠엠 + F&V 세트'],['n2','루루와릴리스를 보냄: 하얀 용의 낙윤 · 에클레시아 · 카르테시아 · 쿠엠, 묘지에 알버스의 낙윤']]}],'clinks':{'n3':[{'t':'Master Duel Meta 콤보: 1 card Fallen of the White Dragon','u':'https://www.masterduelmeta.com/combo/6a25a517cc97d1771dd5b965'}],'n2':[{'t':'마듀 갤러리: 낙인드테에 루루와릴리스 괜찮네','u':'https://gall.dcinside.com/mgallery/board/view/?id=masterduel&no=5861920'}],'n1':[{'t':'Master Duel Meta 낙인 콤보 모음','u':'https://www.masterduelmeta.com/spreadsheet/6a9ea9e254346dd0c0c7555c'}]},'base':'base','baseName':'기본 파츠'},
 {'key':'opening','name':'낙인개막 · 알베르 추가 구축','sub':'쿠엠·낙인개막·데스피아의 도화 알베르·혁의 낙인·신염룡 루벨리온을 넣어 하얀 용의 낙윤 1장으로 미라제이드까지 가는 구축','deck':'opening','combos':['o1','opb','alu','qwd','opl','opf'],'base':'base','baseName':'기본 파츠','groups':[{'name':'하얀 용의 낙윤 1장','items':[['o1','미라제이드 · 쿠엠 · 카르테시아 · 검은 용의 에클레시아']]},{'name':'낙인개막 + 루키아스 + 아무 카드','items':[['opl','알베르 · 사크라멘툼 드라군 · 하얀 용의 낙윤 · 에클레시아 + 플레임·F&V 세트']]},{'name':'낙인개막 + 파이메나 + 아무 카드','items':[['opf','알베르 · 그랑기뇰 · 하얀 용의 낙윤 · 에클레시아 + F&V, 패에 파이메나']]},{'name':'알베르 1장','items':[['alu','그랑기뇰 · 하얀 용의 낙윤 · 에클레시아 · 알베르 + F&V 세트']]},{'name':'쿠엠 + 하얀 용의 낙윤','items':[['qwd','검은 용의 에클레시아 · 카르테시아 · 그랑기뇰 + F&V, 패에 카르테시아·에클레시아, 묘지에 린드블룸']]},{'name':'낙인개막 1장','items':[['opb','그랑기뇰 · 하얀 용의 낙윤 · 에클레시아 · 알베르 + F&V 세트']]}],'clinks':{'o1':[{'t':'Master Duel Meta 콤보: 1 card Fallen of the White Dragon','u':'https://www.masterduelmeta.com/combo/6a25a517cc97d1771dd5b965'}]}},
 {'key':'gulsan','name':'그라멜 · 진염룡 알비온 추가 구축','sub':'프리클 금지 전 기본 무브(알자리온 → 아나콘다 → 라후로 그라멜 → 아나콘다로 낙인융합 → 진염룡)를 지금 덱으로','deck':'gulsan','combos':['gs1','gs2','u1h','u1s','u1','u2h','u2s','u2'],'base':'base','baseName':'기본 파츠','groups':[{'name':'케투 + 드래곤테일 몬스터 + 아무 몬스터','items':[['gs1','그라멜 · 진염룡 알비온 · 아나콘다 + 함정 2장 세트']]},{'name':'루키아스 + 드래곤테일 몬스터 + 아무 몬스터','items':[['gs2','그라멜 · 진염룡 알비온 · 아나콘다 + 함정 2장 세트']]},{'name':'루키아스 + 파이메나 + 아무 몬스터','items':[['u1h','그라멜 · 진염룡 · 아나콘다 + 플레임·혼 세트 (내 수순)'],['u1s','그라멜 · 진염룡 · 아나콘다 + 플레임·스팅 세트 (내 수순)'],['u1','그라멜 · 진염룡 · 아나콘다 + 플레임·케투 세트 (내 수순)']]},{'name':'루키아스 + 무루루 + 아무 몬스터','items':[['u2h','그라멜 · 진염룡 · 아나콘다 + 플레임·혼 세트 (내 수순)'],['u2s','그라멜 · 진염룡 · 아나콘다 + 플레임·스팅 세트 (내 수순)'],['u2','그라멜 · 진염룡 · 아나콘다 + 플레임·케투 세트 (내 수순)']]}]},
 {'key':'spirits','name':'낙인의 기염 추가 구축','sub':'기본 파츠에 낙인의 기염만 더한 구축. 패의 드래곤족을 버려 하얀 용의 낙윤 같은 알버스 관련 몬스터를 서치 (서치한 턴에는 묘지에서 돌아오지 않음)','deck':'spirits','combos':['s1','sps','spf','smu','slu','ske','sca','sur','sld','sht'],'groups':[{'name':'낙인의 기염 + 드래곤족 1장','items':[['s1','검은 용의 에클레시아 + F&V 세트, 패 3장']]},{'name':'낙인의 기염 + 마법사족 1장','items':[['sps','검은 용의 에클레시아 + F&V 세트 (그랑기뇰을 묘지로)']]},{'name':'낙인의 기염 + 드래곤족 + 무루루','items':[['smu','하얀 용의 낙윤 + 무루루 결과 + 묘지에 린드블룸']]},{'name':'낙인의 기염 + 드래곤족 + 루키아스','items':[['slu','하얀 용의 낙윤 + 루키아스 결과 + 묘지에 린드블룸']]},{'name':'낙인의 기염 + 드래곤족 + 케투','items':[['ske','하얀 용의 낙윤 + 케투 결과 + 묘지에 린드블룸']]},{'name':'낙인의 기염 + 드래곤족 + 카르테시아','items':[['sca','하얀 용의 낙윤 + 카르테시아 결과 + 낙인융합 서치']]},{'name':'낙인의 기염 + 드래곤족 + 우르굴라·판','items':[['sur','하얀 용의 낙윤 + 우르굴라 결과 + 묘지에 린드블룸']]},{'name':'낙인의 기염 + 드래곤족 + 빛·어둠 몬스터','items':[['sld','하얀 용의 낙윤 + 빛·어둠 결과 + 낙인융합 서치']]},{'name':'낙인의 기염 + 드래곤족 + 패 트랩','items':[['sht','하얀 용의 낙윤 + 패 트랩 결과 + 묘지에 린드블룸']]},{'name':'낙인의 기염 + 후와로스','items':[['spf','검은 용의 에클레시아 + F&V 세트 → 상대 턴 린드블룸']]}],'base':'base','baseName':'기본 파츠'},
 {'key':'sanct','name':'진염룡 알비온 추가 구축','sub':'엑스트라 덱에 진염룡 알비온을 넣는 구축 (프리클 없이 카르테시아·에클레시아를 소재로)','deck':'sanct','combos':['sa1'],'base':'base','baseName':'기본 파츠','groups':[{'name':'하얀 용의 낙윤 + 레벨 4','items':[['sa1','진염룡 알비온 · 검은 용의 에클레시아 + F&V 세트']]}],'clinks':{'sa1':[{'t':'Master Duel Meta 드래곤테일 콤보 모음 (dominick)','u':'https://www.masterduelmeta.com/spreadsheet/6a20d431c3038d6b28c66ace'}]}},
 {'key':'sting','name':'드래곤테일 스팅','sub':'','deck':'sting','combos':['xs1','xs2'],'base':'base','baseName':'기본 파츠','groups':[{'name':'하얀 용의 낙윤 + 무루루','items':[['xs2','검은 용 · 드라군 · 무루루 · 알자리온 + 플레임·스팅·F&V 세트, 패에 파이메나·카르테시아']]},{'name':'하얀 용의 낙윤 + 루키아스','items':[['xs1','검은 용 · 카르테시아 · 드라군 · 알자리온 · 무루루 + 플레임·스팅·F&V 세트, 패에 파이메나·에클레시아']]}],'clinks':{'xs1':[{'t':'Master Duel Meta: Walbaz (SS) + Lukias / Ketu (Cyden)','u':'https://www.masterduelmeta.com/combo/6a185f896922d81e66b6f54a'},{'t':'ygotac: ドラゴンテイル展開ルート 5','u':'https://ygotac.com/dragon-tail_combo/'}],'xs2':[{'t':'Master Duel Meta: Walbaz (SS) + Mululu (Cyden)','u':'https://www.masterduelmeta.com/combo/6a227de8a3c859cb654da6a1'}]}},
 {'key':'trap3','name':'드래곤테일 함정 3장','sub':'','deck':'trap3','combos':['x3t'],'base':'base','baseName':'기본 파츠','groups':[{'name':'루키아스 + 파이메나','items':[['x3t','알자리온 · 미라제이드 + 플레임·혼·스팅 세트, 패에 파이메나·판']]}],'clinks':{'x3t':[{'t':'Master Duel Meta: Lukias + Faimena / Urgula / Ketu (dominick)','u':'https://www.masterduelmeta.com/combo/6a20cebb39a5d92345ca2b1e'}]}},
 {'key':'horn','name':'드래곤테일 혼 추가 구축','sub':'메인 덱에 드래곤테일 혼 1장을 더하는 구축. 해외 공략의 표준 필드(플레임 + 혼)','deck':'horn','combos':['xh1','xh2'],'base':'base','baseName':'기본 파츠','groups':[{'name':'하얀 용의 낙윤 + 무루루','items':[['xh2','검은 용 · 드라군 · 무루루 · 알자리온 + 플레임·혼·F&V 세트, 패에 파이메나·카르테시아']]},{'name':'하얀 용의 낙윤 + 루키아스','items':[['xh1','검은 용 · 카르테시아 · 드라군 · 알자리온 · 무루루 + 플레임·혼·F&V 세트, 패에 파이메나·에클레시아']]}],'clinks':{'xh2':[{'t':'Master Duel Meta: Walbaz (SS) + Mululu (Cyden)','u':'https://www.masterduelmeta.com/combo/6a227de8a3c859cb654da6a1'}],'xh1':[{'t':'Master Duel Meta: Walbaz (SS) + Lukias / Ketu (Cyden)','u':'https://www.masterduelmeta.com/combo/6a185f896922d81e66b6f54a'},{'t':'ygotac: ドラゴンテイル展開ルート 5','u':'https://ygotac.com/dragon-tail_combo/'}]}},
 {'key':'gulpan','name':'그라멜 · 판 추가 구축','sub':'드래곤테일 그라멜(엑스트라)과 드래곤테일 판(메인)을 넣는 구축','deck':'gulpan','combos':['g1','g1k','g2'],'base':'base','baseName':'기본 파츠','groups':[{'name':'루키아스 + 아무 몬스터','items':[['g1','알자리온 · 그라멜 + 플레임·케투 세트, 패에 파이메나'],['g1k','케투로 파이메나 2장 → 상대 턴 믹시아 · 아이온']]},{'name':'루키아스 + 파이메나','items':[['g2','알자리온 · 미라제이드 + 플레임·케투 세트, 패에 파이메나·판']]}],'clinks':{'g1':[{'t':'Master Duel Meta 드래곤테일 콤보 모음 (dominick)','u':'https://www.masterduelmeta.com/spreadsheet/6a20d431c3038d6b28c66ace'}],'g2':[{'t':'Master Duel Meta 드래곤테일 콤보 모음 (dominick)','u':'https://www.masterduelmeta.com/spreadsheet/6a20d431c3038d6b28c66ace'}]}},
 {'key':'shrouded','name':'흑의룡 알비온 추가 구축','sub':'기본 파츠에 흑의룡 알비온만 더한 구축. 낙인융합·The Fallen & The Virtuous·알버스의 낙윤과 같이 잡히면 알버스의 낙윤 취급 레벨 8로 특수 소환, 아니면 패 교환','deck':'shrouded','combos':['shl'],'groups':[{'name':'흑의룡 알비온 + 카르테시아 + 루키아스','items':[['shl','카르테시아 · 사크라멘툼 드라군 · 알자리온 + 플레임 세트, 패에 루키아스·파이메나 + 1장 드로우']]}],'base':'base','baseName':'기본 파츠'},
 {'key': 'gal', 'name': '갤러리 전개 31종', 'sub': '', 'deck': 'gal', 'combos': ['l1h', 'l1s', 'g1h', 'g1s', 'g2h', 'g2s', 'q3', 'q4h', 'q4s', 'q3p', 'r1h', 'r1s', 'c1h', 'c1s', 'r0', 'r2h', 'r2s', 'r3h', 'r3s', 'r4h', 'r4s', 'r5', 'q4', 'r1', 'c1', 'r2', 'r3', 'r4', 'k27h', 'k27s', 'k27', 'k26', 'k26a', 'k26b', 'k26c', 'k23'], 'base': 'base', 'baseName': '기본 파츠', 'groups': [{'name': '루키아스 + 아무 몬스터', 'items': [['g1h', '알자리온 · 그라멜 + 플레임·혼 세트, 패에 파이메나'], ['g1s', '알자리온 · 그라멜 + 플레임·스팅 세트, 패에 파이메나'], ['l1h', '알자리온 2장 + 플레임·혼 세트, 패에 파이메나'], ['l1s', '알자리온 2장 + 플레임·스팅 세트, 패에 파이메나']]}, {'name': '루키아스 + 파이메나', 'items': [['g2h', '알자리온 · 미라제이드 + 플레임·혼 세트, 패에 파이메나·판'], ['g2s', '알자리온 · 미라제이드 + 플레임·스팅 세트, 패에 파이메나·판']]}, {'name': '무루루 + 루키아스', 'items': [['q4h', '알자리온 · 그라멜 + 플레임·혼 세트, 패에 파이메나·루키아스'], ['q4s', '알자리온 · 그라멜 + 플레임·스팅 세트, 패에 파이메나·루키아스'], ['q4', '알자리온 · 그라멜 + 플레임·케투 세트, 패에 파이메나·루키아스']]}, {'name': '무루루 + 드래곤테일 이외 몬스터', 'items': [['q3p', '알자리온 · 그라멜 + 플레임 세트, 묘지에 판 (융합이 파괴되면 무루루 소생)'], ['q3', '알자리온 · 그라멜 + 플레임 세트']]}, {'name': '라후 + 아무 몬스터', 'items': [['r1h', '알자리온 · 그라멜 + 플레임·혼 세트, 패에 파이메나'], ['r1s', '알자리온 · 그라멜 + 플레임·스팅 세트, 패에 파이메나'], ['r0', '그라멜 · 루키아스 + 플레임 세트, 패에 파이메나'], ['r1', '알자리온 · 그라멜 + 플레임·케투 세트, 패에 파이메나']]}, {'name': '루키아스 + 무루루 + 아무 몬스터', 'items': [['c1h', '미라제이드 · 그라멜 + 플레임·혼 세트, 패에 파이메나'], ['c1s', '미라제이드 · 그라멜 + 플레임·스팅 세트, 패에 파이메나'], ['c1', '미라제이드 · 그라멜 + 플레임·케투 세트, 패에 파이메나']]}, {'name': '라후 + 루키아스', 'items': [['r2h', '그라멜 · 루키아스 + 플레임·혼 세트, 패에 파이메나'], ['r2s', '그라멜 · 루키아스 + 플레임·스팅 세트, 패에 파이메나'], ['r2', '그라멜 · 루키아스 + 플레임·케투 세트, 패에 파이메나']]}, {'name': '라후 + 무루루', 'items': [['r3h', '사크라멘툼 · 무루루 + 플레임·혼 세트, 패에 파이메나'], ['r3s', '사크라멘툼 · 무루루 + 플레임·스팅 세트, 패에 파이메나'], ['r3', '사크라멘툼 · 무루루 + 플레임·케투 세트, 패에 파이메나']]}, {'name': '라후 + 파이메나', 'items': [['r4h', '사크라멘툼 · 알자리온 · 무루루 + 플레임·혼 세트, 패에 파이메나'], ['r4s', '사크라멘툼 · 알자리온 · 무루루 + 플레임·스팅 세트, 패에 파이메나'], ['r4', '사크라멘툼 · 알자리온 · 무루루 + 플레임·케투 세트, 패에 파이메나']]}, {'name': '라후 + 하얀 용의 낙윤', 'items': [['r5', '사크라멘툼 · 알자리온 · 에클레시아 + 플레임·F&V 세트, 패에 파이메나']]}, {'name': '카르테시아 + 루키아스 + 무루루', 'items': [['k27h', '사크라멘툼 · 알자리온 · 미라제이드 · 검은 용 + 플레임·혼·F&V 세트'], ['k27s', '사크라멘툼 · 알자리온 · 미라제이드 · 검은 용 + 플레임·스팅·F&V 세트'], ['k27', '사크라멘툼 · 알자리온 · 미라제이드 · 검은 용 + 플레임·케투·F&V 세트']]}, {'name': '카르테시아 + 파이메나 + 무루루', 'items': [['k26', '사크라멘툼 · 알자리온 · 미라제이드 · 검은 용 + 플레임·혼·스팅 세트'], ['k26a', '사크라멘툼 · 알자리온 · 미라제이드 · 검은 용 + 플레임·혼·케투 세트'], ['k26b', '사크라멘툼 · 알자리온 · 미라제이드 · 검은 용 + 플레임·스팅·케투 세트'], ['k26c', '사크라멘툼 · 알자리온 · 미라제이드 · 검은 용 + 플레임·케투 세트']]}, {'name': '에클레시아 + 무루루 + 아무 몬스터', 'items': [['k23', '사크라멘툼 · 그라멜 · 알자리온 · 루키아스 · 검은 용 + F&V 세트']]}], 'clinks': {'l1h': [{'t': 'Master Duel Meta 드래곤테일 콤보 모음 (dominick)', 'u': 'https://www.masterduelmeta.com/spreadsheet/6a20d431c3038d6b28c66ace'}], 'l1s': [{'t': 'Master Duel Meta 드래곤테일 콤보 모음 (dominick)', 'u': 'https://www.masterduelmeta.com/spreadsheet/6a20d431c3038d6b28c66ace'}], 'g1h': [{'t': '마듀 갤러리: 낙인 드래곤테일 전개 방법 34종 (돼곰이, 31종 개정판)', 'u': 'https://gall.dcinside.com/mgallery/board/view/?id=masterduel&no=5653031'}, {'t': 'Master Duel Meta 드래곤테일 콤보 모음 (dominick)', 'u': 'https://www.masterduelmeta.com/spreadsheet/6a20d431c3038d6b28c66ace'}], 'g1s': [{'t': '마듀 갤러리: 낙인 드래곤테일 전개 방법 34종 (돼곰이, 31종 개정판)', 'u': 'https://gall.dcinside.com/mgallery/board/view/?id=masterduel&no=5653031'}, {'t': 'Master Duel Meta 드래곤테일 콤보 모음 (dominick)', 'u': 'https://www.masterduelmeta.com/spreadsheet/6a20d431c3038d6b28c66ace'}], 'g2h': [{'t': 'Master Duel Meta 드래곤테일 콤보 모음 (dominick)', 'u': 'https://www.masterduelmeta.com/spreadsheet/6a20d431c3038d6b28c66ace'}], 'g2s': [{'t': 'Master Duel Meta 드래곤테일 콤보 모음 (dominick)', 'u': 'https://www.masterduelmeta.com/spreadsheet/6a20d431c3038d6b28c66ace'}], 'q3': [{'t': '마듀 갤러리: 낙인 드래곤테일 전개 방법 34종 (돼곰이, 31종 개정판)', 'u': 'https://gall.dcinside.com/mgallery/board/view/?id=masterduel&no=5653031'}], 'q4h': [{'t': '마듀 갤러리: 낙인 드래곤테일 전개 방법 34종 (돼곰이, 31종 개정판)', 'u': 'https://gall.dcinside.com/mgallery/board/view/?id=masterduel&no=5653031'}], 'q4s': [{'t': '마듀 갤러리: 낙인 드래곤테일 전개 방법 34종 (돼곰이, 31종 개정판)', 'u': 'https://gall.dcinside.com/mgallery/board/view/?id=masterduel&no=5653031'}], 'q3p': [{'t': 'Master Duel Meta: Mululu + 1 (Cyden)', 'u': 'https://www.masterduelmeta.com/combo/6a1d8ca145536314394b1892'}, {'t': 'Master Duel Meta 드래곤테일 스프레드시트 (jeewon · Cyden)', 'u': 'https://www.masterduelmeta.com/spreadsheet/6a2678bc6d36490346e7c8cc'}], 'r1h': [{'t': 'Master Duel Meta: Rahu + 1 (Cyden)', 'u': 'https://www.masterduelmeta.com/combo/6a27b2bbf6f46a155ba0ff32'}, {'t': 'Master Duel Meta 드래곤테일 스프레드시트 (jeewon · Cyden)', 'u': 'https://www.masterduelmeta.com/spreadsheet/6a2678bc6d36490346e7c8cc'}], 'c1h': [{'t': 'Master Duel Meta: Lukias + Dtail + 1 (Cyden)', 'u': 'https://www.masterduelmeta.com/combo/6a2d2dddadcb020500224805'}, {'t': 'Master Duel Meta 드래곤테일 스프레드시트 (jeewon · Cyden)', 'u': 'https://www.masterduelmeta.com/spreadsheet/6a2678bc6d36490346e7c8cc'}], 'r1s': [{'t': 'Master Duel Meta: Rahu + 1 (Cyden)', 'u': 'https://www.masterduelmeta.com/combo/6a27b2bbf6f46a155ba0ff32'}, {'t': 'Master Duel Meta 드래곤테일 스프레드시트 (jeewon · Cyden)', 'u': 'https://www.masterduelmeta.com/spreadsheet/6a2678bc6d36490346e7c8cc'}], 'c1s': [{'t': 'Master Duel Meta: Lukias + Dtail + 1 (Cyden)', 'u': 'https://www.masterduelmeta.com/combo/6a2d2dddadcb020500224805'}, {'t': 'Master Duel Meta 드래곤테일 스프레드시트 (jeewon · Cyden)', 'u': 'https://www.masterduelmeta.com/spreadsheet/6a2678bc6d36490346e7c8cc'}], 'r0': [{'t': '마듀 갤러리: 낙인 드래곤테일 전개 방법 34종 (돼곰이, 31종 개정판)', 'u': 'https://gall.dcinside.com/mgallery/board/view/?id=masterduel&no=5653031'}], 'r2h': [{'t': '마듀 갤러리: 낙인 드래곤테일 전개 방법 34종 (돼곰이, 31종 개정판)', 'u': 'https://gall.dcinside.com/mgallery/board/view/?id=masterduel&no=5653031'}], 'r2s': [{'t': '마듀 갤러리: 낙인 드래곤테일 전개 방법 34종 (돼곰이, 31종 개정판)', 'u': 'https://gall.dcinside.com/mgallery/board/view/?id=masterduel&no=5653031'}], 'r3h': [{'t': '마듀 갤러리: 낙인 드래곤테일 전개 방법 34종 (돼곰이, 31종 개정판)', 'u': 'https://gall.dcinside.com/mgallery/board/view/?id=masterduel&no=5653031'}], 'r3s': [{'t': '마듀 갤러리: 낙인 드래곤테일 전개 방법 34종 (돼곰이, 31종 개정판)', 'u': 'https://gall.dcinside.com/mgallery/board/view/?id=masterduel&no=5653031'}], 'r4h': [{'t': '마듀 갤러리: 낙인 드래곤테일 전개 방법 34종 (돼곰이, 31종 개정판)', 'u': 'https://gall.dcinside.com/mgallery/board/view/?id=masterduel&no=5653031'}], 'r4s': [{'t': '마듀 갤러리: 낙인 드래곤테일 전개 방법 34종 (돼곰이, 31종 개정판)', 'u': 'https://gall.dcinside.com/mgallery/board/view/?id=masterduel&no=5653031'}], 'r5': [{'t': '마듀 갤러리: 낙인 드래곤테일 전개 방법 34종 (돼곰이, 31종 개정판)', 'u': 'https://gall.dcinside.com/mgallery/board/view/?id=masterduel&no=5653031'}], 'q4': [{'t': '마듀 갤러리: 낙인 드래곤테일 전개 방법 34종 (돼곰이, 31종 개정판)', 'u': 'https://gall.dcinside.com/mgallery/board/view/?id=masterduel&no=5653031'}], 'r1': [{'t': 'Master Duel Meta: Rahu + 1 (Cyden)', 'u': 'https://www.masterduelmeta.com/combo/6a27b2bbf6f46a155ba0ff32'}, {'t': 'Master Duel Meta 드래곤테일 스프레드시트 (jeewon · Cyden)', 'u': 'https://www.masterduelmeta.com/spreadsheet/6a2678bc6d36490346e7c8cc'}], 'c1': [{'t': 'Master Duel Meta: Lukias + Dtail + 1 (Cyden)', 'u': 'https://www.masterduelmeta.com/combo/6a2d2dddadcb020500224805'}, {'t': 'Master Duel Meta 드래곤테일 스프레드시트 (jeewon · Cyden)', 'u': 'https://www.masterduelmeta.com/spreadsheet/6a2678bc6d36490346e7c8cc'}], 'r2': [{'t': '마듀 갤러리: 낙인 드래곤테일 전개 방법 34종 (돼곰이, 31종 개정판)', 'u': 'https://gall.dcinside.com/mgallery/board/view/?id=masterduel&no=5653031'}], 'r3': [{'t': '마듀 갤러리: 낙인 드래곤테일 전개 방법 34종 (돼곰이, 31종 개정판)', 'u': 'https://gall.dcinside.com/mgallery/board/view/?id=masterduel&no=5653031'}], 'r4': [{'t': '마듀 갤러리: 낙인 드래곤테일 전개 방법 34종 (돼곰이, 31종 개정판)', 'u': 'https://gall.dcinside.com/mgallery/board/view/?id=masterduel&no=5653031'}], 'k27h': [{'t': '마듀 갤러리: 낙인 드래곤테일 전개 방법 34종 (돼곰이, 31종 개정판)', 'u': 'https://gall.dcinside.com/mgallery/board/view/?id=masterduel&no=5653031'}], 'k27s': [{'t': '마듀 갤러리: 낙인 드래곤테일 전개 방법 34종 (돼곰이, 31종 개정판)', 'u': 'https://gall.dcinside.com/mgallery/board/view/?id=masterduel&no=5653031'}], 'k27': [{'t': '마듀 갤러리: 낙인 드래곤테일 전개 방법 34종 (돼곰이, 31종 개정판)', 'u': 'https://gall.dcinside.com/mgallery/board/view/?id=masterduel&no=5653031'}], 'k26': [{'t': '마듀 갤러리: 낙인 드래곤테일 전개 방법 34종 (돼곰이, 31종 개정판)', 'u': 'https://gall.dcinside.com/mgallery/board/view/?id=masterduel&no=5653031'}], 'k26a': [{'t': '마듀 갤러리: 낙인 드래곤테일 전개 방법 34종 (돼곰이, 31종 개정판)', 'u': 'https://gall.dcinside.com/mgallery/board/view/?id=masterduel&no=5653031'}], 'k26b': [{'t': '마듀 갤러리: 낙인 드래곤테일 전개 방법 34종 (돼곰이, 31종 개정판)', 'u': 'https://gall.dcinside.com/mgallery/board/view/?id=masterduel&no=5653031'}], 'k26c': [{'t': '마듀 갤러리: 낙인 드래곤테일 전개 방법 34종 (돼곰이, 31종 개정판)', 'u': 'https://gall.dcinside.com/mgallery/board/view/?id=masterduel&no=5653031'}], 'k23': [{'t': '마듀 갤러리: 낙인 드래곤테일 전개 방법 34종 (돼곰이, 31종 개정판)', 'u': 'https://gall.dcinside.com/mgallery/board/view/?id=masterduel&no=5653031'}]}},
]
_b=SEL[0]
for g in _b['groups']:
    if g['name']=='루키아스 + 아무 몬스터': g['name']='루키아스 + 드래곤테일 이외 몬스터'; g['items'].append(['l1k','케투로 파이메나 2장 → 상대 턴 믹시아 · 아이온'])
    if g['name']=='루키아스 + 파이메나': g['items'].append(['l2m','믹시아 · 알자리온 + 플레임·케투 세트, 패에 파이메나·무루루'])
_b['groups']+= [
 {'name':'루키아스 + 무루루','items':[['lmu','알자리온 · 미라제이드 + 플레임 세트, 패에 파이메나·무루루'],['lmum','믹시아 · 알자리온 + 플레임 세트, 패에 파이메나·루키아스']]},
 {'name':'케투 + 파이메나','items':[['kfa','알자리온 · 미라제이드 + 플레임·케투 세트, 패에 파이메나'],['kfam','믹시아 · 알자리온 + 플레임·케투 세트, 패에 파이메나']]},
 {'name':'케투 + 무루루','items':[['kmu','알자리온 2장 + 플레임·케투 세트, 패에 파이메나']]},
 {'name':'무루루 + 파이메나','items':[['mufam','믹시아 버전: 알자리온 · 믹시아 + 플레임·케투 세트 → 상대 턴 아이온'],['mufah','보유 버전: 알자리온 2장 + 플레임, 패에 파이메나·루키아스 → 상대 턴 믹시아 · 아이온'],['mufa','알자리온 2장 + 플레임·케투 세트, 패에 파이메나']]},
 {'name':'에클레시아 1장','items':[['ec0','검은 용의 에클레시아 · 카르테시아 (상대 턴 알버스 융합 · 카르테시아 융합)']]},
 {'name':'에클레시아 + 무루루','items':[['emx','믹시아 버전: 검은 용 · 드라군 · 에클레시아, 패에 파이메나 → 상대 턴 믹시아 · 아이온'],['ems','드라군 버전: 검은 용 · 사크라멘툼 드라군 · 알자리온 + 플레임, 패에 파이메나'],['emu','검은 용의 에클레시아 · 그랑기뇰, 패에 카르테시아·파이메나·에클레시아, 묘지에 린드블룸']]},
 {'name':'에클레시아 + 우르굴라·판','items':[['eur','검은 용의 에클레시아 · 사크라멘툼 드라군 · 에클레시아, 패에 파이메나']]},
 {'name':'에클레시아 + 알버스의 낙윤','items':[['eaz','검은 용의 에클레시아 · 낙인룡 알비온 · 그랑기뇰, 패에 에클레시아, 묘지에 린드블룸']]},
 {'name':'하얀 용의 낙윤 + 우르굴라·판','items':[['wum','믹시아 버전: 검은 용 · 믹시아 · 루키아스 + F&V, 패에 카르테시아·에클레시아·파이메나 → 상대 턴 아이온'],['wdu','검은 용의 에클레시아 · 드라군 · 루키아스 · 에클레시아 + F&V, 패에 파이메나·카르테시아']]},
 {'name':'하얀 용의 낙윤 + 알버스의 낙윤','items':[['wzm','믹시아 버전: 검은 용 · 믹시아, 패에 카르테시아·에클레시아·낙인융합 → 상대 턴 아이온'],['wdz','검은 용의 에클레시아 · 낙인룡 알비온 · 그랑기뇰, 패에 에클레시아·낙인융합, 묘지에 린드블룸']]},
 {'name':'하얀 용의 낙윤 + 빛·어둠 몬스터 (뵐러·니비루 등)','items':[['wdlm','믹시아 버전: 검은 용 · 믹시아 + F&V 세트, 패에 카르테시아·에클레시아 → 상대 턴 아이온'],['wdl','검은 용의 에클레시아 · 그랑기뇰 + F&V, 패에 카르테시아·에클레시아, 묘지에 린드블룸']]},
 {'name':'하얀 용의 낙윤 + 패 트랩 (우라라·G·후와로스·푸루리아 등)','items':[['wdo','검은 용의 에클레시아 · 믹시아 + F&V, 패에 카르테시아·에클레시아 → 상대 턴 아이온']]},
 {'name':'카르테시아 + 케투','items':[['ckm','그랑기뇰 · 하얀 용의 낙윤 · 에클레시아 + 라후 세트, 패에 카르테시아']]},
 {'name':'케투 + 라후','items':[['kra','알자리온 · 루키아스 + 플레임·케투 세트, 패에 파이메나 → 상대 턴 믹시아·아이온']]},
 {'name':'낙인융합 + 루키아스','items':[['bfl','사크라멘툼 드라군 · 하얀 용의 낙윤 · 에클레시아 + 플레임·F&V 세트']]},
 {'name':'낙인융합 + 파이메나','items':[['bff','낙인융합 1장 결과 + 상대 턴 파이메나로 사크라멘툼 드라군·믹시아']]},
 {'name':'무루루 + 아무 몬스터 (파이메나·루키아스·우르굴라 X, 무루루 2장 O)','items':[['mux','알자리온 2장 + 플레임 세트']]},
 {'name':'무루루 + 우르굴라·판','items':[['muum','믹시아 버전: 알자리온 · 믹시아 + 플레임·케투 세트 → 상대 턴 아이온'],['muuh','보유 버전: 알자리온 2장 + 플레임, 패에 파이메나·루키아스 → 상대 턴 믹시아 · 아이온'],['muu','알자리온 2장 + 플레임·케투 세트, 패에 파이메나 (무루루 + 파이메나와 같음)']]},
 {'name':'카르테시아 + 패 트랩 (우라라·G·후와로스·푸루리아 등)','items':[['cxm','믹시아 → 상대 턴 그랑기뇰 · 하얀 용의 낙윤 · 에클레시아']]},
 {'name':'카르테시아 + 무루루','items':[['cmux','믹시아 버전: 드라군 · 카르테시아, 패에 파이메나 → 상대 턴 믹시아 · 아이온'],['cmg','그랑기뇰 · 하얀 용의 낙윤 · 에클레시아, 패에 카르테시아·파이메나'],['cmu','사크라멘툼 드라군 · 알자리온 + 플레임 세트, 패에 파이메나']]},
 {'name':'카르테시아 + 빛·어둠 몬스터 (카르테시아 2장·뵐러·니비루 등)','items':[['cld','그랑기뇰 · 하얀 용의 낙윤 · 에클레시아, 패에 카르테시아']]},
 {'name':'카르테시아 + 우르굴라·판','items':[['cur','사크라멘툼 드라군 · 카르테시아, 패에 파이메나 → 상대 턴 믹시아·아이온']]},
 {'name':'카르테시아 + 알버스의 낙윤','items':[['cza','그랑기뇰 · 하얀 용의 낙윤 · 에클레시아 + F&V 세트']]},
 {'name':'카르테시아 + 파이메나 + 케투','items':[['ckf','알자리온 · 미라제이드 + 플레임·케투 세트, 패에 파이메나·무루루·카르테시아'],['cku','사크라멘툼 드라군 · 카르테시아 · 알자리온 + 플레임·케투 세트, 패에 파이메나']]},
 {'name':'하얀 용의 낙윤 + 케투','items':[['wkm','믹시아 버전: 검은 용 · 카르테시아 · 믹시아 · 알자리온 + 플레임·케투·F&V, 패에 루키아스·에클레시아'],['wdk','검은 용의 에클레시아 · 카르테시아 · 드라군 · 알자리온 · 에클레시아 + 플레임·케투·F&V 세트']]},
 {'name':'하얀 용의 낙윤 + 카르테시아','items':[['wdc','검은 용의 에클레시아 · 그랑기뇰 + F&V 세트, 패에 카르테시아·에클레시아, 묘지에 린드블룸']]},
 {'name':'파이메나 + 우르굴라·판 + 아무 몬스터','items':[['pux','알자리온 2장 · 루키아스 + 플레임 세트, 패에 파이메나·무루루 → 상대 턴 믹시아·아이온']]},
 {'name':'카르테시아 + 파이메나 + 라후','items':[['cfr','알자리온 · 사크라멘툼 드라군 · 믹시아 + 플레임·케투 세트 → 상대 턴 아이온(소재 3)']]},
 {'name':'케투 + 드래곤테일 이외 몬스터','items':[['kel','알자리온 2장 + 플레임·케투 세트, 패에 파이메나 (루키아스 전개와 같음)']]},
 {'name':'라후 + 아무 몬스터','items':[['rax','알자리온 · 믹시아 + 플레임 세트, 패에 파이메나']]},
 {'name':'라후 + 카르테시아','items':[['rca','알자리온 · 드라군 · 루키아스 + 플레임, 패에 파이메나 → 상대 턴 믹시아 · 아이온']]},
 {'name':'라후 + 에클레시아 + 드래곤테일 이외 몬스터','items':[['rex','검은 용 · 드라군 · 알자리온 · 루키아스 + 플레임, 패에 파이메나 → 상대 턴 믹시아 · 아이온']]},
 {'name':'라후 + 에클레시아 + 드래곤테일 몬스터','items':[['red','검은 용 · 드라군 · 알자리온 · 루키아스 + 플레임·호른, 패에 파이메나 → 상대 턴 믹시아 · 아이온']]},
 {'name':'낙인융합 1장','items':[['bf1t','알비온 · 그랑기뇰 · 하얀 용의 낙윤 · 에클레시아 (성흔을 먹는 용 보존)'],['bf1','그랑기뇰 · 하얀 용의 낙윤 · 에클레시아 + F&V 세트'],['bf1m','알비온 · 믹시아 (상대 턴 아이온)']]},
]
_b['combos']+=['rex','red','cmux','emx','rca','mufam','mufah','muum','muuh','wdlm','d1r','ems','bf1t','d3m','wum','wzm','d4m','wkm','ec0','emu','eur','eaz','wdu','wdz','wdl','wdo','ckm','kra','bfl','bff','l1k','l2m','lmu','lmum','kfa','kfam','kmu','mufa','wdk','wdc','mux','muu','cmg','cld','cxm','cmu','cur','cza','ckf','cku','cfr','pux','kel','rax','bf1','bf1m']

# ---- 전수 탐색 결과로 기본 파츠 목록 교체 ----
# 2026-11-18: 검색으로 찾은(출처가 있는) 전개만 남김. 계산 결과(auto_dt.json)와 출처 없는 전개는 가이드에서 내림
# 검수(2026-11-19): 함정 대체 판을 원본과 같은 손패 그룹·출처로 등록, 표기 통일
_VAR={'mg3':[('mg3a','스팅 대신 케투 세트'),('mg3b','혼 대신 케투 세트'),('mg3c','혼·스팅 없이 플레임·케투 세트')],'shm':[('shmh','스팅 대신 혼 세트'),('shmk','스팅 대신 케투 세트')]}
for _x in SEL:
    for _g in _x.get('groups',[]):
        for _it in list(_g['items']):
            for _n,_lab in _VAR.get(_it[0],[]):
                _g['items'].append([_n,_it[1]+' ('+_lab+')'])
                _x.setdefault('combos',[]).append(_n)
                if _it[0] in _x.get('clinks',{}): _x['clinks'][_n]=_x['clinks'][_it[0]]
_LAB={'d3':'검은 용 · 사크라멘툼 · 무루루 · 알자리온 + 플레임·라후·F&V 세트, 패에 파이메나·카르테시아','d4':'검은 용 · 카르테시아 · 사크라멘툼 · 알자리온 · 무루루 + 플레임·케투·F&V 세트, 패에 파이메나·에클레시아'}
for _x in SEL:
    for _g in _x.get('groups',[]):
        for _it in _g['items']:
            if _it[0] in _LAB: _it[1]=_LAB[_it[0]]
            _it[1]=_it[1].replace('사크라멘툼 드라군','사크라멘툼').replace('드라군','사크라멘툼')
KEEP=set()
for _x in SEL: KEEP|=set(_x.get('clinks',{}).keys())
KEEP|={'u1h','u1s','u1','u2h','u2s','u2'}  # 사용자가 직접 알려 준 수순 (2026-11-19)
KEEP-={'o1'}  # 낙인개막·알베르·혁의 낙인·루벨리온·쿠엠 5장이 모두 있어야 켜지는 전개: 사용자 요청으로 내림 (2026-11-18)
for _x in SEL:
    _x['combos']=[c for c in _x.get('combos',[]) if c in KEEP]
    _gs=[]
    for _g in _x.get('groups',[]):
        _it=[i for i in _g['items'] if i[0] in KEEP]
        if _it: _gs.append(dict(_g,items=_it))
    _x['groups']=_gs
import copy
RAW={x['key']:copy.deepcopy(x) for x in SEL}
_base=next(x for x in SEL if x['key']=='base')
for x in SEL:
    if x['key']=='base': continue
    own=[dict(g,items=list(g['items'])) for g in x.get('groups',[])]
    names={g['name']:g for g in own}
    for g in _base['groups']:
        if g['name'] in names: names[g['name']]['items']+=[[i,l+' (기본 파츠 전개)'] for i,l in g['items']]
        else: own.append(dict(g,name=g['name']+' · 기본'))
    x['groups']=own
    x['combos']=x.get('combos',[])+[c for c in _base['combos'] if c not in x.get('combos',[])]
    cl=dict(_base.get('clinks',{})); cl.update(x.get('clinks',{})); x['clinks']=cl

# ---- custom deck builder ----
import sys,collections
sys.path.insert(0,'.')
import io,contextlib
with contextlib.redirect_stdout(io.StringIO()):
    import combos_dt as CD
EXK={'fusion','synchro','link','xyz'}
# 전개마다 필요한 패 표시 (아무 몬스터 필요 여부)
_cmap={c['id']:c for c in dat['combos']}
for sid,deck,start,note,hand,script,res in CD.SETS:
    if sid not in _cmap: continue
    named=[h for h in hand if h!='패사고' and not h.startswith('패의 ')]
    gen=[h for h in hand if h.startswith('패의 ')]
    disc=sum(1 for st in script for op in st[3] if op[0]=='to_gy' and len(op)>2 and op[2]=='hand' and op[1]=='패사고')
    t='필요한 패: '+' + '.join(named)
    if gen: t+=' + '+' + '.join(g[3:]+' 1장' for g in gen)+' (필요)'
    else: t+=' · 아무 몬스터 불필요'
    if disc: t+=f' · 비용으로 버릴 패 {disc}장 (아무 카드)'
    _cmap[sid]['need']=t
    _cmap[sid]['gen']=len(gen)
pool={'main':[],'extra':[]}
for key in ['base','nadir','spirits','shrouded','sanct','horn','sting','trap3','gulpan','gal','bfpost','shrmu','sanana','opening','gulsan']:
    for p in ('main','extra'):
        for n,_ in decks[key][p]:
            if n not in pool[p]: pool[p].append(n)
allm=set(pool['main']);alle=set(pool['extra'])
req={}
for sid,deck,start,note,hand,script,res in CD.SETS:
    if sid=='n3x': continue
    hm=collections.Counter(h for h in hand if h in allm)
    cur=collections.Counter();mx=collections.Counter();ex=collections.Counter()
    def take(n):
        cur[n]+=1;mx[n]=max(mx[n],cur[n])
    for st in script:
        for op in st[3]:
            o=op[0]
            if o=='to_hand' and (len(op)<3 or op[2]=='deck'): take(op[1])
            elif o in('ss','put') and len(op)>3 and op[3]=='deck': take(op[1])
            elif o=='to_gy' and op[2]=='deck': take(op[1])
            elif o=='st' and len(op)>3 and op[3]=='deck': take(op[1])
            elif o=='shuffle' and op[2] in('gy','ban') and op[1] in allm: cur[op[1]]-=1
            if o=='put' and len(op)>3 and op[3]=='extra': ex[op[1]]+=1
            elif o in('fusion','synchro','link','xyz'): ex[op[2]]+=1
            elif o in('to_gy','banish') and op[2]=='extra': ex[op[1]]+=1
    m={n:hm[n]+mx[n] for n in set(hm)|set(mx) if n in allm and hm[n]+mx[n]>0}
    e={n:c for n,c in ex.items() if n in alle}
    # Branded Fusion via Anaconda (not modeled as op)
    if any('낙인융합' in st[0]+st[1]+st[2] and '아나콘다' in st[0] for st in script): m['낙인융합']=max(m.get('낙인융합',0),1)
    req[sid]={'main':m,'extra':e}
# groups: base first, then builds, merged by name
order=['base','nadir','spirits','shrouded','sanct','horn','sting','trap3','gulpan','gal','bfpost','shrmu','sanana','opening','gulsan']
groups=[];gi={}
for key in order:
    for g in RAW[key].get('groups',[]):
        if g['name']=='루키아스 + 드래곤테일 이외 몬스터': g=dict(g,name='루키아스 + 아무 몬스터')
        if g['name'] not in gi:
            gi[g['name']]={'name':g['name'],'items':[]};groups.append(gi[g['name']])
            if 'hand' in g: gi[g['name']]['hand']=g['hand']
        for it in g['items']:
            if it[0] not in [i[0] for i in gi[g['name']]['items']]: gi[g['name']]['items'].append(list(it))
clinks={}
for key in order: clinks.update(RAW[key].get('clinks',{}))
HAND={sid:hand for sid,deck,start,note,hand,script,res in CD.SETS}
PH={'패사고'}
SHORT={'케투 드래곤테일':'케투','라후 드래곤테일':'라후','순백의 성녀 에클레시아':'에클레시아','혁의 성녀 카르테시아':'카르테시아','드래곤테일 루키아스':'루키아스','드래곤테일 무루루':'무루루','드래곤테일 파이메나':'파이메나','드래곤테일 우르굴라':'우르굴라','낙인의 기염':'낙인의 기염','천저의 사도':'천저의 사도','낙인융합':'낙인융합','하얀 용의 낙윤':'하얀 용의 낙윤','알버스의 낙윤':'알버스의 낙윤','인도하는 성녀 쿠엠':'쿠엠','데스피아의 도화 알베르':'알베르','낙인개막':'낙인개막','흑의룡 알비온':'흑의룡 알비온'}
for g in groups:
    h=[x for x in (g.get('hand') or HAND.get(g['items'][0][0],[])) if x not in PH]
    g['size']=len(h)
    g['cards']=[SHORT[x] for x in h if x in SHORT and SHORT[x] not in ('우르굴라','파이메나','알버스의 낙윤')]

basemap={p:dict(decks['base'][p]) for p in ('main','extra')}
builds=[]
for key in order[1:]:
    d=decks[key];cards=[]
    for p in ('main','extra'):
        for n,c in d[p]:
            if c>basemap[p].get(n,0):
                cards.append([p,n,c,1 if n in d.get('range',{}) else c])
    own={(c[0],c[1]) for c in cards}
    uses=sorted({(p,n) for cid in RAW[key].get('combos',[]) if cid in req for p in ('main','extra') for n in req[cid][p] if (p,n) not in own})
    builds.append({'key':key,'name':RAW[key]['name'].replace(' 추가 구축',''),'cards':cards,'uses':[list(u) for u in uses],'combos':[c for c in RAW[key].get('combos',[]) if c in req],'how':d.get('how',[])})
# 추가 구축을 카드 1장 단위로 쪼갬 (덱 리스트에서 카드별로 켜고 끔)
_cards={}
for _b in builds:
    for p,n,c,mn in _b['cards']:
        e=_cards.setdefault((p,n),{'c':0,'how':[]}); e['c']=max(e['c'],c)
        for h in _b.get('how',[]):
            key=n.replace('드래곤테일 ','').replace(' 드래곤테일','')
            if (n in h or key in h) and h not in e['how']: e['how'].append(h)
builds=[]
for (p,n),e in _cards.items():
    ids=[sid for sid,r in req.items() if r[p].get(n,0)>basemap[p].get(n,0)]
    if n not in ('낙인의 기염',) and not [i for i in ids if i in KEEP]: continue  # 넣어도 켜지는 전개가 없는 카드는 버튼을 만들지 않음 (낙인의 기염은 사용자 요청으로 유지)
    builds.append({'key':'c:'+n,'name':n,'cards':[[p,n,1,0]],'uses':[],'combos':[i for i in ids if i in KEEP],'how':e['how']})
NOTES=['이 가이드의 전개는 공략 사이트에서 찾은 수순만 실었습니다(Master Duel Meta, 일본 ygotac 등). 전개마다 출처 링크가 있고, 넣기 전에 카드 텍스트대로 한 단계씩 검증했습니다. 2026년 11월 5일 금지 제한(드래곤테일 프릭술 금지)을 반영해 프릭술을 쓰는 전개는 싣지 않았습니다.',
'덱 리스트에서 카드를 추가하면 그 카드가 필요한 전개가 켜집니다(예: 드래곤테일 혼, 그라멜, 판, 진염룡 알비온).',
'검증에 쓴 규칙: 각 효과의 이름당 1턴 1번 · 하얀 용의 낙윤 패 효과 뒤에는 레벨 8 융합·싱크로만(레벨 7 그라멜, 아나콘다 불가) · 무루루 융합 효과·라후·낙인융합 뒤에는 융합 몬스터만 · 라후는 아나콘다를 낸 뒤에 발동 · 아나콘다 효과 뒤에는 특수 소환 불가 · 라후는 덱의 드래곤테일을 먼저 고른 뒤 패의 몬스터를 더함 · 알자리온은 패에서 쓴 소재 수만큼만 되돌림.',
'케투로 시작하는 손패는 케투를 1턴에 1장만 발동할 수 있어서, 드래곤테일 몬스터 효과로 세트한 2번째 케투는 다음 턴용입니다. 루키아스·우르굴라처럼 드래곤테일 몬스터 2장이 융합 소재로 동시에 묘지로 가면 케투와 라후를 둘 다 세트하고 그 턴에 둘 다 발동할 수 있는데, 이게 루키아스 + 파이메나 전개입니다.',
'구축 혼합 · 천저의 사도 + 다른 초동: 천저를 쓰면 그 턴 엑스트라 덱 소환이 막혀서 천저 전개와 다른 전개 중 하나만 고릅니다. · 낙인의 기염 + 쿠엠/알베르: 쿠엠은 마법사족, 알베르는 악마족이라 기염 + 마법사족 전개와 같거나(쿠엠) 안 됩니다(알베르: 악마족 레벨 8 융합 중 공격력·수비력 2500이 없음). · 낙인개막 + 다른 초동: 낙인개막 → 알베르 → 낙인융합이라 낙인융합 + 그 카드 전개와 같습니다(낙인개막 비용으로 패 1장 필요). · 혁의 낙인: 묘지에 알버스·데스피아가 있어야 해서 혼자는 안 되고, 하얀 용의 낙윤·쿠엠 전개 뒤에 추가 융합 1장을 더하는 정도입니다.',
'하얀 용의 낙윤이 섞인 손패는 하얀 용의 낙윤 전개를 우선합니다. 하얀 용의 낙윤 효과를 쓴 턴에는 엑스트라 덱에서 레벨 8 융합·싱크로만 낼 수 있어서 아나콘다 루트와 같이 쓸 수 없습니다.',
'· 카르테시아 2장: 검은 용의 에클레시아는 덱·묘지에서만 꺼내므로 묘지의 에클레시아를 꺼내고, 카르테시아는 패에서 자기 효과로 특수 소환합니다.',
'· 쿠엠: 천저의 사도·낙인개막 전개는 일반 소환을 안 쓰므로 패의 쿠엠을 일반 소환합니다. · 알버스의 낙윤: 낙인융합(직접·아나콘다)은 패의 소재도 쓸 수 있어서 그대로 됩니다.',
'· 라후·플레임·혼처럼 1장 넣는 마법·함정: 패의 카드를 직접 발동·세트하고, 드래곤테일 몬스터의 세트 효과는 남은 다른 드래곤테일 마법·함정을 세트합니다. 케투가 패에 있으면 그 케투를 발동하고 세트 효과로는 라후·플레임을 세트합니다.']
custom={'baseCombos':[c for c in RAW['base']['combos'] if c in req],'gen':[n for n,_,_ in GENPOOL],'notes':NOTES,'key':'dt-deck-v1','base':{'main':decks['base']['main'],'extra':decks['base']['extra']},'baseMap':basemap,'pool':pool,'req':req,'groups':groups,'clinks':clinks,'builds':builds,'sup':CD.SUP,
 'cut':[['공극의 원성룡',0],['심연룡 알버 레나투스',0],['드래곤테일 알자리온',1],['혁언룡 그랑기뇰',0]]}
import copy as _cp
_byid={c['id']:c for c in dat['combos']}
for _g in groups:
    if 'hand' not in _g: continue
    for _it in _g['items']:
        _o=_it[0]; _n=f"{_o}~{__import__('zlib').crc32(_g['name'].encode())%100000}"
        if _n not in _byid:
            _c=_cp.deepcopy(_byid[_o]); _c['id']=_n; _c['title']=_g['name']
            dat['combos'].append(_c); _byid[_n]=_c
            if _o in req: req[_n]=req[_o]
            if _o in custom['baseCombos']: custom['baseCombos'].append(_n)
            for _b in builds:
                if _o in _b['combos']: _b['combos'].append(_n)
            if _o in clinks: clinks[_n]=clinks[_o]
        _it[0]=_n
allids=[i[0] for g in groups for i in g['items']]
MY=[{'key':'my','name':'드래곤테일 낙인','sub':'','deck':'my','combos':allids,'groups':groups,'clinks':clinks}]
DTD=build.page('site_dt/index.html','드래곤테일 낙인 전개 필드 가이드',MY,img,dat,gen,custom)
DTD['short']='드래곤테일 낙인'
DTD['solver']=True
json.dump(DTD,open('bundle_dt.json','w'),ensure_ascii=False)

print(len(img),'imgs')
