# Zhuang Canvas and Flip / Rotate categories, 5 November 2026

## Scope and wording

The live review branch was reconciled at parent `72cc2d747a775d7983a42d955dcc890abd88323a`, tree `9f891cb91b6c9c0771a57a56dc4779763fcc6ccf`. No write was pending or uncertain. This fills two missing P1 category labels, `ui_edit_canvas33` and `ui_edit_transform33`. All 273 preceding typed resources remain unchanged; the total is 275. Only canonical XML and this report change.

Independent wording/context review recommended the drafts unchanged: the Canvas category is described as “drawing area”, while Flip / Rotate names the two distinct operations. [Sawloih Cuengh-Gun dictionary OCR](https://dokumen.pub/sawloih-cuengh-gun-ocr.html) supports `benq` as an area/expanse classifier (B section 32/80), `dieg` as region/place (D 51/110), `fan` as flip/turn over (F 10/29), and `baenq` as turn/rotate (B 9/80). These references are the OCR's internal section pagination, not verified printed-book page numbers. The OCR's transcription warning remains relevant.

[Guangxi Minzu Bao, “Veh Gyaeq”, 6 July 2016, page 05](https://www.guangximinzubao.cn/szbzw/html/2016-07/06/content_18139.htm) independently corroborates `veh` as draw. It does not attest the complete drawing-area expression or software terminology. Lexical and consumer fit is strong for the two transform verbs. The complete drawing-area phrase has moderate idiomatic confidence, with no concrete semantic contradiction found. No official technical-term status, native-human certification or whole-language acceptance is claimed. Canonical XML owns the wording.

A separate bounded check did not support a reliable noun phrase for the text line-spacing percentage control. That resource remains on its existing English fallback rather than introducing an unsupported distance/interval construction. This is a specific wording-evidence gap, not a native-human approval gate.

## Actual consumers

`ClassicPaintActivity.EditGroup` supplies both category labels. Each `panelButton` receives the complete localized string as text, accessibility description and tooltip. Clicking the category toggles its disclosure and the visible command group; it does not immediately change image pixels.

Canvas exposes bounds, canvas dimensions, image resize, color inversion and image clear, at command indices 1, 3, 5, 10 and 11. “Drawing area” is the category umbrella, not a promise that every action only adjusts dimensions. Transform exposes horizontal and vertical reflections plus 90-degree and 180-degree rotations, at indices 6 through 9. Its negative-scale and rotation matrices remain unchanged.

`PanelToolButton` retains fixed 64 dp tiles. Horizontal captions use at most two lines and ellipsis; complete text remains available to accessibility and tooltips. This binding is not evidence that the Zhuang captions fit without ellipsis on every device or font setting. No category, image, history or layout implementation changes.

## Verification

- All 171 offered-option catalogue checks and the importance manifest passed. Existing nodes, source attributes, ordered arguments, numerals, literal tokens, newline escapes and XML escaping are preserved.
- `python -m unittest -v test_translations test_translation_boundaries test_string_importance test_current_localization_contracts`: **61 tests passed in 10.405 seconds**.
- Four host Java XML-to-string cases check nonempty English/Zhuang labels, unchanged no-argument formatting and the slash separating transform operations. They do not compile Android resources.
- Temporary token-aware Kotlin checks verify both direct resource bindings, full label/accessibility/tooltip assignment, disclosure toggling, command-index mappings, reflection/rotation matrices and retained tile/ellipsis behavior. These are static consumer checks, not Android execution.
- Base snapshot verification matched Git blobs and executable modes for **1,288 materialized files**, retaining **269** unmaterialized entries. Publication verifies the complete path/mode/type/blob overlay, expected-parent non-force lease and exact remote bytes.

The inspected `ResponsiveToolboxTest.editGroupsExposeTheirActionsAndCanvasBoundsReturnToTheGroup` exercises group expansion/collapse, selection preservation, bounds cancellation and transform/canvas action visibility in the existing English workspace. It was not run. No permanent per-edit wording mirror or test package is added.

Zhuang presence is P0 **69/94**, P1 **152/249**, P2 **54/305**, P3 **0/71**. Across 171 options, missing resources are P0 **162**, P1 **1,339**, P2 **30,075**, P3 **7,481**; 46 options have complete presence. Scope remains 59 scoped catalogues and 112 outside-scope catalogues with explicit English fallback. Presence is not fluency or runtime acceptance.

Android SDK/Kotlin compiler are unavailable here. Android compilation, Robolectric, category interaction, screen layout, caption fit, TalkBack and image transforms were not executed. Exact-head Actions state is checked after publication and reported separately. No merge, release or CI-pass claim is made.
