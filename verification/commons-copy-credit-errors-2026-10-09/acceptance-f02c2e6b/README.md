# PR34 exact-head acceptance and inherited API30 blocker

Head `f02c2e6bfd51eda81b6d16db10322e1f623dcaec`, tree `e27d7c346452912082089f58278e57dcef46a3ab`.
Run: https://github.com/c933103/AN-Paint/actions/runs/38022221410
Tested merge `d4d9db1b83bd6edf4ccc35a0df48aebed866d0af` has the identical tree.

## Result

The strict Korean routing checks pass in both API30/API35 native-resource JVM tests and both actual installed applications. Both installed logs contain all four requested phases with exact mixed/ordinary text, unchanged public identities and real orientation/dimension changes. The seven pinned-toolchain generation stages pass. The full JVM result is 766 passed, no failures/errors/skips. Lint and both APK types compile. CI host result is 382 passed + two optional Pillow skips out of 384; local validation passed all 384.

The overall run is failed. API30 has 73/73 native and 17/18 ordinary app methods passed; the existing GalleryViewport font transition is the sole failure. API35 has 74/74 native, 19/19 ordinary app, and complete one-test seed/verify phases passed. Never substitute these bounded passes for a green combined run.

## Exact API30 comparison

- The viewport test blob is unchanged from develop80c: `d6f3a60a74625172c4c78ef4f3cdd869dac98fd2`.
- In baseline release run 38018126008, the first real 2× French viewport succeeds at 03:09:56.895, reset reaches 1× at 03:09:58.014, and the next requested 2× transition ends after 10s with setting/system/target all 1×.
- In PR34 run 38022221410, the same first French 2× viewport succeeds at 04:08:56.903, reset reaches 1× at 04:08:58.234, and the next requested 2× transition ends at 04:09:08.254 with all 1×.
- The new Korean test passed its final phase at 04:08:19.863. Viewport setup began about 37s later with setting/system/target all 1×. The first French transition and both orientations then succeeded. This matches the inherited synchronization failure signature and does not indicate a Korean text-resolution failure; it is not proof against every possible test-state interaction.
- PR38 head `e97c85186973ad69589ff1adf380df3e378bce84` passes the same sequence in run 38022027780, preserving the real system/app matches, four French/Mongolian viewport captures, original shared 10s deadline and network rejection. It requires five exact private-display added/removal acknowledgments.
- PR38 explicitly documents a limit: asynchronous DMS callbacks can bypass queued synchronous ATMS persistence behind a MessageQueue synchronization barrier. Its helper is conditional on normal FIFO/no intervening barrier, not a portable queue-drain guarantee. Its model retains that counterexample. Exact-device assertions remain necessary.

Filtered baseline, current and PR38 logs are retained alongside the raw API30 failed summary. No assertion was removed, no failure retried unchanged, and no fixture change duplicated.

## Integration decision after this historical run

The reviewed PR38 repair subsequently advanced to `f27d70a925aa659983b25cd875a39b485f44909d`, tree `f6b5c93999c945ef0735efe20c84c045e1c2f8a8`. Its original fixture/counterexample is unchanged; the additional release-label option is documented in CI.md. An explicit candidate combines that source with f02c2e6b, preserving both parents and reconciling the workflow/docs. See [the integration record](../integration-pr38-f27d70a9/README.md). This historical evidence does not establish success of that combined source.

## Artifact/source verification

`summary.json` identifies all five downloaded artifact IDs, sizes and SHA-256 digests. All digests were checked. Every generator log hash matches its summary. `source-verification.json` records 1,339 exact source-file matches and the three existing metadata exclusions (`.gitignore`, `.idea/codeStyles/Project.xml`, `colorpicker/.gitignore`). The source contains the canonical XML and generator, with no generated variant duplicate. AAPT2 confirms all 695 compiled canonical/variant entries match. Gradle FileTree uses Ant defaults, including `.gitignore`: https://docs.gradle.org/current/userguide/working_with_files.html and https://ant.apache.org/manual-1.9.x/dirtasks.html .

The APK uses the CI debug key. This is not upgrade-signing, release-variant verification, linguistic acceptance or supported-minimum-API21 certification. Codex's earlier review request hit its usage limit; no further manual request or PR-state cycling occurred.
