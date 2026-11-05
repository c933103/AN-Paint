# Zhuang standard-palette gesture description, 5 November 2026

## Scope and wording review

The live review branch was reconciled at parent `d25db8f3a1b213a186776b298ce401df77915422`, tree `8f14c1f013f4b0f0f2c03eb531d9fc0d70c69dbf`; no prior operation was pending. This addition fills the missing P1 `ui_colour_tap_foreground_hold_background` accessibility description for standard palette swatches. Its source is “Colour #%1$s. Tap foreground, hold background.” All 256 preceding typed resources remain unchanged; the total is 257. Source attributes, the single `%1$s` argument and the preceding hash are retained. Only canonical XML and this report change.

Independent linguistic/context review accepted the concise contrast between tap and continued pressing with **moderate confidence**. It retains the existing colour, tap and foreground/background vocabulary. The [Zhuang–Chinese dictionary OCR](https://dokumen.pub/sawloih-cuengh-gun-ocr.html), main G section, page 7, supports `gaemh` as press, distinct from `gaem` for grasp/hold. B15 supports the paired front/back role names. The chosen continued-press construction is a contextual translation, not an established touchscreen term.

The exact `gaemh youq` construction occurs in [Guangxi Minzu Bao, 30 April 2025, page 6](https://www.guangximinzubao.cn/szbzw/page/21/2025-04/30/06/2025043006_pdf.pdf), extracted lines 187–190. **Its meaning there is figurative persistence/holding out** by a vendor against an official, not literal finger pressure. It supports the persistence reading only. Combining that construction with the dictionary press sense and explicit tap contrast makes the intended hold action reasonably recoverable, but neither source proves unambiguous native touchscreen usage. Review found no blocking semantic defect; the residual ambiguity is recorded rather than hidden. No force requirement or number of seconds is invented.

Canonical XML owns the complete wording. No native-user, established-terminology or complete-language acceptance is claimed.

## Actual consumer

`ClassicPaintActivity.makePalette` creates 28 standard colour swatches. Each focusable swatch receives the full selected description with its six-character uppercase RGB value, without a hash in the argument. The source string supplies that hash once.

A normal click calls `setColour(colour,false)`; a long click calls `setColour(colour,true)` and consumes the event. Both are gated while the editor is busy. `setColour` updates foreground or background accordingly, refreshes recent colours and the status indicator, invalidates the canvas and schedules autosave. The label names these roles, not physical swatch position.

The surrounding palette-scroll instruction, recent-colour descriptions and FG/BG drawing labels are separate resources and remain unchanged. This is not complete palette localization. The check does not perform a click or change a user's drawing.

## Executed verification

- All 171 offered-option catalogue checks and the importance manifest passed. Existing-node identity, source attributes, ordered arguments, literal tokens and escaping were checked.
- `python -m unittest -v test_translations test_translation_boundaries test_string_importance test_current_localization_contracts`: **61 tests passed in 13.732 seconds**.
- Host Java parsed English and integrated Zhuang XML and ran **62 cases**: 56 compositions using all 28 actual source-array RGB values, four opaque-string payload cases and two missing-argument failures. The full value and single hash prefix survive formatting; argument text is not reinterpreted. These are host XML/Java checks, not Android formatting execution.
- Temporary token-aware source checks passed for the full focusable-swatch binding, tap/long-click role mapping, busy gate, consumed long click, matching document fields and subsequent indicator/autosave updates.
- Base snapshot checks verified Git blob identity and executable mode for **1,276 materialized files**. **269** unmaterialized non-tree entries remain retained. Publication verifies the full resulting path/mode/type/blob overlay, a fresh expected-parent non-force lease and exact remote bytes.

Existing `ClassicWorkspaceTest.paletteForegroundBackgroundAndImageTransformMenusWork` and `restartingPreservesForegroundAndBackgroundIncludingAnExplicitWhiteForeground` were inspected, not run. No permanent per-edit wording test or mirror is added.

## Coverage and limits

Zhuang presence is P0 **69/94**, P1 **138/249**, P2 **50/305**, P3 **0/71**. Global missing typed resources across 171 options are P0 **162**, P1 **1,353**, P2 **30,079**, P3 **7,481**; 46 options have complete resource presence. Scope remains 59 scoped catalogues plus 112 outside-scope catalogues with explicit English fallback. Presence does not establish fluency or runtime acceptance.

Android compilation, Robolectric, actual long-press/accessibility-action behavior, TalkBack comprehension and device layout were not executed. Exact-head Actions state is checked after publication and reported separately; review-branch pushes do not normally trigger CI. No merge, release, complete-language or CI-pass claim is made.
