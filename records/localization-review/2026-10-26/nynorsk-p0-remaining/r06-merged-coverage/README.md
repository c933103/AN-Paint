# Integrated Nynorsk P0 batch: 171-option structural coverage

Source: merged `develop` commit [`df9bc04b848ab5e99457bc67265d771bb839ec9d`](https://github.com/c933103/AN-Paint/commit/df9bc04b848ab5e99457bc67265d771bb839ec9d), tree `8ca5fc4f3989cf8c9307432d5e5c28ceef698251`. Its valid signed merge has parents `857a20103285a77846e340b326667c15a402ff9e` and reviewed PR174 head `3c8123707106dfc991221517e443276f857797db`. All 1,367 tracked blobs and modes match the reviewed tree. The snapshot stays pinned if develop moves.

**72 reviewed Nynorsk P0 values are integrated.** Nynorsk now has **190/717 containers** (previously 118), including **87/92 P0** (previously 15). All 118 inherited values and attributes remain unchanged; P1 stays 87/249. The five remaining missing P0 identities are explicit no-current-consumer holds, not presumed defects: `formats22_derived_exported`, `ui_save_as`, `ui_save_as_jpeg`, `ui_save_as_jpeg_xl`, `ui_save_as_png`. No P1 or unreviewed neighboring fallback was added.

Across the same **171 picker options**:

| Metric | Integrated snapshot | Change |
|---|---:|---:|
| Present containers | 50,549 | +72 |
| Missing containers | 72,058 | −72 |
| Missing P0 | 9,206 | −72 |
| Missing P1 | 22,557 | 0 |
| Present leaves | 50,583 | +72 |
| Missing leaves | 72,195 | −72 |
| English-identical leaves | 7,051 | 0 |
| Source-different leaves | 43,532 | +72 |

All 170 other options are unchanged. Full-presence options remain 59; zero-presence options remain 31. **Presence is not linguistic acceptance; English-identical text is not automatically wrong.** Each option has the same 717 canonical container / 718 leaf denominator. Leaf equality retains the prior report's XML-decoded text comparison, not a new normalization or runtime-fallback metric. Android quote wrapping is preserved and separately bound to the reviewed display text for each of the 72 new values.

## Review reconciliation, not a rewritten acceptance ledger

The CSV/JSON are structural tables. The [prior 171-option evidence report](https://github.com/c933103/AN-Paint/tree/cdc469f0005ebbfeecfded45722f360119425a20/records/localization-review/2026-10-26/current-language-coverage/r02) and [previous merged structural snapshot](https://github.com/c933103/AN-Paint/tree/cde98d358f0035addae961490202b027b4a0e206/records/localization-review/2026-10-26/nynorsk-p0-save/r05-merged-coverage) remain immutable. Every pre-existing catalogue value remains unchanged, so none of its accepted, qualified, clause-only, author-only, historical, unmatched or synthetic scopes is revoked or upgraded here. Global linguistic categories are not recalculated by these structural tables.

The [four final independent reviews and exact approved manifest](https://github.com/c933103/AN-Paint/tree/b4fa13c19f45a66cc701909eb90aa2ee66ed7e4f/records/localization-review/2026-10-26/nynorsk-p0-remaining/r02-reviewed) bind 72 new whole-value AI linguistic/static scopes (69 accepted unchanged, three revised then accepted). Their exact source/target hashes match current source, and their identities are absent in the prior 118-value catalogue and disjoint from the previously reviewed eight. Thus Nynorsk has **80 bounded review-linked whole values**, not whole-locale or native-human acceptance. Original per-entry and global qualifications remain: mixed English count qualifiers and actual fallback command labels, single-key P0 memory warning without its P1 companion, and export/recovery/Save distinctions. The paired oracle remains 120 entries/60 tags; frozen history is unchanged.

## Verification and reproduction

`source-bindings.json` compares every one of the 176 coverage inputs against the fresh merged tree: 175 unchanged, only Nynorsk XML changed. Canonical catalogue, picker tags and tier partition are unchanged. The complete filtered tree is `coverage-source-tree.json`; merge parents/tree/signature outcome are in `merge-identity.json`. `coverage-delta.json` includes exact new review bindings and held identities. The computation rejects unexpected inventory, duplicates, missing inputs, denominator drift, changed inherited values, unmatched review identities or hashes. A separate DOM parser and Git executable independently recompute all 171 rows, totals and CSV/JSON equality.

Obtain the pinned checkout, the prior merged snapshot linked above, its Nynorsk XML at 857a201, and the four final public review JSONs plus approved manifest. Run:

```sh
python3 recompute_delta.py --source-root CHECKOUT --source-tree coverage-source-tree.json --baseline-report PRIOR_MERGED_REPORT --baseline-nn PRIOR_NN_XML --review REVIEW_DIRECTORY/approved-values.json --out OUTPUT
python3 verify_independently.py --source-root CHECKOUT --report OUTPUT
```

[PR terminal tests](https://github.com/c933103/AN-Paint/tree/99359ef89c44b14ecb896b3f8a56ca2d1296677b/records/localization-review/2026-10-26/nynorsk-p0-remaining/r05-terminal-pr) passed. Actual [postmerge run 40281975192](https://github.com/c933103/AN-Paint/actions/runs/40281975192) is **pending at this structural snapshot**; its results will be recorded separately, not inferred from PR evidence. No physical-device, whole-language, native-human, layout or release certification. The 59 scoped/112 fallback distinction, PR56 never-merge, PR159 freeze, PR113 held/retarget scope, Help callback/archive identity and release pauses remain unchanged.
