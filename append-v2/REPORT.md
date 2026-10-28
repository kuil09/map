# Daegu · Ulsan · Gyeonggi append v2 (2026-10-28 KST)

Not applied to live map or repo. 8 columns, existing types only, Record ID `<layer>-dug-<daegu|ulsan|gg>-<slug>`.

| Layer | New | Base | New total |
|---|---|---|---|
| culture | 68 | 419 | 487 |
| nature | 35 | 406 | 441 |
| food | 22 | 388 | 410 |
| activities | 14 | 327 | 341 |
| shopping | 9 | 175 | 184 |
| total | 148 | 1715 | 1863 |

## Checks
- Dedupe vs 1,715 live rows (names + addresses): 0 hits. Shared addresses within batch: 0. Round-1 Daegu 8 excluded.
- Restaurant spot-check (web, 2026-10-28): 10 confirmed operating — 미성당 납작만두, 오뎅식당, 대동강식당, 산호찜갈비, 연포갈비, 처가집부대찌개, 대백손칼국수, 구공탄막창, 거송갈비찜, 언양기와집불고기. Other 14 food rows marked not live-checked. Several spot-check sources are aggregators (koreacharts/ktriptips) mirroring TourAPI, plus 2026 blog visits.
- Videos: 48 rows, official channels only (울산시청TV, 대구TV, 비짓대구, 경기도청, 연천군), matched from upload playlists (search.list intermittently 429). 102 rows pending/no official video (count now 100):

  - Ulsan Eonyang Bulgogi | 울산언양불고기
  - Eonyang Giwajip Bulgogi | 언양기와집불고기
  - Wonjojip | 원조집
  - Dodong Sanbang | 도동산방
  - Badabaragi | 바다바라기
  - Greetvi Coffee | 카페그릿비
  - Gosong Galbijjim Main Branch | 거송갈비찜 본점
  - Miseongdang Napjak Mandu | 미성당 납작만두
  - Sanho Jjimgalbi | [백년가게]산호찜갈비
  - Gugongtan Makchang | 구공탄막창 본점
  - Wonjo Hyeonpung Park Soseon Halmaejip Gomtang | 원조현풍박소선할매집곰탕
  - Donbaksa Gopchang Makchang | 돈박사곱창막창
  - Yongjibong | 용지봉
  - Daebaek Sonkalguksu | 대백손칼국수
  - Daedonggang Sikdang | 대동강식당
  - Park Jiyun's Gachang Jinbang | 박지연의 가창옛날찐빵본점
  - Geumgang Station Rail Café (Banyawol Lotus Village Cooperative) | 금강역 레일 카페(반야월 연꽃마을 협동조합)
  - Odeng Sikdang Uijeongbu Main Branch | 오뎅식당
  - Cheogajip Budaejjigae | 처가집부대찌개
  - Yeonpo Galbi | 연포갈비
  - Gapyeong Naengmyeon Buson Seorak Main Branch | 가평냉면 부손 설악본점
  - Gillimseong | 길림성
  - Ganwolsan Mountain | 간월산
  - Paraesopokpo Falls | 파래소폭포
  - Sunmot Ecological Park | 숯못 생태공원
  - Ulsan Ilsan Beach | 일산해수욕장 (울산)
  - Sinbulsan Falls National Recreational Forest | 국립 신불산폭포자연휴양림
  - Ulsan Grand Park | 울산대공원
  - Dalseong Marsh | 대구 달성습지
  - Biseulsan Recreational Forest | 비슬산자연휴양림
  - Gunwi Janggok Recreational Forest | 군위 장곡자연휴양림
  - Hwawon Park | 화원동산
  - Gwangmyeong Cave | 광명 동굴
  - Pocheon Sanjeonghosu Lake | 포천 산정호수
  - Namhansanseong Provincial Park [UNESCO World Heritage] | 남한산성도립공원 [유네스코 세계문화유산]
  - Bucheon Botanical Garden | 부천식물원
  - Gimpo Daemyeong Port | 김포 대명항
  - Hwaseong Fossilized Dinosaur Egg Site | 화성 공룡알 화석지
  - Yuldong Park | 율동공원
  - Jungmisan Recreational Forest | 중미산자연휴양림
  - Yangpyeong Wild Flower Arboretum | 양평 들꽃수목원
  - Ulsan Lotte Grand Wheel | 울산 롯데 그랜드 휠
  - Oegosan Onggi Village | 외고산옹기마을
  - Onggigol Ceramics | 옹기골도예
  - Myeongpum Otgol 1616 Cooperative Society | 명품옻골 1616 협동조합
  - Hwaseong Fortress Tourist Trolley | 화성어차
  - Yeoju Hwangpo Sailboat | 여주 황포돛배
  - Pocheon Art Valley [Hantangang UNESCO Global Geopark] | 포천아트밸리 (한탄강 유네스코 세계지질공원)
  - Herb Island | 허브아일랜드
  - Pocheon Sansawon | 포천 산사원
  - Chisanseowon Confucian Academy | 치산서원
  - Petroglyphs of Bangudae Terrace in Daegok-ri [UNESCO World Heritage] | 울주 대곡리 반구대 암각화 [유네스코 세계유산]
  - Daegu Concert House (Formerly Daegu Citizens' Hall) | 대구콘서트하우스 (구.대구시민회관)
  - Nokdongseowon Confucian Academy | 녹동서원
  - Daegu Opera House | 대구오페라하우스
  - Dongsan Cheongna Hill | 동산청라언덕
  - Village of the Nampyeong Mun Clan in Bon-ri | 남평문씨본리세거지
  - Daegu Dalseong Park | 대구 달성공원
  - Museum of Natural Dye Arts | 자연염색박물관
  - Daegu Gyesan Cathedral | 대구 계산동성당
  - Yongyeonsa Temple (Daegu) | 용연사(대구)
  - Daegyeonsa Temple | 대견사
  - Buinsa Temple (Daegu) | 부인사(대구)
  - Gunwi Buddha Triad Grotto (2nd Seokguram) | 군위 아미타여래삼존 석굴
  - Yuksinsa Shrine | 육신사
  - Ancient Tombs in Bullo-dong | 대구 불로동 고분군
  - Nakdong River Victory Memorial Hall | 낙동강승전기념관
  - Daegu Textile Museum | 대구섬유박물관
  - Sammaksa Temple | 삼막사
  - Woljeon Museum of Art Icheon | 이천시립월전미술관
  - Yeoju Museum | 여주박물관
  - Anyang Art Park | 안양예술공원
  - Seongnam Arts Center | 성남아트센터
  - Anseong Namsadang Performance Hall | 안성 남사당 공연장
  - Odusan Unification Observatory | 오두산 통일전망대
  - Imjingak Resort (Pyeonghwa Nuri Park) | 파주 임진각(평화누리공원)
  - Yangju Olleung Royal Tomb [UNESCO World Heritage] | 양주 온릉(단경왕후) [유네스코 세계문화유산]
  - Paju Jangneung Royal Tomb [UNESCO World Heritage] | 파주 장릉(인조, 인열왕후) [유네스코 세계문화유산]
  - Goyang West Five Royal Tombs [UNESCO World Heritage] | 고양 서오릉 [유네스코 세계문화유산]
  - Hongneung and Yureung Royal Tombs [UNESCO World Heritage] | 남양주 홍릉(고종과 명성황후)과 유릉(순종과 순명,순정 황후) [유네스코 세계문화유산]
  - Janganmun Gate | 장안문
  - Banghwasuryujeong Pavilion | 방화수류정(동북각루)
  - Suwonhyanggyo Confucian School | 수원향교
  - Simgokseowon Confucian Academy | 심곡서원
  - Osan Dolmen Park | 오산 고인돌역사공원
  - Yeoju Godalsa Temple Site | 여주 고달사지
  - Goyang Heungguksa Temple | 흥국사(고양)
  - Paju Bogwangsa Temple | 보광사(파주)
  - Suwon Hwaseong Museum | 수원화성박물관
  - Gwacheon Chusa Museum | 추사박물관(과천)
  - Haewoojae Museum (Mr. Toilet House) | 해우재
  - Paju Book City | 파주 출판도시
  - Petite France | 쁘띠프랑스
  - Eonyang Market | 언양알프스시장
  - Ulsan Jungang Traditional Market | 울산 중앙전통시장
  - Ulsan Keunaegi Night Market | 울산큰애기청년야시장
  - Bangeojin Live Fish Center | 방어진 활어센터
  - Daegu Medicinal Herb Wholesale Market | 대구 한약재 도매시장
  - Suwon Nammun Market | 수원 남문시장
  - Uijeongbu Jeil Market | 의정부 제일시장

## Uncertain / review
- 오두산 통일전망대, 임진각 평화누리: public sites (no military pass) but near DMZ — included; confirm policy.
- 화성 공룡알 화석지: KTO address has new 2026 gu 만세구; FIX to `경기도 화성시 송산면 공룡로 659`.
- Lot/approx addresses kept (sourced): 천전리·반구대 암각화, 서생포왜성, 슬도, 숯못, 강동 주상절리, 처용암, 울산중앙시장(옥교동 98-8), 원조집, 불로동 고분군, 달성습지, 고달사지, 비둘기낭폭포. 큰애기야시장 `울산광역시 중구 젊음의거리 90` confirmed by KTO accessible-tourism page (access.visitkorea.or.kr) and tripinfo/koreacharts; 중구 tourism site gives the strip as 시계탑거리 23 ~ 젊음의거리 101. Sources added to the row. Note: sources list Mon–Tue closures.
- 울산대공원: KTO text mentions a pool; included as park, guide omits it.
- Fix-up pass 2026-10-28: both Starbucks rows (184332 대구종로고택, 184336 더양평DTR) dropped.
- KTO 218045 dropped: listing is titled 'Korean Traditional Culture Center (한국전통문화체험관)', 대구 수성구 달구벌대로525길 14-23, but its whole description is about Momyeongjae (모명재), the Dureung Doo clan shrine to Ming general Doo Sa-chung. Name/address and description describe different things, so the row cannot be sourced consistently. Replaced by 수창청춘맨숀 (177459).
- Guides written from KTO descriptions only; no distances added. All 49 Ulsan rows re-checked line by line; corrected 10: 간절곶 ("earliest on east coast", not mainland), 반구대 (removed unsupported 'whale/hunting scenes'), 석남사 (south of Gajisan; nuns' temple), 슬도 (removed 'off Bangeojin'), 강동몽돌 (removed 'Buk-gu'), 화암 주상절리 (removed 'fan-shaped'), 태화강 국가정원 (removed 'themed gardens'), 롯데 그랜드휠 ('rooftop'→7th floor), 중앙시장 (vendor types per KTO), 옹기골도예 (named craftsman; reservations).

## Exclusions
Military-access DMZ sites (3rd Tunnel, Dora, 승전OP, 통일촌, 캠프그리브스, 애기봉, 평화곤돌라); spa/water-park/pool rows; village-only addresses (명선도, 나사해변, 신불산, 3·1로, 북한산성, 고대산); shared-address rows (대왕암 출렁다리, 고래바다여행선, 고래문화마을 판타지움, 블레어하우스); live duplicates (수원화성, 화성행궁, 민속촌, 동화사 등).