# Translation handling: successful postmerge verification

Ordinary integration commit: `4355869e2e198b5616419291cba225b018444fab`  
Tree: `b9b148d5d8ef7c7b088500a9c177f9f59304b800`  
Parents: `1c9b71afb5f5cbde39bc5fff70630bca1a7a3419` and reviewed PR114 head `384063f65aaeabc08a0f633d795da4fd28d57e76`.

All six jobs in the natural push-triggered [run39547541573](https://github.com/c933103/AN-Paint/actions/runs/39547541573) completed successfully. This was ordinary backlog integration. No release workflow, version bump or publication was requested by this verification work.

## Independently inspected raw results

- 1,098 Python contracts; 205.840-second phase, exit 0.
- 1,311 JVM cases across 137 suites; zero failures, errors or skips. Phase 725.776 seconds, within the unchanged 20-minute cap.
- Native lint preparation 63.193 seconds; lint 114.257 seconds; exit 0 and zero issues in the lint XML.
- All 13 clean/incremental resource-generation probes passed their expected outcomes, including companion source add/remove, alias/plural/literal behavior, stale cleanup and expected reserved-overlay rejection.
- API35 complete composed app union: 45 of 45 cases. Library: 74 of 74 cases. No missing/unexpected/error cases; all declared cases are represented in the raw reports.
- Verification APK/source and test-APK identity are bound to this exact merge, run and device-test inventory.

API35 APK SHA-256: `a5c9be52be0a32baba975c4eeaf4277ec4bb48602b97bc00fc8ae5fa719928f0`  
Corresponding source SHA-256: `fb64309c3a39a8b00f373105df9a800cb274cfe63c5c123fb010648644f02c66`  
App instrumentation APK SHA-256: `e90f7ed516ef4fee7a679e6938096645601a95fc3c71141747b7276f24b53a64`.

The merged tree is identical to the fully reviewed/tested head. [Premerge terminal receipt](https://github.com/c933103/AN-Paint/blob/2a7d41131121fbd8781834a68065ed08908ec658/verification/translation-runtime-current-20261021/COMPOSED-384063f6.md) preserves the exact-head Code/Security completions, premerge CI and earlier local/compiled-catalogue evidence. This postmerge run adds a successful actual-develop verification, not a replacement for those reviews.

## Retention and scope

The compact archive contains raw JUnit XML, suite/case summary, lint reports, timed phase logs, API35 JSON/XML/instrumentation results, exact resource-generation archive, source/APK identities and Actions run/job/artifact metadata. Downloaded archive SHA-256 values were checked against GitHub's artifact metadata. Large build products, screenshots, duplicate HTML reports and device logcat are not duplicated; durable test receipts remain available if the original Actions artifacts expire.

This covers the executed test matrix, not every device/API or linguistic completeness. All current CI budgets and the merged vertical-feedback behavior were preserved. Arbitrary provider/caller text remains data; no translation strings were rewritten to hide unsafe formatting. The independent lifecycle/Czech follow-on work is outside this receipt and needs its own exact-head verification.

[Compact raw archive](postmerge-terminal-4355869e.zip), SHA-256 `8743636ee9f0928c313be6da8c7698651acad5bd3492ce7bb36254816fdb62a6`.
