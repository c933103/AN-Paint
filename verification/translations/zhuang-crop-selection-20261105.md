# Zhuang crop-to-selection command, 5 November 2026

## Scope and wording

The live branch was reconciled at parent `88bc5d348e7fc83a91be85d51acc2924a11ef05e`, tree `6218e248390594531c3eb5af50e2ccc533c73b8d`; no operation was pending. This fills missing P1 `ui_crop_to_selection`. All 267 preceding typed resources remain unchanged; the total is 268. Only canonical XML and this report change.

Independent wording/context review recommended the composed command “Trim/crop according to the selection.” The according-to phrase precedes the action; an English-influenced postverbal alternative was not used. No ellipsis or format argument is added.

- [Sawloih Cuengh-Gun dictionary OCR](https://dokumen.pub/sawloih-cuengh-gun-ocr.html), C57/D23/H24/S24/G37, supports the components: `ciuq` according to, `daet` cut, `henz` edge, `senj` select and nominalizing `gij`. These support the composition, not established digital-cropping terminology.
- [Guangxi Minzu Bao, “Veh Gyaeq,” 6 July 2016](https://www.guangximinzubao.cn/szbzw/html/2016-07/06/content_18139.htm), paragraph beginning “Ngoenzcog,” uses `ciuq yiengh makdauz nyinhcaen bae veh`, independently supporting the preverbal according-to-model construction.

The existing crop and selection vocabulary is consistent with this label, but catalogue presence is not linguistic proof. Confidence is **moderate**: the complete phrase, selection noun and digital crop idiom are not independently attested in a native software corpus. No native-human certification or complete-language acceptance is claimed. Canonical XML owns the wording.

## Actual consumer and meaning

`ClassicPaintActivity` has the sole direct binding in the Edit command list. It calls `document.cropSelection()`, fits the result on success, or displays the existing select-an-area-first notice when there is no selection.

`PaintDocument.cropSelection` obtains the transformed selection image, finishes the selection and replaces the document as an undoable edit. `transformedSelectionImage` renders the current scaled/rotated selection into the axis-aligned bounds of its four transformed corners, rounding dimensions upward and applying existing memory checks. Initial selection capture intersects the canvas and applies any optional path mask. Later crop output can include floating selection content moved outside the original canvas: it is **not** merely a crop of the original canvas rectangle at the selection's current position.

Replacement fills transparent areas behind selected content with the background. Rotated corners and nonrectangular selections therefore produce rectangular, opaque output with background outside the selected content. No geometry, clipping, bitmap, history or memory-policy implementation changes.

## Verification

- All 171 offered-option catalogue checks and the importance manifest passed. Existing nodes, source attributes, ordered arguments, numerals, literal tokens, newline escapes and XML escaping are preserved.
- `python -m unittest -v test_translations test_translation_boundaries test_string_importance test_current_localization_contracts`: **61 tests passed in 9.999 seconds**.
- Two host Java XML-to-string cases check complete no-argument commands without an added newline or ellipsis. This is not Android resource compilation.
- Temporary token-aware Kotlin checks verify the command binding, no-selection path, transformed geometry bounds, rendering origin, memory admission, background flattening and undo checkpoint. They do not execute bitmap operations.
- Base snapshot verification matched Git blobs and executable modes for **1,284 materialized files**, retaining **269** unmaterialized entries. Publication checks the complete path/mode/type/blob overlay, expected-parent non-force lease and exact remote bytes.

`CanvasEditingControlsTest.copyAndCropUseTheRotatedSelectionDimensionsAndPixels` was inspected, not run. It checks 90-degree selection rotation, output dimensions/pixels and undo. It does not cover every nonrectangular or outside-canvas case. No permanent per-edit wording mirror or test package is added.

Zhuang presence is P0 **69/94**, P1 **145/249**, P2 **54/305**, P3 **0/71**. Across 171 options, missing resources are P0 **162**, P1 **1,346**, P2 **30,075**, P3 **7,481**; 46 options have complete presence. Scope remains 59 scoped catalogues and 112 outside-scope catalogues with explicit English fallback. Presence is not fluency or runtime acceptance.

Android SDK/Kotlin compiler are unavailable here. Android compilation, Robolectric, crop rendering, undo, TalkBack and command layout were not executed. Exact-head Actions state is checked after publication and reported separately; this review branch does not normally trigger CI. No merge, release or CI-pass claim is made.
