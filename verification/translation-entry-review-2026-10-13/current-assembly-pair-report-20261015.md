# Current assembly-pair reconciliation — 15 October 2026

## Result

Three current English/target pairs are accepted unchanged after separate complete model/source-assisted reviews: Japanese assembly Help, Hong Kong Chinese assembly Help, and the complete HK crop-preview plural. The unchanged source is `e53b2e6aaaa9ac231cfdd38485e28ee9d638e870`; the preceding tracker checkpoint is `f507f4c4d8fde2731434ad5ee2b122d747ec6d6d`.

Derived totals: **2,978 current / 24 needing re-review / 44,198 present unknown / 72,500 exact-catalogue gaps**. There are still 3,002 active receipts and 119,700 total slots. Japanese is 691 current / 9 open; HK is 267 / 5; French remains 692 / 8. Language-level full acceptance remains zero.

## Complete evidence

- [Japanese complete review](https://github.com/c933103/AN-Paint/blob/1422e223df2c9a06dc3c959fb326abdc9e0ac8d7/verification/current-assembly-help-review-20261015/japanese.json): seven Help paragraphs, 32 full sentence/clause units.
- [HK complete review](https://github.com/c933103/AN-Paint/blob/1422e223df2c9a06dc3c959fb326abdc9e0ac8d7/verification/current-assembly-help-review-20261015/hong-kong.json): all seven Help paragraphs, both complete English plural forms and the sole complete HK `other` form.
- [Parent exact-source acceptance receipt](https://github.com/c933103/AN-Paint/pull/56#issuecomment-6195806297).
- Exact final JSON files are also included in `current-assembly-review-evidence/` for offline verification. SHA-256: Japanese `bebad46b4d2c2abf2fa2125af9d6c74427eafa502b641ba97f90ffc8e516e5c2`; HK `05615a99edde6bd04ecc21b04eb1fcbfdc1589d0e591e132c1c236bdb2e97975`.

## Preservation

Only these three active receipts change. The other 2,999 active receipts, all prior cohorts, all 56 partial records, and all 56 prior superseded records remain exact. The three replaced stale receipts are appended intact with explicit successor links, giving 59 superseded records. The four paused ms/id/ja/zh-HK processing-label records remain unchanged and open. PR96/PR99 fixtures, every historical prose section, 171 language rows, and the 700-entry denominator are preserved. No resource or application bytes changed. PR67 and its six new keys remain unmerged and excluded.

The new receipt metadata explicitly says `accept_unchanged`, complete current-pair re-review, and no correction in this step. Historical code corrections retain their original provenance in preserved predecessor records.

## Verification

Both normal and optimized Python runs passed the internal validator, the exact-source/history/table validator, and all **29 test methods** with no skips. Tests include missing/duplicated/substituted resource identities, all original seven complete-review gates, all three new complete-review metadata gates, altered/missing final reports, partial Help/plural coverage, source hash changes, historical receipt/partial/cohort tampering, all four paused holds, duplicate plural quantities and table mismatches. All 182 resource identities, 3,002 English and 3,002 target hashes, 171 catalogue partitions, and 13 distinct fresh-review source/context files were verified.

Use `AN_PAINT_SOURCE=/path/to/merged/source` when running the unit tests; the two full-source mutation methods otherwise explicitly skip. Detailed results and commands are in `current-assembly-pair-validation-20261015.json`.

## Limits

This is data reconciliation plus mechanical validation of complete independent model/source-assisted linguistic/static evidence. No application tests were rerun. It does not establish native-speaker, installed-device, font/layout, accessibility, whole-language or release certification. The remaining 24 records retain their actual findings. **PR56 stays an intentional tracking draft and must not be merged.**
