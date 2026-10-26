# Nynorsk save messages: terminal PR-head gates

[PR #173](https://github.com/c933103/AN-Paint/pull/173), exact reviewed head `2d940e411829f991b3399c1fdb572dd12b0ad44f`, tree `6bb4fa11534149df7f8f58cb3d21faf2b802089f`, against `develop` base `d0e4a3868c376bb857be8ca9762e7ef5ed31cbd4`.

[Run 40270220462](https://github.com/c933103/AN-Paint/actions/runs/40270220462) completed **success**; all six selected jobs passed. [The exact-head Codex code review](https://github.com/c933103/AN-Paint/pull/173#issuecomment-6408393821) found no major issues. The extra review request remains separately observed; neither its running state nor the stale optional security lane is represented as an exact-head acceptance or invented required gate.

## Independently checked artifact results

- JVM: **1,344 unique cases passed**, zero failed/errored/skipped, across 143 JUnit XML reports. The new compiled-resource and real Save/Export/Share dialog tests passed, as did the Nynorsk real-export filename/dirty-state test. The eight reviewed strings are unchanged by the test lifecycle fix.
- Hosted Python: **1,357 run, 1,355 passed, 2 skipped**, exit 0. The non-verbose log does not name the skipped tests; their identities are not guessed. Local ordinary and optimized suites separately passed all 1,357 with zero skips, as recorded in r03.
- Lint XML: **zero issues**; Python/JVM/native-preparation/lint phase command exits all 0.
- API35: **74/74 native** current-source SDK-eligible identities and **45/45 app** identities across the complete composed union. All required phases, both job groups and exact source-test digests were revalidated. No unexpected, missing, failed or timed-out native methods. The device identity matches the previously verified APK, corresponding source and test-merge tree.
- Artifact digests, full case names for the focused JVM suites, phase counts and source identities are in the two JSON receipts. Earlier exact APK/source/compiled strings/signature and 13-probe resource-generation receipts remain at [r03](https://github.com/c933103/AN-Paint/tree/eb868ea209dff1059d5b739afff55265173a8ad6/records/localization-review/2026-10-26/nynorsk-p0-save/r03).

The superseded first-head P2 finding and cancelled CI run remain preserved in r03; no cancelled run was relabelled passed. Current-head gates support merge after a final unchanged-base/head check; this is **not a postmerge receipt**. Subsequent develop CI must be identified separately.

This eight-value batch is bounded AI linguistic/static acceptance plus the stated compiled/JVM/API35 regression evidence, **not native-language, whole-Nynorsk, physical-device, layout or release certification**. Nynorsk remains partial with 77 P0 entries missing after these additions. The 59/112 scope distinction and all #56/#159/#113/Help/release holds remain unchanged. The report snapshot stays pinned to d0e4a386. No release.
