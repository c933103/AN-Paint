# AN Paint M04 independent technical review

Review date: 2026-10-12. Status: **provisional technical review; translation snapshot remains incomplete**. No source changes were made by this reviewer.

## Scope and disposition

Reviewed the M04 production exception/localization delta, isolated prior-test successor, new query-failure flow tests, historical-preservation adapters and Nôm font extension. Read AGENTS.md, TRANSLATING.md and CI.md. Language quality is a separate review. This report does not confer completion credit on earlier withdrawn localization work.

The expected develop base is `4231edaac45d89c52f51e2b77d0f94a1176ad88c`, tree `c1d65b3f0f89a8af12a9dbe69eb1824ef19e28c1`. Local temporary baseline HEAD is `ce846da94f6d5240b0ee88de7506b8bfc26c4a9a`; its tree was independently verified to equal the exact expected tree.

No blocking production/font defect was identified in the reviewed bytes. The current 53-of-59 scoped catalogue state remains incomplete, and two strict host completeness checks fail as intended. Android compilation, resources, JVM runtime, lint and installed rendering are not established locally.

## Pass: production and test scope

- `CommonsAttribution.parse` retains exactly `root.has("error")`, including null/false/empty values. Its only behavior change is replacing the original English-message IOException with a message-less `QueryFailureException : IOException`.
- No provider error fields are attached. Malformed JSON, HTTP, response-size, field-size, page validation, ambiguity, request hosts/parameters and metadata content handling remain unchanged.
- Both Copy credit and insertion catch routes invoke the same mapper inside the alive-activity UI callback. Only the new typed condition maps to the new resource; untyped details remain verbatim and existing empty-reason behavior remains action-specific.
- The prior `CommonsCopyCreditErrorTest` successor separates exactly the old query case into its localized-resource assertion. Every other reason and its helper/retry assertions are retained. Fixture reversal was compared directly with Git baseline bytes, not solely with fixture-provided hashes.
- New flow tests use the actual WebView action routes and fixture connections. Source review covered top-level-versus-nested errors, cleanup, provider-content non-leakage, M03/M05/M09 distinctions, both actions, successful retry, clipboard/document/draft/cache/temp/result preservation, UI-time resource resolution, percent/newline and blank details, duplicate input and destruction during/after work.
- The new repeated vertical test requires genuine horizontal overflow, moves to its far edge, performs another real action, checks reading-start restoration and unchanged failure state, and verifies the second request sequence. It does not claim installed-touch coverage.
- Four readability cases cover normal/double scale and portrait/short landscape across 12 representative profiles and both actions. Assertions distinguish complete laid-out text from simultaneous visibility and require reachable scroll endpoints. The source emits clearly labelled Robolectric NATIVE evidence. These cases were inspected, not executed here.
- Narrow adapters remove only hash-pinned M04 deltas before applying historical expectations. Direct Git comparison confirms all 205 separately pinned paths and all 561 historical verification/fixture files remain byte-identical.

Production/test SHA-256 values are in `source-scope-independent-check.json`. New flow-test SHA-256 at this review: `623cd3099174f55ed72a6173cf71ecebf4bab9d0158754df6f99dc78786b77a4`.

## Pass: independent font and raster evidence

`check_font_independent.py` compares the actual Git baseline, actual current font and separately supplied pinned source without relying on M04 assertion flags.

