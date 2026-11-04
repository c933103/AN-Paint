# Latin image format controls and diagnostics

## Scope and review

Twenty-three missing Latin strings cover ICO, TIFF, Base64 and ASCII controls and explanations; BMP, DIB and GIF size diagnostics; colour-profile conversion guidance; and save-format captions. The canonical wording is in `Paintroid/src/main/res/values-b+la/strings.xml`. Independent review accepted all entries unchanged.

Reviewed against English resources and `SaveOptionsDialog`, `IcoCodec`, `TextImageCodec`, `BitmapFileCodec`, `DibCodec` and `TiffCodec`. The wording preserves exact ICO sizes, directory/image dimension mismatch, proportions on a transparent square, the Base64 prefix and recovery distinction, GIF's per-side bound, BMP/DIB header and size distinctions, 24-bit RGB, ASCII character width and inversion, and conditional lossless TIFF compression. Retained format-specific captions and the tagged-colour warning were translated without declaring them unused. The JPEG XL caption matches the existing generic lossless caption.

## Verification

- 514 prior typed resources and attributes preserved; 23 strings added, yielding 537 typed Latin resources.
- XML, Android escaping, ordered typed arguments, newline escapes and source numerals checked.
- 78 host tests passed; structural validation passed for all 171 offered language options.
- 46 Java resource-render checks passed across English and Latin.
- Base-tree verification checked content hashes and executable modes for all 1,252 materialized files; 214 other entries retained through the base tree.
- Priority coverage: P0 94/94, P1 249/249, P2 185/305 and P3 9/71. There are 182 priority keys still missing in Latin.

## Limits

This is a bounded translation and host-structure review, not Android compilation, AAPT, device, layout, accessibility-runtime, CI or specialist linguistic certification. No issue 1 action was retried.
