# Recovery notice translations: Breton, Walloon, Wolof and Lingala

Base commit: 447f3f152ec2a94ef88ebdca54a2bbe2bc9dd3be.

Adds eight direct translations of ui_recovery_copy_preserved_unverified and ui_recovery_copy_exported_unverified for br, wa, wo and ln, each an exact offered language option. Independent review accepted all eight unchanged with no holds. Direct resources are distinguished from inherited fallback coverage.

Validation passed:
- Base resource Git blob identities match the verified current tree. Existing string attributes/text remain unchanged; exactly the two requested keys are added per resource.
- XML parsing, duplicate-name, Android apostrophe/format, exact current localized menu-label, placeholder, ZIP and canvas.png checks.
- Damage/unreadability remains possible, not asserted. Extraction requires both ZIP opening and readable canvas.png. Both notices retain the instruction to keep even an unopenable copy. Preserved notices include the sole %1$s and optional resizing; exported notices state unchanged contents and unverified possible settings or floating selection.
- 78 host tests passed across test_translations, test_localized_help, test_translation_boundaries, test_current_localization_contracts, test_language_translation_note, test_string_importance, test_ordinary_priority_followthrough and test_open_review_recovery. Structural coverage includes all 171 offered options.

Limits: no Android build, device, native-speaker certification, rendered glyph/RTL inspection or CI result is claimed. These structural results do not establish whole-catalogue translation completeness.
