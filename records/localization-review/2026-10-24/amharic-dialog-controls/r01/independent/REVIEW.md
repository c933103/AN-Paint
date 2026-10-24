# Independent review: Amharic common dialog controls

Date: 2026-10-24 UTC. Production source: `66be61df27c5359bffc32d56db21f3949899f873`; tree `870c5a584120d92710be516af0dc3b3847b183d9`.

## Decision

- `string/ui_ok` — **retain** `እሺ`. High confidence within this bounded static review.
- `string/ui_done` — **hold** `ተከናውኗል`. Exact lexical attestation is strong, but target-language interpretation beside the actual failed-save/restore notice remains unresolved. No replacement is recommended.
- `string/ui_cancel` — **retain** `ይቅር`. High confidence within this bounded static review.
- `string/ui_apply` — **retain** `ተግብር`. High confidence within this bounded static review.

Three retained, zero revisions, one hold. “Retain” means retain the proposed wording after this independent evidence review, not native-reader sign-off, production implementation, or release approval. These four keys are separate from the prior 69 ready and 11 held keys. None was added to the production resource.

## 1. OK → እሺ

The retained AOSP Settings generic `okay` pair is exact (English line 571; Amharic line 245). AOSP Gallery2 corroborates the label, and the independent LibreOffice stock `_OK` record at lines 130–133 also uses `_እሺ`. The accelerator is not part of the proposed Android label. The glossary's competing `ይሁን` does not require replacing this strongly attested Android convention.

