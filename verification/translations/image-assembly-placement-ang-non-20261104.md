# Image assembly placement: Old English and Old Norse

Base: `a437ba22f5f0d0521aeb57e4f9dccc377b808ef7` on `review/nv-bottom-2038-20261103`.

Added 24 missing strings each to `values-b+ang` and `values-b+non`. This block covers image-assembly titles, placed/unplaced states, drag and snap instructions, exact X/Y placement, and workspace viewing. Canonical wording remains in the Android resources; this record does not duplicate the translations as approval fixtures.

## Context and review

The source consumers checked were `AssemblyActivity.kt`, `AssemblyCanvas.kt`, `AssemblyPlacementDialog.kt` and `ImageAssembly.kt`.

- Dragging a thumbnail places an imported image; existing images can be moved. Right attachment aligns upper edges; lower attachment aligns left edges. The drag-data label describes an image for the assembly, not a completed export.
- Exact positioning sets the selected image's top-left corner. Both axes use whole pixels from zero, with inclusive input bounds 0–2147483647. Other images retain their positions. Overlap is explicitly permitted, and later-imported images are drawn above earlier images. The canvas expands while crops and image sizes remain unchanged.
- Unplace removes an image from the workspace, without describing deletion of a source file or removal from the assembly's source list. View fit and pinch instructions preserve the distinction between view scale and image/output dimensions.
- Dynamic counts distinguish imported images from placed images. Thumbnail accessibility retains filename, placement state, width and height in the original argument order.

Independent semantic and linguistic review accepted all 48 strings, including the applied Old English nominative-plural correction `sniðunga`. Existing catalogue terminology and script were retained. The Old English exact-position caption uses the functional description “position by pixel count.” The Norse precision adjective is attested in [Cleasby–Vigfusson, nákvæmr](https://norroen.info/dct/cleasby/n.html). Computing compounds are catalogue adaptations, not claims of historical computing terminology.

## Validation and coverage

- All 78 repository host tests passed after final review.
- Structural validation passed for all 171 offered language options.
- Both XML files parse, contain unique names, preserve source attributes, and pass Android escaping and ordered typed-placeholder checks. Newline escapes, X/Y identifiers, numeric bounds and the 20-image header limit were retained.
- All 439 prior entries per locale and their original bytes remain unchanged; the resulting catalogues contain 463 entries each.
- Per locale, P2 direct coverage rises from 96 to 116 of 305 keys; P3 rises from 0 to 4 of 71. The four P3 strings are related drag, thumbnail, pinch and view-fit hints included to keep this workflow coherent. P0 remains 94/94 and P1 remains 249/249.
- All 1,276 materialized base files matched remote Git blob identities and modes. The 162 unmaterialized research/verification records were retained through the base tree. The intended publication changes are the two catalogue files and this evidence record only.

These results are host and structural checks, not an Android build, device/rendering run, external CI result, or historical-language specialist certification. No issue1 action was attempted.
