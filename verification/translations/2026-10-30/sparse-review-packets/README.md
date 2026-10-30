# Sparse-language priority review packets — 30 October 2026

**Research records only. No application integration, test result, merge approval or release credit.**

Baseline: [`96681f687671a1fdffe134a325843919c1543401`](https://github.com/c933103/AN-Paint/commit/96681f687671a1fdffe134a325843919c1543401), tree `39bb7351fa5532194e2c0430432b2f0cc6358a86`. This records branch is based directly on that frozen merged commit; it does not update `develop`.

## Decision status and entry points

| Packet | Exact status at this snapshot | Read first |
|---|---|---|
| Yucatec Maya (`yua`) | **53 language-bearing values accepted**: 15 P0 + 38 P1. Two original candidates are corrected in the final ledger. | [Final review](yucatec/accepted/YUCATEC_PRIORITY_REVIEW.md), [exact acceptance ledger](yucatec/accepted/acceptance-ledger.tsv) |
| Yucatec invariant notation | **7 templates accepted separately**, 0 P0 + 7 P1; **zero linguistic-progress credit**. | [Notation ledger](yucatec/accepted/notation-ledger.tsv) |
| Yucatec remaining inventory | **232 holds**: 74 P0 + 158 P1. No proposed translation; production English fallback remains. | [Exact held sources](yucatec/accepted/residual-source.tsv), [item-specific limits](yucatec/accepted/residual-limits.md) |
| Old English (`ang`) and Old Norse (`non`) | **DRAFT / UNACCEPTED**: 341 source rows × 2 locales = **682 target candidates**, 92 P0 + 249 P1 per locale. Reviewer corrections and holds remain unresolved at final-acceptance level. | [Draft inventory](historical/draft/README.md), [mandatory exact override ledger](historical/draft/90-author-secondcheck.md), [latest override index](historical/draft/91-latest-override-index.md), [independent reviews](historical/independent-review/) |

The **49 existing Yucatec production values are untouched**. Linguistic acceptance here is a bounded research decision, not native-human certification or proof that any value was integrated. Historical review tables use `ACCEPT` for experimental-candidate recommendations only; **none of the 682 historical-language targets is final-accepted by this publication**.

### Original candidates versus revised wording

- `yucatec/provenance/` preserves the original 10 Save candidates, 43 further candidates, 7 notation candidates, full held-source inventory, lexical rationale and [orthographic second-check receipt](yucatec/provenance/orthography-second-check-receipt.md). It is provenance, **not the authoritative final target list**. Use the acceptance/notation ledgers above. `ui_underline` and `ui_centred` use their exact corrected full targets there.
- Historical batches 1–6 preserve the original v1 candidates. **Do not import them without the exact override ledger.** The frozen author ledger runs through revision 9; its navigation index identifies **24 ang + 16 non latest text overrides**, plus three explicitly restated recovery-copy evidence-status cells and whole-convention caveats. These are still low-confidence, unaccepted proposals.
- Historical independent reviews 1–6 bind their adjacent reviewed snapshots, not later author wording. Earlier conventions and rev6/rev9 ledger snapshots are retained to preserve those relationships. Later author corrections do not silently change reviewer decisions. Existing report language reflects its recorded stage, not a new blanket acceptance.

## Snapshot identity and integrity

Snapshot completed **2026-10-30 21:28:52.081584 UTC**. All selected text files were copied before publication preparation and their source hashes were checked unchanged across the copy pass. This is a fixed point-in-time snapshot, not a claim to include later review activity.

- [snapshot-manifest.tsv](snapshot-manifest.tsv): 39 selected research files, with **original snapshot SHA-256** and **published SHA-256/Git blob SHA-1**, sizes, provenance identifiers and byte-change status. Exact source/target/key tables, TSVs and override text are preserved. Fourteen Markdown files have metadata-only sanitization: temporary paths and internal operational coordination were removed or replaced with project-facing descriptions.
- Hashes embedded in original review reports and receipts identify their **original input snapshots**; when metadata sanitization changes a file, those embedded hashes are intentionally not rewritten. The manifest maps original to published bytes. The final Yucatec review and both final TSV ledgers, all historical base candidate tables and the exact historical override ledger/index are byte-identical to the snapshot.
- [source-bindings.tsv](source-bindings.tsv): six underlying project input files, with SHA-256, Git blob SHA-1 and byte sizes. Their computed Git blob identities/sizes match the remote baseline tree. The remote baseline commit also resolves to the stated tree. This publication verification supplements, rather than rewrites, the original reviewers' limited local-checkout claims.
- [SHA256SUMS](SHA256SUMS): published-file checksums, excluding the checksum file itself. The immutable commit's Git tree binds that file as well.

Document inventory and hash checks confirm 53 lexical rows, 7 separate notation rows, 232 held rows and 341 paired historical source rows. No project scripts, tests, builds or runtime checks are claimed. Application source, resources, tests, workflows and existing records remain unchanged.

## Attribution and evidence limits

[source-urls.tsv](source-urls.tsv) indexes the 67 cited external URLs and the records using them. The reports retain source titles, authors/publishers, page references and bounded evidentiary claims. Principal evidence includes Mozilla's explicitly tagged Yucatec translation memory, Javier Abelardo Gómez Navarrete/UQROO, INALI, La Jornada Maya, Bosworth–Toller, Cleasby–Vigfusson, university grammars and edited historical texts. Dictionary bases do not establish whole software sentences; proposed historical-language digital terminology remains modern adaptation.

Only authored translation/review records and limited cited evidence are included—**no raw external PDF, TMX corpus, source rendering, credential or unrelated private data**. The repository's [existing license](https://github.com/c933103/AN-Paint/blob/96681f687671a1fdffe134a325843919c1543401/LICENSE) and public visibility are unchanged. Cited external works retain their respective rights and attribution; linking them does not relicense them or claim an unrestricted corpus-import right.

Further work requires exact-value reconciliation of historical corrections/holds and separate source-bound integration validation. This record does not perform or authorize implementation.
