# Amharic nine-label author review

AUTHOR REVIEW FOR INDEPENDENT CHECKING; NOT ACCEPTED OR IMPLEMENTED

Production: `66be61df27c5359bffc32d56db21f3949899f873`; tree `870c5a584120d92710be516af0dc3b3847b183d9`.

Seven retain recommendations; one substantive proposal requiring independent checking; one optional punctuation refinement. Zero independent acceptances or implementations. No English correction prerequisite established.

Exact XML text, source/value hashes and immutable consumer references are in author-review.json; complete-file bindings are in source-bindings.json.

## string/ui_eraser

English: Eraser  
Current XML text: `"ላጲስ"`  
Author decision: retain-current

Eraser / rubbing-out implement.

PaintTool.ERASER label, rendered by ToolButton and tool options/help. PaintDocument.paint selects background colour for erasing, not transparency.

The teaching source explicitly identifies this exact word as eraser. In this app it names a background-colour painting tool, not a promise of transparent deletion. The short noun does not contradict that behaviour; the separate hint explains background colour. Do not replace it with pencil based on a cross-language false friend.

Proposed XML text: none; retain exact current value.

Confidence: semantics high; UI idiom medium-high. No native-speaker certification.

Independent check: Check ordinary contemporary UI familiarity; no spelling replacement is justified by the recovered lexical evidence.

