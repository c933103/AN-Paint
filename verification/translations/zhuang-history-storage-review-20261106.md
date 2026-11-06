# Zhuang Undo-storage failure review

2026-11-06. Base `f88a76501a4b59a47d2ce7d1cf61644a3bcd312e`, branch `review/nv-bottom-2038-20261103`. Only canonical Zhuang XML and this report change.

## Wording and independent review

Add missing P0 `ui_cannot_create_the_undo_cache_free_some_device`:

“siu” · AN Paint guh giz rom gij soqgawq haenx mbouj ndaej. Hawj giz rom vwnzgen ndaw gihgi neix hoengq di, caiq guh.

Functional reading: for Undo, AN Paint cannot create the place storing that data. Make file-storage space in this machine somewhat free, then retry. The quoted name matches the actual Undo label. This describes inability to create the cache and provides the source's space/retry advice. It does not assert that storage is necessarily full, call the failure corruption, confuse storage with RAM, prescribe deleting files, or guarantee that freeing space will fix every cause.

Independent review replaced an initial “have more space” construction with `hoengq di` (somewhat empty/free), avoiding a storage-capacity expansion reading. The explicit `ndaw gihgi neix` locator means in this machine; it avoids suggesting the user must empty the not-yet-created cache itself. `gihgi` is attested machine, not the incorrectly guessed bare `gih`. `rom vwnzgen` identifies file storage.

Confidence is moderate for the composed technical wording, high for the failure/consumer distinction. “Machine” is a broader, less modern device paraphrase; the complete free-storage collocation and sentence idiomaticity are not independently attested specialist terminology or native-human usability certification. These are stated quality limits, not a claim of universal fluency.

Full review of related existing strings found no concrete defect; retain:
- `ui_could_not_complete_the_edit`: “AN Paint gaij mbouj ndaej. %1$s” — functional inability to perform the edit, followed by its detail.
- `ui_please_try_again`: “Cingj caiq guh.” — polite retry instruction.

No other string, locale or full catalogue receives review credit from this batch.

## Evidence

[Sawloih Cuengh-Gun OCR](https://dokumen.pub/sawloih-cuengh-gun-ocr.html): main-dictionary G38/L803 `gihgi` machine; H35/L1022 `hoengq` empty/blank with a physical-space example; H22 `hawj`; R26 `rom`; C17 `caiq`; `gaij` change/modify. Both integrator and reviewer checked the critical machine/empty distinction. The dictionary supports components, not an exact technical UI sentence.

[2025 terminology announcement](https://www.guangximinzubao.cn/szbzw/html/2025-09/03/content_54472.htm), item 102, uses `soqgawq` for data in a standardized compound. The integrator directly retrieved its text at L23 this batch. The reviewer opened the page but could not extract the term list, so this is not claimed as a second independent retrieval.

A search result for [2023-11-22 primary prose](https://www.guangximinzubao.cn/szbzw/page/21/2023-11/22/04/2023112204_pdf.pdf) showed `dieg hoengq` for vacant ground. Direct opening failed. It is supplementary search evidence only, not a directly verified IT phrase, and is unnecessary to the dictionary-supported component choice.

## Actual consumers

`RasterHistory.kt:22,51`: `capture` and `importSnapshot` throw this localized IOException when the session directory is not already a directory and `mkdirs()` fails. Both precede temporary-file creation. `EditorDraftRecovery.kt:50` places production history under `context.cacheDir/classic-history`; this is local file storage, not working-memory allocation.

`PaintDocument.checkpoint` captures before adding an Undo entry, and `commitShape` checkpoints before drawing. `ClassicPaintActivity.editFailed` uses the complete edit wrapper with the failure message, or the complete retry fallback when no message exists; memory and size errors have separate branches. `receiveStartup` also composes this wrapper/fallback. No literal error-detail formatting is reapplied to the inserted text.

Inspected `FullResolutionStorageTest.unavailableUndoStorageAbortsEditWithoutChangingTheImage`: a regular file is used as the history parent, so directory creation fails. The test catches IOException, retains the checked white pixel and finds no Undo entry. This illustrates unavailable storage, not exclusively a full disk. It was not executed here. The separate `importSnapshot` failure path was statically checked; no runtime claim is made for it.

## Verification and remaining work

- All 1,595 base non-tree entries matched the live remote tree and local bytes/executable modes. Review head matched the prior receipt; no pending or uncertain write remained. Develop was unchanged at `412aab0c604060fb66fbd2edc6bb05572d10b56d`; disjoint Navajo work is untouched.
- Resource checks preserved all 322 existing Zhuang elements and the source attributes. No XML, duplicate identity, placeholder, Android escape, literal-token or manifest errors.
- 61 existing host tests passed in 5.758 seconds: `test_translations`, `test_translation_boundaries`, `test_string_importance`, `test_current_localization_contracts`.
- JDK execution passed 16 English/Zhuang static and wrapper-composition cases, including actual failure text, retry fallback, percent-looking details, blank/null details and the Zhuang Undo-label reference. These are not Android resource compilation.
- Six static bindings across three resources, directory-failure ordering, production cache location and checkpoint-before-edit checks passed. The temporary source checker initially used incomplete method headers; correcting that harness invocation resolved its failure. No production defect was inferred. `git diff --check` passed.
- No Android SDK/Kotlin compiler is available. No Android build, Robolectric, native/device, TalkBack or rendered-layout execution. Exact-head Actions status is reported separately; no CI, merge or release pass is claimed.

Presence is now 323 typed Zhuang resources: P0 81/94, P1 158/249, P2 81/305 and P3 3/71. Across 171 offered options, missing P0/P1/P2/P3 counts are 150/1,333/30,048/7,478; 46 options have complete direct presence. Presence is not linguistic acceptance, English fallback is not translation, and scope exclusions remain. Continue the [P0/P1 completion and all-translated-string review plan](p0-p1-release-plan-20261106.md); release remains gated.
