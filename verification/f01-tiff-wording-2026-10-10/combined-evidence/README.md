# F01 combined candidate: 37 bounded TIFF wording corrections

10 October 2026. Frozen for independent review, without publication or CI dispatch at this stage.

## Exact source

- Develop base commit: `80c14372b0504bc44f9f2809ad477247fdc8100b`; tree `d9858229f98068bef9c6194c90d77610c5ecceec`.
- Preserved eleven-entry candidate: `89e43725c5b7c2f01827cfa06510c21f5268314c`.
- Isolated 26-resource expansion: `b81391fb46dd9ee1bdb86c3faf693462e1316232`.
- Combined tree: **`bde13ca4bbd9a45198ab4da9cadd85d900aaa594`**.

[Manifest](candidate-manifest.json) and [patch](candidate.patch) prove the exact union: 37 single-resource modal corrections, four new focused test files, 1,253 unchanged base files, 1,294 total files, no removals. All application/encoder code, existing tests, policies, routing and other resource bytes are unchanged. A01 is separate and is not included in this develop-based candidate.

The original eleven-entry packet remains a historical, independently reviewable stage. The additional 26 original/proposal pairs, replacements, confidence, reasons and primary-language sources are recorded in the separately preserved linguistic proposal map. Applying that exact individually reviewed map is not regeneration from historical translation JSON.

## Complete scope and unresolved cases

[The full individual inventory](all-language-inventory.json) records every one of 60 explicit descriptions and 81 missing-key offered locales. At the base, 49 strings were unqualified/reductive (37 high-confidence, twelve probable), seven had capability wording and four were linguistically uncertain. The combined candidate qualifies those 37 clear entries. High confidence in identifying an unqualified clause does not imply identical confidence in every replacement: the additional reviewer records Korean regional, Swahili/Tagalog and primary-source limits per entry.

Twelve probable cases remain unchanged/open: bo, ceb, dz, hak-Hant-TW, hak-Latn-TW, jje, mn-Cyrl-MN, mn-Mong, mnc-Mong, nan-Hant-TW, nan-Latn-TW, wuu-Hans.

Four uncertain cases remain unchanged/open: ain-Kana, ain-Latn, ryu, vi-Hani. In particular, no neighboring-language text is used as a mechanical replacement for these cases.

Seven already-capability-qualified entries remain unchanged: ja, lzh-Hant, yue-Hant, yue-Latn, zh-CN, zh-HK, zh-TW. This is a narrow no-edit disposition, not acceptance of their complete translations.

The 81 offered missing-key locales remain unchanged. No same-language source alternative defines the key; default-English fallback is source-predicted, not proved separately at runtime for those 81 locales. The candidate adds a Welsh execution test, but it has not run locally. No new translation or other 81-locale completion is created.

All live XML catalogues, including English and emoji layout fixtures, remain canonical. The emoji prefix, exact region/script qualifiers, Korean Hanja, pixel-preservation clauses and unchecked/uncompressed instructions are preserved. No Crowdin, imported provenance or generator changes occur.

## Source and linguistic basis

The [encoder](https://github.com/c933103/AN-Paint/blob/80c14372b0504bc44f9f2809ad477247fdc8100b/Paintroid/src/main/cpp/tiff_bridge.cpp#L480-L518) writes the selected Deflate or uncompressed output; it does not compare outputs and choose the smaller. It preserves opaque RGB samples and anticipates possible Deflate growth. [RFC1951 §1.1](https://www.rfc-editor.org/rfc/rfc1951.html#section-1.1) and [zlib's expansion/bounds documentation](https://zlib.net/zlib_tech.html) support qualifying the size outcome. No stream-level percentage is claimed as a whole-TIFF bound.

Default English and its explicit copies use **may reduce**; pt-BR uses **pode reduzir**. The additional exact modal proposals are independently model-reviewed and range between possibility and capability. They do not claim that outputs always shrink or explicitly warn about every possible larger output. Sources support only the construction or usage cited; none supplies native-speaker or whole-locale approval. Korean source support is standard South Korean usage, not separate DPRK attestation. Existing terms outside the modal clause remain outside this narrow review.

## Test coverage and current limits

Author checks on the combined tree: the structural validator, 32 translation tests and eight focused wording tests passed. The earlier eleven-entry source passed all 372 then-present host tests and fifteen negative controls. The primary independent reviewer passed all **374 host tests with no skips** on revised tree `bde13ca4bbd9a45198ab4da9cadd85d900aaa594`, and independently rejected all **41 negative controls** (the original fifteen plus twenty-six per-locale reversions) by assertions, with positive eight-test runs before and after. See [final host log](independent-final-host.log) and [final negative controls](independent-final-negative-controls.json).

Nine new API33 Robolectric methods across two classes use actual resources and SaveOptionsDialog. They cover the English variants, pt-BR, vertical/emoji fixtures, Welsh fallback and all 26 additional locale descriptions, with checked/unchecked selection, positive callback flags, toggling, format switches and cancellation. They deliberately do not invoke an encoder. Exact expected strings are independent reviewed test oracles rather than being read back from resources.

The exact combined Gradle attempt at pre-review tree `40a4df55453208f46cf9c3188e717c07e75882a4`, selecting both new classes and existing ExportFormatDialogTest, failed while bootstrapping uncached Gradle8.13: **Network is unreachable**, before any task or Kotlin compiler. All nine new methods remain uncompiled/unrun locally. No local APK, lint, Android/emulator/physical-device, screenshot, rendering/accessibility or size-measurement pass is claimed. Candidate-specific CI and applicable rendered checks remain required after review/publication.

## Status

Full F01 remains pending: the twelve probable/four uncertain cases and applicable candidate/runtime/language requirements are unresolved. The authoritative reset counts remain **475 total / 3 structural completed / 472 pending**; original scope is only partially recovered and remaining original-thread/term history reconciliation persists. No parent row is closed. Both source stages and this combined packet are to be retained in AN-Paint when publication is authorized after independent review.

## Independent review correction before publication

The first source/API-contract review identified a test-design blocker: `CompoundButton.performClick()` toggles the checkbox, but its return value reports whether an `OnClickListener` ran. This TIFF checkbox has none, so asserting a true return was invalid. The test now performs the click and retains its explicit checked-state, description and callback assertions. No production or resource byte changed. This was established by source/API-contract review, not reproduced Android execution.

References: [Android CompoundButton contract](https://developer.android.com/reference/android/widget/CompoundButton#performClick()), [pinned Robolectric4.14.1 ShadowCompoundButton](https://github.com/robolectric/robolectric/blob/robolectric-4.14.1/shadows/framework/src/main/java/org/robolectric/shadows/ShadowCompoundButton.java), [ShadowView delegation](https://github.com/robolectric/robolectric/blob/robolectric-4.14.1/shadows/framework/src/main/java/org/robolectric/shadows/ShadowView.java#L269-L275).

Prior manifests and patches are retained as before-checkbox-review snapshots. Revised eleven-entry tree: `89e43725c5b7c2f01827cfa06510c21f5268314c`; revised combined tree: `bde13ca4bbd9a45198ab4da9cadd85d900aaa594`. The resource-only26 expansion remains `b81391fb46dd9ee1bdb86c3faf693462e1316232`. Earlier host results apply to unchanged Python/resource content; the primary reviewer accepted the revised combined source after the 374-test and 41-negative-control checks above. Kotlin compilation remains blocked before execution.
