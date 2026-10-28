# Gyeongbuk append, v2 format (2026-10-28 KST). Not applied to the live map or the repo.

Format: same 11 columns as single-v2 (이름, 주소, Latitude, Longitude, Type, Region, Guide, Practical, Video, Sources, Record ID). Lat/Lng left empty so rows are placed by address, following the t16 decision.

## Per-layer counts (130 total)
| Layer | File | Rows | Type breakdown |
|---|---|---|---|
| Culture & Sights | culture_sights-gyeongbuk-append-v2.csv | 32 | landmark 15, temple 10, museum 5, catholic_pilgrimage 2 |
| Nature & Camping | nature_camping-gyeongbuk-append-v2.csv | 28 | beach_coast 11, scenery 10, camping 5, garden_arboretum 2 |
| Food & Drink | food_drink-gyeongbuk-append-v2.csv | 25 | korean 8, bakery_cafe 6, seafood 4, chicken 2, bbq_grill 2, korean_soup 2, noodles 1 |
| Activities & Wellness | activities_wellness-gyeongbuk-append-v2.csv | 24 | rides_railbike 7, museum_science 5, adventure 5, craft_workshop 4, animals 2, theme_park 1 |
| Shopping | shopping-gyeongbuk-append-v2.csv | 21 | traditional_market 10, mall 5, warehouse_store 3, outlet 2, department_store 1 |

Every Type value is taken from that layer's TYPE-MAP.md list, so no new groups are introduced. Some mappings are judgement calls:
- jjimdak goes to chicken, sundubu goes to korean_soup, and tea house goes to bakery_cafe.
- Souvenir, cosmetics and clothing shops go to mall, hypermarkets go to warehouse_store, and the gotgam direct-sale centre goes to traditional_market.
- Skywalks, monorails, the skyrail, Space Walk and the floating walkway go to rides_railbike.
- Paragliding, the zipline and the forest therapy and forest activity centres go to adventure.
- Recreational forests go to camping (see the camping caveat below).
- Confucian academies, villages, bridges and tombs go to landmark.

## Dropped in this pass: 0
- **Duplicates: 0.** I compared all 130 against the 687 single-v2 rows by Record ID, by name (normalised en and ko parts) and by exact address. Only one Gyeongbuk row is already on the map (Mungyeong Rail Bike), and the candidate set had already excluded it.
- **Round-1 Daegu: 0.** All 8 round-1 IDs (dining-daegu-*, scenery-daegu-*) are Daegu city records. None is in this set.
- **Military access: 0.** No candidate requires military access. Bohyunsan Optical Astronomy Observatory is a civilian research site (KASI) with a visitor centre.
- **Closed restaurants: 0.** All 10 spot-checked restaurants are still operating (table below).
- **Excluded upstream** (gap-limitations-ko.md):
  - hot springs and spas
  - lodging, hospitals and golf courses
  - festivals
  - Hwarang training centre
  - V-Train, because its page text was corrupted
  - items with no address
  - Palgongsan Gatbawi and Seonbonsa, because they overlap a Daegu hold

## Restaurant spot-check (10 of 25, run 2026-10-28)
| Record ID | Result | Evidence |
|---|---|---|
| dining-gb-andong-geobukgol-andong-guksi | Operating. Licence status 정상영업 (public data dated 2026-05/06) | pick.ozro.kr |
| dining-gb-andong-wonjo-andong-jjimdak | Operating. 2026-10-22 listing: 08:00–20:00, closed Thursdays. Practical updated because the KTO page is stale | info.koreacharts.com (KTO data) |
| dining-gb-andong-andong-bonga-galbi | Operating. Listed in the Andong city galbi-alley directory | tourandong.com |
| dining-gb-andong-andong-gangodeungeo-teojutdaegam | Operating under the new sign 하회터줏대감. A 2026-01 article; licence 영업 | fmr.purpleo.co.kr, onkorea |
| dining-gb-andong-ongcheon-21segi-jjinppang | Operating. NTS status 계속사업자 | bizno.net |
| dining-gb-andong-heotjesabap | Operating. Current hours and Tuesday closure added | info.koreacharts.com |
| dining-gb-gyeongju-yongganggukbap | Operating. Split hours; closed 2nd and 4th Wednesdays | diningcode |
| dining-gb-gyeongju-yosukgung-1779 | Operating. 2026 hours, reservation-based | access.visitkorea.or.kr (KTO) |
| dining-gb-yeongdeok-jukdosan | Operating. 09:30–21:00, open all year | info.koreacharts.com |
| dining-gb-pohang-camellia | Operating. 2026 hours | info.koreacharts.com |

