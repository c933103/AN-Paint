# Localization integration review

This is the combined review candidate for open localization PRs #2–#9 and #12.
It is published as draft [PR #15](https://github.com/c933103/AN-Paint/pull/15).
No pull request has been merged into `develop` as part of this work.

## Scope and review disposition

| Finding or request | Repair and shared application |
| --- | --- |
| Stacked PRs did not run CI | Remove the `develop`-only pull-request base filter. Keep the existing build, regression/lint and device gates; repair branch conflicts against the updated shared base. |
| Unescaped apostrophes and literal percent text | Repair Dutch and Swahili resources; validate Android quoting in every catalogue and mark static literal percent text as non-format text. Escape literal percent signs in strings with runtime arguments. Check all catalogues and compile the whole resource tree with AAPT2. |
| Duplicate Portuguese resource configuration | Keep one canonical `values-b+pt+PT` catalogue. Reject equivalent Android resource qualifiers in the validator. |
| Lithuanian few plural omitted | Supply `few`, preserve the distinct `other` form and test the quantity data. |
| French Star corrupted by substitution | Restore Étoile and matching shape/help references. Check related semantic substitutions in other locales. |
| Base64 prefix, licence identifier and GIF size corrupted | Preserve `data:image/png;base64,`, `CC BY-SA 4.0` and the intact 65535 limit; validate protected literals across translated catalogues. Localized numeric grouping remains allowed. |
| Truncated help and incorrect operation meaning | Restore Tibetan, Dzongkha and Mongolian instructions; correct image replacement versus foreground colour, view zoom versus output dimensions, and other omissions in the locale passes. |
| Stale Jeju identifier and locale assertions | Keep `jje` as the current tag and `cju` only as a migration alias. Do not require a legitimate shared/borrowed caption to differ from English. |
| Manchu and Literary Chinese vertical UI | Use script-aware layout and typefaces across editor controls, menus, dialogs, picker labels and app-injected gallery controls. Mongolian/Manchu columns advance left to right; Literary Chinese advances right to left. |
| Vertical text test cases | Add explicit English vertical (`en-XV`) and emoji vertical (`qaa-Zsye-XV`) catalogues, including upright emoji sequences and script-appropriate labels. Keep subdivision-flag tag sequences together when measuring and wrapping in either column direction. |
| Hán-Nôm unsupported by old platform fonts | Bundle licensed, reproducible UI subsets covering the actual catalogue, with exact glyph-coverage and inventory-hash checks. Keep user-selected drawing fonts independent from locale UI fonts. Apply the same review to Wu's supplementary character. |
| Taiwan Hakka conventions | Use `hak-Hant-TW` and `hak-Latn-TW`, with migration from old tags and no duplicate unregionalized catalogues. |
| Attribution lost when inserting gallery images | Keep original source/creator/licence text with the document and floating selection. Preserve it through selection commit/cancel, clipboard, undo/redo, draft and recovery state; reset it for a new/opened document. |
| Edited gallery credits lost after rotation | Restore the pending credit-only activity result after recreation. Leaving an untouched gallery still returns no edit. |
| Copyable export attribution | Save as / Export as show a collapsed image-credit section with selectable text and Copy all. Attribution text keeps its original language when the application language changes. |
| Obsolete Help-menu instructions | Use actual localized File → About, licences & credits → Image credits routes. Check documented labels against the active resources, allowing casing and terminal punctuation differences. |

The original PRs receive scoped catalogue and build repairs as well. Shared
application behavior is reviewed together here to avoid restricting it to the
language of the branch that first exposed the defect. The branch publication
process compares the complete intended and remote Git trees, including obsolete
file deletion, before triggering CI.

The Nôm catalogue font is a UI subset, so it is no longer exposed as a drawing
font choice. Default Nôm text retains its fallback coverage; explicitly selected
drawing fonts retain their own faces. The device check loads and hashes every
font asset, including the UI-only Nôm and Wu subsets, and derives drawing choices
from inventory roles. Complete Mongolian remains selectable.

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
- [Manchu colour and typography audit](../translations/MANCHU_COLOUR_TYPOGRAPHY_AUDIT.md)

Ainu and Manchu required additional completion after the initial integration.
Their starting catalogues contained English-heavy passages and incorrect
dictionary-word substitutions. The follow-up replaces those passages with
source-assisted descriptions of the actual controls, memory behavior, image
formats, credits and full help instructions. Both Ainu scripts are reviewed
together; Manchu uses its own vocabulary and clause structure. Retained format
names and external button labels are distinguished from untranslated prose.
The audits record evidence and terminology choices. This completes known
translation gaps without claiming independent fluent-speaker certification.

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
The repaired snapshot `d861555d1c8cfe453a7abf1cf34e5efc2dcfdeb6` passed all 305
Robolectric tests and lint, and produced 150 UI previews in
[run 35935361997](https://github.com/c933103/AN-Paint/actions/runs/35935361997).
All 11 editor device tests passed. Its sole failure among 71 completed native
tests was the font-choice count, which exposed the UI-subset issue repaired
above. The previews were inspected for Manchu, Mongolian, Literary Chinese,
English vertical and emoji vertical controls and save dialogs.

The font-role and gallery-recreation repairs were first published as
`ee6d2d5e258d9424f8987bb14b11517953019843`,
[run 35937264365](https://github.com/c933103/AN-Paint/actions/runs/35937264365).
The matching local snapshot passed 97 host tests and strict AAPT2 compilation.
That complete Android workflow passed: 307 unit tests and lint, production/test
APK compilation, 71 native checks and 11 editor device checks.
Later translation completion and emoji-tag changes require their own exact-head
Android result; the current result is linked in PR #15. An APK build or an
earlier passing run does not establish full validation of a later commit.

The final 24 September completion pass passes all 99 host tests and strict
whole-resource AAPT2 compilation. This includes the two additional percent
regressions, both completed Ainu scripts, the combined Manchu repairs, and all
other catalogues. The final independent Ainu correction check confirmed the
reported findings were addressed in the actual integrated files. The emoji
cluster implementation also passed focused Kotlin compilation and execution;
its Android measurement/wrapping test is included in the final CI source.

Local Maven dependency retrieval is restricted in this environment, so a full
local Gradle pass is not claimed. Focused typography Kotlin compilation against
`android.jar` and production emoji-clustering checks passed; full Gradle, lint, Robolectric and device validation belong
to the published CI runs. No signing material was added to the repository.
