# Localization handoff backport for PR #6

Reviewed integration snapshot: `c0b33f11de5c2f9e9251225200ad1d6977883f2d`. Original PR head: `8f805868f15bc4f255a4f31455668fc7ffeeb590`.

Full reviewed catalogues carried by this branch (including its stacked localization parents): `lzh-Hant`, `hak-Hant-TW`, `hak-Latn-TW`, `nan-Hant-TW`, `nan-Latn-TW`, `wuu-Hans`, `ja`, `zh-HK`, `zh-TW`, `zh-CN`, `yue-Hant`, `yue-Latn`.

Known shared help, navigation-caption, English fallback-note and crop-count repairs also apply to resource catalogues already present on this branch. Required local button-caption overrides travel with their help text. Other branches’ new locale directories and completeness tooling are not introduced. The original scoped translation test definitions are preserved.

The shared Wu UI fallback font, vertical-layout support and image-credit feature changes are part of integration PR #15. This scoped original PR does not claim to contain or validate those app changes on its own.

The Wu U+20C8E character was already present at this PR’s original head. These catalogue edits add no new supplementary Wu glyph. Bundled Wu coverage is verified with PR #15’s fallback asset and runtime support, not with this original branch alone.

Local validation: 25 tests passed (`test_translations.py`: 19, `test_localized_help.py`: 6). Strict AAPT2 compilation of all resources and `git diff --check` passed. These checks verify catalogue structure, documented controls and the specific recorded regressions; they do not certify native fluency.

Android build and runtime results must be read from the workflow for the published head. Local resource compilation is not an APK or device-test result. The linked audit documents distinguish completed repairs from remaining linguistic review limits.
