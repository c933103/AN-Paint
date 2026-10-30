# Independent Shan review — D, E and F

## Decisions

| Batch | Missing lexical candidates | Accepted final values | Held |
|---|---:|---:|---:|
| D | 33 P1 | 32 P1 | Airbrush: 1 P1 |
| E | 5 P0 + 12 P1 | 5 P0 + 11 P1 | Palette argument contract: 1 P1 |
| F | 2 P0 + 1 P1 | 2 P0 + 1 P1 | 0 |
| Total | 7 P0 + 46 P1 | **7 P0 + 44 P1** | **2 P1** |

Exact decisions, values, backtranslations, reasons and confidence are in the accompanying D/E/F TSVs. For F, the reviewed final values are the sampled-decode and icon revisions, not the historical original values. No missing key receives credit twice.

## Full-message findings

- Functional tool labels were assessed against the actual operation, not simply a noun gloss. Paste includes both cut and copied contents; Redo reapplies the undone change; Eyedropper samples image color; Bucket fill acts on an area. Long labels have not passed device/layout review.
- `ui_fit_image` has no found live caller, but `translations/gimp-terms.json` maps that exact key to the view action “Fit Image in Window.” This is positive evidence for fit-to-view wording. It does not become fit-to-canvas or source-pixel resampling. `ui_fit_selection34` is separately the floating geometry operation and retains `formatted="false"`.
- Ratios remain fixed while dimensions may change. Whole-pixel trim amounts versus percentages, each-image bounds, strict positive dimensions and minimum resolved one pixel remain distinct requirements.
- Metadata absence, invalid/unsupported metadata, truncation and converter startup failure are different diagnostics. The converter warning expressly says import did not occur.
- ASCII output remains plain text, with equal-width character-font guidance and explicit inability to reopen it as the original image. Export keeps both current image and its Save destination unchanged.
- Memory warnings retain source/output distinction, current safe budget, approximate demand, minimum-output source-memory floor, before-allocation stopping, and no automatic resize. Original resolution is appropriately rendered as original pixel dimensions in these callers, not dpi or byte size.
- The sampled-decoding original was overabsolute: `ImportPlan.create` can keep `sample = 1`. The accepted successor says decoding **can** reduce pixel count. It retains canvas/clipboard/buffers, variable actual use, smaller-copy detail loss and unchanged original file.
- The accepted export successor uses the digital-icon noun **ဢၢႆႇၵွၼ်ႇ**, independently read in the primary [VisualEditor Shan catalogue](https://github.com/wikimedia/mediawiki-extensions-VisualEditor/blob/master/i18n/ve-mw/shn.json) and matched to its [English counterpart](https://github.com/wikimedia/mediawiki-extensions-VisualEditor/blob/master/i18n/ve-mw/en.json). That noun fits exported ICO icons; the rest of the entire sentence was reviewed independently.

## Two unresolved values

### `ui_airbrush`

Exact held target: **ၶိူင်ႈၽူၼ်သီ**. The intended color-spraying-tool meaning fits SPRAY, but the exact syllable **ၽူၼ်** is directly documented as rain in its [dictionary entry](https://en.wiktionary.org/wiki/ၽူၼ်). A spray sense for this exact form has not been secured. This is a lexical/tone-sense competence limit, not a claim that the language has no spray word or that a homonymous sense is impossible. The entire compound remains excluded.

### `ui_foreground_background_colour_palette`

Exact held target: **သီတၢင်းၼႃႈ %1$s၊ သီပိုၼ်ႉလင် %2$s။ ပၢၼ်ႉသီ %3$s။**

The foreground/background clauses and ordinary palette noun are acceptable; a noun followed by a name/descriptor is plausible. However, canonical `docs/swedish-remaining-p1.md` explicitly records that the third argument may be an action, state or descriptor, and no current caller settles that contract. Moving it after the noun can fail for an action, whose verb would normally precede the object in Shan; a bare numeric value could also be read as a palette identifier instead of a color count. Therefore the full alias remains held for integration. This is not a generic absence-of-caller rejection, not a lexical rejection of palette, and not a rollback of other reviewed palette controls. All three format tokens are intact.

## Source and method

Bound to develop `96681f687671a1fdffe134a325843919c1543401`, tree `39bb7351fa5532194e2c0430432b2f0cc6358a86`. Exact English resources, priority classification, app implementations, prior review evidence and primary language references were read. Attributes/placeholders/escaped newlines were compared manually. No source edits, scripts or tests were performed. Independent AI/model review is not native-human certification or rendered UI/TalkBack verification.

The 35 existing specific semantic holds remain unchanged. Failed web cache retrievals were worked around with the read-only GitHub connector for the primary icon catalogue; they were not permission denials or evidence of absent terminology.
