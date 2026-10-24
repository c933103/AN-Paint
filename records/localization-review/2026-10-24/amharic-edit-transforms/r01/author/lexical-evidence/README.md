# Amharic Edit transform command lexical draft

Research date: 2026-10-24. Original proposals for independent review, not native-speaker acceptance. Research only: no application changes, builds, remote publication or Work tasks.

## Proposed review inventory

All eight rows below are candidates, not eight approved translations. The imperative forms intentionally differ from LibreOffice's predominantly nominal command labels. Exact source quotations are distinguished below from newly composed strings.

| English command | Proposed short imperative | Evidence / confidence / alternative |
|---|---|---|
| Flip horizontal | በአግድም ገልብጥ | Medium. Constructed imperative from LO Flip Horizontally `በ አግድም መገልበጫ`. Preserves left/right reflection, not rotation. Exact full imperative not attested here. |
| Flip vertical | በቁመት ገልብጥ | Medium. Same adaptation of LO `በ ቁመት መገልበጫ`; top/bottom reflection. |
| Rotate 90° clockwise | 90° ወደ ቀኝ አሽከርክር | Medium-high. Android directly attests `ወደ ቀኝ አሽከርክር`; LO separately attests 90° Right. Added angle is original composition. Shorter alternative `90° ወደ ቀኝ አዙር` adapts LO's rotate stem but is not directly attested as this command. Clockwise is conventional rotate-right, not translating the abstract clock metaphor literally. |
| Rotate 180° | 180° አሽከርክር | Medium-high. Android rotate imperative plus LO 180° label. Alternative `180° አዙር` is shorter, derived rather than quoted. |
| Invert colours | ቀለሞችን ገልብጥ | Medium. Constructed imperative; LO GraphicFilterInvert gives the same flip/invert lexical family in explicit colour-value context. Android independently attests colour-inversion noun `የቀለም ግልበጣን`. Must not become “swap colours,” which would suggest exchanging foreground/background. |
| Clear image | ምስሉን አጽዳ | Medium. Android attests imperative `አጽዳ` in Clear effects, not clear-image; LO attests Clear Contents `ይዞታዎችን ማጽጃ`. Image object added by researcher. Alternative `ምስሉን አጥፋ` is not preferred because it can blur clear-image with deletion. |
| Crop to selection | በምርጫው መጠን ከርክም | Low-medium; HOLD for independent naturalness/precision review. Android directly attests crop `ከርክም`; LO supports crop/selection vocabulary. The selection-size phrase is an original adaptation, not a source quotation. It could overemphasize dimensions rather than selected content, so do not silently finalize it. Alternative `በተመረጠው መሠረት ከርክም` (“crop according to what is selected”) also needs review and is less short. Bare `ከርክም` loses the selection scope. |
| Delete selection | የተመረጠውን ሰርዝ | Medium. Android directly attests Delete `ሰርዝ` and selected-item delete confirmation; the exact object+imperative is newly composed. Prefer selected-content reading over `ምርጫውን አጽዳ`, which can be misread as clearing the selection state. Alternative `የተመረጠውን አጥፋ` adapts LO delete stem, but Android's imperative gives stronger direct-form evidence. |

No claim of native review, render fit, unique correctness, or acceptance. Confidence refers to evidence plus semantic fit, not approval status. Spacing without LO's separate `በ ` is an intentional draft normalization, never represented as a verbatim quotation.

## Exact primary records

The source files and pinned URLs are in sources.json, with byte hashes and comparison against the initially fetched branch versions. po-evidence.json preserves raw records, English, Amharic, context and fuzzy status. android-evidence.json pairs source-language and Amharic keys. Source snapshots are retained in this directory.

### LibreOffice

Official project translations repository, source/am/officecfg/registry/data/org/openoffice/Office/UI.po:
- GenericCommands.xcu / .uno:FlipHorizontal / Label: Flip Horizontally → `በ አግድም መገልበጫ`.
- GenericCommands.xcu / .uno:FlipVertical / Label: Flip Vertically → `በ ቁመት መገልበጫ`.
- WriterCommands.xcu / .uno:RotateRight / Label: Rotate 90° ~Right → `ማዞሪያ 90° ወደ ~ቀኝ`.
- WriterCommands.xcu / .uno:Rotate180 / Label: Rotate 1~80° → `ማዞሪያ 1~80°`.
- GenericCommands.xcu / .uno:GraphicFilterInvert / Label: Invert → `መገልበጫ`.
- GenericCommands.xcu / .uno:Crop / Label: Crop → `መከርከሚያ`; TooltipLabel Crop Image → `ምስል መከርከሚያ`.
- CalcCommands.xcu / .uno:ClearContents / Label: Clear Contents → `ይዞታዎችን ማጽጃ`.
- CalcCommands.xcu / .uno:Deselect / Label: Undo Selection → `ምርጫውን መተው`. This is contrast evidence, NOT a delete-selection proposal.

