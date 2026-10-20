# All-language review reconciliation, 20 October 2026

Source: AN Paint develop `0134e79c588a027bbd239f7685fff52b0771819f`.

The report and CSV cover all 171 offered options, each with 717 source identities. Counts: 8,631 bounded-current reviews (44 test-mode conventions), 241 held/re-review, 39,905 present entries with unmapped accepted review, and 73,830 exact-catalogue gaps. Every row partitions to 717; no whole-language acceptance is established.

The compressed machine-readable union preserves per-entry original evidence pointers and exact source bindings. Its uncompressed JSON contains 8,872 unique mapped identities. This audits existing evidence; it does not create new linguistic review. Newly prepared/unmerged Swedish, Korean, Taiwan Chinese and open-item repairs are excluded.

Current pairs preserve original confidence, wording-only, dormant and runtime limits. Original Spanish full-batch evidence and some Russian/European Portuguese full ledgers remain unreconciled; accepted independent corrections are counted without inventing full-batch credit. Help reviews against the separate corrected English in unmerged PR122 remain distinguished from exact-current-English pair acceptance.

The human-readable current table is in tracking PR56's opening post. Historical receipts and their original immutable refs remain intact. Decompress `all-language-review-union.json.gz` to inspect the full mapped evidence. The CSV also includes P0–P3 source-presence columns; those columns do not measure review acceptance.
