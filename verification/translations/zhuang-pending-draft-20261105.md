# Zhuang pending-draft status, 5 November 2026

## Scope and language review

The live review branch was reconciled at parent `3f0e0f59789c4510ebb5f3223a45ce780b26911c`, tree `2586a04a0b45f36e5224b94a68da0d4f2163df0e`. No write was pending or uncertain. This fills missing P1 `ui_draft_pending`. All 287 preceding typed resources remain unchanged; the total is 288. Only canonical XML and this report change.

Independent review recommended the existing not-yet-autosaved phrasing, meaning “AN Paint has not yet autosaved.” This accurately describes the queued draft state without promising success or instructing the user to wait. It deliberately shares wording with the existing initial not-yet-saved notice rather than inventing a queue term. The explicit distinction between initially unsaved and queued is therefore not expressed in the text. Older stored drafts may still exist; the notice concerns pending current state.

Evidence:

- [Sawloih Cuengh-Gun OCR](https://dokumen.pub/sawloih-cuengh-gun-ocr.html), retrieved by the reviewer, defines `mboujcaengz` as not yet, with a person-not-yet-arrived example. It also defines `caj` as wait, but that alone does not establish a natural software status using the proposed waiting constructions, so they were not adopted.
- [Guangxi Minzu Bao, “Gangj Vahgun Vujsenh Cab Vahcuengh”, 3 December 2014](https://www.guangximinzubao.cn/szbzw/html/2014-12/03/content_11259.htm), first found by the reviewer and then directly retrieved, pairs `Mboujcaengz guh sat` with not completed and includes ordinary not-yet-going usage. Its discussion concerns language contact and local speech, not computing terminology.

Confidence is **moderate overall**, with strong support for the not-yet meaning. Technical `gag rom` follows the project's existing autosave convention; this batch does not establish it as authoritative terminology. No native-human certification is claimed. Canonical Android XML owns current wording.

## Actual consumer

The sole binding is `ClassicPaintActivity.scheduleAutosave`. After checking autosave readiness, blocked state and destruction, it advances the draft generation, assigns this status, removes an older queued callback and posts the next callback after 1,500 ms, or immediately when stopped. Assigning the pending label does not write the draft.

`saveDraftIfReady` retains its generation/readiness guards and defers for 400 ms while busy or an input gesture is active. Actual writing uses the existing saving notice. Success and failure select distinct existing saved/failed notices. The pending status is included in the normal status resource; busy/saving display may temporarily replace that normal status. No timing, lifecycle, storage, failure or status-layout logic changes.

## Verification

Work and tests used the available temporary filesystem. No unrelated work was removed to address the full main workspace.

- All 171 offered-option catalogue checks and the importance manifest passed. Existing nodes, source attributes, ordered arguments, numerals, literal tokens, newline escapes and XML escaping are preserved.
- `python -m unittest -v test_translations test_translation_boundaries test_string_importance test_current_localization_contracts`: **61 tests passed in 10.362 seconds**.
- Two host Java XML-to-string cases check nonempty English/Zhuang labels and unchanged no-argument formatting. These are not Android resource compilation.
- Temporary token-aware Kotlin checks verify the sole binding, readiness guards, queued callback replacement/delay, busy/gesture deferral, distinct saving/saved/failed notices and normal-status presentation route. These are static checks, not timer or autosave execution.
- Base snapshot verification matched Git blobs and executable modes for **1,279 materialized files**, retaining **288** unmaterialized entries. Publication verifies the complete path/mode/type/blob overlay, expected-parent non-force lease and exact remote bytes.

Inspected but not run: `WorkspaceRefinementTest.autosaveRunsWhileEditingAndRestoresPixelsNameToolAndSettings` waits through autosave, inspects stored data and restores pixels/settings while retaining the document's unsaved-to-destination state. It does not assert this pending label. Inspection is not runtime evidence for the timing, failures or text. No permanent per-edit wording mirror or test package is added.

Zhuang presence is P0 **69/94**, P1 **157/249**, P2 **61/305**, P3 **1/71**. Across 171 options, missing resources are P0 **162**, P1 **1,334**, P2 **30,068**, P3 **7,480**; 46 options have complete presence. Scope remains 59 scoped catalogues and 112 outside-scope catalogues with explicit English fallback. Presence is not fluency or runtime acceptance.

Android SDK/Kotlin compiler are unavailable here. Android compilation, Robolectric, timers, lifecycle, actual autosave/failure, TalkBack and status layout were not executed. Exact-head Actions state is checked after publication and reported separately. No merge, release or CI-pass claim is made.
