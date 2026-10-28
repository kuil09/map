# Korea Local Guide quality audit

Base: kuil09/map main fce17ab, data/v2/exports (1,863 rows). Live map and repo untouched. Outputs: `<layer>-FULL.csv` here.

Final counts: culture_sights 487, nature_camping 441, food_drink 410, activities_wellness 341, shopping 184 = 1,863. No rows removed.

## Summary of changes
- Unsupported distance (Guide, 5 langs): 1 (Wondae-ri birch forest, now `2.7 km`, Source KTO gives only trail times)
- Unsupported walking time (Details EN/KO): 2
- Internal 'straight-line km from Desiderio airfield reference' notes removed from Details EN/KO: 37 rows (unsourced distance, not visitor info, and references a military airfield)
- Unsupported superlatives rewritten (Guide, 5 langs): 13 (Gyeongpo also gained KTO-sourced 1.8 km)
- Malformed Source URLs repaired: 14

## Distance/time claims checked and KEPT (number found in row's own Source)
Jukbyeon Skyrail 2.8 km, Tongyeong Cable Car ~2 km (KTO 1,975 m), Gimhae rail park 3 km, Samcheok railbike 5.4 km, Inje Speedium 3.9 km (KTO 3.908 km), Yeosu railbike 3.5 km, Namwon AirRail 2.44 km, Sanmagi trail 3.93 km, Ulsan Lotte wheel 20-min ride, Amethyst cave 2.5 km, Geumjeongsanseong 18.8 km (KTO 18,845 m), Dodonghang 188 km, Chilpo 4 km, Padosori 1.7 km, Jeoryeong 3 km, Haeundae 1.5 km, Songjeong 1.2 km, Samnak 7 km, Dalmaji 8 km, Samcheok beach 1.2 km, Badahyanggiro 1.7 km (KTO 1.74), Yeongnangho 7.8 km, Seonjaegil 9 km, Jujeon 1.5 km. Source already in row, so no source added. Opening-hour lines ('last admission 30 min before closing') are copied from KTO and were not treated as claims.

## All changes

- **activities_wellness / cgv-dongtan** [Details] internal straight-line distance from Desiderio airfield reference point (not visitor info, unsourced as a travel distance); removed EN/KO (row has no JA/ZH/ES Details)
- **activities_wellness / asan-insects** [Details] internal straight-line distance from Desiderio airfield reference point (not visitor info, unsourced as a travel distance); removed EN/KO (row has no JA/ZH/ES Details)
- **activities_wellness / activity-jeonju-crafts-hall** [Details] internal straight-line distance from Desiderio airfield reference point (not visitor info, unsourced as a travel distance); removed EN/KO (row has no JA/ZH/ES Details)
- **activities_wellness / activity-wonju-hanji** [Details] internal straight-line distance from Desiderio airfield reference point (not visitor info, unsourced as a travel distance); removed EN/KO (row has no JA/ZH/ES Details)
- **activities_wellness / activity-asan-railbike** [Details] internal straight-line distance from Desiderio airfield reference point (not visitor info, unsourced as a travel distance); removed EN/KO (row has no JA/ZH/ES Details)
- **activities_wellness / activity-hoengseong-luge** [Details] internal straight-line distance from Desiderio airfield reference point (not visitor info, unsourced as a travel distance); removed EN/KO (row has no JA/ZH/ES Details)
- **activities_wellness / activity-mancheonha** [Details] internal straight-line distance from Desiderio airfield reference point (not visitor info, unsourced as a travel distance); removed EN/KO (row has no JA/ZH/ES Details)
- **activities_wellness / activity-alpaca-world** [Details] internal straight-line distance from Desiderio airfield reference point (not visitor info, unsourced as a travel distance); removed EN/KO (row has no JA/ZH/ES Details)
- **activities_wellness / activity-king-canoe** [Details] internal straight-line distance from Desiderio airfield reference point (not visitor info, unsourced as a travel distance); removed EN/KO (row has no JA/ZH/ES Details)
- **activities_wellness / activity-imsil-cheese** [Details] internal straight-line distance from Desiderio airfield reference point (not visitor info, unsourced as a travel distance); removed EN/KO (row has no JA/ZH/ES Details)
- **activities_wellness / activity-jeongseon-railbike** [Details] internal straight-line distance from Desiderio airfield reference point (not visitor info, unsourced as a travel distance); removed EN/KO (row has no JA/ZH/ES Details)
- **activities_wellness / culture-national-ecology** [Details] internal straight-line distance from Desiderio airfield reference point (not visitor info, unsourced as a travel distance); removed EN/KO (row has no JA/ZH/ES Details)
- **activities_wellness / culture-seaqrium** [Details] internal straight-line distance from Desiderio airfield reference point (not visitor info, unsourced as a travel distance); removed EN/KO (row has no JA/ZH/ES Details)
- **activities_wellness / cgv-cheonan** [Details] internal straight-line distance from Desiderio airfield reference point (not visitor info, unsourced as a travel distance); removed EN/KO (row has no JA/ZH/ES Details)
- **activities_wellness / activities-si-incheon-wolmi-sea-train** [Sources] malformed URL repaired
  - before: https://english.visitkorea.or.kr/svc/contents/contentsView.do?vcontsId=194596 https://www.ictr.or.kr/a> Checked 2026-10-28
  - after: https://english.visitkorea.or.kr/svc/contents/contentsView.do?vcontsId=194596 https://www.ictr.or.kr/ Checked 2026-10-28
