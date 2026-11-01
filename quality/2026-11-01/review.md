# Korea map data-quality audit — review list (2026-10-31 KST)

Auto-fixes are in fixes.json (153 cells, 148 records). Everything below was NOT changed and needs a human decision.

## 1. Dead sources (KTO English page removed: HTTP 400 '400 Error'; same URL pattern works for live IDs)
### Sole source dead (11) — place itself unverified, review/re-source

- `culture-bg-haman-ancient-tombs-in-marisan-mountain-haman` Ancient Tombs in Marisan Mountain, Haman | 함안 말이산 고분군 — https://english.visitkorea.or.kr/svc/contents/contentsView.do?vcontsId=177241
- `culture-dw-daegu-petite-joongang-family-museum` Petite Joongang Family Museum | 작은 중앙가족박물관 — https://english.visitkorea.or.kr/svc/contents/contentsView.do?vcontsId=87490
- `scenery-gb-cheongsong-three-falls-of-juwangsan-mountain` Three Falls of Juwangsan Mountain | 주왕산 1.2.3 폭포 — https://english.visitkorea.or.kr/svc/contents/contentsView.do?vcontsId=189442
- `nature-gw-hoengseong-hoengseonghosugil-trail` Hoengseonghosugil Trail | 횡성호수길 — https://english.visitkorea.or.kr/svc/contents/contentsView.do?vcontsId=174675
- `nature-cc-cb-sangsoo-herb-land` Sangsoo Herb Land | 상수허브랜드 — https://english.visitkorea.or.kr/svc/contents/contentsView.do?vcontsId=75028
- `food-jl-jeongeup-jeongeupanu` Jeongeupanu | 정읍한우 — https://english.visitkorea.or.kr/svc/contents/contentsView.do?vcontsId=54995
- `food-bn-jeonbuk-jungboni-jaengban-jjajang` Jungboni Jaengban Jjajang | 중본이쟁반짜장 — https://english.visitkorea.or.kr/svc/contents/contentsView.do?vcontsId=48888
- `food-bn-jeonbuk-chaiking` CHAIKING | 차이킹 — https://english.visitkorea.or.kr/svc/contents/contentsView.do?vcontsId=49318
- `food-bn-jeonbuk-ichiryu-yangsim` Ichiryu Yangsim | 이치류양심 — https://english.visitkorea.or.kr/svc/contents/contentsView.do?vcontsId=48735
- `activities-cc-cn-anmyeondo-maze-park` Anmyeondo Maze Park | 안면도 미로공원 — https://english.visitkorea.or.kr/svc/contents/contentsView.do?vcontsId=215560
- `shopping-gb-uiseong-uiseong-garlic-market-uiseong-traditional-market` Uiseong Garlic Market (Uiseong Traditional Market) | 의성마늘장터 (의성명품마늘영농조합법인) — https://english.visitkorea.or.kr/svc/contents/contentsView.do?vcontsId=192614

### One of several sources dead (6) — drop the dead URL when convenient

- `culture-gb-cheongdo-unmunsa-temple` — https://english.visitkorea.or.kr/svc/contents/contentsView.do?vcontsId=94547
- `culture-cc-sejong-haposeowon-confucian-academy` — https://english.visitkorea.or.kr/svc/contents/contentsView.do?vcontsId=80471
- `culture-cc-cn-boryeong-mud-museum` — https://english.visitkorea.or.kr/svc/contents/contentsView.do?vcontsId=94985
- `activities-bg-gimhae-gimhae-nakdonggang-river-rail-park` — https://english.visitkorea.or.kr/svc/contents/contentsView.do?vcontsId=67813
- `ak-suwon` — https://english.visitkorea.or.kr/svc/contents/contentsView.do?vcontsId=73366
- `shopping-jl-jangheung-jeongnamjin-jangheung-saturday-market` — https://english.visitkorea.or.kr/svc/contents/contentsView.do?vcontsId=66462

### Server errors (HTTP 5xx / connection, 32 places, other sources OK) — recheck later, not counted as dead

