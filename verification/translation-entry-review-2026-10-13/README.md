# Translation entry-review checkpoint

Current source: [`e53b2e6a`](https://github.com/c933103/AN-Paint/commit/e53b2e6aaaa9ac231cfdd38485e28ee9d638e870). The [current overview](current-entry-review.md) preserves all 171 choices and 700 typed entries per choice.

Fresh complete [Japanese Help](https://github.com/c933103/AN-Paint/blob/1422e223df2c9a06dc3c959fb326abdc9e0ac8d7/verification/current-assembly-help-review-20261015/japanese.json) and [HK Help/crop-plural](https://github.com/c933103/AN-Paint/blob/1422e223df2c9a06dc3c959fb326abdc9e0ac8d7/verification/current-assembly-help-review-20261015/hong-kong.json) reviews accept all three existing values unchanged. Derived totals are 2,978 current / 24 open / 44,198 present unknown / 72,500 exact-catalogue gaps. Japanese is 691/9 and HK 267/5.

PR96 and PR99 reconciliation evidence remains unchanged. The last three changed-English holds are resolved; all four paused processing-label findings remain exact. PR67 and its six new keys are unmerged and excluded.

- 3,002 unique active pairs; 59 superseded historical records; 56 partial historical records.
- `current-assembly-pair-reconciliation-20261015.json`: complete pairs, preserved predecessors, exact final-review report bindings and durable receipts.
- `current-assembly-review-evidence/`: exact independent final review JSON artifacts.
- `entry-review-counts.json`: all per-language states and exact key membership.
- `source-identities.json`: unchanged 182-path resource manifest and preserved source/context history.
- `validation.json` and `independent-validation.json`: fresh mechanical check scope with prior validation preserved.

Run `python validate_entry_review.py`, then `python validate_merged_assembly_reconciliation.py /path/to/merged/source [previous_tracker_data]`. Run `AN_PAINT_SOURCE=/path/to/merged/source python -m unittest -v test_merged_assembly_reconciliation.py` for strict manifest, complete-review and history mutation tests. Repeat under `python -O` to ensure gates do not depend on assertions.

No application tests are rerun here. Independent model/source-assisted full-value linguistic/static review is bounded; it is not native-speaker, device-layout, whole-language or release certification. PR56 remains the intentional tracking draft and must not be merged.
