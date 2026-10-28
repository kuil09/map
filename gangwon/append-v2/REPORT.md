# Gangwon-do append (v2), built 2026-10-28 KST

## Output
These files use the 11-column v2 format. Latitude and Longitude are empty, and every Type comes from TYPE-MAP.md. Guide has 5 newly written lines (EN/KO/JA/ZH/ES); Practical has EN and KO.

| Layer | File | Rows | Types |
|---|---|---|---|
| culture_sights | culture-gangwon-append-v2.csv | 38 | museum 16, temple 9, landmark 8, performing_arts 3, catholic_pilgrimage 2 |
| nature_camping | nature-gangwon-append-v2.csv | 40 | scenery 18, beach_coast 14, garden_arboretum 4, park_wetland 3, camping 1 |
| food_drink | food-gangwon-append-v2.csv | 36 | korean 8, noodles 8, bbq_grill 7, bakery_cafe 5, seafood 4, korean_soup 4 |
| activities_wellness | activities-gangwon-append-v2.csv | 20 | rides_railbike 4, water_sports 4, adventure 3, theme_park 2, animals 2, craft_workshop 2, museum_science 1, games 1, sports_fitness 1 |
| shopping | shopping-gangwon-append-v2.csv | 13 | traditional_market 12, hobby_games 1 |
| **Total** | | **147** | all 18 Gangwon cities/counties |

- **Record IDs:** `<layer>-gw-<city>-<slug>`. All addresses use the prefix 강원특별자치도.
- **Sources:** each row has the VisitKorea English page, plus the official site when KTO lists one.
- **Rebuilding:** run `python3 build_v2.py`. The picks are in `../sel.py` and the guides are in `guides.py`.

## Method and dedupe
- **Candidate pool:** 682 VisitKorea English items, from the Gangneung (RPRS_RGN 09) and Sokcho (20) regional lists plus totalSearch keyword sweeps filtered to stdg 42/51. 500 of them had a Korean address.
- **Dedupe:** checked against the 967 live rows (single-v2 plus every append-v2). The Gangwon places already live were excluded: Neurin Sup and Donggang campgrounds, AK Plaza Wonju, Gangchon Rail Park, Hantangang Su Leisure, Wonju Hanji Theme Park, Samaksan Cable Car, Balwangsan, Byeolmaro, the Wonju climate-change centre, Hoengseong Luge, Alpaca World, King Canoe, Jeongseon Rail Bike, Sutasa, Jeongamsa, Gyereuk and Hoengseong Hanu-gukbap. **0 overlaps remain.** The automated name-prefix matches were checked by hand and are false positives (for example Donggang rafting vs. the Donggang campground). None of the 8 round-1 Daegu places is involved.

## Restaurant spot-check (10, checked 2026-10-28 KST)
All 10 are still operating. Their 2026 hours were written into Practical. The sources are KTO TourAPI mirrors dated October 2026 (koreacharts), plus the owners' own site or Instagram where they exist.
Chodang Halmeoni Sundubu (closed Wed) · Donghwa Garden (closed Wed) · Gangneung Gamja Ongsim (closed Thu) · Eomjine Kkomakjip (now signed 엄지네포장마차 본점; open daily) · Dancheon Sikdang · Chungchosoo Mulhoe · Woomi Dakgalbi · Odaesan Minsok Sikdang · Cheorwon Makguksu (closed Seollal/Chuseok) · Wondae Makguksu (closed Tue).

## Videos (official channels only, YouTube Data API)
10 rows have videos: Ojukheon (Gangneung City), Jeongdongjin Beach (Gangneung City), Yeongwol Jangneung (Yeongwol County), Hwanseongul (Samcheok City), Gwongeumseong (Korea National Park Service TV), Odaesan Seonjae-gil (KNPS TV), Seoraksan Botanical Garden (Sokcho City), Sokcho Eye (Sokcho City), Sogeumsan bridge (Wonju City) and Soyang Dam (Chuncheon City). Raw results are in `../raw/yt.json`.

## Excluded on purpose
- **Military or civilian-control-line access:** Goseong Unification Observatory, the DMZ Peace Trail, the Goseong DMZ Museum, Cheorwon Peace Observatory, the Iron Triangle security tour, Yanggu Punch Bowl / War Memorial / Unification Hall, Cheorwon Plain, Daeamsan Yongneup (permit) and Dopiansa (former CCL area; excluded to be safe).
- **Spa, waterpark, lodging, golf and ski:** Cheoksan Hot Springs, Sol Beach Ocean Plays, Waterpia, Alpensia Ocean700, every hotel/condo/resort/pension, High1, Welli Hilli, Phoenix, Elysian Gangchon and Alpensia ski/CC.
- **Festivals and tax-refund shops:** all of them.
- **No street number:** Cheongchoho, Gyeongpoho, Sogeumgang valley, Daecheongbong, Jujeongol, Heullimgol, Hajodae, Beopsuchi, Micheongol, Mindungsan, the Soyangho sections, Paroho, Hyangho, Milky Way Bridge, Namdaecheon, the BTS bus stop, Deokangsan, Forest Museum and others.
- **Mountain lot or unclear access:** Cheongnyeongpo, Eorayeon, Hambaeksan, the Soyangho ferry, Ulsanbawi; the recreational forests (campsite status not verified); Bongjeongam.
- **Duplicates or inside another entry:** Ojukheon second listing, Morundae/Hwaam complex, Ulleong Bridge, Daegeumgul, the Haesindang folk museum, Maze Art (inside Wonju Jungang Market), Inner and Southern Seorak, Naksan Provincial Park.
- **Other:** Donghae Railroad Experience Center (no public programme; hours by arrangement). Some minor cafés and restaurants were trimmed to keep the total near 150.

## Address changes and remaining imprecision
There are 43 address cleanups, listed in build-log.json: dong parentheses, trailing text such as 안내소~자작나무숲 / 정동진역 / 나동 / 9동 1호 / building names, and the province prefix.
Still imprecise:
- **Mountain lot:** Chuam Chotdaebawi, 동해시 추암동 산 69.
- **Lot-number (jibun) addresses:** Geumjin Beach (금진리 149-3), Badabuchae Trail (심곡리 114-3; this is one of two trail entrances), Hoedong-ri (회동리 1-14).
- **Shared or facility addresses:** Hwanseongul shares 환선로 800 with the cave-park ticket office; Guryong Falls uses the Sogeumgang trailhead (소금강길 500); Outer Seorak uses the visitor centre (설악산로 833); Seonjae-gil uses Woljeongsa (오대산로 374-8); the Wondae-ri birch forest uses the information centre (자작나무숲길 760, about 3 km walk); Jeongdongjin rail bike uses Jeongdongjin station (정동역길 17, same as the beach).
