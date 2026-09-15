# JPEG XL lossless verification

File → Save as → JPEG XL uses lossless encoding. File → Save reuses that file's
format, lossless setting and destination. File → Export as → JPEG XL uses lossy
quality settings; quality 100 by itself is not the lossless Save as path.

`SaveOptionsDialog` forces lossless mode for Save as. `ImageExporter` passes the
setting to the packaged `JxlCodec` JNI implementation, which sets
`uses_original_profile`, `JxlEncoderSetFrameLossless(true)` and distance zero.

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
The workflow's actual pass/fail result is recorded with the release evidence.

Lossless here means exact preservation of AN Paint's opaque, 8-bit sRGB canvas
pixels. Imported images may already have been resized, flattened or converted
to that canvas representation. This does not preserve arbitrary source metadata,
original HDR samples, layers or an original JPEG's byte stream.
