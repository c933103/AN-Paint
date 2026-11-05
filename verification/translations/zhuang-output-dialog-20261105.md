# Zhuang assembly output-size dialog, 5 November 2026

## Scope and language review

The live branch was reconciled at parent `d2bd0bb7f27d5a5f47e6af190974a256b45b23f0`, tree `5f7ba27e066d8f73bd0b9b8c9e596d5fa2228c83`. The preceding publication was confirmed with no pending or uncertain write. This adds missing P2 `ui_assembly_output_size` and `ui_create_output`, preserving all 298 previous typed resources for a total of 300. Only canonical XML and this report change.

Independent review recommends the functional title “New image dimensions” and button “Make image.” The title identifies the generated result; the surrounding assembly dialog supplies the assembly context. The button describes creating the result without claiming a completed save. Confidence is **moderate for the title** and **moderately high for the button's contextual semantics**.

The [Sawloih Cuengh-Gun OCR](https://dokumen.pub/sawloih-cuengh-gun-ocr.html), independently checked by the reviewer, supports `cikconq` dimensions, `guh` make/build and `moq` new. Its example `Guh ranz moq` also supports noun-before-new order. `Dozsiengq` remains the existing project term for image; this check does not establish the exact full label as standard computing terminology. The OCR mirror may contain transcription errors. An initially proposed longer relative construction was replaced because its grammar was less well supported. No native-human certification is claimed.

## Actual consumer

Both resources are used only by `AssemblyActivity.outputSizeDialog`. DimensionControls starts from the original output extent and a suggested size. The positive button is enabled only for valid dimensions fitting the existing memory estimate, and the click handler rechecks the same condition before calling `makeOutput`. Cancel has no output callback.

`AssemblyRenderer.render` allocates a new bitmap at the chosen dimensions, maps placed inputs into it and rechecks the memory constraint. It does not resize the stored assembly source files. `makeOutput` writes a temporary PNG, then either returns it to painting or opens the document picker. The document-picker path still requires destination selection and writing; creating the temporary output is not a completed save. Image-size or memory failures can reopen the size dialog. No sizing, rendering, source-file, retry, picker or lifecycle logic changes.

The title/button use the complete resources through the existing dialog builder. Device measurements, font scaling and accessibility presentation remain unverified.

## Verification

Temporary files and tests used the available temporary filesystem. No unrelated files were removed from the full main workspace.

- All 171 offered-option catalogue checks and the importance manifest passed. Existing nodes, source attributes, ordered typed arguments, numerals, literal tokens, newline escapes and XML escaping are preserved.
- `python -m unittest -v test_translations test_translation_boundaries test_string_importance test_current_localization_contracts`: **61 tests passed in 8.834 seconds**.
- Four Java XML-to-string cases checked both English/Zhuang title and button for nonempty text and unchanged no-argument formatting. These are not Android resource compilation.
- Temporary token-aware Kotlin checks verified both bindings, dimension/memory guards before rendering, cancellation, creation of a new composite bitmap/temporary PNG, Paint-versus-picker routing and the existing size-failure retry.
- Base snapshot verification matched Git blobs and executable modes for **1,287 materialized files**, retaining **288** unmaterialized entries. Publication verifies the complete path/mode/type/blob overlay, expected-parent non-force lease and exact remote bytes.

Existing assembly renderer/activity tests were inspected for adjacent output behavior, including `savePngStreamsExactCompositeAndCancelRemovesOnlyTemporaryOutput` and `editInPaintTransfersCompositeAndMainUndoRestoresPreviousCanvas`. They were not run and do not establish this translated dialog's fit or its memory-triggered flow. No permanent per-edit wording mirror or test package is added.

Zhuang presence is P0 **69/94**, P1 **158/249**, P2 **71/305**, P3 **2/71**. Across 171 options, missing resources are P0 **162**, P1 **1,333**, P2 **30,058**, P3 **7,479**; 46 options have complete presence. Scope remains 59 scoped catalogues and 112 outside-scope catalogues with explicit English fallback. Presence is not fluency or runtime acceptance.

Android SDK/Kotlin compiler are unavailable here. Android compilation, Robolectric, actual dialog/rendering/source-file preservation, memory retries, picker completion, TalkBack and device layout were not executed. Exact-head Actions state is checked after publication and reported separately. No merge, release or CI-pass claim is made.
