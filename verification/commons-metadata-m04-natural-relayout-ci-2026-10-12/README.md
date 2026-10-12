# Independent PR55 natural-relayout artifact review

Final bounded artifact review for the exact checkpoint below. Existing JVM failure and incomplete later controls remain explicit. Subsequent migration work requires its own source/run review.

## Binding

- Head: `04b128889a4ff9159f199d1737bd07d41e22162d`
- Base: `71f4d288669858e7975ec4c094b7f47a9a1ff145`
- Synthetic merge: `de1b934e4786fd041638d00e72e880940328f7a9`
- Tree: `3dcc1a82f878ad7e0e708cff25ec8d493b88bbc6`
- Run: `38269993000`

Publication/tree/remote provenance was supplied by the coordinating writer; this reviewer independently compares the downloaded ZIPs, extracted members, exact source objects, raw receipts and raster arrays. No GitHub writes, source changes or local Android execution occurred.

## Results

PASS: seven retained exact-script probes, including clean/incremental/stale-output/release-first behavior. Logs, commands, task ordering, source and output hashes match. This is retained real Gradle evidence, not a local rerun.

PASS: APK/source delivery has 2,120 exact source blobs against the 2,123-leaf tree. The only omissions are the three existing bundle omissions (`.gitignore`, `colorpicker/.gitignore`, `.idea/codeStyles/Project.xml`). All 6,258 extra source files are confined to the four declared native-source roots. Embedded source ZIP equals the separate source ZIP. All 14 font assets match. No release-signing, upgrade-key, native-upstream-content or installed execution conclusion follows from this check.

PASS: actual APK M04 table has default + all 59 values + the generated Korean exact-script alias (61 configurations). U+180E and U+202F are retained at their exact expected positions. Resource compilation is distinct from actual locale selection/shaping and linguistic acceptance.

PASS WITH EXPLICIT SKIPS: hosted Python reports 719 total methods, 717 passes and 2 skips in 165.575 seconds, exit0. The compact raw log does not identify the skips. Native preparation and lint both exit0.

FAIL UNDER THE EXISTING ORACLE: all 892 expected JVM identities ran, 891 pass and one fails. The failure is `paintedInkOracleRejectsNativeOverflowAndClippedEdgeGlyphsAtDoubleScale`, Arabic mixed-paragraph reset. Existing zero-alpha containment reports two overflow/missing/different pixels. No missing/extra/duplicate/skipped JVM identity.

PASS: all 112 ordinary root PNG/JSON pairs, all 28 normal-landscape diagnostic profiles, and all 36 live horizontal painted-ink profiles are present and consistent. The prior Ainu advance-bound violation remains recorded as diagnostic, with zero actual ink overflow.

INCOMPLETE: 155/181 strict ink triplets are present. 154 meet their intended per-frame conditions; the mixed reset is the single failing positive. The assertion abort leaves 14 positive frames, 12 mutants and both font2 summaries absent. Normal-scale summaries are complete. An additional independent forensic pass confirms the intended full-reference/actual mutation relation for all 60 present mutants, including the 24 font2 mutants whose summary was never written. Absent controls are not passes.

## Current failure and proportional review

Only reference samples at layout (1232,29) and (1232,30), alpha7 and alpha1, are absent in the actual mixed-paragraph raster. No allocation-edge contact or other ARGB difference. The affected connected ink component retains 76/78 samples, 10625/10633 alpha units and all opaque samples. Full actual/reference images were inspected; metrics use original unscaled arrays. See `mixed-reset-forensic-result.json`, `inspected-images.json` and `mixed-reset-disposition.json`.

The explicit review disposition is low-severity antialias fringe loss, with no demonstrated material missing glyph, mark or line. The root-approved behavior-first policy allows such an evidence-backed disposition while keeping all unmasked diagnostics. It does not rewrite the old failed assertion as passed or invent a numeric tolerance. `READABILITY-CRITERION.md` documents the rationale, limits and focused control requirements. Installed results are independently verified below.

The mixed native glyph box is much wider than the actual painted text. In the current algorithm, both paragraph directions make the needed absolute margin exceed the bounded 2em limit, plausibly leaving inset zero. This is a static explanation consistent with the record, not a traced internal `onMeasure` execution. No larger production workaround is recommended from this fringe-only evidence.

## Installed result

PASS: both official installed ZIP digests and every extracted member match. API30 completes all95 scheduled identities (97 SDK-eligible declarations, two explicit API35 restart omissions). API35 completes all104 identities, including restart seed/verification. Current selectors/source fingerprints, raw instrumentation protocol, XML, summary statuses and coverage unions match, with no missing/extra/duplicate completion.

