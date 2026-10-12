# Independent PR52/current-develop integration review

## Verdict

Bounded acceptance of the source composition. No blocking integration defect found in the reviewed frozen code/test tree. This is not a merge/release recommendation and does not substitute host receipts for exact-head Android/JVM/build evidence.

Reviewed local commit: `f7b22df53d7ccb59863dd2dbf18a74d7405b6009`.
Reviewed code/test tree: `cad5e3baf65ff0e34965e4010b12f4e5f73d8f50`.
Inputs: verified local `accepted-pr52` and `current-develop` snapshots supplied for remote PR52 `2755e30573d6ea2c071a128b6fa2940fc675af1a` and develop `4231edaac45d89c52f51e2b77d0f94a1176ad88c`. Synthetic local commits are not remote publication identities. Later author changes observed during review were verification-only, not source/test changes.

## Independently reproduced checks

- 105 focused host tests passed in 106.074 seconds, including normal execution of production/resource/history guards, font preservation, SDK partitions, actual shell startup/boundary fakes and budgets.
- 89 focused host tests passed under Python `-O` in 61.343 seconds. These exclude only the 16 normal-mode emulator driver tests from the preceding run; no optimization-stripped assertions are relied on for acceptance.
- Independent literal-substitution audit, not the implementation's projection helpers, recovered both full original standalone M02 and M03 production files and their common pre-change whole-file hashes. The recovered files also exactly match the two supplied source refs.
- All six M02/M03/C05 reversal orders restored each of 60 original catalogue files: 360 order/catalogue checks. All 360 missing, duplicated or changed M02/M03 resource-line mutations were rejected. XML comparison independently confirmed that the delta from develop is only the M02 addition in those 60 catalogues plus exactly C05's 17 Hungarian replacements. Both source-ref resource endpoints are recoverable.
- Seven historical fixture files remain byte-identical to their respective input refs. The preserved 247-path producer guard and nine successor-overlap reversals also pass.
- All 14 current font asset files exactly match develop. The exact additive M03 Nôm font delta reverses to the complete accepted PR52 font. Focused tests additionally verify old glyph outlines, metrics, licence/name/global tables and the single added U+8FD4 glyph.
- 329 other production files retain accepted PR52 bytes. No production files are deleted relative to either input. No PR51 colour correction or stopped PR53 production/archive work is introduced.
- 115 of 116 accepted Kotlin JVM/instrumentation source files are byte-identical. The sole changed existing file is `CommonsCopyCreditErrorTest.kt`: its already-merged M03 test rename and typed-resource expectation replace the old oversized-response literal while retaining the separate field-limit assertion. Its accepted M02 mixed-Korean HTTP expectation is preserved. Both additional M03 Kotlin source files are exactly pinned to develop.
- Independent synthetic receipts establish API21/24/30/35 selected app counts 0/0/22/30, suppressed counts 28/28/6/0 and app budget totals 0/0/630/1050 seconds. API21/24 retain `success: null` and the explicit not-run status. A further 220 independently constructed missing/extra/duplicate/renamed/failed/skipped/source/SDK/budget mutations were rejected, including new eligible legacy ordinary/dialog cases and stale dialog reports.
- Bash syntax and source/test `git diff --check` pass. The complete diff has one inherited extra blank line at EOF in the preserved historical `combined-about.1783e798.kt.txt` evidence file; it is not a new code defect and should not be rewritten merely to clean historical evidence.

## Semantic review

The single `commonsMetadataReason` helper uses two distinct typed branches and the unchanged verbatim fallback. HTTP status remains an ASCII decimal string. Both Copy-credit and insertion translate only inside their existing alive UI callbacks. Unrelated/provider failures, the distinct attribution-field limit, original request host/query language, redirect policy, response-size boundary, disconnection, cancellation, draft retention and late-result cleanup are retained. Literal text classification is not introduced.

The accepted dialog production files and installed tests remain byte-for-byte preserved. Lifecycle listeners, native button instances, rotation and dismissal behavior are consequently not replaced during conflict resolution.

The harness keeps the accepted five-method API35 dialog phase, exact disjoint source union and failure propagation while retaining PR40's manual legacy workflow, ABI checks, startup command choices and fail-closed zero-test omission. Ordinary/gallery/dialog failure still withholds restart, while vertical diagnostics continue. No failed/skipped/missing phase can satisfy a successful union.

Budget reconciliation preserves all existing phase limits and the accepted 300-second dialog phase. The controlled API35 continuing-failure envelope is 2,482 seconds; the 43-minute execution and 53-minute job caps match documentation. API30 remains 1,669 seconds in the modeled path. These are explicitly controlled cancellation budgets rather than universal liveness guarantees.

Historical tests are adapted using exact, pinned reversible changes rather than rewritten historical fixture hashes. The original producers remain independently reconstructable, so accepted assertions are not silently replaced with a looser merged-source expectation.

## Other observed evidence and limits

The author-run logs were inspected and report baseline `568 tests / OK` and frozen candidate `636 tests / OK`. These are separate from the reviewer-executed runs above. The full-host log's synthetic failure diagnostics are expected negative-fixture output, not aggregate failure.

No Android compilation, JVM execution, installed-device run, rendered screenshot review or new linguistic acceptance was performed by this review. Exact remote successor identity, hosted build/JVM/lint/source-generation results, final installed app/native union and required independent hosted review remain to be established before a merge recommendation. Existing colour usability limitations, physical-device/TalkBack coverage and wider locale acceptance are not resolved by this composition.

## Evidence

- `independent_check.py`, `independent-preservation.json`, `independent-preservation.log`: independent source/resource/font endpoint checks and source bindings.
- `independent_sdk_check.py`, `independent-sdk-receipts.json`, `independent-sdk.log`: synthetic SDK receipts, 220 negative controls and budget outcomes.
- `focused-normal.log`, `focused-optimized.log`: reviewer test outputs.
- `candidate-vs-develop.diff`, `candidate-vs-pr52.diff`: inspected code/test diffs.
- `independent-preservation-invocation-error.log`: retained first invocation error (empty Git pathspec), fixed only in the review script before the successful complete run.

No production source was modified and no remote state was changed by this reviewer.
