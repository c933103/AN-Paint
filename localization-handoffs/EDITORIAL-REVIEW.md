# Editorial review checkpoint

Input: `a537ece7b363d7cb32014c3978c1db44ff1e2864` (the frozen 2,334-slot combined authoring handoff). No translations are changed by this review checkpoint.

## First pass: the long help text in Cherokee, Navajo and Tai Nüa

The assembly guide, compact help and editor guide in each of these three languages keep the expected 8, 1 and 10 paragraphs. A targeted comparison found the original technical names, controls' numeric anchors, color hex values, provider names and keystroke tokens in their corresponding paragraphs. This is not evidence of grammatical or semantic equivalence.

- Cherokee editor guide, paragraph 2: the label `Pale Violet` remains in English while the same handoff already has separate Cherokee wording for the swatch. Reconcile the label after its wording is validated; keep `#5B67FF` literal.
- Cherokee editor guide, paragraphs 3 and 7: the generic `slider` and trailing `stroke smoothing` are still in English. Decide on descriptive wording and check it against both actual control captions. Do not collapse brush-stroke smoothing into pixel anti-aliasing.
- Navajo editor guide, paragraph 7: the brush control is described generically; verify that a reader can identify the actual Strength control. Separately validate polygon completion and rotation captions.
- Tai Nüa editor guide, paragraphs 1 and 7: `Watercolor` remains English. Check the exact localized brush label before altering the guide. In paragraph 5, cross-check that `mask` refers to the shape of the selection, not hiding or deleting a layer.
- The compact Cherokee help and all three assembly guides still need a sentence-by-sentence semantic comparison, especially around crop undo, allowed overlap and RAM fallback. The paragraph/token screen alone does not show those relationships.

New linguistic acceptances: **0**. Retain all source-facing holds. No Android resources, PR, device test or integration changes.

## Second pass: generic typeface labels saved unchanged