- Base: `4ae4cab599622f6c9d66b8a99074f2a291ffc32000a78ba69f241fc12eb64e05`.
- Source Nom Na Tong v5.18: `37bd8506257d0905d499395e7f0bc2b6a2ae619dbb635a82ea0905b75b2ff5f3`.
- Current/rebuilt output: `6b70d3c5c146c9d11503e5dff7ade5e7ccb3ae5a70c511f71902d4a75f7a3006`, 276,500 bytes.
- All 737 old glyphs keep compiled outlines, glyph IDs/order, advances and bearings. All 735 old Unicode mappings remain unchanged in both original cmap subtables.
- Exactly U+3002, U+554F and U+8FFD are appended as glyph IDs 737–739. Their nonempty noncomposite outlines and horizontal metrics exactly equal the pinned source. They contain no glyph instructions or unavailable hinting dependencies.
- Raw OS/2, hhea, name and post tables are byte-identical. Head differs only in checksum adjustment; maxp differs only in glyph count. glyf/loca/hmtx retain their complete old prefixes; no table is added or removed.
- Inventory differs only by the asset digest. Bundled notice is byte-identical to the baseline, retaining MIT plus OFL text; name/licence metadata is unchanged. This is a preservation check, not a new legal opinion.
- Rebuilding with the existing preservation-only builder and source is byte-identical to the delivered font.
- Reran the renderer and opened the actual PNG. All 2,205 old-codepoint mask/offset/advance comparisons at 24/48/96px are identical. Added glyphs and phrase are visible with no tofu or image-edge clipping. At 24px, 問/追 source/subset raster differences are retained in the machine-readable evidence; all new glyph masks match at 48/96px. This is local Pillow/FreeType evidence, not Android or linguistic acceptance.

Independent results: `font-independent-check.json`, `font-rebuild.json`, `raster/nom-renderer-checks.json`, `raster/nom-renderer-comparison.png`.

## Partial catalogue snapshot

At this checkpoint, default plus 53 reviewed scoped values are inserted, with six deliberately absent: ain-Kana, ain-Latn, bo, mn-Mong, mnc-Mong and ryu. Independent reversal of each of the 54 changed catalogue files restores exact baseline bytes. The added API30/API35 resource test preserves strict 59-value and 81-fallback expectations, so the partial state cannot count as a pass.

The new partial-state host check validates implemented values against decisions, absence of every unresolved value, 140 per-tag dispositions and 81 out-of-scope fallbacks. It supplements rather than replaces the strict failing gates. No language acceptance is inferred.

## Executed checks

- PASS: `python check_font_independent.py`.
- PASS: preservation-only font rebuild and byte-for-byte `cmp`.
- PASS: `python tools/verify_nom_m04_renderer.py ... raster` plus actual image inspection.
- PASS: 14 focused M04/M03/font coverage methods; `font-contract-tests.log`.
- PASS: 3 initial production/test-preservation methods; `production-contract-tests.log`.
- PASS: `python check_scope_independent.py`, including 205 protected paths and 561 historical files.
- PASS: independent exact baseline reversal for all 54 currently changed catalogue files; `partial-catalogue-independent.json`.
- PARTIAL/FAILED: 39 focused M04/M03/copy-credit/SVG/TIFF host methods, 37 pass and 2 strict M04 completeness failures. Both failures identify the known 53/59 shortage, with no unexpected failure. Raw log: `partial-focused-contract-tests.log`.
- PASS: Python syntax compilation of six new M04 modules/scripts.
- UNRUN by this reviewer: Android/Kotlin compilation, Robolectric execution/render capture, lint, APK/native tests and installed-device checks. The producer's retained configured Gradle attempt was inspected and stops with `SDK location not found`; it is not an Android pass. No SDK installation, remote workflow or Work task was initiated.
- PENDING: final language/resource snapshot, final 59/81 and aggregate host rerun, exact-source Android CI and actual Android render inspection.

## Reproduction

From `/workspace/shared/anpaint-m04-20261012`:

```
python /workspace/shared/anpaint-m04-technical-review-20261012/check_font_independent.py
python /workspace/shared/anpaint-m04-technical-review-20261012/check_scope_independent.py
PYTHONPATH=tools python -m unittest -v test_commons_metadata_m04_font test_commons_metadata_m03_font test_locale_font_coverage
PYTHONPATH=tools python -m unittest -v test_commons_metadata_m04 test_commons_metadata_m03 test_commons_copy_credit_errors test_svg_error_translations test_tiff_c023_wording
```

The report and executable checks are review artifacts outside the source tree. They need final snapshot binding and the repository owner's durable publication; they are not a merge, release or complete-language recommendation.
