# PR55 receiver and natural-relayout successor: independent source review

**FROZEN source review: no blocking source finding within the reviewed scope. The local full aggregate is incomplete; fresh Android/runtime proof remains required.**

Base: failed head `d5fb31f6cb1562eecba51e5ccff9b118a7e71714`, tree `8f9f0d5399f88d173a508e0ce5c96682ca173ed4`, run 38263619232. The earlier source review missed a local `val text` shadowing the TextView receiver; actual hosted compilation caught it. The same head independently failed installed Arabic software-raster containment. Both failed artifact reviews remain frozen separately.

## Exact current scope

Eight source paths are bound by `reviewed-source-manifest.json` (SHA256 0cf44710342250ec6cd16f9fe967db7b331b02a9930b3f627df426e1cbbac4d7), derived from the writer's frozen manifest 4994c68e3929406659e0bafca2d3b9dfd9550d2fc35583c56f8bb4edc391b267.

- Production adds only `requestLayout()` and its two explanatory comments after `setStatusText` resets state and assigns text. API30/vertical routes, layout algorithm, fonts, strings, deadlines, providers and thresholds remain unchanged.
- JVM test uses explicit `this.text` in the independent original-plain TextView control. Native reset setup additionally checks that a settled status replacement requests measurement before existing test-forced reset measurements. This check itself does not prove natural traversal.
- The installed Arabic helper first settles INSERT normally, then performs different COPY→INSERT replacements. It asserts exact GlyphBoundsStatusView class, visible positive width, settled root/view before replacement, immediate production-triggered false→true view layout request in the same main-thread action, unchanged positive native Layout height and view width after normal traversal. It does not call measure/layout/requestLayout/forceLayout. Source/route/text/class/state/height metadata is retained in `GalleryStatusNaturalUpdate` logcat records.
- The full installed raster transport and strict pixel oracle bodies remain byte-identical. No alpha cutoff, spatial/color tolerance, cropped expectation, omitted glyph or exception-as-pass was introduced.
- Five existing source/test helper paths have strict bidirectional inverse projections. Three new files hold the pinned compact fixture, inverse helper and source/mutation contracts. Earlier endpoints are recognized only by exact hashes for idempotent historical checks. Existing failed fixtures and all historical evidence remain unchanged.

## Independent checks already completed

- PASS: 118 focused methods normally in 11.533s, process exit 0; the same 118 under Python -O in 13.151s, exit 0. Full logs contain no failed/error method result. These include new successor checks, glyph/painted/diagnostic/M04 composition, M02/M03/composition, transport and instrumentation protocol checks. Later deliberately negative `success:false` JSON is expected test output.
- PASS: ordinary and optimized byte/mode audits inspect all 2,117 predecessor leaves: 2,112 unchanged, exactly five expected changes, each restored and replayed byte-for-byte against the immutable Git tree. No predecessor file/mode disappeared or changed unexpectedly. Existing fonts/catalogues/licences/fixtures/manifests/reports remain exact.
- PASS: all eight reviewed source hashes match; three new source files are exact. Flow 18 and installed gallery 1 declared test-method inventories remain unchanged. New evidence-only additions are reported separately from source and do not silently change this scope.
- UNRUN locally: Kotlin/Android compilation, installed execution, natural traversal, native glyph containment, all fresh JVM/render/control outcomes. No local SDK/Gradle/Kotlin execution is claimed. Source checks do not establish that the lifecycle hypothesis is the only issue.

## Why the candidate is bounded

The previous installed receipts contained zero measured inset despite native right ink exceeding content width. Exact upstream Android15 TextView source has a fixed-width, same-height replacement path that rebuilds Layout and invalidates without requesting view layout. Explicit production requestLayout addresses that concrete mechanism while preserving the existing measurement and strict acceptance algorithms. Current failed receipts did not record subclass identity/callback history, so this remains a supported candidate, not a retrospectively proved execution trace. The new installed assertions directly test that missing lifecycle coverage.

