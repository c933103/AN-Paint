# Bounded cold universal-build allowance

11 October 2026 UTC+08. Parent `9a780d767df6aa6d11a48f84a52308020d585a9c`, tree `ecbea9e819134fcb5fefe511752507831f987e6f`.

## Evidence

Run [38083526609](https://github.com/c933103/AN-Paint/actions/runs/38083526609) passed generator and regression/lint but failed universal assembly. [Public annotation](https://github.com/c933103/AN-Paint/actions/runs/38083526609/job/114305158663#annotation:8:220449), read without sign-in: “The action 'Build universal APK' has timed out after 22 minutes.” Device jobs never started.

The newly preserved diagnostic artifact 11681701557 is included byte-for-byte as `failed-build-diagnostics-38083526609.zip`: 1,086,850 bytes, SHA256 `ce026bfab5b27b9e0b957ce2f57fe5f2843364a72ad9900fb733fd2394785608`, Git blob `cbe6b8634ad63dc9d9515f8477275b83f6e125c7`. It contains the start timestamp, empty timing file and 25,564,684-byte partial build log, with no completed profile/end receipt. All four CMake ABI task groups are present; the final output reaches `preReleaseBuild`, `mergeReleaseJniLibFolders`, `checkKotlinGradlePluginConfigurationErrors` and `generateReleaseBuildConfig`. No compiler-error/BUILD-FAILED marker is present. These markers locate retained progress; they do not certify compilation or exclude an unprinted error.

The preceding diagnostic-source run 38081755104 succeeded in 861.830s. Its profile attributes approximately 688s to four native-build task groups (223.10+179.45+151.16+134.39s), plus configuration, Kotlin, packaging and other tasks. Timings vary across hosted runs. The immutable cache-key correction remains necessary, but failed universal jobs cannot save their new full-ABI cache; it does not make a cold build fit 22 minutes.

## Deliberate budget revision

- Universal assembly hard cap changes 22→30 minutes; build-job aggregate cap 35→45 minutes.
- 30 minutes is a bounded engineering allowance for observed cold native work plus remaining Kotlin/package work and hosted variability, not a predicted runtime guarantee. The job cap remains an aggregate cancellation policy, not a theorem admitting every step maximum plus unbounded runner setup simultaneously.
- All four ABIs, two Gradle workers, release signing, application/device code, instrumentation phase limits, restart checks, image evidence and failure propagation remain unchanged. No test is dropped and no successful result is inferred from a timeout.
- Build cache statistics are now retained in the existing allowlisted diagnostic directory via a failure-preserving pipeline; no environment/credential dump or compiler-cache binaries are uploaded.
- Previous 22-minute failures remain failed. The corrected source needs fresh Codex review and release/API30/API35 CI before merging.

## Host validation

- 489 full host tests passed in 172.030s, no skips.
- 24 focused cache/build/check/budget tests passed normal in 4.705s and Python `-O` in 1.151s.
- Existing test identifiers are retained; the build-budget contract explicitly acknowledges the intentional 30/45-minute revision. New executable cache-statistics success/failure controls preserve 0/7 exit status and captured output.
- YAML parsing, shell syntax and diff whitespace checks pass. No Android SDK is present locally, so these are not installed tests.
