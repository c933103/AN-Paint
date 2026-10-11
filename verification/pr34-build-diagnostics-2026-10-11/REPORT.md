# PR34 universal-build diagnostic checkpoint

Date: 11 October 2026 UTC+08. Source parent: `3835cabbcaf9b3eaa887a705ec1f64cf8fbdd149`, tree `bb5e02515760249772e55ac6b0237f6ed8df6a25`.

## Verified failure

Run [38077813274](https://github.com/c933103/AN-Paint/actions/runs/38077813274) failed universal APK assembly twice on unchanged source. Public GitHub annotations were read in dot's cloud browser without signing in:

- [Attempt 1](https://github.com/c933103/AN-Paint/actions/runs/38077813274/job/114288371508#annotation:8:220799): build18:58:24–19:20:34 UTC.
- [Attempt 2](https://github.com/c933103/AN-Paint/actions/runs/38077813274/job/114293573224#annotation:8:220709): build19:24:40–19:46:52 UTC.

Both annotations say: “The action 'Build universal APK' has timed out after 22 minutes.” Generator/regression/lint succeeded; source/test-APK uploads and device matrices were skipped. Full decoded-log connector reads returned transport errors, so the exact slow Gradle/native phase is unknown. The one failed-job retry is preserved, not relabelled success. No third unchanged-source retry was issued.

## Diagnostic-only change

- Reuse existing timed-phase wrapper for `apk`, preserving pipeline exit status and partial output.
- Add Gradle `--profile`; preserve task, two workers, universal ABI defaults, signing and build variant.
- Always upload only `build/reports/ci-phases/` and `build/reports/profile/`, using the existing pinned artifact action, 2-minute upload cap,14-day retention and attempt-specific names.
- Preserve22-minute build,35-minute job and all device-phase limits. No application, runner, cache policy, signing, production permission or test method changes.
- A canceled build may lack a completed profile/end timestamp. Artifact availability is diagnostic evidence, never APK or device acceptance.

Shared immutable native-cache keys across x86_64 checks and four-ABI builds are a source-level coverage hypothesis, not an established cause. No cache changes are made here. The job ceiling remains an aggregate cancellation policy, not a proof that every step can reach its maximum together.

## Validation

- Full484 host tests passed188.411s, no skips. Some negative-case fixtures intentionally print `success:false`; unittest's final result is `OK`.
-19 focused build/check/budget contracts passed1.168s; the same19 passed with Python `-O` in2.020s.
- Executed debug/release command stubs preserve0/7 exits, exact command tokens and logs.
- A terminated synthetic build retains partial output/start time without a false success receipt; log-write failure remains nonzero.
- YAML parsed, shell syntax and whitespace checks passed.

Host checks do not establish Android compilation, installed MediaStore export behavior, screenshot correctness or the cause of the universal-build slowness. Fresh exact-source review and CI remain required. Merge and release remain held.
