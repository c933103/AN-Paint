# PR59 current colour preparation receipts

Source: [519f043ad7472065cb9cbf50c4db2cf9a1db7607](https://github.com/c933103/AN-Paint/pull/59), tree dc50303c0e75b90b29dbebcb27819ce3aa8ef90f. Parent b20a8279 is merged PR52 and has the same cf1ffdb1 tree used for local preparation. All 1,099 remote source paths, blobs and modes were checked before opening PR59.

Both final full host suites pass 658 tests on that unchanged tree: ordinary 137.434s, optimized 134.833s, each within the 240s cap. The two receipts bind exact commands, timestamps, source tree and log hashes. Independent source/host review cleared the PNG corruption gap; the focused transport run passes 34 tests.

The earlier focused/exploratory failure logs are retained as failures, not current acceptance: stale five-case synthetic selector/doc expectations and later SDK/count expectations in a synthetic vertical fixture were corrected without relaxing production gates or deadlines. The source-scope comparisons and JVM inventory are one-time author receipts, not application/CI historical inverse gates. JVM 942 and API35 106/API30 95 are source expectations, not local Android execution.

No local Android SDK/cached Gradle 8.13 was available; Kotlin, JVM/native, lint, build and installed acceptance were unrun locally. [Fresh full-matrix run38322850500](https://github.com/c933103/AN-Paint/actions/runs/38322850500) is running. This separate evidence ref is not application source and must not be merged into develop. No font-2x, physical-device, TalkBack, fluency or release acceptance is claimed.

PR51/PR53 source and historical evidence remain linked in PR59. This archive contains newly generated preparation results only, and does not resume the historical denied raw-evidence upload.
