# Hosted runtime result for Esperanto PR124

[Run 39063156079, attempt 1](https://github.com/c933103/AN-Paint/actions/runs/39063156079) completed successfully. All six jobs passed. No runtime correction or rerun was necessary.

The unchanged source head is `57eaa704b7bd7944e5d794cae00a72e7496fd65e`. Actions checked out PR merge commit `66a1a3c189be09b74808f5bcaee05935e3ab409a`; both have the exact reviewed tree `5f0fab23aadd6cc6ecec4233e2fc7a88f7784b24`.

## Exact consumer result

All three source-declared `EsperantoPriorityWordingTest` cases executed under Robolectric SDK33, with zero failures, errors or skips:

- `dimensionsUseCountNeutralLabelForOneAndMultiplePixels`
- `cropValidationReportsAttestedSpellingWithoutWeakeningBounds`
- `cropDialogUsesCorrectedActionsAndRejectsIncompleteInput`

The complete hosted JVM suite has 1,107 test cases in 116 XML suites, all passed with zero failures, errors or skips. Android lint has zero reported issues. The hosted Python suite reports 905 tests and two skips, not full execution of every case; its non-verbose output does not name the skipped methods. This is separate from the previously preserved fully executed local normal and optimized host suites.

The API35 composed report contains all 45 source-declared app method identities, with no duplicates or omissions, and records the same source/run/APK identities across core and position attempt 1. Its native report has 74 expected/completed passing cases, no missing/unexpected/errors. Exact-script generation also passed. These results do not certify Esperanto installed layout, native-speaker fluency, physical devices, large fonts or TalkBack. All nine linguistic holds, 27 wording-only distinctions and thirteen unchanged outside-priority crop occurrences remain open as originally recorded.

## Preserved evidence

[Runtime packet](runtime-packet.zip), [checksum](runtime-packet.sha256), and [JVM summary](jvm-summary.json). The packet includes all 116 original JUnit XML files, complete phase logs/timings, lint XML, exact-script evidence, run/job/commit/artifact metadata, emulator summary receipts, and a verifier. Original review evidence remains intact in the parent evidence commit.

The downloaded regression artifact is `12112976056`, 83,963,349 bytes, SHA-256 `1c1586a8148c5cb46c8ad17d0ca475fc87f3a5eadc6aa4badc3b723aaec5b081`. The emulator aggregate artifact is `12112414256`, 11,340,263 bytes, SHA-256 `47dbb6b0f740cc2097bee628421d0ab396f9bf61ae5e444fac4105c7f9935b45`. Both complete downloads matched GitHub's artifact digests. This compact packet preserves relevant textual results rather than unrelated image/report assets from the full artifacts; no screenshot inspection or installable release/signature acceptance is claimed.

Run `python verify_hosted.py /path/to/exact/reviewed/source` (and `python -O` equivalently) after extracting the packet. Both modes passed here. This rechecks source identities and recorded outcomes; it does not rerun Android. The packet manifest binds every included file by SHA-256.

No application files or PR readiness/merge state were changed by this runtime follow-up. Parent review coordination remains separate.
