# Zhuang canvas-size labels, 5 November 2026

## Scope and wording

The live branch was reconciled at parent `d908e3b4e42284d6a0217a1e47fb34bdbdb35982`, tree `fc562cb45237c4a5355ef2bca512ee0706141378`; no operation was pending. This fills P1 `ui_canvas_size` and `ui_canvas_size_30460e`. All 265 preceding typed resources remain unchanged; the total is 267. Only canonical XML and this report change.

Independent wording/context review accepted the descriptive labels “Drawing-area dimensions…” and “Drawing-area dimensions.” The command retains its ellipsis; the dialog title does not add one. The drawing-area description preserves the distinction from the existing image-resize wording, which describes changing the picture's dimensions. It is not presented as an established software term for canvas.

Sources:
- [Sawloih Cuengh-Gun dictionary OCR](https://dokumen.pub/sawloih-cuengh-gun-ocr.html), C50/B32/D51: `cikconq` means dimensions, `benq` is an area classifier, and `dieg` means area/place.
- [Guangxi Minzu Bao, “Veh Gyaeq,” 6 July 2016](https://www.guangximinzubao.cn/szbzw/html/2016-07/06/content_18139.htm): a primary drawing context for `veh`.
- [Gyaucingz Gihcuj Vahcuengh, lesson 3](https://newdoc.nccu.edu.tw/teasyllabus/113721209100/Lesson%203.pdf), page 2: general head-before-modifier noun-phrase ordering, compatible with the dimensions-of-drawing-area composition.

The sources support components and general structure, not the complete software label. Semantic confidence is high; idiomatic composition remains **moderate**. No native-user certification or complete-language acceptance is claimed. Canonical XML owns the wording.

## Actual consumers

`ClassicPaintActivity` has one direct binding for each resource. The edit command opens `dimensionsDialog(false,false)`. The dialog selects the canvas-size title only for the nonfresh, nonstretch branch, independently of the new-image and image-resize titles. Existing instructions explain the top-left pixel preservation and potential cropping.

Confirmation validates dimensions and memory, applies pending work and calls `document.resize` with `stretch=false`. `PaintDocument.resize` creates the new background-filled bitmap and draws the original at `(0,0)` without scaling; overflow is clipped and expanded area retains the background. The stretch branch instead scales into the new rectangle. The separately named interactive Canvas bounds command is unchanged. No resizing, bitmap or memory-policy implementation changes.

## Verification

- All 171 offered-option catalogue checks and the importance manifest passed. Existing nodes, source attributes, ordered arguments, numerals, literal tokens, newline escapes and XML escaping are preserved.
- `python -m unittest -v test_translations test_translation_boundaries test_string_importance test_current_localization_contracts`: **61 tests passed in 13.902 seconds**.
- Four host Java XML-to-string cases check unchanged no-argument formatting and command-only ellipses. This is not Android resource compilation.
- Temporary token-aware Kotlin checks verify both bindings, nonfresh/nonstretch routing, separate titles, validation sequence and unscaled origin copying. They do not execute bitmap operations.
- Base snapshot verification matched Git blobs and executable modes for **1,283 materialized files**, retaining **269** unmaterialized entries. Publication checks the complete path/mode/type/blob overlay, expected-parent non-force lease and exact remote bytes.

`SizingAndTrimTest.resizeAndCanvasSizeDialogsSupportPercentAndOptionalRatioLock` was inspected, not run. It exercises percentage sizing, optional aspect locking, preserved pixel location, background expansion and undo. No permanent per-edit wording mirror or test package is added.

Zhuang presence is P0 **69/94**, P1 **144/249**, P2 **54/305**, P3 **0/71**. Across 171 options, missing resources are P0 **162**, P1 **1,347**, P2 **30,075**, P3 **7,481**; 46 options have complete presence. Scope remains 59 scoped catalogues and 112 outside-scope catalogues with explicit English fallback. Presence is not fluency or runtime acceptance.

Android SDK/Kotlin compiler are unavailable here. Android compilation, Robolectric, bitmap behavior, TalkBack and dialog/button layout were not executed. Exact-head Actions state is checked after publication and reported separately; this review branch does not normally trigger CI. No merge, release or CI-pass claim is made.
