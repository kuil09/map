# Batch-next append (v2): 150 rows, 2026-10-28 (KST)

Base: kuil09/map main 83af27c, 1,863 live places. The live map and the repo were not touched.

## Regions and why
I counted the repo exports per si/gun. These areas had the fewest rows relative to their population and foreign-visitor relevance:
- **Gwangju (40 rows):** the whole city had 24 rows (동구 9, 북구 7, 광산 3, 남구 3, 서구 2). It is a metro city of about 1.4M, with Yangnim-dong, the Biennale and the Mudeungsan gateway.
- **Jeonbuk / Jeonju (47):** Jeonju had 16 rows, and Jeonju Hanok Village itself was missing. Other si/gun had 1–10 rows each (Wanju, Sunchang, Muju, Gunsan, Gimje, Namwon, Imsil, Gochang, Buan, Jeongeup).
- **Gyeongnam (28):** Changwon had 3 rows despite about 1M people. Gimhae had 6, Jinju 5 and Yangsan 0. Inland counties (Sancheong, Hamyang, Hapcheon, Geochang, Uiryeong) had 1–4 each.
- **Gyeonggi (29):** Goyang 8, Seongnam 4, Bucheon 4, Ansan 8, Gimpo, Gwacheon, Gunpo 0, Guri 0, Gwangmyeong 2, Suwon (outside the Hwaseong core), Paju (outside the CCZ), Pocheon, Namyangju, Anyang.
- **Busan (6):** Saha 3, Sasang 2, Yeonje 0.

## Rows per layer
| layer | added | base → new total |
|---|---|---|
| culture | 71 | 487 → 558 |
| nature | 32 | 441 → 473 |
| food | 29 | 410 → 439 |
| activities | 10 | 341 → 351 |
| shopping | 8 | 184 → 192 |
| **total** | **150** | **1,863 → 2,013** |

All Type values come from the existing 37. Names are "EN | KO". Guides are one sentence each in EN, KO, JA, ZH and ES. There is no "…" anywhere. Record IDs use the format `<layer>-bn-<gwangju|jeonbuk|gn|gg|busan>-<slug>`.

## Sources and addresses
- **Sources:** the VisitKorea English contentsView page for each place. The road address comes from the Korean address text on that page.
- **Old-style names:** KTO now prints 전남광주통합특별시. It was mapped back to 광주광역시 (old-style name rule).
- **Cleaning:** floors, units, parentheses and trailing building names were stripped. 83 addresses changed; the before → after list is in build-log.json.
- **One manual fix:** 174479 Gwacheon Wildflower: KTO gives "밤나무길 100 (갈현동) 520", where 520 is the lot number (confirmed by koreatourinfo, 밤나무길 100(갈현동 520)). I used 경기도 과천시 밤나무길 100.
- **Dedupe:** checked against all 1,863 live names and addresses with 0 hits. The 8 round-1 Daegu places are excluded, since no Daegu rows were added.

## Restaurant open-check (10 of 29 food rows, web-checked 2026-10-28)
All 10 are listed as operating, with hours, closures and phone in Details and the sources in Sources:
- 고궁 전주본점
- 솔가
- 다문
- 밀양돼지국밥 (김해)
- 유명회관
- 미미원
- 대광식당
- 곰보식당
- 우백갈비 아중리본점
- 기찻길옆오막살이

The other 19 food rows, and every non-food row, are marked "not live-checked".

Conflicts I found:
- **다문:** KTO English shows 10:00–21:00, while 2026 listings show 11:30–20:00. I used the 2026 hours and noted the conflict.
- **유명회관:** the Chinese Gwangju tour page says "open all year". The 2026-09 sources say it is closed on Sundays, which is what I used.

## Videos: 28
All 28 come from official government or tourism channels, matched from uploads playlists only (raw/yt-uploads.json, 27 channels). Each video is dedicated to the place or names it in the title. If there was no clear match, the cell is empty. A few choices to note:
- **Seosamneung:** the Goyang video covers 서삼릉 and 서오릉 together.
- **Jeonju Hanok Village:** a 전주시 night drone video.
- **Saha:** the Jangnim Port video is from the 사하구 district channel.

## Uncertainties
- **Lot-number (jibun) addresses**, used where KTO gives no road address. They are sourced, but are not road addresses:
  - 186558 용봉동 700-24
  - 186625 성리 417
  - 199411 삼례리 768
  - 81302 석상리 707
  - 93633 평촌리 1021
  - 193121 백산리 265-66
  - 63365 동완산동 612
  - 81547 풍암동 460
  - 215965 금남로3가 20-2
  - 111557 궁동 78
- **Shared address:** 중원동로 52 is used by both Jehwangsan Park and the Jinhae Museum, which sits inside the Jinhae Tower on that hill.
- **Gochang Blue Farm (248243):** the KTO English text calls it "Geochang", but the address is Gochang. The guide follows the address.
- **KTO description quality:** some descriptions are promotional. The guides keep only factual claims, and any number they use (heights, counts, years) comes from KTO.
- **Excluded:**
  - Hwaseong Fortress, which the live Paldalmun row already covers.
  - Aegibong and the Imjingak gondola, because of military/CCZ access.
  - Rows with only approximate addresses (일대/부근/산 lot numbers).
  - Hotels, hospitals, festivals, golf, spas or jjimjilbang, chains and tax-refund shops.
- **Video channels:** I picked them by title search. Each is clearly a city, province or tourism-body account, but none was verified beyond its name.