For these 10, the Practical column carries the updated hours and Sources has the check URLs plus "Spot-checked 2026-10-28". Most of the evidence comes from aggregators that mirror KTO or licence data. Official operator or city pages were not reachable from the box. The other 15 restaurants were not checked and keep the KTO "confirm before visiting" wording.

## Translations
Guide has 5 lines in this order: EN, KO, JA, ZH, ES. All 5 lines are newly written for each row from the KTO English description, and they replace the template text. The ja/zh/es lines are translations of the en/ko meaning.
- A few lines add widely known facts that are not on the KTO page, for example Bongjeongsa's oldest wooden hall, Unmunsa as a nuns' temple, and Mammoth's cream cheese bread.
- After checking the KTO text I corrected 8 lines: Surime, Andong Hanji, Cheongdo Hanok School, Seongdong Market, Gasil Church, Jukbyeon Skyrail, Zootopium and Yeongdeok Sunrise Park.
- No human has reviewed them. A native-speaker skim is still recommended.
- Practical is EN and KO only, matching single-v2. KTO field values such as hours are still in English in the KO line for the 120 rows that were not spot-checked.

## Addresses
- I cleaned 32 addresses: removed parenthetical dong names, removed "1층", removed building or tenant suffixes (온뜨레피움, 용문사), and expanded "경북" to 경상북도. The full list is in build-log.json.
- **9 rows have only a village- or road-level address with no number.** They may geocode to the centre of the village or district, or not at all. Check them after import, and do not invent numbers:
  - three-falls-of-juwangsan (상의리)
  - dodonghang-port (도동리)
  - samseonam-rocks (천부리)
  - chilpo-beach (흥해읍 해안로)
  - homigot-sunrise-square (대보리)
  - yeongdeok-sunrise-park (창포리)
  - hupo-beach (삼율리)
  - bomunho-lake (신평동)
  - gyeongju-namsan (배동)
- Several rows use lot addresses (jibeon, including 산 numbers) because KTO gives no road address for them, for example the Ulleung rocks and trails, Jisandong tombs and Daereungwon. No coordinates were added or guessed.

## Videos
| Place | Videos attached |
|---|---|
| Bulguksa | UNESCO (★Official) |
| Seokguram | 국립중앙박물관 (★Official) |
| Hahoe | VISITKOREA (★Official), plus Chris Travels the World labelled "Video ·" because it is not official |
| Dosan | 세계유산 한국의 서원 통합관리센터 (★Official) and 한국국학진흥원 (★Official) |

All videos come from videos-pending-gyeongbuk.json, and multiple videos are separated by newlines. single-v2 has no earlier example of a non-official or multi-video cell, so the "Video ·" label is new.

## Caveats carried over
- **Camping:** the 4 recreational forests (Tohamsan, Geommasan, Unmunsan, Cheongoksan) have not been confirmed to operate campsites. Their Guide says so. Consider holding them until GoCamping or 숲나들e confirms.
- **Market days:** market days for Uiseong and Seongju are unconfirmed. Their Guide says so.
- **Cell budget:** 130 × 11 = 1,430 cells, bringing the map to about 9,000 of 20,000.

## Files
- append CSVs: `*-gyeongbuk-append-v2.csv` (5 files)
- `guides.py`: the 5-language guide text
- `build_v2.py`: the generator, which can be re-run
- `build-log.json`: the address changes and the approximate-address list
