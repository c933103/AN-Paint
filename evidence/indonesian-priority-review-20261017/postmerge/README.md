# Indonesian PR125: post-merge develop verification

The natural [develop push run 39069617890](https://github.com/c933103/AN-Paint/actions/runs/39069617890) completed successfully on **attempt 1**. All six jobs passed. No post-merge retry, source change, gate adjustment or deadline change was needed.

Merged commit `b6a99b41c4390ca6a412e3a1938eb913c59509fb` has the exact reviewed application tree `f12e3f31420ab23c8edc67d72607150b796b1571`. Its parents are the former develop commit `9bff0abd8f7bc04facbb556908b3a6f578c7346f` and reviewed PR head `949e8ccb0d60ac2e46da1b30e33069ff56ec8506`.

## Exact post-merge results

- **1,109 JVM cases**, 117 original JUnit XML suites: zero errors, failures or skips.
- Both source-declared Indonesian consumer methods executed under Robolectric SDK33: `failedPngAndDerivedEncodersReportIncompleteEncodingAndKeepSourcePixels` and `liveDimensionDescriptionsUseLowercaseUnitsAcrossRepeatedSwitches`.
- Android lint reports **zero issues**.
- Hosted Python reports **911 tests with two skips**; non-verbose output does not identify the skipped methods. These are distinct from the fully executed local normal/optimized suites preserved in the original review packet.
- API35 composed coverage contains exactly **45 source-declared app identities**, with no duplicates or omissions. Core and position both executed in attempt 1. Native instrumentation completed **74 expected cases**, all passing with no missing/unexpected identities or protocol errors.
- API35 identities bind the merged source, this run, the same APK/source/test-APK bytes, and the source-discovered instrumentation inventory.
- Exact-script resource generation and universal APK/corresponding-source jobs passed.

## Preserved evidence

[Post-merge packet](postmerge-packet.zip), [checksum](postmerge-packet.sha256), [summary](jvm-summary.json). The packet includes all original JUnit XML, complete Python/JVM/native/lint phase logs and timings, lint XML, exact-script evidence, run/job/commit/artifact metadata, source-bound emulator receipts, and a verifier.

Full downloads matched GitHub artifact digests:
- Regression artifact 12114464869: 83,965,054 bytes; SHA-256 `f9ff62ccaa17af8eae1d0f4df005ef531d906a00e916ba8dedbd0dd631b6ea13`.
- API35 aggregate artifact 12115426820: 11,380,216 bytes; SHA-256 `293c14d657259ee1dc634677750996301b14e3461737363cb7d2ca2520537980`.
- Exact-script artifact 12114856467: 7,831 bytes; SHA-256 `4dac3f825ef981531a09dcbfe486c4f7d549a3de63b998f3958e56521cb066c4`.

Run `python verify_postmerge.py /path/to/reviewed/source`, or `python -O`. Both modes passed here. It rechecks retained outcomes and exact source identities, not a new Android execution. The manifest binds every packet file by SHA-256.

The evidence update is additive to the existing source-preserving evidence tree: all 1,200 reviewed application files and the complete original review/runtime/failure records remain intact. PR-run attempt 1's ADB transport failure remains a historical failure; this separate natural post-merge run passed without retries.

## Limits retained

Four linguistic uncertainty holds and 32 wording-only decisions remain unchanged. PR56 remains read-only with no duplicate tracker credit. No native-speaker, Indonesian installed-layout, large-font, physical-device or TalkBack acceptance is claimed. Screenshots and APK signatures were not independently inspected in this follow-up; this is not a new installable-release certification.
