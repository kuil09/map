# Thin-regions append v2 (tag -tr-), built 2026-10-28 KST

The live map and the repo were not touched. The base is kuil09/map at 9070138 (data/v2), with 2,222 places.

## Rows
| Layer | New rows | New total |
|---|---|---|
| Food | 39 | 571 |
| Shopping | 19 | 240 |
| Culture | 22 | 626 |
| Nature | 13 | 504 |
| Activities | 13 | 387 |
| **Total** | **106** | **2,328** |

After this batch, 172 rows of capacity remain.

## Regions
- **Busan:** Haeundae, Busanjin, Jung, Suyeong, Dongnae, Seo, Yeongdo, Nam and Gijang. Busan had only 28 Food and 12 Shopping rows.
- **Gyeongbuk:** Gyeongju and Andong.

## Pipeline
This follows the Pyeongtaek pipeline: TourAPI KorService2 calls (areaBasedList2, detailCommon2, detailIntro2) run on the user's PC, then build.py applies the emit() checks.

## Addresses
- Addresses are TourAPI road addresses with no floor or unit suffix.
- The legal-dong is kept in parentheses wherever TourAPI gives it (8 rows).

## Duplicate checks
- Candidates were deduped against all 2,222 places by normalized name and by address (344 candidate duplicates were dropped).
- At build time, Yeongdo Bongnae Market turned out to be already live, so it was dropped.

## Spot checks
Ten restaurants were checked against listings on 2026-10-28:
- 개미집 본점
- 미포할매복국본가
- 류센소
- 엄용백 돼지국밥
- 원조18번완당
- 신창국밥
- 백구당
- 동래할매파전
- 고향밀면
- 효자통닭

**교동쌈밥 was dropped.** A blog post reports it closed on 2025-12-28.

## Videos
16 rows have videos, all from official uploads only. The channels are 부산광역시 (부산튜브), 영도구, 해운대구, 기장군, 부산 중구, 안동시 and 경상북도 (BOISO TV).

## Caveats
- **Jeonnam was skipped.** The lDong 46 code returned 0 items, probably because the code changed with the 전남광주 merger.
- **Facility claims left out.** TourAPI's "world's largest" and "first" claims (Shinsegae, Wooyang, Hahoe mask museum, Yugyo museum, Brick Campus) and Shinsegae's spa facilities are not used.
- **전촌용굴.** TourAPI says it was a former military operations zone that is now open to the public. Nothing about access is mentioned in the row.
- **Booking or limited days.**
  - The Busan Film Studio tour needs an application.
  - 명인안동소주 tours need a reservation.
  - The 부산공동어시장 auctions run only in the early morning.
  - 자갈치크루즈 needs ID.
- **Five-day markets.** 감포공설시장 and 풍산장터 run on dates ending in 3 and 8.
- **Korean-only hours.** In 70 rows the EN Details point readers to the Korean note for hours, because TR could not fully translate them.
- **Shared address.** The Centum City Ice Rink shares an address with Shinsegae Centum City, because it is inside the store.