- **culture_sights / hwaseong-haenggung** [Details] internal straight-line distance from Desiderio airfield reference point (not visitor info, unsourced as a travel distance); removed EN/KO (row has no JA/ZH/ES Details)
- **culture_sights / culture-daegu-bangjja-yugi-museum** [Guide] superlative not in Sources; softened/replaced with sourced fact
  - before: EN: Korea's only museum dedicated to hand-forged bangjja bronze ware, on Palgongsan.
  - after: EN: Museum dedicated to hand-forged bangjja bronze ware, on Palgongsan.
- **culture_sights / oeam** [Details] internal straight-line distance from Desiderio airfield reference point (not visitor info, unsourced as a travel distance); removed EN/KO (row has no JA/ZH/ES Details)
- **culture_sights / yunggeolleung** [Details] internal straight-line distance from Desiderio airfield reference point (not visitor info, unsourced as a travel distance); removed EN/KO (row has no JA/ZH/ES Details)
- **culture_sights / culture-osan-art-museum** [Details] internal straight-line distance from Desiderio airfield reference point (not visitor info, unsourced as a travel distance); removed EN/KO (row has no JA/ZH/ES Details)
- **culture_sights / culture-gb-gyeongju-cheomseongdae-observatory** [Guide] superlative not in Sources; softened/replaced with sourced fact
  - before: EN: 7th-century stone observatory from Queen Seondeok's reign, among the oldest in East Asia.
  - after: EN: 7th-century stone observatory from Queen Seondeok's reign, about 9 m tall.
- **culture_sights / culture-gb-andong-woryeonggyo-bridge** [Guide] superlative not in Sources; softened/replaced with sourced fact
  - before: EN: Korea's longest wooden footbridge, over the river near Andong Dam; lit up at night.
  - after: EN: Wooden footbridge over the river near Andong Dam; lit up at night.
- **culture_sights / culture-gb-goryeong-jisandong-ancient-tombs** [Sources] malformed URL repaired
  - before: https://english.visitkorea.or.kr/svc/contents/contentsView.do?vcontsId=81842 https://tour.goryeong.go.krwww.cha.go.kr Checked 2026-10-28
  - after: https://english.visitkorea.or.kr/svc/contents/contentsView.do?vcontsId=81842 https://tour.goryeong.go.kr https://www.cha.go.kr Checked 2026-10-28
