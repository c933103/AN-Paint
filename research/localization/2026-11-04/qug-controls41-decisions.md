# Independent controls review

Reviewed all 46 entries against the supplied 5777383 source snapshot and REVIEW.md (no README was present). This is an authored translation/context review, not native Chimborazo certification.

## Three conservative revisions

- ui_flip_horizontal: Lluki-allita tikrachina. Treat left/right as the pair reversed, rather than a destination (-man). setScale(-1,1) reverses left/right; do not describe reflection about a horizontal axis.
- ui_flip_vertical: Hawa-urayta tikrachina. Treat top/bottom as the pair reversed. setScale(1,-1) reverses top/bottom; do not describe reflection about a vertical axis.
- ui_rotate_90_clockwise: Alliman 90° muyuchina. Concise rotate-right UI instruction, retaining 90 degrees. Authored contextual alternative, not a claimed attested technical phrase.

## Decisions retained

Fit says show the whole view, while Fit image to canvas says fit the image within the canvas; this correctly separates viewport framing from floating-selection geometry. The latter preserves original pixels and clears selection rotation. Do not imply bitmap resampling there.

Crop gestures preserve edge/corner dragging versus dragging inside to move the crop. Reset correctly returns to the full image. Crop to selection does not imply resizing the selection. Canvas size remains distinct from image scaling. Palette gestures correctly preserve tap foreground versus press-and-hold background. Generic Churana is usable for Apply as well as insertion in different contexts; lexical reuse alone is not a defect. Tolerance explicitly concerns permitted colour difference, and is preferable to an abstract patience/error word. Keep it, with layout testing for the long label.

The unchanged navigation labels File, Canvas, Load image, Resize image and Undo remain coherent with existing help. No additional label-only changes recommended.

## Five isolated uncertainty entries

Three entries share one unresolved ratio term: ui_lock_aspect_ratio, ui_lock_proportions, and ui_scales_the_image_unlock_the_ratio_to_stretch. Tupunakuy must be understood as a fixed width-height relationship, not a frozen size or arbitrary measurement comparison. Retain the consistent candidate but do not call this terminology independently established. A missing dictionary hit alone does not prove it is wrong.

ui_italic: Ecuadorian dictionary lists wiksu as a variant of wistu, with bent/crooked senses. That supports the lexical base but not conventional slanted-type UI use. Retain as a candidate pending a stronger linguistic decision.

ui_left_arrow_collapse: caller absent from supplied subset, so arrow-key versus drawn-arrow meaning cannot be resolved. This does not establish dormant code.

## Sources and validation

Ecuadorian dictionary supports tikrachina as voltear/virar: https://prolipa.com.ec/blog/wp-content/uploads/2024/10/RK_diccionario_kichwa_castellano-1.pdf

Ecuadorian dictionary documents wiksu under wistu: https://kichwa.net/wp-content/uploads/2011/03/diccionario_kichwa_castellano.pdf

Official illustrated Ecuadorian Kichwa dictionary documents pacharikuchik for clock, but does not establish the original full clockwise phrase: https://www.educacionbilingue.gob.ec/wp-content/uploads/2025/05/Diccionario-ilustrado-Kichwa_compressed.pdf

Reviewed JSON preserves all source attributes and placeholders. Only the three values above were revised; original batch.json, strings.xml and all repository branches remain untouched. No device, layout or Android build test was performed. The original batch checks were removed from this derivative artifact to avoid implying that their original resource hash describes the revised proposals.
