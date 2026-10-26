# PR176 exact-head terminal evidence

[PR176](https://github.com/c933103/AN-Paint/pull/176), reviewed head `a365f4b552448803c0bb48b3c44cdf508550eaf9`, passed all six checks in [run 40307905242](https://github.com/c933103/AN-Paint/actions/runs/40307905242). Exact-head Code review is clean; optional Security also completed without findings and is not a required merge gate. This is PR evidence, not actual develop integration or postmerge evidence.

The tested synthetic merge `a789c572e173dcdd5a43ee1b290432d10a6c773e` has ordered parents `05607f0d60131cc9148461ce595155d820748e4e` plus the reviewed head and exact tree `65afa7b96a83c08e0ae08365166dec0520694356`. All 1,373 source blobs and 1,370 packaged tracked files were verified, with three explicit dotfile exclusions; embedded and external source ZIPs match. Additional generated/vendor members are counted, not authenticated by the project Git tree.

Actual hosted results:
- JUnit: **1358 tests** in 146 reports, zero failures/errors/skips. All seven focused source-method sets match, including the two new Catalan/Romanian methods and the seven-method DerivedExport suite.
- Hosted Python: **1381 run = 1379 passed + 2 skipped**, 221.729 seconds. Skip identities are not named in nonverbose output and are not guessed. Local ordinary and optimized 1,381/zero-skip results remain separate in r04.
- Lint: **0 issues**; all four recorded phase exit codes zero.
- API35: **45 app + 74 native** exact source-case sets passed; actual prebuilt main/test APK and source identities were revalidated.
- All **13 exact-script probes**, including the expected reserved-variant rejection, have matching hashes and expected exits.
- All **256 scoped compiled values** match: 10 ca + 10 ro new, 78 da + 78 no + 80 nn prior. Debug signature v1/v2 verifies.

APK SHA-256: `ffe367b92562f2286542303f9802cd34677cf99b5cbf0bf9dee60d8eafb2f733`. Corresponding-source ZIP SHA-256: `626118e88c1e8509b9410ca3b89c4441cc4b1e32f2c4b997f2362228d0e16efe`.

The verifier harness passed four synthetic positives and 32 negatives in ordinary and optimized modes; mocked tools in those synthetic checks are not hosted/runtime evidence. Actual artifact receipts above are separate. A local extraction initially exhausted temporary storage; copied evidence was hash-verified onto available authorized storage, partial bytes retained, and unchanged archive verification passed. This was not a CI failure or tool denial.

The 20 missing-only values retain bounded AI linguistic/static acceptance, not native-human or whole-locale certification. All 254 inherited values, ten explicit held absences, mixed/fallback labels, paired P1/frozen history, #56/#113/#159 and Help/archive/release pauses remain unchanged. New runtime tests exercise actual dialogs/cancel, ordinary Save and real export preserving dirty state and the original non-null Save target/bytes. Export-notice and chooser-failure wording has compiled/static checks; those branches are not claimed newly exercised. No physical-device, layout, private signing or release claim. A final live base/head lease is still required at merge.
