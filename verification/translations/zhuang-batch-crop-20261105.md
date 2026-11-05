# Zhuang batch-crop entry points, 5 November 2026

## Scope and wording

The live review branch was reconciled at parent `5e4254def82e5d536cae5fecd70423e9a53c421f`, tree `5522c9792da77e1a6f24df20b742f669e9c7d37d`. No write was pending or uncertain. This fills missing P2 `ui_batch_crop` and `ui_batch_crop_images`. All 280 preceding typed resources remain unchanged; the total is 282. Only canonical XML and this report change.

Independent wording and consumer review recommended the same plain-language “crop multiple images” paraphrase for the action and multi-image dialog title. It retains the existing crop/image vocabulary and uses `lai` for multiplicity. It names a capability, not a mandatory minimum selection count or a promise to crop every available image. An “all images” rendering would be wrong because checkboxes permit a subset.

Evidence and remaining uncertainty:

- [Sawloih Cuengh-Gun OCR](https://dokumen.pub/sawloih-cuengh-gun-ocr.html): the independent reviewer directly retrieved `lai` meaning many/much in appended Sawndip L p.3. Earlier crop vocabulary review established `daet` for cutting and `henz` for edge (D23/H24). Keeping the canonical crop phrase is a consistency choice, not new independent proof of the complete label.
- [People's Daily Zhuang text](https://sawcuengh.people.com.cn/158003/15813459.html): the search excerpt retrieved `lai mbaw cingq` and `lai yiengh` constructions, supporting a preceding quantity expression. Full-page retrieval returned 502. These are excerpt-level evidence and do not attest the exact digital-image phrase.
- The reviewer also retrieved `caez` and `doengzcaez` meaning together/jointly, but found no suitable example establishing batch processing of objects rather than people acting together. They were not used. A page/sheet classifier was not inserted because its suitability for digital images was not independently established in this batch.

Confidence is **moderate for intended meaning, low-to-moderate for exact idiomatic wording**. The naturalness of classifier-free `lai dozsiengq` is specifically unresolved; no exact native UI example was located. This is a transparent compositional paraphrase, not a verified technical term for batch processing or a native-human certification. That uncertainty is recorded rather than converted into a human-approval gate. Canonical XML owns current wording.

## Actual consumers

`AssemblyActivity` binds the complete action resource to the batch-crop button and calls `crop(true)`. The method passes all currently available assembly images to `ImageCropDialog`; an empty assembly produces the existing add-images message. The entry point also works with a single available image. `ImageCropDialog` uses its named single-image title when the input list has one item and the batch title only when it has more than one.

For multiple images, checkboxes choose the target IDs. Confirmation requires at least one selected ID, computes the requested margins against each selected image's original dimensions, then calls the apply callback with one map of rectangles. The model changes only images represented in that map and validates the proposed state before writing it or recording undo. Shared percentage margins can therefore yield different pixel margins for differently sized images.

Preview gestures and fields update local dialog values. Cancel has no apply callback. This label does not imply immediate modification on opening the dialog, mandatory selection of every image, parallel execution, or destructive rewriting of source image files. No cropping, preview, selection, metadata or history implementation changes.

## Verification

- All 171 offered-option catalogue checks and the importance manifest passed. Existing nodes, source attributes, ordered arguments, numerals, literal tokens, newline escapes and XML escaping are preserved.
- `python -m unittest -v test_translations test_translation_boundaries test_string_importance test_current_localization_contracts`: **61 tests passed in 13.746 seconds**.
- Four host Java XML-to-string cases check the two English/Zhuang labels are nonempty and unchanged by no-argument formatting. These do not compile Android resources.
- Temporary token-aware Kotlin checks verify action and title bindings, the single/empty-image paths, checkbox subset selection, nonempty confirmation, per-image rectangle calculation, one map application, preview-local updates, no cancel callback, and model validation before write. These are static checks, not Android behavior execution.
- Base snapshot verification matched Git blobs and executable modes for **1,293 materialized files**, retaining **269** unmaterialized entries. Publication verifies the complete path/mode/type/blob overlay, expected-parent non-force lease and exact remote bytes.

Inspected but not run: `AssemblyActivityTest.individualAndBatchCropUsePercentAndAreUndoableBeforePlacement` checks percentage crops for three images and undo/redo. `frenchActualBatchCropShowsCompleteWarningForZeroOneAndTwoSelectedImages` checks the real dialog's zero/one/two selection count display, but does not apply those subsets. `AssemblyModelTest.batchMarginsUseEachOriginalSizeAndTwentyImageCapPreservesExistingItems` checks size-relative margins; the existing crop/reflow test checks invalid-arrangement rejection. None of these inspections is runtime evidence for this patch. No permanent per-edit wording mirrors or test packages are added.

Zhuang presence is P0 **69/94**, P1 **154/249**, P2 **59/305**, P3 **0/71**. Across 171 options, missing resources are P0 **162**, P1 **1,337**, P2 **30,070**, P3 **7,481**; 46 options have complete presence. Scope remains 59 scoped catalogues and 112 outside-scope catalogues with explicit English fallback. Presence is not fluency or runtime acceptance.

Android SDK/Kotlin compiler are unavailable here. Android compilation, Robolectric, actual crop/subset/cancel/undo behavior, TalkBack and action/title layout were not executed. Exact-head Actions state is checked after publication and reported separately. No merge, release or CI-pass claim is made.
