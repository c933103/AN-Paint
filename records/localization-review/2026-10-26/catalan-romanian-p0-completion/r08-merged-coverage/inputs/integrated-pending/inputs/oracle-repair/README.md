# PR178 Romanian numeric-oracle repair

Corrected head `82995ec1f030d23cb4e2b1426b511abe802890eb`, tree `806d9577409c4044212d1c12e6e38da46417bae6`, changes **only NumericDisplayLocaleTest.kt** from original head `93f27ed172cc730c80ed7a2ffbcacc1b0c04383f`. All 1,379 file identities/modes were reconciled; the branch advance used the expected original-head lease and exact ref readback. No translation or production logic changed.

The old literal assumed Romanian still used the English oversize-warning fallback. The repair uses the exact reviewed Romanian prefix and independently requires both comma-decimal quantities. The complete resource-formatted equality, intentionally US process locale, resource-locale selection, maxPixels/admission/resident-pixel checks and invalid-size rejection remain. Unchanged English P1 captions stay unchanged. Original required JVM failure remains separately recorded in r04, not relabelled as success.

## Independent bounded review

- Thirteen static repair negatives reject under ordinary and optimized Python, including stale English/dot-decimal expectations and removal of real controls.
- The requested dependency scan covers all 55 changed identities across 506 tracked text/test/helper/fixture files, including 257 partial-literal candidates and ten explicit CA/RO/Valencian JVM classes. Eighty-eight unchanged encoded-image inputs remain separately excluded. No additional concrete stale CA/RO expectation was found. All 110 selected fixture pairs match final independent reviews; no direct Valencian expectation is invented.
- Fixed artifact verifiers preserve all prior checks and add NumericDisplayLocaleTest as the tenth source-derived focused suite (six methods). Four synthetic positives and 36 synthetic negatives pass normally and optimized; these are not fresh hosted execution.

## Actual repaired-source local execution

Focused ordinary and optimized suites each passed 58 tests (3.012 / 3.151 seconds). Full ordinary and optimized discovery each passed 1,398 tests (191.198 / 197.782 seconds), zero failures/errors/skips, and all 1,379 input files stayed unchanged.

Two initial focused invocations used the repository root instead of tools and produced seven module-loader errors each; no targeted test ran in those attempts. They remain explicitly retained as r01 harness failures. Corrected-cwd focused r02 results are separate. The full suites used correct discovery commands and passed individually; the original coordinator exit of one reflects its recorded loader failures, not a hidden full-suite failure. The terminal reconciliation is authoritative.

Host receipts keep raw-log hashes. Public display logs replace generic interpreter installation prefixes with `<PYTHON_STDLIB>`; `host/log-redactions.json` lists exact raw/published hashes and replacement counts. No result or failure is removed. No local Kotlin/JVM/device execution is claimed.

Fresh [run40346532936](https://github.com/c933103/AN-Paint/actions/runs/40346532936) and exact-head Codex request6419510688 are pending in this record. The PR test commit047d6f04cd88ae879f8f87316efeadc9f3e159fd has exact base/head parents and the corrected tree. Old-head Code/CI/artifacts are historical, not new-head passes.

All 110 translation values, 300 inherited pairs, ten holds, P1/paired120/60/frozen/global59/112, inherited Valencian routing and PR56/113/159/Help/archive/release boundaries remain unchanged. No release or expanded linguistic certification.
