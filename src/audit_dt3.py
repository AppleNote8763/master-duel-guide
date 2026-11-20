import sys,io,contextlib; sys.path.insert(0,'.')
with contextlib.redirect_stdout(io.StringIO()):
    import combos_dt as CD, sim, build_dt as BD
ids=set(i[0].split('~')[0] for g in BD.groups for i in g['items'])
tot=0
for sid,deck,title,note,hand,script,res in CD.SETS:
    if sid not in ids: continue
    P=[]
    for si,item in enumerate(script):
        ops=item[3]; groups=[];cur=[];has=False
        for op in ops:
            k=sim._kind(op)
            if k in('S','R') and has: groups.append(cur);cur=[];has=False
            cur.append(op)
            if k=='S': has=True
        if cur: groups.append(cur)
        if len(item)>4 and item[4]: groups=[list(ops)]
        if len(groups)<2: continue
        for gi,g in enumerate(groups):
            main=next((op for op in g if op[0] in sim.SUMMON),None)
            mats=[op for op in g if op[0]=='to_gy' and op[2] in('hand','deck')]
            hasfus=any(op[0]=='fusion' or (op[0]=='put' and len(op)>3 and op[3]=='extra') for op in g)
            if mats and not hasfus and main and main[0]=='st':
                P.append(f'{si+1}단계 "{item[0]}" ({gi+1}/{len(groups)}): 소재/비용 {[m[1] for m in mats]}이 소환 장면보다 먼저 빠짐 (화면: {sim._auto(main)[0]})')
            if main and main[0]=='put' and len(main)>3 and main[3]=='extra' and not mats and any(any(o[0]=='to_gy' and o[2] in('hand','deck') for o in gg) for gg in groups[:gi]):
                P.append(f'{si+1}단계 "{item[0]}" ({gi+1}/{len(groups)}): {main[1]} 소환 장면에 소재 표시 없음')
            if not main:
                P.append(f'{si+1}단계 "{item[0]}" ({gi+1}/{len(groups)}): 소환·세트 없는 장면이 따로 떨어짐 {[o[0]+":"+str(o[1])[:10] for o in g]}')
    if P: tot+=len(P); print(f'[{sid}] {title}'); [print('   -',x) for x in P]
print('문제',tot)