- **culture_sights / culture-gb-uljin-uljin-bulyeongsa-temple** [Sources] malformed URL repaired
  - before: https://english.visitkorea.or.kr/svc/contents/contentsView.do?vcontsId=94557 https://bulyoungsa.krwww.uljin.go.kr/tour Checked 2026-10-28
  - after: https://english.visitkorea.or.kr/svc/contents/contentsView.do?vcontsId=94557 https://bulyoungsa.kr https://www.uljin.go.kr/tour Checked 2026-10-28
- **culture_sights / culture-gb-gyeongju-bunhwangsa-temple** [Guide] superlative not in Sources; softened/replaced with sourced fact
  - before: EN: Temple founded in 634 with Silla's oldest surviving stone-brick pagoda, next to the Hwangnyongsa site. Dress modestly.
  - after: EN: Temple founded in 634 with a National Treasure stone-brick pagoda, next to the Hwangnyongsa site. Dress modestly.
- **culture_sights / culture-jl-gwangju-buk-gwangju-biennale-exhibition-hall** [Guide] superlative not in Sources; softened/replaced with sourced fact
  - before: EN: Main venue of the Gwangju Biennale, Asia's first contemporary art biennale, with exhibitions between editions.
  - after: EN: Main venue of the Gwangju Biennale contemporary art exhibition since 1994, with exhibitions between editions.
- **culture_sights / culture-jl-naju-naju-geumseonggwan-hall** [Guide] superlative not in Sources; softened/replaced with sourced fact
  - before: EN: Joseon-era guesthouse for royal envoys in central Naju, one of the largest surviving examples.
  - after: EN: Joseon-era guesthouse for royal envoys in central Naju, built in the 1470s.
- **culture_sights / culture-jl-naju-naju-geumseonggwan-hall** [Sources] malformed URL repaired
  - before: https://english.visitkorea.or.kr/svc/contents/contentsView.do?vcontsId=62860 https://www.cha.go.krwww.naju.go.kr Checked 2026-10-28
  - after: https://english.visitkorea.or.kr/svc/contents/contentsView.do?vcontsId=62860 https://www.cha.go.kr https://www.naju.go.kr Checked 2026-10-28
- **culture_sights / culture-jl-jeonju-jeonju-pungnammun-gate** [Guide] superlative not in Sources; softened/replaced with sourced fact
  - before: EN: South gate of old Jeonju fortress, rebuilt in 1734 and the only gate still standing.
  - after: EN: South gate of old Jeonju fortress, built in 1734 and designated a Treasure.
- **culture_sights / culture-jj-seogwipo-daejeonghyanggyo-confucian-school** [Sources] malformed URL repaired
  - before: https://english.visitkorea.or.kr/svc/contents/contentsView.do?vcontsId=76956 https://www.visitjeju.netwww.cha.go.kr Checked 2026-10-28
  - after: https://english.visitkorea.or.kr/svc/contents/contentsView.do?vcontsId=76956 https://www.visitjeju.net https://www.cha.go.kr Checked 2026-10-28
- **culture_sights / culture-si-seoul-myeongdong-cathedral** [Guide] superlative not in Sources; softened/replaced with sourced fact
  - before: EN: Korea's first Gothic Catholic cathedral, built in 1898 in Myeongdong; visitors should keep quiet during Mass.
  - after: EN: Gothic Catholic cathedral of the Archdiocese of Seoul, built in 1898 in Myeongdong; visitors should keep quiet during Mass.
- **culture_sights / culture-si-seoul-munmyo-confucian-shrine-and-seonggyungwan-national** [Sources] malformed URL repaired
  - before: https://english.visitkorea.or.kr/svc/contents/contentsView.do?vcontsId=85542 https://www.skk.or.krwww.cha.go.kr Checked 2026-10-28
  - after: https://english.visitkorea.or.kr/svc/contents/contentsView.do?vcontsId=85542 https://www.skk.or.kr https://www.cha.go.kr Checked 2026-10-28
