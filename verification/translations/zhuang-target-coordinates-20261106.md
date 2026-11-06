# Zhuang assembly target coordinates, 6 November 2026

## Scope and language review

Reconciled parent `aa81d29b2372d596109281eeaa562f8c7ee763a4`, tree `2fd0a34bb04f3b1a4de3d0b314cc168bc0ae5448`, with the preceding publication complete and no pending write. Adds missing P2 `ui_assembly_target_x` and `ui_assembly_target_y`, preserving all 304 previous typed resources for a total of 306. Only canonical XML and this report change.

Independent review recommends concise labels identifying X from the left and Y from the top, with the standard `px` unit. Explicit “Target” is omitted: these are editable coordinate inputs whose values are applied as the requested placement. Adding a literal “to be used” phrase was judged unnecessary. Directional meaning is well supported; exact technical-register idiomaticity is less certain. Variables and unit abbreviations alone are not counted as linguistic review: the from/left/top content is actually translated.

The reviewer checked the actual dialog/model and existing project lexical evidence. A fresh direct check of the [Sawloih Cuengh-Gun OCR](https://dokumen.pub/sawloih-cuengh-gun-ocr.html) confirmed `daj` from (D5, L438), `baihgwnz` upper side (B15, L133), and `baihswix` left side (B16, L135). The project consistently separates the directional words, unlike those fused dictionary entries. The OCR reproduction is not a pristine edition and does not attest the complete coordinate labels as standard software terminology. No native-human certification is claimed.

## Actual consumer and remaining fallback

`AssemblyPositionDialog` in `AssemblyPlacementDialog.kt` is the only consumer. Each resource is used twice: as a complete visible TextView label and as the corresponding EditText contentDescription. X initializes from the selected image rectangle's left coordinate, Y from its top coordinate; unplaced images default to zero.

Apply parses both values as finite, nonnegative whole integers within Int range and passes them in X/Y order to `assembly.position`. The model stores `ImagePosition(x,y)` and computes the image rectangle from `(x,y)` to `(x+width,y+height)`, subject to its existing coordinate constraints. These are absolute image-pixel coordinates for the image's top-left corner, not screen-density units, relative drag amounts, crop margins or image dimensions. Dialog density scaling affects its padding, not these values.

Cancel has no position callback. Validation errors keep the dialog open and display an error message. No positioning, input parsing, error, persistence, overlap or undo logic changes. The dialog's title and explanatory help still fall back to English; these two labels do not make the entire flow fully Zhuang-understandable. TalkBack pronunciation of `px`, focus behavior and screen layout remain unverified.

## Verification

- All 171 offered-option catalogue checks and the importance manifest passed. Existing resource nodes, source attributes, arguments, source numerals, literal tokens, newline escapes and XML escaping are preserved. Target X/Y identity, left/top mapping and `px` units were separately checked.
- `python -m unittest -v test_translations test_translation_boundaries test_string_importance test_current_localization_contracts`: **61 tests passed in 5.883 seconds**.
- Four Java English/Zhuang XML-to-string cases passed for nonempty labels and unchanged no-argument formatting. This is not Android resource compilation.
- Temporary token-aware source checks passed for all four direct bindings, complete visible/accessibility resource use, initial values, whole-number parsing, X/Y model mapping, Apply and Cancel paths.
- All **1,578 base tracked blobs and executable modes** were verified before editing. `git diff --check` passed. Publication verifies the complete path/mode/type/blob overlay, expected-parent non-force lease and exact remote bytes.

Existing `AssemblyActivityTest.exactPositionMovesOnlySelectedImageAllowsOverlapAndSurvivesReopening` and `invalidPositionAndCancelDoNotChangeImagesOrTheSavedProject` were inspected for adjacent successful/invalid/cancel/reopen behavior. They were not executed and do not establish this Zhuang label pair's device or accessibility presentation. No permanent per-edit wording mirror or test package is added.

Zhuang presence: P0 **69/94**, P1 **158/249**, P2 **77/305**, P3 **2/71**. Across 171 options, missing resources are P0 **162**, P1 **1,333**, P2 **30,052**, P3 **7,479**; 46 options have complete presence. Scope remains 59 scoped catalogues plus 112 outside-scope catalogues with explicit English fallback. Presence is not fluency or runtime acceptance.

Android SDK/Kotlin compiler are unavailable here. Android compilation, Robolectric, actual positioning, TalkBack and device/font-scale layout were not executed. Exact-head Actions state is checked after publication and reported separately. No merge, release or CI-pass claim is made.
