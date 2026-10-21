# Verified current-base translation integration

PR114 head: `384063f65aaeabc08a0f633d795da4fd28d57e76`  
Tree: `b9b148d5d8ef7c7b088500a9c177f9f59304b800`  
Base: `1c9b71afb5f5cbde39bc5fff70630bca1a7a3419`  
CI checkout: `a3824d87d074e09c86d9e7a4894202a0e18c820e`, identical tree.

The head includes the reviewed translation composition `3ff637e6` plus the already-landed base's version metadata in root `build.gradle` and `LOCAL_BUILD.md`. No code/test/generator changes were made in that last composition. This work is backlog integration, not a release or publication. No release action was taken.

## Terminal gates

Both Code and Security review completed without findings on the exact head. The machine-readable review receipt is retained, together with the completed predecessor receipt. [Review summary](https://github.com/c933103/AN-Paint/pull/114#issuecomment-6231085322).

All six jobs of [run39544989052](https://github.com/c933103/AN-Paint/actions/runs/39544989052) passed:

- 1,098 hosted Python contracts; 264.903-second phase.
- 1,311 JVM cases in 137 suites; zero failures, errors or skipped cases; 924.479 seconds under the unchanged 20-minute limit.
- Native lint dependencies: 82.275 seconds. Android lint: 150.640 seconds and zero XML-report issues.
- 13 actual Gradle resource-generation probes: clean debug/release, up-to-date generation, mirror mutations/restoration, source change/stale cleanup, companion addition/removal, reserved-overlay rejection and release-first ordering. All expected outcomes passed; the negative overlay probe correctly returns nonzero.
- Complete API35 union of 45 app and 74 library cases, with no missing/unexpected/error cases. Source, APK and instrumentation inventory are bound to this exact checkout and run.
- Verification APK and corresponding source build passed; the artifact is not a published release.

Focused JVM coverage includes 28 boundary cases (including API21/30/35 resource fallback), 11 formatter cases including present-null behavior, 4 prefix-search cases, 4 native-graphics caption cases, 16 viewport/vertical-text cases, 6 selected-locale numeric-display cases, 5 expanded Czech cases and 9 Unicode-minus cases. Current catalogues and all 18 Ainu/Manchu percent templates remain unchanged; Japanese crop accessibility displays a single percent. Action identity/repeat/cancel, complete warnings, source aliases/plurals/literals, inserted text as data, companion templates, full tooltip/accessibility text and Mongolian suffix shaping all remain covered.

## Integration and continued verification

The ordinary merge `4355869e2e198b5616419291cba225b018444fab` has the identical tree and parents base `1c9b71af` plus head `384063f6`. Its subject is “Integrate general translation handling safeguards”. The natural postmerge [run39547541573](https://github.com/c933103/AN-Paint/actions/runs/39547541573) was running when this receipt was saved; it is not claimed complete here. No release workflow was requested.

## Raw record and limits

This archive retains raw JUnit XML, lint XML/text, timed phase logs, API35 JSON/XML/instrumentation reports, source/APK identity, clean/incremental resource artifact, exact-head review snapshots, composition diff and workflow/artifact identities. Large reproducible APK/source archives, duplicate HTML reports, screenshots and device logcat are not duplicated. The Actions artifact IDs and digests are retained; durable raw test receipts do not depend on those artifacts remaining unexpired.

The first local focused command omitted the tools import path and failed at test import. Its output remains `composed-focused.log`. The corrected command (`PYTHONPATH=tools python -m unittest test_translation_boundaries test_source_text_resources test_exact_script_resource_routing -v`) passed 20 tests; its output is retained separately. Earlier failed/superseded outputs and complete catalogue comparisons remain in the predecessor evidence archive, not relabelled as new-head results.

Scope remains bounded runtime robustness and the executed matrix, not linguistic completeness or universal device/API safety. Arbitrary external exception messages are not translated; provider/argument text stays data. Invalid XML is still rejected. Long tile captions may use a measured prefix shorter than the nonmonotonic optimum, while full logical accessibility/tooltip text stays intact. Current CI budgets were not relaxed.

[Compact raw archive](composed-terminal-384063f6.zip), SHA-256 `9199b77100a3c394e389badbab2083c38797b843c670872f5683ea191a007ae7`.
