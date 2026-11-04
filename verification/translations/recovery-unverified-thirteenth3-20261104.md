# Recovery notices: Hakka, Southern Min and Wu

Base commit: 72ff76c0e7f468ea02792293ff408a26d963da07.

Adds six direct translations for hak-Hant-TW, nan-Hant-TW and wuu-Hans. Romanized options remain separate; inherited fallback is not counted as translated. Independent review accepted all six with one Wu correction: the final clause now uses 打勿开 rather than 打不开 in both notices and its shared semantic segment. Hakka and Southern Min were accepted unchanged.

Validation passed:
- Current base resource Git blob identities and exact offered-option membership; all existing string attributes/text unchanged, only the two requested keys added per catalogue.
- XML, duplicate-name, Android quoting/format, exact current menu labels, ZIP/canvas.png literals and placeholder checks. %1$s remains exactly once in preserved notices and absent from exported notices.
- Both notices retain possible damage OR unreadability, both ZIP-opening AND readable-image preconditions, and keeping even an unopenable copy. Preserved notices retain conditional resizing; exported notices retain unchanged contents and unverified possible settings OR selection.
- 78 host tests passed across test_translations, test_localized_help, test_translation_boundaries, test_current_localization_contracts, test_language_translation_note, test_string_importance, test_ordinary_priority_followthrough and test_open_review_recovery. Structural checks cover all 171 offered options.

Limits: no Android build, device, native-speaker certification, glyph/layout inspection or CI result is claimed. Structural coverage is not whole-catalogue completeness.
