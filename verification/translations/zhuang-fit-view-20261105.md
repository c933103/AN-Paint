# Zhuang fit-to-view labels, 5 November 2026

## Scope and language review

The live review branch was reconciled at parent `a76cd523e16a57fa099b98ddbfceb45bdbe64315`, tree `ee7a6867b2fe68b7da09f50bdadadafd80e65306`. No publication was pending or uncertain. This fills missing P1 `ui_fit` and `ui_fit_entire_canvas_in_view`. All 285 preceding typed resources remain unchanged; the total is 287. Only canonical XML and this report change.

Independent review recommended “View all” for the compact action and “View the whole drawing area” for its descriptive/accessibility label. These describe viewing rather than resizing image pixels. The canvas emphasis follows the English source, although fitting also accommodates pending trim and floating-selection bounds.

Evidence:

- [Unicode IRGN2677, pages 2–3](https://www.unicode.org/L2/L2024/24089-kzhuang.pdf), retrieved by the reviewer, identifies standard Zhuang `yawj` for look and reproduces the 1984 Sawloih Cuengh-Gun entry. It distinguishes a nonstandard spelling.
- [Wiktionary's yawj entry](https://en.wiktionary.org/wiki/yawj) independently supports see/look. This is secondary dictionary evidence.
- [Calling Lost Souls glossary](https://newdoc.nccu.edu.tw/teasyllabus/113721209100/Glossary.pdf), retrieved by the reviewer, supports `daengx` as all/the whole of. It is a textual glossary, not a UI terminology standard.
- [Guangxi Minzu Bao, “Fwen Yahmaiq”, 6 July 2016](https://www.guangximinzubao.cn/szbzw/html/2016-07/06/content_18142.htm), retrieved by both checks, uses `Yawj daengx mbanj dacaengz`, supporting the verb + whole + noun construction. Its literary context does not attest a software command.

Confidence is **moderate overall**. Viewing and whole-area components are supported; complete UI labels are composed paraphrases. The drawing-area phrase follows existing canvas wording, not a newly certified technical term. No native software-usability certification is claimed. Canonical Android XML owns current wording.

## Actual consumers

`ClassicPaintActivity` uses the compact resource in zoom/status controls, zoom-tool options and canvas-trim controls. All three buttons call `PaintCanvas.fit`. The full resource supplies the status Fit control's accessibility description and the FIT action icon's label. Complete text is assigned; the status text button explicitly permits wrapping without ellipsis. Other button/device/font-scale layouts were not measured.

`PaintCanvas.fit` combines canvas, pending trim and floating-selection bounds. It calculates viewport scale from available width and height, with handle padding and a 32x upper cap, then centers those bounds with pan offsets. Very small/uninitialized viewports return early. It sets fit mode and refreshes display/status, without directly resizing or committing document pixels. Existing polygon tap tracking is reset.

`ui_fit_selection34` is a different image/selection fitting action and is excluded. The unused `ui_fit_image` is also excluded. No viewport, selection, crop, image or layout logic changes.

## Verification

Work used the temporary filesystem; no unrelated work was deleted to address the full main workspace.

- All 171 offered-option catalogue checks and the importance manifest passed. Existing nodes, source attributes, ordered arguments, numerals, literal tokens, newline escapes and XML escaping are preserved.
- `python -m unittest -v test_translations test_translation_boundaries test_string_importance test_current_localization_contracts`: **61 tests passed in 11.499 seconds**.
- Four host Java XML-to-string cases check both English/Zhuang labels are nonempty and unchanged by no-argument formatting. These are not Android resource compilation.
- Temporary token-aware Kotlin checks verify resource bindings, complete text/accessibility assignment, the three Fit routes, unioned bounds, scale/centering, fit-mode refresh, and absence of direct pixel resize/commit calls in `fit`. These are static checks, not Android execution.
- Base snapshot verification matched Git blobs and executable modes for **1,278 materialized files**, retaining **288** unmaterialized entries. Publication verifies the complete path/mode/type/blob overlay, expected-parent non-force lease and exact remote bytes.

Inspected but not run: `CanvasEditingControlsTest.sliderCentreIsExactlyActualSizeAndFitFramesTheCanvas` checks the status Fit control frames canvas corners. `SizingAndTrimTest.touchExpansionOnEverySidePreservesOpaquePixelsAndUndo` checks trim Fit makes an expanded corner visible before separately applying the trim. `ClassicWorkspaceTest.navigatePansWithoutTapZoomAndScrollbarsChangeViewport` calls Fit after zooming. Inspection does not establish execution or this Zhuang label's layout. No permanent per-edit wording mirror or test package is added.

Zhuang presence is P0 **69/94**, P1 **156/249**, P2 **61/305**, P3 **1/71**. Across 171 options, missing resources are P0 **162**, P1 **1,335**, P2 **30,068**, P3 **7,480**; 46 options have complete presence. Scope remains 59 scoped catalogues and 112 outside-scope catalogues with explicit English fallback. Presence is not fluency or runtime acceptance.

Android SDK/Kotlin compiler are unavailable here. Android compilation, Robolectric, viewport fit, selection/trim interaction, TalkBack and button layout were not executed. Exact-head Actions state is checked after publication and reported separately. No merge, release or CI-pass claim is made.
