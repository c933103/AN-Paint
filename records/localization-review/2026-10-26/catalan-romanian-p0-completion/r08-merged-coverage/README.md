# PR178 integrated coverage and actual postmerge success

**Actual merge `e5f2d4e2d07e678076f022aa7b3ef923e13c3721` is verified through terminal postmerge success.** Its tree is `806d9577409c4044212d1c12e6e38da46417bae6`. Fresh push run **40350966050** completed successfully at **2026-10-26 16:00:53 UTC**, with all six exact-merge checks successful. The monitor is closed; this report performs no further polling.

The [nine-file actual postmerge evidence packet](https://github.com/c933103/AN-Paint/tree/4e9897b8c030c0ab785a34a69f2c872d2d9505d9/records/localization-review/2026-10-26/catalan-romanian-p0-completion/r07-postmerge-terminal) is pinned by manifest SHA-256 `e0a961d4e4f2d6c280836e308adfaf192bea43f7b8a19e2c3686c854ace63b8b`. Fresh actual-merge artifacts are joined to their own run, head, tree, IDs, hashes and fixture identities—not relabelled PR artifacts.

## Current 171-option coverage

| Measure | Catalan (ca) | Romanian (ro) |
|---|---:|---:|
| Direct catalogue values | 205 (+55) | 205 (+55) |
| P0 present / total | 87/92 | 87/92 |
| P0 missing | 5 held | 5 held |
| P1 present / total | 94/249, unchanged | 94/249, unchanged |
| P1 missing | 155, unchanged | 155, unchanged |
| Exact English-identical leaves | 6, unchanged | 8, unchanged |
| New qualified whole-value scopes | 55 | 55 |
| Prior bounded scopes retained separately | 23 | 23 |

Across all **171 options**, P0 presence is **6,838** (+110), with **8,894** P0 gaps (−110). Present containers are **50,861** and leaves **50,895**, each +110. Missing containers are **71,746** and leaves **71,883**, each −110. English-identical leaves remain **7,051**; equality is not automatically a defect. Other 169 option rows are unchanged. The denominators remain 717 canonical containers, 718 leaves and 92 P0 values. Full structural presence remains 59 options; 31 have zero direct presence.

The five held P0 identities per CA/RO locale remain `formats22_derived_exported`, `ui_save_as`, `ui_save_as_jpeg`, `ui_save_as_jpeg_xl`, and `ui_save_as_png`. No other direct P0 gaps remain in these two catalogues.

## Fresh actual-merge evidence

- **JVM:** 1,366 tests across 148 XML files, zero failures/errors/skips; all ten source-bound focused suites passed.
- **Hosted Python:** 1,398 run = **1,396 passed + 2 skipped**, 267.641 seconds. The non-verbose summary does not name skipped identities; they are not guessed or counted as passes.
- **Lint:** zero issues. All Python/JVM/native/lint phase receipts have exit code zero.
- **API35 emulator:** exactly 45 selected/completed app cases and 74 native cases, with composed source/build/fixture/artifact identities checked.
- **Resource generation:** 13 probes, including the expected reserved-variant rejection.
- **Source/APK:** all 1,379 tracked source files are bound; 1,376 are packaged exactly, with three explicit packager exclusions. Extra archive members are counted, not authenticated by the project Git tree. The compiled APK matches **392 scoped values: 110 new + 282 prior**.

This is existing emulator regression coverage, not locale-specific physical-device, layout or native-human certification. The valid CI debug signature is not private upgrade signing or a release. GitHub's reported merge-signature verification is not this report's independent PGP validation.

## Review scope and history are unchanged

Exactly 110 new whole-value judgments remain receipt-bound: 107 unchanged accepts and three exact reviewed revisions (CA 53 + 2, RO 54 + 1). They remain qualified independent AI linguistic/source-static outcomes. **Terminal CI adds zero linguistic acceptances.** All 150 inherited values and attributes per locale and the prior 23 reviewed pairs per locale are preserved separately. No global linguistic total is guessed, and prior accepted, qualified, clause-only, author-only, historical, unmatched and synthetic scopes remain intact.

Valencian parent routing is not direct acceptance and gains none. Five NN/DA/NO holds, paired P1/frozen evidence, global scoped59/fallback112, #56 never-merge, #113 hold/retarget, #159 freeze and Help/archive/release pauses remain unchanged.

The complete **175-file integrated/pending package** is preserved byte-for-byte under `inputs/integrated-pending`, including the original 84-file preview, its 47-file ce796 baseline, original failed PR run, forward-corrected/sanitized repair records and separate corrected PR proof. Pending observations remain historical; none were overwritten. The test-only NumericDisplayLocaleTest repair still has one changed path from the preview; the full base-to-merge delta remains 13 paths. All 176 coverage source inputs and all 171 rows are unchanged by terminal status.

## Reproducibility and checks

`structural-per-locale.csv` and `.json` are the current full table. `coverage-delta.json`, `review-scope-reconciliation.json`, `source-bindings.json` and `data-quality-profile.json` are newly source/status-bound wrappers, with immutable pending-file hashes. `terminal-status-supplement.json` joins all five fresh verification receipts to actual terminal metadata.

Ordinary and optimized report-validation outputs are byte-identical. **48 targeted mutations reject** wrong run/event/head/tree, artifact/fixture identity, terminal status, source counts, compiled scope or hidden/guessed skips. Independent DOM/Git-CLI verification recomputes current source rows/counts and joins exact terminal bytes. These local validator modes do not imply an optimized hosted-CI run.

Use Python 3.9+ and Git. Point `SOURCE_ROOT` to actual merged source, `ORIGINAL_SOURCE_ROOT` to the immutable `93f27ed172cc730c80ed7a2ffbcacc1b0c04383f` preview source, and `BASELINE_SOURCE_ROOT` to `ce796879f4568a27b9d905a8e8db639dd0a93a30`.

```sh
python -B verify_terminal.py --inputs inputs --source-root "$SOURCE_ROOT" --original-source-root "$ORIGINAL_SOURCE_ROOT" --baseline-source-root "$BASELINE_SOURCE_ROOT" --out ordinary
python -B test_terminal_guards.py --inputs inputs --source-root "$SOURCE_ROOT" --original-source-root "$ORIGINAL_SOURCE_ROOT" --baseline-source-root "$BASELINE_SOURCE_ROOT" --out ordinary
python -B verify_independently.py --inputs inputs/integrated-pending/inputs/original-preview/inputs --actual-inputs inputs/integrated-pending/inputs --terminal-inputs inputs/actual-terminal --source-root "$SOURCE_ROOT" --baseline-source-root "$BASELINE_SOURCE_ROOT" --result ordinary --out ordinary
```

Repeat with `-O` and output directory `optimized`, then compare `ordinary` and `optimized`. `manifest.json` hashes every payload except itself. Its external hash belongs in the publication receipt. No source edits, CI polling, external publication or release were performed by this report preparation.
