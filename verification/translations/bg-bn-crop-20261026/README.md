# Bulgarian, Bengali and crop wording integration

Base: `393f2804b5f3fabb935aa773758a9a8f6f464b31`.

This evidence binds exact independently reviewed wording to a bounded change:

- Bulgarian: 341 P0/P1 scalar identities, including 238 additions, 14 replacements and 89 unchanged values.
- Bengali: 341 P0/P1 scalar identities, including 256 additions, 27 replacements and 58 unchanged values.
- Three `ui_crop_preview_images` `other` forms: Taiwan Sixian Hakka in Han and Pha̍k-fa-sṳ, and Shanghai-based Simplified written Wu. Preview/apply prefixes, argument order and newline escapes are retained. No optional Wu alternative is used.

`reviewed-wording.json` contains the full source/target priority pairs, independent review notes and crop dispositions. Original candidate/review artifact digests identify the preparation inputs; internal process notes are not part of this export. `validation.json` binds the proposed application/test files by exact Git blob and content hashes. This is a one-time evidence record, not a CI source-hash oracle.

## Qualifications

These are model linguistic/static judgments, not native-human certification. Thirty priority identities per locale have source-only context and remain explicitly qualified. The three crop judgments are source-assisted whole-value judgments with the language-specific limitations recorded in the evidence; they are not unconditional idiomatic or runtime acceptance. Hakka Latin retains the reviewed inherited preview/apply prefix without unreviewed orthographic normalization. Help acceptance is not transferred to crop text.

No complete-catalogue, Android rendering, glyph-shaping, accessibility-output or installed-device acceptance is claimed. The frozen initial memory-warning queue and separately accepted successor inventory are preserved; four newly translated priority values have separate qualified current-source expectations. Global localization scope is unchanged.

## Validation

- Catalogue/resource/placeholder checks pass.
- 161 focused host tests pass in normal Python and again with `python -O`.
- Exact candidate matching covers all 682 priority values and all three crop values. 104 static consumer snapshots match the base tree.
- The global `--complete` check fails with the existing 222 catalogue-gap diagnostics; only the BG/BN missing-string diagnostic contents change. Partial priority work is not whole-language completion.
- Full host aggregate, Android resource compilation, JVM/lint, native/APK and device checks were not run locally. The temporary connector snapshot is not a complete Android build checkout and has no Android SDK/adb/installed Gradle.

The exact focused command is recorded below; use the ordinary PR CI for complete build/runtime gates.

```sh
python tools/translation_catalogues.py
PYTHONPATH=tools python -m unittest -v test_bulgarian_bengali_priority_wording test_hakka_wu_crop_wording test_chinese_crop_warning test_crop_movement_translations test_crop_followon_wording test_crop_counterpart_guidance test_assembly_help_pr6 test_assembly_help_pr12 test_assembly_help_pr8 test_memory_warning_source_review test_memory_warning_successors test_sampled_memory_modality test_current_localization_contracts test_translations.TranslationCatalogueTests test_translations.AndroidResourceValidationTests test_locale_font_coverage
# Repeat the unittest command with python -O.
python tools/translation_catalogues.py --complete
```
