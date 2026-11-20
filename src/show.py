import sys,json
KO={'MU':'무루루','LU':'루키아스','FA':'파이메나','UR':'우르굴라','KE':'케투','RA':'라후','FL':'플레임','WD':'하얀 용의 낙윤','AZ':'알버스의 낙윤','EC':'에클레시아','CA':'카르테시아','BF':'낙인융합','FV':'F&V','GN':'비드테(기타)','GW':'비드테(마법사)','GWL':'비드테(빛마법사)','GL':'비드테(빛·2500+)','ART':'알자리온','SEC':'드라군','MIX':'믹시아','GRA':'그랑기뇰','ALB':'알비온','TIT':'배스터드','DEV':'성흔','RIN':'린드블룸','MJ':'미라제이드','LEN':'레나투스','VOI':'공극','AEO':'아이온','EDD':'검은 용','ANA':'아나콘다','ARX':'알자리온(소생)'}
k=lambda xs:'·'.join(KO[x] for x in xs)
top=int(sys.argv[1]) if len(sys.argv)>1 else 1
for l in sys.stdin:
    d=json.loads(l)
    print('####',d['hand'],d.get('n'),'CAP' if d.get('cap') else '')
    for r in d.get('res',[])[:top]:
        print('  ==',r['sc'],k(r['fld']),'|',k(r['st']),'| 패',k(r['h']),'| 묘지',k([x for x in r['gy'] if x in ('RIN','TIT','ALB','DEV','LEN','ART','SEC','MIX','GRA')]))
        print('     ',' / '.join(r['why']))
        if '-p' in sys.argv:
            for p in r['steps']: print('      -',p['lg'])