These quoted records are nonempty and not fuzzy. The `~` characters are LO mnemonics, not literal AN Paint punctuation.

LO help source/am/helpcontent2/source/text/shared/02.po, 24010000.xhp / par_id3145345 explicitly describes GraphicFilterInvert as inverting colour values or grayscale brightness values. Its Amharic contains `የ ቀለም ዋጋዎች መገልበጫ`. This establishes colour inversion, unlike arbitrary appearance-based inference from the bare English word Invert. It does not independently attest AN Paint's exact RGB/alpha algorithm.

### Android Open Source Project

Gallery2 res/values-am/strings.xml matched to res/values/strings.xml:
- rotate_right: Rotate right → `ወደ ቀኝ አሽከርክር`.
- rotate_left: Rotate left → `ወደ ግራ አሽከርክር`.
- crop_action: Crop → `ከርክም`.
- delete: Delete → `ሰርዝ`.
- clear_effects: Clear effects → `ማሳመሪያዎች አጽዳ`.
- delete_selection singular confirmation contains `የተመረጠው ንጥል ይሰረዝ?`; this is selected gallery-item deletion, not pixel-region deletion. Use only for lexical/syntactic support, not identity of operation.
- deselect_all: Deselect all → `ሁሉንም አትምረጥ`. Separate action, not a delete translation.

Settings res/values-am/strings.xml:
- accessibility_display_inversion_preference_title: `ተቃራኒ ቀለም`.
- accessibility_display_inversion_switch_title: `የቀለም ግልበጣን ተጠቀም`.
These establish colour-inversion terminology, not an imperative image-edit operation. Android XML has no gettext fuzzy flag; these are nonempty checked-in localized strings, not evidence of native AN Paint acceptance.

### GIMP exclusion and alternatives

Official GNOME/gimp am.po snapshot was checked. Nonfuzzy standalone tool names Rotate → `ያሽከርክሩ` and Flip → `በፍጥነት ግለጥ` exist. The rotate term supports the same root but uses a different politeness/number form. The flip phrase has an unwanted apparent speed modifier and is not selected for these precise reflections.

Critically, GIMP's Crop to Selection, Delete Selection, direction-specific flips, Rotate 180°, and many Invert records are fuzzy, empty, or obsolete. They are not accepted exact evidence merely because the English keys look perfect. po-evidence.json includes fuzzy flags to make this exclusion auditable. A particularly misleading fuzzy record translates Invert the selection with a delete-looking string; it must not be reused.

Microsoft's known corrupted PDF Ethiopic extraction was not used for exact labels. The ICT/ELRC glossary was not needed to replace the closer first-party image-editing records; no unverified glossary entry is claimed.

## AN Paint semantic guardrails supplied by parent

Flip/rotate/invert/clear first commit pending trim, polygon, curve or floating-selection edits via applyPending, then operate on the whole bitmap. Horizontal flip reflects left/right; vertical reflects top/bottom. 90° rotation is clockwise. 180° has no directional distinction. Invert complements RGB while retaining alpha; it is not exchanging foreground/background swatches. Clear fills with canvas background; it does not delete the saved file.

Crop replaces the canvas from the transformed selected content's bounding rectangle, which may be rotated/masked; transparent margins flatten onto background. Do not describe it as only the original rectangular coordinates or promise alpha retention. Delete selection erases a nonfloating selected region with background or removes floating selected content, then clears the selection. It is not simply deselecting. Short labels need not expose implementation sequence; reviewers should use these semantics to judge them.

## Review requests

1. Verify imperative `ገልብጥ` naturalness for both spatial reflection and colour inversion, retaining explicit objects/directions.
2. Prefer one rotate verb consistently; the longer Android-attested `አሽከርክር` is the evidence-first proposal.
3. Resolve Crop to selection before implementation. Specifically test whether the proposed size phrase suggests mere resizing rather than replacing the canvas with selected content.
4. Verify clear-image versus delete-selected-content distinction and that the selected-object construction cannot be understood as deselect.

No claim that a full eight-label set is final. Crop remains explicitly held; the other seven remain reviewable original drafts.