Checked all nine localized name slots wired into [FontCatalog](https://github.com/c933103/AN-Paint/blob/597e644c31c450d45aa6962d89564581d4434758/Paintroid/src/main/java/org/catrobat/paintroid/classic/FontCatalog.kt#L20-L27) against the frozen handoff. **15 locale-key pairs need a terminology decision**, not automatic acceptance as invariants. These are visible chooser captions; Android family IDs and bundled proper names are separate and should stay unchanged.

- Tai Nüa (`tdd`): all nine captions: `ui_sans_serif`, `ui_serif`, `ui_monospace`, `ui_sans_light`, `ui_sans_thin`, `ui_sans_condensed`, `ui_sans_medium`, `ui_cursive`, `ui_casual`.
- Navajo (`nv`), Central Nahuatl (`nch`), and Western Huasteca Nahuatl (`nhw`): `ui_sans_serif` and `ui_serif` in each. A familiar borrow is a legitimate outcome only if it distinguishes the choices for the locale. Eastern Huasteca's descriptive pair is a comparison, not a term to copy between varieties.
- When drafting Tai Nüa captions, treat fixed character spacing, stroke weight, and letter width as separate attributes. Keep light, thin and medium distinct. Keep connected handwriting and informal lettering distinct. Consult [W3C font terminology](https://www.w3.org/TR/CSS22/fonts.html#generic-font-families) for the source-side concepts and Luo's [Dehong Tai dictionary](https://openresearch-repository.anu.edu.au/bitstreams/1b27afe2-adda-4fe2-95bf-5402206be010/download) for locale vocabulary. The dictionary did not establish a conventional typeface term in this pass. No borrowed or newly coined captions are accepted here.
- Later, test Tai Nüa and Cherokee glyph rendering in the default-font chooser and long help on a real Android build before deciding whether to bundle fonts. [AOSP Android 15's font inventory](https://android.googlesource.com/platform/frameworks/base/+/android-vts-15.0_r5/data/fonts/fonts.xml) includes Noto Sans Tai Le and Noto Sans Cherokee; that is not a device-rendering result.

New linguistic acceptances in this pass: **0**. Frozen authoring file unchanged; no Android XML, app coverage or integration changes.

## Third pass: numbered format arguments across the handoff

Compared typed source and candidate strings, including each plural quantity separately, for indexed Android/Java format tokens, `%%`, and `%n`. All **691 token occurrences across 392 text cells** match their source multisets; **0 missing, added, or altered tokens** in this defined class. Ordinary percent signs in prose were not treated as placeholders. This pass does not verify grammatical placement, rendering, or application behavior. No linguistic acceptances, integration, or resource changes.

## Fourth pass: Cherokee attribution action and feedback

`gallery_copy_credit` is a button command to copy the attribution text. `gallery_credit_copied` is shown after the clipboard action succeeds. The frozen Cherokee candidates use the same phrase for both. Each of the seven other draft locales with both keys has different wording for the two contexts. Hold the Cherokee pair pending wording that distinguishes the action from its result; review the pair together. No newly accepted wording or resource changes in this pass.

Provisional replacement pair, not accepted:

- `gallery_copy_credit`: `ᏧᏬᏪᎳᏅᎯ / ᏅᏓᏳᏓᎴᏅᎯ ᎠᎪᎵᏰᏗ — ᎤᏠᏱ ᎪᏢᏅᏗ`
- `gallery_credit_copied`: `ᏧᏬᏪᎳᏅᎯ / ᏅᏓᏳᏓᎴᏅᎯ ᎠᎪᎵᏰᏗ: ᏗᏟᎶᏍᏔᏅᎯ (ᎠᏍᏆᏛᎯ)`

Word choice follows existing Cherokee app keys `gallery_credit_could_not_save`, `ui_export_recovery_copy`, and `ui_full_text_copied` on the pinned source. This supports distinguishing action and result within the app, not the naturalness of the complete phrases. Check the idiomatic attribution term and whether the completion marker is redundant. Keep both on hold.

## Typeface follow-on authoring: 15 previously unchanged captions

Below are provisional alternatives for the 15 slots flagged in the second pass. Keep the original authoring snapshot intact; these are replacements for review, not acceptances. Validate stroke endings, fixed advance versus narrow glyphs, all three stroke weights, and handwriting versus casual style. Do not change Android family IDs.

```json
{
  "tdd": {
    "ui_sans_serif": "ᥘᥤᥐ ᥟᥛᥱ ᥛᥤᥰ ᥔᥥᥢᥲ ᥟᥥᥱ ᥖᥤ ᥙᥣᥭ",
    "ui_serif": "ᥘᥤᥐ ᥛᥤᥰ ᥔᥥᥢᥲ ᥟᥥᥱ ᥖᥤ ᥙᥣᥭ",
    "ui_monospace": "ᥖᥨᥝ ᥘᥤᥐ ᥐᥧ ᥖᥨᥝ · ᥖᥣᥒᥰ ᥐᥣᥒᥲ ᥛᥫᥢᥴ ᥐᥢ",
    "ui_sans_light": "ᥘᥤᥐ ᥙᥣᥭ ᥟᥛᥱ ᥛᥤᥰ ᥔᥥᥢᥲ ᥟᥥᥱ · ᥔᥥᥢᥲ ᥛᥣᥒ",
    "ui_sans_thin": "ᥘᥤᥐ ᥙᥣᥭ ᥟᥛᥱ ᥛᥤᥰ ᥔᥥᥢᥲ ᥟᥥᥱ · ᥔᥥᥢᥲ ᥛᥣᥒ ᥖᥤ ᥔᥧᥖᥴ",
    "ui_sans_condensed": "ᥘᥤᥐ ᥙᥣᥭ ᥟᥛᥱ ᥛᥤᥰ ᥔᥥᥢᥲ ᥟᥥᥱ · ᥖᥨᥝ ᥘᥤᥐ ᥞᥤᥙᥴ",
    "ui_sans_medium": "ᥘᥤᥐ ᥙᥣᥭ ᥟᥛᥱ ᥛᥤᥰ ᥔᥥᥢᥲ ᥟᥥᥱ · ᥔᥥᥢᥲ ᥐᥣᥒ",
    "ui_cursive": "ᥘᥤᥐ ᥖᥦᥛᥲ ᥘᥒᥱ ᥛᥪᥰ · ᥖᥨᥝ ᥘᥤᥐ ᥓᥙᥴ ᥐᥢ",
    "ui_casual": "ᥞᥣᥒᥲ ᥘᥤᥐ ᥓᥬᥳ ᥐᥧ ᥝᥢᥰ"
  },
  "nch": {
    "ui_serif": "Letras ica pilquentzi tlahuasantli campa tlami ininrayas",
    "ui_sans_serif": "Letras amo quipiyaj pilquentzi tlahuasantli campa tlami ininrayas"
  },
  "nhw": {
    "ui_serif": "Letras ica piltziquitetzi tlahuazantli campa tlami ininrayas",
    "ui_sans_serif": "Letras amo quipiyaj piltziquitetzi tlahuazantli campa tlami ininrayas"
  },
  "nv": {
    "ui_serif": "Saad: niníʼáhgi ídzoh yázhí hólǫ́",
    "ui_sans_serif": "Saad: niníʼáhgi ídzoh yázhí ádin"
  }
}
```

- Tai Nüa: [Dehong dictionary](https://openresearch-repository.anu.edu.au/bitstreams/1b27afe2-adda-4fe2-95bf-5402206be010/download) supports components for tip (p. 109), narrow (p. 28), thin (p. 88), middle (p. 39), and join (introduction). The [Tai Nüa script chart](https://arhiiv.eki.ee/knab/lat/kbltdd2.pdf) is a spelling reference. Review modern narrow/join spelling, caption length, and whether light versus thin reads naturally. The descriptive compounds are not attested typeface names.
- Central and Western Huasteca Nahuatl: compare each locale's pinned app keys `ui_line`, `ui_choose_a_smaller_size`, `ui_font`, and `ui_font_family`. The loan `rayas` is deliberate for the terminal stroke description. Validate idiom and chooser length separately for both locales.
- Navajo: the pinned app supplies text and line vocabulary; [Wall and Morgan](https://upload.wikimedia.org/wikipedia/commons/6/6c/Navajo-English_Dictionary.pdf) supports lexical components, and the [Swarthmore lexicon](https://talkingdictionary.swarthmore.edu/navajo_postposition/?introduction=&lang=nav) has speaker examples for the presence/absence construction. The adapted generic endpoint term is the weakest component. Do not assume the full compounds are attested.

No linguistic acceptance, Android integration, or device verification.

## Fifth pass: source names in UI messages and unchanged entries

Reviewed the canonical combined handoff at `027c199839d7e78cf0174841fcb5a9e82f990e2c` (blob `a8ff12aacf9bd675bfffb373e79eeaa0cb372dee`). Checked 238 non-invariant string entries with one or more defined literal product names, format names, colour codes, or shortcut tokens. Three entries omit a source literal; all three omit PDF. The other 235 retained every literal checked. This is an editorial screen, not a translation, grammar check, or Android test.

- Eastern and Western Huasteca Nahuatl, `formats22_pdf_page_index`: both tell the reader to choose a page from this document but omit the format name, while neighbouring errors retain PDF. Check whether the same error can appear without a visible PDF heading. If it can, restore the literal PDF to the error so users can identify the workflow. Compare each variant's wording separately.
- Western Huasteca Nahuatl, `formats22_pdf_crop`: the draft preserves the selected-page and non-empty-region instructions but omits PDF. Check its standalone error context before accepting its omission.
- All 114 records marked invariant are identical to the typed source values in the handoff. Eight cursor-help aliases preserve `@string/ui_cursor_help31` verbatim. Equality alone does not establish that a recorded invariant is linguistically appropriate or that the alias resolves on Android.

**New wording authored, accepted or integrated: 0.** No device verification. The combined file was not changed.

## Sixth pass: PDF error context and explicit numerical limits

Candidate file: `b05fb20235ea266b4265f4236c3fb7258d6c790a` (blob `4ec048d12a74dd312d9dfd99801b5fd0a403f053`), pinned app base `597e644c31c450d45aa6962d89564581d4434758`.

- **PDF error context:** In the pinned source, `ImportSelection.kt` closes the page chooser before the import handler revalidates the page index. Classic and Assembly error callbacks can show a generic dialog afterwards, so the page message should name PDF independently of the picker. `AssemblyRenderer.kt` also passes the placed item's crop back to the PDF renderer; an output failure can be shown outside the original picker. This supports preserving PDF in the three provisional replacements (Eastern and Western Huasteca page index; Western Huasteca crop). It does not establish normal-UI reproducibility, target-language idiom, or acceptance.
- **Numerical screen:** Of the strings with distinct source and draft wording, 70 entries across the nine locales contained an explicit source numeral followed by MiB, GiB, px/pixels, %, or ° (including both ends of dashed ranges). All 120 source value occurrences had a matching standalone numeral somewhere in that candidate. This limited test does not verify the unit, duplicate counts, upper/lower bound, scope of the limit, spelled-out numbers, or the sentence's meaning. For editorial review, check source bounds and qualifiers as a unit, especially `formats22_pdf_file_size` (>0 and ≤512 MiB), the pixel-grid threshold (≥800%), and the pencil default (1 px) versus max (100 px).
- **New review flag:** The Tai Nüa editor guide (`ui_the_arrow_on_the_left_directly_below_the`) adds `90°` twice in descriptions of rectangular selection, although the pinned source specifies no angle in either description. A right-angle description may be a legitimate explanation of the shape, but it should not sound like a limit on rotation. Hold both sentences for a language check and retain the separate Rotate instruction.

New translations, linguistic acceptances, Android integration, and device verification: **0**. The combined authoring file is unchanged.

## Seventh pass: colour-range notation and duplicate short captions

Input: canonical candidate blob `4ec048d12a74dd312d9dfd99801b5fd0a403f053` at the pinned application source `597e644c31c450d45aa6962d89564581d4434758`. This is editorial review only; no rewriting or Android resource edits.

- **78 approved for unchanged technical notation in this editorial pass.** These comprise nine numeric validation hints (one per locale, `0–%1$d`), 48 HSV/HSL captions (six each across eight locales), and 21 RGB captions (three each across seven locales). [Pinned code](https://github.com/c933103/AN-Paint/blob/597e644c31c450d45aa6962d89564581d4434758/Paintroid/src/main/java/org/catrobat/paintroid/classic/AdvancedColourDialog.kt#L237-L251) binds the validation hint to an integer maximum and the captions to their respective field keys and maxima. The R/G/B, H/S/V and H/S/L names are identifiers here, not UI sentences or colour names. This records approval to retain the source notation, not 78 accepted translations; 36 other unchanged entries were outside this decision. Typography, localized numeral rendering and accessibility have not been checked on device.
- Screened 1,935 short draft captions or messages (string values up to 120 characters; matched case-insensitively with canonical Unicode normalization). After removing pairs whose English sources differ only by case or terminal punctuation, the only same-target/different-source group was `ui_batch_crop` and `ui_batch_crop_images`, repeated across Cherokee, Eastern Huasteca Nahuatl, Central Nahuatl and Tai Nüa. The first is the [action button](https://github.com/c933103/AN-Paint/blob/597e644c31c450d45aa6962d89564581d4434758/Paintroid/src/main/java/org/catrobat/paintroid/classic/AssemblyActivity.kt#L95-L98); the second is the [multi-image dialog title](https://github.com/c933103/AN-Paint/blob/597e644c31c450d45aa6962d89564581d4434758/Paintroid/src/main/java/org/catrobat/paintroid/classic/ImageCropDialog.kt#L138-L143) it opens when there are multiple images. They do not need distinct words purely to avoid duplication. The imperative/title idiom and fit in both surfaces still require language review; none of the eight strings is thereby approved.

New translations accepted or written: **0**. Unchanged technical entries approved in editorial review: **78**. Integrated: **0**. Device verified: **0**. Combined candidate file unchanged; do not treat this note as a change in app coverage.

## Eighth pass: same-width and same-height dialogs

Checked the targeted normalize-size cluster: 54 draft labels, descriptions and explanatory strings across eight locales. In [the pinned dialog](https://github.com/c933103/AN-Paint/blob/597e644c31c450d45aa6962d89564581d4434758/Paintroid/src/main/java/org/catrobat/paintroid/classic/NormalizeImagesDialog.kt#L18-L56), the live summary shows the target dimension, the range on the other axis, and the largest current dimension on the selected axis. In percent mode, the target is the input multiplied by that largest dimension and divided by 100. The accessible input name must work without the visual summary: one percentage, applied to the stated pixel reference, not a percentage and a separate pixel input.

The 16 summary drafts kept the axis swap, literal units and two newline escapes. The wording must also preserve that “placed images” reflow, but the normalization applies to every image in the assembly; source files and crop settings stay unchanged. No app behavior or visual/device result inferred from these strings.

Cherokee: the 2024 [Cherokee Language Consortium list](https://language.cherokee.gov/media/vdiic5hr/2024consortium.pdf) lists `igadvi` (percent) and `nayadvv` (width), supporting the lexical choices `ᎢᎦᏛᎢ` and `ᎾᏯᏛᎥ`; the syllabary in indexed PDF extraction is unreliable, so use the Romanized entries as cross-checks. The two Cherokee percent-mode accessibility names (`ui_normalize_width_input_percent`, `ui_normalize_height_input_percent`) put the pixel reference in parentheses after “percent.” Hold them for an explicit and idiomatic “percent of this reference size” relation when heard on their own. The supported words do not validate entire phrases, the height label, or the percentage construction.

New translations accepted or written: **0**. New integration/device verification: **0**. Combined candidate file unchanged.

## Independent wording review: batch 1 (100 `za` draft keys)

Compared each keyed draft with the pinned source in the combined handoff (blob `4ec048d12a74dd312d9dfd99801b5fd0a403f053`). K = keep current wording at editorial pass; H = hold for the stated issue. Keep is not native-speaker certification, integration, or device verification. No metadata changes. **69 keep, 31 hold, 0 new drafts, 0 integrated.**

1. `ui_drag_a_line_then_drag_twice_to_set` **K**: Two bends and early commit are both present.
2. `ui_drag_a_selection_drag_inside_to_move_square` **K**: Distinguishes move, resize, rotate and aspect lock.
3. `ui_drag_across_the_ellipse_s_bounding_box` **H**: The bounding rectangle is implied but the ellipse label is not established; align with the actual shape caption.
4. `ui_drag_between_opposite_corners_to_draw_a_five` **K**: Keeps corner-to-corner gesture, five points and outline/fill choice.
5. `ui_drag_from_the_start_to_the_end_of` **K**: Keeps the ordered start and end points.
6. `ui_drag_from_the_tail_towards_the_arrowhead_choose` **H**: Verify the tail term against the app’s arrow label; the first anchor should unambiguously be the non-head end.
7. `ui_drag_out_to_expand_in_to_trim_drag` **K**: Keeps expand/trim, move, view assistance and BG fill distinct.
8. `ui_drag_to_pan_without_drawing_pinch_with_two` **K**: Panning is non-drawing; preserves the separate two-finger gesture.
9. `ui_draw_a_crisp_one_pixel_line` **K**: Correctly retains the inclusive 1–100 pixel range and crisp edge.
10. `ui_draw_around_an_area_drag_inside_to_move` **K**: Preserves drawn selection plus all manipulations and commit.
11. `ui_draw_soft_watercolor_strokes_strength_controls_how_strongly` **H**: Verify the soft-stroke and blending terms against the watercolor tool, not a hard outline.
12. `ui_pinch_to_zoom_drag_to_pan` **K**: Distinguishes the two gestures and names both zoom directions.
13. `ui_set_radius_px_then_drag_between_opposite_corners` **K**: Radius and half-of-shorter-side limit are preserved.
14. `ui_smooth_freehand_strokes` **K**: Refers to freehand strokes rather than pixel boundaries.
15. `ui_smooth_pixel_edges_anti_aliasing` **K**: Refers to pixel boundaries and retains technical anti-aliasing.
16. `ui_tap_an_enclosed_area_adjust_tolerance_for_similar` **K**: Enclosed region, tolerance and similar colors retained.
17. `ui_pencil_keeps_crisp_one_pixel_strokes_cursor_drawing` **K**: Explicitly says any selected width, not one pixel.
18. `ui_pencil_crisp_adjustable_strokes` **K**: Intentional identical corresponding source for the pencil caption.
19. `ui_cursor_settings31` **K**: Keeps drawing-cursor settings distinct from brush settings.
20. `ui_cursor_marker_help31` **K**: Marker enlarges without changing painted stroke size.
21. `ui_cursor_pan_draw32` **K**: Preserves drag-and-start followed by the later stop tap.
22. `ui_cursor_pan_move32` **K**: Preserves positioning followed by the drawing-button tap.
23. `ui_cursor_tap_hint37` **K**: Cursor tap toggles the drawing action.
24. `ui_toolbox_and_tool_options_scroll_for_more` **K**: Toolbox and options followed by scroll cue.
25. `ui_pixel_grid_help33` **K**: Inclusive 800% threshold and ruler units preserved.
26. `ui_an_image_cannot_attach_to_itself_or_one` **H**: Translation adds edge wording to a graph rule; keep the prohibition on attaching to self or an attached image without limiting it to an edge.
27. `ui_cropped_thumbnail` **K**: Thumbnail and crop state distinguished; format slot retained.
28. `ui_drop_at_a_highlighted_edge_right_top_aligned` **K**: Both drop directions and their different alignment edges are preserved.
29. `ui_image_assembly_workspace_drag_placed_images_or_drop` **K**: Distinguishes moving placed items, snapping thumbnails and view gestures.
30. `ui_image_thumbnails_and_filenames_scroll_horizontally_for_more` **K**: Thumbnails, filenames and horizontal direction all remain.
31. `ui_invalid_image_attachments` **H**: The phrase for invalid risks reading as unlawful; use operational incompatibility rather than a legal characterization.
32. `ui_no_attachment_fits_within_the_current_coordinate_range` **K**: Distinct X/Y bound and practical smaller-image remedy.
33. `ui_some_previews_could_not_be_decoded_you_can` **H**: Confirm the removal verb means removing these assembly items, not cutting pixels or deleting source files.
34. `ui_sort_tray` **K**: Sorting thumbnails conveys the tray operation in this UI.
35. `ui_that_arrangement_overlaps_another_image_use_a_different` **H**: The source allows unplacing the attached images; edge-specific wording narrows the remedy.
36. `ui_the_assembly_exceeds_android_s_coordinate_range` **K**: Keeps the assembly-wide Android coordinate limitation.
37. `ui_the_attachment_image_is_missing` **K**: Identifies the missing attached image rather than the base image.
38. `ui_the_images_cannot_fit_within_android_s_coordinate` **K**: Keeps coordinate fit and the smaller-size remedy.
39. `ui_the_normalized_image_dimensions_are_outside_android_s` **K**: Preserves that the computed dimensions are outside Android’s range.
40. `ui_trim_from_the_original_edges_drag_the_handles` **K**: Explicitly starts at original edges and preserves source files.
41. `ui_unplace` **K**: Removes from its placed position; not deleting the image.
42. `ui_give_all_images_the_same_each_image_keeps` **H**: The generic supporting string needs an unequivocal per-image aspect-ratio guarantee and exact crop-settings wording; placeholders are intact.
43. `ui_normalize_width_input_percent` **H**: Make the percent-of-reference relationship explicit independently of the visible summary.
44. `ui_normalize_height_input_percent` **H**: Same accessible percent-of-reference requirement on the height axis.
45. `ui_about_copyright_licence` **H**: Check the About/credits menu family against the current visible captions; avoid using general information as a navigation label if the button differs.
46. `ui_catrobat_online_gallery_artwork_by_its_credited_creators` **K**: Keeps provider, online gallery, and attribution to named creators.
47. `ui_catrobat_s_own_artwork_uses_cc_by_sa` **H**: Check all referenced menu captions in order and preserve separate attribution and licence terms as distinct obligations.
48. `ui_icons_artwork` **K**: The draft distinguishes icons from artwork.
49. `ui_icons_fonts_artwork_credits` **K**: Retains icons, fonts and artwork as separate credited classes.
50. `ui_open_source_credits_and_notices` **H**: Verify the open-source term modifies the credited software, not the notices.
51. `ui_source_code_exported_including_build_scripts_and_licence` **K**: Includes source code, build scripts and licence notices in the completed export.
52. `ui_the_gallery_redirected_outside_its_supported_hosts` **K**: Unsupported URL after redirection distinguished from general network failure.
53. `ui_this_image_is_outside_the_supported_catrobat_gallery` **K**: Retains restriction to explicitly supported Catrobat gallery images.
54. `ui_too_many_gallery_redirects` **K**: Excessive redirect count, not a refused initial address.
55. `gallery_image_component_unavailable` **H**: Draft narrows the required component to opening; the generic import error does not specify which component was missing.
56. `formats22_tiff_compression` **K**: Lossless behavior and Deflate name retained.
57. `formats22_tiff_description` **K**: Preserves one RGB page, optional lossless compression and turning it off.
58. `formats22_dib_description` **K**: Keeps 24-bit, uncompressed DIB and BMP-header exception distinct.
59. `formats22_preview_memory` **K**: No memory only for preview; reduced opening dimensions are conditional.
60. `formats22_pdf_invalid` **K**: Preserves damaged-file vs unsupported-Android-feature alternatives.
61. `formats22_pdf_encrypted` **K**: Password or unsupported encryption, with an unprotected copy as remedy.
62. `formats22_pdf_memory` **K**: Explicit PDF rendering and the image memory limit.
63. `formats22_base64_description` **K**: Exact Base64 PNG prefix, losslessness, reopen operation and size tradeoff preserved.
64. `gallery_copy_credit` **H**: Check the clipboard action as a natural Copy command; wording risks sounding like duplicating text in place or preparing to paste.
65. `gallery_edit_credits` **K**: Editing the creator credits is clear and distinct from copying.
66. `gallery_credit_copied` **H**: Recognizable completion marker, but review together with the clipboard command before clearing either string.
67. `gallery_credit_edit_hint` **H**: Keep any required names and copyright notices, but make clear sources absent from the published image are removed from the editable credits, not source files.
68. `gallery_credit_title` **K**: Artwork and title-value placeholder retained.
69. `gallery_credit_publisher` **K**: Explicit named Catrobat project in publisher role.
70. `gallery_credit_gallery` **K**: Gallery and its value retained.
71. `gallery_credit_licence` **K**: Original artwork, licence and URL slot retained.
72. `gallery_credit_saved` **K**: Feedback is past/completed and specifies the credit text.
73. `formats22_ico_description` **H**: Transparent square refers to alpha, not merely a visible light background; verify the term before integrating.
74. `formats22_ico_decode_budget` **K**: Decoding this icon and the available image-memory budget.
75. `formats22_ico_dimensions_error` **H**: Say directory entry rather than a vague record/sample; it is the ICO-internal entry corresponding to that image.
76. `save20_bmp_description` **K**: Exact RGB depth and distinction between fidelity and file size.
77. `ui_creator_on_source34` **K**: Source page directs the reader to the person who contributed.
78. `ui_irasutoya_credit34` **K**: Preserves creator copyright, terms of use and non-CC distinction.
79. `legacy_credits_title` **K**: Identifies already-saved credits, not a new action.
80. `legacy_credits_hint` **K**: Warns credits can belong to other images and keeps both add and save options.
81. `legacy_credits_add` **K**: Selected attribution added to this specific image.
82. `legacy_credits_save_text` **K**: Selected attribution saved as text rather than inserted.
83. `legacy_credits_existing` **K**: Preserves specific source and unchanged existing text.
84. `legacy_credits_added` **K**: Completed add action and target image.
85. `gallery_external_link_no_handler` **K**: Android could not find a link handler; not error from the link itself.
86. `ui_casual` **H**: Verify casual refers to informal lettering, not normal/default type.
87. `ui_cursive` **K**: Connected-letter description distinguishes cursive in a font chooser.
88. `ui_monospace` **H**: Make explicit that individual characters have fixed advance width; text itself does not have a fixed overall width.
89. `ui_sans_condensed` **H**: Width condensation depends on a precise shared sans-serif term; review with other font-family variants.
90. `ui_sans_light` **H**: Confirm light stroke weight against thin and against condensed width; hold the matched family.
91. `ui_sans_medium` **H**: Confirm medium stroke weight against light/thin; hold the matched family.
92. `ui_sans_serif` **H**: Literal missing edges is ambiguous; name the small terminal strokes that distinguish sans from serif.
93. `ui_sans_thin` **H**: Comparative thinner wording depends on clear stroke weight and the light counterpart.
94. `ui_serif` **H**: Literal with edges is ambiguous; resolve together with sans-serif.
95. `ui_pale_violet` **H**: Verify hue as pale violet rather than generic pale purple or blue and match the help/swatches.
96. `ui_spectrum` **K**: Colors as a range is workable in the palette context.
97. `ui_honeycomb` **H**: Verify the honeycomb analogy denotes the cell pattern and not a general beehive; keep wording consistent across all three keys.
98. `ui_honeycomb_colour_06x` **H**: Hex format is preserved; hold until the shared honeycomb caption is resolved.
99. `ui_honeycomb_colour_swatches_with_a_greyscale_row` **H**: Grayscale row is described, but hold pending shared honeycomb wording.
100. `ui_colour_hsv_hue_range` **K**: HSV hue letter and 0–360° domain remain; the extra descriptive label does not change the numeric operation.

## Independent wording review: batch 2 (100 draft keys)

Personally compared 61 remaining Standard Zhuang (`za`) draft keys and the first 39 Standard Moroccan Tamazight (`zgh`) draft keys with their pinned source and related captions. Input: `remaining-translations.json`, blob `4ec048d12a74dd312d9dfd99801b5fd0a403f053`. No duplication of batch 1; earlier structural checks do not count as wording decisions. K = keep at this editorial pass, not native-speaker certification. H = hold for the stated reason; the draft remains available. **57 keep, 43 hold** (`za`: 30 / 31; `zgh`: 27 / 12). Across the two batches: **200 distinct draft keys reviewed, 126 keep, 74 hold**. No new wording, locale metadata change, Android integration, or device test in this batch.

1. `za/ui_colour_hsv_saturation_range` **H**: Added “thick colour” gloss may be read as paint density; numeric interval alone does not validate the HSV S label.
2. `za/ui_colour_hsv_value_range` **H**: The added brightness wording needs to distinguish HSV value from HSL lightness; both slider descriptions use the same generic brightness wording.
3. `za/ui_colour_hsl_hue_range` **H**: The new “kind of colour” gloss needs to read as the angular hue coordinate rather than a category; the degree interval alone is not sufficient.
4. `za/ui_colour_hsl_saturation_range` **H**: The HSL S gloss has the same thick-paint ambiguity; assess it as saturation, not coverage or opacity.
5. `za/ui_colour_hsl_lightness_range` **H**: The added lightness expression differs from the generic brightness used in the slider help. Reconcile the accessibility and visual labels before keeping it.
6. `za/ui_other_terms` **K**: Reads as additional terms/conditions, distinct from licence title and acknowledgement headings.
7. `za/ui_third_party_notices` **H**: The ordinal third-person wording does not reliably establish independent third parties; verify notices wording separately from a public announcement.
8. `za/ui_gimp_translations31` **H**: The line narrows credits to translators’ names and expresses licences as permission to use. Verify against the actual translation attribution and licence listing.
9. `za/ui_copy_an_area_or_use_file_insert_image` **H**: Other images reads differently from the established menu wording in the longer help. The instruction should point to the exact available item.
10. `za/ui_current_safe_budget_2f_mp` **K**: Retains current safe limit and the measured megapixel value rather than implying a permanent device maximum.
11. `za/ui_current_safe_editing_budget_s_up_to_2f` **K**: Explicitly identifies editing RAM, keeps both formatted values and excludes additional decoder RAM from the MP estimate.
12. `za/ui_hue_and_saturation_spectrum_lightness_slider_on_the` **H**: Hue and saturation are recognizable as the two spectrum axes, but the right slider wording says brightness rather than distinguishing HSL lightness.
13. `za/ui_hue_and_saturation_wheel_value_slider_on_the` **H**: The wheel is identifiable, but the right slider uses the same wording as the HSL help and does not disambiguate HSV value.
14. `za/ui_tap_vertices_then_double_tap_the_last_vertex` **H**: Last vertex and double-tap are present; closing uses an imprecise join-the-shape expression, and both quoted controls need exact caption matches before keeping.
15. `za/ui_vertical_letters23` **K**: Identifies characters within vertically arranged text rather than the direction of columns.
16. `za/ui_vertical_mixed23` **H**: Retains CJK, but the upright term also reads as straight/correct in isolation; contrast with sideways must survive a short standalone caption.
17. `za/ui_vertical_sideways23` **K**: The sideways option states that letters of each word stay joined, unlike the per-character mode.
18. `za/ui_vertical_upright23` **H**: The upright term needs validation against the paired automatic and sideways labels; character-by-character alone does not convey orientation.
19. `za/ui_vertical_hint23` **H**: The first sentence describes the direction of a column but not the creation of a new column for each new line; combining-mark wording also needs a clearer attestation.
20. `za/colour20_stored_slot` **K**: Keeps slot and stored colour distinct, and makes Replace the explicit step that saves edits.
21. `za/colour20_empty_slot` **K**: Distinguishes choosing a destination for the current colour from recalling a stored colour.
22. `za/save20_dither` **H**: The draft describes mixing alternating colours for intermediate appearance but the term needs to distinguish dithering from blending and anti-aliasing in the save controls.
23. `za/save20_unsupported_tagged_colour` **K**: Preserves the tagged BMP/GIF limitation and requires conversion to sRGB PNG in an editor that handles colour profiles before import.
24. `za/ui_cursor_help31` **K**: Correct sequence: position cursor, tap the on-screen control, then drag to draw, then tap again to stop. Brush and stroke settings are not described as cursor-size controls.
25. `za/ui_normalize_width_intro` **K**: Common width, image count, individual proportions, unchanged originals and unchanged crops are all stated.
26. `za/ui_normalize_height_intro` **K**: Common height rather than width; keeps the individual ratio and both unchanged items.
27. `za/commons_check_file_licence` **H**: “Name of the maker” is narrower than required attribution; page requirements can include more than a name, and “adaptation” needs less ambiguous legal wording.
28. `za/commons_import_svg_changes` **K**: Keeps original dimensions distinct from source file identity; preserves SVG to PNG and all three literal render settings.
29. `za/commons_import_raster_changes` **H**: The alpha description may read as an opacity-related colour operation rather than compositing onto the stated white background.
30. `za/commons_credit_copy_failed` **H**: Wording reduces image credit to the maker’s name; this app copies a richer citation.
31. `za/commons_credit_copy_failed_reason` **H**: Reason argument remains, but the action still names only the maker’s name instead of the whole citation.
32. `za/commons_credit_copy_out_of_memory` **H**: Memory error is preserved but its object is still only the maker’s name, inconsistent with the actual clipboard action.
33. `za/commons_metadata_http_error` **K**: The file-data qualifier establishes metadata in this error context; HTTP and its supplied status remain literal.
34. `za/commons_metadata_response_too_large` **K**: Names the size of the returned Commons data, not the size of the downloaded image.
35. `za/commons_metadata_query_failed` **K**: Failure of querying the Commons file data is distinct from an HTTP code or an oversized response.
36. `za/commons_metadata_ambiguous_file` **K**: Makes the ambiguity about which file is identified, not the image content.
37. `za/commons_metadata_unavailable` **K**: States that the file metadata could not be obtained, without asserting the image does not exist.
38. `za/commons_metadata_original_mismatch` **H**: The comparison is narrowed to the artist name rather than whether the whole Commons attribution matches the selected original.
39. `za/commons_metadata_invalid_page` **H**: The page is described as a creator-name page; that is not the full attribution record/page checked here.
40. `za/commons_metadata_field_too_large` **H**: The constrained field is any applicable attribution text field, not just the creator-name field.
41. `za/commons_metadata_cache_failed` **H**: “Could not save the creator’s name” leaves out the remaining stored attribution, including source/licence information.
42. `za/commons_download_original_mismatch` **K**: Expresses that the download was redirected to a different original rather than that the selected file itself was edited.
43. `za/commons_svg_png_encode_failed` **K**: Distinguishes the blank map and PNG encoding failure from attribution or download failures.
44. `za/ui_assembly_decoded_output_estimated_editing_render_memory_at` **K**: Keeps assembly, decoded output, and editing/render RAM at original size as three distinct lines with the original formatter indices.
45. `za/ui_copy_decoded_image_at_this_size_estimated_loading` **K**: Labels the copy rather than the original, keeps decoded size separate from loading/editing memory, and leaves the trailing line break.
46. `za/ui_each_px_px_percent_is_relative_to_the` **K**: Retains each dynamic axis, pixel bounds and scaling against the current largest reference; reflow applies to placed images.
47. `za/ui_estimates_include_the_current_canvas_and_clipboard_sampled` **H**: The description of sampled decoding and temporary editing buffers is ambiguous, and the selected opaque background must not read as an import colour-profile property.
48. `za/ui_gallery_artwork_catrobat_and_its_credited_creators_cc` **H**: Uses author name as the only explicit credit action; licensing boilerplate should preserve the broader requirement to credit artwork and identify modifications.
49. `za/ui_gnu_affero_general_public_license` **K**: The local description is accompanied by the complete official GNU licence name, preserving its unambiguous identity.
50. `za/ui_original_decoded_image_rgba_4_bytes_pixel_estimated` **K**: Separates decoded RGBA bytes/pixel from estimated editing RAM and correctly conditions the estimate on no resizing.
51. `za/ui_crop_preview_images` **K**: Keeps preview dimensions and image count in both variants, and warns only that attachments might move when placed images are cropped.
52. `za/formats22_page_description` **K**: Indicates choosing a single page to edit as an image; preserves file information and page count separately.
53. `za/gallery_description` **H**: The quoted Copy credit action reads as copying the maker name even though the next clause lists fuller fields; align panel and button captions to preserve the complete citation workflow.
54. `za/ui_normalize_width_info` **K**: States that the percentage uses the maximum current width while displaying the resulting heights separately; retains placed-image reflow.
55. `za/ui_normalize_height_info` **K**: Uses maximum current height, not width, for the scale reference and retains the distinct output width range and reflow.
56. `za/ui_irasutoya_help34` **H**: The threshold wording can convey “21 or more than that” but “require money” is weaker than the commercial-use payment requirement; reconcile the full source/credits route as well.
57. `za/ui_openclipart_help34` **K**: Keeps CC0 tied to Openclipart artwork and locates Use image beside the Large PNG link; separately identifies retained source page and licence.
58. `za/ui_assembly_position_help` **K**: Retains the top-left whole-pixel position, zero origin, unchanged other positions, later-import stacking, canvas expansion and unchanged crops/sizes.
59. `za/ui_add_up_to_20_images_with_android_s` **H**: Remove is rendered with an apparently erroneous repetition, and Reset crop uses a caption that reads as reuse of the whole image. Verify both against the actual buttons rather than approving an otherwise largely aligned guide.
60. `za/ui_help23` **H**: The compact guide’s reset-colour caption differs from the longer guide and the repeated Draw/Drawing label is hard to navigate. Match the guide to the shipped control captions.
61. `za/ui_the_arrow_on_the_left_directly_below_the` **H**: The editor guide still has the flagged edge anti-aliasing versus stroke smoothing ambiguity and a rounded-radius sentence that needs to unambiguously name half the shorter side.
62. `zgh/ui_draw_with_the_selected_brush_tip_and_size` **K**: Keeps both selected parameters: the brush tip, not a second drawing tool, and the brush size.
63. `zgh/ui_drag_from_the_start_to_the_end_of` **K**: Specifies dragging along the line operation from the start point to the end point, with the direction in the correct order.
64. `zgh/ui_draw_a_crisp_one_pixel_line` **H**: The 1–100 pixel adjustment is intact, but the edge adjective can read as bright/clear rather than crisp or unsmoothed; cross-check the pencil help before accepting.
65. `zgh/ui_pencil_keeps_crisp_one_pixel_strokes_cursor_drawing` **H**: The draft keeps “any selected width,” but the same potentially brightness-related adjective could misrepresent the pencil’s crisp edges.
66. `zgh/ui_pencil_crisp_adjustable_strokes` **H**: Identical source and draft to the other pencil description, which is appropriate for consistency; the shared edge adjective remains unresolved on this surface too.
67. `zgh/ui_pinch_to_zoom_drag_to_pan` **K**: The two opposite finger gestures adjust zoom, and the separate drag moves the view rather than the image.
68. `zgh/ui_tool_option` **K**: The singular option is explicitly attached to a tool, not a global preference.
69. `zgh/ui_toolbox_and_tool_options_scroll_for_more` **H**: Tools and their options are present, but the object of the scroll verb needs to identify the tool panel rather than a generic view.
70. `zgh/ui_cursor_ink30` **K**: The imperative names the cursor as the means of drawing, not as the thing being painted.
71. `zgh/ui_cursor_settings31` **K**: Settings applies to the cursor-drawing mode, and the ellipsis is retained for the follow-on panel.
72. `zgh/ui_cursor_tap_hint37` **H**: The wording follows the English instruction to tap the cursor, but adjacent help says to tap the on-screen drawing button. Verify which element receives the tap before using this hint.
73. `zgh/ui_cursor_pan_move32` **K**: Positions the cursor with a drag and starts drawing from the named button, preserving their order.
74. `zgh/ui_cursor_pan_draw32` **K**: States that dragging moves the cursor and draws; the subsequent tap stops drawing rather than repositioning the cursor.
75. `zgh/ui_right_arrow_expand` **H**: The rightward direction is clear, but the arrow noun and expand action need to match the actual toolbar toggle for accessibility.
76. `zgh/ui_add_to_custom_colours` **K**: “Your colours” cleanly identifies the user-managed set in an add-to action, not the stock palette.
77. `zgh/ui_custom_colour` **K**: Singular personal colour caption keeps the supplied label or identifier in the intended slot.
78. `zgh/ui_fill_text_box_with_bg_colour` **H**: The background wording needs to identify the actual background paint colour; the current compound can read as a rear auxiliary item rather than BG.
79. `zgh/ui_copy_an_area_or_use_file_insert_image` **H**: Copy and area are distinct, but the Draw → Insert → Other images steps must match the exact three localized captions; the long guide does not settle the route.
80. `zgh/ui_cursor_help31` **H**: The gesture sequence and brush/stroke distinction are present; the two identical menu labels leave the intended subsection ambiguous without matching the app’s labels.
81. `zgh/ui_cursor_marker_help31` **K**: Qualifies enlargement as affecting only the marker and explicitly excludes stroke-size change.
82. `zgh/ui_drag_between_opposite_corners_choose_outline_or_fill` **K**: Keeps the opposite-corner drag and explicitly places the outline/fill choice below.
83. `zgh/ui_drag_between_opposite_corners_to_draw_a_heart` **K**: Names a heart shape and keeps the outline/fill choice separate from drawing the bounding box.
84. `zgh/ui_drag_between_opposite_corners_to_draw_a_five` **K**: Star and five points are both present, and the fill/outline choice is preserved.
85. `zgh/ui_drag_to_pan_without_drawing_pinch_with_two` **K**: Distinguishes the non-drawing pan, two-finger zoom/pan, and gesture availability while drawing.
86. `zgh/ui_draw_soft_watercolor_strokes_strength_controls_how_strongly` **H**: “Draw with water” does not reliably name the Watercolor brush; align with the existing brush caption before keeping the otherwise meaningful strength instruction.
87. `zgh/ui_show_pixel_grid_800` **K**: A show action and lines between pixels identify what is made visible; the 800%+ threshold is preserved.
88. `zgh/ui_hide_pixel_grid_800` **K**: Uses the opposing hide action for the same pixel lines and keeps the same threshold.
89. `zgh/ui_added_palette23` **K**: A completed-addition message rather than an imperative; names the colour palette as the destination.
90. `zgh/ui_replace_palette23` **K**: Makes palette fullness explicit and identifies the stored colour as the one to choose for replacement.
91. `zgh/ui_replace_with_active23` **K**: Preserves the direction of substitution: replace using the in-use colour rather than removing it.
92. `zgh/ui_add_active23` **K**: Adds the in-use colour rather than requesting a new unrelated colour.
93. `zgh/ui_top` **K**: A compact top-side label without an added alignment instruction.
94. `zgh/ui_top23` **K**: Adds the alignment meaning explicitly and chooses the top as the reference edge.
95. `zgh/ui_bottom23` **K**: Keeps the same alignment construction but correctly selects bottom, not top.
96. `zgh/ui_vertical_rl23` **K**: Distinguishes downward reading within a column from right-to-left progression between columns.
97. `zgh/ui_vertical_lr23` **K**: Mirrors the paired option correctly: downward reading within a column, left-to-right progression between columns.
98. `zgh/ui_assembly_exact_position` **K**: Describes precise location, not centre alignment or saving a preset.
99. `zgh/ui_set_radius_px_then_drag_between_opposite_corners` **H**: The centre-to-edge paraphrase conveys radius, but the shorter-side phrase needs verification for singular agreement and unambiguous application to each rectangle.
100. `zgh/ui_drag_a_line_then_drag_twice_to_set` **H**: The first drag and two subsequent adjustments are present; the button wording describes a non-straight line rather than clearly naming Finish curve, and should match the actual control.

## Independent wording review: batch 3 (100 `zgh` draft keys)

Personally reviewed the next 100 distinct Standard Moroccan Tamazight draft keys against their source in `remaining-translations.json`, blob `4ec048d12a74dd312d9dfd99801b5fd0a403f053`, and used [the pinned locale catalogue](https://github.com/c933103/AN-Paint/blob/597e644c31c450d45aa6962d89564581d4434758/Paintroid/src/main/res/values-b%2Bzgh/strings.xml) for related existing labels. No revisits or structural-only checks counted in the batch. K = keep at this editorial pass, not native-speaker certification; H = hold for the stated reason. **70 keep, 30 hold. Running total: 300 reviewed, 196 keep, 104 hold.** No authoring, Android integration, metadata changes or device verification.

1. `zgh/ui_corners_and_edges_resize_round_handle_rotates` **K**: Distinguishes the corner/edge resizing controls from the round rotation handle.
2. `zgh/ui_vertical_letters23` **K**: Says letters within top-to-bottom text, not the direction in which the columns advance.
3. `zgh/colour20_save_slot` **K**: Names the numbered destination slot and uses the save action, not the replace action.
4. `zgh/colour20_replace_slot` **K**: Names the numbered slot as the replacement target, consistent with the stored-slot explanation.
5. `zgh/colour20_saved_slot` **K**: Completed action: the colour has been saved in the numbered position, not merely selected.
6. `zgh/ui_percent_of_pixels` **K**: Expresses percent of the supplied reference pixel count; the unit applies to the reference and not to the percentage itself.
7. `zgh/ui_common_in` **H**: The singular “one” construction may not express a shared target for all images, and the dynamic width/height label may require different agreement.
8. `zgh/ui_common_in_pixels` **H**: Shares the ambiguity of one versus common with the unit-parameter variant; the pixels unit itself is clear.
9. `zgh/commons_check_file_licence` **H**: The attribution phrase still directs the reader mainly to what to say about the author, not to every required credit item. The adaptation term also needs a clearer licence-context reading.
10. `zgh/ui_an_image_cannot_attach_to_itself_or_one` **K**: Retains both prohibited targets: the image itself and an image already attached to it.
11. `zgh/ui_casual` **K**: The typography label describes everyday/casual lettering rather than an editing mode.
12. `zgh/ui_catrobat_online_gallery_artwork_by_its_credited_creators` **K**: The online Catrobat gallery and its credited artists remain separate, and neither is recast as the other.
13. `zgh/ui_catrobat_sticker_gallery` **H**: The modifier for sticker images needs verification; the wording can suggest pasted images rather than a sticker-art gallery.
14. `zgh/ui_copper` **K**: Names copper as the swatch material/colour, which distinguishes it from gold and silver.
15. `zgh/ui_could_not_export_source_code` **K**: The action that failed is source-code export, rather than opening or downloading source.
16. `zgh/ui_could_not_load_gallery_image` **H**: The placeholder is intact and the source is the gallery, but the verb can imply fetching rather than loading; distinguish this from the separate download-failure string.
17. `zgh/ui_credits_terms` **H**: The heading identifies creators and terms, not the attribution and terms records presented on this surface.
18. `zgh/ui_current_safe_budget_2f_mp` **K**: Uses the current safe RAM-derived budget and retains the MP estimate; it does not present the figure as a permanent device limit.
19. `zgh/ui_current_safe_editing_budget_s_up_to_2f` **K**: Preserves both quantities and the exclusion of additional decoder RAM from the megapixel estimate.
20. `zgh/ui_cursive` **K**: “Joined writing” is a useful description of the cursive style in this short menu label.
21. `zgh/ui_custom_colours_hold_a_swatch_to_replace_it` **H**: Tap followed by hold can read as two gestures. The instruction should indicate a single long press on the swatch, not on the whole palette.
22. `zgh/ui_downloading_image` **H**: The download noun differs from the verb used by the gallery error group; verify the intended transfer direction across in-progress and failure messages.
23. `zgh/ui_drag_a_selection_drag_inside_to_move_square` **K**: Retains move, resize and rotate independently, and conditions shape preservation on the proportions lock.
24. `zgh/ui_drag_across_the_ellipse_s_bounding_box` **K**: Identifies opposite corners of the enclosing rectangle and uses the existing ellipse caption rather than a generic shape.
25. `zgh/ui_drag_from_the_tail_towards_the_arrowhead_choose` **H**: The head and arrow name are recognizable, but the word for the tail needs validation in the directional pair before this instruction is used.
26. `zgh/ui_drag_out_to_expand_in_to_trim_drag` **H**: Expand, trim, move and Fit are distinct, but the trailing BG wording needs resolution against the actual colour control.
27. `zgh/ui_drag_to_erase_with_the_background_colour` **H**: The instruction should plainly say which paint colour the eraser applies; keep in sync with the BG terminology hold rather than approving the same ambiguous compound.
28. `zgh/ui_draw_around_an_area_drag_inside_to_move` **H**: The freehand outline and its handles are clear; the quoted commit control can read as shutting off selection. Verify the control caption and applying the edit.
29. `zgh/ui_drop_at_a_highlighted_edge_right_top_aligned` **K**: Expresses drop onto the highlighted edge with the correct right/top and below/left combinations.
30. `zgh/ui_export_this_version_s_source_code` **K**: Explicitly exports the source code of the current version and retains the ellipsis for the follow-on action.
31. `zgh/ui_gallery_image` **K**: Distinguishes an image sourced from the gallery from a heading or source credit.
32. `zgh/ui_give_all_images_the_same_each_image_keeps` **K**: Retains all-image scope, adjustable common dimension, individual aspect ratio, unchanged originals and unchanged crops; positional placeholders are intentionally reordered.
33. `zgh/ui_gnu_affero_general_public_license` **K**: The localized full title retains General/Public and the GNU Affero proper name.
34. `zgh/ui_hold_or_drag_to_spray_colour` **K**: Indicates holding or dragging produces a spray of coloured droplets, keeping the gesture separate from a normal brush pass.
35. `zgh/ui_honeycomb` **K**: Uses the palette context and six-sided grouping to identify the honeycomb design rather than literal honey.
36. `zgh/ui_honeycomb_colour_06x` **K**: Ties the sample to the honeycomb and leaves the hex formatter and leading number sign intact.
37. `zgh/ui_icons_artwork` **K**: Keeps icons and artwork as two asset categories in this short heading.
38. `zgh/ui_icons_fonts_artwork_credits` **H**: The opener says creators of icons/fonts/artwork, narrower than the credits dossier. Coordinate with the full attribution terminology.
39. `zgh/ui_image_credits` **K**: Describes image credit as source, creator and rights data rather than a maker-name field alone.
40. `zgh/ui_insert_gallery_image` **K**: Preserves the confirmation question and the direction of insertion from the gallery into the app.
41. `zgh/ui_invalid_image_attachments` **K**: The invalidity applies to linked/attached images rather than the entire workspace or merely image format.
42. `zgh/ui_modified_newest_first` **K**: Modification time rather than creation time; the most recent entries are first.
43. `zgh/ui_modified_oldest_first` **K**: The paired wording reverses the order to oldest first while keeping modification time as the criterion.
44. `zgh/ui_monospace` **K**: Says one width for each character, identifying fixed character advances without conflating this with font weight.
45. `zgh/ui_no_attachment_fits_within_the_current_coordinate_range` **K**: Identifies the current positional bounds rather than a missing file, and proposes smaller image sizes.
46. `zgh/ui_no_gallery_images_have_been_inserted` **K**: Expresses absence of credit text, not that no images are loaded; follows the current English source rather than the legacy resource name.
47. `zgh/ui_not_enough_memory_to_inspect_the_gallery_image` **K**: Names safe RAM shortage for inspecting the gallery image, distinct from download or decoding-format errors.
48. `zgh/ui_open_source_credits_and_notices` **H**: The wording references open-source programs and notices, but the credit element again reads as people rather than acknowledgement records; verify this phrase for dependencies as a whole.
49. `zgh/ui_same` **H**: “One %1$s” can read as a count rather than equal values across images; grammar also depends on the inserted axis.
50. `zgh/ui_smooth_freehand_strokes` **K**: Specifies smoothing the paths drawn by hand, distinct from edge treatment at the pixel level.
51. `zgh/ui_smooth_pixel_edges_anti_aliasing` **K**: Names pixel edges explicitly and distinguishes that operation from the separate freehand stroke smoothing option.
52. `zgh/ui_some_previews_could_not_be_decoded_you_can` **H**: “Could not convert to pixels” conveys a decoding idea but may read as a resize or effects operation. Clarify that preview decoding failed while saving is still an option.
53. `zgh/ui_sort_images_by_filename_or_modification_time` **K**: Both ordering criteria are explicit, and the object is the images rather than the filesystem.
54. `zgh/ui_sort_tray` **H**: Says to order small images; it should identify the tray/thumbnails being sorted rather than suggesting a size-based filter.
55. `zgh/ui_source_code_exported_including_build_scripts_and_licence` **K**: Completion is explicit, and the exported contents still include build-related files and licence notices.
56. `zgh/ui_strikethrough` **K**: The line goes across the middle of the text rather than beneath it.
57. `zgh/ui_that_arrangement_overlaps_another_image_use_a_different` **K**: Preserves overlap with another image and gives both alternatives. Returning attachments to the tray is distinct from deleting them.
58. `zgh/ui_the_attachment_image_is_missing` **K**: Identifies the missing image as the attachment, not the parent or a failed attachment operation.
59. `zgh/ui_the_first_image_starts_at_the_top_left` **K**: Locates the first image at the upper left rather than merely saying it goes at the top.
60. `zgh/ui_the_gallery_download_is_too_large` **H**: The size condition is clear, but the draft says file of the image page rather than the gallery download; check the transfer verb with the paired errors.
61. `zgh/ui_the_gallery_image_is_unavailable` **H**: Says the image is not present on the gallery site; the source only says it is unavailable, which may be temporary.
62. `zgh/ui_the_gallery_redirected_outside_its_supported_hosts` **K**: Retains the image URL and unsupported condition without implying the whole gallery site is unsupported.
63. `zgh/ui_the_image_could_not_be_downloaded` **K**: Says the app could not download the image and does not speculate about size or network cause.
64. `zgh/ui_the_images_cannot_fit_within_android_s_coordinate` **K**: Preserves both Android coordinate axes and the corrective advice to select smaller dimensions.
65. `zgh/ui_the_normalized_image_dimensions_are_outside_android_s` **K**: Attributes the error to the normalized dimensions being outside Android limits, not to the original files.
66. `zgh/ui_the_online_gallery_could_not_be_loaded_check` **K**: Retains the online gallery, the retry suggestion and connection check, without diagnosing a specific cause.
67. `zgh/ui_third_party_notices` **H**: The notice noun is plausible but “other people” is narrower than third-party organizations and components in the licences panel.
68. `zgh/ui_this_image_is_outside_the_supported_catrobat_gallery` **K**: Retains Catrobat as the source boundary and limits the error to the supported gallery.
69. `zgh/ui_time_unavailable` **H**: The word for generic time should be aligned with the modification timestamp wording in the adjacent sort labels so this is not read as a duration.
70. `zgh/ui_too_many_gallery_redirects` **K**: Says the gallery moved to another URL too many times, distinguishing excessive redirection from a single unsupported URL.
71. `zgh/ui_unplace` **K**: Specifies returning a placed image to the tray, without implying input removal or erasure.
72. `zgh/ui_you_can_add_more_images_select_fewer_files` **K**: Retains the remaining capacity, placeholder and instruction to select fewer files, not to delete existing ones.
73. `zgh/ui_preview_memory_error` **K**: The supplied item remains attached to its own preview-memory failure.
74. `zgh/ui_sans_condensed` **H**: The sans qualifier is distinct, but the width adjective needs an attestation for condensed lettering rather than thickness or brevity.
75. `zgh/ui_sans_light` **H**: The adjective can read as thin; establish a consistent light-versus-thin weight distinction without implying narrower glyphs.
76. `zgh/ui_sans_medium` **H**: “Middle” has a meaning in the weight selector, but the label should distinguish medium weight from centred alignment or medium size.
77. `zgh/ui_sans_serif` **H**: Establish that the missing marks are specifically stroke-end serifs, not any letter-edge or diacritic marks; keep consistent with Serif.
78. `zgh/ui_sans_thin` **H**: Strengthening the “light/thin” adjective with “very” distinguishes intensity but does not by itself validate the two distinct weight labels.
79. `zgh/ui_serif` **H**: The wording mentions edge marks but does not clearly limit them to stroke terminals, risking confusion with diacritics.
80. `zgh/ui_tap_vertices_then_double_tap_the_last_vertex` **H**: The double tap and last vertex are explicit; the final command reads as not using Close polygon rather than switching it off. Check the actual switch caption.
81. `zgh/ui_wheel` **H**: The expression can denote a ball or sphere of colours rather than the flat colour wheel; distinguish it from the spectrum panel.
82. `zgh/ui_horizontal23` **H**: The noun appears to describe an operation/positioning; verify that this label simply sets horizontal text direction and does not imply centring.
83. `zgh/ui_vertical_mixed23` **K**: Retains automatic selection, upright CJK and sideways words as two different orientation rules.
84. `zgh/ui_vertical_sideways23` **K**: Preserves the connection within each word rather than merely rotating the letters individually.
85. `zgh/ui_vertical_upright23` **K**: Explicitly labels upright mode and distinguishes its character-by-character behaviour from sideways words.
86. `zgh/ui_vertical_hint23` **K**: Distinguishes new columns at line breaks, preservation of joining (including Mongolian), and combining-mark/emoji grouping in upright mode.
87. `zgh/colour20_custom_selected_slot` **K**: The selected slot number is spoken explicitly, not implied to be saved or overwritten.
88. `zgh/colour20_stored_slot` **K**: Tap-to-use and change-then-replace are separate; the second placeholder identifies the stored colour.
89. `zgh/colour20_empty_slot` **K**: Names the empty numbered slot and says the tap chooses where the current colour is saved.
90. `zgh/ui_lossless_format` **K**: Names absence of data loss without implying uncompressed output; keeps the format argument.
91. `zgh/formats22_dib_size_limit` **K**: Identifies a DIB file-size maximum, not conflicting canvas dimensions or a generic save error.
92. `zgh/formats22_page_preview` **K**: Specifies a preview of the chosen page rather than a page number, canvas or entire document.
93. `zgh/formats22_loading_page` **K**: Retains current/total page numbers in correct positions and identifies preview loading.
94. `zgh/formats22_preview_unavailable` **K**: Preview is unavailable, but the reason placeholder is preserved and there is no false claim the page is missing.
95. `zgh/formats22_preview_memory` **K**: Names preview memory and makes smaller dimensions conditional on opening the page and availability.
96. `zgh/formats22_text_not_image` **K**: The negative condition is on supported image content within Base64 text, not a claim that Base64 itself is unsupported.
97. `zgh/gallery_copy_credit` **K**: Uses a source/artist/rights bundle as the copy object, not only the artist’s name; consistent with the credit heading.
98. `zgh/gallery_edit_credits` **K**: Uses the same bundle with an edit action rather than copying or replacing the image.
99. `zgh/gallery_credit_copied` **K**: Completed copy of the same attribution bundle, not an imperative or a claim the image was copied.
100. `zgh/gallery_credit_title` **K**: Retains an artwork/image label and the dynamic title argument without recasting it as the creator field.

## Independent wording review batch 4: 72 zgh and 28 chr draft keys

2026-11-20 UTC. Personally compared the combined authored file (blob `4ec048d12a74dd312d9dfd99801b5fd0a403f053`) with its pinned source `597e644c31c450d45aa6962d89564581d4434758`. Reviewed Standard Moroccan Tamazight draft indices 139–210 and Cherokee draft indices 0–27 (zero-based within each locale); no overlap with previous editorial batches. Compared related terms and button names against the locale catalogues. K means keep for downstream integration subject to technical checks; H means hold wording for revision or better evidence. This is not native-speaker, integration, or device sign-off.

Results: **70 keep, 30 hold**. Running total: **400 distinct drafts reviewed, 266 keep, 134 hold**.

1. `zgh/gallery_credit_publisher` **K**: Publisher role and named Catrobat project remain distinct from creator.
2. `zgh/gallery_credit_gallery` **K**: Gallery is an image collection, with the displayed gallery name intact.
3. `zgh/gallery_credit_licence` **K**: Original Catrobat image, license version and link are all retained.
4. `zgh/gallery_credit_saved` **K**: Completed save of attribution text, not a claim that image was saved.
5. `zgh/formats22_ico_size` **K**: Icon’s size is explicit and matches the ICO description.
6. `zgh/save20_dither` **H**: Combining adjacent pixels suggests mixing, not spatial distribution of palette colours to approximate shades.
7. `zgh/save20_bmp_size_limit` **K**: States the image exceeds the BMP file-size maximum, not a width bound.
8. `zgh/save20_gif_size_limit` **K**: Retains 65,535 pixels on each side of the GIF.
9. `zgh/ui_gimp_translations31` **H**: Names translators rather than the complete translation credit record, alongside licenses.
10. `zgh/ui_search_english34` **K**: Gives the two accepted query languages as alternatives.
11. `zgh/gallery_image_component_unavailable` **K**: Required component missing, with the import explicitly not performed.
12. `zgh/formats22_tiff_compression` **K**: Deflate is intact and the wording rules out loss of data.
13. `zgh/formats22_tiff_description` **K**: One RGB page, possible size reduction without pixel changes, and the off-state are preserved.
14. `zgh/formats22_dib_description` **H**: Verify that the phrase for receiving app is not read as separate or special app; BMP header is a condition on the destination.
15. `zgh/formats22_pdf_invalid` **K**: Gives two possible causes and limits unsupported features to this Android version.
16. `zgh/formats22_pdf_encrypted` **H**: Encryption wording uses a generic protection term too close to the instruction to save an unprotected copy; distinguish encryption from password and protection.
17. `zgh/formats22_ico_description` **H**: Last clause says no background colour; transparent pixels in a square need to be explicit.
18. `zgh/formats22_ico_decode_budget` **H**: Uses image creation from the icon, not decoding; name the process that consumes the budget.
19. `zgh/formats22_ico_dimensions_error` **K**: Mismatch is between actual dimensions and the corresponding slot of the internal ICO table.
20. `zgh/save20_bmp_description` **K**: Exact colours and larger files remain separate consequences of uncompressed 24-bit RGB.
21. `zgh/ui_pixel_grid_help33` **K**: Grid and rulers stay distinct, with the 800% threshold and image-pixel units.
22. `zgh/ui_gallery_unsupported34` **K**: Says the image is not from the selected source, rather than unsupported format.
23. `zgh/ui_open_artwork34` **K**: Correctly keeps first opening the artwork page, then pressing the named button.
24. `zgh/ui_creator_on_source34` **K**: Refers user to the source page to identify the contributor.
25. `zgh/ui_irasutoya_credit34` **H**: Last line deictically refers to this license even though source discusses provider terms that are not a CC license. Keep terms separate from license status.
26. `zgh/legacy_credits_title` **K**: Distinguishes already saved attribution records from a new save action.
27. `zgh/legacy_credits_hint` **K**: Retains credits may belong elsewhere, selection attaches credit to this image, or exports full text.
28. `zgh/legacy_credits_add` **K**: Adds the selected credit data to the current image, consistent with the hint.
29. `zgh/legacy_credits_save_text` **K**: Saves selected attribution as text, not the selected source image.
30. `zgh/legacy_credits_existing` **K**: Same-source credit already exists and its original wording stays intact.
31. `zgh/legacy_credits_added` **K**: Completed addition to the current image, not a save of the artwork.
32. `zgh/ui_catrobat_s_own_artwork_uses_cc_by_sa` **H**: Separate attribution is narrowed to additional creator information; source notices may contain more than that.
33. `zgh/ui_copy_decoded_image_at_this_size_estimated_loading` **K**: Identifies the copy and separates decoded pixels from estimated loading/editing RAM.
34. `zgh/ui_each_px_px_percent_is_relative_to_the` **H**: Reads percent as corresponding to the largest dimension, rather than calculated from it; use the explicit phrasing in width/height help.
35. `zgh/ui_estimated_memory_current_working_budget` **K**: Preserves estimate versus current working limit with both distinct variables.
36. `zgh/ui_gallery_artwork_catrobat_and_its_credited_creators_cc` **H**: Crediting the artwork becomes naming the creator alone; this omits other applicable attribution elements.
37. `zgh/ui_honeycomb_colour_swatches_with_a_greyscale_row` **K**: Hexagonal swatches and separate black-to-white row are both represented.
38. `zgh/ui_original_decoded_image_rgba_4_bytes_pixel_estimated` **K**: Original, decoded RGBA at four bytes per pixel, and estimated edit memory without resizing remain distinct.
39. `zgh/ui_pale_violet` **H**: Violet term reads as a leaf/wing-type noun; cannot clear as a colour name without an attested violet sense.
40. `zgh/ui_spectrum` **K**: Colour spectrum label matches its spectrum accessibility description.
41. `zgh/ui_crop_preview_images` **K**: Both plural forms keep one versus multiple images, preview dimensions, and possible attached-image movement.
42. `zgh/formats22_page_description` **K**: Keeps page count separate from page selection; selected page is edited as an image.
43. `zgh/formats22_base64_description` **K**: Retains exact Base64 prefix, reopening to recover image, and size relative to encoded PNG.
44. `zgh/save20_unsupported_tagged_colour` **K**: Colour metadata unavailable for conversion now; user is directed to sRGB PNG through a colour-managed editor.
45. `zgh/ui_normalize_width_info` **K**: Explicitly calculates percent from greatest current width and names reflow after resizing.
46. `zgh/ui_normalize_height_info` **K**: Uses greatest current height as the percent base, keeping the width interval distinct.
47. `zgh/commons_import_svg_changes` **K**: SVG to PNG and original size conveyed, with exact rasterization parameters retained.
48. `zgh/commons_import_raster_changes` **K**: Keeps white background token and the qualification that it is alpha compositing.
49. `zgh/commons_credit_copy_failed` **K**: Failure is to copy full image attribution, not the bitmap.
50. `zgh/commons_credit_copy_failed_reason` **K**: Same copy failure with the actual why field inserted after the colon.
51. `zgh/commons_credit_copy_out_of_memory` **K**: Separates RAM shortage from generic failure, and names attribution as copied content.
52. `zgh/commons_metadata_response_too_large` **K**: Metadata response exceeds size limit; no claim that image download failed.
53. `zgh/commons_metadata_query_failed` **K**: Reads as request for Commons file metadata failed, not inability to open the file.
54. `zgh/gallery_external_link_no_handler` **K**: Says Android cannot find a handler for this specific link, not that link is broken.
55. `zgh/commons_metadata_ambiguous_file` **K**: Ambiguity lies in which file the metadata resolved to.
56. `zgh/commons_metadata_original_mismatch` **K**: The whole attribution record is compared against the selected original, not merely its creator.
57. `zgh/commons_metadata_invalid_page` **K**: Labels an invalid Commons attribution page, not a general network error.
58. `zgh/commons_metadata_field_too_large` **K**: One Commons attribution field exceeds text limit, not the entire response.
59. `zgh/commons_metadata_cache_failed` **K**: Retaining attribution failed; no suggestion the metadata query itself failed.
60. `zgh/commons_download_original_mismatch` **K**: Gives transfer redirection to a different original, distinct from metadata mismatch.
61. `zgh/commons_svg_png_encode_failed` **H**: Blank map is constrained to no writing; verify against the UI meaning, since map linework survives.
62. `zgh/ui_estimates_include_the_current_canvas_and_clipboard_sampled` **K**: Keeps estimated buffers, varying actual use, smaller copy losing detail, opaque background, and original file untouched.
63. `zgh/gallery_description` **H**: Preserve full navigation wording against the exact paired labels before clearing this long licensing instruction. 
64. `zgh/gallery_credit_edit_hint` **K**: Preserves names and copyright notices, change description, removing absent sources, and that text is editable.
65. `zgh/ui_irasutoya_help34` **H**: The term used for free and required fee is not established as payment here; verify the commercial 21-item clause and matched path.
66. `zgh/ui_openclipart_help34` **H**: Check the exact menu path and keep CC0 a specific dedication, not an ordinary licence category.
67. `zgh/ui_assembly_position_help` **K**: Whole-pixel X/Y start at zero; other images remain fixed, overlap is allowed, canvas expands, no crop/size change.
68. `zgh/ui_add_up_to_20_images_with_android_s` **H**: Reset crop is called Use whole image; reconcile with the exact control label and make non-destructive crop distinct from restoring original size.
69. `zgh/ui_help23` **H**: Two-tap gesture wording can read tap and hold; check against the actual long-press and short-tap contrast, and reconcile menu captions.
70. `zgh/ui_hue_and_saturation_spectrum_lightness_slider_on_the` **K**: Keeps hue/saturation in the field and distinguishes HSL lightness on the right.
71. `zgh/ui_hue_and_saturation_wheel_value_slider_on_the` **K**: Separates circular hue/saturation wheel from the HSV value slider on the right.
72. `zgh/ui_the_arrow_on_the_left_directly_below_the` **H**: Duplicates the word for Draw and Drawing and calls Watercolor by a label different from the existing dedicated tool; align navigation throughout.
73. `chr/commons_blank_maps` **H**: Blank maps must be distinguished from a map with an empty background; verify the parenthetical term and use a clear map-category label.
74. `chr/ui_about_copyright` **H**: The possessive writing formulation is not established as the copyright term; verify against a Cherokee rights notice.
75. `chr/ui_about_copyright_licence` **H**: Keep copyright distinct from licence. The final term matches the draft licence convention but the copyright phrase remains ambiguous.
76. `chr/ui_add_images` **K**: Uses the established insert/add verb with images as the object.
77. `chr/ui_add_images_first` **K**: Preserves the same action with an explicit first step.
78. `chr/ui_add_images_then_drag_a_thumbnail_here` **H**: Small picture hints at thumbnail but mini-preview is important, especially when placed and unplaced images are both visible; verify that the action reads drag it here.
79. `chr/ui_add_to_custom_colours` **H**: The same-colour phrase could read add a colour generally; reconcile personal/custom terminology and the verb with the locale’s save-colour action.
80. `chr/ui_an_assembly_can_contain_up_to_20_images` **K**: Retains the 20-image maximum and the remove-one-before-adding-another instruction.
81. `chr/ui_an_assembly_can_contain_up_to_20_images_86d995` **K**: Maximum of 20 images retained without adding the remove action from the adjacent variant.
82. `chr/ui_an_paint_assembly_image` **K**: Uses established assembly term and identifies the image as its output label.
83. `chr/ui_an_paint_image_assembly` **K**: Holds the brand separate from the assembly workspace title.
84. `chr/ui_an_paint_image_assembly_20_images_placed` **K**: Progress and placed counts stay distinct, in the existing assembly title and two-line layout.
85. `chr/ui_apply_to_all` **K**: All is explicitly scoped, with the same apply/use verb as other confirmations.
86. `chr/ui_apply_to_these_images` **K**: Demonstrative narrows the action to these images, not the entire workspace.
87. `chr/ui_assembly_decoded_output_estimated_editing_render_memory_at` **H**: Pixel arrow alone does not read as decoded output; make the rendering-memory estimate explicit and keep it at original size.
88. `chr/ui_assembly_output_size` **H**: The arrow into generic size does not unambiguously name the dimensions of the output rather than those of the input files.
89. `chr/ui_assembly_png` **K**: Filename stem follows assembly term and retains the .png suffix.
90. `chr/ui_batch_crop` **K**: Uses the established crop action with multiple images as its scope, not one image’s crop.
91. `chr/ui_batch_crop_images` **K**: Explicitly puts images in the plural as the objects of cropping, consistent with shorter batch action.
92. `chr/ui_by_pixels_hold_and_drag_to_place` **H**: Action reads hold and move alongside drag/place; remove duplicate competing verbs but preserve the hold-before-drag gesture.
93. `chr/ui_catrobat_online_gallery_artwork_by_its_credited_creators` **H**: Attribution clause juxtaposes pictures and credited names but does not clearly say those named creators made the artwork.
94. `chr/ui_common_in` **K**: Shared value label keeps the axis and the dynamic unit separate.
95. `chr/ui_common_in_pixels` **K**: Same common-axis label, with pixels specified explicitly rather than a dynamic unit.
96. `chr/ui_copy_an_area_or_use_file_insert_image` **H**: Uses an area-selection phrase without a clear copy imperative; match the Draw tab and exact nested button captions before accepting.
97. `chr/ui_copy_decoded_image_at_this_size_estimated_loading` **H**: Same-made can be the wrong meaning of copy here; make the copy/decoded size/memory distinction and explicit loading versus editing.
98. `chr/ui_corners_and_edges_resize_round_handle_rotates` **K**: Keeps which handles resize and which handle rotates in separate instructions.
99. `chr/ui_could_not_create_the_assembly` **K**: Uses the established assembly and failure frame but identifies creation, not saving, with the reason retained.
100. `chr/ui_could_not_decode_the_cropped_region_of` **H**: Pixel arrow does not clearly identify decoding as the failed action; explicitly retain the cropped subregion scope.

## Independent wording review batch 5: 100 chr draft keys

2026-11-20 UTC. Personally reviewed Cherokee draft indices 28–127 inclusive (zero-based) in the combined file, blob `4ec048d12a74dd312d9dfd99801b5fd0a403f053`, against source and the Cherokee UI controls at develop `597e644c31c450d45aa6962d89564581d4434758`. Distinct keys, excluding all earlier batches. K means keep for later integration checks, H means hold for wording or terminology. No native-speaker certification, resource integration, or runtime testing.

Results: **58 keep, 42 hold**. Running total: **500 distinct drafts reviewed, 324 keep, 176 hold**.

1. `chr/ui_could_not_export_source_code` **H**: Technical verb is shared with ambiguous conversion wording; distinguish exporting source files from compiling or decoding them.
2. `chr/ui_could_not_load_gallery_image` **K**: Gallery, image loading failure, and the actual reason parameter remain separate.
3. `chr/ui_create_output` **K**: Directly tells the user to make the image output, not to save an existing file.
4. `chr/ui_credits_terms` **K**: Retains attribution/source notices and usage terms as different objects, aligned with the About section.
5. `chr/ui_current_safe_budget_2f_mp` **K**: Uses current safe-limit wording and keeps the two-decimal megapixel quantity.
6. `chr/ui_current_safe_editing_budget_s_up_to_2f` **H**: Decoder-memory exclusion is a risk-bearing clause; use an explicit additional RAM component rather than image-to-pixel shorthand.
7. `chr/ui_custom_colour` **K**: Personally saved colour and numbered slot stay distinct from an ordinary colour name.
8. `chr/ui_custom_colours_hold_a_swatch_to_replace_it` **K**: Uses the established long-press gesture and says the selected swatch is changed/replaced.
9. `chr/ui_disable_cursor_drawing` **K**: Matches the cursor drawing term and makes this an off action, not a delete operation.
10. `chr/ui_drag_a_line_then_drag_twice_to_set` **K**: Exact Finish curve caption, two distinct bend drags, and early commit are preserved.
11. `chr/ui_drag_a_selection_drag_inside_to_move_square` **H**: Square handles and the exact Lock proportions label are missing; distinguish the handles, not just the corner/edge locations.
12. `chr/ui_drag_across_the_ellipse_s_bounding_box` **H**: The paired-corners phrase does not make the ellipse's bounding rectangle explicit.
13. `chr/ui_drag_between_opposite_corners_choose_outline_or_fill` **K**: Preserves the opposite-corner drag and a later choice of outline or fill.
14. `chr/ui_drag_between_opposite_corners_to_draw_a_five` **K**: Five points, the opposite bounding corners, and outline/fill are all present.
15. `chr/ui_drag_between_opposite_corners_to_draw_a_heart` **K**: Heart shape, diagonal drag, and distinct outline/fill choices are represented.
16. `chr/ui_drag_from_the_start_to_the_end_of` **K**: Start and end are visually and linguistically distinguished as the drag endpoints.
17. `chr/ui_drag_from_the_tail_towards_the_arrowhead_choose` **H**: Check arrowhead versus generic head and the tail term; these determine the direction of dragging.
18. `chr/ui_drag_out_to_expand_in_to_trim_drag` **K**: Uses the established trim/expand terms and Fit caption, preserving BG fill in newly added space.
19. `chr/ui_drag_placed_images_to_move_them_hold_and` **H**: First instruction repeats move/drag and the second needs the established thumbnail wording rather than a potentially small source image.
20. `chr/ui_drag_to_erase_with_the_background_colour` **K**: Erasing by painting with the existing background colour term is explicit.
21. `chr/ui_drag_to_pan_without_drawing_pinch_with_two` **H**: The wording can imply not using the Draw tab and does not clearly preserve two-finger panning while a drawing tool is active.
22. `chr/ui_draw_a_crisp_one_pixel_line` **H**: The proposed crisp modifier is not established as an edge quality; keep the real width label and 1–100 range.
23. `chr/ui_draw_around_an_area_drag_inside_to_move` **H**: The drag passage omits square handles; match the exact Commit selection button wording as well.
24. `chr/ui_draw_soft_watercolor_strokes_strength_controls_how_strongly` **H**: Aligns the tool name, but verify that the second phrase means strength of blending into the canvas, not simply using a mixed colour.
25. `chr/ui_draw_with_the_selected_brush_tip_and_size` **H**: The brush edge wording could mean boundary rather than the selected tip; match the Brush tool label and tip setting.
26. `chr/ui_drop_at_a_highlighted_edge_right_top_aligned` **H**: Makes the right/top and below/left hard to distinguish as two separate snap rules; keep the respective alignments explicit.
27. `chr/ui_each_px_px_percent_is_relative_to_the` **H**: Percentage reference is not grammatical enough for an accessibility instruction; explicitly say percent of the largest current dimension and show subsequent repositioning.
28. `chr/ui_edit_in_paint` **K**: Paint is left as the named editor and the action matches the app's Edit label.
29. `chr/ui_enable_android_s_files_or_documents_app_then` **K**: Files/Documents remain Android app names and reattempt is after enabling.
30. `chr/ui_estimated_memory_current_working_budget` **K**: The memory estimate and the currently available working limit are distinctly labeled.
31. `chr/ui_export_this_version_s_source_code` **H**: Draft describes this kind, not unambiguously this installed version; align the export verb with the failure state.
32. `chr/ui_fill_text_box_with_bg_colour` **K**: The target is the text box and the selected colour is BG, not foreground.
33. `chr/ui_fits_the_current_budget` **K**: States that the option fits the current memory ceiling, using the same budget terms as the related dialog.
34. `chr/ui_font_licences` **K**: Fonts and licences remain distinct; wording follows the established app font label closely.
35. `chr/ui_gallery_image` **K**: Concise gallery-picture label matches the loading and insert terminology.
36. `chr/ui_give_all_images_the_same_each_image_keeps` **H**: Disambiguate one shared dimension from a shared aspect ratio; each image keeps its own ratio and its crop.
37. `chr/ui_gnu_affero_general_public_license` **K**: Preserves the official licence name verbatim and gives a Cherokee categorizing gloss.
38. `chr/ui_hide_pixel_grid_800` **K**: Uses the existing pixel-grid wording, an explicit hide verb, and the unchanged zoom threshold.
39. `chr/ui_hold_a_thumbnail_and_drag_it_here_or` **H**: Verify thumbnail wording and make the two taps separate and ordered; do not imply the tap is on a placed image.
40. `chr/ui_hold_or_drag_to_spray_colour` **K**: Matches the Airbrush concept, retains two possible gestures, and indicates paint colour.
41. `chr/ui_honeycomb_colour_06x` **K**: Matches the established Honeycomb label and keeps the exact hexadecimal format placeholder.
42. `chr/ui_honeycomb_colour_swatches_with_a_greyscale_row` **K**: States a separate row runs from black to white; consistent with the existing Honeycomb label.
43. `chr/ui_icon_licences` **H**: Check that the draft noun denotes interface icons, rather than marks or generic signs, before assigning licence notices to it.
44. `chr/ui_icon_licences_kde_breeze` **H**: KDE Breeze identifies the pack, but the same ambiguous interface icon terminology must be resolved first.
45. `chr/ui_icons_artwork` **H**: Draft's marks-and-pictures contrast does not securely identify icons separately from artwork.
46. `chr/ui_icons_fonts_artwork_credits` **H**: Attribution/credit wording should cover full records and artwork, not merely named sources; resolve the ambiguous icon term too.
47. `chr/ui_image_assembly_workspace_drag_placed_images_or_drop` **H**: Exact right and bottom snap targets and the difference between thumbnails and placed images need clearer syntax.
48. `chr/ui_image_credits` **K**: Existing credits/source pair anchors this heading as attribution records for the images.
49. `chr/ui_image_placed_drag_it_to_move_or_hold` **H**: Distinguish moving the already placed image from holding and dragging a second tray thumbnail.
50. `chr/ui_image_shown_in_crop_preview` **K**: Keeps the crop context and labels the displayed image as the preview.
51. `chr/ui_image_thumbnails_and_filenames_scroll_horizontally_for_more` **H**: Make the thumbnail representation distinct from a physically small input image; verify the horizontal scroll direction explicitly.
52. `chr/ui_insert_gallery_image` **K**: Existing gallery-image and insert terms combine naturally as a confirmation question.
53. `chr/ui_invalid_image_attachments` **K**: Invalid attachments are identified as the problem, not a blanket image-format error.
54. `chr/ui_lossless_jpeg_xl` **H**: The missing/lost gloss could describe the file being present or not; express that compression loses no image data.
55. `chr/ui_magnified_preview` **K**: Preview plus nearer view conveys magnification and retains the ellipsis of the control.
56. `chr/ui_magnified_preview_ea9209` **K**: Same magnification phrase without the affordance ellipsis, matching the static label.
57. `chr/ui_modified_newest_first` **K**: The date sort sorts by modification and explicitly puts newer entries first.
58. `chr/ui_modified_oldest_first` **K**: Oldest is the leading sort direction, consistently paired with newest.
59. `chr/ui_monospace` **K**: Equal widths in a font context distinguishes monospace from an ordinary font family name.
60. `chr/ui_no_attachment_fits_within_the_current_coordinate_range` **H**: The current range is too generic; make coordinate limits and image resizing clear rather than asking for another source image.
61. `chr/ui_no_gallery_images_have_been_inserted` **H**: The source requires no credit text available; draft points broadly at credit details and viewing rather than specifically absent text.
62. `chr/ui_not_enough_memory_to_inspect_the_gallery_image` **K**: Negative memory sufficiency is linked to inspecting this gallery image, not importing or saving it.
63. `chr/ui_not_placed` **K**: Directly negates the same placement state used by the positive label.
64. `chr/ui_open_source_credits_and_notices` **H**: Open-source modifier may imply files are opened, and wording should distinguish credits from formal notices.
65. `chr/ui_original_decoded_image_rgba_4_bytes_pixel_estimated` **H**: Keep original and decoded image distinct without an unexplained arrow, and confirm the no-resizing limitation of the estimate.
66. `chr/ui_other_terms` **K**: Same terms noun as the paired credits-and-terms heading, scoped to additional terms.
67. `chr/ui_pencil_keeps_crisp_one_pixel_strokes_cursor_drawing` **H**: Same unverified crisp term as the pencil instructions; verify that it describes a sharp edge at all selected widths.
68. `chr/ui_percent_of_pixels` **H**: Percent and pixel value are juxtaposed; explicitly denote the percentage of the dynamic reference, not a pixel unit selector.
69. `chr/ui_pinch_to_zoom_drag_to_pan` **K**: The two separate gestures remain tied to zooming and moving the view, respectively.
70. `chr/ui_place_at_least_one_image_in_the_workspace` **K**: Establishes first placing an image in the workspace and gives an explicit minimum of one.
71. `chr/ui_placed` **K**: Placed label matches the term elsewhere in the workspace.
72. `chr/ui_px_drag_an_image_to_move_hold_a` **H**: Resolve the thumbnail term and distinguish hold-to-add from starting a drag of an already placed image.
73. `chr/ui_rendering_images` **K**: Completed-image wording matches the progress counter, and retains processed versus total placement of placeholders.
74. `chr/ui_restore_original_sizes` **K**: Restoration applies to original dimensions, not original cropped pixels.
75. `chr/ui_right_arrow_expand` **H**: Prefer existing expansion verb for the UI control; the current verb also labels canvas enlargement and could describe the wrong action.
76. `chr/ui_same` **K**: Uses the same modifier as the width and height specific labels; dynamic axis retained.
77. `chr/ui_same_height` **K**: Uses the locale's existing height term and the shared-dimension wording.
78. `chr/ui_same_width` **K**: Uses the established width term and distinguishes it from same height.
79. `chr/ui_set_radius_px_then_drag_between_opposite_corners` **K**: Matches the Radius concept, opposite corners, and the explicit half-shorter-edge bound for each rectangle.
80. `chr/ui_show_pixel_grid_800` **K**: Show is the converse of hide, with established grid term and the exact 800% threshold.
81. `chr/ui_shows_the_whole_assembly_image_and_output_sizes` **K**: Says the entire assembly is shown, not resized; image and output dimensions stay unchanged.
82. `chr/ui_smallest` **K**: The superlative form is scoped by the dimension selector, not a general smaller-copy instruction.
83. `chr/ui_some_previews_could_not_be_decoded_you_can` **H**: Pixel conversion shorthand does not clearly identify preview decode failures; also ensure remove refers only to the affected images.
84. `chr/ui_sort_images_by_filename_or_modification_time` **K**: Keeps two alternative sort keys, filename and when the image changed.
85. `chr/ui_sort_tray` **H**: Current text can read as sort small photos; label the tray as the UI object, not source image resolution.
86. `chr/ui_source_code_exported_including_build_scripts_and_licence` **H**: Clear source-code export needs the same terminology as the command and error; the build-script and notices concepts should remain separate.
87. `chr/ui_strikethrough` **K**: The graphic is a line in the middle of written text, distinct from underline.
88. `chr/ui_tap_a_pixel` **K**: Applies the existing short tap gesture to a single pixel.
89. `chr/ui_tap_an_enclosed_area_adjust_tolerance_for_similar` **H**: Retain the boundary of the tapped area (not an already filled area) and use the established tolerance control wording.
90. `chr/ui_tap_an_image_thumbnail_first` **H**: Preserve the first short tap but disambiguate the tray thumbnail from the image itself.
91. `chr/ui_tap_the_canvas_to_place_text_and_choose` **K**: Short tap on the canvas to position the text, then choose the established font and size controls.
92. `chr/ui_tap_the_image_to_sample_the_foreground_colour` **H**: Tells the reader to choose foreground colour without making clear the tap samples that point's existing colour.
93. `chr/ui_tap_vertices_then_double_tap_the_last_vertex` **H**: Ensure double-tap is on the final vertex, use the exact Close polygon caption, and clearly say that the result can remain open.
94. `chr/ui_that_arrangement_overlaps_another_image_use_a_different` **H**: The overlap meaning and unplace (not delete) for attached images should be explicit.
95. `chr/ui_the_assembly_exceeds_android_s_coordinate_range` **H**: Generic limit and a greater-than sign do not unambiguously explain Android's x/y coordinate-range limit.
96. `chr/ui_the_assembly_needs_about_choose_a_smaller_output` **H**: Identifies estimated memory, but the proposed smaller size needs to be scoped to assembly output, not the originals.
97. `chr/ui_the_assembly_output_is_unavailable_reopen_image_assembly` **K**: Names the unavailable output and preserves reopen-then-retry steps with the workspace label.
98. `chr/ui_the_attachment_image_is_missing` **K**: Identifies missing attached bitmap rather than a blank target or an unplaced image.
99. `chr/ui_the_attachment_image_is_not_placed` **K**: Uses the same placement state as the label and does not call the file missing.
100. `chr/ui_the_first_image_starts_at_the_top_left` **K**: The first input's top-left origin is explicit without implying every image starts there.

## Batch 6: Cherokee, 100 draft entries

- Combined wording snapshot: `b05fb20235ea266b4265f4236c3fb7258d6c790a` (Cherokee draft positions 129–228, one-based).
- Compared the source and candidate per key; checked recurring UI, accessibility, format and diagnostic terms against the pinned Cherokee resources at `597e644c31c450d45aa6962d89564581d4434758`. Keep means retained as reviewed draft wording; hold means revise or verify the stated concern. This is not Android integration or runtime verification.
- This batch: 68 keep, 32 hold. Running totals: 600 reviewed, 392 keep, 208 hold.

1. `chr/ui_the_gallery_download_is_too_large` **H**: Size is stated, but the wording may describe downloading a gallery or an image dimension rather than the download payload.
2. `chr/ui_the_gallery_image_is_unavailable` **K**: Unavailability is tied to the gallery image rather than a missing local file.
3. `chr/ui_the_gallery_redirected_outside_its_supported_hosts` **H**: Unsupported URL is named; the preceding away-to-another-URL fragment does not clearly describe a redirect.
4. `chr/ui_the_image_could_not_be_downloaded` **K**: Keeps the failed online transfer distinct from failure to open or draw the image.
5. `chr/ui_the_images_cannot_fit_within_android_s_coordinate` **H**: Keeps the smaller-size remedy, but the Android limit needs to name the coordinate range explicitly.
6. `chr/ui_the_normalized_image_dimensions_are_outside_android_s` **H**: A greater-than fragment does not encompass all dimensions outside the valid range, and the slash leaves the affected axes unclear.
7. `chr/ui_the_online_gallery_could_not_be_loaded_check` **H**: Keeps check-and-retry; the load failure reads as closing the gallery, not opening or loading it.
8. `chr/ui_third_party_notices` **K**: The heading ties notices to other parties and does not narrow them to licences alone.
9. `chr/ui_this_image_is_outside_the_supported_catrobat_gallery` **K**: Keeps the specific Catrobat gallery boundary rather than alleging a broken image.
10. `chr/ui_time_unavailable` **K**: Brief unavailable-time status does not substitute a date or a zero duration.
11. `chr/ui_too_many_gallery_redirects` **H**: The doubled degree phrasing is unclear, and sending to another URL needs an explicit redirect term.
12. `chr/ui_tool_option` **K**: Compact option caption distinguishes the selection from the tool itself.
13. `chr/ui_toolbox_and_tool_options_scroll_for_more` **H**: The toolbox and choices are present, but the movement instruction does not unambiguously mean scroll in this panel.
14. `chr/ui_top` **K**: Uses the same upper-side term as the pinned vertical-flip label.
15. `chr/ui_trim_from_the_original_edges_drag_the_handles` **H**: Keep the source-file assurance; distinguish dragging the handles from general movement and state that the fields take trim amounts.
16. `chr/ui_trim_in_pixels` **K**: Preserves the edge slot and identifies pixels as the trim unit.
17. `chr/ui_unplace` **H**: Same removal idiom could mean deleting the image; this action only detaches its placement.
18. `chr/ui_widths` **K**: Keeps the plural width label distinct from the pinned height wording and a width-value field.
19. `chr/ui_you_can_add_more_images_select_fewer_files` **H**: Preserves the remaining-image count but the remedy can read as choosing smaller files rather than fewer files.
20. `chr/ui_agpl_licence` **K**: AGPL remains identifiable and the licence term matches the pinned About caption.
21. `chr/ui_jpeg_xl_codec_licences` **K**: Keeps both the JPEG XL component and the licence grouping.
22. `chr/ui_gnu_agpl_licence` **K**: Retains GNU as well as AGPL without replacing the exact licence identifier.
23. `chr/ui_preview_memory_error` **H**: Uses a preview label but shortens the explicit insufficient-memory wording used elsewhere.
24. `chr/ui_trim_in_percent` **K**: Uses the established trim stem, retains the edge slot and distinguishes percent from pixels.
25. `chr/ui_crop_preview_images` **H**: Both branches retain all three format slots and the newline. Clarify that cropping already placed images may move attached images, not remove them.
26. `chr/ui_add_palette23` **K**: Reuses the pinned palette term and presents an add action.
27. `chr/ui_added_palette23` **K**: The completed form distinguishes the confirmation from the preceding add command.
28. `chr/ui_replace_palette23` **K**: Gives the full-palette state and instructs the user to choose a colour to replace.
29. `chr/ui_edit_palette23` **K**: Identifies editing the palette itself rather than opening colour editing for one swatch.
30. `chr/ui_replace_with_active23` **K**: Active colour is the replacement value, not the swatch the user needs to replace.
31. `chr/ui_remove_palette23` **K**: Identifies removal of a colour from the palette rather than removal of the palette.
32. `chr/ui_add_active23` **K**: Identifies the current colour and the add action, consistent with the paired replace control.
33. `chr/ui_vertical_rl23` **K**: Separates vertical reading direction from right-to-left column order.
34. `chr/ui_vertical_lr23` **K**: Separates vertical reading direction from left-to-right column order.
35. `chr/ui_vertical_letters23` **K**: Identifies letter layout in vertical text rather than ordering the columns again.
36. `chr/ui_vertical_mixed23` **H**: The upper-side and sideways terms need a clearer orientation contrast; confirm the automatic mode denotes upright glyphs, not a top position.
37. `chr/ui_vertical_sideways23` **K**: The sideways option retains the condition that words stay joined.
38. `chr/ui_vertical_upright23` **H**: Character-by-character is clear but the pinned upper-side term does not by itself establish upright glyph orientation.
39. `chr/ui_top23` **K**: Pinned alignment term and upper-side value match the intended pair.
40. `chr/ui_bottom23` **K**: Pinned alignment term and lower-side value match the intended pair.
41. `chr/ui_webp_codec_licences` **K**: Names WebP and its codec licences rather than the project licence.
42. `chr/ui_heic_avif_codec_licences` **K**: Keeps both HEIC and AVIF in the same licence grouping.
43. `chr/colour20_custom_selected_slot` **K**: Custom colours follow pinned colour-tab wording; the selected numbered slot remains obvious.
44. `chr/colour20_stored_slot` **K**: Retains both slots and the distinction between tap to use and Replace to save; the quoted caption matches the replace verb.
45. `chr/colour20_empty_slot` **K**: The empty numbered slot and tap-to-select destination are distinct from an immediate save.
46. `chr/colour20_save_slot` **K**: Numbered destination and save action match the empty-slot workflow.
47. `chr/colour20_replace_slot` **K**: Numbered slot and replace action match the action named in the help.
48. `chr/colour20_saved_slot` **K**: Completed save form and destination slot remain visible.
49. `chr/gallery_image_component_unavailable` **K**: Identifies a required image component and the resulting unsuccessful import.
50. `chr/ui_lossless_format` **H**: The negative phrase needs to name no loss of image data or quality, not simply an absence or non-missing state.
51. `chr/ui_save_as_webp` **K**: Save command and explicit WebP destination retain an ellipsis for the next step.
52. `chr/ui_save_as_heic` **K**: Save command and explicit HEIC destination retain an ellipsis for the next step.
53. `chr/ui_save_as_avif` **K**: Save command and explicit AVIF destination retain an ellipsis for the next step.
54. `chr/ui_image_codec_licences` **K**: Identifies image codecs as the subjects of the licences.
55. `chr/formats22_base64_label` **H**: The generic reading/text term needs to distinguish Base64 text output from an image preview or decode step.
56. `chr/formats22_ascii_label` **K**: ASCII plus the picture term conveys a text picture within the established ASCII format family.
57. `chr/formats22_tiff_compression` **H**: The pinned bitmap term is not clear as an action of compression; confirm lossless plus compression rather than just non-missing bitmap data.
58. `chr/formats22_dib_size_limit` **K**: Correct greater-than relation is paired with the DIB file limit, not the PDF cap.
59. `chr/formats22_select_page` **K**: Direct page choice is appropriate before the numbered picker.
60. `chr/formats22_page_description` **K**: Retains filename, second metadata slot and page count on their respective lines, plus choice of one page for image editing.
61. `chr/formats22_page_number` **K**: Page term plus number matches the picker range and avoids confusing page index with file size.
62. `chr/formats22_previous_page` **K**: Paired wording clearly marks the preceding page.
63. `chr/formats22_next_page` **K**: Paired wording clearly marks the page that follows.
64. `chr/formats22_open_page` **K**: Same page stem as the adjacent picker controls plus the established Open verb.
65. `chr/formats22_page_preview` **K**: Selection and preview are both present; does not label the open action.
66. `chr/formats22_page_range` **K**: Inclusive 1–maximum range and numeric entry action remain explicit.
67. `chr/formats22_loading_page` **K**: Current and total page slots plus in-progress preview are distinct from loading the whole document.
68. `chr/formats22_page_dimensions` **K**: Page pair precedes the width-by-height pair and the pinned pixel unit.
69. `chr/formats22_preview_unavailable` **K**: Preview unavailable is distinct from loading or failed opening; preserves the diagnostic slot.
70. `chr/formats22_preview_memory` **H**: Use pinned insufficient-memory phrasing, and state that smaller dimensions are offered when opening if possible rather than guaranteed or automatically applied.
71. `chr/formats22_pdf_invalid` **H**: Distinguish unreadable file from unsupported features, and make the dependency on this Android version explicit.
72. `chr/formats22_pdf_file_size` **K**: Both constraints are present: nonempty PDF and an inclusive 512 MiB ceiling.
73. `chr/formats22_pdf_page_count` **K**: Inclusive page-count range preserves the dynamic maximum.
74. `chr/formats22_pdf_page_index` **H**: The invalid selection is present but drops the now/no-longer distinction and should explicitly tell the user to select from this same document.
75. `chr/formats22_pdf_dimensions` **H**: The connective reads as and; the warning must cover invalid dimensions or excessive size independently.
76. `chr/formats22_pdf_crop` **K**: Retains the rectangle, nonempty constraint and confinement to the selected page.
77. `chr/formats22_pdf_memory` **K**: PDF-to-image action is explicit and is compared with available image memory, not the file-size limit.
78. `chr/formats22_ascii_columns` **K**: Uses the pinned width term and specifies characters rather than pixels.
79. `chr/formats22_ascii_invert` **H**: Replacement wording does not unambiguously describe a two-way light/dark inversion rather than editing the glyphs.
80. `chr/formats22_text_not_image` **K**: Preserves the supported-image qualifier in the Base64 diagnostic.
81. `chr/gallery_copy_credit` **H**: Review the action against the pinned Copy caption and use a credit term identical to the credit confirmation.
82. `chr/gallery_edit_credits` **H**: Author-only wording is narrower than editable attribution text, which can also include source and licence.
83. `chr/gallery_credit_copied` **H**: The parenthetical save term can turn a clipboard confirmation into a file-save confirmation; align it to Copy.
84. `chr/gallery_credit_title` **K**: Identifies the artwork and retains the name slot.
85. `chr/gallery_credit_publisher` **K**: Distinguishes publisher from artwork and keeps the Catrobat project name.
86. `chr/gallery_credit_gallery` **K**: Reuses the gallery noun in the adjacent gallery warnings and leaves the source name slot intact.
87. `chr/gallery_credit_licence` **K**: Keeps original Catrobat artwork, exact licence identifier and linked value together.
88. `chr/gallery_credit_saved` **H**: Broaden beyond author text so this confirms saving the entire attribution field.
89. `chr/formats22_ico_size` **H**: The icon noun is the same stem used for bitmap elsewhere; distinguish an icon choice explicitly.
90. `chr/formats22_ico_decode_budget` **H**: Decoding needs to name the icon rather than a generic bitmap as the source of this memory check.
91. `chr/formats22_ico_invalid_size` **H**: The literal size list is correct; resolve the icon-vs-bitmap label consistently with the size picker first.
92. `chr/save20_bmp_size_limit` **K**: Names BMP and points to its file-size limit rather than a per-axis limit.
93. `chr/save20_gif_size_limit` **K**: Width and height are explicitly subject to the same inclusive 65,535-pixel limit.
94. `chr/ui_pencil_crisp_adjustable_strokes` **K**: Pencil is distinguished by crisp edges and the caption keeps the any-selected-width qualification.
95. `chr/ui_cursor_ink30` **K**: Exact match to pinned cursor-drawing feature caption, rather than the brush-only action.
96. `chr/ui_cursor_help31` **H**: The staged gestures remain, but the Drawing submenu caption does not match pinned ui_drawing23; verify the actual submenu path and use exact labels.
97. `chr/ui_cursor_settings31` **K**: Extends the pinned cursor-drawing caption with settings and preserves the dialog ellipsis.
98. `chr/ui_cursor_marker_help31` **H**: It says cursor size and stroke size; specify the visible cursor marker itself, not pointer movement or the actual drawing region.
99. `chr/ui_gimp_translations31` **K**: Retains translations, credits and licences as distinct concepts, consistent with the pinned About grouping.
100. `chr/ui_cursor_pan_draw32` **H**: The first directional movement verb also appears in removal contexts; clarify that dragging repositions the cursor while painting and the second tap stops drawing.

## Batch 7: Cherokee and Eastern Huasteca Nahuatl, 100 draft entries

- Combined wording snapshot: `b05fb20235ea266b4265f4236c3fb7258d6c790a` (Cherokee draft positions 229–308 and Eastern Huasteca Nahuatl draft positions 1–20, one-based).
- Reviewed wording against each source and checked relevant terms, gestures, diagnostics and control captions against locale resources at `597e644c31c450d45aa6962d89564581d4434758`. Earlier structural-only observations about the two Cherokee percent labels inform this decision but were not counted as previous wording decisions. Keep is an editorial decision on this draft, not a merge or runtime check.
- This batch: 49 keep, 51 hold. Running totals: 700 reviewed, 441 keep, 259 hold.

1. `chr/ui_cursor_pan_move32` **H**: The cursor movement uses the same removal stem held in batch 6; distinguish repositioning from removal and identify the drawing button separately.
2. `chr/ui_cursor_tap_hint37` **K**: Preserves tap on the cursor itself and both possible toggle outcomes.
3. `chr/ui_normalize_width_intro` **H**: Same-width command and file/crop preservation are clear, but “same width/height” may read as both dimensions staying fixed rather than each image keeping its ratio.
4. `chr/ui_normalize_height_intro` **H**: Same-height command and count are clear, but each image's width-to-height ratio needs to be explicit.
5. `chr/ui_normalize_width_info` **H**: All four slots survived; make the percentage denominator the largest current width, not an adjacent independent number.
6. `chr/ui_normalize_height_info` **H**: All four slots survived; make the largest current height the comparison base, and keep the opposite-axis width range.
7. `chr/ui_normalize_width_input_percent` **H**: This distinct draft entry has the accessibility issue seen in the structural pass: parenthetical pixels do not express “percentage of” the reference width.
8. `chr/ui_normalize_height_input_percent` **H**: Parenthetical pixels likewise do not express “percentage of” the reference height; do not reuse the width label.
9. `chr/ui_pixel_grid_help33` **K**: Keeps the inclusive 800% threshold and identifies ruler readings as locations in image pixels.
10. `chr/ui_gallery_back34` **K**: Short back action matches the return wording used elsewhere in the locale.
11. `chr/ui_gallery_unsupported34` **K**: Keeps the selected-source boundary, not deletion or unavailability of the image.
12. `chr/ui_open_artwork34` **K**: Exact pinned Use image caption follows the instruction to open the artwork page first.
13. `chr/ui_creator_on_source34` **H**: Creator name is narrower than contributor; do not invent that the contributor necessarily made the image.
14. `chr/legacy_credits_title` **H**: Earlier and saved are clear, but the author-only stem understates the contents of the existing credit records.
15. `chr/legacy_credits_hint` **H**: Earlier records and possible other images survive; make the export a text file, not simply saving the displayed text in the app.
16. `chr/legacy_credits_add` **H**: The selection and destination are clear, but credit needs to include licence and source, not just author.
17. `chr/legacy_credits_save_text` **H**: Distinguish the selected complete credit text from saving an author's name or a generic read action.
18. `chr/legacy_credits_existing` **H**: Preserve both existing attribution for that same source and the fact that its text was retained, not overwritten.
19. `chr/legacy_credits_added` **H**: Completed add is distinct from the action, but author-only terminology would misdescribe a full credit record.
20. `chr/commons_check_file_licence` **H**: The list keeps creator and licence, but required attribution and “may count as an adaptation” need clearer scope than name and new creation.
21. `chr/ui_an_image_cannot_attach_to_itself_or_one` **K**: Retains both prohibited targets, self and its attached image, rather than banning all attachments.
22. `chr/ui_catrobat_s_own_artwork_uses_cc_by_sa` **H**: File and About captions align, but verify the last menu caption and express attribution requirements beyond a creator name.
23. `chr/ui_catrobat_sticker_gallery` **K**: Identifies both sticker imagery and its gallery, with ellipsis for a subsequent screen.
24. `chr/ui_gallery_artwork_catrobat_and_its_credited_creators_cc` **H**: Licence exception and trailing line breaks survived; ensure the credit requirement covers artwork attribution, not only the creator's name.
25. `chr/formats22_tiff_description` **H**: One RGB page and undisturbed pixels are present; reuse a clearer compression term rather than the bitmap stem.
26. `chr/formats22_dib_description` **H**: Preserves the BMP-header condition and 24-bit DIB; clarify uncompressed so it cannot read as no bitmap.
27. `chr/formats22_base64_description` **H**: Literal prefix and size direction are right; clarify lossless and that reopening the Base64 text recovers the image without silently converting formats.
28. `chr/formats22_ico_description` **H**: Numeric bounds and centring survive; align the icon noun with the held size control and make the transparent square explicit.
29. `chr/formats22_ico_dimensions_error` **H**: Keep the image-size mismatch but explicitly locate the competing dimensions in the corresponding ICO directory record.
30. `chr/save20_bmp_description` **H**: The colour and larger-file contrast is present; same compression-vs-bitmap ambiguity as the DIB description.
31. `chr/save20_unsupported_tagged_colour` **H**: The conversion sequence survives, but metadata alone is broader than colour profile; keep the format condition exact and check the older key's consumer.
32. `chr/ui_search_english34` **K**: Clear choice between searching in English and Japanese; does not imply the artwork itself is translated.
33. `chr/ui_openclipart_help34` **H**: The tap verb reads as press/hold in other pinned help; align the gesture and verify the precise Image credits caption.
34. `chr/ui_irasutoya_credit34` **K**: States retained copyright, source terms and the specific distinction from Creative Commons without inventing a permission.
35. `chr/commons_import_svg_changes` **K**: Protects the four technical fields and identifies size as the original size.
36. `chr/commons_import_raster_changes` **K**: Keeps the white background literal and an explanation that this is alpha/background composition, not an independent licence restriction.
37. `chr/commons_credit_copy_failed` **H**: Copy action reads as making a duplicate; align clipboard wording with the pinned Copy caption.
38. `chr/commons_credit_copy_failed_reason` **H**: Diagnostic slot survives, but the copy action must match the no-reason variant and the actual clipboard action.
39. `chr/commons_credit_copy_out_of_memory` **H**: Explicit memory shortage matches pinned diagnostics; clipboard action still needs the same wording as the other two variants.
40. `chr/commons_metadata_http_error` **K**: Commons metadata stage, HTTP prefix and diagnostic value remain separate.
41. `chr/commons_metadata_response_too_large` **H**: The wording points to size but is less clear about the limit being the server response limit.
42. `chr/commons_metadata_query_failed` **K**: A query failure is distinct from missing metadata or failed image transfer.
43. `chr/gallery_description` **H**: Align the copied control captions and distinguish named creators, copyright and source notices from generic credits in this long help.
44. `chr/gallery_credit_edit_hint` **H**: Retains editable text and changes, but avoid reading removal of an unused source as deletion of the file.
45. `chr/ui_irasutoya_help34` **H**: Retains the 21-or-more condition, but the hold-like gesture and the exact source-credit path need correction before reuse.
46. `chr/ui_assembly_exact_position` **K**: Marks precise X/Y positioning with a familiar alignment term; it is not a snap command.
47. `chr/ui_assembly_target_x` **K**: The X input names the left-edge origin in pixels.
48. `chr/ui_assembly_target_y` **K**: The paired Y input names the top-edge origin in pixels.
49. `chr/ui_assembly_position_help` **H**: Coordinates and allowed overlap are present, but whole pixels and later-imported images being drawn above earlier ones need unambiguous phrasing.
50. `chr/ui_assembly_position_nonnegative` **H**: Numeric range is exact, but the completed/saved form does not reliably communicate integer-only entry.
51. `chr/ui_assembly_unknown_image` **K**: Kept clear that the selected image is not in this assembly now, without calling its file lost.
52. `chr/gallery_external_link_no_handler` **K**: Names Android's inability to find an app for this link rather than a generic network error.
53. `chr/commons_metadata_not_file_page` **K**: Correctly limits the diagnostic to the required Commons file-page type.
54. `chr/commons_metadata_ambiguous_file` **K**: The returned file is indeterminate; does not claim that a known file is missing.
55. `chr/commons_metadata_unavailable` **K**: Unavailability is specifically of Commons file metadata, not the image.
56. `chr/commons_metadata_original_mismatch` **K**: Distinguishes the selected original file from the attribution that failed to match it.
57. `chr/commons_metadata_invalid_page` **K**: Invalid applies to the attribution page, not to the Commons service or image format.
58. `chr/commons_metadata_field_too_large` **H**: The candidate says the field is too large; identify the explicit text limit, not size of a file or page.
59. `chr/commons_metadata_cache_failed` **K**: Retaining existing attribution is the unsuccessful action, not a query or clipboard failure.
60. `chr/commons_download_original_mismatch` **H**: The target original file survives but the same send-to-a-URL phrasing held in batch 6 needs a distinct redirect action.
61. `chr/commons_svg_png_encode_failed` **K**: Distinguishes blank map to PNG encoding from downloading or opening the map.
62. `chr/ui_add_up_to_20_images_with_android_s` **H**: The help preserves the 20-image limit and trim structure, but its long-press/drop instructions and crop-triggered movement need a control-by-control correction.
63. `chr/ui_help23` **H**: The shorter help already uses a Drawing caption different from pinned ui_drawing23; reconcile named controls and gesture terms before integration.
64. `chr/ui_casual` **H**: The phrase can mean handwriting broadly rather than the Casual typeface category; compare with Cursive.
65. `chr/ui_cursive` **K**: The joining description differentiates cursive from the non-joined writing style.
66. `chr/ui_estimates_include_the_current_canvas_and_clipboard_sampled` **K**: Preserves the canvas, clipboard and sampled decode/buffer sources of the estimate, variability, detail loss and the original-file guarantee.
67. `chr/ui_hue_and_saturation_spectrum_lightness_slider_on_the` **K**: HSL H/S and L remain distinct, and the lightness control stays on the right.
68. `chr/ui_hue_and_saturation_wheel_value_slider_on_the` **K**: Wheel term and HSV/V distinguish this variant from the HSL spectrum.
69. `chr/ui_pale_violet` **H**: The parenthetical appears to mark small/light colour generically; verify that it denotes a pale violet shade and not a reduced amount.
70. `chr/ui_sans_condensed` **K**: Keeps the sans modifier and the reduced glyph-width descriptor.
71. `chr/ui_sans_light` **K**: Sans modifier is retained and the low-weight form contrasts with medium.
72. `chr/ui_sans_medium` **K**: Medium is tied to weight within the same sans family rather than middle alignment.
73. `chr/ui_sans_serif` **K**: No-end-stroke description pairs clearly with the serif counterpart.
74. `chr/ui_sans_thin` **H**: Thin is differentiated by degree, but drops the sans-family modifier retained in the other weights.
75. `chr/ui_serif` **K**: Positive stroke-ending marker is the counterpart to the sans label.
76. `chr/ui_smooth_freehand_strokes` **K**: Smoothing is tied to hand-drawn strokes rather than the antialiasing of pixel edges.
77. `chr/ui_smooth_pixel_edges_anti_aliasing` **K**: Pixel edges and explicit anti-aliasing disambiguate this from stroke smoothing.
78. `chr/ui_vertical_hint23` **H**: Preserves column starts and joined scripts, but the upper-side term does not establish upright glyphs; clarify combining marks as opposed to all marks.
79. `chr/formats22_pdf_encrypted` **H**: Preserve the alternatives, not a requirement for both password and unsupported encryption, and make clear that the saved copy is unprotected.
80. `chr/ui_the_arrow_on_the_left_directly_below_the` **H**: Long tutorial repeats the Drawing submenu mismatch and treats some cursor and unplace movements with the held removal stem.
81. `nhe/ui_an_paint_assembly_image` **K**: AN Paint is the named origin and the image is the result of arranging inputs.
82. `nhe/ui_an_paint_image_assembly` **K**: Matches the pinned assembly term and keeps the brand separator.
83. `nhe/ui_assembly_output_size` **H**: The output image size remains, but the assembly is unnamed and could be mistaken for a generic new-image size.
84. `nhe/ui_could_not_create_the_assembly` **K**: Names the failed assembly creation and preserves the diagnostic slot.
85. `nhe/ui_could_not_load_gallery_image` **H**: Tlapoa matches Open in existing strings; here establish whether the operation means load, not simply open the gallery artwork.
86. `nhe/ui_downloading_image` **H**: The generic take/get verb does not distinguish an online download from selecting or picking an image.
87. `nhe/ui_gallery_image` **K**: Concise gallery source label is consistent with the paired insert prompt.
88. `nhe/ui_insert_gallery_image` **K**: Question retains insertion and gallery provenance without sounding like an immediate action.
89. `nhe/ui_the_attachment_image_is_missing` **K**: Tlatzquilti distinguishes the missing attached image from a missing base image.
90. `nhe/ui_the_attachment_image_is_not_placed` **K**: Ayicanah and placement verb keep not-yet-placed distinct from missing.
91. `nhe/ui_the_gallery_image_is_unavailable` **K**: Axoncah qualifies the gallery image's availability, not device connectivity.
92. `nhe/ui_the_image_could_not_be_downloaded` **H**: Error needs the same explicit download stem as the progress state, not generic inability to take the image.
93. `nhe/formats22_select_page` **K**: Pinned picker verb works directly with the page noun and does not imply opening the whole document.
94. `nhe/ui_cursor_ink30` **K**: Pinned cursor controls already establish the cursor and drawing stems; imperative suits the action.
95. `nhe/ui_cursor_settings31` **H**: The phrase can read as how to draw with the cursor; make settings explicit rather than a how-to caption.
96. `nhe/ui_cursor_pan_draw32` **K**: Drag/move, start drawing and second tap to stop remain three distinct steps.
97. `nhe/ui_cursor_pan_move32` **H**: Positioning is clear, but the second clause says generic button; name the drawing button to avoid tapping the cursor itself.
98. `nhe/ui_cursor_tap_hint37` **K**: Directly names the cursor as the toggle target and pairs start with stop.
99. `nhe/ui_the_first_image_starts_at_the_top_left` **H**: The origin sounds like a top edge only; retain both top and left explicitly.
100. `nhe/ui_create_output` **K**: Output is described as the image to create, not an instruction to save or export it.

## Batch 8: Eastern Huasteca Nahuatl, 100 draft entries

- Combined wording snapshot: `b05fb20235ea266b4265f4236c3fb7258d6c790a` (Eastern Huasteca Nahuatl draft positions 21–120, one-based).
- Reviewed each candidate and source. Checked established locale terminology and UI captions against `597e644c31c450d45aa6962d89564581d4434758`. Keep is a draft editorial decision only, not integration or a device check.
- This batch: 79 keep, 21 hold. Running totals: 800 reviewed, 520 keep, 280 hold.

1. `nhe/ui_drag_to_erase_with_the_background_colour` **K**: The drag action and erasing with the background colour are both explicit; iica matches the pinned background terminology.
2. `nhe/ui_fill_text_box_with_bg_colour` **H**: Pinned wording distinguishes text from its area, but “where text is” does not establish the box or all of its fill.
3. `nhe/ui_hold_or_drag_to_spray_colour` **K**: Retains a sustained press or drag and uses the air metaphor to distinguish spraying from regular brush strokes.
4. `nhe/ui_magnified_preview` **H**: Reads as an instruction to show something larger; use a preview noun or a caption consistent with pinned Preview for the tool opening.
5. `nhe/ui_magnified_preview_ea9209` **H**: The no-ellipsis label has the same command-vs-preview ambiguity; keep the paired form consistent after revision.
6. `nhe/ui_not_placed` **H**: This reads as not yet placed; the standalone state should also apply to something unplaced after having been placed.
7. `nhe/ui_placed` **K**: The completed form gives a placement state rather than a place command.
8. `nhe/ui_unplace` **H**: Remove from where it is may sound like deleting or moving the image; explicitly keep the input and remove only its placement.
9. `nhe/ui_restore_original_sizes` **K**: Restores the prior dimensions of each image instead of imposing a common dimension.
10. `nhe/ui_pinch_to_zoom_drag_to_pan` **K**: Identifies a two-finger gesture separately from moving the view and does not mention drawing.
11. `nhe/ui_tap_a_pixel` **K**: A single pixel is the direct tap target; the existing gesture verb is not paired with a hold here.
12. `nhe/ui_the_gallery_download_is_too_large` **H**: General “what is taken” does not identify the gallery download payload and may instead mean image size.
13. `nhe/ui_replace_with_active23` **K**: Treats the active colour as the replacement value, not the swatch being replaced.
14. `nhe/ui_add_active23` **K**: Identifies the current colour as the item to add, mirroring the previous control.
15. `nhe/ui_top23` **K**: Marks upper alignment, paired with the lower alternative.
16. `nhe/ui_bottom23` **K**: Marks lower alignment, distinct from the top anchor and sorting.
17. `nhe/ui_assembly_target_x` **K**: X is measured in pixels from the left, consistent with the position controls.
18. `nhe/ui_assembly_target_y` **K**: Y is measured in pixels from the top, retaining the correct axis origin.
19. `nhe/ui_assembly_exact_position` **K**: Refers to an exact location rather than snapping or alignment.
20. `nhe/commons_blank_maps` **H**: “Without writing” can imply only unlabelled text; verify that the map term covers blank outlines rather than an empty map or zero text.
21. `nhe/commons_check_file_licence` **K**: Preserves per-file Commons checks, creator, licence, required credit and the possibility of adaptation.
22. `nhe/ui_about_copyright` **K**: Identifies the app's About information plus copyright, distinct from the full three-part heading.
23. `nhe/ui_about_copyright_licence` **K**: Preserves copyright and licence as distinct concepts in the About heading.
24. `nhe/ui_add_images_then_drag_a_thumbnail_here` **K**: Explicitly adds images before a miniature is dragged into this position.
25. `nhe/ui_add_to_custom_colours` **K**: Identifies the saved custom-colour area as the destination, not a generic colour picker.
26. `nhe/ui_an_image_cannot_attach_to_itself_or_one` **K**: Specifies both prohibited targets, the image itself and one already attached to it.
27. `nhe/ui_batch_crop` **H**: Wording can mean keep a single shared region in all images; batch crop applies margins to multiple images, not necessarily one identical pixel box.
28. `nhe/ui_batch_crop_images` **H**: Same shared-region ambiguity as the short Batch crop label; keep the multiple-image action explicit.
29. `nhe/ui_by_pixels_hold_and_drag_to_place` **K**: Both text slots and the two dimensions are intact; finger-down pause and drag remain separate.
30. `nhe/ui_catrobat_online_gallery_artwork_by_its_credited_creators` **K**: Retains the online venue and named creators rather than attributing all art to Catrobat alone.
31. `nhe/ui_catrobat_sticker_gallery` **K**: Sticker-specific wording distinguishes this entry from a generic Catrobat gallery and keeps the ellipsis.
32. `nhe/ui_common_in` **K**: Keeps the variable dimension and unit in separate format slots; san se expresses common.
33. `nhe/ui_common_in_pixels` **K**: Keeps the variable dimension and explicit pixel unit, consistent with the unit-variable companion.
34. `nhe/ui_copper` **K**: Cobre is the recognizable copper palette colour and pairs with the metal names.
35. `nhe/ui_corners_and_edges_resize_round_handle_rotates` **K**: Distinct square corners/edges and round handle are correctly assigned to resize and rotation.
36. `nhe/ui_could_not_decode_the_cropped_region_of` **H**: Generic read does not distinguish decoding from file access; keep the selected cropped region and identify decode failure.
37. `nhe/ui_could_not_export_source_code` **K**: Source code is expressly the target and the extraction action matches export, not opening or printing it.
38. `nhe/ui_credits_terms` **H**: Authorship alone is narrower than credits, which also contain attribution and source information; do not collapse that distinction.
39. `nhe/ui_cropped_thumbnail` **K**: A cropped miniature, not a full preview; diagnostic/name slot is preserved.
40. `nhe/ui_current_safe_budget_2f_mp` **K**: Gives the current usable megapixel ceiling and preserves the decimal precision token.
41. `nhe/ui_current_safe_editing_budget_s_up_to_2f` **K**: Keeps memory and MP slots separate and notes exclusion of additional decoding memory.
42. `nhe/ui_cursive` **K**: Recognizable Cursiva names the font category rather than instructing the user to italicize.
43. `nhe/ui_custom_colour` **K**: The colour identifier remains attached to the user-selected custom colour.
44. `nhe/ui_custom_colours_hold_a_swatch_to_replace_it` **K**: Sustained finger contact on a colour entry is distinct from a tap, and replacement is the outcome.
45. `nhe/ui_drag_a_line_then_drag_twice_to_set` **K**: Retains two bend-setting drags and uses the exact pinned Finish curve caption for early commitment.
46. `nhe/ui_drag_a_selection_drag_inside_to_move_square` **K**: Distinguishes draw, drag, resize and rotate; the lock wording expresses a relation between width and height.
47. `nhe/ui_drag_across_the_ellipse_s_bounding_box` **H**: The second corner appears but the initial opposite corner is implicit; define the drag across the bounding rectangle.
48. `nhe/ui_drag_between_opposite_corners_choose_outline_or_fill` **K**: Both opposing corners and the outline-or-interior choice are visible.
49. `nhe/ui_drag_between_opposite_corners_to_draw_a_five` **K**: Retains the five points plus the same two fill modes and corner-to-corner gesture.
50. `nhe/ui_drag_between_opposite_corners_to_draw_a_heart` **K**: Identifies the heart independently while matching the star's gesture and outline/fill choices.
51. `nhe/ui_drag_from_the_start_to_the_end_of` **K**: Keeps the drawing start and end distinct without assigning a particular slope.
52. `nhe/ui_drag_from_the_tail_towards_the_arrowhead_choose` **K**: Arrow tail and head set direction; the outline/fill decision is separate.
53. `nhe/ui_drag_out_to_expand_in_to_trim_drag` **K**: Four operations remain distinct, and the new space is filled by background colour, not a foreground swatch.
54. `nhe/ui_drag_placed_images_to_move_them_hold_and` **K**: Keeps movement of a placed image distinct from the long-press-and-drag used to add a new thumbnail.
55. `nhe/ui_drag_to_pan_without_drawing_pinch_with_two` **K**: Single drag explicitly does not draw; the two-finger gesture works even when a drawing tool is selected.
56. `nhe/ui_draw_a_crisp_one_pixel_line` **H**: Melahuac can make crisp read as straight, losing sharp edges even though the numeric width range is right.
57. `nhe/ui_draw_around_an_area_drag_inside_to_move` **K**: The freeform outline and the three subsequent manipulations remain separate; the caption names committing the selection.
58. `nhe/ui_draw_soft_watercolor_strokes_strength_controls_how_strongly` **K**: The water-and-colour description preserves soft strokes, and the strength parameter affects blending.
59. `nhe/ui_draw_with_the_selected_brush_tip_and_size` **K**: Brush tip and size are explicitly the two chosen settings.
60. `nhe/ui_drop_at_a_highlighted_edge_right_top_aligned` **K**: Distinct highlighted drop target and right/top versus below/left snap options are preserved.
61. `nhe/ui_enable_android_s_files_or_documents_app_then` **K**: Both exact Android app names and the retry sequence survive.
62. `nhe/ui_export_this_version_s_source_code` **K**: Describes the current version's source and preserves the ellipsis for the export flow.
63. `nhe/ui_filename_a_z` **K**: Filename is explicit and the ascending direction is unchanged.
64. `nhe/ui_filename_z_a` **K**: The same filename caption correctly reverses its sorting direction.
65. `nhe/ui_fits_the_current_budget` **K**: Specifies available RAM as the relevant budget without claiming a storage or file-size check.
66. `nhe/ui_font_licences` **K**: Licence and typeface terms distinguish this from icon licensing.
67. `nhe/ui_give_all_images_the_same_each_image_keeps` **H**: Aspect-ratio and original-file safeguards are present, but cencah can be read as very rather than same; match the common-sizing controls.
68. `nhe/ui_gnu_affero_general_public_license` **K**: The official licence name remains quoted in English alongside the understandable descriptive form.
69. `nhe/ui_gold` **K**: The familiar Oro palette term is consistent with Cobre and the other metal labels.
70. `nhe/ui_hide_pixel_grid_800` **K**: Explicit Hide, pixel grid and the 800%+ threshold are retained.
71. `nhe/ui_hold_a_thumbnail_and_drag_it_here_or` **K**: Separates long-press and drag from two quick taps on different targets.
72. `nhe/ui_honeycomb` **K**: Panal is a concise description of the honeycomb arrangement, not the regular palette.
73. `nhe/ui_honeycomb_colour_06x` **K**: Preserves the hex formatting slot and ties the colour to a honeycomb swatch.
74. `nhe/ui_honeycomb_colour_swatches_with_a_greyscale_row` **K**: Honeycomb arrangement and the black-to-white row are both named for accessibility.
75. `nhe/ui_hue_and_saturation_spectrum_lightness_slider_on_the` **H**: Describes hue broadly as colour and lightness as whiteness; check contrast with the adjacent HSV control before clearing.
76. `nhe/ui_hue_and_saturation_wheel_value_slider_on_the` **H**: Wheel and right-hand slider are clear; verify value/brightness wording apart from HSL lightness so the two controls stay distinguishable.
77. `nhe/ui_icon_licences` **K**: Names the licence category and the specific icon scope.
78. `nhe/ui_icon_licences_kde_breeze` **K**: Uses the same icon-licence heading and retains KDE Breeze unchanged.
79. `nhe/ui_icons_artwork` **K**: Distinguishes icons from other artwork without implying all artwork is an icon.
80. `nhe/ui_icons_fonts_artwork_credits` **H**: “Who made” alone omits possible source and licence attribution across the three categories.
81. `nhe/ui_image_assembly_workspace_drag_placed_images_or_drop` **K**: Label identifies the workspace, both drag/drop inputs, right and bottom targets, and empty-space panning.
82. `nhe/ui_image_credits` **K**: Creator and source are both named; the concise menu caption is broad enough to open the credits panel.
83. `nhe/ui_image_placed_drag_it_to_move_or_hold` **K**: Completed placement is distinct from later movement and adding another thumbnail by long press.
84. `nhe/ui_image_shown_in_crop_preview` **K**: Describes the image shown before selecting what to retain; does not imply that cropping is already applied.
85. `nhe/ui_image_thumbnails_and_filenames_scroll_horizontally_for_more` **K**: Horizontal swipe and the two contents, thumbnails and filenames, are explicit.
86. `nhe/ui_invalid_image_attachments` **H**: Uses general joining wording and can read as a physical incompatibility; retain the specific invalid attachment relationships.
87. `nhe/ui_largest` **K**: Achi huei expresses the greatest size, appropriate to a selection by image dimensions.
88. `nhe/ui_lossless_jpeg_xl` **H**: Retains the format and parenthetical Lossless, but “does not lose what is visible” is weaker than preserving image data exactly.
89. `nhe/ui_modified_newest_first` **K**: Sorts by modification, newest first, clearly distinct from import order.
90. `nhe/ui_modified_oldest_first` **K**: Reverses the modification-time ordering and keeps oldest first.
91. `nhe/ui_monospace` **H**: The width phrase can read as a lot of width, rather than each glyph having one fixed width.
92. `nhe/ui_no_attachment_fits_within_the_current_coordinate_range` **K**: Keeps the current coordinate constraint and suggests smaller image dimensions rather than fewer files.
93. `nhe/ui_no_gallery_images_have_been_inserted` **K**: No attribution text available is clearly distinguished from there being no inserted images.
94. `nhe/ui_not_enough_memory_to_inspect_the_gallery_image` **K**: RAM failure is tied to inspecting the gallery image, not to downloading it or inability to access the gallery.
95. `nhe/ui_open_source_credits_and_notices` **H**: Authorship wording narrows credits, while the documents also include attribution and notices; preserve both functions.
96. `nhe/ui_other_terms` **K**: Short terms label fits the document list and does not claim additional licences.
97. `nhe/ui_pale_violet` **K**: Names violet and a lighter shade, distinguishing the preset from plain violet.
98. `nhe/ui_pencil_keeps_crisp_one_pixel_strokes_cursor_drawing` **K**: Explicitly ties crisp edges to the pencil across all selected widths, avoiding the earlier straight-line shift.
99. `nhe/ui_percent_of_pixels` **K**: A relational percent phrase retains the pixel quantity and original format slot.
100. `nhe/ui_place_at_least_one_image_in_the_workspace` **K**: Explicit first action and one-or-more minimum prevent the error from being read as select exactly one.

## Batch 9: Eastern Huasteca Nahuatl, 100 draft entries

- Combined wording snapshot: `b05fb20235ea266b4265f4236c3fb7258d6c790a` (Eastern Huasteca Nahuatl draft positions 121–220, one-based).
- Personal per-key wording review; relevant controls and established terminology checked against pinned locale resources at `597e644c31c450d45aa6962d89564581d4434758`. Keep remains separate from Android integration and device verification. The parallel integration assignment is frozen to batches 1–8 and does not include these decisions.
- This batch: 80 keep, 20 hold. Running totals: 900 reviewed, 600 keep, 300 hold.

1. `nhe/ui_px_drag_an_image_to_move_hold_a` **K**: Pixel dimensions and both gestures are intact; long-press thumbnail is not confused with dragging the placed image.
2. `nhe/ui_quality` **K**: Keeps the setting's quality meaning and percent unit, with Quality as a familiar label.
3. `nhe/ui_rendering_images` **K**: The two slots remain processed versus total, and the ellipsis marks ongoing work.
4. `nhe/ui_right_arrow_expand` **K**: Right arrow is identified, with opening/expanding as the contrasting action.
5. `nhe/ui_sans_condensed` **K**: Narrow lettering and absence of serifs distinguish condensed from the weight variants.
6. `nhe/ui_sans_light` **K**: Keeps the sans category and pairs light weight with the stronger thin modifier.
7. `nhe/ui_sans_medium` **K**: Tlahco names the middle option within the fixed sans category rather than omitting the family.
8. `nhe/ui_sans_serif` **K**: Explicit absence of remates contrasts with the serif caption.
9. `nhe/ui_sans_thin` **K**: The intensifier distinguishes thin from light without losing the sans modifier.
10. `nhe/ui_serif` **K**: Positive presence of remates makes the intended contrasting font category clear.
11. `nhe/ui_show_pixel_grid_800` **H**: The visual verb can read as look at the grid, not toggle it on; align with the inverse Hide label.
12. `nhe/ui_shows_the_whole_assembly_image_and_output_sizes` **K**: Distinguishes viewing the whole assembly from changing input or output sizes.
13. `nhe/ui_silver` **K**: Recognizable Plata fits the same palette family as Cobre and Oro.
14. `nhe/ui_smallest` **K**: Comparative smallness identifies the minimum within the set rather than an absolute size.
15. `nhe/ui_tap_an_image_thumbnail_first` **K**: The gesture specifies immediate lift and that the thumbnail is tapped first.
16. `nhe/ui_tap_the_canvas_to_place_text_and_choose` **H**: Quen neci can mean appearance generally; name the font/typeface choice separately from its size.
17. `nhe/ui_tap_the_image_to_sample_the_foreground_colour` **K**: Identifies image sampling with foreground terminology shared by the current palette.
18. `nhe/ui_time_unavailable` **H**: Adds date and hour to a time-only fallback; match the actual metadata shown where this label is used.
19. `nhe/ui_set_radius_px_then_drag_between_opposite_corners` **K**: Opposite corners and the shorter-edge half bound both survive; radius terminology matches pinned settings.
20. `nhe/ui_some_previews_could_not_be_decoded_you_can` **H**: Recast the second remedy as trying to save, not checking whether saving is possible; keep preview failure distinct from source corruption.
21. `nhe/ui_sort_images_by_filename_or_modification_time` **K**: File name and time of modification remain two different sorting criteria.
22. `nhe/ui_sort_tray` **H**: Narrows tray contents to not-yet-placed images; the tray may include placed images too.
23. `nhe/ui_tap_an_enclosed_area_adjust_tolerance_for_similar` **K**: Tap stays tied to an enclosed region, and tolerance controls which similar colours are included.
24. `nhe/ui_tap_vertices_then_double_tap_the_last_vertex` **K**: Exact pinned Finish and Close polygon captions, double tap, and open connected segments are retained.
25. `nhe/ui_that_arrangement_overlaps_another_image_use_a_different` **H**: Clarify that the remedy detaches placements and does not delete the attached images.
26. `nhe/ui_the_assembly_exceeds_android_s_coordinate_range` **K**: Names the assembly and Android's coordinate limit, not a memory limit.
27. `nhe/ui_the_assembly_needs_about_choose_a_smaller_output` **K**: The approximate requirement is separate from the remedy of selecting a smaller output.
28. `nhe/ui_the_assembly_output_is_unavailable_reopen_image_assembly` **H**: Use the exact Image assembly caption for reopening; the second “again” could mean reopening twice rather than retrying output.
29. `nhe/ui_the_gallery_redirected_outside_its_supported_hosts` **H**: Sending a URL can mean issuing or sharing it rather than redirecting to it; clarify the change of target.
30. `nhe/ui_the_images_cannot_fit_within_android_s_coordinate` **K**: Names Android's coordinate range and asks for smaller image dimensions.
31. `nhe/ui_the_normalized_image_dimensions_are_outside_android_s` **H**: Quipano only clearly conveys exceeding an upper limit; source covers any out-of-range normalized dimension.
32. `nhe/ui_the_online_gallery_could_not_be_loaded_check` **K**: Distinguishes failure to open/load the online gallery, connection check and retry.
33. `nhe/ui_this_image_is_outside_the_supported_catrobat_gallery` **K**: Keeps the supported Catrobat gallery boundary instead of implying the image was removed.
34. `nhe/ui_too_many_gallery_redirects` **H**: Repeated URL sends are not necessarily redirects; use the same explicit redirect term as the unsupported-target warning.
35. `nhe/ui_smooth_freehand_strokes` **K**: Freehand strokes are the object of smoothing, distinct from pixel-edge antialiasing.
36. `nhe/ui_smooth_pixel_edges_anti_aliasing` **K**: Adds the visible stair-step explanation without changing the anti-aliasing control.
37. `nhe/ui_source_code_exported_including_build_scripts_and_licence` **K**: Build scripts and licence notices stay part of the exported source package.
38. `nhe/ui_spectrum` **K**: Colour arrangement caption works as the spectrum option beside a contrasting circular wheel.
39. `nhe/ui_third_party_notices` **H**: The paraphrase points to people who made things; retain the breadth of third-party notices beyond maker attribution.
40. `nhe/ui_tool_option` **K**: Option remains something the user can change on the current tool.
41. `nhe/ui_toolbox_and_tool_options_scroll_for_more` **K**: Distinguishes toolbox and configurable controls, and the drag-for-more affordance is present.
42. `nhe/ui_trim_from_the_original_edges_drag_the_handles` **K**: Original edges, draggable controls or typed amounts, and unchanged source files are all present.
43. `nhe/ui_trim_in_pixels` **K**: Edge slot stays tied to a pixel removal amount rather than an absolute position.
44. `nhe/ui_wheel` **K**: Circular colour caption is distinct from the spectrum counterpart.
45. `nhe/ui_you_can_add_more_images_select_fewer_files` **K**: Remaining image count and choosing fewer files are both clear; no size restriction is added.
46. `nhe/ui_agpl_licence` **K**: AGPL identifier is unchanged and the heading plainly names its licence.
47. `nhe/ui_jpeg_xl_codec_licences` **K**: JPEG XL is tied specifically to codec licences, not the whole app's licence.
48. `nhe/ui_an_paint_image_assembly_20_images_placed` **K**: Preserves newline, fixed capacity and separate placed count.
49. `nhe/ui_assembly_decoded_output_estimated_editing_render_memory_at` **K**: All three slots remain distinct and the memory estimate explicitly uses original size.
50. `nhe/ui_assembly_png` **K**: Localized basename preserves the PNG extension and remains an output filename.
51. `nhe/ui_casual` **H**: The wording can mean familiar/ordinary writing; check that it identifies the Casual font category distinctly.
52. `nhe/ui_copy_decoded_image_at_this_size_estimated_loading` **K**: The first line is the copy, the second decoded size and the third a load/edit RAM estimate, with all three slots and trailing newline.
53. `nhe/ui_each_px_px_percent_is_relative_to_the` **K**: Explicit percent denominator and opposite-dimension range remain separate; placed images may move to make room.
54. `nhe/ui_estimated_memory_current_working_budget` **K**: Distinguishes an estimate of needed RAM from currently available working RAM and keeps both slots.
55. `nhe/ui_original_decoded_image_rgba_4_bytes_pixel_estimated` **K**: Keeps original and decoded values, fixed RGBA bytes per pixel and the no-resize RAM condition.
56. `nhe/ui_gnu_agpl_licence` **K**: Preserves both GNU and AGPL in the licence caption.
57. `nhe/ui_trim_in_percent` **K**: Specifies the percentage trim amount for the named edge, distinct from pixels.
58. `nhe/ui_webp_codec_licences` **K**: WebP codec remains the subject of the licence heading.
59. `nhe/ui_catrobat_s_own_artwork_uses_cc_by_sa` **H**: Use the exact pinned Image credits label and broader separate attribution than just another person's name.
60. `nhe/ui_estimates_include_the_current_canvas_and_clipboard_sampled` **K**: Includes all named memory sources and variable actual usage, plus loss of detail and opaque background/source-file safeguards.
61. `nhe/ui_gallery_artwork_catrobat_and_its_credited_creators_cc` **H**: Preserve the credit scope beyond creator name when describing adaptations; the condition for separate terms is present.
62. `nhe/ui_crop_preview_images` **K**: Both plural branches preserve dimensions, count and the possible movement of attached images; no guaranteed movement is added.
63. `nhe/ui_add_palette23` **K**: Colour is added to the palette, consistent with the adjacent palette actions.
64. `nhe/ui_added_palette23` **K**: Completed save form distinguishes the feedback from the preceding Add command.
65. `nhe/ui_replace_palette23` **K**: Expresses a full palette and asks which entry will be replaced, not which colour to use.
66. `nhe/ui_edit_palette23` **K**: The palette is explicitly the edit target rather than an individual selected colour.
67. `nhe/ui_remove_palette23` **K**: Selected colour is removed from the palette, without deleting the whole palette.
68. `nhe/ui_horizontal23` **H**: Left-to-right is narrower than horizontal orientation and could conflict with bidirectional horizontal text.
69. `nhe/ui_vertical_rl23` **K**: Preserves top-down reading along the column separately from right-to-left column order.
70. `nhe/ui_vertical_lr23` **K**: Preserves top-down reading and correctly reverses only column direction.
71. `nhe/ui_vertical_letters23` **K**: Labels the behaviour of letters in vertically running text rather than document alignment.
72. `nhe/ui_vertical_mixed23` **K**: Automatic mode keeps CJK in its existing orientation and turns other words sideways.
73. `nhe/ui_vertical_sideways23` **H**: “Stays the same” is less specific than keeping letters joined within each word; sharpen the shaping instruction.
74. `nhe/ui_vertical_upright23` **K**: Names non-rotation and individual character treatment, distinguishing this from sideways words.
75. `nhe/ui_vertical_hint23` **K**: New columns, Mongolian joining, combining marks and emoji grouping survive without assuming a code point is a whole character.
76. `nhe/ui_help23` **H**: Long help uses control paraphrases such as Navigate that need exact caption alignment; verify the image credits route against pinned labels.
77. `nhe/ui_add_up_to_20_images_with_android_s` **H**: Align the long-press/drop instructions and the Unplace effect terminology with the actual controls; avoid implying deletion of inputs.
78. `nhe/ui_heic_avif_codec_licences` **K**: Both HEIC and AVIF remain part of the same codec-licence heading.
79. `nhe/colour20_custom_selected_slot` **H**: The first phrase can be read as colours you're placing; make it explicitly the saved custom-colours section.
80. `nhe/colour20_stored_slot` **K**: Both placeholders survive and the quoted Replace action is distinct from tap to use.
81. `nhe/colour20_empty_slot` **K**: Identifies an empty numbered slot and the tap as choosing a save destination rather than immediately overwriting.
82. `nhe/colour20_save_slot` **K**: Pinned save verb and numbered destination match the empty-slot flow.
83. `nhe/colour20_replace_slot` **K**: Replacement targets the identified slot and is consistent with the adjacent Replace action.
84. `nhe/colour20_saved_slot` **K**: Completed save is clear, including colour and destination slot.
85. `nhe/gallery_image_component_unavailable` **H**: Polihui can imply the component is missing or lost rather than temporarily unavailable; preserve the broader failure condition.
86. `nhe/ui_lossless_format` **K**: The explicit unchanged-pixels wording expresses lossless output for the formatted codec name.
87. `nhe/ui_image_codec_licences` **K**: Image codec licences are clear and narrower than general image rights.
88. `nhe/formats22_base64_label` **K**: Identifies Base64 text representation rather than calling the draft a Base64 image viewer.
89. `nhe/formats22_ascii_label` **K**: Image made of ASCII writing distinguishes the export from plain Base64 text.
90. `nhe/formats22_tiff_compression` **K**: Retains smaller byte size, unchanged pixels and the precise Deflate method.
91. `nhe/formats22_tiff_description` **K**: Keeps the single RGB page, reversible compression choice and unchanged pixels.
92. `nhe/formats22_dib_description` **K**: Keeps 24-bit Windows DIB and the conditional BMP-header alternative.
93. `nhe/formats22_dib_size_limit` **K**: The byte ceiling belongs to DIB; it is not a pixel-dimension cap.
94. `nhe/formats22_page_description` **K**: Both metadata fields and page count follow source order; choose one page to edit as an image.
95. `nhe/formats22_page_number` **K**: Clearly identifies a page number, not total pages or file size.
96. `nhe/formats22_previous_page` **K**: Previous-page caption aligns with the following next-page counterpart.
97. `nhe/formats22_next_page` **K**: Next-page caption keeps motion in the correct direction.
98. `nhe/formats22_open_page` **K**: Open refers to the selected page, not a separate file picker.
99. `nhe/formats22_page_preview` **K**: Uses the established preview expression and keeps the selected-page qualification.
100. `nhe/formats22_page_range` **K**: Inclusive limits and dynamic maximum are preserved, with a clear page-number entry instruction.

## Batch 10: Eastern Huasteca Nahuatl and Central Huasteca Nahuatl

Reviewed 100 previously unreviewed wording candidates: 83 `nhe` (Eastern Huasteca Nahuatl) and 17 `nch` (Central Huasteca Nahuatl). Decision codes: K = keep exact candidate for separate integration; H = hold for wording revision or stronger supporting evidence. This pass does not modify Android resources. Batch: **65 keep, 35 hold**. Cumulative: **1,000 reviewed, 665 keep, 335 hold**.

1. `nhe/formats22_loading_page` **H**: The progress indicator says the app makes something you will see first, without clearly naming an in-progress preview consistent with the neighboring captions.
2. `nhe/formats22_page_dimensions` **K**: Correct current page, total pages, and width-by-height order with all four typed placeholders.
3. `nhe/formats22_preview_unavailable` **K**: Concise “cannot see it beforehand” message with the diagnostic detail retained.
4. `nhe/formats22_preview_memory` **K**: Keeps the preview RAM failure separate from the smaller dimensions offered on opening and retains the condition.
5. `nhe/formats22_pdf_invalid` **K**: Distinguishes a possibly damaged PDF from features the current Android version cannot handle.
6. `nhe/formats22_pdf_encrypted` **K**: Retains both password and unsupported encryption, and instructs saving an unprotected copy before import.
7. `nhe/formats22_pdf_file_size` **K**: Requires readable content and retains 512 MiB as an inclusive maximum, not a pixel limit.
8. `nhe/formats22_pdf_page_count` **K**: Keeps one page as the inclusive floor and the dynamic upper page count.
9. `nhe/formats22_pdf_page_index` **K**: Despite the provisional provenance, explicitly says the selected page is no longer usable and asks for a page from this document.
10. `nhe/formats22_pdf_dimensions` **K**: Preserves both invalid and too large dimensions as alternative import failures.
11. `nhe/formats22_pdf_crop` **K**: The rectangle must have dimensions and be inside the selected page; nothing implies resizing the PDF.
12. `nhe/formats22_pdf_memory` **K**: Rendering the PDF is described as needing more RAM than is available for images.
13. `nhe/formats22_base64_description` **K**: Preserves lossless PNG, the data URI prefix, reopening to recover the image, and the size overhead.
14. `nhe/formats22_ascii_columns` **K**: Width is expressed in written characters, not in image pixels.
15. `nhe/formats22_ascii_invert` **H**: The adjectives can read as clean and dark; use less ambiguous bright/dark terms and ensure the two categories exchange roles.
16. `nhe/formats22_text_not_image` **K**: Says the Base64 lacks an image the app can open, without declaring all Base64 invalid.
17. `nhe/gallery_description` **H**: The text never names the Copy credit control and alternates interpretations of the credit route; align button captions and preserve source, licence and attribution distinctions.
18. `nhe/gallery_copy_credit` **H**: The caption narrows credit to a creator’s writing; the action copies source and licensing information as well.
19. `nhe/gallery_edit_credits` **H**: Names only who created it; editing credits also includes source and changes. Use the same broader term as Copy credit and Image credits.
20. `nhe/gallery_credit_copied` **H**: The first-person completion and creator-only phrase conflict with the app’s broader copied attribution text.
21. `nhe/gallery_credit_edit_hint` **H**: “Remove those that are not visible” is underspecified; explicitly remove source entries not used in the final image, not parts of the image.
22. `nhe/gallery_credit_title` **K**: Labels artwork and its title value without conflating it with publisher or source.
23. `nhe/gallery_credit_publisher` **K**: Retains the app’s Catrobat project attribution as the publisher.
24. `nhe/gallery_credit_source` **K**: Identifies where the image was obtained and preserves the value slot.
25. `nhe/gallery_credit_gallery` **K**: Keeps the separate gallery field and its placeholder.
26. `nhe/gallery_credit_licence` **K**: Keeps Catrobat as creator of original artwork, the exact licence ID, and its dynamic value.
27. `nhe/gallery_credit_saved` **H**: Preserving the app subject is fine, but the phrase still limits the saved text to the creator rather than all credits.
28. `nhe/formats22_ico_size` **K**: Clearly identifies the icon size setting, not canvas size.
29. `nhe/formats22_ico_description` **H**: PNG remains, but the text only says “with PNG”; explicitly retain PNG compression and avoid making the visible-through square sound like the image is transparent.
30. `nhe/formats22_ico_decode_budget` **K**: The RAM shortfall applies to decoding the icon, not saving it or to a format size cap.
31. `nhe/formats22_ico_dimensions_error` **H**: The phrase addresses “what is inside ICO” generally; it omits the corresponding internal directory item, which matters when multiple entries exist.
32. `nhe/formats22_ico_invalid_size` **K**: Every supported numerical size and the pixel unit survive in order.
33. `nhe/save20_dither` **H**: The phrase suggests bringing colours close with differently coloured pixels but does not clearly denote dithering; align the setting caption and its Save GIF help.
34. `nhe/save20_bmp_description` **K**: Keeps 24-bit RGB, uncompressed storage, exact colours and larger files.
35. `nhe/save20_bmp_size_limit` **K**: Identifies the BMP file-byte limit, not its width or height.
36. `nhe/save20_gif_size_limit` **K**: Clearly caps each GIF side at 65,535 pixels.
37. `nhe/save20_unsupported_tagged_colour` **K**: Keeps unsupported colour profile and directs the user to a colour-managed editor to make a PNG in sRGB before importing.
38. `nhe/ui_pencil_crisp_adjustable_strokes` **H**: “Looks good” loses crisp/non-antialiased edges, and the tool caption should match the pinned Lapiz label.
39. `nhe/ui_cursor_help31` **H**: The physical tap/drag/tap sequence survives, but Draw and Drawing currently share Xicpa and the draft does not identify the second exact route label.
40. `nhe/ui_cursor_marker_help31` **K**: Distinguishes a larger cursor marker from the unchanged brush stroke width.
41. `nhe/ui_gimp_translations31` **K**: Separates the attribution for translations from licences rather than treating them as image credits.
42. `nhe/ui_normalize_width_intro` **H**: The aspect ratio survives, but the closing clause describes the crop result, not the saved crop settings; name both unchanged settings and originals.
43. `nhe/ui_normalize_height_intro` **H**: Same crop-settings ambiguity as the width counterpart; keep the equal-height and per-image ratio statements.
44. `nhe/ui_normalize_width_info` **K**: Retains width for each image, differing heights, maximum current width for the percentage reference, and layout reflow.
45. `nhe/ui_normalize_height_info` **K**: Retains height for each image, differing widths, maximum current height for percentage and layout reflow.
46. `nhe/ui_normalize_width_input_percent` **K**: The input clearly asks for shared width as a percentage of the typed pixel reference.
47. `nhe/ui_normalize_height_input_percent` **K**: The vertical counterpart consistently asks for shared height using the same typed reference.
48. `nhe/ui_pixel_grid_help33` **H**: 800% is retained but the condition describes a large-looking image, not the active zoom value; name zoom explicitly.
49. `nhe/ui_search_english34` **K**: Short instruction distinguishes the two supported search languages.
50. `nhe/ui_gallery_back34` **K**: Clear return/navigation imperative; does not imply canceling an edit.
51. `nhe/ui_irasutoya_help34` **H**: The 21-item threshold is present, but commercial design is narrower than the phrase used for selling, and the exact Image credits route needs alignment before publishing legal wording.
52. `nhe/ui_openclipart_help34` **H**: CC0, larger PNG and tap direction are retained; hold until the final quoted Image credits destination matches the actual caption.
53. `nhe/ui_gallery_unsupported34` **K**: Says the image is not part of the selected source; does not imply service or network failure.
54. `nhe/ui_open_artwork34` **K**: Clear page-first sequence; the quoted action matches the existing gallery_use_image caption exactly.
55. `nhe/ui_creator_on_source34` **K**: Directs the user to the source page to identify who supplied the artwork, not to a generic external search.
56. `nhe/ui_irasutoya_credit34` **K**: Keeps creator-held rights, conditions of use and explicit non-CC status separate.
57. `nhe/legacy_credits_title` **K**: Says the app saved the attribution earlier, distinguishing it from credits newly associated with this image.
58. `nhe/legacy_credits_hint` **H**: The instruction to put “its writing here” is less precise than adding that source’s credit to this specific image; align vocabulary with the legacy action captions.
59. `nhe/legacy_credits_add` **H**: The button says add the selected thing to the image; name the credit so the user does not expect the source image itself to be inserted.
60. `nhe/legacy_credits_save_text` **H**: The button says save “the selected thing” as text; name attribution explicitly and distinguish exporting the text from saving the source image.
61. `nhe/legacy_credits_existing` **K**: Correctly says the existing credit corresponds to that source and its earlier wording was left unchanged.
62. `nhe/legacy_credits_added` **H**: The result reports only creator information despite the source credit containing broader attribution; match the corrected action and other credit confirmations.
63. `nhe/commons_import_svg_changes` **K**: Translates only the original-size description; preserves API names, Boolean literal, colour value and SVG-to-PNG transformation.
64. `nhe/commons_import_raster_changes` **K**: Preserves exact background token and gives a descriptive explanation of alpha compositing instead of implying shape transparency survives.
65. `nhe/commons_credit_copy_failed` **H**: First person (“I could not copy”) is inconsistent with app notifications, and the wording still limits the credit to creator information.
66. `nhe/commons_credit_copy_failed_reason` **H**: Use the broader credit term and neutral app phrasing from the corrected copy-failure counterpart; retain the reason slot.
67. `nhe/commons_credit_copy_out_of_memory` **H**: Memory cause is clear, but this still limits the affected text to a creator’s writing; align all three credit-copy errors.
68. `nhe/commons_metadata_http_error` **K**: Keeps HTTP exact and leaves the dynamic status slot intact for a file-metadata message.
69. `nhe/commons_metadata_response_too_large` **K**: Distinguishes Commons response byte size from the requested image’s pixel dimensions.
70. `nhe/commons_metadata_query_failed` **K**: Reports failure to retrieve file information rather than claiming the file is corrupt or missing.
71. `nhe/ui_assembly_position_help` **K**: Retains top-left reference, integer coordinates from zero, no movement of other images, stacking order, expansion, and unchanged size/crop.
72. `nhe/ui_assembly_position_nonnegative` **K**: All numbers must be integral and within inclusive 0–2147483647 bounds.
73. `nhe/gallery_external_link_no_handler` **K**: Names Android and the absence of an app that can open this link; no browser-specific claim.
74. `nhe/commons_metadata_not_file_page` **K**: Identifies the expected Commons file-page type, not any page on that site.
75. `nhe/commons_metadata_ambiguous_file` **K**: Says the returned file information fails to identify which file; ambiguity rather than a broken or missing file.
76. `nhe/commons_metadata_unavailable` **H**: The phrase says there is no file information, which can assert nonexistence rather than information not being available now.
77. `nhe/commons_metadata_original_mismatch` **H**: Attribution is reduced to the creator’s wording; the matcher also compares source information to the selected original.
78. `nhe/commons_metadata_invalid_page` **H**: Same creator-only issue; identify an invalid Commons attribution page without implying no artist is named.
79. `nhe/commons_metadata_field_too_large` **H**: Says a piece of creator text is long; identify an attribution field exceeding its text limit, not a general length judgment.
80. `nhe/commons_metadata_cache_failed` **H**: The app inability to save is clear, but the object is the Commons attribution record, not just creator text.
81. `nhe/commons_download_original_mismatch` **H**: The wording says it leads somewhere else but drops that the redirect goes to a different original file; distinguish from a generic link redirect.
82. `nhe/commons_svg_png_encode_failed` **K**: Clearly reports inability to make the blank map into PNG; no suggestion that Commons refused the download.
83. `nhe/ui_the_arrow_on_the_left_directly_below_the` **H**: Keep the complete guide as draft: quoted control paths must match exact current captions, and the guide should not equate transparency to cleanliness or omit controls such as the width/height unit selectors’ actual labels.
84. `nch/commons_blank_maps` **H**: “Maps without writing” narrows blank maps to unlabeled maps; verify the category’s geography/base-map meaning before using it as the picker caption.
85. `nch/commons_check_file_licence` **K**: Retains the separate per-file creator, licence and required attribution checks and the possibility edits count as adaptation.
86. `nch/ui_about_copyright` **K**: A clear short about-app label with a distinct copyright component.
87. `nch/ui_about_copyright_licence` **K**: Retains both copyright and licence rather than collapsing either into app information.
88. `nch/ui_add_images` **K**: Concise Add images instruction; ixkopinali aligns with the locale’s existing image vocabulary.
89. `nch/ui_add_images_first` **K**: Uses the same action as Add images and keeps the prerequisite marker.
90. `nch/ui_add_images_then_drag_a_thumbnail_here` **K**: Keeps order, the drag action, smaller thumbnail, and the destination here.
91. `nch/ui_add_to_custom_colours` **H**: Describes the place where selected colours are saved but can be mistaken for recently chosen colours; name the editable custom palette consistently with its other actions.
92. `nch/ui_an_assembly_can_contain_up_to_20_images` **K**: Keeps the assembly capacity and explicitly requires removing one image before another can be added.
93. `nch/ui_an_assembly_can_contain_up_to_20_images_86d995` **K**: Short limit copy matches the same 20-or-fewer condition without introducing a remove action.
94. `nch/ui_an_image_cannot_attach_to_itself_or_one` **K**: Retains both attachment exclusions: itself and an image already attached to it.
95. `nch/ui_an_paint_assembly_image` **K**: Uses the established assembly-workspace term and identifies the image generated there, not the workspace itself.
96. `nch/ui_an_paint_image_assembly` **K**: Uses the same established assembly-workspace expression as the picker and keeps the exact app name.
97. `nch/ui_an_paint_image_assembly_20_images_placed` **K**: Preserves the title, inserted line break and separate loaded-versus-placed placeholder counts.
98. `nch/ui_apply_to_all` **K**: Direct imperative with the target “all,” not a select-all command.
99. `nch/ui_apply_to_these_images` **K**: Matches the all-images counterpart while constraining the action to these images.
100. `nch/ui_assembly_decoded_output_estimated_editing_render_memory_at` **H**: The second field is “image the app reads,” not decoded output memory; the third needs to distinguish estimated editing/render allocation at original size.

## Batch 11: Central Huasteca Nahuatl

Reviewed 100 previously unreviewed `nch` candidates. K = keep exact candidate for separate integration; H = hold for a wording fix or quality check. Batch: **69 keep, 31 hold**. Cumulative **1,100 reviewed, 734 keep, 366 hold**. Merge checkpoint for the next cleared cohort is 1,500 reviewed; this batch does not change Android resources.

1. `nch/ui_assembly_output_size` **K**: Names the output image dimensions, not the size of the workspace or assembly file.
2. `nch/ui_assembly_png` **K**: Descriptive filename keeps its exact PNG extension and identifies assembled imagery.
3. `nch/ui_batch_crop` **H**: Could mean keep one identical part in every image; distinguish a crop applied to multiple images from using identical selected pixels.
4. `nch/ui_batch_crop_images` **H**: Use the same unambiguous batch-crop wording as the paired action rather than suggesting images keep one identical portion.
5. `nch/ui_by_pixels_hold_and_drag_to_place` **K**: Keeps four typed slots, dimension order, and both the hold and drag gestures for placement.
6. `nch/ui_catrobat_online_gallery_artwork_by_its_credited_creators` **K**: Retains the online gallery identity and separately named creators.
7. `nch/ui_catrobat_s_own_artwork_uses_cc_by_sa` **H**: Licence and source link are present, but the destination denotes only the person who made the image; match the complete credits caption and explicitly retain any separate attribution.
8. `nch/ui_catrobat_sticker_gallery` **K**: Names the sticker gallery and retains the ellipsis for its next screen.
9. `nch/ui_common_in` **K**: The two placeholders still denote the shared dimension and its chosen units.
10. `nch/ui_common_in_pixels` **K**: Pixel-unit counterpart uses the same shared-value wording as the generic-units caption.
11. `nch/ui_copper` **K**: Unambiguous standard colour/material loan, short enough for a preset.
12. `nch/ui_copy_an_area_or_use_file_insert_image` **H**: Says make an image from part of something instead of Copy. Also verify that all three route labels match their controls.
13. `nch/ui_copy_decoded_image_at_this_size_estimated_loading` **H**: The decoded-image row speaks of an image the app reads, not the footprint at that size; distinguish bytes from the separate estimated loading/editing RAM row.
14. `nch/ui_corners_and_edges_resize_round_handle_rotates` **K**: Corner and side handles resize; the round handle rotates, with both physical drag gestures retained.
15. `nch/ui_could_not_create_the_assembly` **K**: The app could not create the image-assembly workspace, with the diagnostic field still visible.
16. `nch/ui_could_not_decode_the_cropped_region_of` **K**: Reads as inability to decode the retained region and preserves the source-image identifying slot.
17. `nch/ui_could_not_export_source_code` **K**: Saving the specified source code to another destination conveys export, rather than failing to compile.
18. `nch/ui_could_not_load_gallery_image` **K**: Open/load failure still points to a gallery image rather than an unavailable gallery, with detail slot.
19. `nch/ui_create_output` **K**: Names creating the output image, not saving over a source file.
20. `nch/ui_credits_terms` **H**: The first half names only who made the project; credits must also cover contributions, sources and notices. The terms half should not imply only steps to run it.
21. `nch/ui_cropped_thumbnail` **K**: Identifies a thumbnail of the cropped image and retains the association through its slot.
22. `nch/ui_current_safe_budget_2f_mp` **K**: Preserves an up-to current safe limit and the two-decimal megapixel token.
23. `nch/ui_current_safe_editing_budget_s_up_to_2f` **K**: Clearly distinguishes current editing RAM, its MP estimate and the excluded additional decode memory.
24. `nch/ui_cursive` **K**: Concise established typography loan for the cursive choice.
25. `nch/ui_custom_colour` **H**: Says colour previously chosen rather than an explicit custom-colour slot; align it with the custom palette and its Add/Replace flow.
26. `nch/ui_custom_colours_hold_a_swatch_to_replace_it` **H**: Hold-to-replace is right, but saved custom swatches should not be confused with previously selected colours.
27. `nch/ui_disable_cursor_drawing` **K**: Matches the pinned cursor-drawing disable caption and preserves the scope of the toggle.
28. `nch/ui_downloading_image` **H**: Taking an image could mean selection or capture; name an in-progress download.
29. `nch/ui_drag_a_line_then_drag_twice_to_set` **H**: Two separate curves are implied, not two bends of a single curve. The early Finish action is present but needs exact caption alignment.
30. `nch/ui_drag_a_selection_drag_inside_to_move_square` **K**: Retains draw/drag selection, interior movement, square resize handles, round rotation handle and aspect locking.
31. `nch/ui_drag_across_the_ellipse_s_bounding_box` **K**: Explains the diagonal as a drag from one corner of the ellipse’s enclosing rectangle to the opposite corner.
32. `nch/ui_drag_between_opposite_corners_choose_outline_or_fill` **K**: Retains opposite-corner gesture and the separate below-control choice between outline and fill.
33. `nch/ui_drag_between_opposite_corners_to_draw_a_five` **K**: Five points, opposite corners and outline versus filled interior all survive.
34. `nch/ui_drag_between_opposite_corners_to_draw_a_heart` **K**: Correct heart gesture and optional outline versus filled interior.
35. `nch/ui_drag_from_the_start_to_the_end_of` **K**: Clear start-to-end line drag, not tapping an endpoint twice.
36. `nch/ui_drag_from_the_tail_towards_the_arrowhead_choose` **H**: Itsonco can describe the broad top or tip; distinguish the arrowhead from the tail with a term consistent with the arrow tool.
37. `nch/ui_drag_out_to_expand_in_to_trim_drag` **H**: Pinch and Fit are recognizable, but the final “colour behind” needs explicit BG terminology and matching Fit caption in the revised bounds help.
38. `nch/ui_drag_placed_images_to_move_them_hold_and` **H**: The first phrase can mean images merely loaded into the workspace. Specify already placed images to distinguish them from thumbnails.
39. `nch/ui_drag_to_erase_with_the_background_colour` **K**: Erasure is explicitly performed with the background colour, not transparency.
40. `nch/ui_drag_to_pan_without_drawing_pinch_with_two` **K**: Preserves non-drawing pan and combined two-finger zoom/pan even with a drawing tool active.
41. `nch/ui_draw_a_crisp_one_pixel_line` **H**: The line is described as clear, not crisp-edged; distinguish pencil from antialiased drawing while preserving the 1–100 range.
42. `nch/ui_draw_around_an_area_drag_inside_to_move` **H**: Gesture details survive, but confirm that the quoted action matches the actual Commit selection caption instead of sounding like inserting a separate image.
43. `nch/ui_draw_soft_watercolor_strokes_strength_controls_how_strongly` **K**: Keeps the soft water-and-colour stroke and strength controlling how the colour mixes into the canvas.
44. `nch/ui_draw_with_the_selected_brush_tip_and_size` **K**: Preserves both selected brush-tip shape and selected size.
45. `nch/ui_drop_at_a_highlighted_edge_right_top_aligned` **H**: Clarify the two attachment edges and that top/left are alignment targets, not two independent movement directions.
46. `nch/ui_each_px_px_percent_is_relative_to_the` **K**: Preserves all seven slots, relative percentage base and reflow of placed images, with line structure intact.
47. `nch/ui_edit_in_paint` **K**: Names the action and Paint destination; no confusion with saving the assembly.
48. `nch/ui_enable_android_s_files_or_documents_app_then` **K**: Specifies the Android app to enable and directs a retry rather than asking the user to find a file.
49. `nch/ui_estimated_memory_current_working_budget` **K**: Keeps estimated RAM and present working allowance as different numbers with both line breaks.
50. `nch/ui_estimates_include_the_current_canvas_and_clipboard_sampled` **K**: Keeps sampled decode, current canvas, clipboard, editing buffers, possible variation, reduced-copy detail loss, opaque background and unchanged original.
51. `nch/ui_export_this_version_s_source_code` **K**: Names the current version, source code and export to another destination; retains ellipsis.
52. `nch/ui_filename_a_z` **K**: Uses the pinned filename term and ascending A–Z order.
53. `nch/ui_filename_z_a` **K**: Uses the same filename term and descending Z–A order.
54. `nch/ui_fill_text_box_with_bg_colour` **K**: Clearly fills the text box with the behind/background colour, not the lettering itself.
55. `nch/ui_fits_the_current_budget` **K**: Says the operation can use the currently available RAM, not that it necessarily uses all of it.
56. `nch/ui_font_licences` **K**: The licence object is the appearance/form of letters, distinguishing fonts from image and codec licences.
57. `nch/ui_gallery_artwork_catrobat_and_its_credited_creators_cc` **K**: Retains identification of creators, the default licence and source-specific exceptions, including creator credit and description of modifications when sharing.
58. `nch/ui_gallery_image` **K**: Names an image from the gallery without implying a download or insertion has already occurred.
59. `nch/ui_give_all_images_the_same_each_image_keeps` **H**: The final crop clause can be read as the selected material rather than crop settings; preserve both original files and each saved crop setting unchanged.
60. `nch/ui_gold` **K**: Concise standard colour/material loan that matches the preset meaning.
61. `nch/ui_hide_pixel_grid_800` **K**: Hides the pixel grid, preserving the 800%-and-up shorthand.
62. `nch/ui_hold_a_thumbnail_and_drag_it_here_or` **H**: The second “tap workspace” is left implicit; make both taps explicit and distinguish the tap alternative from hold-and-drag.
63. `nch/ui_hold_or_drag_to_spray_colour` **K**: Retains both hold and drag for colour application via the established airbrush description.
64. `nch/ui_honeycomb` **K**: Concise equivalent for the honeycomb palette option.
65. `nch/ui_honeycomb_colour_06x` **K**: Honeycomb colour name and exact uppercase, zero-padded hexadecimal token retained.
66. `nch/ui_honeycomb_colour_swatches_with_a_greyscale_row` **K**: Describes individual honeycomb swatches and a separate grey-scale row.
67. `nch/ui_hue_and_saturation_spectrum_lightness_slider_on_the` **K**: Keeps hue/saturation and the lightness adjustment on the right; does not confuse with HSV value.
68. `nch/ui_hue_and_saturation_wheel_value_slider_on_the` **K**: Keeps the wheel and numeric V adjustment on the right, distinguishing it from HSL lightness.
69. `nch/ui_icon_licences` **K**: Correct plural licences for icons, distinct from the visual icons themselves.
70. `nch/ui_icon_licences_kde_breeze` **K**: Preserves the exact KDE Breeze name and the same icon-licence terminology.
71. `nch/ui_icons_artwork` **K**: Both icons and artwork remain listed as separate parts of this credit section.
72. `nch/ui_icons_fonts_artwork_credits` **H**: Only asks who made the items; credit may include source, ownership and related notices. Keep the heading broad and align with the credits/terms labels.
73. `nch/ui_image_assembly_workspace_drag_placed_images_or_drop` **K**: Right/bottom targets, snap effect, separate thumbnail/placed drag, pinch zoom and empty-space panning are all expressed.
74. `nch/ui_image_credits` **H**: “Who made the image” omits source and licence; revise the heading alongside the related routes pointing to it.
75. `nch/ui_image_placed_drag_it_to_move_or_hold` **H**: “The image is already there” fails to distinguish placement on the canvas from having loaded a thumbnail; align with both placement status captions.
76. `nch/ui_image_shown_in_crop_preview` **K**: Identifies the image visible in the before-commit crop view.
77. `nch/ui_image_thumbnails_and_filenames_scroll_horizontally_for_more` **K**: Clear thumbnail/file-name description and horizontal-scroll directions for accessing more.
78. `nch/ui_insert_gallery_image` **K**: Asks whether to insert this gallery image, without suggesting it will replace the entire canvas.
79. `nch/ui_invalid_image_attachments` **K**: Conveys the arrangement of image attachments is not valid, not an image decode failure.
80. `nch/ui_largest` **K**: Clear superlative for selecting the largest candidate.
81. `nch/ui_lossless_jpeg_xl` **H**: “Saved everything visible” is not expressly bit-/pixel-preserving; use the established lossless formulation.
82. `nch/ui_magnified_preview` **H**: The imperative “look beforehand in larger size” is recognizable but reads as an instruction, not the magnified preview setting.
83. `nch/ui_magnified_preview_ea9209` **H**: Keep this plain variant aligned with the corrected magnified-preview noun phrase.
84. `nch/ui_modified_newest_first` **K**: Orders by most recently modified, not by capture or creation date.
85. `nch/ui_modified_oldest_first` **K**: Orders by earliest modification with wording parallel to the newest-first option.
86. `nch/ui_monospace` **K**: A readable explanation of equal-width glyphs captures the monospace choice.
87. `nch/ui_no_attachment_fits_within_the_current_coordinate_range` **K**: Keeps current coordinate-range constraint and recommends smaller images rather than retrying blindly.
88. `nch/ui_no_gallery_images_have_been_inserted` **H**: Implies that no creator text is available; the source can also mean no source/licensing credit text regardless of creator.
89. `nch/ui_not_enough_memory_to_inspect_the_gallery_image` **K**: Specifies RAM and the gallery image inspection action, not save, import or network failure.
90. `nch/ui_not_placed` **H**: “Not yet there” could mean not loaded; use a placement-specific negative state.
91. `nch/ui_open_source_credits_and_notices` **H**: Says who created software and “this writing”; it does not reliably distinguish open-source attribution from required notices.
92. `nch/ui_original_decoded_image_rgba_4_bytes_pixel_estimated` **H**: Formula, three values and no-resize qualifier survive, but the second row should name decoded-image memory rather than the decoded image itself.
93. `nch/ui_other_terms` **H**: “Other things you must do” can read as setup steps; make clear these are additional terms of use.
94. `nch/ui_pale_violet` **H**: “Chipahuac” may suggest clean rather than pale/light; align the colour modifier with the other pastel names.
95. `nch/ui_pencil_keeps_crisp_one_pixel_strokes_cursor_drawing` **K**: Names exact Lápiz label, crisp edges, and the fact that the property applies at any selected width.
96. `nch/ui_percent_of_pixels` **K**: Percentage wording preserves the dynamic pixel reference rather than a literal number.
97. `nch/ui_pinch_to_zoom_drag_to_pan` **K**: Distinguishes two-finger zoom from dragging the view.
98. `nch/ui_place_at_least_one_image_in_the_workspace` **K**: Explicit first-step minimum of one placed image in the workspace.
99. `nch/ui_placed` **H**: “It is already there” is too generic for the placed status; pair the revision with its negative form to distinguish from loaded.
100. `nch/ui_px_drag_an_image_to_move_hold_a` **K**: Exact dimension order/unit plus the separate image move and thumbnail-hold actions remain intact.

## Batch 12: Central Huasteca Nahuatl

Reviewed 100 previously unreviewed `nch` candidates. K = keep exact candidate for separate integration; H = hold for a wording fix or quality check. Batch: **76 keep, 24 hold**. Cumulative **1,200 reviewed, 810 keep, 390 hold**. This batch does not change Android resources.

1. `nch/ui_quality` **K**: Quality remains an explicit percentage; the concise loan matches the existing setting context.
2. `nch/ui_rendering_images` **H**: “Images the app made” suggests creation rather than processing progress; preserve both counters for the revision.
3. `nch/ui_restore_original_sizes` **K**: Returns every image to its original dimensions rather than reverting the whole workspace.
4. `nch/ui_right_arrow_expand` **K**: Right arrow and opening the controls accurately describe expansion, not moving an image rightward.
5. `nch/ui_same` **K**: Keeps the generic shared-dimension slot.
6. `nch/ui_same_height` **K**: Names the shared height distinctly from width.
7. `nch/ui_same_width` **K**: Names shared width and matches the height counterpart.
8. `nch/ui_sans_condensed` **K**: Describes narrower Sans glyphs, independent of font weight.
9. `nch/ui_sans_light` **K**: The thinner-than-usual phrasing conveys the light weight.
10. `nch/ui_sans_medium` **K**: Intermediate weight distinguishes medium from light and thin.
11. `nch/ui_sans_thin` **K**: Especially thin weight remains distinguishable from light.
12. `nch/ui_set_radius_px_then_drag_between_opposite_corners` **K**: Explains the corner radius in pixels, the diagonal gesture, and the per-rectangle half-short-side limit.
13. `nch/ui_show_pixel_grid_800` **K**: Retains show action, pixel grid and threshold notation; compatible with its hide counterpart.
14. `nch/ui_shows_the_whole_assembly_image_and_output_sizes` **K**: All of the assembly becomes visible without changing source or output sizes.
15. `nch/ui_sans_serif` **K**: Explains absence of serifs at stroke ends instead of a specific font family.
16. `nch/ui_serif` **K**: Stroke-end marks distinguish the serif family from Sans serif.
17. `nch/ui_silver` **K**: Clear standard colour/material loan for the preset.
18. `nch/ui_smallest` **K**: Clear superlative for the smallest option.
19. `nch/ui_smooth_freehand_strokes` **H**: “Look good” is not specific to smoothing freehand motion, and fails to distinguish the anti-alias control.
20. `nch/ui_smooth_pixel_edges_anti_aliasing` **H**: The technical label survives but “look good” does not describe smoothing jagged pixel edges.
21. `nch/ui_some_previews_could_not_be_decoded_you_can` **K**: Preserves the preview decode failure and offers removing affected images or trying Save.
22. `nch/ui_sort_images_by_filename_or_modification_time` **K**: Identifies the two separate filename and modification-time sort criteria.
23. `nch/ui_sort_tray` **K**: Names sorting the thumbnail tray, not sorting a list of source folders.
24. `nch/ui_source_code_exported_including_build_scripts_and_licence` **K**: Retains source export, build scripts and licensing notices.
25. `nch/ui_spectrum` **K**: Clearly names the colour spectrum, not the hue-wheel alternative.
26. `nch/ui_strikethrough` **K**: Explicitly places a line through the middle of text.
27. `nch/ui_tap_a_pixel` **K**: Clear single-finger contact and release on one pixel.
28. `nch/ui_tap_an_enclosed_area_adjust_tolerance_for_similar` **K**: Keeps the enclosed-region tap and adjustment to admit more or fewer similar colours.
29. `nch/ui_tap_an_image_thumbnail_first` **K**: Correctly asks to tap the thumbnail before the next action.
30. `nch/ui_tap_the_canvas_to_place_text_and_choose` **K**: Tap canvas, place text, choose its appearance/font and size remain in the proper order.
31. `nch/ui_tap_the_image_to_sample_the_foreground_colour` **K**: Samples colour from the image to the foreground.
32. `nch/ui_tap_vertices_then_double_tap_the_last_vertex` **K**: Double-tap last vertex, Finish alternative, and turning off closure for joined open segments all survive.
33. `nch/ui_that_arrangement_overlaps_another_image_use_a_different` **H**: The remedy can imply removing the attached images themselves; distinguish unplacing from deletion or removing source files.
34. `nch/ui_the_assembly_exceeds_android_s_coordinate_range` **K**: The assembly exceeds the allowable Android coordinate range, not necessarily device RAM.
35. `nch/ui_the_assembly_needs_about_choose_a_smaller_output` **K**: Preserves estimated requirement and recommends reducing output dimensions.
36. `nch/ui_the_assembly_output_is_unavailable_reopen_image_assembly` **H**: Says no image exists rather than output is unavailable; align the action with the exact Image assembly caption.
37. `nch/ui_the_attachment_image_is_missing` **K**: Reports a missing attached image, not permission to detach it.
38. `nch/ui_the_attachment_image_is_not_placed` **H**: “Not there yet” can describe an unloaded item. Reuse the explicit placed/unplaced terminology from the paired status.
39. `nch/ui_the_first_image_starts_at_the_top_left` **K**: Correct first-image origin at the upper left.
40. `nch/ui_the_gallery_download_is_too_large` **K**: Reports excessive size of the gallery download rather than the source gallery itself.
41. `nch/ui_the_gallery_image_is_unavailable` **H**: Says there is no image; temporary unavailability must not imply nonexistence.
42. `nch/ui_the_gallery_redirected_outside_its_supported_hosts` **K**: Distinguishes a redirect to an unsupported image URL from an unsupported file format.
43. `nch/ui_the_image_could_not_be_downloaded` **H**: “Could not take the image” could mean choose, capture or import; use the same explicit download term as progress.
44. `nch/ui_the_images_cannot_fit_within_android_s_coordinate` **K**: Retains coordinate constraint and advises smaller image sizes.
45. `nch/ui_the_normalized_image_dimensions_are_outside_android_s` **K**: Names normalized width and height outside Android’s limit.
46. `nch/ui_the_online_gallery_could_not_be_loaded_check` **K**: Keeps gallery load failure, connection check and retry as separate instructions.
47. `nch/ui_third_party_notices` **H**: “Writing from others” does not give the legal-notice meaning or distinguish it from general third-party content.
48. `nch/ui_this_image_is_outside_the_supported_catrobat_gallery` **K**: Preserves the Catrobat gallery allowlist context rather than implying every URL outside Catrobat is broken.
49. `nch/ui_time_unavailable` **H**: “There is no hour” can imply clock time does not exist. Identify unavailable time metadata in the sort context.
50. `nch/ui_too_many_gallery_redirects` **K**: Clearly reports the gallery repeatedly redirected to other URLs rather than claiming it redirected outside the site.
51. `nch/ui_tool_option` **K**: A setting the user can change for this tool, not a switch for selecting the tool itself.
52. `nch/ui_toolbox_and_tool_options_scroll_for_more` **K**: Keeps the tools, adjustable options and scroll-for-more hint, without specifying the wrong direction.
53. `nch/ui_trim_from_the_original_edges_drag_the_handles` **K**: Measurement starts at original edges; both handles and numeric entry survive, with original files unchanged.
54. `nch/ui_trim_in_pixels` **K**: Retains the side/dimension slot and makes clear the amount removed is in pixels.
55. `nch/ui_unplace` **H**: May imply removing the image rather than removing only its placement; keep the thumbnail/source-image distinction.
56. `nch/ui_wheel` **K**: Clear colour-wheel control name consistent with surrounding hue-wheel wording.
57. `nch/ui_width_in` **K**: Explicit width and its dynamic unit in parentheses.
58. `nch/ui_widths` **K**: A bare dimension noun works as the widths heading above a range; nothing introduces a single-image constraint.
59. `nch/ui_you_can_add_more_images_select_fewer_files` **K**: Preserves the number of remaining slots and asks the user to select fewer files.
60. `nch/ui_agpl_licence` **K**: Exact standard licence identifier and proper object.
61. `nch/ui_jpeg_xl_codec_licences` **K**: The descriptive read/write term preserves JPEG XL codec licensing rather than image licences.
62. `nch/ui_gnu_agpl_licence` **K**: Retains both GNU and AGPL identifiers.
63. `nch/ui_preview_memory_error` **K**: Identifies insufficient RAM for preview and preserves the specific item slot.
64. `nch/ui_trim_in_percent` **K**: Matches the pixel trim row but correctly switches to percent.
65. `nch/ui_crop_preview_images` **H**: Both plural variants retain all slots, but “images already there” is ambiguous and the attached-image pronoun can be read as singular; specify placed images and their attachments.
66. `nch/ui_add_palette23` **H**: Palette is phrased as a place to select colours, which can be confused with the colour picker; establish consistent palette terminology.
67. `nch/ui_added_palette23` **H**: “Already there where you choose” does not state that the colour was added to the saved palette.
68. `nch/ui_replace_palette23` **H**: The replacement action is clear but “the place you choose colour is full” is easily confused with the picker; use the same palette term as Add/Edit.
69. `nch/ui_edit_palette23` **H**: Do not describe editing the picker; name the palette consistently with the corresponding Add and Remove actions.
70. `nch/ui_replace_with_active23` **K**: Replace clearly uses the currently selected colour.
71. `nch/ui_remove_palette23` **H**: “Remove from where you choose colours” is underspecified; match the palette term from the other captions.
72. `nch/ui_add_active23` **K**: Add the currently selected colour, without conflating it with a palette replacement.
73. `nch/ui_horizontal23` **K**: Describes a row lying across, distinct from the two vertical column directions.
74. `nch/ui_vertical_rl23` **K**: Correctly combines top-to-bottom progression with right-to-left column order.
75. `nch/ui_vertical_lr23` **K**: Correctly combines top-to-bottom progression with left-to-right column order.
76. `nch/ui_vertical_letters23` **K**: Makes clear that the options are about glyphs within top-to-bottom text.
77. `nch/ui_vertical_mixed23` **H**: “CJK comes out straight, words lie down” needs more distinct vertical-orientation wording and consistency with the neighboring settings.
78. `nch/ui_vertical_sideways23` **K**: Keeps sideways words as joined units rather than individually rotated letters.
79. `nch/ui_vertical_upright23` **H**: “One letter at a time” may exclude digits, punctuation and emoji; use character/glyph language consistent with the mode.
80. `nch/ui_vertical_hint23` **H**: Columns and Mongolian example survive, but the terms for combining marks and emoji sequences are vague; retain that each unit stays intact in upright mode.
81. `nch/ui_top23` **K**: Aligns relative to the top edge, not left/right within a column.
82. `nch/ui_bottom23` **K**: Correct bottom-edge counterpart with neutral wording.
83. `nch/ui_webp_codec_licences` **K**: Accurately identifies codec licences by WebP read/write support.
84. `nch/ui_heic_avif_codec_licences` **K**: The exact HEIC and AVIF names and both codec licence scopes remain.
85. `nch/colour20_custom_selected_slot` **H**: Custom colours and the selected slot each use the same selected-colour wording; distinguish the saved palette section from the slot currently selected.
86. `nch/colour20_stored_slot` **K**: Preserves slot number and colour, tap to use, and Replace as a separate save action.
87. `nch/colour20_empty_slot` **K**: Identifies an empty numbered slot and tap-to-choose-a-destination rather than tap-to-complete.
88. `nch/colour20_save_slot` **K**: Save targets the numbered slot explicitly.
89. `nch/colour20_replace_slot` **K**: Replace targets the numbered slot with the same verb as the adjacent action.
90. `nch/colour20_saved_slot` **K**: Clear completed save including the colour and destination.
91. `nch/gallery_image_component_unavailable` **H**: Says the component does not exist. Preserve its broader unavailability and make the failed import equally clear.
92. `nch/ui_lossless_format` **H**: “Everything visible” suggests perceptual equivalence, not unchanged pixels; align lossless wording with the TIFF explanation.
93. `nch/ui_image_codec_licences` **K**: The read/write description denotes image codec licences rather than general copyright.
94. `nch/formats22_base64_label` **K**: Identifies Base64 as text, not as a separate picture format.
95. `nch/formats22_ascii_label` **K**: Unambiguously says the image is made of ASCII writing.
96. `nch/formats22_tiff_compression` **H**: “Saves everything” does not establish identical pixels; align with the explicit unchanged-pixel TIFF description and keep Deflate exact.
97. `nch/formats22_tiff_description` **K**: Single RGB page, smaller file without pixel changes, and the uncompressed option are distinct.
98. `nch/formats22_dib_description` **K**: Keeps the exact Windows DIB bit depth and recommends BMP only when the receiving application needs its header.
99. `nch/formats22_dib_size_limit` **K**: Recognizable file-capacity message tied to DIB, not to width or height.
100. `nch/formats22_select_page` **K**: Clear one-page selection command, not a page-number range error.

## Batch 13: Central Huasteca Nahuatl

Reviewed 100 previously unreviewed `nch` candidates. K = keep exact candidate for separate integration; H = hold for a wording fix or quality check. Batch: **68 keep, 32 hold**. Cumulative **1,300 reviewed, 878 keep, 422 hold**. This batch does not change Android resources.

1. `nch/formats22_page_description` **K**: Both metadata values and total page count remain in order, and the selected page becomes an editable image.
2. `nch/formats22_page_number` **K**: Names the number of this page, not total pages.
3. `nch/formats22_previous_page` **K**: Clear backwards-page action paired with Next.
4. `nch/formats22_next_page` **K**: Clear forwards-page action paired with Previous.
5. `nch/formats22_open_page` **K**: Open targets the chosen page, not a new file.
6. `nch/formats22_page_preview` **H**: Reads as “look at this page beforehand,” an instruction rather than the title of its preview; align with the rest of the preview dialog.
7. `nch/formats22_page_range` **K**: Correct inclusive first page and dynamic maximum, with a number-entry instruction.
8. `nch/formats22_loading_page` **K**: Opening for a preview is clearly ongoing and both page counters are retained.
9. `nch/formats22_page_dimensions` **K**: Retains both page counters and width × height in pixels.
10. `nch/formats22_preview_unavailable` **K**: Briefly reports inability to preview and retains the reason placeholder.
11. `nch/formats22_preview_memory` **K**: Preserves insufficient preview RAM and the conditional smaller-dimension choice on opening.
12. `nch/formats22_pdf_invalid` **K**: Distinguishes potentially damaged files and features this version of Android does not support.
13. `nch/formats22_pdf_encrypted` **K**: Keeps password/encryption alternatives and the need to save an unprotected copy before opening/importing.
14. `nch/formats22_pdf_file_size` **K**: Requires content in the PDF and preserves the inclusive 512 MiB maximum.
15. `nch/formats22_pdf_page_count` **K**: Keeps the first page and typed upper bound.
16. `nch/formats22_pdf_page_index` **K**: Says the selected page is no longer usable, and asks for another from this same document.
17. `nch/formats22_pdf_dimensions` **K**: Both unusable dimensions and oversized dimensions are preserved as import failures.
18. `nch/formats22_pdf_crop` **K**: Requires a nonempty rectangular retained region entirely inside the selected page.
19. `nch/formats22_pdf_memory` **H**: The draft mentions generic available RAM rather than the separate budget for rendering image data; distinguish the two.
20. `nch/formats22_base64_description` **H**: “Stores all that is visible” does not guarantee unchanged pixels; retain the intact prefix, reopening behavior and size overhead in the revision.
21. `nch/formats22_ascii_columns` **K**: Letters and written symbols correctly distinguish columns from pixel width.
22. `nch/formats22_ascii_invert` **K**: Explicitly swaps both brightness classes in both directions, reducing ambiguity about inversion.
23. `nch/formats22_text_not_image` **K**: Restricts the failure to images the app supports, not to all Base64 text.
24. `nch/gallery_description` **H**: Button/route names narrow the broad credit to the creator alone, even though the paragraph lists other fields; update the linked captions together before clearing.
25. `nch/gallery_copy_credit` **H**: Names copying information about who created the art only; preserve title, publisher, source and licence scope in the action label.
26. `nch/gallery_edit_credits` **H**: Editing concerns broader credits and changes, not only biography or creator text.
27. `nch/gallery_credit_copied` **H**: The confirmation inherits the creator-only ambiguity; use the same broad credit term as the corrected copy action.
28. `nch/gallery_credit_edit_hint` **K**: Keeps required creator/copyright notices and modification description, removes only sources absent from the published image, and says the field is editable.
29. `nch/gallery_credit_title` **K**: Names the artwork field and preserves its identifying slot.
30. `nch/gallery_credit_publisher` **K**: Distinguishes the Catrobat project publisher from the creator and source fields.
31. `nch/gallery_credit_source` **K**: Identifies where the work came from and preserves the value slot.
32. `nch/gallery_credit_gallery` **K**: Keeps the gallery field distinct from publisher and source.
33. `nch/gallery_credit_licence` **K**: Exact Catrobat original-work wording, licence ID and dynamic value all survive.
34. `nch/gallery_credit_saved` **H**: Creator-only focus misstates what was saved; align with the broader credit terminology.
35. `nch/formats22_ico_size` **K**: Clearly names icon size rather than document or canvas dimensions.
36. `nch/formats22_ico_description` **K**: Preserves PNG compression, selected size range, aspect ratio and centring on a see-through square.
37. `nch/formats22_ico_decode_budget` **H**: Generic available RAM does not expressly identify the image decoding budget; retain the decoding actor and scope.
38. `nch/formats22_ico_dimensions_error` **K**: Identifies the corresponding recorded ICO directory entry, rather than an arbitrary image or directory.
39. `nch/formats22_ico_invalid_size` **K**: All seven allowed icon sizes and the unit are retained.
40. `nch/save20_dither` **K**: The exact dithering loan disambiguates the short colour-mixing description from a blending toggle.
41. `nch/ui_add_up_to_20_images_with_android_s` **H**: Preserve as draft until assembly menu/crop/sort captions and the Unplace effect are checked together against the current application.
42. `nch/ui_casual` **H**: “As writing usually is” does not clearly denote a casual font style; distinguish from the cursive and normal families.
43. `nch/save20_bmp_description` **K**: Preserves uncompressed 24-bit RGB, unchanged colours and larger files.
44. `nch/save20_bmp_size_limit` **K**: Applies the size constraint to BMP file capacity, not a width/height cap.
45. `nch/save20_gif_size_limit` **K**: Each side is limited to the precise 65,535 pixels.
46. `nch/save20_unsupported_tagged_colour` **K**: Keeps the BMP/GIF alternatives, unsupported embedded profile, colour-managed sRGB PNG conversion and subsequent import.
47. `nch/ui_pencil_crisp_adjustable_strokes` **K**: Uses the pinned pencil label and describes crisp edges for any chosen width.
48. `nch/ui_cursor_ink30` **K**: Explicitly enables drawing with the cursor, not merely moving it.
49. `nch/ui_cursor_help31` **K**: Sequence is drag, tap the on-screen button, drag to draw and tap to stop. Both route labels match the pinned nch Draw and Drawing captions.
50. `nch/ui_cursor_settings31` **K**: Identifies cursor-drawing settings and retains ellipsis.
51. `nch/ui_cursor_marker_help31` **K**: Correctly changes only the cursor marker, not the painted stroke width.
52. `nch/ui_gimp_translations31` **H**: The wording can mean whoever altered speech; make credit for translating text explicit alongside licences.
53. `nch/ui_cursor_pan_draw32` **K**: Moves the cursor to start drawing, with the separate tap-to-stop instruction.
54. `nch/ui_cursor_pan_move32` **K**: Positions the cursor without drawing first; explicitly taps the drawing button to start.
55. `nch/ui_cursor_tap_hint37` **K**: Correct toggle target is the cursor itself; both start and stop survive.
56. `nch/ui_normalize_width_intro` **H**: The last clause can mean the actual crop content rather than settings; state originals and saved crop settings remain unchanged.
57. `nch/ui_normalize_height_intro` **H**: The same crop-settings issue affects the height version; preserve the ratio and count in the revision.
58. `nch/ui_normalize_width_info` **K**: Preserves per-image width, a range of resulting heights, largest current width as percentage base, and reflow to fit.
59. `nch/ui_normalize_height_info` **K**: Preserves per-image height, a range of widths, largest current height as percentage base, and reflow.
60. `nch/ui_normalize_width_input_percent` **K**: Uses the shared width and typed pixel base for its percentage.
61. `nch/ui_normalize_height_input_percent` **K**: Parallel shared height entry with the typed pixel reference and percentage.
62. `nch/ui_pixel_grid_help33` **H**: Makes an image appear at 800% rather than explicitly tying activation to the current zoom setting; use the same zoom term as the view controls.
63. `nch/ui_search34` **K**: Concise command to search rather than requesting help from a person.
64. `nch/ui_search_english34` **K**: Clearly restricts query input to English or Japanese.
65. `nch/ui_gallery_back34` **K**: Clear back-navigation imperative.
66. `nch/ui_irasutoya_help34` **H**: Keep as draft until Image credits route is aligned to broad attribution; verify the commercial-design and special-collaboration conditions against the existing source wording.
67. `nch/ui_openclipart_help34` **H**: CC0 and Large PNG are preserved, but the last destination reduces Image credits to who created the image; update with the common caption.
68. `nch/ui_gallery_unsupported34` **K**: Identifies that the selected source does not contain the image, not a download failure.
69. `nch/ui_open_artwork34` **K**: Artwork page opens before tapping the exact existing Use image caption.
70. `nch/ui_creator_on_source34` **K**: Directs the user to the source page to learn who supplied the image.
71. `nch/ui_irasutoya_credit34` **K**: Creator retains copyright, Irasutoya’s terms apply and this is not Creative Commons.
72. `nch/legacy_credits_title` **H**: The label narrows old credits to creator text; keep its earlier-saved time qualifier but use the broader credit term.
73. `nch/legacy_credits_hint` **H**: Keeps file export, but align the source-specific credit wording and the destination image without relying on a pronoun for the full record.
74. `nch/legacy_credits_add` **H**: Selected text could be any text; identify the specific attribution/credit record being added.
75. `nch/legacy_credits_save_text` **H**: Does not name what is selected; explicitly preserve that the credit is exported as a text file, rather than choosing an image.
76. `nch/legacy_credits_existing` **K**: Existing source credit remains and its original text is kept; no overwrite implied.
77. `nch/legacy_credits_added` **H**: Says only creator text was inserted, while the app adds the full attribution; match corrected action.
78. `nch/commons_import_svg_changes` **K**: Preserves developer tokens, output direction, exact white colour, and explicitly states original dimensions.
79. `nch/commons_import_raster_changes` **H**: “Attach everything with alpha” can imply attachment or keeping transparencies, not composition onto white. Preserve exact background token and specify blending by transparency.
80. `nch/commons_credit_copy_failed` **H**: The copy failure says only creator attribution failed; align with the corrected broad credit label.
81. `nch/commons_credit_copy_failed_reason` **H**: Reason slot is correct; retain it while replacing the narrow creator-only object.
82. `nch/commons_credit_copy_out_of_memory` **H**: Memory failure is properly described but use the same broad credit object as the other copy failures.
83. `nch/commons_metadata_http_error` **K**: Clear file information heading retains HTTP and the exact dynamic status slot.
84. `nch/commons_metadata_response_too_large` **K**: Describes the size of the Commons response exceeding what the app can receive.
85. `nch/commons_metadata_query_failed` **K**: Accurately describes an unsuccessful request for file information, not a broken image.
86. `nch/ui_assembly_exact_position` **K**: Names precise position rather than moving relative to an attached image.
87. `nch/ui_assembly_target_x` **K**: X is correctly measured from the left edge in pixels.
88. `nch/ui_assembly_target_y` **K**: Y is correctly measured from the top edge in pixels.
89. `nch/ui_assembly_position_help` **H**: Top-left, integer zero-based coordinates, overlap and stacking survive; name the output canvas distinctly from the workspace and explicitly distinguish placed images from loaded thumbnails.
90. `nch/ui_assembly_position_nonnegative` **K**: Retains inclusive zero to 2147483647 and integer-only X and Y.
91. `nch/ui_assembly_unknown_image` **K**: The selected image is no longer part of this assembly rather than simply unplaced.
92. `nch/gallery_external_link_no_handler` **K**: Android cannot find a handler app for this link; not a network error.
93. `nch/commons_metadata_not_file_page` **K**: Clearly denies the Commons file-page type, not Commons access generally.
94. `nch/commons_metadata_ambiguous_file` **K**: Preserves the inability of returned metadata to identify which file.
95. `nch/commons_metadata_unavailable` **H**: Phrase asserts no information exists, not that it cannot currently be obtained; preserve the broader unavailable condition.
96. `nch/commons_metadata_original_mismatch` **H**: Broaden creator wording to all source attribution and keep the mismatch tied to the selected original file.
97. `nch/commons_metadata_invalid_page` **H**: The author-only page description narrows the expected Commons attribution page and does not clearly report invalid data.
98. `nch/commons_metadata_field_too_large` **H**: The limit is applied to part of creator text; identify the attribution field without dropping why it was rejected.
99. `nch/commons_metadata_cache_failed` **H**: Reports a failure to retain creator text only; use the broader Commons attribution record term.
100. `nch/commons_download_original_mismatch` **K**: States the download led to a different original file, not just a different URL.

## Batch 14: Central Huasteca Nahuatl and Navajo

Reviewed 100 previously unreviewed drafts. K = keep the exact candidate for separate integration; H = hold for wording revision or verification. Batch: **67 keep, 33 hold**. Cumulative: **1400 reviewed, 945 keep, 455 hold**. This pass does not change Android resources.

1. `nch/commons_svg_png_encode_failed` **H**: Maps without writing is narrower than blank maps; name the blank-map category without treating every label-free map as the same.
2. `nch/ui_help23` **H**: The short guide needs exact UI caption verification for Save/Undo/Redo and the changed Image credits terminology; the route currently uses the restricted “maps without writing” phrase.
3. `nch/ui_the_arrow_on_the_left_directly_below_the` **H**: Hold the full ten-paragraph guide pending a control-caption audit, particularly Image credits, the non-destructive Unplace action, and opacity against the actual build.
4. `nv/commons_blank_maps` **H**: Kéyah and the picture phrase identify pictured land but the parenthetical restricts blank to absence of words; confirm the accepted map-category term.
5. `nv/ui_add_images` **K**: Concise add-to-container directive uses the existing picture and insertion vocabulary.
6. `nv/ui_add_images_first` **K**: The same add-images action is retained, with Áłtsé making it a prerequisite.
7. `nv/ui_add_to_custom_colours` **H**: The parenthetical describes colours you choose rather than the separate persistent custom palette; align the palette name first.
8. `nv/ui_an_assembly_can_contain_up_to_20_images` **H**: The wording shifts between first-person assembly/removal and a user-directed insertion; verify both removal and 20-image capacity without implying source deletion.
9. `nv/ui_an_assembly_can_contain_up_to_20_images_86d995` **H**: This paired capacity label needs a clear upper limit and the established assembly object, rather than resembling a first-person operation.
10. `nv/ui_an_paint_assembly_image` **K**: The already-combined image phrasing differentiates the output from the workspace title.
11. `nv/ui_an_paint_image_assembly` **K**: Uses the exact established Image assembly wording, with app branding retained.
12. `nv/ui_an_paint_image_assembly_20_images_placed` **K**: Matches the established assembly title and keeps distinct loaded and placed counts with the exact indices and line structure.
13. `nv/ui_apply_to_all` **K**: “All” and the existing use/apply verb convey the all-target action.
14. `nv/ui_apply_to_these_images` **K**: Specifies these images as the recipients of the apply action, unlike its all-target counterpart.
15. `nv/ui_batch_crop` **H**: Says crop the selected material; it does not identify multiple selected images or a batch operation.
16. `nv/ui_batch_crop_images` **H**: Mentions selected images but does not make the shared batch operation clear; pair its revision with the short caption.
17. `nv/ui_common_in_pixels` **K**: Retains a generic common dimension and a clear px unit marker.
18. `nv/ui_could_not_create_the_assembly` **K**: Names failure to create the assembly and retains the dynamic error detail.
19. `nv/ui_create_output` **H**: The generic action makes an image; name the assembly output specifically so it is not mistaken for creating a new input.
20. `nv/ui_current_safe_budget_2f_mp` **H**: Retains the numerical cap but the first phrase is generic available allowance, not clearly the safe working limit.
21. `nv/ui_add_images_then_drag_a_thumbnail_here` **K**: Add images first, then drag a small image/thumbnail here; action order is explicit.
22. `nv/ui_an_image_cannot_attach_to_itself_or_one` **H**: The first-person verb makes the attachment prohibition harder to interpret; verify phrasing that precludes both self-attachment and attachment to an existing child image.
23. `nv/ui_assembly_decoded_output_estimated_editing_render_memory_at` **H**: Labels decoded output as pixels, but the slot represents decoded output memory; distinguish it from dimensions and estimated working RAM.
24. `nv/ui_assembly_output_size` **K**: Explicit output width and height match the dimensions terminology used elsewhere.
25. `nv/ui_by_pixels_hold_and_drag_to_place` **K**: All placeholders survive, in sequence; both hold and drag are required for placement.
26. `nv/ui_common_in` **K**: Retains the generic dimension and the separately supplied unit.
27. `nv/ui_copy_decoded_image_at_this_size_estimated_loading` **H**: The decoded-image row adds px even though its dynamic value is a decoded-memory estimate, not pixel count; keep all three quantities distinct.
28. `nv/ui_could_not_decode_the_cropped_region_of` **H**: The same inbound load wording can mean opening the whole image rather than decoding a selected region; retain both crop region and decode.
29. `nv/ui_cropped_thumbnail` **K**: Identifies a small cropped image and preserves its value slot.
30. `nv/ui_custom_colours_hold_a_swatch_to_replace_it` **H**: Hold and replacement survive but the colour qualifier still names a chosen colour, not a stored custom swatch.
31. `nv/ui_downloading_image` **H**: The phrase indicates incoming imagery, which can mean loading or inserting; name the download operation distinctly.
32. `nv/ui_drag_a_line_then_drag_twice_to_set` **H**: Clarify that two later drags set two bends of the same line, and verify the exact Finish curve caption.
33. `nv/ui_drag_a_selection_drag_inside_to_move_square` **K**: Preserves selection, interior movement, square corner/edge resizing, round rotation and aspect locking.
34. `nv/ui_drag_across_the_ellipse_s_bounding_box` **K**: Describes the rectangle enclosing the ellipse and the corner-to-opposite-corner drag.
35. `nv/ui_drag_between_opposite_corners_choose_outline_or_fill` **K**: Retains opposing corners and the below-control outline/fill choice.
36. `nv/ui_drag_between_opposite_corners_to_draw_a_five` **K**: The five-point star, diagonal drag and outline/fill choice are present.
37. `nv/ui_drag_between_opposite_corners_to_draw_a_heart` **H**: The proposed shape term needs confirmation for a heart, rather than just a long form; do not rely on the correct gesture alone.
38. `nv/ui_drag_from_the_start_to_the_end_of` **K**: Retains a drag along the line from start to end.
39. `nv/ui_drag_from_the_tail_towards_the_arrowhead_choose` **K**: Retains tail-to-head direction and the outline/fill option as separate concepts.
40. `nv/ui_drag_placed_images_to_move_them_hold_and` **K**: Biiʼ hééł ályaa identifies placed images; hold and drag a smaller thumbnail to add it.
41. `nv/ui_drag_to_erase_with_the_background_colour` **K**: Matches the fixed background-colour and erase terms, so this is not alpha clearing.
42. `nv/ui_drag_to_pan_without_drawing_pinch_with_two` **K**: Distinguishes non-drawing pan, two-finger zoom/pan, and two-finger use with a drawing tool selected.
43. `nv/ui_draw_a_crisp_one_pixel_line` **H**: Describes the line as good rather than crisp-edged; keep the correct width range when revising.
44. `nv/ui_draw_with_the_selected_brush_tip_and_size` **K**: Uses the established brush term and refers to both the selected tip and selected size.
45. `nv/ui_drop_at_a_highlighted_edge_right_top_aligned` **K**: Identifies the highlight, the right/top alternative and below/left alternative in the intended edge order.
46. `nv/ui_edit_in_paint` **K**: Clearly edits in Paint, not a source image or assembly-save command.
47. `nv/ui_enable_android_s_files_or_documents_app_then` **H**: App name alternatives and retry survive, but the enable instruction should read as enabling those Android apps, not just opening or launching them.
48. `nv/ui_estimated_memory_current_working_budget` **K**: Correct distinct rows for estimated and currently available working RAM, with newline and slot positions.
49. `nv/ui_fill_text_box_with_bg_colour` **K**: Matches the pinned behind/background-colour term and fills the inside of the text box rather than the lettering.
50. `nv/ui_fits_the_current_budget` **K**: States the current working RAM limit is not exceeded.
51. `nv/ui_font_licences` **K**: Refers to diverse forms of lettering as the licensing object, separate from icons and images.
52. `nv/ui_gallery_image` **K**: Recognizable image from the gallery, using the catalogue’s image vocabulary.
53. `nv/ui_give_all_images_the_same_each_image_keeps` **K**: Keeps both typed slots, per-image aspect ratio, original files and unchanged cropping settings.
54. `nv/ui_hide_pixel_grid_800` **H**: Preserves Hide and threshold, but the draft uses a different grid phrase from Show; review both as a pair so each indicates the same overlay.
55. `nv/ui_hold_a_thumbnail_and_drag_it_here_or` **K**: Both transfer methods are explicit: hold and drag the thumbnail here, or tap it and then tap the workspace.
56. `nv/ui_icon_licences` **K**: Describes small tool images as the licence subject, distinguishable from artwork and fonts.
57. `nv/ui_icon_licences_kde_breeze` **K**: Exact KDE Breeze name and the same icon-licence term as the generic caption.
58. `nv/ui_image_credits` **H**: “About the people who made the image” can omit source and licence; establish the broader image-attribution label.
59. `nv/ui_image_placed_drag_it_to_move_or_hold` **K**: Uses the pinned placement wording and separates dragging the placed image from holding and dragging a new thumbnail.
60. `nv/ui_image_shown_in_crop_preview` **K**: Identifies an image, the crop and its projected view without implying the crop already applied.
61. `nv/ui_image_thumbnails_and_filenames_scroll_horizontally_for_more` **K**: Identifies thumbnails and names, then explicitly offers left/right dragging to see more.
62. `nv/ui_insert_gallery_image` **K**: A clear gallery-image insertion question, not replacing the canvas.
63. `nv/ui_icons_artwork` **K**: Distinguishes small tool icons from drawn artwork.
64. `nv/ui_icons_fonts_artwork_credits` **H**: The heading can limit credits to creator information alone; preserve distinct icons, font and artwork categories with a broader credit term.
65. `nv/ui_image_assembly_workspace_drag_placed_images_or_drop` **H**: Retains pinch and empty-space pan, but clarify attachment as snapping to right/bottom targets rather than just putting thumbnails on those sides.
66. `nv/ui_invalid_image_attachments` **K**: Keeps the attachment-specific invalidity, rather than blaming the source image format.
67. `nv/ui_largest` **K**: An unambiguous largest option matching the scale choices.
68. `nv/ui_lossless_jpeg_xl` **H**: “No image information missing” is promising but the negative scope needs checking for literal losslessness versus unavailable metadata.
69. `nv/ui_magnified_preview` **K**: Consistent with the pinned magnified drawing-preview wording and retains ellipsis when it opens a control.
70. `nv/ui_magnified_preview_ea9209` **K**: The no-ellipsis counterpart keeps the same preview terminology.
71. `nv/ui_modified_newest_first` **K**: Uses modification as the ordering basis and newest first.
72. `nv/ui_modified_oldest_first` **K**: Uses the same modification basis and earliest first.
73. `nv/ui_monospace` **K**: Defines monospace as equal widths for all writing symbols.
74. `nv/ui_no_attachment_fits_within_the_current_coordinate_range` **K**: Names the current X/Y limit and advises smaller image sizes rather than implying all attachment is disabled.
75. `nv/ui_no_gallery_images_have_been_inserted` **H**: Could suggest absence of creator information alone; use the same broad text-based attribution term as Image credits.
76. `nv/ui_not_enough_memory_to_inspect_the_gallery_image` **K**: The RAM limit is specific to inspecting the gallery image, not downloading it.
77. `nv/ui_not_placed` **K**: Negative placement counterpart clearly means not yet placed in the workspace, not missing a file.
78. `nv/ui_original_decoded_image_rgba_4_bytes_pixel_estimated` **K**: Keeps the source/decoded/estimated rows distinct with RGBA and 4 bytes per pixel; editing estimate explicitly assumes no resize.
79. `nv/ui_other_terms` **K**: Uses the established terms/licence vocabulary for remaining conditions.
80. `nv/ui_pencil_keeps_crisp_one_pixel_strokes_cursor_drawing` **H**: Uses the right pencil and width but describes edges as “good”; describe crisp edges in contrast with smoothed or antialiased edges.
81. `nv/ui_percent_of_pixels` **H**: The percentage phrasing needs verification that it reads as a fraction of the typed pixel quantity and not in multiples of one hundred pixels.
82. `nv/ui_pinch_to_zoom_drag_to_pan` **K**: Starts with two-finger zoom and separately specifies dragging the view to pan.
83. `nv/ui_place_at_least_one_image_in_the_workspace` **K**: Makes one image the minimum and retains workspace placement as the prerequisite.
84. `nv/ui_placed` **K**: Simple completed placement state matches the negative counterpart and instruction text.
85. `nv/ui_px_drag_an_image_to_move_hold_a` **K**: Keeps exact width/height slots and px, along with separate move and thumbnail-hold gestures.
86. `nv/ui_rendering_images` **H**: The status counts prepared items; clarify it means completed processing rather than loaded or already saved images, while retaining both counters.
87. `nv/ui_restore_original_sizes` **K**: Restores original width and height, not a fixed default size.
88. `nv/ui_right_arrow_expand` **K**: Right-arrow glyph and direction are explicit and distinguish the expansion action.
89. `nv/ui_same` **K**: Generic same-dimension pattern keeps its dynamic dimension slot.
90. `nv/ui_same_height` **K**: Clearly identifies shared height, distinct from width.
91. `nv/ui_same_width` **K**: Clearly identifies shared width, consistent with counterpart.
92. `nv/ui_set_radius_px_then_drag_between_opposite_corners` **H**: Opposite corners and half-short-side limit survive, but verify the quoted radius label exactly and confirm the center-to-edge wording is read as corner radius.
93. `nv/ui_show_pixel_grid_800` **H**: Preserves 800%+ but uses a different term than Hide for the overlay; establish the shared grid terminology.
94. `nv/ui_shows_the_whole_assembly_image_and_output_sizes` **K**: The whole assembly becomes visible, without changing size of input or output images.
95. `nv/ui_smallest` **K**: Clear smallest choice matching the other extreme.
96. `nv/ui_some_previews_could_not_be_decoded_you_can` **H**: Removal action is first-person in form and the save alternative reads as a direct command; clarify both permitted options without implying the app already deleted images.
97. `nv/ui_strikethrough` **K**: Specifies a line through the middle of the text, distinct from underline.
98. `nv/ui_tap_a_pixel` **K**: Clear direct tap gesture on one pixel.
99. `nv/ui_tap_an_enclosed_area_adjust_tolerance_for_similar` **K**: Preserves tapping an enclosed region and modifying settings for similar colours.
100. `nv/ui_tap_an_image_thumbnail_first` **K**: Requires first tapping the thumbnail, not a placed image or the workspace.

## Batch 15: Navajo

Reviewed 100 previously unreviewed drafts. K = keep the exact candidate for separate integration; H = hold for wording revision or verification. Batch: **77 keep, 23 hold**. Cumulative: **1500 reviewed, 1022 keep, 478 hold**. This pass does not change Android resources.

1. `nv/ui_tap_the_canvas_to_place_text_and_choose` **K**: The touch and placement vocabulary matches the existing canvas prompt, followed by selecting font and size.
2. `nv/ui_tap_the_image_to_sample_the_foreground_colour` **K**: Uses the established Foreground term and identifies the image as the sampled surface.
3. `nv/ui_that_arrangement_overlaps_another_image_use_a_different` **K**: Overlap and alternate-edge remedy survive; the matched Unplace wording means taking the attached images out of the layout, not erasing the inputs.
4. `nv/ui_the_assembly_needs_about_choose_a_smaller_output` **K**: Preserves the approximate requirements slot and the suggestion to make a smaller output.
5. `nv/ui_the_assembly_output_is_unavailable_reopen_image_assembly` **H**: Says the combined output is absent, not just unavailable, and does not explicitly say to retry after reopening.
6. `nv/ui_the_attachment_image_is_missing` **K**: Reports the specific attached image is missing, distinct from a merely unplaced source.
7. `nv/ui_the_attachment_image_is_not_placed` **K**: Uses the same placement distinction as the adjacent positive and negative status labels.
8. `nv/ui_the_first_image_starts_at_the_top_left` **K**: Explicitly matches the top-left origin for the first image.
9. `nv/ui_the_gallery_download_is_too_large` **K**: Applies excessive size to the incoming file from the gallery, not to the gallery as a whole.
10. `nv/ui_the_gallery_image_is_unavailable` **H**: Absence does not cover temporary unavailability; keep the gallery term and avoid implying deletion.
11. `nv/ui_the_image_could_not_be_downloaded` **H**: “Cannot open/load” can describe a decode or import failure rather than a failed download; align with downloading terminology.
12. `nv/ui_the_online_gallery_could_not_be_loaded_check` **K**: Identifies the online gallery, checks the internet connection and directs another attempt.
13. `nv/ui_third_party_notices` **H**: The description of another person’s information does not distinguish third-party legal notices from ordinary external content.
14. `nv/ui_this_image_is_outside_the_supported_catrobat_gallery` **K**: Keeps Catrobat exact and identifies an image not within that gallery.
15. `nv/ui_time_unavailable` **K**: States the data about when the event occurred are unavailable, not that system time itself has failed.
16. `nv/ui_tool_option` **K**: An option belonging to the tool is distinct from a new tool or external app.
17. `nv/ui_toolbox_and_tool_options_scroll_for_more` **K**: Names tools and tool choices and tells the user to scroll for more.
18. `nv/ui_trim_from_the_original_edges_drag_the_handles` **K**: Original image edges, drag versus numeric entry, and unchanged source files are all expressed.
19. `nv/ui_trim_in_pixels` **K**: Matches the established trim action and retains the typed amount/side slot with px.
20. `nv/ui_unplace` **K**: Removal from the interior/workspace matches non-destructive removal of a placement; distinct from erase.
21. `nv/ui_wheel` **K**: Describes the circular colour control, separate from the spectrum.
22. `nv/ui_widths` **K**: Keeps the width heading used above multiple dimensions and does not add a unit.
23. `nv/ui_you_can_add_more_images_select_fewer_files` **K**: Keeps the remaining-image count and the need to select a smaller batch of files.
24. `nv/ui_agpl_licence` **K**: Exact AGPL identifier and established licence phrasing.
25. `nv/ui_jpeg_xl_codec_licences` **K**: Names the specific JPEG XL codec rather than file attribution or the app licence.
26. `nv/ui_gnu_agpl_licence` **K**: Retains exact GNU AGPL identifier and consistent licence wording.
27. `nv/ui_preview_memory_error` **K**: Preserves the item slot and RAM constraint specifically for previewing it.
28. `nv/ui_trim_in_percent` **H**: Same unverified mathematical percentage wording as the pixel-reference caption; compare with native usage before replacing the verified px trim label.
29. `nv/ui_crop_preview_images` **K**: Both quantity variants retain the preview dimensions/count, application of cropping, and conditional move of attached images.
30. `nv/ui_add_palette23` **K**: Consistent palette and insertion wording with the existing toolbar label.
31. `nv/ui_added_palette23` **K**: Completed addition parallels the palette action and does not imply replacing another colour.
32. `nv/ui_replace_palette23` **K**: Indicates no free palette slots and instructs selecting one to replace.
33. `nv/ui_edit_palette23` **K**: Names editing the palette rather than opening the picker.
34. `nv/ui_replace_with_active23` **K**: The current colour is the replacement value, not the slot to remove.
35. `nv/ui_remove_palette23` **K**: Specifies taking a colour out of the palette, not erasing a pixel.
36. `nv/ui_add_active23` **K**: Adds the current colour using the existing palette insertion terminology.
37. `nv/ui_horizontal23` **K**: The left-right direction and double arrow distinguish horizontal writing.
38. `nv/ui_vertical_rl23` **K**: Both direction axes are correct: glyphs down, successive columns right to left.
39. `nv/ui_vertical_lr23` **K**: The matched counterpart switches only the column direction.
40. `nv/ui_vertical_letters23` **K**: The writing-symbol qualifier and top-to-bottom arrow identify the glyph options.
41. `nv/ui_the_assembly_exceeds_android_s_coordinate_range` **K**: Reports that assembly X/Y bounds exceed Android’s coordinate range, not device memory.
42. `nv/ui_the_images_cannot_fit_within_android_s_coordinate` **K**: Names the same Android X/Y limit for input images and advises choosing smaller images.
43. `nv/ui_the_normalized_image_dimensions_are_outside_android_s` **K**: Specifies the normalized dimension and the Android restriction rather than saying the images cannot be loaded at all.
44. `nv/ui_vertical_mixed23` **K**: Preserves automatic selection and separate upright CJK and sideways-word conditions.
45. `nv/ui_vertical_sideways23` **K**: Retains the sideways setting and keeping words together as units.
46. `nv/ui_vertical_upright23` **K**: Uses symbols rather than letters-only terminology for the one-by-one upright mode.
47. `nv/ui_top23` **K**: Matches the upper alignment term used for snapped layouts.
48. `nv/ui_bottom23` **K**: Keeps the corresponding lower alignment distinct from top.
49. `nv/colour20_custom_selected_slot` **H**: The chosen-colours parenthetical can describe any user-picked colour; distinguish the stored Custom section and currently selected slot.
50. `nv/colour20_stored_slot` **K**: Preserves both placeholders, tap-to-use, adjustment and explicit separate Replace-to-save action.
51. `nv/colour20_empty_slot` **K**: Identifies an empty numbered slot and tapping to choose where to save the current colour.
52. `nv/colour20_save_slot` **K**: Saves to the uniquely numbered slot rather than opening a generic picker.
53. `nv/colour20_replace_slot` **K**: Replacement phrase matches the adjacent Replace-to-save instruction and names its slot.
54. `nv/colour20_saved_slot` **K**: Completed save message identifies both colour and slot.
55. `nv/gallery_image_component_unavailable` **H**: Mentions image information that is needed, which is narrower than an unavailable required image component; keep the import-not-performed outcome.
56. `nv/formats22_base64_label` **K**: Clear distinction of Base64 text from PNG or ASCII art.
57. `nv/formats22_ascii_label` **K**: Keeps ASCII and a meaningful “made by drawing” art distinction.
58. `nv/formats22_tiff_compression` **H**: Verify the no-information-loss expression for strict reversible compression rather than appearance or metadata; retain Deflate exact.
59. `nv/formats22_tiff_description` **H**: The RGB page, unchanged pixel caveat and possible smaller file survive, but the final instruction uses the enable/use verb where the source asks to disable compression.
60. `nv/formats22_dib_size_limit` **K**: Applies the limit to the DIB file size, not its dimensions.
61. `nv/formats22_select_page` **K**: Selects exactly one page using the same noun as the page dialog.
62. `nv/formats22_page_description` **K**: Both metadata slots, total page count and choice to edit one page as an image survive.
63. `nv/formats22_page_number` **H**: The phrase also labels the total page count on the previous row; distinguish the current page number from number of pages.
64. `nv/formats22_previous_page` **H**: Níwohdę́ę́ʼ can evoke an earlier or old page, not necessarily the immediately previous page. Establish consistent neighboring-page controls.
65. `nv/formats22_next_page` **K**: Bikʼijįʼ denotes the following page and aligns with forward navigation.
66. `nv/formats22_open_page` **K**: Open action targets the current choice rather than a general file picker.
67. `nv/formats22_page_preview` **K**: Describes preview of the selected page, not the already-open document.
68. `nv/formats22_page_range` **K**: Retains one as the minimum and the formatted maximum page number.
69. `nv/formats22_loading_page` **K**: Both page counters and ongoing preview load remain distinct.
70. `nv/formats22_page_dimensions` **K**: Keeps all four slots in order and identifies the two ending slots as pixel dimensions.
71. `nv/formats22_preview_unavailable` **K**: States the preview is unavailable and preserves the diagnostic token.
72. `nv/formats22_preview_memory` **K**: Explains the preview memory problem and makes the smaller-dimension offer conditional on opening the page and availability.
73. `nv/formats22_pdf_invalid` **H**: The second alternative can read as Android not recognizing the entire file rather than this Android version not supporting features used by the PDF.
74. `nv/formats22_pdf_file_size` **K**: Numeric notation precisely states both nonempty and capped at 512 MiB.
75. `nv/formats22_pdf_page_count` **K**: Inclusive page-count range retains 1 and the typed upper bound.
76. `nv/formats22_pdf_page_index` **K**: Keeps the invalid selection and asks for a different page within this PDF.
77. `nv/formats22_pdf_dimensions` **K**: Retains either invalid page dimensions or dimensions too large to import.
78. `nv/formats22_pdf_crop` **K**: Keeps rectangle wholly inside the selected page and explicitly requires strictly positive width and height.
79. `nv/formats22_pdf_memory` **H**: A generic RAM shortage does not distinguish the specific image memory budget from available device RAM.
80. `nv/formats22_base64_description` **H**: Check strict lossless wording here as in the TIFF label; URI prefix, recover-by-reopen direction and Base64 size overhead are otherwise intact.
81. `nv/formats22_ascii_columns` **K**: Explicitly uses width in writing units, not pixels.
82. `nv/formats22_ascii_invert` **H**: Uses white and black, which narrow light and dark character groups to exact extrema; revise so contrast inversion applies to all characters.
83. `nv/formats22_text_not_image` **K**: No supported image is contained in the Base64 text; it does not assert no valid Base64.
84. `nv/gallery_copy_credit` **H**: The object of copying is framed principally as creator information; use the same broader attribution term as the corrected gallery credit heading.
85. `nv/gallery_edit_credits` **H**: Creator-oriented phrasing risks excluding editing licence/source and change information; revise with matching terminology.
86. `nv/gallery_credit_copied` **H**: The completion has the same creator-only ambiguity; use the corrected copy action term.
87. `nv/gallery_credit_title` **K**: Identifies artwork rather than gallery or publisher and retains the title slot.
88. `nv/gallery_credit_publisher` **H**: The phrase suggests the creator of a document, not its publisher; state the Catrobat project’s publication role explicitly.
89. `nv/gallery_credit_source` **K**: Concise provenance label preserves dynamic source value.
90. `nv/gallery_credit_gallery` **K**: Clear gallery field and separate value slot.
91. `nv/gallery_credit_licence` **K**: Names Catrobat original artwork and preserves both CC BY-SA 4.0 and the licence placeholder.
92. `nv/gallery_credit_saved` **H**: Retain the saved outcome using the corrected term for complete credit text rather than creator information alone.
93. `nv/formats22_ico_size` **K**: A specific icon-size question distinct from sizing the whole canvas.
94. `nv/formats22_ico_description` **H**: Aspect ratio, size and centre survive, but explicitly describe PNG compression and the transparent square instead of only something visible behind the image.
95. `nv/formats22_ico_decode_budget` **H**: Reads as opening/loading the icon with insufficient RAM; distinguish decoding from the available image-specific memory limit.
96. `nv/formats22_ico_invalid_size` **K**: Retains every supported icon size and the exact pixel unit.
97. `nv/save20_bmp_description` **K**: Retains RGB and 24-bit, no compression, unchanged colours and larger file size.
98. `nv/save20_bmp_size_limit` **K**: Names the BMP file-size limit rather than the per-side limit.
99. `nv/save20_gif_size_limit` **K**: Sets the same precise inclusive pixel limit on both width and height.
100. `nv/gallery_description` **H**: Hold this legal/help paragraph until the complete credits route, copy captions, publisher vs creator, and compatible-licence wording agree with the pinned controls.

## Batch 16: Navajo

Personally reviewed 100 distinct wording records. Batch: **60 keep, 40 hold**. Overall: **1600 reviewed, 1082 keep, 518 hold**. This changes only the review ledger, not Android resources.

1. `nv/gallery_credit_edit_hint` **H**: The clause for removing unused sources risks describing good provenance rather than the entry to remove; legal notices and editability survive, but check that clause before clearance.
2. `nv/formats22_ico_dimensions_error` **H**: The text gives disagreement with information stored inside ICO without clearly naming the corresponding internal directory entry associated with this image.
3. `nv/save20_unsupported_tagged_colour` **K**: Preserves BMP/GIF input, colour-profile conversion failure, colour-managed editor, sRGB PNG and the subsequent import step.
4. `nv/ui_pencil_crisp_adjustable_strokes` **H**: The pencil term differs from the existing tool caption; the edge phrase also needs to mean crispness at all widths rather than visibility alone.
5. `nv/ui_cursor_ink30` **K**: The marker and drawing wording matches existing Cursor drawing terminology.
6. `nv/ui_cursor_help31` **H**: All gestures remain, but the second quoted Drawing caption differs from the current Drawing label; align the route.
7. `nv/ui_cursor_settings31` **K**: Uses the same marker/drawing settings caption as the existing corresponding control, with ellipsis.
8. `nv/ui_cursor_marker_help31` **K**: Makes the cursor marker bigger without resizing the rendered stroke.
9. `nv/ui_gimp_translations31` **H**: Verify the contributor phrase means people who translated the app rather than simply altered words; retain the licence part.
10. `nv/ui_cursor_pan_draw32` **K**: Moves the cursor to start drawing and separates the second tap that stops it.
11. `nv/ui_cursor_pan_move32` **K**: Explicitly separates positioning the cursor from tapping the drawing button to start.
12. `nv/ui_cursor_tap_hint37` **K**: Names the cursor itself as the touch target and retains both actions.
13. `nv/ui_normalize_width_intro` **K**: Keeps equal width, numbered count, each image’s ratio, and unchanged originals and crop settings.
14. `nv/ui_normalize_height_intro` **K**: Parallel equal-height action keeps the count, width-height ratio and unchanged originals/settings.
15. `nv/ui_normalize_width_info` **H**: Dimensions, largest current width and reflow survive; percentage wording needs the same verification as the other percentage labels.
16. `nv/ui_normalize_height_info` **H**: Height and width slots are correctly transposed, but hold until the percentage wording is approved with its width counterpart.
17. `nv/ui_normalize_width_input_percent` **H**: Verify the per-hundred construction explicitly means percentage of the formatted pixel quantity.
18. `nv/ui_normalize_height_input_percent` **H**: Same percentage issue as width; retain the shared height and typed pixel base.
19. `nv/ui_pixel_grid_help33` **H**: Clarify this is zoom level, specifically the pixel grid, and that rulers rather than generic marks show image-pixel positions.
20. `nv/ui_search_english34` **K**: Names English and Japanese as alternative search languages rather than translation of returned titles.
21. `nv/ui_gallery_back34` **K**: Concise return action for gallery navigation.
22. `nv/ui_irasutoya_help34` **H**: The legal threshold is present; verify commercial-purpose wording and the exact Image credits route.
23. `nv/ui_openclipart_help34` **H**: Art-page sequence, Large PNG and CC0 survive; hold until the exact final credits caption is settled.
24. `nv/ui_assembly_position_help` **K**: Specifies top-left, whole pixels from zero, unchanged other positions, overlap and newest-on-top priority, expansion and unchanged crop/size.
25. `nv/ui_gallery_unsupported34` **K**: Image is not from the selected source; does not claim it cannot be loaded or is nonexistent.
26. `nv/ui_open_artwork34` **K**: Page-before-Use order and the existing Navajo Use image wording.
27. `nv/ui_creator_on_source34` **K**: Points to the source for the credited contributor, not the app publisher.
28. `nv/ui_irasutoya_credit34` **K**: Keeps creator-held rights, service terms and explicit non-Creative-Commons status.
29. `nv/legacy_credits_title` **K**: Identifies formerly saved credit information, distinguishing it from a new credit.
30. `nv/legacy_credits_hint` **K**: Prior-save and other-image warning survive, as do selecting a source and adding its information or exporting full text.
31. `nv/legacy_credits_add` **K**: The selected credit information is added to this image, not used to insert a second image.
32. `nv/legacy_credits_save_text` **K**: Names the selected information as text and aligns Save with the same credit object.
33. `nv/legacy_credits_existing` **K**: Indicates a credit for that same source already exists and its wording was not overwritten.
34. `nv/legacy_credits_added` **K**: Reports the completed attachment of credit information to this image.
35. `nv/commons_import_svg_changes` **K**: Keeps original width/height and all machine-style tokens, including exact background and SVG-to-PNG operation.
36. `nv/commons_import_raster_changes` **H**: The parenthetical does not clearly distinguish alpha compositing from redrawing or layering an image; preserve the exact white-background token.
37. `nv/commons_credit_copy_failed` **H**: Use broad attribution wording from the corrected Copy credit action; this can mean only creator information.
38. `nv/commons_credit_copy_failed_reason` **H**: Same broader credit object as the base failure; keep the formatted reason.
39. `nv/commons_credit_copy_out_of_memory` **H**: The memory shortage is clear but the object needs the fuller attribution term used in related copy errors.
40. `nv/commons_metadata_http_error` **K**: Correct file-information context, provider, HTTP label and status slot.
41. `nv/commons_metadata_response_too_large` **K**: The incoming response exceeds allowed size, not the image or map dimensions.
42. `nv/commons_metadata_query_failed` **K**: Reports failure to look up Commons file information without calling the file corrupt.
43. `nv/ui_assembly_exact_position` **K**: Names precise position distinctly from image dimensions.
44. `nv/ui_assembly_target_x` **K**: Preserves the x direction and the left pixel reference.
45. `nv/ui_assembly_target_y` **K**: Preserves the y direction and the top pixel reference.
46. `nv/ui_assembly_position_nonnegative` **K**: Shows whole-number progression from zero to the precise upper limit for both coordinates.
47. `nv/ui_assembly_unknown_image` **K**: The selection is no longer in this assembly rather than simply unplaced.
48. `nv/gallery_external_link_no_handler` **K**: No Android application is available to open this link; it is not a network outage.
49. `nv/commons_metadata_not_file_page` **K**: Denies the Commons file-page type rather than any Commons link.
50. `nv/commons_metadata_ambiguous_file` **K**: Describes uncertainty about which file the metadata means rather than invalid decoding.
51. `nv/commons_metadata_unavailable` **H**: The draft may assert no Commons metadata exists, rather than being presently unavailable; retain the file-information distinction.
52. `nv/commons_metadata_original_mismatch` **H**: The mismatch is against the selected original file, but the other side can read as who made it rather than the full attribution record.
53. `nv/commons_metadata_invalid_page` **H**: The line calls the maker information invalid without identifying the Commons attribution page; include page and full credit record.
54. `nv/commons_metadata_field_too_large` **H**: Retains a text-length ceiling, but clarify the individual attribution field and broaden creator-only wording.
55. `nv/commons_metadata_cache_failed` **H**: The ability to retain/save is clear; use the broader Commons attribution record as the object.
56. `nv/commons_download_original_mismatch` **K**: Correctly identifies a redirect to a different original file, not just to another address.
57. `nv/commons_svg_png_encode_failed` **H**: Blank-map terminology needs verification because the wording limits it to maps lacking text; PNG encode failure itself is present.
58. `nv/ui_about_copyright` **K**: Identifies the application’s About information and preserves a distinct creator-rights component.
59. `nv/ui_about_copyright_licence` **K**: Distinguishes copyright from permission to use/licence rather than merging them into one pointer.
60. `nv/ui_corners_and_edges_resize_round_handle_rotates` **K**: Correctly separates corner/edge resizing from circular-handle rotation.
61. `nv/ui_could_not_load_gallery_image` **K**: Keeps the image from the gallery as the item that failed to load and preserves the diagnostic.
62. `nv/ui_credits_terms` **H**: The credits phrase leans toward the creators as the only credit subject; make it broad enough for source and other notices separately from terms.
63. `nv/ui_current_safe_editing_budget_s_up_to_2f` **K**: Preserves current available editing RAM, exact megapixel bound and exclusion of additional decode RAM from the estimate.
64. `nv/ui_custom_colour` **H**: Qualifies the colour as selected, not a specific custom colour; align it with the rest of the custom palette controls.
65. `nv/ui_drag_out_to_expand_in_to_trim_drag` **K**: Outward and inward drags are distinguished from moving the whole bounds, with pinch/Fit and background fill retained.
66. `nv/ui_hold_or_drag_to_spray_colour` **K**: Hold or drag activates spraying colour with the already established Airbrush terminology.
67. `nv/ui_smooth_pixel_edges_anti_aliasing` **K**: Preserves explicit anti-aliasing, and smoothing the stepped pixel edges is distinguishable from freehand stroke smoothing.
68. `nv/ui_sort_images_by_filename_or_modification_time` **K**: File name and modification time remain separate sort options.
69. `nv/ui_sort_tray` **K**: Identifies the bottom thumbnail tray as the sorted collection, rather than sorting placements.
70. `nv/ui_webp_codec_licences` **K**: Names WebP read/write tools and their licensing, not the licence of a source image.
71. `nv/ui_heic_avif_codec_licences` **K**: Same codec wording covers both named HEIC and AVIF formats.
72. `nv/ui_image_codec_licences` **K**: Generic encoder/decoder licence heading is clearly tied to image tooling.
73. `nv/formats22_dib_description` **K**: Includes Windows DIB, exact bit depth and no compression, and recommends BMP only when the receiving app needs its header.
74. `nv/formats22_pdf_encrypted` **H**: The password wording is recognizable; the second alternative needs explicit unsupported encryption rather than general inability to open the PDF.
75. `nv/ui_add_up_to_20_images_with_android_s` **H**: Hold the full assembly guide until preview, Batch crop, aspect/percentage and placement captions agree with the actual UI; preserve non-destructive removal.
76. `nv/ui_help23` **H**: Hold the compact guide pending the exact View/Draw/navigation labels and verification of Save/overwrite and credits routes.
77. `nv/ui_the_arrow_on_the_left_directly_below_the` **H**: Hold the ten-paragraph guide until paths, controls, source/rights wording and image transparency versus opaque canvas are checked against the current app.
78. `nv/commons_check_file_licence` **H**: Creator, licence and adaptation are mentioned; confirm that required attribution is broader than creator information in this compliance text.
79. `nv/ui_casual` **H**: The descriptive term can indicate ordinary handwriting, not a casual font; distinguish from Cursive and the default.
80. `nv/ui_catrobat_online_gallery_artwork_by_its_credited_creators` **K**: Separates Catrobat’s gallery from artwork made by its credited contributors.
81. `nv/ui_catrobat_s_own_artwork_uses_cc_by_sa` **H**: Licence stays exact, but align the final menu caption to a broad Image credits term and make separate attribution more explicit than another maker name.
82. `nv/ui_catrobat_sticker_gallery` **K**: The small/insertable-image description matches the sticker-gallery entry and carries the ellipsis.
83. `nv/ui_could_not_export_source_code` **H**: The failure names saving the app’s text generally; distinguish exporting actual source code to an external file rather than saving text.
84. `nv/ui_cursive` **K**: Describes joining handwritten glyphs, distinct from the unqualified handwriting or normal families.
85. `nv/ui_export_this_version_s_source_code` **H**: Describes saving app text; make both the exact app version and source-code export meaning clear.
86. `nv/ui_gallery_artwork_catrobat_and_its_credited_creators_cc` **H**: The legal text retains default licence and exceptions; confirm full artwork attribution rather than creator-only information before publishing.
87. `nv/ui_open_source_credits_and_notices` **H**: Being readable by all does not itself mean open source; preserve both source-licence notices and credit objects.
88. `nv/ui_sans_condensed` **K**: Specifies narrower horizontal spacing rather than a lighter stroke or smaller point size.
89. `nv/ui_sans_light` **H**: “Not very thick” can overlap the medium option; establish a stable named relative weight.
90. `nv/ui_sans_medium` **K**: Names an intermediate stroke weight instead of the middle alignment.
91. `nv/ui_sans_thin` **H**: Marks small lines, not necessarily very thin strokes; check alongside Light and Medium.
92. `nv/ui_source_code_exported_including_build_scripts_and_licence` **H**: Describes saved app text and text to make the app, but ensure exported source code and included build scripts are recognized as distinct.
93. `nv/ui_the_gallery_redirected_outside_its_supported_hosts` **K**: Keeps both the redirect and the new URL being unsupported by the app.
94. `nv/ui_too_many_gallery_redirects` **K**: Reports excessive repetition of URL redirects without recasting it as an unsupported image type.
95. `nv/ui_sans_serif` **K**: Small terminal strokes are explicitly absent, distinguishing the Sans serif family.
96. `nv/ui_serif` **K**: Matched counterpart explicitly describes the presence of fan/terminal small strokes.
97. `nv/ui_draw_around_an_area_drag_inside_to_move` **K**: Preserves free-form boundary, interior movement, square edge/corner handles, round rotation and the existing Commit selection button.
98. `nv/ui_draw_soft_watercolor_strokes_strength_controls_how_strongly` **K**: Water is part of the brush action, with softer strokes and Strength adjusting colour blending into the canvas.
99. `nv/ui_each_px_px_percent_is_relative_to_the` **H**: All dimension slots and placed reflow survive, but the mathematical phrase is the same unverified percentage expression.
100. `nv/ui_estimates_include_the_current_canvas_and_clipboard_sampled` **H**: Keeps current image, sampled decode/edit memory, lost detail and unchanged original, but verify current clipboard terminology and explicitly that the selected background is opaque.

## Batch 17: Navajo and Tai Nüa

Personally reviewed 100 distinct wording records. Batch: **90 keep, 10 hold**. Overall: **1700 reviewed, 1172 keep, 528 hold**. This changes only the review ledger, not Android resources.

1. `nv/ui_honeycomb_colour_06x` **K**: Keeps the honeycomb swatch category as a descriptive qualifier and preserves the exact uppercase hexadecimal format token.
2. `nv/ui_honeycomb_colour_swatches_with_a_greyscale_row` **K**: Uses the honeycomb descriptor consistently and explicitly includes the black-to-white row.
3. `nv/ui_hue_and_saturation_spectrum_lightness_slider_on_the` **K**: Labels the right control HSL L and retains hue and saturation, distinguishing it from HSV value.
4. `nv/ui_hue_and_saturation_wheel_value_slider_on_the` **K**: Names a circular colour control with H/S and the right slider as HSV V, distinct from lightness.
5. `nv/ui_pale_violet` **H**: Verify the named purple hue and the light/pale qualifier for this preset rather than assuming that “like white” is sufficiently specific.
6. `nv/ui_smooth_freehand_strokes` **K**: The wording describes making hand-drawn strokes less uneven rather than only smoothing individual pixels.
7. `nv/ui_spectrum` **K**: Names the organized colour variety and does not identify it as the wheel alternative.
8. `nv/ui_tap_vertices_then_double_tap_the_last_vertex` **H**: Gestures and open segments survive, but confirm that the long quoted Close polygon label and Finish label exactly match the shipped controls.
9. `nv/ui_vertical_hint23` **K**: New columns, joined sideways scripts including Mongolian and the integrity of upright combining marks/emoji runs are all separately described.
10. `tdd/ui_about_copyright` **K**: Explicit about-app wording and a separate creator-rights heading.
11. `tdd/ui_about_copyright_licence` **K**: Keeps copyright and licence distinct; licence matches the pinned licence terminology.
12. `tdd/ui_add_images` **K**: Concise add-images action with a picture as the item and insertion as the action.
13. `tdd/ui_add_images_first` **K**: Parallel caption adds the requirement to do this first.
14. `tdd/ui_add_images_then_drag_a_thumbnail_here` **K**: Two sequential actions are explicit; the small preview is the item dragged here after adding images.
15. `tdd/ui_add_to_custom_colours` **K**: Uses the palette/colour vocabulary and qualifies it as the user's own, not simply the currently selected colour.
16. `tdd/ui_an_assembly_can_contain_up_to_20_images` **H**: The second sentence uses a removal verb that can imply discarding a source image; keep the 20-image limit while clarifying which assembly item is removed.
17. `tdd/ui_an_assembly_can_contain_up_to_20_images_86d995` **K**: Short form keeps the inclusive upper limit and the assembly's image group.
18. `tdd/ui_an_paint_assembly_image` **K**: Describes the resulting assembled image and preserves the app name, rather than naming a workspace action.
19. `tdd/ui_an_paint_image` **K**: Short caption identifies an AN Paint image without implying it is necessarily assembled.
20. `tdd/ui_an_paint_image_assembly` **H**: It says image group, but the top-level Image assembly action uses a longer arrangement expression; align the screen title and help routes with that convention.
21. `tdd/ui_an_paint_image_assembly_20_images_placed` **H**: Keeps count of loaded and placed images; hold until the assembly heading is aligned with the exact paired title.
22. `tdd/ui_apply_to_all` **K**: The action is applied to all, not selection of all.
23. `tdd/ui_apply_to_these_images` **K**: Targets these specific images and matches the apply-to-all wording where the scope is not replaced.
24. `tdd/ui_assembly_decoded_output_estimated_editing_render_memory_at` **K**: Three measurements stay distinct and in order; names decoded output and approximate editing/render RAM at original size.
25. `tdd/ui_assembly_output_size` **K**: Identifies size of the combined output, not the specific source file size.
26. `tdd/ui_assembly_png` **K**: Clear descriptive assembly-image filename retaining the exact extension.
27. `tdd/ui_batch_crop` **K**: Expressly crops multiple images together, not merely every selected rectangle in one image.
28. `tdd/ui_batch_crop_images` **K**: Identical matching wording is appropriate for the action and its explanatory caption in this context.
29. `tdd/ui_by_pixels_hold_and_drag_to_place` **K**: Dimensions and placeholders remain in order; hold and drag are both specified.
30. `tdd/ui_catrobat_online_gallery_artwork_by_its_credited_creators` **K**: The gallery remains identified as online, and the artwork is assigned to its named creators.
31. `tdd/ui_catrobat_sticker_gallery` **H**: Sticker remains an English loan with no other distinguishing phrase; confirm it matches the existing source/picker vocabulary.
32. `tdd/ui_common_in` **K**: Keeps a shared dimension followed by its typed unit in the correct order.
33. `tdd/ui_common_in_pixels` **K**: Same shared-dimension label with explicit px rather than the formatted generic unit.
34. `tdd/ui_copy_decoded_image_at_this_size_estimated_loading` **K**: Copy, decoded image at the given size and estimated load/edit RAM stay in separate rows with their slots.
35. `tdd/ui_corners_and_edges_resize_round_handle_rotates` **K**: Corner and edge handles resize, while the round handle rotates.
36. `tdd/ui_could_not_create_the_assembly` **K**: Assembly-creation failure still provides the formatted cause/details slot.
37. `tdd/ui_could_not_decode_the_cropped_region_of` **K**: Refers to decoding the cropped area rather than the whole image; preserves the item slot.
38. `tdd/ui_could_not_load_gallery_image` **K**: Gallery image load failure with a detail slot, not a failed gallery list.
39. `tdd/ui_create_output` **K**: Makes creating the output image explicit rather than starting a new document.
40. `tdd/ui_cropped_thumbnail` **K**: Names a reduced preview image that was cropped and preserves the requested placeholder.
41. `tdd/ui_current_safe_budget_2f_mp` **K**: Clearly a current safe available limit and preserves exact fixed-precision MP format.
42. `tdd/ui_current_safe_editing_budget_s_up_to_2f` **K**: Two formatted quantities stay distinct; excludes extra decoder RAM from the MP estimate.
43. `tdd/ui_custom_colour` **K**: Uses the same personal-colour qualifier as Add to custom colours, and retains the swatch identifier.
44. `tdd/ui_custom_colours_hold_a_swatch_to_replace_it` **K**: Specifies hold-to-replace and keeps the object an individual swatch rather than the whole palette.
45. `tdd/ui_downloading_image` **K**: The temporal wording and explicit downloading action distinguish from completed insertion.
46. `tdd/ui_drag_a_line_then_drag_twice_to_set` **H**: The two dragged bends are present, but verify that the quoted early Finish curve control matches the actual localized caption.
47. `tdd/ui_drag_a_selection_drag_inside_to_move_square` **K**: Retains select/drag, interior move, square handles, circular rotation and width:height lock.
48. `tdd/ui_drag_across_the_ellipse_s_bounding_box` **K**: The diagonal is described as opposite corners of the four-sided box surrounding the oval.
49. `tdd/ui_drag_between_opposite_corners_choose_outline_or_fill` **K**: Opposite corners and a below-control choice of perimeter only or filled interior both survive.
50. `tdd/ui_drag_between_opposite_corners_to_draw_a_five` **K**: Correctly includes five-pointed star and separate outline/fill choice.
51. `tdd/ui_drag_between_opposite_corners_to_draw_a_heart` **K**: The heart figure, diagonal gesture and outline/fill options remain distinct.
52. `tdd/ui_drag_from_the_start_to_the_end_of` **K**: Direct line-start-to-line-end drag, with no extra tap step.
53. `tdd/ui_drag_out_to_expand_in_to_trim_drag` **K**: Outward expands and inward trims; interior drag moves the bounds, Fit/pinch are offered, and the new area uses BG.
54. `tdd/ui_drag_placed_images_to_move_them_hold_and` **K**: Already placed images can move; holding and dragging a small preview is the separate add operation.
55. `tdd/ui_drag_to_erase_with_the_background_colour` **K**: The background-colour phrase matches the existing UI and is clearly used for erasure.
56. `tdd/ui_drag_to_pan_without_drawing_pinch_with_two` **K**: Pan does not draw, and two-finger pan/zoom still works while a drawing tool is active.
57. `tdd/ui_draw_a_crisp_one_pixel_line` **K**: Retains a crisp/visible edge contrast and the exact 1–100 px width range.
58. `tdd/ui_draw_around_an_area_drag_inside_to_move` **H**: The gestures are accurate, but the closing instruction must quote the actual Commit selection control and state it applies the edit.
59. `tdd/ui_draw_with_the_selected_brush_tip_and_size` **K**: Names the selected brush tip and size as separate properties, using the existing brush tool terminology.
60. `tdd/ui_drop_at_a_highlighted_edge_right_top_aligned` **K**: The highlighted perimeter and both right/top and below/left alignment alternatives remain.
61. `tdd/ui_each_px_px_percent_is_relative_to_the` **K**: Preserves all seven slots, the largest-current dimension as percentage basis, and reflow of placed images.
62. `tdd/ui_edit_in_paint` **K**: Clearly specifies transferring the assembly into Paint for editing, not saving it in place.
63. `tdd/ui_enable_android_s_files_or_documents_app_then` **K**: Specifies enabling either exact Android application, followed by another attempt.
64. `tdd/ui_estimated_memory_current_working_budget` **K**: Two independent memory values retain the exact slot order and newline layout.
65. `tdd/ui_fill_text_box_with_bg_colour` **K**: The background-colour term matches the control and targets the text box, not the text.
66. `tdd/ui_fits_the_current_budget` **K**: Says the operation does not exceed the current limit rather than claiming RAM is generally plentiful.
67. `tdd/ui_font_licences` **K**: Matches established licence wording and specifically refers to typeface forms.
68. `tdd/ui_gallery_image` **K**: Identifies the image as coming from the gallery, without suggesting it is already imported.
69. `tdd/ui_give_all_images_the_same_each_image_keeps` **K**: Preserves both dynamic values, each image’s width/height ratio, and unchanged originals and crop settings.
70. `tdd/ui_hide_pixel_grid_800` **H**: Can read as hiding pixel outlines rather than an overlay grid; verify Show and Hide together using the same term.
71. `tdd/ui_hold_a_thumbnail_and_drag_it_here_or` **K**: Both alternatives retain the required gestures: hold-drag, or tap thumbnail then tap workspace.
72. `tdd/ui_hold_or_drag_to_spray_colour` **K**: Names spraying colour and both gestures, matching the Airbrush action.
73. `tdd/ui_honeycomb_colour_swatches_with_a_greyscale_row` **K**: Uses the pinned honeycomb term and explicitly describes a separate black-to-white row.
74. `tdd/ui_image_assembly_workspace_drag_placed_images_or_drop` **K**: Covers moving placed imagery, dropping thumbnails to attach right/bottom, pinch zoom and empty workspace pan.
75. `tdd/ui_image_credits` **K**: Explicitly includes origin, creator and usage terms, not only who drew the picture.
76. `tdd/ui_image_placed_drag_it_to_move_or_hold` **K**: States it was placed and distinguishes move by dragging from adding another held thumbnail.
77. `tdd/ui_image_shown_in_crop_preview` **K**: Names the image shown in crop preview and does not state the crop has been committed.
78. `tdd/ui_image_thumbnails_and_filenames_scroll_horizontally_for_more` **K**: Uses filenames and previews with explicit left/right drag for the rest.
79. `tdd/ui_insert_gallery_image` **K**: A question about inserting an image from the gallery rather than replacing a document.
80. `tdd/ui_invalid_image_attachments` **K**: The error is about image attachments, not a bad file or a failed download.
81. `tdd/ui_lossless_jpeg_xl` **K**: Clear no-data-loss qualifier and exact JPEG XL name.
82. `tdd/ui_magnified_preview` **K**: The enlarged preview is recognizable; ellipsis retained for the setting variant.
83. `tdd/ui_magnified_preview_ea9209` **K**: Same preview wording without ellipsis for the plain caption.
84. `tdd/ui_modified_newest_first` **K**: Keeps modification as the sort basis and newest as a first choice.
85. `tdd/ui_modified_oldest_first` **K**: Oldest-first counterpart changes direction without changing sort criteria.
86. `tdd/ui_no_attachment_fits_within_the_current_coordinate_range` **K**: Preserves current X/Y range and smaller dimensions as remedy, not deleting images.
87. `tdd/ui_no_gallery_images_have_been_inserted` **K**: Uses the established broad image-credit term and says its text is unavailable.
88. `tdd/ui_not_enough_memory_to_inspect_the_gallery_image` **K**: RAM deficiency is for inspecting an image from the gallery, not the whole gallery's load.
89. `tdd/ui_not_placed` **K**: Negative status uses the same placement verb as the completed state.
90. `tdd/ui_original_decoded_image_rgba_4_bytes_pixel_estimated` **K**: All slots, RGBA, four bytes per pixel and the no-resize editing estimate survive in order.
91. `tdd/ui_other_terms` **K**: Indicates additional terms, not another licence identifier or technical options.
92. `tdd/ui_pencil_keeps_crisp_one_pixel_strokes_cursor_drawing` **K**: Consistent pencil term with sharp edges across any selected width.
93. `tdd/ui_percent_of_pixels` **K**: Keeps percentage as a proportion of the formatted pixel reference.
94. `tdd/ui_pinch_to_zoom_drag_to_pan` **K**: Separates pinch to resize view from drag to pan; no change to actual image size implied.
95. `tdd/ui_place_at_least_one_image_in_the_workspace` **K**: Requires at least one placed image in the workspace first, distinct from loading thumbnails.
96. `tdd/ui_placed` **K**: Short placed status is the positive counterpart of Not placed.
97. `tdd/ui_px_drag_an_image_to_move_hold_a` **K**: Exact width/height notation plus dragging an image to move and holding the thumbnail to add.
98. `tdd/ui_quality` **K**: Short quality label keeps the percentage marker and matches save quality meaning.
99. `tdd/ui_rendering_images` **H**: The phrase can denote images already made, not processed; keep both typed counts and ellipsis when revising.
100. `tdd/ui_restore_original_sizes` **K**: Clearly restores original dimensions rather than applying a common fixed size.

## Batch 18: Tai Nüa

Personally reviewed 100 distinct wording records. Batch: **90 keep, 10 hold**. Overall: **1800 reviewed, 1262 keep, 538 hold**. This changes only the review ledger, not Android resources.

1. `tdd/ui_right_arrow_expand` **K**: Identifies the right-pointing arrow as a control that opens or expands the panel.
2. `tdd/ui_same` **K**: Keeps the dynamic name of the dimension being made common.
3. `tdd/ui_same_height` **K**: Short shared-height wording stays distinct from width.
4. `tdd/ui_same_width` **K**: Short shared-width wording matches the height counterpart.
5. `tdd/ui_set_radius_px_then_drag_between_opposite_corners` **H**: Opposite corners and per-rectangle half-short-side limit are present; validate the very long quoted radius label against the actual control and ensure this means corner radius.
6. `tdd/ui_show_pixel_grid_800` **H**: The noun can describe pixel outlines rather than the grid overlay; resolve both Show and Hide together using a shared term.
7. `tdd/ui_shows_the_whole_assembly_image_and_output_sizes` **K**: Shows all assembled imagery without resizing sources or output.
8. `tdd/ui_smooth_freehand_strokes` **K**: Describes making strokes drawn by hand smooth, rather than anti-aliasing individual edges.
9. `tdd/ui_smooth_pixel_edges_anti_aliasing` **K**: Explicitly names smoothing pixel edges and retains the anti-aliasing term, distinct from freehand smoothing.
10. `tdd/ui_some_previews_could_not_be_decoded_you_can` **H**: The delete-like verb can imply deleting file inputs; distinguish removing the affected images from the assembly while keeping the save alternative.
11. `tdd/ui_sort_images_by_filename_or_modification_time` **K**: Keeps filename and modification time as interchangeable sort keys.
12. `tdd/ui_sort_tray` **K**: Specifically identifies sorting the image tray, not the already placed arrangement.
13. `tdd/ui_tap_a_pixel` **K**: Clear touch on exactly one pixel, without a drag gesture.
14. `tdd/ui_tap_an_enclosed_area_adjust_tolerance_for_similar` **K**: Tap inside the enclosing boundary and adjust tolerance around similar colours rather than changing the active fill colour.
15. `tdd/ui_tap_an_image_thumbnail_first` **K**: The thumbnail is the item to tap first, not a placed image.
16. `tdd/ui_tap_the_canvas_to_place_text_and_choose` **K**: Uses the canvas term and preserves placement, choice of typeface and choice of size.
17. `tdd/ui_tap_the_image_to_sample_the_foreground_colour` **K**: Correctly derives foreground colour from the touched image point.
18. `tdd/ui_tap_vertices_then_double_tap_the_last_vertex` **H**: Both double-tap and connected open segments survive; verify exact quoted Finish and Close control labels and make switching off the closure rule clear.
19. `tdd/ui_the_assembly_exceeds_android_s_coordinate_range` **K**: Identifies Android’s X/Y limit rather than file size or memory.
20. `tdd/ui_the_assembly_needs_about_choose_a_smaller_output` **K**: Preserves estimated requirement and smaller output size as remedy.
21. `tdd/ui_the_assembly_output_is_unavailable_reopen_image_assembly` **H**: The wording can assert no output exists and the quoted reopen caption differs from the existing assembly action; distinguish unavailability and use the exact menu name.
22. `tdd/ui_the_attachment_image_is_missing` **K**: States the image required for attachment is missing rather than unplaced.
23. `tdd/ui_the_attachment_image_is_not_placed` **K**: Not-yet-placed wording is consistent with the separate Placed status.
24. `tdd/ui_that_arrangement_overlaps_another_image_use_a_different` **K**: Names overlap and separately allows another edge or removing attached images only from their placement.
25. `tdd/ui_the_first_image_starts_at_the_top_left` **K**: Correct location of the first image at the top left.
26. `tdd/ui_the_gallery_download_is_too_large` **K**: Excessive size refers to the downloaded file, not the gallery itself.
27. `tdd/ui_the_gallery_image_is_unavailable` **K**: Expresses inability to obtain the particular image from the gallery rather than its deletion.
28. `tdd/ui_the_gallery_redirected_outside_its_supported_hosts` **K**: Clearly shows the URL changed to one the app cannot use.
29. `tdd/ui_the_image_could_not_be_downloaded` **K**: Matches the download-progress term and reports that obtaining the image failed.
30. `tdd/ui_the_images_cannot_fit_within_android_s_coordinate` **K**: Names the Android X/Y constraint and advises smaller image sizes.
31. `tdd/ui_the_normalized_image_dimensions_are_outside_android_s` **K**: Specifies the dimensions after equalizing as exceeding Android’s limit.
32. `tdd/ui_the_online_gallery_could_not_be_loaded_check` **K**: Identifies the gallery load failure, internet connection and retry in order.
33. `tdd/ui_third_party_notices` **H**: “Notices from others” is close but can be confused with user notifications; align legal third-party notices with the related licence captions.
34. `tdd/ui_this_image_is_outside_the_supported_catrobat_gallery` **K**: Keeps supported Catrobat gallery as the boundary, not a generic network problem.
35. `tdd/ui_time_unavailable` **H**: Can be read as no time available rather than no timestamp for sorting; identify modification metadata as the thing unavailable.
36. `tdd/ui_too_many_gallery_redirects` **K**: Clearly reports excessive repeat URL redirection, rather than one disallowed domain.
37. `tdd/ui_tool_option` **K**: A selectable option belonging to the tool, not a different tool.
38. `tdd/ui_toolbox_and_tool_options_scroll_for_more` **K**: Names the tools and options, and the ability to drag/scroll for more.
39. `tdd/ui_trim_from_the_original_edges_drag_the_handles` **K**: Starts measuring at original image edges, allows drag or entry, and explicitly says source files do not change.
40. `tdd/ui_trim_in_pixels` **K**: Uses trim action, dynamic side/amount slot and px unit.
41. `tdd/ui_unplace` **K**: Specifies taking the image out of its placement rather than deleting the underlying source.
42. `tdd/ui_width_in` **K**: Existing width term with a placeholder for the unit.
43. `tdd/ui_widths` **K**: The unmarked noun works as the heading for a series of width values.
44. `tdd/ui_you_can_add_more_images_select_fewer_files` **K**: Retains remaining capacity and instructs choosing fewer files.
45. `tdd/ui_jpeg_xl_codec_licences` **K**: Exact JPEG XL name with the licence object explicitly identified as its codec.
46. `tdd/ui_preview_memory_error` **K**: Preserves the item’s detail slot and states the RAM shortfall is specifically for preview.
47. `tdd/ui_trim_in_percent` **K**: Uses the same trim wording as pixels, but with the percent unit instead.
48. `tdd/ui_crop_preview_images` **K**: Both typed quantity variants preserve the dimensions/count and potential movement of attached images if placed inputs are cropped.
49. `tdd/ui_add_palette23` **K**: The terminology matches the pinned colour palette and specifies adding to it.
50. `tdd/ui_added_palette23` **K**: Distinguishes completed addition from the action by retaining the completion marker.
51. `tdd/ui_replace_palette23` **K**: Indicates full palette and specifies selecting the colour to replace.
52. `tdd/ui_edit_palette23` **K**: Names editing the palette without suggesting a different picker.
53. `tdd/ui_replace_with_active23` **K**: Uses the current colour as replacement, rather than treating it as the item replaced.
54. `tdd/ui_remove_palette23` **K**: Makes removal from the palette explicit; does not imply erasing the drawing.
55. `tdd/ui_add_active23` **K**: Identifies adding the active colour, without conflating it with Replace.
56. `tdd/ui_horizontal23` **K**: Describes writing along the width, distinct from the column modes.
57. `tdd/ui_vertical_rl23` **K**: Retains top-to-bottom progression and right-to-left column order.
58. `tdd/ui_vertical_lr23` **K**: Matched alternative switches only the column direction.
59. `tdd/ui_vertical_letters23` **K**: Indicates the settings are about glyphs within vertical text rather than the layout of the whole canvas.
60. `tdd/ui_vertical_mixed23` **K**: Clearly contrasts upright CJK characters and other words turned sideways, with automatic wording.
61. `tdd/ui_vertical_sideways23` **K**: Preserves right-angle sideways rotation and joining the word’s glyphs together.
62. `tdd/ui_vertical_upright23` **K**: Clearly pairs upright orientation with handling each character, not only alphabetic letters.
63. `tdd/ui_top23` **K**: Explicitly aligns the top edge, not the right edge of a vertical line.
64. `tdd/ui_bottom23` **K**: Matches top alignment while naming the distinct bottom edge.
65. `tdd/ui_webp_codec_licences` **K**: Exact WebP name and its codec as the licence object.
66. `tdd/ui_heic_avif_codec_licences` **K**: Both HEIC and AVIF remain in the same codec-licence heading.
67. `tdd/colour20_custom_selected_slot` **K**: Matches the established personal/custom-colour phrase and the exact numbered selection.
68. `tdd/colour20_stored_slot` **K**: Both slots survive and tapping to use is distinguished from the later Replace action saving changes.
69. `tdd/colour20_empty_slot` **K**: Indicates an empty numbered slot and a touch to choose where to save the current colour.
70. `tdd/colour20_save_slot` **K**: Direct save action points at its specific numbered slot.
71. `tdd/colour20_replace_slot` **K**: Explicitly changes the colour in the numbered slot rather than selecting a new slot.
72. `tdd/colour20_saved_slot` **K**: Reports that the colour was already saved to the specified slot.
73. `tdd/gallery_image_component_unavailable` **H**: The component is called absent, which does not cover present but unavailable components. Keep the fact that import did not occur.
74. `tdd/formats22_page_number` **K**: Names the current page number rather than total number of pages.
75. `tdd/formats22_page_preview` **K**: Preview identifies the selected page rather than the active file.
76. `tdd/formats22_page_range` **K**: Instructs entering a number between one and the exact formatted maximum.
77. `tdd/formats22_loading_page` **K**: Preserves page counters and clearly identifies an ongoing preview load.
78. `tdd/formats22_page_dimensions` **K**: All four typed slots and the pixel unit remain in the expected order.
79. `tdd/formats22_preview_unavailable` **K**: Inability to see the preview is clear, with the provided diagnostic intact.
80. `tdd/formats22_preview_memory` **K**: The lack of preview RAM is distinct from opening with smaller available dimensions.
81. `tdd/formats22_pdf_invalid` **K**: Potential file damage and features unsupported by the current Android version remain separate failure reasons.
82. `tdd/formats22_pdf_encrypted` **K**: Preserves required password versus unsupported encryption and saving an unprotected copy before import.
83. `tdd/formats22_pdf_file_size` **K**: Requires some content in the file and retains 512 MiB as its exact inclusive limit.
84. `tdd/formats22_pdf_page_count` **K**: The first page and typed upper bound are retained.
85. `tdd/formats22_pdf_page_index` **K**: Indicates the old selection is no longer usable and asks for a page in this document.
86. `tdd/formats22_pdf_dimensions` **K**: Correctly distinguishes invalid dimensions and dimensions too large to import.
87. `tdd/formats22_pdf_crop` **H**: The wording adds a minimum of 1 px, which the source does not specify. Preserve a nonempty rectangle within the selected page without inventing coordinates or units.
88. `tdd/formats22_pdf_memory` **K**: Distinguishes memory for rendering PDF as an image from the allowed image RAM.
89. `tdd/formats22_base64_description` **K**: Retains lossless content, precise URI prefix, recovery by reopening and the Base64 size overhead.
90. `tdd/formats22_ascii_columns` **K**: Width unit is individual characters, not pixels.
91. `tdd/formats22_ascii_invert` **H**: Bright and black can imply only blacks rather than all dark glyphs; make light and dark groups symmetric.
92. `tdd/formats22_text_not_image` **K**: Says the text lacks a supported image, not that every Base64 string is invalid.
93. `tdd/gallery_use_image` **K**: Concise instruction to use an image, consistent with gallery insertion.
94. `tdd/gallery_copy_credit` **K**: Broad attribution wording includes source, maker and permitted use and is clearly an action to copy.
95. `tdd/gallery_edit_credits` **K**: Edits the same broad record rather than restricting editing to the name of the creator.
96. `tdd/gallery_credit_copied` **K**: Keeps the completion marker in contrast with the Copy action and uses the same exact credits vocabulary.
97. `tdd/gallery_credit_title` **K**: Identifies artwork and retains the associated title slot.
98. `tdd/gallery_credit_publisher` **K**: States Catrobat as the publishing project, distinct from attribution to the maker of each work.
99. `tdd/gallery_credit_gallery` **K**: Short gallery label preserves the field’s value and does not confuse it with the origin or publisher.
100. `tdd/gallery_credit_licence` **K**: Original Catrobat artwork, exact CC BY-SA 4.0 and the dynamic licence detail are preserved.

## Batch 19: Tai Nüa

Personally reviewed 100 distinct wording records. Batch: **93 keep, 7 hold**. Overall: **1900 reviewed, 1355 keep, 545 hold**. This changes only the review ledger, not Android resources.

1. `tdd/gallery_credit_saved` **K**: Uses the same broad attribution/text wording as the matching controls and marks saved completion.
2. `tdd/formats22_ico_size` **K**: Clearly sizes the icon image, not the canvas.
3. `tdd/formats22_ico_description` **K**: Retains selected size, one compressed PNG, fixed range, original proportions and centered transparent square.
4. `tdd/formats22_ico_decode_budget` **K**: Distinguishes icon decode RAM from the allowed image-memory amount.
5. `tdd/formats22_ico_dimensions_error` **K**: The mismatch is with the corresponding picture’s row in the ICO file, not with the file extension.
6. `tdd/formats22_ico_invalid_size` **K**: Every allowed value and the pixel unit are retained.
7. `tdd/save20_dither` **K**: Specifies pixels of differing neighbouring colours and keeps dithering exact rather than mixing colours indiscriminately.
8. `tdd/save20_bmp_description` **K**: Preserves 24-bit RGB, no compression, exact colours and larger files.
9. `tdd/save20_bmp_size_limit` **K**: Identifies the BMP file-size limit rather than a per-side dimension limit.
10. `tdd/save20_gif_size_limit` **K**: Exact 65,535 px cap applies to each GIF side.
11. `tdd/save20_unsupported_tagged_colour` **K**: Preserves both input formats, unsupported profile, and conversion to sRGB PNG in a colour-managed editor before importing.
12. `tdd/ui_cursor_ink30` **K**: Points to drawing with the existing cursor marker rather than general drawing.
13. `tdd/ui_cursor_help31` **K**: Drag, tap the on-screen button, drag/draw and tap to stop are all preserved; both Draw and Drawing match the pinned short action caption.
14. `tdd/ui_cursor_settings31` **K**: Identifies the cursor drawing settings and preserves the invocation ellipsis.
15. `tdd/ui_cursor_marker_help31` **K**: Enlarges only the cursor marker and preserves the width of the brush stroke.
16. `tdd/ui_gimp_translations31` **K**: Explicit translator information alongside the licence heading; not art attribution.
17. `tdd/ui_cursor_pan_draw32` **K**: Indicates moving the cursor while initiating drawing, then a further tap to stop.
18. `tdd/ui_cursor_pan_move32` **K**: Positions the cursor first and identifies the drawing button as the separate start action.
19. `tdd/ui_cursor_tap_hint37` **K**: Specifies tapping the cursor itself, for both start and stop.
20. `tdd/ui_normalize_width_intro` **K**: Equalizes width while keeping each ratio, exact image count, original files and crop settings unchanged.
21. `tdd/ui_normalize_height_intro` **K**: Parallel height variant preserves count, ratios and the unchanged-source/crop qualification.
22. `tdd/ui_normalize_width_info` **K**: Preserves per-image width, range of heights, percentage of the current maximum width and reflow.
23. `tdd/ui_normalize_height_info` **K**: Keeps counterpart height and width order, and bases the percentage on the largest current height.
24. `tdd/ui_normalize_width_input_percent` **K**: Explicit shared width input as a percentage of the typed pixel base.
25. `tdd/ui_normalize_height_input_percent` **K**: Matched height counterpart changes only the dimension.
26. `tdd/ui_pixel_grid_help33` **H**: The phrase can be understood as showing pixel outlines rather than the grid overlay. Resolve terminology with the paired grid controls; retain 800% and ruler positions.
27. `tdd/ui_search_english34` **K**: Clearly a search command using either named language.
28. `tdd/gallery_description` **K**: Quoted uses match the candidate controls; the copyable title, publisher, origin and licence, creator notices and compatible-licence requirement are distinguished.
29. `tdd/gallery_credit_edit_hint` **K**: Retains notice and creator obligations, recording edits, removing unused source entries and editing the text below.
30. `tdd/ui_irasutoya_help34` **K**: Keeps Use image, the search languages and Japanese page text, 21-or-more commercial threshold and special collaboration terms; credits destination matches the current labels and kept candidate.
31. `tdd/ui_openclipart_help34` **K**: The next-to-Large-PNG action, CC0 and the exact source/credits route are retained.
32. `tdd/ui_gallery_unsupported34` **K**: The image is outside the selected source; does not assert impossible decoding.
33. `tdd/ui_open_artwork34` **K**: Artwork page first, then the exact Use image action.
34. `tdd/ui_creator_on_source34` **K**: Explicitly points to the source page to identify the contributor.
35. `tdd/ui_irasutoya_credit34` **K**: Keeps creator rights, Irasutoya’s own terms and non-CC status separate.
36. `tdd/legacy_credits_title` **K**: References the previously saved broad credit records, not just recently added names.
37. `tdd/legacy_credits_hint` **K**: Explains possible other-image origin and offers adding the chosen source record or exporting the complete text.
38. `tdd/legacy_credits_add` **K**: Names the selected credit information and specific destination image.
39. `tdd/legacy_credits_save_text` **K**: Saves selected credit as text, not as an image.
40. `tdd/legacy_credits_existing` **K**: Reports prior credit for that source and that its text was retained.
41. `tdd/legacy_credits_added` **K**: The added action is complete and modifies the credit on this image rather than claiming a source import.
42. `tdd/commons_import_svg_changes` **K**: Preserves exact SVG-to-PNG, Boolean and other machine-like tokens; original dimensions clear.
43. `tdd/commons_import_raster_changes` **K**: Technical alpha is retained alongside image compositing and exact white background.
44. `tdd/commons_credit_copy_failed` **K**: Copy failure references the same complete attribution as the corresponding action.
45. `tdd/commons_credit_copy_failed_reason` **K**: Matching copy failure with exact reason slot included.
46. `tdd/ui_gallery_artwork_catrobat_and_its_credited_creators_cc` **K**: Keeps Catrobat, named creators, default source licence exception and obligations when sharing modified artwork.
47. `tdd/ui_hue_and_saturation_spectrum_lightness_slider_on_the` **K**: Names H and S plus right-side lightness L, distinct from the V setting.
48. `tdd/ui_hue_and_saturation_wheel_value_slider_on_the` **K**: Names circular H/S selector and the right slider’s value V, distinct from the lightness variant.
49. `tdd/ui_pale_violet` **H**: English Violet is retained, but verify the pale qualifier and a consistent term with the pinned purple colour options.
50. `tdd/ui_spectrum` **K**: A descriptive colour spectrum label remains distinct from the wheel.
51. `tdd/ui_vertical_hint23` **K**: Preserves new columns, unbroken joined scripts including Mongolian, and combining marks and emoji sequences kept together in upright mode.
52. `tdd/ui_casual` **H**: Daily-use lettering is not necessarily a casual style; distinguish it from the default and cursive alternatives.
53. `tdd/ui_cursive` **K**: Joined handwritten glyphs explain cursive rather than simply its italic angle.
54. `tdd/ui_monospace` **K**: Every written character has the same width, not merely narrow outlines.
55. `tdd/ui_sans_condensed` **K**: Sans construction stays unadorned and the qualifier identifies narrow glyphs, not thin strokes.
56. `tdd/ui_sans_light` **K**: Light stroke weight is indicated as thinner relative to other options but not the thinnest.
57. `tdd/ui_sans_medium` **K**: Middle stroke weight is clear from its position in the matched series.
58. `tdd/ui_sans_serif` **K**: Describes lack of small end strokes, distinguishing the sans family.
59. `tdd/ui_sans_thin` **K**: The thinnest-stroke qualifier distinguishes it from the Light option.
60. `tdd/ui_serif` **K**: Describes letters with small terminal strokes rather than a decorative underline.
61. `tdd/ui_lossless_format` **K**: The candidate explicitly keeps all data and the formatted codec name.
62. `tdd/ui_image_codec_licences` **K**: The read/write tools and purpose identify image codecs and their licences.
63. `tdd/formats22_ascii_label` **K**: Names picture made of ASCII characters rather than ordinary text.
64. `tdd/formats22_dib_size_limit` **K**: The limit belongs to DIB file size, not image dimensions.
65. `tdd/formats22_page_description` **K**: Two metadata slots and total count survive, and the selected page is edited as an image.
66. `tdd/commons_credit_copy_out_of_memory` **K**: Reports not enough RAM to copy the same broad credit record named by the action.
67. `tdd/commons_metadata_http_error` **K**: Identifies Commons metadata and preserves HTTP and its status placeholder.
68. `tdd/commons_metadata_response_too_large` **K**: Names the returned metadata exceeding the allowed response limit, not a size cap on the requested map.
69. `tdd/commons_metadata_query_failed` **K**: Reports failure to obtain Commons file metadata, not a corrupted page.
70. `tdd/ui_assembly_target_x` **K**: X coordinate explicitly uses pixels measured from the left.
71. `tdd/ui_assembly_target_y` **K**: Y coordinate explicitly uses pixels measured from the top.
72. `tdd/ui_assembly_unknown_image` **K**: Selected image no longer present in this assembly, rather than a general read failure.
73. `tdd/commons_metadata_not_file_page` **K**: Denies the specific Commons file-page type.
74. `tdd/commons_metadata_original_mismatch` **K**: Uses the complete attribution category in a mismatch against the selected original file.
75. `tdd/commons_metadata_field_too_large` **K**: Specific attribution field and text-length cap survive; not the byte size of a download.
76. `tdd/commons_metadata_cache_failed` **K**: The failed save/retain object is the full Commons attribution record.
77. `tdd/commons_download_original_mismatch` **K**: Explicitly says the download switched to a different original file.
78. `tdd/commons_blank_maps` **K**: Describes blank maps as an empty or blank map figure, without limiting it to labels.
79. `tdd/commons_check_file_licence` **K**: Keeps per-file creator, licence and required attribution separate, and says modifications may be adaptations.
80. `tdd/ui_an_image_cannot_attach_to_itself_or_one` **K**: Prohibits attaching the image both to itself and to an image already attached to it.
81. `tdd/ui_catrobat_s_own_artwork_uses_cc_by_sa` **K**: Preserves licence, proper creator credit, adaptations under the same terms, separate notices and consistent exact file route.
82. `tdd/ui_could_not_export_source_code` **K**: Identifies source-code export as the thing that failed, not constructing a build.
83. `tdd/ui_credits_terms` **H**: The credits heading can mean only creator information; check broader source and notice terms alongside the usage terms heading.
84. `tdd/ui_drag_from_the_tail_towards_the_arrowhead_choose` **K**: Preserves arrow-tail to arrowhead direction and the outline/fill choice.
85. `tdd/ui_draw_soft_watercolor_strokes_strength_controls_how_strongly` **H**: The cue reads like background overlap percent; verify the exact Strength control label rather than changing the intended Watercolor setting.
86. `tdd/ui_estimates_include_the_current_canvas_and_clipboard_sampled` **K**: Preserves source and clipboard, sampled decode/working buffers, variable use, smaller copies losing details, selected opaque BG and untouched original file.
87. `tdd/ui_export_this_version_s_source_code` **K**: Names export, this app version and source code, retaining ellipsis.
88. `tdd/ui_icon_licences` **K**: Icon licence uses the same icon-image term as the format and credits screens.
89. `tdd/ui_icon_licences_kde_breeze` **K**: Uses exact KDE Breeze and distinguishes the specific licence from the generic icon heading.
90. `tdd/ui_icons_artwork` **K**: Lists icons and created artwork as separate classes.
91. `tdd/ui_icons_fonts_artwork_credits` **H**: The creator-focused wording needlessly narrows credits for fonts, artwork and icons; keep categories and broaden the attribution heading.
92. `tdd/ui_open_source_credits_and_notices` **K**: The exact open source qualifier is retained; credit and notices are separately named.
93. `tdd/ui_source_code_exported_including_build_scripts_and_licence` **K**: Source code export success, build scripts and bundled licence notices are all distinct.
94. `tdd/gallery_external_link_no_handler` **K**: Android could not locate an app to open this link, not a failed page download.
95. `tdd/commons_metadata_ambiguous_file` **K**: Returned metadata does not identify which file, retaining ambiguity instead of alleging corruption.
96. `tdd/commons_metadata_unavailable` **H**: May say file metadata does not exist; preserve the unavailable state without overclaiming.
97. `tdd/commons_metadata_invalid_page` **K**: Names the Commons page for origin, authorship and usage terms and labels it invalid.
98. `tdd/commons_svg_png_encode_failed` **K**: Failed to make a PNG file from the blank map; consistent map-category wording.
99. `tdd/formats22_tiff_compression` **K**: Names reducing file size without losing data, and keeps Deflate exact.
100. `tdd/formats22_tiff_description` **K**: Keeps one RGB page, unchanged pixels, a possible reduction of size, and disabling compression for uncompressed TIFF.

## Batch 20: Tai Nüa and Western Huasteca Nahuatl

Personally reviewed 100 distinct wording records. Batch: **73 keep, 27 hold**. Overall: **2000 reviewed, 1428 keep, 572 hold**. This changes only the review ledger, not Android resources.

1. `tdd/formats22_dib_description` **K**: Keeps uncompressed Windows DIB, exact 24-bit depth and conditional BMP-header alternative.
2. `tdd/ui_pencil_crisp_adjustable_strokes` **K**: Matches the pinned pencil term and describes clearly defined edges at any picked width.
3. `tdd/ui_assembly_exact_position` **K**: Concise exact-position heading without a claim about image size.
4. `tdd/ui_assembly_position_help` **K**: Retains top-left, integer X/Y from zero, unchanged other positions, later images on top, expansion and unchanged crops/sizes.
5. `tdd/ui_assembly_position_nonnegative` **K**: Both coordinates must be whole numbers within the exact inclusive bounds.
6. `tdd/ui_add_up_to_20_images_with_android_s` **H**: Hold the long assembly guide until named sorting, crop, placement, Unplace and output controls match the pinned screen labels.
7. `tdd/ui_help23` **H**: Hold this compact help until the exact Draw/Navigation, source-credit and save routes are reconciled; preserved paragraph/technical values are not sufficient.
8. `tdd/ui_the_arrow_on_the_left_directly_below_the` **H**: Hold the full editor guide pending control-path and terminology audit, especially imported transparency versus the opaque canvas and the three licence controls.
9. `nhw/commons_blank_maps` **H**: The phrase describes maps without place names, narrowing the blank-map category; verify intended meaning against the catalogue.
10. `nhw/ui_about_copyright_licence` **K**: Matches the existing About/copyright phrase and adds a distinct licence item.
11. `nhw/ui_an_image_cannot_attach_to_itself_or_one` **K**: Both exclusions are explicit: itself and an image already attached to it.
12. `nhw/ui_an_paint_assembly_image` **K**: Refers to the image AN Paint made by combining inputs, not the working area.
13. `nhw/ui_assembly_decoded_output_estimated_editing_render_memory_at` **H**: The decoded row reads as the picture the app opens; distinguish its measured footprint from the estimated editing/render footprint at original size.
14. `nhw/ui_catrobat_online_gallery_artwork_by_its_credited_creators` **K**: Preserves online Catrobat gallery and the separately credited makers.
15. `nhw/ui_catrobat_sticker_gallery` **H**: Sticker is left as an English loan; confirm the insert/gallery scope and acceptable labelling before clearing.
16. `nhw/ui_common_in` **K**: Preserves the common measurement and dynamic unit as separate slots.
17. `nhw/ui_common_in_pixels` **K**: Retains the common measurement with pixels rather than the general unit slot.
18. `nhw/ui_copper` **K**: Clear colour/material loan consistent with the preset family.
19. `nhw/ui_copy_decoded_image_at_this_size_estimated_loading` **H**: The first and second rows refer to pictures rather than size of the copy and its decoded footprint; keep all three measurements and RAM distinct.
20. `nhw/ui_could_not_decode_the_cropped_region_of` **K**: Reports a decoding failure of the retained part of the formatted image, not the whole file.
21. `nhw/ui_could_not_export_source_code` **H**: Generic saving of source code may miss export to a separate destination; align with the paired export command and result.
22. `nhw/ui_current_safe_editing_budget_s_up_to_2f` **K**: Keeps current safe editing RAM and MP bounds distinct, explicitly excluding the additional decode RAM from the latter estimate.
23. `nhw/ui_cursive` **K**: Clear standard typography loan for cursive, distinct from casual lettering.
24. `nhw/ui_custom_colour` **K**: Personal/custom colour qualifier and exact swatch identifier retained.
25. `nhw/ui_downloading_image` **K**: Names the image arriving over the internet and ongoing download, not inserting a local file.
26. `nhw/ui_drag_a_line_then_drag_twice_to_set` **K**: Both committed bends plus earlier Finish curve are explicit; the quoted action matches the existing label.
27. `nhw/ui_drag_between_opposite_corners_choose_outline_or_fill` **K**: Opposite-corner gesture and the exact existing Outline and Fill choices survive.
28. `nhw/ui_drag_between_opposite_corners_to_draw_a_five` **K**: Five-pointed star plus diagonal and same two exact fill/outline choices.
29. `nhw/ui_drag_between_opposite_corners_to_draw_a_heart` **K**: Heart gesture and both exact options are present.
30. `nhw/ui_drag_from_the_start_to_the_end_of` **K**: Preserves dragging from the line’s beginning to its end.
31. `nhw/ui_drag_from_the_tail_towards_the_arrowhead_choose` **K**: Arrow tail to arrowhead is clear and both confirmed outline/fill captions match.
32. `nhw/ui_add_images_then_drag_a_thumbnail_here` **K**: Adds images first and then drags a small image/thumbnail here.
33. `nhw/ui_add_to_custom_colours` **K**: Saves the current colour specifically to the personal colour collection.
34. `nhw/ui_batch_crop` **H**: Could mean identical image content is kept across all inputs; use wording for applying one crop operation to multiple selected images.
35. `nhw/ui_batch_crop_images` **H**: Selected inputs are named, but same-portion wording remains ambiguous; pair with the short Batch crop label.
36. `nhw/ui_by_pixels_hold_and_drag_to_place` **K**: All four placeholders retain width/height order, followed by hold plus drag to place.
37. `nhw/ui_corners_and_edges_resize_round_handle_rotates` **K**: Corner/edge handles resize and circular handle rotates; actions remain separate.
38. `nhw/ui_cropped_thumbnail` **K**: Identifies thumbnail and retained crop portion and keeps the exact formatted value.
39. `nhw/ui_custom_colours_hold_a_swatch_to_replace_it` **K**: Uses consistent custom-colour wording and commands holding a single swatch to replace it.
40. `nhw/ui_drag_a_selection_drag_inside_to_move_square` **K**: Preserves selection, inside movement, square resize and round rotation handles, then maintains proportions.
41. `nhw/ui_drag_across_the_ellipse_s_bounding_box` **K**: Clear diagonal across the enclosing rectangle, not a line along the ellipse itself.
42. `nhw/ui_drag_out_to_expand_in_to_trim_drag` **H**: Gestures and BG use survive, but Fit stays in English rather than the actual Ma nochi nesi button caption.
43. `nhw/ui_drag_placed_images_to_move_them_hold_and` **K**: Distinguishes images already placed from holding and dragging a thumbnail to add it.
44. `nhw/ui_drag_to_erase_with_the_background_colour` **K**: Uses the established background colour and makes erasure through that colour clear.
45. `nhw/ui_drag_to_pan_without_drawing_pinch_with_two` **K**: Retains pan without drawing and two-finger zoom/pan even when drawing tools are selected.
46. `nhw/ui_draw_a_crisp_one_pixel_line` **H**: “Clearly visible” can mean attractive or readable, not crisp-edged. Preserve the exact 1–100 px range and name the pencil edge behavior.
47. `nhw/ui_draw_around_an_area_drag_inside_to_move` **K**: Free-form outline and each handle gesture survive; exact Commit selection is expressed as applying the edit.
48. `nhw/ui_draw_soft_watercolor_strokes_strength_controls_how_strongly` **H**: Strength wording closely matches the slider, but check the user-visible caption includes its existing percentage qualifier and that the blend interaction remains explicit.
49. `nhw/ui_draw_with_the_selected_brush_tip_and_size` **K**: Uses the selected brush tip and size, not an instruction to select a different brush.
50. `nhw/ui_drop_at_a_highlighted_edge_right_top_aligned` **K**: The highlighted edge is the drop target and the right/top and below/left alignments are distinct.
51. `nhw/ui_each_px_px_percent_is_relative_to_the` **K**: Preserves all seven slots and identifies the largest current selected dimension as the percentage basis, with placed-image reflow.
52. `nhw/ui_enable_android_s_files_or_documents_app_then` **K**: Clearly enables one of the two exact Android applications and then directs a retry.
53. `nhw/ui_estimates_include_the_current_canvas_and_clipboard_sampled` **H**: Check that the decode is explicitly sampled, not merely an ordinary open. Retain the English technical annotations only if necessary, and preserve opaque BG and unchanged source.
54. `nhw/ui_export_this_version_s_source_code` **K**: Clear code export for this exact version, with ellipsis.
55. `nhw/ui_fill_text_box_with_bg_colour` **K**: Uses the pinned background-colour phrase and targets the text box rather than the glyphs.
56. `nhw/ui_font_licences` **K**: Licence object is the typeface family, distinct from artwork and icon licences.
57. `nhw/ui_give_all_images_the_same_each_image_keeps` **H**: The closing clause speaks of the portion already kept, not the crop settings themselves; preserve both unchanged settings and originals.
58. `nhw/ui_gold` **K**: Common concise gold preset loan consistent with the copper/silver family.
59. `nhw/ui_hide_pixel_grid_800` **K**: Clear hide action, pixel grid and 800%-and-above parameter.
60. `nhw/ui_hold_a_thumbnail_and_drag_it_here_or` **K**: Both alternatives remain: drag while holding, or tap thumbnail and then tap the workspace.
61. `nhw/ui_hold_or_drag_to_spray_colour` **K**: Both gestures use the colour spray through air, aligned with airbrush behavior.
62. `nhw/ui_honeycomb` **K**: Concise transparent descriptor for the honeycomb control.
63. `nhw/ui_honeycomb_colour_06x` **K**: Same palette term and exact hexadecimal token.
64. `nhw/ui_honeycomb_colour_swatches_with_a_greyscale_row` **H**: The greyscale qualifier may be understood as dark-to-clear or clean rather than black through grey to white; use the greyscale contrast explicitly.
65. `nhw/ui_hue_and_saturation_spectrum_lightness_slider_on_the` **K**: Names hue and saturation spectrum and the right lightness control without mixing it with HSV value.
66. `nhw/ui_hue_and_saturation_wheel_value_slider_on_the` **K**: Names the wheel and explicitly marks the right control HSV value.
67. `nhw/ui_icon_licences` **K**: Separate licences for icons; concise and distinct from fonts/artwork.
68. `nhw/ui_icon_licences_kde_breeze` **K**: Keeps exact KDE Breeze name and consistent licence wording.
69. `nhw/ui_icons_artwork` **H**: The artwork noun requires evidence for visual art in this context rather than a generic craft term.
70. `nhw/ui_icons_fonts_artwork_credits` **H**: Heading limits the record to who made items, and the art term needs the same check as Icons & artwork.
71. `nhw/ui_image_assembly_workspace_drag_placed_images_or_drop` **K**: Retains movement of placed images and snapping thumbnails at right/bottom, plus pinch zoom and panning in empty space.
72. `nhw/ui_image_credits` **H**: The draft says maker or origin but omits the licence and broader credit contents; align this heading and references to it.
73. `nhw/ui_image_placed_drag_it_to_move_or_hold` **K**: Completed placement is explicit and distinct from moving it or dragging a new held thumbnail.
74. `nhw/ui_image_shown_in_crop_preview` **K**: Identifies the image during preview of the retained crop portion.
75. `nhw/ui_image_thumbnails_and_filenames_scroll_horizontally_for_more` **K**: Names the previews and individual filenames, and directions for horizontal scrolling.
76. `nhw/ui_invalid_image_attachments` **K**: The error describes inability to connect images in the requested way, not corrupted source data.
77. `nhw/ui_lossless_jpeg_xl` **K**: Explicitly states JPEG XL does not change pixels.
78. `nhw/ui_magnified_preview` **H**: Imperative “first look bigger” reads as an instruction; use a noun/setting phrase for the enlarged preview.
79. `nhw/ui_magnified_preview_ea9209` **H**: No-ellipsis variant needs the same title grammar as the ellipsis counterpart.
80. `nhw/ui_modified_newest_first` **K**: Sorts by modification time, newest first rather than newest file creation.
81. `nhw/ui_monospace` **K**: Clear each glyph has the same width; use of letra can serve as a concise typography label.
82. `nhw/ui_no_attachment_fits_within_the_current_coordinate_range` **K**: Keeps attachment and X/Y coordinate limit and suggests smaller sizes.
83. `nhw/ui_no_gallery_images_have_been_inserted` **H**: Limits absence to author or origin text; the app is reporting no complete credit record including usage terms.
84. `nhw/ui_not_enough_memory_to_inspect_the_gallery_image` **K**: RAM shortage is explicitly for inspecting an image from the gallery.
85. `nhw/ui_open_source_credits_and_notices` **H**: “Source code everyone can see” does not establish open source; name its notices and give attribution its full scope.
86. `nhw/ui_original_decoded_image_rgba_4_bytes_pixel_estimated` **H**: RGBA, four bytes per pixel and no resize survive but the decoded row reads as an image, not its decoded memory amount.
87. `nhw/ui_other_terms` **K**: Concise additional conditions, appropriate to a terms tab.
88. `nhw/ui_pencil_keeps_crisp_one_pixel_strokes_cursor_drawing` **H**: “Well visible” does not specify a crisp edge distinct from smoothed/antialiased; keep the correct pencil label and any width.
89. `nhw/ui_percent_of_pixels` **K**: Preserves percentage of the exact formatted pixel base.
90. `nhw/ui_pinch_to_zoom_drag_to_pan` **K**: Separates two-finger zoom from dragging to pan, without changing actual image size.
91. `nhw/ui_px_drag_an_image_to_move_hold_a` **K**: Keeps the formatted dimension pair and separate move/hold actions.
92. `nhw/ui_quality` **K**: Contextually clear save quality setting including percent notation.
93. `nhw/ui_rendering_images` **H**: The phrase can indicate images already made; distinguish processing progress and retain both counters and ellipsis.
94. `nhw/ui_right_arrow_expand` **K**: Identifies the right arrow and expansion/opening of the panel.
95. `nhw/ui_same` **K**: Common dimension heading retains the specific dynamic dimension.
96. `nhw/ui_same_height` **K**: Short shared height caption distinct from width.
97. `nhw/ui_same_width` **K**: Matching shared width counterpart uses the width term.
98. `nhw/ui_sans_condensed` **K**: Describes narrower glyph width and leaves the parenthetic typeface identifier clear.
99. `nhw/ui_sans_light` **H**: “Not very thin” can describe medium rather than light. Verify light stroke weight very clearly relative to Medium and Thin.
100. `nhw/ui_sans_medium` **K**: Describes a stroke neither very thin nor thick and keeps Medium visibly distinct.

## Batch 21: Western Huasteca Nahuatl

Personally reviewed 100 distinct wording records. Batch: **91 keep, 9 hold**. Overall: **2100 reviewed, 1519 keep, 581 hold**. This changes only the review ledger, not Android resources.

1. `nhw/ui_sans_thin` **K**: Explicitly labels the very thin Sans stroke weight and keeps the family identifier.
2. `nhw/ui_set_radius_px_then_drag_between_opposite_corners` **H**: Retains corner radius, opposite-corner drag and half the shorter side; confirm the long quoted label is exact and does not imply the radius of the whole rectangle.
3. `nhw/ui_show_pixel_grid_800` **K**: Matches Hide using the same pixel-grid term and preserves 800%-and-above.
4. `nhw/ui_shows_the_whole_assembly_image_and_output_sizes` **K**: Displays the whole layout without resizing the images or the output.
5. `nhw/ui_silver` **K**: Clear conventional silver preset loan, parallel to gold and copper.
6. `nhw/ui_smooth_freehand_strokes` **K**: Describes smoothing strokes drawn by hand rather than smoothing pixel boundaries.
7. `nhw/ui_smooth_pixel_edges_anti_aliasing` **K**: Names edge smoothing and retains anti-aliasing explicitly.
8. `nhw/ui_some_previews_could_not_be_decoded_you_can` **K**: Preview decode failure and both available responses survive, without claiming the app deleted anything.
9. `nhw/ui_sort_images_by_filename_or_modification_time` **K**: Sorts by each filename or its modification time as separate options.
10. `nhw/ui_sort_tray` **H**: Says sort pictures generally; identify the tray to avoid implying it rearranges placed images.
11. `nhw/ui_source_code_exported_including_build_scripts_and_licence` **K**: Preserves source code export, build scripts for this version and licence notices.
12. `nhw/ui_spectrum` **K**: Clear spectrum selector name, distinct from the colour wheel.
13. `nhw/ui_strikethrough` **K**: A line placed in the middle of text distinguishes strikethrough from underline.
14. `nhw/ui_tap_a_pixel` **K**: One-pixel touch and immediate release are explicit.
15. `nhw/ui_tap_an_enclosed_area_adjust_tolerance_for_similar` **K**: Names tapping inside the enclosed space and tolerance for including similar colour values.
16. `nhw/ui_tap_an_image_thumbnail_first` **K**: The initial touch targets a preview thumbnail, not the placed image.
17. `nhw/ui_tap_the_canvas_to_place_text_and_choose` **K**: Preserves touch on the canvas, text placement, then typeface/size selection.
18. `nhw/ui_tap_the_image_to_sample_the_foreground_colour` **K**: Uses the established foreground concept and takes the sampled value from the image.
19. `nhw/ui_tap_vertices_then_double_tap_the_last_vertex` **K**: Retains vertex taps, double-tap to close, Finish alternative and an open connected line setting.
20. `nhw/ui_that_arrangement_overlaps_another_image_use_a_different` **K**: Names the overlap and offers another edge or unplacing only the attachments.
21. `nhw/ui_the_attachment_image_is_missing` **K**: Identifies the attached image as missing, distinct from mere absence of a placement.
22. `nhw/ui_the_first_image_starts_at_the_top_left` **K**: Correct first-image origin at the upper-left corner.
23. `nhw/ui_the_gallery_download_is_too_large` **K**: The item from the gallery is too large, not the gallery or its index.
24. `nhw/ui_the_gallery_redirected_outside_its_supported_hosts` **K**: The changed image URL is not supported by the app. No claim of bad file extension.
25. `nhw/ui_the_image_could_not_be_downloaded` **K**: Uses the same internet acquisition verb as the Download progress state to indicate failure.
26. `nhw/ui_the_images_cannot_fit_within_android_s_coordinate` **K**: Names X/Y coordinate feasibility and the option to choose smaller images.
27. `nhw/ui_the_normalized_image_dimensions_are_outside_android_s` **K**: Correctly names normalized dimensions beyond the Android range.
28. `nhw/ui_the_online_gallery_could_not_be_loaded_check` **K**: Distinguishes online gallery load failure from checking internet and retrying.
29. `nhw/ui_third_party_notices` **H**: Restricts the third parties to those who made this project; third-party material can include external dependencies and other rightsholders.
30. `nhw/ui_sans_serif` **K**: Describes lack of small stroke-end details, a correct sans/serif distinction.
31. `nhw/ui_serif` **K**: Matches the sans counterpart, here with small terminal strokes.
32. `nhw/ui_credits_terms` **H**: Credit should cover source and notices as well as who made the work; retain the conditions heading.
33. `nhw/ui_modified_oldest_first` **K**: Records the oldest modification first with wording aligned to newest-first.
34. `nhw/ui_pale_violet` **H**: The modifier can mean clean or clear rather than pale; verify the intended light violet shade.
35. `nhw/ui_this_image_is_outside_the_supported_catrobat_gallery` **K**: Keeps an image outside the supported Catrobat gallery, not outside Catrobat as a whole.
36. `nhw/ui_time_unavailable` **H**: Can imply that no hour exists; identify unavailable timestamp metadata in this sorter.
37. `nhw/ui_too_many_gallery_redirects` **K**: Too many redirects are clear and app no longer follows them; no unverified claim about any one destination.
38. `nhw/ui_tool_option` **K**: Names the setting the user can vary for this tool.
39. `nhw/ui_toolbox_and_tool_options_scroll_for_more` **K**: Retains toolbox and options plus dragging to see more.
40. `nhw/ui_top` **K**: Correct short vertical location label for the upper side.
41. `nhw/ui_trim_from_the_original_edges_drag_the_handles` **K**: Trim starts at original edges, drag/number entry are separate, source file untouched.
42. `nhw/ui_trim_in_pixels` **K**: Correct unit and retains exact side or measurement label slot.
43. `nhw/ui_unplace` **K**: Removes the placement rather than deleting the source image.
44. `nhw/ui_wheel` **K**: Concise colour wheel name, consistent with the nearby H/S controls.
45. `nhw/ui_widths` **K**: The width noun is clear for a group of values in this UI.
46. `nhw/ui_agpl_licence` **K**: Exact AGPL identifier and clear licence subject.
47. `nhw/ui_jpeg_xl_codec_licences` **K**: Correct JPEG XL codec licences, not a licence for images.
48. `nhw/ui_gnu_agpl_licence` **K**: GNU AGPL exact with the licence context.
49. `nhw/ui_preview_memory_error` **K**: Retains the formatted item and insufficient memory for its preview.
50. `nhw/ui_trim_in_percent` **K**: Names the trim amount in percent rather than in pixels.
51. `nhw/ui_crop_preview_images` **K**: Both plural forms preserve the transferred dimensions/count and the conditional repositioning of images attached to placed inputs.
52. `nhw/ui_add_palette23` **K**: Explicit save into the palette collection, not selecting colour with the picker.
53. `nhw/ui_added_palette23` **K**: Completion is distinguished from the action and names the same palette.
54. `nhw/ui_replace_palette23` **K**: The palette is already full and user is told to select a colour to replace.
55. `nhw/ui_edit_palette23` **K**: Names changing contents of the palette rather than a brush option.
56. `nhw/ui_replace_with_active23` **K**: The active colour is the replacement value, not the value being discarded.
57. `nhw/ui_remove_palette23` **K**: Removes from the palette rather than deleting a colour in the image.
58. `nhw/ui_add_active23` **K**: Save/add targets the currently active colour.
59. `nhw/ui_horizontal23` **H**: “On its side” can denote a glyph orientation rather than the horizontal text layout; distinguish from the Sideways glyph setting.
60. `nhw/ui_vertical_rl23` **K**: Correct downwards glyph flow and right-to-left progression for successive columns.
61. `nhw/ui_vertical_lr23` **K**: Matched variant switches only the order of columns.
62. `nhw/ui_vertical_letters23` **K**: Identifies glyphs inside top-to-bottom text, not UI layout direction.
63. `nhw/ui_vertical_mixed23` **K**: Retains automatic choice with upright CJK and sideways words.
64. `nhw/ui_vertical_sideways23` **K**: Words stay intact when turned on their sides.
65. `nhw/ui_vertical_upright23` **K**: The character-by-character qualifier covers more than alphabetic letters and retains upright meaning.
66. `nhw/ui_vertical_hint23` **K**: Keeps new columns, Mongolian and joining, and grouped combining marks and emoji in upright mode.
67. `nhw/ui_top23` **K**: Aligns to the top edge and does not use horizontal left/right terms.
68. `nhw/ui_bottom23` **K**: Bottom counterpart is explicit and terminology matches the top version.
69. `nhw/ui_webp_codec_licences` **K**: Accurate WebP codec-licence caption.
70. `nhw/ui_heic_avif_codec_licences` **K**: Both HEIC and AVIF remain distinct named codecs in one licensing heading.
71. `nhw/colour20_custom_selected_slot` **K**: Personal colour collection and selected slot number are separately identified.
72. `nhw/colour20_stored_slot` **K**: Distinct tap to use, edit, and Replace to save; both exact slots remain.
73. `nhw/colour20_empty_slot` **K**: The numbered slot is empty, and tap chooses where to save the current colour rather than performing the save.
74. `nhw/colour20_save_slot` **K**: Save goes to the exact numbered slot.
75. `nhw/colour20_replace_slot` **K**: Replaces the colour in the identified slot rather than deleting the slot.
76. `nhw/colour20_saved_slot` **K**: Completion confirms both colour and numbered destination.
77. `nhw/gallery_image_component_unavailable` **H**: The phrasing says a required component is missing; preserve unavailable even when it exists, and distinguish the skipped import from a failed placement.
78. `nhw/ui_lossless_format` **K**: The formatted codec name and exact unchanged-pixels meaning survive.
79. `nhw/ui_image_codec_licences` **K**: Specifies image codec licences, separate from copyright of the imported image.
80. `nhw/formats22_tiff_compression` **K**: The compression option preserves pixels, and the exact Deflate method is named.
81. `nhw/formats22_tiff_description` **K**: Single RGB page, smaller possible bytes without changing pixels and optional uncompressed output survive.
82. `nhw/formats22_dib_description` **K**: Exact bit depth, uncompressed Windows DIB and a conditional BMP header interpretation.
83. `nhw/formats22_select_page` **K**: Clear one-page selection label for the multipage picker.
84. `nhw/formats22_page_description` **K**: Keeps metadata, total pages and selecting one page as an image in order.
85. `nhw/formats22_page_number` **K**: Explicit current page identifier rather than total pages.
86. `nhw/formats22_previous_page` **K**: Clear backward navigation wording; paired with Next page.
87. `nhw/formats22_next_page` **K**: Paired forward navigation term explicitly names page.
88. `nhw/formats22_open_page` **K**: Open is scoped to the already selected page.
89. `nhw/formats22_page_preview` **H**: The phrase is an instruction to look early, rather than the selected-page preview heading. Use a noun or screen label.
90. `nhw/formats22_page_range` **K**: Correct inclusive numbered range and dynamic endpoint.
91. `nhw/formats22_loading_page` **K**: Clearly an in-progress operation for previewing, retaining both page numbers.
92. `nhw/formats22_page_dimensions` **K**: All four placeholders and directions/units properly ordered.
93. `nhw/formats22_preview_unavailable` **K**: Preview cannot be shown and the error/detail slot survives.
94. `nhw/formats22_preview_memory` **K**: Keeps preview memory shortfall distinct from the offer of smaller dimensions when opening.
95. `nhw/formats22_pdf_invalid` **K**: Distinguishes likely file damage from features not supported by this Android version.
96. `nhw/formats22_pdf_encrypted` **K**: Password and unsupported encryption remain separate, with an unprotected copy needed before import.
97. `nhw/formats22_pdf_page_count` **K**: Keeps the first page and exact dynamic maximum.
98. `nhw/formats22_pdf_page_index` **K**: Old selection no longer works and replacement must be from this very document.
99. `nhw/formats22_pdf_dimensions` **K**: Both invalid and too-large page dimensions are separately preserved.
100. `nhw/formats22_pdf_crop` **K**: The crop must contain part of the page and the full rectangle is confined to the selected page.
