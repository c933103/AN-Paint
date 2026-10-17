# Hosted runtime outcome for Indonesian PR125

[Run 39067106836](https://github.com/c933103/AN-Paint/actions/runs/39067106836) reached terminal **success** in attempt 2. All six jobs are successful. Application head `949e8ccb0d60ac2e46da1b30e33069ff56ec8506` is unchanged. Actions checked out PR merge commit `8d9898768ef625f47f4f46eae0dce6630866899e`; both use the reviewed tree `f12e3f31420ab23c8edc67d72607150b796b1571`.

## Executed checks

- All 1,109 JVM cases across 117 original JUnit XML suites passed, with zero errors, failures or skips. Both source-declared `IndonesianPriorityWordingTest` consumer cases executed under Robolectric SDK33: `failedPngAndDerivedEncodersReportIncompleteEncodingAndKeepSourcePixels` and `liveDimensionDescriptionsUseLowercaseUnitsAcrossRepeatedSwitches`.
- Android lint reports zero issues. Hosted Python reports 911 tests with **two skips**; non-verbose output does not identify the skipped methods. This is separate from the locally preserved normal and optimized suites, each reporting 911 tests with no skips.
- Universal APK/source and exact-script resource generation jobs passed. This packet does not independently certify the APK signature or provide an installable release.
- The final API35 composed report has exactly all 45 source-declared eligible app method identities, no duplicates/omissions. Native instrumentation completed all 74 expected methods with no errors, missing or unexpected identities. The final identity combines core attempt 2 with position attempt 1 and binds the same run, source, APK and test-APK bytes.

## Failed first core attempt retained

Attempt 1 remains a failure. It completed native 74, then received 17 ordinary-app individual pass records but lost ADB transport before the final instrumentation result; those 17 records are **not** a successful instrumentation phase. Later core phases were missing/unrun. Device logs recorded adbd host-17 write failure/offline and a new host transport shortly afterward. No app fatal exception/signal was found; the underlying transport-loss cause is not proven.

The initial [failure diagnosis](attempt1-failure.json), [raw/selected diagnostics](attempt1-failure.zip) and [checksum](attempt1-failure.sha256) were preserved before the targeted retry completed. Exactly one core-job retry, with its dependent aggregate, was requested after the original workflow became terminal. No source, gate, deadline or matrix changes were made. Successful build, regression, resource and position jobs were reused.

## Durable packet and limits

[Runtime packet](runtime-packet.zip), [SHA-256](runtime-packet.sha256), [JVM summary](jvm-summary.json). It retains all 117 JUnit XML files, phase logs/timings, lint XML, exact-script results, final run/job/artifact/commit metadata, composed emulator receipts, first-attempt failure summary, and a source-bound verifier. The initial full review packet and first-failure evidence remain intact in this source-preserving evidence history.

The complete regression artifact download matched GitHub digest `7a9d6a66672be8ff80b608a653a7a3874d7d854dbb776b4ddbd0df8a18a994bc` (83,965,295 bytes; artifact 12113648050). Final device artifact 12114860292 matched digest `2f67b6cf829f5ddc1bacdc480f7b4b64eac00d1e3bf34632971532f15b0c820f` (11,389,784 bytes). This packet preserves relevant textual results rather than unrelated image/report assets. No screenshot inspection is claimed.

Run `python verify_hosted.py /path/to/reviewed/source`, also under `python -O`. Both passed here. This checks preserved outcomes and source identities; it does not rerun Android. Every packet member is SHA-256 bound by the manifest.

Four linguistic uncertainty holds and 32 wording-only distinctions remain unchanged. These tests do not certify Indonesian installed layout, native-speaker fluency, large fonts, physical devices or TalkBack. PR56 remains read-only with no duplicate tracker credit. Draft readiness/Codex review/merge belongs to the parent coordinator.
