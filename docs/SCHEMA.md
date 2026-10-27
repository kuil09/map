# Data contract

`data/places.json` is the canonical ordered list. Preserve stable `id`; never identify records by row number, translated name, guessed name similarity or an external provider's changing title. `schemas/places.schema.json` describes the minimum contract. Extra category-specific fields are intentional and must not be dropped by transforms.

Required fields: `id`, `name_en`, `name_ko`, `area`, `category`, `setting`, `address`, five-language `description` and `notes`, `sources`, `checked`, `map_type`, `coordinates`, `coordinate_status`, `radial_distance_km`. Language keys are `en`, `ko`, `ja`, `zh`, `es`. Empty optional values are not an assertion of absence.

## Sources

Each source has public `url`, `quality` and `audit`. Preserve the audit's checked date, semantic scope, status, title, HTTP code if known, final URL if known, reason and access method where provided. HTTP success alone does not prove the venue or the relevant claim. A brand page is not branch-service evidence; registry inclusion is not live-operation evidence. Keep `unconfirmed` and `blocked` as such, even when another source independently supports a record. `raw_scope` retains more precise source classification when the site's display uses a broader scope.

Do not remove an unavailable historical source without leaving an evidence-backed change entry. Do not retry an access-denied target through another tool or hostname to bypass the restriction.

## Coordinates and distance

Unknown coordinates mean `coordinates: null` **and** `radial_distance_km: null`, not zero, a city centroid, a map viewport, a guessed entrance, or an address-geocoder result. Non-null coordinates are `{lat, lng}` and require `coordinate_source_url` and `coordinate_provenance`; the source URL must also appear in the place's `sources`. A measured distance additionally requires `distance_reference_id` and `distance_method`. The original 648 records retain their strict coordinate/distance pairing. New records may preserve a verified published general venue point while distance remains unmeasured, as specified below.

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

## Active nationwide additions (append-only extension)

The original 648 records, `coarse-category-plan.json`, and `public-exclusions.json`
are an immutable baseline, not files to regenerate for new places. Their historical
hashes and source-record hashes remain checked. The original records must remain
an unchanged, ordered prefix of `data/places.json`; editing an original record
requires a separately reviewed migration, not this addition-only mechanism.

When new records are ready, add **only their assignments** to the optional canonical
`data/map/active-classification.json` input:

```json
{
  "schemaVersion": "1.0",
  "status": "active_classification",
  "canonicalRepository": "https://github.com/kuil09/map",
  "historicalPlanSha256": "<unchanged historical plan SHA-256>",
  "canonicalPlacesSha256": "<current data/places.json bytes SHA-256>",
  "assignments": [
    {
      "id": "<new stable place ID>",
      "sourceRecordSha256": "<canonical record hash using record_sha>",
      "sourceCategory": "landmarks",
      "visitorPurpose": "culture_sights",
      "presentationGroup": "culture_sights",
      "nativeId": null
    }
  ]
}
```

Assignments must match the added-record order exactly, with no historical IDs,
missing/duplicate IDs or sixth purpose. The existing five purposes and translations
remain unchanged. New records require `access: "public"`; restricted or unknown
access fails closed rather than changing the original military exclusion policy.
All existing canonical source/audit, five-language, address, coordinate-provenance
and count checks still apply. New evidence and the approved change record belong
in a new dated history file, not an overwritten restoration/append receipt.

First additions require explicit `entrance_verification: "unverified"`. Unknown
coordinates remain null, never guessed. A new record may retain a published general
venue point **without calculating any distance**: use `radial_distance_km: null`,
`distance_kind: "unmeasured"`, and `distance_reference_id: null`. Non-null points
require nonempty coordinate provenance and a linked source audit with
`status: "verified"` and `scope: "exact"`; a brand-level or unconfirmed source is
not sufficient. The point is not a verified entrance or a Camp Walker distance.

If a distance is actually calculated, coordinates must be present, with
`distance_kind: "straight_line"`, the documented reference ID and method; the
existing Haversine check still applies. There is **no 200 km eligibility cap** and
no forced Humphreys-origin calculation for the Camp Walker additions. This initial
extension neither defines a new origin nor supports verified entrances or road
routing. Do not copy historical Humphreys-radius wording onto new additions.

`metadata.counts.coordinatePoints` counts non-null coordinates independently.
`metadata.counts.unmeasured` and `research.distance_audit.unchecked_records` count
null distances; `research.distance_audit.checked_records` counts measured distances.
Thus adding three sourced general points with all distances null raises only the
coordinate-point count, not the measured-distance count. Original records are
unchanged and retain their old strict pairing checks.

For an addition, update current aggregate counts and queue its ID once in both
`sync-state.pendingAppendPlaceIds` and the ordered `placeIds` of `pendingCohorts`.
Keep `currentAppendFile: null` and
`currentAppendStatus: "pending_rows_not_authorized_for_upload"`. This patch does
not support recording a new completed map import. Historical membership remains
648; the current restoration receipt still establishes 646 / 639 / 7, regardless
of the growing public directory. No invented native IDs or automatic import.
Offline CSV generation retains its existing reviewed-category limitations and
`uploadAuthorized: false`; preparing an export is not map synchronization.

With no overlay and no additions, generated public files and counts are unchanged.
The extension tests use synthetic fixtures only; no real new records are included.

Prepared release labels must also advance truthfully: new/edited metadata names
the latest successful public deployment receipt (currently v38) as
`lastPublishedSiteRelease`, while `snapshotRelease`/`sync-state.siteRelease` is a
newer prepared release (e.g. v39). Failed/pending receipts do not establish
publication. The exact original pre-v38-publication metadata bytes remain accepted
as a historical snapshot; this exception does not apply to newly changed counts or
metadata. Keep both historical deployment receipts unchanged. Update explanatory
status prose when preparing a new release; successful validation is not deployment.
