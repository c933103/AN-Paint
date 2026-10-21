# PR157 exact-head terminal CI verification

Verified 21 October 2026, 02:50 UTC. [PR #157](https://github.com/c933103/AN-Paint/pull/157) head `23f88311d8a8a28903975758751e6cf88a3ad536` remains the two-file 0.0.41/code 98 change. Natural PR [run 39532712417](https://github.com/c933103/AN-Paint/actions/runs/39532712417) passed all six applicable jobs.

The workflow head is the PR head. Its checked-out synthetic merge source is `90da56bfc5fbb83b7a924243b079560f30fd5393`, with parents `9a7a052d7458cf08f280ead1173c66c2992e4254` and the PR head. The synthetic merge tree exactly equals the reviewed candidate tree `5fa767ed5bb57364a1ca4bd3cab95cae36187847`.

## Independently checked raw reports

- Regression artifact `12316343359`, 84,007,876 bytes, SHA-256 `24fcec42f8967ac8a9add059e8a4acadd65dbdb474b879a595631658dfcadf53`: 1,264 JVM tests in 133 XML suites, no failures/errors/skips; debug lint has zero issues. Czech, shared numeric-input and Unicode-minus suites contain 5, 35 and 9 successful executions respectively. These are hosted Robolectric/JVM results, not installed-device paste or physical-device proof.
- Final API35 artifact `12316847443`, 11,361,954 bytes, SHA-256 `0b7d9f4619bf51f7e60884c26e65cfc4e3087f3fbde8e4909a99583bc0fb61cf`: current-source disjoint inventories match all 45 app and 74 Paintroid selected tests. Unmodified source inventory, report, export, screenshot and reachability validators reproduce 32 matrix screenshots, eight reachability cases/64 frames, 104 vertical data files and 12 dialog exports. Both core and position inputs are attempt 1 of this run.
- Exact-script artifact `12316078490`, 7,775 bytes, SHA-256 `f5dd941a21ae4f08f8a9e3a09cea70fc385c9d42090c1489d4be4a94a51251d8`: all nine probes exited zero; every raw log hash and producer-defined root-build/wrapper-properties hash matches current source. The complete small raw artifact is retained here.

API35 report identities agree on CI APK SHA-256 `c43fbff926113ce0abd20cdf6c737656b55414565c14a428e3e40016f42f3882`, source SHA-256 `b9f87122a874aa7533c456df935af655be6e26aa07c0f61648f1a19a29932a83` and test APK SHA-256 `9fe3c23a533b5008236d739792b96c226a8d221ca8d217fcd579d94ad917f3db`. These identities were checked between reports; actual delivery APK/source bytes were not independently downloaded at this PR checkpoint. The future release stage must perform its own full artifact-byte/source/signature verification.

`pr157-gates.json` preserves terminal run/job/artifact metadata. `pr157-report-verification.json` records source-aware checks, inventories and limits. `pr157-focused-jvm-receipt.json` records exact target-suite hashes. `pr157-raw-report-receipts.zip` preserves every JVM XML suite, lint XML, phase logs and API35 JSON/XML receipt with a per-file manifest; it is not a duplicate of every PNG/export ZIP. Full CI artifacts retain their original 14-day retention.

## Remaining gate and release boundary

At this checkpoint Security review is completed without findings on the exact head; Code review remains running. Do not merge on CI alone. [Current exact-head review state](https://github.com/c933103/AN-Paint/pull/157#issuecomment-6306440505) must be checked when deciding the merge.

This is debug/API35 PR verification, not the later release/API30+35 run. The actual merge subject must begin `Release ` to select the full release pipeline. No signing or publication request changed, and 0.0.40 remains untouched. All Czech, Swedish, Afrikaans and broader language/UI holds remain explicit; original failed attempts are not rewritten as passes.
