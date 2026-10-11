# AN-W05-C05: Hungarian attribution terminology

## Bounded result

The 17 individually identified replacements from the [original C05 proposal](https://github.com/c933103/AN-Paint/tree/1aea91391db29d2e1359524aaf48ffff1a395d53/verification/attribution-terminology-2026-10-09) are applied to the current canonical Hungarian catalogue. Every original proposed value still matched develop `691f8870649a1d21d1441f4e3d0e795660b23e9a`, tree `040a35f40a6e8e143c6a9b2121e804f0704dd5d1`, before this change. The complete local base was checked against all 1,514 remote leaf identities. The local snapshot commit is not upstream provenance.

This is the next independent item on the [project board](https://github.com/c933103/AN-Paint/blob/docs/project-kanban-2026-10-10/docs/PROJECT_KANBAN.md): C05's C04 integration dependency is now settled. The existing inventory distinguishes it from the 12 Commons metadata reasons. M02/PR47 is separate and unchanged; this candidate is based on develop, not PR47. No other locale is corrected or certified by this item.

Production changes are exactly 17 existing `values-hu/strings.xml` entries. No new keys, Kotlin/Java behavior, locale routing, fonts, workflow, release setting, legal body, provider field or request policy changes. The button, confirmation messages, About/notice titles and their exact Help references change together. Placeholders, XML attributes, escaped newlines, licence identifiers and Irasutoya's paid-use condition remain unchanged. Already-correct C04 copy-failure and older save/size errors remain intact.

## Fresh contextual evidence and limits

- The Hungarian National Bank's [account explanation](https://www.mnb.hu/fogyasztovedelem/bankszamlak/bankszamlavalasztas-es-bankszamlanyitas/a-bankszamlak-csoportositasa) uses `jóváírás` for account crediting. This supports the financial sense; it is not an exhaustive dictionary claim.
- The Hungarian Intellectual Property Office's [2022/10 journal](https://sztnh.gov.hu/sw/static/file/202210-szemle.pdf), printed page 174 (PDF page 174), uses `forrásmegjelölés` for identifying reused audiovisual sources.
- Creative Commons' [own Hungarian BY 4.0 summary](https://creativecommons.org/licenses/by/4.0/deed.hu) describes identifying the creator, linking the licence and identifying modifications. This supports the operation's attribution domain, not an exact prescribed UI phrase.
- Current `GalleryCredits.copy`, the real gallery editor, About actions and source-provider instructions were re-read. They concern author/source/licence information, with no financial-account operation. Existing correct Hungarian failure strings already use the proposed attribution terminology.

The unchanged 17-item proposal receives a fresh bounded model contextual review, recorded individually in [dispositions.json](dispositions.json). Matching strings, catalogue compilation and runtime oracles are **not native-speaker acceptance**. HU-12 and HU-17 are retained guidance resources whose live UI reachability is not established. Naturalness across the Hungarian catalogue and the other languages remains open. The original 475-row reset register is unchanged; no row is closed here.

## Strict successor contracts

[The new scope fixture](../../tools/fixtures/hungarian_attribution_c05_scope.json) records all 17 exact before/after XML lines and both complete Hungarian file hashes. Its SHA-256 is pinned in the test helper. It is an evidence boundary, not a translation generator.

The existing C04/F01/C023 full-file historical guard first reverses **only these 17 exact Hungarian lines**, then runs its original resource reversals and unchanged historical hashes. Reverting, deleting or duplicating any one new line fails; unrelated changes also fail. The original F01 37-entry fixture and C023 one-entry fixture and their pins are unchanged.

C03 receives its separately planned exact HU-15 successor: require the complete new Help hash, reverse the one About label, recover the unchanged historical C03 after-hash, then apply the original provider-list reversal and pre-C03 hash. Every original current-text caption, provider, placeholder and quoting assertion remains. Other locales receive no successor normalization. Historical manifests, source-scope records and reports are unchanged; [preserved-source-hashes.json](preserved-source-hashes.json) records selected protected source/legal/evidence files.

Eight new host tests include 51 per-entry reversion/deletion/duplication controls, four fixture-corruption controls, seven C03 controls, complete current/base hashes, label-reference coherence and Android source coverage. They use explicit checks active in normal and optimized Python modes.

## Android coverage and text-fit acceptance

Hungarian is added to the existing gallery normal/large-text portrait, 240dp narrow and landscape control-reachability loops, preserving all former languages and assertions. Hungarian is also added to the existing real File → Help dismissal/language-change route.

New API30/API35 tests cover fixed compiled Hungarian labels; both retained guides; the actual gallery attribution editor at system font scales 1 and 2; Copy, Save, Done and reopen; exact clipboard/accepted-credit preservation including literal percent sequences and provider text; and real About → asset/open-source/translation notice routes with byte-exact legal bodies at large text.

The new dialog captures deliberately record actual `complete_fit` and `text_fit_accepted` geometry results, including failures. Behavioral JUnit success **does not accept text fit**. Any false fit result remains a layout defect requiring a separate disposition and any necessary authorized UI correction. The tests do not resize child views, reduce text size, rewrite labels or claim clipped text is accepted. New and existing captures are Robolectric NATIVE output, not installed screenshots or TalkBack testing. Both capture inspection and runtime status remain pending until CI artifacts are reviewed.

## Reproduction and current verification

Run from the repository root:

```sh
python3 tools/translation_catalogues.py
python3 -m unittest discover -s tools -p 'test_hungarian_attribution_c05.py' -v
python3 -O -m unittest discover -s tools -p 'test_hungarian_attribution_c05.py' -v
python3 -m unittest discover -s tools -p 'test_*.py' -v
./gradlew :Paintroid:testDebugUnitTest --tests org.catrobat.paintroid.local.HungarianAttributionC05Test
```

- Canonical catalogue validation: passed.
- Eight focused host tests: passed normally and with `python3 -O`.
- Complete host suite: **554 passed, zero skips**, 142.543 seconds; [all-host.log](all-host.log).
- Strict AAPT2 compilation of the changed Hungarian catalogue: passed; exact tool/output identity and limitation are in [aapt2-compile.log](aapt2-compile.log). This is not application resource linking or Kotlin compilation.
- Local Gradle/Android execution: blocked before compilation. The pinned Gradle distribution is absent and the writable-home bootstrap reports `Network is unreachable`; see [gradle-local-attempt.log](gradle-local-attempt.log). No local JVM, lint, APK or emulator pass is claimed.
- Exact-head normal current-platform CI and Code review: to be linked after verified publication. No additional full installed matrix is requested for this resource-only increment.

Keep the PR draft. Native-language, text-fit/visual, physical-device and broader localization acceptance remain separate, and no merge or release is requested by this report.
