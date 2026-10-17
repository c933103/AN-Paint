# Polish and Czech priority translation evidence

This separate evidence ref records the bounded review behind application commit
`75c59756900f80535b87eae173d9c9eebb155cd9`, based on develop
`7f69e915485b2eeb1d0a97af29c7e00a8a4b5fbe`.
The application tree contains only two resource updates and six compact test/fixture changes.
This evidence ref is not intended to merge into develop.

## Review packet

Download [priority-review-packets.zip](priority-review-packets.zip). The ZIP contains:

- `pl/producer-priority-ledger.json`: all 341 original English/Polish pairs, producer findings, proposed new translations and provenance.
- `pl/independent-final-receipt.json`: independent final decisions, complete final target values and consumer evidence for all 341 pairs.
- `pl/independent-p2-companions.json`: the two independently reviewed composition helpers, counted separately.
- `cs/final-priority-ledger.json`: complete baseline/final pairs and retained source evidence for all 341 Czech targets.
- `cs/independent-final-receipt.json`: final independent decisions, including the two applied v3 corrections, for all 341 Czech targets and separate P2 helpers.
- Both independent reviewer summaries and an export manifest.

The export manifests retain original artifact hashes. Executor-specific absolute path prefixes are replaced by logical `input-artifacts/` references. The Czech packets' separate upcoming Commons companion section is omitted; every priority row and P2 helper remains. These logical references describe input provenance and are not additional downloadable files. Original review-time statements, including pending publication and zero integrated credit, are historical statements preserved without silently rewriting reviewer verdicts.

## Exact bounded accounting

Each locale has 341 P0/P1 keys: 92 P0 and 249 P1.

- Polish: 221 new priority translations, six existing corrections and two separate P2 helpers. All 341 final pairs were independently read. There are 310 bounded wording/static-context accepts and 31 holds: 30 no-direct-consumer holds and one unchanged `ui_fit` layout hold. The 221 additions comprise 203 static-context accepts and 18 context-unverified wording candidates.
- Czech: 241 new priority translations, 12 existing corrections and two separate P2 helpers. All 341 final pairs were independently read. There are 310 bounded wording/static-context accepts and 31 holds: 30 no-direct-consumer holds and one unchanged `ui_fit` layout hold. The 241 additions comprise 220 static-context accepts and 21 wording-only candidates awaiting concrete consumer verification. The 30 no-consumer holds comprise 25 wording passes and five retained wording/context uncertainties.
- The four pre-existing Polish uncertainty values, five pre-existing Czech uncertainty values and both Fit captions remain unchanged.

The original review source pin is `c86ecfd707cd88e6656010a800cb6048ed867d4e`. All cited consumer files, the English catalogue and priority definition were checked unchanged at the integration base. This identity recheck earns no additional linguistic review credit. Prior withdrawn conclusions are not reinstated.

## Composition and tests

See [combined-test-receipt.json](combined-test-receipt.json) for exact final local results,
[final-pair-verification.json](final-pair-verification.json) for value/placeholder/attribute checks,
and [source-publication-manifest.json](source-publication-manifest.json) for the eight application files and complete remote leaf/mode verification.

The cs/pl SVG-warning additions are limited to that two-key message family. All other families and the global 59-scoped/112-open-fallback inventory remain unchanged. The separate nine-key upcoming Commons batch is absent from both locale resources and from this application change. Existing PR56 is not modified.

No full-locale completion, native-speaker certification, Android runtime, TalkBack, glyph/layout, device or release acceptance is claimed. Local host checks are not Android build or installed UI evidence. Exact-head hosted CI and Codex review are separate gates and must be checked before merge; merging remains gated on those exact-head results.
