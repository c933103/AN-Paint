# PR #27: automatic post-merge verification

Accepted merge `5bf82b67199aaecbd341a8b150a887f8d60b5567` has tree
`05f9f6aa330f2f1432264938d5d0e41dfe8d86ee`, exactly matching the reviewed PR
head and successful PR test tree. The automatic develop-push
[run 37895625554](https://github.com/c933103/AN-Paint/actions/runs/37895625554)
completed successfully at 07:05:07 UTC on 9 October 2026.

All three jobs passed: APK/source build, regression/lint and installed API35.
The downloaded result archives independently confirm **661 JVM tests**, including
**35 numeric-entry cases**, with zero failures/errors/skips; **0 lint issues**;
and **89 installed API35 cases** (74 library, 13 ordinary editor, one seed and one
post-force-stop verification), with no missing or unexpected cases. The complete
unit and installed case identities match those in the final PR run.

## Artifact identity

| Artifact | ID | Verified SHA-256 |
| --- | --- | --- |
| Regression/lint | 11601090017 | `47f542cd6a361cd40284163c0ffb53623857c9da9b886da57117cab1f18484d0` |
| API35 | 11600453657 | `10567000c68d88b59dafbede36e685aec6fe83e6f659eb8e700c3f8221116086` |

The APK/source and instrumentation archives were produced successfully. Their
GitHub identities and digests are retained in `acceptance.json`; their bytes
were not independently downloaded. No upgrade-signed release is claimed.

## Retained evidence

All 67 original JUnit XML files and the lint XML are in
`unit-and-lint-xml.zip`. `device-results.zip` contains all four runner summaries,
JUnit XML and raw instrumentation logs, plus the accepted-credit process-stop
boundary, complete app coverage and verify status. The manifest files record
every retained member's byte count and SHA-256. `all-device-cases.json` lists all
installed cases; `focused-unit-cases.json` lists all 35 new JVM cases.
`ci-jobs.json` preserves the final job/step status on the accepted merge.

Run `python3 verify_results.py` here to verify retained file identities, archive
inventories, complete JUnit and installed-runner totals and zero lint issues.
The checker passed both normal and optimized Python execution after download.
It validates these results; it does not rerun Android.

The [final PR receipt](../README.md) records the 310 local Python tests, fresh
Code/Security review and prior failed iterations. New numeric-entry cases are
Robolectric tests, with the API21 identity shadow restricted to its source-backed
control. Installed results are emulator regressions. These results do not claim
real-IME, physical-device, linguistic or complete all-language layout acceptance.
Broader AN-W04 work remains open.
