import csv,json
from pathlib import Path

base = Path('data/v2/exports/')
layers=['culture_sights','nature_camping','food_drink','activities_wellness','shopping']
OUT=['이름','주소','Type','Guide','Details','Video','Sources','Record ID']
rep={}
for L in layers:
    rows=list(csv.DictReader(open(base / f'{L}.csv',encoding='utf-8-sig')))
    out=[];stats={'rows':len(rows),'coords':0,'noaddr':0,'video':0}
    for r in rows:
        parts=[]
        if r['Region'].strip(): parts.append('Region: '+r['Region'].strip())
        if r['Latitude'].strip() or r['Longitude'].strip():
            stats['coords']+=1; parts.append(f"Coordinates (reference only, from source): {r['Latitude'].strip()}, {r['Longitude'].strip()}")
        if r['Practical'].strip(): parts.append(r['Practical'].strip())
        if not r['주소'].strip(): stats['noaddr']+=1
        if r['Video'].strip(): stats['video']+=1
        out.append({'이름':r['이름'],'주소':r['주소'],'Type':r['Type'],'Guide':r['Guide'],
          'Details':'\n'.join(parts),'Video':r['Video'],'Sources':r['Sources'],'Record ID':r['Record ID']})
    with open(base / f'{L}.csv','w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,OUT);w.writeheader();w.writerows(out)
    # validate: reparse, check lossless
    back=list(csv.DictReader(open(base / f'{L}.csv',encoding='utf-8')))
    assert len(back)==len(rows)
    for a,b in zip(rows,back):
        for k in ['이름','주소','Type','Guide','Video','Sources','Record ID']: assert a[k]==b[k]
        d=b['Details']
        for k in ['Region','Practical','Latitude','Longitude']:
            assert a[k].strip() in d, (k,a['Record ID'])
        assert max(len(v) for v in b.values())<=  50000
    stats['maxcell']=max(len(v) for r in back for v in r.values())
    rep[L]=stats
print(json.dumps(rep,indent=1)); print(sum(s['rows'] for s in rep.values()))