- `temple-daegu-eunjeoksa` — http://www.eunjeoksa.or.kr/?c=1%2F9 (500)
- `culture-bg-busan-national-maritime-museum` — https://www.knmm.or.kr (500)
- `culture-gw-samcheok-gangwon-comprehensive-museum` — http://www.museum.gangwon.kr (500)
- `culture-jl-haenam-daeheungsa-temple-unesco-world-heritage` — http://www.daeheungsa.co.kr/ (500)
- `culture-jj-seogwipo-teddy-bear-museum-jeju` — http://www.teddybearmuseum.com (500)
- `culture-si-incheon-goryeogung-palace-site` — http://www.ghss.or.kr (500)
- `culture-dug-daegu-nakdong-river-victory-memorial-hall` — http://www.nakdongwar.or.kr/ (500)
- `culture-bn-gwangju-bium-museum` — http://biummuseum.com/ (500)
- `culture-bn-jeonbuk-jeonju-hanbyuk-cultural-center` — http://www.jt.or.kr/ (500)
- `camping-gb-sangju-sangju-woosan-auto-campground` — http://cafe.daum.net/woosancamping/ (500)
- `nature-jl-buan-chaeseokgang-cliff-jeonbuk-national-geopark` — http://www.jwcgeopark.kr (500)
- `nature-jj-seogwipo-pyoseon-haevich-beach` — http://www.visitjeju.net/ (500)
- `nature-jj-seogwipo-nonjinmul` — http://www.visitjeju.net (500)
- `nature-jj-jeju-hwansang-gotjawal-forest` — http://www.jejupark.co.kr (500)
- `nature-cc-cn-daedunsan-provincial-park-geumsan-section` — http://www.ijinsan.co.kr/main/main.html (500)
- `nature-dug-ulsan-ulsan-grand-park` — http://www.uic.or.kr/ulsanpark (500)
- `louis` — https://restaurantguru.com/cafe-louis-Pyeongtaek-si (503)
- `food-gw-sokcho-chungchosoo-mul-hoe` — http://www.chungchosoofish.com/?doc_id=1_1 (500)
- `food-jl-damyang-deokinkwan` — http://www.deokinkwan.com (500)
- `food-jj-jeju-samdae-guksuhoegwan` — http://samdnoodle.com/ (500)
- `food-si-seoul-myeongdong-kyoja` — http://www.mdkj.co.kr/restaurant/head.php (500), http://m.mdkj.co.kr/news/notice_view.php?no=587&start=0 (500)
- `food-si-incheon-sinseung-banjeom` — http://ss-chinese.com/layout/res/home.php?go=store.list&mid=40 (500), http://ss-chinese.com/layout/res/home.php?go=pds.list&mid=50&num=294&pds_type=1&s_key1=&s_que=&start=0 (500)
- `food-cc-daejeon-sungsimdang` — http://sungsimdang.co.kr/31/15 (500)
- `food-dw-daegu-yang-jeong-hwa-ne-apsan-oncheongol` — https://restaurantguru.com/%EC%98%A8%EC%B2%9C%EA%B3%A8%EC%95%9E%EC%82%B0%EC%A0%90-Daegu (503)
- `food-tr-dongnae-dongnae-halmae-pajeon` — http://www.dongraehalmaepajun.co.kr/ (500)
- `family-sejong-beartree` — https://www.beartreepark.com/ (500)
- `spa-gangbyeon-spaland` — https://data.visitkorea.or.kr/linkedview/128961 (503)
- `activity-daegu-sun-sports-plaza-bowling` — http://www.sunsportsplaza.co.kr/Class/04 (500)
- `activities-bg-hadong-hadong-korea-zip-wire` — http://www.hdalps.or.kr/ (500)
- `activities-gw-inje-x-game-resort-naerincheon-bungee-jumping` — http://injejump.co.kr/ (500)
- `activities-cc-cn-ziptrek-korea` — http://www.ziptrek.co.kr/ (500)
- `shopping-si-seoul-seoul-jungbu-market` — http://www.jungbusijang.co.kr/ (500)

Excluded as not-dead (geo/TLS blocks or timeouts): access/korean/english1/k-mice.visitkorea, *.go.kr, info.koreacharts.com (265 URLs, TLS handshake fails from box), gocamping.or.kr (86, TLS). 1,055 URLs excluded in total.

## 2. Possible closures (evidence from Naver mobile search, 2026-10-31; nothing deleted)
Strong:
- `food-si-seoul-center-coffee-seoul-forest` 센터커피 서울숲점 — Naver summary: "2025년 10월부로 영업을 종료했습니다". Likely closed → remove or replace.
- `food-bn-jeonbuk-jungboni-jaengban-jjajang` 중보니쟁반짜장 — business registry snippet (마켓비즈) "영업상태 폐업" AND its only source (KTO vcontsId=48888) is gone.
- `food-dw-daegu-apsan-dolsoe-jjajang` — 마켓비즈 snippet "영업상태 폐업" (same-name registry match; confirm).
- `psvill-pyeongtaek-godeok` (Shopping) — 마켓비즈 snippet "영업상태 폐업" (confirm).
- `food-cc-daejeon-ganamji` 가남지 — blog title "[폐업했대요ㅠ]", no Naver place card found.
Weak / check:
- `dining-yeongyeong-boryeong` — registry "휴업"; Naver card at a different address (원동1길 56-9).
- `activity-muzit-darts-pyeongtaek` — only an equipment-supplier listing found.
- `market-yesan` — address conflict between sources.
- Earlier-pass flags with 폐업/이전 words: dining-seusimyeong, dining-gonghwachun (relocated-name context, already handled), market-cheonan-jungang.
- Naver card at a different address (possible move; or search noise): pyeongyang-naengmyeon, moti-mahal, dining-namhangang-jecheon, dining-sanjang-garden-sejong, food-gw-gangneung-gamasot-seolleongtang, food-gw-chuncheon-woomi-dakgalbi-main-branch, food-jl-mokpo-mujinjang-kkorigomtang, food-si-seoul-mangnae-hoejip, food-cc-daejeon-sonamujip, food-dw-daegu-gaejeong, food-dw-daegu-tara-indian, hanwoori-electronics-center, lotte-outlet-paju (search hits are often other branches).
Note: Naver "영업 종료" badges mean closed for today, not permanently; not used as evidence.

