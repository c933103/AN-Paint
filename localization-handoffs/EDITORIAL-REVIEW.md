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
