# Verified CI after phase split, source 5f1098b

[Run37940356914](https://github.com/c933103/AN-Paint/actions/runs/37940356914) passed all three jobs at source `5f1098b1a89ea34cfe725e420cfa0e9915dee370`. Its synthetic merge `7c17cd75c27d518620aaacb976f1cd19a28f112c` has the identical complete tree `0587a0f5a601164d3257e78728578d1b2b319d4c`.

- 336 host Python contracts, all 700 JVM tests across 71 suites, and lint with zero issues passed.
- All 93 API35 installed checks passed: 74 native Paintroid, 17 ordinary app, accepted-credit seed and independent process-restart verification. Ordinary app invocation:159.521 seconds under its unchanged180-second bound.
- Exact phase wall times: Python64.073s, JVM406.179s, lint316.822s. All returned exit0. The checks job completed, including evidence upload, within15m07s of start under the unchanged20-minute outer cap.
- The Gradle profiles reveal CMake native compilation in the lint invocation (3m16.05s), not the JVM invocation. Main library lint takes1m20.56s; additional test analyses are also present. The JVM test task takes4m30.10s. Task durations overlap and are not additive wall time. The JVM step's current “and native build” label is misleading about placement; every required task nevertheless completed.

The bounded ZIP preserves all JUnit XML and identities, all lint reports, complete local Gradle profiles, UTC start/end and timing files, each installed invocation and restart boundary, raw job logs, job-step timestamps, and hash inventories of the two original artifacts. Only unrelated rendered previews and the large system logcat are omitted from duplication and remain hash-inventoried. Original artifact hashes and bounded archive identity are in `summary.json`.

This record refers to the source commit above, not to the source snapshot inherited by this historical evidence-only branch. The two older b0cc764 aggregate timeouts remain preserved in adjacent directories and are not relabeled. This is emulator API35 evidence, not a physical-device/TalkBack/full-layout acceptance claim.

PR31 was transitioned once from draft to ready at14:13:45 UTC after these artifact checks. Fresh review outputs and the final current-develop integration/merge gate remain separate requirements.
