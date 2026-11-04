# Conditional recovery notices: tenth reviewed batch

Integration parent: 7c8c595ed6e32c40bd51b0326106b4c3ef6bd4f9.

Adds ten independently reviewed direct translations for tt-Cyrl, tt-Latn, ug, mi and sm. Both resources are ui_recovery_copy_preserved_unverified and ui_recovery_copy_exported_unverified. Review accepted all ten with a Samoan modifier correction in the preserved notice, now applied: Ua teuina se kopi ese mo le toe faafoʻi. All five original catalogue identities match the integration parent; previous entries are preserved. These are direct entries, not inherited-fallback coverage credit.

Reviewed boundaries preserve possible damage or unreadability; extraction only if ZIP opening and readable canvas.png both hold; exact File / Load image commands; keeping an unopenable export; %1$s, export route and optional later resizing in preserved notices; unchanged contents and possible but unverified settings or floating selection in exported notices.

Local checks:
- All 171 offered catalogue structural checks passed inside test_translations.
- test_translations, test_localized_help, test_translation_boundaries, test_current_localization_contracts, test_language_translation_note, test_string_importance, test_ordinary_priority_followthrough and test_open_review_recovery: 78 tests passed.
- Five XMLs parse without duplicate keys, add exactly two entries each, and preserve existing string attributes/text.
- Actual menu labels, expected placeholders, ZIP/canvas.png literals, conditional/notice-specific segments and the Samoan correction pass focused checks.

No whole-locale completion, Android/native compilation, device/rendering/RTL/glyph verification, hosted CI or release verification is claimed. These findings are bounded to the reviewed batch and host checks.
