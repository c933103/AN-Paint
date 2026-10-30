# Old English / Old Norse — revision 10 bounded wording adoption

**Frozen 2026-10-30 22:21:00.426589 UTC. Research records only; no application integration.**

This is a **new revision-10 record**, not an overwrite or relabeling of the [earlier rev9 snapshot](https://github.com/c933103/AN-Paint/tree/329017883a5639b30fb688785c8a5b02bab20fb9/verification/translations/2026-10-30/sparse-review-packets/historical). The frozen project source remains commit [`96681f687671a1fdffe134a325843919c1543401`](https://github.com/c933103/AN-Paint/commit/96681f687671a1fdffe134a325843919c1543401), tree `39bb7351fa5532194e2c0430432b2f0cc6358a86`.

## Adopted wording and remaining holds

| Locale | P0 adopted / held | P1 adopted / held | Total adopted / held |
|---|---:|---:|---:|
| Old English (`ang`) | 49 / 43 | 170 / 79 | **219 / 122** |
| Old Norse (`non`) | 47 / 45 | 183 / 66 | **230 / 111** |
| Total | **96 / 88** | **353 / 145** | **449 / 233** |

The 682 locale/key rows cover 341 exact source keys per locale. **449 exact values are adopted as bounded AI-reviewed wording**, including **14 notation-only rows** (7 per locale, all P1). Those 14 are included, not additional linguistic credit; **435 adopted rows contain lexical wording**. All **233 holds remain excluded**.

These are experimental normalized late West Saxon and Old West Norse, with explicit **modern technical coinages and new software senses**. Historical word bases do not attest whole software phrases. Adoption is not native-human certification, whole-language completion, Android resource presence, installed rendering, TalkBack, runtime, CI or release acceptance.

## Which record controls which decision?

1. [Separate later adoption receipt](adoption/adoption-receipt.md), [structured receipt](adoption/adoption-receipt.json), and [exact 449-row adopted wording overlay](adoption/adopted-wording-values.tsv) establish the bounded adoption after conditional ledger-only validation passed. [Notation subset](adoption/notation-only-values.tsv) separates the 14 included nonlexical rows.
2. [Dependency-audited 682-row ledger](dependency-audited/current-value-recommendations.tsv) preserves the **earlier recommendation stage** with exact sources, current targets, reasons, confidence and provenance. Its historical `UNADOPTED` metadata is intentional: the later adoption overlay changes adoption status, not the exact targets or those original recommendation decisions. Do not mistake the two stages for conflicting final totals.
3. [Dependency audit](dependency-audited/terminology-dependency-audit.md), [four hold exceptions](dependency-audited/dependency-hold-exceptions.tsv), [family membership](dependency-audited/family-membership.tsv), [prior-accept gates](dependency-audited/prior-accept-value-gates.tsv) and [reason-scope corrections](dependency-audited/reason-scope-corrections.tsv) record why 453 earlier recommendations became 449. All 229 earlier holds remain; four common-metadata holds were added. No target wording changed in that audit.
4. [Final author overrides](author/90-author-secondcheck.md) and [latest override index](author/91-latest-override-index.md) preserve revision 10, including 44 text overrides and three evidence-only restatements. [Independent override review](independent-review/90-independent-override-review-through-rev9.md) and [revision-10 dynamic-label review](independent-review/91-independent-dynamic-label-review-rev10.md) bind their exact decisions. Original author batches remain visible in `author/` as v1 history, not the final adoption list.

The six initial independent batch reviews and matching source snapshots remain available in the [immutable earlier archive](https://github.com/c933103/AN-Paint/tree/329017883a5639b30fb688785c8a5b02bab20fb9/verification/translations/2026-10-30/sparse-review-packets/historical/independent-review); their identifiers and original hashes remain in the new ledger. Withdrawn grammatical allegations stay withdrawn; honest modern coinages are not rejected solely because medieval software attestations cannot exist.

### Four metadata holds deliberately retained

Both locales' `ui_autosave_metadata_is_missing` and `ui_invalid_autosave_metadata` remain **HOLD** in this snapshot. No shared metadata glossary is automatically adopted. Any later metadata reassessment is outside this frozen record and must receive its own dated decision; it is not silently incorporated here.

## Data-only validation, not application testing

The reviewer reports [ledger-token/number validation](adoption/ledger-token-number-validation.tsv) for all **682 rows**, including exact format-token sequences on **72 placeholder-bearing rows** (56 in the adopted subset). Technical identifiers, units, numeric/range limits and relevant symbols were compared. Sixteen digit-representation differences express positive as greater than zero or spelled zero as `0`; their semantic explanations are retained. The receipt records **zero substantive mismatches and no new hold**.

Publication inventory checks independently confirm the row counts, exact adopted source/target equality to the corresponding ACCEPT rows, and all four metadata exclusions. These are document/data checks. No project script, test, build, XML/resource compilation, UI or runtime check is claimed.

The [PR 56 adoption comment](https://github.com/c933103/AN-Paint/pull/56#issuecomment-6534700034) has exact [submitted-body](adoption/pr56-comment-request.md) and [readback evidence](adoption/pr56-comment-exact-readback.json) here. PR 56 remains a tracking record, not a merge target.

## Integrity and original versus published hashes

- [snapshot-manifest.tsv](snapshot-manifest.tsv) maps **33 frozen input files** to original and published SHA-256, sizes and Git blob identities. Nineteen files have **metadata-only sanitization**: temporary paths, internal coordination wording and transport-error notes were removed; review-stage metadata labels use project-facing acceptance terminology. No exact source/target/key, linguistic recommendation, confidence or attribution value was changed. The prior `UNADOPTED` recommendation stage and later bounded adoption remain distinct.
- Embedded hashes in original receipts and manifests intentionally bind **original snapshot bytes**, not sanitized publication bytes. Use the top-level snapshot manifest to resolve each original-to-published mapping. In particular, the original 682-row ledger hash is `6e6f8ad79d3243c7e41c75e0c401abf2f23d0eb01e7ff383abfe66fb9df43eb2`; the original adoption overlay hash is `df3fd4f16c4e26f713379eb72d34595b486625c566e63461d63ae1a66522b7c6`. Their publication differences are metadata only.
- The author revision-10 ledger and override index are byte-identical to their supplied originals: `533e16a1aea28666f53b0c66f0ba5aad34f7d569bd451c017c4ae789363a5901` and `092f3d415337ca108e51c3658f8726352adb3fbcbd97feccbdee9a237911d28e`.
- [source-bindings.tsv](source-bindings.tsv) verifies five underlying project inputs against their remote baseline-tree Git blob identities and byte sizes. This supplements, rather than rewrites, the reviewers' narrower local-checkout claims.
- [SHA256SUMS](SHA256SUMS) checks all publication files except itself; the immutable Git tree binds the checksum file. [Source URL index](source-urls.tsv) retains the 47 cited URLs and the records using them.

Only authored translation/review material is archived—no raw third-party PDF/TMX corpora, credentials or unrelated private data. Repository visibility and the [existing license](https://github.com/c933103/AN-Paint/blob/96681f687671a1fdffe134a325843919c1543401/LICENSE) are unchanged. Cited dictionaries, grammars and other external works retain their own rights and attribution; this record does not relicense them.

All preexisting records and application/resource/test/workflow files remain unchanged. No implementation, merge or release is performed by this archive.
