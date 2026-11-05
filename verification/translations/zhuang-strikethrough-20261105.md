# Zhuang text strikethrough label, 5 November 2026

## Scope and reviewed source

This bounded addition uses parent `dd96edeaa41204c04e60dce231befa3a1a5d4ab6` on `review/nv-bottom-2038-20261103`. The live ref and complete, untruncated tree were reconciled before editing. The missing P2 scalar `ui_strikethrough` now supplies a descriptive Zhuang label in the canonical `Paintroid/src/main/res/values-b+za/strings.xml`. The source English label is “Strikethrough”. All 248 preceding typed resources remain unchanged; there are now 249. No application code, fallback policy, language scope, or other catalogue changes are included.

## Wording evidence and independent review

[The digitized Zhuang–Chinese dictionary](https://dokumen.pub/sawloih-cuengh-gun-ocr.html), main sections S29, G80 and C39, supports the joined compound `sienqdiuz` for a line, spatial `gvaq` for passing/crossing, and `cih` for word/character-related usage. G80 illustrates crossing a river; the spatial sense is not inferred from the separate dialect-marked past-experience usage. The existing underline label uses the same joined line compound with a below-text relation.

[Guangxi Minzu Bao, 14 April 2021, page 7](https://www.guangximinzubao.cn/szbzw/page/21/2021-04/14/07/2021041407_pdf.pdf), the pronunciation discussion at extracted lines 320–322, independently pairs `gvaq` with crossing and a river example. The article also discusses postposed modifiers. This supports the ingredients and general construction, not an established typography term.

An independent linguistic/context review accepted the noun-plus-crossing description with moderate confidence and found no concrete lexical or semantic blocker. It describes the line rendered across the characters without implying that text content is deleted. The complete expression is a compositional UI translation, not a dictionary-attested translation of “strikethrough”. Conventional software idiom and native-user comprehension remain unverified. Canonical XML owns the wording; this report does not create a parallel approval catalogue.

## Actual consumers and behavior

- `TextStyleDialog.kt:48–53`: the only direct resource binding gives the complete selected label to the `text_strike` CheckBox. The helper assigns ordinary checkbox text and initial checked state. The paired row has equal-width cells and 48 dp height; actual wrapping and fit require device inspection. No separate explicit content description is added by this binding.
- `TextStyleDialog.kt:75,93`: checked-state changes update `preview.strike`; preview rendering sets `Paint.isStrikeThruText` and passes the original preview value to `VerticalText.draw`.
- The positive action constructs `TextSettings` with unchanged input text and the strike boolean, committing only through the existing callback; Cancel has no commit listener. JSON writes/reads the strike boolean.
- `ClassicPaintActivity.kt:1065–1071` forwards both text and strike state to `PaintDocument.text`. That method retains the blank-text guard and undo checkpoint, sets the paint strike flag, and draws the supplied text. This option is styling, not removal of content.

These are source-level binding/control-flow observations. They are not executed Android interaction or accessibility evidence.

## Targeted checks executed

- All 171 offered-option catalogue checks and importance-manifest validation passed. The new entry retains the source attributes, placeholder/format contract, literal tokens and escaping. Existing resources were checked for unchanged node content and attributes.
- `python -m unittest -v test_translations test_translation_boundaries test_string_importance test_current_localization_contracts`: **61 tests passed in 8.327 seconds**.
- Host Java parsed English and integrated Zhuang XML and formatted the label without arguments: **2 literal-label cases passed**. This is host Java/XML behavior, not Android resource compilation.
- Temporary token-aware consumer checks passed for the complete checkbox binding, initial state, preview-change listener, preview and final strike flag, input-text forwarding, JSON persistence, cancel listener, blank guard and undo checkpoint. An initial temporary check selected an incomplete Kotlin function signature; it was corrected to the full opening signature and rerun successfully. No application change was needed.
- Every materialized base file's Git blob identity and executable mode was checked: **1,271 files**. Another **269** non-tree entries remain retained by the verified base tree. Publication verifies the complete resulting path/mode/type/blob map, with only this XML and report overlaid, using a fresh expected-parent non-force lease and final readback.

The existing `WorkspaceRefinementTest.fontPreviewFormattingAndTextPlacementWorkWithUndo` was inspected: it toggles the style checkboxes, checks preview strike state, places text and exercises undo. It was **not run** here. No permanent per-edit test mirror was added.

## Coverage and limits

Zhuang resource presence is P0 **69/94**, P1 **133/249**, P2 **47/305**, P3 **0/71**. Across 171 offered options, missing typed resources are P0 **162**, P1 **1,358**, P2 **30,082**, P3 **7,481**; 46 options have complete resource presence. The bounded scope remains 59 scoped catalogues plus 112 outside-scope catalogues with explicit English fallback. Presence does not establish fluency or runtime acceptance.

Android SDK/Gradle compilation, Robolectric execution, device layout, glyph rendering, TalkBack and rendered strikethrough behavior were not executed. The workflow does not ordinarily run for this review-branch push; the exact-head Actions state is checked after publication and reported separately. No release, merge, complete-language or CI-pass claim is made.
