# PR186 — exact JVM expectation repair and initial-run evidence

Current candidate: `728ddd062b4fef9e9440978959d85c199da6dccc`, tree `0ad3a1d8e0fb752571027415d268ac65ab301dd9`.
Synthetic PR checkout `7a37c90584769153465d2cb013105cb4cb37eff6` has that identical tree and the expected base/head parents. All 1,396 remote blobs and executable modes match the reviewed checkout; 23 paths differ from the base.

The complete three-language P0/P1 ledgers, 439 exact resource edits, all 171 P0/P1 before/after presence rows and exact holds remain [unchanged from the source-bound review package](https://github.com/c933103/AN-Paint/blob/0e4132cc68648a7e038320285a632469f2cf3a5e/verification/uk-lt-ro-priority-20261027/local/README.md). No application logic or linguistic value changed in this repair.

## Concrete failures and precise fixes

[Initial run 40462722790](https://github.com/c933103/AN-Paint/actions/runs/40462722790), on predecessor `0023c724`, is **failed**, not relabelled: 1,410 JVM tests, three failures, zero errors/skips. Its five other canonical jobs passed and lint reported no issues.

1. The CA/RO actual animation test still expected Romanian's old English lower-bound label and old animation sentence. It now uses the finite exact-prior-value successor and reviewed Romanian count qualifier; Catalan's existing fallback and all import/cancel/ownership branches remain.
2. The numerical English-fallback test still chose newly translated Romanian. It now uses verified-untranslated Albanian and keeps the complete literal fallback, selected-locale decimal/group separators, opposing US process locale and memory-unit check.
3. The new all-values test requested a formatted held palette label with no arguments while expecting raw placeholders. Production correctly substitutes missing arguments with `?`. The test now separately checks the exact raw fallback through `getString` and three explicit arguments containing `100%` through the production `ui` formatter. This does not accept the held palette translation or assert a real palette-name composition.

Both independent supplemental reviews accept these test-only changes. All three locale resource SHA256s match the prior integrated readback. No unrelated P2 budget fallbacks were changed merely to remove English.

## Verification at the current candidate

- Complete ordinary host: **1,469 passed**, exit 0, 197.920 s.
- Complete optimized host: **1,469 passed**, exit 0, 197.522 s.
- Focused 12-test exact-scope suite passes in both modes.
- [Current exact-head run 40465665783](https://github.com/c933103/AN-Paint/actions/runs/40465665783) and renewed exact-head Codex review are **pending**. Prior results are not substituted for this source head.

The predecessor's seven other new actual-consumer JVM methods passed. Its source-bound API35 complete app union 47/47 and native inventory 74/74, matching core/position APK/source/test-APK identities, and all 13 exact-script probe outcomes passed. Original failed JUnit/phase records and source-bound API35 summaries are retained with artifact identities/digests. These bounded checks are not installed Ukrainian/Romanian/Lithuanian layout, native-human, physical-device or whole-language certification. No release.
