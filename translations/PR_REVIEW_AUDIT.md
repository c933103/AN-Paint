# Localization PR review audit

Reconstructed from GitHub on 25 September 2026. Source baseline:
`7939f1292e706bd24dfd6596a8d3d51f3b202a84`, integration PR #15.
This records review findings and concrete source evidence. A resolved thread,
outdated diff, complete catalogue, or green build is not linguistic sign-off.
Original conversation handoffs are a separate obligation from these PR reviews.

## Retrieval coverage

All inline threads (including resolved/outdated), submitted review bodies and
issue-discussion comments were read for #2–#9, #12 and #15:

| PR | Inline threads | Review bodies | Discussion records | Reviewed commit |
| --- | ---: | ---: | ---: | --- |
| [#2](https://github.com/c933103/AN-Paint/pull/2) | 0 | 0 | 2 | No code review: quota notice |
| [#3](https://github.com/c933103/AN-Paint/pull/3) | 0 | 0 | 2 | No code review: quota notice |
| [#4](https://github.com/c933103/AN-Paint/pull/4) | 2 | 1 | 1 | `1711f55e6d` |
| [#5](https://github.com/c933103/AN-Paint/pull/5) | 1 | 1 | 1 | `ec23e06b2d` |
| [#6](https://github.com/c933103/AN-Paint/pull/6) | 4 | 1 | 1 | `687885e6c4` |
| [#7](https://github.com/c933103/AN-Paint/pull/7) | 1 | 1 | 1 | `f709df3dfb` |
| [#8](https://github.com/c933103/AN-Paint/pull/8) | 3 | 1 | 1 | `6d591aa6f3` |
| [#9](https://github.com/c933103/AN-Paint/pull/9) | 2 | 1 | 1 | `80c778654d` |
| [#12](https://github.com/c933103/AN-Paint/pull/12) | 2 | 1 | 1 | `43d3e51d84` |
| [#15](https://github.com/c933103/AN-Paint/pull/15) | 0 | 0 | 0 | No submitted review at retrieval |
| Total | 15 | 7 | 11 | |

The seven review bodies identify the reviewed commits and point to their inline
findings; they do not contain additional substantive findings. All 15 inline
threads were marked resolved. The #9 pair and #12 font thread were not outdated;
the other 12 were outdated. These flags were not used as proof of a fix.

The two quota notices are [#2's notice](https://github.com/c933103/AN-Paint/pull/2#issuecomment-5771145292)
and [#3's notice](https://github.com/c933103/AN-Paint/pull/3#issuecomment-5772387941).
Their security-activity summaries are [#2](https://github.com/c933103/AN-Paint/pull/2#issuecomment-5771146066)
and [#3](https://github.com/c933103/AN-Paint/pull/3#issuecomment-5772430829);
neither establishes a completed code review. Remaining activity summaries:
[#4](https://github.com/c933103/AN-Paint/pull/4#issuecomment-5786988315),
[#5](https://github.com/c933103/AN-Paint/pull/5#issuecomment-5788419867),
[#6](https://github.com/c933103/AN-Paint/pull/6#issuecomment-5788465143),
[#7](https://github.com/c933103/AN-Paint/pull/7#issuecomment-5789547774),
[#8](https://github.com/c933103/AN-Paint/pull/8#issuecomment-5789646750),
[#9](https://github.com/c933103/AN-Paint/pull/9#issuecomment-5789699973),
[#12](https://github.com/c933103/AN-Paint/pull/12#issuecomment-5789855016).

## Individual findings and propagation

Paths below are relative to the repository; resource directories are under
`Paintroid/src/main/res`. “Baseline repaired” describes the exact finding only,
not the whole locale or conversation.

| Finding | Source evidence and cross-locale treatment | Status |
| --- | --- | --- |
| [#4 Android apostrophes](https://github.com/c933103/AN-Paint/pull/4#discussion_r4078032144) | Dutch/Swahili resources use Android escaping. `tools/translation_catalogues.py:android_string_errors` and `tools/test_translations.py` inspect all catalogues, not just those two. XML entity decoding alone does not escape Android apostrophes. | Baseline repaired; 27 translation tests pass after gallery patch. |
| [#4 Lithuanian plurals](https://github.com/c933103/AN-Paint/pull/4#discussion_r4078032149) | `values-lt/strings.xml:ui_crop_preview_images` now has `one`, `few` with `vaizdams`, and `other` with `vaizdų`. Crop placeholders retain the same arguments. Other locale plural categories and meaning require their own grammar, not Lithuanian endings copied globally. | Baseline repaired. Arabic zero/one/two count semantics separately reopened. |
| [#5 French star corruption](https://github.com/c933103/AN-Paint/pull/5#discussion_r4078788608) | French tool/help entries restore the star term; corrupted `Écanevas` is absent. Audit extends to the five-point instruction and long manual, not only the button. | Baseline repaired; additional Show all caption corruption found during renewed review. |
| [#6 Base64 prefix](https://github.com/c933103/AN-Paint/pull/6#discussion_r4078807370) | `data:image/png;base64,` is kept as syntax. `literal_token_errors` compares exact protected tokens across every default/string/plural/array catalogue. | Baseline repaired and global gate present. |
| [#6 CC BY-SA version](https://github.com/c933103/AN-Paint/pull/6#discussion_r4078807374) | `CC BY-SA 4.0` is retained in every affected POJ resource. Same global literal-token gate also covers other locales and licence identifiers. | Baseline repaired and global gate present. |
| [#6 GIF limit](https://github.com/c933103/AN-Paint/pull/6#discussion_r4078807377) | GIF limit is the single number 65,535; malformed separated numbers are rejected by `literal_token_errors`. Valid local grouping is checked semantically against 65535. | Baseline repaired and global gate present. |
| [#6 Literary Chinese assembly replacement](https://github.com/c933103/AN-Paint/pull/6#discussion_r4078807379) | `values-b+lzh+Hant/strings.xml:ui_add_up_to_20_images_with_android_s` no longer calls the operation a foreground-colour replacement. `test_literary_assembly_help_describes_image_replacement` guards that specific error. Other locale assembly instructions are compared with the undoable image-transfer behavior. | Baseline finding repaired; false Show all label and final copyright route separately reopened. |
| [#7 duplicate pt-PT](https://github.com/c933103/AN-Paint/pull/7#discussion_r4079350287) | Only `values-b+pt+PT` remains. `android_configuration` and equivalent-directory tests normalize legacy/BCP-47 aliases across every locale. | Baseline repaired and global gate present. |
| [#8 truncated main help](https://github.com/c933103/AN-Paint/pull/8#discussion_r4079390043) | Tibetan, Dzongkha and Traditional Mongolian long manuals exist with expanded instructions. Text length/paragraph count cannot establish clause equivalence. Renewed review compares the actual default instructions; stale final Help routes remain independently detectable. | Linguistic/semantic re-review reopened; do not mark complete from the resolved flag. |
| [#8 Traditional Mongolian assembly omissions](https://github.com/c933103/AN-Paint/pull/8#discussion_r4079390046) | Expanded `ui_add_up_to_20_images_with_android_s` covers operational instructions. Re-review must preserve crop reset/undo, snap preview and + placement, overlap rejection, view-only zoom, memory resize choices, and retained assembly. | Clause-by-clause review reopened with locale owner. |
| [#8 Irasutoya conditions](https://github.com/c933103/AN-Paint/pull/8#discussion_r4079390051) | The 21-item commercial threshold and collaboration caveat exist in the affected baseline catalogues. However abbreviated About captions remained in the active gallery help. `2bb96ea17` replaces existing routes in all three active gallery resources, covering 150 entries in 52 XML files. | Route repairs committed; missing retained-source sentences in bo/dz/mn-Mong `gallery_description` separately assigned. |
| [#9 stale cju expectation](https://github.com/c933103/AN-Paint/pull/9#discussion_r4079424343) | `AppLanguageTest.regionalLabelsLegacyMigrationsAndStarterChoicesUseTheirCatalogues` tests `jje` as an available locale and `cju` only as a migration alias. | Baseline repaired; original PR #9 complete workflow verified. |
| [#9 Manchu vertical UI](https://github.com/c933103/AN-Paint/pull/9#discussion_r4079424347) | `VerticalText.uiDirection` routes every `Mong` script locale vertically. Shared typography and picker handling cover Manchu as well as Mongolian. Literary Chinese and English/emoji test locales also have explicit vertical directions. `ViewportAndVerticalTextTest` covers shared behavior and emoji cluster handling. | Baseline repaired globally, not scoped to Manchu labels alone. |
| [#12 Hán-Nôm font coverage](https://github.com/c933103/AN-Paint/pull/12#discussion_r4079521091) | `LocaleTypography`, bundled Nôm subset and font inventory cover the catalogue/picker. Wu has its own needed fallback. UI-only subsets are excluded from drawing-font choices while `NativeCodecTest.everyAdvertisedBundledFontLoadsItsActualFontFile` still loads every declared font asset. | Baseline repaired; final integrated build/device workflow verified. |
| [#12 Korean regex escapes](https://github.com/c933103/AN-Paint/pull/12#discussion_r4079521096) | `tools/test_translations.py` uses actual Hangul/Han Unicode ranges for `ko-Kore-KR`. This proves both scripts occur, not that Hanja substitutions are attested or appropriate; the recovered terminology/corpus obligation remains separate. | Regex repaired; corpus/terminology evidence review reopened. |

## Reopened global gaps

`ClassicPaintActivity.menuActions("File")` opens `showAboutOptions()`, whose
caption is `ui_about_credits23`; image sources are under `ui_image_credits`.
The previous help regression inspected `values*/strings.xml` and only searched
whole manual text. It omitted default `editor34_strings.xml`, the two active
external-gallery instructions and `gallery_description`. A correct route in an
early manual paragraph also concealed a wrong final copyright paragraph.

`tools/test_localized_help.py` is a separate, PR-scope-independent regression
file. It reads all XMLs, checks the three active gallery routes in order,
checks the final copyright paragraph separately, and rejects specifically
identified Show all mistranslations. Normalization handles NFC, case, quote
style, final punctuation and word-separating hyphens/spaces; it does not invent
inflected-word equivalences. The Literary Chinese guard rejects the wrong full
phrase even though it contains the shorter correct label as a substring.

After the route patch alone, the existing 27 translation tests pass but the new
three tests report **54 failing subchecks**: three missing gallery-source
sentences, fourteen stale final copyright routes, and 37 ambiguous/wrong Show all
references. Those failures are real pending language edits, not skipped tests.
Update this paragraph after the combined language patches land and rerun them.

## Build evidence, bounded by commit

On 25 September, GitHub reports all three jobs (APK and corresponding source,
regression/lint, API 35 emulator) successful for:

- Integration `7939f1292e706bd24dfd6596a8d3d51f3b202a84`:
  [run 35939028394](https://github.com/c933103/AN-Paint/actions/runs/35939028394).
- Original PR #9 `2e0d3251223c07f71c49b09307b968f89cf9c9e1`:
  [run 35938950148](https://github.com/c933103/AN-Paint/actions/runs/35938950148).

These runs establish build/runtime checks for those snapshots. They do not
validate subsequent edits or establish authentic translation. New source is
published only after checking its exact Git tree; later CI status must be
reported under its own commit/run identity.
