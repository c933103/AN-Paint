# Conditional recovery notices: 18-locale translation review

Integration parent: d61230e4138ba4232a6073312eabb03c2596510f.
Source/draft base: 31fdd100c5f1162e2e416284a051e78732c53b46. All 18 original catalogue blob identities are unchanged between these commits. The intervening commit changes only a guard and its correction receipt.

Adds `ui_recovery_copy_preserved_unverified` and `ui_recovery_copy_exported_unverified` in cs, da, de, fi, fr, id, it, ja, nl, pl, pt-BR, ru, sv, tr, uk, zh-CN, zh-HK and zh-TW. Existing entries and application behavior are unchanged.

Independent review accepted the 36 translations with the following changes, now applied: Czech optional-content wording explicitly says none of the possible contents was verified; Japanese damage/unreadability wording preserves uncertainty over both alternatives; Japanese optional settings/selection are explicitly unverified. These are bounded translation findings, not whole-locale completion claims.

Every translation retains: potentially damaged OR unreadable contents; the joint condition of opening as ZIP AND containing readable canvas.png before extraction; the actual locale File / Load image command names; and keeping the copy even if it cannot be opened. The preserved notice keeps %1$s, export instructions and optional later resizing. The exported notice states unchanged contents and merely possible, unverified draft settings or floating selection. Menu labels include their actual ellipses.

Local checks on the resulting resources:
- All 171 offered catalogues: structural validation reports zero errors.
- Full test_translations module: 34 tests passed.
- test_localized_help, test_translation_boundaries, test_current_localization_contracts, test_language_translation_note and test_string_importance: 42 tests passed.
- 18 existing affected-language test modules: 81 tests passed.
- Each changed catalogue: XML parsed, no duplicate keys, exactly two additions, every existing node's attributes/text unchanged, exact menu labels, expected placeholder count, ZIP and canvas.png preserved.
- Each notice: reviewed conditional, uncertainty and keep-copy segments present; resizing and optional-unverified-content clauses remain in their intended notices.

Total named unittest runs: 157 tests passed. Structural checks and source guards do not establish Android compilation, on-device rendering, glyph coverage or runtime correctness. No Android build, device run, hosted CI, whole-language acceptance or release verification is claimed. Other untranslated options continue to fall back to the English source for these two IDs.
