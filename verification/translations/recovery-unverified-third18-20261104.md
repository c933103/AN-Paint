# Conditional recovery notices: third reviewed batch

Integration parent: 05da9fdea6215f63db5501fe96922bab2255124a.

Adds 36 independently reviewed translations of ui_recovery_copy_preserved_unverified and ui_recovery_copy_exported_unverified across 18 offered locale options: af, eo, et, is, lv, mr, ne, sr-Cyrl, sr-Latn, bn, bs, gl, lt, ms, sq, sw, th and ur. Independent review accepted all 36 unchanged, with no holds. Existing entries remain unchanged; all 18 original catalogue blobs match the integration parent.

Reviewed boundaries: contents may be damaged or unreadable; extraction requires both ZIP opening and a readable canvas.png; actual local File / Load image commands are retained; the export is kept even if it cannot be opened. The preservation notice retains %1$s, the actual export route and optional later resizing. The exported notice reports unchanged contents and merely possible, unverified draft settings or floating selection.

Checks on the integrated resources:
- All 171 offered catalogue structural checks passed inside test_translations.
- test_translations, test_localized_help, test_translation_boundaries, test_current_localization_contracts, test_language_translation_note, test_string_importance: 76 tests passed.
- test_afrikaans_priority_wording, test_bulgarian_bengali_priority_wording, test_croatian_bosnian_p0_wording, test_esperanto_priority_wording, test_estonian_priority_wording, test_finnish_estonian_latvian_crop_companions, test_latvian_priority_wording, test_serbian_p0_wording, test_ordinary_priority_followthrough, test_open_review_recovery: 23 tests passed.
- All 18 XMLs parse without duplicate names, add exactly two keys, preserve every old string attribute/text, and retain exact menu labels, ZIP, canvas.png and expected format placeholders.
- Both notices retain their reviewed conditional/uncertainty/keep-copy clauses; resizing and optional unverified metadata remain confined to their intended notices.

99 named host tests passed. No Android compilation, device behavior, RTL/layout/glyph verification, hosted CI, release verification or whole-locale completion is claimed. The findings concern only this translation batch and the stated host checks.