- **culture_sights / culture-si-incheon-gwangseongbo-fortress** [Sources] malformed URL repaired
  - before: https://english.visitkorea.or.kr/svc/contents/contentsView.do?vcontsId=84079 https://www.ghss.or.krwww.cha.go.kr Checked 2026-10-28
  - after: https://english.visitkorea.or.kr/svc/contents/contentsView.do?vcontsId=84079 https://www.ghss.or.kr https://www.cha.go.kr Checked 2026-10-28
- **culture_sights / culture-si-incheon-incheon-chinatown** [Guide] superlative not in Sources; softened/replaced with sourced fact
  - before: EN: Korea's oldest Chinatown, with red gates, jjajangmyeon restaurants and open-port-era streets.
  - after: EN: Chinatown dating from the 1883 opening of Incheon Port, with red gates, jjajangmyeon restaurants and open-port-era streets.
- **culture_sights / culture-cc-cn-buyeo-neungsan-ri-ancient-tombs-unesco-world-herit** [Sources] malformed URL repaired
  - before: https://english.visitkorea.or.kr/svc/contents/contentsView.do?vcontsId=94929 https://www.buyeo.go.krwww.cha.go.kr Checked 2026-10-28
  - after: https://english.visitkorea.or.kr/svc/contents/contentsView.do?vcontsId=94929 https://www.buyeo.go.kr https://www.cha.go.kr Checked 2026-10-28
- **culture_sights / culture-dug-gg-jeongok-ri-prehistoric-site-hantangang-river-geopa** [Sources] malformed URL repaired
  - before: https://english.visitkorea.or.kr/svc/contents/contentsView.do?vcontsId=93801 https://www.yeoncheon.go.krwww.cha.go.krwww.hantangeopark.kr Checked 2026-10-28
  - after: https://english.visitkorea.or.kr/svc/contents/contentsView.do?vcontsId=93801 https://www.yeoncheon.go.kr https://www.cha.go.kr https://www.hantangeopark.kr Checked 2026-10-28
