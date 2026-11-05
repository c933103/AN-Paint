# Zhuang assembly membership and drag description, 5 November 2026

## Scope and language review

Reconciled parent `b5ccb8e8f6d373b2f6c4dc6cf91711232494a7b0`, tree `029ec109562c38c50e6ee14e570c9fb2cb4c68fa`, with the preceding publication complete. This adds missing P2 `ui_assembly_unknown_image` and `ui_an_paint_assembly_image`. All 300 previous typed resources remain unchanged, for 302 total. Only canonical XML and this report change.

The error says the selected image is no longer in this assembly. Independent review found no concrete grammatical or contextual error in the proposed negative sentence with final `lo`, and considered explicit `mbouj caiq` defensible. The latter is included to preserve “no longer,” rather than merely saying “absent now.” The drag label describes an image in the AN Paint assembly, not a completed composite. Confidence is **moderate**, without a claim of certified software terminology or native-human certification.

Evidence:

- The independently inspected [Sawloih Cuengh-Gun dictionary OCR](https://dokumen.pub/sawloih-cuengh-gun-ocr.html), L1119, explains sentence-final `lo` as an assertion/request particle. Its example under `mboujmiz`, L1227, uses a negative sentence with final `lo` for not waiting any longer/now. This supports a changed negative state, not an invariant equivalence between every negative-plus-`lo` and “no longer.” OCR transcription can be imperfect.
- The directly retrieved [Guangxi Minzu Bao article of 8 January 2025](https://www.guangximinzubao.cn/szbzw/html/2025-01/08/content_52410.htm), L34, uses `aen ranzcoj mbouj caiq nauhyied` after residents move away. It supports the explicit negative continuation construction, not the complete technical sentence.
- `Dozsiengq` and `buek` retain existing project image/assembly terminology. Dictionary `buek` denotes a batch of goods, not a certified computing term. The labels are contextual constructions, not quotations from a software glossary.

## Actual consumers

`ImageAssembly.position` is the only direct consumer of the missing-image resource. It checks ID membership before coordinates or model changes. The message does not diagnose source-file corruption, decoding failure or loss of a device file.

The Exact position action opens `AssemblyPositionDialog` in `AssemblyPlacementDialog.kt`. Apply calls `assembly.position`; exceptions display the complete message in `assembly_position_error`, a polite accessibility live region, without dismissing the dialog. The initial `show()` lookup is outside this handler; this change does not add recovery for an ID already missing before opening.

`AssemblyActivity.renderTray` uses the second resource only as the label for `ClipData.newPlainText`. Its payload and local drag state remain `item.id`, in both modern and legacy drag-start branches. `AssemblyCanvas.onDragEvent` reads the ID from local state or clip text, not the translated description. This is drag metadata, not a system-clipboard write, image-byte transfer, output creation or save confirmation.

## Verification and recovery

Before the publication interruption:

- All 171 offered-option catalogue checks and the importance manifest passed. Existing nodes, source attributes, ordered arguments, source numerals, literal tokens, newline escapes and XML escaping were preserved.
- `python -m unittest -v test_translations test_translation_boundaries test_string_importance test_current_localization_contracts`: **61 tests passed in 9.805 seconds**.
- Four Java English/Zhuang XML-to-string cases passed for nonempty text and unchanged no-argument formatting. These are not Android resource compilation.
- Token-aware source checks passed for both unique bindings, the missing-ID guard, dialog error path and unchanged ID-based drag handling.
- Base snapshot verification matched Git blobs and executable modes for **1,288 materialized files**, retaining **288** unmaterialized entries.

The execution workspace was then replaced and temporary source snapshots/logs disappeared. Reconciliation found the remote branch unchanged and both intended new blobs absent (404); no branch update had been performed. The canonical XML was reconstructed from the unchanged remote base and the reviewed additions. Its **28,636 bytes exactly match the previously tested Git blob `5037ee4244d75a754ca33f84b1fb564d601d5bff`**. Previous-resource/prefix checks, four Java cases and targeted consumer checks passed again after recovery. The four consumer files and tokenizer were freshly retrieved at the same parent and their identities matched its tree. The full 61-test suite and 171-option sweep were not rerun after replacement; their passing results above are the observed pre-interruption run on the identical XML/base, not new runs. Raw temporary logs are no longer available.

Publication checks the complete path/mode/type/blob overlay, expected-parent non-force lease and exact remote bytes. No unrelated files were deleted. No permanent per-edit wording mirror or test package is added.

Existing `AssemblyModelTest.invalidCoordinatesAreAtomicAndDoNotConsumeUndo` includes a missing-ID case and state/file preservation checks. `AssemblyActivityTest.multiPickerLoadsNamesTimesAndThumbnailsThenNativeDragEventsSnapBothDirections` exercises adjacent drag behavior. Both were inspected, not executed; neither establishes this Zhuang error's layout/accessibility.

Zhuang presence: P0 **69/94**, P1 **158/249**, P2 **73/305**, P3 **2/71**. Global missing counts over 171 options: P0 **162**, P1 **1,333**, P2 **30,056**, P3 **7,479**; 46 options have complete presence. Scope stays 59 scoped catalogues plus 112 outside-scope catalogues with explicit English fallback. Presence is not fluency or runtime acceptance.

Android SDK/Kotlin compiler were unavailable for the original checks. Android compilation, Robolectric, actual stale-ID interaction, drag/drop, TalkBack and device/font-scale layout were not executed. Exact-head Actions state is checked after publication and reported separately. No merge, release or CI-pass claim is made.
