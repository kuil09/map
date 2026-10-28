# V2 Data Verification State

**Date**: 2026-10-28  
**Status**: Live  
**Total Places**: 813  
**Unplaced**: 0 known  

## Latest Update: Gyeongbuk Addition (2026-10-28)

Added 126 new Gyeongbuk (경상북도) places to the map, bringing the total from 687 to 813.

### Update Details
- **New places**: 126 (Shopping 21, Culture 32, Food 25, Nature 24, Activities 24)
- **Held back**: 4 recreational forests (휴양림) pending confirmation
- **Pin corrections**: 7 places received updated addresses (see docs/gyeongbuk-2026-10/FIX.md)
- **Special case**: 삼선암 (Samseonam Rocks) remains pinned at village level (천부리)

## Layer Distribution

| Layer | Count | Change | File |
|---|---:|---:|---|
| Shopping (쇼핑) | 100 | +21 | shopping.csv |
| Culture & Sights (문화·관광) | 161 | +32 | culture_sights.csv |
| Food & Drink (음식·카페) | 164 | +25 | food_drink.csv |
| Nature & Camping (자연·캠핑) | 173 | +24 | nature_camping.csv |
| Activities & Wellness (체험·휴식) | 215 | +24 | activities_wellness.csv |
| **Total** | **813** | **+126** | |

## Data Quality

- ✓ 813 unique Record IDs
- ✓ All places have Guide content (description in at least one language)
- ✓ All Type values use lowercase_snake_case format
- ✓ CSV columns match specification: 이름, 주소, Latitude, Longitude, Type, Region, Guide, Practical, Video, Sources, Record ID
- ✓ All CSVs are consistent with places.v2.json

## Key Changes from Initial V2 (687 places)

**Gyeongbuk Integration (2026-10-28):**
1. Added 126 places from Gyeongbuk region
2. Applied 7 pin corrections for improved location accuracy
3. 4 recreational forests held pending campsite confirmation
4. All new places use v2 format with 5-language descriptions

**Initial V2 (687 places):**
1. **Normalized Type Taxonomy**: 87 distinct types consolidated into 37 normalized types across 5 layers
2. **농다리캠핑장 Address**: Updated to use lot address `충청북도 진천군 문백면 평산리 543`
3. **Uniform CSV Structure**: All layers use identical 11-column format
4. **Cell Budget**: Initially 7,557 / 20,000 cells (37.8%), now 8,943 / 20,000 (44.7%)

## Cell Budget & Capacity

- **Current**: 8,943 / 20,000 cells (44.7% utilization)
- **Maximum capacity**: 1,818 rows (with 11 columns)
- **Remaining capacity**: 1,005 rows available for expansion

## Export Workflow

The v2 export CSVs in `data/v2/exports/` are ready for Google My Maps import:

1. **Coordinate-based entries**: Use Latitude/Longitude columns
2. **Address-based entries**: Use 주소 (Address) column for geocoding
3. **Import order**: Recommended to start with smallest layer (Shopping, 100 rows) for testing

See `data/v2/exports/manifest.json` for detailed file metadata.

## Documentation

- **Gyeongbuk addition report**: docs/gyeongbuk-2026-10/REPORT.md
- **Pin corrections**: docs/gyeongbuk-2026-10/FIX.md
- **V2 design specification**: docs/v2-proposal-ko.md
- **Type mapping**: migration/v2/TYPE-MAP.md

## Notes

- **Held places**: 4 recreational forests (Tohamsan, Geommasan, Unmunsan, Cheongoksan) are held pending confirmation that they operate campsites. They are NOT included in the 813 count.
- **Village-level pin**: 삼선암 (Samseonam Rocks, scenery-gb-ulleung-samseonam-rocks) is pinned at village level (경상북도 울릉군 북면 천부리) as no specific viewpoint/parking address was found.
- **Geocoding accuracy**: 9 Gyeongbuk places have only village- or road-level addresses without lot numbers. Verify their geocoded positions after import.
