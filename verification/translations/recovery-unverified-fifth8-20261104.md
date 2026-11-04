# Conditional recovery notices: fifth reviewed batch

Integration parent: ab01327ffb59f2655a4b7feab308bffcdcc4977d.

Adds 16 independently reviewed translations for ast, ca-ES-valencia, cy, fy, ga, ia, la and oc. The resources are ui_recovery_copy_preserved_unverified and ui_recovery_copy_exported_unverified. Independent review accepted all 16 with one Welsh sentence refinement applied to both notices: explicit paired conditions and coordinated imperative instructions. All eight base resource identities match the integration parent; all old entries remain unchanged.

Reviewed semantics retain possibly damaged or unreadable contents, both ZIP opening and readable canvas.png as extraction preconditions, actual menu labels, and keeping the export even when it cannot be opened. Preservation notices retain %1$s, the export menu and optional later resizing. Export notices retain unchanged contents and possible but unverified settings or floating selection.

Checks:
- All 171 offered catalogue structural checks passed inside test_translations.
- test_translations, test_localized_help, test_translation_boundaries, test_current_localization_contracts, test_language_translation_note, test_string_importance, test_ordinary_priority_followthrough and test_valencian_variant_packaging: 81 tests passed.
- Eight candidate XMLs parse without duplicate names, add exactly two keys each, and preserve existing attributes/text.
- Exact menu labels, placeholder counts, ZIP/canvas.png literals, reviewed conditional segments and Welsh replacement checks passed.

This is bounded translation evidence, not whole-locale completion or runtime acceptance. No Android compilation, device/rendering/glyph coverage, hosted CI or release verification is claimed.
