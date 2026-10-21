# Post-merge verification complete after one transport retry

The natural post-merge run [39481127358, attempt 2](https://github.com/c933103/AN-Paint/actions/runs/39481127358/attempts/2) completed successfully on the unchanged merge commit `9a7a052d7458cf08f280ead1173c66c2992e4254`. All six jobs are successful. The initial failed attempt remains preserved below and at immutable commit [4e99474d1f05918ae338191ea98d8f4d6611ae3b](https://github.com/c933103/AN-Paint/tree/4e99474d1f05918ae338191ea98d8f4d6611ae3b), not relabeled as a pass.

## Fresh retry verification

- Fresh API35 core job 118841815794 passed. Its raw XML records 74 Paintroid tests and 38 app tests, with zero failures/errors/skips.
- All four expected vertical exports were pulled: 2,917,047 bytes in 0.072 seconds. Dialog pull, vertical pull, logcat and overall collection exits are all 0.
- Core artifact 12293637143 SHA-256: `50c725f58f91fa3a38f138171e3b99bf10d2f74579ed81bd5bbaed1aa3556785`.
- The unchanged transport, screenshot and reachability validators were independently rerun locally on this hash-verified artifact: 104 data files, 32 matrix screenshots and 8 reachability cases / 64 frames passed. Their derived JSON values exactly equal the hosted receipts.
- The four unchanged export ZIPs are retained in `attempt-2/exports/`. They include all required screenshots and native-input receipt data. This is validation of complete content and structured evidence, not a new independent visual review of every PNG.
- The aggregate job 118848300612 passed and explicitly binds the same commit, source/test source and APK hashes. It composes fresh core attempt 2 with retained successful position attempt 1, completing all 45 app tests. Its combined raw XML totals 119 device tests, zero failures/errors/skips.
- Aggregate artifact 12294190644 SHA-256: `3f9df2b841d753ffc656ee32031ce0fb78d4ebbdcd00094d26a975ccaa863772`.
- Build/source, exact-script resources, regression/lint and position results were retained from successful attempt 1 jobs. They were not newly rerun. The post-merge JVM artifact remains the independently verified 1,264 passing tests, including Czech 5, shared numeric 35 and Unicode-minus 9.

No source code, assertion, timeout or required evidence was changed to obtain this retry result. Published 0.0.40 remains untouched. Parent release preparation is separate; this receipt does not claim a new release or installation. The Unicode-minus-specific tests remain hosted Robolectric/JVM consumer execution, not installed-device Unicode paste verification.

## Historical attempt-1 receipt (unchanged below)

# Unicode-minus fix: post-merge attempt 1 and retry diagnosis

PR: https://github.com/c933103/AN-Paint/pull/155
Merged commit: `9a7a052d7458cf08f280ead1173c66c2992e4254`.
Parents: `23e95c76161d8a84fe2f62df2b13f20e5c8aa8e7` and `3fa741c06e8116443e8de3adbf82a3439ff177fc`.
Tree: `69a1aebdfe35feefd7292d1b47cc6ef3450f57f9`, exactly the tested combined tree.
Natural push run: https://github.com/c933103/AN-Paint/actions/runs/39481127358

## Attempt 1: real failed gate, passing numeric/Czech tests

- Build/APK/source, exact-script resources, regression/lint, and API35 position jobs passed.
- API35 core and its aggregate failed. This attempt is not a green post-merge verification.
- The hash-verified regression artifact (ID 12293041124, SHA-256 `cec5b5063414637e299153cc39223dc56ee53ef0cfa53f9fc05ce099120edc1b`) contains 1,264 passing JVM tests across 133 suites, with zero failures/errors/skips. All CzechExtendedWordingTest 5, LocaleNumberInputTest 35, and UnicodeMinusInputTest 9 executions passed.
- Raw device XML records 74 Paintroid instrumentation tests, 38 core app tests, and 7 position app tests passed. Those passing assertions do not override missing mandatory screenshot evidence.

## Exact collection failure

The unchanged cleanup command at tools/ci_emulator.sh:261 was:

`timeout --kill-after=3s 15s "$adb" pull /sdcard/Download/anpaint-ci-vertical-evidence "$report/vertical-locale-export"`

It exited 1 in less than one second, not timeout 124. The pull log shows transfer had begun for qaa-Zsye-XV.zip (8% of that file) before interruption. At 19:32:09 UTC the host adb logged a connection-terminated read failure and guest adbd logged a write failure/offline transport. A new transport connected shortly afterwards and logcat collection succeeded. The emulator was then stopped by normal cleanup. The logs do not establish the deeper cause of this short transport loss.

Logcat records MediaProvider publishing all four expected export ZIPs (en-XV, mnc-Mong, qaa-Zsye-XV and lzh-Hant) before collection. All four vertical tests passed, including their export rule's complete required inventory, content SHA-256 readback, exact ownership/path and published-row checks. This supports recoverable transfer interruption rather than missing expected screenshot production. However, attempt 1's uploaded artifact contains no complete pulled vertical export ZIPs, and the host screenshot/reachability validators were not reached. No complete receipt is claimed for them.

Same-tree premerge comparison: run 39476623276, artifact 12291312788, SHA-256 `8107d1ac366772860a6b3b9710b1362f8700f7ec554d133435fd88a27746b739`. Its unchanged collection command pulled four files in 0.070 seconds and passed the 32 screenshot / 8 reachability-case validators. This is diagnostic comparison only, not a substitute for post-merge evidence.

Post-merge core artifact: 12293006415, SHA-256 `8af87ff2ab53879dbe0a24ebabda119e89616d6d6d1848f24fc5ce96a19e5e33`.
Post-merge position artifact: 12292446705, SHA-256 `74b7fa95fb10c9efab7cf303852a1c6e9407416224d89092a21a4fc763489ad1`.

## Retry status at receipt creation

After reconciling the known failed outcome and this transport diagnosis, the parent initiated one normal failed-job retry at 19:34:45 UTC. Attempt 2 binds the same merge commit and is pending/running. No code, timeout, assertion, screenshot requirement or release input was changed for the retry. It must earn its own complete fresh mandatory evidence before any post-merge release-gate credit.

## Preserved merge history and limits

The earlier guarded merge was explicitly rejected and not executed because develop had advanced with Czech changes. The same PR was then integrated with current develop; all six combined CI jobs and fresh exact-head code/security reviews passed. Only then did the parent's normal guarded retry merge the reviewed combined tree. No alternative PR or indirect merge bypassed the rejection.

Published 0.0.40 remains untouched. This is not arbitrary Unicode numeric support. Parser/range validation and layout are unchanged. Unicode-minus-specific regression evidence is hosted Robolectric/JVM execution on SDK21/25/35, not installed-device Unicode paste verification. The offered-locale filter check also covers SDK30. Local JVM/Android remains unrun because Gradle could not download and no SDK was configured.

The two local host logs each record 1,082 passing tests against the same combined tree before merge; they are not represented as a new post-merge execution. Negative fixture diagnostic text in these logs belongs to passing host tests; both process exits are retained as 0.

## Files and provenance

- all-jvm-results.zip repackages unchanged XML bytes for all 133 post-merge JVM suites. The three individually exposed Czech/numeric XMLs and JVM/lint/Python logs are unchanged artifact bytes.
- device-diagnostics.zip contains unchanged selected XML/log/JSON files from the three hash-verified device artifacts, in distinct attempt-1 and premerge-comparison directories. It is not the missing screenshot payload.
- core-logcat-excerpts.log is an explicitly selected, unedited-line subset of attempt 1 logcat containing the four published ZIP paths and transport loss/recovery. It is not the full logcat.
- JSON summaries/manifests are derived binding/count records, not replacements for raw results.

Earlier immutable evidence:
- Expected-red baseline: https://github.com/c933103/AN-Paint/tree/8138fa0f95dccc1696d756fb5587122d01eb9d08
- Old-base fixed red/green: https://github.com/c933103/AN-Paint/tree/a4a5dc20be720536b3a5f7b2165ccf39ce0be5cf
- Current-base premerge: https://github.com/c933103/AN-Paint/tree/971adae8d33da9a859a5c83ab280de0cc6467cec

