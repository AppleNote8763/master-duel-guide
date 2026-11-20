import json, os, shutil, build
import re
def _josa_fix(d):
    names=sorted({n for n in list(d.get('kinds',{}))+list(d.get('img',{})) if n and '가'<=n[-1]<='힣'},key=len,reverse=True)
    if not names: return d
    info={}
    for n in names:
        o=ord(n[-1])-0xAC00; info[n]=(o%28!=0, o%28==8)
    pat=re.compile('('+'|'.join(re.escape(n) for n in names)+r')(으로|로|를|을|는|은|가|이|와|과)(?![가-힣])')
    def rep(m):
        n,p=m.group(1),m.group(2); b,r=info[n]
        if p in('로','으로'): q='로' if (not b or r) else '으로'
        else: q={'를':'을','을':'을','는':'은','은':'은','가':'이','이':'이','와':'과','과':'과'}[p] if b else {'를':'를','을':'를','는':'는','은':'는','가':'가','이':'가','와':'와','과':'와'}[p]
        return n+q
    def walk(x):
        if isinstance(x,str): return pat.sub(rep,x)
        if isinstance(x,list): return [walk(v) for v in x]
        if isinstance(x,dict): return {k:(walk(v) if k not in ('kinds','img','zones') else v) for k,v in x.items()}
        return x
    return walk(d)

os.makedirs('site_all/card', exist_ok=True)
for src in ('site_dt/card', 'site_twin/card', 'site_yubel/card'):
    for f in os.listdir(src):
        if not os.path.exists(f'site_all/card/{f}'): shutil.copy(f'{src}/{f}', f'site_all/card/{f}')
S0 = {k: json.load(open(f'bundle_{k}.json')) for k in ('dt', 'tw', 'yb')}
S = {k: _josa_fix(v) for k, v in S0.items()}
miss = [(k, n, p) for k, d in S.items() for n, p in d['img'].items() if not os.path.exists('site_all/' + p)]
print('missing imgs', miss[:5], len(miss))
build.page_multi('site_all/index.html', '마스터 듀얼 전개 필드 가이드', S)
print(len(os.listdir('site_all/card')), os.path.getsize('site_all/index.html'))
