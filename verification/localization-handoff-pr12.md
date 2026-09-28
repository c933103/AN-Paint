# Localization handoff backport for PR #12 — claims withdrawn

**Localization status reset — 28 September 2026: all previous progress, completion, repair, verification and no-defect conclusions for PRs #2–#9, #12 and #15 are withdrawn. Every item requires a full recheck; no previous progress is accepted.**

See the [individual recheck register](https://github.com/c933103/AN-Paint/blob/review/localization-integration/verification/localization-recheck-register.md). The rejected delivery is additional material to check, not an accepted audit. Historical source, test outputs and evidence classifications remain available as inputs. They carry no current completion credit. Completing the other 81 locales is outside this task.

Every assertion in the record below is a **withdrawn prior claim requiring full recheck**, including any statement that work was reviewed, implemented, repaired, complete, verified, preserved, or free of further defects. Prior lexical acceptance labels and test outcomes are historical inputs, not current task status.

[Original record at its previous commit](https://github.com/c933103/AN-Paint/blob/3d674096fc7ae5f4ed4507136085f1f49c6f453b/verification/localization-handoff-pr12.md).

<details>
<summary>Withdrawn historical claim record — no accepted progress</summary>

# Localization handoff backport for PR #12

Reviewed integration snapshot: `c0b33f11de5c2f9e9251225200ad1d6977883f2d`. Original PR head: `29ef7eab4587071c59a2d013cd7e88112decd674`.

Full reviewed catalogues carried by this branch (including its stacked localization parents): `ko-KR`, `ko-KP`, `ko-Kore-KR`, `vi`, `vi-Hani`, `ja`, `zh-HK`, `zh-TW`, `zh-CN`, `yue-Hant`, `yue-Latn`.

Known shared help, navigation-caption, English fallback-note and crop-count repairs also apply to resource catalogues already present on this branch. Required local button-caption overrides travel with their help text. Other branches’ new locale directories and completeness tooling are not introduced. The original scoped translation test definitions are preserved.

The shared Wu UI fallback font, vertical-layout support and image-credit feature changes are part of integration PR #15. This scoped original PR does not claim to contain or validate those app changes on its own.

The revised Nôm catalogue is accompanied by its rebuilt UI subset and matching inventory hash. Font coverage and the unchanged pinned source and licence metadata were checked. Other font inventory entries and the existing legal notices remain unchanged. The Korean corpus evidence checker also passed against the pinned external corpus; the source table separates accepted occurrences from rejected UI senses.

Local validation: 28 tests passed (`test_translations.py`: 16, `test_localized_help.py`: 6, `test_korean_nom_semantics.py`: 4, `test_locale_font_coverage.py`: 2). Strict AAPT2 compilation of all resources and `git diff --check` passed. These checks verify catalogue structure, documented controls and the specific recorded regressions; they do not certify native fluency.

Android build and runtime results must be read from the workflow for the published head. Local resource compilation is not an APK or device-test result. The linked audit documents distinguish completed repairs from remaining linguistic review limits.

</details>
