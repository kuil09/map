import json,re
c=json.load(open('cands.json'));names=json.load(open('chnames.json'))
n=lambda s:re.sub(r'[\s·\-()\[\]]','',s)
NEG=re.compile('행사|캠페인|수어|식수|특별전|기획전|소장품|무료|재개장|공사|재탄생|정책|ON-AIR|체전|카운트다운|숙소|리조트|제휴사|모집|개봉|표류기|인파|축제|팸투어|대회|교육|봉사|협의|점검|안전|사고|화재|기념식|추모|위령|개막|폐막|시상|공연|촬영지|케데헌|올림픽|ㅣ#20|이벤트|할인|선정|브이로그|VLOG|투어!|드라마')
sel={}
for x in c:
  ko=x['name'].split('|')[-1].strip();k=n(re.sub(r'\(.*?\)','',ko))
  best=None
  for cid,vid,t in x['hits']:
    if NEG.search(t): continue
    s=0
    if len(re.findall(r'[,，、]',t))>=1: s-=3
    if '#shorts' in t.lower(): s-=1
    if re.search('[A-Za-z]{4,}',re.sub('(?i)shorts|JEC|ASMR|4K|UHD','',t)): s+=1
    if n(t).endswith(k) or n(t).startswith(k): s+=2
    if len(n(t))<len(k)+25: s+=1
    if names[cid] in('Visit Jeju','VisitSeoul','VISITKOREA','충남관광','대전관광공사','비짓대구','경기관광','투어전북','Incheon Tourism'): s+=1
    if best is None or s>best[0]: best=(s,cid,vid,t)
  if best and best[0]>=0: sel[(x['layer']+'|'+str(x['idx']))]=dict(rid=x['rid'],name=x['name'],ch=names[best[1]],cid=best[1],vid=best[2],title=best[3],score=best[0])
json.dump(sel,open('sel.json','w'),ensure_ascii=False,indent=0)
print(len(sel))
for k,v in sel.items(): print(f"{k} | {v['name'].split('|')[-1].strip()} || {v['ch']} | {v['title']}")
