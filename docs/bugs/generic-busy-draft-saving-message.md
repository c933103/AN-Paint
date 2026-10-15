# Investigate whether credit attachment can overlap non-autosave I/O

**Status:** Open reachability investigation, not a confirmed user-visible bug. This documentation-only issue-style tracking PR was narrowed after [Codex source review](https://github.com/c933103/AN-Paint/pull/72#discussion_r4278211178). The original claim that ordinary import/save overlap establishes a wrong draft-saving diagnosis is not supported by the traced callers and is withdrawn pending a reachable sequence.

**Source baseline:** develop `647a4b5647cabf3e51cb6dcf20d41ae08143ccdb`, checked 15 October 2026. No runtime/device reproduction or code/resource/test change. [Project board](https://github.com/c933103/AN-Paint/pull/39) · [Translation tracker](https://github.com/c933103/AN-Paint/pull/56). Keep open/draft as an investigation; no wording change is required unless the hypothesized misleading path is established.

## Confirmed code facts

- [ClassicPaintActivity.kt L1411–1412](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L1411-L1412) maintains generic `busy` state for counted I/O operations, not only autosaving.
- [attachLegacyImageCredit L1432–1435](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L1432-L1435) responds to `busy` with `ui_the_draft_is_saving_try_again_shortly`.
- The message is accurate when autosaving: [saveDraftIfReady L1596–1618](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L1596-L1618) sets `autosaving=true` before `beginIo` and clears it on completion. [editAction L915–916](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L915-L916) also uses the wording under an explicit autosaving guard.
- Resource values: [EN L413](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/res/values/strings.xml#L413), [FR L473](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/res/values-fr/strings.xml#L473), [JA L521](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/res/values-ja/strings.xml#L521) are faithful draft-saving descriptions; no independent translation defect is established.

## Reachability gap and counterevidence

The two current attachment invocations are activity-result paths: [LEGACY_CREDITS L1177–1178](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L1177-L1178) and [GALLERY_IMAGE L1213–1215](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L1213-L1215). The gallery attachment runs before that result starts [readImage L1232–1233](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L1232-L1233).

[Queued startup results L252–263](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L252-L263) dispatch only while `!busy`. The normal overlap while a selector is open is autosaving, for which the current wording is accurate. The existence of unrelated `beginIo` calls alone does not prove a non-autosave attachment overlap. Directly forcing private state/calling the helper would not demonstrate a reachable user path.

## Hypothesis and bounded investigation criteria

If a legitimate Android lifecycle/event sequence reaches an attachment result while a non-autosave operation is active, the draft-saving explanation could be misleading. No such sequence is established here. No lost credit, stuck operation, failed autosave or current user-visible impact is claimed.

- [ ] Trace valid launch/result/onNewIntent/recreation sequences and entry-point guards against current source. Identify an actual non-autosave operation and how an attachment result can arrive before it finishes.
- [ ] If reachable, create a behavior-level regression using the real event sequence, with evidence of operation kind, `busy` and `autosaving`; do not manufacture an impossible combination or bypass normal guards solely to make it fail.
- [ ] Only then select operation-aware/generic wording, preserving the accurate draft-saving message on real autosaving and all credit/concurrency safeguards. Review any changed localized text in every affected locale.
- [ ] If no supported reachable sequence is found, record the bounded negative result and consider closing/deprioritizing this investigation without altering truthful normal-path wording. Inability to find a path is not proof of global impossibility.
- [ ] Preserve idle attachment, real autosave overlap, pending-input order, credit deduplication and successful completion behavior in any eventual regression work.

## Next action and dependencies

Establish or reject the specific reachability hypothesis using real source/lifecycle evidence before authorizing a semantic “fix” on this basis. Earlier French/Japanese context-review holds remain evidence of the generic-state observation, not proof of runtime impact; reconcile their status with the reachability result. This investigation is distinct from the confirmed background, picker-classification and count bugs. No implementation or language-acceptance credit is claimed.
