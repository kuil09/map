# Humphreys Field Guide — canonical map data

이 저장소는 장소 수집·가공·출처·검증 이력의 기준입니다. **수정은 여기에서 먼저 하고**, 검증된 산출물을 Google My Maps에 반영하며 필요할 때 기존 사이트를 갱신합니다. 기존 공개 URL은 바꾸지 않습니다.

- [기존 가이드](https://humphreys-field-guide.kuil09.chatgpt.site)
- [기존 Google My Maps](https://www.google.com/maps/d/u/0/viewer?mid=1-wHgIPUvxP4PS6YwuxBsMp8luu_amrk)

## V2 데이터 구조 (2026-10-28)

**저장소는 이제 v2 데이터 구조를 표준으로 사용합니다.** 687개 장소가 5개 목적 레이어로 정리되었으며, 통합된 Type 분류 체계와 균일한 CSV 형식을 갖추었습니다.

- **기준 데이터**: `data/v2/places.v2.json` — 전체 장소·출처·다국어·좌표의 정본
- **내보내기 CSV**: `data/v2/exports/*.csv` — Google My Maps 가져오기용 5개 레이어 (11열 통일 형식)
- **검증 상태**: [data/v2/VERIFICATION_STATE.md](data/v2/VERIFICATION_STATE.md) — 687곳 live, 0 unplaced (2026-10-28)
- **마이그레이션 스크립트**: `migration/v2/migrate_v2.py`
- **Type 매핑**: `migration/v2/TYPE-MAP.md` — 87개 → 37개 정규화된 type
- **설계 문서**: [docs/v2-proposal-ko.md](docs/v2-proposal-ko.md)

### V2 주요 변경사항

1. **정규화된 Type 분류**: 기존 87개 type을 37개 lowercase_snake_case type으로 정리
2. **균일한 CSV 구조**: 모든 레이어가 동일한 11열 사용 (이름, 주소, Latitude, Longitude, Type, Region, Guide, Practical, Video, Sources, Record ID)
3. **농다리캠핑장 주소 수정**: 도로명 주소 → 지번 주소 `충청북도 진천군 문백면 평산리 543`
4. **셀 예산 최적화**: 7,557 / 20,000 셀 (37.8% 사용), 최대 1,818행까지 확장 가능

### 내보내기 워크플로

1. `data/v2/places.v2.json`에서 수정 작업
2. `python3 scripts/validate_v2.py` 실행해 검증
3. 필요시 `migration/v2/migrate_v2.py`로 CSV 재생성
4. `data/v2/exports/*.csv` 파일을 Google My Maps에 가져오기



## 현재 공개 사이트 · v38

2026-10-27 19:57:30 UTC에 기존 공개 URL로 재배포했습니다. 기준 데이터 커밋은 `4db2466fd06867cdf8a4fb1c24207a0f1b86d95e`이며 공개 646곳·5개 목적 분류, 군 시설 2곳 제외를 적용했습니다. 다섯 언어의 목적별 건수와 393 CSS px 좁은 화면의 가로 넘침을 확인했습니다. 실제 모바일 기기 시험은 아니며 지도 전체 필드·좌표 재검수는 여전히 부분 상태입니다. [배포·검수 기록](data/history/site-deployment-v38.json)을 참고하세요.

## 현재 공개 지도 · 2026-10-27 19:45:23 UTC 재로드 확인

공개 지도는 **5개 목적 레이어 · 646행 · 위치 표시 639 · 미해결 7**입니다. 목적별 행 수는 음식·카페 127, 자연·캠핑 140, 체험·휴식 185, 쇼핑 74, 문화·관광 120입니다. 646개 표시 이름은 준비된 다섯 CSV와 정확히 일치하며, **16개 내부 하위분류 그룹의 색상·아이콘**이 저장·재로드 후 확인되었습니다. 19:47:25 UTC DOM에는 646개의 서로 다른 현재 UI 식별자가 있습니다. 두 군 시설은 공개 목록에서 제외하고 **기준 원본 648개는 보존**합니다.

**시각적 정리는 완료했지만 전체 동기화 검증 상태는 `partial`입니다.** 전체 Record ID 열·원 필드·현재 숫자 좌표를 최종 내보내기로 대조하지 않았습니다. 두 번의 다운로드 시도에서 접근 가능한 파일을 얻지 못했습니다. 기존 7개 미해결 신원은 이전 복원 영수증에서 이어받고 최종 표시 이름 및 총 오류 수를 확인한 것으로, 행별 오류나 Record ID를 다시 전수 확인한 결과가 아닙니다. 이전 최초 복원 내보내기에서는 명시 좌표 100개 중 6개 동일·94개 소수 여섯 자리 반올림, 최대 약 7.13 cm 차이를 확인했으나 최종 스타일 변경 후 반복한 검사는 아닙니다. 정확한 전체 좌표 보존을 주장하지 않습니다.

최종 작업은 스타일 변경뿐이며 가져오기·행 삭제·원 필드 편집·좌표 변경은 0건입니다. 공개 사이트 배포는 별도 단계입니다. [현재 범위·한계 영수증](data/history/map-restore-current-receipt.json), [최종 DOM 증거](data/history/map-restore-final-dom-20261027.json), [이전 복원 기록](data/history/map-restore-partial-20261027.json)을 보존합니다. 이전 6개·7개 미해결 파일, 추가 이력, 여섯 그룹 원 제안과 기존 정리 제안은 변경하지 않습니다.

## 역사적 append41 기준 데이터 상태 · 2026-10-27 / v38 준비

아래 단락과 표는 복원 전 append41 검증 당시의 기록이며, 현재 지도 수치·레이어·스타일 상태를 뜻하지 않습니다.


| 구분 | 내용 |
|---|---:|
| 기준 장소 / 출처 참조 | 648 / 970 |
| 출처 상태 | verified 911 · unconfirmed 55 · blocked 4 |
| 출처가 있는 일반 지점 / 거리 미측정 | 130 / 518 |
| 저장·재로드 검증 지도 행 / 위치 표시 / 위치 미해결 | 648 / 641 / 7 |
| 지도 추가 대기 | 0 — 재업로드 금지 |
| 기존 지도 원 필드 / 원 Source audit | 607행 / 296개 |
| 정리 적용 / 남은 필드 변경 | 213 / 692 — 재개 전 기록 |
| 실제 사진 라이선스 명세 | 16장 · 32개 사이트 자산 |

**41행은 한 번만 추가되어 저장·재로드 검증이 끝났습니다.** 40개 위치가 표시되었고 Red Button Ansan은 새 미해결 항목입니다. 기존 6개 미해결은 보존됩니다. 원래 607개 이름·레이어, 4,674개 원 필드, 스타일, 100개 명시적 좌표와 501개 주소 locator는 동일했습니다. 다만 501개 주소 기반 마커의 숫자 좌표와 신규 native ID는 노출되지 않았으므로 전체 601개 좌표 보존이나 새 ID 연결을 주장하지 않습니다. [공개 검증 영수증](data/history/map-append41-verified-receipt.json)을 참고하세요.

기존 제목 열은 `U+FEFF + Name`이고 가져온 열은 `Name`이었습니다. 41개 표시 제목을 수정하고 열 개 필드를 각각 재검증했으며 추가 `Name` 열은 남겨 두었습니다. BOM 제거는 인코딩 호환 조치일 뿐 기존 제목 열 연결 문제를 자동 해결하지 않습니다. Source audit 열 삭제와 이번 분류 변경은 모두 0건입니다.

v37은 익산 나바위성당·홍천 수타사·정선 정암사/수마노탑 3곳을 추가합니다. 왕송호수캠핑장은 운영기관 매표소 도로명주소 **왕송못동로 295**를 현재 주소 검색용으로 반영하되 이전 지번을 다섯 언어 참고사항에 보존합니다. 화랑오토캠핑장에는 **2026-11-09~13 배수로 정비 공사**를 기록하며 전체 휴장으로 해석하지 않습니다. 종료된 10월 19~26일 후문 통제는 현재 통제로 표시하지 않습니다. 다섯 장소 모두 좌표·거리 미확인 상태를 유지합니다.

v38은 지도 상태·내보내기 안전장치·분류 **제안**만 준비합니다. 648개 장소 내용, 970개 출처, 좌표·거리, 사진과 기존 지도 수정 대기는 변경하지 않습니다. **현재 공개 사이트는 v37이며 v38은 아직 배포되지 않았습니다.** [v37 게시·검수 기록](data/history/site-deployment-v37.json)을 보존합니다. 기존 35/38/41행 BOM CSV와 성공한 BOM 없는 CSV는 모두 역사 증거이며 **다시 업로드하면 안 됩니다**. 추가 대기가 없으면 생성기는 가져오기 CSV를 만들지 않고 기존 staging CSV를 제거합니다.

[대분류 계획](data/map/coarse-category-plan.json)은 5개 일반 목적과 출입 제한 경고 그룹 1개를 제안합니다. **아직 지도 분류·레이어·사이트 필터에 적용하지 않았습니다.** 기존 출처·주소·지점 수정과 692개 정리 제안도 별도 미적용 상태입니다.

## 사용

Python 3 표준 라이브러리만 필요합니다. 네트워크 호출·지도 업로드·사이트 배포는 자동으로 하지 않습니다.
역사적 바이트 회귀 검증에는 v35·v36·v37 기준 커밋을 포함한 로컬 Git 이력이 필요합니다. 테스트는 누락된 이력을 네트워크에서 자동으로 가져오지 않습니다.

```sh
# V1 검증 (역사 기록)
python scripts/validate.py
python -m unittest discover -s tests -v

# V2 검증 (현재 표준)
python scripts/validate_v2.py

# V1 내보내기 (역사 기록)
python scripts/build_exports.py --out build
python scripts/build_site_data.py --out build/site-data
```

기존 사이트 사진이 있는 빌드 디렉터리로 자산 무결성을 추가 확인할 수 있습니다.

```sh
python scripts/validate.py --asset-root PATH_TO_SITE_BUILD
```

## 구조

### V2 데이터 (현재 표준)

- `data/v2/places.v2.json`: 687개 장소의 정본. schema_version 2, 정규화된 type, 5개 언어 분리, region 구조화.
- `data/v2/exports/*.csv`: Google My Maps 가져오기용 5개 레이어 CSV (균일한 11열 형식).
- `data/v2/VERIFICATION_STATE.md`: 687곳 live, 0 unplaced 검증 상태 (2026-10-28).
- `migration/v2/migrate_v2.py`: V1 → V2 마이그레이션 스크립트.
- `migration/v2/TYPE-MAP.md`: Type 정규화 매핑 (87개 → 37개).
- `scripts/validate_v2.py`: V2 데이터 검증 스크립트.

### V1 데이터 (역사 기록)

- `data/places.json`: 장소 ID, 5개 언어 설명, **완전한 원 주소**, 현재 출처 상태, 좌표·미확인 사항. 역사 기록.
- `data/photos.json`: 실제 사진 출처·저자·라이선스·변경 내용·32개 파일 해시 및 장소 연결. 사진 파일은 기존 사이트에 그대로 둡니다.
- `data/research.json`: 현재 사이트가 읽는 검증 범위·변경 이력·거리 기준·열린 문제. 현재 영업 보증이 아닙니다.
- `data/map/`: 607행 역사적 원 필드, 296개 기존 ID 연결, 현재 7개 미해결(이전 6개 보존), 검증된 추가 이력, 변경 대기 및 불완전한 좌표 증거.
- `data/history/`: 원 Source audit **296개 문자열과 SHA-256**, 적용 변경, 실패 기록, 검증 이력.
- `exports/map-append35-v35.csv`: 35행 역사 증거. 성공한 41행과 겹치므로 재업로드 금지.
- `exports/map-append38-v36.csv`: 38행 역사 증거. 이전 쓰기 0건 실패를 보존하며 재업로드 금지.
- `exports/map-append41-v37.csv`: 원래 BOM 바이트 보존. `map-append41-v37-utf8-no-bom.csv`는 성공한 바이트 증거이며 둘 다 재업로드 금지.
- `data/history/batch19-change-record.json`: 이번 변경·보존 범위와 공개 출처 검토 자료의 해시. 비공개 작업 자료는 포함하지 않습니다.
- `schemas/`, `scripts/`, `tests/`: 계약·결정적 산출물 생성·검증.

[데이터 계약](docs/SCHEMA.md) · [지도/사이트 반영 절차](docs/INTEGRATION.md) · [출처와 보존 한계](docs/PROVENANCE.md) · [권리/사진](docs/RIGHTS.md) · [V2 설계 제안](docs/v2-proposal-ko.md)

`verified`는 기록된 범위의 출처 본문 확인을 뜻하며 현재 영업·입장·예약 가능·외국인 인증·영어 응대를 보증하지 않습니다. 일반 지점은 입구·주차장·접근 가능한 경로가 아닙니다. 반경 값은 공개 비행장 기준점에서의 직선 계획 거리이며 게이트·운전 거리와 다릅니다.