## 3. Addresses
- **전남광주통합특별시**: all 140 Jeonnam/Gwangju addresses still say 전라남도/광주광역시, while JSON region.sido for ~100 jl- rows already says 전남광주통합특별시 (internally inconsistent). Legally the new name applies since 2026-07-01 (law.go.kr decree; MOIS notice). Recommend: geocode-test a few in a scratch My Maps layer before mass rename. Not applied.
- **Incheon (applied, 30 rows)** 중구/동구→제물포구/영종구, 서구→서해구 per incheon.go.kr. **Hwaseong (applied)** eup/myeon→만세구/효행구, 동탄→동탄구 per hscity.go.kr. After re-import, eyeball pins for these rows; Google may geocode new gu names imperfectly.
- Hwaseong left unchanged: `yongjusa` (용주로 136) and `yunggeolleung` (효행로481번길 21) — probably 병점구 (화산동/안녕동) but not confirmed.
- `dining-cheongpungjip-chungju` has an English address in the KO field; Naver shows 충북 충주시 무학천변길 90 → suggested: 충청북도 충주시 무학천변길 90 (confirm then apply).
- 84 jibun-only addresses (e.g. dining-jeongok-eochon-kalguksu 전곡리 898; Naver road addr 서신면 전곡항로14번길 1-10). Geocode fine usually; convert opportunistically.
- `shopping-si-seoul-seoul-jungbu-market` Sources contains "서울중구 문화관광 www.junggu.seoul.kr/tour/" (not a link; site TLS-blocked from box). Suggest replacing with https://www.junggu.seoul.kr/tour/ after a check from Korea.

## 4. Content / language
- **Details has only EN+KO in 2,322 of 2,327 rows** (JA/ZH/ES only in Guide). Systemic; Guide covers all 5 languages in every row. Decide whether Details needs 5 languages (would add ~3× text, still within the cell limit since cell count is unchanged).
- `attraction-seoul-grand-park-zoo` popup carries a closure notice dated through Oct 30/31 2026 — now stale; remove after confirming reopening.
- `food-tr-haeundae-geumo-hoetjip` ZH uses Japanese "・"; cosmetic.
- Camping "운영 미확인" and market "市の日は未確認" lines kept as visitor caveats.

## 5. Duplicates
- No duplicate IDs. 26 same-address groups are legitimate co-located places (e.g. Independence Hall + its campground, Gyeonggi Provincial Museum + Children's Museum, Starfield Anseong cluster). Same name: two "가족회관" are different cities (Gwangju vs Jeonju); "Gajokhwegwan" romanization could be unified to "Gajok Hoegwan".

## 6. Policy checks (OK)
- Round-1 Daegu 8 (dining-daegu-samsong-main, dining-daegu-gugil-ttarogukbap, scenery-daegu-apsan-park, scenery-daegu-duryu-park, activity-daegu-second-ice-rink, activity-daegu-international-shooting-tourist, shopping-daegu-seomun-market, culture-daegu-seongmodang) each appear exactly once (from the verified state file); confirm the intended meaning of "never re-add" is "no duplicates".
- Military: 22 keyword hits, all false positives (camp names, USAG video channels). No base-access places.
- Spa: 14 spa rows, no videos, guidance place-specific.
- All-caps brand names (PETERPAN 1978, CHAIKING, DPIRANG) left as-is.


## Round 3 (2026-11-01 KST) decisions applied
- Removed 15 places (removed.json). Jungboni was in both lists, so 15 not 16.
- 140 addresses renamed to 전남광주통합특별시 (prefix only); test with jngj-test.csv.
- Zoo stale closure notice removed.
- Horyonggoksan kept at 인천광역시 중구 (geocoding).
