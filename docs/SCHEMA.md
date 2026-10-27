# Data contract

`data/places.json` is the canonical ordered list. Preserve stable `id`; never identify records by row number, translated name, guessed name similarity or an external provider's changing title. `schemas/places.schema.json` describes the minimum contract. Extra category-specific fields are intentional and must not be dropped by transforms.

Required fields: `id`, `name_en`, `name_ko`, `area`, `category`, `setting`, `address`, five-language `description` and `notes`, `sources`, `checked`, `map_type`, `coordinates`, `coordinate_status`, `radial_distance_km`. Language keys are `en`, `ko`, `ja`, `zh`, `es`. Empty optional values are not an assertion of absence.

## Sources

Each source has public `url`, `quality` and `audit`. Preserve the audit's checked date, semantic scope, status, title, HTTP code if known, final URL if known, reason and access method where provided. HTTP success alone does not prove the venue or the relevant claim. A brand page is not branch-service evidence; registry inclusion is not live-operation evidence. Keep `unconfirmed` and `blocked` as such, even when another source independently supports a record. `raw_scope` retains more precise source classification when the site's display uses a broader scope.

Do not remove an unavailable historical source without leaving an evidence-backed change entry. Do not retry an access-denied target through another tool or hostname to bypass the restriction.

## Coordinates and distance

Unknown means `coordinates: null` **and** `radial_distance_km: null`, not zero, a city centroid, a map viewport, a guessed entrance, or an address-geocoder result. Non-null coordinates are `{lat, lng}` and require `coordinate_source_url`, `coordinate_provenance`, `distance_reference_id`, and `distance_method`. The source URL must also appear in the place's `sources`.

The current distance reference and Haversine method are in `data/research.json.distance_audit`: Earth mean radius 6371.0088 km, published Desiderio airfield planning point. No gate or road distance is implied. GoCamping map anchors and source-code display offsets do not establish surveyed accuracy.

## Native map identity versus site identity

`data/map/baseline607.json` preserves captured native table `baselineFields`, including old field text. It is historical data, not the canonical description to republish or a live import file. `nativeId` identifies the existing Google My Maps feature. `place.id` identifies the guide entry.

`identity-index.json` establishes only 296 explicit native-to-place joins from captured `Record ID` cells. The remaining 311 native records remain unjoined. Receipt-backed membership of all 607 imported place IDs is preserved separately; it does not establish a one-to-one native mapping for those 311. No fuzzy or row-order joins are accepted. `verified-import-history.json` separately adds receipt-backed membership for 41 later imported place IDs, bringing current membership to 648 without changing the historical identity index or inventing new native IDs. `unresolved7.json` records the current seven unresolved place IDs; `unresolved6.json` remains immutable historical evidence. Empty `pendingAppendPlaceIds` requires `currentAppendFile: null`; historical CSVs are not import candidates.

The original audit values have per-string UTF-8 hashes. Do not change those strings to improve wording. New evidence belongs in current source objects and a new dated history event. Historical proposed edits are not instructions to execute, and recorded success is not fresh map verification.

## Photos

`data/photos.json` is the unchanged existing-site photo manifest. Exact `place_ids` establish a photo-to-place link; an empty array means regional imagery and must not be presented as a photograph of a specific venue. Asset `path` is relative to a site build, not a local computer path. Keep license/author/source/modification fields and every uncertainty. Verify bytes and SHA-256 before reusing existing assets.

## Change discipline

1. Add or edit canonical records; retain unsupported details as unknown.
2. Record old/new values, evidence URL, date, scope and known limitations in a new dated history entry. Do not overwrite historical snapshots.
3. Recompute metadata counts and derived research summaries where affected. Run validation/tests and regenerate outputs.
4. Review map deltas separately from site data. An imported row does not mean later source or coordinate changes were synchronized.

## Proposed visitor-purpose presentation

`data/map/coarse-category-plan.json` is `proposed_not_applied`: an exhaustive 648-ID presentation contract with exact names, addresses and source-record hashes. Five ordinary purposes plus a two-place restricted-access warning override do not replace canonical `category` or subtype fields. Only 296 historical native joins are supplied; all others remain null. No live category, layer or Site filter change is established by this plan.
