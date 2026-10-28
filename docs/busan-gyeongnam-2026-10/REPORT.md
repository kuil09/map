# Busan + Gyeongsangnam-do append (v2), built 2026-10-28 KST

## Output
These files use the 11-column v2 format. Latitude and Longitude are empty, and every Type comes from TYPE-MAP.md. The Guide column has 5 newly written lines (EN/KO/JA/ZH/ES), and Practical has EN and KO.

| Layer | File | Rows | Types |
|---|---|---|---|
| culture_sights | culture-busan-gyeongnam-append-v2.csv | 37 | landmark 16, museum 13, temple 7, performing_arts 1 |
| nature_camping | nature-busan-gyeongnam-append-v2.csv | 34 | beach_coast 12, scenery 10, garden_arboretum 6, park_wetland 5, camping 1 |
| food_drink | food-busan-gyeongnam-append-v2.csv | 33 | korean_soup 8, korean 6, noodles 5, seafood 5, bakery_cafe 5, chinese 2, bbq_grill 1, chicken 1 |
| activities_wellness | activities-busan-gyeongnam-append-v2.csv | 27 | rides_railbike 8, theme_park 5, museum_science 4, adventure 4, animals 2, craft_workshop 2, water_sports 2 |
| shopping | shopping-busan-gyeongnam-append-v2.csv | 19 | traditional_market 15, outlet 2, mall 1, home_living 1 |
| **Total** | | **150** | Busan 86, Gyeongnam 64 |

- **Record IDs:** use the pattern `<layer>-bg-<city>-<slug>`.
- **Sources:** each row has the VisitKorea English page, plus the official site when KTO lists one.
- **Rebuilding:** run `python3 build_v2.py`. The picks are in `../sel.py` and the guides are in `guides.py`.

## Method and dedupe
- **Candidate pool:** 608 VisitKorea English items. They came from the Busan regional list (RPRS_RGN 02), the Tongyeong list (17, the only Gyeongnam regional list), and totalSearch filtered on legal-dong codes 26 and 48. Tax-refund shops were removed.
- **Dedupe:** I checked against the 813 live rows (single-v2, gyeongbuk append-v2 and fix-pins) and found **0 overlaps**. None of the live rows has a Busan or Gyeongnam address. None of the 8 round-1 Daegu places is included.
- **Gyeongnam coverage:** it is thinner than Busan, because KTO's English site only has a regional list for Tongyeong. The rest came from keyword searches.

## Restaurant spot-check (10, checked 2026-10-28 KST)
All 10 are still operating. Current hours, closing days and phone numbers are in Practical, and the check pages are in Sources.

| Restaurant | Result |
|---|---|
| 금수복국 | Operating (Michelin Selected 2024). The ground floor is open 24 hours. |
| 해운대암소갈비집 | Operating. Confirmed on its own site. |
| 평산옥 | Operating. Closed Sundays. |
| 장성향 | Operating. Hours differ slightly between listings. |
| 모모스커피 본점 | Operating. Its own site gives 07:30–18:00. |
| 태종대짬뽕 | Operating. Closed Wednesdays. Confirmed on the Yeongdo-gu tourism site. |
| 뚱보할매김밥 | Operating. Confirmed on Tongyeong U-Tour. |
| 부산식당 (Haeinsa) | Operating. |
| 진주통닭 | Operating. Closed Mondays. |
| 할매복국 | Operating. Closed Mondays. |

The other 23 food rows keep the standard line "KTO-listed; not live-checked".

## Videos (official channels only, YouTube Data API)
10 rows have videos. Every channel below is official:

| Place | Channel |
|---|---|
| Beomeosa | VISIT BUSAN |
| Gamcheon | VISIT BUSAN and 부산튜브 (the Busan Metropolitan City official channel) |
| Jagalchi | VISIT BUSAN |
| Haedong Yonggungsa | VISIT BUSAN |
| UN Memorial Cemetery | The UNMCK channel and 부산튜브 |
| Jinjuseong | 하모진주 (the Jinju City official channel) |
| Tongyeong Cable Car | 통영시 |
| Gwangalli Beach | VISIT BUSAN |
| Blueline Park | VISIT BUSAN and 부산튜브 |
| Haeundae Beach | 부산튜브 |

Haeinsa, Upo and the other places had no specific video on these channels, so none was attached.

## Excluded on purpose
- **Spas, jjimjilbang and waterparks** (to avoid generic guidance): Spaland Centum, Hurshimchung, Taejongdae Spa, Cimer, SMB Wellness, and Clubd Oasis waterpark.
- **Other categories:** the casino, hotels and resorts, golf, festivals and hospitals.
- **Military or access caution:** Gadeokdo Lighthouse.
- **Recreational forests:** their campsite status was not verified for this region.
- **No street number (village-only address):** Cheongsapo, and island villages such as Bijindo.
- **No usable data:** Mokjangwon (the KTO text was too thin) and Suyeongman Yachting Center (a competition venue with no public programme or hours).
- **Sinseondae:** it has only a 산-lot address.
- **Kwangjuyo:** it is a shop inside Shinsegae Centum City, not a standalone place.
- **Duplicate brand:** the second Gaya Halmae Milmyeon (I kept the Nampo one).
- **Trimmed to about 150** (lower priority or overlapping a kept place):
  - Gimhae National Museum
  - Jinhae Museum
  - Namhae German Exhibition Hall
  - Sancheong Herbal Medicine Museum
  - Yongmunsa (Namhae)
  - Taejongdae cliffs (Busan Tower and Jeoryeong cover that coast)
  - Jinhae NFRDI eco-park
  - Daepunggwan
  - Geochang Wolseong Space Center
  - Daewonsa
  - Woljeon Fish Market
  - Lotte Mall Jinju
  - Hallyeohaesang NP (the general park entry; its sights are covered by other rows)
  - Sondo Yonggung Suspension Bridge

## Address changes and remaining imprecision
- **Cleanup:** 58 addresses were changed. I removed dong names in parentheses, 일대/일원 and building-name suffixes, and expanded 부산/경남 to the full province names. Every change is logged in `build-log.json`.
- **Possibly imprecise (all have a number, none is guessed):**
  - **Underground road numbers that may not geocode well:**
    - 국제시장 `부산광역시 중구 중구로 지하31`
    - 부전시장 `부산광역시 부산진구 중앙대로 지하717`
    - 서면지하도상가 `부산광역시 부산진구 중앙대로 지하737`
  - **Mountain lot:** 거제 해금강 `경상남도 거제시 남부면 갈곶리 산1`, which points to the islets' lot rather than a boat terminal.
  - **Lot-number (지번) addresses, not road names:**
    - 일광해수욕장 (삼성리 143-10)
    - 송정해수욕장 (송정동 712-2)
    - 구조라해수욕장 (구조라리 500-1)
    - 달아공원 (연화리 114-2)
    - 하동송림 (광평리 440-5)
    - 상림공원 (교산리 1073-1)
    - 여좌천 (여좌동 217)
    - 통영생태숲 (인평동 1279)
    - 삼락생태공원 (삼락동 29-46)
    - 기장시장 (대라리 72-3)
    - 송도구름산책로 (암남동 129-4)
    - 밀곳 (부평동2가 72-2)
- **Data caveats:**
  - **LOTTE Premium Outlets Dongbusan:** KTO's English page carries the hours and description of Lotte Department Store Gwangbok. I kept the address (기장해안로 147, which is correct for Dongbusan) and dropped the wrong hours.
  - **Dadaepo Beach:** KTO has no English description, so I wrote the guide fresh.
