# PR31 final current-head verification packet

Source: `083cd7b955836f88a0822f86f734edce9bfb6e06`. Tested merge: `08ad8d503f60887b076cad9ac759050a13170d56`, whose complete tree exactly matches source tree `16c10eaa44608e0cdfb328400506a172f9b867e9`. Full remote source tree verification covered 1,207 leaves with no mismatch.

[Run 37943376051](https://github.com/c933103/AN-Paint/actions/runs/37943376051) passed all three required jobs. Hash-verified artifacts contain:

- All 700 JVM tests across 71 suites, zero failures/errors/skips, including all 37 Commons executions. Lint XML reports zero issues.
- 336 Python contracts. Recorded phase wall times are 50.876s Python, 297.249s JVM, 175.467s lint and native dependencies; every exit status is 0. The 20-minute outer cap and 2/12/6-minute phase bounds are unchanged.
- All 93 API35 installed checks: 74 native Paintroid, 17 ordinary app, 1 accepted-credit seed and 1 independent restart verification. No protocol errors, missing tests or timeouts. Ordinary app invocation 149.664s under its unchanged 180-second cap.

## Exact review boundary

[Code Review](https://github.com/c933103/AN-Paint/pull/31#issuecomment-6082822747) reports no major issues at current 083cd7b. The [summary](https://github.com/c933103/AN-Paint/pull/31#issuecomment-6081543893) reports completed Security at preceding 5f1098b; no distinct 083cd7b Security run is claimed. Final readback found no pending rows, inline review threads or review submissions. Original exact-head re-review requests were sent; none were repeated and no state cycling was used to change labels.

`head-equivalence.json` verifies exactly five changed paths since 5f1098b. The workflow and contract-test file are byte-identical after normalizing only the two displayed phase names. The other three changes are explanatory evidence Markdown, the new host-test log and workflow-equivalence JSON. Production Kotlin, all resources/fonts, timing helper, task commands, order, conditions, workers, permissions, deadlines and artifact paths are unchanged. The final merge gate must assess this documented boundary rather than claim an unrun Security result.

## Durable evidence

The bounded ZIP retains all JUnit XML/test identities, lint reports, local Gradle profiles, raw phase/job logs, UTC/timing files, all installed invocation/restart records, final review snapshot, exact-head equivalence and original-artifact hash inventories. Only unrelated rendered previews and large system logcat are inventoried rather than duplicated. The source/merge IDs, original hashes and bounded archive SHA256 are recorded in `summary.json`.

This evidence-only branch's inherited source snapshot is historical; use the explicit source commit above. Earlier b0cc764 aggregate timeout attempts and the successful 5f1098b phase run remain preserved separately. API30/35 JVM probes are not two installed-emulator runs. No new physical-device, TalkBack, fluent-language or layout acceptance is claimed. Final current-develop integration and merge are separate checks.
