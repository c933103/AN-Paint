# PR #40 legacy workflow reconciliation

## Original failure remains recorded

The original head was `1fa0bea0105ac03c3873d1b70988135608d9e77b`. [Run 38024059774](https://github.com/c933103/AN-Paint/actions/runs/38024059774), [regression job 114131020866](https://github.com/c933103/AN-Paint/actions/runs/38024059774/job/114131020866), failed `test_api30_omission_and_phase_deadlines_are_explicit`: the test required the literal `API35-only; both phase classes excluded on API30`, while the shell correctly parameterized the actual API. Its Python result was 366 tests, one failure, two skips. That historical run is still failed.

`original-contract-failure.log` reproduces the exact original source failure locally. No passing rerun overwrites it. `original-ci-excerpt.log` retains the original Actions failure/count lines.

## Reconciled source and exact limitations

This repair merges current `develop` at `691f8870649a1d21d1441f4e3d0e795660b23e9a` into the existing PR branch. It preserves that source, standard workflow, release metadata, and the current API 30/35 phase split. No default-branch publication or merge is performed.

The old exact-text assertion is replaced by executed driver checks for APIs 21, 24, 30 and 35. The API35 restart gate, exclusions, deadlines, failure propagation and actual omission text are checked together. Startup selection checks cover both x86 ABIs, expected SDK/ABI rejection, package-manager commands, keyguard behavior, and the existing 180-second legacy versus 120-second current readiness budgets. These are host fakes, not device tests.

Reconciliation exposed an additional real contract mismatch: the current app partition verifier accepted only API 30/35, while every ordinary app class is SDK-ineligible on API 21/24. Current source inventory is:

- API 21/24 native/import: 73 eligible methods; Ultra HDR is SDK-suppressed.
- API 21/24 app: 23 SDK-suppressed methods, two explicitly excluded API35-only restart methods, zero selected or completed app methods.
- API 30 app: 22 selected methods in ordinary/gallery/vertical phases, one SDK-suppressed method, two explicitly excluded restart methods.
- API 35 app: 25 selected methods including the restart pair.

These are source counts, not newly observed device pass counts. No SDK annotation or instrumentation-method body is removed, changed or relaxed.

Legacy app phases now emit explicit `NOT RUN` status files. Source validation produces `app/coverage.json` with `success: null`, `execution_status: not-run-no-sdk-eligible-selected-tests`, `receipt_scope: sdk-ineligible-app-omission`, zero selected/completed tests and separate suppression/exclusion identities. It never fabricates a successful empty instrumentation summary or an app/gallery/vertical pass. Any newly eligible ordinary, gallery or vertical method fails closed until the legacy execution plan is updated. Stale/foreign app summaries also fail and clear old success receipts.

The native/import runner remains strict: missing, skipped, failed, duplicate, foreign, incomplete and timed-out eligible tests remain failures. API 30/35 native/ordinary deadlines remain 180 seconds; gallery remains 90 seconds; each vertical shard remains 180 seconds; restart seed/verify remain 60 seconds. The 36-minute regular execution step and its source-bound arithmetic are unchanged.

## Verification

- Original red test reproduced before modification.
- Normal host suite: 552 tests passed, zero failures. A final receipt-label clarification was followed by the focused final checks and the final optimized whole-suite run recorded separately.
- Final exact-source whole host suite under `PYTHONOPTIMIZE=1`: 552 tests passed, zero failures (216.119 seconds).
- Final normal focused suite: 13 tests passed, including the production driver, current timeout model, and all legacy contract checks.
- Optimized legacy-focused suite: six tests passed, including normal, `-O` and `PYTHONOPTIMIZE=1` CLI paths.
- Seven mutation controls were all rejected, without harness errors: API30 restart enabled, Ultra HDR exclusion reversed, native deadline relaxed, SDK-ineligible editor invoked, stale API30-only status wording, wrong ABI accepted, and wrong SDK accepted. See `negative-controls.json`; rerun `mutation_controls.py` from the repository root.
- Both workflow YAML files parsed; every embedded shell run block and `tools/ci_emulator.sh` passed `bash -n`. `git diff --cached --check origin/develop` passed for the PR delta. Inherited historical evidence remains byte-for-byte unchanged.
- `source-manifest.json` binds the reviewed code/document inputs by SHA-256.

The final optimized host result and final focused result are recorded in their accompanying logs. Fresh exact-head Code review, Android CI and actual manual API 21/24 runs remain separate required evidence. No legacy emulator run, physical-device verification, editor compatibility pass, release readiness or merge approval is claimed by this report.

The new workflow is still manual-only. Its regular Actions dispatch requires registration on the default branch; this repair does not merge it just to obtain a run. Standard PR CI is not an API21/24 run.
