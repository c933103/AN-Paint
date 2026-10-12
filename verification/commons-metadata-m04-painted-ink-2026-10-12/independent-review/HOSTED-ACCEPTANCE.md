# Fresh hosted acceptance plan: painted-ink successor

Status: **PENDING source publication and fresh hosted execution.** This plan does not reuse the diagnostic run's 890/111 acceptance result. Its source scope is the six source files and two inventory/provenance files in `reviewed-source-manifest.json`.

## 1. Immutable source and artifact binding

Record the actual PR55 head, PR base, synthetic merge SHA and its two parents, merge tree, workflow run ID/attempt, event, job IDs, build variant and artifact IDs/digests. Compare all remote leaves and modes with the intended publication tree before starting acceptance. The final tree includes evidence and is not inferred from the six-file source manifest. Verify each downloaded ZIP against GitHub's digest and each extracted member against the ZIP. Preserve original logs and raw failure artifacts.

The prior run `38244193872`, head `dc46abc2add7984358565a88fe65c5278212dcf6`, merge `56e7891852a2da201bf10ad99c486e659da2e6c5`, tree `4ff7f479ffc73964fa8756b6c7e3202f624ad0f1` remains a failed historical result. Its checker is not rebound or overwritten.

Require successful source-bound Kotlin compilation, host aggregate, JVM, native and lint phases independently. Inspect `build/reports/ci-phases/` and Gradle raw logs. The unchanged JVM workflow command is:

```
bash tools/ci_run_timed.sh jvm ./gradlew --no-daemon --max-workers=2 --console=plain --continue --profile -PnativeAbis=x86_64 :Paintroid:test${BUILD_VARIANT^}UnitTest
```

Inspect exact-script generation's seven successful probe commands, exits and log/output hashes under `build/reports/exact-script-generation/`; bind its disposable worktree to the same source. An APK upload or successful independent job does not override a JVM failure.

## 2. Exact JVM inventory

Use `verification/commons-metadata-m04-painted-ink-2026-10-12/expected-jvm-identities.json` and its pinned source/inherited inventory hashes. Read every XML under `Paintroid/build/test-results/testDebugUnitTest/` (or the actually selected release variant). Require the exact multiset of 892 `(classname, name)` identities, preserving SDK suffixes. Reject duplicates, omissions, extras, skipped tests, failures and errors. Do not substitute a count or summary for identities.

The only additions to the frozen 890 are:

- `CommonsMetadataQueryFailureFlowTest.paintedInkOracleRejectsNativeOverflowAndClippedEdgeGlyphsAtNormalScale`
- `CommonsMetadataQueryFailureFlowTest.paintedInkOracleRejectsNativeOverflowAndClippedEdgeGlyphsAtDoubleScale`

Resource API30/API35, font and prior PR52 HTTP/Korean oracles remain in the unchanged inherited inventory. Inspect all failures before rerunning.

## 3. All 112 ordinary success captures

Require exact PNG+JSON pairs under `Paintroid/build/reports/commons-metadata-m04/` for 14 tags × 2 actions × 2 font scales × 2 orientations. Tags: en-GB, ain-Kana, ain-Latn, bo, ryu, fr, ar, ja, vi-Hani, mn-Mong, mnc-Mong, lzh-Hant, en-XV, qaa-Zsye-XV. Filenames identify API35, tag, 320x640 or 640x320 dp, font1.0/font2.0, copy/insert. Decode all PNGs and validate dimensions (640x1280 or 1280x640 pixels), exact text and action metadata against the frozen messages, full-character flags, and direction-correct reading-start metadata. Match current JUnit results rather than trusting JSON success flags.

Inspect actual normal/enlarged Ainu, Tibetan, Arabic, Nôm, Mongolian and Manchu pixels, both routes as appropriate. These are native Robolectric captures, not installed-device evidence. Parent scroll reachability remains independently asserted in source.

## 4. Diagnostic advance preservation

