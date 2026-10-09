# C05 refinement and explicit successor contract

Status: planning and in-memory proof only. Application resources, repository tests and historical C03 files remain unchanged.

## HU-16 refinement

The proposal no longer uses the generic `Catrobat/AGPL-adatokat`. Its replacement final sentence is:

> Ez a mód ugyanazokat a Catrobat/AGPL-re és a felhasznált elemekre vonatkozó forrásmegjelöléseket használja, amelyek a fő szerkesztő «Fájl > Névjegy, licencek és forrásmegjelölések» paneljén szerepelnek.

It explicitly retains attribution information relating to Catrobat/AGPL and the assets, together with the exact renamed About panel. It does not reduce the concept to unspecified data, change licensing terms or rewrite any other assembly instructions. The 17 subitem IDs remain unchanged in `proposal.json`.

## Existing contract that will intentionally fail

`tools/test_help_commons_provider.py::test_exact_caption_added_once_and_all_surrounding_help_preserved` currently asserts the complete decoded `ui_help23` after-hash and reverses only C03's Commons insertion to recover its before-hash. C05-HU-15 changes one About-label reference outside that insertion. Therefore retaining the old test unchanged would correctly fail its first complete after-hash assertion for Hungarian.

The historical Hungarian endpoints are:

- Pre-C03: `d8f63f0fb9232fdf54d327d9181439b2aca889ad4e46a7e68f32f15c24be4e73`
- Post-C03/current analysis base: `7e3b7c773ed71d7aba0c169cda439b307b65398eda49ea7da6241be6b3c45f76`
- Proposed post-C05: `7497f8acf98165ce939d1e7be21806431db43ca8bd5c8416416532c85b82b688`

Do not rewrite C03's `translations.json`, `source-scope.json`, review reports, or historical test outputs. Their before/after claims refer to their original snapshot. `historical-c03-file-hashes.json` records their present bytes so this preservation is verifiable.

## Planned strict successor mechanism

1. Add a separate C05 successor manifest for exactly locale `hu`, resource `ui_help23`, subitem `AN-W05-C05-HU-15`, with the exact old/new About phrase, occurrence count 1, old post-C03 hash and new post-C05 hash. The review-only draft is `help-successor-proposal.json`.
2. The test must assert the successor map has exactly that one locale/key; no generalized allowlist, skip or wildcard normalization is allowed. Its old hash must equal the unchanged C03 row's after-hash. Pin the unchanged historical C03 manifest SHA-256 `8bd7faf4ec72843827d0bc5e4effd95bc72a782a69f5f8f4323cc4c8cec3f74a` in the successor linkage.
3. For Hungarian, first require the complete CURRENT help to match the new C05 hash. Require exactly one new About phrase and no old one. Reverse only that exact new phrase once, reconstructing the historical C03 after-text; require both linked old hashes to match it.
4. Run every original C03 assertion against the appropriate text: its after-hash and provider-list reversal use the reconstructed C03 text; the Commons caption, provider passage, after-context, quoting/format and provider counts also remain checked against the real current text. Its before-hash still proves the original Commons change touched nothing else.
5. For the default and the other 58 scoped catalogues, run the original identity/hash/reversal assertions directly, unchanged. No other locale receives a successor exemption.
6. Add negative cases: an unrelated Hungarian opening or trailing-space change; missing Commons caption; changed provider wording; reverting or duplicating the attribution correction; and an unrelated non-Hungarian change. All must fail. Do not allow both old and new whole hashes as success after C05 is applied.

This is an explicit two-transition chain, not a weakened preservation test: current C05 → exact historical C03 → exact pre-C03.

## Proof performed without applying the patch

`help-successor-design-check.py` uses the proposed text in memory for Hungarian and the unchanged canonical strings for the other entries. It exercises all existing C03 content assertions plus the successor reversal.

- 60/60 default+scoped positive cases passed.
- All seven enumerated negative mutations were rejected.
- Original host C03 tests: 6 passed on the unchanged base.
- Existing localized Help route tests: 8 passed on the unchanged base.
- These are planning/proof results, not evidence that repository tests have been edited or that Android runtime has passed. See `help-successor-design-check.json`.

## Other impacted tests and boundaries

- `tools/test_localized_help.py` resolves About/Image credits captions from the current canonical catalogue. Its active Gallery paths and final manual paragraph checks should stay unchanged and pass because the label and every literal path reference move together.
- The Hungarian clauses in `test_assembly_dimensions_help_pr4.py`, `test_assembly_memory_help_pr4.py` and `test_save_export_help_pr4.py` describe dimensions, memory and Save/Export state. C05 changes none of those paragraphs/anchors. Keep these tests unmodified and rerun them.
- `CommonsHelpProviderTranslationTest.kt` does not freeze a whole Hungarian help hash. Its 59-resource caption check should need no expectation change; keep its 81-locale fallback assertions and representative punctuation checks intact. Adding `hu` to its real File → Help dismissal/language-change route loop provides direct successor coverage without changing expectations for any existing locale.
- Add the promised Hungarian narrow/large-text gallery and attribution-editor coverage separately. Source-attribution fields and clipboard content behavior must remain unchanged; longer title/button labels are the concrete runtime risk.
- C04's new strings and contract tests remain untouched. Once its base is settled, re-read the candidate base and verify it still has C03's Hungarian Help endpoint before applying. If another legitimate Help edit intervened, stop and record a new explicit transition instead of silently recalculating historical hashes.

Application changes and implementation publication remain on hold until the C04 integration base is settled. This branch publishes only the proposal and diagnostic evidence.
