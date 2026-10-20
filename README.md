# Current-develop combined Unicode-minus verification

PR: https://github.com/c933103/AN-Paint/pull/155
Exact combined head: `3fa741c06e8116443e8de3adbf82a3439ff177fc`.
Incorporated develop: `23e95c76161d8a84fe2f62df2b13f20e5c8aa8e7` (Czech PR #156).
Combined tree: `69a1aebdfe35feefd7292d1b47cc6ef3450f57f9`.
Hosted PR merge source: `e57baf7a0bcf4598564e3010d2750a87ca3d6c80`.
Run: https://github.com/c933103/AN-Paint/actions/runs/39476623276
Artifact ID: `12290380951`.
Original artifact SHA-256: `f1bb042dc7addcbf0b74b6090363bf5c57fcc536cd1e989028ccc608aacc687a`.

## New combined evidence

- All 1,264 hosted JVM tests passed across 133 suites, with zero failures, errors or skips.
- All 5 CzechExtendedWordingTest, 35 LocaleNumberInputTest and 9 UnicodeMinusInputTest executions passed together on this current-base composition.
- Hosted Android lint passed. The raw JVM and lint logs are retained here.
- Local combined host checks passed 1,082 tests in normal mode and 1,082 in optimized mode. Focused checks passed 42 tests: numeric 3, Czech 22, shared localization 14 and position translation 3.
- Fresh exact-head Codex code review completed with no findings. The security summary still pointed to the older source head when this receipt was created, so it is not being counted as refreshed security review.

The new Unicode-minus-specific cases are hosted Robolectric/JVM tests on SDK21/25/35, not installed-device paste tests. The all-offered-locale test also covers SDK30. API35 installed-device suites run separately in the linked workflow; this receipt alone does not claim their completion. Local JVM/Android execution was unrun because the Gradle distribution download could not start.

## Composition and preservation

The complete source tree was verified locally and remotely: 1,273 leaves, including executable modes. All 30 Czech files exactly match the incorporated develop commit. All four numeric production/test files exactly match previously reviewed fixed head `36c20df8044c79b3da308bc2149bdef6e5cb72c5`. Relative to current develop, this PR still changes only those four numeric files. Existing Czech scope holds and review receipts remain intact; published 0.0.40 is unchanged.

This current-base integration was completed in the same PR, not by an alternate PR or an indirect merge to develop. It provides materially new verification after the earlier guarded merge was not executed for lack of current-base composition checks. Only the parent may consider a normal guarded merge after all required current-head gates pass.

## Raw report binding

`all-jvm-results.zip` contains unchanged XML bytes for every suite extracted from the hash-verified combined artifact, with new archive packaging only. Individual Czech/numeric XMLs and JVM/lint logs are unchanged artifact files. The JSON summary is a derived count/source binding, not a replacement for those raw results.

Earlier immutable evidence remains distinct:
- [Expected-red baseline](https://github.com/c933103/AN-Paint/tree/8138fa0f95dccc1696d756fb5587122d01eb9d08).
- [Old-base fixed result and complete red/green JUnit suites](https://github.com/c933103/AN-Paint/tree/a4a5dc20be720536b3a5f7b2165ccf39ce0be5cf).
