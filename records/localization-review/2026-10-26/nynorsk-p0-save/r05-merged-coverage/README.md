# Integrated Nynorsk batch: current structural coverage delta

Source: merged AN-Paint `develop` commit [`857a20103285a77846e340b326667c15a402ff9e`](https://github.com/c933103/AN-Paint/commit/857a20103285a77846e340b326667c15a402ff9e), tree `6bb4fa11534149df7f8f58cb3d21faf2b802089f`. The signed merge has parents `d0e4a3868c376bb857be8ca9762e7ef5ed31cbd4` and reviewed PR173 head `2d940e411829f991b3399c1fdb572dd12b0ad44f`; all 1,364 merged blobs and modes match the reviewed tree. This is a new snapshot, not a silent change to the earlier report's source pin.

**Eight missing Nynorsk P0 strings are now integrated.** Nynorsk has 118/717 present containers (formerly 110), including 15/92 P0 (formerly 7); 77 P0 entries remain missing. Every inherited Nynorsk value/attribute is unchanged. All 170 other picker options are unchanged.

Across the same **171 options**, presence is **50,477 containers**, missing **72,130**. P0 missing is **9,278** (eight fewer); P1 missing stays **22,557**. Present leaves are **50,511**, missing **72,267**. English-identical leaves remain **7,051**; source-different leaves rise to **43,460**. Full-presence options remain 59; zero-presence options remain 31. Presence is not acceptance, and English-identical text is not automatically an error.

The CSV/JSON are **structural coverage tables**, not a rewritten linguistic ledger. The [prior current-value evidence report](https://github.com/c933103/AN-Paint/tree/cdc469f0005ebbfeecfded45722f360119425a20/records/localization-review/2026-10-26/current-language-coverage/r02) remains immutable. Its author-only, historical, qualified, clause-only and synthetic scopes are preserved; no old scope is revoked or upgraded. Exactly eight new disjoint Nynorsk whole-value scopes have the [independent AI linguistic/static review](https://github.com/c933103/AN-Paint/tree/1b75cf9d0614728f1ad2c9276ddd5566ce70ed23/records/localization-review/2026-10-26/nynorsk-p0-save/r02), with original confidence and limitations retained. This is not native-human or whole-language acceptance.

`source-bindings.json` proves all 176 source inputs against the fresh merged Git tree: 175 unchanged, only Nynorsk strings changed. Canonical source, picker inventory and tier partition are unchanged. `coverage-delta.json` binds each new exact source/target hash to the final review. Computation checks malformed/missing/duplicate data and independently rechecks all 171 rows through a separate DOM parser and the Git executable; CSV and JSON agree.

## Reproduce

Use a checkout of the merged source above; save the recursive Git tree API response for that commit; obtain the immutable baseline report, its original Nynorsk XML from d0e4a386, and the public independent review linked above. Then run:

```sh
python3 recompute_delta.py --source-root CHECKOUT --source-tree MERGED_TREE_JSON --baseline-report BASELINE_REPORT --baseline-nn BASELINE_NN_XML --review INDEPENDENT_REVIEW_JSON --out OUTPUT
python3 verify_independently.py --source-root CHECKOUT --report OUTPUT
```

[PR-head terminal gates](https://github.com/c933103/AN-Paint/tree/0d04d7ce6d983d691bc304621f23507601bfd242/records/localization-review/2026-10-26/nynorsk-p0-save/r04) passed before merge. Separate [postmerge run 40272570496](https://github.com/c933103/AN-Paint/actions/runs/40272570496) is **pending at this snapshot**; PR artifacts are not relabelled postmerge artifacts. This receipt adds no native-language, physical-device, layout or release certification. The 59 scoped / 112 fallback distinction and #56 never-merge, #159 freeze, #113 retarget/held-warning, Help callback/archive identity and release holds remain unchanged.
