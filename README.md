# PR117 + PR119 numeric-display dependency integration

The integrated source has merge parents:
- PR117 `a5e3ed03c58f2bf6fde5d5562e873a18df47b55a`
- PR119 `5401d2bd3a8287ac4ce517c0c8e216bdbe8241fe`

Common base: develop `8c08554995f4d07be1b47736746ab2d0771e810e`.
See source-publication.json for the verified final source head and tree.

## Why both changes are required

PR117 formats ImageDimensions.describe() and memoryLabel() with the selected
resource locale. PR119 formats the outer resize budget and five other identified
display consumers with that locale. Either branch alone can produce a mixed
resize caption. Their reciprocal Codex findings are preserved verbatim:
- https://github.com/c933103/AN-Paint/pull/117#discussion_r4303476803
- https://github.com/c933103/AN-Paint/pull/119#discussion_r4303533482

Production is the exact union of both reviewed parents. No extra production
behavior is introduced. The shared Russian/Portuguese host file retains both
source-consumer assertions. The actual resize-budget consumer test now asserts
ten literal complete captions, initial and refreshed, for pt-BR, German, English,
Arabic and Romanian English fallback. Expected memory values are independent of
the production helper. Resource/process locale mismatch remains deliberate.
Queued show/dismiss callbacks are processed before observations, and Cancel must
dismiss without applying. All six actual-consumer tests from PR119 and all PR117
wording, numeric, parsing/safety and native-input tests remain.

The complete local tree contains 1,188 blobs. Seven paths differ from PR117 and
sixteen from develop. Only the shared host assertions and strengthened new
consumer test differ from the exact parent union. No file is removed. Existing
pt-BR wording, Greek changes, all three pt-BR holds and prior receipts remain.
Canonical edit fields, serialization, arithmetic, admission bounds, hexadecimal
values and zoom thresholds remain unchanged.

## Preserved environmental failure, not a test retry

Run https://github.com/c933103/AN-Paint/actions/runs/39049328991 tested the prior
PR117 tree c930f2cc. Position API35 passed all seven selected methods with the
strict partial-position inventory; regression/JVM/lint, build and exact-script
jobs passed. The core job failed before test execution: sdkmanager's emulator
download reached the unchanged five-minute deadline at 21%, exit124 at
16:40:18.5617563Z. Aggregate emulator failure reflects that absent core coverage.
The original core artifact, exact source binding, all job outcomes and complete
core/position/regression job logs are retained. No core pass is claimed and that
old head was not rerun. The new run is justified by real dependency integration,
not a source-only retry trigger. No workflow, timeout or gate was changed.

## Preserved PR119 queued-show failure

The separate PR119 run39050219892 completed 1,089 JVM tests with one failure.
Its NumericDisplayLocaleTest expected a mixed Portuguese caption containing
ROOT-formatted `25.7 MiB`, but observed an empty budget before queued OnShow.
The XML reports unexecuted main-looper callbacks. That exact XML, artifact digest,
job log and synthetic-merge source binding are preserved. The integrated test's
already-reviewed OnShow idle addresses this demonstrated ordering gap, while
literal `25,7 MiB` expectations fix the independent oracle defect. The other five
PR119 numeric consumer methods passed in that run; this is prior-parent evidence,
not an integrated-source pass. No retry of that old head was requested.

## Validation and limits

See test-summary.json for final normal/optimized full host results. Fresh AAPT2
compile/link and supplementary combined Kotlin compilation cover the integrated
production and all numeric/pt-BR JVM test files. Independent review found no
blocking issue. Literal full-caption JVM probes reject a missing inner repair,
missing outer repair and wrong process-default formatting. These probes use an
explicit resource-formatter stand-in and are not Android UI execution.

Fresh exact-head hosted Robolectric, lint, build and installed tests remain
required. Successful prior-parent jobs do not certify this integrated source.
Root owns Codex review and merge, and will reconcile PR119 afterward. This packet
does not claim all app numeric UI, whole-language/native-speaker acceptance,
physical-device coverage, or unrun configurations.

Prior immutable evidence:
- Original pt-BR review: https://github.com/c933103/AN-Paint/tree/fb0c77cb5964df034989c692d39f952d76a73e01
- PR117 numeric repair: https://github.com/c933103/AN-Paint/tree/f9da527b0b37b52e852470e95c19118f2b95e397
- PR117 test-ordering diagnosis: https://github.com/c933103/AN-Paint/tree/d11caac14adb71ca677e989a965bd31fa0700ed8
- PR119 numeric-display repair: https://github.com/c933103/AN-Paint/tree/2dd6e577ae962e460f3614301d2c1a96603cf0ef
