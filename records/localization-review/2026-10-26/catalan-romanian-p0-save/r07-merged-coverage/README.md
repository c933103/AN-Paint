# PR176 integrated coverage — actual postmerge checks passed

**Actual merge run [40311048893](https://github.com/c933103/AN-Paint/actions/runs/40311048893) completed successfully at 2026-10-26 11:19:16 UTC, with all six checks successful.** This report is pinned to merge [`6a42948a3ac7bad241d502f3b6c18ebf1c0327d8`](https://github.com/c933103/AN-Paint/commit/6a42948a3ac7bad241d502f3b6c18ebf1c0327d8), tree `65afa7b96a83c08e0ae08365166dec0520694356`. The terminal receipt observed `develop` at that merge; later movement does not change this denominator. These are actual postmerge outcomes, not substituted PR results.

[Immutable terminal evidence](https://github.com/c933103/AN-Paint/tree/e9fbc0899ec952b1b5ae95cafb98a4b40f7c5ef8/records/localization-review/2026-10-26/catalan-romanian-p0-save/r06-postmerge-terminal) is separately bound by `terminal-status-supplement.json`.

## Current pinned coverage

- **171 options:** 50,725 containers present; 71,882 missing. P0: 6,702 present / 9,030 missing. English-identical leaves: 7,051, unchanged and not automatically defects.
- **Catalan and Romanian:** each 137 containers, P0 **19/92**. Each has **73 missing P0 values: five explicit no-current-consumer holds and 68 outside this batch**, not newly held or declared defects.
- Twenty missing-only complete values were added. All 254 inherited ca/ro values and all 169 other option rows remain unchanged.

Convenient full tables: [CSV](structural-per-locale.csv) · [JSON](structural-per-locale.json). They are byte-identical copies of the already verified integrated tables, not a new computation.

## Actual merge-run evidence

| Evidence | Verified result |
|---|---|
| Hosted JVM | 1,358 tests; zero failures, errors or skips |
| Hosted Python | 1,381 total: **1,379 passed + two skips**; skipped identities are unnamed in the terminal summary and are not guessed |
| Android lint | Zero issues |
| API35 emulator | 45 source-bound app cases + 74 native cases completed |
| Exact-script generation | 13 probes matched expected outcomes, including one deliberate reserved-variant rejection |
| Source/APK | Exact merge/run and archive identity joined; 20 new + 236 prior bounded reviewed compiled values verified |

The APK is CI-debug-signed. Packaged tracked source is verified; extra vendored/generated members are counted, not authenticated by the project Git tree. Artifact availability alone is not used as a test-pass claim. Local/optimized test results are not substituted for hosted outcomes.

## Historical pending evidence remains intact

`integrated-pending/` contains the **complete original 17-file package unchanged**, including its original README, manifest, pending source-identity observation, arithmetic, independent verification and 62 controls. Original manifest SHA-256: `a52598bf8ef983a2016a7e8f0fab6e6843cf368bb7f4ea6cd708e6be6ceabe7b`. Its earlier pending status is historical, not the current terminal outcome. No historical receipt or validator is rewritten to say it had already passed.

The terminal supplement validates six supplied receipts against the same source/run, six check/job identities, archive/APK hashes and twenty exact new compiled-value/review pairs. It does not rerun CI, re-extract artifacts or recompute stable coverage. `verify_terminal_supplement.py` and `test_terminal_guards.py` reproduce these joins and 41 rejected malformed/semantic controls. Ordinary and optimized validation outputs agree.

```sh
python3 verify_terminal_supplement.py --report-root REPORT_DIRECTORY
python3 test_terminal_guards.py --report-root REPORT_DIRECTORY
```

All original linguistic qualifications remain in the [preserved review reconciliation](integrated-pending/review-scope-reconciliation.json). Twenty bounded independent AI whole-value decisions do **not** become native-human, physical-device, layout or whole-language certification because tests passed. No global accepted count is invented. Prior qualified, clause-only, author-only, historical, unmatched and synthetic scopes; NN/DA/NO holds; paired P1/frozen/global59/112 boundaries; PR56 never-merge, PR159 freeze, PR113 hold/retarget, Help callback/archive identity, interrupted-archive and release pauses remain unchanged. **No release was performed.**
