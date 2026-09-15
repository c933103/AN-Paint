# JPEG XL and image save settings

In 0.0.31, File → Save as contains PNG, JPEG, JPEG XL, WebP, HEIC, AVIF,
BMP, GIF, DIB and TIFF. JPEG XL, WebP and AVIF expose a Lossless checkbox.
Turning it off shows numeric quality (1–100). JPEG and HEIC expose quality;
TIFF exposes lossless Deflate compression and GIF exposes palette dithering.
PNG, BMP and DIB have no lossy quality control. File → Export as contains only
ICO, ASCII art and Base64 text. Sharing retains all formats.

File → Save reuses the last successful Save as destination, file name, format
and settings, including after draft recovery. Quality 100 alone is not the
JPEG XL lossless mode. The checkbox passes `lossless=true` through ImageExporter
and JxlCodec to `JxlEncoderSetFrameLossless(true)` and distance zero, using the
original colour profile. No codec implementation changed in 0.0.31.

The released 0.0.29 codec passed native Android 30 and 35 tests comparing every
opaque RGB pixel after encoding and decoding, including 2057×17, 17×2057 and
2065×2049 images spanning the chunk boundaries. Evidence:
[release build 34914389654](https://github.com/c933103/AN-Paint/actions/runs/34914389654).

Version 0.0.30 adds an installed-app check of the complete File → Save as →
JPEG XL workflow: select the format in the real dialog, write through Android's
content resolver, reopen the file with the packaged decoder and compare all
49,601 RGB pixels of a 257×193 pattern. It then edits a pixel, invokes File → Save,
checks that no new destination picker was requested, and compares every pixel
again. Only the external file picker is replaced with a controlled test result.
Both save operations and the native lossless/chunk-boundary tests passed on
Android API 30 and 35 in [release run 34945326732](https://github.com/c933103/AN-Paint/actions/runs/34945326732).
The release verification JSON records the exact test names and report hashes.

Lossless here means exact preservation of AN Paint's opaque, 8-bit sRGB canvas
pixels. Imported images may already have been resized, flattened or converted
to that canvas representation. This does not preserve arbitrary source metadata,
original HDR samples, layers or an original JPEG's byte stream.

Version 0.0.31's visible lossless checkbox, Save as/Save round trip, and lossy
JPEG XL/AVIF quality controls passed on both platforms in [release run 34979038050](https://github.com/c933103/AN-Paint/actions/runs/34979038050).
