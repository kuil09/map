# V2 Data Verification State

**Date**: 2026-10-28  
**Status**: Live  
**Total Places**: 687  
**Unplaced**: 0  

## Layer Distribution

| Layer | Count | File |
|---|---:|---|
| Food & Drink (음식·카페) | 139 | food_drink.csv |
| Nature & Camping (자연·캠핑) | 149 | nature_camping.csv |
| Activities & Wellness (체험·휴식) | 191 | activities_wellness.csv |
| Shopping (쇼핑) | 79 | shopping.csv |
| Culture & Sights (문화·관광) | 129 | culture_sights.csv |
| **Total** | **687** | |

## Data Quality

- ✓ 687 unique Record IDs
- ✓ All places have Guide content (description in at least one language)
- ✓ All Type values use lowercase_snake_case format
- ✓ CSV columns match specification: 이름, 주소, Latitude, Longitude, Type, Region, Guide, Practical, Video, Sources, Record ID
- ✓ All CSVs are consistent with places.v2.json

## Key Changes from V1

1. **Normalized Type Taxonomy**: 87 distinct types consolidated into 37 normalized types across 5 layers
2. **농다리캠핑장 Address**: Updated to use lot address `충청북도 진천군 문백면 평산리 543` (from `충청북도 진천군 문백면 평산3길 35`)
3. **Uniform CSV Structure**: All layers now use identical 11-column format
4. **Cell Budget**: 7,557 / 20,000 cells (37.8% utilization), allowing expansion to 1,818 total rows

## Migration Notes

- Migration completed: 2026-10-28
- Source: proposal-ko.md design specification
- Script: migration/v2/migrate_v2.py
- Type mapping: migration/v2/TYPE-MAP.md
- Validation: scripts/validate_v2.py

## Export Workflow

The v2 export CSVs in `data/v2/exports/` are ready for Google My Maps import:

1. **Coordinate-based entries**: Use Latitude/Longitude columns
2. **Address-based entries**: Use 주소 (Address) column for geocoding
3. **Import order**: Recommended to start with smallest layer (Shopping, 79 rows) for testing

See `data/v2/exports/manifest.json` for detailed file metadata and SHA-256 checksums.
