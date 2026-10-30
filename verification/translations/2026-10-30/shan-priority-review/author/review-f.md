# Shan batch F — last feasible technical paraphrases

`batch-f.tsv` contains **3 further missing candidates (2 P0 + 1 P1)**, all new rather than repeated prior proposals. Same source-bound source commit/tree as batches A–E; canonical source remains read-only.

These were not waived merely because they contain specialist concepts. Actual caller and implementation context allowed bounded functional descriptions:

- `ImageImport.kt`, `ImportPlan.create`, performs sampled decoding before final scaling; the memory explanation describes decoding to fewer pixels. Current canvas/clipboard, uncertain actual memory use, lost detail in a smaller copy, and unchanged original file remain separate propositions. The descriptive sampling phrase requires independent review.
- `ImportMemoryRequirements` and `ImageResizeDialog` distinguish formats with source/tile native decode work that does not necessarily shrink with output. Tiles are rendered descriptively as source-image sections, with mandatory decode-before-resize and the possible memory overrun intact.
- `SaveOptionsDialog.kt` uses the export explanation for derived export, while `ImageExporter.kt` maps the icon path to `ImageFormat.ICO`/`IcoCodec.encode`. The candidate says **ICO-format image** instead of pretending to know an established general Shan icon noun. ASCII art is described as an image made of ASCII characters. This contextual adaptation needs explicit reviewer approval, not silent equivalence credit. The current image and its existing Save destination both remain unchanged.

No implementation or test result is asserted. Candidate count is not acceptance. The remaining per-item limits are recorded separately; no blanket Shan pass/fail is asserted.
