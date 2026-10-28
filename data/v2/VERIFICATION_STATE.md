# V2 Data Verification State

**Date**: 2026-10-28  
**Status**: Live  
**Total Places**: 1,565  
**Unplaced**: 0 known  

## Latest Update: 8-Column Migration (2026-10-28)

Migrated My Maps exports to 8-column format, consolidating Region + reference coordinates + Practical into a single Details column. Total places remain at 1,565 with 0 unplaced.

### Update Details
- **Export format**: Migrated from 11 columns to 8 columns
- **New columns**: 이름, 주소, Type, Guide, Details, Video, Sources, Record ID
- **Details column**: Combines Region + reference coordinates (100 places) + Practical information
- **Places unchanged**: 1,565 total (Culture 370, Nature 372, Food 343, Activities 314, Shopping 166)
- **Capacity improvement**: Cell usage reduced from 86.1% to 62.6%, enabling ~935 more places

## Layer Distribution

| Layer | Count | Change | File |
|---|---:|---:|---|
| Shopping (쇼핑) | 166 | +15 | shopping.csv |
| Culture & Sights (문화·관광) | 370 | +55 | culture_sights.csv |
| Food & Drink (음식·카페) | 343 | +39 | food_drink.csv |
| Nature & Camping (자연·캠핑) | 372 | +30 | nature_camping.csv |
| Activities & Wellness (체험·휴식) | 314 | +12 | activities_wellness.csv |
| **Total** | **1,565** | **+151** | |

## Data Quality

- ✓ 1,565 unique Record IDs
- ✓ All places have Guide content (description in at least one language)
- ✓ All Type values use lowercase_snake_case format
- ✓ CSV columns: 이름, 주소, Type, Guide, Details, Video, Sources, Record ID (8 columns)
- ✓ All CSVs are consistent with places.v2.json
- ✓ Details column preserves Region, coordinates (100 places), and Practical information

## Regional Coverage

- **Initial (v1)**: Central region (Gyeonggi, Chungcheong)
- **Gyeongbuk (2026-10-28)**: +126 places (경상북도)
- **Busan & Gyeongnam (2026-10-28)**: +150 places (부산광역시, 경상남도)
- **Gyeongbuk forests confirmed (2026-10-28)**: +4 recreational forests with campsites
- **Gangwon (2026-10-28)**: +147 places (강원도)
- **Jeolla (2026-10-28)**: +150 places (광주광역시, 전라남도, 전북특별자치도)
- **Jeju (2026-10-28)**: +150 places (제주특별자치도)
- **Seoul/Incheon (2026-10-28)**: +151 places (서울특별시, 인천광역시)

## Cell Budget & Capacity

- **Current**: 12,520 / 20,000 cells (62.6% utilization)
- **Row capacity**: 2,500 rows maximum (with 8 columns)
- **Current usage**: 1,565 rows (62.6% of capacity)
- **Remaining capacity**: 935 rows available for expansion
- **Migration benefit**: Reduced from 17,215 cells (11 columns) to 12,520 cells (8 columns)

## Key Changes Summary

**8-Column Migration (2026-10-28):**
1. Consolidated export format from 11 columns to 8 columns
2. Details column now combines Region, reference coordinates, and Practical information
3. Reduced cell usage from 17,215 to 12,520 (freed 4,695 cells)
4. Increased maximum capacity from 1,818 to 2,500 rows
5. Canonical data in places.v2.json remains unchanged

**Seoul/Incheon Integration (2026-10-28):**
1. Added 151 places from Seoul and Incheon metropolitan areas
2. All new places use v2 format with 5-language descriptions

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

The v2 export CSVs in `data/v2/exports/` are ready for Google My Maps import (8-column format):

1. **Column structure**: 이름, 주소, Type, Guide, Details, Video, Sources, Record ID
2. **Placement column**: 주소 (Address) for geocoding
3. **Style column**: Type (lowercase_snake_case format)
4. **Details column**: Combined Region + reference coordinates + Practical information
5. **Import order**: Recommended to start with smallest layer for testing

Export generator: `scripts/export_v2_8col.py`  
See `data/v2/exports/manifest.json` for detailed file metadata.  
Migration plan: `docs/eight-column-2026-10/PLAN.md`

## Documentation

- **8-column migration plan**: docs/eight-column-2026-10/PLAN.md
- **Seoul/Incheon report**: docs/seoul-incheon-2026-10/REPORT.md
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
