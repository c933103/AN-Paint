# Zhuang foreground/background colour roles, 5 November 2026

## Scope and wording

The live review branch was reconciled at parent `8db1166de259e16090b5804436d6156bb0476a4d`, tree `15f9843dfa6ee4d40e9e66b456c91a09643e3c4f`. No prior operation was pending. Four missing P1 strings are added to canonical `Paintroid/src/main/res/values-b+za/strings.xml`: the foreground/background colour names and their value-plus-edit accessibility descriptions. All 251 existing typed resources are unchanged; the total is 255. Source attributes and each `%1$s` argument are preserved. Only the XML and this report are published.

Independent linguistic/context review accepted all four as paired descriptive colour-role labels, with **moderate confidence**, not standardized computing terminology. The [Zhuang–Chinese dictionary OCR](https://dokumen.pub/sawloih-cuengh-gun-ocr.html), main B section, page 15, supports `baihnaj` through front/in-front senses and an additional foreground/prospect gloss; `baihlaeng` has rear/behind and backstage senses. These justify a front/back opposition but do not prove an established software background-colour term. Existing colour and Edit colour vocabulary is retained. No semantic reversal or material misdirection was found in this two-role interface.

These names describe colour roles, not upper/lower or left/right positions: the actual controls change orientation. Native-user comprehension and conventional software idiom remain unverified. Canonical XML, not a separate wording mirror, owns the complete translations.

## Actual consumer bindings

- `ColourStatusButton.kt:16–36` keeps distinct clickable/focusable foreground/background targets and edit callbacks. Each complete accessibility sentence receives the matching colour's uppercase six-digit RGB hex value. The container description combines the two full role names. The RGB formatter masks alpha before formatting.
- `ClassicPaintActivity.kt:418` routes the targets to `colourDialog(false)` and `colourDialog(true)`. Dialog initialization, preview updates and accepted values use the corresponding document field. Refresh sends both fields back to the indicator.
- `AdvancedColourDialog.kt:314` selects the same foreground/background titles outside the separate add/edit-palette flow. Invalid fields prevent acceptance; cancel/dismiss restores the original preview when not accepted.
- `ClassicPaintActivity.kt:1007–1009` also uses the background name in the custom-palette menu; that action assigns the stored swatch to the background role.
- The drawn FG/BG abbreviations are separate resources and remain unchanged, as do other palette instructions. This is not complete colour-interface localization.

These are source-level findings. No Android focus, TalkBack, dialog layout or colour-rendering claim follows from them.

## Verification executed

- All 171 offered-option catalogue checks and importance-manifest validation passed. Old-resource identity, source attributes, ordered format arguments, literal tokens and escaping passed.
- `python -m unittest -v test_translations test_translation_boundaries test_string_importance test_current_localization_contracts`: **61 tests passed in 8.140 seconds**.
- Host Java XML/format checks: **32 cases passed** across English and integrated Zhuang. These comprise four literal-title cases, 24 `%1$s` payload cases (four RGB samples plus opaque percent/Unicode-markup-like text), and four missing-argument failures. Argument content remains data, not a second format string. This does not execute Android resource resolution.
- Temporary token-aware checks passed for every direct binding, matching role callbacks/arguments, RGB formatter, orientation-independent identity, dialog title and palette assignment, preview/commit paths and cancel restoration.
- Base snapshot verification checked Git blob identity and executable mode for **1,274 materialized files**. **269** unmaterialized non-tree entries remain retained. Publication compares the complete final path/mode/type/blob overlay, uses a fresh expected-parent non-force lease and verifies remote bytes after the update.

Existing `ANPaintControlsTest.pinnedColourAreasOpenPickersAndOnlyArrowTogglesPalette` and `WorkspaceRefinementTest.colourArrowStartsExpandedStaysPinnedAndRemembersCollapse` were inspected, not run. They exercise separate colour editing, swap/reset and indicator updates. No permanent per-edit wording tests or mirrors were added.

## Coverage and limits

Zhuang presence is P0 **69/94**, P1 **137/249**, P2 **49/305**, P3 **0/71**. Across 171 offered options, missing typed resources are P0 **162**, P1 **1,354**, P2 **30,080**, P3 **7,481**; 46 options have complete resource presence. Scope remains 59 scoped catalogues and 112 outside-scope catalogues with explicit English fallback. Presence does not establish fluency or runtime acceptance.

Android compilation, Robolectric, device glyph/layout checks, TalkBack and interactive preview/cancel/commit behavior were not executed. Exact-head Actions state is checked after publication and reported separately; this review-branch push does not ordinarily trigger CI. No merge, release, complete-language or CI-pass claim is made.
