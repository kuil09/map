# Korea Local Guide: data-quality pass (2026-10-28 KST)

Source: kuil09/map main@85b0491 data/v2. No places added. The 172 free rows were kept. The repo and the live map were not touched.

## Totals (before = after)
culture_sights 626 · nature_camping 504 · food_drink 571 · activities_wellness 387 · shopping 240 = 2,328

## Fix counts
- sentence_dropped: 7937
- ko_duplicate_sentence_removed: 4731
- region_line: 2328
- check_date_removed: 2328
- call_ahead_added_EN: 1808
- whitespace_cells: 465
- call_ahead_added_KO: 225
- clause_trimmed: 124
- ph_tr_hours_translated: 118
- coord_line: 100
- attribution_stripped: 76
- guide_internal_text_rewritten: 62
- generic_guide_rewritten: 50
- superlative_softened: 37
- concat_domain_split: 26
- source_url_fixed: 14
- details_manual_cleanup: 13
- text_url_fixed: 4
- soft_fact_sentence_flagged: 1

## Popup cleanup
Removed from the popups: reference coordinates, source and process notes, check dates, batch and dedupe notes, and raw API labels. All of this is kept verbatim per place in places.v2.cleaned.json under legacy.popup_cleanup_2026_10_28 (original_popup, removed_text, guide_change).
Record ID column is kept. It is the join key to places.v2.json ids that the repo build and merge use. Without it a full layer replace cannot be mapped back to the data.

## Sources / URLs
- 3,241 URLs checked. The box cannot reach most Korean .go.kr and KTO hosts (TLS EOF/000/500). A sample re-fetched from another network (koreacharts, gocamping, tour.chungnam, injejump, samdnoodle) all loaded. These are unverifiable from the box, not dead.
- cgv.co.kr 403 (bot block), siksinhot and smartstore 429, restaurantguru 503: rate limits or blocks, not dead.
- Dead link: dining-mihyang-sejong english.visitkorea rgnContentsView vcontsId=80514 returns 400. Replaced with the contentsView.do?vcontsId=80514 form, which search engines index (it also returns 400 to automated clients, so this needs a manual browser check). KTO contentid 801273 was recorded. Details now say 11:00–22:00, 044-866-3173, 20 parking spaces, cards, take-out, plus call ahead. Third-party listings disagree on closed days, so none is stated.
- Concatenated/malformed URLs split into separate links: 14 in Sources, 30 in text (e.g. buan.go.kr/tourtour.jb.go.kr…, cha.go.krbit.ly…, mongsanpo.or.krtaean.go.kr). cha.go.kr was replaced with khs.go.kr (renamed Korea Heritage Service) where it was split.
- koreacharts.com (265 links) is a third-party TourAPI mirror. It is flagged in JSON as weak_third_party_mirror, with kto_contentid recorded.

