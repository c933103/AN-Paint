# PR3 and PR4 recovered handoff review — 25 September 2026

This pass started from published integration commit `7939f1292`, after the user
rejected the earlier completion claim. Filled resource keys and successful CI did
not establish that the original language work had received a semantic review.

## Recovered obligations and evidence

The integration reviewer recovered these original conversation handoffs:

- PR3, 22 September at 06:54:48 UTC: the assistant said that Cebuano had been
  rewritten after a corrupt mechanical conversion, Indonesian contamination from
  Malay had been removed, and four catalogues had 669 strings plus their plural.
  CI was still pending on the stacked branch. The claimed rewrite needed to be
  checked against the actual remaining prose.
- PR4, 23 September at 00:40:12 UTC: the assistant reported eight complete
  catalogues, format checks, and a mergeable PR. Its final commit had no CI run.
  Those claims concerned coverage and format validity, not independent proof of
  every sentence's meaning.

The relevant catalogues are Tagalog, Cebuano, Malay, Indonesian, Swahili, Finnish,
Hungarian, Afrikaans, Dutch, Estonian, Latvian, and Lithuanian. The Chinese and
Cantonese work earlier in the same branch conversation is recorded separately
by the integration reviewer.

## Concrete findings and repairs

| Finding | Scope and repair | Evidence |
| --- | --- | --- |
| The English clause “Show all changes zoom” had been parsed as a button named “Show all changes.” | Both assembly and legacy help now name the actual Show all control in 11 catalogues; Indonesian already had the correct control. Swahili also had the wrong grammatical form for the displayed caption. | Compare `ui_show_all` with `ui_add_up_to_20_images_with_android_s` and `ui_the_arrow_on_the_left_directly_below_the`; commit `487c11c6a`. |
| Dutch prose had stale tool names and an invalid decoder-memory conditional. | Verfspuit, Kromme, Dezelfde breedte/hoogte now agree with the controls. The warning says that decoder buffers still do not fit even at the smallest output size. | `ui_no_resize_fits_decoder_memory` and the two manuals; `487c11c6a`. |
| Many Cebuano technical passages retained English phrases instead of explaining their meaning. | Authored 149 short/medium entries and all three complete manuals. This covers gestures, memory allocation and decoder limits, PDF pages, first-frame/poster-image distinctions, vertical text, export formats, gallery credits and licence conditions. Subsequent review refined the draft and PDF-area wording. | `f8866ea28`, `4a2453f71`, and the later label consistency change. |
| “Right/top or bottom/left” did not distinguish placement from alignment. | Short placement help and legacy instructions now explicitly distinguish placement **at the right with top edges aligned** from placement **below with left edges aligned**. The full assembly instructions already expressed this distinction in the other 11 catalogues; Cebuano was rewritten in full. | `ui_drop_at_a_highlighted_edge_right_top_aligned`; `4be61ae48` and the Cebuano manual. |
| Active help named shortened or obsolete Fit/Swap controls. | All 12 owned active-help texts now use the corresponding displayed captions. Malay and Tagalog help also used an English or stale Navigate name. Indonesian consistently calls its mode Navigasi. | `ui_help23`, `ui_fit_selection34`, `ui_swap23`, `ui_navigate`; `4be61ae48`. |
| Zoom gestures were described only as enlarging. | Seven clauses each in Indonesian, Swahili, Hungarian, and Latvian now describe both directions and distinguish moving the fingers together from changing their distance. | `4be61ae48`, `33108e6fb`. |
| Legacy source guidance no longer matched the application menus. | All 12 manuals now put Assembly in File, and device/gallery insertion under Draw → Insert → Other images. | `ClassicPaintActivity.menuActions`, INSERT category construction, and `showOtherImages`; `4a2453f71`. The default and other locale owners were notified because this defect also exists in their source text. |

The Malay/Indonesian review read every non-manual entry longer than 100
characters (62 Malay and 66 Indonesian entries at the starting snapshot), plus
all six full manuals. In that reviewed set, the Indonesian text uses Indonesian
sentences and vocabulary rather than Malay sentences with surface substitutions.
The review found navigation/gesture defects and a missing bounded-panel qualifier,
which are repaired. The findings for the other PR4 languages are the concrete
cross-language repairs above; this document does not label them all as independently
certified for fluency.

## Cebuano lexical and semantic evidence

The Cebuano catalogue remains directly authored Android XML. No sentence
converter, translation generator, or preferred upstream-app catalogue was used.
Technical identifiers (PNG, RGB, PDF, Base64, CC BY-SA 4.0), standard font-family
labels, and useful technical loanwords are retained where they carry specific
meaning. Surrounding instructions use Cebuano clauses.

Lexical reference: John U. Wolff, *A Dictionary of Cebuano Visayan* (Cornell
University Southeast Asia Program and Linguistic Society of the Philippines,
1972), consulted in the
[Project Gutenberg transcription](https://github.com/GITenberg/A-Dictionary-of-Cebuano-Visayan_40074/blob/cb6f35757d26a8afb534396de1794c351c99b737/40074-0.txt).
The inspected text blob is `4f9851a772395976ca7574f772bf12547c82f348`.
Dictionary meanings guide individual choices; they are not evidence that an
automatically assembled sentence is correct.

| Entry checked | Application decision |
| --- | --- |
| `panid₂ / pánid` | Use panid for document pages, including page selection, counts, ranges and previews. |
| `líhuk`, `higdà` | Describe moving images and words laid sideways with Cebuano clauses; retain the distinct upright/sideways behavior. |
| `gahin` | Explain reserved/available memory as a gahin, preserving the decoder's separate working-memory requirement. |
| `kini₁`, genitive/dative `niíni` | Repair literal “sa kini” constructions to the appropriate demonstrative form. |
| `bagà`, `badlis` | Baga, Badlisan sa ubos and Badlisan sa tunga describe text weight and decoration. |
| `brutsa` | Use Brutsa for Brush, including its category and the manual's references. |
| `mantálà` | Use Cebuano publication clauses in editable attribution text; keep the creator, source, copyright and licence obligations distinct. |
| `sinugdan / sinugdánan`, checked by the independent reviewer | Rejected for the current working draft: it points to an initial/beginning state. Retain the already used technical loanword draft instead. |

Independent review by a separate agent compared the rewritten Cebuano manuals
and codec/memory warnings with the English source. It found and corrected two
meaning changes: the working draft must not imply an initial image, and a
nonempty PDF crop means a rectangle with positive width and height, even if it
contains blank pixels. It also identified the shared obsolete menu routes.

The review explicitly checked the bounded options panel, first-launch state,
landscape layout, and separately connected external keyboard. It retained
non-destructive source files, no automatic resize after allocation failure,
first animation frame versus separate PNG poster image, retained assembly
inputs, the Irasutoya **21 or more** paid-use threshold, special-collaboration
conditions, named creators, copyright notices, licence links, modification
descriptions, and CC BY-SA-compatible sharing requirements.

## Validation

- 27 translation tests pass after each completed batch, including positional
  parameters, numeric literals, aliases, plural resources and documented credits.
- Whole-resource compilation with Android SDK 35 `aapt2 compile --dir` passes.
- `git diff --check` passes.
- These checks establish resource validity. The sentence review and its
  corrections are recorded above separately from build/coverage results.
