# Integrated PR177 coverage: 26 missing Catalan/Romanian P0 values added

**Integrated source; actual postmerge CI pending in the supplied identity receipt.** At [merge `ce796879f4568a27b9d905a8e8db639dd0a93a30`](https://github.com/c933103/AN-Paint/commit/ce796879f4568a27b9d905a8e8db639dd0a93a30), tree `f7c5f2fca54eb06b4a0c55df25a0b80b2ac4c12c`, Catalan and Romanian each have **150 containers and 32 of 92 P0 values present**. Each has **60 missing P0 values: five explicit no-current-consumer holds and 55 outside this batch**, not newly held, reviewed or declared defects.

The signed merge occurred at 2026-10-26 13:04:33 UTC. The supplied `source-identity.json`, verified at 13:07:03 UTC, binds ordered parents `6a42948a3ac7bad241d502f3b6c18ebf1c0327d8` and reviewed head `10acbff912812b938bf2626be1e8a9e84e7aa7bc`, exact matching tree, and explicit `develop` at this merge. Actual push [run 40327501312](https://github.com/c933103/AN-Paint/actions/runs/40327501312) is **pending in that receipt**, not declared passed here. This is a pinned observation, not a claim about later current run status. The computation checks the supplied receipt locally; it does not poll CI or freshly authenticate the remote commit graph.

The baseline is actual [PR176 merge `6a42948a3ac7bad241d502f3b6c18ebf1c0327d8`](https://github.com/c933103/AN-Paint/commit/6a42948a3ac7bad241d502f3b6c18ebf1c0327d8), tree `65afa7b96a83c08e0ae08365166dec0520694356`. Its [immutable coverage evidence](https://github.com/c933103/AN-Paint/tree/501c89a0b4e3c908571870f2ef16b1be8eddcfff/records/localization-review/2026-10-26/catalan-romanian-p0-save/r07-merged-coverage) preserves both the original pending observation and separate terminal success. Baseline actual push run 40311048893 completed successfully at 2026-10-26 11:19:16 UTC. `baseline-source-identity.json` retains the earlier pending bytes; `baseline-terminal-status.json` retains the separate terminal supplement. The baseline is **not** described as currently pending. Neither baseline result is substituted for PR177 evidence; corrected PR proof and actual postmerge status are separately bound below.

## Test-only correction and runtime inheritance

The original PR177 head `06a2e4078efa1fe8ef8ea37b186ece0431633f08` failed [run 40319792630](https://github.com/c933103/AN-Paint/actions/runs/40319792630): one JVM oracle expected English for `ca-ES-valencia`, but Android resolved the reviewed parent Catalan value. [Original failure evidence](https://github.com/c933103/AN-Paint/tree/fe8f255de677c1a1a843f70a4c7800f40916cc5a/records/localization-review/2026-10-26/catalan-romanian-p0-import/r04-original-head-failure) remains unchanged. Its original provisional package is preserved with manifest SHA-256 `49cd2dae0dee1c9fe7bbe2373d47e1f0fb4551dfb33eaa1a2fa874d99efa2fd0`.

The corrected PR head changed exactly two test files, not production resources or review values. Its complete provisional package remains unchanged with manifest SHA-256 `cdb497d05be1894167c8d3c25e611ebc75f0f1411c794d064e1ee55ab600607d`. Both complete supplied Git trees are reconstructed and compared: 1,374 blob identities are unchanged. **All 171 structural rows are byte-identical to the original provisional report.** `head-correction-provenance.json` records the exact changed test hashes and preserves the failure receipts. Corrected [PR run 40323966400](https://github.com/c933103/AN-Paint/actions/runs/40323966400) subsequently passed all six checks. The [immutable corrected PR terminal receipts](https://github.com/c933103/AN-Paint/tree/4700fd58aa4e5637793157eaadeffafa2d261b84/records/localization-review/2026-10-26/catalan-romanian-p0-import/r06-pr-terminal) are source-bound to synthetic tested commit `fb6b356d6fd87ecbdf79ddc816a92fd87fbfda17`, not the actual merge commit.

Structural presence remains **70 direct / 101 absent** for the selected tagged-colour key. Separately, its source-bound runtime-resolution partition is **70 direct + one parent-inherited + 100 English defaults**. The failed JVM assertion directly observed `ca-ES-valencia` inheriting `ca`; this does not add a Valencian resource or independent linguistic acceptance. The complete corrected PR runtime oracle passed, as recorded in the exact `TaggedColourImportTest` case receipt. That PR evidence is not relabelled as execution of the fresh actual postmerge run. No structural or global acceptance denominator is changed by this distinction.

## Structural change

| Catalogue | Containers before → merge | P0 before → merge | P1 | English-identical leaves |
|---|---:|---:|---:|---:|
| Catalan `ca` | 137 → 150 / 717 | 19 → 32 / 92 | 94 / 249, unchanged | 6, unchanged |
| Romanian `ro` | 137 → 150 / 717 | 19 → 32 / 92 | 94 / 249, unchanged | 8, unchanged |

Exactly thirteen previously absent P0 values per locale are added. All **274 inherited values and attributes**, including the previous twenty reviewed Save values, are unchanged. All **169 other picker-option rows** are unchanged. Nynorsk remains at 190 containers, Danish at 205 and the existing Norwegian `no` catalogue at 193. P1/P2/P3 remain unchanged everywhere.

The five absent holds per ca/ro are `formats22_derived_exported`, `ui_save_as`, `ui_save_as_jpeg`, `ui_save_as_jpeg_xl` and `ui_save_as_png`. The JSON report explicitly enumerates those five and the separate 55 outside-batch missing identities. The inherited no-current-consumer evidence does not imply future non-use or classify absence as a defect.

Across **171 options / 717 canonical containers / 718 canonical leaves**:

| Metric | Pinned integrated source | Delta |
|---|---:|---:|
| Present / missing containers | 50,751 / 71,856 | +26 / −26 |
| Present / missing P0 | 6,728 / 9,004 | +26 / −26 |
| Missing P1 / P2 / P3 | 22,557 / 32,519 / 7,776 | unchanged |
| Present / missing leaves | 50,785 / 71,993 | +26 / −26 |
| English-identical leaves | 7,051 | unchanged |
| Source-different leaves | 43,734 | +26 |

Full-presence options remain 59; zero-presence options remain 31. Equality uses the inherited exact XML-decoded leaf text, without new Android quote normalization. Runtime fallback is not target-catalogue presence. English-identical text is not automatically wrong.

**Separate single-key observation:** `save20_unsupported_image_colour` is present in 70 option catalogues and absent in 101. This selected P0 resource family's 70/101 split is **not** a replacement for global scoped59/fallback112, not seventy new acceptances and not whole-locale coverage.

## Exact review reconciliation

[Original independent review receipts](https://github.com/c933103/AN-Paint/tree/9049ae41bee76f0d74c9160bb738d19aff6abe90/records/localization-review/2026-10-26/catalan-romanian-p0-import/r02-reviewed) bind all **26 complete values**: Catalan twelve unchanged plus one exact ASCII clarification; Romanian thirteen unchanged. Every new source/target/attribute hash joins the original verdict and normalized approved manifest. The original candidate and final replacement remain distinct. Full original per-entry rationale, confidence, author-context qualifications, independent qualifications, global qualifications and **18 static composition examples** are preserved. Those examples remain static, not runtime evidence.

The Catalan replacement describes characters representing light/dark tones and a fixed-width font; it does not declare the original `monoespaiat` ungrammatical. Mixed English lower-bound counts, actual `Image format`, inherited action/Save labels and `Dithering`/`Tramatge` labels remain untouched. Nominal PDF 144 dpi does not guarantee every rendered size; generic slash/control-character filename wording is not an exhaustive validator specification. These and other limits remain in the exact receipts.

This is bounded independent AI whole-value linguistic/source-static acceptance—not native-human, device, layout, release or whole-language certification. **Global accepted count remains null.** No prior accepted, qualified, clause-only, author-only, historical, unmatched or synthetic scope is promoted, revoked or guessed. NN/DA/NO holds, paired P1/frozen history/global59/112, PR56 never-merge, PR159 freeze, PR113 hold/retarget, Help callback/archive identity, interrupted-archive and release pauses remain unchanged.

## Verification and reproduction

- `structural-per-locale.csv` and `.json`: all 171 rows, recomputed rather than incremented from a summary.
- `source-bindings.json`: exact Git SHA-1/SHA-256/size/mode for 176 coverage inputs. Only ca/ro XML changed; **174 inputs and 172 catalogue files are unchanged**. The complete supplied tree's recursive Git hashes are reconstructed to the pinned root; this computation rechecks the 176 coverage inputs, not all 1,376 source blobs.
- `source-identity.json` and `corrected-pr-*.json`: byte-bound actual merge/pending-push and distinct successful corrected PR runtime receipts.
- `input-bindings.json`: exact corrected provisional and original failed-head manifests, merge identity, successful corrected PR runtime receipts, baseline manifests and historical/terminal evidence, prior ca/ro source, full supplied head tree, approved values and both original review receipts. Paths are portable evidence roles.
- `review-scope-reconciliation.json`: twenty-six exact full-value joins, original-versus-final revision evidence and all qualifications. No invented global linguistic total.
- `independent-verification.json`: separate DOM parser and Git executable reproduce all rows/totals, CSV equality, 274 inherited values, review joins, baseline-status distinction and single-key scope.
- `mutation-controls.json`: **78 rejected malformed/hash/schema/qualification/missingness controls**, including indexed/unindexed format-token mismatches, falsely current baseline pending status, erased ASCII revision and single-key scope promoted to global acceptance.
- `reproducibility-check.json`: eighteen calculation/verification outputs agree byte-for-byte ordinarily and under `python3 -O`; guards do not depend on removable assertions.
- `privacy-check.json` and `manifest.json`: decoded-content privacy review and exact prepared-file identities. No application/review input or external repository is changed by this computation.

```sh
python3 recompute_delta.py --source-root MERGED_CHECKOUT --source-tree-file SOURCE_TREE_RESPONSE.json --corrected-report CORRECTED_PROVISIONAL_REPORT --merge-identity MERGE_IDENTITY.json --pr-terminal-dir CORRECTED_PR_TERMINAL_PACKET --previous-report ORIGINAL_PROVISIONAL_REPORT --previous-head-tree ORIGINAL_HEAD_TREE_RESPONSE.json --failure-evidence ORIGINAL_FAILURE_PACKET --baseline-report BASELINE_FLAT_REPORT --baseline-terminal-report BASELINE_TERMINAL_WRAPPER --baseline-source-root BASELINE_CHECKOUT --review-dir FINAL_REVIEWS --out OUTPUT
python3 verify_independently.py --source-root MERGED_CHECKOUT --report OUTPUT --corrected-report CORRECTED_PROVISIONAL_REPORT --previous-report ORIGINAL_PROVISIONAL_REPORT --baseline-report BASELINE_FLAT_REPORT --baseline-terminal-report BASELINE_TERMINAL_WRAPPER --baseline-source-root BASELINE_CHECKOUT --review-dir FINAL_REVIEWS
python3 test_coverage_guards.py --source-root MERGED_CHECKOUT --report OUTPUT --corrected-report CORRECTED_PROVISIONAL_REPORT --previous-report ORIGINAL_PROVISIONAL_REPORT --baseline-report BASELINE_FLAT_REPORT --baseline-terminal-report BASELINE_TERMINAL_WRAPPER --baseline-source-root BASELINE_CHECKOUT --review-dir FINAL_REVIEWS --source-tree-file SOURCE_TREE_RESPONSE.json
```

Repeat with `python3 -O` and a separate output directory. The actual merge pin is deliberately fixed. **Ready within the checked integrated structural/review-binding scope.** Actual postmerge results remain pending in the supplied receipt; a later terminal supplement must preserve that historical observation rather than rewriting it. No native-human or whole-language acceptance is inferred from either PR tests or integration.
