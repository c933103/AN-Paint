# JPEG XL correction and lossy-test review

Recorded 12 September 2026.

The 2057 × 17 encoding failure was an integration defect. With an input callback
but `JxlEncoderProcessOutput`, libjxl 0.12.0 calls `CopyBuffers()` and requests the
whole image at once. AN Paint rejected that valid rectangle above 2048 pixels.
The bridge now streams input and output, validates actual image bounds, and
writes through bounded buffers using `pwrite64`, including interrupted/partial
write handling. Memory limits still apply.

In [CI run 34685806408](https://github.com/c933103/AN-Paint/actions/runs/34685806408),
the original boundary case, portrait equivalent, 2065 × 2049 pixel-exact lossless
round trip, boundary crop, native memory exhaustion/retry, and other JPEG XL
checks passed. The remaining failure was a newly written lossy test's arbitrary
maximum difference of 12 in each sRGB channel.

An independent host reproduction with stock libjxl 0.7 through FFmpeg, without
AN Paint's bridge, gives the same failure. The 3073 × 65 fixture is
`RGB(x*255/(width-1), y*255/(height-1), 128)`, using integer division. Encoding
with `-c:v libjxl -effort 3 -distance 1` and decoding with FFmpeg changes pixel
(160,48) from **(13,191,128) to (0,192,128)**. Its red-channel difference is 13,
but its CIE76 colour difference is approximately **0.956**. Whole-image RGB mean
absolute differences are **(1.621, 0.631, 1.033)**.

[libjxl's API](https://libjxl.readthedocs.io/en/latest/api_encoder.html#c.JxlEncoderSetFrameDistance)
defines lossy quality through a perceptual Butteraugli target. Quality 90 maps to
distance 1; it does not impose a maximum error in individual gamma-encoded sRGB
channels. A per-channel bound was therefore the wrong test of this contract.

The test intentionally keeps quality 90 and the same two long-image fixtures.
It now checks CIE76 colour differences at the same sample positions using
AndroidX `ColorUtils`: mean ≤ 1.5 and maximum ≤ 5. These are regression bounds
for this fixture, not a claimed universal guarantee for JPEG XL or a substitute
for Butteraugli. The independent host results are:

| Fixture | Sampled mean CIE76 | Sampled maximum CIE76 |
|---|---:|---:|
| 3073 × 65 | 1.0470 | 3.1194 |
| 65 × 3073 | 0.8305 | 2.4511 |

Both pass the revised checks. Dimension checks, opaque pixels and all exact
lossless per-pixel checks remain. No codec setting or production code was
changed to accommodate the lossy test. The host reproduction uses an older
independent codec. [CI run 34686571856](https://github.com/c933103/AN-Paint/actions/runs/34686571856)
subsequently passed the revised test with the actual Android libjxl 0.12.0 build,
along with all 18 native codec/font tests and seven installed-app tests. That
run's later ARMv7 AVIF compilation failure was separate from the JPEG XL tests;
the final release report identifies the fully verified universal APK.
