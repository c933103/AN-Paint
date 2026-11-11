# PR #428 final qualification

PR #428 merged as `51ca0b7abf9b6ba824411ebea98b74d39672859d` at 2026-11-11 03:54:48 UTC. Actual develop was verified at that merge, with ordered parents `7915ed52a868ba2bc2b5dbceaf98afd74a830481` and `6e53e3849fd0d6b31381cfde772add94e508ced1`. Its complete tree `accef4f4d0ab0cf3ffaafb11e316d6ba4be17ab4` equals the exact reviewed and tested source.

- Original exact-head run: https://github.com/c933103/AN-Paint/actions/runs/42952737261, attempt 1, successful.
- Review: https://github.com/c933103/AN-Paint/pull/428#issuecomment-6786098229, exact-head code review completed with no findings; exact-head security marker completed; no inline threads.
- Results: 865 Python passes and two optional-image skips; 1,392 JVM passes; clean lint; 13 exact-script probes; 74 native and 50 composed app API35 tests. The existing source-bound app inventory validator independently accepted the final archived reports.
- APK, corresponding source, instrumentation APK and final regression/composed report digests were verified. The prior checkpoint's complete source comparison remains valid because no tree changed.
- Post-merge run: https://github.com/c933103/AN-Paint/actions/runs/42955811987, successful. Its verified receipt accepted the original PR evidence under the existing immediate-merge policy. Six regular jobs were skipped, not newly executed or double-counted.
- All 17 other open PR heads were reconciled unchanged before merge. Existing holds, including the eight gallery-redirect clauses, remain unchanged. No held or stacked source was imported.

`qualification.json` is the concise record. `qualification-evidence.zip` preserves 244 members: original regression/JVM/lint records, composed device JSON reports, exact-script artifact, immutable run/artifact metadata, review, and original post-merge receipt. It omits bulky APKs, screenshots and unrelated diagnostics. Archive SHA-256: `9c5fd659d160aa31dea8575b63fd10a7c7043c287a38f95e964715357d9f0402`; Git blob: `6ef5d44695618eea2f34d1c84d7f0e9469c43cdc`; 406,033 bytes.

These are source-bound CI/debug-key results, not private upgrade signing, a release, native-human linguistic review, exhaustive installed layout/glyph/speech acceptance, or an API30 run. Previous language-review withdrawals and all independent holds remain in force.
