# Integrated CA/RO coverage at PR178 merge — postmerge CI pending

The source snapshot is the **actual merge `e5f2d4e2d07e678076f022aa7b3ef923e13c3721`**, tree `806d9577409c4044212d1c12e6e38da46417bae6`, with ordered parents `ce796879f4568a27b9d905a8e8db639dd0a93a30` and reviewed head `82995ec1f030d23cb4e2b1426b511abe802890eb`. The supplied identity receipt confirms the merge and matching develop ref.

**Actual postmerge push run 40350966050 is pending in that receipt.** No terminal result is asserted here. Successful PR artifacts are preserved as PR evidence, not relabelled as postmerge evidence. GitHub-reported signature fields were supplied as verified=true, reason=valid, verified_at 2026-10-26T15:36:21Z; this is not our independent PGP validation.

## Coverage and review delta

| Measure | CA | RO |
|---|---:|---:|
| Direct catalogue values | 150 → 205 | 150 → 205 |
| P0 present / total | 32/92 → 87/92 | 32/92 → 87/92 |
| P0 missing | 60 → 5 | 60 → 5 |
| P1 present / total | 94/249, unchanged | 94/249, unchanged |
| Exact English-identical leaves | 6, unchanged | 8, unchanged |
| New qualified complete-value scopes | 55 | 55 |
| Prior bounded scopes retained separately | 23 | 23 |

All **171 option rows** match the original preview exactly. P0 presence is **6,838**, up 110; P0 gaps are **8,894**, down 110. Containers present are **50,861** and leaves present **50,895**, each up 110. Missing containers are **71,746** and missing leaves **71,883**, each down 110. English-identical leaves remain **7,051**; equality is not automatically a defect. The other 169 option rows are unchanged.

The only remaining P0 gaps per CA/RO catalogue are the preserved holds: `formats22_derived_exported`, `ui_save_as`, `ui_save_as_jpeg`, `ui_save_as_jpeg_xl`, `ui_save_as_png`. P1 remains unchanged, with 155 missing values per locale.

Exactly **110 new receipt-bound whole values** are carried: 107 accepted unchanged and three reviewed replacements (CA 53 + 2, RO 54 + 1). All original qualifications and historical author caveats remain. These are bounded independent AI linguistic/source-static judgments, not native-human, device, layout, runtime or whole-language certification. Each locale's 150 inherited values and 23 prior reviewed pairs are preserved and separately hash-checked. No global linguistic total is guessed; prior accepted, qualified, clause-only, author-only, historical, unmatched and synthetic categories remain intact.

Valencian parent routing is distinct from direct acceptance and gains none. All five NN/DA/NO holds, paired P1/frozen evidence, global scoped59/fallback112, #56 never-merge, #113 hold/retarget, #159 freeze and Help/archive/release pauses remain unchanged.

## The correction changes a test, not coverage

The corrected reviewed head differs from the preserved `93f27ed` preview in exactly **one file**, `NumericDisplayLocaleTest.kt`: the obsolete English Romanian prefix was replaced by the reviewed Romanian prefix, with an additional independent `2,25 MP` assertion. All **176 coverage inputs** are byte-identical; no production code or resource changed during that repair. The complete ce796-to-merge delta contains **13 paths** (three added), not the preview's 12.

The original PR run 40340230583 is preserved as failed: one failure among 1,366 JVM tests. Corrected PR run 40346532936 is preserved separately as successful, including all six numeric-locale tests. These observations are not actual postmerge results.

## Source and historical evidence

- All **1,379 actual source blobs** match the recursively verified full Git tree. All 174 catalogues are present, and all 176 coverage source bindings agree with the current tree and baseline.
- The full **84-file original preview** is retained byte-for-byte, including its exact 47-file ce796 baseline and pending/historical statuses.
- Original failure, forward-corrected repair and corrected PR-terminal packages remain unchanged under `inputs/`. The repair package preserves explicit raw/display log hash mappings and the prior log-hygiene correction; unsanitized historical display logs are not reintroduced.
- Original failure record revision: `1984fd4`; repair record: `79192cbafad86f7c582f357844efe8fb8cf7eb2e`; PR-terminal record: `67a7dfe36e7f9652aa081ddcab7bb5e8aa062e44`.

Ordinary and optimized recomputation are byte-identical. **27 additional merge/status/source/provenance controls reject**, alongside the unchanged historical preview's 71 controls. Independent DOM/Git-CLI calculation rechecks all 171 rows, CSV/JSON agreement, totals, 110 new complete source/target pairs and 46 prior pairs.

## Reproduce

Use Python 3.9+ and Git. Set `SOURCE_ROOT` to the exact actual merge tree, `ORIGINAL_SOURCE_ROOT` to the original `93f27ed172cc730c80ed7a2ffbcacc1b0c04383f` preview source and `BASELINE_SOURCE_ROOT` to `ce796879f4568a27b9d905a8e8db639dd0a93a30`. Included historical files are immutable inputs, not live statuses.

```sh
python -B recompute_integrated.py --inputs inputs --source-root "$SOURCE_ROOT" --original-source-root "$ORIGINAL_SOURCE_ROOT" --baseline-source-root "$BASELINE_SOURCE_ROOT" --out ordinary
python -B test_integrated_guards.py --inputs inputs --source-root "$SOURCE_ROOT" --original-source-root "$ORIGINAL_SOURCE_ROOT" --baseline-source-root "$BASELINE_SOURCE_ROOT" --out ordinary
python -B verify_independently.py --inputs inputs/original-preview/inputs --actual-inputs inputs --source-root "$SOURCE_ROOT" --baseline-source-root "$BASELINE_SOURCE_ROOT" --result ordinary --out ordinary
python -B -O recompute_integrated.py --inputs inputs --source-root "$SOURCE_ROOT" --original-source-root "$ORIGINAL_SOURCE_ROOT" --baseline-source-root "$BASELINE_SOURCE_ROOT" --out optimized
python -B -O test_integrated_guards.py --inputs inputs --source-root "$SOURCE_ROOT" --original-source-root "$ORIGINAL_SOURCE_ROOT" --baseline-source-root "$BASELINE_SOURCE_ROOT" --out optimized
python -B -O verify_independently.py --inputs inputs/original-preview/inputs --actual-inputs inputs --source-root "$SOURCE_ROOT" --baseline-source-root "$BASELINE_SOURCE_ROOT" --result optimized --out optimized
diff -qr ordinary optimized
```

`manifest.json` covers every payload file except itself. This package performs no external publication, source edit, CI polling or release. Later postmerge terminal evidence must be attached separately with its exact actual-merge artifact bindings; it must not overwrite this pending observation or the original preview.
