import sys,io,contextlib,re,collections; sys.path.insert(0,'.')
with contextlib.redirect_stdout(io.StringIO()):
    import combos_dt as CD, sim, build_dt as BD
KE,RA,FA,LU,MU,UR,WD,ANA,BF=CD.KE,CD.RA,CD.FA,CD.LU,CD.MU,CD.UR,CD.WD,CD.ANA,CD.BF
PA=CD.PA; EDD=CD.EDD; CA=CD.CA; SEC=CD.SEC; ART=CD.ART; GUL=CD.GUL
ids=set(i[0].split('~')[0] for g in BD.groups for i in g['items'])
LIM={LU:1,RA:1,MU:2,KE:2,'The Fallen & The Virtuous':2,ANA:1}
SPELLC={FA,LU,'드래곤테일 프리클'}
def kind(n): return sim.DB.get(n,('?',0))[0]
def lvl(n): return sim.DB.get(n,('?',0))[1]
tot=0
for sid,deck,title,note,hand,script,res in CD.SETS:
    if sid not in ids: continue
    P=[]
    H=collections.Counter(hand); G=collections.Counter(); F={}; S={}; BAN=collections.Counter(); taken=collections.Counter(); mx=collections.Counter()
    ns=0; act=collections.Counter(); seteff=collections.Counter(); wdlock=False; fuslock=False; nosp=False
    for si,st in enumerate(script):
        t,a,d,ops=st[0],st[1],st[2],st[3]
        opp=t.startswith('상대 턴'); endp=t.startswith('엔드 페이즈')
        if opp: break
        for nm,key in ((KE,KE+' 발동'),(RA,RA+' 발동'),(BF,BF+' 발동'),(FA+'패',FA+' 효과 (패)'),(UR+'묘지',UR+' 묘지 효과'),(MU+'융합',MU+' 효과 (필드)'),(SEC,SEC+' 효과'),(ANA,ANA+' 효과')):
            if t.startswith(key): 
                act[nm]+=1
                if act[nm]>1: P.append(f'{si+1}단계: {key} 2번째')
        for part in re.split(r' / ',d):
            m=re.match(r'\s*(드래곤테일 (?:무루루|루키아스|파이메나|우르굴라|판))\s*(?:·[^:]*)?:.*세트',part)
            if m:
                seteff[m.group(1)]+=1
                if seteff[m.group(1)]>1: P.append(f'{si+1}단계: {m.group(1)} 세트 효과 2번째')
        for op in ops:
            o=op[0]
            def need(c,src,where):
                if c[src]<=0: P.append(f'{si+1}단계 "{t}": {src}에 없는 {where}')
            if o=='ns':
                ns+=1; 
                if H[op[1]]<=0: P.append(f'{si+1}단계: 패에 없는 {op[1]} 일반 소환')
                H[op[1]]-=1; F[op[2]]=op[1]
                if ns>1: P.append(f'{si+1}단계: 일반 소환 2번째')
            elif o in('ss','put'):
                src=op[3] if len(op)>3 else 'hand'; n=op[1]
                if nosp and not endp: P.append(f'{si+1}단계: 아나콘다 효과 뒤 특수 소환 {n}')
                if src=='gy':
                    if G[n]<=0: P.append(f'{si+1}단계 "{t}": 묘지에 없는 {n} 특소')
                    G[n]-=1
                elif src=='hand':
                    if H[n]<=0: P.append(f'{si+1}단계 "{t}": 패에 없는 {n} 특소')
                    H[n]-=1
                elif src=='ban':
                    if BAN[n]<=0: P.append(f'{si+1}단계 "{t}": 제외에 없는 {n} 복귀')
                    BAN[n]-=1
                elif src=='deck': taken[n]+=1; mx[n]=max(mx[n],taken[n]+hand.count(n))
                elif src=='extra':
                    k=kind(n)
                    if wdlock and not (k in('fusion','synchro') and lvl(n)==8): P.append(f'{si+1}단계: 하얀 용의 낙윤 패 효과 뒤 {n} 소환')
                    if fuslock and k!='fusion': P.append(f'{si+1}단계: 융합만 가능한 상태에서 {n} 소환')
                if op[2] in F: P.append(f'{si+1}단계 "{t}": {op[2]} 자리에 이미 {F[op[2]]} 있음 ({n})')
                F[op[2]]=n
            elif o in('fusion','synchro','link','xyz'):
                mats,n,z=op[1],op[2],op[3]; k=kind(n)
                if nosp: P.append(f'{si+1}단계: 아나콘다 효과 뒤 {n} 소환')
                if wdlock and not (k in('fusion','synchro') and lvl(n)==8): P.append(f'{si+1}단계: 하얀 용의 낙윤 패 효과 뒤 {n}({k} {lvl(n)}) 소환')
                if fuslock and k!='fusion': P.append(f'{si+1}단계: 융합만 가능한 상태에서 {n}({k}) 소환')
                gy=len(op)>4 and op[4]=='gy'
                for m in mats:
                    if gy:
                        if G[m]<=0: P.append(f'{si+1}단계 "{t}": 묘지에 없는 소재 {m}')
                        G[m]-=1
                    else:
                        zz=[q for q,v in F.items() if v==m]
                        if not zz: P.append(f'{si+1}단계 "{t}": 필드에 없는 소재 {m}')
                        else: del F[zz[0]]; G[m]+=1
                if z in F: P.append(f'{si+1}단계 "{t}": {z} 자리에 이미 {F[z]} 있음 ({n})')
                F[z]=n
            elif o=='to_gy':
                n,src=op[1],op[2]
                if src=='hand':
                    if H[n]<=0: P.append(f'{si+1}단계 "{t}": 패에 없는 {n}을 묘지로')
                    H[n]-=1
                elif src=='field':
                    zz=[q for q,v in F.items() if v==n]
                    if not zz: P.append(f'{si+1}단계 "{t}": 필드에 없는 {n}을 묘지로')
                    else: del F[zz[0]]
                elif src=='deck': taken[n]+=1; mx[n]=max(mx[n],taken[n]+hand.count(n))
                G[n]+=1
            elif o=='to_hand':
                n=op[1]; src=op[2] if len(op)>2 else 'deck'
                if src=='gy':
                    if G[n]<=0: P.append(f'{si+1}단계 "{t}": 묘지에 없는 {n} 회수')
                    G[n]-=1
                elif src=='deck': taken[n]+=1; mx[n]=max(mx[n],taken[n]+hand.count(n))
                elif src=='ban': BAN[n]-=1
                H[n]+=1
            elif o=='st':
                n,z,src=op[1],op[2],(op[3] if len(op)>3 else 'deck')
                if src=='hand':
                    if H[n]<=0: P.append(f'{si+1}단계 "{t}": 패에 없는 {n} 발동/세트')
                    H[n]-=1
                elif src=='deck': taken[n]+=1; mx[n]=max(mx[n],taken[n]+hand.count(n))
                elif src=='gy': G[n]-=1
                if z in S: P.append(f'{si+1}단계 "{t}": {z}에 이미 {S[z]} 있는데 {n} 세트')
                S[z]=n
            elif o=='st_gy':
                z=op[1]
                if z not in S: P.append(f'{si+1}단계 "{t}": 빈 {z}를 묘지로')
                else:
                    # 방금 덱에서 세트한 케투/라후를 같은 턴 발동하는 건 마법이라 가능. 함정이면 불가
                    if kind(S[z])=='trap': P.append(f'{si+1}단계 "{t}": 세트한 턴에 함정 {S[z]} 발동')
                    G[S[z]]+=1; del S[z]
            elif o=='banish':
                n,src=op[1],op[2]
                if src=='field':
                    zz=[q for q,v in F.items() if v==n]
                    if not zz: P.append(f'{si+1}단계 "{t}": 필드에 없는 {n} 제외')
                    else: del F[zz[0]]
                elif src=='gy':
                    if G[n]<=0: P.append(f'{si+1}단계 "{t}": 묘지에 없는 {n} 제외')
                    G[n]-=1
                BAN[n]+=1
            elif o=='shuffle':
                n,src=op[1],op[2]
                if src=='gy':
                    if G[n]<=0: P.append(f'{si+1}단계 "{t}": 묘지에 없는 {n} 되돌림')
                    G[n]-=1
                elif src=='field':
                    zz=[q for q,v in F.items() if v==n]
                    if zz: del F[zz[0]]
                elif src=='ban': BAN[n]-=1
                if n in taken and taken[n]>0: taken[n]-=1
        # 우르굴라 회수 대상
        if t.startswith(UR+' 묘지 효과'):
            tg=[op[1] for op in ops if op[0]=='to_hand']
            for x in tg:
                if x not in SPELLC: P.append(f'{si+1}단계: 우르굴라 회수 대상이 마법사족 드래곤테일이 아님 ({x})')
        if t.startswith(WD+' 효과 (패)') or (any(op[0]=='ss' and op[1]==WD and len(op)>3 and op[3]=='hand' for op in ops) and any(op[0]=='to_gy' and op[2]=='extra' for op in ops)): wdlock=True
        if t.startswith(RA+' 발동') or t.startswith(MU+' 효과 (필드)') or t.startswith(BF+' 발동'): fuslock=True
        if t.startswith(ANA+' 효과'): nosp=True; fuslock=True
    for n,c in LIM.items():
        if mx[n]>c or hand.count(n)>c: P.append(f'금제 초과: {n} {max(mx[n],hand.count(n))}장 필요 (허용 {c})')
    lim5=len(F)
    if P:
        tot+=len(P); print(f'[{sid}] {title} — {res[:50]}'); [print('   -',x) for x in P]
print('검사한 전개',len([1 for s in CD.SETS if s[0] in ids]),'문제',tot)
