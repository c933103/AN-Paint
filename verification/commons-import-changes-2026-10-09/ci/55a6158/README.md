# PR31 post-merge completion receipt

[PR31](https://github.com/c933103/AN-Paint/pull/31) merged as `55a6158a9b651871d0d204e52fb34c0f8a20d2a0`. The actual merge tree `16c10eaa44608e0cdfb328400506a172f9b867e9` exactly matches accepted PR head `083cd7b955836f88a0822f86f734edce9bfb6e06`; parents are original develop `8a75b825` and that PR head.

[Automatic push run 37945787725](https://github.com/c933103/AN-Paint/actions/runs/37945787725) reached terminal **success** for all three jobs: regression/lint, APK/corresponding-source/test-APK build, and API35. This receipt is for the real merged commit, not a synthetic PR merge or the separate PR30 integration.

Hash-verified post-merge artifacts confirm:

- All 336 Python contracts and 700 JVM tests across 71 suites passed, zero failures/errors/skips. All 37 Commons executions passed. Lint XML reports zero issues.
- All 93 API35 installed checks passed: 74 library tests, 17 ordinary app tests, accepted-credit seed and independent restart verification. No errors, missing cases or timeouts. Ordinary app invocation: 158.057s under the unchanged 180s cap.
- Measured phase walls: Python 64.778s, JVM 369.612s, lint/native dependencies 295.366s, all exit 0. Each explicit phase deadline and the unchanged 20-minute outer job were respected.
- The ZIP preserves every JUnit XML/test identity, lint report, local Gradle profile, phase timing file, installed invocation/restart record, raw job log and original-artifact inventory. Original hashes and archive identity are in `summary.json`.

The [premerge packet](https://github.com/c933103/AN-Paint/tree/878eea80f343d91413dd77aa97b5e96263f7cd07/verification/commons-import-changes-2026-10-09/ci/083cd7b) retains the exact current Code result, actual preceding Security result and verified name/docs-only equivalence. No distinct 083cd7b Security run is claimed. The older aggregate timeouts and intermediate green run remain separate historical records.

Scope remains the two whole-message import-change notes across 59 scoped tags with 81 explicit incomplete/fallback tags. Provider attribution and existing/user-edited persisted credits remain unchanged. No fonts, PR30 layout files, physical-device/TalkBack acceptance or fluent-language approval are included. Source snapshots inherited by this evidence-only branch are historical; the explicit real merge commit above is authoritative.