References: [eraser](https://conference.usu.edu/SYSTEM/Uploads/Handouts/15233_1981miriamredleaf.pdf)

## string/ui_pencil

English: Pencil  
Current XML text: `"እርሳስ"`  
Author decision: retain-current

Pencil (also a word associated with lead).

PaintTool.PENCIL label. The drawing implementation uses adjustable document.pencilWidth (1–100), square cap and no antialiasing. Current hint already describes adjustable Width; resource identifier is historical, not the English sentence.

The drawing-tool noun is appropriate for the crisp, non-antialiased stroke. Adjustable width does not make the pencil metaphor false. Current English hint already states Width 1–100; its historical one-pixel identifier is not a source-text defect.

Proposed XML text: none; retain exact current value.

Confidence: semantics high; UI idiom high. No native-speaker certification.

Independent check: Confirm normal software-tool register, without adding a one-pixel restriction.

References: [pencil](https://dictionary.abyssinica.com/pencil)

## string/ui_text

English: Text  
Current XML text: `"ጽሑፍ"`  
Author decision: retain-current

Text / writing.

PaintTool.TEXT label, opens text placement/style flow. Distinguish the drawing text tool from generic prose/content.

A noun naming the tool that places and styles written text fits the current consumer. It is not a document-reading command or the name of a specific font.

Proposed XML text: none; retain exact current value.

Confidence: semantics high; UI idiom high. No native-speaker certification.

Independent check: No correction proposed; verify short tool-label idiom.

References: [text](https://dictionary.abyssinica.com/text)

## string/ui_palette

English: Palette  
Current XML text: `"መደርደሪያ"`  
Author decision: proposed-correction-needs-independent-check

Shelf / storage surface; potentially an inherited software-palette metaphor.

AdvancedColourDialog tab selects mode0, showing basic/saved colour swatches, not a general shelf or toolbar. Review existing wording in this exact colour-selection sense without presuming it is wrong.

The current mode contains basic and saved colour swatches. The existing noun does not identify colours and risks sounding like a general shelf. Propose a descriptive colour-collection label rather than asserting an unsupported standard palette equivalent. This is an author-composed contextual proposal, not an attested complete dictionary phrase. The possibility that the current shelf metaphor is established remains open.

Proposed XML text: `"የቀለም ስብስብ"`

Confidence: semantics medium-high; UI idiom medium. No native-speaker certification.

Independent check: Assess whether the complete proposed phrase is idiomatic for selectable basic/saved colour swatches and better than established Amharic software terminology. Do not accept from component dictionary matches alone.

References: [shelf](https://dictionary.abyssinica.com/%E1%88%98%E1%8B%B0%E1%88%AD%E1%8B%B0%E1%88%AA%E1%8B%AB), [collection](https://dictionary.abyssinica.com/%E1%88%B5%E1%89%A5%E1%88%B5%E1%89%A5), [ict](https://oromianeconomist.com/wp-content/uploads/2017/08/ict-glossary-in-afaan-oromoo-amharic-and-tigarinya.pdf)

## string/ui_preview

English: Preview  
Current XML text: `"ቅድመ ዕይታ"`  
Author decision: retain-current

Prior view / preview.

TextStyleDialog heading immediately before TextPreview; update() displays the edited sample with size/font/colour/direction. It is a text-style preview, not save/export preview.

The heading introduces a live sample of text styling. It does not assert print fidelity, export output or saving. The glossary has a closely corresponding spelling with እ rather than current ዕ; this alone is insufficient reason for orthographic churn.

Proposed XML text: none; retain exact current value.

Confidence: semantics medium-high; UI idiom medium-high. No native-speaker certification.

Independent check: Check contemporary spelling preference independently if desired; no semantic defect established.

References: [ict](https://oromianeconomist.com/wp-content/uploads/2017/08/ict-glossary-in-afaan-oromoo-amharic-and-tigarinya.pdf)

## string/ui_zoom_in

English: Zoom in  
Current XML text: `"ከቅርበት ዕይታ"`  
Author decision: retain-current

Close-up / near view.

EditIcon.PLUS label/content description; zoom_in action calls paintCanvas.zoomStep(1.5f). Changes viewport magnification, not image dimensions.

This nominal label describes increasing apparent canvas magnification and is directionally correct for the plus action. It does not explicitly promise document resizing. A glossary imperative equivalent exists, but changing a clear paired noun label solely to match English imperative grammar is not necessary.

Proposed XML text: none; retain exact current value.

Confidence: semantics medium-high; UI idiom medium. No native-speaker certification.

Independent check: Check the near/far pair together for clear action-label and accessibility idiom; lexical alternatives are not automatic corrections.

References: [ict](https://oromianeconomist.com/wp-content/uploads/2017/08/ict-glossary-in-afaan-oromoo-amharic-and-tigarinya.pdf)

## string/ui_zoom_out

English: Zoom out  
Current XML text: `"ከርቀት ዕይታ"`  
Author decision: retain-current

Distant / far view.

EditIcon.MINUS label/content description; zoom_out action calls paintCanvas.zoomStep(1/1.5f). Changes viewport magnification, not image dimensions.

This is the counterpart to near view and correctly describes reducing apparent magnification. The code changes the viewport, not image dimensions. Retain the coherent pair rather than silently substituting a generic shrink command.

Proposed XML text: none; retain exact current value.

Confidence: semantics medium-high; UI idiom medium. No native-speaker certification.

Independent check: Check with Zoom in as one paired UI convention; no runtime or screen-reader execution was performed.

References: [ict](https://oromianeconomist.com/wp-content/uploads/2017/08/ict-glossary-in-afaan-oromoo-amharic-and-tigarinya.pdf)

## string/ui_horizontal23

English: Horizontal  
Current XML text: `"አግድም፦"`  
Author decision: optional-punctuation-refinement

Horizontal, followed by Ethiopic introductory punctuation (፦).

TextStyleDialog text_direction spinner first option maps to TextDirection.HORIZONTAL; not a horizontal flip or page-orientation command. Existing terminal punctuation needs linguistic review in an option list, not automatic deletion.

The directional word fits the horizontal text-flow option. The terminal punctuation is unnecessary for a standalone spinner option, which introduces no following value. Removing it is optional UI polish, not a meaning correction or evidence that the current word is wrong. A different glossary noun is not grounds to replace the current direction word.

Proposed XML text: `"አግድም"`

Confidence: semantics medium-high; UI idiom medium-high. No native-speaker certification.

Independent check: Decide whether punctuation omission is preferable in this option list; keep separate from the substantive Palette proposal.

References: [ict](https://oromianeconomist.com/wp-content/uploads/2017/08/ict-glossary-in-afaan-oromoo-amharic-and-tigarinya.pdf)

## string/ui_category_selection

English: Selection  
Current XML text: `"ምርጫ"`  
Author decision: retain-current

Selection / choice.

ToolCategory.SELECTION groups rectangle/lasso selection; also EditGroup.SELECTION label. ToolCategoryButton composes category and selected-tool labels in accessibility text. This is image-area selection, not choosing a menu option.

The category groups rectangular and lasso image-area tools; the broad selection noun is usable in that disambiguating context. Its other choice/election senses do not establish an error. This review covers the noun only, not the mixed-language expanded/collapsed accessibility templates or the untranslated tool names.

Proposed XML text: none; retain exact current value.

Confidence: semantics medium-high; UI idiom medium. No native-speaker certification.

Independent check: Check image-editing category idiom; do not treat this as acceptance of complete composed accessibility announcements.

References: [selection](https://dictionary.abyssinica.com/selection)

## Limits

- No native-speaker or independent acceptance claimed. Lexical sources do not establish full contextual acceptance.
- No app/resource changes, remote publication, builds, CI, runtime, rendering, layout or accessibility execution.
- All original XML text and source hashes preserved; wrapping quotes are literal XML text, not a compiled-resource assertion.
- 12 present / 705 missing canonical containers remains source coverage, not quality; only these nine existing labels were assessed.
- Full Help holds, all prior warning/optional holds and unrelated programme exclusions unchanged.
- Palette exact preferred terminology remains unresolved; a search-snippet/PDF extraction conflict was not silently resolved.
- Text-direction government textbook PDF could not be opened (response too large); its search snippet is not used as review evidence.
