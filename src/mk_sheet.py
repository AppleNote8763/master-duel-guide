import json,glob
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter
SH={'MU':'무루루','LU':'루키아스','FA':'파이메나','UR':'우르굴라','KE':'케투','RA':'라후','FL':'플레임','WD':'하얀 용의 낙윤','AZ':'알버스의 낙윤','EC':'에클레시아','CA':'카르테시아','BF':'낙인융합','FV':'F&V','GN':'NDM(그 외)','GW':'NDM(마법사족)','GD':'NDM(드래곤족)','ART':'알자리온','ARX':'알자리온','SEC':'드라군','MIX':'믹시아','GRA':'그랑기뇰','ALB':'알비온','TIT':'배스터드','DEV':'성흔을 먹는 용','RIN':'린드블룸','MJ':'미라제이드','EDD':'검은 용의 에클레시아','ANA':'아나콘다','LEN':'레나투스','VOI':'공극의 원성룡','AEO':'아이온'}
ORDER=['WD','EC','CA','BF','LU','MU','FA','UR','KE','RA','AZ','FV','GN','GW','GD']
EXT={'ART','SEC','MIX','GRA','ALB','TIT','DEV','RIN','MJ','EDD','ANA'}
def vec(r):
    v=dict(ex=0,de=0,ng=0,bo=0,fu=0,lock=0,ed3=0,solid=0,cond=0); det=[]
    for w in r['why']:
        if '아이온(' in w:
            n=3 if '3장 이상' in w else 2; v['ex']+=n; v['ed3']=1 if n==3 else 0
            if w.startswith('믹시아'): det.append(f'믹시아 → 아이온({n}장 제외)')
            else: det.append(w.split('(')[0]+f'({n}장 제외)')
            v['cond']+=n
        elif w.startswith('미라제이드'): v['ex']+=1; v['solid']+=1; det.append('미라제이드 제외')
        elif w.startswith('F&V'): v['de']+=1; v['solid']+=1; det.append('F&V 파괴')
        elif w.startswith('플레임'): v['ng']+=1; v['solid']+=1; det.append('플레임 무효(마법)')
        elif w.startswith('린드블룸'): v['ng']+=1; v['solid']+=1; det.append('린드블룸 무효')
        elif w.startswith('무루루 → 알자리온'): v['bo']+=1; v['ng']+=1; v['cond']+=2; det.append('무루루 → 알자리온(바운스 + 효과 무효)')
        elif w.startswith('파이메나 → 알자리온'): v['bo']+=1; v['cond']+=1; det.append('파이메나 → 알자리온(바운스)')
        elif w.startswith('알버스의 낙윤 호출'):
            n=2 if 'DEV' in r['ex'] else 1; v['fu']+=n; v['cond']+=n; det.append(f'알버스의 낙윤 융합({n}장)')
        elif w.startswith('드라군'): v['lock']=1; det.append('드라군 락')
    v['ht']=sum(1 for x in r['h'] if x in('GN','GW','GD'))
    v['res']=sum(1 for x in r['h'] if x in('CA','EC','FA','WD','LU','MU','UR','BF'))
    return v,det
rows=[]; summ=[]
for f in glob.glob('r3/*.jsonl'):
    d=json.loads(open(f).read())
    if not d.get('res'): continue
    h=sorted(d['hand'].split(','),key=ORDER.index)
    cnt={}
    for c in h: cnt[c]=cnt.get(c,0)+1
    name=' + '.join(SH[c]+(f' {n}장' if n>1 else '') for c,n in cnt.items())
    rs=[]
    for r in d['res']:
        v,det=vec(r); tot=v['ex']+v['de']+v['ng']+v['bo']+v['fu']
        rs.append((tot,v['solid'],v,det,r))
    rs.sort(key=lambda x:(-x[0],-x[1],-x[2]['res']))
    key=(len(h),[ORDER.index(c) for c in h])
    for i,(tot,sol,v,det,r) in enumerate(rs,1):
        rows.append((key,[name,len(h),i,' · '.join(SH[x] for x in r['fld']) or '-',' · '.join(SH[x] for x in r['st']) or '-',' · '.join(SH[x] for x in r['h']) or '-',' · '.join(SH[x] for x in r['gy'] if x in EXT) or '-',
            v['ex'],v['de'],v['ng'],v['bo'],v['fu'],None,v['solid'],v['cond'],'있음' if v['lock'] else '-','가능' if v['ed3'] else '-',v['ht'],v['res'],'보존' if 'DEV' in r['ex'] else '사용','사용' if 'ANA' not in r['ex'] else '-',' / '.join(det) or '-']))
    summ.append((key,[name,len(h),len(rs),rs[0][0],rs[0][1],' · '.join(SH[x] for x in rs[0][4]['fld']) or '-',' · '.join(SH[x] for x in rs[0][4]['st']) or '-','예' if d.get('cap') else '-']))
