# Image formats

AN Paint edits one opaque 8-bit RGB canvas. Imported transparency is flattened
onto the background colour. File formats do not introduce layers or transparency
controls. Animation, multiple pages/items, HDR editing and preservation of camera
metadata are outside this still-image workflow.

| Format | Open / insert / assembly | Save as | Controls |
|---|---|---|---|
| PNG | Yes | Yes | Lossless |
| JPEG | Yes | Yes | Quality 1–100 |
| JPEG XL | Bundled libjxl | Bundled libjxl | Lossless or quality 1–100 |
| WebP | Android decoder | Bundled libwebp | Lossless or quality 1–100 |
| HEIC | Bundled libheif + libde265 | libheif + Kvazaar | Quality 1–100 |
| AVIF | Bundled libheif + libaom | libheif + libaom | Lossless or quality 1–100 |

The bundled codecs are built from pinned source for the supported Android CPU
architectures. HEIC/AVIF saving does not require a phone-provided encoder. The
primary still image is opened from HEIF containers; auxiliary depth images and
additional collection items are not imported as separate documents. The container
rotation and crop are applied once by libheif.

HEIC/AVIF colour conversion currently uses libheif's NCLX colour information and
sRGB output. Embedded ICC-only profiles have not received a separate conversion
or colour-accuracy verification pass.

WebP's format limit is 16383 pixels per side. The editor's device-dependent memory
budget also applies. A smaller HEIC/AVIF output can still require a large source
image or tile to be decoded; the import estimate includes that native working
memory. Resize choices never alter the original file. Codec failures preserve the
current canvas and do not mark an unsuccessful save as complete.

HEIC/AVIF exports use image grids when needed to bound individual encoder input
sizes. Applications reading the output must support the standard grid form. All
encoders operate on still, opaque pixels; lossless refers to the editor's pixel
values, not restoration of metadata or higher-precision source data.

The JPEG XL correction streams encoder output and accepts valid input-buffer
requests beyond 2048 pixels. Native regression tests include the formerly failing
2057 × 17 image, the corresponding tall image, a 2065 × 2049 image, lossless crop
checks, lossy encoding and exhausted-memory recovery.

Full dependency notices and exact source locators are available in Help and in
`Paintroid/src/main/assets/legal/`. Fetch scripts under `tools/` reproduce each
native source revision; the build does not download precompiled codec binaries.

The Kvazaar source receives a documented mutex-lifetime correction in
`tools/fetch_heif_sources.py`: optional RD logging mutexes are destroyed only
after successful initialization, and their state is cleared on close. This fixes
the Android FORTIFY abort reproduced when encoding successive HEIC grid tiles.
It does not alter compression algorithms. The patched source and its notice are
included in the offline source bundle.

Implementation and tests in this file describe the intended local.17 build.
Consult `HANDOFF.md` and `verification/` for the verification actually completed
for a delivered APK, including the distinction between emulator and physical
phone checks.
