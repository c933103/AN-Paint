# Shan batch D — manipulation and interaction

`batch-d.tsv` contains **33 additional missing P1 candidates**. It shares the same current source binding as preceding batches; previous authored/reviewed rows are not duplicated. Text direction revises one previous unaccepted candidate; the other 32 are new.

This batch deliberately uses explicit functional descriptions where a short specialized tool noun is not confidently known: colour-spraying tool, colour-sampling tool, insert cut-or-copied content, and reapply the undone change. These are not claims of conventional short Shan UI terminology. Independent review must assess semantics and naturalness; long labels still need later device/UI-fit checks.

Source-context checks used actual values and callers, not names alone:

- PaintDocument's tool definitions and real English hints distinguish SPRAY, FILL, PICKER, free-form LASSO, rectangular SELECT and watercolor.
- `finishSelection` composites floating content before ending selection; candidate does not discard its pixels.
- `paintCanvas.fit` is a viewing change, whereas `fitSelectionToCanvas` changes floating placement geometry, preserving source pixels. Their wording is distinct. The unused exact `ui_fit_image` alias has an explicit intent-confirmation caveat.
- The proportions checkbox locks width/height aspect, not file edits; the explanatory sentence preserves independent stretching when that constraint is off.
- TextStyleDialog's text direction options include horizontal and vertical column directions, separate from alignment and glyph orientation.
- Positive dimensions resolving to at least one pixel retain both conditions. Trim validation keeps every image, whole-pixel amounts OR percentages, and uses the verified corrected trim-amount noun phrase.

All targets are candidates requiring independent review. No acceptance totals are increased here. No implementation or test result is asserted.
