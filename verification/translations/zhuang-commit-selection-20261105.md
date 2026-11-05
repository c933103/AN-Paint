# Zhuang commit-selection action, 5 November 2026

## Scope and wording

The live review branch was reconciled at parent `239cdc28d7eafa396503e62a6d218378eea6c18b`, tree `7a4fdc4393e77d5c0e3536da8438c41fd6957f37`. No write was pending or uncertain. This fills missing P1 `ui_commit_selection`. All 277 preceding typed resources remain unchanged; the total is 278. Only canonical XML and this report change.

Independent wording/context review recommended a completion paraphrase, backtranslated as “Finish the selection” or “Complete the selection operation”. It covers both applying floating content and ending an unchanged selection. A provisional “Use the selection” rendering did not clearly communicate completion. A proposed “Put the selection into the image” rendering was rejected because a nonfloating selection does not add pixels.

Language evidence:

- [Guangxi Minzu Bao, “Daxboh Daejnga’nga”, 21 May 2025](https://www.guangximinzubao.cn/szbzw/html/2025-05/21/content_53548.htm), directly retrieved, uses `Guh liux gij neix` after completing described actions. This supports completion with a following nominal object, not the exact software label.
- [Wiktionary's Zhuang `guh` entry](https://en.wiktionary.org/wiki/guh#Zhuang), verb sense 8, supports doing a task. This is secondary dictionary evidence, not a native UI attestation.
- [Parallel Zhuang/Chinese agricultural prose on Rauz](https://bbs.rauz.net.cn/rauz-38816-13-1.html), directly retrieved, pairs selecting suitable land with `Senj dieg ngamqhab`. It supports the selection verb, not the complete noun phrase or graphics meaning. Existing project usage of the selection noun aids consistency but is not linguistic proof.

Confidence is **moderate for the complete wording**. The paraphrase is supported by completion usage and the actual consumer, but its idiomatic UI naturalness is not independently established. The main dictionary timed out during this batch; an indexed classifier-paper excerpt could not be retrieved in full and is not used as primary evidence here. No native-human certification or official technical-term status is claimed. Canonical XML owns the wording.

## Actual consumer

`ClassicPaintActivity` uses this label for the rectangular-selection and lasso tools' apply button. Polygon and curve tools have their own finish labels. The complete localized resource is assigned to visible button text and accessibility description; its action calls `PaintCanvas.applyPending`.

`PaintCanvas.applyPending` calls `PaintDocument.finishSelection`. With floating content, that method draws the selection into the current bitmap using its geometry, commits its image credits and marks the document dirty. With nonfloating content, it does not redraw pixels. Both paths clear and recycle the selection and notify display/state listeners; no current selection is a no-op.

Finishing the selection does not itself write an image file or create a fresh undo checkpoint. Movement/insertion history is managed elsewhere, and normal change notifications may drive the application's existing autosave behavior. No save guarantee, promise to preserve all off-canvas selected pixels, or cancel/revert meaning is introduced. No rendering, selection, history or autosave implementation changes.

## Verification

- All 171 offered-option catalogue checks and the importance manifest passed. Existing nodes, source attributes, ordered arguments, numerals, literal tokens, newline escapes and XML escaping are preserved.
- `python -m unittest -v test_translations test_translation_boundaries test_string_importance test_current_localization_contracts`: **61 tests passed in 52.681 seconds**.
- Two host Java XML-to-string cases check nonempty English/Zhuang labels and unchanged no-argument formatting. They do not compile Android resources.
- Temporary token-aware Kotlin checks verify the rectangular/lasso binding, complete label/accessibility assignment, apply-to-finish route, floating-only drawing/credit commitment, common selection cleanup and absence of a direct file write or new checkpoint in `finishSelection`. These are static checks, not Android execution.
- Base snapshot verification matched Git blobs and executable modes for **1,291 materialized files**, retaining **269** unmaterialized entries. Publication verifies the complete path/mode/type/blob overlay, expected-parent non-force lease and exact remote bytes.

Inspected but not run: `ClassicWorkspaceTest.rectangularSelectionMovesAndUndoRestoresOriginal` checks a moved selection's committed pixels and undo; `freeFormSelectionAndInsertedImagesCompositeThroughTheirMasks` checks lasso and inserted-image compositing through masks. Neither inspection is execution evidence for this Zhuang label or the unchanged-selection path. No permanent per-edit wording mirror or test package is added.

Zhuang presence is P0 **69/94**, P1 **154/249**, P2 **55/305**, P3 **0/71**. Across 171 options, missing resources are P0 **162**, P1 **1,337**, P2 **30,074**, P3 **7,481**; 46 options have complete presence. Scope remains 59 scoped catalogues and 112 outside-scope catalogues with explicit English fallback. Presence is not fluency or runtime acceptance.

Android SDK/Kotlin compiler are unavailable here. Android compilation, Robolectric, selection compositing, unchanged-selection behavior, undo, TalkBack and button layout were not executed. Exact-head Actions state is checked after publication and reported separately. No merge, release or CI-pass claim is made.
