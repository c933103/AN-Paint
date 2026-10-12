# Exact PR55 migration installed-artifact audit

**Installed aggregate FAIL: API30 94/95 passed, one real failed test. API35 104/104 passed. Artifact/source/protocol integrity checks PASS.**

This is a read-only audit of downloaded CI evidence. It did not modify application source, APKs or the supplied artifact extraction, run Android, publish anything, or diagnose the separate API30 failure.

## Binding

- Head `43ab6622cdf6aac957a8d31cf2c5c20009e71d6e`
- Frozen source tree `592a60877524c5c118695cb45a4d0d5cd257b25a`
- Synthetic merge `e191c4660ef8709450df213cb75bd4bcf0810cb2`, base `71f4d288669858e7975ec4c094b7f47a9a1ff145`
- Run [38279470164](https://github.com/c933103/AN-Paint/actions/runs/38279470164)
- API30 artifact 11761685563: SHA256 `19da71039753da8626a80fa85eb31247fe6b72eac2a8a6fbc8e021c66e2f7a84`, 31 exact extracted file members
- API35 artifact 11760988700: SHA256 `d1c567cb7341e6c56ad3b4d355e04ca7bbad78f1193ae0bb51baa38bcbb2a3bf`, 180 exact extracted file members

Official artifact IDs/digests and remote source/run authenticity were supplied by the coordinating review. This audit independently recomputes ZIP hashes, every extracted member, local source inputs, raw protocol/summary/XML consistency and bounded job receipt consistency. It does not reauthenticate GitHub's server independently.

## Installed phase outcome

All expected identities are derived from the frozen current source and SDK-aware phase partition. No past test count is an inventory oracle. Every expected raw phase exists, with no unexpected phase summary, duplicate/missing identity, protocol/summary/XML mismatch or phase hard timeout.

- API30: 97 SDK-eligible identities, two explicitly unscheduled restart identities, 95 scheduled and completed, 94 passed, one failed. Ordinary 15/15, gallery-draft 3/3, English/Manchu 2/2, literary-Chinese/emoji 1/2, library 73/73. No successful union receipt remains for the failed matrix.
- API35: 104 SDK-eligible identities, all scheduled, completed and passed. Ordinary 16/16, gallery-draft 3/3, English/Manchu 2/2, literary-Chinese/emoji 2/2, dialog 5/5, seed 1/1, verify 1/1, library 74/74. All four coverage receipts agree exactly with the complete current-source app union.
- API30 failure: `paint.anpaint.android.VerticalLocaleDeviceTest#literaryChinesePickerRibbonToolsAndJpegUseNativeInputInBothOrientations`, `java.lang.AssertionError: Timed out: native vertical Save layout; last I/O error: null`. The 100.196-second phase did not hit its 180-second process ceiling; ADB exit 0 does not override the failed test. Root cause belongs to the separate diagnosis.

The API35 restart boundary independently records the same live seed PID 7093 before and after successful seed instrumentation, resumed Gallery activity, successful external force-stop, and explicit process absence before successful verify instrumentation. Seven bounded boundary commands returned 0.

## Arabic native raster and natural update

Both routes pass the frozen current strict transport/PNG decoder and independent Pillow 12.3.0/NumPy whole-raster recomputation. All actual PNG pixels are compared against the complete bounded reference at the recorded origin, without masking, thresholding, cropping, rescaling or tolerance. Exact Arabic message, complete layout text and accessibility text agree with the frozen resource XML.

- COPY: 4,287 reference ink pixels; actual 640x92, reference 622x92.
- INSERT: 4,435 reference ink pixels; actual 640x92, reference 622x92.
- For both: zero allocation-edge, horizontal-overflow, outside-view, missing-expected-ink and different-ARGB pixels; alpha/color/position tolerances all zero.
- API35, target SDK35, Arabic, font scale 2, root 640x320, density 1. Bounds-width mode is enabled, shifted drawing offset disabled, measured leading inset 1.
- COPY and INSERT natural-update log records each show old/new layout height 88, exact different old/new text, width 640, initially settled view/root, a real requested view/root layout after replacement, and settled flags afterward. The complete text and dimensions bind to the corresponding full-raster records. Raw logcat lines 54677 and 54728; strict schema/order/duplicate checks pass.

All four original transparent PNGs were actually viewed. The inspected crops show two-line Arabic text with Latin `Commons`; no additional visible discrepancy was identified. This is a bounded visual check, not fluent-Arabic linguistic approval. Image paths and hashes are in `visual-inspection.json`.

## Same-run prebuilt provenance

Both full job logs check out the exact synthetic merge, request both artifacts from run 38279470164, enforce digest mismatch as an error, and report matching downloaded SHA256 values. Both use the frozen prebuilt install driver, debug variant and correct SDK. Main APK and every recorded test APK installation report success.

- Main APK SHA256 recomputed from downloaded bytes: `445b9b6e393e63490c7054ef44e0aefb1fefd5b56954fa8736e9974dee06f588`
- Delivered source ZIP SHA256 recomputed: `7beaf27696c948d94dec39b58cb0678a6a6315d2b3b89b43c74d582f1daf20b4`
- App instrumentation source fingerprint: `f8f8de6d967000411de5dc6a3e8a8309b6fd61f2eba9e4393556e3ad35fafe3e`
- 122 input files, including complete app/library test-source trees, imported source helpers, install driver, workflow and exact Arabic/default resource XML, match the frozen tree's bytes and executable modes.

This is bounded download/install provenance. The instrumentation archive is not separately extracted here and no installed APK is rehashed on-device. Main APK/embedded corresponding-source and compiled-resource review is separate. CI debug signing is not private release/upgrade signing.

## Reproduction

The scripts are adapted copies in this directory; all older scripts/results remain untouched. Python 3, NumPy and Pillow are needed. Supply the exact Git tree's checkout/object database and the original downloaded artifact directory with ZIPs, exact extraction folders, full job logs and `apk-and-source` extraction. Output must be a fresh directory.

```sh
PYTHONDONTWRITEBYTECODE=1 python3 run_audit.py \
  --repo /path/to/exact-checkout \
  --artifacts /path/to/downloaded-artifacts \
  --output /path/to/fresh-audit-output
```

Expected exit **1** is deliberate because API30 genuinely failed. `result.json` distinguishes `audit_integrity_status: PASS` from `installed_gate_status: FAIL`. Other checker failures raise an audit error. `reproduced/` is the fully rerun final checker output; `reproduction.log` captures that exit condition's result.

Local checker controls: 11 synthetic raster/natural-update tests passed normally and under `python -O`; all 31 frozen source strict decoder tests passed normally and optimized. These host controls validate checking behavior and are not additional Android executions.

## Limits and disposition

Do not claim the full installed matrix passed, a fully verified release, hardware screenshot equivalence, genuine network-failure route execution, broad language fluency, physical-device coverage or expanded locale completion. The known advanced-colour limitation is characterized by a passing diagnostic identity, not positive viewport acceptance. API35 success and the narrow Arabic evidence do not erase the API30 failure or restore withdrawn localization conclusions.

## Expiry-safe declared delivery

`DELIVERY-FILES.json` is the authoritative frozen list of files to copy, with relative paths, byte lengths and SHA256 values. Copy that manifest itself as well. Files outside its list are temporary or superseded and are not part of the delivery.

`replay-inputs/raw-inputs.tar.gz` preserves 63 exact raw inputs (22,232,555 bytes expanded): all 13 phase protocols, JUnit XML, summaries and install receipts; all four API35 coverage receipts; restart boundary/status; full API35 logcat; both full CI job logs; build-info and supplied source-publication metadata. The original Arabic PNG/JSON records are also retained uncompressed in `installed-observed/`. `RAW-INPUTS.json` binds every retained input and the deterministic compressed archive. `ORIGINAL-ARCHIVE-MEMBERS.json` preserves hashes for every member of both original emulator artifacts.

No APKs, APK/source ZIPs, complete source-tree dumps or original outer artifact ZIPs are included. An exact checkout of the durable head/tree named above is still required for source-derived replay. Obtain it from the source repository, not an expiring CI artifact.

```sh
PYTHONDONTWRITEBYTECODE=1 python3 replay_evidence.py \
  --repo /path/to/exact-checkout \
  --output /path/to/fresh-replay-output
```

This expiry-safe replay has been run successfully: `replayed/results/result.json` and `replay-check.log` preserve the result. Expected exit **1** again means API30 94/95 with its real failure; API35 is 104/104. It revalidates archive/member input integrity, exact source-derived raw phases, strict decoding against the retained Arabic records, independent pixels, natural updates and prebuilt/restart receipts. The prebuilt result explicitly sets `payload_hash_recomputed: false`. It does not pretend to repeat the original outer-ZIP or omitted APK/source-payload rehash checks; those original results and digest manifests remain preserved separately.