- **food_drink / cafe-daegu-espace-bakery** [Details] walking time not found in Sources; removed EN/KO
- **food_drink / food-jl-mokpo-clb-bakery** [Details] walking time not found in Sources; removed EN/KO
- **nature_camping / waemok** [Details] internal straight-line distance from Desiderio airfield reference point (not visitor info, unsourced as a travel distance); removed EN/KO (row has no JA/ZH/ES Details)
- **nature_camping / dodamsambong** [Details] internal straight-line distance from Desiderio airfield reference point (not visitor info, unsourced as a travel distance); removed EN/KO (row has no JA/ZH/ES Details)
- **nature_camping / baedari** [Details] internal straight-line distance from Desiderio airfield reference point (not visitor info, unsourced as a travel distance); removed EN/KO (row has no JA/ZH/ES Details)
- **nature_camping / gocamping-100873** [Details] internal straight-line distance from Desiderio airfield reference point (not visitor info, unsourced as a travel distance); removed EN/KO (row has no JA/ZH/ES Details)
- **nature_camping / gocamping-7830** [Details] internal straight-line distance from Desiderio airfield reference point (not visitor info, unsourced as a travel distance); removed EN/KO (row has no JA/ZH/ES Details)
- **nature_camping / gocamping-101102** [Details] internal straight-line distance from Desiderio airfield reference point (not visitor info, unsourced as a travel distance); removed EN/KO (row has no JA/ZH/ES Details)
- **nature_camping / gocamping-2032** [Details] internal straight-line distance from Desiderio airfield reference point (not visitor info, unsourced as a travel distance); removed EN/KO (row has no JA/ZH/ES Details)
- **nature_camping / gocamping-2422** [Details] internal straight-line distance from Desiderio airfield reference point (not visitor info, unsourced as a travel distance); removed EN/KO (row has no JA/ZH/ES Details)
- **nature_camping / gocamping-101776** [Details] internal straight-line distance from Desiderio airfield reference point (not visitor info, unsourced as a travel distance); removed EN/KO (row has no JA/ZH/ES Details)
- **nature_camping / gocamping-6984** [Details] internal straight-line distance from Desiderio airfield reference point (not visitor info, unsourced as a travel distance); removed EN/KO (row has no JA/ZH/ES Details)
- **nature_camping / gocamping-3139** [Details] internal straight-line distance from Desiderio airfield reference point (not visitor info, unsourced as a travel distance); removed EN/KO (row has no JA/ZH/ES Details)
- **nature_camping / gocamping-8157** [Details] internal straight-line distance from Desiderio airfield reference point (not visitor info, unsourced as a travel distance); removed EN/KO (row has no JA/ZH/ES Details)
- **nature_camping / gocamping-100219** [Details] internal straight-line distance from Desiderio airfield reference point (not visitor info, unsourced as a travel distance); removed EN/KO (row has no JA/ZH/ES Details)
- **nature_camping / gocamping-100900** [Details] internal straight-line distance from Desiderio airfield reference point (not visitor info, unsourced as a travel distance); removed EN/KO (row has no JA/ZH/ES Details)
- **nature_camping / gocamping-101341** [Details] internal straight-line distance from Desiderio airfield reference point (not visitor info, unsourced as a travel distance); removed EN/KO (row has no JA/ZH/ES Details)
- **nature_camping / gocamping-315** [Details] internal straight-line distance from Desiderio airfield reference point (not visitor info, unsourced as a travel distance); removed EN/KO (row has no JA/ZH/ES Details)
- **nature_camping / gocamping-101195** [Details] internal straight-line distance from Desiderio airfield reference point (not visitor info, unsourced as a travel distance); removed EN/KO (row has no JA/ZH/ES Details)
- **nature_camping / scenery-siheung-gaetgol** [Details] internal straight-line distance from Desiderio airfield reference point (not visitor info, unsourced as a travel distance); removed EN/KO (row has no JA/ZH/ES Details)
- **nature_camping / camping-gb-gyeongju-tohamsan-national-recreational-forest** [Sources] malformed URL repaired
  - before: https://english.visitkorea.or.kr/svc/contents/contentsView.do?vcontsId=97418 https://www.foresttrip.go.krwww.gyeongju.go.kr Checked 2026-10-28
  - after: https://english.visitkorea.or.kr/svc/contents/contentsView.do?vcontsId=97418 https://www.foresttrip.go.kr https://www.gyeongju.go.kr Checked 2026-10-28
- **nature_camping / nature-gw-gangneung-gangneung-gyeongpo-beach** [Guide] "best-known/most famous" not in Source; replaced with KTO-sourced 1.8 km length
  - before: EN: Gangneung's best-known beach, a long sand bar between Gyeongpoho Lake and the sea.
  - after: EN: Popular Gangneung beach, a 1.8 km sand bar between Gyeongpoho Lake and the sea.
- **nature_camping / nature-gw-inje-wondae-ri-birch-forest-whispering-birch-forest** [Guide] 2.7 km forest-road distance not in Sources (KTO gives only trail times); removed in 5 languages
  - before: EN: Planted forest of white birch near Inje reached by a 2.7 km uphill forest road; seasonal closures apply.
  - after: EN: Planted forest of white birch near Inje reached by an uphill forest road; seasonal closures apply.
- **nature_camping / nature-jj-jeju-hallasan-mountain-trekking** [Sources] malformed URL repaired
  - before: https://english.visitkorea.or.kr/svc/contents/contentsView.do?vcontsId=90434 https://www.visitjeju.netwww.jeju.go.kr Checked 2026-10-28
  - after: https://english.visitkorea.or.kr/svc/contents/contentsView.do?vcontsId=90434 https://www.visitjeju.net https://www.jeju.go.kr Checked 2026-10-28
- **nature_camping / nature-si-seoul-yangjaecheon-ecological-park** [Sources] malformed URL repaired
  - before: https://english.visitkorea.or.kr/svc/contents/contentsView.do?vcontsId=75574 https://www.seocho.go.kr(Korean, Checked 2026-10-28
  - after: https://english.visitkorea.or.kr/svc/contents/contentsView.do?vcontsId=75574 https://www.seocho.go.kr Checked 2026-10-28