Primary source: [Android15 TextView.checkForRelayout](https://github.com/aosp-mirror/platform_frameworks_base/blob/android-15.0.0_r1/core/java/android/widget/TextView.java#L11630-L11672). The exact upstream tag is not asserted byte-identical to the emulator framework. Kotlin receiver correction follows [property resolution](https://kotlinlang.org/spec/overload-resolution.html#resolving-property-access).

## Fresh hosted acceptance

Use a new actual head/merge/tree/run binding and preserve every previous checker/result. Require exact 892 JVM identities without failures/skips/duplicates/missing cases; 112 success root pairs; 28 diagnostics; 181 strict ink triplets and four summaries; 72 genuine negative controls; all 108 positive live/intact/reset frames and the original Arabic failing counterfactual. Recompute every alpha>0 pixel/full ARGB and inspect actual PNGs. Keep advance metrics diagnostic and all complete-text/accessibility/line-coverage checks.

Require API30's 95 scheduled identities (97 SDK-eligible declarations with two explicit restart omissions) and API35's 104, including restart phases. Both installed Arabic full-raster records must pass strict source/protocol decoding and independent pixel recomputation. Additionally require exactly two ordered source/route/message-bound natural-update log records that agree with those rasters. `audit_natural_update.py` is prepared for this purpose and needs explicit future publication/log bindings; its synthetic tests are not Android evidence. The app-source digest is f8f8de6d967000411de5dc6a3e8a8309b6fd61f2eba9e4393556e3ad35fafe3e; library digest remains 1412fb3f410c439d3543daab499667dd288f720368b958275158edc2a9dd6e0b.

Retain exact APK/source/font/resource/probe and prebuilt installation provenance checks. Installed software-raster injection does not prove hardware composition or a real network-failure route. Root owns readiness and merge.

## Final local receipt and checker validation

The exact writer receipt SHA256 is d5f64d65ef4d55b143f7d25e4f625bfdae427c92fd70d4240ae5f5167292e308. Independent raw-log parsing and fresh discovery establish 719 expected host methods. The single final aggregate timed out at the unchanged 240-second cap (240.007s, saved exit 124): 408 methods started, 407 passed, one was interrupted, and 312 did not complete. There are no completed failures/skips, but this is explicitly **not an aggregate pass**. The warning-wrapped duplicate-ZIP test ends with a standalone ok and is included in 407. A prior wrapper launch exited127 because /usr/bin/time was absent before any test ran; the test command then used Bash time. No aggregate rerun is claimed. Writer focused 135 normal/22.902s and optimized/17.597s both pass and have saved exit0 receipts.

The separate natural-update auditor passes all seven synthetic test methods normally and under Python -O (0.004s each), covering malformed/duplicate/truncated JSON, missing/extra/reordered routes, wrong source/class/messages/state, invalid or unequal native heights/width, and failed/incomplete raster receipts. It requires explicit future publication/log bindings and rejects a failed raster record. These tests establish checker behavior, not Android traversal.

The failed predecessor evidence is preserved at [commit 94b91c4e](https://github.com/c933103/AN-Paint/tree/94b91c4eb04d856853e29bdf7c90c61d52405bff/verification/commons-metadata-m04-glyph-bounds-ci-2026-10-12). No future head or run is bound by this source review.

## Portable checks

From the exact candidate checkout, run the focused modules with `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=tools python -m unittest -v test_commons_metadata_m04_receiver test_commons_metadata_m04_glyph_bounds test_installed_glyph_ink_evidence test_commons_metadata_m04_painted_ink test_commons_metadata_m04_diagnostic test_commons_metadata_m04_composition test_run_android_instrumentation test_commons_metadata_composition test_commons_metadata_m02 test_commons_metadata_m03`; repeat with `python -O`.

Run `audit_natural_relayout_source.py --repo CHECKOUT --reviewed-manifest reviewed-source-manifest.json --manifest-sha256 0cf44710342250ec6cd16f9fe967db7b331b02a9930b3f627df426e1cbbac4d7 --output RESULT.json`. `audit_writer_receipts.py --repo CHECKOUT --writer-root LOG_DIRECTORY --output RESULT.json` binds the named writer logs, original source manifest and local receipt. No script modifies app source. The separate auditor self-tests use `python -m unittest -v test_natural_update_auditor` from this review directory; repeat with `python -O`.
