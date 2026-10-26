# Integrated PR175 coverage delta: Danish and existing Norwegian catalogue

**Terminal integration evidence is now available:** actual postmerge run 40295442728 passed all six checks; fresh source/APK, 1,355 JVM tests, hosted Python 1,372 passed +2 skipped, API35 45 app +74 native, lint and exact-script artifacts were independently verified. See [immutable r06 terminal evidence](https://github.com/c933103/AN-Paint/tree/c46331986de8bd4ffae67bb5c233ff8f4a3e7b5b/records/localization-review/2026-10-26/danish-norwegian-p0/r06-postmerge-terminal). The earlier in-progress source-identity snapshot below remains historical and is not rewritten.

**Integrated source is structurally verified. CI was in progress in the supplied source-identity snapshot; this is not an assertion of its current status.** Source is [PR175 merge `05607f0d60131cc9148461ce595155d820748e4e`](https://github.com/c933103/AN-Paint/commit/05607f0d60131cc9148461ce595155d820748e4e), merged 2026-10-26 at 08:53:33 UTC, with tree `16ff3d877650ad4ad3198ce19007e8606fcd080a`. The supplied authenticated-connector receipt verifies the signed merge, ordered parents `df9bc04b848ab5e99457bc67265d771bb839ec9d` and reviewed head `f6b3e71fd1261935c4d97b20cbbbdcc79ed398ed`, and explicit `develop` ref at that merge when checked. Its tree is identical to the reviewed head. This computation locally validates those receipt fields and binds its exact bytes; it does not independently perform a network commit-graph/signature verification.

Baseline is verified [develop snapshot `df9bc04b848ab5e99457bc67265d771bb839ec9d`](https://github.com/c933103/AN-Paint/commit/df9bc04b848ab5e99457bc67265d771bb839ec9d), tree `8ca5fc4f3989cf8c9307432d5e5c28ceef698251`. The prior provisional PR-head package is preserved unchanged. Source commit and tree are required explicit CLI arguments, checked against the supplied merge receipt and this batch's reviewed tree. No branch movement silently changes the pin or denominator. Actual postmerge push [run 40295442728](https://github.com/c933103/AN-Paint/actions/runs/40295442728) was **in progress in the supplied receipt**, which accompanies the 2026-10-26 08:53:33 UTC merge and has no separate check timestamp. This report does not turn that historical snapshot into an indefinite current-status claim. Its later terminal result is separate evidence; PR results are not relabelled postmerge results.

## Verified structural change

Exactly **78 missing P0 values per locale, 156 total**, are added at the pinned merge. All **127 prior Danish values and 115 prior Norwegian values and their attributes are unchanged**. Locale identity `no` is retained; this report makes no new language-code decision.

| Catalogue | Containers before → merge | P0 before → merge | P1 at merge | English-identical leaves |
|---|---:|---:|---:|---:|
| Danish `da` | 127 → 205 / 717 | 9 → 87 / 92 | 94 / 249, unchanged | 5, unchanged |
| Existing Norwegian `no` | 115 → 193 / 717 | 9 → 87 / 92 | 86 / 249, unchanged | 8, unchanged |

All **169 other picker-option rows are unchanged**, including Nynorsk `nn` at **190 containers / 87 P0**. P2 and P3 are unchanged for every option. The five missing P0 identities in each changed catalogue remain held: `formats22_derived_exported`, `ui_save_as`, `ui_save_as_jpeg`, `ui_save_as_jpeg_xl`, `ui_save_as_png`. Their absence is not classified as a defect. The five Nynorsk holds also remain unchanged.

Across the same **171 picker options**, with **717 canonical containers / 718 canonical leaves**:

| Metric | Integrated snapshot | Delta from baseline |
|---|---:|---:|
| Present containers | 50,705 | +156 |
| Missing containers | 71,902 | −156 |
| Missing P0 | 9,050 | −156 |
| Missing P1 | 22,557 | 0 |
| Missing P2 | 32,519 | 0 |
| Missing P3 | 7,776 | 0 |
| Present leaves | 50,739 | +156 |
| Missing leaves | 72,039 | −156 |
| English-identical leaves | 7,051 | 0 |
| Source-different leaves | 43,688 | +156 |

Full-presence options remain **59** and zero-presence options **31**. These are structural metrics, not certification. English-identical text is not automatically wrong. Equality uses the prior report's exact XML-decoded leaf text without new normalization; Android quote wrapping remains significant. Runtime fallback is not counted as a target-catalogue value.

## Review scopes are reconciled, not summed into an invented global total

`review-scope-reconciliation.json` binds every new locale/identity pair to its full source text, final reviewed display and XML text, attributes, hashes, actual public receipt, and unchanged per-entry/global qualifications. All 156 pairs are proven absent from their baseline catalogues and exactly present at this merge. Their outcomes are **149 accepted unchanged and 7 revised then accepted** (Danish 72/6; Norwegian 77/1). This is **bounded independent AI whole-value linguistic/source-static review**, not native-human, runtime/device, layout, release or whole-locale acceptance.

No prior catalogue value is overwritten. Prior accepted, qualified, clause-only, author-only, historical, unmatched and synthetic scopes remain under their original evidence and qualifications; none is revoked or promoted. **Global linguistic acceptance categories are not recomputed here**, and `global_accepted_count` is explicitly null. The original 171-option evidence report and subsequent Nynorsk delta remain authoritative for inherited classifications.

Specific qualifications remain visible: mixed English count fragments and `Load image…`, actual inherited `Image format`, existing save confirmations/action names, one optional floating selection, export/recovery versus Save behavior, and single-key P0 memory warnings without their P1 companions. Paired-warning 120-entry/60-tag scope and frozen history are not expanded by this coverage report. Global scoped59/fallback112, PR56 never-merge, PR159 freeze, PR113 held/retarget, Help callback/archive identity, interrupted-archive and release pauses remain unchanged.

## Evidence and reproduction

- `source-bindings.json`: exact Git blob SHA-1, SHA-256, size and mode for all **176 coverage inputs** (174 catalogues, picker tags, priority partition). **174 are unchanged; only da/no catalogues changed.**
- `coverage-source-tree.json`: the exact filtered integrated-tree entries; full recursive tree input is hash-bound in `input-bindings.json`. The computation reconstructs and validates every supplied Git subtree hash. The source pin is checked against the exact supplied public merge receipt, copied byte-for-byte as `source-identity.json`. This computation performs no network retrieval or new commit-graph verification. The supplied receipt reports a separate fresh check of all 1,370 source blobs; this coverage computation itself rechecks the 176 relevant inputs.
- `input-bindings.json`: exact baseline-report, prior da/no XML, full integrated tree, supplied merge receipt, approved manifest and eight public review-receipt hashes. Its paths are portable evidence roles, not execution locations.
- `structural-per-locale.csv` / `.json`: all 171 rows, identical across formats, with P0/P1/P2/P3/container/leaf/English-identity fields.
- `independent-verification.json`: separate DOM parser and Git executable recomputation of all rows, totals, prior-value preservation and 156 exact review joins.
- `mutation-controls.json`: positive validation plus **39 rejected malformed/corrupted inputs**, including missing/duplicate rows or source inputs, altered hashes, changed target text, omitted qualifications, fabricated global acceptance, changed develop ref or merge parents/signature/commit and relabelled postmerge success.

Obtain the pinned integrated checkout, its complete recursive Git-tree API response, the supplied merge verification receipt, the verified df9 baseline report and checkout, and the final public review packet. Approved-manifest SHA-256 is `ecafd7485336b095c59c9c3103b93cabdf909f03da0da5526aa031367c2f657e`. No application or review input is modified by these scripts.

```sh
python3 recompute_delta.py --source-root MERGED_CHECKOUT --source-tree-file SOURCE_TREE_RESPONSE.json --identity-receipt MERGE_RECEIPT.json --source-commit 05607f0d60131cc9148461ce595155d820748e4e --source-tree 16ff3d877650ad4ad3198ce19007e8606fcd080a --postmerge-run-id 40295442728 --baseline-report BASELINE_REPORT --baseline-source-root BASELINE_CHECKOUT --review-dir FINAL_REVIEWS --out OUTPUT
python3 verify_independently.py --source-root MERGED_CHECKOUT --report OUTPUT --baseline-report BASELINE_REPORT --baseline-source-root BASELINE_CHECKOUT --review-dir FINAL_REVIEWS --source-commit 05607f0d60131cc9148461ce595155d820748e4e --source-tree 16ff3d877650ad4ad3198ce19007e8606fcd080a
python3 test_coverage_guards.py --source-root MERGED_CHECKOUT --report OUTPUT --baseline-report BASELINE_REPORT --baseline-source-root BASELINE_CHECKOUT --review-dir FINAL_REVIEWS --source-tree-file SOURCE_TREE_RESPONSE.json --source-commit 05607f0d60131cc9148461ce595155d820748e4e --source-tree 16ff3d877650ad4ad3198ce19007e8606fcd080a
```

**Ready within the checked integrated structural/review-binding scope.** CI and Android runtime outcomes are not polled or evaluated by this computation. The copied source-identity receipt records the actual postmerge run as in progress at that snapshot, not passed; later terminal evidence must be read separately and does not rewrite this receipt. No PR result is represented as postmerge evidence. Publication and terminal postmerge test evidence are separate actions.
