# Conditional recovery notices: seventh reviewed batch

Integration parent: 56d4eee8fe57e5c97c427cac1e70ab183e8be5b6.

Adds 16 independently reviewed translations for as, km, ko-KP, lo, lzh-Hant, my, yue-Hant and si. Both resources are ui_recovery_copy_preserved_unverified and ui_recovery_copy_exported_unverified. Independent review accepted all 16 with the Classical Chinese possibility clause refined in both notices to 其所存或已損壞，亦或不可讀。. All eight original catalogue identities match the integration parent, and all existing entries remain unchanged.

Reviewed boundaries retain potentially damaged or unreadable contents; extraction only if the export opens as ZIP and contains readable canvas.png; current menu captions; and keeping an unopenable export. Preserved notices retain %1$s, the export route and optional subsequent resizing. Exported notices retain unchanged contents and possible but unverified draft settings or floating selection.

Local checks:
- All 171 offered catalogues pass structural validation within test_translations.
- test_translations, test_localized_help, test_translation_boundaries, test_current_localization_contracts, test_language_translation_note, test_string_importance, test_ordinary_priority_followthrough and test_korean_priority_wording: 81 tests passed.
- Eight XMLs parse without duplicate keys, add precisely two entries each, and preserve old string attributes/text.
- Exact menu labels, placeholder counts, ZIP/canvas.png literals, reviewed conditional/notice-specific clauses and Classical Chinese refinement checks passed.

No whole-locale completion, Android compilation, native/device/rendering/RTL/glyph verification, hosted CI or release verification is claimed. Results are bounded to these translations and host checks.
