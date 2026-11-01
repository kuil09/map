# Korea Local Guide / 외국인을 위한 한국 생활·여행 가이드

A curated Google My Maps guide of places in South Korea for foreigners living in or staying long-term in the country.

**[View the map](https://www.google.com/maps/d/viewer?mid=1-wHgIPUvxP4PS6YwuxBsMp8luu_amrk)**

## Overview

This repository maintains the data for **Korea Local Guide**, a Google My Maps layer set covering places of interest for English-speaking expats, military personnel, and long-term visitors in South Korea. The guide emphasizes sourced, multilingual descriptions and practical details.

### Current Coverage

- **2,312 places** across 5 categories
- **Culture & Sights**: 624 places
- **Nature & Camping**: 501 places
- **Food & Drink**: 563 places
- **Activities & Wellness**: 386 places
- **Shopping**: 238 places

Coverage started around **Camp Humphreys (Pyeongtaek)** and **Daegu/Camp Walker**, and has expanded to include Busan, Gyeongju, Andong, Seoul, Incheon, Jeju, and other regions. **This is not nationwide-complete** — many areas remain unrepresented.

### Data Sources

- **Korea Tourism Organization (KTO)**: TourAPI open data and VisitKorea listings
- **Official local government tourism sites**: Regional tourism boards and municipal sources
- **Military community sources**: USAG official channels (videos only)
- **Collection method**: AI-assisted data gathering with human cross-checking and source verification

Videos are limited to official channels only. Internal verification notes and process metadata are stored in the source data but excluded from public map popups.

## Map Details

### Columns (8-column format)

Each layer exports to CSV with these columns:

1. **이름** (Name): English | Korean
2. **주소** (Address): Korean address
3. **Type**: Lowercase snake_case category (e.g. `theme_park`, `seafood`, `hiking_trail`)
4. **Guide**: Multilingual descriptions (EN / KO / JA / ZH / ES)
5. **Details**: User-facing notes and practical information
6. **Video**: Official video links with channel attribution
7. **Sources**: Up to 3 source URLs
8. **Record ID**: Unique place identifier (join key to `places.v2.json`)

### Technical Constraints

- **Google My Maps limit**: ~20,000 cells total
- **Current utilization**: 18,496 cells (92.5%)
- **Remaining capacity**: ~183 rows
- **Encoding**: UTF-8 without BOM (BOM breaks My Maps title column detection)
- **Pinning**: Places are pinned by Korean address

### Multilingual Support

- **Names**: English first, then Korean (e.g. `Everland | 에버랜드`)
- **Descriptions**: Available in English, Korean, Japanese, Chinese (Simplified), and Spanish
- **Address**: Korean only (as provided by sources)

**Note on address prefixes**: For 47 Jeonnam/Gwangju rows (IDs in `quality/2026-11-01/map-legacy-address-ids.json`) and Horyonggoksan, the My Maps CSV deliberately keeps the old address prefix (`전라남도` / `광주광역시`, and Incheon `중구` for Horyonggoksan) because Google cannot yet geocode the new official names. `places.v2.json` holds the official new address (`전남광주통합특별시` for those Jeonnam/Gwangju places).

## Repository Structure

```
data/v2/
  places.v2.json          # Source of truth: 2,312 places, full nested schema
  exports/                # 8-column CSV exports per layer (UTF-8 no BOM)
    culture_sights.csv
    food_drink.csv
    nature_camping.csv
    activities_wellness.csv
    shopping.csv
    manifest.json

scripts/
  export_v2_8col.py       # Generate 8-column CSV exports from places.v2.json
  validate_v2.py          # Validate schema, counts, and export consistency

tests/
  test_v2.py              # Unit tests for schema and layer distribution
  test_export_quality.py  # Enforce UTF-8 without BOM, proper encoding

docs/                     # Batch documentation and quality reports
quality/                  # Quality-pass files and cleaned data snapshots
```

## Data Quality

The November 2026 quality pass (building on October 2026) applied ~293 cell fixes and removed 15 places:

**October 2026** (initial cleanup):
- 7,937 redundant/internal sentences dropped
- 4,731 Korean duplicate sentences removed
- 62 internal-text guides rewritten as sourced content
- 50 generic guides rewritten with proper sourcing
- 37 unsourced superlatives softened
- 3,241 URLs checked; dead links replaced, concatenated URLs split

**November 2026** (quality3):
- ~293 cell fixes over two passes: video-cell prefix cleanup, leaked internal notes removed, name typos fixed
- Incheon/Hwaseong gu name updates applied
- 140 Jeonnam/Gwangju places updated with the official `전남광주통합특별시` address prefix in JSON; 47 of those rows plus Horyonggoksan keep the old prefix in the My Maps CSV because Google cannot geocode the new names yet (see `quality/2026-11-01/map-legacy-address-ids.json`)
- 15 places removed: 5 likely closed, 10 with dead-only sources (see `quality/2026-11-01/removed.json`)

Internal metadata (region lines, reference coordinates, check dates, process notes) is preserved in `legacy.popup_cleanup_2026_10_28` within `places.v2.json` but excluded from CSV exports. Quality-pass documentation is in `quality/2026-11-01/`.

## Usage

### Validate Data

```bash
python3 -B scripts/validate_v2.py
```

Checks:
- Schema compliance
- Unique Record IDs
- Guide content present in at least one language
- Type values are lowercase snake_case
- CSV consistency with `places.v2.json`

### Regenerate Exports

```bash
python3 -B scripts/export_v2_8col.py
```

Generates UTF-8 (no BOM) CSVs in `data/v2/exports/` from `places.v2.json`. **Important**: Future exports automatically exclude internal notes from popup fields.

### Run Tests

```bash
python3 -B -m unittest discover tests -v
```

Tests validate:
- Total place count (2,312)
- Layer distribution
- Schema version consistency
- Export quality (no BOM, valid UTF-8)
- CSV/JSON consistency

## Contributing

This is a personal project. The data is maintained primarily for the Google My Maps guide. External contributions are not currently accepted, but issues reporting dead links or incorrect information are welcome.

## License

Data is collected from public tourism sources and is provided as-is. No commercial use. The guide is intended for personal, non-commercial use by the expat and military community in South Korea.

## Discontinued

The website deployment and business infrastructure previously associated with this project have been discontinued. Website code remains in the repository for historical reference but is no longer maintained or deployed.

---

**Map Viewer**: https://www.google.com/maps/d/viewer?mid=1-wHgIPUvxP4PS6YwuxBsMp8luu_amrk
