# Zhuang canvas-boundary controls, 5 November 2026

## Scope and wording

The live branch was reconciled at parent `361ec6d195a459854082b557a135803b4d4c049a`, tree `43cc581361c0cec692f0d999271755f31a566f18`; no operation was pending. This fills P1 `ui_canvas_bounds` and `ui_apply_bounds`. All 268 preceding typed resources remain unchanged; the total is 270. Only canonical XML and this report change.

Independent wording/context review recommended “Edges/boundaries of the drawing area” and “Use/apply these bounds.” The latter directly identifies the previewed bounds being committed. A proposed “apply changes to boundaries” paraphrase was plausible but introduced unnecessary nominalization uncertainty; the narrower wording was selected and rechecked. Neither label implies crop-only behavior or image resampling.

Sources:
- [Sawloih Cuengh-Gun dictionary OCR](https://dokumen.pub/sawloih-cuengh-gun-ocr.html), H24/B32/D51/Y29: `henz` edge/side, `benq` an area classifier, `dieg` area/place, and `yungh` use/apply. This is an OCR transcription, not a guarantee of transcription accuracy or official software terminology.
- [Guangxi Minzu Bao, “Veh Gyaeq,” 6 July 2016](https://www.guangximinzubao.cn/szbzw/html/2016-07/06/content_18139.htm), independently supports drawing usage of `veh`.
- [Gyaucingz Gihcuj Vahcuengh, lesson 3](https://newdoc.nccu.edu.tw/teasyllabus/113721209100/Lesson%203.pdf), page 2, supports general head–modifier order and postposed `neix`, “this.”

Confidence is **moderate** in whole-phrase idiomaticity, stronger in component meanings and functional accuracy. These are descriptive compositions, not attested official computing terms. No native-human certification or complete-language acceptance is claimed. Canonical XML owns the wording.

## Actual consumers

`ClassicPaintActivity` has one direct binding per key. The Canvas bounds command opens `trimCanvas` and its preview controls; Apply bounds invokes `paintCanvas.applyTrim` before closing those controls. Cancel follows a distinct `cancelTrim` path.

`PaintCanvas.beginTrim` applies preceding pending work, then creates `CropOverlay` with `allowOutside=true`. The rectangular preview supports edge/corner changes and translation, including expansion beyond the original canvas. Applying passes its rectangle to `PaintDocument.changeCanvasBounds`. That method validates dimensions, returns immediately for unchanged bounds, checks memory, creates a background-filled bitmap and offsets the existing bitmap by the rectangle origin without scaling. Cropped overflow is clipped; expanded area uses the background. Changed output is an undoable edit.

Cancel discards the boundary preview; it does not undo unrelated pending work already committed when this mode was entered. No touch, pixel, history, memory-policy or cancellation implementation changes.

## Verification

- All 171 offered-option catalogue checks and the importance manifest passed. Existing nodes, source attributes, ordered arguments, numerals, literal tokens, newline escapes and XML escaping are preserved.
- On the final reviewed wording, `python -m unittest -v test_translations test_translation_boundaries test_string_importance test_current_localization_contracts`: **61 tests passed in 10.296 seconds**.
- Four host Java XML-to-string cases check no-argument labels without added ellipses or newlines. This is not Android resource compilation.
- Temporary token-aware Kotlin checks verify both bindings, expansion-enabled preview, distinct apply/cancel routes, no-op return before allocation/replacement, background fill and origin translation without scaling. They do not execute Android gestures or bitmaps.
- Base snapshot verification matched Git blobs and executable modes for **1,285 materialized files**, retaining **269** unmaterialized entries. Publication checks the complete path/mode/type/blob overlay, expected-parent non-force lease and exact remote bytes.

Three existing `SizingAndTrimTest` methods were inspected, not run: `cancellingTouchTrimKeepsAllPixelsAndTrimCanRemoveLeftAndTopMargins`, `touchExpansionOnEverySidePreservesOpaquePixelsAndUndo`, and `noOpBoundsCreateNoHistoryAndUndoCancelsOnlyThePendingExpansion`. No permanent per-edit wording mirror or test package is added.

Zhuang presence is P0 **69/94**, P1 **147/249**, P2 **54/305**, P3 **0/71**. Across 171 options, missing resources are P0 **162**, P1 **1,344**, P2 **30,075**, P3 **7,481**; 46 options have complete presence. Scope remains 59 scoped catalogues and 112 outside-scope catalogues with explicit English fallback. Presence is not fluency or runtime acceptance.

Android SDK/Kotlin compiler are unavailable here. Android compilation, Robolectric, touch/bitmap behavior, undo, TalkBack and layout were not executed. Exact-head Actions state is checked after publication and reported separately; this review branch does not normally trigger CI. No merge, release or CI-pass claim is made.
