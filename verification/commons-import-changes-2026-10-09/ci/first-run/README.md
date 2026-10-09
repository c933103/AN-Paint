# PR #31 first-run CI evidence

Source head: b0cc76430727bacefee71faf0f0a33d0b12ada0f.
CI merge 5a9514f09c5c2a134ca742444329904e04555265 has the same complete tree 7630701b9ab9193bdde9a20e33c0e425eaa7f56f.

Run 37934848967 attempt 1: all 700 JVM tests pass; regression/lint job fails at the unchanged 12-minute step limit during lint analysis. No lint pass is claimed. The dependency/source cache hit its exact key; x86_64 native code and JVM outputs rebuilt. The new eight translation test executions take 1.039 seconds combined.

The ZIP preserves all JUnit reports and identities, the raw job log, task/cache timestamps and the complete original-artifact hash inventory. The downloaded original ZIP was verified as 15,495,432 bytes with SHA-256 4679cd075708e89d0e68476cf4564b092fae0d279afd9eab162ac9af8e08945f. Unrelated PNG/HTML outputs are not duplicated here; no new layout acceptance is claimed.

A single failed-job retry is justified by the bounded aggregate timeout, with no source change or deadline relaxation. It remains a separate attempt and will be reported separately. It must not replace or relabel this failure.

[Original run](https://github.com/c933103/AN-Paint/actions/runs/37934848967) · [PR #31](https://github.com/c933103/AN-Paint/pull/31)
