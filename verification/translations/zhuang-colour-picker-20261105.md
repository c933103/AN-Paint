# Zhuang image colour picker, 5 November 2026

## Scope and language review

The live review branch was reconciled at parent `105f1790959057272e619a4f6b0a070d12a19dbf`, tree `be7e575e115a874b14ae5041a5f339ae0a6f9f5b`. The previous publication was confirmed, with no pending or uncertain write. This fills missing P1 `ui_eyedropper` and P3 `ui_tap_the_image_to_sample_the_foreground_colour`. All 288 preceding typed resources remain unchanged; the total is 290. Only canonical XML and this report change.

The tool name is a functional description, “choose colour from image,” rather than an unverified translation of the physical eyedropper metaphor. Independent review recommended putting the source phrase before the verb. The adopted hint means approximately “Tap the image to choose the foreground colour.” Foreground identifies the destination colour slot, not an automatically detected foreground region in the picture. “From image” distinguishes this tool from the colour palette.

Evidence:

- [Sawloih Cuengh-Gun OCR](https://dokumen.pub/sawloih-cuengh-gun-ocr.html), independently retrieved by the reviewer: `senj` choose/select (S24), `daj` from (D5), `saek` colour (S6), and `baihnaj` front/foreground (B15). The source example for `daj` places the source phrase before the verb. This is an OCR transcription that warns it was not fully checked.
- [Published Yongbei Zhuang translation, Matthew 1:1 note](https://www.bible.com/bible/1656/MAT.1.YBNT), found by the reviewer and directly retrieved during integration, independently uses a source phrase introduced by `daj` before `senj`. This supports word order, not standard software terminology; the variety and religious context differ from this UI.
- The reviewer found independent use of `Dozsiengq` as the [People's Daily Zhuang image-section label](https://sawcuengh.people.com.cn/). A further proposed constitutional-translation source returned HTTP 502 during integration and is not treated as directly verified evidence here.

Meaning confidence is **moderate**; complete idiomatic wording confidence is **low-to-moderate**. Existing project use supports consistency of image, foreground and tap vocabulary, but does not independently establish the modern touchscreen sense of `diemj` or the complete hint's naturalness. No authoritative standard eyedropper term, independently attested complete UI sentence or native-human certification is claimed. Canonical Android XML owns current wording.

## Actual consumers

`PaintTool.PICKER` in `PaintDocument.kt` binds both resources through the selected-locale resolver. `ToolButton` uses the label for its text, content description and tooltip. The activity also exposes the label in the options/status and combines label and hint in contextual help; the normal How to use action displays this hint for PICKER. The separate “Tap a pixel” options text is unchanged and remains fallback, so this does not claim the whole tool panel is localized.

`PaintCanvas.handleTouch` maps touch coordinates to image coordinates. In the ordinary ACTION_UP path, PICKER checks that the point is within the bitmap, reads that pixel and assigns it to `document.foreground`, then calls `onPick`. This branch does not write the bitmap or background colour. The callback updates recent colours and displayed colours/status and schedules autosave. Earlier gesture and viewport guards still apply; no touch, sampling or state logic changes.

The compact tool tile is 64 dp with a two-line, end-ellipsized horizontal caption. Its full label remains assigned to the content description and tooltip. The longer functional label may truncate visibly; this batch does not establish its measured fit or TalkBack presentation.

## Verification

Work and tests used the available temporary filesystem; no unrelated work was removed from the full main workspace.

- All 171 offered-option catalogue checks and the importance manifest passed. Existing nodes, source attributes, ordered arguments, numerals, literal tokens, newline escapes and XML escaping are preserved.
- `python -m unittest -v test_translations test_translation_boundaries test_string_importance test_current_localization_contracts`: **61 tests passed in 10.471 seconds**.
- Four host Java XML-to-string cases checked both English/Zhuang labels and hints for nonempty text and unchanged no-argument formatting. These are not Android resource compilation.
- Temporary token-aware Kotlin checks verified both direct bindings, selected-locale accessors, tool/help presentation, the guarded pixel-to-foreground sampling path, recent-colour/autosave callback and the compact-caption ellipsis behavior. The first static check had an ambiguous ACTION_UP selector; it was narrowed to the ordinary path and rerun successfully. These are structural checks, not touch or UI execution.
- Base snapshot verification matched Git blobs and executable modes for **1,280 materialized files**, retaining **288** unmaterialized entries. Publication verifies the complete path/mode/type/blob overlay, expected-parent non-force lease and exact remote bytes.

Inspected but not run: `ClassicWorkspaceTest.bucketFillsOnlyEnclosedRegionAndEyedropperSamplesIt` taps a filled green region with PICKER and asserts foreground becomes green. `ResponsiveToolboxTest` also exercises selection of the visible PICKER tool. These source inspections are not runtime evidence. No permanent per-edit wording mirror or test package is added.

Zhuang presence is P0 **69/94**, P1 **158/249**, P2 **61/305**, P3 **2/71**. Across 171 options, missing resources are P0 **162**, P1 **1,333**, P2 **30,068**, P3 **7,479**; 46 options have complete presence. Scope remains 59 scoped catalogues and 112 outside-scope catalogues with explicit English fallback. Presence is not fluency or runtime acceptance.

Android SDK/Kotlin compiler are unavailable here. Android compilation, Robolectric, actual sampling, TalkBack and device layout were not executed. Exact-head Actions state is checked after publication and reported separately. No merge, release or CI-pass claim is made.
