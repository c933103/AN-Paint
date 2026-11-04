# Recovery notices: Hmong Daw and Northern Sami

Base commit: d8e87092c959bd31a712d67080449da859964d14.

Adds four direct translations for mww and se. Independent review accepted Hmong unchanged and supplied a Northern Sami correction specifying a canvas.png file that can be read and taking the image out. The correction is applied identically in both notices and the shared semantic segment.

Validation passed:
- Exact base resource blob identities and offered-option membership; old string attributes/text unchanged, only two requested entries added per resource.
- XML parsing, duplicate-name, Android quoting/format, exact current menu labels, ZIP/canvas.png literal and placeholder checks. One %1$s only in preserved notices.
- Possibility of damage OR unreadability, both ZIP-opening AND readable-image conditions, and keeping even an unopenable copy remain in both notices. Preserved notices retain optional resizing; exported notices retain unchanged contents and unverified possible settings OR selection.
- 78 host tests passed: test_translations, test_localized_help, test_translation_boundaries, test_current_localization_contracts, test_language_translation_note, test_string_importance, test_ordinary_priority_followthrough and test_open_review_recovery. Structural coverage includes all 171 offered options.

Limits: direct coverage is distinct from fallback. No native-speaker certification, Android build, device, rendered glyph/layout or CI result is claimed. Structural checks are not whole-catalogue translation completeness.
