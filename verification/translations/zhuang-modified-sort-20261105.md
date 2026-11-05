# Zhuang modification-time sorting, 5 November 2026

## Scope and wording

The live review branch was reconciled at parent `584561c1c9098282c645873e33c3010cdec39e4f`, tree `029595c9a96b2187e16ad936ec1fa5df0e004152`. No write was pending or uncertain. This fills missing P2 `ui_modified_newest_first` and `ui_modified_oldest_first`. All 278 preceding typed resources remain unchanged; the total is 280. Only canonical XML and this report change.

Independent wording and consumer review recommended explicit modification-time headings and explicit superlatives, backtranslated as “Modification time: newest first” and “Modification time: oldest first”. The final wording uses `seizgan` for time rather than the broader `seiz`, and adds `ceiq` to make the superlative explicit. It does not substitute image creation time, file naming, import order or the application's edit history.

Language evidence:

- [1984 Sawloih Cuengh-Gun dictionary OCR](https://dokumen.pub/sawloih-cuengh-gun-ocr.html), directly retrieved by the independent reviewer: G15 supports `gaij` for modifying; G14 and M42 support `gaeuq` and `moq` for old/new; G67 supports `gonq` for first/before; S21–22 distinguish broader `seiz` and time noun `seizgan`; C32 supports superlative `ceiq`, including its position before an adjective. These are component meanings, not an attested file-sorting phrase.
- [Guangxi Minzu Bao, linguistic comparison, 23 May 2018](https://www.guangximinzubao.cn/szbzw/html/2018-05/23/content_25838.htm), retrieved by both checks, describes head-before-modifier constructions and gives `byaij gonq` as going first. This supports the ordering choice, not the complete label.
- [Guangxi language commission's seventh terminology notice, published 12 July 2023](https://www.guangximinzubao.cn/sy/jxzw/389425.html), directly retrieved, supplies new/old contrasts and first/later ordering in entries 89, 99 and 131. Its subject is public terminology, not software sorting; no official technical-term status is transferred to this translation.

Confidence is **moderate for the complete composed labels**, with strong support for the individual meanings. Naturalness of the abbreviated UI phrases remains uncertain. Native-human certification is not claimed or treated as a prerequisite. Canonical Android XML owns current wording; this report is not a parallel approval catalogue.

## Actual consumer

`AssemblySort` maps OLDEST and NEWEST to these resources; its `label` getter returns the complete localized value. `AssemblyActivity` places all enum labels into the sort spinner. Selecting a row updates the sort choice and rebuilds the thumbnail tray with `assembly.sorted(sort)`. The spinner also has a separate existing accessibility description; that unrelated resource is unchanged.

`ImageAssembly.sorted` orders known modification timestamps ascending for OLDEST and descending for NEWEST. Unknown timestamps remain last in either direction; equal timestamps and pairs of unknown times use filename ordering, then ID. Sorting returns a view of the list and does not change image placement, document content or stored timestamps.

The metadata reader obtains `DocumentsContract.Document.COLUMN_LAST_MODIFIED`, with a `date_modified` fallback when the first column is absent/null. Positive valid fallback seconds are converted to milliseconds with an overflow bound. Missing or unusable metadata stays unknown; the method does not invent an import-time value. This is provider-supplied modification metadata, not a guarantee of its accuracy or a new modification-tracking feature. No sorting, import or metadata implementation changes.

## Verification

- All 171 offered-option catalogue checks and the importance manifest passed. Existing nodes, source attributes, ordered arguments, numerals, literal tokens, newline escapes and XML escaping are preserved.
- `python -m unittest -v test_translations test_translation_boundaries test_string_importance test_current_localization_contracts`: **61 tests passed in 14.044 seconds**.
- Four host Java XML-to-string cases check the two English/Zhuang labels are nonempty and unchanged by no-argument formatting. These do not compile Android resources.
- Temporary token-aware Kotlin checks verify complete-resource enum/spinner bindings, selection-to-tray routing, timestamp source, ascending/descending directions, unknown-last/tie handling, and absence of writes or placement changes in sorting. These are static checks, not comparator or Android execution.
- Base snapshot verification matched Git blobs and executable modes for **1,292 materialized files**, retaining **269** unmaterialized entries. Publication verifies the complete path/mode/type/blob overlay, expected-parent non-force lease and exact remote bytes.

Inspected but not run: `AssemblyModelTest.sortByNameOrRealModificationTimeDoesNotChangePlacementAndUnknownTimesStayLast` covers both timestamp orders, unknown-last and placement preservation. `AssemblyActivityTest.multiPickerLoadsNamesTimesAndThumbnailsThenNativeDragEventsSnapBothDirections` selects OLDEST and checks the first thumbnail. Inspection is not execution evidence, and neither establishes the visible fit of these Zhuang labels. No permanent per-edit wording mirrors or test packages are added.

Zhuang presence is P0 **69/94**, P1 **154/249**, P2 **57/305**, P3 **0/71**. Across 171 options, missing resources are P0 **162**, P1 **1,337**, P2 **30,072**, P3 **7,481**; 46 options have complete presence. Scope remains 59 scoped catalogues and 112 outside-scope catalogues with explicit English fallback. Presence is not fluency or runtime acceptance.

Android SDK/Kotlin compiler are unavailable here. Android compilation, Robolectric, provider metadata, runtime ordering, TalkBack and spinner layout were not executed. Exact-head Actions state is checked after publication and reported separately. No merge, release or CI-pass claim is made.
