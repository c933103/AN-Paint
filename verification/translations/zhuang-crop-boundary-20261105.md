# Zhuang assembly crop-boundary warning, 5 November 2026

## Scope and wording

The live review branch was reconciled at parent `19accf33430c37a94fc0755ec90a4300161e7d5b`, tree `e50a0300ca58b621926daf78582320b4a2a912bd`. No write was pending or uncertain. This adds missing P1 `ui_the_crop_must_stay_inside_the_image`. All 275 preceding typed resources remain unchanged; the total is 276. Only canonical XML and this report change.

Independent wording/context review retained the proposed warning, intended as “The crop must be within the image”, with **moderate linguistic confidence**. [Sawloih Cuengh-Gun dictionary OCR](https://dokumen.pub/sawloih-cuengh-gun-ocr.html) supports the components: `daet` cut (D23), `henz` edge (H24), nominalizing use of `gij` (G37), `yaekaeu` must (Y4), and `ndaw` inside (main N20). The appendix's sawndip Y7 additionally supports `youq` be/stay at. These are internal section-page references; the OCR is not a verified transcription.

The remaining uncertainty is that the compound for crop can denote cropping rather than unambiguously naming the retained rectangle. The dictionary does not attest this complete technical noun or UI sentence. Existing project usage supports consistency but is not independent evidence of idiomaticity. Review found no concrete contradiction in this crop-validation context and did not recommend introducing a second unsupported “cropped area” construction. No native-human certification, official terminology status or whole-language acceptance is claimed. Canonical XML owns the wording.

## Actual consumer and boundaries

`ImageAssembly.validate` is the sole direct consumer. It checks every crop against that item's source-image dimensions: left/top must be nonnegative, right/bottom may equal but not exceed the source boundary, and width/height must be positive. This is not the assembled output's boundary or the editor canvas. The English warning itself does not spell out positivity; the translation does not add an unrelated promise or new condition.

The rectangle-based crop overloads pass candidate metadata to `change`. Validation occurs before project-state writing, undo mutation and state replacement; no silent clipping is performed by this guard. Original files and validation logic are unchanged. Assembly initialization also validates restored state.

`AssemblyActivity` supplies the crop dialog's callback to `assembly.crop`. `ImageCropDialog` catches an exception from applying crops and displays its message in the status text, dismissing only after a successful application. Ordinary margin entry has earlier range checks, so this does not claim that every invalid user-entered crop reaches this particular warning. The similarly named `ui_crop_must_stay_inside_the_canvas` remains unchanged: its `cropCanvas` wrapper has no current production call site in the inspected sources.

## Verification

- All 171 offered-option catalogue checks and the importance manifest passed. Existing nodes, source attributes, ordered arguments, numerals, literal tokens, newline escapes and XML escaping are preserved.
- `python -m unittest -v test_translations test_translation_boundaries test_string_importance test_current_localization_contracts`: **61 tests passed in 10.544 seconds**.
- Two host Java XML-to-string cases check nonempty English/Zhuang warnings and unchanged no-argument formatting. They do not compile Android resources.
- Temporary token-aware Kotlin checks verify the source-image boundary predicate, positive extents, validation before mutation, both rectangle overloads, dialog callback/error-message propagation and exclusion of the unused canvas wrapper. They are static checks, not execution of the crop model or UI.
- Base snapshot verification matched Git blobs and executable modes for **1,289 materialized files**, retaining **269** unmaterialized entries. Publication verifies the complete path/mode/type/blob overlay, expected-parent non-force lease and exact remote bytes.

The inspected `AssemblyModelTest.cropReflowsAttachmentsAndAnInvalidBatchIsAtomicWithUndoRedoAndPersistence` checks crop metadata, original-byte preservation, invalid-batch atomicity, history and reload. Its invalid batch uses in-bounds rectangles that cause an arrangement problem; it is **not** a dedicated out-of-bounds crop test. It was not run. No permanent per-edit wording mirror or test package is added.

Zhuang presence is P0 **69/94**, P1 **153/249**, P2 **54/305**, P3 **0/71**. Across 171 options, missing resources are P0 **162**, P1 **1,338**, P2 **30,075**, P3 **7,481**; 46 options have complete presence. Scope remains 59 scoped catalogues and 112 outside-scope catalogues with explicit English fallback. Presence is not fluency or runtime acceptance.

Android SDK/Kotlin compiler are unavailable here. Android compilation, Robolectric, crop-model execution, persistence/undo, warning routing, TalkBack and status layout were not executed. Exact-head Actions state is checked after publication and reported separately. No merge, release or CI-pass claim is made.
