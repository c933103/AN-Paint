# PR178 repaired-head artifact verification preparation

Bound to repaired staged source tree `806d9577409c4044212d1c12e6e38da46417bae6`; the new reviewed head is not supplied yet. The original head `93f27ed172cc730c80ed7a2ffbcacc1b0c04383f` and its failed run remain historical, never relabelled as passing. Original verifier files are unchanged in their separate directory. **No actual hosted artifact is certified by this preparation.**

## Verified scope

- 1,379 tracked source blobs; expected package contains 1,376 after the same three explicit exclusions: `.gitignore`, `.idea/codeStyles/Project.xml`, `colorpicker/.gitignore`.
- Compiled fixture union is exactly **392** disjoint locale/key values: CA78, RO78, DA78, NO78, NN80. The new completion scope is CA55 + RO55; prior CA23 + RO23 + DA78 + NO78 + NN80 remains distinct.
- Ten focused JVM class method inventories are parsed from source: numeric-display6, completion5, import2, save2, Danish/Norwegian4, remaining Nynorsk4, Nynorsk save2, derived-export7, selection-title12, tagged-colour5. **No full JVM aggregate is inferred**; actual XML determines totals, unique cases and statuses.
- API35 identities derive from current source: 45 app + 74 native. These are expected sets, not executions. The API35 and exact-script verifiers are byte-identical to the prior batch. The production API35 validators and exact-script generator are also unchanged and source-hashed.
- Four synthetic positive controls and 36 rejected negatives pass normally and with Python `-O`; receipts are byte-identical. All prior 35 negatives are retained, plus a missing numeric-display suite control.

## Actual-runtime inputs still required

Use a fresh verification directory with downloaded archives and API-provided SHA-256 digests. Do not use a download URL as a durable identity. Record the workflow run/event/head, artifact IDs, expiration state and digest independently from GitHub before invocation.

- `SOURCE_ROOT`: exact reviewed source checkout/extraction, unchanged during verification.
- `TREE_FILE`: complete, non-truncated recursive tree for `806d9577409c4044212d1c12e6e38da46417bae6` (or the independently verified actual postmerge tree if it differs). `preparation/staged-source-tree.json` is the independently reconstructed snapshot, not a substitute for remote commit/ref verification.
- `REVIEWED_HEAD`: the new exact PR178 head after the test-only repair; do not reuse the original failed head.
- `TESTED_COMMIT`: actual checkout commit. For a PR run it can be a synthetic merge commit: verify ordered parents/base/head and identical tree before treating it as source-equivalent. For postmerge use the actual merge commit and fresh push run, never relabel PR artifacts.
- `WORKFLOW_HEAD`: workflow API head identity. Keep it distinct from `REVIEWED_HEAD` and `TESTED_COMMIT` where appropriate.
- `RUN_ID`, each `ARTIFACT_ID` and API digest; the four required archive basenames are `apk-and-source.zip`, `regression-and-lint.zip`, `api35-composed.zip`, `exact-script.zip`, plus `instrumentation-apks.zip` for API35 prebuilt test-byte binding.
- `TOOLS`: directory containing the known `aapt2` and `apksigner.jar`; their actual hashes are included in the compiled-resource receipt.

### Commands

```sh
python verify_apk_artifact.py --directory "$ARTIFACTS" --source-root "$SOURCE_ROOT" --tree-file "$TREE_FILE" --tools "$TOOLS" --expected-commit "$TESTED_COMMIT" --head "$REVIEWED_HEAD" --expected-tree "$TREE" --run-id "$RUN_ID" --artifact-id "$APK_ARTIFACT_ID" --archive-sha256 "$APK_ARTIFACT_SHA256"
python verify_regression_artifact.py --directory "$ARTIFACTS" --source-root "$SOURCE_ROOT" --head "$REVIEWED_HEAD" --tested-commit "$TESTED_COMMIT" --run-id "$RUN_ID" --artifact-id "$REGRESSION_ARTIFACT_ID" --sha256 "$REGRESSION_ARTIFACT_SHA256"
python verify_api35_artifact.py --directory "$ARTIFACTS" --source-root "$SOURCE_ROOT" --head "$WORKFLOW_HEAD" --reviewed-pr-head "$REVIEWED_HEAD" --tested-commit "$TESTED_COMMIT" --tree "$TREE" --run-id "$RUN_ID" --artifact-id "$API35_ARTIFACT_ID" --sha256 "$API35_ARTIFACT_SHA256" --test-apks-sha256 "$TEST_APKS_SHA256"
python verify_exact_script_artifact.py --directory "$ARTIFACTS" --commit "$TESTED_COMMIT" --tree "$TREE" --reviewed-pr-head "$REVIEWED_HEAD" --run-id "$RUN_ID" --artifact-id "$EXACT_ARTIFACT_ID" --sha256 "$EXACT_ARTIFACT_SHA256"
```

Run APK/source verification first: API35 consumes its exact extracted APK/source archive. The API35 verifier rejects stale extraction. Its current identity contract expects first attempts for core, position and composition; an actual rerun needs explicit source/receipt reconciliation rather than silently accepting a stale group.

Regression verifies source-declared focused method names, unique JUnit cases, status/count consistency, zero JVM failures/errors/skips, phase exits and the hosted Python terminal summary. Hosted Python skips remain separately counted and unnamed when the hosted log omits their identities; they are never promoted to passes. Lint issue counts/severities are reported as observed, not hidden. Source/commit provenance for this artifact also depends on the independent workflow/artifact association and prior exact source validation; caller-supplied labels alone are not proof.

### Reproduce preparation

```sh
python prepare_source_expectations.py --source-root "$SOURCE_ROOT" --base-tree "$BASE_TREE_FILE" --source-head "$REVIEWED_HEAD" --out preparation
python test_artifact_verifiers.py --source-root "$SOURCE_ROOT" --tree-file "$TREE_FILE" --expected-tree "$TREE" --source-head "$REVIEWED_HEAD" --out ordinary
python -O test_artifact_verifiers.py --source-root "$SOURCE_ROOT" --tree-file "$TREE_FILE" --expected-tree "$TREE" --source-head "$REVIEWED_HEAD" --out optimized
cmp ordinary/artifact-verifier-sanity.json optimized/artifact-verifier-sanity.json
```

Synthetic archives, mocked APK-tool outputs and stub API35 validators exist only inside the sanity harness. Real verifier paths retain actual archive/source/resource/signature checks and invoke the current real source validators. No Android/JVM/emulator execution, native-human/physical-device/layout/whole-locale certification, private upgrade-signing or release claim is made here. All existing holds and review qualifications remain unchanged.

The only source difference from the original PR178 tree is the independently audited NumericDisplayLocaleTest literal repair. The regression verifier now requires that exact source-derived six-method suite in addition to all prior nine focused classes. Re-run synthetic controls with `--source-head` after the new head is supplied; until then receipts explicitly say no published head supplied.
