# Gwangju · Jeollanam-do · Jeonbuk-do append (v2), built 2026-10-28 KST

## Output
These files use the 11-column v2 format. Latitude and Longitude are empty, and every Type comes from TYPE-MAP.md. Guide has 5 newly written lines (EN/KO/JA/ZH/ES); Practical has EN and KO.

| Layer | File | Rows | Types |
|---|---|---|---|
| culture_sights | culture-jeolla-append-v2.csv | 41 | landmark 17, museum 13, temple 10, catholic_pilgrimage 1 |
| nature_camping | nature-jeolla-append-v2.csv | 40 | scenery 20, beach_coast 12, garden_arboretum 5, park_wetland 3 |
| food_drink | food-jeolla-append-v2.csv | 36 | korean 10, seafood 9, bbq_grill 4, noodles 4, korean_soup 4, chinese 2, bakery_cafe 2, chicken 1 |
| activities_wellness | activities-jeolla-append-v2.csv | 20 | rides_railbike 9 (cable cars, rail bike, monorails, steam train), museum_science 5, animals 2, adventure 1, water_sports 1, craft_workshop 1, sports_fitness 1 |
| shopping | shopping-jeolla-append-v2.csv | 13 | traditional_market 12, outlet 1 |
| **Total** | | **150** | Gwangju 5 districts, 18 Jeonnam and 11 Jeonbuk cities/counties |

- **Record IDs:** `<layer>-jl-<city>-<slug>` (Gwangju districts as `gwangju-dong`, `gwangju-buk`, …).
- **Province prefix:** 전남광주통합특별시 launched 2026-07-01 and replaced 광주광역시 and 전라남도; road names and numbers are unchanged. All Gwangju/Jeonnam rows use 전남광주통합특별시, all Jeonbuk rows 전북특별자치도. Some geocoders may not yet know the new name; if one fails, retry with the old prefix (same road address).
- **Sources:** each row has the VisitKorea English page, plus the official site when KTO lists one.
- **Rebuilding:** run `python3 build_v2.py`. The picks and the drop list are in `../sel.py`; the guides are in `guides.py`.

## Method and dedupe
- **Candidate pool:** 1,071 VisitKorea English items from the Gwangju (RPRS_RGN 04), Jeonju (11), Mokpo (12) and Yeosu (16) regional lists plus totalSearch keyword sweeps filtered to stdg 29/46/45/52 and the new 12 prefix.
- **Dedupe:** checked against the 1,176 live rows (single-v2 plus every append-v2), by name (EN and KO) and by road address, automated in the build. The 10 Jeolla places already live were excluded (see below). **0 overlaps remain.** None of the 8 round-1 Daegu places is involved.

## Restaurant spot-check (10, checked 2026-10-28 KST)
All 10 are still operating; their 2026 hours were written into Practical. Sources: KTO TourAPI mirrors dated October 2026 (koreacharts, ktriptips), city tourism sites (Mokpo, Yeosu, Gwangju city blog) and the owner's site where one exists.
Songjeong Tteokgalbi 1 (now also closed Sundays, not only the 1st Monday) · 1960 Cheongwonmomil (11:00-20:00 with a 15:00-16:00 break; KTO still says 10:30) · Dokcheon (closed 2nd/4th Sun) · CLB Bakery (daily) · Gyeongdo Hoegwan (11:00-21:00) · Naju Gomtang Noanjip (closed Mon) · Deokinkwan (daily) · Veteran Kalguksu (daily 09:00-20:00; older English listing said closed Thu) · Waengi Kongnamul-gukbap (daily) · Han Kook Jib (daily).

## Videos (official channels only, YouTube Data API)
9 rows have videos: Odongdo (Yeosu City), Mokpo Marine Cable Car (Mokpo City), Suncheonman Bay and Suncheonman National Garden and Naganeupseong (Suncheon City), Jeondong Cathedral (Jeonju City), Juknokwon and Metasequoia Road (Damyang County), Daeheungsa (Haenam County). The API quota ran out (HTTP 403) partway through, so the Gunsan, Iksan, Buan, Gochang, Jindo, Wando and KNPS searches returned nothing. A 10th candidate (Hyangiram) was skipped because the only hit was a festival live stream. Raw results are in `../raw/yt.json`.

## Excluded on purpose
- **Spa, waterpark, lodging, golf, festivals, medical:** Sol Beach Jindo, The Ocean Resort and waterpark, Sono Belle and Ocean Play, Damyang spa, Wolchulsan hot springs, Hampyeong haesujjim, Jinan Red Ginseng Spa, Gunsan CC, hospital listings, every hotel/resort/pension, every festival and tax-refund shop. No military-access places were in the pool.
- **No street number:** Nokdong Port, Gaudo, Seonyudo Beach, Jangjado, Baemsagol, Samhakdo, Dolsando, Geumodo, Baekdo, Chodo, Bogildo, Doripo, Jangheung Jeongnamjin, Hyangjeokbong, Wibong falls and fortress, Taepyeong botanical garden, Jjangttungeo Bridge, Cheonsa Bridge and others.
- **Mountain lot (산):** Mudeungsan Jusangjeolli, Yudalsan, Gatbawi, Geumseongsanseong, Naejangsan NP (봉덕리 산122), Maisan Hwaeomgul.
- **Address conflict:** Gugyedeung (KO and EN addresses disagree).
- **Duplicates or inside another entry:** Royal Portrait Museum (in Gyeonggijeon), Iksan National Museum (Mireuksa address), Gochang Dolmen Museum, Korea Tea Museum (inside Korean Tea Culture Park), Gyeokpo Beach (next to Chaeseokgang), Eunsusa (next to Tapsa), Gapgi Hoegwan second listing.
- **Already live:** Imsil Cheese Theme Park, Nabawi, Seonyu Sky Sunline, Jeonju Crafts Exhibition Hall, Okdol Beach, Ungpo campground, Iksan riding centre, Maisan Tapsa, Leesungdang, Binhaewon.
- **Campsite status not verified:** the Nagan, Bangjangsan, Cheongwansan, Hoemunsan and Byeonsan recreational forests.
- **Trimmed to stay near 150:** Owen Hall, Uijae, Hall of Popular Music, Yongjangseong, Pungpaejigwan, Wanggung-ri, Mokpo Natural History Museum, Heungguksa, Baengnyeonsa, Cheoneunsa, Ajung Lake, Oedaldo, Jangseongho, Muan tidal flat, Jeungdo slow city, some minor restaurants, cafés and cruises.

## Address changes and remaining imprecision
There are 36 address cleanups, listed in build-log.json: dong parentheses, old prefixes (광주광역시 / 전라남도 → 전남광주통합특별시), and trailing names (거목한정식, 대전횟집, 롯데쇼핑몰).
Still imprecise:
- **Maple Ecology Park (Jeongeup):** the KO list gives lot 내장동 560; the row uses 내장호반로 273-17 from KTO's English page.
- **Facility or trailhead addresses:** Jirisan Nogodan uses 화엄사로 356 (Hwaeomsa area; the Nogodan trail starts at Seongsamjae); Jiksopokpo uses the Silsang-sa trailhead (실상길 62); the national/provincial parks (Mudeungsan, Wolchulsan, Deogyusan, Jirisan Namwon, Maisan, Moaksan, Daedunsan, Cheongwansan, Seonunsan) use a visitor centre or office address; Korean Tea Culture Park shares 녹차로 775 with the Tea Museum; Jindo Sea Route, Cheongsando and Seonyudo use one point on a long site.
