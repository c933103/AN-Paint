# Separate required CI phases after measured aggregate timeouts

## Evidence and scope

Source `b0cc76430727bacefee71faf0f0a33d0b12ada0f` completed all 330 Python and 700 JVM tests in two attempts, but both exceeded the single 12-minute `Run local checks` budget during later lint analysis. Neither attempt is a lint pass. No third unchanged retry was started.

The [durable retry record](https://github.com/c933103/AN-Paint/tree/917b9badf1ab85c9d7321c989c0c7309c5bcffca/verification/commons-import-changes-2026-10-09/ci/retry) retains every JUnit identity, source/merge mapping, exact artifact hash, raw log and reference comparison. PR30's successful checks reference took 697.178 seconds from Python start through final lint, leaving only 22.8 seconds below the aggregate limit. Its separate installed test failed, so that overall run is not called green.

Both PR31 attempts and PR30's checks reference restored the same dependency/native-source cache, without compiled native/JVM outputs. Native configuration to production-Java log spans were 248.802/247.508 seconds for PR31 and 194.908 seconds for PR30; the native sources/settings did not change. These are overlapping, potentially buffered log-emission markers, not exclusive task CPU times or attribution to a specific runner cause. PR31 retry's 700 JVM tests sum 277.804 seconds, with the eight new translation-test executions taking 1.070 seconds.

## Correction and retained gates

Keep the same `Regression tests and lint` job and unchanged 20-minute outer deadline, separating:

1. All Python contracts: 2-minute deadline.
2. All Paintroid JVM regression tests: 12-minute deadline.
3. Complete app Android lint, including its x86_64 native-build and library/test lint dependencies: 6-minute deadline.

Every existing task, assertion, variant expansion and report path remains required. Gradle still uses `--no-daemon --max-workers=2 --console=plain --continue -PnativeAbis=x86_64`. No filter, exclusion, lint suppression, native-object/JVM cache, `continue-on-error` or changed installed-test deadline is introduced. Each phase runs after an earlier failure unless canceled; failed phases retain their nonzero status, so later success cannot make the job green. The unchanged outer deadline remains a hard cap even though the individual maximum phase allowances need not all fit simultaneously. These maxima do not guarantee that all phases and artifact upload finish before that cap; actual hosted timings must establish whether the split fits.

The small Bash wrapper preserves live stdout/stderr and nonzero command or log-write status. It records UTC start/end markers, elapsed/user/system time and exit status below `build/reports/ci-phases/`. Missing end markers after forced termination are incomplete evidence, not success. Gradle `--profile` adds local performance reports under `build/reports/profile/`; no external Build Scan is requested. Both paths join the existing always-uploaded artifact. Actual new phase costs and final Kotlin/runtime/lint acceptance require the new exact-head hosted run.

## Verification and source references

Six focused host tests execute the real wrapper and actual workflow command strings with bounded stub commands for both debug and release. They cover successful commands, exit 7/9 with a successful tee, stderr preservation, log-write failure, invalid arguments, exact unchanged task lists and failure/cancellation/report contracts. These tests validate shell behavior and workflow declarations; they do not emulate GitHub's scheduler or replace hosted checks.

- [GitHub status-check semantics](https://docs.github.com/en/actions/reference/workflows-and-actions/expressions#status-check-functions): `!cancelled()` deliberately allows diagnostics after failure while excluding cancellation; including a status function overrides implicit `success()`.
- [Gradle command-line performance reports](https://docs.gradle.org/current/userguide/command_line_interface.html#sec:command_line_performance): `--profile` writes local report files; task log ordering alone is not a performance profile.

This CI correction is a separate commit from the two-resource localization change and needs fresh Code/Security review plus all exact-head CI gates. Coordinated integration with PR30 and the final merge gate remain required.

## Measured execution and label-only follow-up

The [verified 5f1098b run and full profiles](https://github.com/c933103/AN-Paint/tree/c79b182ad9229bc6bf00017b1876525a200c4fbe/verification/commons-import-changes-2026-10-09/ci/5f1098b) passed all 336 Python contracts, 700 JVM tests, zero-issue lint and 93 API35 installed checks. Phase wall times were 64.073s, 406.179s and 316.822s respectively. The full checks job including upload fit within 15m07s under the unchanged 20-minute outer bound.

The actual task graph places CMake native compilation in the lint invocation, not the JVM invocation. Its profile reports native build 3m16.05s, main library lint 1m20.56s, and further library/app test lint analyses. JVM test execution is 4m30.10s. These task durations overlap and are not additive wall time. Lint's 316.822s phase wall time leaves 43.178s below its unchanged 360s limit; this is one observed margin, not a guarantee for every runner.

Rename only the two displayed steps to “Run JVM regression tests” and “Run Android lint and native dependencies”, and update the matching contract labels and this wording. Verify all commands, order, conditions, timeouts, workers, permissions and artifact paths are byte-identical after normalizing only the two display names. No state cycling, timeout change or skipped validation. The resulting exact head still receives fresh CI and Code/Security review; the earlier green run remains explicit historical evidence.
