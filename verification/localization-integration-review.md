# Localization integration review

This is the combined review candidate for open localization PRs #2–#9 and #12.
It is published as draft [PR #15](https://github.com/c933103/AN-Paint/pull/15).
No pull request has been merged into `develop` as part of this work.

## Scope and review disposition

| Finding or request | Repair and shared application |
| --- | --- |
| Stacked PRs did not run CI | Remove the `develop`-only pull-request base filter. Keep the existing build, regression/lint and device gates; repair branch conflicts against the updated shared base. |
| Unescaped apostrophes and literal percent text | Repair Dutch and Swahili resources; validate Android quoting in every catalogue and mark literal percent strings as non-format text throughout the resources. Compile the whole resource tree with AAPT2. |
| Duplicate Portuguese resource configuration | Keep one canonical `values-b+pt+PT` catalogue. Reject equivalent Android resource qualifiers in the validator. |
| Lithuanian few plural omitted | Supply `few`, preserve the distinct `other` form and test the quantity data. |
| French Star corrupted by substitution | Restore Étoile and matching shape/help references. Check related semantic substitutions in other locales. |
| Base64 prefix, licence identifier and GIF size corrupted | Preserve `data:image/png;base64,`, `CC BY-SA 4.0` and the intact 65535 limit; validate protected literals across translated catalogues. Localized numeric grouping remains allowed. |
| Truncated help and incorrect operation meaning | Restore Tibetan, Dzongkha and Mongolian instructions; correct image replacement versus foreground colour, view zoom versus output dimensions, and other omissions in the locale passes. |
| Stale Jeju identifier and locale assertions | Keep `jje` as the current tag and `cju` only as a migration alias. Do not require a legitimate shared/borrowed caption to differ from English. |
| Manchu and Literary Chinese vertical UI | Use script-aware layout and typefaces across editor controls, menus, dialogs, picker labels and app-injected gallery controls. Mongolian/Manchu columns advance left to right; Literary Chinese advances right to left. |
| Vertical text test cases | Add explicit English vertical (`en-XV`) and emoji vertical (`qaa-Zsye-XV`) catalogues, including upright emoji sequences and script-appropriate labels. |
| Hán-Nôm unsupported by old platform fonts | Bundle licensed, reproducible UI subsets covering the actual catalogue, with exact glyph-coverage and inventory-hash checks. Keep user-selected drawing fonts independent from locale UI fonts. Apply the same review to Wu's supplementary character. |
| Taiwan Hakka conventions | Use `hak-Hant-TW` and `hak-Latn-TW`, with migration from old tags and no duplicate unregionalized catalogues. |
| Attribution lost when inserting gallery images | Keep original source/creator/licence text with the document and floating selection. Preserve it through selection commit/cancel, clipboard, undo/redo, draft and recovery state; reset it for a new/opened document. |
| Copyable export attribution | Save as / Export as show a collapsed image-credit section with selectable text and Copy all. Attribution text keeps its original language when the application language changes. |
| Obsolete Help-menu instructions | Use actual localized File → About, licences & credits → Image credits routes. Check documented labels against the active resources, allowing casing and terminal punctuation differences. |

The original PRs receive scoped catalogue and build repairs as well. Shared
application behavior is reviewed together here to avoid restricting it to the
language of the branch that first exposed the defect. The branch publication
process compares the complete intended and remote Git trees, including obsolete
file deletion, before triggering CI.

## Language review evidence

Full key and placeholder coverage does **not** certify linguistic correctness.
Substantive edits include an Indonesian rewrite distinct from Malay, Brazilian
Portuguese terminology, Cantonese control references/readings, Sinitic compound
and pronunciation corrections, Korean Hanja substring errors, and authored
Jeju/Okinawan and Tibetan/Dzongkha/Mongolian help.

Detailed provenance and limits are recorded in:

- [Mainstream source audit](../translations/MAINSTREAM_SOURCE_AUDIT.md)
- [Sinitic catalogue audit](localization-sinitic-audit.md)
- [Ainu semantic audit](../translations/AINU_SEMANTIC_AUDIT.md)
- [Manchu semantic audit](../translations/MANCHU_SEMANTIC_AUDIT.md)

Ainu and Manchu require particular care. Their starting catalogues contained
English-heavy passages and incorrect dictionary-word substitutions. This work
repairs supported meanings and active instructions; it must not be presented as
independent fluent-speaker certification. Any remaining language limitations in
their audits remain merge-review items, even when all resources compile.

## Verification

Run the host regression suite:

```sh
python3 -m unittest discover -s tools -p 'test_*.py'
```

Compile all application resources with SDK 35 AAPT2, without `--legacy`:

```sh
aapt2 compile --dir Paintroid/src/main/res -o /tmp/an-paint-resources.zip
```

The first integrated application snapshot (`e52669d79868016931094adb16139ebe2bcfa4a8`)
passed 96 host checks and strict resource compilation, and its universal APK
build succeeded in [CI run 35933704428](https://github.com/c933103/AN-Paint/actions/runs/35933704428).
That run exposed four test failures caused by one real null-tag crash in the
shared font installer. The source now handles untagged controls safely, without
weakening the tests, and the same fix is backported to the original Nôm PR.
Later language, help-route and font-coverage checks bring the host suite to
97 passing tests; strict resource compilation also passes. Full Android
validation of the repaired source is reported by its own exact-head run.
Do not infer a full green CI result from an APK build or an earlier commit.

Local Maven dependency retrieval is restricted in this environment, so a full
local Gradle pass is not claimed. Focused typography Kotlin compilation against
`android.jar` passed; full Gradle, lint, Robolectric and device validation belong
to the published CI runs. No signing material was added to the repository.