- **nature_camping / nature-cc-cn-seongjusan-recreational-forest** [Sources] malformed URL repaired
  - before: https://english.visitkorea.or.kr/svc/contents/contentsView.do?vcontsId=95009 https://www.brcn.go.krwww.foresttrip.go.kr Checked 2026-10-28
  - after: https://english.visitkorea.or.kr/svc/contents/contentsView.do?vcontsId=95009 https://www.brcn.go.kr https://www.foresttrip.go.kr Checked 2026-10-28
- **nature_camping / nature-dug-gg-yangpyeong-wild-flower-arboretum** [Sources] malformed URL repaired
  - before: https://english.visitkorea.or.kr/svc/contents/contentsView.do?vcontsId=81506 https://www.nemunimo.co.kr(Korean Checked 2026-10-28
  - after: https://english.visitkorea.or.kr/svc/contents/contentsView.do?vcontsId=81506 https://www.nemunimo.co.kr Checked 2026-10-28
- **shopping / starfield-anseong** [Details] internal straight-line distance from Desiderio airfield reference point (not visitor info, unsourced as a travel distance); removed EN/KO (row has no JA/ZH/ES Details)
- **shopping / shopping-gb-gyeongju-gyeongju-jungang-market** [Guide] superlative not in Sources; softened/replaced with sourced fact
  - before: EN: Gyeongju's largest traditional market, with a night market and 5-day market days.
  - after: EN: Gyeongju's main local marketplace, with a night market and 5-day market days.
- **shopping / shopping-jl-gwangju-seo-gwangju-yangdong-market** [Guide] superlative not in Sources; softened/replaced with sourced fact
  - before: EN: Gwangju's largest traditional market, known for seafood and fried chicken.
  - after: EN: Long-running Gwangju traditional market, known for seafood and fried chicken.
- **shopping / shopping-si-seoul-seoul-yangnyeongsi-market** [Guide] superlative not in Sources; softened/replaced with sourced fact
  - before: EN: Korea's largest herbal medicine market, with ginseng and medicinal herbs.
  - after: EN: Herbal medicine market with ginseng and medicinal herbs.

## Checks with no change needed
- Generic jjimjilbang/spa/pool guidance: none. All 14 spa_hot_spring rows and 6 pool rows are venue-specific (tickets, swimwear rules). Temple rows have short 'general temple etiquette' lines, which are not spa guidance.
- Military access: none needing permits. Imjingak/Odusan (earlier cleared), Jeoryeong & Oeongchi trails (former restricted, now open), Naerincheon (DMZ website only).
- Near-duplicates: none. Same Korean name = different places (Buseoksa Yeongju vs Seosan, Songgwangsa Suncheon vs Wanju, Gajok Hoegwan Gwangju vs Jeonju) or separate park sections (Jirisan x4, Deogyusan x2, Daedunsan x2). Shared addresses are distinct venues in one complex (Starfield, Times Square, COEX etc.). Chains (Red Button x12, VAUNCE, Gangchon Rail Park) are separate branches.
- Empty Sources: 0. Record IDs unique.

## Flagged, not changed
- Dead links: https://foodpick.co.kr/place/cmst4m2zur5hysmr6lqhi0j07 (404), https://english.visitkorea.or.kr/svc/whereToGo/locIntrdn/rgnContentsView.do?vcontsId=80514 (400). ~1,074 other URLs did not answer from the audit box (timeouts, mostly gocamping, access.visitkorea, koreacharts, Korean .go.kr); likely geo/bot blocking, not judged broken.
- Superlative check was automated against each row's Source text; rows where the source page could not be fetched (e.g. Bangjja museum, access.visitkorea) were treated as unsupported. Non-KTO pages were scanned as raw HTML, so a few 'first/only' passes may be weak.
- 444 Guide/Details cells end in '…' (truncated during 8-column migration), mostly long EN Details. Not fixed.
- Several Details lines are English text inside KO lines (KTO hours copied untranslated).
- Gyeongpo, Busan etc. kept 'Korea's largest' claims only where KTO says so (e.g. UN Cemetery 'sole', Dongmun 'most expansive', Sebyeonggwan 'one of the widest').

