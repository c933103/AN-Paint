# Initial French Help head: retained JVM failure

PR: https://github.com/c933103/AN-Paint/pull/133
Initial head: `aeabd97550d82ea7bff9a0e3e9e5e06e906b2c57`
Initial run: https://github.com/c933103/AN-Paint/actions/runs/39099580752
Regression artifact: https://github.com/c933103/AN-Paint/actions/runs/39099580752/artifacts/12125564277

The initial JVM run executed 1,130 tests with one failure, zero errors and zero skips. All three new FrenchAssemblyHelpTest methods passed. The sole failure was AssemblyActivityTest.frenchCompleteHelpAndActualDragStatusUseImageAttachmentLanguage, whose complete inline expected Help still contained the old seven-paragraph value. Its comparison failed exactly at the reviewed placement/Exact position/Unplace/Undo-Redo edits. The subsequent drag-status assertion was not reached in that method on this run.

The failure is a stale complete-value test oracle, not evidence that the resource failed to update. The production resource exactly matched the new complete fixture in all three new French methods. The repair updates only that existing complete inline expected value. It retains full equality, the real Help toolbar, drag-status behavior and every other byte of AssemblyActivityTest, with no assertion/cap/deadline weakening.

`failure.json` retains the exact failed comparison and stack. Both relevant original XML files are separate. `original-jvm-evidence.zip` preserves every original JVM XML, all CI phase logs/timings, source binding, artifact digest and initial clean Codex review records. Original failure evidence is not replaced by a later pass. This additive evidence commit retains the original complete application tree and all previous evidence. Final-head runtime and review verification remain separate requirements.