PASS: both installed Arabic routes pass the existing strict decoder and an independent Pillow/NumPy recomputation. At density1, content width616, measured leading inset1, both actual views are640x92 and full references622x92. Copy has4287 ink pixels; insert4435; both right-exclusive ink edges are616. All allocation-edge, overflow, outside-view, missing-ink and ARGB-difference counts are zero. All four actual/reference PNGs were visually inspected. Actual compiled Arabic reason and route wrappers equal both observed messages.

PASS: two ordered `GalleryStatusNaturalUpdate` records prove exact `GlyphBoundsStatusView`, differing complete messages, equal88px native layout heights, and settled false -> requested true -> settled false state transitions. The reviewed helper does not force geometry. Both records cross-match the exact-source full-raster records, with no malformed/missing/duplicate natural record. This is source-bound installed native software drawing of injected status text, not a hardware screenshot or actual network-error execution.

The original live installed lifecycle/clipping regression is resolved on this exact run. The synthetic mixed-paragraph fringe observation remains the failed old JVM oracle with incomplete later controls. PASS: both full installed job logs verify the exact merge, same-run digest-enforced main/test artifact downloads and successful installs from the reviewed prebuilt paths. Main APK/source bytes independently match the published tree. The instrumentation APK archive was not independently extracted or hashed on-device; that bounded provenance limit remains.

## Separate archival-helper issue

The exact-head Codex strict-forwarding finding was independently reproduced for the two delegated receiver paths; direct strict receiver calls reject the same reverted endpoints. Whole-file endpoint tests also detect the reversion, so this is a wrapper-contract defect, not evidence that all checks can be bypassed. Reproduction is retained in `strict-forwarding-result.json`. The owner's subsequent workflow policy retires permanent source-snapshot chains; no additional inverse layer was designed or written after that instruction. `MIGRATION-REVIEW.md` separates useful behavior/resource contracts from archival inputs.

## Portable commands

All commands use Python 3 and the reviewed source checkout as `SOURCE`, current extracted artifacts as `CI`, and this directory as `REVIEW`.

- `python3 "$REVIEW/audit_natural_probes.py" --repo "$SOURCE" --probes "$CI/exact-script" --artifact "$CI/exact-script.zip" --output "$REVIEW/probe-result.json"`
- `python3 "$REVIEW/audit_natural_delivery.py" --repo "$SOURCE" --archive "$CI/apk-and-source.zip" --probes "$CI/exact-script" --output "$REVIEW/delivery-result.json"`
- `python3 "$REVIEW/audit_natural_compiled_m04.py" --repo "$SOURCE" --apk "$CI/apk-and-source/app/build/outputs/apk/debug/app-debug.apk" --aapt2 "$AAPT2" --delivery-result "$REVIEW/delivery-result.json" --output "$REVIEW/compiled-m04-result.json"`
- `python3 "$REVIEW/audit_natural_artifacts.py" --repo "$SOURCE" --artifact "$CI/regression.zip" --extracted "$CI/regression" --binding "$REVIEW/regression-binding.json" --output "$REVIEW/regression-result.json"` (expected exit1 for this failed checkpoint)
- `python3 "$REVIEW/forensic_mixed_reset.py" --frames "$CI/regression/Paintroid/build/reports/commons-metadata-m04-painted-ink" --output "$REVIEW/mixed-reset-forensic-result.json"`
- `python3 "$REVIEW/audit_phase_receipts.py" --phases "$CI/regression/build/reports/ci-phases" --output "$REVIEW/phase-result.json"`

`AAPT2` is the previously verified Android SDK35 tool, SHA256 `d1096e11aba9c974644369ee3c50d239acac3f3428ffa928e5b9c14dfb7a57de`; no new SDK was installed. `audit_natural_update.py` and the installed pixel checker have now checked the actual installed records. Their synthetic tests remain separately labelled checker tests.

All historical checkers/reports retain their own bindings. These per-run source bindings authenticate observed evidence; they are not a proposal to retain permanent source-equality gates in normal CI.

## Checker and archive limits

Prepared checker tests passed19 normal and19 optimized; the current complete checker self-test rerun passed19. One initial synthetic fixture-path setup error was corrected and its failed log retained; it was not an app/CI failure. `raw-receipts` contains raw phase/protocol/XML/install inputs and a losslessly compressed full API35 logcat. `inspected-images` and `installed-observed` retain the actual reviewed pixels. The outer APK/source and CI ZIPs are not duplicated in this review bundle. The official digests and exact member checks are retained in result JSONs. No source, translation, font, production geometry, threshold or current test result was changed by this reviewer.
