# Recovery notice translations: four additional options

Base commit: eb9e9debbbb1743f6e31a5f3f97189a5732a7489.

Adds eight direct translations of ui_recovery_copy_preserved_unverified and ui_recovery_copy_exported_unverified for Nigerian Pidgin (pcm), Tok Pisin (tpi), Yiddish (yi), and Sanskrit (sa). These are direct resources, not inherited fallback coverage.

Independent review accepted all eight with three Tok Pisin corrections: explicit reader subjects for possibly unreadable contents and readable canvas.png; explicit subject/object for the unverified optional settings or floating selection. All requested replacements were applied to the full notices and matching semantic segments before validation.

Checks passed:
- Exact base resource blob identities; all pre-existing string attributes and text retained unchanged; only the two requested entries added to each catalogue.
- XML parsing and duplicate-name checks, one %1$s in preserved notices and none in exported notices, and exact ZIP/canvas.png literals.
- Current localized File, Export recovery copy, and Load image menu labels retained exactly.
- Shared conditional guidance requires both an opening ZIP and readable canvas.png; possible damage/unreadability and keeping even an unopenable copy are preserved. Resize guidance belongs to the preserved notice; unchanged export and unverified optional settings/selection belong to the exported notice.
- 78 host tests passed: test_translations, test_localized_help, test_translation_boundaries, test_current_localization_contracts, test_language_translation_note, test_string_importance, test_ordinary_priority_followthrough, test_open_review_recovery. The structural suite covers all 171 offered language options.

Scope limits: no Android build, device, native-speaker certification, rendered glyph/RTL inspection, or CI result is claimed. Structural coverage is not whole-catalogue translation completeness.
