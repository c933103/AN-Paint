# Independent Amharic file-action review

Production: `66be61df27c5359bffc32d56db21f3949899f873`. Input manifest seal: `c5f5fbc2177a40735a59ff8097869f77eb249ed33aec317f52bcc39f92fe7e79`.

**Verdict: retain all five exact drafts; revise 0, hold 0, implement 0.** Retention is bounded independent AI linguistic/source review, not native-speaker or runtime acceptance.

## Exact decisions

### string/ui_new: RETAIN

English: New…
Retained displayed text: **አዲስ…**

Retain the concise adjective used as a File-menu label. The image noun is supplied by the context and following New image title. Do not add an imperative merely to match the action buttons: the English is itself an elliptical menu label.

The menu calls confirmReplacement, which first applies pending geometry; only its continuation opens the fresh dimensions dialog. Selecting the menu item does not yet create a new image. Canceling later is not a promise to restore pre-menu pending geometry.

Keep U+2026, because size input/dialog interaction follows. Do not substitute three ASCII periods.
Confidence: semantics high; UI idiom medium-high.
Quoted XML-text SHA-256: `c817e189d29f6633d56082977f189a2a220117fd11065013895c6c37399bb9bb`.

Source: [code 1](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L835-L846), [code 2](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L1074-L1080), [code 3](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L1012-L1028), [code 4](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/PaintCanvas.kt#L443-L449).

### string/ui_new_image: RETAIN

English: New image
Retained displayed text: **አዲስ ምስል**

Retain the adjective-plus-noun title. The adjective precedes the image noun; both components are directly attested. This is a dialog title, not an instruction to open, save, name or immediately replace a file.

For fresh=true the dimensions dialog uses this title. A valid Apply checks dimensions and the memory budget, applies pending content, calls document.newImage, resets the name and saved target, and dismisses. newImage creates the blank background-colour bitmap through replace; normal replacement clears previous history.

No ellipsis, matching the source title.
Confidence: semantics high; UI idiom medium-high.
Quoted XML-text SHA-256: `219eda8bf4625d23b8693a706c2d4d8d7f9c0ba4e777801fc28216621d7673f4`.

Source: [code 1](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L1012-L1028), [code 2](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/PaintDocument.kt#L197-L220).

### string/ui_load_image: RETAIN

English: Load image…
Retained displayed text: **ምስል ክፈት…**

Retain the contextual Open verb. It faithfully describes loading an existing image as the current document, not inserting/pasting it into the existing canvas. Open is directly attested as a file-dialog/button command. The glossary uses the same verb for generic Load and Insert, so a mechanical choice would obscure this distinction. This is contextual translation, not an unannounced correction to English.

The File menu passes import=false into launchOpen after confirmation. ACTION_OPEN_DOCUMENT falls back to GET_CONTENT; replacement occurs only after a successful result, optional frame/page/size selection and decode. import=true follows the distinct paste path. Picker or intermediate dialog cancellation may leave the existing document in place. Temporary cache-file cleanup is not deletion of the selected saved original.

Keep U+2026: the picker and sometimes further choices intervene.
Confidence: semantics high; UI idiom medium-high.
Quoted XML-text SHA-256: `650c355dc8541b3ce85f50a6d99ddee6c5f2d7ae5023e58a586aae1c51a03b85`.

Source: [code 1](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L835-L846), [code 2](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L1082-L1102), [code 3](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L1177-L1185), [code 4](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L1250-L1253), [code 5](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L1266-L1342), [code 6](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ImportSelection.kt#L50-L122).

### string/ui_keep_editing23: RETAIN

English: Keep editing
Retained displayed text: **አርትዖቱን ቀጥል**

Retain exactly. The full phrase is independently recovered in paired AOSP Contacts source and in AndroidX PDF editor resources at a July 2026 commit. The short imperative is compatible with the other retained action commands and existing Amharic change-background command. It is not a noun meaning saved edit or a promise to roll changes back.

The negative confirmation button has a null listener, with native AlertDialog behavior retained by the inspected builder. It dismisses the choice without invoking the replacement, Save or finish continuation. applyPending has already run before dirty checking and can commit trim/polygon/curve/selection content, so Keep editing does not restore an untouched pre-prompt state. The same prompt covers external-image handling and Back.

No added ellipsis.
Confidence: semantics high; UI idiom medium-high.
Quoted XML-text SHA-256: `a3925a6ec843d152e9cfc13828a04d564825c0261d6ee51bb137fa327c112d59`.

Source: [code 1](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L1074-L1080), [code 2](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/PaintCanvas.kt#L443-L449), [code 3](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/VerticalUi.kt#L118-L152), [code 4](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L1136-L1144), [code 5](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L1639-L1647).

### string/ui_discard_changes23: RETAIN

English: Discard changes
Retained displayed text: **ለውጦችን አስወግድ**

Retain the plural changes object plus the short discard imperative. Full AndroidX resources independently pair the discard verb with English Discard and use the same changes noun in the unsaved-changes context; the glossary separately attests discard versus delete. The complete candidate phrase is compositionally sound. The Google exact-phrase search excerpt is supplemental only and is not promoted to a verified full-page source.

The neutral button calls the requested continuation without first saving. In New/Load this can merely open another dialog or picker, which may later be canceled; successful replacement clears the current document/history. External open and Back have their own continuations. The button is not an immediate bitmap-erasure operation, a saved-file deletion command, an Undo/revert command, or a guarantee that recovery drafts are destroyed. Autosave is visible in onStop, so no data-destruction claim is accepted.

No added ellipsis: preserve the source label; it is a confirmation choice, not the File-menu initiation label.
Confidence: semantics high; UI idiom medium.
Quoted XML-text SHA-256: `ac248bc21dcd65e988a670b26f8c1ea04ceb6b80e72eb68591c8c41bee5a624c`.

Source: [code 1](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L1074-L1080), [code 2](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L1012-L1028), [code 3](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L1177-L1185), [code 4](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/PaintDocument.kt#L197-L220), [code 5](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L1136-L1144), [code 6](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L1639-L1647).

## Evidence adjudication

- Keep editing is no longer dependent on an index excerpt. Complete paired English/Amharic source was recovered from the official AOSP mirror, at commit 15922c5aae0b20f4ad0bc3a30919246c49c30e03 (2017-02-02), and independently corroborated in AndroidX PDF editing at 9546570831c2780f7356c68bcf8e2cc722cff746 (2026-07-24). Both pairs are included with verified Git blobs and SHA-256 in source-receipts.json.
- Google Open terminology is now directly verified in a full extracted first-party help page. AndroidX also supplies paired Open button evidence.
- Google Discard changes remains an exact-phrase search-index excerpt. Direct Amharic retrieval returned HTTP 429; alternate fetches were inaccessible. The English counterpart was retrieved. Do not call this full-page Amharic verification. The candidate remains acceptable from the independently attested noun and imperative in the same unsaved-changes setting; the excerpt is corroboration only.
- The ICT/ELRC PDF is primary-authored but third-party hosted. Targeted parsed entries were checked; page screenshots failed with Cache miss. Treat it as component evidence, not an exclusive current style authority.

### Primary source links

- [androidx_am](https://github.com/androidx/androidx/blob/9546570831c2780f7356c68bcf8e2cc722cff746/pdf/pdf-viewer/src/main/res/values-am/strings.xml), Git blob `ad7fa2f98edb4bb6e51cc4436ab97c42a8854fa6`, SHA-256 `74d22bbc96be4cdca708d495c56eb5608d484aae6ca341f6192770c7150f86a2`.
- [androidx_en](https://github.com/androidx/androidx/blob/9546570831c2780f7356c68bcf8e2cc722cff746/pdf/pdf-viewer/src/main/res/values/strings.xml), Git blob `91790ec4ad869d04d43c8419053a9fa183c62865`, SHA-256 `487c6535c98aa92d0378349d3f7f0778915e27d0382230ca0f768737ce9ce00d`.
- [contacts_am](https://github.com/aosp-mirror/platform_packages_apps_contacts/blob/15922c5aae0b20f4ad0bc3a30919246c49c30e03/res/values-am/strings.xml), Git blob `7b3a3ed2d76ff1065cad646869bfd208f913a088`, SHA-256 `ead42602543a8e463cd805bffb952810bf8c1b6d7db956f0c711e121d1eda87c`.
- [contacts_en](https://github.com/aosp-mirror/platform_packages_apps_contacts/blob/15922c5aae0b20f4ad0bc3a30919246c49c30e03/res/values/strings.xml), Git blob `d8bcd57a10da822369980babc4dcd56b677aa8ca`, SHA-256 `5236e6562a7f738c6ce251a24adcc0911058b1225b395997e2dc50d8cd363285`.
- [ICT/ELRC terminology PDF](https://oromianeconomist.com/wp-content/uploads/2017/08/ict-glossary-in-afaan-oromoo-amharic-and-tigarinya.pdf), entries 728, 1488, 1928, 944, 863, 1657 and 1522.
- [LibreOffice Amharic shortcut help](https://help.libreoffice.org/latest/am/text/shared/04/01010000.html), Ctrl+N action.
- [Google Accessibility help](https://support.google.com/accessibility/answer/90559?hl=am), Open dialog/button in computer file attachments.
- [Google Play Amharic help](https://support.google.com/googleplay/android-developer/answer/13849271?hl=am), excerpt-only; [retrieved English counterpart](https://support.google.com/googleplay/android-developer/answer/13849271?hl=en).

## Register and source policy

The two New labels remain adjective/title noun phrases. The other three use conventional short command forms, consistently with verified Android buttons and the existing Amharic change-background label. Formal/polite instruction prose elsewhere is not a reason to mix registers within these controls.

No English-source correction is proposed by this translation review. Do not silently rewrite Discard changes as Do not save to compensate for possible lifecycle concerns. If a source contract defect is established later, correct English, flag every affected language, then review each language individually.

## Integrity, coverage and limits

- 16 input manifest entries match SHA-256.
- All 11 complete source copies match their supplied Git blobs and the independently fetched, non-truncated production Git tree.
- All five canonical English values and quoted proposed XML text hashes match the draft packet.
- All five exact keys are absent from the supplied Amharic catalogue.
- All five XML fragments parse; no placeholders or source punctuation are introduced or removed.
- Coverage denominator is 716 translatable string keys plus one plural key: 717. Three translatable=false filename strings are excluded. Coverage remains 12 present and 705 missing.
- Four independently fetched complete Android source XML copies recompute to their connector-reported Git blob hashes.

Coverage remains **12 present / 705 missing**. Five retained candidates are separate from the prior 19. No production additions were made.

- No Work task started or resumed; no delegation onward.
- No product resource or code edits, app builds/tests, CI, release or remote publication. XML parsing and hash checks are review-integrity checks only.
- No native-speaker consultation, rendered UI, glyph/line fit, screen-reader, or device/lifecycle verification.
- Input source semantics checked at the stated production commit; no assertion that it remains branch HEAD after review.
- No acceptance of the entire unsaved-changes prompt, Save/Cancel, surrounding hints, other locales or inherited external-resource strings.
- Existing 12 resources, previous 19 reviewed candidates and all unrelated holds remain unchanged.
- The Google Amharic exact-phrase citation remains excerpt-only; original glossary binary hash and visual page check are unavailable.
