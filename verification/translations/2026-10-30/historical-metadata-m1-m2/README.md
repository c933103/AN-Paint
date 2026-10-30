# Historical-language metadata — separate M1 and M2 adoption records

**Frozen 2026-10-30 22:41:17.279981 UTC. Documentation/data only; no source implementation.**

This is a later, additive record. It does **not** overwrite or relabel the [frozen revision-10 449-adoption / 233-hold snapshot](https://github.com/c933103/AN-Paint/blob/e6a2b792cf21bd8a03dfee49a7cafb2b0bc38641/verification/translations/2026-10-30/historical-priority-review-rev10/README.md). All decisions remain bound to source commit [`96681f687671a1fdffe134a325843919c1543401`](https://github.com/c933103/AN-Paint/commit/96681f687671a1fdffe134a325843919c1543401), tree `39bb7351fa5532194e2c0430432b2f0cc6358a86`.

## Final bounded wording totals

| Stage | Added P0 | Added P1 | Added lexical | Cumulative adopted / held |
|---|---:|---:|---:|---:|
| Frozen revision 10 | — | — | — | 449 / 233 |
| M1: six unchanged targets | 4 | 2 | **6** | 455 / 227 |
| M2: two revised clauses | 0 | 2 | **2** | **457 / 225** |

**Combined delta: 8 lexical values, 4 P0 + 4 P1, no notation-only additions.** Final totals are **ANG 223 adopted / 118 held** and **NON 234 adopted / 107 held**; adopted tiers are **100 P0 + 357 P1**. The previously included 14 notation-only rows remain unchanged, so 443 adopted rows contain lexical wording. Every unrelated hold remains.

These are **moderate-confidence, bounded AI-reviewed wording decisions** under experimental normalized late West Saxon / Old West Norse and a limited modern metadata convention. They do not claim native-human certification, medieval software attestation, whole-language completion, source presence, UI/runtime behavior, CI or release readiness.

## Exact values and decision order

- [Combined exact eight-row delta](adopted-metadata-delta.tsv) is a mechanical index of the adopted rows, preserving the exact English, previous held target, final target, confidence and controlling record. It introduces no new linguistic decision.
- **M1:** [author proposals](m1/author/metadata-convention-and-exact-proposals.md), [independent review](m1/independent-review/metadata-M1-independent-review.md), [eight-row recommendation delta](m1/independent-review/metadata-M1-independent-delta.tsv), [six-row adoption overlay](m1/adoption/adopted-metadata-M1-six-values.tsv) and [adoption receipt](m1/adoption/adoption-receipt.json). Six previously held targets are adopted **without wording changes**. At that stage, ANG `colour_invalid_metadata` and NON `colour_truncated_metadata` remained held for separate clause-level review.
- **M2:** [two exact author revisions](m2/author/two-colour-clause-proposals.md), [independent review](m2/independent-review/M2-independent-review.md), [two-row adoption overlay](m2/adoption/adopted-M2-two-values.tsv) and [adoption receipt](m2/adoption/adoption-receipt.json). ANG changes only `onfo` → `onfehþ`; NON changes only `endar` → `endisk`. Both complete old and revised clauses are retained. The earlier forms are **not declared impossible**; the new forms have positive primary dictionary/construction support.

The recommendation-stage `UNADOPTED` metadata remains historical evidence. The later explicit `M1_adoption_status` / `M2_adoption_status` fields record the controlling adoption decisions; do not confuse the two stages or count the same row twice.

### Limited metadata convention

For these reviewed rows, metadata denotes **structured descriptive/control records**, textual or binary, embedded or archive-associated. It does not require ordinary prose, external/appended placement, optionality or disposability. Historical component and grammar evidence supports the chosen forms; the computing senses and encoded-range metaphor remain explicitly modern. This bounded decision is not automatic acceptance of every related glossary term or surrounding sentence.

The original dependency-hold rationales remain in the frozen revision-10 archive; M1's eight-row review and M2's previous-held-target fields show exactly which later evidence resolves or revises each of those eight rows. No earlier record is silently rewritten.

## Validation and durable review receipts

[M2 data-only validation](m2/adoption/data-only-final-validation.json) records exact authorized target/source agreement, one word-form change per M2 row, absence of placeholders and numeric limits in those two clauses, disjoint cumulative counts and unchanged prior fingerprints. Publication document checks independently confirm all eight rows were held in the frozen 682-row ledger, M1 retained its six exact targets, M2 preserves the exact previous targets and source English, and the additive result is **457 / 225**.

These are document/data checks, **not project tests, Android resource compilation or runtime verification**.

- [M1 PR 56 receipt](https://github.com/c933103/AN-Paint/pull/56#issuecomment-6534896627): [exact submitted body](m1/adoption/pr56-comment-request.md), [readback evidence](m1/adoption/pr56-comment-exact-readback.json).
- [M2 PR 56 receipt](https://github.com/c933103/AN-Paint/pull/56#issuecomment-6535005927): [exact submitted body](m2/adoption/pr56-comment-request.md), [readback evidence](m2/adoption/pr56-comment-exact-readback.json).

Both public comment bodies are preserved exactly. PR 56 remains a tracking record, not a merge target.

## Hashes, provenance and publication limits

- [Snapshot manifest](snapshot-manifest.tsv) maps **25 frozen input files** to original and published SHA-256, sizes and Git blob hashes. Sixteen files have metadata-only sanitization: temporary paths, internal coordination and operational notes were replaced with project-facing record identifiers. **Exact source, target, key, confidence, linguistic decision and dictionary/source evidence are unchanged.**
- Embedded hashes intentionally identify **original snapshot bytes**. For sanitized files, use the snapshot manifest to resolve published hashes. Metadata path strings in validation receipts are archive-root identifiers; `historical-priority-review-rev10/` identifies the separate earlier snapshot. The original M2 author hash is `10ce9baef42c5beab6fdb6195778b87589132b5f3c34cbee4e2a26f7074fc930`; the M2 adoption receipt hash is `23cb3b862ecd87578a994ff9025a5135fdd66b38c0a274ae42d30228e5d7ac75`.
- [Source bindings](source-bindings.tsv) identify five frozen project inputs by SHA-256, Git blob SHA-1 and size; their blob identities match the remote records-branch baseline. [Source URL index](source-urls.tsv) retains 18 cited URLs with the records using them.
- [SHA256SUMS](SHA256SUMS) covers all publication files except itself; the immutable Git tree binds the checksum file.

Only authored translation/review work is included—no raw third-party PDF/TMX corpus, credential or unrelated private data. Public visibility and the [existing repository license](https://github.com/c933103/AN-Paint/blob/96681f687671a1fdffe134a325843919c1543401/LICENSE) are unchanged; external works retain their respective rights and attribution.

All prior records and application/resource/test/workflow files remain unchanged. No implementation, merge or release is performed by this archive.
