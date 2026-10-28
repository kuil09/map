# Seoul + Incheon append (v2), built 2026-10-28 KST

## Output
These files use the 11-column v2 format. Latitude and Longitude are empty, and every Type comes from TYPE-MAP.md. Guide has 5 newly written lines (EN/KO/JA/ZH/ES); Practical has EN and KO.

| Layer | File | Rows | Types |
|---|---|---|---|
| culture_sights | culture-seoul-incheon-append-v2.csv | 55 | museum 21, landmark 20, temple 5, performing_arts 5, catholic_pilgrimage 4 |
| nature_camping | nature-seoul-incheon-append-v2.csv | 30 | park_wetland 14, beach_coast 6, garden_arboretum 5, scenery 5 |
| food_drink | food-seoul-incheon-append-v2.csv | 39 | noodles 8, korean_soup 7, korean 5, chinese 5, bakery_cafe 4, seafood 4, bbq_grill 3, world_cuisine 2, chicken 1 |
| activities_wellness | activities-seoul-incheon-append-v2.csv | 12 | rides_railbike 4, games 2, water_sports 2, theme_park 1, sports_fitness 1, adventure 1, museum_science 1 |
| shopping | shopping-seoul-incheon-append-v2.csv | 15 | traditional_market 12, mall 3 |
| **Total** | | **151** | Seoul 104 / Incheon 47 |

- Record IDs: `<layer>-si-<seoul|incheon>-<slug>`.
- Gu names: Incheon reorganised its gu on 2026-07-01 (제물포구, 영종구, 서해구, 검단구). To follow the "no new administrative names" rule, every row uses the pre-2026 gu: 영종/inland 중구 → `중구`, 서해/검단 → `서구`. The one 송림동 row (Samdae Incheon Gejang) is `동구`. build_v2.py asserts that no new gu name remains. Note: some live rows already use 제물포구/영종구, so the map is mixed on this point.
- Rebuild: `python3 build_v2.py` from `..`. Picks and the drop list are in `../sel.py`, guides in `../guides.py`, and the spot-check in `../spot.py`.

## Method and dedupe
- Candidate pool: 1,416 VisitKorea English items (RPRS_RGN__01 Seoul and __05 Incheon, plus keyword sweeps filtered to stdg 11/28, with tax/duty-free shops removed). 437 had no Korean address.
- Dedupe: checked against 1,414 live rows (`../jeolla/full/*-FULL.csv` + `../jeju/append-v2/*.csv`) by name (EN/KO) and road address. 29 name duplicates were skipped at selection. 3 more were dropped for sharing a live address. **The final build has 0 duplicates and 0 shared addresses.**

## Restaurant spot-check (10, checked 2026-10-28 KST)
All 10 are still operating, and the 2026 hours went into Practical:
- Myeongdong Kyoja: 10:30-21:00; the annex merged into the main store in 2026.
- Imun Seolnongtang: break 15:00-16:30.
- Yujin Sikdang: closed Mondays and Tuesdays.
- Mabongrim: closed on the 2nd and 4th Monday.
- Also checked: Nampo Myeonok, Gangseo Myeonok, Samcheong Sujaebi, Sinseung Banjeom, Pyeongnaeok, Samdae Incheon Gejang.

## Videos
YouTube search.list returned 429 (Search quota). Videos were therefore matched from the full upload lists of the official channels VisitSeoul TV (UCtlz8pU3IiHf77V8s740-pQ) and Incheon Tourism (UCZp3wYQOYTfmtqw4yX4RqQA), 1,963 uploads in total. 18 rows have a video:
Changgyeonggung, Deoksugung, Bukchon, Namsangol, Open Port Museum, Seoul Botanic Park, Seoul Forest, Seonyudo, Haneul Park, Yeouido/Ttukseom/Banpo Hangang, Naksan, Seoullo 7017, Wolmi Sea Train, Tongin Market, Sinpo Market, Triple Street.
The other 133 rows need a video (list: see build output / `Video` blank). Highest priority: Gyeongbok-area museums, Changdeokgung, Jongmyo, Jogyesa, Myeongdong Cathedral, Namdaemun, Noryangjin, Gwanghwamun, Heunginjimun, Incheon Chinatown, Ganghwa forts, Eurwangni/Hanagae beaches, Sorae.

## Excluded on purpose
- Spa/jjimjilbang, lodging, golf, festivals, duty-free/tax-refund shops: none kept. No military-access places (e.g. DMZ/observatory sites that need permits) are included.
- No street number or mountain lot (산): Bugaksan, Cheonggyesan, Eungbongsan, Songpa Naru Park, Manisan (산35), Goryeosan (산131-1), Gyeyangsan (산57-1), Mokseom, Wangsan Beach, Minmeoru Beach, Bugeun-ri Dolmen.
- Same address: MMCA Deoksugung (inside Deoksugung, 세종대로 99), Seoul Children's Museum (live Children's Grand Park, 능동로 216), KidZania (live Lotte World, 올림픽로 240), Lotte World Aquarium (live Lotte World Mall, 올림픽로 300).
- Not in the harvested pool: 14677.
- Operation unclear: Yongma Land (the amusement park closed in 2011).
- Trimmed to stay near 150: Sweet Park, Real Escape, Brooklyn The Burger Joint, Bangsan Market, Lotte Star City, Saemaeul Sikdang and Bongchu Jjimdak (chains), Royal Indian.

## Address changes and remaining imprecision
build-log.json lists 93 address cleanups, mostly removing floors, unit numbers, dong parentheses and trailing building names. There are 3 manual fixes:
- Sinpo International Market: the KO field gives the lot `신포동 7-40`; the row uses the road address `우현로49번길 11-5` from KTO English.
- LoL Park: `종로 33 그랑서울 타워[1]` became `종로 33`.
- Mijin: `종로 19 르메이에르종로타운1` became `종로 19`.

Still imprecise:
- **Lot-number addresses:** Yangjaecheon Ecological Park (양재동 261-23), Janghwa-ri Sunset Viewing Point (장화리 1408), Sunset Leisure 435 (망원동 205-5; a boat dock in Mangwon Hangang Park).
- **Area or trail-side addresses:** Bukchon Hanok Village (계동길 37 is one point in a neighbourhood). Horyonggoksan (대무의로 464, near a trailhead). Hanagae Beach (KO gives 하나개로 150; KTO EN gives 대무의로 310-11). Hangang parks use their management-office addresses.
- **Island beaches by ferry:** Seopori (Deokjeokdo) and Sugi (Sido). Simnipo (Yeongheungdo) can be reached by bridge.
