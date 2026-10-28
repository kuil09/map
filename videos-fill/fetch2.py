import json,urllib.request,os
K=os.environ['YOUTUBE_API_KEY']
C={'UCZUPZW5idAxYp-Asj__lVAA':'서울시','UC960xfXepXPsJ8HHePGvAKw':'인천광역시','UCTHZPqsEmZLP5rrCLXJFwNg':'울산시청TV',
'UC9KubMS1eabZzmUTCzcvBcg':'경주시','UC5GZQWQiEt3lDt1Y4_hUwdw':'포항시','UCbdBIZiwlOl8lkvkrEaHGNQ':'안동시','UCak6g9I9CHvYCWLFyLMVh-w':'평창군','UCEimjrj1TmbS367s4NokUWg':'울릉군','UCTwWexE_dvD6kvFDSIQMiwg':'군산시','UCfNZdBAhpTCeFYLU9zmBKow':'하동TV','UCozhcwSAVBPYje5rt_dvlDw':'양양군','UCws2MnAreu8nuHL69BUZt5w':'거제시','UCrkNYoUheA5SdWVI8q2qQPw':'거제해양관광개발공사','UCqZZo0Eqkyot4yQcnxQbX4Q':'정선군','UCHAfC3dziPM6GyP2-DUe-cQ':'울진군','UC_lnzPZZg6Cu7e1TEu4dhYw':'김해시TV','UCsdyUsKy997GmEXB0FW4jZQ':'부안군','UCbWWkc08DXSMnpNqpyrZ5Jg':'GNTO경남관광재단','UCzTZILSlHhAfSNAIhPw5eBw':'광주관광공사','UClUMxNBoKujXtXtzdqhq9sg':'보이소TV',
'UChTeiHYZmNAlqWgcYvhPzBw':'강릉시','UCayrfVDCiE2jliz8m4Jykig':'속초시','UCCjjxZxmneCU5t-Ojw8L_0w':'춘천시','UCaijie_uqaAQQCt_fCZ-5qQ':'통영시','UCWqpEO_K7hUAPV_b2OKs51A':'원주시','UCxILe0IuvJ0GuRvnRHdhfcw':'영월군','UC9KrfTmsZAoRFUvS6tPggKg':'삼척시','UC4ykkRchQ1i2SsPyOq6nt5w':'진주시','UC35SH2IZCoDAyjdM_BKNVlA':'부산튜브','UCW0dK4y2eV-3CllA7MdCILA':'목포시','UCKinsx7JAoKe_Ne8QxaEQ6g':'해남군','UCFS5qcsGXRQku904_ygBSqw':'담양군'}
db=json.load(open('uploads.json'));q=0;BUD=4300
for cid in C:
  if q>=BUD: break
  big=cid in list(C)[:3]
  out=[];tok='';pages=0
  while pages<(170 if big else 50) and q<BUD:
    try: d=json.load(urllib.request.urlopen(f'https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&maxResults=50&playlistId=UU{cid[2:]}&key={K}&pageToken={tok}'))
    except Exception as e: print(cid,e);break
    q+=1;pages+=1
    out+=[(i['snippet']['resourceId']['videoId'],i['snippet']['title'],i['snippet']['description'][:300],i['snippet']['channelTitle']) for i in d['items']]
    tok=d.get('nextPageToken')
    if not tok: break
  db[cid]=out;print(C[cid],len(out),pages,flush=True)
  json.dump(db,open('uploads.json','w'),ensure_ascii=False)
json.dump(C,open('ch2.json','w'),ensure_ascii=False)
print('quota',q)
