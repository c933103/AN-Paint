# PR55 glyph-bounds candidate: independent hosted artifact review

Status: **FAIL — JVM test compilation blocker. This bounded report is frozen; installed matrix review will be a separate supplement.**

Exact candidate: head `d5fb31f6cb1562eecba51e5ccff9b118a7e71714`, merge `b750c54f6411412ee3f1bc1f51815db205212c35`, tree `8f9f0d5399f88d173a508e0ce5c96682ca173ed4`, run [38263619232](https://github.com/c933103/AN-Paint/actions/runs/38263619232). Publication receipt supplied by the writer; independent checks bind downloaded bytes and local exact Git tree. All 12 reviewed source files match that tree. Earlier checkers and source-review deliverables remain unchanged.

## Actual results

- PASS: exact-script ZIP digest/extraction, seven successful probes, generator ordering and incremental state, exact source/log hashes.
- PASS: APK/source ZIP digest, build info, embedded corresponding source, 2,114 exact bundled tracked blobs from 2,117 leaves. Only `.gitignore`, `colorpicker/.gitignore`, `.idea/codeStyles/Project.xml` are omitted. Native extras remain constrained to the four existing source roots; their upstream content was not reaudited. All 14 fonts-directory assets/licences match.
- PASS: actual aapt2 resource table contains exactly default + 59 M04 values + generated Korean alias (61). Manchu U+180E indices 7/18/27 and Mongolian U+202F indices 7/17/30 remain exact. This proves compiled values, not runtime shaping.
- PASS: hosted Python aggregate completed 712 tests in 193.013s with two skips and exit 0. The compact hosted log does not identify skipped names. Native preparation and lint exited 0.
- FAIL: JVM phase exit 1 at `CommonsMetadataQueryFailureFlowTest.kt:648:86`, `Val cannot be reassigned`; `compileDebugUnitTestKotlin` stopped before execution. See `STATIC-COMPILE-FINDING.md` and `phase-result.json`.
- UNRUN: all 892 JVM identities, 112 success render pairs, 28 diagnostics, 181 strict ink triplets and four control summaries. Their absence fails the strict artifact checker; it does not identify a new clipping or layout defect. No actual JVM image is available to inspect for this candidate.
- OUTSIDE THIS FROZEN DELIVERY: separate installed API30/API35 artifacts and both new Arabic software-raster records. Production/test-APK compilation success cannot replace those receipts.

## Checkers and limits

Scripts take explicit repository/artifact paths; use `--help`. `audit_glyph_artifacts.py` verifies exact ZIP extraction, source-pinned 892 identities and complete render/control inventories; its expected exit is currently 1. `audit_phase_logs.py` validates the failed compile receipt and classifies runtime evidence as unrun. A 0 exit from that forensic script validates the diagnosis, not candidate acceptance. Twelve synthetic checker tests pass ordinarily and under Python -O. Synthetic pixels do not establish Android execution.

`audit_installed_pixels.py` is prepared to cross-check decoded real installed PNGs independently with Pillow/NumPy and exact-source Arabic text. It requires the reviewed strict transport decoder plus separate successful raw instrumentation/source/APK/run binding. It does not authenticate those itself. Installed native software raster of injected status text is neither a hardware screenshot nor real network-failure execution.

The local source review did not compile Kotlin and missed the lexical-shadowing defect later identified by writer and reviewer. Its byte-preservation and host-test results retain their exact historical scope; they do not provide Android readiness. Correcting an explicit receiver in a successor will still require fresh native evidence for the production geometry and all strict zero-tolerance controls. No production, translation, font or oracle threshold was changed during this audit. Root owns readiness and merge.
