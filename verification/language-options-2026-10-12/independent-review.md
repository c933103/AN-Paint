# Independent source review: six language options

Review date: 12 October 2026. Scope: the bounded Hausa (`ha`), Igbo (`ig`), Lingala (`ln`), Sundanese (`su`), Yoruba (`yo`) and Zulu (`zu`) option addition against the supplied exact-develop `4231edaac45d89c52f51e2b77d0f94a1176ad88c` baseline, represented locally by the reconstructed baseline commit in the adjacent SHA-256 manifest.

## Result

No remaining blocking defect found in the reviewed source patch. This result is a focused source/host review, not Android runtime acceptance, translation completion, linguistic acceptance, or permission to merge. Publication, the author’s full host aggregate, Android compilation/runtime, and installed-device evidence have separate statuses.

- The picker and Android locale configuration contain the same 146 unique choices. Removing only the six additions reproduces the original 140 choices and order exactly.
- The six tags have the expected exact canonical Android catalogues. All six catalogues contain zero translated strings and zero plurals. Their missing 695 strings and one plural each remain genuine default-English fallback; completeness checks continue to reject them.
- Names match the pinned MediaWiki autonym source, independently fetched through GitHub: Hausa, Igbo, lingála, Sunda, Yorùbá and isiZulu. `Lingála` is explicitly documented menu capitalization. [Pinned source](https://github.com/wikimedia/mediawiki/blob/eb2c0acaeeb2135c7a6e2952b536f0deb3343ba2/includes/Languages/Data/Names.php).
- All old picker labels, aliases and alias targets remain unchanged, as do all historical metadata rows. The metadata file retains its pre-existing Hakka aliases and exclusion of the two test modes; it is not substituted for live XML inventory authority.
- The four historical disposition manifests are byte-identical to the baseline and their new SHA-256 pins agree with that baseline. Current fallback checks explicitly compose the old 81 fallback choices with the six new choices, while retaining the 59-locale exact-message oracles. No historical oracle waiver was introduced.
- The exact-script generator, Korean private resource-routing variant, and script-specific production branches are unchanged. Existing script-routing, picker, gallery, numeric-input and tooltip assertions remain in place.
- The new AppLanguage API30/API35 test checks exact selected identity, wrapped configuration, process default locale, displayed autonym, representative English strings, the fallback notice, and platform-side switching on API35. It has been source-reviewed, not executed on Android here.
- Documentation and added metadata clearly record untranslated/not-started status and link the outstanding [translation tracker PR #56](https://github.com/c933103/AN-Paint/pull/56). The branch’s option additions do not establish that they are merged, released, translated or installed-device verified.

## Independent checks

Final combined focused run: **123 tests passed**, `Ran 123 tests in 6.212s`, after the author’s final stale-name cleanup. Exact output is retained in `independent-focused-host.log`.

```sh
PYTHONPATH=tools python3 -m unittest \
  test_translations test_language_option_additions \
  test_commons_copy_credit_errors test_commons_gallery_contract \
  test_commons_import_change_translations test_commons_metadata_m03 \
  test_commons_metadata_m03_font test_exact_script_generation \
  test_exact_script_resource_routing test_gallery_back_direction \
  test_locale_number_input test_locale_tooltips test_help_commons_provider \
  test_picker_fallback_notice_pr6 test_picker_fallback_notice_pr12
git diff --check
```

Canonical XML validation returned zero structural errors. `git diff --check` passed. This combined run is separate from, and does not claim success for, the author’s full host aggregate.

Five independent negative controls were performed on isolated temporary copies, never on the author’s source tree. All were rejected by the intended checks:

1. Remove the Hausa picker tag: identity/inventory test fails.
2. Replace the Hausa label with an incorrect autonym: identity test fails.
3. Add copied English `ui_menu_file=File` to the empty Hausa catalogue: truthful-untranslated catalogue test fails.
4. Append whitespace to the historical copy-credit disposition evidence: byte-integrity test fails.
5. Add legacy `values-ha/strings.xml` alongside `values-b+ha/strings.xml`: duplicate-resource-configuration validation fails.

An initial new-test failure was found during review: comparing all historical metadata tags directly to live XML incorrectly required old Hakka aliases to be current canonical tags. The author corrected the new check to validate the six added metadata identities/status while retaining XML as live inventory authority. The final 123-test run includes that correction. The stale `other81` Kotlin method name was also corrected without changing its assertions.

## Limits and remaining evidence

No Android build, AAPT/resource merge, Robolectric execution, emulator test or installed-device check was run by this review. `ANDROID_HOME` and `ANDROID_SDK_ROOT` are unset, and the checked standard SDK locations are absent. The environment’s Java is OpenJDK 21; this is not the project’s verified JDK17/Android SDK build setup. Exact-source CI compilation and runtime results remain pending/separate, and must be reported as such.

The adjacent `independent-review-source-sha256.json` identifies every reviewed changed/new source, data, test and documentation file. Evidence files in this receipt directory are excluded from that manifest to avoid self-reference. No production source was edited by the reviewer; only these review receipts were written after author coordination.
