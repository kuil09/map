# Pyeongtaek / Camp Humphreys append (v2): 106 rows, 2026-10-28 (KST)

Base: kuil09/map 274f833, 2,116 live places. The live map and the repo were not touched.
Area: Pyeongtaek (Anjeong-ri/Paengseong, Songtan, downtown/Bijeon/Sosabeol, Godeok) with day trips to Osan, Anseong, Asan and Dangjin.

## Rows per layer
| layer | added | base → new total |
|---|---|---|
| culture | 20 | 584 → 604 |
| nature | 11 | 480 → 491 |
| food | 47 | 485 → 532 |
| activities | 13 | 361 → 374 |
| shopping | 15 | 206 → 221 |
| **total** | **106** | **2,116 → 2,222** |

By city: Pyeongtaek 47, Asan 16, Anseong 15, Osan 14, Dangjin 14. Capacity left after this batch: 278.

## Sources and checks
- Data: KTO TourAPI KorService2 (96 rows; run from the user's PC as approved, source link = koreacharts TourAPI mirror) and VisitKorea English (10 Songtan/Anjeong food rows).
- Addresses: sourced road addresses; dong in parentheses, floor and trailing building names removed (log in build-log.json). Dedupe vs all 2,116 live rows by name and address: 0 hits in final set; no shared addresses within the batch.
- Leave-outs applied: no on-post places, no jjimjilbang/spa/pool guidance, no unsourced distances/times/superlatives (e.g. TourAPI "5분 거리", "전국 최다", "국내 최초/유일" not used), no "…".
- Rows not spot-checked carry the "not live-checked" note.

## Restaurant spot-checks (10, all operating per current listings, 2026-10-28)
The Big Bite, Miss Jinn Hamburger, Gimne-jip, Songtan Dukkeobi Sikdang, Obok Dwaeji, Chicago, Yubaksa Kalguksu, Jaehong Bunsik, Seopo Kalguksu, Hyundai Galbi (Asan). Source URLs in each row's Sources.

## Videos
19 rows, official city channels only (평택시, 안성시, 아산시, 당진시, 오산시); USAG Humphreys uploads scanned, no place match. News/council clips skipped.

## Uncertain
- Chicago: KTO English hours "11:00-10:00" are invalid; spot-check hours (11:00–22:00, closed Wed) used.
- KTO English text for Songtan Song's Budaejjigae and Gungmin Budaejjigae wrongly says Andong; not used.
- The Big Bite: listings differ on closing time (22:00 vs 20:30).
- Obok Dwaeji: confirmed only via a third-party NAVER mirror.
- Pyeongtaek Art Center opened January 2026; Yeohae Naru opened September 2025 — new venues, programs may change.
- Reservation-only: Pyeongtaek Herb Farm, Kongkongi studio, Gyeonggi Safety Experience Center. Sapgyoho Amusement Park is seasonal (spring–autumn).
- Dangjin World Art Circus: TourAPI listing only, not live-checked.
- 48 rows: TourAPI hours are Korean-only; the EN note points to the KO line instead of machine-translating.

## Geocode fix (2026-10-28)
- shopping-ph-pyeongtaek-daiso-songtan-main-store: 주소 `경기도 평택시 경기대로 1636` failed to geocode in My Maps. Changed to `경기도 평택시 경기대로 1636 (신장동)` (legal-dong suffix, postcode 17719) per TourAPI-derived listing https://info.koreacharts.com/tour/4026339/contents.html and https://www.ktriptips.com/kor/shopping/4026339; Daiso store list (https://www.daisogift.co.kr/usestoreinfo) confirms 경기대로 1636. No sourced 지번 found. If this still fails, drop the row.
