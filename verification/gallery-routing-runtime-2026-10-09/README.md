# Gallery routing: current-tree API35 evidence, 9 October 2026

[PR19](https://github.com/c933103/AN-Paint/pull/19) head `a1f9d6d8cf4062c4f764c3436a73ecec21a59d9a` passed [workflow 37920356727](https://github.com/c933103/AN-Paint/actions/runs/37920356727). No test-code correction or rerun was needed for this result.

## Provenance

The workflow captured pre-retarget synthetic merge `cc061ffb8a8982632e06bf46c29b8d2d76c7e8ad`, whose first parent is the former base. Its complete tree `3ac89e305f168a12f55bcf1c2ca898229e8e41a6` is identical to current head and the develop-based synthetic merge `fd4f8f05525a5564f6392d9993cc8f1e44cf500e`. Artifact names retain the actual tested SHA. Both report ZIPs were independently downloaded and matched the official GitHub SHA-256 digests in `provenance.json`. Full ZIPs/APKs are not duplicated here.

## Observed results

- APK and instrumentation compilation succeeded; 675 JVM/unit/Robolectric cases passed, no failures/errors/skips; lint zero issues.
- 93 installed API35 cases passed: 74 native/import, 17 ordinary app, one restart seed and one restart verify. The strict disjoint app inventory is 19/19, with no missing/unexpected/ignored cases.
- All three real gallery-over-editor flows passed: restore and confirm unconfirmed text; restore/cancel without reopening the modal; save A then cancel empty B. Assertions cover task/recipient identity after recreating the covered editor, pixels/selection/rotation/undo, accepted token ownership, further autosave recreation, clipboard/dialog cancellation and actual later Base64/PNG output.
- Each gallery case positively recorded HTTPS CONNECT for the preflight fixture and initial gallery home request at the local rejecting sink. Its 153 lifecycle lines span tasks 36, 38 and 40. Passing teardown asserts zero native acquisition attempts and destroyed/detached WebViews before proxy restoration. This is selected-flow test evidence, not a universal network guarantee.
- Ordinary app execution took 164.552 seconds under the unchanged 180-second deadline, about 15.4 seconds spare. One successful run does not establish repeat-run stability. No timeout, inventory weakening, test exclusion or old CI partition was introduced.
- The unchanged accepted-credit seed/verify partition separately passed, with live PID 5251 verified before external force-stop and absence verified before normal new-process verification. This does not turn the three recreation cases into process-death tests.
- Local Python: 315/315 passed. CI Python: 315 total, 313 passed and two skips. The CI log does not name the individual skips; source has optional-dependency skip sites. There were no installed skips.

## Boundaries

This evidence does not claim physical-device/API30/live-provider/linguistic acceptance. It does not adopt the excluded #18 prototype UI. The original PR19 old-tree evidence remains separately preserved under `verification/gallery-routing-reconciliation-2026-10-09` and must not be confused with this run.

`files.sha256.json` hashes every other file in this directory. `provenance.json` maps full preserved reports and focused raw-log selections to their artifact members. `jvm/summary.json` records totals and hashes for every source JUnit report; only the two focused gallery/recovery reports are copied. Final review/merge decisions are recorded on PR19, independently of this evidence snapshot.
