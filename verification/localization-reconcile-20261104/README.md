# Localization / PR296 reconciliation

Published merge: `31fdd100c5f1162e2e416284a051e78732c53b46` on `review/nv-bottom-2038-20261103`.
Tree: `9209a290ffdda4f3ff06126e7fe74f8ee36208ab`.
Ordered parents: `4e0c3a8f061e1b54d4951357f4d05b97aefd27aa`, `1f763dbd25e93ad13285041e3d2bcb5051a40241`.
Merge base: `df0b1e4cb247a728e108bd2b666a96ce5114da2a`.

## Reconciliation
Full nontruncated Git trees show 146 locale-side changed paths and 10 develop-side changed paths, with no intersection. The resulting remote tree was compared against every expected path, blob, type and mode (1407 blobs). This is a conflict-free three-way tree reconciliation, not a claimed local `git merge` run. No rewriting, removals, credential content, translation changes, or old-recovery-to-new-ID copying occurred. All PR296 source/test changes and all prior locale-side blobs remain intact. The merge commit, ordered parents, tree and branch head were read back after the non-force expected-head update.

## Coverage
The actual app_language_tags.xml offers 171 distinct locales. The exact manifest has 719 identities: P0 94, P1 249, P2 305, P3 71. Direct missing totals are respectively 466, 1435, 31307, 7765. Complete-by-direct-presence locale counts are 0, 159, 61, 61. The new recovery pair has no direct definition in any offered exact-tag catalogue, so it uses default-English fallback. P0 missing consists of 342 new-pair entries plus 124 older gaps.

coverage-171.csv lists every offered locale. presence-classification.csv separates direct resource presence, text equal to default, direct aliases and missing/fallback entries. Text equality is diagnostic, not proof of English fallback or authorship: proper names, numbers and legitimate shared words can match. Direct presence does not certify authored prose, linguistic review or quality. No fallback entries receive translation credit.

## Checks and limitations
Passed: canonical catalogue structural validator; 73 priority-wording tests; 17 importance tests; 40 translation/boundary tests; 2 language-note tests.

The broader Python host attempt ran 806 tests in 200.132 seconds: 3 failures and 28 errors. Initial partial-snapshot dependencies caused 27 of those errors; after restoring content-verified dependencies, all seven affected modules were rerun: 85 tests, 84 passed and one environment error remains. The remaining test_download_selected_artifacts observed-input test needs git HEAD/tree metadata; this content-verified connector snapshot is not a Git checkout. No installation or Android build was attempted to bypass that limitation.

Three genuine existing failures remain in test_localized_help.test_protected_draft_warning_names_recovery_and_save_as_routes for nch, nhe and nhw: the guard requires the recovery route to precede Save-as, but these strings order them differently. The guard and all three locale blobs are byte-identical to the pre-merge locale head. This reconciliation does not claim the wording or guard should be changed without reviewing their semantics. No full-suite green result, Kotlin execution, hosted CI, device rendering or linguistic certification is claimed.

The two raw host logs are retained here only on this dedicated evidence ref, not added to the application branch. No denied issue comment was retried.
