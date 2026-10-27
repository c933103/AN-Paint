# PR186 — actual merge and superseded natural push

PR186 merged as `4c7c20059030067fa736a0b999e10a08905441a8`. Its tree is exactly `0ad3a1d8e0fb752571027415d268ac65ab301dd9`, matching reviewed head `728ddd062b4fef9e9440978959d85c199da6dccc`; ordered parents are `0c4f732e7c959bb0829bc537b8e1d34e474e4258` and that reviewed head.

The natural [develop push run 40468929333](https://github.com/c933103/AN-Paint/actions/runs/40468929333) is terminal **cancelled** after the next merge superseded it under the workflow concurrency rule. It is not a pass or a refusal. The final composition job is separately recorded as **failed** at its required-prerequisites guard: both CORE_RESULT and POSITION_RESULT were cancelled, so the guard exited 1 before checkout or report composition. This is not evidence that an app test ran and failed. No redundant manual run was launched.

The successor merge `651ab24b2c4dfd26d432daf0d8771fdb179ff013`, tree `d06833e6d8cd1ec700fd03f61858433290808ab7`, has ordered parents `4c7c20059030067fa736a0b999e10a08905441a8` and `941e4a15b1ebf0fd0242cae7765ab75e94922818`. All Ukrainian, Lithuanian and Romanian catalogue blob hashes and modes remain exactly equal to PR186's reviewed source.

The separate [current composed-source push run 40469098669](https://github.com/c933103/AN-Paint/actions/runs/40469098669) covers both PR186 and PR187; it is still in progress at this snapshot. Its final source/APK/runtime verification is coordinated with the second unit and will be linked here when available. Neither successful PR-run evidence nor the cancelled first push substitutes for that result.

[PR186 exact-head terminal review and all six successful premerge jobs](https://github.com/c933103/AN-Paint/blob/18ea7f236654e6cdf922c7ee9fd0ed3cc0796588/verification/uk-lt-ro-priority-20261027/pr-terminal/README.md) remain independently bound to their reviewed source. Full inventory, language decisions, prior receipts, 439 edits, atomic dependencies and exact holds remain unchanged. Counts in that report describe PR186's exact tree, not later combined-language totals. No release, whole-language or installed target-locale layout certification.
