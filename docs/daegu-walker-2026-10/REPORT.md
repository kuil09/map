# Daegu / Camp Walker append (v2): 103 rows, 2026-10-28 (KST)

Base: kuil09/map 5e31d4b, 2,013 live places. The live map and the repo were not touched.
Focus: Nam-gu (Daemyeong-dong / Bongdeok-dong, around Camp Walker), plus the rest of Daegu and day trips to Chilgok, Gyeongsan and Cheongdo.

## Rows per layer
| layer | added | base → new total |
|---|---|---|
| culture | 26 | 558 → 584 |
| nature | 7 | 473 → 480 |
| food | 46 | 439 → 485 |
| activities | 10 | 351 → 361 |
| shopping | 14 | 192 → 206 |
| **total** | **103** | **2,013 → 2,116** |

- Nam-gu rows: 30 food, 7 shopping and 2 activities (39 in total).
- Day trips: Gyeongsan 3, Cheongdo 6, Chilgok 3.
- Only the existing 37 types are used (the build asserts this). The record prefix is `-dw-`.

## Sources
- **68 KTO (VisitKorea English) rows.**
- **35 rows from official Nam-gu and Daegu lists:**
  - Nam-gu 별미음식점, 대를 이은 음식점, 앞산맛둘레길, 안지랑곱창골목 and 전통시장현황
  - the daegufood.go.kr certified-restaurant list
- Kansong and Hyangchon addresses come from 열린관광 (access.visitkorea) and tour.daegu.go.kr.

## Excluded
- Jibun-only or village-only addresses: Daegu Stadium, Cheongdo Stone Ice Storage, Daemyeong Reservoir, Romance Papa, Sicily and others.
- Spa Valley and other spa, hot-spring or pool entries.
- Medical, lodging and festival entries.
- Daegu Grand Hotel Duty Free (likely closed).
- Starbucks.
- Suseongmot Lake Resort (duplicates the live Suseong Lake).
- Miryang Dwaeji Gukbap (already live; caught by the dedupe).

## Spot-checks (10 restaurants, 2026-10-28)
- **The 10 spot-checked rows** (7 from Nam-gu lists, 3 from KTO):
  - 대덕식당, 이태리피자, 앞산할매손칼국수, 인디안식당, 와촌손칼국시본점, 양정화네앞산온천골, 일미정
  - KTO: Bongsan Jjimgalbi, Midam, Cheongdo Chamhanwoo
- These were checked against current third-party listings (koreacharts, autoreserve, siksin, odiga). Each listing showed the place as operating with current hours, and those hours are written into Details.
- This is not a phone call. The Details say to call ahead.

## Videos
- **21 rows have videos**, all from official channels:
  - 대구TV
  - 비짓대구
  - 대구중구
  - 남다르게구석구석 (the official Nam-gu office channel)
  - 달성사이다 (Dalseong-gun)
  - 경산시
  - 청도군
- The USAG Daegu uploads (53) were scanned, but none of them is about a listed place.

## Uncertain / flag
- **Bongdeok New Market address.** The Nam-gu list says 봉덕로 113, and the Daegu market agency (dtmsa) says 봉덕로25길 6. I used Nam-gu's and noted the conflict in Details.
- **Anjirang Gopchang Alley.** The KTO address is 안지랑로16길 67, but Nam-gu lists the alley's shops on 대명로36길. I kept the KTO address.
- **Indian Sikdang (인디안식당).** It is registered as hansik, not Indian cuisine, and the guide says so.
- **Sparse Nam-gu list rows.** Many Nam-gu list rows have only a name, address, phone and category, so their guides stay generic: they describe only the category or the dish in the name.
- **Ttangttang Chicken Land.** It takes reservations only, and I did not live-check it.
