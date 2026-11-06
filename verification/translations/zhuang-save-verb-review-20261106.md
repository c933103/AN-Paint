# Zhuang Save-verb evidence and reference correction

6 November 2026. Parent `2d6ced39c1f79c1d0d21ed47a120baf94a7ee877`, tree `4fec6a8874ce92fe9806a2f20263eb0f2bf68f83`, was reconciled with no pending write. Changes the Save verb in **16 existing canonical string resources** and preserves the **unchanged Save alias**. Resource presence remains 313. Only canonical Zhuang XML and this report change; develop and the separate Navajo work are untouched.

## Decision and evidence

The [preceding scoped review](zhuang-export-safety-review-20261106.md) recorded five unresolved lexical holds involving `Cunz`. An independent review now accepts using the better-supported storage verb **rom**, consistently in commands, the unsaved-work question/body and quoted command references. This resolves those five specific holds on the new wording's evidence. It does **not** establish that the old term was linguistically wrong, restore withdrawn catalogue approval, or certify every surrounding paragraph anew.

Evidence was directly retrieved by both checks:

- [Sawloih Cuengh-Gun OCR](https://dokumen.pub/sawloih-cuengh-gun-ocr.html), L1505, includes storage among the senses of `rom`.
- [MediaWiki Zhuang catalogue](https://raw.githubusercontent.com/wikimedia/mediawiki/master/languages/i18n/za.json), `postedit-confirmation-saved`, uses `rom lo` for a saved edit. Its English subject is not Zhuang sentence-grammar evidence, and its other labels are not adopted as automatic authority.
- The reviewer also checked dictionary L115 for the result/become sense of `baenz`, L2878 for an actual positive-negative question pattern and L1221 for not-yet negation. These support the affected Save-as/question/body compositions without claiming standardized software attestation.

Confidence is **bounded moderate** for the new Save family and its contextual compositions. Native-speaker/software-usability certification is not claimed or imposed as an invented gate. The change chooses supported wording rather than indefinitely retaining a specific evidential uncertainty.

## Exact reviewed scope

All identities below are `string` resources. The only text substitutions are case-preserving `Cunz` to `Rom` and `cunz` to `rom`; every other character, node, attribute and resource order is preserved.

- **Shared Save command:** `ui_save`; `ui_save_a5d0d9` remains an alias to it. The common meaning is saving the relevant data. The checked consumers are the document Save action/icon, dirty-document Save confirmation, replacement of a saved palette colour, and credit Save. Palette and credit controls must not be described as necessarily writing an image file.
- **Save-as/output family:** `save20_title`, `ui_save_as`, `ui_save_as_jpeg`, `ui_save_as_jpeg_xl`, `ui_save_as_png`, `ui_save_png`. The Save-as title is live in the File menu and options dialog; Save PNG is live in assembly output. No current direct production binding was found for the four `ui_save_as*` resources. They remain canonical and consistent, but have no claimed runtime-display verification.
- **Unsaved-work decision:** `ui_save_your_changes`, `ui_your_current_image_has_unsaved_changes`. The positive-negative question and not-yet-saved changes statement retain their existing dialog context. They do not imply that no prior saved original exists. Together with the Save command, alias and Save-as title, these are the five formerly held entries whose Save-verb evidence is now resolved narrowly.
- **Autosave/recovery references:** `ui_autosave_failed_use_save`, `ui_autosave_paused_use_save`, `ui_autosave_is_paused_to_protect_that_draft_use`. Quoted Save and File → Save as labels now match the corrected controls. Existing surrounding storage wording, the recovery-copy command, `%1$s`, and PNG/JPEG choices are unchanged. Prior-draft preservation and saving the current drawing remain distinct.
- **Animation notices:** `formats22_animation_still`, `formats22_animation_poster`. Only the quoted Save command changes. Existing notices still distinguish the first still frame from a separate PNG default image and explain the saved result is not animated.
- **Export safety:** `ui_export_did_not_save23`, `ui_export_explanation23`. Only quoted Save/Save-as references change. Completed export output is still distinct from saving the working drawing, and the ordinary Save destination remains unchanged by export.

The longer recovery/animation/export paragraphs receive a **Save-reference consistency review** here, not a blanket new linguistic certification of every unchanged clause. Existing bounded evidence and remaining limitations continue to apply. Canonical Android XML owns runtime wording. `translations/basic-translations.json` retains its historical source vocabulary unchanged; the current catalogue tooling explicitly treats such files as provenance/reference material, not generated production output. No full-language approval mirror or per-edit permanent wording test is introduced.

## Consumer and test verification

- All 171 offered-option catalogue checks and priority-manifest validation passed. Exactly 16 existing values changed; all attributes, placeholders, numbers, escapes, aliases and other text are preserved.
- `python -m unittest -v test_translations test_translation_boundaries test_string_importance test_current_localization_contracts`: **61 tests passed in 5.991 seconds**.
- **46 English/Zhuang Java cases** passed for the 16 affected resources and Save alias, including Unicode, percent-containing, empty and null arguments for the two formatted messages. This is host XML/format testing, not Android compilation.
- Temporary token-aware checks verified the document, palette, credit and assembly Save bindings; unsaved-dialog Save/Discard/Keep editing routes; non-export-only saved-target and markSaved updates; autosave failure and protected-recovery branches; animation-notice selection; exact current quoted labels; and the four retained unbound resources. These are static source checks, not executed Android flows.
- All **1,586 base tracked blobs and executable modes** were verified before editing. `git diff --check` passed. Publication verifies the complete tree overlay, expected-parent non-force lease and exact remote bytes.

No new key is added, so direct-presence totals are unchanged: Zhuang **P0 72/94, P1 158/249, P2 80/305, P3 3/71**; global gaps **159 P0 / 1,333 P1 / 30,049 P2 / 7,478 P3**. This batch advances evidence-backed review, not gap-count arithmetic.

Android SDK/Kotlin compiler are unavailable here. Android compilation, Robolectric, actual saving/recovery/animation/export behavior, device/font-scale layout and TalkBack were not run. Shorter text is not by itself a measured layout pass. Exact-head Actions state is checked after publication and reported separately. The [full review and release plan](p0-p1-release-plan-20261106.md) remains in progress; no merge, release or complete-review claim is made.
