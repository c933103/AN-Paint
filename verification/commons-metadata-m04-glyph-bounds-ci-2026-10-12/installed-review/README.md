# PR55 glyph-bounds candidate: installed evidence supplement

**FROZEN: FAIL on installed API35. API30's exact scheduled matrix passes.** This supplement does not alter the frozen compile/APK/probe review.

Binding: head `d5fb31f6cb1562eecba51e5ccff9b118a7e71714`, merge `b750c54f6411412ee3f1bc1f51815db205212c35`, tree `8f9f0d5399f88d173a508e0ce5c96682ca173ed4`, run [38263619232](https://github.com/c933103/AN-Paint/actions/runs/38263619232). Official artifact downloads/digests were supplied by the writer. The reviewer independently matched both ZIP digests and every extracted member, then reconciled source-derived identities, source hashes, raw instrumentation, JSON receipts and JUnit XML.

## Actual installed results

- API30: 95/95 scheduled identities pass: 73 library +22 app. There are 97 SDK-eligible declarations; two restart identities are explicitly unscheduled at this SDK. The original API30 path is unchanged by this candidate.
- API35: 102/104 scheduled identities completed, 101 passed, one failed. `GalleryViewportDeviceTest.realBrowserKeepsItsViewportAtLargeTextAcrossGalleryRotation` failed both injected Arabic COPY/INSERT ink checks. Restart seed and verify receipts are absent; successful earlier phases cannot replace them.
- Both Arabic records have the reviewed complete text/accessibility/Layout strings and match the actual compiled APK strings. They record API35/target35, scale2, density1, root640×320, content width616, origin(12,0), width-mode true on view/Layout, shifted-overhang false and paragraph inset0. The fresh default TextView width flag is also true.
- Each reference has exactly one alpha>0 pixel beyond the accepted content box: layout coordinate `(616,14)`, reference PNG `(618,16)`, actual view `(628,14)`. Reference RGBA is `(0,0,0,1)`; actual RGBA is transparent `(0,0,0,0)`. Therefore horizontal overflow, missing expected ink and whole-view ARGB difference are each1. Allocation-edge and outside-whole-view counts are0. COPY reference has4,287 ink pixels; INSERT has4,435.
- The complete actual TextView PNG is640×92 and independently allocated reference is621×92, box `[-2,-2][619,90]`. The reference was not cropped from the already-clipped actual view. Standard-library decoding and independent Pillow/NumPy full-raster recomputation agree exactly. Strict acceptance decoding rejects both the failed runner and each overflowing record. Forensic extraction is clearly labelled as failed evidence.

## Images actually inspected

The reviewer opened all four unchanged complete images: `observed/copy-actual.png`, `observed/copy-reference.png`, `observed/insert-actual.png`, `observed/insert-reference.png`. Their hashes and exact problematic pixel coordinates are in `observed/forensic-result.json`. The tiny alpha1 loss is established numerically; this report does not claim a conspicuous visual defect. No tolerance or alpha cutoff was increased.

## Bounded diagnosis

See `LIFECYCLE-FINDING.md`. Exact upstream Android15 source supports a same-height fixed-width setText fast path that rebuilds Layout and invalidates without requesting view measurement. This candidate resets its measured inset on status replacement but does not explicitly request layout, while installed checks await natural traversal. That mechanism is consistent with the measured zero inset. Actual subclass identity and measurement-callback history are absent from current receipts, so the precise path remains an inference. A narrow explicit requestLayout candidate needs a same-height text-replacement regression with no test-forced measurement, exact subclass telemetry and fresh strict native/installed proof.

## Scope limits

These are actual installed native software rasters of injected status strings, not hardware screenshots or real network-failure route execution. The API35 emulator fingerprint is recorded in the route reports. Current installed evidence does not change the separate Kotlin compile failure: all892 JVM identities,112 root captures and181 ink triplets on this exact head remain unrun. Neither the source-only receiver correction nor the proposed lifecycle fix establishes readiness.

`forensic_installed_ink.py` verifies the two ZIPs and extracts failed records without treating them as acceptance. `audit_installed_matrix.py` independently reconciles both exact matrices and preserves missing/failed phases. `audit_compiled_arabic.py` compares both records to the source-bound actual APK string table. Each takes explicit paths via `--help`. A successful forensic script exit validates its diagnosis, not the failed candidate.

## Prebuilt/source provenance

`prebuilt-provenance-result.json` independently matches the writer's receipt against both actual full job logs and actual main APK/source bytes. Logs bind the exact merge and same-run main/test artifact names, require digest mismatch to be fatal, retain matching downloaded SHA256 receipts and successful installation. There is no independent extraction or on-device hash of instrumentation test APKs in this review. That limitation is retained rather than replaced by a stronger binary-provenance claim.
