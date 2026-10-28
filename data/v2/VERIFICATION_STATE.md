# V2 Data Verification State

**Date**: 2026-10-28  
**Status**: Live  
**Total Places**: 1,414  
**Unplaced**: 0 known  

## Latest Update: Jeju Addition (2026-10-28)

Added 150 new places from Jeju (제주특별자치도), bringing the total from 1,264 to 1,414.

### Update Details
- **New places**: 150 (Shopping 6, Culture 38, Food 35, Nature 51, Activities 20)
- **Total added**: 150 places from Jeju
- **Note**: Jeju official videos are pending due to YouTube API quota exhaustion during data collection

## Layer Distribution

| Layer | Count | Change | File |
|---|---:|---:|---|
| Shopping (쇼핑) | 151 | +6 | shopping.csv |
| Culture & Sights (문화·관광) | 315 | +38 | culture_sights.csv |
| Food & Drink (음식·카페) | 304 | +35 | food_drink.csv |
| Nature & Camping (자연·캠핑) | 342 | +51 | nature_camping.csv |
| Activities & Wellness (체험·휴식) | 302 | +20 | activities_wellness.csv |
| **Total** | **1,414** | **+150** | |

## Data Quality

- ✓ 1,414 unique Record IDs
- ✓ All places have Guide content (description in at least one language)
- ✓ All Type values use lowercase_snake_case format
- ✓ CSV columns match specification: 이름, 주소, Latitude, Longitude, Type, Region, Guide, Practical, Video, Sources, Record ID
- ✓ All CSVs are consistent with places.v2.json

## Regional Coverage

- **Initial (v1)**: Central region (Gyeonggi, Chungcheong)
- **Gyeongbuk (2026-10-28)**: +126 places (경상북도)
- **Busan & Gyeongnam (2026-10-28)**: +150 places (부산광역시, 경상남도)
- **Gyeongbuk forests confirmed (2026-10-28)**: +4 recreational forests with campsites
- **Gangwon (2026-10-28)**: +147 places (강원도)
- **Jeolla (2026-10-28)**: +150 places (광주광역시, 전라남도, 전북특별자치도)
- **Jeju (2026-10-28)**: +150 places (제주특별자치도)

## Cell Budget & Capacity

- **Current**: 15,554 / 20,000 cells (77.8% utilization)
- **Row usage**: 1,414 / 1,800 (78.6% of recommended threshold)
- **Maximum capacity**: 1,818 rows (with 11 columns)
- **Remaining capacity**: 404 rows available for expansion

## Key Changes Summary

**Jeju Integration (2026-10-28):**
1. Added 150 places from Jeju region
2. All new places use v2 format with 5-language descriptions
3. Official videos pending due to YouTube API quota exhaustion

**Jeolla Integration (2026-10-28):**
1. Added 150 places from Jeolla region (Gwangju, Jeonnam, Jeonbuk)
2. All new places use v2 format with 5-language descriptions
3. Address fix: Gwangju/Jeonnam addresses use 광주광역시 and 전라남도 instead of 전남광주통합특별시 (which caused 38 unplaced rows due to My Maps geocoding failure)

**Gangwon Integration (2026-10-28):**
1. Added 147 places from Gangwon region
2. All new places use v2 format with 5-language descriptions

**Busan & Gyeongnam Integration (2026-10-28):**
1. Added 150 places from Busan and Gyeongnam regions
2. Confirmed and added 4 Gyeongbuk recreational forests with camping
3. All new places use v2 format with 5-language descriptions
4. 10 restaurants spot-checked for current operation
5. 10 places with official video attachments (VISIT BUSAN, city channels)

**Gyeongbuk Integration (2026-10-28):**
1. Added 126 places from Gyeongbuk region
2. Applied 7 pin corrections for improved location accuracy
3. 4 recreational forests initially held pending confirmation

**Initial V2 (687 places):**
1. Normalized Type Taxonomy: 87 distinct types → 37 normalized types
2. 농다리캠핑장 Address: Updated to lot address
3. Uniform CSV Structure: All layers use identical 11-column format

## Export Workflow

The v2 export CSVs in `data/v2/exports/` are ready for Google My Maps import:

1. **Coordinate-based entries**: Use Latitude/Longitude columns
2. **Address-based entries**: Use 주소 (Address) column for geocoding
3. **Import order**: Recommended to start with smallest layer for testing

See `data/v2/exports/manifest.json` for detailed file metadata.

## Documentation

- **Jeju report**: docs/jeju-2026-10/REPORT.md
- **Jeolla report**: docs/jeolla-2026-10/REPORT.md
- **Gangwon report**: docs/gangwon-2026-10/REPORT.md
- **Busan & Gyeongnam report**: docs/busan-gyeongnam-2026-10/REPORT.md
- **Gyeongbuk addition report**: docs/gyeongbuk-2026-10/REPORT.md
- **Gyeongbuk pin corrections**: docs/gyeongbuk-2026-10/FIX.md
- **V2 design specification**: docs/v2-proposal-ko.md
- **Type mapping**: migration/v2/TYPE-MAP.md

## Special Cases & Notes

### Confirmed Recreational Forests
The 4 Gyeongbuk recreational forests are now confirmed to have campsites (2026-10-28):
- Tohamsan National Recreational Forest (camping-gb-gyeongju-tohamsan-national-recreational-forest)
- Geommasan National Recreational Forest (camping-gb-yeongyang-geommasan-national-recreational-forest)
- Unmunsan National Recreational Forest (camping-gb-cheongdo-unmunsan-national-recreational-forest)
- Cheongoksan National Recreational Forest (camping-gb-bonghwa-cheongoksan-national-recreational-forest)

### Address Precision Notes (Busan & Gyeongnam)
- **Underground shopping areas**: 3 places use underground road numbers (지하) which may geocode to entrances
- **Mountain lot**: 거제 해금강 uses 산1 (mountain lot) pointing to islets rather than boat terminal
- **Lot addresses**: 11 places use jibeon addresses without road names
- See docs/busan-gyeongnam-2026-10/REPORT.md for complete list

### Previous Special Cases
- **삼선암 (Samseonam Rocks)**: Remains at village level (경상북도 울릉군 북면 천부리)
- **9 Gyeongbuk places**: Have only village- or road-level addresses without lot numbers
