# Amharic view controls: six reviewable drafts, one held caption

Production 66be61df27c5359bffc32d56db21f3949899f873; tree 870c5a584120d92710be516af0dc3b3847b183d9. Fourteen complete source copies and nine primary lexical snapshots are included with hashes and immutable locators.

These are drafts for independent checking. Fit entire canvas in view remains author HOLD for canvas/viewport terminology precision. No English source defect established.

## string/ui_fit

English: Fit

Proposed XML: `<string name="ui_fit">"በመስኮቱ ልክ"</string>`

Status: review; UI confidence medium-high.

Exact nonfuzzy LibreOffice Fit To Window value transferred to a viewport-fitting button. It denotes window-fit scale, not resizing image content. The English source is shorter, so this is contextual reuse, not an identical English/Amharic pair.

Displayed button in status zoom controls, Navigate options and canvas-bounds editor. Calls paintCanvas.fit: adjusts zoom/pan to include whole canvas plus outlying trim/floating-selection bounds with handle padding. No image resampling or document-dimension change. May return early if viewport too small. Not the separate Fit image to canvas selected-image placement operation.

Source: https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L668-L675, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L768-L773, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L1055-L1055, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/PaintCanvas.kt#L177-L192

## string/ui_fit_entire_canvas_in_view

English: Fit entire canvas in view

Proposed XML: `<string name="ui_fit_entire_canvas_in_view">"የመሳያ ቦታውን በሙሉ አሳይ"</string>`

Status: hold; UI confidence low-medium.

HOLD: drawing-area noun phrase is composed and may mean viewport/editor area rather than bitmap canvas. Whole-area show imperative does not independently establish the precise fit/view relation. No accepted canvas technical term or complete caption attestation recovered. Do not implement or silently promote a replacement.

Accessible caption for fit status button; also EditIcon.FIT label used for contentDescription and tooltip. Same viewport-only fit operation as ui_fit, including outlying selected/trim bounds rather than excluding them. Exact text is accessibility wording but source inspection is not screen-reader acceptance.

Source: https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L668-L675, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ActionButton.kt#L12-L34, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/PaintCanvas.kt#L177-L192

## string/ui_draw_again

English: Draw again

Proposed XML: `<string name="ui_draw_again">"ድጋሚ ሳል"</string>`

Status: review; UI confidence medium.

Exact Android user-redraw phrase transferred from lock-pattern entry, not repaint. Contextual risk remains: AN Paint returns remembered non-navigation tool, possibly selection/fill. Independent reviewer must assess whether this conventional return-to-drawing label is sufficiently broad; alternative return phrase in lexical report is unaccepted.

Navigate options button chooses drawingTool remembered by showToolOptions whenever tool is not ZOOM; default PENCIL. It returns to the preceding non-navigation tool and Draw panel, not Undo/Redo, replay a stroke, or automatically draw. selectTool applies pending content before switch. Non-ZOOM includes selection/fill/etc, so label is conventional return-to-drawing-workspace phrasing, not guarantee that every prior tool makes a mark.

Source: https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L732-L744, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L768-L773, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/PaintCanvas.kt#L153-L158

## string/ui_pixel_grid33

English: Pixel grid

Proposed XML: `<string name="ui_pixel_grid33">"የፒክሰል ፍርግርግ"</string>`

Status: review; UI confidence medium.

Composed pixel+grid noun phrase from separate Android attestations, not an exact phrase match. Names an overlay rather than snapping, downsampling or changing image pixels.

View command toggles paintCanvas.grid; grid lines are drawn only when enabled and zoom>=8 (800%). Image-pixel rulers depend on grid toggle, not that same threshold. A display overlay, not grid baked into document pixels or image resolution change.

Source: https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L862-L864, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/PaintCanvas.kt#L278-L286, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/PaintCanvas.kt#L83-L85

## string/ui_fullscreen33

English: Full screen

Proposed XML: `<string name="ui_fullscreen33">"ሙሉ ገጽ ዕይታ"</string>`

Status: review; UI confidence medium-high.

Exact Android Full screen wording reused as a mode label, not resizing content. Source hides editor controls/status bar but does not guarantee immersive navigation-bar hiding.

View command toggles fullscreen and calls syncFullscreen. Hides root controls except workspace, sidebar/status rails; adds Show controls return button and requests Android fullscreen status-bar flag. Does not claim navigation-bar immersive mode, image resizing, saving, or permanently hiding controls.

Source: https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L871-L871, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L1574-L1585

## string/ui_show_controls

English: Show controls

Proposed XML: `<string name="ui_show_controls">"መቆጣጠሪያዎችን አሳይ"</string>`

Status: review; UI confidence medium-high.

