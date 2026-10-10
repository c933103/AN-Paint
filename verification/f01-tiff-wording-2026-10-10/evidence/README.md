# F01 bounded TIFF description candidate

10 October 2026. Frozen for independent review; no source/evidence publication or CI dispatch has occurred at this stage.

## Result and scope

Exactly eleven canonical `formats22_tiff_description` values replace the unqualified size assertion with English **may reduce** / pt-BR **pode reduzir**. The English default, seven regional/001 catalogues, vertical English and emoji layout fixtures, and pt-BR are included. The emoji prefix and all remaining text in those XML files are byte-for-byte preserved. No encoder, application code, existing test, resource routing, generation policy, imported provenance or other catalogue changes occur. Two focused test files are added.

Base commit: `80c14372b0504bc44f9f2809ad477247fdc8100b`; base tree: `d9858229f98068bef9c6194c90d77610c5ecceec`.

Candidate tree: `89e43725c5b7c2f01827cfa06510c21f5268314c`.

[Candidate manifest](candidate-manifest.json) records all thirteen changed/added blobs and SHA-256 identities. All 1,290 base blobs were reconstructed and verified before editing. The final candidate has 1,279 unchanged base files, eleven single-resource edits, two added tests and no removals. [Exact patch](candidate.patch).

## Wording

English: Saves one RGB page. Compression may reduce file size without changing pixels; turn it off for uncompressed TIFF.

pt-BR: Salva uma página RGB. A compressão pode reduzir o tamanho do arquivo sem alterar os pixels; desative-a para criar um TIFF sem compressão.

The source describes the benefit as possible, while retaining lossless pixel semantics and unchecking guidance. This does not promise a maximum whole-TIFF size, change the encoder, or select the smaller of two encodings.

## Full individual language scope

[All-language inventory](all-language-inventory.json) retains exact original/current strings, paths, line numbers, base blobs, classifications, confidence/uncertainty and individual open dispositions for all 60 explicit definitions. Its 81 separate fallback records retain the missing-key limitations for each other offered locale.

At the base, 37 descriptions have high-confidence unqualified size assertions, 12 have probable unqualified/reductive readings, seven already have capability wording, and four are linguistically uncertain. No confidently interpreted string has no size claim. These categories concern only this clause; they are model linguistic triage rather than native-speaker or full-language acceptance.

Eleven of the 37 high-confidence cases receive this candidate. The other 26 clear cases and all twelve probable and four uncertain cases remain individually open and unchanged. The seven already-qualified entries are unchanged; this is not acceptance of their complete language strings. Hakka/Hokkien/Wu 會/voi/ē modal-versus-generic-result force is explicitly qualified. Ainu, Okinawan and Chữ Nôm readings are not forced into a definitive category.

The 81 missing-key offered locales have no same-language alternative defining this key in source. Corrected English fallback is therefore source-predicted; runtime routing for those 81 locales has not been proved. No new translations are created. Legacy generic es and ko catalogues also lack the key but are not separate offered choices.

