# Old English and Old Norse image-loading memory estimates

Base: `f8f72085eca269a7b9970ba6cb7ed837d84cbd1b` on `review/nv-bottom-2038-20261103`.

## Change and context

Add four substantive P2 strings to each catalogue, completing the missing image-resize dialog summaries and the shared canvas/new-image size budget caption. The Android XML remains canonical; no memory calculations or decoder code change.

- Original and copy dimensions remain separate from decoded-image bytes and estimated editing/loading memory.
- The original summary preserves RGBA at 4 bytes per pixel and estimated editing memory without resizing. The copy summary describes decoded memory at the selected size.
- The current budget retains its upper bound in MP and explicitly excludes decoder overhead until that additional usage is counted. It does not promise successful allocation at that bound.
- The copy summary keeps its trailing newline because the dialog appends an existing fit/too-large/decoder-floor message.
- Actual consumers and calculations were inspected in `ImageResizeDialog.kt`, `DimensionControls.kt`, `ImageImport.kt`, `ImageMemoryPolicy.kt` and the dimension dialog in `ClassicPaintActivity.kt`. All direct resource references in the first four files are present after this block: 14, 10, 7 and 2 keys respectively.
- Unused legacy memory captions were not added. Existing sampled-decoding and native-decoder safety explanations remain unchanged.

Independent review accepted all eight strings with an applied Old English clarification expressing decoder memory being counted in addition, avoiding reliance on an ambiguous adjective. Technical vocabulary follows the existing catalogue and is a modern adaptation, not historical computing terminology.

## Verification

- All 78 host tests passed after the final clarification: translation, localized-help, translation-boundary, current-contract, language-note, string-importance, ordinary-priority and recovery suites. Reviewed XML matches the tested bytes.
- All 171 offered options passed structural validation with `require_complete=False`.
- XML parsing, unique typed keys, Android escaping, source attributes, exact indexed argument types/order and newline-escape runs pass. Per locale, nine format arguments and five newline escapes are preserved across these four strings, including the final copy-summary escape.
- Host substitution examples cover original/copy summaries and the appended fit caption. RGBA, 4 bytes per pixel, MP and the two-decimal float formats are retained.
- All 571 prior resources per locale, including the existing plural and its items, are unchanged. Removing the additive fragment restores the original bytes.
- All 1,276 materialized base files match remote blob identities and modes. The 169 unmaterialized research/verification documents are preserved by the base tree. Only the two locale XML files and this evidence record are intended publication changes.
- Per locale: P0 stays 94/94; P1 stays 249/249; P2 rises 216→220/305; P3 stays 12/71. Each catalogue has 575 typed resources: 574 strings and one plural. Counts measure direct presence, not whole-catalogue linguistic certification.

## Limits

No Android build/device, actual memory allocation/decoder execution, text fit, Android runtime formatting, CI or historical-language specialist certification is claimed. No issue1 action was attempted.