Derived shortening of Android Show device controls, removing device qualifier, with independently attested Controls noun. Refers to restoring app controls by leaving fullscreen, not device-control settings.

Full-screen workspace return button sets fullscreen=false then syncFullscreen restores editor root controls/rails and system UI flag subject to panel state. It does not open device-control settings or change canvas image content.

Source: https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L1574-L1585

## string/ui_navigate

English: Navigate

Proposed XML: `<string name="ui_navigate">"እይታ ማንቀሳቀሻ"</string>`

Status: review; UI confidence medium.

Composed view-movement tool noun from attested pan/movement root and view noun. Explicit view object distinguishes pan from moving drawing content; not exact Navigate phrase attestation. General Navigate alternative in LibreOffice is not proof of pan-specific meaning.

PaintTool.ZOOM label shown as View tool tile. chooseTool selects View and paintCanvas.selectTool first applies pending trim/polygon/curve/floating content. Subsequent ordinary single-finger drag pans and single tap neither draws nor zooms; pinch is separate zoom behavior. Navigation here is canvas inspection, not route guidance or file browsing.

Source: https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/PaintDocument.kt#L14-L22, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ToolButton.kt#L10-L12, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L490-L497, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L732-L744, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/PaintCanvas.kt#L153-L158, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/PaintCanvas.kt#L739-L744, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/PaintCanvas.kt#L770-L804

## Primary evidence

Full source records, alternatives and exclusions are in lexical-evidence/README.md and the paired PO/Android evidence JSON. Exact primary-source URLs:

https://raw.githubusercontent.com/LibreOffice/translations/681a7f1e79cd6e27496259dab7940c8e490059de/source/am/officecfg/registry/data/org/openoffice/Office/UI.po

https://raw.githubusercontent.com/LibreOffice/translations/681a7f1e79cd6e27496259dab7940c8e490059de/source/am/helpcontent2/source/text/shared/01.po

https://raw.githubusercontent.com/LibreOffice/translations/681a7f1e79cd6e27496259dab7940c8e490059de/source/am/helpcontent2/source/text/shared/02.po

https://raw.githubusercontent.com/GNOME/gimp/7d518c7971e80719ce30f70ec44b55e49ab2aeb7/po/am.po

https://android.googlesource.com/platform/packages/apps/Gallery2/+/c0712a1daee50e52cd6f3e8e7698ddb8da3e1bcb/res/values-am/strings.xml?format=TEXT

https://android.googlesource.com/platform/packages/apps/Gallery2/+/c0712a1daee50e52cd6f3e8e7698ddb8da3e1bcb/res/values/strings.xml?format=TEXT

https://android.googlesource.com/platform/packages/apps/Settings/+/7c598253ff60f06f8e6fe046f18fd88e9daa72d3/res/values-am/strings.xml?format=TEXT

https://android.googlesource.com/platform/packages/apps/Settings/+/7c598253ff60f06f8e6fe046f18fd88e9daa72d3/res/values/strings.xml?format=TEXT

https://raw.githubusercontent.com/LibreOffice/translations/681a7f1e79cd6e27496259dab7940c8e490059de/source/am/svx/messages.po

## Exclusions and limits

No English-source defect established in this bounded inspection. Draw again denotes return to prior drawing-workspace tool, not automatic stroke replay. Fit description is inclusive of whole canvas, not exclusive of outlying handles/content.

Existing Zoom in/out translations and all36 ready additions plus Crop HOLD excluded.

ui_canvas_zoom initial caption is overwritten by formatted ui_canvas_zoom_771f84 in updateStatus; both excluded from this format-free group.

No generic claims that tool switching cannot commit pending content.

Separate ui_fit_selection34 / Fit image to canvas changes selected-image placement and is not this viewport-only Fit group.

Fourteen complete source copies, exact commit/tree/blob binding; no exhaustive whole-repository consumer-search claim.

No native-speaker, runtime, glyph/layout, screen-reader or lifecycle acceptance.

No production edit, Work task, app builds/tests, CI or release.

Palette uncertainty, optional Horizontal and all held Help remain separate.

Primary exact-wording reuse remains contextual transfer, not AN Paint native acceptance.

Fit-caption, Pixel grid and Navigate contain composed terminology; Fit-caption remains explicitly held.

Draw again return-to-prior-tool semantics require scrutiny beyond lexical equivalence with Android Redraw.

GIMP fuzzy fit/pan/grid/canvas-looking matches excluded; Microsoft corrupted Ethiopic extraction not used.

No new independent acceptance; prior36 ready and Crop HOLD remain separate.

Coverage unchanged:12 present/705 missing of717. Prior36 reviewed ready candidates and Crop HOLD unchanged; six new reviewable drafts plus one held caption, zero new independent acceptances or implementation.
