# Commons import-resize guidance incorrectly promises selected background

**Status:** Open bug; documentation-only issue-style tracking PR, not an applied fix. Keep open/draft pending separately reviewed implementation and acceptance evidence.

**Source baseline:** develop `647a4b5647cabf3e51cb6dcf20d41ae08143ccdb`, checked 15 October 2026. **Evidence boundary:** independently confirmed linguistic/static-source finding only; no runtime/device reproduction, CI or whole-language acceptance. [Project board](https://github.com/c933103/AN-Paint/pull/39) and [translation review](https://github.com/c933103/AN-Paint/pull/56) track related work. Issues remain disabled; visibility/settings are unchanged.

## Expected and actual

Expected: the resize/import explanation reflects the background policy of the current import. For Commons images forced onto white, it must not promise the selected opaque background.

Actual: `ui_estimates_include_the_current_canvas_and_clipboard_sampled` says “Imports use the selected opaque background” in the non-native resize explanation. The Commons import path carries `whiteBacking=true` outside the dialog and explicitly fills transparency with white, regardless of the selected background colour.

Impact: a user resizing a transparent Commons image while a nonwhite background is selected receives misleading guidance about the imported result. This is a context/wording bug, not a request to remove the existing Commons white-backing behavior or an allegation that that policy is itself incorrect. French and Japanese faithfully reproduce the English claim.

## Static path and evidence

- [ImageResizeDialog.kt L15–35](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/java/org/catrobat/paintroid/classic/ImageResizeDialog.kt#L15-L35) chooses the explanation from `memoryRequirements.hasNativeWork`; the dialog has no `whiteBacking` context.
- [Commons gallery result L1225–1233](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L1225-L1233) calls `readImage(... whiteBacking=provider==IllustrationSource.COMMONS)`.
- [Import selection and resizing L1270–1297](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L1270-L1297) preserve that flag through `askToResize` and the callback to `decodeImage`, without exposing it to the explanation.
- [decodeImage L1299–1308](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L1299-L1308) fills transparent pixels using `Color.WHITE` with `DST_OVER` when the flag is true.
- Complete explanatory resource: [EN L184](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/res/values/strings.xml#L184), [FR L318](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/res/values-fr/strings.xml#L318), [JA L366](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/res/values-ja/strings.xml#L366). The memory-estimation, smaller-copy and unchanged-original statements are separate and should be retained accurately.

Independent review receipt: [French priority batch 02](https://github.com/c933103/AN-Paint/pull/56#issuecomment-6182490731).

## Bounded fix and acceptance

- Make the explanation aware of forced-white versus selected-background policy, or use wording accurate for both. Preserve existing Commons compositing and ordinary import behavior.
- Test the real oversized Commons import/resize branch with a transparent image and a nonwhite selected background: guidance must not promise that selected colour; accepted decode must use the existing white policy and preserve opaque pixels.
- Add an ordinary non-Commons control using the selected background, plus cancellation/no-document-mutation and applicable native-codec guidance controls.
- Preserve memory limits, estimate qualification, smaller-copy detail loss and source-file immutability. Do not weaken guards to avoid showing the dialog.
- Enumerate/update every affected localized value if text changes, and re-review the full explanations in their actual contexts. A shared call-site repair must cover all locales/fallbacks, not only French/Japanese.

## Next action and dependencies

Implement the smallest context-aware explanation selection, then add actual import/resize regression coverage and complete current-source review/test gates. Coordinate held entry re-review with PR56; no translation-count credit until the corrected source/context is verified. Independent of the other bug trackers. This PR adds only this bug document.
