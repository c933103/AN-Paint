# Zhuang image-assembly entry and headers, 5 November 2026

## Scope and review

The live branch was reconciled at parent `97f57bbef235d033027e2cfebe1a66592167dd17`, tree `1e842e5ade6f5131cd6ec5f61d3681f501a7a91b`. Its preceding publication was confirmed, with no pending or uncertain write. This adds missing P2 `ui_image_assembly`, `ui_an_paint_image_assembly` and `ui_an_paint_image_assembly_20_images_placed`. All 295 previous typed resources remain unchanged; the new total is 298. Only canonical XML and this report change.

Independent review recommends the menu/title wording and label-first count line. Confidence is high for the count semantics and **moderate for linguistic naturalness**. The [Sawloih Cuengh-Gun OCR](https://dokumen.pub/sawloih-cuengh-gun-ocr.html), independently retrieved by the reviewer, supports `baij` placing/arranging and `gaenq` already. It lists `buek` as a goods-batch classifier, not a computing assembly term. The full image-assembly compound is an established project convention, not dictionary-certified terminology. The OCR mirror may contain transcription errors; failure to find a word there is not evidence of invalidity.

The live header labels the total images and placed images separately rather than introducing an unverified numeral classifier. Brand spelling, denominator 20, ordered `%1$s`/`%2$s`, and the exact existing newline escape are preserved. No standardized-term or native-human certification claim is made.

## Consumers and layout limit

`ClassicPaintActivity` uses the menu resource to open the assembly activity. `AssemblyActivity.buildInterface` initially uses the title resource, then calls `refresh`, which replaces it with the live count header. The first argument is `assembly.images.size`, including unplaced inputs. The second is `assembly.layout().size`, counting placed entries. Unplace retains an input while removing its placement; Remove also reduces the input count. Thus the two figures are not interchangeable.

The header retains its existing 15sp text, maximum two lines, fixed 44dp compact/54dp regular height, and neighboring undo/redo buttons. The explicit newline uses the second line, and the longer translated count line may wrap or lose its trailing placed count on narrow screens or enlarged fonts. **Device layout and complete visible fit are not verified.** No layout, menu, placement, counting or state logic changes. Clipboard labels, filename fallback and workspace instructions are outside this batch.

## Verification

Work and tests used the available temporary filesystem; no unrelated files were removed from the full main workspace.

- All 171 offered-option catalogue checks and the importance manifest passed. Existing nodes, source attributes, ordered typed arguments, numerals, literal tokens, newline escapes and XML escaping are preserved.
- `python -m unittest -v test_translations test_translation_boundaries test_string_importance test_current_localization_contracts`: **61 tests passed in 24.331 seconds**.
- Twelve Java XML-format cases checked the two static labels and live-header empty, partially placed, full-capacity and localized count arguments in English/Zhuang. Counts remain in their respective fields with denominator 20. These are not Android resource compilation or header measurement.
- Temporary token-aware Kotlin checks verified all three exact resource bindings, menu navigation, initial/live header assignments, total-input versus placed-layout arguments, Unplace/Remove distinction and existing height/two-line constraints.
- Base snapshot verification matched Git blobs and executable modes for **1,286 materialized files**, retaining **288** unmaterialized entries. Publication verifies the complete path/mode/type/blob overlay, expected-parent non-force lease and exact remote bytes.

Inspected but not run: `AssemblyActivityTest.frenchHeaderTracksAddPlaceUnplaceAndRemoveIncludingOne` exercises live counts through empty, added, placed, unplaced and removed states. It is an existing French consumer test, not evidence of Zhuang wording, glyphs or layout. No permanent per-edit wording mirror or test package is added.

Zhuang presence is P0 **69/94**, P1 **158/249**, P2 **69/305**, P3 **2/71**. Across 171 options, missing resources are P0 **162**, P1 **1,333**, P2 **30,060**, P3 **7,479**; 46 options have complete presence. Scope remains 59 scoped catalogues and 112 outside-scope catalogues with explicit English fallback. Presence is not fluency or runtime acceptance.

Android SDK/Kotlin compiler are unavailable here. Android compilation, Robolectric, actual menu/navigation/count changes, TalkBack and device layout were not executed. Exact-head Actions state is checked after publication and reported separately. No merge, release or CI-pass claim is made.
