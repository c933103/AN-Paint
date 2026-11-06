# Zhuang oversized-credit data-safety warning, 6 November 2026

Parent `30fe52e4a84c70762fa77511af565ba004af842b`, tree `83dbaeae65dabd70017ebf5086930ae71b139373`, was reconciled with no pending write. Adds missing P0 `gallery_credit_too_large`, preserving all 310 previous typed resources for 311 total. Canonical XML, this report and the requested completion/review/release plan change. No release action is performed.

Develop `412aab0c604060fb66fbd2edc6bb05572d10b56d` includes merged PR #295. Its three Zhuang diagnostic additions already match this branch; the existing differing height labels are untouched. No develop merge/rebase, other locale or active engineering branch is changed.

## Language and operation

Independent review corrected the first draft to say **drawing data** becomes too large, avoiding a physical canvas-enlargement interpretation, and to repeat **previous** and **still present** for both the drawing and credits. The condition describes what would happen if the rejected credit data were applied. It does not say the current drawing is damaged, that new edits were saved, or that external storage or a successful recovery has been verified.

The quoted `Image credits` identifies the current English-fallback panel heading, as in adjacent Zhuang diagnostics. Its heading is not silently counted as translated. The data, restoration and still-present terminology follows the current catalogue.

Independent review directly retrieved [Sawloih Cuengh-Gun OCR](https://dokumen.pub/sawloih-cuengh-gun-ocr.html): L504 supports `dangh` if, L520 `dem` add, and L730 `gaxgonq` previous. The first checker also retrieved the conditional entry and appended example at L2615. This is constituent evidence; the full UI sentence is composed. The inherited technical terms' entire evidence chain was not independently re-certified by this one review. Confidence is **moderate** on full wording, with no native software-usability certification claimed.

Three real bindings were checked:

- `GalleryCredits.buildEditor.save` checks inline size and invokes the edit callback before updating its entries. An IllegalArgumentException shows this warning and returns false, preserving the rejected field text and old accepted entries.
- `ClassicPaintActivity` handles returned credit edits via `PaintDocument.editImageCredits`. Metadata/history checks precede mutations to committed/floating credits, clipboard credits and undo/redo history.
- Legacy credit attachment validates projected metadata/history before committing the additional credit. The editor callback also validates document state before changing the session and adopting edits.

These paths support retention of the previous drawing/credits, rather than a claim that the rejected new edit was saved. No validation, persistence, drawing or credit logic changes.

## Verification and limits

- All 171 offered-option catalogue checks and priority-manifest validation passed. Existing nodes, source attributes, formatting, numerals, protocol literals, newline escapes and XML escaping are preserved.
- `python -m unittest -v test_translations test_translation_boundaries test_string_importance test_current_localization_contracts`: **61 tests passed in 5.969 seconds**.
- Two English/Zhuang Java XML-to-string cases passed for nonempty text and unchanged no-argument formatting. This is not Android compilation.
- Temporary token-aware source checks passed for all three bindings, validation-before-mutation ordering and the quoted heading's current fallback value. They are static checks, not runtime rejection or persistence tests.
- All **1,583 base tracked blobs and executable modes** were verified before editing; `git diff --check` passed. Publication verifies the complete path/mode/type/blob overlay, expected-parent non-force lease and exact remote bytes.

Existing `GalleryCreditBoundsTest` oversized-field recreation coverage and `LegacyImageCreditsUpgradeTest.oversizedExplicitSelectionIsRejectedBeforeMutatingDocumentOrItsValidAutosave` were inspected, not executed. No permanent per-edit wording mirror or test package is added. Warning toast/dialog layout, glyphs, font scaling, TalkBack, Android compilation and Robolectric were not run locally because the Android SDK/Kotlin compiler is unavailable. Longer explicit wording may affect presentation; no layout pass is claimed.

Zhuang presence is now **P0 70/94, P1 158/249, P2 80/305, P3 3/71**. Global direct gaps over 171 options are **161 / 1,333 / 30,049 / 7,478** for P0–P3. These are presence counts, not complete translation review. The [release plan](p0-p1-release-plan-20261106.md) separately records the all-translated-string review requirement and release gates. Exact-head Actions state is checked after publication and reported separately; no CI-pass, completed-review or release claim is made.
