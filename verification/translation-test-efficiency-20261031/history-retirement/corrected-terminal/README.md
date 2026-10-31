# Qualified retirement delivery and observed work reduction

PR #252 head 01d4d7ede7f6730ed437b4ebb0cc2984dab9fc38 passed all six required jobs in run 41208820555 and automatic exact-head Codex code review (summary comment 6543971764; no findings). Security summary still refers to the previous head and has mergeGateEnabled=false; it is not claimed as current-head review.

Merged to actual develop 6efaa3b1f4baf955cd5da54b6a4de075a10c0084. Actual merge tree bd629dba318179f7bce59270978612a7a2eb05ac equals the qualified candidate and tested synthetic merge 8b480928e3ca20719f8b36abe7320814b4a9c51d. All 1,615 candidate leaves were verified earlier.

- Python: 2,000 tests, no failures/errors, two existing optional skips.
- JVM: artifact XML parsed, 1,860 cases with no failures/errors/skips; actual public selection/wrap all-offered-language check passed in 3.759 seconds.
- Emulator: native 74/74 and app 49/49 passed with matching source/run identities.
- Build, resource generation and lint passed.
- Regression artifact 13046478337 SHA-256 4f993112d6706bb514db7f90c554aa6d684d7460dcb65dcc4e357c60e5e7dfc3.
- Emulator aggregate artifact 13046012500 SHA-256 b4a264b2677b7c220effaede1295565bb1d452e333b6b623599b8331e40d7045.
- Original run 41205629788 remains FAILED (obsolete source-count guard). Its passing JVM phase is not an overall pass. Focused correction evidence is retained separately.

## Existing hosted observations, not new benchmarks

| Source | Python cases / unittest seconds | JVM cases / timed step seconds | Regression job first-to-last log |
| --- | --- | --- | --- |
| #250 f74981b | 2,086 / 1,496.544 | 1,962 / 1,155.445 | 2,986.632 s (49m46.6s) |
| #251 0acbc50 | 2,070 / 1,192.768 | 1,956 / 1,083.293 | 2,582.060 s (43m02.1s) |
| #252 corrected 01d4d7e | 2,000 / 1,269.181 | 1,860 / 980.591 | 2,552.608 s (42m32.6s) |

Observed #250-to-#252 job difference: 434.024 seconds / 14.53%; Python 227.363 seconds / 15.19%; JVM timed step 174.854 seconds / 15.13%. These are different hosted VMs and source revisions, not a controlled causal benchmark or promised global speedup. The same dependency and native compiler cache keys were restored, but cache keys do not equal identical runner state. #252 Python was slower than #251 despite fewer tests. JVM step includes Gradle overhead, not only test case execution; job span includes preparation/native/lint/upload. The #250 successful regression job is used, not its unrelated failed emulator job/retry. No extra timing runs were launched. Earlier 45.8-second / 14.3% affected-module comparison remains one paired local observation, distinct from these full hosted observations.

Active current-localization payloads across #251/#252: 137 files / 19,250,531 bytes to 130 files / 15,100,129 bytes: 4,150,402 bytes (21.56%) less. Python suite count falls by 86; JVM count by 102. #250 only reduced maintenance duplication, not execution count. No production resource or workflow edits occur in these cleanup PRs. #249's separate manual correction is not included in these counts.

## Finite remaining scope (planning only)

The remaining 130 JSON payloads divide exhaustively into 24 per-locale files in eight full-catalogue families (4,333,287 bytes), 23 other catalogue/cohort mirrors (8,151,142 bytes), seven cross-cutting review/successor/provenance records (607,640 bytes), and 76 bounded feature/delta/boundary fixtures (2,008,060 bytes). These are scope groups, not a pre-approved deletion list.

1. One family-wide catalogue batch: retire remaining full-catalogue copied approval freezes and repeated cohort consumer implementations after mapping actual behavior and helper/locale setup. A textual scan of 488 matched @Test methods finds 31 repeated normalized body groups and 225 extra copies, but this is not yet a safe-removal count. Preserve meaningful independent semantics, script/alias cases and representative real consumers.
2. One cross-cutting adapter batch: remove predecessor, review-status, held-catalogue and whole-payload digest obligations when their last active consumers disappear. Immutable reviewed source records preserve historical acceptance. Do not replace this machinery with another metadata system.
3. One feature-boundary batch: examine the bounded feature/delta fixtures together. Retain independently specified layout/font/format/provider boundaries and actual consumer regressions; archive copied sentence approval tables. Retained examples include alias cycles/missing targets, raw Android quoting/whitespace, default versus regional-English routing, exact-script tooltip corruption checks, actual RTL/native layout, credit save/size ownership, crop selection/cancel, dither confirmation, flip/undo/airbrush, quality request changes and fill threshold/foreground alpha.

Counts alone do not authorize removing distinct regressions. Current #252/#249 delivery finishes before another PR. The project-wide expansion is reduced, not yet resolved. No benchmark/full-suite run or new framework was started for this planning.
