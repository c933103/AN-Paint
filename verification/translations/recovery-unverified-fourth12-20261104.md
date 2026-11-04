# Conditional recovery notices: fourth reviewed batch

Integration parent: 6ad0ff5d378435816a959ed8e60be39fb827a4ef.

Adds 24 independently reviewed translations for az, fil, hy, eu-ES, gu, ka, kn, mk, ml-IN, pa-IN, ta and te. Both resources are ui_recovery_copy_preserved_unverified and ui_recovery_copy_exported_unverified. Independent review accepted all 24 unchanged, with no holds. Original catalogue identities were checked against the integration parent; all existing entries are preserved.

The review verifies uncertain damaged/unreadable contents; extraction conditional on both ZIP opening and a readable canvas.png; exact local File / Load image captions; and keeping the exported copy even when unopenable. Preserved notices retain %1$s, the actual export route and optional later resizing. Exported notices retain unchanged contents and only possible, unverified draft settings or floating selection.

Local checks:
- All 171 offered catalogues passed structural validation in test_translations.
- test_translations, test_localized_help, test_translation_boundaries, test_current_localization_contracts, test_language_translation_note, test_string_importance, test_ordinary_priority_followthrough and test_open_review_recovery: 78 tests passed.
- All 12 XMLs parse without duplicate keys, add exactly two entries, and preserve old attributes/text.
- All exact menu labels, expected placeholder counts, ZIP/canvas.png literals and reviewed conditional/notice-specific segments are retained.

These are bounded linguistic and host-check results, not whole-locale completion or runtime acceptance. No Android compilation, device/rendering/glyph/RTL verification, hosted CI or release verification is claimed.
