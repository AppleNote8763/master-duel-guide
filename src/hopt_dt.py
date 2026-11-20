import json,re
b=json.load(open('bundle_dt.json'))
names=sorted(b['kinds'].keys(),key=len,reverse=True)
def nm(t):
    t=t.replace('2번째 ','').replace('첫 ','')
    for n in names:
        if t.startswith(n): return n,t[len(n):].strip()
    return None,t
bad=0
for c in b['combos']:
    if '~' in c['id']: continue
    seen={}; items=[]
    for s in c['steps'][1:]:
        t=s['title'] or ''; d=s.get('desc') or ''
        if t.startswith('상대 턴'): break
        m=re.match(r'\((\d+)/(\d+)\) (.*?):',d)
        orig=m.group(3) if m else t
        if items and items[-1][0]==orig: continue
        items.append((orig,d))
    for orig,d in items:
        keys=[]
        if orig.startswith('체인:') or orig.startswith('엔드 페이즈:'):
            for seg in re.split(r' / ',re.sub(r'^\(\d+/\d+\) [^:]*: ','',d)):
                n,_=nm(seg.split(':')[0].strip())
                if n and ':' in seg: keys.append((n,'트리거'))
        else:
            n,rest=nm(orig)
            if n and ('효과' in rest):
                kind='묘지' if '묘지' in rest else ('패' if '(패)' in rest else ('소환시' if '소환 시' in rest else '효과'))
                keys.append((n,kind))
            if n and rest.startswith('특수 소환 (패)'): keys.append((n,'패특소'))
        for k in keys:
            seen[k]=seen.get(k,0)+1
    for k,v in seen.items():
        if v>1: bad+=1; print(c['id'],k,v)
print('중복',bad)
