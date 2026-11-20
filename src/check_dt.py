import json
b=json.load(open('bundle_dt.json'))
K=b['kinds']; CA,EC='혁의 성녀 카르테시아','순백의 성녀 에클레시아'
T=['낙인룡 알비온','회신룡 배스터드','성흔을 먹는 용']
isend=lambda s:(s['title'] or '').startswith('엔드 페이즈') or ') 엔드 페이즈' in (s.get('desc') or '')
bad=0
for c in b['combos']:
    if '~' in c['id']: continue
    st=c['steps']; prev=st[0]; fus=False; cnt={CA:0,EC:0}
    for i,s in enumerate(st[1:],1):
        if (s['title'] or '').startswith('상대 턴'): break
        added=[n for n in s['gy'] if s['gy'].count(n)>prev['gy'].count(n)]
        if any(K.get(n)=='fusion' for n in added): fus=True
        for n in (CA,EC):
            if isend(s) and s['hand'].count(n)>prev['hand'].count(n) and prev['gy'].count(n)>s['gy'].count(n):
                cnt[n]+=1
                if not fus: bad+=1; print('!! 회수 조건 없음',c['id'],i,n)
                if cnt[n]>1: bad+=1; print('!! 회수 2번',c['id'],n)
        prev=s
    ends=[i for i,s in enumerate(st) if isend(s)]
    for nm in T:
        use=[i for i in ends if (nm+':') in ((st[i]['title'] or '')+' '+(st[i].get('desc') or '')) or ('엔드 페이즈: '+nm) in (st[i]['title'] or '')]
        if not use: continue
        u=use[0]; seen=left=False
        for x in st[1:u]:
            if nm in x['gy']: seen=True
            elif seen: left=True
        if nm not in st[u-1]['gy'] or left: bad+=1; print('!! 엔드 효과 조건',c['id'],nm)
print('문제',bad)
