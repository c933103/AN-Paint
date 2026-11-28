# Translation review checkpoint

Current source `5ece04b6c604b98fc0e59db600c728e541d08261`: 171 choices × 707 typed entries. PR56 remains an intentional tracking draft. The [current table](current-entry-review.md) and [gallery evidence index](gallery-review-evidence-index.json) distinguish 54 bounded-current records from five open idiom/attestation reviews. Other disclosed confidence/script limits stay attached to their exact review pointers.

## Separate immutable evidence

No complete report tree is copied into this tracker. Use authorized, separately obtained evidence checkouts:

1. Position evidence at `15295e6ca392fef2ec41f2ab29e741dbd83ab9e3` contains the 21 prior reports plus the archived complete Mongolian parent-acceptance comment. Its original immutable report/index bindings and strict acceptance checks remain unchanged. Earlier `fc5d6842` alone lacks the required acceptance record.
2. Gallery evidence at `97c91f05bb2192f13db309d1ce2927cc3f328024` contains `evidence/pr85-gallery-external-link/`: the complete statement review, original source binding, SDK fixture correction and `hosted-7630142/verification.json`. The source binding's earlier application tree is preserved; the two-file test-only correction binds the current tree. All statement values are independently matched to merged XML.

Both utilities are offline and verify exact immutable path/blob/SHA256/size, complete values, original decisions and limits before writing. The cache must neither contain nor sit inside the tracker repository or evidence checkout. In the published nested data layout, this excludes the repository root, its ancestors and every sibling directory inside the repository. Resolved symlink paths obey the same boundary; a genuinely external sibling cache is allowed. Cache-relative paths are aliases under an explicitly supplied external root. Missing, corrupted or URL-only evidence fails; source fixtures and CI never substitute for linguistic review.

```
python materialize_position_review_evidence.py /path/to/position-evidence /external/review-cache
python materialize_gallery_review_evidence.py /path/to/gallery-evidence /external/review-cache
python validate_entry_review.py
python validate_gallery_reconciliation.py /path/to/merged-source /path/to/previous-tracker-data --evidence-root /external/review-cache
python -O validate_gallery_reconciliation.py /path/to/merged-source /path/to/previous-tracker-data --evidence-root /external/review-cache
AN_PAINT_SOURCE=/path/to/merged-source AN_PAINT_PREVIOUS=/path/to/previous-tracker-data AN_PAINT_POSITION_EVIDENCE=/external/review-cache python -m unittest -v test_gallery_reconciliation.py test_materializer_cache_roots.py
AN_PAINT_SOURCE=/path/to/merged-source AN_PAINT_PREVIOUS=/path/to/previous-tracker-data AN_PAINT_POSITION_EVIDENCE=/external/review-cache python -O -m unittest -v test_gallery_reconciliation.py test_materializer_cache_roots.py
```

`SOURCE` is the application repository root at `5ece04b6`. `PREVIOUS_TRACKER_DATA` is the `verification/translation-entry-review-2026-10-13` directory from tracker head `2499c5e32e75d5bd1de916174b9992ea001af6b6`, not its repository root. `TRANSLATION_PROGRESS.md` is resolved at each snapshot's repository root; the current-entry document stays in its data directory. A previous snapshot is optional for the validator but required by the full current test suite. The explicit external evidence root is always required, via the argument or `AN_PAINT_POSITION_EVIDENCE`.

## Preserved historical regression suite

The original position validator, index, fixture and 68-test suite remain unchanged and checkpoint-specific. Its materializer has only the exact cache-boundary hardening recorded in validation.json; the gallery predecessor comparison recognizes that pinned before/after change and rejects unrelated modifications. Run those tests from the actual preceding tracker data directory at `2499c5e3`, with application source at `0aa6c89c` and its own predecessor data directory at `7c5c9779`. This uses the real published checkpoints, not a reconstructed old source. The current gallery validator also directly reuses the original strict report, complete-value, immutable acceptance, receipt and historical gates against unchanged earlier records and current source values.

```
cd /path/to/tracker-2499c5e3/verification/translation-entry-review-2026-10-13
AN_PAINT_SOURCE=/path/to/source-0aa6c89c AN_PAINT_PREVIOUS=/path/to/tracker-7c5c9779/verification/translation-entry-review-2026-10-13 AN_PAINT_POSITION_EVIDENCE=/external/review-cache python -m unittest -v test_merged_assembly_reconciliation.py test_position_reconciliation.py
AN_PAINT_SOURCE=/path/to/source-0aa6c89c AN_PAINT_PREVIOUS=/path/to/tracker-7c5c9779/verification/translation-entry-review-2026-10-13 AN_PAINT_POSITION_EVIDENCE=/external/review-cache python -O -m unittest -v test_merged_assembly_reconciliation.py test_position_reconciliation.py
```

The original merged-assembly command dispatches current gallery data to the new strict validator. Every existing progress/table document requires its marker and all 171 rows; only the compact PR body is exempt. No new application tests, linguistic decisions, whole-language approvals, native-speaker certifications or release claims are made here.
