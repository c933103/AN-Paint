# Conditional recovery notices: sixth reviewed batch

Integration parent: fee7b046c1f6109738aa3d79bf2a2cd3b1d93a32.

Adds 24 independently reviewed translations for be, ceb, ha, ht, jv, ky, mn-Cyrl-MN, so, su, tg, uz-Latn and kk. Both resources are ui_recovery_copy_preserved_unverified and ui_recovery_copy_exported_unverified. Review accepted all 24 with one Mongolian genitive correction, applied in the exported notice: Нооргийн тохиргоо. All original catalogue blobs match the integration parent; all existing entries remain unchanged.

Reviewed boundaries preserve possibly damaged or unreadable contents; extraction conditional on both ZIP opening and readable canvas.png; current File / Load image captions; and keeping an unopenable exported copy. Preserved notices retain %1$s, the export route and optional later resize. Exported notices retain unchanged contents and only possible, unverified draft settings or floating selection.

Local verification:
- All 171 offered catalogues pass structural validation within test_translations.
- test_translations, test_localized_help, test_translation_boundaries, test_current_localization_contracts, test_language_translation_note, test_string_importance, test_ordinary_priority_followthrough and test_open_review_recovery: 78 tests passed.
- All 12 XMLs parse with no duplicate keys, exactly two additions per catalogue, and unchanged prior string attributes/text.
- Actual menu captions, placeholder counts, ZIP/canvas.png literals, reviewed conditional clauses, notice-specific segments and the Mongolian correction pass focused checks.

No whole-locale completion, Android compilation, native/device/rendering/RTL/glyph verification, hosted CI or release verification is claimed. Evidence is bounded to this reviewed translation batch and the listed host checks.
