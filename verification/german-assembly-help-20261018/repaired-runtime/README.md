# German assembly Help: repaired exact-head acceptance evidence

Application head: [`2686f35c1c43910f659fdfe48944a61516bd473e`](https://github.com/c933103/AN-Paint/commit/2686f35c1c43910f659fdfe48944a61516bd473e).
PR: https://github.com/c933103/AN-Paint/pull/129
Hosted run: https://github.com/c933103/AN-Paint/actions/runs/39086030171

The run completed successfully with all six jobs passing: APK/corresponding source, exact-script resources, regression/lint, position API35, core API35 and combined API35 gate. The actual PR checkout `83076bcd18fd6d664fdbacf1d586d8e121424498` has tree `05f725b3a5c64acdace799cfb8cb5d5768ce8f63`, identical to the reviewed head.

## Actual regression result

All **1,124 JVM tests pass**, with zero failures, errors or skips across 120 suites. All four `CropCounterpartGuidanceTest` methods passed, including the previously failing German toolbar/position method (0.215 seconds), complete resource values, actual full Help dialog and real batch-crop controls. The readable affected XML is included separately; every JUnit XML file is retained in the packet.

The repaired method exercises the exact German initial toolbar label, first exact placement away from origin, rejected negative/fractional X/Y, unchanged saved project on invalid input and Cancel, valid zero, overlapping exact placement with unchanged other rectangles, absolute Unplace leaving other positions unchanged, origin/collision rules for snapping, conditional snapped gap filling and Undo. Every assertion from the failed head is preserved. The only repair is fixture resource initialization before Activity creation; no production bytes changed in the repair.

The downloaded passing regression artifact SHA-256 is `438503f6ed86fe3806a97808784601ae2be9b27cad68793adb53c4b875e2192b`, matching GitHub's artifact digest. `checks.json` records the artifact/run/job IDs and method durations.

## Code, Security and local checks

[Code and Security reviews](https://github.com/c933103/AN-Paint/pull/129#issuecomment-6243937404) both completed with no findings on this exact head after the draft was marked ready. The earlier manual Code review was also clean; the readiness-triggered results are the current gate evidence.

The final repaired source passes 932 host tests normally and 932 with Python optimization, plus 12 focused tests in each mode. Full AAPT2 resources, exact-script mirrors/link and supplementary changed-test compilation pass. Full local Gradle/Robolectric remains network-blocked; hosted JVM execution above supplies the runtime result. Source/mode verification covered all 1,209 retained application files.

## Historical failure retained

[Immutable failure and diagnosis](https://github.com/c933103/AN-Paint/blob/a16c2dd099eba7a0127cd02710da8602b32f2136/verification/german-assembly-help-20261018/hosted-failure/README.md) remain intact. The failed run had one toolbar-locale fixture assertion failure out of 1,124 tests; its later method assertions did not run. The packet additionally preserves all 120 old-run JUnit XML files alongside all 120 repaired-run XML files, so the old failure is not replaced by the final success.

`verification-packet.zip` contains the exact runner/review snapshots, all failed/repaired JUnit XML, local final logs and source-binding/compile receipts with a per-file SHA-256 manifest. These records stay on a separate evidence ref; the app branch contains no generated evidence.

## Scope limits

This establishes the bounded resource and real-consumer correction. It does not certify a complete German catalogue, native-speaker acceptance, installed German glyph/layout or TalkBack behavior. The ordinary API35 suite passed but does not add those missing German-specific device claims. PR75's broader scope remains open, and PR56 plus all explicit holds remain untouched. Merge decisions remain separate from this evidence.
