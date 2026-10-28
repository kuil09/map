# 8-column migration plan (prepared 2026-10-28, live map NOT edited)

Source: kuil09/map main @ e84f71a, data/v2/exports/*.csv (11 columns).
Counts: Culture 370, Nature 372, Food 343, Activities 314, Shopping 166 = 1,565.

## Column mapping (11 -> 8)
| New column | From | Notes |
|---|---|---|
| 이름 | 이름 | unchanged (English \| Korean) |
| 주소 | 주소 | unchanged; placement column |
| Type | Type | unchanged; style column |
| Guide | Guide | unchanged; EN/KO/JA/ZH/ES lines |
| Details | Region + Latitude/Longitude + Practical | "Region: …" line, then "Coordinates (reference only, from source): lat, lon" only when the source row had them (100 rows), then Practical text verbatim |
| Video | Video | unchanged |
| Sources | Sources | unchanged (source + official links + Checked date) |
| Record ID | Record ID | unchanged; stable key for future merges |

Dropped as separate columns: Latitude, Longitude, Region (content kept in Details).

## Cell math
- Now: 1,565 x 11 = 17,215 / 20,000.
- After: 1,565 x 8 = 12,520 / 20,000 (7,480 free).
- Max rows at 8 cols: 20,000 / 8 = 2,500 -> about 935 more places.
- (Optional later: folding Record ID into Details -> 7 cols = 2,857 rows.)

## Validation (build.py)
- Row counts identical per layer; total 1,565.
- 0 rows with empty 주소.
- 이름, 주소, Type, Guide, Video, Sources, Record ID byte-identical to source.
- Region, Practical, Latitude, Longitude strings all found inside Details for every row.
- Longest cell 1,675 chars.

## Risks
1. Placement: 100 rows carried Lat/Lon (Nature 76, Activities 17, Culture 6, Food 1). The live layers are placed by 주소; after replace they will be geocoded from 주소 only. Check these 100 pins after import (the coordinates stay in Details for comparison).
2. "Replace all items" must keep 이름 as title, 주소 as position, Type as style; confirm the mapping dialog per layer. Imports can silently do nothing or 429; retry once and verify legend counts.
3. Popup field rename: Practical/Region no longer appear as their own popup fields; content shows under Details.
4. Do one layer at a time, serially; back up current exports (already in repo at e84f71a) before replacing.
5. Repo exports/schema must be updated to 8 columns after the live switch so future appends use the same header.
