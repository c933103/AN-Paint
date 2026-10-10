# PR34 release evidence transport correction: source-only preparation

Candidate tree: `bb5e02515760249772e55ac6b0237f6ed8df6a25`.
Intended parent: `739a3dcf1a59785d98a5f5a00f4b76a1b00e6472`.
Actual develop base: `a758daceda1d4fc37c605e50715f892557da9fc8`.

This bounded preparation archive records source, host checks and historical controls. It is not installed Android acceptance. Fresh release-configured API30 and API35 CI, exact method unions, exported-file integrity, original screenshot/reachability checks, APK/source binding and review remain required before merge.

## Two independent corrections

1. The separately reviewed budget snapshot `db713bbf28abdf45311454329b6435b1ce24b62d` retains all seven instrumentation deadlines (930 seconds total) and assertions. Emulator step/job hard cancellation ceilings are 36/46 minutes; Python step is 4 minutes and checks job 22 minutes. Source-bound arithmetic and under-budget/mutated-path negative controls justify the outer change. The ceilings are not target runtimes or universal liveness guarantees. Unbounded host validation/I/O and inherited checks-job sum-of-maxima policy risk remain explicit.
2. A test-only JUnit rule exports only the fixed synthetic evidence through its own MediaStore.Downloads rows. No production manifest, release/debug flags, storage permissions or original test bodies changed. It removes stale owned rows, checks exact owner/path/name and pending lifecycle, bounds and hashes streaming data, and preserves original plus export/cleanup errors. The host accepts only four exact archives and 104 exact data files into a fresh destination, with strict size/member/manifest/hash validation before atomic extraction. The original visual validators remain mandatory.

Both existing and dangling symlink roots/components are rejected by explicit symbolic-link checks and canonical-path checks. A host Java File/NIO control reproduces these path semantics. It does not substitute for compiling or executing the Android helper.

## Source and test preservation

The audit records all 1,473 source paths, every changed path and blob, and the complete Android method inventory. The only change inside an existing Android test file is the Rule import/property; removing those two lines reproduces the old VerticalLocaleDeviceTest.kt bytes exactly. Every other existing app/Paintroid file and the strict direct-ADB runner are unchanged. All host test identifiers from published 739a3dcf remain; six budget and eleven transport methods are added. The previously inherited PR38 host-test rename is already in accepted aa266c2c and is not a composition change; its earlier byte/source receipt remains in the original preparation archive.

The original ordinary/gallery/two-vertical-shard/seed/restart/verify partition and its distinct receipts remain. API30 requires 73 native + 22 app methods; API35 requires 74 native + 25 app methods. The JVM union remains exactly 793 methods.

## Preserved unsuccessful evidence

[Original combined run 38073935029](https://github.com/c933103/AN-Paint/actions/runs/38073935029) is a failure. Its Python Actions step timed out after two minutes; a later process exit with 462 tests in 176.348 seconds and two named optional-Pillow skips does not override that failure. API30 passed its method union but collection failed with Permission denied at the app external-files path; no API30 screenshot acceptance is claimed. API35's raw/source/image inventories passed independently, without crediting a visual review that was not performed for this run.

The earlier local focused harness failure is retained. Its inherited one-second fake deadline could time out an otherwise complete first-shard protocol under concurrent host load. The correction asserts the original 180-second requested deadline and shortens only the intentionally sleeping negative control to one second. The production runner and inner phase deadlines are unchanged.

The real old API35 evidence was also round-tripped through a host-generated transport fixture: all 104 files and 7,127,121 bytes remained identical, and the original 32 locale + 64 reachability checks passed. This validates host transport compatibility only; it is not a MediaStore execution receipt.

## Prior immutable records

- [Original composition preparation](https://github.com/c933103/AN-Paint/tree/a9bec3406779600d47c2c8a3ab36e743138f07a9/verification/pr34-pr41-integration-2026-10-10/preparation)
- [Separate budget preparation and original failed-run evidence](https://github.com/c933103/AN-Paint/tree/191424b803957be1a87ec185d0b6d13e7badfbb8/verification/pr34-pr41-integration-2026-10-10/budget-preparation)
- [Durable progress receipt](https://github.com/c933103/AN-Paint/pull/34#issuecomment-6100914134)

See `receipt.json` and `SHA256SUMS` for exact commands, final test results and archive inventory. Source preparation never implies that the final combined CI has passed.
