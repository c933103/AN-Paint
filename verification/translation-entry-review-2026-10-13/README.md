# Translation review checkpoint

Current source `0aa6c89c`; 171 choices × 706 entries. See [current overview](current-entry-review.md) and [complete report bindings](position-review-evidence-index.json). PR56 remains an intentional tracking draft.

## Separate evidence contract

The 21 complete reports are already durable on the separate evidence branch; their 462,279 bytes are not duplicated in this tracker tree. The unchanged index binds each report to its immutable revision, exact Git blob SHA1, SHA256, byte count, complete value, JSON pointer, acceptance and superseded decisions. Relative `position-review-evidence/...` paths in the ledger/index are aliases beneath an explicit external materialization root, not paths promised inside this repository.

- Twelve recovered reports: [`fc5d684289c08acd8ea1bc1947f70dad39e8a907`](https://github.com/c933103/AN-Paint/tree/fc5d684289c08acd8ea1bc1947f70dad39e8a907/verification/assembly-position-review-20261015).
- Nine earlier reports remain individually bound to [`7a653672121333a3f30e85ae57347d4005987559`](https://github.com/c933103/AN-Paint/tree/7a653672121333a3f30e85ae57347d4005987559/verification/assembly-position-review-20261015). Those exact blobs are also retained in the descendant above.

Obtain the immutable evidence checkout separately using an authorized repository read. It must contain `verification/assembly-position-review-20261015/`. Then run:

```
python materialize_position_review_evidence.py /path/to/evidence-checkout /external/review-cache
```

The utility is offline. It verifies all 21 complete report byte sequences and accepted-value pointers before writing anything, then verifies the resulting cache again. It does not trust an URL, branch name, or archive name as evidence. Missing or altered input fails; it never substitutes current wording fixtures for independent reports. Keep the cache outside the tracker and evidence checkouts.

## Offline validation and tests

`SOURCE` is the application repository root at `0aa6c89c9d3a4d133a8b231e7002783b60ead46d`. `PREVIOUS_TRACKER_DATA` is the `verification/translation-entry-review-2026-10-13` data directory from tracker head `7c5c9779ab3ef70ddc5df35bfd62fa05fce87172`, not its repository root. The current validator lives in that same data-directory layout on the successor. `TRANSLATION_PROGRESS.md` is resolved at each snapshot's repository root; `current-entry-review.md` remains in its data directory. The separately obtained evidence checkout can be `fc5d684289c08acd8ea1bc1947f70dad39e8a907`, which retains all 21 individually pinned report blobs.

```
python validate_entry_review.py
python validate_position_reconciliation.py /path/to/merged-source /path/to/previous-tracker --evidence-root /external/review-cache
python -O validate_position_reconciliation.py /path/to/merged-source /path/to/previous-tracker --evidence-root /external/review-cache
AN_PAINT_SOURCE=/path/to/merged-source AN_PAINT_PREVIOUS=/path/to/previous-tracker AN_PAINT_POSITION_EVIDENCE=/external/review-cache python -m unittest -v test_merged_assembly_reconciliation.py test_position_reconciliation.py
AN_PAINT_SOURCE=/path/to/merged-source AN_PAINT_PREVIOUS=/path/to/previous-tracker AN_PAINT_POSITION_EVIDENCE=/external/review-cache python -O -m unittest -v test_merged_assembly_reconciliation.py test_position_reconciliation.py
```

`PREVIOUS_TRACKER_DATA` and `AN_PAINT_PREVIOUS` are optional additional predecessor comparisons. The explicit evidence root is required, through `--evidence-root` or `AN_PAINT_POSITION_EVIDENCE`; unavailable evidence fails closed. Tests require the evidence environment variable and use actual report bytes, never network access or skipped evidence checks. Set both source and previous variables to exercise all source and predecessor mutation paths without skips.

The original merged-assembly entry point also dispatches current data to the new validator using `AN_PAINT_POSITION_EVIDENCE`. Its historical helper gates remain pinned to the e53b2e6a checkpoint, and tests reconstruct only the unchanged historical view for those original gates. Every existing progress/table document still requires its marker and all 171 rows; only the deliberate compact PR body is exempt.

No application tests are rerun here. No broader language, native-speaker or device certification is claimed.
