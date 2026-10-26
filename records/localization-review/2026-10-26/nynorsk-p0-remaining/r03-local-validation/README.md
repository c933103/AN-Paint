# PR174: source publication and local validation r03

[PR174](https://github.com/c933103/AN-Paint/pull/174), head `3c8123707106dfc991221517e443276f857797db`, tree `8ca5fc4f3989cf8c9307432d5e5c28ceef698251`.

**Both full local host checks passed separately:** 1,364 ordinary tests (171.931 s), 1,364 optimized tests (171.858 s), zero skips. Focused tests passed 12 Nynorsk + 18 memory-warning + 14 current-contract cases in each mode. The first full local run failed two stale tagged-colour fallback guards; exact failures and narrow repairs are preserved in `local-validation.json`.

All 13 source/test/fixture files and the complete 1,367-blob tree/modes were read back exactly before PR creation. Only Nynorsk strings changed in application resources. Prior 118, five no-consumer holds, the missing P1 warning, paired 120/60 warning oracle and historical queue are preserved. The one-message tagged-colour family is now 66/105; global 59/112 is unchanged.

The [independent reviewed values](https://github.com/c933103/AN-Paint/tree/b4fa13c19f45a66cc701909eb90aa2ee66ed7e4f/records/localization-review/2026-10-26/nynorsk-p0-remaining/r02-reviewed) remain bounded AI linguistic/static judgments. Compiled resources, real JVM tests, lint and API35 require [the current hosted run](https://github.com/c933103/AN-Paint/actions/runs/40279026132), which is **in progress**, not passed at this record. Exact-head Codex review was requested; no merge eligibility is yet claimed.

No native-human, physical-device, layout, whole-language or release certification. Existing pauses and PR56 never-merge remain unchanged. Later CI/artifact receipts supersede pending status, not this historical record.
