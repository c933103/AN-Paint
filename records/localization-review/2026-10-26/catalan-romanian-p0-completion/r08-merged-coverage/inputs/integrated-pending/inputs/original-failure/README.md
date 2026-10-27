# PR178 original head — required JVM gate failed

**Do not merge this head.** Run [40340230583](https://github.com/c933103/AN-Paint/actions/runs/40340230583) completed with failure at reviewed head `93f27ed172cc730c80ed7a2ffbcacc1b0c04383f`. Its PR test commit `867b4e86919a7b382cf10b5199ef1450093ba500` has ordered baseline/head parents and the exact reviewed tree `571ec84860cb837ae8376f72d0becfb8fd2b7b6d`.

## Actual terminal results

- **1,366 JVM tests: one failure**, zero errors/skips, 148 JUnit XML files. All five new completion tests passed; that does not override the aggregate failure.
- The sole failure is `NumericDisplayLocaleTest.oversizeWarningUsesResourceDigitsAndDecimalsWithoutChangingAdmission`, line 99. Its existing Romanian assertion still expected an English fallback prefix. The preceding exact resource-formatted equality passed; the newly reviewed Romanian value correctly starts “Dimensiunea de 1500 × 2000 pixeli (3,00 MP)…”. This is a stale test expectation, not a translation rollback reason.
- Hosted Python: 1,398 run, 1,396 passed, two unnamed skips. Skipped identities are not guessed from local results. Lint has zero issues.
- All API35 source/prebuilt-bound identities passed: 45 app + 74 native. Build/source and exact-script jobs passed; 13 exact-script probes verified.
- Exact APK/source verification matched 1,376 packaged files against 1,379 tracked files with the three established exclusions. All 392 bounded compiled values matched: 110 new + 282 prior, separate scopes. CI debug v1/v2 signatures verified, not release signing.
- Exact-head Codex Code was clean (receipt 6418698655, full-SHA summary 6418589155); optional Security was clean with its merge gate disabled. Those reviews do not supersede required CI failure.

`failure-analysis.json` and the complete `junit-case-ledger.json` retain every case result, raw XML hashes, failure detail and phase exit identities. Derived records omit runner hostname and infrastructure-local paths; original artifact IDs/digests identify the raw evidence. The unchanged regression verifier rejected this real failed archive with `ValueError: JUnit failure/error/skip`, as required. Separate artifact receipts retain their own success scope, not an overall pass.

## Bounded correction

Update only the Romanian literal numeric-warning expectation to its exact reviewed prefix and retain an explicit 2,25 MP decimal assertion. Preserve the intentionally desynchronized process/resource locale, complete formatted-message equality and memory admission/resident/invalid-size checks. A bounded scan of all changed resource consumers/fixtures precedes the corrected head. No translation or application logic is changed by that repair. New-head review and CI are required; original failures remain here permanently.

All prior linguistic qualifications, inherited values, ten no-current-consumer holds, P1/paired120/60/frozen/global59/112, Valencian routing and PR56/113/159/Help/archive/release boundaries remain. No native-human, whole-language, physical-device/layout certification or release.