rows.sort(key=lambda x:(x[0],x[1][2])); summ.sort(key=lambda x:x[0])
F=Font(name='Arial',size=10); FB=Font(name='Arial',size=10,bold=True,color='FFFFFF'); HF=PatternFill('solid',fgColor='305496'); ALT=PatternFill('solid',fgColor='EEF3FA')
wb=Workbook(); ws=wb.active; ws.title='결과물'
hdr=['손패','장수','안','필드','세트','패','묘지의 엑스트라 덱 몬스터','제외','파괴','무효','바운스','융합 제거','방해 합계','세워 둔 방해','융합 통과 필요','드라군 락','아이온 3장 소재','패 트랩','다음 턴 자원','성흔을 먹는 용','아나콘다','상대 턴 방해 내용']
wid=[40,6,5,40,20,30,26,6,6,6,7,9,9,11,13,10,13,8,11,13,9,90]
ws.append(hdr)
prev=None; alt=False
for key,r in rows:
    if r[0]!=prev: alt=not alt; prev=r[0]
    ws.append(r); n=ws.max_row
    ws.cell(n,13).value=f'=SUM(H{n}:L{n})'
    for c in ws[n]:
        c.font=F
        if alt: c.fill=ALT
for c in range(1,len(hdr)+1):
    cell=ws.cell(1,c); cell.font=FB; cell.fill=HF; cell.alignment=Alignment(horizontal='center',wrap_text=True); ws.column_dimensions[get_column_letter(c)].width=wid[c-1]
ws.freeze_panes='D2'; ws.auto_filter.ref=ws.dimensions
w1=wb.create_sheet('손패 요약')
w1.append(['손패','장수','결과물 수','최대 방해 합계','그때 세워 둔 방해','그때 필드','그때 세트','계산 중단(미완)'])
for _,r in summ: w1.append(r)
for row in w1.iter_rows():
    for c in row: c.font=F
for c,w in zip('ABCDEFGH',[40,6,10,14,16,40,20,14]): w1.column_dimensions[c].width=w
for c in range(1,9):
    cell=w1.cell(1,c); cell.font=FB; cell.fill=HF
w1.freeze_panes='A2'; w1.auto_filter.ref=w1.dimensions
w2=wb.create_sheet('읽는 법')
for t in ['· 한 줄 = 그 손패로 선공 1턴에 만들 수 있는 결과물 1개. 가중치 점수 없이, 방해를 종류별 횟수로 셌습니다.',
 '· 남긴 기준: 같은 손패 안에서 제외·파괴·무효·바운스·융합 제거·드라군 락·패 트랩·다음 턴 자원 8칸 중 어느 칸에서도 다른 결과에 전부 뒤지지는 않는 결과만 남겼습니다. 8칸이 모두 같은 결과는 1개만 남겼습니다.',
 '· 제외: 미라제이드 1, 믹시아 → 아이온 2 (전개 중 자연히 속성이 다른 융합 몬스터가 2종 이상 쌓였으면 3, "아이온 3장 소재" 칸에 표시되고 상대 엑스트라 덱 3장 제외도 가능).',
 '· 파괴: 세트한 F&V 1 / 무효: 세트한 플레임 1(필드 앞면 마법), 묘지의 린드블룸 1(엑스트라 덱 몬스터 효과), 무루루가 소재가 될 때 1.',
 '· 바운스: 필드의 무루루 → 알자리온 1, 패의 파이메나 → 알자리온 1 / 융합 제거: 검은 용의 에클레시아·에클레시아 → 알버스의 낙윤으로 상대 몬스터와 융합 1 (성흔을 먹는 용이 엑스트라 덱에 남아 있으면 2).',
 '· 방해 합계 = 제외 + 파괴 + 무효 + 바운스 + 융합 제거 (드라군 락은 합계에 넣지 않고 따로 표시).',
 '· 세워 둔 방해 = 내 턴에 이미 깔아 둔 것(미라제이드, F&V, 플레임, 린드블룸). 융합 통과 필요 = 상대 턴에 융합·효과가 통과해야 생기는 것(아이온, 알자리온 바운스, 알버스의 낙윤 융합).',
 '· 정렬: 손패별로 방해 합계가 큰 순, 같으면 세워 둔 방해가 많은 순. "안" 번호는 그 순서입니다.',
 '· 패 트랩 = 패에 남은 NDM 수. 다음 턴 자원 = 패에 남은 카르테시아·에클레시아·파이메나·하얀 용의 낙윤·루키아스·무루루·우르굴라·낙인융합 수.',
 '· 가정: 선공 1턴, 상대 필드 없음, 상대 방해 없음, 기본 파츠 덱(메인 21장·엑스트라 15장). NDM = 드래곤테일 이외 몬스터(마법사족·드래곤족은 빛·어둠이 아닌 것으로 가정, 드래곤족은 일반 소환 불가).',
 '· 계산에서 제외한 수: 레나투스 사용, 공극의 원성룡 융합 소환, F&V로 알비온·배스터드 이외의 자기 몬스터 파괴. 알자리온의 패 소재는 2장까지만 계산(실제로는 3장 이상 가능).',
 '· 계산에 없는 것: 패 버리기 비용(알버스의 낙윤·초융합), 흑의룡·초융합 등 기본 파츠 밖 카드, 수순. 수순이 필요한 줄은 손패와 안 번호를 알려 주세요.']:
    w2.append([t]); w2.cell(w2.max_row,1).font=F
w2.column_dimensions['A'].width=170
wb.save('드테낙인_전개_결과물_전체.xlsx'); print(len(rows),len(summ))
