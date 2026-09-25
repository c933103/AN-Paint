# Localization handoff backport for PR #9

Reviewed integration snapshot: `c0b33f11de5c2f9e9251225200ad1d6977883f2d`. Original PR head: `2e0d3251223c07f71c49b09307b968f89cf9c9e1`.

Full reviewed catalogues carried by this branch (including its stacked localization parents): `jje`, `mnc-Mong`, `ain-Kana`, `ain-Latn`, `ryu`, `ja`, `zh-HK`, `zh-TW`, `zh-CN`, `yue-Hant`, `yue-Latn`.

Known shared help, navigation-caption, English fallback-note and crop-count repairs also apply to resource catalogues already present on this branch. Required local button-caption overrides travel with their help text. Other branches’ new locale directories and completeness tooling are not introduced. The original scoped translation test definitions are preserved.

The shared Wu UI fallback font, vertical-layout support and image-credit feature changes are part of integration PR #15. This scoped original PR does not claim to contain or validate those app changes on its own.

Local validation: 22 tests passed (`test_translations.py`: 16, `test_localized_help.py`: 6). Strict AAPT2 compilation of all resources and `git diff --check` passed. These checks verify catalogue structure, documented controls and the specific recorded regressions; they do not certify native fluency.

Android build and runtime results must be read from the workflow for the published head. Local resource compilation is not an APK or device-test result. The linked audit documents distinguish completed repairs from remaining linguistic review limits.
