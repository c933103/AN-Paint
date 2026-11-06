# Zhuang snapped-assembly origin message, 6 November 2026

Parent `24bb013a8ea515f9f1b5da2aaf1efd916f51f3de`, tree `6095b8f9f1aed339f868bb08635aea141024b9d5`, was reconciled with no pending write. Adds missing P2 `ui_the_first_image_starts_at_the_top_left`, preserving all 308 previous typed resources for 309 total. Only canonical XML and this report change.

Concurrent PR [#295](https://github.com/c933103/AN-Paint/pull/295) was checked at `6d4a07c73b345c17a1d33841427ba0e56f1c2d87` on its separate priority48 branch. Its three Zhuang diagnostic values already match this branch and are untouched. This batch does not update that PR, its branch, other catalogues or its review/CI state.

## Wording and precise scope

Independent review accepts the spatial paraphrase saying the first image is at the upper-left corner. “Is at” preserves the relevant placement meaning of “starts at” without introducing a temporal process. Existing project image, ordinal and directional terminology is retained.

The directly checked [combined dictionary/OCR page](https://dokumen.pub/sawloih-cuengh-gun-ocr.html) supports `gok` corner/place and the locative example `Youq gok lawz?` in its appended vocabulary section (L2692). Its main vocabulary also has corner compounds such as `gokciengz` wall corner (L863), with upper/left directional entries at L133–135. Independent review checked these constituent meanings and locative syntax. The complete upper-left phrase is compositional, not independently attested as software wording. Confidence is **moderate**, not native-certified idiomaticity; OCR/source-section limitations remain.

The only direct resource consumer is `ImageAssembly.validate`, which permits at most one image with a non-null attachment whose anchor is null. That is the snapped assembly's root. A valid root has no explicit ImagePosition and its layout defaults to `(0,0)`. Model validation occurs before state/file changes; errors may reach the activity error dialog or the saved-assembly loading error.

This is **not** a rule that every first imported image or every absolute-position image must occupy `(0,0)`. Absolute positions are independent, can be nonzero, and are not counted as root attachments. The English source is itself a short diagnostic rather than a full explanation of the one-root invariant. No placement, snapping, loading, validation, persistence or undo logic changes.

## Verification

- All 171 offered-option catalogue checks and the importance manifest passed. Existing nodes, source attributes, formatting, numerals, literal tokens, newline escapes and XML escaping are preserved.
- `python -m unittest -v test_translations test_translation_boundaries test_string_importance test_current_localization_contracts`: **61 tests passed in 6.224 seconds**.
- Two English/Zhuang Java XML-to-string cases passed for nonempty text and unchanged no-argument formatting. This is not Android resource compilation.
- Temporary token-aware source checks passed for the unique binding, root-count constraint, zero-origin defaults, separate explicit positioning, validation before writing, and activity error presentation.
- All **1,581 base tracked blobs and executable modes** were verified before editing; `git diff --check` passed. Publication checks the full path/mode/type/blob overlay, expected-parent non-force lease and exact remote bytes.

Existing model tests for attachment alignment and changing a snap root to exact coordinates were inspected, not run. They cover adjacent placement behavior, not a newly executed two-root rejection or Zhuang dialog-layout check. No permanent per-edit wording mirror or test package is added.

Zhuang presence: P0 **69/94**, P1 **158/249**, P2 **80/305**, P3 **2/71**. Global missing counts over 171 options: **162 / 1,333 / 30,049 / 7,479** for P0–P3; 46 options have complete presence. Scope stays 59 scoped catalogues and 112 outside-scope catalogues with explicit English fallback. Presence is not fluency or runtime acceptance.

Android SDK/Kotlin compiler are unavailable here. Android compilation, Robolectric, actual root validation, loading/placement, TalkBack and device/font-scale layout were not executed. Exact-head Actions state is checked after publication and reported separately. No merge, release or CI-pass claim is made.
