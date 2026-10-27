# Canonical repository → consumers

## Authority and one-way generation

Collect and process place data in this repository first. `data/places.json`, `data/photos.json`, and `data/research.json` are canonical site inputs; the Site is a generated consumer. Do not independently edit the same JSON in the Site and then overwrite this repository. Commit reviewed canonical changes, run all checks, and record the exact canonical commit in the consuming build.

The existing public Site URL remains `https://humphreys-field-guide.kuil09.chatgpt.site`. This repository does not contain or redeploy its UI. Migration alone changes neither that public URL nor the Google map.

## Site build

```sh
python scripts/validate.py --asset-root PATH_TO_EXISTING_SITE_BUILD
python scripts/build_site_data.py --out build/site-data
```

The output contains the three exact canonical JSON files and `canonical-input-manifest.json` with input hashes, source snapshot and the canonical Git commit only when the data working tree is clean. Dirty builds expose the observed HEAD separately, leave canonicalCommit null, and identify the actual bytes by hashes. Copy them into the existing Site's data-serving directory through that Site's supported release workflow. Keep its HTML/CSS/JS and the 32 existing licensed `photos/...` files. Run the existing Site tests and verify deployed JSON hashes after a specifically authorized release. Never claim a Site deployment because this generator succeeded.

`--out` must be a staging directory, not the live Site source or public serving directory. The script never publishes or edits the existing site. Existing assets must pass the optional `--asset-root` check before release. Missing assets require restoration of the exact licensed files; do not regenerate them or downgrade photo attribution.

## Google My Maps append

The pending append queue is **empty**. The 41 rows were added once and verified after save/reload; current receipt-backed totals are **648 rows / 641 positioned / 7 unresolved**. The historical 35-, 38- and 41-row files overlap this completed operation and **must not be uploaded again**. `currentAppendFile` is null; `verified-import-history.json` carries all eight completed cohorts, while `identity-index.json` retains the unchanged historical 607-member evidence. New native IDs are unknown, not inferred.

`build_exports.py --out build` emits no append CSV or rows artifact when there are no pending IDs. It removes its own stale `map-append-current.csv` and `.rows.json` from that staging directory, and writes `importable:false`, `uploadAuthorized:false` and `appendStatus:no_pending_rows_do_not_upload` in the manifest. A header-only CSV is never an upload candidate. Historical reconstruction and source-point reference outputs remain non-import backups/references, not native geometry.

The named v35, v36 and v37 CSVs retain their original BOM-bearing bytes and hashes. `exports/map-append41-v37-utf8-no-bom.csv` separately retains the successful 151,463-byte import evidence: only the initial UTF-8 BOM was removed, and every one of 410 data cells and all ten headers is equivalent. All four files are evidence, not future candidates. New nonempty staging CSVs use BOM-free UTF-8, unchanged quoted fields/CRLF records/five-language text; `csv_bytes(..., include_bom=True)` exists only for historical reproduction.

**Encoding compatibility is not destination-schema compatibility.** The destination's display-title column is literally `U+FEFF + Name`, distinct from `Name`. The accepted BOM-free import introduced a separate `Name` column; all 41 displayed titles then needed repair. The receipt verifies the repaired titles and all ten fields per new row after reload; the extra `Name` column remains. Do not normalize exact column code points, assume accepted import means correct displayed titles, delete columns, or re-upload saved rows to fix a title binding. Inspect actual destination schema and title binding before any separately authorized future append.

The 607 earlier names/layers, 4,674 original field values and existing styles were unchanged. Evidence confirms 100 explicit geometries and 501 address locators unchanged, **not all 601 numeric pin coordinates**. The 501 address-geocoded pin coordinates and new native IDs were not exposed. The original six unresolved listings remain, with Red Button Ansan added as the seventh. Map-description count clauses were saved/reloaded as 648/641/7 at 2026-10-27T07:45:51.523Z, with all other description text, all 648 Placemarks and styles unchanged. Exact original append save-click time was not captured.

The Wangsong address correction, Hwarang maintenance note and all existing source/address/point update queues remain separate and unapplied. The 692 historical cleanup proposals and 213 completed historical edits are untouched; no Source audit column was deleted. Seven physical layers remain. `data/map/coarse-category-plan.json` is **proposed_not_applied**; this release does not change canonical categories, live map classifications, physical layers or Site filters.

Canonical **v38 is prepared, not Site-deployed**. The latest published Site is **v37**, recorded in immutable `data/history/site-deployment-v37.json`. That historical publication receipt truthfully retains the map counts known when v37 shipped. `sourceSiteCommit` still identifies the original v35 migration source. A separately authorized v38 consumer release must refresh cache versions, verify all three deployed JSON hashes and all 32 photo assets, and record publication evidence without overwriting prior receipts.

Before any map write:

1. Read the current map's inventory and exact destination column code points/display-title binding. Reconcile against the 648 receipt-backed imported place IDs and historical 607 native identities; do not invent the 41 new native IDs or assume old evidence is fresh.
2. Check all pending IDs and names against the current map. Verify full source addresses and source evidence; preserve all uncertainty.
3. Use **append/add rows only** in the authorized existing destination layer. Do not use replace/match/update against the 607 old rows and do not create/delete layers or fields as a side effect.
4. Use the full Address field for geocoding; Name for the label. The file has no coordinate columns and no Source audit column. General source point text is not an instruction to move existing markers. Any newly positioned result is address-geocoded, not a verified entrance.
5. Categories are English-first bilingual existing values. `Activities / 체험` is intentionally retained where compatibility requires it; this append does not finish display-category normalization or purpose-layer consolidation.
6. After save **and reload**, read back each new Record ID and all fields, separately verify its displayed title, check position/unresolved counts, and verify that all existing identities, full addresses, source URLs, geometry and styles were preserved to the extent actually observable. Record scope and limits. Do not claim full geometry preservation without full geometry evidence.
7. Update sync-state only from verified results. Uncertain writes must be inspected before retry; a denied action must not be retried without materially new authority/evidence. Keep source/status/coordinate correction queues separate from row membership.

## Existing metadata cleanup

`pending-field-edits692.json` is a historical proposal list, **not an executable patch**. Check current value for exact native ID and field; if it differs from `before`, stop and reconcile. Do not replay the 213 completed keys. Preserve the 296 original audit strings before any explicitly authorized clearing/deletion. This repository's existence does not itself authorize deleting columns, normalizing addresses, merging layers, recreating features, or replacing the map.

## Verified consolidation trial — not applied

The 2026-10-27 supported-UI consolidation trial moved zero features. Temporary styles were restored; final reload preserved 648 rows, 641 positioned and seven unresolved. Two empty numeric Latitude/Longitude preparation columns remain in the 41-row Pilgrimage & sports layer. See [trial evidence](../data/history/legend-consolidation-trial-20261027.json).

A current DOM-ID snapshot exposed 648 IDs, but 227 differ from the historical baseline and the cause is unknown. Fresh IDs were not rechecked after the final reload because the extension disconnected. Do not overwrite historical identity evidence or reuse old joins without exact current verification. All eight conditional historical name/address aliases were verified for this trial only; no address was normalized or re-geocoded. Native and extension dragging produced no layer membership change. Do not repeat identical attempts or claim physical consolidation.
