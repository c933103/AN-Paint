# PR178 corrected head — terminal required gates passed

Exact reviewed head `82995ec1f030d23cb4e2b1426b511abe802890eb`, base `ce796879f4568a27b9d905a8e8db639dd0a93a30`, source tree `806d9577409c4044212d1c12e6e38da46417bae6`. Fresh [run40346532936](https://github.com/c933103/AN-Paint/actions/runs/40346532936) completed successfully. All six current-head check-runs passed; the live PR was ready/open/mergeable with unchanged head/base and no inline comments at eligibility verification. This is **PR evidence**, not an actual postmerge run.

## Actual source-bound results

- **1,366 JVM tests, 148 XML files, zero failures/errors/skips.** All ten focused class/method sets match source, including all six NumericDisplayLocaleTest methods and five new completion methods. The formerly failing Romanian literal oracle now passes without changing the translations or weakening numeric/admission checks.
- Hosted Python: **1,398 run / 1,396 passed / two unnamed skips**, 219.299 seconds. These are separate from local ordinary and optimized runs, each 1,398 with zero skips. No skipped identity is guessed.
- Lint: zero issues; all phase exits zero.
- API35: **45 app + 74 native exact source identities**, passing with source, main APK and prebuilt test APK binding. Emulator execution is not physical-device, native-human linguistic or whole-language certification.
- Exact-script: 13 probes plus expected-negative behavior verified.
- All 1,376 packaged source files match the 1,379-file Git tree after the same three exclusions. The test commit `047d6f04cd88ae879f8f87316efeadc9f3e159fd` has exact ordered base/head parents and identical tree.
- All **392 compiled bounded values** match exact approved fixtures: 110 new CA/RO completion values + 282 prior values, disjoint. No global or Valencian direct review is inferred. CI debug v1/v2 signatures verified; no release signing.

APK SHA-256: `5c339021d12a04ac537faca20af6f14686ee44dbe33c86a42aa8dd771420c96b`. Corresponding source ZIP SHA-256: `97ecc89f2a6970330a0b35d199ad9b1b02c2ac505cfe9b2d4679adf2a8b3ce9b`. Archive IDs and API digests are in `run-review-artifact-identity.json`; no temporary download URLs are retained.

Exact-head Code receipt [6419705822](https://github.com/c933103/AN-Paint/pull/178#issuecomment-6419705822) and full-SHA summary6418589155 are clean. Optional Security remains the prior-head93f27ed receipt with merge gate disabled; it is not promoted to current-head acceptance or required as an extra gate.

## Reproduce and preserve history

Use the exact source, Git tree and four verifiers published in [r05](https://github.com/c933103/AN-Paint/tree/79192cbafad86f7c582f357844efe8fb8cf7eb2e/records/localization-review/2026-10-26/catalan-romanian-p0-completion/r05-numeric-oracle-repair/verifiers). Supply the actual tested commit, reviewed/workflow head, tree, run/artifact IDs and digests from this record; its README gives exact commands. The fixed verifier covers ten source-derived focused suites and preserves synthetic positive/negative controls separately.

The original required failure in run40340230583 remains in r04; the two local harness loader failures and all repair/source audit evidence remain in r05. No failed evidence is overwritten or relabelled. The r03 display-log hygiene correction is explicit and retains raw hashes.

Only the 110 independently reviewed missing values enter this batch; all 300 inherited pairs, ten no-current-consumer holds, mixed English composition labels, paired120/60/P1/frozen/global59/112, inherited Valencian routing and PR56/113/159/Help/archive/release boundaries remain. No release. Actual merge identity, fresh push artifacts and integrated coverage must be verified separately.
