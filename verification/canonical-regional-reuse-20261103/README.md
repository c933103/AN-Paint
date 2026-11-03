# Canonical regional catalogue preflight correction

Local qualification against develop5a52e80237e41f53cb96f665be609a0f3045b9a5, source tree4baef8e0bb9614a7b737e04f360862b208a0c3a1. Three changed files: classifier, existing behavior tests and CI policy documentation. This is preparatory evidence; no hosted qualification or merge claim.

The old path regex excluded hyphenated regional values-fa-rIR. The correction uses canonical catalogue_paths() and the existing language picker rather than a broad values* spelling match. It keeps default strings and picker-backed canonical catalogues eligible. Non-picker catalogues remain conservative full fallback. Both picker and resolver remain immutable producers. Every before/current tracked path and mode must still match, and every other blob remains unchanged. Review, artifacts, provenance, immediate-merge identity, branch policy and race checks remain mandatory.

Full host suite:851 tests/285.178s, exit0. Affected transport/selection/composition:39 tests/5.003s, pass. Focused transport:12 tests/0.596s, pass. Three intentionally broken copies fail the existing end-to-end preflight test: old regional-exclusion regex; broad values* exemption; missing path/mode equality guard. Their logs contain expected failures. The full host log also contains expected negative instrumentation diagnostics from simulated cases, while the unittest terminal result is OK.

The policy-introducing merge must use normal full execution because classifier/test/documentation producers change. Only later qualifying resource merges may reuse prior evidence. No additional Android build or benchmark was launched to demonstrate reuse.
