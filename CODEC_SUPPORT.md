# Image formats

AN Paint edits one opaque 8-bit RGB canvas. Opening an image composites its
transparency onto the selected background colour; inserting an image keeps an
internal floating mask and composites onto the existing canvas pixels when
committed. Assembly output composites onto white. File formats do not introduce
layers or transparency controls. Animation, multiple pages/items, HDR editing
and preservation of camera metadata are outside this still-image workflow.

| Format | Open / insert / assembly | Save as | Controls |
|---|---|---|---|
| PNG | Yes | Yes | Lossless |
| JPEG | Yes | Yes | Quality 1–100 |
| JPEG XL | Bundled libjxl | Bundled libjxl | Lossless or quality 1–100 |
| WebP | Android decoder | Bundled libwebp | Lossless or quality 1–100 |
| HEIC | Bundled libheif + libde265 | libheif + Kvazaar | Quality 1–100 |
| AVIF | Bundled libheif + libaom | libheif + libaom | Lossless or quality 1–100 |
| BMP | Android decoder | Uncompressed 24-bit RGB | Exact RGB pixels; larger files |
| GIF | Android decoder; first frame | Single indexed frame, at most 256 colours | Optional Floyd–Steinberg dithering |

File > Save as opens one panel for all eight formats. Choose a filename and
format, then set quality, lossless mode or GIF dithering where applicable before
opening Android's destination picker. The filename extension follows format
changes. Save and share uses the same options, writes the selected destination,
then invokes sharing with that format. Save uses the current export format and
opens the destination picker directly.

BMP output is uncompressed 24-bit RGB with standard row padding. GIF builds an
adaptive palette: images with at most 256 unique RGB colours preserve those
colours; larger colour sets are quantized, optionally with Floyd–Steinberg
dithering. GIF's format limit is 65,535 pixels per side; the device memory budget
also applies. GIF export writes one still frame and animated GIF import opens
the first frame. BMP/GIF encoders are original AN Paint code, not another native
codec dependency. They add no layers, editable transparency or animation timeline.

The bundled codecs are built from pinned source for the supported Android CPU
architectures. HEIC/AVIF saving does not require a phone-provided encoder. The
primary still image is opened from HEIF containers; auxiliary depth images and
additional collection items are not imported as separate documents. The container
rotation and crop are applied once by libheif.

HEIC/AVIF imports preserve native 10/12-bit RGB samples while libheif applies
container rotation/crop and converts YCbCr using the source NCLX matrix/range.
AN Paint then uses skcms for ICC/primary/transfer conversion before producing
8-bit sRGB. Embedded ICC takes precedence over NCLX colour primaries/transfer;
NCLX is still needed for YCbCr decoding. A digest-checked libheif patch preserves
NCLX passthrough metadata after RGB layout conversion, including codec-bitstream
profiles with no container `colr` property. Invalid or unsupported profiles fail
visibly instead of silently being interpreted as sRGB.

PQ and HLG HDR are converted to a 203 cd/m² SDR target using the bundled JPEG XL
Rec.2408 tone mapper and gamut mapping. PQ uses absolute ST 2084 luminance; HLG
uses the BT.2100 1,000 cd/m² reference-display OOTF, with luminance calculated
after primary conversion so Display-P3 HLG is handled correctly. Source peak selection prefers
MaxCLL, then mastering-display maximum luminance. When those are absent, PQ
uses 10,000 cd/m² and HLG uses 1,000 cd/m². Linear-light HEIF tagged with a source
peak above 255 cd/m² is also tone-mapped. This produces an SDR rendition; it
cannot preserve HDR brightness/headroom in the editor or its exported images,
and tone-mapped appearance depends on the source metadata and target display.

Transparency remains unassociated through colour conversion (premultiplied
source samples are first unassociated). Only the final temporary Android bitmap
is premultiplied. Opening/assembly can therefore composite onto the chosen
background; inserting can composite onto existing canvas pixels without dark
transparent fringes. Alpha controls are not reintroduced into the editor.

Synthetic AVIF regression fixtures cover 10-bit linear, PQ, HLG, Display-P3 NCLX,
ICC-only Display-P3 and fractional alpha. Their generator and source samples are
under `tools/generate_heif_colour_fixtures.py`; the tests use independent colour
references and verify crop/alpha behaviour as well as tonal ordering.

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

JPEG XL HDR imports decode floating-point source samples before explicit transfer,
primary and tone conversion. This also covers non-XYB lossless streams, where the
initial built-in conversion path produced incorrect PQ levels. The bridge uses a
bounded pixel callback rather than allocating another full floating-point image.
Regression fixtures include actual 10-bit PQ/HLG, 16-bit linear SDR/HDR, ICC,
fractional alpha, XYB and crop/resize across callback boundaries.

PNG, JPEG and WebP embedded RGB/gray ICC profiles use the same bundled colour
management. A private decode copy strips colour tags before conversion, preventing
the Android decoder from converting twice. PNG metadata precedence is cICP, ICC,
sRGB, then gAMA/cHRM. On Android 8/API 26 and later, 16-bit PNG samples use an F16
intermediate before final quantization. Earlier Android decoders reduce the
samples to 8 bits first; profile conversion still applies. Unsupported ICC colour
models such as CMYK fail explicitly. Colour metadata is bounded to avoid an
uncontrolled profile allocation.

Ultra HDR JPEG opens its authored SDR base rendition. The gain map is discarded
before editing, because reapplying the original gain map to edited pixels would
produce incorrect output. This does not reproduce the source's HDR display
brightness. Memory admission and resize prompts account for high-precision and
colour-conversion buffers as well as the current document.

Full dependency notices and exact source locators are available in Help and in
`Paintroid/src/main/assets/legal/`. Fetch scripts under `tools/` reproduce each
native source revision; the build does not download precompiled codec binaries.

The Kvazaar source receives a documented mutex-lifetime correction in
`tools/fetch_heif_sources.py`: optional RD logging mutexes are destroyed only
after successful initialization, and their state is cleared on close. This fixes
the Android FORTIFY abort reproduced when encoding successive HEIC grid tiles.
It does not alter compression algorithms. The patched source and its notice are
included in the offline source bundle.

Implementation and tests in this file describe the local.20 source.
Consult `HANDOFF.md` and `verification/` for the verification actually completed
for a delivered APK, including the distinction between emulator and physical
phone checks.
