# Amharic: seven missing drawing labels, original draft only

Production `66be61df27c5359bffc32d56db21f3949899f873`; tree `870c5a584120d92710be516af0dc3b3847b183d9`. Ten complete source files verified against Git blobs.

All seven exact keys are currently missing. Presence remains12/717, missing705. Nothing implemented or independently accepted.

## string/ui_brush

English: Brush
Proposed XML: `<string name="ui_brush">"ብሩሽ"</string>`

PaintCanvas.stroke applies foreground paint with selected tip/width; brushTip2 draws diagonal marks, other tips draw/smooth strokes. PaintDocument.paint controls cap and antialiasing.

Brush noun, not a command to clean. The drawing-tool context supplies the painting sense.

Confidence: semantic high; UI idiom medium-high.

Independent check: Confirm familiar painting-tool rather than cleaning-brush idiom.

Sources: [brush](https://dictionary.abyssinica.com/brush)

## string/ui_line

English: Line
Proposed XML: `<string name="ui_line">"መስመር"</string>`

shapePath falls through to moveTo/start and lineTo/end; pointer-up commits that path. drawShape always strokes LINE, regardless of fill-only setting.

The attested drawn-line noun fits the two-endpoint straight-line tool; it does not mean a line of verse.

Confidence: semantic high; UI idiom medium-high.

Independent check: Confirm the short noun without needing an adjective for straight.

Sources: [ict](https://oromianeconomist.com/wp-content/uploads/2017/08/ict-glossary-in-afaan-oromoo-amharic-and-tigarinya.pdf)

## string/ui_curve

English: Curve
Proposed XML: `<string name="ui_curve">"ጥምዝ"</string>`

curvePath initially previews a straight segment, then cubicTo uses two control points. Pointer-up advances three stages; applyPending commits early when requested. The label names the completed tool capability, not a promise every intermediate preview is curved.

Use the glossary’s attested curve noun, avoiding an unsupported expanded phrase. Distinguishes the bendable path tool from the straight line.

Confidence: semantic high; UI idiom medium.

Independent check: Check whether the noun alone sounds natural as a tool label or requires a conventional fuller form.

Sources: [ict](https://oromianeconomist.com/wp-content/uploads/2017/08/ict-glossary-in-afaan-oromoo-amharic-and-tigarinya.pdf)

## string/ui_rectangle

English: Rectangle
Proposed XML: `<string name="ui_rectangle">"ቀጤ ጎነ አራት"</string>`

shapePath adds an axis-aligned RectF between opposite dragged corners; drawShape supports outline/fill. A square remains a valid special case.

The glossary specifically defines a right-angled quadrilateral. Prefer this precise term over generic four-sided-shape wording; do not imply arbitrary quadrilaterals.

Confidence: semantic high; UI idiom medium.

Independent check: Check contemporary UI familiarity and spacing of this attested mathematical term; loanword alternatives are not automatically preferable.

Sources: [ict](https://oromianeconomist.com/wp-content/uploads/2017/08/ict-glossary-in-afaan-oromoo-amharic-and-tigarinya.pdf)

## string/ui_heart

English: Heart
Proposed XML: `<string name="ui_heart">"ልብ"</string>`

ShapePaths.heart builds a closed symmetric heart silhouette using cubic segments within the drag bounds, then shared outline/fill rendering applies.

The ordinary heart noun also has primary symbol-annotation precedent. Here it names a heart silhouette, not an anatomical diagram or emotional command.

Confidence: semantic high; UI idiom medium-high.

Independent check: Confirm noun as a shape-tool label; no medical meaning intended.

Sources: [heart](https://dictionary.abyssinica.com/%E1%88%8D%E1%89%A5), [cldr36](https://www.unicode.org/cldr/cldr-aux/charts/36/annotations/afro_asiatic.html)

## string/ui_star

English: Star
Proposed XML: `<string name="ui_star">"ኮከብ"</string>`

ShapePaths.star alternates ten outer/inner vertices, yielding five points; bounds may stretch the shape. This is not a favourite/rating action.

The star-symbol noun fits a five-pointed geometric star. Do not use the dictionary’s unrelated verb sense of marking an item with a star.

Confidence: semantic high; UI idiom medium-high.

Independent check: Check short shape label; five-point detail is already in the separate English hint, not added here.

Sources: [cldr36](https://www.unicode.org/cldr/cldr-aux/charts/36/annotations/afro_asiatic.html)

## string/ui_arrow

English: Arrow
Proposed XML: `<string name="ui_arrow">"ቀስት"</string>`

ShapePaths.arrow creates a closed seven-vertex shaft/head polygon oriented from start/tail to end/head, with head and shaft scaled by length/width. Very short zero-length gesture returns an empty path.

The ICT glossary explicitly supports the directional-symbol sense despite other bow/arch meanings. The drawing context distinguishes the shape from a bow or a keyboard key.

Confidence: semantic high; UI idiom medium-high.

Independent check: Check directional arrow-shape idiom, not only dictionary equivalence.

Sources: [ict](https://oromianeconomist.com/wp-content/uploads/2017/08/ict-glossary-in-afaan-oromoo-amharic-and-tigarinya.pdf)

## Limits

- Original draft translations only; independent checking required for every row.
- Lexical attestation is not contextual acceptance or native-speaker review.
- No production edits, builds, tests, CI, rendering, publication or accessibility execution.
- No English correction prerequisite established for the selected seven complete labels; hints are context only and remain untranslated/outside scope.
- No approval of mixed-language composed status/help/accessibility strings.
- All prior full Help/warning/optional holds preserved.
- Polygon deferred because the tool also supports open polylines. No source defect asserted.
- Previous Palette uncertainty and optional Horizontal punctuation are separate.
