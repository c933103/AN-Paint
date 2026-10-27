# PR178 preview: CA and RO P0 gaps reduce to five explicit holds each

**This is a source-pinned PR preview, not an integrated or production update.** It describes head `93f27ed172cc730c80ed7a2ffbcacc1b0c04383f`, tree `571ec84860cb837ae8376f72d0becfb8fd2b7b6d`. No new merge or terminal CI receipt was supplied to this preparation. The production baseline retained here is `ce796879f4568a27b9d905a8e8db639dd0a93a30`.

## Exact proposed delta

| Measure | CA | RO |
|---|---:|---:|
| Direct catalogue containers | 150 → 205 | 150 → 205 |
| P0 present / total | 32/92 → 87/92 | 32/92 → 87/92 |
| P0 missing | 60 → 5 | 60 → 5 |
| P1 present / total | 94/249, unchanged | 94/249, unchanged |
| P1 missing | 155, unchanged | 155, unchanged |
| Exact English-identical leaves | 6, unchanged | 8, unchanged |
| Newly reviewed whole values | 55 | 55 |
| Prior bounded reviewed values retained separately | 23 | 23 |

Across all **171 options**, direct P0 presence is **6,838** (+110), with **8,894** P0 gaps (−110). There are **50,861** containers and **50,895** leaves present, each +110. Missing containers are **71,746** and missing leaves **71,883**, each −110. English-identical leaves remain **7,051**; that equality is not automatically an error. The other 169 option rows are unchanged. Canonical denominators remain 717 containers, 718 leaves and 92 P0 values. Full structural presence remains 59 options; 31 still have zero direct presence.

The five remaining P0 identities per locale are `formats22_derived_exported`, `ui_save_as`, `ui_save_as_jpeg`, `ui_save_as_jpeg_xl`, and `ui_save_as_png`. These are the preserved no-current-consumer holds, not new defect judgments. No other P0 gaps remain in these two direct catalogues at this head.

## Review accounting stays bounded

Only the 110 newly present locale/identity pairs gain exact current-value receipt bindings: **107 unchanged accepts and three exact revisions** (CA 53 + 2; RO 54 + 1). They are qualified independent AI whole-value linguistic/source-static outcomes—not native-human, physical-device, layout, runtime or whole-language certification.

All 150 inherited values and attributes per locale are unchanged. The prior 23 bounded reviewed pairs per locale (10 save/message plus 13 import/format) are independently hash-joined and remain separate from the new 55. The complete original review entries, their confidence, scope, composition qualifiers and historical author caveats are retained; earlier accepted, qualified, clause-only, author-only, historical, unmatched and synthetic categories are carried unchanged through their immutable ledgers. No global linguistic total is guessed or recomputed.

Valencian remains parent-routed where supported by the prior runtime evidence, not newly directly reviewed. The historical baseline runtime receipt is carried explicitly as history, not current-head runtime proof. Mixed English action labels/dynamic reasons, paired P1/frozen boundaries, global scoped59/fallback112, #56 never-merge, #113 hold/retarget, #159 freeze and Help/archive/release pauses remain unchanged.

## Verification

- All **1,379** head blobs match the complete recursively hash-verified Git tree. The full diff has 12 changed/added paths, including three new test/fixture files; only CA/RO catalogue files change coverage.
- All **176** coverage input files are checked against current and baseline raw Git/SHA-256 identities: 174 unchanged, two changed. All 174 catalogue files are present exactly.
- The complete 47-file production baseline package is copied byte-for-byte under `inputs/baseline`, preserving prior successful and failed receipts and historical pending observations. Its manifest is independently rechecked.
- Ordinary and Python `-O` results are byte-identical. **71** malformed/mutation controls reject, including 26 refreshed-pair format probes derived from the **two actual `formatted="false"` values**. All mutations are explicitly synthetic and never alter source files.
- An independent implementation using DOM and read-only Git CLI—not the recomputation helper—recalculates all 171 rows, CSV/JSON agreement, totals, 110 new reviewed source/target pairs and 46 prior reviewed pairs.

`structural-per-locale.csv` and `.json` are the full proposed 171-option table. `review-scope-reconciliation.json` contains exact new receipt-bound scopes. `data-quality-profile.json`, `source-bindings.json`, `full-source-delta.json` and `input-bindings.json` expose denominators, source deltas, immutable input identities and counting limits.

## Reproduce locally

Use Python 3.9+ and Git. Set `SOURCE_ROOT` to an exact checkout/extraction of the pinned PR head, and `BASELINE_SOURCE_ROOT` to the exact `ce796879f4568a27b9d905a8e8db639dd0a93a30` source. All other inputs are included here as UTF-8 project evidence.

```sh
python recompute_delta.py --inputs inputs --source-root "$SOURCE_ROOT" --baseline-source-root "$BASELINE_SOURCE_ROOT" --out ordinary
python test_coverage_guards.py --inputs inputs --source-root "$SOURCE_ROOT" --baseline-source-root "$BASELINE_SOURCE_ROOT" --out ordinary
python verify_independently.py --inputs inputs --source-root "$SOURCE_ROOT" --baseline-source-root "$BASELINE_SOURCE_ROOT" --result ordinary --out ordinary
python -O recompute_delta.py --inputs inputs --source-root "$SOURCE_ROOT" --baseline-source-root "$BASELINE_SOURCE_ROOT" --out optimized
python -O test_coverage_guards.py --inputs inputs --source-root "$SOURCE_ROOT" --baseline-source-root "$BASELINE_SOURCE_ROOT" --out optimized
python -O verify_independently.py --inputs inputs --source-root "$SOURCE_ROOT" --baseline-source-root "$BASELINE_SOURCE_ROOT" --result optimized --out optimized
diff -qr ordinary optimized
```

The baseline methodology is reused without silently changing its source pin, denominator or historical status. The preview must remain immutable if the source or merge moves. Later integrated coverage needs actual merge identity and separately bound postmerge artifact/terminal receipts; the preview alone establishes neither.

This preparation performs no source edits, external writes, CI polling, publication or release. `manifest.json` hashes every payload file except itself; retain its external SHA-256 when recording the package.
