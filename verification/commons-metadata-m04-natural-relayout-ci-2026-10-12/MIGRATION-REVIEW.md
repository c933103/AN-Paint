# Behavior-first migration review

Scope: read-only review of 04b128889a4ff9159f199d1737bd07d41e22162d (tree 3dcc1a82f878ad7e0e708cff25ec8d493b88bbc6). No migration source changes by this reviewer. The later owner instruction supersedes the earlier requirement to perpetually preserve source hashes through inverse adapters.

## Preserve as current product contracts

- Parse the accepted default + 59 M04 values and the equivalent current M02/M03/C05 message expectations. Retain Unicode controls, Android quoting/placeholders, duplicate-key detection, catalogue tag uniqueness and explicitly intentional fallback choices. A compact key/tag/value fixture is useful; a hash of its surrounding XML file is not required.
- Keep current Kotlin resource resolution on API30/35, exact-script Korean alias selection and script-sensitive tags. Tests should compare parsed values and runtime resolution, not the bytes of their own test source.
- Keep actual query-error semantics (all top-level `error` values, nested-error distinction), separate HTTP/response-size/field-validation cases, both real WebView action routes, late callback resource resolution, retry/state/credit-draft preservation, cancellation/destruction and connection/input/file cleanup.
- Keep full displayed/layout/accessibility text, no ellipsis, complete line coverage, positive sizes, parent reachability, reading-start scroll reset, portrait/landscape/font-scale behavior, natural same-height status replacement and lifecycle regression tests.
- Keep independent full-layout reference allocation, native real-overflow and removed-ink controls, source/route-bound installed records, malformed/duplicate/missing transport rejection, and natural-update state-transition checks. Visual severity/acceptance needs the separate reassessment in READABILITY-CRITERION.md; preserving diagnostics does not require perpetuating zero-alpha as the release policy.
- Keep runtime font coverage, UI-only font selection, cmap/metrics sanity, packaged licence and font inventory consistency. Pinned upstream input provenance is useful for deterministic rebuilding. Historic old-outline/raster comparisons belong with the one-time font-extension review, not a mandatory reconstruction of every prior binary on every source change.
- Derive eligible and scheduled test identities from current source/configuration. Compare actual same-run completion against that discovery, including explicit API eligibility and restart omissions. Per-run source/artifact binding remains useful provenance; the old 890/892 identity JSON is not a permanent source oracle.

## Archive; remove from active dependency graph

- `commons_metadata_*_scope.py` inverse/projection chains and successor edit fixtures, including receiver -> glyph bounds -> painted ink -> diagnostic -> composition -> M04/M03/M02/C05 byte reconstruction.
- Whole-file before/after hashes, 24-order historical reversal tests, all-leaf manifests, historical test-source equality, fixture-byte pin corruption tests, and requirements that old evidence reports/manifests remain in the live checkout.
- Generated diffs, historical raw logs, raster dumps, old reviewer reports, source inventories and failed checkpoint records. Preserve immutable archive links and concise provenance in the repository; do not make normal CI download and reconstruct the archive.
- The Codex P2 strict-forwarding defect is a real defect in an archival helper. Once the chain and its consumers are retired, the meaningful resolution is removal of the affected mechanism and verification that no live dependency remains, rather than another inverse layer.

## Mixed methods need splitting

`test_commons_metadata_m04.py` combines useful value/format/fallback assertions and source hashes in the same methods. Extract the former; do not delete the whole module blindly. `test_commons_metadata_m04_font.py` mixes current cmap/licence/inventory expectations with old binary reversals. `test_commons_metadata_m04_glyph_bounds.py` and `...receiver.py` mostly inspect source strings; the real behavior already lives in the Kotlin/device methods. Prefer exercising that behavior over retaining a substring assertion that merely names it.

Host transport/runner/inventory tests have independent value even when their data contains run/source identifiers. Preserve behavioral malformed/missing/duplicate/state mismatch controls. Do not confuse authentication of a particular artifact with a requirement that source can never change.

## One-time migration acceptance

Use a single external diff audit to show production Kotlin, current Android tests, resources/fonts/licences and transport implementation unchanged unless a separately reviewed behavior fix is explicitly included. Inventory removed host methods by purpose and map each useful assertion to its retained/replacement contract. Run current focused host tests, current full suite, compilation, actual JVM tests and installed API30/35 phases. Report the new discovered counts and any intentional removed historical tests; do not force them to equal a historical count. Confirm there are no imports/file reads from archived inverse/evidence paths and that the ordinary checkout can run without those archives.
