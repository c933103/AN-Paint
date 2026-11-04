# Recovery notices: Romanized Cantonese and mixed-script Korean

Base commit: da0b4fcfc37a0bbab24e218d77ef6ba4ae992615.

Adds four direct translations for yue-Latn and ko-Kore-KR, accepted unchanged by independent review with no holds. Romanized Cantonese uses Jyutping and current romanized menu labels; Korean retains the option's mixed Hangul/Hanja technical terminology. These are exact script-specific resources, not inherited-parent coverage.

Validation passed:
- Current base resource identities and exact picker membership; all existing string attributes/text retained, only the two requested entries added per resource.
- XML parse, duplicate-name, Android quoting/format, exact menu label, ZIP/canvas.png literal and placeholder checks. One %1$s in preserved notices, none in exported notices.
- Possible damage OR unreadability, joint ZIP-opening AND readable-image preconditions, and keeping even an unopenable copy preserved in both notices. Conditional resizing remains in preserved notices; unchanged export and unverified possible settings OR selection remain in exported notices.
- 78 host tests passed: test_translations, test_localized_help, test_translation_boundaries, test_current_localization_contracts, test_language_translation_note, test_string_importance, test_ordinary_priority_followthrough and test_open_review_recovery. Structural coverage includes all 171 offered options.

Limits: no native-speaker certification, Android build, device, rendered script/glyph inspection or CI result is claimed. Structural checks do not establish whole-catalogue completeness.