## Incheon district naming (report only, addresses not changed)
New 2026 names used: 제물포구 4 (wolmi-zzang-land, gonghwachun, sinpo-dakgangjeong, myeongwoljip), 영종구 1 (spa-cimer-incheon).
Old names still used: 중구 22, 동구 1 (food-si-incheon-samdae-incheon-gejang), 서구 1 (cheongna-lake-park).
Of the 중구 rows, those on Yeongjong/Yongyu/Muui (eurwangni, hanagae, masian, horyonggoksan, yeongjong-seaside-railbike, incheon-yonggungsa) would now be 영종구; the rest (Chinatown, Wolmi, Sinpo, Yeonan pier etc.) would be 제물포구. Same street (e.g. 신포로23번길, 우현로49번길, 차이나타운로) appears under both 중구 and 제물포구. Leave as is per instruction since all place correctly; unify later using old names (they geocode reliably).
## 2. Truncated text ("…") repair (2026-10-28 KST)

**Cause:** `migration/v2/migrate_v2.py` uses `short(text, n)` = `text[:n-1] + '…'`. `to_csv_row` caps Guide at 140 characters per language and practical notes at 200 (EN) / 120 (KO). Several notes in `places.v2.json` were also stored already cut. The 8-column build (`eight-col/build.py`) copied text verbatim and is not the cause. Every truncated line already existed in the 11-column exports at e84f71a.

**Scope found:** 694 truncated lines in 444 cells: Details EN 360, Details KO 253, Guide ES 34, EN 14, JA 1, ZH 1.

**Repair:**
- **693 lines restored** from our own data: a per-Record-ID index over v2 JSON, the e84f71a CSVs and JSONL. The longest candidate was used only when every other candidate was a prefix of it, so there were no conflicts. Log: `restore-log.json`.
- **1 cell trimmed** to the 1,675-character cap at a sentence boundary: temple-daegu-donghwasa Details, 1,756 → 1,672.
- **1 line with no full text** (cafe-daegu-espace-bakery Details EN): ended at the last complete clause. "Takeout/delivery available." was re-added because the row's own KO line, from the same Daegu Food source, says 포장·배달 가능.
- **0 re-fetched** from sources.
- **Clean-up of restored text** (log: `geoclean-log.json`):
  - The restored full text brought back the policy-removed notes. 100 lines of Desiderio straight-line distances, map-anchor and display-offset notes were removed again (EN/KO/ES), including the 4 ES Guide lines.
  - Jinnam railbike: the "1.1 km from address marker" note was removed.
  - Suseongmot: the unsourced "10 min walk" text was removed (EN/KO), because the source page couldn't be checked.
  - Donghwasa (templestay.com) and Daegu Arboretum (daegu.go.kr) walk times are kept, since both are stated by the source.
  - Pre-existing ".." double periods in Guide/Details were fixed.

**Final state:**
- 0 lines end in "…".
- 0 Desiderio/데시데리오/직선/straight-line/línea recta matches.
- Max Guide/Details cell: 1,675 characters.
- Rows 487/441/410/341/184.
- Compared with the pre-repair backup, only Guide, Details and one Sources cell changed.

## 3. Dead links
- food-dug-gg-gapyeong-naengmyeon-buson-seorak-main-branch: dropped the foodpick 404. VisitKorea 188557 and jidoro remain (both 200).
- dining-mihyang-sejong: VisitKorea vcontsId=80514 returns 400, and no working official page was found. The KTO TourAPI content is id 801273, but only third-party mirrors are reachable (tripinfo, ktourmap). It is the row's only source, so the link was **left in place and flagged** for a decision: replace it with a mirror, keep it, or remove the row.
