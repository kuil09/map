# Jeju append (v2), built 2026-10-28 KST

## Output
These files use the 11-column v2 format. Latitude and Longitude are empty, and every Type comes from TYPE-MAP.md. Guide has 5 newly written lines (EN/KO/JA/ZH/ES); Practical has EN and KO.

| Layer | File | Rows | Types |
|---|---|---|---|
| culture_sights | culture-jeju-append-v2.csv | 38 | museum 21, landmark 12, temple 3, performing_arts 2 |
| nature_camping | nature-jeju-append-v2.csv | 51 | scenery 21, beach_coast 20, garden_arboretum 9, park_wetland 1 |
| food_drink | food-jeju-append-v2.csv | 35 | seafood 7, bakery_cafe 7, bbq_grill 4, noodles 4, world_cuisine 4, korean_soup 3, korean 2, chinese 2, western 1, chicken 1 |
| activities_wellness | activities-jeju-append-v2.csv | 20 | theme_park 5, animals 4, craft_workshop 2, adventure 2, museum_science 2, rides_railbike 2, sports_fitness 2, water_sports 1 |
| shopping | shopping-jeju-append-v2.csv | 6 | traditional_market 5, mall 1 |
| **Total** | | **150** | 제주시 and 서귀포시 |

- Record IDs: `<layer>-jj-<jeju|seogwipo>-<slug>`.
- Province prefix: every row uses `제주특별자치도` (a long-established name). No new administrative names are used.
- Rebuild: `python3 build_v2.py` from `..`; picks and drop list in `../sel.py`, guides in `../guides.py`, spot-check in `../spot.py`.

## Method and dedupe
- Candidate pool: 782 VisitKorea English items (RPRS_RGN__08 Jeju region, restaurant and shopping lists, plus totalSearch keyword sweeps filtered to stdg 50). 98 had no Korean address.
- Dedupe: checked against the 1,264 live rows in `../jeolla/full/*-FULL.csv` by name (EN and KO) and by road address. None of the live rows is in Jeju. **0 overlaps, 0 shared addresses within the append.**

## Restaurant spot-check (10, checked 2026-10-28 KST)
All 10 are still operating; the 2026 hours went into Practical. Sources: visitjeju.net, KTO mirrors (koreacharts), matjipnote (Kakao-based, Oct 2026), the owner's site and recent blogs.
Ujin Haejangguk (annex closed Tuesdays) · Samdae Guksu Hoegwan (07:30-02:00) · Oneunjeong Gimbap (takeaway only, phone reservation, closed Sundays) · Sukseongdo (11:30-22:00) · Haenyeo Kitchen Jongdal (Thu-Sun 12:00/17:00, KRW 59,000, booking required) · Dombedon · Ollae Guksu (Mon-Sat 08:00-15:00) · Sanbang Sikdang (closed Wednesdays) · Deokseongwon (Tuesday closure unclear: every vs 2nd Tuesday) · Heukdonga (break 15:00-17:00).

## Videos
The YouTube Data API returned HTTP 429 (quota exhausted) on every call, so Video is blank on all 150 rows. Priority rows to fill later from official channels (Jeju Special Self-Governing Province, Jeju City, Seogwipo City, Hallasan NP / Cultural Heritage):
Seongsan Ilchulbong, Manjanggul, Geomunoreum, Hallasan Yeongsil, Cheonjiyeon, Jeongbang, Cheonjeyeon, Jusangjeolli, Udo Seobinbaeksa, Bijarim, Seongeup Folk Village, Jeju Haenyeo Museum, Jeju 4.3 Peace Park, Jeju-mok Office, Dongmun Market, Seogwipo Maeil Olle Market.

## Excluded on purpose
- Spa, waterpark, lodging, golf, festivals, adult: Waterworld Jeju, Sanbangsan Carbonate Hot Springs, Sono Calm, Sono Belle, Grand Josun, Maison Glad, pensions, glamping and youth hostel, Jeju Love Land, ICC Jeju, every tax-refund or duty-free shop. No military-access places were in the pool.
- No street number: Iho Tewoo, Samyang, Sehwa, Hagosudong, Geommeolle and Jungmun Saekdal beaches, Gimnyeongsagul, Gueom and Yongsu ports, Handam trail, Hagwi-Aewol road, Sanjicheon, Gangjeongcheon, Saryeoni trail, Yongnuni and Jeoji oreum, Gapado, Chujado, Saeyeongyo, Geumsan Park, Altteureu airfield, Tokkiseom, Byeoldobong, Jungmun Tourist Complex, Geumneung Port, Hallim 5-day market.
- Mountain lot (산): Hallasan (토평동 산15-1), Sanbangsan, Geum, Darangswi and Saebyeol oreum, Udobong, Gosalli trail.
- Closed to the public: Yongcheondonggul, Dangcheomuldonggul, Bengdwigul.
- Inside another entry or same address: Gyorae Recreational Forest (Stone Park address), World Natural Heritage Center (Geomunoreum address), Sinyang Seopji Beach (Yumin address), New Paradise cruise (submarine address), The Cliff (inside Pacific Land), duplicate Innisfree, Spirited Garden, Dochidol and Haenyeo Kitchen listings, Sarabong Park, Suwolbong Peak, Hyeopjaegul/Ssangyonggul (Hallim Park), Seogwang Tea Garden, Baengnokdam.
- Trimmed to stay near 150: Panpo, Sammaebong, Dotoreum, Gunsan Oreum, Gogeunsan, Sinsan Park, Conan, Hamo and Geumneung beaches, Changkkom, Andeok Valley, Daheeyeon, Hallim Park, Jeju Central Park, Wonder Island, Teseum, chocolate museums, Joanne Bear, Marine Park, Norimae, 5.16 tree tunnel, many cafés and black-pork restaurants.
- Camping: no Jeju campsite came up with a verifiable street address and confirmed operation, so nature has no `camping` rows. Recreational forests are typed `scenery`.

## Address changes and remaining imprecision
39 address cleanups are listed in build-log.json, mostly removing dong parentheses, 번지 and trailing building names. There are 3 manual fixes:
- Seongeup Folk Village: the KO field was garbled (`서귀포시 표선면 서성일로 20 3294`), so the row uses the lot `성읍리 3294` from the KTO English page.
- Seogwipo Maeil Olle Market: the KO field gives the lot `서귀동 340`, so the row uses the road address `중앙로62번길 18` from KTO English.
- Oedolgae: the KO field has a typo, `서흥동 791`. The row uses `서홍동 791` (KTO English: Seohong-dong).

Still imprecise:
- **Lot-number addresses**, which may land on a parcel next to the sight: Seongeup 성읍리 3294, Gwakji 곽지리 1565, Sagye 사계리 2147-35, Yongmeori 사계리 112-3, Gwangchigi 고성리 224-33, Glass House 고성리 46, Cheonjiyeon 서홍동 666-1, Oedolgae 서홍동 791, Jungmun Equestrian 대포동 2270.
- **Facility or entrance addresses:** Biyangdo uses the Hallim port ferry terminal (한림해안로 146). Hallasan Trekking uses the Eorimok visitor centre. Yeongsil uses the Yeongsil trail office. Marado uses an on-island address. Udo Sanho Beach and Hundertwasser Park are on Udo, reached by ferry. Geomunoreum uses the Heritage Center address.
- **Check access:** Manjanggul has had sections closed for repairs. Geomunoreum needs a reservation. Yongmeori Coast closes at high tide and in rough seas.
