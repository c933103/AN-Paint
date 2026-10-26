# CA/RO P0 completion — local implementation evidence

Source PR [178](https://github.com/c933103/AN-Paint/pull/178), exact head `93f27ed172cc730c80ed7a2ffbcacc1b0c04383f`, tree `571ec84860cb837ae8376f72d0becfb8fd2b7b6d`, base `ce796879f4568a27b9d905a8e8db639dd0a93a30`. All 12 changed/new files were byte-read back at the new commit, the entire 1,379-file remote tree was reconciled with the baseline, and branch head was verified before PR creation. The PR was created draft, marked ready, and one exact-head Codex request posted at comment 6418586329.

## Actual local results

| Execution | Tests | Failures/errors/skips | Time |
|---|---:|---:|---:|
| Focused ordinary Python | 58 | 0/0/0 | 3.667 s |
| Focused optimized Python | 58 | 0/0/0 | 4.023 s |
| Full ordinary Python | 1,398 | 0/0/0 | 210.406 s |
| Full optimized Python | 1,398 | 0/0/0 | 204.379 s |

Full runs are separate actual executions; all 1,379 bound input file bytes/modes stayed unchanged across them. Raw logs, exact commands/hashes and inventory are retained in `host/`. Deliberate instrumentation-metadata fixture JSON following unittest OK is synthetic host-test output, not an actual device failure/pass.

Independent audit separately joined all 110 final values, checked all 300 inherited pairs and 1,376 baseline Git blobs, reproduced the two XML files/fixture/approved manifest exactly, and ran the nine new host tests normally and optimized. Its publishable receipts are under `independent-audit/`. No concrete defect was found. The five-method JVM test was statically traced to real memory/recovery/encoder consumers and bound to the exact fixture; the zero-budget assertion arms the existing failure shadow so a compress-before-budget regression cannot pass silently. `jvm-static-binding.json` retains this preparation refinement. **No local Kotlin/JVM/Android/device execution is claimed.**

The actual PR workflow is [40340230583](https://github.com/c933103/AN-Paint/actions/runs/40340230583), initially running; exact-head Codex and hosted required checks remain pending in this record. Later terminal CI/artifact and actual postmerge evidence must remain separate, not inferred from local host results.

This batch implements only the 110 reviewed missing values. Ten no-current-consumer holds, all prior values, paired 120/60 oracle, P1/frozen/global59/112, inherited Valencian routing and PR56/113/159/Help/archive/release boundaries remain unchanged. No native-human, whole-language, physical-device/layout certification or release.

## Forward log-hygiene correction

The two full-suite display logs replace a generic Python interpreter installation prefix in an expected duplicate-ZIP warning. Results and raw-log identities are unchanged. `log-hygiene-correction.json` records exact old/new hashes; raw hashes in host receipts identify the original logs, not these sanitized display copies. The original immutable record remains historical.
