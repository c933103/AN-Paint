# Amharic Edit transforms: seven reviewable drafts and one held proposal



Production 66be61df27c5359bffc32d56db21f3949899f873, tree 870c5a584120d92710be516af0dc3b3847b183d9. All twelve complete source files are included under source/, freshly bound through commit/tree/blob reads.

This is original translation drafting, not independent acceptance. All eight exact keys are missing and disjoint from the previous29 reviewed additions. Crop to selection is explicitly held for precision review; seven other drafts are reviewable but not accepted.



## string/ui_flip_horizontal

English: Flip horizontal

Proposed XML: `<string name="ui_flip_horizontal">"በአግድም ገልብጥ"</string>`

Status: review; UI confidence medium.

Directional modifier and reflection stem are attested in nonfuzzy LibreOffice; imperative and joined prefix are original grammatical adaptation. Distinguish left/right mirror from180° rotation.

After applyPending, setScale(-1f,1f) reflects the entire current bitmap left/right. It is not rotating by180°, changing screen orientation, or transforming only a floating selection.

Source: https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L854-L854, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/PaintDocument.kt#L453-L459



## string/ui_flip_vertical

English: Flip vertical

Proposed XML: `<string name="ui_flip_vertical">"በቁመት ገልብጥ"</string>`

Status: review; UI confidence medium.

Same reflection family and vertical modifier; top/bottom mirror, not orientation or rotation. Joined prefix is editorial composition, not a verbatim quotation.

After applyPending, setScale(1f,-1f) reflects the entire current bitmap top/bottom, not a180° turn.

Source: https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L855-L855, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/PaintDocument.kt#L453-L459



## string/ui_rotate_90_clockwise

English: Rotate 90° clockwise

Proposed XML: `<string name="ui_rotate_90_clockwise">"90° ወደ ቀኝ አሽከርክር"</string>`

Status: review; UI confidence medium-high.

Android attests rotate-right imperative; LibreOffice attests90° right. Combined numeric angle is original composition; right-turn convention conveys clockwise, not moving the object right.

After applyPending, setRotate(90f) transforms the whole bitmap and then fits the canvas view. Positive Android screen-coordinate rotation is clockwise. Preserve90 and degree sign, not arbitrary rotation or horizontal flip.

Source: https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L856-L856, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/PaintDocument.kt#L453-L459



## string/ui_rotate_180

English: Rotate 180°

Proposed XML: `<string name="ui_rotate_180">"180° አሽከርክር"</string>`

Status: review; UI confidence medium-high.

Android rotate imperative plus exact180° half-turn amount; no direction added because the source has none.

After applyPending, setRotate(180f) gives the whole bitmap a half-turn. English intentionally does not specify direction; either direction gives same result.

Source: https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L857-L857, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/PaintDocument.kt#L453-L459



## string/ui_invert_colours

English: Invert colours

Proposed XML: `<string name="ui_invert_colours">"ቀለሞችን ገልብጥ"</string>`

Status: review; UI confidence medium.

Nonfuzzy LibreOffice colour-inversion context and Android inversion terminology support the root. Explicit plural color object separates channel inversion from spatial mirroring and swatch swapping.

After applyPending, invert complements low24 RGB bits while preserving high8 alpha bits. It is not swapping foreground/background or geometrically reflecting the image.

Source: https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L858-L858, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/PaintDocument.kt#L467-L476



## string/ui_clear_image

English: Clear image

Proposed XML: `<string name="ui_clear_image">"ምስሉን አጽዳ"</string>`

Status: review; UI confidence medium.

Android Clear effects attests the imperative; image object is an original addition. Means clearing image content in context, not deleting its saved file or creating transparency.

After applyPending, clear finishes selection, checkpoints, fills the bitmap with current background and clears committed image credits. It does not delete a saved image file, replace with transparent canvas, clear clipboard, or create a new document size.

Source: https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L859-L859, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/PaintDocument.kt#L478-L478



## string/ui_crop_to_selection

English: Crop to selection

Proposed XML: `<string name="ui_crop_to_selection">"በምርጫው መጠን ከርክም"</string>`

Status: hold-for-precision-review; UI confidence low-medium.

Author HOLD: the selected-size wording is not directly attested and may misleadingly suggest resizing or just selection dimensions. Do not include this provisional value in an implementation candidate set. Alternate according-to-selected-content construction in lexical report also requires precision/naturalness review. English itself has no established defect.

Requires selection; otherwise shows select-area-first. Renders the transformed selection into its bounding rectangle, finishes selection, then replaces canvas as edit and fits view. Masked/rotated transparent margins are flattened over background by replace. It is not deletion of selected content or a promise to preserve original canvas bounds.

