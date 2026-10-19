# Corrected-head terminal verification

PR139 head `a2503197cdf9d268beb512bbde40e576bbc84922`, tree `958ca32244b43131e181186c836a8bb31b09fe26`. [Run39149447853](https://github.com/c933103/AN-Paint/actions/runs/39149447853) finished successfully on 2026-10-18 at 17:46:34 UTC. Its synthetic checkout `ac04bd5195c60bbfa4be2a5b3f0b7a72c9525506` has the identical tree. All six jobs passed; no workflow, production font or other-locale changes were made.

## Verified current-head results

- Four local focused full-value tests; 985 host tests both normally and optimized; 985 hosted host tests.
- 1,144 JVM methods in 123 suites, zero failure/error/skip. All eight source-discovered `ChineseCropPreviewTest` methods passed, including both Taiwanese real-toolbar crop cases. The repaired Han method covers alternate 怹; POJ retains its combining-dot guard. Full string/count/accessibility, selection independence, trim/reset, Cancel/reopen and project/original-byte preservation are exercised.
- Relevant model/translation/help source inventories match their XML: AssemblyModel20, CropMovementTranslation2, FrenchAssemblyHelp3, JapaneseActiveGuidance3. Android lint passed.
- Nine exact-script clean/incremental resource-generation probes passed with exact commit/tree and raw-log digest checks.
- Complete source-discovered API35 union: 74 native and 45 app methods. Exact successful core/position artifact IDs were selected independently against run/attempt/time windows. Main and both instrumentation APK hashes, source identity, native/app inventories, force-stop phases and composed receipt agree. No missing, unexpected, ignored, failed or aborted test receives credit.
- Capture transport independently replayed: 12 dialog cases, four vertical exports, 32 vertical matrix captures, eight reachability cases/64 reachability captures; all 168 extracted files match collected bytes. This verifies transport/inventories/native state/bounds, not an independent pixel or Taiwanese installed-rendering review.
- APK `d0d5cd9af058327ed1a5f0b4116ed93b0050a05f900c0f87e83b5186102c8cbe`; source ZIP `82c5cc351b36f54bc50e428ed26bb4057eef4ada2531ae030f5570ec91b0c08b`. Embedded source is byte-identical to delivered source. All 1,222 included source blobs and executable modes match the reviewed Git tree; the three expected metadata exclusions are enumerated in `build-binding.json`. Current APK signature v1/v2 and 16 KiB zip alignment verify. This is CI debug signing, not private upgrade signing or a release.
- AAPT2 output from that APK contains the exact full Han/POJ plural values, including all placeholders and the newline.
- [Codex current-head Code review](https://github.com/c933103/AN-Paint/pull/139#issuecomment-6252898184) completed with no findings; no review threads. Advisory Security remains a clean review of initial `c46fc44`, not current-head security coverage.

## Rendering and language limits retained

The positive actual-status-font coverage, non-tofu painted ink and native layout guards remain intact. The Han alternate 怹 (MOE13567 異用字, same `in`/third-person-plural sense) passes in the actual API33 Robolectric status font. POJ `ô͘` has positive codepoint coverage, nonempty/non-tofu composite ink, and differs from unmarked `ô`; a multi-character ligature requirement was not used as a combining-mark proxy. Raster borders remain transparent. Full UTF-16 status layout coverage, no ellipsis and height fit pass across updates.

The original preferred 𪜶 U+2A736 failure is preserved separately under `../failed-head-c46fc44/`, including its raw XML/logs and terminal cancellation disposition. This spelling substitution does not fix or close [the broader preferred-glyph font limitation](https://github.com/c933103/AN-Paint/pull/75#issuecomment-6252833986). Other platforms are not inferred to lack that glyph. Initial-head POJ success was not substituted for corrected-head evidence.

Full-sentence linguistic confidence remains moderate, lexical/readings support stronger. No native-speaker certification, whole-language/catalogue acceptance, installed Taiwanese dialog pixel/TalkBack acceptance, physical-device, legacy-platform or release acceptance is claimed. Hakka/Wu remain held. The parent merged PR139 as `798e6159939fa06beb27755700a1320a5970cb7b` after these gates passed; post-merge verification is recorded separately.

## Files and reproducibility

`checks.json` links run/jobs/review and the focused receipts. `verification-packet.zip` retains all JVM XML, raw phase logs, exact-script logs, run/artifact/review metadata, source-bound device reports, collector logs, independent verifier scripts, local host logs, signature/alignment output and the complete compiled-resource dump. Its internal manifest hashes every member. Companion JSON/XML files expose the bounded receipts without unpacking logs.

Temporary verification had one local input-shape error (passing the REST jobs envelope rather than its jobs list); that error and its correction do not represent a CI or application failure. The raw local verifier error is retained in the packet. The corrected verifier replay completed successfully without changing source/tests or loosening assertions.
