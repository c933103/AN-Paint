# Failed 0.0.41 candidate: original API30 locale assertion

The frozen candidate `1c9b71afb5f5cbde39bc5fff70630bca1a7a3419` (tree `5fa767ed5bb57364a1ca4bd3cab95cae36187847`) did not pass release verification. Natural [run 39540842251](https://github.com/c933103/AN-Paint/actions/runs/39540842251), attempt 1, is terminal failure: six jobs passed; API30 core and both aggregate jobs failed. Release progression is paused. No upgrade signing, publication-input PR, publication-request change, tag or release creation was performed.

## Preserved actual failure

[Core API30 job 119030652466](https://github.com/c933103/AN-Paint/actions/runs/39540842251/job/119030652466) failed `manchuPickerRibbonToolsAndJpegUseNativeInputInBothOrientations` at `VerticalLocaleDeviceTest.kt:386`: process-wide `Locale.getDefault()` was `en-US`, expected `mnc-Mong`. The preceding Activity-resource locale and saved preference assertions passed. This occurs at the first landscape View-tab check after a successful portrait flow. It is not a picker-selection/resource assertion failure or a transport-only failure.

The original complete uploaded API30 artifact is retained byte-for-byte as `raw-api30-artifact.zip`: artifact 12319937300, 3,350,727 bytes, SHA-256 `c0f21c0db7240b1387b858ba72029fac45bebe023057fd2b515079df62d0feba`. It contains raw instrumentation/JUnit, device/source/APK binding, logcat, collection logs and all four original app-owned export ZIPs including the partial Manchu portrait plus landscape-failure capture. Pull and logcat exited zero. The 15-member Manchu export correctly fails the unchanged 27-member completeness validator after the test assertion.

API35 core and both position jobs passed, but both final aggregates remain failed. The API35 aggregate stopped at its initial guard with the matrix-level `CORE_RESULT=failure` from the failed API30 core; it did not produce a successful union. Its exact job log is preserved separately.

## Diagnosis and boundaries

`diagnosis.md` records the read-only comparison with passing 0.0.40 and exact AOSP/source references. The leading hypothesis is a pre-existing Application-context/process-default locale synchronization gap during Android11 configuration ordering. Relevant locale and vertical-test sources are unchanged from the passing 0.0.40 source. The exact setter caller and repeatability are not established by this observation; no cause is invented, no generic rerun was issued and no assertion was removed.

The raw release regression artifact independently showed 1,264 JVM cases in 133 suites, zero errors/failures/skips and zero lint issues. Hosted Python selected 1,082 cases with two skips and no failures; the non-verbose log does not identify the skipped cases. These passed portions do not make the failed release gate pass. Existing language/device holds remain.

The prior integrated-base postmerge attempt-2 receipt is separate: https://github.com/c933103/AN-Paint/tree/85f0790e2fb6e3b761cd10944f98822a6f797000 . It preserves its own attempt-1 failure and does not substitute for this failed version-source release run.

This evidence write only makes already-collected diagnostic evidence durable. It does not restart release work or authorize signing/publication. Published 0.0.40 is unchanged.
