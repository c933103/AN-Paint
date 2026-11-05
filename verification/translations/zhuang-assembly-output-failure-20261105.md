# Zhuang assembly-output failure notice, 5 November 2026

## Scope and language review

The live branch was reconciled at parent `4269a0999f125b9b4035345630a81fd3c6238fc2`, tree `d6dd64807ecc9a68aea2bd9c96a0bd5db4a6aa75`. The preceding publication was confirmed with no pending or uncertain write. This adds missing P2 `ui_could_not_create_the_assembly`, preserving all 294 previous typed resources for a total of 295. Only canonical XML and this report change.

Independent review recommends the notice meaning “The image assembly could not be made,” with high confidence in code-context fit and **moderate confidence in independent linguistic naturalness**. The [Sawloih Cuengh-Gun OCR](https://dokumen.pub/sawloih-cuengh-gun-ocr.html), retrieved by the reviewer, supports `ndaej` as ability, including post-verbal use, and `buek` as a batch classifier. Existing catalogue notices use the same noun-plus-unable-to-make construction and the same image-assembly compound.

This is compositional support, not proof that the whole compound is standardized computing terminology. The dictionary is an OCR mirror with possible errors. The translation preserves exactly one `%1$s` for the exception detail. It does not diagnose corruption, promise successful saving, or say the assembly or source images were destroyed. No native-human certification is claimed.

The earlier radius candidate remains untranslated: bounded checking did not establish its proposed mathematical term. It is not counted as progress in this batch.

## Actual consumers

Both bindings are in `AssemblyActivity`:

- `requestOutput` catches an ordinary exception while preparing the renderer/output plan. Its existing active-activity guard clears busy state, refreshes the view and formats this notice with `error.message`. An OutOfMemoryError has a separate existing notice.
- `makeOutput` catches an ordinary exception during rendering or temporary PNG creation. It deletes that temporary output and, under the existing destruction guard, clears busy state, refreshes and shows the formatted notice. Memory and image-size failures instead use the existing output-size retry dialog.

The temporary PNG is distinct from the assembly input files. No new deletion or recovery behavior is introduced. Later provider-save failures use a different resource, `ui_could_not_save_the_assembly`. The generic creation notice does not replace that distinction or infer a particular cause from an arbitrary exception.

No rendering, file handling, busy state, retry, lifecycle or error-routing code changes.

## Verification

Work and tests used the available temporary filesystem. No unrelated files were removed from the full main workspace.

- All 171 offered-option catalogue checks and the importance manifest passed. Existing nodes, source attributes, ordered typed arguments, numerals, literal tokens, newline escapes and XML escaping are preserved.
- `python -m unittest -v test_translations test_translation_boundaries test_string_importance test_current_localization_contracts`: **61 tests passed in 20.711 seconds**.
- Eight Java XML-format cases checked English/Zhuang notices with literal percent/format-like tokens, Unicode and newline text, an empty detail, and a null detail. Each detail remains the argument rather than being interpreted as a format string. These are not Android resource compilation or actual exception delivery.
- Temporary token-aware Kotlin checks verified both exception bindings and their detail arguments, distinct memory/size paths, lifecycle/busy-state guards, temporary-output cleanup and the separate provider-save notice.
- Base snapshot verification matched Git blobs and executable modes for **1,285 materialized files**, retaining **288** unmaterialized entries. Publication verifies the complete path/mode/type/blob overlay, expected-parent non-force lease and exact remote bytes.

Inspected but not run: `AssemblyActivityTest.savePngStreamsExactCompositeAndCancelRemovesOnlyTemporaryOutput` and `editInPaintTransfersCompositeAndMainUndoRestoresPreviousCanvas`. These test adjacent success/cancel flows, not injection of the ordinary exceptions localized here. No Android exception-path execution is claimed. No permanent per-edit wording mirror or test package is added.

Zhuang presence is P0 **69/94**, P1 **158/249**, P2 **66/305**, P3 **2/71**. Across 171 options, missing resources are P0 **162**, P1 **1,333**, P2 **30,063**, P3 **7,479**; 46 options have complete presence. Scope remains 59 scoped catalogues and 112 outside-scope catalogues with explicit English fallback. Presence is not fluency or runtime acceptance.

Android SDK/Kotlin compiler are unavailable here. Android compilation, Robolectric, rendering, exception injection, cleanup, lifecycle, TalkBack and device layout were not executed. Exact-head Actions state is checked after publication and reported separately. No merge, release or CI-pass claim is made.
