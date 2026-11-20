import json
from sim import DB
d=json.load(open('data.json'))
k={n:v[0] for n,v in DB.items()}
k.update({'원 포 원':'spell','유벨－다스 엑스트렘 트라우리히 드라헤':'eff','유령토끼':'eff','말살의 지명자':'spell','로기어스텔라 티 폰':'xyz','유벨－다스 에비히 리베 베히터':'fusion','마루챠미 후와로스':'eff','에너미 컨트롤러':'spell','하루 우라라':'eff','Live☆Twin 트러블상':'spell','데먼스미스 아뉴스데이':'link','원시생명체 니비루':'eff','금지된 일적':'spell','증식의 G':'eff','무한포영':'trap','마계특파원 데스캐스터':'eff','드롤 & 로크 버드':'eff','이펙트 뵐러':'eff','삼전의 재':'spell','무덤의 지명자':'spell','무덤의 지명자 (현재 금지 · 빼야 함)':'spell','우:피 팬시볼':'link','시크릿 패스프레이즈':'spell','저택 와라시':'eff','네크로입 프린세스':'fusion','마루챠미 푸루리아':'eff','패사고':'eff'})
d['kinds']=k
FIX=[('딜를','딜을'),('레퀴엠를','레퀴엠을'),('레퀴엠나','레퀴엠이나'),('키스킬는','키스킬은'),('난나을','난나를'),('키스킬와','키스킬과')]
for cb in d['combos']:
    for s in cb['steps']:
        for f in ('title','act','desc'):
            for a,b in FIX: s[f]=s[f].replace(a,b)
json.dump(d,open('data.json','w'),ensure_ascii=False)
