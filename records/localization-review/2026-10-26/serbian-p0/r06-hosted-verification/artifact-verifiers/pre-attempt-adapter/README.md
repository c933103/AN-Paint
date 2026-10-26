# Serbian PR180 artifact verifier preparation

These tools validate exact-source artifact bytes and narrowly scoped runtime results. Preparation and synthetic controls are not an Android build, hosted CI pass, linguistic review, deployment or release.

## Current source binding

Corrected immutable staged commit: `6b7cbfceefe66f7a78a46e792f57b49455384e18`; tree: `385bd19a6cd68c7b8ce9644f157e4acb4e4cf93e`. The parent verified that Git object. **The branch had not advanced when this preparation was made.** Do not relabel it as the published PR head or as a tested commit. Reconcile actual live head, workflow head, PR test-merge parents/tree, artifacts and digests separately before any real verification.

The source contains 1,385 tracked paths, with 1,382 expected packaged tracked paths after the three explicit established exclusions. The corrected source differs from the original PR180 head only in the numeric display test and its host guard; production resource/linguistic fixture values are unchanged. Original-head preparation directories are historical, not current corrected-head evidence.

## Checked scopes

- APK: exact packaged tracked bytes, Git blob/tree identities, executable modes, external/embedded source identity, build/run identity, artifact digest, and v1/v2 CI debug signature.
- Compiled resource entries: **1,288**, divided into **148 new reviewed Serbian values**, **548 prior reviewed values**, and **592 inherited preservation-only values**. New Serbian counts are 74 per script; inherited Serbian counts are 170 Cyrillic and 168 Latin. Prior SK/SL contribute 156 reviewed and 254 preserved values; prior CA/RO/DA/NO/NN contribute 392 reviewed values. No inherited value is promoted to linguistic acceptance.
- Script configurations: only `(b+sr+Cyrl)` and `(b+sr+Latn)` represent the targeted project catalogues. Generic `(sr)` is deliberately ignored, even when the APK also contains it. Missing, substituted, swapped or duplicate explicit configurations fail.
- Two inherited `ui_save_a5d0d9` entries are symbolic `@string/ui_save` references, not quoted text. Verify both the exact symbolic target and its exact same-script scoped display. A quoted lookalike, changed/omitted target, direct-display substitution or cycle is rejected. The receipt distinguishes reference identity from resolved display hashes.
- Regression: all actual XML test identities/counts/statuses and phase receipts, plus source-derived methods in 12 focused classes. Serbian and SK/SL each have eight methods; NumericDisplayLocaleTest has six. No full JVM aggregate count is inferred from these classes. Hosted Python skips remain explicitly skipped, not credited as passes.
- API35: real exact-source app/native validators and prebuilt APK/source/test-APK identity; source expectations are 45 app and 74 native methods, not executed results.
- Exact-script: 13 source-bound probes, the expected negative, logs, ordering, source mirrors, restoration and companion-change hash contracts. Generated XML bytes are absent from this artifact, so fallback verification is the source-bound producer's assertion and artifact relationships, not independent generated-byte readback.

## Run order

1. Derive source expectations with `prepare_source_expectations.py --source-root SOURCE --base-tree COMPLETE_VERIFIED_TREE --out FRESH_PREPARATION --source-head COMMIT --source-head-status EXPLICIT_STATUS`. Use the complete corrected tree, especially if files are added later. Compare the reconstructed tree to the independently verified remote tree.
2. Run `test_artifact_verifiers.py --source-root SOURCE --tree-file COMPLETE_VERIFIED_TREE --expected-tree TREE_SHA --source-head COMMIT --out FRESH_OUTPUT`, ordinarily and with `python -O`, using a task-local temporary directory.
3. Independently reconcile actual GitHub head/tested-commit/tree/parents/run/artifact IDs and downloaded archive hashes. CLI arguments are not evidence of that provenance.
4. Run `verify_apk_artifact.py` first against the downloaded `apk-and-source.zip`, source, complete verified tree and existing aapt2/apksigner tools. It creates the APK/source/compiled-resource receipts.
5. Run `verify_regression_artifact.py` and `verify_exact_script_artifact.py` against their distinct downloaded artifacts with exact run/source/artifact identities.
6. Run `verify_api35_artifact.py` only with the already APK-verified app/source, exact test APK archive and composed API35 archive. Use a fresh extraction directory; old successful receipts cannot be silently reused.

Each script's `--help` specifies its exact arguments. None discovers credentials, downloads artifacts, modifies repository state or changes production source.

## Preparation history and limitations

The initial string-only parser would not have represented the two inherited Serbian symbolic aliases. This was caught by checking actual prior APK aapt output **before any PR180 artifact verification**. The final parser preparation checked all 338 unchanged inherited Serbian entries in that prior output, including exact explicit script configurations and aliases. This validates parser handling only and establishes no current PR180 runtime outcome. `existing-aapt-parser-preparation.json` records its hashes and limits.

Original-head ordinary controls initially passed 4 positive / 55 negative before alias controls were added; the alias-aware original-head pass rejected 60 negatives. They are retained separately and are not the corrected-head verdict. Current corrected ordinary/optimized results and script hashes are in their dedicated receipts. Synthetic APKs/signature output/run identities are fabricated test fixtures; the API35 coverage validators are stubbed only in those synthetic controls. Real API35 verification imports unmocked exact-source validators.
