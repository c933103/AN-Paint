# Synthetic JPEG XL colour fixtures

These images contain only explicitly specified constant test pixels. They were
generated for AN Paint with `tools/generate_jxl_colour_fixtures.py`, licensed
AGPL-3.0-or-later with the project. There is no third-party photograph or artwork.
Base64 is used only to preserve the exact binary files through source publishing.

| File | Actual encoded precision/profile | Purpose |
| --- | --- | --- |
| linear16 | 16-bit linear sRGB | Transfer conversion before 8-bit quantization |
| linear16-hdr | 16-bit linear sRGB, 1000-nit intensity target | Linear HDR mapped to the same SDR range as PQ |
| p3-icc16 | 16-bit P3/D65, embedded gamma-2.2 ICC | ICC primaries and transfer conversion |
| p3-icc-alpha16 | Same ICC, 16-bit RGB and alpha | Alpha 0, 0.25, 0.5 and 1 remains available for background compositing |
| pq10 | 10-bit BT.2020/PQ, 1000-nit mastering peak | BT.2408 mapping into a 203-nit SDR range; distinct highlights |
| pq10-xyb | Same source, lossy XYB internal encoding | Equivalent colours through the alternate JPEG XL decoding path |
| pq10-alpha | 10-bit PQ and alpha | HDR conversion precedes Android alpha premultiplication |
| pq10-chunks | 10-bit PQ, 1031-pixel row | Crop/resizing across bounded float conversion chunks |
| hlg10 | 10-bit BT.2020/HLG, 1000-nit source target | HLG OETF/reference OOTF then BT.2408 mapping into the same SDR target |

The native Android tests inspect the actual bitstream bit depth. Expected RGB
values are derived from the specified source values, P3-to-sRGB matrix, IEC sRGB
transfer curve, ST 2084 PQ and BT.2408/HLG equations. They are not obtained by
running the production decoder and saving its output as the expectation.

SDR JPEG XL import uses the pinned library's CMS followed by 8-bit SDR output.
For HDR, it requests floating point pixels in the original profile, converts the
transfer/primaries explicitly and applies the shared BT.2408 mapping into a
203-nit SDR target. This avoids a libjxl 0.12.0 pipeline defect where the built-in
tone-mapping stage uses the destination transfer function on non-XYB source
pixels. The test's 1-nit PQ input exposed that defect: RGB 88 instead of RGB 15.
Alpha is converted to Android's premultiplied representation
after colour conversion; the editor subsequently composites onto its opaque
background. This is SDR import conversion, not preservation of an HDR document.

Primary implementation/API references:
- https://libjxl.readthedocs.io/en/latest/api_decoder.html#_CPPv435JxlDecoderSetDesiredIntensityTargetP10JxlDecoderf
- https://github.com/libjxl/libjxl/blob/a7a9c787341cf703dede03c2009fa460cae5e5df/lib/jxl/render_pipeline/stage_tone_mapping.cc
- https://github.com/libjxl/libjxl/blob/a7a9c787341cf703dede03c2009fa460cae5e5df/lib/jxl/cms/tone_mapping.h
