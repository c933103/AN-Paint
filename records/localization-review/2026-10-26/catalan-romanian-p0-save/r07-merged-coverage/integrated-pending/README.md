# Integrated PR176 coverage: 20 missing Catalan/Romanian P0 values added

**Integrated source; actual postmerge CI pending in the supplied identity receipt.** At [PR176 merge `6a42948a3ac7bad241d502f3b6c18ebf1c0327d8`](https://github.com/c933103/AN-Paint/commit/6a42948a3ac7bad241d502f3b6c18ebf1c0327d8), tree `65afa7b96a83c08e0ae08365166dec0520694356`, Catalan and Romanian each have **137 containers and 19 of 92 P0 values present**. Each still has **73 missing P0 values: five explicit no-current-consumer holds and 68 outside this batch**. The 68 are not newly held, reviewed or declared defects.

The supplied `source-identity.json` receipt binds actual postmerge push [run 40311048893](https://github.com/c933103/AN-Paint/actions/runs/40311048893) as in progress and verifies the actual signed merge, ordered parents `05607f0d60131cc9148461ce595155d820748e4e` and reviewed head `a365f4b552448803c0bb48b3c44cdf508550eaf9`, explicit `develop` ref at this merge when checked, and identical tree to the reviewed head. This computation validates and hash-binds that supplied receipt; it does not freshly authenticate the remote commit graph. The receipt's pending actual-postmerge status is an observation at its check, not an indefinite current-status claim. It supplies no separate check timestamp; the 2026-10-26 10:54:36 UTC merge timestamp is not represented as a CI polling time. Later terminal evidence belongs in a separate receipt; PR results are never relabelled postmerge evidence.

The baseline is the [verified PR175 merge `05607f0d60131cc9148461ce595155d820748e4e`](https://github.com/c933103/AN-Paint/commit/05607f0d60131cc9148461ce595155d820748e4e), tree `16ff3d877650ad4ad3198ce19007e8606fcd080a`. Its [immutable integrated coverage report](https://github.com/c933103/AN-Paint/tree/e4340c2ba50658df8b3164a08611a34623cda5c1/records/localization-review/2026-10-26/danish-norwegian-p0/r07-merged-coverage) is preserved. No branch movement changes this analysis's pin or denominator. The original provisional PR-head report is preserved unchanged. This integrated computation does not poll workflows or infer a passing result.

## What changed

Exactly ten previously absent P0 values are added to each catalogue. All **127 inherited values and attributes per locale—254 total—are unchanged**, as are all **169 other picker-option rows**.

| Catalogue | Containers before → merge | P0 before → merge | P1 at merge | English-identical leaves |
|---|---:|---:|---:|---:|
| Catalan `ca` | 127 → 137 / 717 | 9 → 19 / 92 | 94 / 249, unchanged | 6, unchanged |
| Romanian `ro` | 127 → 137 / 717 | 9 → 19 / 92 | 94 / 249, unchanged | 8, unchanged |

The five explicit holds are `formats22_derived_exported`, `ui_save_as`, `ui_save_as_jpeg`, `ui_save_as_jpeg_xl` and `ui_save_as_png`. The supplied review evidence's no-direct-reference finding is limited to its pinned production inventory; absence is not proof of a defect or of future non-use. `remaining_missing_P0_classification` in the JSON artifacts enumerates all 73 missing identities and separates the five holds from the 68 outside-batch identities for each locale.

Nynorsk remains at 190 containers, Danish at 205 and the existing Norwegian `no` catalogue at 193, with their five holds each intact. P1/P2/P3 values are unchanged for every option. This report makes no new language-code decision.

## All 171 options were recomputed

The denominator remains **717 canonical containers / 718 canonical leaves**, partitioned into P0 92, P1 249, P2 305 and P3 71.

| Metric | Pinned integrated source | Change from baseline |
|---|---:|---:|
| Present containers | 50,725 | +20 |
| Missing containers | 71,882 | −20 |
| Present P0 | 6,702 | +20 |
| Missing P0 | 9,030 | −20 |
| Missing P1 | 22,557 | 0 |
| Missing P2 | 32,519 | 0 |
| Missing P3 | 7,776 | 0 |
| Present leaves | 50,759 | +20 |
| Missing leaves | 72,019 | −20 |
| English-identical leaves | 7,051 | 0 |
| Source-different leaves | 43,708 | +20 |

Full-presence options remain **59** and zero-presence options **31**. These are structural measures, not linguistic certification. English-identical text is not automatically wrong. As in the baseline, equality means exact XML-decoded leaf-text equality; Android quote wrapping is not newly normalized, and runtime fallback is not counted as target-catalogue presence.

## Twenty exact review joins; no invented global acceptance total

The [original independent review packet](https://github.com/c933103/AN-Paint/tree/137b2917329a1dcf85bbc78b2d9581101cbcb649/records/localization-review/2026-10-26/catalan-romanian-p0-save/r02-reviewed) accepted all twenty complete values unchanged. Every new locale/identity pair is proven absent at baseline and exactly present at the pinned merge, joined by source/target hashes and attributes to the normalized approved manifest and original locale-specific verdict. `review-scope-reconciliation.json` preserves each **full original verdict, rationale, confidence, per-entry and global qualifications**, plus all eleven reviewer static composition examples. Those examples remain synthetic/static, not Android execution.

The acceptance is **bounded independent AI whole-value linguistic/source-static review**, not native-human, physical-device, layout, release or whole-language certification. Review-time limitations remain attributed to their original receipts; they are not rewritten into claims about later tests. The actual inherited Catalan `Save changes?`, Romanian `Salvaţi modificările?`, `Image format`, action labels and canonical fallbacks remain unchanged and are not newly accepted. Export/share may write a file while retaining unsaved document state and the ordinary Save destination; the reviewed save-success notification is not a clean-state assertion. Substituted provider errors and user-controlled names are not translated or certified.

The inherited review ledger is exact-hash-bound, not recounted. Prior accepted, qualified, clause-only, author-only, historical, unmatched and synthetic scopes remain under their original evidence: none is revoked, promoted or guessed. **Global linguistic categories are not recomputed; `global_accepted_count` is null.** The 120-entry/60-tag paired-warning boundary, frozen history and global scoped59/fallback112 remain unchanged. PR56 never-merge, PR159 freeze, PR113 held/retarget, Help callback/archive identity, interrupted-archive and release pauses remain in force.

## Evidence and reproducibility

- `structural-per-locale.csv` / `.json`: all 171 rows with identical P0/P1/P2/P3/container/leaf/English-identity fields.
- `source-bindings.json`: exact Git blob SHA-1, SHA-256, size and mode for **176 coverage inputs**: 174 `values*/strings.xml` catalogues, picker tags and priority partition. **174 inputs are unchanged; only ca/ro XML changed.** Thus 172 catalogue files are byte-identical to baseline.
- `coverage-source-tree.json`: filtered entries from the supplied complete recursive source-tree response. `recompute_delta.py` reconstructs every supplied Git subtree hash to the pinned root and checks all 176 coverage input byte identities. The byte-preserved `source-identity.json` additionally binds the supplied actual commit/parents/signature/ref/pending-run verification. It does not freshly query a branch, authenticate the remote commit graph, or execute application code.
- `input-bindings.json`: exact baseline manifest/report/ledger, baseline ca/ro XML, complete supplied source-tree response, merge identity receipt, approved manifest and original reviewer receipt hashes. Paths are portable evidence roles, not execution locations.
- `independent-verification.json`: a separate DOM parser and Git executable reproduce all rows/totals, CSV equality, inherited values/attributes, twenty exact review joins, complete qualifications and the five-versus-68 missingness distinction.
- `mutation-controls.json`: positive validation and **62 rejected malformed/corrupted controls** (all 54 provisional controls retained plus eight merge/status controls), including JSON/XML/schema defects, missing/duplicate rows or files, tree/hash corruption, indexed/unindexed format-token mismatch, altered full-value review metadata/qualifications, misclassified missingness, removed prior pauses and fabricated global acceptance. Added controls reject wrong merge/develop/ordered parents/signature, a PR event mislabelled as postmerge, a false pending-CI success, unbound receipt metadata and the wrong reported run.
- `reproducibility-check.json`: ordinary and `python3 -O` computations, independent verification and controls agree byte-for-byte. Checks do not rely on removable Python `assert` statements.
- `privacy-check.json` and `manifest.json`: semantic content review and exact prepared-file identities. These files are prepared locally; this computation performs no publication.

Obtain the exact integrated checkout and complete recursive Git-tree response, the supplied merge identity receipt, the immutable baseline report and its checkout, and the final review packet. The scripts do not change any source or review input.

```sh
python3 recompute_delta.py --source-root MERGED_CHECKOUT --source-tree-file SOURCE_TREE_RESPONSE.json --identity-receipt MERGE_RECEIPT.json --baseline-report BASELINE_REPORT --baseline-source-root BASELINE_CHECKOUT --review-dir FINAL_REVIEWS --out OUTPUT
python3 verify_independently.py --source-root MERGED_CHECKOUT --report OUTPUT --baseline-report BASELINE_REPORT --baseline-source-root BASELINE_CHECKOUT --review-dir FINAL_REVIEWS
python3 test_coverage_guards.py --source-root MERGED_CHECKOUT --report OUTPUT --baseline-report BASELINE_REPORT --baseline-source-root BASELINE_CHECKOUT --review-dir FINAL_REVIEWS --source-tree-file SOURCE_TREE_RESPONSE.json
```

Repeat with `python3 -O` and a separate output directory for the optimization check. The scripts deliberately require this exact PR176 merge and verified baseline. They retain the supplied pending-CI observation rather than assuming later success. The original provisional source identity and its manifest remain unchanged.

**Ready within the checked integrated structural/review-binding scope.** Actual postmerge CI is pending in the supplied receipt. Its later terminal result and runtime/artifact outcomes remain separate evidence, not inferred here.
