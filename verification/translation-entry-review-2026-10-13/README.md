# Translation entry-review checkpoint

Current source: [`e53b2e6a`](https://github.com/c933103/AN-Paint/commit/e53b2e6aaaa9ac231cfdd38485e28ee9d638e870). The [current overview](current-entry-review.md) contains all 171 language choices, partitioned over 700 typed resources each.

Two separate actual-merge reconciliations are recorded:
1. PR96: three complete French assembly findings resolve; seven other pairs become source-stale. Intermediate totals: 2,971 current / 31 open.
2. PR99: four complete LT/AR/RU/JA crop plurals (all 14 forms) resolve four of those holds. Current totals: 2,975 current / 27 open / 44,198 present unknown / 72,500 exact-catalogue gaps.

Japanese Help and HK Help/crop still need current-English pair review. Four paused processing-label findings remain untouched. PR67 is unmerged and excluded. Identical aggregate totals to the preceding published checkpoint do not mean identical per-language dispositions: French is 692/8, Japanese 690/10 and HK 265/7.

- `entry-review-receipts.json`: 3,002 unique active pairs, 56 superseded records, 56 preserved partial records.
- `entry-review-counts.json`: per-language states and exact key membership.
- `fr-assembly-merged-reconciliation-20261015.json`: PR96 full French pairs and seven intermediate stale pairs.
- `four-crop-merged-reconciliation-20261015.json`: PR99 full crop pairs and three remaining stale pairs.
- `source-identities.json`: immutable bindings and preserved historical context.
- `validation.json` and `independent-validation.json`: check scope and results; the latter explicitly labels fresh mechanical recomputation separately from prior independent review.

Run `python validate_entry_review.py` for internal consistency. Run `python validate_merged_assembly_reconciliation.py /path/to/merged/source [previous_tracker_data]` for exact-source, stale-pair, table and historical-preservation checks. Neither command runs application tests or grants language acceptance. Technical CI evidence remains separate from complete-value linguistic/static acceptance.

PR56 remains the intentional tracking draft and must not be merged.
