# Zhuang Save versus Export safety and existing-string review

6 November 2026. Parent `e278bd710b2d1020bb66233fc1709fe2873408f1`, tree `12b0e3ba292fad205f3228f667f91b6177848fb9`, was reconciled with no pending write. Adds two missing P0 resources, `ui_export_did_not_save23` and `ui_export_explanation23`, preserving all 311 preceding typed resources for 313 total. Only canonical XML and this report change. Develop remains `412aab0c604060fb66fbd2edc6bb05572d10b56d`; no other locale, branch or active engineering work is changed.

## New wording and exact behavior

Independent review accepts both additions at **moderate compositional confidence**. The export-success warning reports that a file was saved, then directs the user to the current Save or Save as controls before proceeding. The first draft's “new” was removed because the output stream uses `wt` and can replace an existing destination file. The continuation is an instruction to the user, not a promise that a previously deferred action resumes automatically.

The options explanation distinguishes ICO, Base64 text and ASCII-art output. It explicitly preserves the current image and the location used by ordinary Save. Naming ICO is a concrete reference to the actual icon output format. The Save-destination clause is an authored technical paraphrase, not an independently attested full UI sentence. The quoted commands exactly match the current labels; this does not resolve their separate lexical evidence limitation below.

Actual consumers:

- `ClassicPaintActivity.writeImage` writes and closes the selected output before showing file success. Only the non-export branch changes filename, savedTarget and document.markSaved. It clears afterSave and, for an export with a pending action, shows the new warning instead of invoking that action.
- `SaveOptionsDialog` supplies the explanation to both ordinary and vertical form construction. The export list consists of ICO, Base64 and ASCII art; sharing follows its separate explanation. The complete selected resource is assigned, with scrolling form containers. No actual text layout was measured.
- `confirmReplacement` checks dirty state. Save stores the deferred action and requests an ordinary save; Discard invokes the replacement action; Keep editing dismisses without executing it. The dialog applies pending editor geometry before checking dirty state.

No Save/Export state logic, formats, output encoding, overwrite behavior, pending-action handling or UI layout changes. `formats22_derived_exported` has no current production binding found and is not added or counted in this batch.

## Bounded review of nine existing resources

This is a fresh scoped review against the current canonical values and consumers, not restoration of withdrawn catalogue acceptance. None of these nine values changes:

- `ui_saved`: accepted at bounded moderate confidence. The filename argument scopes success to the written file, including an export; it does not assert the working drawing is marked saved.
- `ui_discard_changes23`: accepted at moderate confidence. The verb explicitly discards changes, not the original source file.
- `ui_keep_editing23`: accepted at moderate confidence. Modern linguistic commentary supports the continuation word used with editing.
- `ui_could_not_save_image`: accepted at moderate confidence. File-output failure is a safe contextual paraphrase for the write error, without a recovery promise or unsupported diagnosis.
- `ui_save` and `ui_save_a5d0d9`: action/alias correspondence checked; **independent lexical acceptance unresolved** for `Cunz`. The shared Save label also serves credit and palette persistence controls, so its eventual resolution must retain those contexts.
- `save20_title`: consistent with the current Save family and ellipsis, but **lexical acceptance unresolved** on the same Save-verb premise.
- `ui_save_your_changes`: the save-or-not question fits the following body and three buttons, but **lexical acceptance unresolved** for its Save verb.
- `ui_your_current_image_has_unsaved_changes`: not-yet negation and changes object fit the single-document dialog; omission of an explicit current-image noun is contextually reasonable. **Lexical acceptance unresolved** for the Save verb.

Thus this cohort records **four existing entries with bounded linguistic acceptance and five with unresolved lexical evidence**, not nine cleared entries. It is not all-string release clearance. Current-resource presence, alias resolution and label matching are not independent proof of language correctness. Bounded dictionary/search results did not corroborate `cunz` as save; their absence is not proof that the software sense is wrong. No unsupported replacement is made. Resolving that term must also recheck labels and quoted references across the catalogue, including these two new messages. These unresolved entries remain on the release-review queue.

## Sources and confidence

- Directly retrieved [MediaWiki Zhuang catalogue](https://raw.githubusercontent.com/wikimedia/mediawiki/master/languages/i18n/za.json) supports the saved-state phrase `rom lo`, editing, file and current vocabulary. Its saved-edit message has an English subject, which is not used as Zhuang grammar evidence.
- Directly retrieved [Sawloih Cuengh-Gun OCR](https://dokumen.pub/sawloih-cuengh-gun-ocr.html) supports the first/then ordering, not-yet negation, alternative conjunction, change verb and discard verb. The discard entry is at L235, the before/first entry at L1581. Retrieved `cunz` entries concerned visiting/patrolling, not saving. OCR and sense-selection limits remain.
- Directly retrieved [Guangxi Minzu Bao translation commentary, 22 June 2022](https://www.guangximinzubao.cn/szbzw/html/2022-06/22/content_44015.htm), especially L26 following example 1, explains `laebdaeb` as continuing action. This resolves the concern raised by the older dictionary's narrower connecting gloss; it does not certify the entire UI phrase as native-tested.

No native-speaker or software-usability certification is claimed. The actual consequential distinctions are reviewed separately from idiomaticity and presentation.

## Verification

- All 171 offered-option catalogue checks and the priority manifest passed; existing nodes, attributes, ordered placeholders, numerals, protocol literals, newline escapes and XML escaping are preserved.
- `python -m unittest -v test_translations test_translation_boundaries test_string_importance test_current_localization_contracts`: **61 tests passed in 6.246 seconds**.
- **12 English/Zhuang Java formatting cases** passed: the two new static messages and the saved-file template with percent-containing, Unicode, empty and null filename arguments. This is host formatting, not Android compilation.
- Temporary token-aware checks passed for all three new-resource bindings, output-before-success ordering, non-export-only saved-state updates, cleared/blocked deferred action, the Save/Discard/Keep editing routes, the three output formats and exact current quoted-command labels. These are source checks, not runtime state execution.
- All **1,585 base tracked blobs and executable modes** were verified before editing. `git diff --check` passed. Publication checks the complete tree overlay, expected-parent non-force lease and exact remote file bytes.

Existing `DerivedExportStateTest` ICO/ASCII/Base64 cases and `SavedImageSettingsTest.derivedExportsCannotReplaceTheRememberedSaveDestination` were inspected, not run. They cover output contents, dirty state, unchanged ordinary destination and blocking pending close; their presence is not a new pass. No permanent per-edit wording fixture/test is added.

Zhuang direct presence: **P0 72/94, P1 158/249, P2 80/305, P3 3/71**. Global direct gaps: **159 P0 / 1,333 P1 / 30,049 P2 / 7,478 P3** across 171 options. The [release plan](p0-p1-release-plan-20261106.md) still requires completion plus review of all translated strings, including existing P2/P3.

Android SDK/Kotlin compiler, Android compilation, Robolectric, actual save/export UI execution, device/font-scale layout and TalkBack were unavailable or unrun locally. Exact-head Actions state is checked after publication and reported separately. No full-review, CI-pass, merge or release claim is made.