Require all 28 normal-landscape profiles in `Paintroid/build/reports/commons-metadata-m04-diagnostic/`: each root PNG, expanded-layout PNG and JSON, plus `normal-landscape-outcomes.json`. Recompute contiguous UTF-16 line coverage, geometry, old advance booleans, finite probe edge flags and per-line ink metrics from pixels. Keep the old `left>=-1 && right<=width+1` value observable.

Specifically inspect Ainu Kana COPY line 0. The historical observation was right=1233.043, width=1232, old guard=false, with visible ink ending at x=1231. A current painted-ink pass must not be labelled an old-guard pass. If native geometry changes, report that fact and review it rather than manufacture the historical value. The diagnostic metadata explicitly distinguishes current painted-ink acceptance from old advance diagnostics.

## 5. Strict ink frames and native negative controls

Under `Paintroid/build/reports/commons-metadata-m04-painted-ink/`, require exactly:

- 36 live horizontal frames: 9 horizontal tags × copy/insert × font1.0/font2.0, landscape only
- 12 intact control frames: en-GB, ain-Kana, bo, ar, ja, vi-Hani × both scales
- 72 native mutant frames: each intact profile × six mutations
- Each frame has `-actual-textview.png`, `-complete-layout.png`, and `.json`: 120 JSON records and 240 PNGs
- `native-negative-controls-font1.0.json` and `native-negative-controls-font2.0.json`, each with six unique locale outcomes and six unique cases per locale

Decode the complete reference and actual-view images. Parse the reference rectangle and origin. Independently recompute, using every alpha>0 pixel: reference ink count/spatial bounds, all four allocation-edge contacts, horizontal overflow, ink outside the view, missing expected ink, and exact full-view mapped ARGB differences. Require the reported counts to match. Require alpha cutoff, position tolerance and color tolerance all exactly zero. Compare whole reference support; never use an already clipped crop as expected output.

All 48 intact/live frames must have nonzero ink and zero edge, overflow, outside-view, missing and differing pixels. For 48 translation controls (left/right crossing and wholly-left/right), require positive real overflow, identical total reference ink count, no allocation-edge contact, and the specific horizontal-overflow rejection. For 24 clipping controls (first/last spatial edge), require unchanged complete reference pixel arrays and geometry, positive removed expected ink, no unrelated overflow, and the specific clipped-ink rejection. Verify pixels independently of summary booleans. The native tests also assert unchanged view/layout/cached bounds, text, accessibility and key paint state after each mutation; both methods must pass.

Inspect actual intact and mutant images across RTL, combining and Han/Latin scripts at both scales, including wholly displaced reference images. Any unsupported-feature precondition failure is a failure, never successful negative-control evidence.

## 6. Resources, scripts and font binding

Audit APK build-info/source binding, corresponding-source leaves with only the established three bundle omissions and declared native-source roots, and all 14 font-directory assets. Use the verified SDK `aapt2 dump resources <apk>` on the actual successor APK; compare default plus all exact 59 localized M04 values and existing Korean alias configurations. Preserve U+180E in Manchu at character indices 7,18,27 and U+202F in Mongolian at 7,17,30; compare full strings and code points rather than normalized text. The accepted translation-input SHA remains `00830298aefa73ca075d585c4d9191e1f2fdf5becbd9320783b5e11fa7409e1d`.

Font SHA remains `6b70d3c5c146c9d11503e5dff7ade5e7ccb3ae5a70c511f71902d4a75f7a3006`. Source/packaged font and licences must remain exact. Retain API30/API35 resource/font/glyph coverage results, whole-word script-shaping and real-view render evidence from the inherited inventory; source checks and font cmap presence alone do not establish shaping. No new font rebuild or translation review is implied by this test-only successor.

## 7. Separate device and delivery conclusions

Installed API35 terminal receipts, actual expected device identities and emulator captures remain a separate gate. Current-platform success is not full API30/API35 release verification. Signing, corresponding source and APK installability are independent delivery checks. Root decides readiness/merge only after the exact-source outstanding gates are resolved.
