# Image formats

AN Paint edits one opaque 8-bit RGB canvas. Opening an image composites its
transparency onto the selected background colour; inserting an image keeps an
internal floating mask and composites onto the existing canvas pixels when
committed. Assembly output composites onto white. File formats do not introduce
layers or transparency controls. PDF and TIFF imports select one page for raster
editing. Animation, multipage document editing, HDR editing and preservation of
camera metadata remain outside this still-image workflow.

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
| DIB | Validated packed DIB wrapped privately for Android decoding | Packed 24-bit RGB DIB | Uncompressed; no BMP file header |
| TIFF (`.tif`, `.tiff`) | Bundled libtiff; page selector | One opaque 8-bit RGB page | Lossless Deflate or uncompressed |
| ICO | Largest PNG or classic DIB icon entry | One PNG icon entry | 16, 24, 32, 48, 64, 128 or 256 px square; aspect preserved |
| Base64 text (`.txt`) | Raw Base64 or image data URI, decoded before normal import | Lossless PNG in a Base64 data URI | Exact PNG pixels; larger than binary PNG |
| ASCII art (`.txt`) | Not an image import format | Plain text rendition | 40–240 columns; invert light/dark |
| PDF | Android PdfRenderer; page selector | Not offered | Rasterizes the chosen page at 144 dpi; resize when needed |

File > Save as opens one panel for all thirteen export formats. Choose a filename and
format, then set quality, lossless mode, GIF dithering, TIFF compression, icon size
or ASCII width/inversion where applicable before
opening Android's destination picker. The filename extension follows format
changes. Save and share uses the same options, writes the selected destination,
then invokes sharing with that format. Save uses the current export format and
opens the destination picker directly.

