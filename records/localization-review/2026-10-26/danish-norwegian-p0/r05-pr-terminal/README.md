# PR175 terminal gates and source-bound artifact verification

Exact head `f6b3e71fd1261935c4d97b20cbbbdcc79ed398ed`, tree `16ff3d877650ad4ad3198ce19007e8606fcd080a`, passes all six checks in [run 40291904610](https://github.com/c933103/AN-Paint/actions/runs/40291904610). Exact-head Code review is clean ([receipt](https://github.com/c933103/AN-Paint/pull/175#issuecomment-6411577761)); optional Security is also clean, not represented as a required gate. Inline findings: zero.

Actual tested PR merge `4f345c48f6502ef1fc98a480f83e6cd241d98d5a` has verified parents df9bc04 + f6b3e71 and the identical head tree. All 1,370 local Git blobs match that tree; 1,367 packaged project files match exact bytes with only the three documented packager dotfile exclusions. Embedded and external source archives match. Extra vendored/generated source members are counted separately, not claimed to be authenticated by the project Git tree.

- Compiled resources: 78 Danish + 78 Norwegian newly reviewed values and 80 prior Nynorsk values match exactly; CI debug signature v1/v2 verifies.
- Hosted JUnit: **1,355 unique tests**, 145 XML reports, zero failures/errors/skips. All six focused source-method inventories match actual reports.
- Hosted Python: **1,374 run = 1,372 passed + 2 skipped**. Non-verbose output does not name the skips; identities are not guessed. Separate final local ordinary/optimized runs in r04 each passed 1,374 with zero skips.
- Lint: zero issues; all recorded phase exit codes zero.
- API35 composed evidence: **45 app + 74 native** exact source-bound cases passed, with APK/test-APK/source/prebuilt identities revalidated. This is existing emulator regression coverage, not locale-specific physical-device/layout certification.
- Exact-script generation: all 13 probe hashes/expected exits verified, including the intended reserved-variant rejection.

The scripts and their separately labelled synthetic sanity checks are retained for reproduction. Artifact IDs and raw archive SHA-256 digests appear in terminal-gates.json and per-artifact receipts. Execute scripts with the pinned checkout, matching tree response, downloaded named archives and stated verification tools; do not reuse a stale API35 extraction directory.

This snapshot establishes PR merge eligibility, subject to the live base/head lease. It is **not postmerge evidence**. No release, native-human, whole-locale or layout certification. All held absences, historical/qualified scopes, paired P1/frozen history, #56/#113/#159 and Help/release pauses remain unchanged.
