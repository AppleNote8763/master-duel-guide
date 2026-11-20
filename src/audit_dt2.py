import sys,io,contextlib,re,collections; sys.path.insert(0,'.')
with contextlib.redirect_stdout(io.StringIO()):
    import combos_dt as CD, sim, build_dt as BD
C=CD
ids=set(i[0].split('~')[0] for g in BD.groups for i in g['items'])
DRAGON={C.MU,C.UR,C.PA,C.WD,C.AZ,C.ART,C.ALB,'흑의룡 알비온','진염룡 알비온',C.SEC}
SPELL={C.LU,C.FA,C.EC,C.CA,C.GUL,C.EDD,'인도하는 성녀 쿠엠','혼효하는 믹시아'}
DT={C.MU,C.LU,C.FA,C.UR,C.PA,C.ART,C.GUL}
tot=0; nA=nS=nR=0
for sid,deck,title,note,hand,script,res in CD.SETS:
    if sid not in ids: continue
    P=[]; lastART=None
    for si,st in enumerate(script):
        t,a,d,ops=st[0],st[1],st[2],st[3]
        if t.startswith('상대 턴'): break
        # 융합 소재 구성
        for oi,op in enumerate(ops):
            tgt=None
            if op[0]=='fusion': tgt=op[2]; fm=list(op[1])
            elif op[0]=='put' and len(op)>3 and op[3]=='extra': tgt=op[1]; fm=[]
            if tgt in (C.ART,C.GUL):
                nA+=1
                hm=[o[1] for o in ops if o[0]=='to_gy' and o[2]=='hand']
                dm=[o[1] for o in ops if o[0]=='to_gy' and o[2]=='deck']
                if t.startswith(C.FA+' 효과 (패)') and C.FA in hm: hm.remove(C.FA)   # 비용
                allm=fm+hm+dm
                ndt=[m for m in allm if m in DT]
                if not ndt: P.append(f'{si+1}단계: {tgt} 소재에 드래곤테일 몬스터 없음 {allm}')
                # 드래곤테일 1장을 뺀 나머지는 전부 패
                rest_hand=len(hm) - (0 if (fm or dm) and any(m in DT for m in fm+dm) else 1)
                nonhand=[m for m in fm+dm]
                if len(nonhand)>1: P.append(f'{si+1}단계: {tgt} 소재 중 패가 아닌 것이 2장 이상 {nonhand} (드래곤테일 1장 + 나머지는 패여야 함)')
                if len(nonhand)==1 and nonhand[0] not in DT: P.append(f'{si+1}단계: {tgt}의 필드/덱 소재가 드래곤테일이 아님 {nonhand}')
                if tgt==C.GUL and len(allm)!=2: P.append(f'{si+1}단계: 그라멜 소재가 2장이 아님 {allm}')
                if len(hm)<1: P.append(f'{si+1}단계: {tgt} 소재에 패의 몬스터 없음')
                if tgt==C.ART: lastART=(si,len(hm))
        if t.startswith('체인') and '알자리온' in t and lastART and lastART[0]==si-1:
            nR+=1
            r=[o for o in ops if o[0]=='to_hand' and len(o)>2 and o[2] in('gy','field')]
            if len(r)>lastART[1]: P.append(f'{si+1}단계: 알자리온 회수 {len(r)}장 > 패에서 쓴 소재 {lastART[1]}장')
        if t.startswith(C.SEC+' 효과'):
            nS+=1
            ss=[o[1] for o in ops if o[0]=='ss']; sh=[o[1] for o in ops if o[0]=='shuffle']
            if len(ss)==1 and len(sh)==1:
                a1,b1=ss[0],sh[0]
                ok=(a1 in DRAGON and b1 in SPELL) or (a1 in SPELL and b1 in DRAGON)
                if not ok: P.append(f'{si+1}단계: 사크라멘툼 대상이 드래곤 1 + 마법사 1이 아님 ({a1}, {b1})')
            else: P.append(f'{si+1}단계: 사크라멘툼 효과 처리 형태 확인 필요 {ss} {sh}')
    if P:
        tot+=len(P); print(f'[{sid}] {title}'); [print('   -',x) for x in P]
print('문제',tot,'| 융합 검사',nA,'알자리온 회수 검사',nR,'사크라멘툼 검사',nS)
