# Zhuang assembly-to-editor action, 5 November 2026

## Scope

The live branch was reconciled at parent `fd7924bf03b87d1d95861e02d32b763820f58ff7`, tree `1e8b46c86fa81e9222b51cf3471080c8dc53ba9d`; no earlier operation was pending. This change fills the missing P2 scalar `ui_edit_in_paint` (“Edit in Paint”) in canonical `Paintroid/src/main/res/values-b+za/strings.xml`. It preserves all 250 preceding typed resources and brings the total to 251. The only published changes are that XML and this report. Product name `Paint`, application behavior and other catalogues remain unchanged.

## Wording evidence

The [digitized Zhuang–Chinese dictionary](https://dokumen.pub/sawloih-cuengh-gun-ocr.html), main sections G15 and Y27, supports `gaij` for modify/change and `youq` for at/in. These are the main entries, rather than similarly spelled dialect material elsewhere in the OCR.

Independent linguistic/context review recommended the location-before-action construction, rather than copying English order. Its supporting grammar example appears in *Studies in Linguistics and Literature*, 7(4), 2023, §2.3.4, p.238: [indexed PDF passage](https://www.scholink.org/ojs/index.php/sll/article/download/35742/8656). The example places the classroom-location phrase before reading. The relevant passage was independently retrieved from the search index; the reviewer's direct PDF open returned 404, so this is indexed evidence, not a downloaded/inspected paper. The primary [Hoenz Fwen text](https://www.guangximinzubao.cn/szbzw/html/2017-12/27/content_24064.htm), extracted line 30, also places a location phrase before the waving action in the bronze-box description.

Review found no substantive semantic blocker. The action edits the output in Paint, rather than editing the assembly layout or saving to an external destination. This is a supported compositional translation, not an attested existing Paint label or native-user validation. Canonical XML owns the complete current wording.

## Actual consumer and preserved behavior

- `AssemblyActivity.kt:53–56,83–88`: the complete resource is ordinary Button text, without all-caps transformation, in a horizontally scrollable action row. The helper gates clicks while busy. The Edit action calls `requestOutput(true)`; the separate Save PNG action passes false.
- `requestOutput` rejects an empty/unplaced assembly and either renders at the original size or offers a smaller-output dialog according to the existing fit check. The true/false destination flag is carried through that dialog and memory-size retry paths.
- `makeOutput` renders and encodes a temporary PNG. A completed edit output returns `assembly_output` with RESULT_OK and closes the assembly activity. The false branch instead launches the external save picker. If the activity is destroyed/finishing, the temporary output is deleted.
- `ClassicPaintActivity.kt:1244–1248` validates the returned file's location/name/existence and calls `readImage` with `asEdit=true` and deletion after copying. The result replaces the main canvas; `PaintDocument.replace` checkpoints the previous image when `asEdit` is true. The label does not promise non-destructive editing of the assembly layout or an external save.

These are source/control-flow findings, not executed Android behavior. Actual button fit, scrolling and accessibility remain untested.

## Targeted checks

- All 171 offered-option catalogue checks and importance-manifest validation passed, together with source attributes, format contract, literal-token/escaping and existing-resource preservation checks. A separate literal check retained exactly one `Paint` product name.
- `python -m unittest -v test_translations test_translation_boundaries test_string_importance test_current_localization_contracts`: **61 tests passed in 8.359 seconds**.
- Host Java parsed English and integrated Zhuang XML and formatted the label without arguments: **2 literal cases passed**, not Android resource compilation.
- Temporary token-aware checks passed for complete button binding, busy guard, distinct edit/save flags, empty/size/lifecycle guards, destination propagation through retries, result validation, temporary cleanup and the undo checkpoint.
- Base snapshot verification checked **1,273 materialized files** against their Git blob identities and executable modes. **269** unmaterialized non-tree entries are retained. Publication verifies the complete path/mode/type/blob overlay, fresh expected parent, non-force lease and final exact-file readback.

`AssemblyActivityTest.editInPaintTransfersCompositeAndMainUndoRestoresPreviousCanvas` was inspected. It covers output transfer, replacement pixels, undo/redo and temporary cleanup, but was **not executed** here. No permanent per-edit wording mirror or test package is added.

## Coverage and limits

Zhuang presence is P0 **69/94**, P1 **133/249**, P2 **49/305**, P3 **0/71**. Global missing typed resources across 171 options are P0 **162**, P1 **1,358**, P2 **30,080**, P3 **7,481**; 46 options have complete resource presence. The scope remains 59 scoped catalogues plus 112 outside-scope catalogues with explicit English fallback. Presence does not establish fluency or runtime acceptance.

Android compilation, Robolectric, device rendering/layout, TalkBack, assembly transfer and undo execution were not run. Exact-head Actions state is checked after publication and reported separately; this review-branch push does not normally trigger CI. No merge, release, CI-pass or complete-language claim is made.
