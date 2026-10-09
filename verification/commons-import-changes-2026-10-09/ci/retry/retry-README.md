# PR31 bounded retry and phase-budget diagnosis

At source b0cc76430727bacefee71faf0f0a33d0b12ada0f, run37934848967 attempt2 again timed out during lint under the unchanged 12-minute aggregate step. No third unchanged retry was started. This failure does not erase attempt1 or imply a lint pass.

- Retry: 330 Python tests in62.732s. All700 JVM tests pass across71 suites with zero failures, errors or skips; summed suite time277.804s, wall span278.539s. The eight new translation-test executions total1.070s. Lint reports were not reached.
- Both PR31 attempts and the PR30 reference restore the identical dependency/native-source cache. Native compiler objects, Java/Kotlin outputs and APKs are not cached in this job; each runner rebuilds them. PR29 restores the same hash from the `-build` prefix-fallback key.
- PR30 b37782d checks finished in697.178s from Python start to final lint task, only22.8s below the nominal720s aggregate allowance. Its706 JVM tests sum301.829s and span302.403s. This checks job passed; the separate installed-test job failed, so its overall run is not green.
- Native-configuration to production-Java log spans are248.802s/247.508s for the two PR31 attempts,194.908s for PR30 and194.303s for the preceding accepted develop run. The PR31 native sources and build settings are unchanged. These are overlapping, potentially buffered log-emission markers, not isolated CPU durations or proof of a particular runner cause.
- Main library lint is logged before JVM completion, then app and Android-test lint continue afterward. Both failures show ongoing task progression, not an identified stuck Commons test. The aggregate budget is too close to the measured required workload to diagnose lint independently.

Approved correction: separate required Python(2m), JVM/native(12m), and lint(6m) phases while retaining the existing20-minute outer job. Preserve commands/assertions, no continue-on-error, later-stage diagnostics unless canceled, and full reports. Add timing/profile evidence and contracts. This is a separate source commit requiring new exact-head CI/review; b0cc764 remains recorded as failing its aggregate CI gate.

The archive retains all retry JUnit XML/test identities, full job log, every task/cache marker, original-artifact hash inventory, and both successful-reference raw logs plus comparison JSON. Original retry ZIP:15,495,025 bytes, SHA25696d8b556da81587c85f18257c624cd9683f0c4318241cc23e3462aad2d9f2ef7. Unrelated rendered outputs are inventoried but not duplicated. No layout or physical-device acceptance is claimed.

[PR31 retry](https://github.com/c933103/AN-Paint/actions/runs/37934848967/job/113842099293) · [PR30 checks reference](https://github.com/c933103/AN-Paint/actions/runs/37936204579/job/113838776101) · [Accepted develop reference](https://github.com/c933103/AN-Paint/actions/runs/37926785579/job/113807716496)
