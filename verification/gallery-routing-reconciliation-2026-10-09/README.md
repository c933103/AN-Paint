# Gallery task-routing evidence reconciliation

Recorded 9 October 2026. This directory preserves focused **historical** evidence from PR19's old source tree. It does not claim new Android execution, acceptance of the current develop tree, physical-device validation, or completion of AN-W03.

## Corrected historical status

- PR19 head: `dc518e7663ee3173f81ee6a931e15fb4ab9c467f`.
- Tested merge: `a3e0ebbb28b6fbff3702bc3df3913dea68eeef80`.
- Both complete trees: `e5f9a122ceaad54d1d73ef752d627cbc0b39ceae`.
- [Workflow 37711485088](https://github.com/c933103/AN-Paint/actions/runs/37711485088) completed successfully. Its regression/lint, APK/source build and API35 emulator jobs passed.
- The downloaded XML records 329 JVM/Robolectric tests, zero failures/errors/skips and zero lint issues.
- The four installed summaries record 91 passing methods: 71 native/import, 13 editor, three gallery and four vertical. Every summary has empty missing/unexpected/error arrays.
- The three actual gallery task-routing cases passed in 39.789 seconds. The retained logcat excerpt includes lifecycle instance IDs and tasks 34, 36 and 38.
- [Code review for this exact historical head](https://github.com/c933103/AN-Paint/pull/19#issuecomment-6050384549) reported no major issues. No separate Security review was found in the retrieved PR19 timeline.

The old PR description still called this run pending when read. The earlier 88-case baseline lacked these three installed gallery methods and must not be substituted for this result.

## Retained evidence and provenance

Original gallery runner summary, JUnit XML and instrumentation output are copied byte-for-byte, as are the three-case host composition XML and lint XML. `gallery-logcat-excerpt.txt` retains only original lines containing `GalleryDraftDeviceTest`. It contains no rewritten line content. `derived-aggregate.json` records per-suite counts and source XML/summary hashes derived from the downloaded archives; it is an analysis product, not a raw CI report.

`provenance.json` records official artifact identities and SHA-256 digests. Both downloaded archives matched those digests. The complete ZIPs, APKs and unrelated vertical screenshots are intentionally not duplicated here. The original artifacts expire on 22 October 2026:

- [Installed artifact 11522322293](https://github.com/c933103/AN-Paint/actions/runs/37711485088/artifacts/11522322293)
- [Regression artifact 11521814845](https://github.com/c933103/AN-Paint/actions/runs/37711485088/artifacts/11521814845)

`files.sha256.json` covers every retained evidence/description file except itself. `check_evidence.py` verifies these hashes and the historical gallery/aggregate contracts. Its execution only checks saved evidence; it does not run Android.

## Current source gap

The inspected develop snapshot is `4b615ce2d9e27814df84812b90858b5f676ce51a`, tree `84107dd03e8ac96ed953afd95bf6cbe5b72f84c4`. It includes merged Commons PR20 and device-language-row PR28. PR29 was independently active at `ea60a00001d766674cbd6b91da791894af5ea624`; its files were inspected for overlap and remain outside this continuation.

Current production already implements draft restoration, explicit acceptance, discard, durable private credit sessions, ownership checks and deferred startup result handling. The three individual `GalleryImportTest` draft regressions are present. The combined `GalleryDraftAutosaveCompositionTest` and installed `GalleryDraftDeviceTest` are absent.

Historical PR19 tests use obsolete inline-ledger Intent/Bundle expectations. Production now sends `image_credit_session`; token ownership, private durability and asynchronous startup must be retained when migrating tests. Current `ClassicStartupRecoveryTest` exercises accepted-result deferral by direct callback, which cannot prove OS routing. Current `EditorDeviceTest` substitutes gallery results.

The accepted `AcceptedCreditRestartSeedTest`/`AcceptedCreditRestartVerifyTest` and strict CI force-stop boundary genuinely test accepted-text survival and explicit archive recovery across a new process. They do not recreate the covered editor and then let Android return a gallery result to it. These distinctions prevent a blanket claim that process-stop evidence is absent while keeping the gallery task-stack gap explicit.

## Remaining acceptance

Port and execute three installed cases on current accepted source: restored draft confirmation; restored draft cancellation without modal reopening; and saved source A plus an empty unconfirmed source B that is cancelled. Retain same-task/same-recipient checks, pixels, floating geometry, separate ledgers, undo, subsequent autosave, Save/Export panels, clipboard and actual output decoding.

The old test's WebView block at CREATED was too late to guarantee no initial provider request. A replacement test boundary must be applied and positively checked before the initial load. No provider/WebView integration, API30, physical-device or language-fluency claim follows from this historical API35 routing evidence.

See [the proposed history reconciliation](reconciliation-plan.md). No original branch/base was changed by this evidence publication.
