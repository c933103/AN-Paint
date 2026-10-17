# Exact-head validation update, 17 October 2026 at 08:30 UTC

Source head remains e434c5e779183a017ca9153e688dc77a79a0fc39; tree a39746ee5b7bb4d51bcd66f88697e26a0adf05ce. No code, translations, assertions or deadlines changed for these reruns.

- Local normal aggregate: 849 tests pass. The retained first optimized aggregate had one 10-second subprocess timeout in the unchanged instrumentation-matrix negative-control test. That exact test passes unchanged, followed by a complete unchanged optimized rerun: 849 tests pass in 194.724 seconds. The original failure remains in the earlier evidence snapshot.
- Hosted run39014409987 attempt1: build, resource graph, Python contracts, Android lint, both API35 groups and the disjoint aggregate pass. JVM step misses its existing 12-minute deadline, so the run is not accepted.
- Retained JVM artifact: all 108 JUnit suites / 1,090 cases completed with zero failures, errors or skips. This includes 24 resource/dialog boundary cases over API21/30/35 and 11 pure formatter cases. Gradle subsequently records BUILD SUCCESSFUL after 13m48s and exit_status=0. That late completion does not erase the failed deadline gate.
- Requested only the failed job again on the unchanged source and deadline. Attempt2 is running as job117352665472; its outcome is pending.
- Exact-head Codex code review passed (receipt6231323104). Security's last completed receipt is for db076197, so it remains stale. Manual exact-head request6231301895 has not been acknowledged. This is not merge-ready.

The selected diagnostics ZIP retains all JUnit XML, complete phase logs/timings and Gradle profiles from original artifact12095285064. The original 79,721,771-byte artifact was downloaded and SHA256-verified as ae2185482858582b37b8f5307b353596a8a8573f778e4c1c95e0487244908289. Screenshots and unrelated bulky reports are not duplicated. The JSON receipt binds test counts, archive hashes and local rerun commands to the source head.

The earlier immutable evidence snapshot is a1d6b299d5a7e6632de06662406b80912a894f9d. It records the full source/compatibility audit and preserves earlier failures. This update supplements it without rewriting that history.
