# Final current-head verification receipt

PR: https://github.com/c933103/AN-Paint/pull/62
Head: 21f659e2c0a23e10273cdb13efdcf642375eac1f
Base: 6a77442847e385742ab274b059cb4d022c364e08
GitHub CI merge commit: 7d5b7ceac986376e6afe53848be503ba447e717d
Verified identical head/merge tree: 267d43b3a7f9deb296346e19f57168c68101372c

Run 38349567326 completed successfully, attempt 1:
https://github.com/c933103/AN-Paint/actions/runs/38349567326
All four jobs passed: Regression tests and lint; Build APK and corresponding
source; Exact-script resource generation; Emulator API 35.

Downloaded JUnit receipts show 948 JVM cases, zero failures/errors/skips.
The two complete attached JUnit suites include:
- russianCropPreviewKeepsCountsAndWarnsThatAttachedImagesMove[30]: passed
- russianCropPreviewKeepsCountsAndWarnsThatAttachedImagesMove (API35): passed
  Each invocation checks real Russian Android getQuantityString for counts 0–20,
  preview dimensions, count-case wording, decoded newline and corrected warning.
- cropReflowsAttachmentsAndAnInvalidBatchIsAtomicWithUndoRedoAndPersistence:
  passed, including the added invariant that all anchor/edge attachments remain
  unchanged while the cropped parent's attached image moves.

The eight strict API35 partition summaries contain 108/108 expected completed
tests, with no missing, unexpected or errored test identities. This is the normal
current-platform suite; it does not establish Russian crop-dialog visual layout,
screen-reader output, physical-device behavior, or the API30 installed matrix.
The exact-script summary binds its successful clean/incremental probes to the
same reviewed tree. Android lint passed. APK/source and test-APK build passed.

Exact-head Codex reported no major issues:
https://github.com/c933103/AN-Paint/pull/62#issuecomment-6138677150
Independent corrected-source linguistic/context receipt:
https://github.com/c933103/AN-Paint/pull/62#issuecomment-6138662274

Original artifact IDs: regression-and-lint 11790638281 (79,305,672 bytes);
API35 11790064660 (10,388,621 bytes); exact-script 11790426453 (6,181 bytes).
These selected receipts preserve the relevant results beyond CI artifact expiry;
full original artifacts remain attached to the run under its retention policy.

The app PR is still draft and unmerged at verification time. No application source
or tests changed after the reviewed head. No whole-locale or release acceptance.
