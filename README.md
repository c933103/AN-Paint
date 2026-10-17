# Emulator readiness deadline regression evidence

Source: [37e81b351fc197d6d6e3a04a0df9639e484dbf70](https://github.com/c933103/AN-Paint/commit/37e81b351fc197d6d6e3a04a0df9639e484dbf70)
Parent: 0f9ae261aa83dfcb5007cbabfab6cacabfb5790c
Tree: a1856f32503dce470d606ee65b88a5d1c92f0995

The one-second hung-service test could spend its entire budget scheduling the initial progress log, before any ADB process started. Production correctly returned deadline exit 124, but the test incorrectly required evidence from the unexecuted probe. The original assertion is reproduced by selecting that scheduling boundary.

The repair changes only tools/test_ci_emulator.py. A controlled test-shell clock independently selects the running-probe path and the at/past-deadline path. GNU timeout still runs for real. Assertions require actual child startup and termination, observed 1s timeout and 1s kill-after arguments, real elapsed time from 1 to under 4 seconds, exactly one timeout result, and no probe at or after an expired deadline. No production script, deadline, Turkish resource or workflow is changed.

## Verification
- Final normal host suite: 866 tests passed in 213.566 seconds.
- Final optimized host suite: 866 tests passed in 218.919 seconds.
- Focused optimized readiness and phase-budget contracts: 13 passed.
- Repeated real timeout and deterministic boundary tests: 40 passed.
- Negative controls: removing the deadline guard, removing timeout, and increasing the timeout from 1s to 2s each fail. The timeout-removal control ran in an isolated session and its remaining processes were explicitly killed.
- Remote tree comparison: exactly one changed blob; all 1,180 tracked blobs accounted for, no additions/deletions or executable-mode changes.
- Local JVM, lint, APK and emulator execution were not run. Exact-source hosted gates remain required.

The ZIP contains logs, compact receipts, reproduction scripts and the reviewed patch. Logs intentionally include expected negative-control failures and synthetic instrumentation-error output from passing behavior tests; summary.json distinguishes their meaning. The evidence manifest hashes this packet's files, not the application source tree. This dedicated evidence ref is not an application merge candidate.
