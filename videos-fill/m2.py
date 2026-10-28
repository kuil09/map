import csv,json,re
db=json.load(open('uploads.json'));names=json.load(open('chnames.json'));names.update(json.load(open('ch2.json')))
REG={'Visit Jeju':'제주','제주도TV':'제주','제주시':'제주','서귀포시청':'제주','VisitSeoul':'서울','서울시':'서울','Incheon Tourism':'인천','인천광역시':'인천','충남관광':'충청남도','대전관광공사':'대전','충북여행':'충청북도','충청북도청':'충청북도','세종':'세종','비짓대구':'대구','대구TV':'대구','울산시청TV':'울산','경기관광':'경기','경기도청':'경기','파주시청':'파주','투어전북':'전북','전남광주통합':'전라남도|광주광역시','강원관광재단':'강원','VISIT BUSAN':'부산','순천시':'순천','전주시':'전주','여수시':'여수','USAG Daegu':'대구|칠곡',
'경주시':'경주','포항시':'포항','안동시':'안동','평창군':'평창','울릉군':'울릉','군산시':'군산','하동TV':'하동','양양군':'양양','거제시':'거제','거제해양관광개발공사':'거제','정선군':'정선','울진군':'울진','김해시TV':'김해','부안군':'부안','GNTO경남관광재단':'경상남도','광주관광공사':'광주광역시','보이소TV':'경상북도','강릉시':'강릉','속초시':'속초','춘천시':'춘천','통영시':'통영','원주시':'원주','영월군':'영월','삼척시':'삼척','진주시':'진주','부산튜브':'부산','목포시':'목포','해남군':'해남','담양군':'담양'}
BAD=re.compile('브리핑|회의|간담회|기자|시정|공고|채용|협약|업무|토론|의회|선거|국감|회견|뉴스|소식|주간|시장|도지사|군수|구청장|모집|공모|라이브|LIVE|생중계|행사|캠페인|수어|식수|특별전|기획전|소장품|무료|재개장|공사|재탄생|정책|체전|카운트다운|숙소|리조트|제휴사|개봉|인파|팸투어|대회|교육|봉사|점검|안전|사고|화재|기념식|추모|개막|폐막|시상|공연|촬영지|이벤트|할인|선정|브이로그|VLOG|드라마|커버|cover|챌린지')
n=lambda s:re.sub(r'[\s·\-()\[\]]','',s)
out=[]
for L in ['culture_sights','nature_camping','food_drink','activities_wellness','shopping']:
  for i,r in enumerate(csv.DictReader(open(f'{L}-FULL.csv'))):
    if r['Video'].strip(): continue
    ko=r['이름'].split('|')[-1].strip();k=n(re.sub(r'\(.*?\)','',ko));a=r['주소']
    if len(k)<3: continue
    best=None
    for cid,vs in db.items():
      rg=REG.get(names.get(cid,''))
      if rg is None or not re.search(rg,a): continue
      for vid,t,d,ct in vs:
        if BAD.search(t) or k not in n(t): continue
        s=0
        if re.search('[,，、/]',t): s-=3
        if 'shorts' in t.lower(): s-=1
        if n(t).startswith(k) or n(t).endswith(k): s+=2
        if len(n(t))<len(k)+25: s+=1
        if best is None or s>best[0]: best=(s,vid,t,ct)
    if best and best[0]>=0: out.append(dict(k=f'{L}|{i}',ko=ko,a=a,vid=best[1],t=best[2],ch=best[3]))
json.dump(out,open('sel2.json','w'),ensure_ascii=False)
print(len(out))
for x in out: print(x['k'],'|',x['ko'],'|',' '.join(x['a'].split()[:2]),'||',x['ch'],'|',x['t'])