## Closure spot-check (60 rows: 40 dining + 20 markets), Naver mobile search
- Open or with a current listing: 52. '영업 종료' or '오늘 휴무' only means closed today, not permanently closed.
- No Naver place card, re-checked by web search: dining-yeomong-sogalbi (tripinfo: 평택 중앙2로 166, 10:30–22:30, closed Mondays) and dining-yuchi (official yuchifnb.com, 24h). Both are open.
- 'Closed' keyword hits were false positives: 스시명 (Naver's generic 휴폐업 disclaimer), 천안중앙시장 (a review mentions 영업종료시간), and 공화춘 (the ORIGINAL 공화춘 closed in 1983, and that building is now the Jajangmyeon Museum. The current restaurant is a separate business that is operating). Check that the dining-gonghwachun popup doesn't imply it is the historic original.
- Andong 2/7-day markets and Pohang 5-day markets have no Naver card, which is normal for periodic markets.
- **Removal candidates: none confirmed closed.**

## Addresses
- No address changes. Incheon gu names are mixed (중구 22, 강화군 19, 연수구 8, 옹진군 4, 제물포구 4, 남동구 3, 영종구 1). They were not renamed because it is uncertain whether the new 2026 gu names geocode in My Maps.

## Consistency
- No duplicate IDs. All names are 'EN | KO'. No '…' truncation. 39 Type values, all existing. Rows that share an address are distinct venues, so there are no cross-layer duplicates to remove. 465 whitespace cells were normalized.
- Guides: 50 generic and 62 internal-text guides were rewritten as sourced one-sentence guides in 5 languages. 37 unsourced superlatives were softened. One distance was removed (Ulleung 188 km). Hours were translated in the 118 -ph-/-tr- rows.
- The 14 spa rows were not touched. No military-access places. No personal data.

## Before / after examples
### gocamping-3394
Before:
```
{'Guide': 'EN: Tent camping · Own trailer site · verify vehicle.\nKO: 텐트 캠핑 · 개인 트레일러·차종 확인.\nJA: テントキャンプ · 持込トレーラー・車種確認.\nZH: 帐篷露营 · 自带拖挂营位·确认车型.\nES: Camping en tienda · Remolque propio · confirma vehículo.', 'Details': 'Region: 충청남도 태안군\nCoordinates (reference only, from source): 36.897995, 126.207265\nEN: Use the national-park booking portal. The shop is listed for July–August only; conflicting pitch counts are omitted. Confirm dates, unit, equipment, vehicle admission and booking requirements. Foreign-ID, Korean phone/ID and English service eligibility are unverified. The entrance, parkin
```
After:
```
{'guide': 'EN: Tent pitches and own-trailer sites in Wonbuk-myeon, Taean; check vehicle size rules before bringing a trailer.\nKO: 태안군 원북면에 있는 텐트·개인 트레일러 사이트 캠핑장입니다. 트레일러 반입 전 차량 규정을 확인하세요.\nJA: Wonbuk-myeon, Taeanにあるテント・持ち込みトレーラーサイトのキャンプ場です。トレーラー持ち込み前に車両規定を確認してください。\nZH: 位于Wonbuk-myeon, Taean、提供帐篷营位、自带拖车营位的露营地。携带拖车前请确认车辆规定。\nES: Parcelas para tienda y plazas para remolque propio en Wonbuk-myeon, Taean; consulta las normas de vehículos antes de llevar remolque.', 'details': 'EN: Book through the national-park reservation portal. The camp shop opens July–August only. Confirm dates, unit, equipm
```
### scenery-gb-ulleung-dodonghang-port
Before:
```
{'Guide': 'EN: Main ferry port of Ulleungdo, about 188 km from Pohang.\nKO: 포항에서 약 188km 떨어진 울릉도의 대표 여객선 항구입니다.\nJA: 浦項から約188km、鬱陵島の主要フェリー港。\nZH: 郁陵岛的主要渡轮港口，距浦项约188公里。\nES: Principal puerto de ferris de Ulleungdo, a unos 188 km de Pohang.', 'Details': 'Region: 경상북도 울릉군\nEN: Tel: • 1330 Travel Hotline: +82-2-1330(Korean, English, Japanese, Chinese)  • For more info: +82-54-790-6454. Website: www.ulleung.go.kr/tour. Listed by Korea Tourism Organization (VisitKorea English); current operation was not live-checked, so confirm hours and closures before visiting. Booking, foreign-card payment, ID ru
```
After:
```
{'guide': 'EN: Main ferry port of Ulleungdo.\nKO: 울릉도의 대표 여객선 항구입니다.\nJA: 鬱陵島の主要フェリー港。\nZH: 郁陵岛的主要渡轮港口。\nES: Principal puerto de ferris de Ulleungdo.', 'details': 'EN: Tel: +82-54-790-6454 (1330 Travel Hotline: +82-2-1330). Website: www.ulleung.go.kr/tour. Check hours and booking before visiting.\nKO: 방문 전 운영시간·휴무를 확인하세요.', 'sources': 'https://english.visitkorea.or.kr/svc/contents/contentsView.do?vcontsId=96926\nhttps://www.ulleung.go.kr/tour'}
```
### dining-yuchi
Before:
```
{'Guide': 'EN: Beef-blood haejangguk and boiled meat.\nKO: 선지해장국과 수육。\nJA: 牛の血入りヘジャングクとゆで肉。\nZH: 牛血醒酒汤和白切肉。\nES: Sopa con sangre de ternera y carne cocida.', 'Details': 'Region: 경기도 수원시 팔달구\nEN: Public restaurant listing checked; current opening, menu and English service are unconfirmed. Confirm ingredients and allergies; dish names do not establish vegetarian or halal suitability.\nKO: 공개 음식점 자료를 확인했습니다. 당일 영업·메뉴·영어 응대는 미확인입니다. 재료와 알레르기를 문의하세요. 음식 이름만으로 채식·할랄 적합성을 판단하지 마세요.', 'Sources': 'https://yuchifnb.com/\nChecked 2026-10-28'}
```
After:
```
{'guide': 'EN: Beef-blood haejangguk and boiled meat.\nKO: 선지해장국과 수육。\nJA: 牛の血入りヘジャングクとゆで肉。\nZH: 牛血醒酒汤和白切肉。\nES: Sopa con sangre de ternera y carne cocida.', 'details': 'EN: Confirm ingredients and allergies; dish names do not establish vegetarian or halal suitability.\nKO: 재료와 알레르기를 문의하세요. 음식 이름만으로 채식·할랄 적합성을 판단하지 마세요.', 'sources': 'https://yuchifnb.com/'}
```
### dining-mihyang-sejong
Before:
```
{'Guide': 'EN: Jochiwon seafood restaurant with haemul-jjim and agwi-jjim, listed by KTO.\nKO: 한국관광공사가 해물찜과 아귀찜을 소개하는 조치원의 해물요리 식당.\nJA: 韓国観光公社が海鮮蒸し煮とアンコウの蒸し煮を紹介する鳥致院の海鮮料理店。\nZH: 韩国旅游发展局介绍的鸟致院海鲜餐厅，菜单包括海鲜炖煮和鮟鱇鱼炖煮料理。\nES: Restaurante de mariscos en Jochiwon incluido por KTO, con haemul-jjim y agwi-jjim de rape.', 'Details': 'Region: 세종특별자치시 None\nEN: Tourism sources identify this venue and address, not current operation. Check opening, menu, reservations and dietary needs before visiting.\nKO: 관광 출처로 상호와 주소를 확인했으며 현재 영업은 미확인입니다. 방문 전 영업 여부·메뉴·예약·식이 제한을 확인하세요.', 'Sources': 'https://english.visitk
```
After:
```
{'guide': 'EN: Jochiwon seafood restaurant serving haemul-jjim and agwi-jjim.\nKO: 해물찜과 아귀찜을 내는 조치원의 해물요리 식당.\nJA: 海鮮蒸し煮とアンコウの蒸し煮を出す鳥致院の海鮮料理店。\nZH: 鸟致院海鲜餐厅，供应海鲜炖煮和鮟鱇鱼炖煮。\nES: Restaurante de mariscos en Jochiwon con haemul-jjim y agwi-jjim de rape.', 'details': 'EN: Hours 11:00–22:00; tel 044-866-3173 (phone booking). Parking for 20 cars, take-out, cards accepted. Call ahead to confirm hours, booking, card payment and English support.\nKO: 11:00~22:00, 044-866-3173(전화 예약). 주차 20대, 포장 가능, 카드 결제 가능. 방문 전 영업 여부·메뉴·예약·식이 제한을 확인하세요.', 'sources': 'https://english.visitkorea.or.kr/svc/contents/content
```
## Re-import fixes (2026-10-28)

- **Missing popup titles, root cause:** the quality FULL CSVs were written with a UTF-8 BOM (`EF BB BF`) before `이름`. The earlier working exports (`/workspace/audit/*-FULL.csv` and `data/v2/exports/*.csv` at main 85b0491) had no BOM. With the BOM, My Maps read the first header as `\ufeff이름`, so it didn't treat it as the title column and fell back to "제목 없음". Fix: BOM removed. The header line, column order, CRLF record endings, LF line breaks inside cells and quoting style are now byte-identical to 85b0491.
- **Language lines:** every Guide and Details cell still has LF line breaks between the EN/KO/JA/ZH/ES lines (0 cells run together; the average is 4 breaks per Guide, the same as 85b0491). The run-together display came from the same failed header detection, so it should clear once the BOM-free files are re-imported.
- **Addresses:** every 주소 matches main 85b0491 (0 differences). Daiso Songtan is `경기도 평택시 경기대로 1636 (신장동)`.
- **Typos fixed in English Details:** Novebmer→November (2), servere, unforseen, cheack, storea (2), circumsances, faciliity, facilty, offical, safey, seperately.
- **Gonghwachun (dining-gonghwachun):** Details now say the original Gonghwachun closed in 1983, its building is now the Jjajangmyeon Museum, and this is a separate, later restaurant using the name. The full-width "。" in the Korean guide was also fixed.
- **Counts:** Culture 626, Nature 504, Food 571, Activities 387, Shopping 240 (2,328 in total).