Every live XML is canonical, including layout fixtures. There is no regeneration step from historical JSON. Existing language/script/region routing, Crowdin mappings and paired-script policy remain intact. See [TRANSLATING.md](https://github.com/c933103/AN-Paint/blob/80c14372b0504bc44f9f2809ad477247fdc8100b/TRANSLATING.md#L7-L52).

## Primary source basis

- [SaveOptionsDialog](https://github.com/c933103/AN-Paint/blob/80c14372b0504bc44f9f2809ad477247fdc8100b/Paintroid/src/main/java/org/catrobat/paintroid/classic/SaveOptionsDialog.kt#L63-L105) chooses this resource for TIFF regardless of checkbox state and forwards the selected flag in the request.
- [Encoder](https://github.com/c933103/AN-Paint/blob/80c14372b0504bc44f9f2809ad477247fdc8100b/Paintroid/src/main/cpp/tiff_bridge.cpp#L480-L518) writes one chosen output, with Deflate versus no compression, horizontal prediction/quality 6 when compressed, and the same opaque RGB samples. Its buffer commentary anticipates growth; it does not compare two outputs and choose the smaller.
- [RFC1951 section 1.1](https://www.rfc-editor.org/rfc/rfc1951.html#section-1.1) explains possible lossless/Deflate expansion. [zlib technical details](https://zlib.net/zlib_tech.html) and [deflateBound documentation](https://zlib.net/manual.html) explain expansion bounds. No stream-level bound is asserted as a whole-TIFF bound: strips, metadata and directories have their own overhead.
- [British Council possibility grammar](https://learnenglish.britishcouncil.org/free-resources/grammar/english-grammar-reference/probability) supports may as possibility rather than certainty. [Priberam poder](https://dicionario.priberam.org/poder) records infinitive-complement possibility use. These support the model's narrow modal choice, not native-speaker approval.
- [AppLanguage](https://github.com/c933103/AN-Paint/blob/80c14372b0504bc44f9f2809ad477247fdc8100b/Paintroid/src/main/java/org/catrobat/paintroid/classic/AppLanguage.kt#L60-L85) uses the selected locale, and [UiText](https://github.com/c933103/AN-Paint/blob/80c14372b0504bc44f9f2809ad477247fdc8100b/Paintroid/src/main/java/org/catrobat/paintroid/classic/UiText.kt#L13-L27) resolves Android resources. [Android resource-resolution guidance](https://developer.android.com/guide/topics/resources/multilingual-support) is consistent with the source fallback inference.

## Validation performed and limits

[Validation summary](validation-summary.json): structural validator passed; 32 translation checks and six focused wording checks passed; the complete 372-test host suite passed with no skips. Fifteen negative controls reverted each of the eleven corrected clauses individually, removed the emoji, corrupted pixel/unchecked semantics, or inserted a spurious Welsh translation; all were rejected by assertions, and every file was restored. The full host log includes deliberately rejected mocked instrumentation fixtures; it is not an Android run.

Seven new API33 Robolectric methods target the production SaveOptionsDialog and actual resources: every English variant, pt-BR, Welsh fallback, both layout fixtures, checked/unchecked choices, toggling, DIB/TIFF switching and both cancellation paths. Positive callbacks assert the actual TIFF request, including its independent lossless flag being false and the selected tiffCompressed flag. They do not invoke an encoder or claim rendered pixel/layout accessibility acceptance.

The exact local Gradle attempt at pre-review tree `f0c9e32a6d8e3b69d0d55b2c1972433cd05533d9` failed before any task or Kotlin compiler: the uncached 8.13 wrapper download reported **Network is unreachable**. Thus all seven new methods and existing ExportFormatDialogTest remain uncompiled/unrun here. No APK build, Android lint, installed/emulator/physical-device test or screenshots are claimed. Candidate-specific execution and applicable rendered checks remain required after review/publication.

## Nonduplication and remaining work

The source-scope snapshot records reads of both default/pt-BR entries at all ten open PR heads. Every default remained unqualified; nine pt-BR entries remained unchanged and PR9 lacked the key. None implemented this pair of modal corrections. This does not prove absence of unpublished work.

A01 is separate and is not included in this develop-based tree. F01 remains open for the other 42 explicit language cases needing correction or clarification, and for applicable validation. The seven capability-qualified entries are retained without broader acceptance. No other 81-locale completion task is created. Partially recovered original scope and remaining original-thread/term-specific reconciliation continue to apply.

The authoritative register remains 475 total / 3 structural completed / 472 pending. This packet closes no parent row or full-language obligation. Source and evidence are to be published durably in AN-Paint only after independent review and authorized publication, preserving repository visibility and excluding secrets/unrelated private data.

## Independent review correction before publication

The first source/API-contract review identified a test-design blocker: `CompoundButton.performClick()` toggles the checkbox, but its return value reports whether an `OnClickListener` ran. This TIFF checkbox has none, so asserting a true return was invalid. The test now performs the click and retains its explicit checked-state, description and callback assertions. No production or resource byte changed. This was established by source/API-contract review, not reproduced Android execution.

References: [Android CompoundButton contract](https://developer.android.com/reference/android/widget/CompoundButton#performClick()), [pinned Robolectric4.14.1 ShadowCompoundButton](https://github.com/robolectric/robolectric/blob/robolectric-4.14.1/shadows/framework/src/main/java/org/robolectric/shadows/ShadowCompoundButton.java), [ShadowView delegation](https://github.com/robolectric/robolectric/blob/robolectric-4.14.1/shadows/framework/src/main/java/org/robolectric/shadows/ShadowView.java#L269-L275).

Prior manifests and patches are retained as before-checkbox-review snapshots. Revised eleven-entry tree: `89e43725c5b7c2f01827cfa06510c21f5268314c`; revised combined tree: `bde13ca4bbd9a45198ab4da9cadd85d900aaa594`. The resource-only26 expansion remains `b81391fb46dd9ee1bdb86c3faf693462e1316232`. Earlier host results apply to unchanged Python/resource content; the primary reviewer is validating the revised combined source. Kotlin compilation remains blocked before execution.
