# Qualified PR #253 and actual-develop observation

PR #253 merged to actual develop `0ae074295045aaa794c755b5ff548067ccbfdfa5`.
Actual tree `879586bacd6091e830a558b3eaad7c744037e0d4` exactly equals qualified head `74dfc11cefb10edb51180fe84af8c8ea2bb8b65f` and tested merge `09a17a8446b3dd4a4515da807cf7920ad97b3c0a`. Actual parents are 5367fe1 and 74dfc11; no unverified combined tree was merged.

Required run 41219486029 passed all six jobs. Automatic Codex code review completed on exact 74dfc11 with no findings or unresolved findings. The security summary still points to prior 3c1204f and has mergeGateEnabled=false; it is not represented as current-head review.

Verified artifacts:
- Python: 1,529 tests, no failures/errors, two existing optional skips.
- JVM: 1,521 XML cases, zero failures/errors/skips. All 63 distinct surviving mapped/representative method identities are present, including all 46 retained representative methods. The all-offered real selection/wrap boundary passed.
- Native 74/74 and app 49/49 passed with matching run/source identities.
- Regression artifact 13050640649 SHA-256 f54b496dad8d01c6f1464f5c8b8dc3cd1ec1272561a1ac598031747dbd922b06.
- Emulator aggregate 13050351118 SHA-256 5df284e41308fcd53790d9ab8973d1f5272ff059bbe457288d9fb7d91a3e1bfe.

Original documentation-head run 41218353683 is cancelled overall after supersession; its regression job failed, and JVM tests were not executed due to compile errors. Those failures and narrow corrections remain separately preserved. No unchanged-source retry or duplicate manual review was used.

## Ongoing work reduced; timings are observations

| Existing run | Host cases / unittest seconds | JVM cases / timed Gradle step | Regression first-to-last log |
| --- | --- | --- | --- |
| Actual develop 5367, run 41212775008 | 2,006 /879.896s | 1,862 /666.864s | 1,790.762s (29m50.8s) |
| Qualified PR #253, run 41219486029 | 1,529 /393.027s | 1,521 /896.026s | 1,601.396s (26m41.4s) |

This batch removes 477 host tests (23.78%) and 341 JVM executions (18.31%), plus 47 active mirrored payloads/12,484,429 bytes (82.55% of the current-localization data at its base). Active payloads are 84 files/2,639,587 bytes. No retired payload was copied into an archive.

The observed whole regression-job span decreased 189.366s (10.57%), and Python decreased 486.869s (55.33%). **JVM was slower**, not faster: timed step increased 229.162s (34.36%), and summed case time rose 537.964→712.628s despite fewer cases. Different hosted workers/regions and source revisions prevent causal attribution; the image version and restored cache keys match, but that is not identical runtime state. Do not claim a guaranteed global speedup or hide the slower phase. No benchmark run was added.

The natural actual-develop run 41222010049 is in progress and owned through terminal. This is not yet a final actual-develop pass. No manual duplicate dispatch was launched.

The remaining cross-cutting residual/script and bounded feature review remains unfinished. Production/resources/workflows are unchanged by this cleanup.
