# Final cumulative actual-develop verification

Actual develop `6ae0f768fe6f068c129883ea06eb9d497e25fa4c`, tree `a2aedaa231a4d90009437a2f9b2b320f2de33d3f`, remains unchanged. Natural push run **41235216705**, attempt 1, completed **SUCCESS**, all six jobs. This verifies the actual cumulative tree after PRs 250–255 and the separate Swedish manual correction249. No manual dispatch, duplicate review, extra benchmark or release.

Hashed artifacts: regression13055997593 (`0fd996d376cea5702a28b468479e82a6b538047af20036a22e8543ecdb7c2c44`), composed emulator13055781775 (`48dcb871ded9988db4287fb0937a4769f7032b1ffdeaaa176d5a85d8a1699f8b`). Verified Python1,018; JVM1,464 with no failure/error/skip and all123 retained touched methods present; native74/74 and complete app49/49 with exact actualcommit/run identity.

## Observed ongoing work

| Observation | Before final stage: actual25f | Qualified255 | Final actual6ae |
| --- | ---: | ---: | ---: |
| Python executed cases | 1,464 | 1,018 | 1,018 |
| Python test seconds | 327.912 | 162.151 | 220.795 |
| JVM executed cases | 1,501 | 1,464 | 1,464 |
| JVM case-time sum seconds | 976.322 | 492.846 | 717.999 |
| JVM Gradle step seconds | 1,194.552 | 609.655 | 893.675 |
| Regression/lint job log span seconds | 1,918.164 | 1,001.019 | 1,424.333 |

The final actual observation is **23m44s**, not the faster16m41s qualified PR sample. Compared with the immediately preceding actual31m58s observation it is8m14s shorter; this is not a controlled speedup estimate. Runners differed (eastus→centralus; distinct workers), same Ubuntu image/restored cache keys but uncontrolled runtime conditions. Prior stages had slower actual observations despite less work. No repeat benchmarks were launched.

## Mapped cleanup disposition

Today's original f3 tree had148 host fixture JSON files /21,886,679 bytes. Current tree has11 /47,965: **21,838,714 fewer active bytes (99.78%)**,137 fewer files. Current-localization137 /19,250,531→6 /24,167. Additional memory queues and orphan source tables retired separately. Host executed cases2086→1018; JVM1962→1464 using existing qualified baseline and current receipts. These are net counts including intervening manual tests, not a claim every retired method was a product defect.

All mapped approval-copy families now have recorded retirement or independent-input retention. Eleven surviving fixtures serve font, legal/protocol/format/Unicode, registry or small contextual regressions; upstream catalogue/licence inputs serve provenance. Canonical resources own wording, immutable history owns historical acceptance, and generic routing/format checks plus actual consumer/state/layout regressions remain. No new per-language package/framework or replacement approval table. Affects future translation maintenance without requiring successor-payload edits for every legitimate wording change.

Cheap current-source inventory remains171 offered options /171 exact catalogues,716 translatable string keys and1 plural resource;60 catalogues directly contain all keys,111 do not. This says nothing about linguistic correctness or renewed acceptance. Outstanding linguistic review/withdrawals and release pause remain. Completion here means the finite mapped overexpansion repair and its verified delivery, not translation completion or perfection of all application tests.
