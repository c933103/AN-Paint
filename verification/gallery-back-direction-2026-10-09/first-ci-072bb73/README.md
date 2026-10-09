# First exact-head CI: preserve the failed recreation test

[Run 37956824105](https://github.com/c933103/AN-Paint/actions/runs/37956824105)
tested source `072bb73a88926b3789f4108d9ae1a9b41fbad216` through merge
`1bf8cb55995e1b8d7b0bfef5061c241b9950a01e`. Both have tree
`07e7477916e9acfebd5b57232dc7d3619bd7f19d`; all 1,251 source leaves were verified.

- APK/source and instrumentation APK compilation passed.
- Hosted Python contracts passed.
- JVM: 722 tests executed, two failed. Both are
  `GalleryBackDirectionTest.localeConfigurationChangesRecreateArrowAndRestoreBrowserHistory`
  under API30/35, with `ComparisonFailure` at line 176, the arrow-text assertion.
  The official failed output remains available in the linked Actions run.
  The four other new configured executions are not listed as failures; their detailed
  loop-count records and screenshots have not been independently retrieved.
- Lint completed successfully.
- Installed API35: 74 library + 18 ordinary app + 1 restart seed + 1 restart verify
  = 94 successful tests in the original existing fixtures. These are regression
  checks, not new installed RTL arrow or framework-locale-recreation coverage.
- [Requested Codex Code Review](https://github.com/c933103/AN-Paint/pull/33#issuecomment-6084676360)
  found no major issues at `072bb73a88`; this does not override the JVM failure.

## Retrieval boundary

GitHub artifact `11630490981` is the regression/lint ZIP (31,770,398 bytes), with
reported SHA256 `6a994fbd240d7c5ae41d51c7dd2fada296b4d996143b15259008a0953ddbafa9`.
The artifact download returned an authorized file reference with no local workspace
path. The first transfer returned HTTP403. The documented authenticated file-access
flow accepted that exact reference, but its transfer also returned HTTP403. Retrieval
stopped.
No ZIP hash verification, full JUnit XML readback, comparison values or screenshot
inspection is claimed. The 403 cause is unknown; it is not attributed to the user.

## Raw-log publication limitation

Publishing the unchanged JVM log returned an unexplained tool cancellation. A
read-only check found no blob at the expected content hash; one same-call retry
returned the same cancellation. No explicit owner rejection, reviewer reason or
pending approval identifier was returned. That transfer is paused. The raw log is
not included in this repository record, and was not re-encoded, split, or replaced
with extracted log content. The official Actions run remains the source for the
failure; the factual result summary above does not turn it into a pass.

## Source-backed fixture correction, awaiting verification

[Robolectric 4.14.1 ActivityController](https://github.com/robolectric/robolectric/blob/robolectric-4.14.1/shadows/framework/src/main/java/org/robolectric/android/controller/ActivityController.java#L369-L407)
updates the old Activity's Resources in place before reattachment. Its own context
cache warning appears at lines 477–485. The repository's existing
`DeviceLanguagePickerTest.repeatedOpenAcrossAppOverridesKeepsMountedLabelsAccessibleAndTouchSized`
also documents that such mutations can poison cached locale keys. This is a
source-backed explanation, not a claim about comparison values we could not retrieve.

The replacement replays production save/destroy/create with saved state and a
fresh wrapped locale context. Every arrow, accessibility, vertical-control and
browser-history assertion remains. A separate narrow control intentionally reproduces
the stale locale-key mutation and restores its original configuration. The independent
ten-tag RTL oracle, production three-line fix, installed tests and deadlines are unchanged.

Explicit host recreation establishes save/restore behavior and fresh language wrapping
if it passes. It does not independently establish real framework-triggered locale
recreation. Fresh exact-head compilation and tests are required; the failed original
result is retained independently.

## Later verified readback

The supported Sediment materialization route subsequently retrieved this exact
original ZIP and verified its reported SHA256. The unedited gallery JUnit XML and
140-tag JSONs are now included. Both original failures expected `←` and observed
`→` on the synthetic helper's return to LTR. All 140 tags completed on both APIs.
The [second-run record](../second-ci-f226b4d/README.md) corrects the earlier specific
cache-identity hypothesis: that diagnostic assumption was disproven and removed.
The raw-log Git blob transfer is still paused independently; its contents are not
included or repackaged as a substitute.
