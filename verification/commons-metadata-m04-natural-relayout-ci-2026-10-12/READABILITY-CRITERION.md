# Readability acceptance reassessment (proposal, not a changed test)

## Finding

Zero nontransparent reference pixels outside the content box is an excellent sensitive clipping diagnostic. It is stronger than the user's readable, complete localized UI requirement and is not, by itself, a defensible universal release-blocking rule.

For the installed d5 checkpoint, each Arabic route lost precisely one black alpha=1/255 raster sample. It represents 0.00392157 fully opaque pixels of coverage, and at most one 8-bit channel step when composited against an opaque 8-bit background. The affected connected ink component retains 24 of its 25 nonzero samples, all its fully opaque samples, and 2509 of 2510 summed alpha units. No connected component disappears. Across the whole text the lost alpha fraction is about 0.000166% (copy) or 0.000160% (insert). These numbers establish a very small edge defect; they do not prove that a letter or diacritic is absent or that the UI is unreadable.

Source pixels inspected again: `../anpaint-pr55-glyph-installed-review-20261012/observed/copy-actual.png` and `copy-reference.png`. Full reference and actual arrays, rather than an already-clipped crop, underlie the result. The transparent PNG presentation itself is not proof of contrast against the app's actual background. The current 04 run remains separately pending; this assessment cannot turn its unknown failures into passes.

## Requirement basis and limits

WCAG's resize-text criterion concerns enlargement to 200% without losing content/function, and its clipping failure technique checks actual loss of text or controls. Reflow concerns availability of information/functions in constrained layouts. These web criteria are useful product guidance here, not a certification of this Android app. Neither supplies a zero-alpha raster threshold. W3C's contrast guidance explicitly distinguishes specified foreground/background colors from anti-aliasing-dependent samples; that does not itself authorize clipping, but demonstrates why per-sample opacity is not a standalone accessibility verdict.

Sources consulted:
- https://www.w3.org/WAI/WCAG22/Understanding/resize-text.html
- https://www.w3.org/WAI/WCAG22/Techniques/failures/F69
- https://www.w3.org/WAI/WCAG22/Understanding/reflow.html
- https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html

## Recommended acceptance model

1. Keep hard behavioral gates: exact complete visible/layout/accessibility strings; complete line coverage; no truncation/ellipsis; usable scrolling and controls; no occlusion or missing lines/glyph components; successful natural updates; supported scripts and both normal/enlarged scales. Accessibility text alone cannot excuse visibly missing text.
2. Retain the complete unmasked raster comparison as diagnostic evidence. Record affected pixels, peak composited error, summed coverage loss, spatial extent and loss within each affected component. Keep the independent full-reference allocation and edge-contact safety checks.
3. Triage an isolated very-low-coverage antialias fringe separately from material clipping. The observed alpha=1 sample, with the full component and opaque interior retained, warrants low-severity visual polish, not an assertion of unreadable Arabic. A traceable review decision may accept that specific evidence while leaving the exact diagnostic marked nonzero/failed. Do not silently relabel the historical oracle as passed.
4. Before introducing a general automated perceptual tolerance, calibrate it on supported densities/scales/scripts and independently labelled material defects. Do not pick a cutoff of 1, 7, 8, or an area budget merely because it admits the known failing samples. The available evidence is insufficient to justify a universal numerical visibility threshold.

A practical initial migration can make mathematical raster differences a reported diagnostic and keep hard behavior failures blocking, with explicit review of nonzero differences. This is not carte blanche to ignore clipping: unexplained differences, absent components, stronger/wider losses or semantic failures remain unresolved and require diagnosis.

## Required controls for any revised automation

- Preserve complete-reference origin/allocation; compare against the actual rendering, never a clipped expected crop.
- Positive intact controls across Latin, Arabic, Tibetan, Ainu Kana, Japanese, Nôm, vertical scripts, and normal/double scales at tested densities.
- Deliberately omit the first/last shaped cluster, a whole line, punctuation and an Arabic/Tibetan diacritic; preserve source/accessibility strings in some mutants so those cannot mask visible defects.
- Displace full text left/right and wholly outside; introduce a narrow crop that removes strong stroke ink and a wider faint loss. These must remain material failures.
- Include independently labelled low-coverage fringe-only perturbations as sensitivity/triage controls. A component can be a dot or mark, so aggregate whole-message loss percentage must never be the sole criterion.
- Exercise both same-height text replacement and width/font-scale changes through normal traversal. Verify reference construction and raster transport cannot drop first/last glyphs before comparison.
- Retain malformed, missing and duplicate artifact/record controls; missing evidence is not a visual pass.

No source, thresholds, assertions, images or historical results were modified to produce this recommendation.

## Root decision and current frame disposition

At 15:46 UTC the root approved the requirement-based split for migration: preserve hard actual content/glyph/line/control/accessibility/natural-update gates and full unmasked diagnostic evidence; use explicitly reviewed dispositions for nonzero differences, with no universal numeric tolerance. Keep focused real-clipping/removed-mark controls, without building a larger synthetic matrix.

The current 04 mixed-paragraph frame has now been independently classified in `mixed-reset-disposition.json`: two fringe samples (alpha 7 and 1), 76/78 affected component samples and 10625/10633 alpha units retained, all opaque samples retained, no other ARGB difference and no allocation-edge contact. This supports a low-severity fringe disposition, bounded to that observed frame. It does not change the existing failed JUnit result, nor fill the 26 frames and two summaries missing after its abort.
