# Zhuang image-assembly input limit, 6 November 2026

## Scope and wording

Reconciled branch parent `530e5ba2e3441c91e3505471e0aaa9e048055a0c`, tree `a21749c50386c03060e38f20548ce5e6b9ba350c`, with no pending write. A clean full checkout was restored after the previous workspace replacement. This adds missing P2 `ui_an_assembly_can_contain_up_to_20_images` and `ui_an_assembly_can_contain_up_to_20_images_86d995`. Both have real consumers. All 302 previous typed resources remain unchanged; total presence is 304. Only canonical XML and this report change.

Independent review retains a sentence stating that the images in this assembly cannot number more than 20, preserving the inclusive maximum. The longer variant instructs removal of one image so another can be added. The reviewer added the individual classifier `aen` in that instruction, consistent with existing project phrases for selecting/tapping one image. The collective `gij` at the start of the limit sentence is not used as a numeral counting classifier.

The [Sawloih Cuengh-Gun dictionary OCR](https://dokumen.pub/sawloih-cuengh-gun-ocr.html), independently checked, supports `duz` remove/delete, `dem` add/increase and `wnq` other. [gvaq](https://en.wiktionary.org/wiki/gvaq) and [ndaej](https://en.wiktionary.org/wiki/ndaej) provide secondary lexical support for comparison and permission/ability. A [People's Daily Zhuang text](https://sawcuengh.people.com.cn/158003/15813514.html) supplied **search-index-only** corroboration of `lai gvaq` in a numerical comparison; direct retrieval returned 502. It does not attest this exact maximum-count sentence. Dictionary OCR and secondary/index evidence have limits.

Confidence is **moderate in complete wording**, stronger in contextual semantics. `Dozsiengq` and `buek` retain existing project image/assembly terminology; `buek` is not established here as a certified computing term. No native-speaker fluency certification is claimed, and none is treated as a publication gate.

## Actual behavior

`AssemblyActivity.launchAdd` displays the longer message when `assembly.images.size >= 20`, before opening the picker. This counts all imported inputs, including unplaced ones, not just visible placed images. `ImageAssembly.add` uses the shorter message to require `state.size + items.size <= MAX_IMAGES`, where `MAX_IMAGES` is 20, before modifying state. The model exception can propagate through import-batch error handling to the activity message.

An oversized picker return has a separate existing remaining-capacity message, unchanged here. The UI Remove action calls `assembly.remove`, which filters the selected ID out of the input collection. Unplace retains membership and therefore does not make a capacity slot. The translation does not instruct deleting the original device file. No picker, import, state, placement, undo or source-file logic changes.

## Verification

- All 171 offered-option catalogue checks and the importance manifest passed. Existing nodes, source attributes, arguments, numerals (including 20), literal tokens, newline escapes and XML escaping are preserved.
- `python -m unittest -v test_translations test_translation_boundaries test_string_importance test_current_localization_contracts`: **61 tests passed in 5.810 seconds** on this complete restored checkout.
- Four Java English/Zhuang XML-to-string cases passed for nonempty messages and unchanged no-argument formatting. These are not Android resource compilation.
- Temporary token-aware source checks verified both unique resource consumers, the pre-picker/pre-mutation limit guards, model-error propagation, separate oversized-picker handling and Remove versus Unplace membership behavior.
- All **1,577 base tracked blobs and executable modes** were verified locally, using the original XML bytes for the intentionally edited path. `git diff --check` passed. Publication verifies the full path/mode/type/blob overlay, expected-parent non-force lease and exact remote bytes.

Existing `AssemblyModelTest.batchMarginsUseEachOriginalSizeAndTwentyImageCapPreservesExistingItems` tests rejection of a 21st item without changing the collection. `AssemblyActivityTest.twentyImagesLoadAndAnOversizedPickerBatchIsRejectedBeforeReading` tests the separate picker-return guard. They were inspected, not run; the latter is not proof that the new pre-picker message was displayed. No permanent per-edit wording mirror or test package is added.

Zhuang presence: P0 **69/94**, P1 **158/249**, P2 **75/305**, P3 **2/71**. Global missing resources over 171 options: P0 **162**, P1 **1,333**, P2 **30,054**, P3 **7,479**; 46 options have complete presence. Scope remains 59 scoped catalogues plus 112 outside-scope catalogues with explicit English fallback. Presence is not fluency or runtime acceptance.

Android SDK/Kotlin compiler are unavailable here. Android compilation, Robolectric, actual 20/21-image interactions, TalkBack and device/font-scale layout were not executed. Exact-head Actions state is checked after publication and reported separately. No merge, release or CI-pass claim is made.
