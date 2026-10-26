# PR179 coverage finalization handoff

This preparation is not actual postmerge success. Do not run final mode until all six actual jobs and fresh artifact validators are successful.

## Evidence join repair

The initial generic receipt join incorrectly required fields absent from producer schemas. The compiled-values receipt has no artifact ID, so it now joins to the APK/source receipt through exact APK SHA256, run, tested commit and that receipt's verified artifact ID. The regression receipt has no source-tree field, so its exact tested commit joins to the actual merge and APK source tree. No fields were inserted into or changed in original receipts. Every present identity and artifact digest remains checked. Every referenced receipt must belong to the pinned manifest.

Synthetic tests: nine cases pass in ordinary and optimized Python, including 28 individual identity corruptions plus missing families, cross-artifact association, APK-byte hash and archive digest corruptions. The original six tests retain their 39 terminal-envelope mutations and XML/Git/path controls. The first new test run had a test-count expectation of 29 instead of 28; all actual mutation checks rejected as intended. The count assertion was corrected, and the original failed log remains local. It contains an execution path and must not be published verbatim.

Fresh source previews are byte-identical in ordinary/optimized Python, and independent DOM reconstruction matches all 171 rows and totals. Base is e5f2d4e2d07e678076f022aa7b3ef923e13c3721, not an older CA/RO snapshot. Only sk/sl change.

## Final sequence

1. Finish actual postmerge artifact checks and stage the immutable actual terminal package with its manifest. Keep its original receipt bytes untouched.
2. Run prepare_terminal_envelope.py against the PR evidence, actual evidence, terminal status and merge identity, with the actual manifest SHA256. Write the resulting envelope into a separate fresh join directory.
3. Copy the already verified actual terminal package into that join directory, preserving the original manifest and receipt bytes. The envelope is validated as a join object; it is not retroactively inserted into the original immutable manifest.
4. Run coverage-preparation/recompute_coverage.py with the existing inputs, current source, base-source, a fresh output directory, --mode actual-postmerge, --actual-evidence pointing at the join directory, and --actual-manifest-sha256 equal to the original actual-package manifest hash. Repeat with python -O to another fresh directory. Compare the output bytes.
5. Run coverage-preparation/verify_independently.py on both outputs with --mode actual-postmerge --expected-merge e1e5433e63d45f5b76d39ce1a31ffc11fd7cd79d --expected-run 40366731196. The default mode stays preview; final mode demands these explicit expected identities and the successful terminal supplement.
6. Publish final coverage only after these joins succeed. Include the original source, linguistic and CI qualifications. No new native-human, whole-language, layout, physical-device or release certification. No release. The separate PR178 pending upload is not retried, replaced or claimed public.

The old preparation-manifest.json remains an immutable record of the earlier preparation. The schema-join-supplement-manifest.json identifies the corrected helper scripts and new test results; do not use the old manifest to claim the edited helpers are unchanged.

## Public reproduction dependency

Five original PR178 baseline payloads have deliberately been omitted from this publication because its original blob request remains unresolved and the exact pending target is unknown. baseline-dependency-inventory.json identifies their original input paths, byte lengths, SHA256 and Git blob hashes without including or transforming their payloads. The computations above were executed with the independently validated local dependencies; reproducing them requires those local dependencies until the original publication resolves. No pending upload is duplicated.
