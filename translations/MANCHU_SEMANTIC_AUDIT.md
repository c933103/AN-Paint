# Manchu semantic audit — 23 September 2026

Scope: `Paintroid/src/main/res/values-b+mnc+Mong/strings.xml` (`mnc-Mong`).
Commit `764051ce1` changes 274 string values. The catalogue was read in batches
against the English source; this is a source-assisted repair, not independent
native-speaker review or a claim that every remaining string is idiomatic.

## Sources and method

- Jerry Norman, *A Concise Manchu-English Lexicon*, consulted through the
  [searchable lexical transcription](https://www.studylib.net/doc/7052336/21-826-entries).
  This is a mirror, so ambiguous transcription was checked against the following
  primary historical dictionary index where possible.
- H. Kuribayashi's [Manchu word index to the Qing triglot dictionary](https://gerel.net/articles/roncho/A47All.pdf)
  supplies Manchu entries with their original Chinese and Mongolian equivalents.
  For example, its `dursukilembi` entry confirms the spelling used for Copy.
- L. M. Gorelova, *Manchu Grammar*, consulted for clause structure and morphology
  through this [digitized copy](https://theswissbay.ch/pdf/Books/Linguistics/Mega%20linguistics%20pack/Tungusic/Manchu%20Grammar%20%28Gorelova%29.pdf).

These sources establish vocabulary and grammar. They do not establish modern
software terminology. Descriptions such as `jorire temgetu` (pointing marker)
for cursor and `nirure ba` (drawing area) for canvas are authored UI wording,
not quotations from a modern Manchu software standard. No neighboring-language
catalogue was transliterated to produce the repaired help.

## Concrete repairs

The following are romanized for review; the shipped values use Manchu script.

| Context / example key | Incorrect prior choice | Repair and lexical basis |
| --- | --- | --- |
| Two-finger gestures, `ui_drag_to_pan_without_drawing_pinch_with_two` | `anggala` | `simhun`, finger; `anggala` does not mean finger. |
| Selection corners, `ui_corners_and_edges_resize_round_handle_rotates` | `mujilen` | `hošo`, corner. `mujilen` means heart and remains appropriate for the heart shape. |
| Opposite corners, `ui_drag_between_opposite_corners_choose_outline_or_fill` | `etuku` | `bakcilaha juwe hošo`, two opposite corners; `etuku` is clothing. |
| Smooth strokes, `ui_smooth_freehand_strokes` | `nimanggi` | `bišun`, smooth; the former means snow. |
| Soft watercolor, `ui_draw_soft_watercolor_strokes_strength_controls_how_strongly` | `niyengniyeri` | `nemeyen`, soft; the former means spring. |
| Brush and round tip, `ui_brush`, `ui_round` | `fiyoo`, `fiyangga` | `fi`, writing brush; `muheliyen`, round. |
| Width, height, strength: `ui_width`, `ui_height`, `ui_strength` | `jušuru`, `ondo`, `mergen` | `onco kemun`, `den kemun`, `hūsun`; descriptive width/height measures and strength. `jušuru` is a measuring rule/unit; `mergen` means wise. |
| Metal colours, `ui_gold`, `ui_silver`, `ui_copper` | `altan`, `munggun`, English `Copper` | Manchu `aisin`, `menggun`, `teišun`. |
| Copy / Cut / Paste | Unsupported or respelled labels | `dursukilere`, `hasalara`, `amdulara`, from verbs for copying, cutting and sticking. Crop/trim uses `girire`. |
| Edit / Cancel | Create/write and shave/remove verbs | `dasara`, edit/put in order; `nakara`, stop. |
| Square, `ui_square` | `durbeme` | `durbejen`, square; rectangle uses a descriptive shape phrase. |
| Horizontal/vertical text controls | Unsupported `sampes` and mixed English | `hetu` / `undu`, with explicit top-to-bottom and column-order descriptions. |
| Minimum limits, `ui_enter_positive_dimensions_that_resolve_to_at_least`, `formats22_at_least_frames` | Wording meaning “up to” | `ci komso akū` or “one or more”; five minimum-limit messages repaired. |

The repairs also restore literal `HSV V`, `A–Z` and `Z–A`, and replace the Sibe
IY character in `jai` with Manchu I. Technical literals are not Manchu words and
must not be respelled. The integration branch separately repairs the Base64
prefix `data:image/png;base64,`.

The three full guides were authored clause by clause:

- `ui_help23`: complete quick guide, including navigation, save/export/share,
  autosave and selection controls.
- `ui_the_arrow_on_the_left_directly_below_the`: full editor guide, including
  bounded panel scrolling, first-launch panel state and persistence, landscape
  menu access, colours, undo/recovery, selection, text, import and credits.
- `ui_add_up_to_20_images_with_android_s`: complete assembly guide, including
  non-destructive crop/reset/undo, snap preview and `+` placement, overlap
  rejection, dependent image movement, view-only Show all, smaller-output
  fallback, unchanged originals, persisted reopening and File > About notices.

Recovery and several memory-failure dialogs were rewritten with complete
actions and consequences. `ui_irasutoya_help34` retains the commercial 21-or-more
item fee condition, special collaboration terms and retained source/credits.
Credit routes use the actual File > About > Image credits labels.

## Remaining specialist review

Proper format names and identifiers are deliberately literal: `PNG`, `JPEG`,
`JPEG XL`, `WebP`, `HEIC`, `AVIF`, `TIFF`, `DIB`, `BMP`, `GIF`, `PDF`, `ZIP`,
`Base64`, `ASCII`, `RGB`, `RGBA`, `sRGB`, `ICC`, `HSV`, `HSL`, `CC0`, `CC BY-SA`,
`AGPL`, `Android`, app/provider names, units and filenames. Their presence does
not itself indicate a translation defect. No claim is made that other retained
English words are established Manchu loans.

The following are actual unresolved English phrases, unexplained technical
terms, or inherited wording that needs semantic review. This is a concrete
handoff, not an exhaustive certification of the other values.

| Keys | Remaining work |
| --- | --- |
| `ui_current_safe_editing_budget_s_up_to_2f` | Translate `safe edit budget` and `decoder overhead`; the related detailed RAM warning was repaired, but this short summary remains mixed. |
| `ui_assembly_decoded_output_estimated_editing_render_memory_at`, `ui_copy_decoded_image_at_this_size_estimated_loading`, `ui_original_decoded_image_rgba_4_bytes_pixel_estimated` | Replace `Decode output`, `Load/edit`, `edit/render` and respelled resize text with consistent native descriptions. Preserve numbers, RGBA and bytes/pixel. |
| `ui_estimates_include_the_current_canvas_and_clipboard_sampled` | `clipboard`, `sample decode`, `edit buffer`, `Import` and `copy` remain; verify the full detail-loss/opaque-background explanation, not only nouns. |
| `ui_preview_memory_error`, `formats22_preview_memory` | Recheck inherited `memori elejehe` against “not enough memory”; align with the repaired `RAM hamirakū` warnings and preserve the smaller-page option. |
| `ui_vertical_hint23` | `column`, `combining mark`, `emoji sequence` are partly untranslated/respelled; “upright” still differs from the repaired `undu` controls. Retain joining-script and sequence-preservation semantics. |
| `ui_honeycomb_colour_swatches_with_a_greyscale_row`, `ui_hue_and_saturation_spectrum_lightness_slider_on_the`, `ui_hue_and_saturation_wheel_value_slider_on_the` | Translate English descriptive phrases and distinguish hue, saturation, HSV value and HSL lightness. |
| `ui_airbrush`, `ui_pencil`, `ui_ellipse`, `ui_honeycomb`, `ui_radius_px`, `ui_spray_radius_px`, `ui_cursive`, `ui_quality` | Still English labels. Related authored help intentionally matches the visible labels pending a reviewed terminology choice. |
| `ui_save_explanation23`, `ui_export_explanation23`, `ui_higher_quality_usually_makes_a_larger_file_lossless`, `ui_lossless_format` | Explain format/compression and lossless meaning; do not classify `compression setting` or `Lossless` as a proper name. |
| `colour_unsupported_icc_model`, `colour_converter_unavailable`, `save20_unsupported_tagged_colour` | Translate `image decoder`, `color-managed app/editor`, `converter` and `profile`; retain ICC/sRGB and the required conversion-before-import action. |
| `ui_codec_resize_memory_floor`, `formats22_pdf_memory`, `formats22_ico_decode_budget`, `save20_encoding_budget` | Explain decoder source/tile/buffer memory without English noun clusters. Source-size memory-floor behavior must remain explicit. |
| `formats22_tiff_description`, `formats22_dib_description`, `formats22_pdf_raster_hint`, `formats22_pdf_encrypted`, `formats22_pdf_crop`, `formats22_ico_description` | Technical description review: compression, file header, vector rasterization, encryption, crop rectangle and transparent square. `crop`, `durbe` and `transparent` remain in inherited wording. |
| `formats22_animation_message`, `formats22_animation_unknown`, `formats22_animation_still`, `formats22_animation_poster`, `save20_gif_description` | Review frame/animation/default-image/dithering terminology and inherited verb orthography; preserve still-image-only import and discarded animation. |
| `formats22_base64_description`, `formats22_ascii_description` | Syntax prefix is independently repaired, but surrounding lossless/plain-text/size wording still needs review. Preserve the inability to reopen ASCII art as the original image. |
| `gallery_description`, `gallery_credit_edit_hint`, `ui_gallery_artwork_catrobat_and_its_credited_creators_cc`, `ui_about_copyright_licence`, `ui_credits_terms` | English `publisher`, `copyright`, `Credit`, `terms` and `licence` remain; historical vocabulary alone does not validate modern licensing prose. Verify route wording after integration. |

`language20_translation_note` now explicitly says Manchu and English text are
present and that the translation remains under review. It replaces the former
assertion that the entire catalogue was translated without English fallback.
Resource presence is not evidence of language quality.

Validation on the repair worktree: XML parsing, unchanged format-placeholder
multisets, no temporary conversion markers, `git diff --check`, and all 20 tests
in the inherited `tools/test_translations.py` passed. The integration branch runs
the expanded host/resource tests and Android build separately; these checks
cannot establish idiomatic Manchu or substitute for specialist review.
