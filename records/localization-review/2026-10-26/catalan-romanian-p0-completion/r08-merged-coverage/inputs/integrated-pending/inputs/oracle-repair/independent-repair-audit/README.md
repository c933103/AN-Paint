# Independent numeric warning oracle-repair audit

The original PR178 run `40340230583` remains failed: 1,366 unique JVM cases, one failure in `NumericDisplayLocaleTest.oversizeWarningUsesResourceDigitsAndDecimalsWithoutChangingAdmission` at line 99. Its five new completion tests passed; that does not make the aggregate run successful. The original XML also contains an unexecuted-runnables suppression, retained as evidence rather than silently diagnosed as fixed.

The repair changes exactly one pre-existing test file. The English fallback prefix is replaced with the already-reviewed Romanian full-value prefix, and an explicit `2,25 MP` check is added. Complete resource equality, deliberately mismatched US process/resource locales, successful boundary admission, oversized rejection, resident-pixel and invalid-size guards remain. Unreviewed P1 English captions, all translation XML and all production logic are byte-unchanged.

The ordinary and optimized static audit receipts are identical. Thirteen static negative mutations reject weakening or corrupting these assertions. They do not execute Kotlin, Robolectric or Android. The static composition example is explicit reviewed-template token substitution, not a claim to have run Java locale formatting.

Reproduce with `verify_numeric_oracle_repair.py --root "$PACKET_ROOT" --out "$OUTPUT"`, then repeat with Python `-O`. The packet root must retain the original `head-tree.json` for head `93f27ed172cc730c80ed7a2ffbcacc1b0c04383f`, `implementation-original`, current repaired `implementation`, final reviews, repair/oracle-change.json and original downloaded CI ZIP/individual XML files. This script reads those project inputs and writes only its receipt.

Fresh exact-head CI/Codex and actual artifact verification remain required. No source or external edits were made by this auditor. No new linguistic, native-human, physical-device, layout or release certification.
