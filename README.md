# Unicode-minus fixed-head JVM evidence

Fixed source head: `36c20df8044c79b3da308bc2149bdef6e5cb72c5`.
Hosted PR merge source: `666bf7be8a9e7a1889b73d97102d07267ad35dbb`.
PR: https://github.com/c933103/AN-Paint/pull/155
Run: https://github.com/c933103/AN-Paint/actions/runs/39471947822
Regression job: https://github.com/c933103/AN-Paint/actions/runs/39471947822/job/118798321244
Artifact ID: `12289361338`.
Original fixed artifact SHA-256: `a6349fe1cc896596438533c294fdfd7306ecae40c1960847b6f0846e9c1a5186`.

## Result

All 1,259 hosted JVM tests passed, with zero errors, failures or skips (132 JUnit XML suites). `UnicodeMinusInputTest` passed all nine executions: three behavioral tests on Robolectric SDK21/25/35. `LocaleNumberInputTest` passed all 35 executions, including the 171-offered-locale U+2212 check on SDK21/25/30/35. Lint passed independently.

The unchanged regression tests now prove that U+2212 reaches existing validation intact; Czech/English reject it rather than accepting positive digits, Swedish interprets it as negative, and the tested RTL/native-sign paths never accept a positive value from negative input. Both position fields preserve the image layout, model and saved project bytes after rejected input; Cancel/reopen and valid native-digit updates also pass. Ordinary parser/range rules were not relaxed.

This is hosted **Robolectric/JVM** actual filter/parser/dialog-consumer execution, not a claim that the new paste cases ran on installed devices. The workflow separately runs existing API35 installed-device suites; consult the linked run for those outcomes. No arbitrary Unicode numeric-input support is claimed.

## Red/green binding

The initial production baseline was tested at source head `8ce14f4a25ea242d336b1bb567f8b4cf5cb1878f` / merge source `d8b6b4771b3075fe6956a829869ea7410dd9d5bd`. It completed the same 1,259 tests with exactly 10 new U+2212 failures, including positive coordinate mutation after actual Apply. The native-sign/cancel/success control passed. [Baseline evidence](https://github.com/c933103/AN-Paint/tree/8138fa0f95dccc1696d756fb5587122d01eb9d08) remains unchanged.

Both all-JVM-results ZIPs contain unchanged XML bytes extracted from their respective hash-verified workflow artifacts; only their archive packaging is new. The individual numeric XML files and `jvm.log` are unchanged fixed-artifact files. `jvm-summary.json` is a derived count and source binding, not a substitute for those raw reports.

[Exact-head Codex code and security review](https://github.com/c933103/AN-Paint/pull/155#issuecomment-6297757174) completed with no findings. Local normal/optimized host suites each passed 1,075 tests; local JVM/Android execution was unrun because the Gradle distribution download was unavailable.

The fixed production change is only the shared U+2212 accepted character and explanatory comments. Parser/range implementations, published 0.0.40 inputs and Czech translation are unchanged by this PR. Develop subsequently gained the disjoint Czech change; postmerge current-composition checks are a separate gate, not credited by this evidence.
