# Croatian dither successor: actual merged source and runtime

Verified 27 October 2026 UTC; source batch began 26 October. This is a new current-source record, not a replacement or retry of either pending PR183 publication.

## Actual source

- PR184 merged as `c404e7ea31ef0a22c3645d8c73e50b55d7ff959c`; exact tree `1151529f41c0b0214f0a37b52cabc33d595a3e10`.
- Ordered parents: actual PR181 merge `c63cd44815ef84f498d1e2fbe46c354416b81cdc`, reviewed head `362432da26525229a06c05dea0be1db59a358e59`.
- All 1,388 tracked blobs/modes verified; exactly four successor files versus immediate base. All 18 upstream layout/instrumentation files are preserved.
- Only two existing Croatian resource values change atomically: `save20_dither` becomes **Dithering boja**, and its GIF explanation no longer identifies the obsolete “Zamućivanje” caption. No presence additions, Bosnian edits, held-item edits or release.
- Current HR/BS scope is **157 unique reviewed values =155 unchanged +2 successor values**, plus **214 other inherited values preserved**. Original PR183 history remains **156 reviewed /215 preserved**. Do not add the two successor values to 156 without removing the superseded GIF acceptance.
- Terminology remains **moderate-confidence technical clarity**, not preferred native terminology or native-human certification. Independent full-context pair review is immutable at [R03 review](https://github.com/c933103/AN-Paint/blob/71c32e5ec94613e3e3ba6e7b79e18526953a59e3/records/localization-review/2026-10-26/hr-bs-p0/r03-dither-label-review/review.json).

## All 171 language options

Fresh ElementTree and independent DOM recomputation agree: **P0 7,298 present /8,434 missing**. Every structural presence row is unchanged from immediate base c63. HR remains 86/92; BS 87/92. The five common held absences and Croatian `save20_title` absence remain intact; the separate P1 memory companion remains outside scope. Global review categories are not upgraded by counts, tests or this report.

Ordinary/optimized source outputs are identical. Fourteen source guards per mode include injected inherited-value preservation, wrong merge/tree, wrong source bytes, picker ordering and DOM disagreement. Sixteen actual-join guards per mode reject PR-run substitution, incomplete/failed runs, missing artifact provenance, mismatched execution bytes, altered reviewed scopes and missing cases.

The recomputation scripts record the exact validation used. Reproduce against the pinned repository source and Git tree JSONs, with the prior HR file from c63 and picker path mapping from the published R14 baseline. The prior mapping supplies paths only; source bytes, picker ordering, all counts and both parsers are freshly verified. Historical R14/R03 or pending R05/R06 payloads are referenced, not re-uploaded here.

## Actual natural postmerge verification

[Develop push run40421554043](https://github.com/c933103/AN-Paint/actions/runs/40421554043) completed all six jobs successfully on attempt1. Every downloaded archive digest and every receipt was checked against actual c404, not the preceding PR test merge:

| Family | Actual result | Artifact |
|---|---|---|
| JVM/Python/lint |1,399 JVM tests,151 XML suites;14 focused classes/82 exact methods; Python1,447 passed +2 skipped; lint0|12698501547|
| API35 composition |47 app +74 native exact cases; exact source/APK/test-APK identity; independent Core/Position/composition1/1/1 selection|12699052893|
| APK/source/compiled values |1,385 packaged tracked files;1,659 compiled entries =854 reviewed +805 preserved; signature verified|12696954864|
| Instrumentation bytes |Archive digest and executed test-APK identity verified|12699290092|
| Exact-script generation |13 probes and expected negative verified|12698095441|

Actual receipt manifest SHA256: `13b1054284417f7130c7d3b6f26288887a90a3bd3a7534b5807f17671920f435`. Native emulator cases are not a physical-device, complete-language or native-human linguistic certification. Hosted skipped Python identities were not named by its nonverbose summary and are not guessed.

## Failed history and correction remain visible

Original PR184 run40413471740 failed in two independent ways: its new JVM test treated `CompoundButton.performClick()`'s listener-handled return as checked state; Position could not install the emulator package because the downloaded archive was not a ZIP. The installed Position tests did not run. These are failures, not erased or reclassified successes.

The minimal test-only correction executes the real click, idles, then asserts checked state. Accessibility/text, repeated GIF/JPEG transitions, both locales/initial states and all confirm/negative/cancel assertions remain. Official AOSP contract and exact-file independent review are recorded under `repair/`. Production pair and fixture were not changed by the repair. Original repair commit1d4bafe8 remains in ancestry; fresh integrated head362432da passed Code receipt6429573796 and all actual PR-run artifacts before root merged it. The old Security summary was explicitly old-head, not falsely represented as new-head review.

## Publication boundaries

At package preparation (27 October,00:09 UTC), R05's 22:34 confirmation and R06's 23:04 confirmation were separate unresolved publication operations; exact request attribution was unverified while their workers had not returned. See publication-status.json for the later observed results; this paragraph preserves the original preparation boundary, not a claim that completed calls remain pending. Existing user authorization is not missing, and no user refusal is inferred. This package contains genuinely new successor/actual-postmerge evidence, is checked against both pending inventories, and does not copy, re-encode, retry or substitute their payloads. It uses a distinct records branch; neither pending writer's ref is moved. No credentials, secrets or unrelated private data are included. Public debug certificate fingerprints are not private keys. No release was performed.
