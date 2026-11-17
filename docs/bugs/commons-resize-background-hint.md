# Import-resize guidance misstates context-specific transparency handling

**Status:** Open bug; documentation-only issue-style tracking PR, not an applied fix. Keep open/draft pending separately reviewed implementation and acceptance evidence.

**Source baseline:** develop `647a4b5647cabf3e51cb6dcf20d41ae08143ccdb`, checked 15 October 2026. **Evidence boundary:** independently confirmed linguistic/static-source finding only; no runtime/device reproduction, CI or whole-language acceptance. [Project board](https://github.com/c933103/AN-Paint/pull/39) and [translation review](https://github.com/c933103/AN-Paint/pull/56) track related work. Issues remain disabled; visibility/settings are unchanged.

## Expected and actual

Expected: the resize/import explanation reflects the actual destination path: Commons insertion uses forced white, ordinary insertion retains alpha over existing canvas pixels, and Load Image replacement composites onto the selected background.

Actual: `ui_estimates_include_the_current_canvas_and_clipboard_sampled` says “Imports use the selected opaque background” in the non-native resize explanation. The Commons import path carries `whiteBacking=true` outside the dialog and explicitly fills transparency with white, regardless of the selected background colour.

Impact: a user resizing a transparent Commons image while a nonwhite background is selected receives misleading guidance about the imported result. Ordinary insertion also must not be described as selected-background replacement: its transparency is composited over existing canvas pixels. This is a context/wording bug, not a request to change any of these compositing policies. French and Japanese faithfully reproduce the English claim.

## Static path and evidence

- [ImageResizeDialog.kt L15–35](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/java/org/catrobat/paintroid/classic/ImageResizeDialog.kt#L15-L35) chooses the explanation from `memoryRequirements.hasNativeWork`; the dialog has no `whiteBacking` context.
- [Commons gallery result L1225–1233](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L1225-L1233) calls `readImage(... whiteBacking=provider==IllustrationSource.COMMONS)`.
- [Import selection and resizing L1270–1297](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L1270-L1297) preserve that flag through `askToResize` and the callback to `decodeImage`, without exposing it to the explanation.
- [decodeImage L1299–1308](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L1299-L1308) fills transparent pixels using `Color.WHITE` with `DST_OVER` when the flag is true.
- Complete explanatory resource: [EN L184](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/res/values/strings.xml#L184), [FR L318](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/res/values-fr/strings.xml#L318), [JA L366](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/res/values-ja/strings.xml#L366). The memory-estimation, smaller-copy and unchanged-original statements are separate and should be retained accurately.

Independent review receipt: [French priority batch 02](https://github.com/c933103/AN-Paint/pull/56#issuecomment-6182490731).

## Correction to the original test plan

[Codex review](https://github.com/c933103/AN-Paint/pull/71#discussion_r4278213686) correctly identified an invalid original non-Commons test expectation. [ClassicPaintActivity L1313–1324](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L1313-L1324) calls `paste` for insertion and `replace` for Load Image. [PaintDocument L395–402](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/java/org/catrobat/paintroid/classic/PaintDocument.kt#L395-L402) retains insertion alpha as a floating mask, later composited over the existing canvas; [replace L197–201](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/java/org/catrobat/paintroid/classic/PaintDocument.kt#L197-L201) instead uses selected background. [CanvasColourBoundaryTest L22–41](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/test/java/org/catrobat/paintroid/local/CanvasColourBoundaryTest.kt#L22-L41) encodes the green-canvas/white-selected-background insertion control. This test source was inspected, not executed in this review. The initial expectation that ordinary insertion uses selected background is withdrawn.

## Bounded fix and acceptance

- Make the explanation aware of forced-white insertion, ordinary insertion over existing pixels, and replacement onto selected background, or use wording accurate for all three. Preserve the existing compositing behavior.
- Test the real oversized Commons import/resize branch with a transparent image and a nonwhite selected background: guidance must not promise that selected colour; accepted decode must use the existing white policy and preserve opaque pixels.
- Add separate controls: ordinary non-Commons insertion retains alpha and composites over existing canvas pixels even when the selected background differs; Load Image replacement composites onto the selected background. Keep cancellation/no-document-mutation and applicable native-codec guidance controls.
- Preserve memory limits, estimate qualification, smaller-copy detail loss and source-file immutability. Do not weaken guards to avoid showing the dialog.
- Enumerate/update every affected localized value if text changes, and re-review the full explanations in their actual contexts. A shared call-site repair must cover all locales/fallbacks, not only French/Japanese.

## Next action and dependencies

Implement the smallest context-aware explanation selection, then add actual import/resize regression coverage and complete current-source review/test gates. Coordinate held entry re-review with PR56; no translation-count credit until the corrected source/context is verified. Independent of the other bug trackers. This PR adds only this bug document.
