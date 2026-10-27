# Provenance, verification and preservation limits

The migration starts from the existing public guide's v35 data at source commit `bacf5a334a7850977ff0673925c6305191e221a6`. Canonical baseline commit `88c2ee5409d7c41ffe91ee6c2e2c0eb6059a2590` retains the three v35 site input JSON files byte-for-byte. Their historical hashes remain in `verification-history.json` and are regression-tested against local Git history; current v36 data has separate hashes. No private filesystem locations or private receipts are published.

The baseline comes from the pre-resume archive of captured native tables: 607 feature identities, seven layers, 296 original nonempty Source audit values. Original audit values are preserved exactly, with per-value hashes. Historical applied changes are 213 (audit 115, Access and booking 46, Additional details 46, Category 5, Description 1); pending changes are 692. The separate Beartree source-URL preservation change and three failed edit attempts are recorded separately, not inflated into completed cleanup counts.

**The baseline fields and 213 applied changes are not a fresh full-table snapshot.** For forensic inspection, `build_exports.py` can reconstruct baseline plus recorded successful deltas in an explicitly historical JSON output. Do not import that output.

## Geometry

- Receipt-backed native counts: 607 rows, 601 positioned, 6 unresolved.
- 100 imported latitude/longitude text pairs are metadata, not exported native geometry.
- 47 paired before/after UI coordinate strings provide partial display-level evidence only.
- The retained historical KML was observed to have 61 Placemarks and zero coordinate elements; its corresponding historical receipt claimed 256 and a different hash. They cannot be treated as the same complete geometry backup.
- A later download UI reported completion but the complete file bytes were not obtained. A downloadable/restorable 601-marker KMZ, feature styles and exact native geometries are **not established**.

## Map state and unresolved work

The latest complete row-identity receipt is dated 2026-10-27T00:33:38.121382+00:00. The retained v35 Site snapshot has 642 places and 35 not imported; its historical append file contains 79 source URL occurrences. Prepared canonical v36 has 645 places and 38 pending rows. Both append artifacts use 10 existing-schema fields, with no Source audit or coordinate input columns. Two rows retain published general point values as explicitly labeled reference text only. The v36 additions have unknown coordinates and distances; three existing market point corrections remain a separate unapplied queue.

## Batch 18 canonical update

`batch18-change-record.json` identifies three exact additions and three existing general-market point updates. The preintegration public audits and four candidate holds are preserved with their reviewed hashes. All 639 unaffected records, 956 old source objects/statuses, existing names/full addresses, original 311 records and existing photo manifest remain exact. Prior history entries and the 607-row baseline, 296 original audit strings, 213 applied changes, 692 historical proposals and v35 CSV remain unchanged. General destination coordinates do not establish an entrance, parking, stall or the whole market boundary. This integration performs no new source request, Site deployment or native-map operation.

A later upload attempt failed with browser renderer error 9 before a file chooser opened: no file selection, no upload submission, zero confirmed or uncertain writes. This is not fresh confirmation that all existing map content remains identical. Recheck before the next write.

105 older source-detail rows remain incompletely reconciled. Source/status/coordinate corrections and four proposed civilian address normalizations remain separate work. The latter require specific authorization and identity checks. Source audit columns deleted: zero. Label/category cleanup and physical purpose-layer consolidation are not complete. Preserve the seven physical layers and existing geometry until an authorized, verified change plan is ready.

## Deliberately not republished

Private account settings, credentials, tokens, signed URLs, device paths, internal task/conversation records, browser state, screenshots, complete third-party HTML, and private original manifests are omitted. Public venue/source URLs, native map feature IDs, factual project fields, research notes and per-value audit hashes are included. Archive evidence paths are omitted rather than linked to nonexistent public files. This is a selected public data preservation package, not the complete private working archive.

No network source verification is implied by a successful integrity test or repository publication. All per-source checked dates and actual content-access statuses stay visible in the dataset.
