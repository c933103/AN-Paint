# PR123 repaired Japanese Help: terminal runtime verification

## Result

[Android build and checks run 39063700352](https://github.com/c933103/AN-Paint/actions/runs/39063700352), attempt 1, completed **successfully** on 17 October 2026. All six jobs passed. This packet records the actual hosted execution after the bounded paragraph-test repair.

- Application head: `08768f2d9e46e0d2ab873fdd1fefb192db2a456c`.
- Tested merge: `cea2a5068009dc1b0febb0aadd1d646b73df6e03`.
- Tested merge tree and application-head tree are identical: `68c3c19250dec0003c40666603f66fb2a5d84f56`.
- Merge parents: independent develop base `5dba779c904a25bde2ec6d6f8f48eb3cad901a1e`, then repaired head `08768f2d9e46e0d2ab873fdd1fefb192db2a456c`.

## Exact execution evidence

The regression artifact contains **115 JUnit XML files: 1,105 tests, zero failures, zero errors, zero skipped**. Its SHA-256 was independently computed after download and matches GitHub's artifact digest.

- `JapaneseActiveGuidanceTest.actualAssemblyHelpPreservesAllParagraphsAndQualifiesOnlyOptionalDataAndMovement`: passed. This is the exact method that previously failed with expected 7 paragraphs but actual 8; it now verifies the complete reviewed fixture and eight paragraphs while retaining all original optional-data/movement assertions.
- All 3 `JapaneseActiveGuidanceTest` cases passed.
- `AssemblyActivityTest.japaneseHelpModesReachActualHelpAndCurrentPositionLabel`: passed.
- All 21 `AssemblyActivityTest` cases passed, including actual Exact position overlap/independent movement, invalid/cancelled positions, and short-landscape reachability.
- Hosted Python contracts: 903 tests passed (200.743 seconds).
- Android lint, universal APK and matching source build, instrumentation APK compilation, and clean/incremental exact-script resource generation passed.
- API 35 aggregate: **119 tests, zero failures/errors/skips**, across 10 original JUnit reports and 10 execution summaries. The copied `app/dialog-evidence/source-summary.json` is byte-identical to the original 12-test dialog summary and is explicitly excluded from the count. The 119 comprise 112 core-device tests and 7 position-dialog tests.

The terminal jobs were Build APK and corresponding source (117486798622), Regression tests and lint (117486798699), Exact-script resource generation (117486798710), Position dialog API 35 (117488791270), Core emulator API 35 (117488791296), and Emulator API 35 aggregate (117491212284).

## Preserved evidence and boundaries

This packet contains every raw JVM JUnit XML, all six decoded raw job logs, terminal run/jobs metadata, artifact metadata and verified archive digests, relevant API 35 raw JUnit/instrumentation logs and summaries, and an executable artifact-verification script. Large original artifact ZIPs are not duplicated here; their immutable IDs, exact sizes and SHA-256 digests are preserved. `packet-manifest.json` records the SHA-256 of each included file.

The [original failure and bounded repair evidence](https://github.com/c933103/AN-Paint/blob/8f2b1ffe307eca07fbb2ddd32e019d67a547d346/README.md) remains immutable, including the original 1,105-test run with its single 7-versus-8 failure. The [complete Japanese old/new value and linguistic/source-binding review](https://github.com/c933103/AN-Paint/blob/71e3280bc2482708bd6ee523eda22be9d3d16d75/README.md) also remains intact.

This is a runtime verification update only; it changes no application code, fixture, resource, PR readiness or review state. It imports no PR122 code and does not broaden the bounded Japanese Help review into full-language acceptance, native-speaker certification, or complete visual/device coverage. The successful automated device suite is reported at its actual scope. Review and merge gates are separate from CI success.
