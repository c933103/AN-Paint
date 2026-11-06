# Zhuang Undo-history data warning and command review

Date: 2026-11-06 UTC. Base `f71e06a7326a26ac8808b916a8ae03c482307b7d`, tree `b49dacca0d7c11cc078426c0012a29e4367271df`.

## Change and bounded review

Added missing P0 `ui_unexpected_data_in_the_undo_cache` to canonical `Paintroid/src/main/res/values-b+za/strings.xml`. It identifies AN Paint's stored Undo data and says that other data remains after the required image data. This is a precise functional explanation of the consumer's unexpected trailing payload, not a diagnosis that every byte is unknown, a memory-budget failure, or a generic corruption message. All 314 preceding resource nodes, attributes and original prefix bytes remain unchanged.

Independent review accepted the addition unchanged at moderate compositional confidence. `Laeng` applies “behind/after” to serialized data order; `yaekaeu miz` expresses required presence; `lij miz` preserves remaining data. This is an authored technical sentence, not an attested whole software phrase. The existing image term is retained without claiming a new independent dictionary attestation for that word in this batch.

Three existing full values were also reviewed and retained:
- `ui_undo`: the canonical XML uses Android outer quoting around `siu`; the intended display label is `siu`. The dictionary's revocation/cancellation sense supports this command. This is not a claim of standardized contemporary software terminology.
- `ui_redo`: `Caiq guh` is a coherent short command in its Undo/Redo context. The consumer restores history rather than re-executing any arbitrary earlier command.
- `ui_the_undo_cache_is_damaged`: describes stored Undo data as damaged, fitting its current hash/header/dimension failure consumers. Applying the damage word to digital data is a reasonable technical extension.

The four values form this entire review cohort. Prior withdrawn approvals are not restored, unrelated strings are not cleared, and the full translated-string release review remains incomplete.

## Evidence and actual consumers

[The Sawloih Cuengh-Gun dictionary OCR](https://dokumen.pub/sawloih-cuengh-gun-ocr.html) supports `siu` revocation/cancellation (S.htm 37/52), `laeng` behind/after (L.htm 6/49), `lij` still (L.htm 21/49), and required-presence, repeat, storage and damage vocabulary. The OCR warns of incomplete proofreading. [The official ninth terminology announcement](https://www.guangximinzubao.cn/szbzw/html/2025-09/03/content_54472.htm), item 102, supports `soqgawq` for data within a standardized compound. These are component and construction evidence, not native-speaker or whole-sentence usability certification.

`RasterHistory.read` checks the magic value and dimensions, then reads the exact pixel payload through an `InflaterInputStream`. Only after those required pixels does `input.read() != -1` select the new resource. It describes extra **decompressed payload**, not arbitrary bytes after the compressed file's stream. `restore` first invokes `read(entry, null)` before selecting/allocating an output and running the pixel-writing pass. This source ordering does not establish every possible concurrent-file or runtime failure outcome.

The existing damaged-cache resource has three bindings: imported snapshot digest mismatch; imported header/dimension mismatch; and restoration header/dimension mismatch. Missing files, decompression exceptions and truncated reads can carry other exception text; this warning is not a universal corruption catch-all.

`EditIcon.UNDO` and `REDO` resolve the full current resources. `ActionButton` supplies those labels to accessibility descriptions and tooltips in both the main editor and assembly editor. Main-editor Undo first cancels pending input and only otherwise restores history. Redo cancels pending input, then restores redo history. Assembly actions use their own state-history transitions. Quoted command names in both history-data notices remain consistent with the current Undo label.

## Verification

- Fresh review head reconciled with the preceding publication. Develop remained `412aab0c604060fb66fbd2edc6bb05572d10b56d`; separate Navajo work is untouched. All 1,588 base file contents and executable modes matched the reviewed checkout.
- One unique missing scalar added, preserving source attributes, placeholders, literal-token/numeric/newline boundaries and XML/Android escaping. All 171 offered catalogues and the priority manifest pass structural validation. XML blob `14d858b84cda9dcb58a758795add8f738ca2bab5`, 31,215 UTF-8 bytes.
- 61 host tests passed in 5.699 seconds: `test_translations`, `test_translation_boundaries`, `test_string_importance`, `test_current_localization_contracts`.
- Eight host Java static resource-format checks passed across English and Zhuang. These read XML templates, not Android's compiled display strings.
- Temporary token-aware source checks verified all six resource bindings, required-payload-before-extra-byte ordering, validation-before-writing ordering, distinct damaged-cache paths, main/assembly command consumers and matching quoted Undo label. `git diff --check` passed.
- `FullResolutionStorageTest.damagedUndoEntryIsRejectedBeforeChangingPixels` was inspected, not run. It tests malformed compressed history and preserved pixels, not this exact extra-decompressed-payload branch. No runtime pass for that branch is claimed.

Zhuang has 315 typed resources: P0 74/94, P1 158/249, P2 80/305, P3 3/71. Global missing counts across 171 options are 157/1,333/30,049/7,478 for P0–P3; 46 options have complete presence. Presence does not establish fluency, full review or release readiness.

Android SDK/Kotlin compiler are unavailable here. Android build/AAPT, runtime error display, Undo/Redo execution, corruption handling, layout, accessibility and glyph rendering were not tested. No merge or release is claimed. Only canonical XML and this compact report change; temporary checks and wording mirrors are not published. The existing conditional P0/P1 completion and all-translated-string review release plan remains in force.
