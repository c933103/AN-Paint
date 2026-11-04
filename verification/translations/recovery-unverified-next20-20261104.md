# Conditional recovery notices: second reviewed batch

Integration parent: c474413c457e9ae0ae8be6342d5c2098960f475b.

Adds 40 independently reviewed translations for ar, fa, fa-IR, he, hi, es-ES, es-419, ko-KR, el, ro, hu, bg, sk, sl, hr, ca, no, nn, vi and pt-PT. Both IDs are ui_recovery_copy_preserved_unverified and ui_recovery_copy_exported_unverified. All 20 original catalogue blob identities were verified against the integration parent; all pre-existing nodes are preserved.

Independent review accepted the batch with two refinements now applied to both notices and their draft meaning segments: Hindi explicitly places both damaged and unreadable alternatives under possibility; Nynorsk names canvas.png as a file (canvas.png-fil). Regional Persian and Spanish options have independently inspectable resource entries; Spanish retains the existing regional settings terminology.

Semantic boundaries retained in every locale: possibly damaged or unreadable contents; extraction only if the export opens as ZIP AND contains readable canvas.png; exact local File and Load image menu labels; keeping the exported copy even when it cannot be opened. The preservation notice retains %1$s, the local Export recovery copy route, and optional later resizing. The export notice says contents are unchanged and settings or floating selection may be present but remain unverified. Hebrew menu routing retains the left-arrow convention.

Checks:
- All 171 offered locale catalogues pass structural validation within test_translations.
- test_translations, test_localized_help, test_translation_boundaries, test_current_localization_contracts, test_language_translation_note and test_string_importance: 76 tests passed.
- Twelve existing affected-language modules (Bulgarian/Bengali; three Catalan/Romanian; Croatian/Bosnian; Danish/Norwegian; Greek; Korean priority; two Nynorsk; Slovak/Slovenian; Spanish): 29 tests passed.
- 20 candidate XMLs parse, have no duplicate keys, add exactly two entries each, and preserve all existing string attributes/text.
- Per-locale placeholders, ZIP and canvas.png literals, exact menu captions and conditional/uncertainty segment checks passed.

Total named local unittest runs: 105 passed. No Android compilation, device/rendering/glyph coverage, hosted CI, release verification or whole-locale completion is claimed. These are bounded translation and host-check findings; remaining options still use source fallback for these IDs.
