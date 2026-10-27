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

`exports/map-append35-v35.csv` is the reviewed, immutable v35 append artifact. Its hash is in `data/map/sync-state.json`; never replace that named historical artifact with a future export. `scripts/build_exports.py --out build` produces a current append candidate from the ordered `pendingAppendPlaceIds` and canonical places, plus explicitly historical reconstruction and coordinate-reference outputs. Generated output is not a write authorization.

For canonical v37, `currentAppendFile` records the separate `exports/map-append41-v37.csv`: the unchanged historical 38 rows followed by three new landmark records. `appendFile` retains the immutable v35 artifact; `archivedAppendFiles` retains the immutable v36 38-row artifact and its original metadata. Never overwrite either older file. The Wangsong ticket-office address and Hwarang dated drainage-maintenance note are canonical-only existing-record corrections, not append rows or live map edits. The old lot locator and historical field ledgers remain intact.

The latest 38-row attempt, around 2026-10-27 06:52 UTC, stopped at Chrome renderer error9 when opening the existing destination data table. No import dialog, chooser, upload or save was reached; zero writes and zero uncertain writes. A destination-layer observation is not a fresh full-map inventory. All607/601/6 totals remain receipt-backed. If the user manually uploads35 or38 rows, reconcile that result before using the overlapping41-row file; do not append both blindly.

The v37 canonical release remains prepared, not Site-deployed; the latest actual Site publication is v36 according to `data/history/site-deployment-v36.json`. `sourceSiteCommit` retains the original v35 migration source, not the current/future consumer commit. When exact committed inputs are released, update consumer cache-busting asset/JSON versions, verify all three deployed input hashes and record publication evidence separately. Do not rewrite the v36 deployment receipt or earlier change records.

Before any map write:

1. Read the current map's inventory and intended destination schema. Reconcile against 607 known native identities and the receipt-backed imported IDs; never assume the old row count is fresh.
2. Check all pending IDs and names against the current map. Verify full source addresses and source evidence; preserve all uncertainty.
3. Use **append/add rows only** in the authorized existing destination layer. Do not use replace/match/update against the 607 old rows and do not create/delete layers or fields as a side effect.
4. Use the full Address field for geocoding; Name for the label. The file has no coordinate columns and no Source audit column. General source point text is not an instruction to move existing markers. Any newly positioned result is address-geocoded, not a verified entrance.
5. Categories are English-first bilingual existing values. `Activities / 체험` is intentionally retained where compatibility requires it; this append does not finish display-category normalization or purpose-layer consolidation.
6. After save **and reload**, read back the new row identities and fields, position/unresolved counts, and verify that all existing identities, full addresses, source URLs, geometry and styles were preserved to the extent actually observable. Record scope and limits. Do not claim full geometry preservation without full geometry evidence.
7. Update sync-state only from verified results. Uncertain writes must be inspected before retry; a denied action must not be retried without materially new authority/evidence. Keep source/status/coordinate correction queues separate from row membership.

## Existing metadata cleanup

`pending-field-edits692.json` is a historical proposal list, **not an executable patch**. Check current value for exact native ID and field; if it differs from `before`, stop and reconcile. Do not replay the 213 completed keys. Preserve the 296 original audit strings before any explicitly authorized clearing/deletion. This repository's existence does not itself authorize deleting columns, normalizing addresses, merging layers, recreating features, or replacing the map.
