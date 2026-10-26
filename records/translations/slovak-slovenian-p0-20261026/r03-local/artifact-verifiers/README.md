# SK/SL artifact verifier preparation

This package verifies future exact-source PR and actual postmerge artifacts. It does not transfer any prior run's success and establishes no current hosted, Android, native-human, whole-language or release result.

## Prepared scope

- Staged source tree: `98b89d126533df3c0dbaeb729c74e4bcb44a3a8a`; 1,382 tracked paths, 1,379 expected packaged tracked paths. Recompute after any source change.
- Frozen reviewed fixture SHA-256: `6b1256111320bed7b63df4323ce989770ca4a6375a974b91455f4665f5529594`.
- APK checks: all tracked packaged bytes, reconstructed Git tree, executable bits, embedded/external source identity, build/run identity, artifact digest, v1/v2 CI signature; exact displayed resources: 156 new SK/SL, 254 inherited SK/SL (preservation only), and 392 prior bounded CA/RO/DA/NO/NN values. The three unchanged packaging exclusions are explicitly enumerated.
- Regression: source-derived method sets for 11 focused JVM classes, including all eight SlovakSlovenianP0WordingTest methods and six NumericDisplayLocaleTest methods. Full available JUnit identities/counts/statuses and phase exit receipts must agree; Python skips stay explicitly skipped.
- API35: real exact-source app/native validators, composed/prebuilt APK/source identity, native complete case identity and terminal states. The source-selected expectations are 45 app and 74 native tests, not claimed execution.
- Exact-script: 13 source-bound probes, expected negative, logs, task ordering, unchanged generators, source-derived exact mirror hashes, fallback restoration and companion-change hash contracts. Generated XML bytes are absent from this artifact: fallback validation is the source-bound producer's semantic assertion plus artifact hash relationships, not an independent generated-byte readback.

## Verification order

1. Re-run `prepare_source_expectations.py --source-root SOURCE --base-tree BASE_TREE --out FRESH_PREPARATION [--source-head HEAD]`. The three new SK/SL files are added only when absent from the base. Verify this tree against the live remote exact-head tree separately.
2. Run `test_artifact_verifiers.py --source-root SOURCE --tree-file TREE --expected-tree TREE_SHA --out FRESH_OUT [--source-head HEAD]`, ordinarily and with `python -O`; use task-local TMPDIR.
3. Reconcile workflow head, actual tested commit/tree, terminal job/run status, artifact IDs and server digest before invoking downloaded-artifact verifiers. A PR test merge commit and an actual develop merge commit are separate identities. CLI values alone are not independent GitHub provenance.
4. Run APK verifier first. Its directory contains `apk-and-source.zip`; it extracts the app APK, corresponding source and build-info. Pass the verified tree, source, tools directory (`aapt2`, `apksigner.jar`), expected/tested commit, reviewed head, tree and run/artifact digest arguments.
5. Run regression verifier on `regression-and-lint.zip`. Bind its source to the same verified tree. Run exact-script verifier on `exact-script.zip`, now requiring `--source-root` as well as commit/tree/reviewed-head/run/artifact/digest parameters.
6. Run API35 verifier with the already APK-verified `app-debug.apk`, `AN-Paint-source.zip`, `instrumentation-apks.zip`, and `api35-composed.zip`. It refuses a stale extraction directory. Use fresh directories for separate real verification attempts and retain failures unchanged.

See each script's `--help` for full parameter names. No script discovers credentials, downloads artifacts or changes external state.

## Local preparation result

Ordinary and optimized synthetic controls both pass: **4 positive controls, 45 negative controls rejected**. Their identical current receipt SHA-256 is `0cc1a77003b76f6c6265a348c116162658a9ee4ccebd4dfa1bddfdf0a2f124d8`.

Synthetic archive contents, APK/signature output, run/artifact identities and API35 validator stubs test verifier plumbing only. API35 real verification imports the unmocked source validators. No hosted artifacts for the new SK/SL source have been verified by this preparation. `ordinary.log` is retained as the earlier 39-negative pre-extension control result; `ordinary-extended.log` and `optimized.log` describe the current 45-negative checks.
