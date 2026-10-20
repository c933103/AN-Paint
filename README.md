# Unicode-minus baseline reproduction

Test-only source head: `8ce14f4a25ea242d336b1bb567f8b4cf5cb1878f`.
Base: `7243bac3225fa9aa45be919e2eb3332b9fa5a40a`.
Hosted PR merge source: `d8b6b4771b3075fe6956a829869ea7410dd9d5bd`.
Run: https://github.com/c933103/AN-Paint/actions/runs/39468715598
Regression job: https://github.com/c933103/AN-Paint/actions/runs/39468715598/job/118786812806
Artifact ID: `12286478413`.
Original artifact ZIP SHA-256: `398055c0b5ecd797dd5568091bd707e822eb30fb0e64ab0fcec206430a9bebb7`.

These are unchanged raw JUnit XML files and the JVM phase log extracted from that artifact, before any production fix. The tested production files are unchanged from the base.

## Confirmed failure

On Robolectric SDK21, SDK25 and SDK35, the real Czech `AssemblyPositionDialog` received `−1` via `Editable.replace`, then Apply committed positive x=1. The layout assertion expected image a at `Rect(10, 20 - 210, 420)` but observed `Rect(1, 20 - 201, 420)`; image b was unchanged. Separate filter assertions show `−12` became `12`.

The full JVM phase ran 1,259 tests and had exactly 10 failures, all in the added U+2212 checks: four offered-locale filter tests (SDK21/25/30/35), three targeted filter tests and three real consumer tests (SDK21/25/35). The three native-sign/range/cancel/reopen/valid-coordinate control tests passed. No compiler/setup failure is being counted as the reproduction.

Local focused source contracts passed 3 tests. Full local host suites passed 1,075 tests in normal mode and 1,075 in optimized mode. Local JVM/Android was unrun because Gradle download failed before startup; actual runtime evidence here is hosted.

## Scope and next step

This establishes an accepted-input semantic bug, not a promise to accept all Unicode numeric syntax. Add U+2212 to the shared key filter in every locale so existing parsers can reject it or interpret it as negative. Do not change parser or range behavior. Keep this baseline separate from the fixed-head results, and never merge the expected-red test-only head. The published 0.0.40 release is untouched.
