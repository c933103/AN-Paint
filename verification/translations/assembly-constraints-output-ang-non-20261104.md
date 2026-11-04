# Assembly constraints and output: Old English and Old Norse

Base: `1d5af638cb29aaf6f75f6090c5e8cbe84c6a0907` on `review/nv-bottom-2038-20261103`.

Added 20 missing P2 strings each to `values-b+ang` and `values-b+non`. The block covers attachment constraints, assembly output sizing, memory estimates, progress and failure/retry guidance. Canonical wording is in the Android resources; this record does not duplicate translations as approval fixtures.

## Context and review

Source consumers checked: `AssemblyActivity.kt`, `AssemblyCanvas.kt`, `AssemblyRenderer.kt`, `ImageAssembly.kt`, `ClassicPaintActivity.kt` and `ImageResizeDialog.kt`.

- Attachment means a snap relationship between images. Missing/unplaced attachment-image errors describe the anchor to which another image is attached, not a missing email or file attachment.
- The overlap warning concerns the current snap arrangement and offers another edge or unplacing attached images. It does not prohibit the overlap allowed by exact positioning. Unplace remains distinct from deleting a source file.
- Coordinate-range errors remain separate from memory limits and preserve the smaller-image guidance.
- The output summary retains three separate values: assembly dimensions, decoded output bytes and estimated editing/rendering memory at original dimensions. The subsequent estimate/working-budget string keeps its trailing newline for the appended fit or choose-smaller caption.
- Estimated and approximate quantities remain qualified. Meeting the current budget does not promise successful rendering. A failed-preview notice permits removing the affected images from the assembly or trying to save, without guaranteeing save success or directing source-file deletion.
- Progress counts are processed images, not an assertion of overall completion. Reopen guidance quotes the existing Image assembly menu root. Android and Paint identifiers remain unchanged.

Independent semantic and linguistic review accepted all 40 strings unchanged. Existing catalogue terminology is retained. Attachment language uses ordinary fastening vocabulary, including Old English [fæstnian](https://www.gutenberg.org/files/31543/old/files/dict_dg.html). Historical-language computing terms are catalogue adaptations, not claims of ancient technical usage.

## Validation and coverage

- All 78 repository host tests passed against the accepted candidate.
- All 171 offered-language structural checks passed.
- XML parsing, unique keys, Android escaping, source attributes, ordered typed placeholders and exact newline-escape runs passed. The quoted existing menu root and unchanged Android/Paint tokens were checked.
- All 463 prior entries and their original bytes per locale are preserved. Each resulting catalogue contains 483 entries.
- Per locale, P2 direct coverage increases from 116 to 136 of 305 keys. P0 remains 94/94, P1 remains 249/249 and P3 remains 4/71.
- All 1,276 materialized base files matched the remote Git tree's identities and modes. The 163 unmaterialized research/verification records are preserved through the base tree. Only the two catalogues and this evidence record are intended publication changes.

These are host/structural results, not an Android build, device/rendering or screen-reader run, external CI result, or historical-language specialist certification. No issue1 action was attempted.