Source: https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L852-L852, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/PaintDocument.kt#L349-L364



## string/ui_delete_selection

English: Delete selection

Proposed XML: `<string name="ui_delete_selection">"የተመረጠውን ሰርዝ"</string>`

Status: review; UI confidence medium.

Android directly attests Delete and selected-item syntax, but selected pixel content is AN Paint-specific composition. Selected-object phrasing avoids implying merely clear/deselect selection. Gallery-item deletion is supporting vocabulary, not equivalent runtime behavior.

Requires selection; otherwise shows select-area-first. Nonfloating selection is checkpointed and its mask/rectangle filled with current background. Floating content is removed without committing it; clearSelection removes the selection object. Not mere deselection, saved-file deletion or guaranteed new standalone undo checkpoint for already-floating content.

Source: https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L850-L850, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/PaintDocument.kt#L373-L377



## Primary lexical evidence

See lexical-evidence/README.md for exact nonfuzzy PO records, paired Android strings, alternatives and excluded fuzzy matches. sources.json contains immutable source revisions and SHA-256. The full source copies and targeted record JSON are included for independent checking.

- libreoffice-am-ui.po: https://raw.githubusercontent.com/LibreOffice/translations/681a7f1e79cd6e27496259dab7940c8e490059de/source/am/officecfg/registry/data/org/openoffice/Office/UI.po

- libreoffice-am-help01.po: https://raw.githubusercontent.com/LibreOffice/translations/681a7f1e79cd6e27496259dab7940c8e490059de/source/am/helpcontent2/source/text/shared/01.po

- libreoffice-am-help02.po: https://raw.githubusercontent.com/LibreOffice/translations/681a7f1e79cd6e27496259dab7940c8e490059de/source/am/helpcontent2/source/text/shared/02.po

- gimp-am.po: https://raw.githubusercontent.com/GNOME/gimp/7d518c7971e80719ce30f70ec44b55e49ab2aeb7/po/am.po

- android-gallery2-am.xml: https://android.googlesource.com/platform/packages/apps/Gallery2/+/c0712a1daee50e52cd6f3e8e7698ddb8da3e1bcb/res/values-am/strings.xml?format=TEXT

- android-gallery2-en.xml: https://android.googlesource.com/platform/packages/apps/Gallery2/+/c0712a1daee50e52cd6f3e8e7698ddb8da3e1bcb/res/values/strings.xml?format=TEXT

- android-settings-am.xml: https://android.googlesource.com/platform/packages/apps/Settings/+/7c598253ff60f06f8e6fe046f18fd88e9daa72d3/res/values-am/strings.xml?format=TEXT

- android-settings-en.xml: https://android.googlesource.com/platform/packages/apps/Settings/+/7c598253ff60f06f8e6fe046f18fd88e9daa72d3/res/values/strings.xml?format=TEXT

## Shared consumer chain

Edit command panel → panelButton → busy/autosaving checks → exact menuActions lambda → PaintCanvas.applyPending where specified → PaintDocument operation. Common source: https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L327-L363, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L551-L556, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L924-L931, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/PaintCanvas.kt#L443-L449, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/PaintDocument.kt#L197-L218, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/PaintDocument.kt#L308-L337, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/PaintDocument.kt#L461-L465

Complete twelve source copies included; no exhaustive repository consumer-search claim.

Commands use common panel buttons, including text/contentDescription/tooltip; that binding is not screen-reader acceptance.

Flip/rotate/invert/clear applyPending first, including pending trim/polygon/curve and floating content. Crop/delete use selected-content branches without that preliminary applyPending call.

Common buttons gate busy/autosaving and catch specified edit failures; wording is an operation label, not a guaranteed success claim.

No application build/test, CI, production edits, Work task or release.

No English source defect established at this bounded source inspection.

No native-speaker, runtime, glyph/layout or lifecycle validation.

All eight exact phrases are original compositions/adaptations, not quotations of independently accepted AN Paint labels.

LibreOffice selected source records are nonfuzzy. GIMP tempting full Crop/Delete Selection/transform matches are fuzzy/empty/obsolete and excluded.

Microsoft corrupted Ethiopic PDF extraction is not used.

Android imperative roots are directly attested; noun/verb alternatives and register remain subject to independent checking.

No new acceptance, implementation or resolution of existing Palette/Horizontal/Help holds.

Coverage remains12 present/705 missing of717. Previous29 reviewed additions remain unapplied. No source correction established; preserve all existing substantive holds.
