# Latin crop controls

## Scope and review

Five missing Latin strings cover batch cropping, the selected-image group, the cropped-thumbnail description and trim guidance. The canonical wording is in `Paintroid/src/main/res/values-b+la/strings.xml`. Independent review accepted all five unchanged.

Reviewed against the English resources and `AssemblyActivity`, `ImageCropDialog`, `AssemblyThumbnail` and `CropOverlay` consumers. The instructions retain original-edge margins, edge/corner handles, numeric entry below the preview, selected-image scope and unchanged original files. Existing crop plural forms, edge names and unit descriptions remain untouched.

## Verification

- 509 prior typed resources and their attributes preserved; five strings added, yielding 514 typed Latin resources.
- XML, Android escaping, ordered typed arguments, newline escapes and source numerals checked.
- 78 host tests passed; structural validation passed for all 171 offered language options.
- 10 Java resource-render checks passed across English and Latin.
- Base-tree verification checked content hashes and executable modes for all 1,252 materialized files; 213 other entries retained through the base tree.
- Priority coverage: P0 94/94, P1 249/249, P2 167/305 and P3 4/71. There are 205 priority keys still missing in Latin.

## Limits

This is a bounded translation and host-structure review, not Android compilation, AAPT, device, layout, accessibility-runtime, CI or specialist linguistic certification. No issue 1 action was retried.
