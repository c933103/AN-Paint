# Recovery notices: Maithili, Chhattisgarhi and Kashubian

Base commit: bc598263453c06c6834fd51191df9099b7835323.

Adds six direct translations for mai, hne and csb. Independent review accepted all six with two corrections: Maithili explicitly refers to all optional settings/selection as unverified; Chhattisgarhi uses an explicit readable-canvas.png relative clause in both notices. Corrections are present in the full notices and corresponding semantic segments. Kashubian was accepted unchanged.

Validation passed:
- Exact base resource blob identities and offered-option membership; all existing string attributes/text unchanged, with only the two requested keys added per catalogue.
- XML and duplicate-name checks, Android escaping/format validity, exact localized menus, ZIP/canvas.png literals, and sole %1$s in preserved notices.
- Both notices retain possible damage OR unreadability, both ZIP-opening AND readable-image preconditions, and keeping even an unopenable copy. Preserved notices retain conditional resizing; exported notices retain unchanged contents and unverified possible settings OR selection.
- 78 host tests passed: test_translations, test_localized_help, test_translation_boundaries, test_current_localization_contracts, test_language_translation_note, test_string_importance, test_ordinary_priority_followthrough and test_open_review_recovery. Structural coverage includes all 171 offered options.

Limits: direct translation coverage is separate from inherited fallback. No Android build, device, native-speaker certification, rendered UI or CI result is claimed. Structural checks are not whole-catalogue completeness.