BMP output is uncompressed 24-bit RGB with standard row padding. GIF builds an
adaptive palette: images with at most 256 unique RGB colours preserve those
colours; larger colour sets are quantized, optionally with Floyd–Steinberg
dithering. GIF's format limit is 65,535 pixels per side; the device memory budget
also applies. GIF export writes one still frame and animated GIF import opens
the first frame. BMP V4/V5 colour metadata and GIF application extensions are
inspected before decoding. Ordinary untagged BMP/GIF and explicitly sRGB BMP are
supported. Calibrated, linked-profile or embedded-profile BMP, and ICC-tagged GIF,
are rejected with a clear conversion message; their profiles are not converted.
Convert those inputs to sRGB PNG using a colour-managed editor first. The metadata
checks follow the [BMP V5 colour-space fields](https://learn.microsoft.com/en-us/windows/win32/api/wingdi/ns-wingdi-bitmapv5header)
and [ICC.1:2010 Annex B.5](https://www.color.org/specification/ICC1v43_2010-12.pdf).
BMP/DIB/GIF encoders are original AN Paint code, not another native
codec dependency. They add no layers, editable transparency or animation timeline.

## DIB and TIFF (local.22)

DIB import recognizes packed OS/2 and Windows headers (12, 40, 52, 56, 108 and
124 bytes), palette-based 1/4/8-bit pixels, 16/24/32-bit pixels, top-down and
bottom-up rows, RGB/bitfields and RLE4/RLE8. A scoped private BMP wrapper supplies
the file header needed by Android; the original remains unchanged and temporary
files are removed after success or failure. Conventional BMP files named `.dib`
also remain readable through signature detection. Export produces a true packed
24-bit DIB without the 14-byte BMP file header; use BMP when another app requires
that header. External Windows palette handles and JPEG/PNG-compressed DIBs are
not supported. The existing BMP colour-profile restrictions also apply to DIB.
The parser validates masks, palette bounds, dimensions, scanline sizes and RLE
runs before platform decoding. Layout follows Microsoft's
[BITMAPINFOHEADER](https://learn.microsoft.com/en-us/windows/win32/api/wingdi/ns-wingdi-bitmapinfoheader)
and [BITMAPV5HEADER](https://learn.microsoft.com/en-us/windows/win32/api/wingdi/ns-wingdi-bitmapv5header).

TIFF uses [libtiff 4.7.2](https://libtiff.gitlab.io/libtiff/) and pinned JPEG support.
A preview and page-number selector open any selected page of classic TIFF or
BigTIFF in either byte order, including
strips, tiles, contiguous or separate sample planes, and all eight orientations.
Supported integer samples include bilevel/palette/grayscale and 8/16-bit RGB,
with associated or unassociated alpha. Compression support includes None, LZW,
Deflate, PackBits, CCITT and supported JPEG RGB/grayscale/YCbCr. Supported embedded
RGB/grayscale ICC profiles are converted before the final 8-bit sRGB quantization.
Unsupported colour models/profiles fail visibly rather than silently changing
their meaning. CMYK, Lab, floating-point/log samples and non-JPEG YCbCr are outside
this decoder's current scope. Up to 4,096 pages are supported; cyclic, broken or
excessive directory chains are rejected before selection. Multipage editing and
saving are not added: opening chooses one page, and saving writes that edited page.

TIFF export writes one classic-TIFF page of opaque 8-bit RGB, with optional
lossless Deflate compression. Both settings preserve the editor's RGB pixels.
The export uses a private temporary file and replaces its destination only after
successful encoding. Import memory estimates account for native strip/tile and
codec work as well as the output; reducing the output does not promise that every
source image will fit the device's budget. Crop/resize and assembly use the same
colour/orientation handling as ordinary opening and insertion.

## PDF, icons and text (local.22)

PDF opens through Android's [PdfRenderer](https://developer.android.com/reference/android/graphics/pdf/PdfRenderer)
on API 21 and newer. The selector shows a preview and accepts a page number, with
previous/next controls. It is shared by opening, insertion and assembly. Assembly
stores the page index with the original source and keeps it through crop, undo,
reopening and output. One PDF point becomes two pixels (144 dpi); page text and
vectors become raster pixels on white. Crop rendering targets the requested region
directly. PDFs needing a password are rejected with an explanation. Files up to
512 MiB, up to 4,096 pages and page dimensions up to 500,000 points are admitted
subject to the device memory budget. PDFium's internal allocations cannot be
strictly capped through Android's API; the importer reserves native headroom and
accounts for the source file as well as the output bitmap.

ICO opens the largest supported icon entry, with up to 256 pixels per side.
PNG entries use the shared colour-aware importer; classic 1/4/8/16/24/32-bit DIB
entries apply XOR pixels, the AND mask and legacy alpha rules. Export produces one
PNG-compressed ICO entry, fitting the canvas into the chosen square without
stretching and using transparent padding. ICO is a resized export: it does not
mark the full drawing saved or allow an outstanding replace/close action to discard
that drawing. Save a full-size PNG or another full-image format too.

Base64 import accepts a supported-image payload encoded as raw Base64 or an
`image/...;base64,` data URI, with whitespace. It streams a strict decode into a
private file before image, page and animation inspection; malformed and nonimage
payloads fail without replacing an existing destination. Export streams a lossless
PNG into `data:image/png;base64,...` text. No clipboard size limit is involved.
All provider copies and decoded Base64 payloads are limited to 512 MiB.

ASCII art is a visual text export, not an editable image format. It samples
luminance into a fixed character ramp, with 40–240 columns and optional inversion.
Rows account for a typical 2:1 monospaced character cell; the appearance depends
on the viewer's font. The output is capped at 4 MiB. Exporting it leaves the drawing
unsaved and does not continue a pending destructive replacement.

## Animated image warning

GIF, APNG and animated WebP containers are inspected before import. When multiple
frames are present, a warning asks whether to open a still image or cancel. GIF,
WebP and ordinary APNG import the first/default frame. APNG can have a separate
poster image; that case explicitly warns that the default poster is imported.
The warning also applies to images decoded from Base64 and images added to assembly.
A bounded metadata scan reports a lower-bound count when an exact count is not
available. If the scan limit is reached before animation can be determined, an
uncertainty warning still asks before opening a still image. Export remains
still-image only; no animation timeline is introduced.

## Remaining formats

The common raster interchange formats are covered, including AVIF which was
already present before local.22. SVG is the most useful next import candidate for
illustrations and logos, but would need a vector renderer and a raster-size choice.
Layered PSD, OpenRaster and Krita projects need a deliberate flattening workflow
or a layer-capable editor; labelling them fully supported in this single-canvas
app would be misleading. Camera RAW and floating-point EXR are specialist workflows
with colour/development requirements, rather than missing everyday paint exports.
These formats are not included in this build. The assessment follows the
[SVG specification](https://www.w3.org/TR/SVG2/Overview.html),
[Adobe PSD/PSB specification](https://www.adobe.com/devnet-apps/photoshop/fileformatashtml/)
and [OpenRaster file layout](https://www.openraster.org/baseline/file-layout-spec.html).

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

Full dependency notices and exact source locators are available in File > About and in
`Paintroid/src/main/assets/legal/`. Fetch scripts under `tools/` reproduce each
native source revision; the build does not download precompiled codec binaries.

The Kvazaar source receives a documented mutex-lifetime correction in
`tools/fetch_heif_sources.py`: optional RD logging mutexes are destroyed only
after successful initialization, and their state is cleared on close. This fixes
the Android FORTIFY abort reproduced when encoding successive HEIC grid tiles.
It does not alter compression algorithms. The patched source and its notice are
included in the offline source bundle.

Implementation and tests in this file describe the local.22 source.
Consult `HANDOFF.md` and `verification/` for the verification actually completed
for a delivered APK, including the distinction between emulator and physical
phone checks.