Primary lexical sources: [AOSP Settings, pinned Amharic XML](https://android.googlesource.com/platform/packages/apps/Settings/+/7c598253ff60f06f8e6fe046f18fd88e9daa72d3/res/values-am/strings.xml), [LibreOffice, pinned PO](https://github.com/LibreOffice/translations/blob/681a7f1e79cd6e27496259dab7940c8e490059de/source/am/cui/messages.po#L130-L133).

Both exact-key consumers attach a null positive-button listener to a message helper: [ClassicPaintActivity](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L1586-L1587) and [AssemblyActivity](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/AssemblyActivity.kt#L117-L121). Their role is acknowledgement/dismissal, including error messages. There is no separate application-specific mutation callback and no basis for a success, Save, Apply, or terms-consent reading.

## 2. Done → ተከናውኗል

The proposed spelling exactly matches AOSP Settings `done` (English 577; Amharic 248) and Gallery2 `done` (English 286; Amharic 121). These are two AOSP products, not two unrelated translation authorities. The pair is good evidence of an established interface convention, not proof of native interpretation in every AN-Paint context.

Primary lexical sources: [AOSP Settings, pinned XML](https://android.googlesource.com/platform/packages/apps/Settings/+/7c598253ff60f06f8e6fe046f18fd88e9daa72d3/res/values-am/strings.xml), [AOSP Gallery2, pinned XML](https://android.googlesource.com/platform/packages/apps/Gallery2/+/c0712a1daee50e52cd6f3e8e7698ddb8da3e1bcb/res/values-am/strings.xml).

The ten direct references require distinguishing these effects:

- Two exception notices display the message that image credits could not be saved or restored. [ClassicPaintActivity 231–240](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L231-L240) dismisses the notice; [MediaGalleryActivity 49–66](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/MediaGalleryActivity.kt#L49-L66) finishes the activity. Neither callback retries, saves, restores, or establishes success.
- About, legal, and language views close. The legal Done action is not acceptance of terms. Gallery and legacy-credit Done actions exit their views. Previously accepted edits or lifecycle cleanup must not be erased from the explanation.
- [Drawing settings 1553–1572](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L1553-L1572) update live and schedule autosave in the toggles/sliders before Done. Done simply closes the settings dialog.
- [GalleryCredits 100–146](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/GalleryCredits.kt#L100-L146) replaces the null listener on show: it calls `save()` and dismisses only if that returns true. Validation or I/O errors return false. Dismissal also invokes the caller's cleanup callback. This is attempted accept/save-and-close, not dismissal-only and not a claim that saving has already succeeded.
- The source addendum binds the injected vertical-feedback callback to [LocaleNotification 175–183](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/LocaleNotification.kt#L175-L183): it removes the notice and cancels its timers. It does not change the underlying operation. Instantiation is conditional on the vertical-layout branch, not evidence that Amharic renders that branch.

**Hold rationale:** the proposed form has completed-result wording, and the supplied sources do not independently establish that an Amharic reader understands it as finishing the interaction rather than reporting successful save/restore beside that failure notice. Morphology alone does not prove the conventional button is wrong; English “Done” is also a conventional completion label. This is an evidence hold, not a diagnosed mistranslation or English-source defect.

**To resolve:** obtain contextual linguistic evidence for the actual failure notice and the contrasting live-settings/credits-save contexts. Do not silently translate unchanged “Done” as “Close”, “OK”, or “Save”. If a real source-label/caller defect is established, correct English first, flag the affected term across languages, then review each language individually.

## 3. Cancel → ይቅር

AOSP Settings `cancel` (English 569; Amharic 244) and Gallery2 `cancel` (English 115; Amharic 58) exactly support the proposed generic label. Both sources use `ሰርዝ` for Delete. The glossary's competing Cancel `ሰርዝ` and LibreOffice's noun-style `መሰረዣ` remain legitimate evidence of alternative product conventions, not reasons to collapse Cancel into Delete or Undo.

Primary lexical sources: [AOSP Settings](https://android.googlesource.com/platform/packages/apps/Settings/+/7c598253ff60f06f8e6fe046f18fd88e9daa72d3/res/values-am/strings.xml), [AOSP Gallery2](https://android.googlesource.com/platform/packages/apps/Gallery2/+/c0712a1daee50e52cd6f3e8e7698ddb8da3e1bcb/res/values-am/strings.xml).

All 21 direct occurrences support abandoning the current interaction, with caller-specific effects. Important qualifications:

- [AdvancedColourDialog 304–327](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/AdvancedColourDialog.kt#L304-L327) explicitly restores the original colour preview and runs its close callback. It does not undo separately saved palette entries.
- [PaintCanvas 429–436](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/PaintCanvas.kt#L429-L436) shows that cancelling trim clears the pending trim and refits. Entering trim already applies pending canvas work. Cancel therefore cannot be described as blanket Undo.
- ImportSelection cleans up the current staged file and preview. In [AssemblyActivity 247–260](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/AssemblyActivity.kt#L247-L260), the cancellation callback advances to the next batch item. It is not a promise to abort the entire batch. Staged-copy cleanup is not deletion of the original provider file.
- SaveOptionsDialog invokes its cancel callback, which clears pending after-save/share state. ImageResizeDialog invokes cancellation through `onDismiss` when not accepted. Many other negative controls simply dismiss their prospective form or chooser. None grants a universal “no side effects” or “revert all prior changes” promise.

## 4. Apply → ተግብር

The exact AOSP Settings pair (English 579; Amharic 249) fits an action requesting that selected input take effect. The supplied bounded glossary reference independently corroborates `apply` → `ተግብር`, entry 149, PDF page ordinal 12. This reviewer independently checked the AOSP record, but did not re-render or authenticate the glossary's public mirror.

Primary lexical source: [AOSP Settings](https://android.googlesource.com/platform/packages/apps/Settings/+/7c598253ff60f06f8e6fe046f18fd88e9daa72d3/res/values-am/strings.xml). Bounded corroboration: [ICT glossary mirror, entry 149](https://oromianeconomist.com/wp-content/uploads/2017/08/ict-glossary-in-afaan-oromoo-amharic-and-tigarinya.pdf#page=12).

The three exact-key consumers validate input before changing it: [NumericSlider 60–76](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/NumericSlider.kt#L60-L76), [canvas dimensions 1012–1027](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L1012-L1027), and [AssemblyPositionDialog 29–43](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/AssemblyPlacementDialog.kt#L29-L43). Invalid input or exceptions can keep the form open. NumericSlider can accept an unchanged value without triggering a new change callback. No file-save or unconditional-success meaning is added. No acceptance transfers to Apply to all, Apply crop, Apply bounds, or Apply to these images.

## Verification and boundaries

- Original manifest SHA-256: `5955bf3fa6f1e3f072b44c56948166446ad91d5c6111576e5bc2b0036db0d944`. All 52 listed files match. Original packet was not edited.
- All 29 original source copies reproduce their bound Git blob identities. Two separately supplied, same-commit source files also reproduce their blob identities and are retained under `source-addendum/`. Total: 31 verified source copies considered.
- Independent exact-key scan of the bounded original source corpus matches all 36 ledger references across 17 direct caller files. `callback-audit.json` records the effect and primary source lines for every occurrence.
- All 16 exact lexical record slices match the six retained snapshots; candidate forms are NFC and parse correctly as Android XML strings. All four target keys remain absent from the supplied production Amharic file.
- Reused external snapshots are not fresh network retrieval. Supplied production provenance, rather than an independent branch-head re-fetch, establishes the reported commit/tree. This is not a fresh exhaustive repository-wide caller search.
- No native-reader, rendered-layout, speech/accessibility, lifecycle/runtime, build, CI, Work-task, production, deployment, or release result is claimed. Overall supplied production coverage remains 12 present and 705 missing of 717 containers.
- No whole glossary PDF, extracted text, or page image is republished here. Bounded evidence does not imply permission to republish the complete work.
