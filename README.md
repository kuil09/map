# Humphreys Field Guide — canonical map data

이 저장소는 장소 수집·가공·출처·검증 이력의 기준입니다. **수정은 여기에서 먼저 하고**, 검증된 산출물을 Google My Maps에 반영하며 필요할 때 기존 사이트를 갱신합니다. 기존 공개 URL은 바꾸지 않습니다.

- [기존 가이드](https://humphreys-field-guide.kuil09.chatgpt.site)
- [기존 Google My Maps](https://www.google.com/maps/d/u/0/viewer?mid=1-wHgIPUvxP4PS6YwuxBsMp8luu_amrk)

## 기준 데이터 상태 · 2026-10-27 / v36

| 구분 | 내용 |
|---|---:|
| 기준 장소 / 출처 참조 | 645 / 960 |
| 출처 상태 | verified 901 · unconfirmed 55 · blocked 4 |
| 출처가 있는 일반 지점 / 거리 미측정 | 130 / 515 |
| 마지막 영수증 기준 지도 행 / 위치 표시 / 위치 미해결 | 607 / 601 / 6 |
| 지도 추가 대기 | 38 |
| 기존 지도 원 필드 / 원 Source audit | 607행 / 296개 |
| 정리 적용 / 남은 필드 변경 | 213 / 692 — 재개 전 기록 |
| 실제 사진 라이선스 명세 | 16장 · 32개 사이트 자산 |

**완전한 601개 마커 지오메트리 백업은 없습니다.** 지도 행 수는 저장·재로드 기록에 근거하며 이 저장소 생성 중 새로 전체 조회한 결과가 아닙니다. 35행 CSV 업로드 시도는 파일 선택 전 브라우저 오류로 중단되었고 업로드·쓰기 0건입니다. 기존 607행 교체용 파일이 아닙니다.

v36은 광천전통시장·이성당·빈해원 3곳을 추가하고, 기존 온양온천시장·청주 육거리종합시장·용인중앙시장에 일반 목적지 지점을 기록합니다. 기존 956개 출처 객체와 원래 311개 장소, 사진과 역사 자료는 보존됩니다. 같은 공개 사이트에는 2026-10-27 06:24 UTC에 배포했으며, 구글 지도에는 아직 반영되지 않았습니다. [게시·검수 범위](data/history/site-deployment-v36.json)를 참고하세요. 기존 35행 파일은 그대로 보존하고 38행 추가 후보를 별도로 제공합니다.

## 사용

Python 3 표준 라이브러리만 필요합니다. 네트워크 호출·지도 업로드·사이트 배포는 자동으로 하지 않습니다.
역사적 바이트 회귀 검증에는 v35 기준 커밋을 포함한 로컬 Git 이력이 필요합니다. 테스트는 누락된 이력을 네트워크에서 자동으로 가져오지 않습니다.

```sh
python scripts/validate.py
python -m unittest discover -s tests -v
python scripts/build_exports.py --out build
python scripts/build_site_data.py --out build/site-data
```

기존 사이트 사진이 있는 빌드 디렉터리로 자산 무결성을 추가 확인할 수 있습니다.

```sh
python scripts/validate.py --asset-root PATH_TO_SITE_BUILD
```

## 구조

- `data/places.json`: 장소 ID, 5개 언어 설명, **완전한 원 주소**, 현재 출처 상태, 좌표·미확인 사항. 앞으로의 편집 기준.
- `data/photos.json`: 실제 사진 출처·저자·라이선스·변경 내용·32개 파일 해시 및 장소 연결. 사진 파일은 기존 사이트에 그대로 둡니다.
- `data/research.json`: 현재 사이트가 읽는 검증 범위·변경 이력·거리 기준·열린 문제. 현재 영업 보증이 아닙니다.
- `data/map/`: 607행 역사적 원 필드, 정확한 ID 연결, 6개 미해결, 변경 대기 및 불완전한 좌표 증거.
- `data/history/`: 원 Source audit **296개 문자열과 SHA-256**, 적용 변경, 실패 기록, 검증 이력.
- `exports/map-append35-v35.csv`: 검토된 35행 **주소 기반 추가 전용** 파일. 좌표 열과 Source audit 열 없음.
- `exports/map-append38-v36.csv`: 현재 38행 **주소 기반 추가 후보**. 업로드되지 않았으며 기존 35행 파일과 별개입니다.
- `data/history/batch18-change-record.json`: 이번 변경·보존 범위와 공개 출처 검토 자료의 해시. 비공개 작업 자료는 포함하지 않습니다.
- `schemas/`, `scripts/`, `tests/`: 계약·결정적 산출물 생성·검증.

[데이터 계약](docs/SCHEMA.md) · [지도/사이트 반영 절차](docs/INTEGRATION.md) · [출처와 보존 한계](docs/PROVENANCE.md) · [권리/사진](docs/RIGHTS.md)

`verified`는 기록된 범위의 출처 본문 확인을 뜻하며 현재 영업·입장·예약 가능·외국인 인증·영어 응대를 보증하지 않습니다. 일반 지점은 입구·주차장·접근 가능한 경로가 아닙니다. 반경 값은 공개 비행장 기준점에서의 직선 계획 거리이며 게이트·운전 거리와 다릅니다.
