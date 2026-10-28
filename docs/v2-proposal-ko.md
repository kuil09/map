# Korea Local Guide 데이터 구조 재설계 제안 (v2)

작성: 2026-10-28 (KST) · 기준: `kuil09/map` main `c9bb782` (읽기 전용 clone) · 실제 지도·GitHub 변경 없음

## 0. 핵심 결론 (먼저 읽기)

1. **가장 큰 제약은 열 수가 아니라 "지도 전체 20,000셀" 한도다.** Google 공식 도움말에 지도당 "Up to 20,000 data table cells", "Up to 10,000 lines, shapes, or places"로 나와 있다([My Maps Help: Draw lines & shapes](https://support.google.com/mymaps/answer/3433053)). 가져오기 파일은 2,000행을 넘기지 말라고 돼 있다([Import map features](https://support.google.com/mymaps/answer/3024836)). 레이어당 2,000개, 레이어 10개, 속성 열 50개는 2차 출처 기준이다([GeoMaps 정리](https://geomaps.co/blog/google-my-maps-limits), [Open Source GIS Blog](http://opensourcegisblog.blogspot.com/2015/08/making-maps-with-google-my-maps-part-ii.html)).
2. **지금 구조(레이어당 16열, Shopping·Nature 추가 열 포함)로는 전국 확장이 불가능하다.** 현재 687행 × 약 16.4열이면 약 11,400셀로 이미 한도의 57%다. 여기에 1,100곳을 더하면 약 1,787행 × 16 ≈ 28,600셀이 돼 한도를 넘는다.
3. 그래서 **언어별 열을 따로 두는 것(설명 5 + 안내 5 = 10열)은 places.json에서만 하고, My Maps에는 넣지 않는다.** My Maps용 CSV는 "가볍게 투영한 결과물"로 보고, 모든 레이어에서 같은 11열을 쓴다. 이러면 최대 1,818행까지 들어간다.
4. 그래도 1,818행이 실질적인 상한이다. **전국 약 1,800곳을 넘기면 지도를 권역별로 나눠야 한다**(예: 수도권·충청 / 영남 / 호남·강원·제주). 이건 소유자가 결정할 일이다.
5. 추천은 **옵션 B(전면 v2)**다. 단, 실제 지도 교체는 백업 KML과 ID 대조 게이트를 통과한 레이어부터 하나씩 한다.

## 1. 현재 구조 진단

| 항목 | 현황 | 문제 |
|---|---|---|
| places.json | 648건(대구 41건은 `data/history/daegu-places-staged-*.json`에 분산), 최상위 키 약 110종 | 키가 레코드마다 다름(`kind`/`cuisine`/`camp_types`…). 검증이 어렵다 |
| 다국어 | `description`·`notes`는 언어별 객체로 되어 있다(이미 분리됨) | CSV에서 한 칸에 5개 언어를 몰아 넣어 팝업이 길다 |
| 좌표 | 숫자 좌표 100쌍. 554행은 주소만 있다. 미해결 7행 | `coordinates`/`coordinate_quality`/`coordinate_provenance`/`coordinate_status` 등이 혼재. 주소로 지오코딩된 실제 마커 좌표는 저장소에 없다 |
| 지역 | `area`(Pyeongtaek 등 영문 도시명) | 시도·시군구 체계가 없어 전국 확장 시 필터링·분할이 불가능하다 |
| My Maps 열 | 16열 + 레이어별 예외(Shopping 숫자 Lat/Lng 중복, Nature Source lat/lng) | 레이어마다 열이 달라 일괄 처리를 할 수 없고 셀을 낭비한다 |
| 외국인 실용 정보 | `english_support`, `foreign_card_payment`, `foreign_id_booking_access` 등 일부 레코드에만 있다 | 키 이름이 제각각이고, "모름"과 "아니오"가 구분되지 않는다 |
| 외부 ID | 없음 | TourAPI `contentid`가 없어 중복 판정과 갱신을 할 수 없다 |

## 2. places.json v2 (정본) 스키마

정본은 하나의 파일(또는 시도별 분할 `data/places/<sido>.json`)이다. 모든 레코드는 같은 키를 갖는다. 모르는 값은 `null`로 둔다.

```jsonc
{
  "id": "temple-daegu-donghwasa",          // 기존 Record ID 그대로 (영구 불변)
  "schema_version": 2,
  "layer": "culture_sights",               // 5개 목적 중 하나
  "type": "temple",                        // 아이콘 결정용 세부 종류 (통제 어휘)
  "name":    {"en": "...", "ko": "...", "ja": null, "zh": null, "es": null},
  "address": {"ko": "대구광역시 동구 ...", "en": null},
  "region":  {"sido": "대구광역시", "sigungu": "동구", "legacy_area": "Daegu"},
  "location": {
    "lat": 35.99, "lng": 128.70,           // null = 주소 지오코딩에 맡김
    "source": "official_tourism_published | kto_tourapi | operator_page | address_geocoded_by_mymaps | manual_review",
    "point_kind": "venue | entrance | parking | area_centroid",
    "entrance_verified": false,
    "provenance_note": "...", "source_url": "...",
    "live_marker": {"lat": null, "lng": null, "read_at": null}   // 지도 KML에서 읽은 실제 마커 (선택)
  },
  "description": {"en": "...", "ko": "...", "ja": "...", "zh": "...", "es": "..."},
  "notes":       {"en": "...", "ko": "...", "ja": "...", "zh": "...", "es": "..."},
  "practical": {                            // 3상태: true / false / null(미확인)
    "tax_refund": null, "foreign_card": null, "english_support": null,
    "passport_booking": null, "reservation_required": null,
    "halal": null, "vegetarian": null,
    "evidence": [{"field": "english_support", "url": "...", "checked": "2026-10-28"}]
  },
  "external_ids": {"kto_contentid": "126508", "kto_contenttypeid": "12", "gocamping_id": null},
  "videos": [{
    "url": "https://www.youtube.com/watch?v=...", "title": "...", "channel": "...", "channel_url": "...",
    "official": true, "official_basis": "operator | kto | local_gov | national_park | museum | none",
    "lang": "ko", "subtitles": ["en"], "upload_date": "2019-06-24", "duration_s": 65,
    "last_checked": "2026-10-28", "check_status": "ok | unavailable | private | region_blocked"
  }],                                       // 최대 2개
  "sources": [ /* 기존 구조 그대로 (url, quality, audit) */ ],
  "status": {"operation": "open | seasonal | closed | unverified", "last_verified": "2026-10-28", "publish": "public | excluded_military | hold"},
  "legacy": { /* v1의 나머지 키 전부 (삭제 없음) */ }
}
```

원칙:
- **ID는 불변이다.** Google 내부 객체 ID는 재발급될 수 있으니 저장하지 않고, 검수용 스냅샷에만 남긴다.
- **아무것도 지우지 않는다.** v1에서 매핑되지 않은 키는 `legacy`로 옮긴다. 1차 마이그레이션 테스트는 "v1 값 == v2에서 되돌린 값"으로 검증한다.
- 실용 플래그는 **시설별 근거가 있을 때만** true/false로 둔다. 근거 URL은 `practical.evidence`에 남긴다.
- 영상은 **official 우선**으로 고른다. 비공식 영상은 영어 음성이나 영어 자막이 있고, 업로드한 지 3년 이내일 때만 넣는다.

## 3. My Maps 열 구성 (모든 레이어 동일, 11열)

| # | 열 | 내용 | 비고 |
|---|---|---|---|
| 1 | Name | `English | 한국어` | 제목 열 (영어 먼저) |
| 2 | Address | 한국어 도로명 주소 | 위치 열 (좌표 없을 때) |
| 3 | Latitude | 숫자 또는 빈칸 | 위치 열 (좌표 있을 때) |
| 4 | Longitude | 숫자 또는 빈칸 | |
| 5 | Type | 세부 종류 | 아이콘 스타일 기준 (스타일 "Type"으로 고정) |
| 6 | Region | `대구광역시 동구` | 검색·필터용 |
| 7 | Guide | EN/KO/JA/ZH/ES 한 줄씩, 언어별 140자 이내 | 팝업 가독성을 위해 자름. 전문은 places.json에 |
| 8 | Practical | `English: Yes · Foreign cards: Unknown…` + EN/KO 핵심 안내 | 미확인 항목은 표시 안 함 |
| 9 | Video | `★Official (ko): URL` / `Review (en): URL` 최대 2줄 | 비어 있으면 팝업에서 숨겨짐 |
| 10 | Sources | 공식 URL 최대 3개 + `Checked YYYY-MM-DD` | |
| 11 | Record ID | 불변 ID | 대조 키 |

- 셀 예산: 11열 × 1,818행 = 20,000이다. 현재 687행이면 7,557셀(38%)이다.
- 좌표가 있는 행과 주소만 있는 행이 한 파일에 섞이는 경우가 있다. My Maps는 가져올 때 위치 열을 하나만 고르게 한다. 그래서 **레이어마다 "좌표 행 파일"과 "주소 행 파일"을 나눠서 가져오거나**, 좌표 행도 주소로 처리할지를 결정해야 한다(아래 열린 질문 3). 대안으로, 좌표가 있는 행만 `WKT` 열(`POINT(lng lat)`)을 쓰는 방법은 주소 행과 같이 쓸 수 없어서 마찬가지로 파일을 나눠야 한다.
- 모바일: 팝업은 위에서부터 Name → Guide → Practical → Video 순으로 보인다. 5개 언어를 각 140자로 제한하면 한 화면 반 정도 길이다. 더 줄이려면 Guide를 EN/KO만 두고, JA/ZH/ES는 별도 열로 빼면 된다. 다만 그러면 셀이 늘어난다.
- 언어 분리 열(Guide_en … Guide_es) 방식은 열이 15개 이상이 돼 최대 약 1,300행으로 줄어든다. 전국 확장 목표와 충돌하므로 비추천한다.

## 4. 두 가지 옵션

### 옵션 A: 최소 변경
- places.json은 v1 그대로 두고, 필드를 추가만 한다(`region`, `external_ids`, `videos`, `practical`, `status`).
- My Maps 열은 16열을 11~12열로 정리한다. 레이어별 예외 열(Shopping 중복 Lat/Lng, Nature Source lat/lng)도 없앤다. 이건 Replace all items가 필요하다.
- 장점: 기존 테스트와 이력 파일이 대부분 그대로 유효하다.
- 단점: 키 혼재가 계속된다. 대구 41건이 history 파일에 흩어져 있는 문제도 그대로 남는다. 셀 한도 문제는 해결된다.

### 옵션 B: 전면 v2 (추천)
- 정본은 places.json v2로 통일한다. 대구 41건을 병합하고, `data/places/` 아래에 시도별로 분할한다.
- My Maps는 v2에서 생성한 11열 CSV를 레이어마다 Replace all items로 교체한다.
- TourAPI 수집기가 v2 형식으로 직접 출력하게 한다. 중복 판정은 `kto_contentid`로 1차, 주소·이름 정규화로 2차로 한다.
- 장점: 전국 1,100곳과 영상, 실용 플래그, 다국어를 같은 구조로 확장할 수 있다.
- 단점: 테스트를 재작성해야 한다. 지도 교체는 한 번에 레이어 5개를 전부 바꾼다(위험은 7절의 게이트로 관리).

**추천: B.** 셀 한도 때문에 어차피 Replace all items가 필요하다. 그럴 바에야 정본까지 한 번에 정리하는 게 비용 대비 낫다.

## 5. 마이그레이션 절차 (실제 지도)

1. **동결:** 단일 담당자를 확정하고, 다른 자동화가 지도를 수정하지 않는지 확인한다.
2. **백업:** 레이어별로 KML을 내려받는다(편집 화면 → 레이어 ⋮ → Export data → KML/CSV). 공개 KML 전체도 받는다(`/maps/d/kml?mid=…&forcekml=1`). 저장소에는 SHA256만 넣고, 파일은 아카이브(비공개)에 보관한다. 지도 전체를 "Copy map"으로 사본으로 만들어 두는 것도 롤백용으로 권장한다.
3. **사전 대조:** 백업 KML의 Record ID 집합과 v2 정본의 ID 집합이 정확히 같아야 한다(687 = 687). 레이어별 행 수가 같아야 하고, 미해결 7개 ID가 기대 목록과 같아야 한다.
4. **생성:** `migrate_v2.py`로 5개 레이어 CSV를 만든다(UTF-8, BOM 없음). 레이어별로 좌표 파일과 주소 파일을 나눌지는 열린 질문 3에 따라 정한다.
5. **리허설:** 사본 지도("Copy map")에서 먼저 Replace all items를 실행하고 전수 검수한다.
6. **본 지도 교체:** 레이어 하나씩 진행한다. Reimport and merge → Replace all items → 저장 확인 → 재로딩 → 검수를 마치고 다음 레이어로 넘어간다. 작은 Shopping 레이어부터 시작한다.
7. **사후 검수:** 공개 KML을 다시 받아서 확인한다.
   - 레이어별 행 수와 ID 집합이 정본과 완전히 같은지
   - 중복이 0인지
   - 위치 미해결 행이 기대 목록(7개)과 같은지
   - 좌표 행의 마커 좌표가 정본과 1e-6 이내인지
   - 표본 20건의 팝업 5개 언어·Video·Sources가 맞는지
   - 아이콘이 Type별로 정상인지
   - 모바일 실기기에서 표본을 확인했는지
8. **영수증:** `data/history/migration-v2-<date>-receipt.json`에 전후 해시, 행 수, ID 차이(0이어야 함), 미해결 목록을 기록한다.

### 위험과 롤백
| 위험 | 대응 |
|---|---|
| Replace all items 후 스타일(색·아이콘)이 초기화된다 | 교체 직후 "Style by Type"을 재설정하고 색을 레이어 고정색으로 맞춘다. 이전 스타일 설정을 스크린샷이 아닌 문서로 기록해 둔다 |
| 주소 지오코딩 결과가 바뀌어 마커 위치가 달라진다 | 교체 전 KML의 실제 마커 좌표를 `location.live_marker`에 저장한다. 교체 후 좌표가 바뀐 행 목록을 수동으로 검토한다. 필요하면 좌표 행으로 전환한다 |
| 미해결 행이 늘어난다 | 기대 목록과 다르면 그 레이어를 즉시 백업 KML로 Replace해 되돌린다 |
| 내부 객체 ID가 재발급된다 | 예상된 일이다. Record ID로만 대조한다 |
| 셀 한도를 넘는다 | 생성 스크립트가 셀 수를 계산해서 20,000을 넘으면 실패하게 한다 |
| 공유 링크·제목 손상 | `mid`는 그대로 유지된다(같은 지도에서 레이어만 교체). 제목과 설명은 건드리지 않는다 |

**롤백:** 레이어 단위로 백업 KML을 Replace all items로 다시 가져온다. 지도 전체가 손상되면 사본 지도를 비교 기준으로 쓴다. 단, 사본은 `mid`가 달라서 공개 링크를 대체할 수 없다. 그러니 원본 지도에서 레이어를 복구하는 게 원칙이다.

## 6. 저장소 테스트·검증기 변경

- `schemas/places.schema.json` → v2 JSON Schema를 새로 만든다. 필수 키를 고정하고, `type`/`layer`/`location.source`/`check_status`는 enum으로, 실용 플래그는 `boolean|null`로 정한다.
- `scripts/validate.py`에 추가할 검사:
  - ID 유일성
  - 5개 언어 모두 존재 여부
  - 시도 17종 enum
  - 좌표가 대한민국 범위(33–39N, 124–132E) 안에 있는지
  - `kto_contentid` 중복
  - 영상 최대 2개, 비공식 영상은 (영어 음성 또는 영어 자막) 및 업로드 3년 이내
  - `last_checked`가 90일을 넘으면 경고
  - CSV 셀 수 ≤ 20,000, 레이어별 ≤ 2,000행
- 기존 기준 테스트(v35/v36/v37 커밋 고정 해시 테스트, 57개)는 **역사 기록으로 동결**한다. 기대값을 바꾸지 않는다. 대신 새 `tests/test_v2_migration.py`를 만든다. 이 테스트는 v1→v2→v1 왕복이 손실 없는지, 687 ID가 모두 보존되는지, 레이어 배정이 `coarse-category-plan.json`·대구 staged의 `map_layer_target`과 같은지 확인한다.
- `scripts/map_csv.py`(현재 6개 카테고리만 허용하는 fail-closed 포맷터)는 v2 투영기(`build_mymaps_v2.py`)로 대체한다. 기존 파일은 이력 재현용으로 남긴다.
- 영상 링크 점검: `scripts/check_videos.py`(yt-dlp 메타 또는 API `videos.list`)를 월 1회 루틴으로 돌린다. 실패한 영상은 `check_status`를 갱신하고, 다음 CSV 생성에서 빼고 내보낸다.

## 7. 산출물

- 마이그레이션 스크립트 초안: `/workspace/schema-review/migration/migrate_v2.py`. 오프라인 전용이고, 지도나 GitHub에 접근하지 않는다.
- 샘플 10행(11열, 영상 4건 포함): `/workspace/schema-review/sample-migrated-10.csv`. Food 레이어 표본은 빠져 있다.
- 샘플 v2 정본: `/workspace/schema-review/migration/out-sample/places.v2.json`
- 전체 687행 드라이런 리포트: `/workspace/schema-review/migration/out-full/migration-report.json`. 레이어별 139/149/191/79/129로 실제 지도와 일치하고, 7,557셀, ID 유일. 군 시설 2건은 공개 대상에서 제외됨.
- 영상 후보에서 뽑은 매핑: `/workspace/schema-review/migration/videos.json`

드라이런의 한계:
- `region` 파서는 주소 첫 두 토큰만 본다.
- `practical`은 v1에 근거가 있는 것만 옮겼고, 대부분 `null`이다.
- 주소만 있는 행의 실제 마커 좌표는 아직 KML에서 읽어 오지 않았다.
- 좌표 행과 주소 행을 나눠 쓰는 파일 분할은 아직 구현하지 않았다.

## 8. 소유자에게 물어볼 것

1. 1,818행을 넘기면 지도를 권역별로 나눠도 되나? 아니면 팝업 열을 더 줄여서(예: 8열이면 2,500행) 한 지도를 유지할까? 단, 한 지도는 최대 10,000곳이고 레이어당 2,000곳이다.
2. 팝업 언어: 5개 언어를 모두 팝업에 보일까, 아니면 EN/KO만 보이고 JA/ZH/ES는 짧게 줄일까?
3. 좌표 행과 주소 행이 섞이는 문제: 레이어당 가져오기를 두 번 할까(좌표 파일 + 주소 파일 Add more)? 아니면 모두 주소 기준으로 통일할까? 그러면 좌표 100쌍의 정밀도를 잃는다.
4. Replace all items를 쓰면 레이어가 바뀌는 동안 공개 지도에서 잠깐 비거나 불완전한 상태가 보일 수 있다. 사본 지도 리허설 후 진행해도 되나?
5. USAG Daegu(미군) 채널 영상처럼 "군 관련 공식" 영상을 official로 인정할까?
