# Initial PR139 failure, preserved without retry or suppression

Exact head `c46fc4495e7afc1e460e1f52cab5607b9422fc25`, tree `9f9e58fc77ee0dda24c0dacffed4aa218fe4c2b0`, synthetic checkout `3acb26303c126cf8b3d5a461c60e5ca9f5a751a6`; [run39147690887](https://github.com/c933103/AN-Paint/actions/runs/39147690887).

Downloaded regression artifact12144361868 matched its GitHub SHA-256. It records 1,144 JVM tests in 123 suites: exactly one failure, no errors/skips. `taiwaneseHanWarningKeepsPlacedAntecedentAndSupplementaryGlyph` fails because the actual API33 crop-status Paint font chain reports no glyph for U+2A736 (𪜶). The Han method stops at that guard, so its later layout/Cancel/reopen assertions are unrun. All seven other ChineseCropPreviewTest methods pass, including the complete POJ consumer, its U+0358 coverage/composed-dot ink and layout assertions. Do not relabel this as a combining-mark API false negative or remove a genuine coverage guard.

The same head has clean Code and advisory Security reviews. Build/source binding (1,222 included repo files, three explicit metadata omissions), embedded matching source, debug signature, 16-KiB alignment and all nine exact-script probes pass. At packet capture, the position device job passed and core/composition were not yet terminal. These passes do not negate the JVM failure.

`failure-packet.zip` retains every JUnit XML, CI phase log, full regression job log, exact failure XML, review, observed run/jobs/artifact metadata, build/source and exact-script receipts and signature/alignment logs, with a per-entry SHA-256 manifest. `failure-summary.json` includes the exact failure trace and archive SHA-256. The original source and initial local evidence remain reachable through this additive evidence ref's ancestors.

Possible remedies need review: use a linguistically supported BMP antecedent (MOE lists 怹 as an alternate graph of 𪜶/in) and retain positive raster checks for the final wording, or separately authorize/test a font fallback expansion. No replacement is applied by this evidence commit. Hakka/Wu remain held.

