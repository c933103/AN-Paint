# Generic busy guard incorrectly reports that a draft is saving

**Status:** Open bug; documentation-only issue-style tracking PR, not an applied fix. Keep open/draft pending separately reviewed implementation and acceptance evidence.

**Source baseline:** develop `647a4b5647cabf3e51cb6dcf20d41ae08143ccdb`, checked 15 October 2026. **Evidence boundary:** independently confirmed linguistic/static-source finding only; no runtime/device reproduction, CI or whole-language acceptance. [Project board](https://github.com/c933103/AN-Paint/pull/39) and [translation review](https://github.com/c933103/AN-Paint/pull/56) track related work. Issues remain disabled; visibility/settings are unchanged.

## Expected and actual

Expected: an operation blocked by generic I/O reports that an operation is in progress, unless autosaving is actually the reason.

Actual: `attachLegacyImageCredit` checks `busy` and emits `ui_the_draft_is_saving_try_again_shortly` (“The draft is saving. Try again shortly.”). `busy` is set by generic `beginIo` operations such as image import/save, so the condition does not establish draft saving.

Impact: misleading status tells users the wrong reason an image-credit action is unavailable. The refusal while busy and request to retry can remain; this report does not claim lost credits, a stuck operation or demonstrated autosave failure. The resource is valid in its actual autosaving guard.

## Static path and evidence

- [Generic state management, ClassicPaintActivity.kt L1411–1412](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L1411-L1412) increments/decrements `operationsInFlight` and derives `busy` from those operations.
- [Import start L1257–1259](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L1257-L1259) and [write start L1345–1348](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L1345-L1348) use generic `beginIo`.
- [attachLegacyImageCredit L1432–1435](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L1432-L1435) selects the draft-saving diagnosis from `busy` alone.
- [Actual autosaving guard L916](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L916) uses this resource appropriately.
- Resource values: [EN L413](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/res/values/strings.xml#L413), [FR L473](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/res/values-fr/strings.xml#L473), [JA L521](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/res/values-ja/strings.xml#L521). Faithful translations inherit the source-context mismatch.

Independent review receipt: [French priority batch 02](https://github.com/c933103/AN-Paint/pull/56#issuecomment-6182490731).

## Bounded fix and acceptance

- Use a truthful generic operation-in-progress message at the generic busy guard, or accurately select a message from the real active operation state. Retain the draft-saving message where autosaving is confirmed.
- Exercise an attempted credit attachment while a non-autosave import/save operation holds `busy`: no draft-saving claim, no credit mutation, and attachment can be retried after completion.
- Exercise the real autosaving guard and preserve its accurate message. Cover idle success and existing error handling/credit deduplication.
- Test multiple in-flight operations so messaging/state does not imply idle after only one finishes. Preserve the existing concurrency/input guards and draft scheduling.
- Apply any new or changed text across every affected locale and independently review complete values/context; verify fallback and placeholder contracts.

## Next action and dependencies

Select generic/context-correct wording, add behavior-level state/message regressions and complete current-source review/test gates. Coordinate full-entry context re-review with PR56 before accepted-current credit. Independent of the other newly tracked wording defects. This PR changes no operation state, app resources or tests.
