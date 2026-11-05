# Zhuang text-tool tap instruction, 5 November 2026

## Scope and wording review

The live branch was reconciled at parent `db4cbc5308301ff7a5bf84896f054c4e10347f71`, tree `96438330715d71120a31396a2a1c8ea663a35411`; no write was pending. This fills missing P1 `ui_tap_canvas_to_type`. All 264 preceding typed resources remain unchanged; the total is 265. Only canonical XML and this report change.

Independent wording/context review retained the descriptive rendering “Tap the drawing area to enter/write text.” It uses a drawing-area phrase rather than claiming an established computing term for canvas. The source's explicit newline remains between the action/location and purpose clauses. Existing resources provide compatible conventions for tapping to enter a number, selecting an area, drawing and entering text; their presence alone is not linguistic proof.

Supporting sources:

- [Sawloih Cuengh-Gun dictionary OCR](https://dokumen.pub/sawloih-cuengh-gun-ocr.html), B32 and D51, supports `benq` as an area classifier and `dieg` as area/place. The independent reviewer also checked draw/write entries and place-plus-activity compounds. The dictionary's older senses of `diemj` do **not** independently establish touchscreen tapping; that is the existing UI convention, reviewed in context here.
- [Guangxi Minzu Bao, “Veh Gyaeq,” 6 July 2016](https://www.guangximinzubao.cn/szbzw/html/2016-07/06/content_18139.htm), is a primary drawing context for `veh`.
- [Gyaucingz Gihcuj Vahcuengh, lesson 3](https://newdoc.nccu.edu.tw/teasyllabus/113721209100/Lesson%203.pdf), page 2, describes general noun-phrase head-before-modifier ordering. It is compatible with the descriptive construction, not attestation of the exact software phrase.

Confidence is **moderate** on idiomatic composition and high on the intended UI behavior. No native-user approval, established canvas terminology or complete-language acceptance is claimed. Canonical XML owns the full wording.

## Actual consumer

`ClassicPaintActivity.populateToolOptions` has the sole direct resource binding: the TEXT tool displays the complete selected resource as a 12sp `FlowTextView` label. It is an instruction, not the text-entry field itself.

`PaintCanvas.handleTouch` invokes `onText` with image coordinates on the relevant touch release, after existing multitouch, scrolling, panning and selection handling. The activity callback opens `TextStyleDialog`. Its multiline input uses the separate existing type-text hint. Confirming valid settings places the text at those coordinates through `document.text`; cancellation does not call that confirmation callback. Tapping alone does not immediately draw text. No interaction or placement implementation changes.

## Executed checks

- All 171 offered-option catalogue checks and the importance manifest passed. Existing nodes, source attributes, ordered format arguments, source numerals, literal tokens, newline escapes and XML escaping remain intact.
- `python -m unittest -v test_translations test_translation_boundaries test_string_importance test_current_localization_contracts`: **61 tests passed in 9.538 seconds**.
- Two host Java XML-to-string cases check one escaped newline, two nonempty clauses and unchanged no-argument formatting. Host newline substitution is not Android resource compilation.
- Temporary token-aware Kotlin checks verify the full-resource TEXT label, touch-release callback, coordinate-preserving dialog path, multiline input and confirmation-before-placement. They are static checks, not executed gestures or rendering.
- Base snapshot verification matched Git blobs and executable modes for **1,282 materialized files**, retaining **269** unmaterialized entries. Publication checks the complete path/mode/type/blob overlay, fresh expected-parent non-force lease and exact remote bytes.

`ClassicWorkspaceTest.textToolDialogPlacesTextAndCanBeUndone` was inspected, not run. It exercises selecting TEXT, tapping, entering text, confirming placement and undo; it does not certify Zhuang label layout. No permanent per-edit wording mirror or test package is added.

## Coverage and limits

Zhuang presence is P0 **69/94**, P1 **142/249**, P2 **54/305**, P3 **0/71**. Global missing resources across 171 options are P0 **162**, P1 **1,349**, P2 **30,075**, P3 **7,481**; 46 options have complete presence. Scope remains 59 scoped catalogues and 112 outside-scope catalogues with explicit English fallback. Presence does not establish fluency or runtime acceptance.

Android SDK and Kotlin compiler are unavailable here. Android compilation, Robolectric, touchscreen/keyboard behavior, text placement, TalkBack and label layout were not executed. Exact-head Actions state is checked after publication and reported separately; this review branch does not normally trigger CI. No merge, release or CI-pass claim is made.
