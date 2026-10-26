# Slovak / Slovenian P0 candidate snapshot

Exactly 78 proposed missing live-consumer values per locale, at source `e5f2d4e2d07e678076f022aa7b3ef923e13c3721` / tree `806d9577409c4044212d1c12e6e38da46417bae6`. All 1,379 source blobs were rebound, all 78 English values and attributes checked, 140 context windows verified. Current bounded direct-consumer scan covers 322 production Kotlin/Java/XML files. All 254 inherited values/attributes remain immutable.

These are author candidates, **not independent acceptance**. Separate full-value reviewers may accept, revise or hold each value. Source contexts/framework may be reused only after exact current revalidation; no previous locale translations or acceptance transfer. Locale-specific action references have been rebound to current sk/sl labels.

Groups per locale: import/format 13, recovery/autosave/undo 28, assembly/memory/resize/destructive 16, save/share/credit/destination/encoding 21. Five absent no-direct-consumer keys remain held: formats22_derived_exported, ui_save_as, ui_save_as_jpeg, ui_save_as_jpeg_xl, ui_save_as_png. The P0-only memory warning does not expand paired120-entry/60-tag acceptance, add its P1 companion, rewrite history or change global59/112. If all78 are accepted, each catalogue becomes205 entries and P0 87/92; not whole-language or native-human certification.

Run `python3 validation/verify_candidates.py --root . --source CHECKOUT` against the pinned source and `python3 -m unittest discover -s validation -v`; repeat with `-O`. Ordinary and optimized structural reports match. Negative controls reject 2,340 actual-entry corruptions, including 32 added-token mutations of actual formatted=false entries, plus duplicate JSON and precision/index/type/flag checks.

Preparation finding retained: pre-sort JSON reports have identical contents but set-derived hold-key ordering differed; deterministic sorted ordering fixes byte reproducibility, without source/candidate changes. Both earlier reports remain as provenance.

No production changes are claimed here. CI, review, source publication and actual postmerge verification are separate later evidence. PR56 never-merge, PR159 Czech/Fit freeze, PR113 retarget, Help/callback/archive and release pauses remain unchanged. No release.
