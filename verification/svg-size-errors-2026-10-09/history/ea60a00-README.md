Historical 53-pair README; relative links adjusted to the parent evidence directory.

# Two SVG original-size errors: incomplete AN-W05 draft

**Not ready to merge.** The current draft contains two default-English resources
and **106 source-assisted proposed values in 53 of the 59 scoped catalogues**.
The remaining **12 values in six scoped catalogues** are absent; those languages
retain the default fallback without English-filled localized overrides. The other
81 incomplete offered catalogues remain separate unfinished work. For these two
keys there are therefore **53 exact offered overrides and 87 offered-tag gaps**.
The full scoped completeness gate is unchanged and still fails.

Analysis base: `5bf82b67199aaecbd341a8b150a887f8d60b5567`, tree
`05f9f6aa330f2f1432264938d5d0e41dfe8d86ee`.
Publication base: merged #28 at `4b615ce2d9e27814df84812b90858b5f676ce51a`, tree
`84107dd03e8ac96ed953afd95bf6cbe5b72f84c4`. Its language-picker changes are untouched.
Initial 48-pair draft head: `80f0448f878165213eaa7e9bd5ad286be00e4ce8`.
This follows [AN-W05-C01's inventory](https://github.com/c933103/AN-Paint/pull/20#issuecomment-6077456325).

## Production scope

`SvgOriginalSize` retains the same finite/positive and ceil-to-Int checks. A typed
`IllegalArgumentException` subclass identifies the two reasons without Android
resources. The existing gallery error presentation maps only this exception to
canonical resources; all other diagnostic messages pass through unchanged.

The source meaning remains:
- The SVG supplies no usable declared original size; no canvas-derived size was substituted.
- Its original size exceeds Android's bitmap dimensional limit; no resizing occurred.
- The dimensional limit is distinct from the memory budget and 32 MiB download limit.
- No resizing must not be narrowed to no automatic shrinking.

No numeric limit, resizing policy, successful import, provider/network operation,
metadata validation, cleanup, credit association or retained user edit changes.
The five-pair second revision changes resource values, test oracles, and the one-glyph
font extension described below; it does not modify either production Kotlin file again.

## Second-pass result

The first draft provided 48 proposed pairs. The bounded dictionary/catalogue pass
produced five more complete pairs: `hak-Hant-TW`, `hak-Latn-TW`, `bo`, `dz`, `vi-Hani`.
An independent source-assisted composition review found their clauses coherent for
incomplete-draft inclusion. It corrected three inherited PFS spellings in the new
Hakka size-limit string only: 點 `tiam → tiám`, 上 `sông → song`, and 調 in the
adjust sense `tiau → thiàu`. No unrelated catalogue spelling was changed.

The new wording uses ordinary supported paraphrases for file-stated original
size and an unused canvas-derived substitute. It does not require inventing a
technical XML-declaration term. Hakka pairs share the same meanings; Nôm retains
the catalogue's `別` variant and already attested `朱 別` compound.

- [Final exact values](../research-v2/added-proposed-values.json)
- [Independent clause review, exact values, sources and limits](../research-v2/independent-composition-review.json)
- [Complete second-pass research index](../research-v2/v2-review-index.md)
- [Current coverage/dispositions for all 59 scoped and 81 other offered tags](../translations.json)

The research inputs are preserved as snapshots: their statements that resources
were not edited or review was pending describe the research stage, before the
separate final composition review and this revision. `initial-proposals.json`,
`translation-review.md` and the original additional-pass reports preserve the
first 48-pair stage. They are not current coverage counters.

These remain source-assisted proposals. Independent composition checking is not
native-speaker acceptance, complete-catalogue approval, or device script/layout QA.

## Six withheld scoped tags

`ain-Kana`, `ain-Latn`, `jje`, `mn-Mong`, `mnc-Mong`, `ryu`.
The research index and its linked source ledgers give exact attempted URLs,
retrieval outcomes and clause-level gaps. No failed lookup is treated as proof that
a language cannot express these messages. No whole UI sentence need appear in a
dictionary, but its grammar, terms and negative scope must be defensible.

- Ainu: original/intrinsic and canvas/dimensional terminology, declaration/usability
  and replacement argument structures, bitmap ceiling and complete no-resize clause.
  `pororu` is an independently documented coinage, not a newly invented word;
  its technical sense still needs review. Both scripts must remain paired.
- Jeju: declaration/usability and canvas-derived replacement clauses remain open.
  A size-limit-only candidate stays in research, not resources; genuine Jeju
  negation must not be replaced by Korean syntax with altered endings.
- Traditional Mongolian: declaration, canvas-derived replacement, dimensional
  bound and completed negative size change require full compositional review.
  Deleting automatic from a nominal no-change phrase does not establish past action.
- Manchu: file-declaration and usable-original-size syntax, derived replacement
  argument roles and bitmap dimension bound remain open. Completed negative
  morphology now has independent support; the whole message does not yet.
- Okinawan: full declaration/usability, derived substitution, bitmap ceiling and
  completed polite negative resizing require review beyond isolated dictionary words.

## Nôm glyph coverage caught and repaired

The first second-pass host run caught a real additional failure: the new,
dictionary-supported `豫` (U+8C6B, in dựa trên) was missing from the bundled Nôm
UI subset. `host-tests-v2-before-font.log` preserves that 315-test / eight-failure
result: seven completeness records plus this glyph failure.

A preservation-only extension appends U+8C6B from the already pinned Nom Na Tong
v5.18 source. All 735 old glyphs and 733 old mapped codepoints, their compiled
outlines, advances/bearings and existing metadata are preserved. Two independent
outputs are byte-identical; the updated subset is 275,312 bytes, SHA256
`797ac4ef00f0dd8a982d5216dbd78db3edda07b578b9f8642d0156add90bd526`.
The font inventory hash is updated; no other font is rebuilt. Reproduction, source
hashes and preservation checks are in `nom-svg-font-extension.json`. Existing
notices remain applicable. This repairs coverage without rewriting supported
wording solely to avoid its character or relying on Android device fallback.

## Tests and exact outcomes

`checks.json` records this revision's actual local results. Canonical XML/format
structure, five focused resource-contract tests, focused font coverage, and whitespace checks pass. The
full host run executes **316 tests with seven completeness-failure records, zero
errors/skips**; `host-tests-v2.log` contains its complete failed output. Those seven
records reject the same 12 missing values across six scoped tags. No non-coverage
failure remains after the font repair.
Global strict completeness reports 87 incomplete offered tags and 168 entries.
No existing completeness group, assertion, workflow or timeout was relaxed.

The new API30/35 Robolectric tests use actual gallery actions, downloaded SVG bytes
and the real parser. They cover displayed localized/fallback reasons, repeated
attempts, cancelled import/no substitute dialog, cleanup/no credit association,
and unchanged unrelated diagnostic formatting. The five new exact catalogues now
have independent reviewed wording oracles. Manchu explicitly remains an English-
reason fallback. Pure dimension tests cover typed classifications and boundaries.

These JVM tests have **not run locally**: this executor has no SDK, Gradle cache or
Kotlin compiler. New-head CI must report its own build and device stages separately;
the unchanged host gate prevents JVM/lint from executing while six scoped gaps remain.

### Historical CI at initial draft head 80f0448

[Workflow 37908873594](https://github.com/c933103/AN-Paint/actions/runs/37908873594)
completed with overall **failure**:
- Host regression gate: 315 tests, 16 failure records from the original 22 missing
  values, two optional Pillow skips; JVM/lint did not run. Actual fetched CI log, losslessly gzip-compressed to preserve its trailing whitespace:
  [ci-host-tests-80f0448.log.gz](../ci-host-tests-80f0448.log.gz).
- APK/source build passed. Existing API35 device tests passed: 74 codec, 14 editor,
  one credit seed and one restart-verification test. These do not run the new JVM tests.
- Code review returned no major issues. The subsequent security-triggered response
  also said no major issues, but its summary was labeled Code Review; no separately
  labeled security attestation is inferred.

Those results and reviews belong only to `80f0448`, not to the later five-pair
revision. The [exact-head status comment](https://github.com/c933103/AN-Paint/pull/29#issuecomment-6078080372)
retains their separate dispositions. Initial local logs remain preserved too.

The draft still needs supported complete wording for six scoped tags, refreshed
fallback expectations, passing full checks and acceptable current-head review
before integration. Physical-device, screen-reader and fluent-language acceptance
remain unclaimed. Integration remains deferred.
