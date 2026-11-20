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
