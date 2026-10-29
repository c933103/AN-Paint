## Current corrected successor — not adopted

Head `19e62e20e5f1862ee107e8a37369694e697a7400`, tree `86cc089101827dfd108838201bb6f7f8343ddddc`, matching tested synthetic `646380fbf8f395b2cf8356d45f54911f97c73c3d`. All 1,606 remote leaves/modes and both changed-file bytes verified. `current-successor.json` records parent review, exact current gates and original failed states. `startup-fix.diff` is the accepted two-file repair of Codex P2 comment 4409332250. The complete same-checkout stale-success reproduction and raw original attempts are reconstructable with `startup-records-manifest.json`.

Original 3cc full local modes passed 2,024 tests each, but its Code P2 and cancelled hosted run are not retroactively cleared: JVM was skipped, core cancelled, aggregate API35 failed. Current 19e full modes began 06:53 after the old owners terminated, with the unchanged 7,200-second local outer owner budget; all internal/CI limits unchanged. Current hosted 40830722346 and exact-head Code are pending. No real two-fork JVM performance outcome exists yet.

---

### Original experiment history (3cc804b)

# Two-worker JVM experiment — not yet adopted

Source PR [#226](https://github.com/c933103/AN-Paint/pull/226), head `3cc804b03205759861f096496e5f5c5507d70f36`, tree `9795047419c1db0c055df2b6e797a7b2b78a6eab`, parent actual merged #224 `956f6b17fc4ab9196bfbe5ca43064c97a8e8179d`. All 1,606 remote leaves/modes and all seven changed-file bytes read back and verified. Only Gradle test-worker configuration, CI observation/test helpers and CI documentation changed. No application/test Kotlin or Java, locale resources, fixtures, workflow command, assertion, filtering, heap cap or deadline changed.

The existing 1,200-second JVM phase passed in 1,188.239 seconds (11.761 seconds headroom). Raw original Gradle profile and artifact-bound diagnosis are retained. Test task 985.020 seconds versus startup 3.451 seconds supports investigating bounded class-level parallel execution, not relaxing the deadline.

The parent read the entire initial patch and independently reproduced its defect: a failed observer could return wrapper 125 while the command-only time receipt still said exit 0. The accepted successor finalizes the observer first, retains both statuses, uses identity/parent-bound pidfds with TERM 1 s then KILL 1 s, and never signals workload processes. Parent read complete successor diff SHA256 d8224809253e4ba59b7959a988b86f2411d4372ffa04b7fa5e406ac0d88b613a and independently passed all ten observer tests in 3.397 seconds before authorizing publication.

Initial six focused failures (unavailable external GNU time and missing Python fixture dispatch), later one broader missing-helper fixture failure, and the initial defective diff remain in original-attempts.tar.xz. The final implementation does not depend on GNU time or skip these checks. Final focused normal 37/11.325 s, optimized 37/12.092 s, broader CI contracts 79/69.177 s all pass. These are not full hosted acceptance.

Collision audit found no proven cross-class report-path collisions; no output paths were altered. The compressed baseline inventory holds all 193 classes / 1,925 test identities and 2,704 PNG/JSON/JSONL paths. The actual experiment must compare the complete sets, not only totals. Baseline input is run 40820454209 artifact 12876111901, SHA256 e24527ea0a949797e73d3fca1fb1fe6819f0c215bf7ef177112ade938469d240.

Fresh full normal/optimized runs began 06:23 UTC in separate exact-head worktrees, unchanged 7,200-second outer local owner budget, no internal deadline change. [Required hosted run 40828822765](https://github.com/c933103/AN-Paint/actions/runs/40828822765) and exact-head Codex Code are pending. Observation records sampled aggregate descendant RSS and observed per-process kernel VmHWM plus host available memory: shared pages can be counted twice, unobserved short peaks can be missed, so this is not an exact aggregate peak or a memory-safety guarantee. Root owns adoption. #224 acceptance/natural postmerge verification remain separate. Release 0.0.41 remains paused.
