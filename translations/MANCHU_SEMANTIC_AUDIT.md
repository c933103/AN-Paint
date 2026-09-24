# Manchu semantic audit — 24 September 2026

Scope: `Paintroid/src/main/res/values-b+mnc+Mong/strings.xml` (`mnc-Mong`).
The first repair changed 274 string values. The 24 September
follow-up completes the previously listed technical gaps: 199 further resources
in this workstream, plus 56 colour/typography resources in the parallel
[colour and typography audit](MANCHU_COLOUR_TYPOGRAPHY_AUDIT.md). The complete
670-resource catalogue was read in batches against the English source. These
are source-assisted translations; independent speaker review has not occurred.

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

## Technical completion — 24 September

The memory/format and general-prose batches replace the previously documented mixed
English passages with complete Manchu descriptions. They retain the actions,
conditions, limits and format arguments; the work is not a change of script
applied to English words. The full help uses the same translated labels as the
controls, including those supplied by the parallel colour/typography repair.

| Previously open area | Completed repair / representative keys |
| --- | --- |
| Memory budgets, estimates and preview failures | `ui_current_safe_editing_budget_s_up_to_2f`, `ui_copy_decoded_image_at_this_size_estimated_loading`, `ui_estimates_include_the_current_canvas_and_clipboard_sampled`, `ui_preview_memory_error`, `formats22_preview_memory`: explain available RAM, estimated temporary space, detail loss and opaque imports; insufficient-memory messages now explicitly use `hamirakū`. |
| Encoding, decoding and source memory floors | `ui_codec_resize_memory_floor`, `save20_encoding_budget`, `formats22_ico_decode_budget`: describe reading a file into an image, converting an image to its stored form, and temporary storage needed while doing so. The smaller-output limitation remains explicit. |
| Save/export and exact file formats | `ui_save_explanation23`, `ui_export_explanation23`, `formats22_tiff_description`, `formats22_dib_description`, `formats22_base64_description`, `formats22_ascii_description`: complete native explanations of format selection, smaller-file storage, lossless colour preservation, DIB headers, Base64 recovery and non-reopenable ASCII renditions. |
| PDF, ICO and animation | `formats22_pdf_raster_hint`, `formats22_pdf_encrypted`, `formats22_pdf_crop`, `formats22_ico_description`, all four `formats22_animation_*` messages and `save20_gif_description`: retain rasterization, password/encryption restrictions, crop constraints, transparent square placement, still-image import and animation loss. Dithering is described as mixing small colour dots. |
| Credits, licensing and gallery actions | `gallery_description`, `gallery_credit_edit_hint`, `ui_catrobat_s_own_artwork_uses_cc_by_sa`, the About/notice/license titles and gallery error messages: translate the actual instructions, retain creator/copyright/source obligations, describe compatible reuse conditions, and synchronize every full File > About > Image credits breadcrumb. |
| Remaining general controls | Pixel-grid, crop-preview plurals, geometry, percentage, device, tool-option and source-export strings are translated. Both Android plural branches preserve their three ordered arguments and attachment-repositioning instruction. |

Additional lexical checks during this pass corrected `tukiyebure` (raising)
used for locking proportions to a description of preserving the width/height
relationship. `ni` is a grammatical particle, so references to another person
now use `niyalma`. Inherited Japanese `kikai` is replaced with `agūra` in device
contexts. The transparent/translucent phrase is the attested `fondo gehun`,
correcting the inherited `fundo` spelling. `temgetu bithe` is attested as a
license/certificate; `baitalara i temgetu bithe` describes a usage license.
These are contextual UI applications of historical vocabulary, not claims of
an established modern software terminology standard.

## Retained literals and review status

Proper format names and identifiers are deliberately literal: `PNG`, `JPEG`,
`JPEG XL`, `WebP`, `HEIC`, `AVIF`, `TIFF`, `DIB`, `BMP`, `GIF`, `PDF`, `ZIP`,
`Base64`, `ASCII`, `RGB`, `RGBA`, `sRGB`, `ICC`, `HSV`, `HSL`, `CC0`, `CC BY-SA`,
`AGPL`, `Android`, app/provider names, units and filenames. `GNU Affero General
Public License` is the formal document title. `English`/`Japanese` identify
supported search languages; `Large PNG`, `Files` and `Documents` identify
external controls/apps. `Aa Bb 0123` is an intentional font sample.
`data:image/png;base64,`, `canvas.png`, `Ctrl+A`, colour codes and format arguments
remain exact. General prose words such as decoder, export, palette, compression,
copyright and quality are no longer retained as untranslated instructions.

A combined scan of both workstreams found no unexplained Latin prose tokens
after excluding these names, units, identifiers and samples. It also found no
remaining occurrences of the reviewed respelled-English scaffolds. The two
workstreams change disjoint keys, and their combined catalogue changes 255
resources from the published `d861555d1` baseline. The earlier open-item table is resolved;
there is no known untranslated passage being deferred under “specialist review.”
This does not turn a lexical/source review into independent speaker review.
Further review can improve idiom and contemporary terminology without treating
every unchanged format name as missing translation.

`language20_translation_note` now says that the text is translated into Manchu,
format/application names retain their original forms, and the translation is
under review. It makes no claim of speaker certification.

Validation: XML parsing, unchanged format-placeholder multisets, no temporary
conversion markers, and `git diff --check` pass. The 97 host tests passed during
the follow-up; all 25 translation tests passed again after the final general
terminology edits. The parallel colour/typography repair also passes full AAPT
resource compilation. The integration branch verifies the combined Android
build separately. These technical checks cannot establish idiomatic Manchu.
