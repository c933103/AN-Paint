# AF / Nepali / Punjabi forward test repair

Source: [`b05a39d4`](https://github.com/c933103/AN-Paint/commit/b05a39d4e8b828abe04ee075b6a15db7127b3124), tree `91dbdf1542c92382fb6b7c45afa2a3a9f8161dec`, sole parent `63745c9a`.

The only source change adds whitespace around an existing Kotlin conditional in the Afrikaans canvas regression test. Independent readback verifies all 1,424 source blobs and executable modes; the other 1,423 paths and all 569 reviewed resource edits are unchanged. Both ordinary and optimized full host aggregates pass 1,532 tests, and each focused cohort passes 17.

The [original run](https://github.com/c933103/AN-Paint/actions/runs/40525183924) remains failed. Kotlin compilation stopped before JVM tests executed. Core instrumentation completed 74 native and 40 selected app tests without testcase failures, but mandatory dialog/vertical evidence export collection failed; the vertical pull reports `device offline`. Position passed separately. Completed instrumentation does not satisfy the missing export gate, and this does not establish general flakiness. Original regression archive bytes, bounded Core XML/summary/export files, all member digests and independent repair receipts are preserved in the package.

The [fresh exact-head run](https://github.com/c933103/AN-Paint/actions/runs/40529954324) must independently satisfy compilation, execution and all mandatory evidence exports. [Exact-head Codex review](https://github.com/c933103/AN-Paint/pull/192#issuecomment-6446094451) found no major issues. This record does not claim the fresh runtime gates have completed, a merge, a release, native-human acceptance or universal layout verification.
